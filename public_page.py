from fastapi.responses import HTMLResponse

def get_public_page_html(uuid_key: str) -> str:
    return """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>VaslZone Sub</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#0a0a0f;--bg2:#0f0f18;--card:#111120;--card2:#1a1a30;--border:rgba(255,215,0,0.12);--border2:rgba(255,215,0,0.25);--accent:#FFD700;--accent2:#FFA500;--accent3:rgba(255,215,0,0.08);--gold:#FFD700;--gold2:#DAA520;--text:#F5F5DC;--text2:#BDB76B;--dim:#666633;--green:#32CD32;--red:#FF4444;--amber:#FFA500;--shadow:0 8px 32px rgba(0,0,0,0.6)}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 40% at 50% -5%,rgba(255,215,0,0.06),transparent 70%),var(--bg);z-index:0;pointer-events:none}
.grd{position:fixed;inset:0;background-image:linear-gradient(rgba(255,215,0,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,215,0,0.02) 1px,transparent 1px);background-size:40px 40px;z-index:0;pointer-events:none}
.wrap{position:relative;z-index:10;max-width:520px;margin:0 auto}
.head{text-align:center;padding:28px 0 20px}
.avatar{width:72px;height:72px;border-radius:20px;margin:0 auto 12px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:32px;color:#000;box-shadow:0 8px 24px rgba(255,215,0,0.2),0 0 0 3px rgba(255,215,0,0.08);position:relative;overflow:hidden}
.avatar img{width:100%;height:100%;object-fit:cover}
.name{font-size:20px;font-weight:900;color:var(--text);letter-spacing:-.02em}
.sub{font-size:10px;color:var(--dim);margin-top:4px;letter-spacing:.12em;text-transform:uppercase}
.info{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px 20px;margin-bottom:14px;text-align:center}
.info h2{font-size:15px;font-weight:800;color:var(--accent);margin-bottom:4px}
.info p{font-size:11px;color:var(--text2);line-height:1.8}
.stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
.stat{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:14px 10px;text-align:center}
.stat-l{font-size:8px;color:var(--dim);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px}
.stat-v{font-size:18px;font-weight:800;color:var(--accent)}
.stat-s{font-size:9px;color:var(--text2);margin-top:4px}
.sub-box{background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.sub-box .url{flex:1;font-family:monospace;font-size:9px;color:var(--accent2);word-break:break-all;line-height:1.6;min-width:0}
.sub-box .btn-c{background:var(--accent2);border:none;color:#000;font-size:10px;font-weight:800;padding:7px 12px;border-radius:8px;cursor:pointer;font-family:inherit;white-space:nowrap;transition:.15s}
.sub-box .btn-c:hover{filter:brightness(1.15)}
.config{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px 18px;margin-bottom:10px;position:relative;overflow:hidden}
.config::before{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:.6}
.config-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-wrap:wrap;gap:6px}
.config-label{font-size:12.5px;font-weight:700;color:var(--text)}
.config-badge{font-size:8px;padding:2px 8px;border-radius:4px;font-weight:700;border:1px solid var(--border)}
.config-badge.active{background:rgba(50,205,50,0.12);color:var(--green);border-color:rgba(50,205,50,0.2)}
.config-badge.inactive{background:rgba(255,68,68,0.12);color:var(--red);border-color:rgba(255,68,68,0.2)}
.config-usage{background:rgba(255,255,255,0.04);border-radius:8px;padding:8px 10px;margin-bottom:8px;display:flex;justify-content:space-between;font-size:10px;color:var(--text2)}
.config-usage span span{color:var(--accent2);font-weight:700}
.config-link{background:rgba(0,0,0,0.25);border:1px solid var(--border);border-radius:8px;padding:10px 12px;font-family:monospace;font-size:9px;color:var(--accent2);word-break:break-all;line-height:1.7;margin-bottom:8px;max-height:60px;overflow-y:auto;display:none}
.config-link.show{display:block}
.config-actions{display:flex;gap:6px}
.btn-s{font-size:10px;font-weight:700;padding:7px 12px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text2);cursor:pointer;font-family:inherit;display:flex;align-items:center;gap:4px;transition:.15s;flex:1;justify-content:center}
.btn-s:hover{background:var(--accent3);color:var(--accent);border-color:var(--border2)}
.btn-s.gold{background:var(--accent2);color:#000;border-color:var(--accent2)}
.btn-s.gold:hover{filter:brightness(1.1)}
.empty{text-align:center;padding:50px 20px;color:var(--dim)}
.empty i{font-size:36px;display:block;margin-bottom:10px;color:var(--dim)}
.ft{text-align:center;padding:24px 0;font-size:9px;color:var(--dim)}
.ft a{color:var(--accent);font-weight:700;text-decoration:none}
@keyframes spin{to{transform:rotate(360deg)}}
.load{text-align:center;padding:60px 20px}
.load i{font-size:36px;color:var(--accent);display:block;margin-bottom:14px;animation:spin 1.2s linear infinite}
.load p{font-size:12px;color:var(--dim)}
@media(max-width:400px){.stats{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="bg"></div><div class="grd"></div>
<div class="wrap">
<div class="head"><div class="avatar"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png" alt="logo" onerror="this.style.display='none';this.parentNode.innerHTML='<i class=\\'ti ti-bolt\\'></i>'"></div><div class="name">VaslZone</div><div class="sub">VaslZone Gateway</div></div>
<div id="root"><div class="load"><i class="ti ti-loader-2"></i><p>در حال بارگذاری...</p></div></div>
<div class="ft">Powered by <a href="https://t.me/VaslZone" target="_blank">VaslZone Gateway</a></div>
</div>
<script>
const KEY='"""+uuid_key+"""';
let allLinks=[];

async function loadData(){try{const r=await fetch('/api/public/sub/'+KEY);return await r.json()}catch(e){return null}}

function showLock(name){document.getElementById('root').innerHTML='<div class="empty"><i class="ti ti-lock" style="color:var(--amber)"></i><p style="color:var(--amber);font-weight:700">این گروه رمز دارد</p><p style="font-size:11px;margin-top:6px">'+name+'</p></div>'}

function showContent(d){
let active=d.links.filter(l=>l.active).length;
let totalUsed=d.links.reduce((s,l)=>s+(l.used_bytes||0),0);
let totalLimit=d.links.reduce((s,l)=>s+(l.limit_bytes||0),0);
let remGb=totalLimit>0?((totalLimit-totalUsed)/1073741824).toFixed(3):'نامحدود';
let h='<div class="info"><h2>'+d.name+'</h2>'+(d.desc?'<p>'+d.desc+'</p>':'<p>گروه اشتراک VaslZone</p>')+'</div>';
h+='<div class="stats"><div class="stat"><div class="stat-l">کانفیگ فعال</div><div class="stat-v">'+active+'</div><div class="stat-s">از '+d.links.length+'</div></div>';
h+='<div class="stat"><div class="stat-l">مصرف کل</div><div class="stat-v" style="font-size:15px">'+d.total_used_fmt+'</div><div class="stat-s">کل ترافیک</div></div>';
h+='<div class="stat"><div class="stat-l">اتصالات</div><div class="stat-v">'+(d.active_connections||0)+'</div><div class="stat-s">زنده</div></div></div>';
h+='<div class="sub-box"><span class="url">'+d.sub_url+'</span><button class="btn-c" onclick="navigator.clipboard.writeText(\\''+d.sub_url+'\\').then(()=>this.textContent=\\'کپی شد\\')">کپی</button></div>';
h+='<div style="display:flex;gap:8px;margin-bottom:14px"><button class="btn-s gold" onclick="copyAll()" style="flex:1"><i class="ti ti-copy"></i> کپی همه لینک‌ها</button>';
h+='<button class="btn-s" onclick="showQR(\\''+d.sub_url+'\\')" style="flex:0"><i class="ti ti-qrcode"></i></button></div>';
h+='<div style="margin-bottom:10px;font-size:10px;color:var(--dim);display:flex;align-items:center;gap:6px"><i class="ti ti-info-circle"></i> برای کپی لینک هر کانفیگ، دکمه کپی را بزنید</div>';
d.links.forEach((l,i)=>{
let pct=l.limit_bytes>0?Math.min(100,(l.used_bytes/l.limit_bytes)*100):0;
let bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--green)';
let rem=l.limit_bytes>0?((l.limit_bytes-l.used_bytes)/1073741824).toFixed(3)+' GB':'∞';
h+='<div class="config"><div class="config-h"><span class="config-label">'+l.label+'</span><span class="config-badge '+(l.active?'active':'inactive')+'">'+(l.active?'فعال':'غیرفعال')+'</span></div>';
h+='<div class="config-usage"><span>مصرف: <span>'+l.used_fmt+'</span></span><span>باقی: <span>'+rem+'</span></span><span>سهمیه: <span>'+(l.limit_fmt||'∞')+'</span></span></div>';
h+='<div class="config-link" id="vlink-'+i+'">'+l.vless_link+'</div>';
h+='<div class="config-actions"><button class="btn-s gold" onclick="showLink('+i+')"><i class="ti ti-eye"></i> نمایش لینک</button>';
h+='<button class="btn-s" onclick="navigator.clipboard.writeText(\\''+l.vless_link.replace(/\\n/g,'\\\\n')+'\\').then(()=>toast(\\'کپی شد\\'))"><i class="ti ti-copy"></i> کپی لینک</button></div></div>';
});
document.getElementById('root').innerHTML=h;
allLinks=d.links;
}

function showLink(i){
let el=document.getElementById('vlink-'+i);
if(el)el.classList.toggle('show');
}
function copyAll(){
let txt=allLinks.map(l=>l.vless_link).join('\\n');
navigator.clipboard.writeText(txt).then(()=>toast('همه کانفیگ‌ها کپی شد'));
}
function showQR(url){window.open('https://api.qrserver.com/v1/create-qr-code/?size=280x280&data='+encodeURIComponent(url),'_blank')}
function toast(m){let t=document.createElement('div');t.textContent=m;t.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--card2);color:var(--accent);border:1px solid var(--border2);padding:10px 22px;border-radius:10px;font-size:12px;font-weight:600;z-index:999;box-shadow:var(--shadow);animation:fade .25s';document.body.appendChild(t);setTimeout(()=>t.remove(),2200)}

async function init(){const d=await loadData();if(!d){document.getElementById('root').innerHTML='<div class="empty"><i class="ti ti-alert-circle" style="color:var(--red)"></i><p>خطا</p></div>';return}if(d.locked){showLock(d.name);return}showContent(d)}
init();
</script>
</body></html>"""
