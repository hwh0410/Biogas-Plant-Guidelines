"""Build full 21 illustrated pages. No image generation API calls; consumes 21 original PNGs.
--browser exports checked PDF and 21 PNGs; --package packages only matching successful QA.
"""
from pathlib import Path
import argparse,ast,base64,html,json,hashlib,http.server,threading,functools,subprocess,zipfile,io,os,shutil,sys
R=Path(__file__).resolve().parents[1];A=R/'assets/illustrations/v1.1-full21'
parser=argparse.ArgumentParser();parser.add_argument('--browser',action='store_true');parser.add_argument('--package',action='store_true')
parser.add_argument('--output-dir',type=Path,default=R/'output/v1.1-full21')
parser.add_argument('--pdftoppm',default=os.environ.get('PDFTOPPM','pdftoppm'),help='Poppler executable path (or PDFTOPPM environment variable)')
parser.add_argument('--font',type=Path,help='Contact sheet TrueType/OpenType font')
parser.add_argument('--renderer',choices=['poppler','pymupdf'],default='poppler',help='Explicit fallback when Poppler is unavailable')
args=parser.parse_args();O=args.output_dir.resolve();O.mkdir(parents=True,exist_ok=True)
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
try:
 from PIL import Image,ImageDraw,ImageFont
 import fitz
except ImportError as exc:
 raise SystemExit('Missing build dependency: '+str(exc)+'. Install requirements-full21-windows.txt in a Windows venv.')
# Explicit UTF-8 also works on Windows systems whose locale uses Big5/CP950.
def contact_font():
 candidates=[args.font] if args.font else [Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/msjh.ttc',Path('/Library/Fonts/Arial Unicode.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
 for candidate in candidates:
  if candidate and candidate.is_file():return ImageFont.truetype(str(candidate),16)
 raise SystemExit('Contact sheet font unavailable; provide --font PATH.')
poppler=None
if args.browser:
 poppler=shutil.which(args.pdftoppm)
 if args.renderer=='poppler' and not poppler:raise SystemExit('Poppler pdftoppm not found. Set PDFTOPPM, pass --pdftoppm PATH, or explicitly use --renderer pymupdf.')
 font=contact_font()
web=(R/'web/v1.1-full21') if O==R/'output/v1.1-full21' else O/'web'
baseline={p:hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['assets','content','output','web','qa'] for p in (R/folder).rglob('*') if p.is_file() and not p.is_relative_to(O) and not p.is_relative_to(web)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s):return html.escape(s)
D=json.loads((R/'content/handbook.json').read_text(encoding='utf-8-sig'));ids=['cover']+[p['id'] for p in D['pages']];assert len(set(ids))==21
expected={'mascot-character-sheet-v0.1.png':'b546e162beb2bdffdc25b128cc900cf60e572cc41c5adf081b42dc4cb7570a63','mascot-pose-sheet-v0.1.png':'9c694a3d5678751225be82cd69e5446a1b99a758682106333c79ae5b87cce06f'}
for name,h in expected.items():assert sha(R/'assets/mascot/reference'/name)==h
if args.package:
 report=json.loads((O/'qa-report.json').read_text(encoding='utf-8-sig'));assert report['browser']=='passed';assert report['html_sha256']==sha(O/'handbook.html');assert report['pdf_sha256']==sha(O/'Biogas-Plant-v1.1-full21.pdf')
 for a in report['assets']:assert sha(R/a['file'])==a['sha256']
 assert len({a['sha256'] for a in report['assets']})==21
 pngs=sorted((O/'pages').glob('*.png'));assert len(pngs)==21
 report['final_png_sha256']={p.name:sha(p) for p in pngs}
 report['png_dimensions']={p.name:Image.open(p).size for p in pngs}
 report.setdefault('visual_qa','pending human inspection of this build')
 (O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 with zipfile.ZipFile(O/'21-original-illustrations.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in A.rglob('*'):
   if p.is_file():z.write(p,str(p.relative_to(A)))
  for name in expected:z.write(R/'assets/mascot/reference'/name,'character-reference/'+name)
 with zipfile.ZipFile(O/'21-complete-pages.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in pngs:z.write(p,p.name)
  z.write(O/'README.md','README.md')
 with zipfile.ZipFile(O/'Biogas-Plant-v1.1-full21-bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in O.rglob('*'):
   if p.is_file() and p.suffix!='.zip':z.write(p,str(p.relative_to(O)))
  for p in A.rglob('*'):
   if p.is_file():z.write(p,str(p.relative_to(R)))
  for path in ['scripts/build_full21.py','scripts/build_v11_r2.py','requirements.txt','content/handbook.json','docs/full21-generation-review.md']:
   z.write(R/path,path)
 print('Packaged complete 21-page edition');raise SystemExit()
for i in ids:assert (A/(i+'.png')).is_file(),'Missing generated original '+i
# Adopt the approved second-round typographic foundation, then specialize all 20 pages.
module=ast.parse((R/'scripts/build_v11_r2.py').read_text(encoding='utf-8-sig'));css=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='css' for t in n.targets))
css=css.replace('"Noto Sans TC",sans-serif','"Noto Sans TC","Microsoft JhengHei",sans-serif')
css+='''
.page .scene{height:94mm}.page.cover .scene{height:133mm}.full-key{margin-top:2mm}.table-wrap{margin:1mm 0 4mm}table{border-collapse:collapse;width:100%;font-size:10pt;line-height:1.4;table-layout:fixed}thead{background:#edf2e7;color:#294f38}th{text-align:left;padding:2mm 2.5mm;border-bottom:1px solid #91aa87;font-weight:600}td{padding:1.7mm 2.5mm;border-bottom:1px solid #d7e0d2;vertical-align:top;overflow-wrap:anywhere}th:nth-child(1){width:30%}th:nth-child(2){width:50%}th:nth-child(3){width:20%}.has-table .heading{margin-bottom:1mm}.has-table .scene{height:33mm}.has-table .visual{margin-bottom:1mm}.has-table .fig-note{font-size:8pt}.has-table .block{padding-top:1.5mm}.has-table .blocks{gap:2mm 5mm}.has-table .block p{font-size:10pt;line-height:1.4}.has-table .block h3{font-size:10.5pt;margin-bottom:1mm}.has-table .warning{margin-top:3mm}.has-table .footer{padding-top:2mm}.has-table .original-tip{margin-bottom:1mm}.has-table .table-wrap{margin-bottom:3mm}.form-line{font-size:10.5pt;margin:2mm 0 3mm}.formula{font-size:10.5pt;line-height:1.5;background:#f2f5ed;padding:3mm;margin-top:3mm}.p19 td{height:7.2mm;padding-top:1.8mm;padding-bottom:1.8mm}.p19 th:nth-child(1){width:37%}.p19 th:nth-child(2){width:33%}.p19 th:nth-child(3){width:30%}.p19 .scene{height:26mm}.p19 .blocks{gap:2mm 5mm}.p18 td{font-size:9.5pt;padding:1.5mm 2mm}.p18 th:nth-child(1){width:38%}.p18 th:nth-child(2){width:42%}.p18 th:nth-child(3){width:20%}.original-tip{display:inline-block;font-size:9pt;color:#31543d;margin-bottom:2mm}.flow-strip,.compare-strip{display:flex;justify-content:space-around;gap:8px;font-size:8.5pt;line-height:1.5;margin:2mm 4mm 0;padding-top:1mm;border-top:1px solid #d7dfd2}.flow-strip span:first-child{color:#8f683f}.flow-strip span:nth-child(2){color:#3e747e}.flow-strip span:nth-child(3){color:#5f7845}.compare-strip span:last-child{color:#91682e}.note-line{font-size:8.5pt;color:#667668}.toolbar input{max-width:190px;border:1px solid #c6d0c4;border-radius:4px;padding:6px 8px;font:inherit}.page[hidden]{display:none}
@media screen and (max-width:820px){.page .scene,.page.cover .scene,.has-table .scene,.p19 .scene{height:auto;aspect-ratio:3/2}.has-table .block p{font-size:16px;line-height:1.55}.has-table .block h3{font-size:17px}.has-table .fig-note{font-size:12px}.table-wrap{overflow-x:auto}table{font-size:14px;min-width:550px}.form-line{font-size:15px}.formula{font-size:15px}.p18 td{font-size:14px}.p19 td{height:38px}.original-tip{font-size:13px}.flow-strip,.compare-strip{font-size:12px;flex-wrap:wrap}}
@media print{.page[hidden]{display:flex!important}}
'''
def annotations(ident):
 if ident=='P03':
  return '<div class="flow-strip"><span>進料 → 厭氧槽</span><span>沼氣 → 處理／儲氣 → 發電</span><span>出料 → 核准處理</span></div>'
 if ident=='P05':
  return '<div class="compare-strip"><span>正常示意：以本場基準判讀</span><span>異常示意：泡沫／浮渣／沉積需確認</span></div>'
 if ident=='P06':
  return '<div class="flow-strip diagnosis"><span>核對紀錄</span><span>比對進料／槽況／用氣</span><span>通知場務判讀</span></div>'
 if ident=='P10':
  return '<div class="compare-strip"><span>A　既有前端量測紀錄</span><span>B　既有後端量測紀錄</span></div>'
 return ''
def artwork(i):
 buffer=io.BytesIO()
 # Encode only the display copy; immutable generated PNG originals stay untouched.
 Image.open(A/(i+'.png')).convert('RGB').save(buffer,format='JPEG',quality=94,subsampling=0)
 return 'data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()
def running(p):return '<div class="running"><span>沼氣場健康檢查手冊　/　'+esc(p['chapter'])+'</span><span class="folio">'+p['id']+'</span></div>'
def footer(p):return '<footer class="footer"><div class="source"><span class="original-tip">'+esc(p['tip'])+'</span><br>'+esc(p['source'])+'<br>相關頁：'+esc(p['related'])+'</div><span class="page-id">'+p['id']+'</span></footer>'
def table(p):
 t=p['table'];return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(v)+'</th>' for v in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(v or '＿＿＿＿')+'</td>' for v in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
notes={
'P01':'先觀察、記錄、比對，再尋求協助；燈號不代表現場安全許可。',
'P02':'十題用來整理待確認項目；未知不能當成正常。',
'P03':'全場功能模型；設備配置及處理順序依案場設計，不是施工圖。',
'P04':'進料與前處理範例；觀察僅限既有安全位置及讀值。',
'P05':'同槽型概念剖面；不得開蓋觀察。泡沫／沉積不是通用判定門檻。',
'P06':'核對同期間資料，再區分進料、槽況、用氣及設備影響；不憑圖診斷。',
'P07':'密閉分析系統範例；曲線無實測數值，不代表允收或環境安全。',
'P08':'出料接收及處理示意；不能把沼渣、沼液視為可直接排放。',
'P09':'雙膜儲氣設備範例；外膜形狀不等於內膜儲氣量。',
'P10':'乾式吸附式範例；密閉量測位置須工程確認，曲線非實測。',
'P11':'封閉管線與密閉排水器概念示意；剖面並非實際開孔。',
'P12':'危險先撤離；通報須在安全地點，不自行返回或進入槽池。',
'P13':'只核對既有指示與授權條件；圖示不提供通用啟動順序。',
'P14':'保存首次警報及反應；不跨接、不強開閥、不反覆啟動。',
'P15':'記下第一個停機警報；不取消保護或反覆重置。',
'P16':'時數、功率及發電量分別記錄；曲線與時鐘不代表實測資料。',
'P17':'保養紀錄情境；不代表讀者已具拆修或能源隔離資格。',
'P18':'依症狀找方向；危險類直接查 P12／P20，不繼續一般排查。',
'P19':'本頁為補充巡檢表；頻率、項目與資格由案場核定。',
'P20':'安全地點求援示意；場址、入口及聯絡資料須事先填妥。'}
alt={p['id']:p['title']+'：以兩張官方原圖參考生成同一位巡檢員參與本頁情境' for p in D['pages']}
cover='<article class="page cover" id="cover"><div class="running"><span>田間巡檢指南　/　BIOGAS FIELD GUIDE</span><span class="folio">v1.1</span></div><div class="title"><p class="chapter">看現象・找方向・安全確認・專業求援</p><h1>沼氣場<br>健康檢查手冊</h1><p class="subtitle">跟著巡檢員，走過你的沼氣場。</p></div><figure class="visual"><div class="scene"><img src="'+artwork('cover')+'" alt="官方同角色新生成的封面場景：持地圖引導讀者認識全場設備"></div></figure><p class="intro">先觀察，再比對；留下紀錄，讓異常有人接手。</p><div class="contents">'+''.join('<div><span>'+a+'</span><small>'+b+'</small></div>' for a,b in [('導讀與快篩','P01–P03'),('生物系統','P04–P08'),('沼氣處理與安全','P09–P12'),('發電與實用工具','P13–P20')])+'</div><footer class="footer"><div>會議討論版｜非正式操作程序<br>封面＋20 頁・設備及安全程序待專業審查</div><span class="page-id">2026</span></footer></article>'
articles=[cover]
for p in D['pages']:
 ident=p['id'];has=' has-table' if p.get('table') else ''
 fig='<figure class="visual"><div class="scene"><img src="'+artwork(ident)+'" alt="'+esc(alt[ident])+'"></div><figcaption class="fig-note">'+notes[ident]+'</figcaption>'+annotations(ident)+'</figure>'
 # Tables remain exact editable content instead of invented AI characters.
 body=('<p class="form-line">'+esc(p['form'])+'</p>' if p.get('form') else '')+(table(p) if p.get('table') else '')+'<div class="blocks">'+''.join('<section class="block"><h3>'+esc(b['title'])+'</h3>'+''.join('<p>'+esc(v)+'</p>' for v in b['items'])+'</section>' for b in p['blocks'])+'</div>'
 if p.get('formula'):body+='<p class="formula">'+esc(p['formula'])+'</p>'
 body+='<aside class="warning"><b>安全界線</b>'+esc(p['warning'])+'</aside>'
 articles.append('<article class="page '+ident.lower()+has+'" id="'+ident+'">'+running(p)+'<header class="heading"><h2>'+esc(p['title'])+'</h2><p class="key">'+esc(p['key'])+'</p></header>'+fig+body+footer(p)+'</article>')
js="""document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.trim();document.querySelectorAll('.page').forEach(p=>p.hidden=!!q&&!p.textContent.includes(q));});"""
markup='<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>沼氣場健康檢查手冊｜21頁圖解版</title><style>'+css+'</style></head><body><nav class="toolbar"><b>封面＋20 頁圖解版</b><a href="#cover">封面</a><a href="#P01">導讀</a><a href="#P04">生物</a><a href="#P09">燃氣</a><a href="#P13">發電</a><a href="#P18">工具</a><label>搜尋 <input id="search" type="search" aria-label="搜尋內容"></label><a href="Biogas-Plant-v1.1-full21.pdf" download>PDF</a><button onclick="print()">列印全書</button></nav><main>'+''.join(articles)+'</main><script>'+js+'</script></body></html>'
(O/'handbook.html').write_text(markup,encoding='utf-8')
web.mkdir(parents=True,exist_ok=True)
pdf_link=Path(os.path.relpath(O/'Biogas-Plant-v1.1-full21.pdf',web)).as_posix()
(web/'index.html').write_text(markup.replace('href="Biogas-Plant-v1.1-full21.pdf"','href="'+pdf_link+'"'),encoding='utf-8')
report={'edition':'v1.1-full21','content_sha256':sha(R/'content/handbook.json'),'html_sha256':sha(O/'handbook.html'),'browser':'not run','engineering_review':'pending','official_reference_hashes':expected,'assets':[{'id':i,'file':str((A/(i+'.png')).relative_to(R)),'sha256':sha(A/(i+'.png')),'pixels':Image.open(A/(i+'.png')).size,'prompt':str((A/'prompts'/(i+'.txt')).relative_to(R))} for i in ids]}
if not args.browser:
 (O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('HTML prepared; --browser required for PDF / PNG');raise SystemExit()
from playwright.sync_api import sync_playwright
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();page=b.new_page(viewport={'width':1200,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((O/'handbook.html').as_uri(),wait_until='networkidle');page.evaluate('document.fonts.ready');assert page.locator('.page').count()==21
  assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  page.locator('#search').fill('發不動');assert page.locator('.page[hidden]').count()>0
  page.emulate_media(media='print');assert page.evaluate("Array.from(document.querySelectorAll('.page')).every(e=>getComputedStyle(e).display==='flex')")
  page.emulate_media(media='screen');page.locator('#search').fill('')
  report['screen_overflow']=page.evaluate("Array.from(document.querySelectorAll('.page')).filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>({id:e.id,scroll:e.scrollHeight,client:e.clientHeight}))");assert not report['screen_overflow'],report['screen_overflow']
  for width in [390,768]:
   page.set_viewport_size({'width':width,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   for ident in ['P02','P09','P12','P19']:page.locator('#'+ident).screenshot(path=str(O/f'mobile-{width}-{ident}.png'))
  report['mobile_widths']=[390,768]
  page.set_viewport_size({'width':1200,'height':1100});page.emulate_media(media='print')
  report['print_overflow']=page.evaluate("Array.from(document.querySelectorAll('.page')).filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>({id:e.id,scroll:e.scrollHeight,client:e.clientHeight}))");assert not report['print_overflow'],report['print_overflow']
  pdf=O/'Biogas-Plant-v1.1-full21.pdf';page.pdf(path=str(pdf),print_background=True,prefer_css_page_size=True)
  doc=fitz.open(pdf);assert len(doc)==21,len(doc);norm=lambda s:''.join(s.split())
  for i,p in enumerate(D['pages'],1):
   t=norm(doc[i].get_text());values=[p[k] for k in ['title','key','warning','source','tip','related']]+[v for block in p['blocks'] for v in block['items']]
   if p.get('table'):values+=p['table']['headers']+[v for row in p['table']['rows'] for v in row if v]
   if p.get('form'):values.append(p['form'])
   if p.get('formula'):values.append(p['formula'])
   for v in values:assert norm(v) in t,(p['id'],v)
  report['pdf_pages']=len(doc);assert all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 for p in doc);doc.close()
  page.emulate_media(media='screen');page.goto((O/'handbook.html').as_uri());assert page.locator('.page').count()==21;assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  assert not errors,errors;report['page_errors']=errors;report['browser']='passed';b.close()
finally:server.shutdown()
# Render publication pages through Poppler at 200 dpi. These 21 PNGs are the requested deliverables.
render=O/'pages';render.mkdir(exist_ok=True)
if args.renderer=='poppler':
 subprocess.run([poppler,'-r','200','-png',str(pdf),str(render/'page')],check=True,timeout=300)
 for i,ident in enumerate(ids,1):
  p=render/f'page-{i:02}.png';assert p.exists(),p;p.replace(render/(ident+'.png'))
else:
 with fitz.open(pdf) as rendered:
  for ident,p in zip(ids,rendered):p.get_pixmap(dpi=200,alpha=False).save(render/(ident+'.png'))
report['renderer']=args.renderer
# Font resolved during preflight.
for start in [0,7,14]:
 sheet=Image.new('RGB',(7*213,330),'#e5e9e1');draw=ImageDraw.Draw(sheet)
 for j,ident in enumerate(ids[start:start+7]):
  im=Image.open(render/(ident+'.png'));im.thumbnail((205,294));sheet.paste(im,(j*213+4,4));draw.text((j*213+8,303),ident,font=font,fill='#244d39')
 sheet.save(O/f'contact-{start//7+1}.png')
atlas=Image.new('RGB',(3*500,7*360),'#e5e9e1');paint=ImageDraw.Draw(atlas)
for i,ident in enumerate(ids):
 art=Image.open(A/(ident+'.png'));art.thumbnail((490,327));atlas.paste(art,((i%3)*500+5,(i//3)*360+4));paint.text(((i%3)*500+8,(i//3)*360+333),ident,font=font,fill='#244d39')
atlas.save(O/'all-21-illustrations.png')
# All previous completed editions remain unchanged.
count=0
for path,h in baseline.items():
 assert path.is_file() and sha(path)==h,'Preserved file changed: '+str(path)
 count+=1
report['previous_files_unchanged']=count;report['pdf_full_text']='all 20 pages: headings, key, every item, full warnings, tips, sources, related pages, tables, form and formula verified'
report['final_png_count']=len(list(render.glob('*.png')));assert report['final_png_count']==21
report['png_resolution']='A4 at 200 dpi; main artwork native resolution recorded separately, not a 300 dpi press-ready claim'
report['pdf_sha256']=sha(pdf);report['character_review']='Original PNGs unchanged by hash; historical character review in docs/full21-generation-review.md. No image generation in this build.';report['visual_qa']='pending inspection of this build';(O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='assets'},ensure_ascii=False,indent=2))
