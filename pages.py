# pages.py - VaslZone Gateway v10 - FINAL
LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>VaslZone</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root{--bg:#060f1d;--card:rgba(10,22,40,0.95);--accent:#F59E0B;--accent2:#FCD34D;--text:#E8F4FF;--border:rgba(245,158,11,0.25)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 0%,rgba(245,158,11,0.08),transparent 70%),var(--bg)}
.card{position:relative;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:35px;width:100%;max-width:380px;backdrop-filter:blur(20px);z-index:1}
.logo{display:flex;align-items:center;gap:12px;margin-bottom:25px}
.logo img{width:48px;height:48px;border-radius:14px;border:1px solid var(--border)}
h2{font-size:18px}p{font-size:12px;color:#7BAED4;margin-bottom:20px}
input{width:100%;padding:12px 15px;border-radius:12px;border:1px solid var(--border);background:rgba(0,0,0,0.3);color:#fff;outline:none;font-family:inherit;margin-bottom:15px}
input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(245,158,11,0.1)}
button{width:100%;padding:12px;border:none;border-radius:12px;background:var(--accent);color:#1a1a2e;font-weight:900;cursor:pointer;font-family:inherit;font-size:14px;transition:0.2s}
button:hover{filter:brightness(1.2)}
.footer{margin-top:18px;font-size:11px;color:#3D6B8E;text-align:center}
.footer a{color:var(--accent2);text-decoration:none}
</style></head>
<body><div class="bg"></div>
<div class="card"><div class="logo"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><div><h2>VaslZone</h2><p>Gateway v10</p></div></div>
<h2>ورود</h2><p>رمز عبور ادمین</p>
<form id="form"><input type="password" id="pw" placeholder="••••••" required><button type="submit">ورود به پنل</button></form>
<div class="footer">📢 <a href="https://t.me/VaslZone">@VaslZone</a></div></div>
<script>document.getElementById('form').onsubmit=async e=>{e.preventDefault();const b=document.querySelector('button');b.disabled=1;b.textContent='...';try{const r=await fetch('/api/login',{method:'POST',body:JSON.stringify({password:document.getElementById('pw').value})});if(r.ok)location.href='/dashboard';else{alert('خطا');b.disabled=0;b.textContent='ورود به پنل'}}catch(e){alert('خطا');b.disabled=0;b.textContent='ورود به پنل'}}</script></body></html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>VaslZone Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#060f1d;--bg2:#0a1628;--card:#0d1b2e;--accent:#F59E0B;--accent2:#FCD34D;--accent-d:rgba(245,158,11,0.12);--border:rgba(245,158,11,0.15);--t1:#E8F4FF;--t2:#7BAED4;--t3:#3D6B8E;--green:#10B981;--green-t:#34D399;--green-bg:rgba(16,185,129,0.1);--red:#EF4444;--red-t:#F87171;--red-bg:rgba(239,68,68,0.1);--amber:#F59E0B;--purple:#8B5CF6;--shadow:0 8px 32px rgba(0,0,0,0.5)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);display:flex;min-height:100vh;font-size:14px}
.sidebar{width:250px;background:var(--bg2);border-left:1px solid var(--border);display:flex;flex-direction:column;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .3s cubic-bezier(.4,0,.2,1)}
.sb-logo{display:flex;align-items:center;gap:10px;padding:20px;border-bottom:1px solid var(--border);background:linear-gradient(135deg,var(--bg2),rgba(245,158,11,0.05))}
.sb-logo img{width:38px;height:38px;border-radius:12px;border:2px solid var(--accent-d);box-shadow:0 0 20px rgba(245,158,11,0.15)}
.sb-logo div{font-weight:800;font-size:15px;background:linear-gradient(135deg,var(--accent2),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sb-logo small{font-size:9px;color:var(--t3);-webkit-text-fill-color:var(--t3)}
.nav-wrap{flex:1;overflow-y:auto;padding:8px 0}
.nav-item{display:flex;align-items:center;gap:10px;padding:11px 18px;cursor:pointer;color:var(--t3);font-size:13px;border-right:3px solid transparent;transition:.2s;margin:2px 10px;border-radius:0 10px 10px 0;font-weight:500}
.nav-item:hover{background:var(--accent-d);color:var(--t2);transform:translateX(-3px)}
.nav-item.active{background:var(--accent-d);color:var(--accent2);border-right-color:var(--accent);font-weight:700}
.nav-item i{font-size:18px;width:22px;text-align:center}
.sb-foot{padding:15px 18px;border-top:1px solid var(--border)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:6px;width:100%;padding:10px;border:none;border-radius:10px;background:var(--red-bg);color:var(--red-t);cursor:pointer;font-family:inherit;font-weight:700;font-size:12px;transition:.2s}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.main{margin-right:250px;flex:1;padding:25px 30px;min-height:100vh;transition:margin .3s}
.pg{display:none}.pg.active{display:block;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.topbar h2{font-size:20px;display:flex;align-items:center;gap:8px;font-weight:800}
.topbar h2 i{color:var(--accent)}
.card{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:22px;margin-bottom:18px;box-shadow:var(--shadow);transition:.2s}
.card:hover{border-color:rgba(245,158,11,0.25)}
.card-title{font-size:12px;font-weight:700;display:flex;align-items:center;gap:7px;margin-bottom:14px;color:var(--t2);text-transform:uppercase;letter-spacing:.04em}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px;text-align:center;transition:.2s}
.stat-card:hover{border-color:rgba(245,158,11,0.25);transform:translateY(-2px)}
.stat-card .num{font-size:26px;font-weight:900;background:linear-gradient(135deg,var(--accent2),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-card .lbl{font-size:10px;color:var(--t3);margin-top:5px;font-weight:600}
input,select{width:100%;padding:10px 14px;border-radius:10px;border:1px solid var(--border);background:rgba(0,0,0,0.25);color:var(--t1);outline:none;font-family:inherit;font-size:12.5px;transition:.2s}
input:focus,select:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-d)}
select option{background:var(--bg2)}
.btn{display:inline-flex;align-items:center;gap:5px;padding:9px 18px;border:none;border-radius:10px;font-family:inherit;font-weight:700;font-size:12px;cursor:pointer;transition:.2s}
.btn-p{background:linear-gradient(135deg,var(--accent),#D97706);color:#1a1a2e;font-weight:800}
.btn-p:hover{filter:brightness(1.15);transform:translateY(-1px)}
.btn-o{background:transparent;border:1px solid var(--border);color:var(--t2)}
.btn-d{background:var(--red-bg);color:var(--red-t)}
.btn-g{background:var(--accent-d);color:var(--accent2)}
.cfg-item{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;transition:.2s}
.cfg-item:hover{border-color:rgba(245,158,11,0.2)}
.cfg-item .addr{padding:2px 8px;border-radius:5px;background:var(--accent-d);color:var(--accent2);font-size:10px;font-family:monospace}
@media(max-width:900px){.sidebar{transform:translateX(100%)}.sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,0.5)}.main{margin-right:0;padding:15px}.grid-2,.grid-3,.grid-4{grid-template-columns:1fr}}
</style></head><body>
<aside class="sidebar" id="sb"><div class="sb-logo"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><div>VaslZone<small>Gateway v10</small></div></div>
<div class="nav-wrap">
<div class="nav-item active" data-pg="overview"><i class="ti ti-dashboard"></i> داشبورد</div>
<div class="nav-item" data-pg="configs"><i class="ti ti-link"></i> کانفیگ‌ها</div>
<div class="nav-item" data-pg="groups"><i class="ti ti-folders"></i> گروه‌ها</div>
<div class="nav-item" data-pg="resellers"><i class="ti ti-users"></i> نمایندگان</div>
<div class="nav-item" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
</div>
<div class="sb-foot"><button class="logout-btn" onclick="logout()"><i class="ti ti-logout"></i> خروج</button></div></aside>

<div class="main">
<div id="pg-overview" class="pg active">
<div class="topbar"><h2><i class="ti ti-layout-dashboard"></i> داشبورد VaslZone</h2><span id="uptime" style="font-size:11px;color:var(--t3)"></span></div>
<div class="grid-4">
<div class="stat-card"><div class="num" id="s-links">0</div><div class="lbl">کانفیگ‌ها</div></div>
<div class="stat-card"><div class="num" id="s-active">0</div><div class="lbl">فعال</div></div>
<div class="stat-card"><div class="num" id="s-groups">0</div><div class="lbl">گروه‌ها</div></div>
<div class="stat-card"><div class="num" id="s-res">0</div><div class="lbl">نمایندگان</div></div>
</div>
<div class="card" style="padding:15px"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی</div>
<div style="display:flex;gap:5px;margin-bottom:10px">
<button class="btn btn-g" style="padding:4px 10px;font-size:10px" onclick="loadChart(1)">۱ ساعت</button>
<button class="btn btn-g" style="padding:4px 10px;font-size:10px" onclick="loadChart(6)">۶ ساعت</button>
<button class="btn btn-g" style="padding:4px 10px;font-size:10px" onclick="loadChart(24)">۲۴ ساعت</button></div>
<canvas id="trafficChart" style="height:200px;width:100%"></canvas></div></div>

<div id="pg-configs" class="pg">
<div class="topbar"><h2><i class="ti ti-link"></i> کانفیگ‌ها</h2><span id="cfg-total" style="font-size:12px;color:var(--t3)"></span></div>
<div class="card"><div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ جدید</div>
<div class="grid-2">
<div><label style="font-size:10px;color:var(--t3);font-weight:700">نام</label><input id="f-name" placeholder="VaslZone"></div>
<div><label style="font-size:10px;color:var(--t3);font-weight:700">تعداد</label><input type="number" id="f-count" value="1" min="1"></div>
<div><label style="font-size:10px;color:var(--t3);font-weight:700">حجم (GB)</label><input type="number" id="f-gb" value="0"></div>
<div><label style="font-size:10px;color:var(--t3);font-weight:700">انقضا (روز)</label><input type="number" id="f-exp" value="0"></div>
<div style="grid-column:1/-1"><label style="font-size:10px;color:var(--t3);font-weight:700">آدرس (IP یا دامنه)</label><input id="f-addr" placeholder="1.1.1.1 یا example.com"></div>
</div>
<div style="display:flex;gap:10px;align-items:center;margin-top:12px;flex-wrap:wrap">
<input type="number" id="f-port" placeholder="پورت" style="width:80px">
<select id="f-proto" style="width:auto;padding:8px 10px">
<option value="vless-ws">VLESS/WS</option>
<option value="xhttp-packet-up">XHTTP Packet</option>
<option value="xhttp-stream-up">XHTTP Stream</option></select>
<label style="display:flex;align-items:center;gap:5px;font-size:12px"><input type="checkbox" id="f-pers" style="width:auto"> شخصی</label>
<button class="btn btn-p" onclick="createLinks()"><i class="ti ti-plus"></i> ساخت کانفیگ</button></div></div>
<div id="cfg-list">بارگذاری...</div></div>

<div id="pg-groups" class="pg">
<div class="topbar"><h2><i class="ti ti-folders"></i> گروه‌ها</h2><button class="btn btn-p" onclick="showModal('grp')"><i class="ti ti-plus"></i> گروه جدید</button></div>
<div id="grp-list">بارگذاری...</div></div>

<div id="pg-resellers" class="pg">
<div class="topbar"><h2><i class="ti ti-users"></i> نمایندگان</h2><button class="btn btn-p" onclick="showModal('res')"><i class="ti ti-plus"></i> نماینده جدید</button></div>
<div id="res-list">بارگذاری...</div></div>

<div id="pg-settings" class="pg">
<div class="topbar"><h2><i class="ti ti-settings"></i> تنظیمات</h2></div>
<div class="card"><div class="card-title"><i class="ti ti-world"></i> آدرس/پورت سراسری</div>
<div style="margin-bottom:10px"><input id="g-addr" placeholder="1.1.1.1, 2.2.2.2, example.com"></div>
<div style="margin-bottom:15px"><input type="number" id="g-port" placeholder="پورت"></div>
<button class="btn btn-p" onclick="saveGlobal()"><i class="ti ti-device-floppy"></i> ذخیره</button></div></div>
</div>

<div id="m-grp" class="modal"><div class="modal-box"><button class="m-close" onclick="hideModal('grp')">✕</button><h3>گروه جدید</h3><input id="g-name" placeholder="نام"><button class="btn btn-p" style="width:100%;margin-top:10px;justify-content:center" onclick="createGroup()">ایجاد</button></div></div>
<div id="m-res" class="modal"><div class="modal-box"><button class="m-close" onclick="hideModal('res')">✕</button><h3>نماینده جدید</h3><input id="r-name" placeholder="نام"><input id="r-pw" type="password" placeholder="رمز" style="margin-top:8px"><input id="r-gb" type="number" placeholder="حجم (GB)" style="margin-top:8px"><button class="btn btn-p" style="width:100%;margin-top:12px;justify-content:center" onclick="createRes()">ایجاد نماینده</button></div></div>

<style>.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:999;align-items:center;justify-content:center;backdrop-filter:blur(4px)}.modal.open{display:flex}.modal-box{background:var(--card);padding:28px;border-radius:20px;width:380px;border:1px solid var(--border);position:relative}.m-close{position:absolute;left:12px;top:12px;background:var(--accent-d);border:none;color:var(--t2);width:30px;height:30px;border-radius:10px;cursor:pointer;font-size:16px}</style>

<script>
let chart;const toast=m=>{let t=document.getElementById('tst');if(!t){t=document.createElement('div');t.id='tst';t.style.cssText='position:fixed;bottom:20px;left:50%;transform:translateX(-50%);padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:9999;background:var(--card);border:1px solid var(--border);color:var(--t1);box-shadow:var(--shadow);display:none';document.body.appendChild(t)}t.textContent=m;t.style.display='block';setTimeout(()=>t.style.display='none',2500)};
const api=async(u,o={})=>{const r=await fetch('/api'+u,o);if(r.status===401)location.href='/login';if(o.method)return r.json();return r.json()};
const nav=id=>{document.querySelectorAll('.pg').forEach(e=>e.classList.remove('active'));document.getElementById('pg-'+id).classList.add('active');document.querySelectorAll('.nav-item').forEach(e=>e.classList.remove('active'));event.currentTarget.classList.add('active');({configs:loadConfigs,groups:loadGroups,resellers:loadRes,settings:loadGlobal}[id]?.())};
document.querySelectorAll('.nav-item').forEach(e=>e.addEventListener('click',()=>nav(e.dataset.pg)));
const showModal=id=>document.getElementById('m-'+id).classList.add('open');
const hideModal=id=>document.getElementById('m-'+id).classList.remove('open');

async function loadStats(){try{const d=await api('/stats');document.getElementById('s-links').textContent=d.links_count||0;document.getElementById('s-active').textContent=d.active_links||0;document.getElementById('s-groups').textContent=d.subs_count||0;document.getElementById('s-res').textContent=d.resellers_count||0;document.getElementById('uptime').textContent='آپتایم: '+d.uptime;return d}catch(e){}}

async function loadChart(hours){try{const d=await api('/stats');const h=d.hourly||{};const now=new Date;const labels=[];const data=[];for(let i=hours-1;i>=0;i--){const t=new Date(now.getTime()-i*3600000);const key=t.getHours().toString().padStart(2,'0')+':00';labels.push(key);data.push(((h[key]||0)/1024/1024).toFixed(2))}if(chart)chart.destroy();const ctx=document.getElementById('trafficChart').getContext('2d');chart=new Chart(ctx,{type:'line',data:{labels,datasets:[{label:'MB',data,borderColor:'#F59E0B',backgroundColor:'rgba(245,158,11,0.1)',fill:true,tension:.4,pointRadius:3,pointBackgroundColor:'#F59E0B',borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'#3D6B8E',font:{size:9}}},y:{grid:{color:'rgba(245,158,11,0.06)'},ticks:{color:'#3D6B8E',font:{size:9}}}}}})}catch(e){}}

async function loadConfigs(){try{const d=await api('/links');const ls=d.links||[];document.getElementById('cfg-total').textContent=ls.length+' کانفیگ';document.getElementById('cfg-list').innerHTML=ls.length?ls.map(l=>{
const used=((l.used_bytes||0)/1024/1024).toFixed(1);const lim=l.limit_bytes?(l.limit_bytes/1024/1024).toFixed(0)+'MB':'∞';
const addr=l.ips&&l.ips.length?l.ips[0]:'';const vless=l.vless_link?.split('\n')[0]||'';
return`<div class="cfg-item"><div><strong>${l.label}</strong><div style="font-size:10px;color:var(--t3);margin-top:3px"><code style="background:rgba(0,0,0,0.3);padding:1px 6px;border-radius:4px;font-size:9px">${l.uuid.slice(0,10)}</code> ${l.active?'<span style="color:var(--green-t)">● فعال</span>':'<span style="color:var(--red-t)">● غیرفعال</span>'}</div></div><div style="text-align:left;font-size:11px"><div>${used}MB / ${lim}</div>${addr?`<div class="addr">${addr}</div>`:''}<div style="margin-top:5px;display:flex;gap:4px"><button class="btn btn-g" style="padding:3px 8px;font-size:9px" onclick="cp('${vless}')">📋 کپی</button><button class="btn btn-d" style="padding:3px 8px;font-size:9px" onclick="delCfg('${l.uuid}')">🗑</button></div></div></div>`}).join(''):'<p style="padding:30px;text-align:center;color:var(--t3)">کانفیگی وجود ندارد</p>'}catch(e){}}
const cp=t=>{navigator.clipboard.writeText(t);toast('کپی شد')};
async function delCfg(id){if(!confirm('حذف کانفیگ?'))return;await api('/links/'+id,{method:'DELETE'});loadConfigs();toast('حذف شد')}

async function createLinks(){try{const b={label:document.getElementById('f-name').value||'VZ',count:document.getElementById('f-count').value||1,limit_value:document.getElementById('f-gb').value||0,limit_unit:'GB',expires_days:document.getElementById('f-exp').value||0,ips:document.getElementById('f-addr').value?[document.getElementById('f-addr').value]:[],port:document.getElementById('f-port').value||null,is_personal:document.getElementById('f-pers').checked,protocol:document.getElementById('f-proto').value};const d=await api('/links/bulk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});if(d.vless_bulk)navigator.clipboard.writeText(d.vless_bulk);toast((d.count||1)+' کانفیگ ساخته شد ✓');loadConfigs()}catch(e){toast('خطا','')}}

async function loadGroups(){try{const d=await api('/subs');const ss=d.subs||[];document.getElementById('grp-list').innerHTML=ss.length?ss.map(s=>`<div class="cfg-item"><div><strong>${s.name}</strong><div style="font-size:10px;color:var(--t3)">${s.links_count} کانفیگ</div></div><div style="display:flex;gap:4px"><button class="btn btn-g" style="padding:3px 8px;font-size:9px" onclick="cp('${s.sub_url}')">📋 ساب</button><button class="btn btn-g" style="padding:3px 8px;font-size:9px" onclick="cp('${s.public_url}')">📋 پابلیک</button><button class="btn btn-d" style="padding:3px 8px;font-size:9px" onclick="delGrp('${s.sub_id}')">🗑</button></div></div>`).join(''):'<p style="padding:30px;text-align:center;color:var(--t3)">گروهی وجود ندارد</p>'}catch(e){}}
async function createGroup(){await api('/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('g-name').value})});hideModal('grp');loadGroups();toast('گروه ساخته شد')}
async function delGrp(id){if(!confirm('حذف گروه؟'))return;await api('/subs/'+id,{method:'DELETE'});loadGroups();toast('حذف شد')}

async function loadRes(){try{const d=await api('/resellers');const rs=d.resellers||[];document.getElementById('res-list').innerHTML=rs.length?`<table><tr><th>نام</th><th>حجم</th><th>مصرف</th><th>باقی</th><th>وضعیت</th><th></th></tr>${rs.map(r=>`<tr><td>${r.name}</td><td>${r.total_fmt}</td><td>${r.allocated_fmt}</td><td style="color:var(--accent2)">${r.remaining_fmt}</td><td>${r.active?'<span style="color:var(--green-t)">فعال</span>':'<span style="color:var(--red-t)">غیرفعال</span>'}</td><td><button class="btn btn-d" style="padding:2px 7px;font-size:9px" onclick="delRes('${r.id}')">✕</button></td></tr>`).join('')}</table>`:'<p style="padding:30px;text-align:center;color:var(--t3)">نماینده‌ای وجود ندارد</p>'}catch(e){}}
async function createRes(){await api('/resellers',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('r-name').value,password:document.getElementById('r-pw').value,limit_gb:document.getElementById('r-gb').value})});hideModal('res');loadRes();toast('نماینده ساخته شد')}
async function delRes(id){if(!confirm('حذف نماینده؟'))return;await api('/resellers/'+id,{method:'DELETE'});loadRes();toast('حذف شد')}

async function saveGlobal(){await api('/settings/global-ips',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ips:document.getElementById('g-addr').value.split(',').filter(x=>x.trim()),port:document.getElementById('g-port').value})});toast('ذخیره شد')}
async function loadGlobal(){try{const d=await api('/settings/global-ips');document.getElementById('g-addr').value=(d.ips||[]).join(', ');document.getElementById('g-port').value=d.port||''}catch(e){}}

function logout(){fetch('/api/logout',{method:'POST'}).then(()=>location.href='/login')}
loadStats();loadGlobal();loadChart(6);setInterval(loadStats,5000);
</script></body></html>"""

def get_public_page_html(uuid_key: str) -> str:
    return f"""<!DOCTYPE html><html lang="fa"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>VaslZone Sub</title><style>body{{background:#060f1d;color:#E8F4FF;font-family:system-ui,sans-serif;padding:30px;text-align:center;max-width:500px;margin:auto}}img{{border-radius:15px;width:80px;margin-bottom:15px;border:2px solid rgba(245,158,11,0.2)}}h2{{font-size:18px;background:linear-gradient(135deg,#FCD34D,#F59E0B);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}.card{{background:#0d1b2e;border:1px solid rgba(245,158,11,0.2);border-radius:14px;padding:15px;margin:10px 0}}button{{background:#F59E0B;color:#1a1a2e;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-weight:700;font-family:inherit}}</style></head><body><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><h2>VaslZone</h2><div id="content">بارگذاری...</div><script>
fetch('/api/public/sub/{uuid_key}').then(r=>r.json()).then(d=>{{if(d.locked)document.getElementById('content').innerHTML='<div class="card">🔒 نیاز به رمز</div>';else document.getElementById('content').innerHTML=d.links.map(l=>'<div class="card"><b>'+l.label+'</b><br><small>'+l.used_fmt+' / '+l.limit_fmt+'</small><br><button onclick="navigator.clipboard.writeText(\\''+l.vless_link.replace(/\\n/g,' ')+'\\')">📋 کپی لینک</button></div>').join('')}}).catch(()=>document.getElementById('content').innerHTML='<div class="card">⚠️ خطا</div>');
</script></body></html>"""
