import asyncio
import json
import os
import hashlib
import secrets
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VaslZone-Gateway")
IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="VaslZone Gateway", docs_url=None, redoc_url=None)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": os.environ.get("SECRET_KEY", secrets.token_urlsafe(32)),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "rvg_state.json"
SAVE_LOCK = asyncio.Lock()

connections: dict = {}
stats = {"total_bytes": 0, "total_requests": 0, "total_errors": 0, "start_time": time.time()}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()
RESELLERS: dict = {}
RESELLERS_LOCK = asyncio.Lock()
GLOBAL_SETTINGS = {"ips": [], "port": None}
PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one")
DEFAULT_PROTOCOL = "vless-ws"

SESSION_COOKIE = "rvg_session"
SESSION_TTL = 60 * 60 * 24 * 7
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "123456"))}

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({"kind": kind, "level": level, "message": message, "time": datetime.now().isoformat()})

async def load_state():
    global LINKS, AUTH, SUBS, GLOBAL_SETTINGS, RESELLERS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            RESELLERS.update(data.get("resellers", {}))
            if "global_settings" in data: GLOBAL_SETTINGS.update(data["global_settings"])
            if "password_hash" in data: AUTH["password_hash"] = data["password_hash"]
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs, {len(RESELLERS)} resellers")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {"links": dict(LINKS), "subs": dict(SUBS), "resellers": dict(RESELLERS),
                    "global_settings": dict(GLOBAL_SETTINGS), "password_hash": AUTH["password_hash"],
                    "saved_at": datetime.now().isoformat()}
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

async def create_session(role="admin", user_id="admin") -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = {"exp": time.time() + SESSION_TTL, "role": role, "user_id": user_id}
    return token

async def get_session_data(token: str | None) -> dict | None:
    if not token: return None
    async with SESSIONS_LOCK:
        s = SESSIONS.get(token)
        if not s: return None
        if isinstance(s, float):
            if s < time.time(): SESSIONS.pop(token, None); return None
            return {"exp": s, "role": "admin", "user_id": "admin"}
        if s["exp"] < time.time(): SESSIONS.pop(token, None); return None
        return s

async def destroy_session(token: str | None):
    if token:
        async with SESSIONS_LOCK: SESSIONS.pop(token, None)

async def require_auth(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"] != "admin": raise HTTPException(status_code=401, detail="unauthorized")
    return s["user_id"]

async def require_reseller_auth(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"] not in ["admin", "reseller"]: raise HTTPException(status_code=401, detail="unauthorized")
    return s

@app.on_event("startup")
async def startup():
    global http_client
    http_client = httpx.AsyncClient(limits=httpx.Limits(max_connections=500, max_keepalive_connections=100),
                                    timeout=httpx.Timeout(30.0, connect=10.0), follow_redirects=True)
    await load_state()
    log_activity("system", "سرور راه‌اندازی شد", "ok")
    logger.info(f"VaslZone Gateway started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client: await http_client.aclose()

def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

async def fetch_ip_flag(ip: str) -> str:
    if not ip: return ""
    try:
        resp = await http_client.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=2.0)
        cc = resp.json().get("countryCode")
        if cc and len(cc) == 2: return chr(ord(cc[0]) + 127397) + chr(ord(cc[1]) + 127397)
    except: pass
    return ""

def _format_vless_uri(uuid: str, ip: str, port: int, remark: str, protocol: str, host: str) -> str:
    if protocol == "vless-ws":
        params = {"encryption": "none", "security": "tls", "type": "ws", "host": host, "path": f"/ws/{uuid}", "sni": host, "fp": "chrome", "alpn": "http/1.1"}
    else:
        mode = protocol.replace("xhttp-", "")
        params = {"encryption": "none", "security": "tls", "type": "xhttp", "mode": mode, "host": host, "path": f"/xhttp-siz10/{mode}/{uuid}", "sni": host, "fp": "chrome", "alpn": "h2,http/1.1"}
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{ip}:{port}?{query}#{quote(remark)}"

def generate_vless_links(link: dict, uuid: str, host: str) -> list:
    protocol = link.get("protocol", DEFAULT_PROTOCOL)
    is_personal = link.get("is_personal", False)
    ips = link.get("ips") or []
    if not is_personal and GLOBAL_SETTINGS.get("ips"):
        ips = GLOBAL_SETTINGS["ips"]
    if not ips: ips = [host]
    port = link.get("port")
    if not is_personal and GLOBAL_SETTINGS.get("port"): port = GLOBAL_SETTINGS["port"]
    if not port: port = 443
    return [_format_vless_uri(uuid, ip, port, f"VaslZone-{link['label']}" if len(ips)==1 else f"VaslZone-{link['label']}-{ip}", protocol, host) for ip in ips]

def uptime() -> str:
    s = int(time.time() - stats["start_time"])
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"

def parse_size_to_bytes(v: float, unit: str) -> int:
    u = unit.upper()
    if u == "GB": return int(v * 1024**3)
    if u == "MB": return int(v * 1024**2)
    if u == "KB": return int(v * 1024)
    return int(v)

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp: return False
    try: return datetime.now() > datetime.fromisoformat(exp)
    except: return False

def is_link_allowed(link: dict | None) -> bool:
    if not link: return False
    if not link.get("active", True): return False
    if is_link_expired(link): return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb: return False
    return True

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd: return fwd.split(",")[0].strip()
    r = request.headers.get("x-real-ip")
    if r: return r.strip()
    return request.client.host if request.client else "نامشخص"

async def check_reseller_capacity(rid: str, new_bytes: int):
    if new_bytes == 0: raise HTTPException(400, "نماینده نمی‌تواند کانفیگ نامحدود بسازد")
    async with RESELLERS_LOCK:
        res = RESELLERS.get(rid)
        if not res or not res.get("active", True): raise HTTPException(403, "نماینده غیرفعال است")
        allocated = sum(d.get("limit_bytes",0) for d in LINKS.values() if d.get("creator_id")==rid)
        if allocated + new_bytes > res.get("total_bytes", 0): raise HTTPException(400, "حجم مجاز تمام شده")

_default_link_created = False
async def ensure_default_link():
    global _default_link_created
    if _default_link_created: return
    async with LINKS_LOCK:
        if not any(l.get("is_default") for l in LINKS.values()):
            uid = hashlib.sha256(f"default{CONFIG['secret']}".encode()).hexdigest()
            uid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
            if uid not in LINKS:
                LINKS[uid] = {"label": "لینک پیش‌فرض", "limit_bytes": 0, "used_bytes": 0,
                    "created_at": datetime.now().isoformat(), "active": True, "expires_at": None,
                    "note": "", "is_default": True, "sub_id": None, "protocol": DEFAULT_PROTOCOL,
                    "ips": [], "port": None, "is_personal": False}
    asyncio.create_task(save_state())
    _default_link_created = True

@app.get("/")
async def root():
    return {"service": "VaslZone Gateway", "version": "9.2", "status": "active", "channel": "https://t.me/VaslZone"}

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}

@app.get("/sub/{uuid}")
async def subscription_single(uuid: str):
    import base64
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link or not is_link_allowed(link): raise HTTPException(404, "not found")
    lines = generate_vless_links(link, uuid, get_host())
    return Response(content=base64.b64encode("\n".join(lines).encode()).decode(), media_type="text/plain",
                    headers={"profile-title": quote(link["label"]), "support-url": "https://t.me/VaslZone"})

@app.get("/sub-all")
async def subscription_all(_=Depends(require_auth)):
    import base64
    host = get_host()
    lines = []
    async with LINKS_LOCK:
        for uid, d in LINKS.items():
            if is_link_allowed(d): lines.extend(generate_vless_links(d, uid, host))
    return Response(content=base64.b64encode("\n".join(lines).encode()).decode(), media_type="text/plain")

@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
        if not sub: raise HTTPException(404)
        if sub.get("password_hash") and hash_password(request.query_params.get("pw","")) != sub["password_hash"]:
            raise HTTPException(403, "wrong password")
    host = get_host()
    lines = []
    async with LINKS_LOCK:
        for lid in sub.get("link_ids", []):
            link = LINKS.get(lid)
            if link and is_link_allowed(link): lines.extend(generate_vless_links(link, lid, host))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain",
                    headers={"profile-title": quote(sub["name"]), "support-url": "https://t.me/VaslZone", "profile-update-interval": "12"})
# ── Sub Groups ────────────────────────────────────────────────────────────────
@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {"name": name, "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key, "created_at": datetime.now().isoformat(), "link_ids": []}
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» ساخته شد", "ok")
    host = get_host()
    return {"sub_id": sub_id, **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}", "sub_url": f"https://{host}/sub-group/{uuid_key}"}

@app.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    host = get_host()
    async with SUBS_LOCK: snap_subs = dict(SUBS)
    async with LINKS_LOCK: snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = sum(1 for lid in link_ids if is_link_allowed(snap_links.get(lid)))
        total_used = sum(snap_links[lid].get("used_bytes", 0) for lid in link_ids if lid in snap_links)
        result.append({"sub_id": sid, **s, "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "links_count": len(link_ids), "active_count": active_count,
            "total_used_bytes": total_used, "total_used_fmt": fmt_bytes(total_used),
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}"})
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS: raise HTTPException(404, "sub not found")
        s = SUBS[sub_id]
        if "name" in body: s["name"] = str(body["name"])[:60]
        if "desc" in body: s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body: s["link_ids"] = list(body["link_ids"])
    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS: raise HTTPException(404, "sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id: link["sub_id"] = None
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» حذف شد", "warn")
    return {"ok": True, "deleted": sub_id}

@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    link_id = str(body.get("link_id", ""))
    action = str(body.get("action", "add"))
    async with SUBS_LOCK:
        if sub_id not in SUBS: raise HTTPException(404)
        s = SUBS[sub_id]
        ids = s.setdefault("link_ids", [])
        if action == "add":
            if link_id not in ids: ids.append(link_id)
        else:
            if link_id in ids: ids.remove(link_id)
    async with LINKS_LOCK:
        if link_id in LINKS: LINKS[link_id]["sub_id"] = sub_id if action == "add" else None
    asyncio.create_task(save_state())
    return {"ok": True}

# ── Global IP Settings ────────────────────────────────────────────────────────
@app.get("/api/settings/global-ips")
async def get_global_ips(_=Depends(require_auth)):
    return dict(GLOBAL_SETTINGS)

@app.post("/api/settings/global-ips")
async def update_global_ips(request: Request, _=Depends(require_auth)):
    body = await request.json()
    GLOBAL_SETTINGS["ips"] = [ip.strip() for ip in body.get("ips", []) if ip.strip()]
    GLOBAL_SETTINGS["port"] = int(body["port"]) if body.get("port") else None
    asyncio.create_task(save_state())
    log_activity("system", "تنظیمات IP سراسری بروز شد", "info")
    return {"ok": True, "settings": dict(GLOBAL_SETTINGS)}

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    pw = str(body.get("password", ""))
    if hash_password(pw) == AUTH["password_hash"]:
        token = await create_session("admin", "admin")
        log_activity("auth", f"ورود ادمین از {ip}", "ok")
        resp = JSONResponse({"ok": True, "role": "admin"})
        resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
        return resp
    async with RESELLERS_LOCK:
        for rid, res in RESELLERS.items():
            if res.get("active", True) and res.get("password_hash") == hash_password(pw):
                token = await create_session("reseller", rid)
                log_activity("auth", f"ورود نماینده {res['name']} از {ip}", "ok")
                resp = JSONResponse({"ok": True, "role": "reseller"})
                resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
                return resp
    log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
    raise HTTPException(401, "رمز عبور اشتباه است")

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    return {"authenticated": bool(s), "role": s["role"] if s else None}

@app.post("/api/change-password")
async def api_change_password(request: Request, _=Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(400, "رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4: raise HTTPException(400, "رمز باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK: SESSIONS.clear()
    await save_state()
    log_activity("auth", "رمز عبور تغییر کرد", "ok")
    return {"ok": True}

# ── Stats ─────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK: snap = dict(LINKS)
    return {"active_connections": len(connections), "total_traffic_mb": round(stats["total_bytes"]/1024**2, 2),
        "total_requests": stats["total_requests"], "total_errors": stats["total_errors"],
        "uptime": uptime(), "hourly": dict(hourly_traffic), "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap), "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS), "resellers_count": len(RESELLERS)}

@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK: snap = dict(LINKS)
    grouped = {}
    for cid, c in connections.items():
        ip = c.get("ip", "نامشخص")
        link = snap.get(c.get("uuid"))
        label = link.get("label") if link else "نامشخص"
        if ip not in grouped:
            grouped[ip] = {"ip": ip, "sessions": 0, "bytes": 0, "labels": set(),
                "transports": set(), "connected_at": c.get("connected_at")}
        g = grouped[ip]
        g["sessions"] += 1
        g["bytes"] += c.get("bytes", 0)
        g["labels"].add(label)
        g["transports"].add(c.get("transport", "vless-ws"))
    result = [{"ip": k, "sessions": v["sessions"], "labels": sorted(v["labels"]),
        "label": " · ".join(sorted(v["labels"])), "transports": sorted(v["transports"]),
        "bytes": v["bytes"], "bytes_fmt": fmt_bytes(v["bytes"]),
        "connected_at": v["connected_at"]} for k, v in grouped.items()]
    result.sort(key=lambda x: x["connected_at"] or "", reverse=True)
    return {"connections": result, "count": len(result), "raw_count": len(connections)}
# ── Links Management ──────────────────────────────────────────────────────────
@app.post("/api/links")
async def create_link(request: Request):
    s = await require_reseller_auth(request)
    body = await request.json()
    label = (body.get("label") or "لینک جدید").strip()[:60]
    lv = float(body.get("limit_value") or 0)
    lim = 0 if lv <= 0 else parse_size_to_bytes(lv, body.get("limit_unit") or "GB")
    exp_days = int(body.get("expires_days") or 0)
    exp_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    ips = [ip.strip() for ip in body.get("ips", []) if ip.strip()]
    port = int(body["port"]) if body.get("port") else None
    is_personal = bool(body.get("is_personal", False))
    sub_id = body.get("sub_id")
    protocol = body.get("protocol") or DEFAULT_PROTOCOL
    if s["role"] == "reseller":
        await check_reseller_capacity(s["user_id"], lim)
        is_personal = True
    flag = await fetch_ip_flag(ips[0]) if ips else ""
    label = f"{label} {flag}" if flag else label
    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {"label": label, "limit_bytes": lim, "used_bytes": 0,
            "created_at": datetime.now().isoformat(), "active": True,
            "expires_at": exp_at, "note": str(body.get("note",""))[:200],
            "is_default": False, "sub_id": sub_id, "protocol": protocol,
            "ips": ips, "port": port, "is_personal": is_personal, "creator_id": s["user_id"]}
        if sub_id:
            async with SUBS_LOCK:
                if sub_id in SUBS:
                    ids = SUBS[sub_id].setdefault("link_ids", [])
                    if uid not in ids: ids.append(uid)
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{label}» ساخته شد", "ok")
    host = get_host()
    vlist = generate_vless_links(LINKS[uid], uid, host)
    return {"uuid": uid, **LINKS[uid], "vless_link": "\n".join(vlist), "sub_url": f"https://{host}/sub/{uid}"}

@app.post("/api/links/bulk")
async def create_links_bulk(request: Request):
    s = await require_reseller_auth(request)
    body = await request.json()
    count = min(max(int(body.get("count", 1)), 1), 100)
    base = (body.get("label") or "Bulk").strip()[:40]
    lv = float(body.get("limit_value") or 0)
    lim = 0 if lv <= 0 else parse_size_to_bytes(lv, body.get("limit_unit") or "GB")
    exp_days = int(body.get("expires_days") or 0)
    exp_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    ips = [ip.strip() for ip in body.get("ips", []) if ip.strip()]
    port = int(body["port"]) if body.get("port") else None
    is_personal = bool(body.get("is_personal", False))
    sub_id = body.get("sub_id")
    protocol = body.get("protocol") or DEFAULT_PROTOCOL
    if s["role"] == "reseller":
        await check_reseller_capacity(s["user_id"], lim * count)
        is_personal = True
    uids = []
    host = get_host()
    for i in range(count):
        tip = ips[i % len(ips)] if ips else ""
        flag = await fetch_ip_flag(tip) if tip else ""
        lb = f"{base}-{i+1}{' '+flag if flag else ''}"
        uid = generate_uuid()
        async with LINKS_LOCK:
            LINKS[uid] = {"label": lb, "limit_bytes": lim, "used_bytes": 0,
                "created_at": datetime.now().isoformat(), "active": True,
                "expires_at": exp_at, "note": "", "is_default": False,
                "sub_id": sub_id, "protocol": protocol,
                "ips": [tip] if tip else [], "port": port,
                "is_personal": is_personal, "creator_id": s["user_id"]}
            if sub_id:
                async with SUBS_LOCK:
                    if sub_id in SUBS:
                        ids = SUBS[sub_id].setdefault("link_ids", [])
                        if uid not in ids: ids.append(uid)
        uids.append(uid)
    asyncio.create_task(save_state())
    log_activity("link", f"{count} کانفیگ {base} ساخته شد", "ok")
    all_v = []
    for uid in uids:
        all_v.extend(generate_vless_links(LINKS[uid], uid, host))
    sub_url = ""
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                uk = SUBS[sub_id].get("uuid_key", "")
                if uk: sub_url = f"https://{host}/sub-group/{uk}"
    return {"ok": True, "count": count, "sub_url": sub_url, "vless_bulk": "\n".join(all_v)}

@app.get("/api/links")
async def list_links(request: Request):
    s = await require_reseller_auth(request)
    host = get_host()
    async with LINKS_LOCK:
        result = []
        for uid, d in LINKS.items():
            if s["role"] == "reseller" and d.get("creator_id") != s["user_id"]: continue
            vlist = generate_vless_links(d, uid, host)
            result.append({"uuid": uid, **d, "expired": is_link_expired(d),
                "vless_link": "\n".join(vlist), "sub_url": f"https://{host}/sub/{uid}"})
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request):
    s = await require_reseller_auth(request)
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS: raise HTTPException(404)
        if s["role"] == "reseller" and LINKS[uid].get("creator_id") != s["user_id"]:
            raise HTTPException(403)
        link = LINKS[uid]
        if "active" in body: link["active"] = bool(body["active"])
        if "label" in body: link["label"] = str(body["label"])[:60]
        if "reset_usage" in body and body["reset_usage"]: link["used_bytes"] = 0
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, body.get("limit_unit") or "GB")
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "ips" in body: link["ips"] = [ip.strip() for ip in body.get("ips", []) if ip.strip()]
        if "port" in body: link["port"] = int(body["port"]) if body.get("port") else None
    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, request: Request):
    s = await require_reseller_auth(request)
    async with LINKS_LOCK:
        if uid not in LINKS: raise HTTPException(404)
        if s["role"] == "reseller" and LINKS[uid].get("creator_id") != s["user_id"]:
            raise HTTPException(403)
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]
        if sub_id:
            async with SUBS_LOCK:
                if sub_id in SUBS:
                    ids = SUBS[sub_id].get("link_ids", [])
                    if uid in ids: ids.remove(uid)
    asyncio.create_task(save_state())
    return {"ok": True}

# ── Reseller Management ───────────────────────────────────────────────────────
@app.get("/api/resellers")
async def list_resellers(_=Depends(require_auth)):
    async with RESELLERS_LOCK: sr = dict(RESELLERS)
    async with LINKS_LOCK: sl = dict(LINKS)
    result = []
    for rid, r in sr.items():
        lc = sum(1 for l in sl.values() if l.get("creator_id") == rid)
        al = sum(l.get("limit_bytes",0) for l in sl.values() if l.get("creator_id") == rid)
        tr = sum(l.get("used_bytes",0) for l in sl.values() if l.get("creator_id") == rid)
        result.append({"id": rid, "name": r["name"], "active": r.get("active",True),
            "total_bytes": r.get("total_bytes",0), "total_fmt": fmt_bytes(r.get("total_bytes",0)),
            "allocated_bytes": al, "allocated_fmt": fmt_bytes(al),
            "remaining_bytes": max(0, r.get("total_bytes",0)-al), "remaining_fmt": fmt_bytes(max(0,r.get("total_bytes",0)-al)),
            "traffic_used": tr, "traffic_fmt": fmt_bytes(tr),
            "created_at": r.get("created_at"), "links_count": lc})
    return {"resellers": result}

@app.post("/api/resellers")
async def create_reseller(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = str(body.get("name","")).strip()
    pw = str(body.get("password","")).strip()
    gb = float(body.get("limit_gb") or 0)
    if not name or not pw: raise HTTPException(400, "نام و رمز الزامی است")
    if gb <= 0: raise HTTPException(400, "حجم باید بیشتر از ۰ باشد")
    rid = secrets.token_hex(8)
    async with RESELLERS_LOCK:
        RESELLERS[rid] = {"name": name, "password_hash": hash_password(pw),
            "total_bytes": parse_size_to_bytes(gb, "GB"), "active": True,
            "created_at": datetime.now().isoformat()}
    asyncio.create_task(save_state())
    log_activity("system", f"نماینده «{name}» با {gb}GB ساخته شد", "ok")
    return {"ok": True, "id": rid, "name": name, "limit_gb": gb}

@app.patch("/api/resellers/{rid}")
async def update_reseller(rid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with RESELLERS_LOCK:
        if rid not in RESELLERS: raise HTTPException(404)
        r = RESELLERS[rid]
        if "active" in body: r["active"] = bool(body["active"])
        if "limit_gb" in body:
            r["total_bytes"] = parse_size_to_bytes(float(body["limit_gb"]), "GB")
        if "password" in body and str(body["password"]).strip():
            r["password_hash"] = hash_password(str(body["password"]).strip())
    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/resellers/{rid}")
async def delete_reseller(rid: str, _=Depends(require_auth)):
    async with RESELLERS_LOCK:
        if rid not in RESELLERS: raise HTTPException(404)
        del RESELLERS[rid]
    asyncio.create_task(save_state())
    return {"ok": True}

@app.get("/api/resellers/{rid}/links")
async def reseller_links(rid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        return {"links": [{"uuid": uid, **d} for uid, d in LINKS.items() if d.get("creator_id") == rid]}

# ── VLESS Relay & XHTTP ──────────────────────────────────────────────────────
from relay_vless import websocket_tunnel
from xhttp_siz10 import router as xhttp_router
app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)
app.include_router(xhttp_router)

# ── HTTP Proxy ────────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"): target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        return Response(content=resp.content, status_code=resp.status_code,
            headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(502, detail=f"Proxy error: {exc}")

# ── Public Pages ──────────────────────────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        sub = next(({"sub_id": sid, **s} for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
        if not sub: return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>گروه پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
        if not entry: raise HTTPException(404)
        sid, sub = entry
        if sub.get("password_hash") and hash_password(request.query_params.get("pw","")) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})
    host = get_host()
    async with LINKS_LOCK:
        out = []
        for lid in sub.get("link_ids", []):
            link = LINKS.get(lid)
            if not link: continue
            out.append({"uuid": lid, "label": link["label"], "active": is_link_allowed(link),
                "protocol": link.get("protocol", DEFAULT_PROTOCOL),
                "used_bytes": link.get("used_bytes",0),
                "used_fmt": fmt_bytes(link.get("used_bytes",0)),
                "limit_bytes": link.get("limit_bytes",0),
                "limit_fmt": "∞" if link.get("limit_bytes",0)==0 else fmt_bytes(link["limit_bytes"]),
                "expires_at": link.get("expires_at"),
                "vless_link": "\n".join(generate_vless_links(link, lid, host)),
                "sub_url": f"https://{host}/sub/{lid}"})
        return {"locked": False, "name": sub["name"], "sub_url": f"https://{host}/sub-group/{uuid_key}",
            "total_used_fmt": fmt_bytes(sum(l["used_bytes"] for l in out)), "links": out}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if s and s["role"] == "admin": return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"] != "admin": return RedirectResponse(url="/login")
    await ensure_default_link()
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
