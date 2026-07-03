# pages.py - VaslZone Gateway v9.2
# Complete replacement with Red Theme + All Features

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · VaslZone Gateway</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root{--bg:#060f1d;--card:rgba(10,22,40,0.9);--accent:#EF4444;--text:#E8F4FF;--dim:#3D6B8E;--border:rgba(239,68,68,0.2)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;height:100vh}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:30px;width:100%;max-width:380px;box-shadow:0 10px 40px rgba(239,68,68,0.1)}
.brand{display:flex;align-items:center;gap:15px;margin-bottom:30px}
.brand img{width:50px;border-radius:12px;border:1px solid var(--border)}
input{width:100%;padding:12px;margin:10px 0 20px;border-radius:10px;border:1px solid var(--border);background:rgba(0,0,0,0.3);color:var(--text);outline:none}
input:focus{border-color:var(--accent)}
button{width:100%;padding:12px;border:none;border-radius:10px;background:var(--accent);color:#fff;font-weight:bold;cursor:pointer;transition:0.2s}
button:hover{filter:brightness(1.2)}
</style>
</head>
<body>
<div class="card">
  <div class="brand">
    <img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png" alt="VaslZone">
    <div><h3>VaslZone</h3><small>Gateway v9.2</small></div>
  </div>
  <h2>ورود به پنل</h2>
  <form id="form">
    <input type="password" id="pw" placeholder="رمز عبور" required>
    <button type="submit" id="btn">ورود</button>
  </form>
</div>
<script>
document.getElementById('form').onsubmit = async(e)=>{
  e.preventDefault();
  const btn=document.getElementById('btn'); btn.disabled=true; btn.textContent='در حال ورود...';
  const r=await fetch('/api/login',{method:'POST',body:JSON.stringify({password:document.getElementById('pw').value})});
  if(r.ok) location.href='/dashboard'; else { alert('خطا'); btn.disabled=false; btn.textContent='ورود'; }
};
</script>
</body></html>"""
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>داشبورد · VaslZone</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root{--bg:#060f1d;--card:#0d1b2e;--accent:#EF4444;--border:rgba(239,68,68,0.2);--text:#E8F4FF;--text-m:#7BAED4}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);display:flex}
.sidebar{width:250px;background:#0a1628;border-left:1px solid var(--border);height:100vh;padding:20px;position:fixed}
.main{margin-right:250px;padding:30px;flex:1;width:calc(100% - 250px)}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:30px;padding-bottom:15px;border-bottom:1px solid var(--border)}
.brand img{width:40px;border-radius:10px}
.nav-item{padding:10px;margin:5px 0;cursor:pointer;border-radius:8px;color:var(--text-m);transition:0.2s}
.nav-item:hover, .nav-item.active{background:rgba(239,68,68,0.1);color:var(--accent)}
.section{display:none} .section.active{display:block}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px}
input,select{width:100%;padding:10px;margin-top:5px;background:rgba(0,0,0,0.3);border:1px solid var(--border);color:var(--text);border-radius:8px;font-family:inherit}
button{background:var(--accent);color:#fff;border:none;padding:10px 15px;border-radius:8px;cursor:pointer;font-family:inherit;font-weight:bold}
button:hover{filter:brightness(1.2)}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:15px}
table{width:100%;border-collapse:collapse;margin-top:15px}
th,td{padding:12px;text-align:right;border-bottom:1px solid var(--border)}
.badge{padding:3px 8px;border-radius:12px;font-size:11px;background:rgba(239,68,68,0.1);color:var(--accent)}
.link-box{background:rgba(0,0,0,0.4);padding:10px;border-radius:8px;font-family:monospace;font-size:11px;word-break:break-all;margin:5px 0}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);z-index:999;align-items:center;justify-content:center}
.modal.open{display:flex}
.modal-content{background:var(--card);padding:25px;border-radius:15px;width:400px;border:1px solid var(--border)}
</style>
</head>
<body>
<div class="sidebar">
  <div class="brand"><img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png"><h3>VaslZone</h3></div>
  <div class="nav-item active" onclick="nav('overview')"><i class="ti ti-dashboard"></i> داشبورد</div>
  <div class="nav-item" onclick="nav('links')"><i class="ti ti-link"></i> کانفیگ‌ها</div>
  <div class="nav-item" onclick="nav('groups')"><i class="ti ti-folders"></i> گروه‌ها</div>
  <div class="nav-item" onclick="nav('resellers')"><i class="ti ti-users"></i> نمایندگان</div>
  <div class="nav-item" onclick="nav('ips')"><i class="ti ti-world"></i> IP سراسری</div>
  <div class="nav-item" style="color:var(--accent);margin-top:20px" onclick="logout()"><i class="ti ti-logout"></i> خروج</div>
</div>

<div class="main">
  <div id="overview" class="section active">
    <h2>داشبورد VaslZone</h2>
    <div class="grid-2" style="margin-top:20px">
      <div class="card"><h3>کانفیگ‌ها</h3><h1 id="stat-links">-</h1></div>
      <div class="card"><h3>نمایندگان</h3><h1 id="stat-res">-</h1></div>
    </div>
  </div>

  <div id="links" class="section">
    <h2>مدیریت کانفیگ‌ها</h2>
    <div class="card" style="margin-top:20px">
      <h3>ساخت کانفیگ جدید / گروهی</h3>
      <div class="grid-2">
        <div><label>نام</label><input id="l-name" placeholder="VaslZone-Config"></div>
        <div><label>تعداد (گروهی)</label><input type="number" id="l-count" value="1" min="1"></div>
        <div><label>حجم (GB)</label><input type="number" id="l-gb" value="0" placeholder="0 = نامحدود"></div>
        <div><label>انقضا (روز)</label><input type="number" id="l-exp" value="0" placeholder="0 = نامحدود"></div>
        <div><label>IP (کاما جدا)</label><input id="l-ips" placeholder="خالی = پیش‌فرض"></div>
        <div><label>پورت</label><input type="number" id="l-port" placeholder="خالی = 443"></div>
      </div>
      <div style="margin-top:15px;display:flex;gap:15px;align-items:center">
        <label><input type="checkbox" id="l-pers" style="width:auto"> استفاده شخصی</label>
        <button onclick="createLinks()">ساخت کانفیگ</button>
      </div>
    </div>
    <div class="card" id="links-list">بارگذاری...</div>
  </div>

  <div id="groups" class="section">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2>گروه‌های ساب</h2>
      <button onclick="document.getElementById('m-grp').classList.add('open')">گروه جدید</button>
    </div>
    <div class="card" style="margin-top:20px" id="groups-list">بارگذاری...</div>
  </div>

  <div id="resellers" class="section">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2>نمایندگان</h2>
      <button onclick="document.getElementById('m-res').classList.add('open')">نماینده جدید</button>
    </div>
    <div class="card" style="margin-top:20px" id="resellers-list">بارگذاری...</div>
  </div>

  <div id="ips" class="section">
    <h2>IP سراسری</h2>
    <div class="card" style="margin-top:20px">
      <label>لیست IPها (با کاما جدا کنید)</label><input id="g-ips" placeholder="1.1.1.1, 2.2.2.2">
      <label>پورت سراسری</label><input type="number" id="g-port" placeholder="443">
      <button onclick="saveGlobalIps()" style="margin-top:15px">ذخیره تنظیمات</button>
    </div>
  </div>
</div>
<!-- Modals -->
<div id="m-grp" class="modal"><div class="modal-content">
  <h3>ساخت گروه</h3><input id="g-name" placeholder="نام گروه"><button onclick="createGroup()">ذخیره</button>
  <button style="background:transparent;border:1px solid #fff;margin-top:10px" onclick="document.getElementById('m-grp').classList.remove('open')">بستن</button>
</div></div>

<div id="m-res" class="modal"><div class="modal-content">
  <h3>ساخت نماینده</h3><input id="r-name" placeholder="نام"><input id="r-pw" placeholder="رمز"><input id="r-gb" type="number" placeholder="حجم (GB)"><button onclick="createReseller()">ذخیره</button>
  <button style="background:transparent;border:1px solid #fff;margin-top:10px" onclick="document.getElementById('m-res').classList.remove('open')">بستن</button>
</div></div>

<script>
const api=async(u,m='GET',b=null)=>{
  const o={method:m};if(b){o.headers={'Content-Type':'application/json'};o.body=JSON.stringify(b);}
  const r=await fetch('/api'+u,o);if(r.status===401)location.href='/login';return r.json();
};

function nav(id){
  document.querySelectorAll('.section').forEach(e=>e.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(e=>e.classList.remove('active'));
  event.currentTarget.classList.add('active');
  if(id==='links')loadLinks(); if(id==='groups')loadGroups(); if(id==='resellers')loadResellers(); if(id==='ips')loadGlobalIps();
}

async function init(){
  const r=await fetch('/stats').then(x=>x.json());
  document.getElementById('stat-links').textContent=r.links_count||0;
  document.getElementById('stat-res').textContent=r.resellers_count||0;
}
init();

async function loadLinks(){
  const d=await api('/links');
  let h='<table><tr><th>نام</th><th>وضعیت</th><th>مصرف</th><th>عملیات</th></tr>';
  (d.links||[]).forEach(l=>{
    h+=`<tr><td>${l.label}</td><td><span class="badge">${l.active?'فعال':'غیرفعال'}</span></td><td>${(l.used_bytes/1024/1024).toFixed(1)}MB</td>
    <td><button style="padding:5px;font-size:11px" onclick="prompt('Link:', '${l.vless_link.split('\\n')[0]}')">کپی</button> <button style="background:var(--card);color:red;padding:5px" onclick="delLink('${l.uuid}')">حذف</button></td></tr>`;
  });
  document.getElementById('links-list').innerHTML=h+'</table>';
}

async function createLinks(){
  const b={label:document.getElementById('l-name').value||'VZ', count:document.getElementById('l-count').value, limit_value:document.getElementById('l-gb').value, limit_unit:'GB', expires_days:document.getElementById('l-exp').value, ips:document.getElementById('l-ips').value.split(',').filter(x=>x), port:document.getElementById('l-port').value, is_personal:document.getElementById('l-pers').checked};
  await api('/links/bulk','POST',b); alert('انجام شد'); loadLinks();
}

async function delLink(id){ if(confirm('حذف؟')) {await api('/links/'+id,'DELETE'); loadLinks();} }

async function loadGroups(){
  const d=await api('/subs');
  let h='<table><tr><th>نام</th><th>لینک ساب</th><th>عملیات</th></tr>';
  (d.subs||[]).forEach(s=>{h+=`<tr><td>${s.name}</td><td style="font-size:10px">${s.sub_url}</td><td><button onclick="delSub('${s.sub_id}')" style="background:red">حذف</button></td></tr>`;});
  document.getElementById('groups-list').innerHTML=h+'</table>';
}
async function createGroup() { await api('/subs','POST',{name:document.getElementById('g-name').value}); document.getElementById('m-grp').classList.remove('open'); loadGroups(); }
async function delSub(id) { if(confirm('حذف؟')){await api('/subs/'+id,'DELETE'); loadGroups();} }

async function loadResellers(){
  const d=await api('/resellers');
  let h='<table><tr><th>نام</th><th>حجم کل</th><th>تخصیص</th><th>عملیات</th></tr>';
  (d.resellers||[]).forEach(r=>{h+=`<tr><td>${r.name}</td><td>${r.total_fmt}</td><td>${r.allocated_fmt}</td><td><button onclick="delRes('${r.id}')" style="background:red">حذف</button></td></tr>`;});
  document.getElementById('resellers-list').innerHTML=h+'</table>';
}
async function createReseller() { await api('/resellers','POST',{name:document.getElementById('r-name').value,password:document.getElementById('r-pw').value,limit_gb:document.getElementById('r-gb').value}); document.getElementById('m-res').classList.remove('open'); loadResellers(); }
async function delRes(id) { if(confirm('حذف؟')){await api('/resellers/'+id,'DELETE'); loadResellers();} }

async function loadGlobalIps() { const d=await api('/settings/global-ips'); document.getElementById('g-ips').value=(d.ips||[]).join(','); document.getElementById('g-port').value=d.port||''; }
async function saveGlobalIps() { await api('/settings/global-ips','POST',{ips:document.getElementById('g-ips').value.split(',').filter(x=>x.trim()), port:document.getElementById('g-port').value}); alert('ذخیره شد'); }

function logout() { fetch('/api/logout',{method:'POST'}).then(()=>location.href='/login'); }
</script></body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    return f"""<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>VaslZone Sub</title>
<style>body{{background:#060f1d;color:#fff;font-family:sans-serif;text-align:center;padding:50px;}} .btn{{background:#EF4444;color:#fff;padding:10px;border:none;border-radius:5px;cursor:pointer}}</style></head><body>
<img src="https://uploadkon.ir/uploads/09bd03_26file-00000000ab2071f486cf6128924e8d11.png" width="100" style="border-radius:15px;margin-bottom:20px">
<h2>سابسکرایب VaslZone</h2><p>کد: {uuid_key}</p>
<div id="content">بارگذاری...</div>
<script>
fetch('/api/public/sub/{uuid_key}').then(r=>r.json()).then(d=>{{ 
  if(d.locked) document.getElementById('content').innerHTML='<div>نیاز به رمز</div>'; 
  else document.getElementById('content').innerHTML=d.links.map(l=>'<div style="background:#0a1628;padding:10px;margin:10px;border-radius:5px">'+l.label+' - '+l.used_fmt+' / '+l.limit_fmt+'</div>').join('');
}});
</script></body></html>"""
