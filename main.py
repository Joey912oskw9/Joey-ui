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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "rvg_state.json"
SAVE_LOCK = asyncio.Lock()

async def load_state():
    global LINKS, AUTH, SUBS, GLOBAL_SETTINGS, RESELLERS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
                data = json.loads(raw)
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
            data = {"links": dict(LINKS), "subs": dict(SUBS), "resellers": dict(RESELLERS), "global_settings": dict(GLOBAL_SETTINGS), "password_hash": AUTH["password_hash"], "saved_at": datetime.now().isoformat()}
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

connections, stats, error_logs, activity_logs, hourly_traffic = {}, {"total_bytes":0,"total_requests":0,"total_errors":0,"start_time":time.time()}, deque(maxlen=50), deque(maxlen=200), defaultdict(int)
http_client = None
LINKS, LINKS_LOCK = {}, asyncio.Lock()
SUBS, SUBS_LOCK = {}, asyncio.Lock()
RESELLERS, RESELLERS_LOCK = {}, asyncio.Lock()
GLOBAL_SETTINGS = {"ips": [], "port": None}
PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one")
DEFAULT_PROTOCOL = "vless-ws"

def log_activity(kind, msg, level="info"):
    activity_logs.append({"kind":kind,"level":level,"message":msg,"time":datetime.now().isoformat()})

SESSION_COOKIE, SESSION_TTL = "rvg_session", 604800

def hash_password(pw):
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "123456"))}
SESSIONS, SESSIONS_LOCK = {}, asyncio.Lock()

async def create_session(role="admin", uid="admin"):
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK: SESSIONS[token] = {"exp":time.time()+SESSION_TTL,"role":role,"user_id":uid}
    return token

async def get_session_data(token):
    if not token: return None
    async with SESSIONS_LOCK:
        s = SESSIONS.get(token)
        if not s: return None
        if isinstance(s, float):
            if s<time.time(): SESSIONS.pop(token,None); return None
            return {"exp":s,"role":"admin","user_id":"admin"}
        if s["exp"]<time.time(): SESSIONS.pop(token,None); return None
        return s

async def destroy_session(token):
    if token: async with SESSIONS_LOCK: SESSIONS.pop(token,None)

async def require_auth(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"]!="admin": raise HTTPException(401)
    return s["user_id"]

async def require_reseller_auth(request: Request):
    s = await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"] not in ["admin","reseller"]: raise HTTPException(401)
    return s

@app.on_event("startup")
async def startup():
    global http_client
    http_client = httpx.AsyncClient(limits=httpx.Limits(max_connections=500), timeout=httpx.Timeout(30.0))
    await load_state()
    log_activity("system","سرور راه‌اندازی شد","ok")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client: await http_client.aclose()

def get_host(): return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])
def generate_uuid():
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
def now_ir(): return datetime.now(IRAN_TZ)

async def fetch_ip_flag(ip):
    if not ip or ":" in ip: return ""
    try:
        r = await http_client.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=2.0)
        cc = r.json().get("countryCode")
        if cc and len(cc)==2: return chr(ord(cc[0])+127397)+chr(ord(cc[1])+127397)
    except: pass
    return ""

def _fmt_vless(uuid, ip, port, remark, protocol, orig):
    if protocol=="vless-ws":
        path=f"/ws/{uuid}"
        p={"encryption":"none","security":"tls","type":"ws","host":orig,"path":path,"sni":orig,"fp":"chrome","alpn":"http/1.1"}
    else:
        mode=protocol.replace("xhttp-","")
        path=f"/xhttp-siz10/{mode}/{uuid}"
        p={"encryption":"none","security":"tls","type":"xhttp","mode":mode,"host":orig,"path":path,"sni":orig,"fp":"chrome","alpn":"h2,http/1.1"}
    q="&".join(f"{k}={quote(str(v))}" for k,v in p.items())
    return f"vless://{uuid}@{ip}:{port}?{q}#{quote(remark)}"

def gen_vless(ld, uuid, host):
    links, proto = [], ld.get("protocol", DEFAULT_PROTOCOL)
    ip = ld.get("ips") or []
    if not ld.get("is_personal") and GLOBAL_SETTINGS.get("ips"): ip=GLOBAL_SETTINGS["ips"]
    if not ip: ip=[host]
    pt = ld.get("port")
    if not ld.get("is_personal") and GLOBAL_SETTINGS.get("port"): pt=GLOBAL_SETTINGS["port"]
    if not pt: pt=443
    for a in ip:
        r = f"VaslZone-{ld['label']}-{a}" if len(ip)>1 else f"VaslZone-{ld['label']}"
        links.append(_fmt_vless(uuid,a,pt,r,proto,host))
    return links

def uptime():
    s=int(time.time()-stats["start_time"])
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"

def p2b(v,u):
    u=u.upper()
    if u=="GB": return int(v*1024**3)
    if u=="MB": return int(v*1024**2)
    if u=="KB": return int(v*1024)
    return int(v)

def is_exp(l):
    e=l.get("expires_at")
    if not e: return False
    try: return datetime.now()>datetime.fromisoformat(e)
    except: return False

def is_ok(l):
    if not l: return False
    if not l.get("active",True): return False
    if is_exp(l): return False
    lb=l.get("limit_bytes",0)
    if lb>0 and l.get("used_bytes",0)>=lb: return False
    return True

def fb(b):
    if b<1024: return f"{b}B"
    if b<1024**2: return f"{b/1024:.0f}KB"
    if b<1024**3: return f"{b/1024**2:.1f}MB"
    return f"{b/1024**3:.2f}GB"

def cip(r):
    f=r.headers.get("x-forwarded-for")
    if f: return f.split(",")[0].strip()
    return r.client.host if r.client else "?"

_created=False
async def deflink():
    global _created
    if _created: return
    async with LINKS_LOCK:
        if not any(l.get("is_default") for l in LINKS.values()):
            uid=hashlib.sha256(f"default{CONFIG['secret']}".encode()).hexdigest()
            uid=f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
            if uid not in LINKS:
                LINKS[uid]={"label":"لینک پیش‌فرض","limit_bytes":0,"used_bytes":0,"created_at":datetime.now().isoformat(),"active":True,"expires_at":None,"note":"","is_default":True,"sub_id":None,"protocol":DEFAULT_PROTOCOL,"ips":[],"port":None,"is_personal":False}
    asyncio.create_task(save_state())
    _created=True

async def chk_cap(rid,n):
    if n==0: raise HTTPException(400,"نمی‌توانید کانفیگ نامحدود بسازید.")
    async with RESELLERS_LOCK:
        r=RESELLERS.get(rid)
        if not r or not r.get("active",True): raise HTTPException(403,"غیرفعال")
        a=0
        async with LINKS_LOCK:
            for d in LINKS.values():
                if d.get("creator_id")==rid: a+=d.get("limit_bytes",0)
        if n>r.get("total_bytes",0)-a: raise HTTPException(400,"حجم درخواستی بیشتر از باقی‌مانده")
@app.get("/")
async def root(): return {"service":"VaslZone Gateway","version":"9.2","status":"active"}

@app.get("/health")
async def health(): return {"status":"ok","connections":len(connections),"uptime":uptime()}

@app.get("/sub/{uuid}")
async def sub_single(uuid: str):
    import base64
    async with LINKS_LOCK:
        l=LINKS.get(uuid)
        if not l or not is_ok(l): raise HTTPException(404)
    h=get_host()
    c=base64.b64encode("\n".join(gen_vless(l,uuid,h)).encode()).decode()
    return Response(content=c,media_type="text/plain",headers={"profile-title":quote(l["label"])})

@app.get("/sub-all")
async def sub_all(_=Depends(require_auth)):
    import base64
    h=get_host();ls=[]
    async with LINKS_LOCK:
        for uid,d in LINKS.items():
            if is_ok(d): ls.extend(gen_vless(d,uid,h))
    return Response(content=base64.b64encode("\n".join(ls).encode()).decode(),media_type="text/plain")

@app.get("/sub-group/{uuid_key}")
async def sub_group(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        s=next((s for s in SUBS.values() if s.get("uuid_key")==uuid_key),None)
        if not s: raise HTTPException(404)
        if s.get("password_hash") and hash_password(request.query_params.get("pw",""))!=s["password_hash"]: raise HTTPException(403)
    h=get_host();ls=[]
    async with LINKS_LOCK:
        for lid in s.get("link_ids",[]):
            l=LINKS.get(lid)
            if l and is_ok(l): ls.extend(gen_vless(l,lid,h))
    return Response(content=base64.b64encode("\n".join(ls).encode()).decode(),media_type="text/plain")

@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body=await request.json()
    sid,uk=generate_uuid(),secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sid]={"name":(body.get("name") or "جدید").strip()[:60],"desc":(body.get("desc") or "").strip()[:200],"password_hash":hash_password(body.get("password","")) if body.get("password") else None,"uuid_key":uk,"created_at":datetime.now().isoformat(),"link_ids":[]}
    asyncio.create_task(save_state())
    h=get_host()
    return {"sub_id":sid,**SUBS[sid],"public_url":f"https://{h}/p/{uk}","sub_url":f"https://{h}/sub-group/{uk}"}

@app.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    h=get_host()
    async with SUBS_LOCK: ss=dict(SUBS)
    async with LINKS_LOCK: sl=dict(LINKS)
    r=[]
    for sid,s in ss.items():
        lids=s.get("link_ids",[])
        r.append({"sub_id":sid,**s,"password_hash":None,"has_password":s.get("password_hash") is not None,"links_count":len(lids),"active_count":sum(1 for lid in lids if is_ok(sl.get(lid))),"total_used_fmt":fb(sum(sl[lid].get("used_bytes",0) for lid in lids if lid in sl)),"public_url":f"https://{h}/p/{s['uuid_key']}","sub_url":f"https://{h}/sub-group/{s['uuid_key']}"})
    r.sort(key=lambda x:x["created_at"],reverse=True)
    return {"subs":r}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body=await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS: raise HTTPException(404)
        s=SUBS[sub_id]
        if "name" in body: s["name"]=str(body["name"])[:60]
        if "desc" in body: s["desc"]=str(body["desc"])[:200]
        if "password" in body: s["password_hash"]=hash_password(str(body["password"]).strip()) if str(body["password"]).strip() else None
        if "link_ids" in body: s["link_ids"]=list(body["link_ids"])
    asyncio.create_task(save_state())
    return {"ok":True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK: del SUBS[sub_id]
    async with LINKS_LOCK:
        for l in LINKS.values():
            if l.get("sub_id")==sub_id: l["sub_id"]=None
    asyncio.create_task(save_state())
    return {"ok":True}

@app.post("/api/login")
async def api_login(request: Request):
    body=await request.json()
    pw=str(body.get("password",""))
    if hash_password(pw)==AUTH["password_hash"]:
        t=await create_session("admin")
        resp=JSONResponse({"ok":True,"role":"admin"})
        resp.set_cookie(SESSION_COOKIE,t,max_age=SESSION_TTL,httponly=True,samesite="lax",path="/")
        return resp
    async with RESELLERS_LOCK:
        for rid,res in RESELLERS.items():
            if res.get("active",True) and res.get("password_hash")==hash_password(pw):
                t=await create_session("reseller",rid)
                resp=JSONResponse({"ok":True,"role":"reseller"})
                resp.set_cookie(SESSION_COOKIE,t,max_age=SESSION_TTL,httponly=True,samesite="lax",path="/")
                return resp
    raise HTTPException(401,"رمز اشتباه")

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp=JSONResponse({"ok":True})
    resp.delete_cookie(SESSION_COOKIE,path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    s=await get_session_data(request.cookies.get(SESSION_COOKIE))
    return {"authenticated":bool(s),"role":s["role"] if s else None}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body=await request.json()
    if hash_password(str(body.get("current_password","")))!=AUTH["password_hash"]: raise HTTPException(400,"غلط")
    new=str(body.get("new_password",""))
    if len(new)<4: raise HTTPException(400,"حداقل ۴ کاراکتر")
    AUTH["password_hash"]=hash_password(new)
    async with SESSIONS_LOCK: SESSIONS.clear();SESSIONS[token]=time.time()+SESSION_TTL
    await save_state()
    return {"ok":True}

@app.get("/api/settings/global-ips")
async def get_global_ips(_=Depends(require_auth)): return GLOBAL_SETTINGS

@app.post("/api/settings/global-ips")
async def update_global_ips(request: Request, _=Depends(require_auth)):
    body=await request.json()
    GLOBAL_SETTINGS["ips"]=[ip.strip() for ip in body.get("ips",[]) if ip.strip()]
    GLOBAL_SETTINGS["port"]=int(body.get("port")) if body.get("port") else None
    asyncio.create_task(save_state())
    return {"ok":True}

@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK: snap=dict(LINKS)
    return {"active_connections":len(connections),"total_traffic_mb":round(stats["total_bytes"]/(1024**2),2),"uptime":uptime(),"links_count":len(snap),"active_links":sum(1 for l in snap.values() if is_ok(l)),"subs_count":len(SUBS),"resellers_count":len(RESELLERS)}

@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK: snap=dict(LINKS)
    g={}
    for cid,c in connections.items():
        ip=c.get("ip","?")
        x=g.setdefault(ip,{"ip":ip,"sessions":0,"bytes":0,"labels":set()})
        x["sessions"]+=1;x["bytes"]+=c.get("bytes",0)
        x["labels"].add(snap.get(c.get("uuid"),{}).get("label","?"))
    return {"connections":sorted([{"ip":k,"sessions":v["sessions"],"label":" - ".join(sorted(v["labels"])),"bytes_fmt":fb(v["bytes"])} for k,v in g.items()],key=lambda x:x["sessions"],reverse=True),"count":len(g)}

@app.post("/api/links")
async def create_link(request: Request):
    s=await require_reseller_auth(request)
    body=await request.json()
    lv=float(body.get("limit_value") or 0)
    lb=0 if lv<=0 else p2b(lv,body.get("limit_unit") or "GB")
    if s["role"]=="reseller": await chk_cap(s["user_id"],lb)
    uid=generate_uuid()
    exp=int(body.get("expires_days") or 0)
    async with LINKS_LOCK:
        LINKS[uid]={"label":(body.get("label") or "جدید").strip()[:60],"limit_bytes":lb,"used_bytes":0,"created_at":datetime.now().isoformat(),"active":True,"expires_at":(datetime.now()+timedelta(days=exp)).isoformat() if exp>0 else None,"note":"","is_default":False,"sub_id":body.get("sub_id"),"protocol":body.get("protocol") or DEFAULT_PROTOCOL,"ips":[ip.strip() for ip in body.get("ips",[]) if ip.strip()],"port":int(body.get("port")) if body.get("port") else None,"is_personal":True,"creator_id":s["user_id"]}
    asyncio.create_task(save_state())
    h=get_host()
    return {"uuid":uid,**LINKS[uid],"vless_link":"\n".join(gen_vless(LINKS[uid],uid,h)),"sub_url":f"https://{h}/sub/{uid}"}

@app.post("/api/links/bulk")
async def create_links_bulk(request: Request):
    s=await require_reseller_auth(request)
    body=await request.json()
    cnt=min(max(int(body.get("count",1)),1),100)
    lv=float(body.get("limit_value") or 0)
    lb=0 if lv<=0 else p2b(lv,body.get("limit_unit") or "GB")
    if s["role"]=="reseller": await chk_cap(s["user_id"],lb*cnt)
    uids,h=[],get_host()
    for i in range(cnt):
        uid=generate_uuid()
        async with LINKS_LOCK:
            LINKS[uid]={"label":f"{(body.get('label') or 'Bulk').strip()[:40]}-{i+1}","limit_bytes":lb,"used_bytes":0,"created_at":datetime.now().isoformat(),"active":True,"expires_at":(datetime.now()+timedelta(days=int(body.get('expires_days') or 0))).isoformat() if int(body.get('expires_days') or 0)>0 else None,"note":"","is_default":False,"sub_id":body.get("sub_id"),"protocol":body.get("protocol") or DEFAULT_PROTOCOL,"ips":[],"port":int(body.get("port")) if body.get("port") else None,"is_personal":True,"creator_id":s["user_id"]}
            if body.get("sub_id"):
                async with SUBS_LOCK:
                    if body["sub_id"] in SUBS:
                        ids=SUBS[body["sub_id"]].setdefault("link_ids",[])
                        if uid not in ids: ids.append(uid)
        uids.append(uid)
    asyncio.create_task(save_state())
    all_vless=[]
    for uid in uids: all_vless.extend(gen_vless(LINKS[uid],uid,h))
    sub_bulk="\n".join([f"https://{h}/sub/{uid}" for uid in uids])
    return {"ok":True,"count":cnt,"created_uids":uids,"sub_bulk":sub_bulk,"vless_bulk":"\n".join(all_vless)}

@app.get("/api/links")
async def list_links(request: Request):
    s=await require_reseller_auth(request)
    h=get_host()
    async with LINKS_LOCK:
        r=[{"uuid":uid,**d,"expired":is_exp(d),"vless_link":"\n".join(gen_vless(d,uid,h)),"sub_url":f"https://{h}/sub/{uid}"} for uid,d in LINKS.items() if s["role"]!="reseller" or d.get("creator_id")==s["user_id"]]
    r.sort(key=lambda x:x["created_at"],reverse=True)
    return {"links":r}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request):
    s=await require_reseller_auth(request)
    body=await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS: raise HTTPException(404)
        l=LINKS[uid]
        if s["role"]=="reseller" and l.get("creator_id")!=s["user_id"]: raise HTTPException(403)
        if "active" in body: l["active"]=bool(body["active"])
        if "label" in body: l["label"]=str(body["label"])[:60]
    asyncio.create_task(save_state())
    return {"ok":True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, request: Request):
    s=await require_reseller_auth(request)
    async with LINKS_LOCK:
        if uid not in LINKS: raise HTTPException(404)
        if s["role"]=="reseller" and LINKS[uid].get("creator_id")!=s["user_id"]: raise HTTPException(403)
        del LINKS[uid]
    asyncio.create_task(save_state())
    return {"ok":True}
# ── Reseller Management ──
@app.post("/api/resellers/{rid}/reset-token")
async def reset_reseller_token(rid: str, _=Depends(require_auth)):
    async with RESELLERS_LOCK:
        if rid not in RESELLERS: raise HTTPException(404)
        RESELLERS[rid]["login_token"]=secrets.token_urlsafe(16)
    asyncio.create_task(save_state())
    return {"ok":True,"login_token":RESELLERS[rid]["login_token"]}

@app.get("/api/resellers")
async def list_resellers(_=Depends(require_auth)):
    h=get_host()
    async with RESELLERS_LOCK: sr=dict(RESELLERS)
    for r in sr.values():
        if not r.get('login_token'): r['login_token']=secrets.token_urlsafe(16); await save_state()
    async with LINKS_LOCK: sl=dict(LINKS)
    r=[]
    for rid,res in sr.items():
        alc=sum(l.get("limit_bytes",0) for l in sl.values() if l.get("creator_id")==rid)
        r.append({"id":rid,"name":res["name"],"active":res.get("active",True),"total_bytes":res.get("total_bytes",0),"total_fmt":fb(res.get("total_bytes",0)),"allocated_bytes":alc,"allocated_fmt":fb(alc),"remaining_bytes":max(0,res.get("total_bytes",0)-alc),"remaining_fmt":fb(max(0,res.get("total_bytes",0)-alc)),"links_count":sum(1 for l in sl.values() if l.get("creator_id")==rid),"login_link":f"https://{h}/r/{res.get('login_token','')}"})
    return {"resellers":r}

@app.post("/api/resellers")
async def create_reseller(request: Request, _=Depends(require_auth)):
    body=await request.json()
    name,pw=str(body.get("name","")).strip(),str(body.get("password","")).strip()
    gb=float(body.get("limit_gb") or 0)
    if not name or not pw: raise HTTPException(400,"نام و رمز الزامی")
    if gb<=0: raise HTTPException(400,"حجم باید بیشتر از ۰")
    rid=secrets.token_hex(8)
    async with RESELLERS_LOCK:
        RESELLERS[rid]={"name":name,"password_hash":hash_password(pw),"total_bytes":p2b(gb,"GB"),"active":True,"login_token":secrets.token_urlsafe(16),"created_at":datetime.now().isoformat()}
    asyncio.create_task(save_state())
    return {"ok":True,"id":rid,"name":name,"limit_gb":gb}

@app.patch("/api/resellers/{rid}")
async def update_reseller(rid: str, request: Request, _=Depends(require_auth)):
    body=await request.json()
    async with RESELLERS_LOCK:
        if rid not in RESELLERS: raise HTTPException(404)
        r=RESELLERS[rid]
        if "name" in body and str(body["name"]).strip(): r["name"]=str(body["name"]).strip()
        if "active" in body: r["active"]=bool(body["active"])
        if "limit_gb" in body: r["total_bytes"]=p2b(float(body["limit_gb"]),"GB")
        if "password" in body and str(body["password"]).strip(): r["password_hash"]=hash_password(str(body["password"]).strip())
    asyncio.create_task(save_state())
    return {"ok":True}

@app.delete("/api/resellers/{rid}")
async def delete_reseller(rid: str, _=Depends(require_auth)):
    async with RESELLERS_LOCK: del RESELLERS[rid]
    asyncio.create_task(save_state())
    return {"ok":True}

def _rp_html(name,ts,us,rs,rg,cnt,pct):
    bar="#EF4444" if pct>90 else "#F59E0B" if pct>70 else "#10B981"
    return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>پنل نماینده</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Tahoma,sans-serif;background:#060f1d;color:#E8F4FF;padding:16px}}
.w{{max-width:450px;margin:auto}}
.h{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.rbox{{background:linear-gradient(135deg,rgba(139,92,246,0.15),rgba(139,92,246,0.05));border:2px solid rgba(139,92,246,0.3);border-radius:16px;padding:20px;text-align:center;margin-bottom:14px}}
.rbox .rl{{font-size:10px;color:#7BAED4;text-transform:uppercase}}
.rbox .rv{{font-size:36px;font-weight:900;color:#E8F4FF;margin:6px 0}}
.c{{background:rgba(10,22,40,0.9);border:1px solid rgba(139,92,246,0.2);border-radius:14px;padding:18px;margin-bottom:12px}}
.g{{display:flex;gap:10px;flex-wrap:wrap}}
.gb{{flex:1;min-width:100px;padding:12px;background:rgba(139,92,246,0.05);border:1px solid rgba(139,92,246,0.15);border-radius:11px;text-align:center}}
.l{{font-size:9px;color:#3D6B8E}}
.v{{font-size:18px;font-weight:800}}
.br{{height:5px;background:rgba(139,92,246,0.1);border-radius:3px;margin:10px 0}}
.bf{{height:100%;border-radius:3px;background:{bar};width:{pct}%}}
.btn{{font-size:11px;padding:7px 14px;border-radius:8px;border:1px solid rgba(139,92,246,0.2);background:transparent;color:#7BAED4;cursor:pointer;font-family:inherit}}
.ft{{text-align:center;padding-top:12px;font-size:9px;color:#3D6B8E}}
</style></head><body><div class="w">
<div class="h"><div><b style="font-size:15px">{name}</b><br><span style="font-size:10px;color:#3D6B8E">نماینده</span></div>
<form action="/api/logout" method="post"><button class="btn" type="submit">خروج</button></form></div>
<div class="rbox"><div class="rl">حجم باقی‌مانده</div><div class="rv">{rg}</div><div class="ru" style="font-size:12px;color:#3D6B8E">گیگابایت</div></div>
<div class="c"><div style="display:flex;justify-content:space-between;font-size:12px;font-weight:700"><span>مصرف: {us}</span><span>از {ts}</span></div>
<div class="br"><div class="bf"></div></div>
<div style="display:flex;justify-content:space-between;font-size:9px;color:#3D6B8E"><span>باقی: {rs}</span><span>{pct}%</span></div></div>
<div class="g"><div class="gb"><div class="l">حجم کل</div><div class="v">{ts}</div></div>
<div class="gb"><div class="l">باقیمانده</div><div class="v" style="color:{bar}">{rs}</div></div>
<div class="gb"><div class="l">کانفیگها</div><div class="v">{cnt}</div></div></div>
<div class="c"><div style="font-size:12px;color:#7BAED4;line-height:2"><b>محدودیتها:</b><br>- حجم کل: {ts}<br>- باقیمانده: {rg} GB<br>- کانفیگ نامحدود: ممنوع</div></div>
<div class="ft">VaslZone Gateway</div></div></body></html>""")

@app.get("/reseller-panel", response_class=HTMLResponse)
async def reseller_panel(request: Request):
    s=await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s or s["role"]!="reseller": return RedirectResponse(url="/login")
    rid=s["user_id"]
    async with RESELLERS_LOCK:
        res=RESELLERS.get(rid)
        if not res or not res.get("active",True):
            await destroy_session(request.cookies.get(SESSION_COOKIE))
            return RedirectResponse(url="/login")
        nm,tot=res["name"],res["total_bytes"]
    async with LINKS_LOCK:
        usd=sum(d.get("used_bytes",0) for d in LINKS.values() if d.get("creator_id")==rid)
        alc=sum(d.get("limit_bytes",0) for d in LINKS.values() if d.get("creator_id")==rid)
        rem=max(0,tot-alc);cnt=sum(1 for d in LINKS.values() if d.get("creator_id")==rid)
    p=int(min(100,usd/tot*100)) if tot>0 else 0
    def _b(x):
        if x<1024: return f"{x}B"
        if x<1024**2: return f"{x/1024:.0f}KB"
        if x<1024**3: return f"{x/1024**2:.1f}MB"
        return f"{x/1024**3:.2f}GB"
    return _rp_html(nm,_b(tot),_b(usd),_b(rem),f"{rem/(1024**3):.3f}",cnt,p)

@app.get("/r/{login_token}")
async def reseller_token_login(login_token: str):
    async with RESELLERS_LOCK:
        for rid,res in RESELLERS.items():
            if res.get("login_token")==login_token and res.get("active",True):
                t=await create_session("reseller",rid)
                resp=RedirectResponse(url="/reseller-panel")
                resp.set_cookie(SESSION_COOKIE,t,max_age=SESSION_TTL,httponly=True,samesite="lax",path="/")
                return resp
    return HTMLResponse("<h2>لینک نامعتبر</h2>",status_code=404)

from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    s=await get_session_data(request.cookies.get(SESSION_COOKIE))
    if s:
        if s["role"]=="admin": return RedirectResponse(url="/dashboard")
        if s["role"]=="reseller": return RedirectResponse(url="/reseller-panel")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    s=await get_session_data(request.cookies.get(SESSION_COOKIE))
    if not s: return RedirectResponse(url="/login")
    if s["role"]=="reseller": return RedirectResponse(url="/reseller-panel")
    await deflink()
    return HTMLResponse(content=DASHBOARD_HTML)

from relay_vless import websocket_tunnel
app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)

from xhttp_siz10 import router as xhttp_router
app.include_router(xhttp_router)

_HOP={"connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}
@app.api_route("/proxy/{target_url:path}",methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"): target_url="https://"+target_url
    try:
        body=await request.body()
        headers={k:v for k,v in request.headers.items() if k.lower() not in _HOP and k.lower()!="host"}
        resp=await http_client.request(method=request.method,url=target_url,headers=headers,content=body)
        stats["total_bytes"]+=len(resp.content)
        return Response(content=resp.content,status_code=resp.status_code)
    except Exception as exc:
        stats["total_errors"]+=1
        raise HTTPException(502)

@app.get("/p/{uuid_key}",response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        s=next(({"sub_id":sid,**s} for sid,s in SUBS.items() if s.get("uuid_key")==uuid_key),None)
        if not s: return HTMLResponse("<h2>NotFound</h2>",status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        e=next(((sid,s) for sid,s in SUBS.items() if s.get("uuid_key")==uuid_key),None)
        if not e: raise HTTPException(404)
        sid,sub=e
        if sub.get("password_hash") and hash_password(request.query_params.get("pw",""))!=sub["password_hash"]:
            return JSONResponse({"locked":True,"name":sub["name"]})
    h=get_host()
    async with LINKS_LOCK:
        lo=[{"uuid":lid,"label":l["label"],"active":is_ok(l),"protocol":l.get("protocol",DEFAULT_PROTOCOL),"used_bytes":l.get("used_bytes",0),"used_fmt":fb(l.get("used_bytes",0)),"limit_bytes":l.get("limit_bytes",0),"limit_fmt":"∞" if l.get("limit_bytes",0)==0 else fb(l["limit_bytes"]),"vless_link":"\n".join(gen_vless(l,lid,h)),"sub_url":f"https://{h}/sub/{lid}"} for lid in sub.get("link_ids",[]) if (l:=LINKS.get(lid))]
        return {"locked":False,"name":sub["name"],"desc":sub.get("desc",""),"links":lo}

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=CONFIG["port"],log_level="info",workers=1)
