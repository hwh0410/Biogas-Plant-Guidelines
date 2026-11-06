"""Second editorial design: generated character interactions, original content retained.
Builds only v1.1-r2. Use --browser for Chromium PDF and QA (requires launch permission).
"""
from pathlib import Path
import argparse,base64,html,json,hashlib,functools,http.server,threading,zipfile,subprocess
from PIL import Image
import fitz
R=Path(__file__).resolve().parents[1];O=R/'output/v1.1-r2';A=R/'assets/illustrations/v1.1-r2'
O.mkdir(exist_ok=True,parents=True)
D=json.loads((R/'content/handbook.json').read_text());ids=['P03','P05','P10'];pages=[next(p for p in D['pages'] if p['id']==i) for i in ids]
def esc(s):return html.escape(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def img(name):
 p=A/(name+'.png');assert p.exists(),f'Missing generated artwork: {p}'
 return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
css='''
@page{size:A4;margin:0}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e6e9e3;color:#253e34;font-family:"PingFang TC","Noto Sans TC",sans-serif;-webkit-font-smoothing:antialiased}a{color:inherit}h1,h2,h3,p,figure{margin:0}.toolbar{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:20px;padding:15px 24px;background:#183f32;color:#fff;font-size:14px}.toolbar a{text-decoration:none}.toolbar button{background:white;border:0;border-radius:4px;padding:7px 13px;color:#183f32;cursor:pointer;font:inherit}.page{width:210mm;height:297mm;background:#fff;margin:24px auto;padding:14mm 17.5mm 12mm;display:flex;flex-direction:column;position:relative;break-after:page;box-shadow:0 5px 24px #1a3a231a}.page:last-child{break-after:auto}.running{display:flex;justify-content:space-between;align-items:center;font-size:8.5pt;letter-spacing:.12em;color:#5a7164;border-bottom:1px solid #ced8ce;padding-bottom:4mm}.running .folio{color:#1f5039;font-size:12pt;letter-spacing:0}.heading{margin:6mm 0 3mm}.chapter{font-size:9pt;color:#597d57;letter-spacing:.1em;margin-bottom:2mm}.heading h2{font-size:25pt;line-height:1.25;font-weight:600;letter-spacing:-.04em}.key{font-size:11.5pt;line-height:1.6;color:#425b4b;margin-top:3mm;max-width:165mm}.visual{margin:0 -4mm 3mm}.scene{height:99mm;position:relative}.scene img{display:block;width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply}.scene svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.label{position:absolute;background:#fffffff2;color:#244d3c;padding:3px 7px;font-size:9pt;line-height:1.3;border-radius:3px;white-space:nowrap;border:1px solid #dce5da}.label.amber{color:#856224;border-color:#d7c9a5}.fig-note{font-size:8.5pt;line-height:1.5;color:#667668;padding:1mm 4mm 0}.voice{font-size:10pt;line-height:1.5;color:#28573b;display:flex;gap:10px;align-items:baseline;margin:1mm 0 4mm}.voice b{white-space:nowrap;font-size:9pt;letter-spacing:.06em}.voice span{border-left:2px solid #a6bc93;padding-left:10px}.legend{display:flex;gap:16px;align-items:center;flex-wrap:wrap;font-size:8.5pt;margin-bottom:1mm}.legend i{display:inline-block;width:18px;border-top:2px solid;margin-right:5px;vertical-align:middle}.legend .gas i{border-top-style:dashed}.blocks{display:grid;grid-template-columns:1fr 1fr;gap:4mm 7mm}.block{border-top:1px solid #d6ded4;padding-top:2.5mm}.block h3{font-size:11pt;font-weight:600;color:#244d3b;margin-bottom:1.5mm}.block p{font-size:10.5pt;line-height:1.55;color:#34463a}.block p+p{margin-top:1.5mm}.warning{margin-top:5mm;padding:3mm 3.5mm;border-left:3px solid #b85843;background:#fbf3ed;font-size:10.5pt;line-height:1.5;color:#873e30}.warning b{margin-right:8px;font-weight:600}.footer{margin-top:auto;padding-top:4mm;display:flex;justify-content:space-between;gap:6mm;color:#647264;font-size:8pt;line-height:1.5}.footer .source{max-width:138mm}.original-tip{display:inline-block;font-size:9pt;color:#31543d;margin-bottom:2mm}.footer .page-id{font-size:12pt;align-self:flex-end;color:#31543d}.cover{background:#f7f8f2}.cover .running{border-color:#d0d9cb}.cover .title{margin-top:10mm}.cover .title .chapter{font-size:10pt;margin-bottom:4mm}.cover h1{font-size:38pt;line-height:1.2;letter-spacing:.02em;font-weight:600;color:#1e4934}.cover .subtitle{font-size:13pt;line-height:1.6;margin-top:5mm}.cover .visual{margin:0 -9mm;width:calc(100% + 18mm)}.cover .scene{height:134mm}.cover .intro{font-size:11pt;line-height:1.7;margin-top:1mm}.contents{display:grid;grid-template-columns:1fr 1fr;gap:3mm 7mm;margin-top:5mm}.contents div{display:flex;justify-content:space-between;border-top:1px solid #cfd9c9;padding-top:2mm;font-size:9.5pt;gap:4mm}.contents small{font-size:8.5pt;color:#667862;white-space:nowrap}.cover .footer{font-size:8.5pt}.compare-labels{display:flex;justify-content:space-around;padding-left:23%;font-size:10pt;color:#446440;margin-bottom:-3mm;position:relative;z-index:1}.compare-labels .watch{color:#926b2d}.p10 .scene{height:103mm}.p05 .scene{height:96mm}
@media print{html{scroll-behavior:auto}body{background:white}.toolbar{display:none}.page{margin:0;box-shadow:none;print-color-adjust:exact;-webkit-print-color-adjust:exact}a{text-decoration:none}.page{break-inside:avoid}}
@media screen and (max-width:820px){.page{width:calc(100% - 24px);height:auto;min-height:0;padding:24px 22px;margin:16px 12px}.running{font-size:11px;letter-spacing:.06em}.heading h2{font-size:28px}.key{font-size:16px;max-width:none}.chapter{font-size:12px}.visual{margin-left:-8px;margin-right:-8px}.scene,.p05 .scene,.p10 .scene{height:auto;aspect-ratio:3/2}.label{font-size:clamp(8px,1.6vw,12px);padding:2px 4px}.fig-note{font-size:12px}.voice{font-size:15px;align-items:flex-start}.voice b{font-size:12px}.block h3{font-size:17px}.block p{font-size:16px}.warning{font-size:16px}.footer{margin-top:25px;font-size:12px}.cover h1{font-size:43px}.cover .subtitle{font-size:17px}.cover .visual{width:calc(100% + 24px);margin:0 -12px}.cover .scene{height:auto;aspect-ratio:3/2}.cover .intro{font-size:16px}.contents div{font-size:14px}.contents small{font-size:12px}.compare-labels{font-size:12px}.cover .footer{font-size:12px}.legend{font-size:12px}}
@media screen and (max-width:560px){.blocks{grid-template-columns:1fr;gap:18px}.contents{grid-template-columns:1fr;gap:12px}.toolbar{gap:14px;font-size:13px}.toolbar b{width:100%;text-align:center}.voice{display:block}.voice span{display:block;margin-top:6px}.heading{margin-top:20px}.compare-labels{font-size:11px}.footer{display:block}.footer .source{max-width:none}.page-id{margin-top:8px}.legend{gap:10px}.cover .title{margin-top:25px}}
'''
def footer(p=None):
 return '<footer class="footer"><div class="source">'+('<span class="original-tip">'+esc(p['tip'])+'</span><br>'+esc(p['source'])+'<br>相關頁：'+esc(p['related']) if p else '給農民、牧場負責人與非環工背景業主的巡檢助手。<br>v1.1 第二輪視覺樣板 · 工程與工安尚待專業審查')+'</div><span class="page-id">'+(p['id'] if p else '2026')+'</span></footer>'
def blockhtml(p):return '<div class="blocks">'+''.join('<section class="block"><h3>'+esc(b['title'])+'</h3>'+''.join('<p>'+esc(v)+'</p>' for v in b['items'])+'</section>' for b in p['blocks'])+'</div><aside class="warning"><b>安全界線</b>'+esc(p['warning'])+'</aside>'
def running(section,folio):return '<div class="running"><span>沼氣場健康檢查手冊　/　'+section+'</span><span class="folio">'+folio+'</span></div>'
def label(x,y,t,extra=''):return f'<span class="label {extra}" style="left:{x}%;top:{y}%">{t}</span>'
def overlay(paths):return '<svg viewBox="0 0 1000 667" preserveAspectRatio="none" aria-hidden="true"><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="context-stroke"/></marker></defs>'+paths+'</svg>'
cover='<article class="page cover" id="cover">'+running('田間巡檢指南','FIELD GUIDE')+'<div class="title"><p class="chapter">從設備現象，找到安全的下一步</p><h1>沼氣場<br>健康檢查手冊</h1><p class="subtitle">跟著巡檢員，一起看懂你的沼氣場。</p></div><figure class="visual"><div class="scene"><img src="'+img('cover')+'" alt="以兩張官方角色原圖重新生成：巡檢員持場區地圖，伸手引導讀者認識厭氧槽與全場設備"></div></figure><p class="intro">先觀察，再比對；留下紀錄，讓異常有人接手。</p><div class="contents">'+''.join('<div><span>'+a+'</span><small>'+b+'</small></div>' for a,b in [('導讀與快篩','P01–P03'),('生物系統','P04–P08'),('沼氣處理與安全','P09–P12'),('發電與實用工具','P13–P20')])+'</div>'+footer()+'</article>'
articles=[cover]
voices={'P03':'先分清楚三條路徑，再找出問題在哪一段。','P05':'我們看的是槽外儀表；剖面只用來幫助理解。','P10':'把處理前後的紀錄放在一起，交給專業人員判讀。'}
for p in pages:
 ident=p['id'];tags='';caption=''
 if ident=='P03':
  tags=label(23,78,'進料')+label(35,24,'厭氧槽')+label(54,9,'儲氣')+label(65,30,'氣體處理')+label(86,33,'發電')+label(72,83,'出料處理')
  tags+=overlay('<path d="M390,500 Q410,470 420,390" fill="none" stroke="#9b7448" stroke-width="3" marker-end="url(#arrow)"/><path d="M490,240 Q540,160 590,150 T680,245 L840,300" fill="none" stroke="#3e7c83" stroke-width="3" stroke-dasharray="9 7" marker-end="url(#arrow)"/><path d="M490,400 Q540,480 700,510" fill="none" stroke="#657d47" stroke-width="3" marker-end="url(#arrow)"/>')
  caption='<div class="legend"><span style="color:#9b7448"><i></i>物料</span><span class="gas" style="color:#3e7c83"><i></i>沼氣</span><span style="color:#657d47"><i></i>出料</span></div>流程模型示意；儲氣、脫硫與脫水順序依案場設計。'
 elif ident=='P05':
  tags=label(70,63,'泡沫／浮渣','amber')+label(75,88,'沉積增加','amber')
  caption='概念剖面，非開槽觀察。正常基準及異常程度須由本場資料與專業人員確認。'
 else:
  tags=label(5,39,'A　前端量測')+label(78,34,'B　後端量測')
  tags+=overlay('<path d="M30,500 L280,500" fill="none" stroke="#3e7c83" stroke-width="3" marker-end="url(#arrow)"/><path d="M580,250 L800,250" fill="none" stroke="#3e7c83" stroke-width="3" marker-end="url(#arrow)"/>')
  tags+=overlay('<path d="M140,288 L230,340 M860,270 L865,322" fill="none" stroke="#8b9d85" stroke-width="1.5"/>')
  caption='乾式吸附式範例；A／B 為既有密閉量測位置，須工程確認。曲線為示意，非實測值。'
 comparison='<div class="compare-labels"><span>正常示意 · 以本場基準判讀</span><span class="watch">異常示意 · 需要進一步確認</span></div>' if ident=='P05' else ''
 articles.append('<article class="page '+ident.lower()+'" id="'+ident+'">'+running(esc(p['chapter']),ident)+'<header class="heading"><p class="chapter">'+{'P03':'先認識全場','P05':'把趨勢放在一起看','P10':'看前後紀錄，不只看一個數字'}[ident]+'</p><h2>'+esc(p['title'])+'</h2><p class="key">'+esc(p['key'])+'</p></header><figure class="visual">'+comparison+'<div class="scene"><img src="'+img(ident)+'" alt="官方同角色新生成情境：'+{'P03':'在全場模型旁指向厭氧槽','P05':'在封閉厭氧槽外查看既有儀表，對照正常異常概念剖面','P10':'觀察後端量測顯示並在平板記錄，未接觸管線'}[ident]+'">'+tags+'</div><figcaption class="fig-note">'+caption+'</figcaption></figure><aside class="voice"><b>巡檢員提醒</b><span>'+voices[ident]+'</span></aside>'+blockhtml(p)+footer(p)+'</article>')
markup='<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>沼氣場健康檢查手冊｜第二輪視覺樣板</title><style>'+css+'</style></head><body><nav class="toolbar" aria-label="樣板頁面導覽"><b>第二輪視覺樣板</b>'+''.join('<a href="#'+i+'">'+('封面' if i=='cover' else i)+'</a>' for i in ['cover']+ids)+'<a href="Biogas-Plant-Health-Check-v1.1-r2.pdf" download>下載 PDF</a><button onclick="print()">列印四頁</button></nav><main>'+''.join(articles)+'</main></body></html>'
(O/'samples.html').write_text(markup);web=R/'web/v1.1-r2';web.mkdir(exist_ok=True);(web/'index.html').write_text(markup.replace('href="Biogas-Plant-Health-Check-v1.1-r2.pdf"','href="../../output/v1.1-r2/Biogas-Plant-Health-Check-v1.1-r2.pdf"'))
report={'design':'v1.1-r2','content_sha256':sha(R/'content/handbook.json'),'html_sha256':sha(O/'samples.html'),'browser':'not run','technical_review':'pending','character_review':'Manual comparison to both official references: helmet leaf, dark faceplate, lime digital eyes, gauge/leaf emblem, green rounded body and short proportions consistent; poses and lighting adapted to scenes. No crop assets used.','assets':[]}
for name in ['cover']+ids:
 p=A/(name+'.png');report['assets'].append({'file':str(p.relative_to(R)),'sha256':sha(p),'pixels':Image.open(p).size,'prompt':str((A/'prompts'/(name+'.txt')).relative_to(R)),'reference_images':['assets/mascot/reference/mascot-character-sheet-v0.1.png','assets/mascot/reference/mascot-pose-sheet-v0.1.png'],'tool':'built-in image_gen.imagegen','mascot_method':'reference-conditioned new scene generation; not crop'})
if not argparse.ArgumentParser().parse_known_args()[1].count('--browser'):
 (O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('HTML generated; run with --browser for PDF and QA');raise SystemExit()
from playwright.sync_api import sync_playwright
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();page=b.new_page(viewport={'width':1200,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'/output/v1.1-r2/samples.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
  report['artwork_effective_dpi']=page.locator('.scene img').evaluate_all('imgs=>imgs.map(i=>({alt:i.alt,dpi:Math.round(Math.min(i.naturalWidth/(i.clientWidth/96),i.naturalHeight/(i.clientHeight/96)))}))')
  assert page.locator('.page').count()==4
  assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  report['screen_overflow']=page.evaluate('''()=>Array.from(document.querySelectorAll('.page')).filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>({id:e.id,scroll:e.scrollHeight,client:e.clientHeight}))''');assert not report['screen_overflow'],report['screen_overflow']
  for ident in ['cover']+ids:
   page.locator('.toolbar a[href="#'+ident+'"]').click();assert page.evaluate('location.hash')=='#'+ident
   page.locator('#'+ident).screenshot(path=str(O/(ident+'.png')))
  for width in [390,768]:
   page.set_viewport_size({'width':width,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'mobile overflow'
   for ident in ['cover']+ids:
    assert page.locator('#'+ident).evaluate('e=>e.scrollWidth<=e.clientWidth+1')
   page.locator('#P10').screenshot(path=str(O/f'mobile-{width}.png'))
  report['mobile_reflow_widths']=[390,768]
  page.set_viewport_size({'width':1200,'height':1100});page.emulate_media(media='print')
  report['print_overflow']=page.evaluate('''()=>Array.from(document.querySelectorAll('.page')).filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>({id:e.id,scroll:e.scrollHeight,client:e.clientHeight}))''');assert not report['print_overflow'],report['print_overflow']
  pdfpath=O/'Biogas-Plant-Health-Check-v1.1-r2.pdf';page.pdf(path=str(pdfpath),print_background=True,prefer_css_page_size=True)
  doc=fitz.open(pdfpath);assert len(doc)==4,len(doc);norm=lambda s:''.join(s.split())
  for i,p in enumerate(pages,1):
   t=norm(doc[i].get_text())
   for value in [p['title'],p['key'],p['warning'],p['source'],p['tip']]+[v for block in p['blocks'] for v in block['items']]:assert norm(value) in t,(p['id'],value)
  report['pdf_pages']=4;report['pdf_original_text']='titles, keys, all eight items, warnings, tips and sources verified'
  assert all(abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1 for p in doc)
  # Native screenshots, one contact sheet, no screenshot-to-PDF conversion.
  sheet=Image.new('RGB',(840,1188),'#e6e9e3')
  for i,p in enumerate(doc):
   pix=p.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);sheet.paste(im,((i%2)*420,(i//2)*594))
  sheet.save(O/'contact-sheet.png');doc.close()
  page.emulate_media(media='screen');page.goto((O/'samples.html').as_uri());assert page.locator('.page').count()==4;assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  report['offline_file']=True;assert not errors,errors;report['page_errors']=errors;b.close();report['browser']='passed'
finally:server.shutdown()
# Preserve old editions, not just JSON.
checks={}
for folder in ['content','web','output','qa']:
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only','3a45bda',folder],cwd=R,text=True).splitlines():
  old=subprocess.check_output(['git','show','3a45bda:'+path],cwd=R);assert (R/path).read_bytes()==old,'Prior edition modified: '+path;checks[path]=hashlib.sha256(old).hexdigest()
report['prior_edition_files_unchanged']=len(checks)
report['publication_limit']='Artwork about 200–230 effective dpi; style proof, not 300 dpi press-ready. AI equipment and instrument traces require professional review.'
(O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
