from fastapi.responses import HTMLResponse

def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب حرفه‌ای"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VaslZone Sub</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Vazirmatn',sans-serif;background:#060a14;color:#EFF4FF;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
.bg{{position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 50% -10%,rgba(59,124,246,0.12),transparent 70%),#060a14;z-index:0}}
.grd{{position:fixed;inset:0;background-image:linear-gradient(rgba(59,124,246,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(59,124,246,0.025) 1px,transparent 1px);background-size:50px 50px;z-index:0}}
.wrap{{position:relative;z-index:10;width:100%;max-width:500px}}
.card{{background:rgba(12,20,40,0.95);border:1px solid rgba(59,124,246,0.15);border-radius:24px;padding:32px 28px;backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,0.5),0 0 40px rgba(59,124,246,0.05)}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}}
.brand{{display:flex;align-items:center;gap:12px}}
.brand i{{font-size:28px;color:#3B7CF6}}
.brand div{{font-size:16px;font-weight:800;color:#EFF4FF;letter-spacing:-.02em}}
.brand span{{display:block;font-size:9px;color:#48577A;font-weight:500;letter-spacing:.1em}}
.info{{text-align:center;margin-bottom:24px;padding:16px;background:rgba(59,124,246,0.05);border:1px solid rgba(59,124,246,0.1);border-radius:14px}}
.info i{{font-size:16px;color:#3B7CF6;margin-bottom:8px;display:block}}
.info h2{{font-size:18px;font-weight:800;margin-bottom:4px}}
.info p{{font-size:11px;color:#7BAED4;line-height:1.8}}
.loading{{text-align:center;padding:50px 0}}
.loading i{{font-size:40px;color:#3B7CF6;display:block;margin-bottom:14px;animation:spin 1.2s linear infinite}}
.loading p{{font-size:12px;color:#48577A}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.ft{{text-align:center;margin-top:24px;font-size:9.5px;color:#48577A;letter-spacing:.05em}}
.ft a{{color:#3B7CF6;font-weight:700;text-decoration:none}}
</style>
</head>
<body>
<div class="bg"></div><div class="grd"></div>
<div class="wrap">
<div class="card">
<div class="top">
<div class="brand"><i class="ti ti-brand-speedtest"></i><div>VaslZone<span>SUBSCRIPTION</span></div></div>
<i class="ti ti-moon" style="font-size:18px;color:#7BAED4;cursor:pointer" onclick="document.documentElement.toggleAttribute('data-dark')"></i>
</div>
<div class="info"><i class="ti ti-link"></i><h2>لینک اشتراک</h2><p>برای استفاده در اپلیکیشن‌های V2Ray لینک زیر را کپی کنید</p></div>
<div class="loading" id="loading"><i class="ti ti-loader-2"></i><p>در حال دریافت اطلاعات...</p></div>
<div id="content" style="display:none">
<div style="background:rgba(0,0,0,0.25);border:1px solid rgba(59,124,246,0.12);border-radius:14px;padding:14px 16px;margin-bottom:16px;word-break:break-all;font-family:monospace;font-size:11px;line-height:1.8;color:#7BAED4;max-height:100px;overflow-y:auto" id="suburl">—</div>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<button class="btn" onclick="copySub()" style="flex:1;padding:12px;border-radius:12px;border:none;background:#3B7CF6;color:#fff;font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 4px 16px rgba(59,124,246,0.3)"><i class="ti ti-copy"></i> کپی لینک</button>
<button class="btn" onclick="showQR()" style="flex:1;padding:12px;border-radius:12px;border:1px solid rgba(59,124,246,0.2);background:transparent;color:#7BAED4;font-family:inherit;font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px"><i class="ti ti-qrcode"></i> QR Code</button>
</div>
</div>
<div class="ft">VaslZone Gateway · <a href="https://t.me/VaslZone" target="_blank">@VaslZone</a></div>
</div>
</div>
<script>
const key='{uuid_key}';
let subUrl='';
async function init(){{
try{{
const r=await fetch('/api/public/sub/'+key);const d=await r.json();
if(d.locked){{document.getElementById('loading').innerHTML='<i class="ti ti-lock" style="font-size:32px;color:#EF4444"></i><p style="color:#EF4444">این گروه رمز دارد</p>';return}}
document.getElementById('loading').style.display='none';
document.getElementById('content').style.display='block';
subUrl=d.sub_url||(location.protocol+'//'+location.host+'/sub-group/'+key);
document.getElementById('suburl').textContent=subUrl;
}}catch(e){{document.getElementById('loading').innerHTML='<i class="ti ti-alert-circle" style="color:#EF4444"></i><p>خطا</p>'}}
}}
function copySub(){{navigator.clipboard.writeText(subUrl).then(()=>alert('کپی شد'))}}
function showQR(){{window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(subUrl),'_blank')}}
init();
</script>
</body></html>"""
