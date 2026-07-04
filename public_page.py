from fastapi.responses import HTMLResponse
from urllib.parse import quote

def get_sub_page_html(api_url: str, title: str, subtitle: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>{quote(title)} · VaslZone</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
:root{{--bg:#050504;--bg2:#0a0a08;--bg3:#11110d;--card:#0d0d0a;--card2:#141410;--card3:#1a1a15;--border:rgba(255,215,0,0.08);--border2:rgba(255,215,0,0.30);--accent:#FFD700;--accent2:#FFC107;--accent3:#FFE44D;--text:#F5F5DC;--text2:#C8C8A0;--text3:#6B6B40;--green:#66BB6A;--green-bg:rgba(102,187,106,0.10);--red:#EF5350;--red-bg:rgba(239,83,80,0.10);--shadow:0 8px 32px rgba(0,0,0,0.6);--radius:16px}}
html,body{{height:100%}}
body{{font-family:Vazirmatn,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;overflow-x:hidden}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 80% 35% at 50% -8%,rgba(255,215,0,0.04),transparent 65%),radial-gradient(ellipse 50% 25% at 20% 100%,rgba(255,215,0,0.02),transparent),var(--bg);z-index:0;pointer-events:none}}
.grd-fx{{position:fixed;inset:0;background-image:linear-gradient(rgba(255,215,0,0.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,215,0,0.015) 1px,transparent 1px);background-size:44px 44px;z-index:0;pointer-events:none}}
.orb{{position:fixed;border-radius:50%;filter:blur(100px);z-index:0;pointer-events:none;animation:fl 10s ease-in-out infinite}}
.o1{{width:350px;height:350px;background:rgba(255,215,0,0.03);top:-100px;right:-80px}}
.o2{{width:300px;height:300px;background:rgba(255,215,0,0.02);bottom:-80px;left:-100px;animation-delay:5s}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-20px)}}}}
.wrap{{position:relative;z-index:10;max-width:580px;margin:0 auto;padding:16px 14px 48px}}
.header{{text-align:center;padding:28px 0 8px;position:relative}}
.header::after{{content:'';position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:40px;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);border-radius:2px}}
.ch-avatar{{width:74px;height:74px;border-radius:22px;margin:0 auto 14px;background:linear-gradient(145deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:34px;color:#000;box-shadow:0 0 0 3px rgba(255,215,0,0.12),0 12px 32px rgba(255,215,0,0.10);position:relative;overflow:hidden;transition:transform .3s}}
.ch-avatar:hover{{transform:scale(1.04)}}
.ch-name{{font-size:18px;font-weight:800;color:var(--text);letter-spacing:-.02em}}
.ch-sub{{font-size:10px;color:var(--text3);margin-top:4px;letter-spacing:.15em;text-transform:uppercase;font-weight:500}}
.ch-link{{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--accent);text-decoration:none;font-weight:600;margin-top:8px;padding:5px 14px;border-radius:20px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.12);transition:.2s}}
.ch-link:hover{{background:rgba(255,215,0,0.18);border-color:rgba(255,215,0,0.25)}}
.info-card{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:20px 22px;margin-top:18px;margin-bottom:14px;position:relative;overflow:hidden;transition:border-color .2s}}
.info-card:hover{{border-color:var(--border2)}}
.info-card::before{{content:'';position:absolute;top:-60px;left:-60px;width:160px;height:160px;background:radial-gradient(circle,rgba(255,215,0,0.05),transparent 70%);pointer-events:none}}
.info-eyebrow{{font-size:9.5px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.info-name{{font-size:20px;font-weight:800;color:var(--text);margin-bottom:4px;letter-spacing:-.01em}}
.info-desc{{font-size:12px;color:var(--text2);line-height:1.8}}
.stats-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px}}
.stat-box{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:15px 14px;text-align:center;transition:.2s}}
.stat-box:hover{{border-color:var(--border2);transform:translateY(-1px)}}
.stat-box .sl{{font-size:8px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px}}
.stat-box .sv{{font-size:20px;font-weight:800;color:var(--accent);line-height:1;letter-spacing:-.01em}}
.stat-box .ss{{font-size:9px;color:var(--text3);margin-top:6px;display:flex;align-items:center;justify-content:center;gap:4px}}
.dot{{width:5px;height:5px;border-radius:50%;display:inline-block;animation:pl 2s infinite}}
@keyframes pl{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}
.dot.g{{background:var(--green)}}
.section-title{{font-size:11px;font-weight:800;color:var(--text3);text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;display:flex;align-items:center;gap:7px}}
.section-title i{{font-size:14px;color:var(--accent)}}
.cfg-list{{display:flex;flex-direction:column;gap:10px}}
.cfg-card{{background:var(--card2);border:1px solid var(--border);border-radius:16px;padding:16px 18px;transition:all .2s;position:relative;overflow:hidden}}
.cfg-card:hover{{border-color:var(--border2)}}
.cfg-card::after{{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--green);border-radius:0 3px 3px 0}}
.cfg-card.inactive::after{{background:var(--red)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:11px;flex-wrap:wrap}}
.cfg-label-wrap{{flex:1;min-width:0}}
.cfg-label{{font-size:14px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:6px}}
.cfg-proto{{font-size:8.5px;padding:2px 8px;border-radius:5px;font-weight:700;display:inline-block;margin-top:4px}}
.pc-ws{{background:rgba(255,215,0,0.10);color:var(--accent)}}
.pc-xhttp{{background:rgba(255,215,0,0.07);color:var(--accent3)}}
.cfg-status-pill{{font-size:9px;padding:4px 10px;border-radius:20px;font-weight:700;display:flex;align-items:center;gap:4px;white-space:nowrap;flex-shrink:0}}
.cfg-status-pill.on{{background:var(--green-bg);color:var(--green)}}
.cfg-status-pill.off{{background:var(--red-bg);color:var(--red)}}
.usage-area{{margin-bottom:10px}}
.usage-text{{font-size:10px;color:var(--text3);display:flex;justify-content:space-between;margin-bottom:5px}}
.usage-text span b{{color:var(--text2);font-weight:700}}
.bar{{height:5px;border-radius:4px;background:rgba(255,215,0,0.06);overflow:hidden}}
.bar-fill{{height:100%;border-radius:4px;transition:width .6s ease;position:relative;overflow:hidden}}
.bar-fill::after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.12),transparent);width:40%;animation:sh 2s linear infinite}}
@keyframes sh{{0%{{transform:translateX(-120%)}}100%{{transform:translateX(280%)}}}}
.remaining-tag{{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;padding:3px 10px;border-radius:6px;margin-top:6px}}
.remaining-tag.ok{{background:var(--green-bg);color:var(--green)}}
.remaining-tag.warn{{background:rgba(255,215,0,0.10);color:var(--accent)}}
.remaining-tag.danger{{background:var(--red-bg);color:var(--red)}}
.server-section{{margin-top:14px;padding-top:14px;border-top:1px solid var(--border)}}
.server-title{{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.08em;margin-bottom:9px;display:flex;align-items:center;gap:6px}}
.server-title i{{color:var(--accent);font-size:13px}}
.server-row{{background:var(--card3);border:1px solid var(--border);border-radius:11px;padding:10px 13px;display:flex;align-items:center;gap:8px;margin-bottom:7px;transition:.15s}}
.server-row:hover{{border-color:var(--border2)}}
.server-row .ip-text{{flex:1;font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent3);word-break:break-all;line-height:1.6;min-width:0;direction:ltr;text-align:left}}
.server-row .ip-label{{font-size:9px;color:var(--text3);white-space:nowrap;margin-left:4px}}
.copy-btn{{font-family:inherit;font-size:10px;font-weight:700;padding:6px 12px;border-radius:8px;cursor:pointer;border:none;display:flex;align-items:center;gap:4px;transition:.15s;white-space:nowrap;flex-shrink:0}}
.copy-btn.g{{background:var(--accent);color:#000;box-shadow:0 3px 10px rgba(255,215,0,0.20)}}
.copy-btn.g:hover{{filter:brightness(1.15);transform:translateY(-1px)}}
.copy-all-bar{{display:flex;align-items:center;gap:10px;background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(255,193,7,0.04));border:1px solid rgba(255,215,0,0.12);border-radius:14px;padding:14px 16px;margin-bottom:14px;flex-wrap:wrap}}
.copy-all-text{{flex:1;min-width:150px}}
.copy-all-title{{font-size:12px;font-weight:700;color:var(--text);display:flex;align-items:center;gap:5px}}
.copy-all-sub{{font-size:9.5px;color:var(--text3);margin-top:3px}}
.copy-all-btn{{font-family:inherit;font-size:11.5px;font-weight:800;padding:9px 18px;border-radius:10px;cursor:pointer;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#000;border:none;display:flex;align-items:center;gap:6px;transition:.15s;box-shadow:0 4px 14px rgba(255,215,0,0.20)}}
.copy-all-btn:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(255,215,0,0.30)}}
.footer{{text-align:center;padding:24px 0 8px;font-size:9px;color:var(--text3)}}
.footer a{{color:var(--accent);font-weight:700;text-decoration:none;transition:.15s}}
.footer a:hover{{color:var(--accent3);text-decoration:underline}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(50px);background:var(--card2);border:1px solid var(--border);color:var(--text);border-radius:12px;padding:10px 20px;font-size:12px;font-weight:600;opacity:0;transition:all .3s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:7px;box-shadow:0 8px 32px rgba(0,0,0,0.5)}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(102,187,106,0.25);background:rgba(102,187,106,0.10);color:var(--green)}}
.empty-state{{text-align:center;padding:70px 20px}}
.empty-state i{{font-size:40px;color:var(--text3);display:block;margin:0 auto 14px}}
.loading{{text-align:center;padding:70px 20px}}
.loading i{{font-size:40px;color:var(--accent);display:block;margin:0 auto 14px;animation:spin 1s linear infinite}}
.loading p{{font-size:12px;color:var(--text3)}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@media(max-width:500px){{.stats-row{{grid-template-columns:1fr 1fr}}.stats-row .stat-box:nth-child(3){{grid-column:1/-1}}.copy-all-bar{{flex-direction:column;align-items:stretch;text-align:center}}.copy-all-btn{{justify-content:center}}.cfg-head{{flex-direction:column;align-items:flex-start}}.wrap{{padding:12px 10px 36px}}}}
@media(max-width:380px){{.stats-row{{grid-template-columns:1fr}}.server-row{{flex-wrap:wrap}}}}
</style></head><body>
<div class="bg-fx"></div><div class="grd-fx"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="toast" id="toast"></div>
<div class="wrap">
  <div class="header">
    <div class="ch-avatar"><i class="ti ti-bolt"></i></div>
    <div class="ch-name">VaslZone</div>
    <div class="ch-sub">SUBSCRIPTION</div>
    <a class="ch-link" href="https://t.me/VaslZone" target="_blank"><i class="ti ti-brand-telegram"></i> @VaslZone</a>
  </div>
  <div id="root">
    <div class="loading"><i class="ti ti-loader-2"></i><p>در حال دریافت اطلاعات...</p></div>
  </div>
  <div class="footer">کانال رسمی: <a href="https://t.me/VaslZone" target="_blank">@VaslZone</a> · v9.3</div>
</div>
<script>
const API_URL = "{api_url}";
let allLinks = [];
function fmtB(b){{if(!b||b===0)return"0 B";if(b<1024)return b+" B";if(b<1048576)return(b/1024).toFixed(1)+" KB";if(b<1073741824)return(b/1048576).toFixed(2)+" MB";if(b<1099511627776)return(b/1073741824).toFixed(2)+" GB";return(b/1099511627776).toFixed(2)+" TB"}}
function esc(s){{return String(s||"").replace(/[&<>"']/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}})[c])}}
function protoBadge(p){{return p&&p.includes("xhttp")?'<span class="cfg-proto pc-xhttp">XHTTP</span>':'<span class="cfg-proto pc-ws">VLESS · WS</span>'}}
async function loadData(){{try{{const r=await fetch(API_URL);if(!r.ok)throw new Error();return await r.json()}}catch(e){{return null}}}}
function render(d){{
  if(!d||!d.links||!d.links.length){{document.getElementById("root").innerHTML='<div class="empty-state"><i class="ti ti-link-off"></i><p style="font-size:12px;color:var(--text3)">کانفیگی یافت نشد</p></div>';return}}
  allLinks=d.links;let h="";
  const active=d.links.filter(l=>l.active).length;
  const totalUsed=d.links.reduce((s,l)=>s+(l.used_bytes||0),0);
  h+="<div class='info-card'><div class='info-eyebrow'><i class='ti ti-folder'></i> "+(d.links.length===1?"کانفیگ":"گروه دسترسی")+"</div><div class='info-name'>"+esc(d.name||"VaslZone")+"</div>"+(d.desc?"<div class='info-desc'>"+esc(d.desc)+"</div>":"")+"</div>";
  h+="<div class='stats-row'><div class='stat-box'><div class='sl'>وضعیت</div><div class='sv' style='font-size:"+(d.links.length===1?"16":"20")+"px'>"+(d.links.length===1?(d.links[0].active?"فعال":"غیرفعال"):active+" / "+d.links.length)+"</div><div class='ss'></div></div><div class='stat-box'><div class='sl'>مصرف کل</div><div class='sv' style='font-size:17px'>"+fmtB(totalUsed)+"</div><div class='ss'>از مجموع</div></div><div class='stat-box'><div class='sl'>اتصالات زنده</div><div class='sv'>"+(d.active_connections||0)+"</div><div class='ss'><span class='dot g'></span> آنلاین</div></div></div>";
  if(d.links.length>1)h+="<div class='copy-all-bar'><div class='copy-all-text'><div class='copy-all-title'><i class='ti ti-copy'></i> کپی همه</div><div class='copy-all-sub'>یکبار کلیک</div></div><button class='copy-all-btn' onclick='copyAll()'><i class='ti ti-clipboard-copy'></i> کپی ("+active+")</button></div>";
  h+="<div class='section-title'><i class='ti ti-link'></i> کانفیگ‌ها</div><div class='cfg-list'>";
  for(let i=0;i<d.links.length;i++){{
    const l=d.links[i];const pct=l.limit_bytes>0?Math.min(100,(l.used_bytes/l.limit_bytes)*100):0;
    const bc=pct>90?"var(--red)":pct>70?"var(--accent)":"var(--green)";
    const remain=l.limit_bytes>0?Math.max(0,l.limit_bytes-l.used_bytes):-1;
    const rf=remain<0?"∞":fmtB(remain);const rc=remain<0?"ok":(remain<1048576?"danger":(remain<1073741824?"warn":"ok"));
    h+="<div class='cfg-card"+(l.active?"":" inactive")+"'><div class='cfg-head'><div class='cfg-label-wrap'><div class='cfg-label'>"+esc(l.label)+"</div><div>"+protoBadge(l.protocol)+"</div></div><span class='cfg-status-pill "+(l.active?"on":"off")+"'>"+(l.active?"<i class='ti ti-circle-check'></i> فعال":"<i class='ti ti-circle-x'></i> غیرفعال")+"</span></div>";
    h+="<div class='usage-area'><div class='usage-text'><span>مصرف: <b>"+l.used_fmt+"</b></span><span>سهمیه: <b>"+l.limit_fmt+"</b></span></div><div class='bar'><div class='bar-fill' style='width:"+pct+"%;background:"+bc+"'></div></div><span class='remaining-tag "+rc+"'><i class='ti "+(remain<0?"ti-infinity":"ti-database")+"'></i> "+(remain<0?"نامحدود":"باقی: "+rf)+"</span></div>";
    const lines=l.vless_link?l.vless_link.split("\\n").filter(x=>x):[];
    if(lines.length>0){{
      h+="<div class='server-section'><div class='server-title'><i class='ti ti-server-2'></i> سرورهای دسترسی</div>";
      for(let j=0;j<lines.length;j++){{
        const si=lines[j].match(/@([^:?]+)/);h+="<div class='server-row'><span class='ip-label'>#"+(j+1)+"</span><span class='ip-text'>"+esc(lines[j])+"</span><button class='copy-btn g' onclick='copyText(allLinks["+i+"].vless_lines["+j+"])'><i class='ti ti-copy'></i> کپی</button></div>"
      }}
      h+="</div>"
    }}
    h+="</div>"
  }}
  h+="</div>";document.getElementById("root").innerHTML=h
}}
function copyText(t){{navigator.clipboard.writeText(t).then(()=>{{const t=document.getElementById("toast");t.textContent="✅ کپی شد";t.className="toast show ok";setTimeout(()=>t.classList.remove("show"),1800)}})}}
function copyAll(){{const t=allLinks.map(l=>l.vless_link||"").filter(x=>x).join("\\n");if(!t)return;navigator.clipboard.writeText(t).then(()=>{{const t=document.getElementById("toast");t.textContent="✅ همه کپی شد";t.className="toast show ok";setTimeout(()=>t.classList.remove("show"),1800)}})}}
(async function init(){{const d=await loadData();if(d){{d.links.forEach(l=>l.vless_lines=l.vless_link?l.vless_link.split("\\n").filter(x=>x):[]);render(d)}}else document.getElementById("root").innerHTML='<div class="empty-state"><i class="ti ti-alert-circle" style="color:var(--red)"></i><p style="font-size:12px;color:var(--text3)">خطا در بارگذاری</p></div>'}})();
</script></body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    return get_sub_page_html(
        api_url=f"/api/public/sub/{uuid_key}",
        title="VaslZone Group",
    )


def get_single_sub_page_html(uuid: str) -> str:
    return get_sub_page_html(
        api_url=f"/api/public/sub-single/{uuid}",
        title="VaslZone Config",
    )
