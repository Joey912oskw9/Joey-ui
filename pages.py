# pages.py - VaslZone Gateway v10
# Complete Professional Dashboard

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · VaslZone</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root{--bg:#060f1d;--card:rgba(10,22,40,0.95);--accent:#EF4444;--text:#E8F4FF;--border:rgba(239,68,68,0.25)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 0%,rgba(239,68,68,0.08),transparent 70%),var(--bg)}
.card{position:relative;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:35px;width:100%;max-width:380px;backdrop-filter:blur(20px);z-index:1}
.logo{display:flex;align-items:center;gap:12px;margin-bottom:25px}
.logo img{width:48px;height:48px;border-radius:14px;border:1px solid var(--border)}
h2{font-size:18px;margin-bottom:5px}p{font-size:12px;color:#7BAED4;margin-bottom:20px}
input{width:100%;padding:12px 15px;border-radius:12px;border:1px solid var(--border);background:rgba(0,0,0,0.3);color:#fff;outline:none;font-family:inherit;margin-bottom:15px}
input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(239,68,68,0.1)}
button{width:100%;padding:12px;border:none;border-radius:12px;background:var(--accent);color:#fff;font-weight:700;cursor:pointer;font-family:inherit;font-size:14px;transition:0.2s}
button:hover{filter:brightness(1.15)}
.footer{margin-top:18px;font-size:11px;color:#3D6B8E;text-align:center}
.footer a{color:var(--accent);text-decoration:none}
</style></head>
<body><div class="bg"></div>
<div class="card">
  <div class="logo"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><div><h2>VaslZone</h2><p>Gateway v10</p></div></div>
  <h2 style="font-size:16px">ورود به پنل</h2>
  <p>رمز عبور ادمین را وارد کنید</p>
  <form id="form">
    <input type="password" id="pw" placeholder="رمز عبور" required>
    <button type="submit">ورود به داشبورد</button>
  </form>
  <div class="footer">کانال رسمی: <a href="https://t.me/VaslZone" target="_blank">@VaslZone</a></div>
</div>
<script>
document.getElementById('form').onsubmit=async(e)=>{
  e.preventDefault();const btn=e.target.querySelector('button');btn.disabled=true;btn.textContent='...';
  try{
    const r=await fetch('/api/login',{method:'POST',body:JSON.stringify({password:document.getElementById('pw').value})});
    if(r.ok)location.href='/dashboard';else{alert('خطا');btn.disabled=false;btn.textContent='ورود به داشبورد';}
  }catch(e){alert('خطا');btn.disabled=false;btn.textContent='ورود به داشبورد';}
};
</script></body></html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VaslZone · پنل مدیریت</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#060f1d;--bg2:#0a1628;--card:#0d1b2e;--accent:#EF4444;--accent2:#F87171;--accent-d:rgba(239,68,68,0.12);--border:rgba(239,68,68,0.15);--t1:#E8F4FF;--t2:#7BAED4;--t3:#3D6B8E;--green:#10B981;--green-t:#34D399;--green-bg:rgba(16,185,129,0.1);--red:#EF4444;--red-t:#F87171;--red-bg:rgba(239,68,68,0.1);--amber:#F59E0B;--purple:#8B5CF6;--shadow:0 8px 32px rgba(0,0,0,0.4)}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);display:flex;min-height:100vh;font-size:14px}
.sidebar{width:250px;background:var(--bg2);border-left:1px solid var(--border);display:flex;flex-direction:column;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .3s}
.sb-logo{display:flex;align-items:center;gap:10px;padding:20px;border-bottom:1px solid var(--border)}
.sb-logo img{width:36px;height:36px;border-radius:10px;border:1px solid var(--border)}
.sb-logo div{font-weight:700;font-size:14px}.sb-logo small{font-size:10px;color:var(--t3)}
.nav-wrap{flex:1;overflow-y:auto;padding:10px 0}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 18px;cursor:pointer;color:var(--t3);font-size:13px;border-right:3px solid transparent;transition:.15s;margin:2px 10px;border-radius:0 8px 8px 0}
.nav-item:hover{background:var(--accent-d);color:var(--t2)}
.nav-item.active{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-item i{font-size:17px;width:20px;text-align:center}
.sb-foot{padding:15px 18px;border-top:1px solid var(--border)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;padding:9px;border:none;border-radius:10px;background:var(--red-bg);color:var(--red-t);cursor:pointer;font-family:inherit;font-weight:600;transition:.15s}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.main{margin-right:250px;flex:1;padding:25px 30px;min-height:100vh;transition:margin .3s}
.pg{display:none}.pg.active{display:block;animation:fade .25s ease}
@keyframes fade{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:10px}
.topbar h2{font-size:20px;display:flex;align-items:center;gap:8px}
.topbar h2 i{color:var(--accent)}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;margin-bottom:18px}
.card-title{font-size:13px;font-weight:700;display:flex;align-items:center;gap:7px;margin-bottom:12px;color:var(--t2)}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
input,select{width:100%;padding:10px 13px;border-radius:10px;border:1px solid var(--border);background:rgba(0,0,0,0.2);color:var(--t1);outline:none;font-family:inherit;font-size:12.5px;transition:.15s}
input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-d)}
select option{background:var(--bg2)}
button,input[type=checkbox]{cursor:pointer}
.btn{display:inline-flex;align-items:center;gap:5px;padding:8px 16px;border:none;border-radius:10px;font-family:inherit;font-weight:600;font-size:12px;cursor:pointer;transition:.15s}
.btn-p{background:var(--accent);color:#fff}
.btn-p:hover{filter:brightness(1.15)}
.btn-o{background:transparent;border:1px solid var(--border);color:var(--t2)}
.btn-d{background:var(--red-bg);color:var(--red-t)}
.btn-g{background:var(--accent-d);color:var(--accent2)}
.badge{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:20px;font-size:10px;font-weight:700}
table{width:100%;border-collapse:collapse;margin-top:8px}
th,td{padding:10px 12px;text-align:right;border-bottom:1px solid var(--border);font-size:12.5px}
th{color:var(--t3);font-weight:700;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em}
td{color:var(--t1)}
.stat-card{text-align:center;padding:15px}
.stat-card .num{font-size:28px;font-weight:800;color:var(--t1)}
.stat-card .lbl{font-size:10px;color:var(--t3);margin-top:5px}
@media(max-width:900px){.sidebar{transform:translateX(100%)}.sidebar.open{transform:translateX(0)}.main{margin-right:0;padding:15px}.grid-2,.grid-3{grid-template-columns:1fr}}
</style></head><body>
<aside class="sidebar" id="sb">
  <div class="sb-logo"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><div>VaslZone<small>v10</small></div></div>
  <div class="nav-wrap">
    <div class="nav-item active" data-pg="overview"><i class="ti ti-dashboard"></i> داشبورد</div>
    <div class="nav-item" data-pg="configs"><i class="ti ti-link"></i> کانفیگ‌ها</div>
    <div class="nav-item" data-pg="groups"><i class="ti ti-folders"></i> گروه‌ها</div>
    <div class="nav-item" data-pg="resellers"><i class="ti ti-users"></i> نمایندگان</div>
    <div class="nav-item" data-pg="ips"><i class="ti ti-world"></i> IP سراسری</div>
  </div>
  <div class="sb-foot"><button class="logout-btn" onclick="logout()"><i class="ti ti-logout"></i> خروج از پنل</button></div>
</aside>
<div class="main" id="main">
<!-- Overview -->
<div id="pg-overview" class="pg active">
  <div class="topbar"><h2><i class="ti ti-dashboard"></i> داشبورد</h2><span id="upd-time" style="font-size:11px;color:var(--t3)"></span></div>
  <div class="grid-3" id="stats-box"><div class="card stat-card"><div class="num" id="s-links">-</div><div class="lbl">کانفیگ‌ها</div></div><div class="card stat-card"><div class="num" id="s-subs">-</div><div class="lbl">گروه‌ها</div></div><div class="card stat-card"><div class="num" id="s-res">-</div><div class="lbl">نمایندگان</div></div></div>
</div>

<!-- Configs -->
<div id="pg-configs" class="pg">
  <div class="topbar"><h2><i class="ti ti-link"></i> کانفیگ‌ها</h2><span id="cfg-count" style="font-size:12px;color:var(--t3)"></span></div>
  <div class="card"><div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ</div>
    <div class="grid-2">
      <div><label>نام</label><input id="f-name" placeholder="مثلاً VaslZone-1"></div>
      <div><label>تعداد</label><input type="number" id="f-count" value="1" min="1"></div>
      <div><label>حجم (GB)</label><input type="number" id="f-gb" value="0" placeholder="0=نامحدود"></div>
      <div><label>انقضا (روز)</label><input type="number" id="f-exp" value="0" placeholder="0=نامحدود"></div>
      <div><label>آدرس (IP یا دامنه)</label><input id="f-addr" placeholder="1.1.1.1 یا example.com"></div>
      <div><label>پورت</label><input type="number" id="f-port" placeholder="443"></div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;margin-top:12px;flex-wrap:wrap">
      <label style="display:flex;align-items:center;gap:5px;font-size:12px"><input type="checkbox" id="f-pers" style="width:auto"> استفاده شخصی</label>
      <label style="display:flex;align-items:center;gap:5px;font-size:12px">
        <select id="f-proto" style="width:auto;padding:6px 10px">
          <option value="vless-ws">VLESS/WS</option>
          <option value="xhttp-packet-up">XHTTP Packet</option>
          <option value="xhttp-stream-up">XHTTP Stream</option>
        </select> پروتکل</label>
      <button class="btn btn-p" onclick="createLinks()"><i class="ti ti-plus"></i> ساخت</button>
    </div>
  </div>
  <div id="cfg-list" style="font-size:13px;color:var(--t3)">بارگذاری...</div>
</div>

<!-- Groups -->
<div id="pg-groups" class="pg">
  <div class="topbar"><h2><i class="ti ti-folders"></i> گروه‌ها</h2><button class="btn btn-p" onclick="showModal('group')"><i class="ti ti-plus"></i> گروه جدید</button></div>
  <div id="grp-list" style="font-size:13px;color:var(--t3)">بارگذاری...</div>
</div>

<!-- Resellers -->
<div id="pg-resellers" class="pg">
  <div class="topbar"><h2><i class="ti ti-users"></i> نمایندگان</h2><button class="btn btn-p" onclick="showModal('res')"><i class="ti ti-plus"></i> نماینده جدید</button></div>
  <div id="res-list" style="font-size:13px;color:var(--t3)">بارگذاری...</div>
</div>

<!-- IP Settings -->
<div id="pg-ips" class="pg">
  <div class="topbar"><h2><i class="ti ti-world"></i> IP سراسری</h2></div>
  <div class="card">
    <div style="margin-bottom:12px"><label>آدرس‌های سراسری (با کاما)</label><input id="g-addr" placeholder="1.1.1.1, 2.2.2.2, example.com"></div>
    <div style="margin-bottom:15px"><label>پورت سراسری</label><input type="number" id="g-port" placeholder="443"></div>
    <button class="btn btn-p" onclick="saveGlobal()"><i class="ti ti-device-floppy"></i> ذخیره تنظیمات</button>
  </div>
</div>
</div>

<!-- Modals -->
<div id="m-group" class="modal"><div class="modal-box"><button class="m-close" onclick="hideModal('group')">✕</button><h3 style="margin-bottom:12px">گروه جدید</h3><input id="g-name" placeholder="نام گروه"><button class="btn btn-p" onclick="createGroup()" style="margin-top:10px;width:100%">ایجاد گروه</button></div></div>
<div id="m-res" class="modal"><div class="modal-box"><button class="m-close" onclick="hideModal('res')">✕</button><h3 style="margin-bottom:12px">نماینده جدید</h3><input id="r-name" placeholder="نام"><input id="r-pw" placeholder="رمز عبور" style="margin-top:8px"><input id="r-gb" type="number" placeholder="حجم (GB)" style="margin-top:8px"><button class="btn btn-p" onclick="createRes()" style="margin-top:12px;width:100%">ایجاد نماینده</button></div></div>

<style>.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:999;align-items:center;justify-content:center}.modal.open{display:flex}.modal-box{background:var(--card);padding:25px;border-radius:16px;width:380px;border:1px solid var(--border);position:relative}.m-close{position:absolute;left:12px;top:12px;background:var(--accent-d);border:none;color:var(--t2);width:28px;height:28px;border-radius:8px;cursor:pointer;font-size:14px}</style>

<script>
const api=async(u,o={})=>{const r=await fetch('/api'+u,o);if(r.status===401)location.href='/login';if(o.method&&o.method!=='GET')return r.json();return r.json()};
const toast=(m,t='ok')=>{const el=document.getElementById('t');if(!el){const d=document.createElement('div');d.id='t';d.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);padding:10px 20px;border-radius:10px;font-size:13px;z-index:9999;background:#0d1b2e;border:1px solid rgba(239,68,68,0.3);color:#E8F4FF';document.body.appendChild(d);el=document.getElementById('t')}el.textContent=m;el.style.display='block';setTimeout(()=>el.style.display='none',2500)};

function nav(id){document.querySelectorAll('.pg').forEach(e=>e.classList.remove('active'));document.getElementById('pg-'+id).classList.add('active');document.querySelectorAll('.nav-item').forEach(e=>e.classList.remove('active'));event.currentTarget.classList.add('active');const fns={configs:loadConfigs,groups:loadGroups,resellers:loadRes};if(fns[id])fns[id]()}

function showModal(id){document.getElementById('m-'+id).classList.add('open')}
function hideModal(id){document.getElementById('m-'+id).classList.remove('open')}

async function loadStats(){try{const d=await api('/stats');document.getElementById('s-links').textContent=d.links_count||0;document.getElementById('s-subs').textContent=d.subs_count||0;document.getElementById('s-res').textContent=d.resellers_count||0;document.getElementById('upd-time').textContent=new Date().toLocaleString('fa-IR')}catch(e){}}

async function loadConfigs(){try{const d=await api('/links');const ls=d.links||[];document.getElementById('cfg-count').textContent=ls.length+' کانفیگ';let h='';ls.forEach(l=>{const used=((l.used_bytes||0)/1024/1024).toFixed(1);const lim=l.limit_bytes?(l.limit_bytes/1024/1024).toFixed(0)+'MB':'∞';h+=`<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px 15px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px"><div><strong>${l.label}</strong><div style="font-size:10px;color:var(--t3);margin-top:2px"><code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;font-size:9px">${l.uuid.slice(0,12)}…</code> <span style="color:${l.active?'var(--green-t)':'var(--red-t)'}">${l.active?'فعال':'غیرفعال'}</span></div></div><div style="text-align:left;font-size:11px"><div>${used}MB / ${lim}</div><div style="margin-top:5px;display:flex;gap:4px">${l.ips&&l.ips.length?`<span style="background:var(--accent-d);color:var(--accent2);padding:2px 7px;border-radius:5px;font-size:9px">${l.ips[0]}</span>`:''}<button class="btn btn-g" style="padding:4px 8px;font-size:10px" onclick="cp('${l.vless_link}')">کپی</button><button class="btn btn-d" style="padding:4px 8px;font-size:10px" onclick="delCfg('${l.uuid}')">✕</button></div></div></div>`});document.getElementById('cfg-list').innerHTML=h||'<p style="padding:20px;text-align:center;color:var(--t3)">کانفیگی وجود ندارد</p>'}catch(e){}}
const cp=t=>{navigator.clipboard.writeText(t.split('\\n')[0]);toast('کپی شد')};
async function delCfg(id){if(!confirm('حذف کانفیگ؟'))return;await api('/links/'+id,{method:'DELETE'});loadConfigs();toast('حذف شد')}

async function createLinks(){try{
  const b={label:document.getElementById('f-name').value||'VZ',count:document.getElementById('f-count').value||1,limit_value:document.getElementById('f-gb').value||0,limit_unit:'GB',expires_days:document.getElementById('f-exp').value||0,ips:document.getElementById('f-addr').value?[document.getElementById('f-addr').value]:[],port:document.getElementById('f-port').value||null,is_personal:document.getElementById('f-pers').checked,protocol:document.getElementById('f-proto').value};
  const d=await api('/links/bulk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});
  if(d.vless_bulk)navigator.clipboard.writeText(d.vless_bulk);toast((d.count||1)+' کانفیگ ساخته شد'+(d.vless_bulk?' - لینک‌ها کپی شد':''));
  loadConfigs();
}catch(e){toast('خطا در ساخت','err')}}

async function loadGroups(){try{const d=await api('/subs');const ss=d.subs||[];document.getElementById('grp-list').innerHTML=ss.length?ss.map(s=>`<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px 15px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px"><div><strong>${s.name}</strong><div style="font-size:10px;color:var(--t3)">${s.links_count} کانفیگ</div></div><div style="display:flex;gap:5px"><button class="btn btn-g" style="padding:4px 8px;font-size:10px" onclick="cp('${s.sub_url}')">کپی ساب</button><button class="btn btn-g" style="padding:4px 8px;font-size:10px" onclick="cp('${s.public_url}')">کپی پابلیک</button><button class="btn btn-d" style="padding:4px 8px;font-size:10px" onclick="delGrp('${s.sub_id}')">✕</button></div></div>`).join(''):'<p style="padding:20px;text-align:center;color:var(--t3)">گروهی وجود ندارد</p>'}catch(e){}}
async function createGroup(){await api('/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('g-name').value})});hideModal('group');loadGroups();toast('گروه ساخته شد')}
async function delGrp(id){if(!confirm('حذف گروه؟'))return;await api('/subs/'+id,{method:'DELETE'});loadGroups();toast('حذف شد')}

async function loadRes(){try{const d=await api('/resellers');const rs=d.resellers||[];document.getElementById('res-list').innerHTML=rs.length?`<table><tr><th>نام</th><th>حجم کل</th><th>تخصیص</th><th>باقی</th><th>وضعیت</th><th></th></tr>${rs.map(r=>`<tr><td>${r.name}</td><td>${r.total_fmt}</td><td>${r.allocated_fmt}</td><td>${r.remaining_fmt}</td><td>${r.active?'<span style="color:var(--green-t)">فعال</span>':'<span style="color:var(--red-t)">غیرفعال</span>'}</td><td><button class="btn btn-d" style="padding:3px 7px;font-size:10px" onclick="delRes('${r.id}')">✕</button></td></tr>`).join('')}</table>`:'<p style="padding:20px;text-align:center;color:var(--t3)">نماینده‌ای وجود ندارد</p>'}catch(e){}}
async function createRes(){await api('/resellers',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('r-name').value,password:document.getElementById('r-pw').value,limit_gb:document.getElementById('r-gb').value})});hideModal('res');loadRes();toast('نماینده ساخته شد')}
async function delRes(id){if(!confirm('حذف نماینده؟'))return;await api('/resellers/'+id,{method:'DELETE'});loadRes();toast('حذف شد')}

async function saveGlobal(){await api('/settings/global-ips',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ips:document.getElementById('g-addr').value.split(',').filter(x=>x.trim()),port:document.getElementById('g-port').value})});toast('تنظیمات ذخیره شد')}
async function loadGlobal(){try{const d=await api('/settings/global-ips');document.getElementById('g-addr').value=(d.ips||[]).join(', ');document.getElementById('g-port').value=d.port||''}catch(e){}}

function logout(){fetch('/api/logout',{method:'POST'}).then(()=>location.href='/login')}

document.querySelectorAll('.nav-item').forEach(el=>el.addEventListener('click',()=>nav(el.dataset.pg)));
loadStats();loadGlobal();
setInterval(loadStats,5000);
</script></body></html>"""

def get_public_page_html(uuid_key: str) -> str:
    return f"""<!DOCTYPE html><html lang="fa"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>VaslZone</title><style>body{{background:#060f1d;color:#E8F4FF;font-family:system-ui,sans-serif;padding:30px;text-align:center}}img{{border-radius:15px;width:80px;margin-bottom:15px}}h2{{font-size:18px}}.card{{background:#0d1b2e;border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:15px;margin:10px auto;max-width:400px}}.btn{{background:#EF4444;color:#fff;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;margin:5px}}</style></head><body><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><h2>VaslZone Sub</h2><div id="content">بارگذاری...</div><script>
fetch('/api/public/sub/{uuid_key}').then(r=>r.json()).then(d=>{{
  if(d.locked)document.getElementById('content').innerHTML='<div class="card">🔒 نیاز به رمز</div>';
  else document.getElementById('content').innerHTML=d.links.map(l=>'<div class="card"><b>'+l.label+'</b><br><small>'+l.used_fmt+' / '+l.limit_fmt+'</small><br><button class="btn" onclick="navigator.clipboard.writeText(\\''+l.vless_link+'\\')">کپی لینک</button></div>').join('');
}}).catch(()=>document.getElementById('content').innerHTML='<div class="card">خطا</div>');
</script></body></html>"""
