"""Four-page v1.1 prototype. Shared point-coordinate scene -> HTML and native PDF.
Requires Pillow + PyMuPDF. Never writes v1 files. No generation API calls.
"""
from pathlib import Path
import argparse,base64,json,hashlib,html,math
from PIL import Image
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/v1.1'; OUT.mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def uri(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
DATA=json.loads((ROOT/'content/handbook.json').read_text())
ASSET=ROOT/'assets/illustrations'
EXPECTED={'mascot-character-sheet-v0.1.png':'b546e162beb2bdffdc25b128cc900cf60e572cc41c5adf081b42dc4cb7570a63','mascot-pose-sheet-v0.1.png':'9c694a3d5678751225be82cd69e5446a1b99a758682106333c79ae5b87cce06f'}
for name,h in EXPECTED.items():assert digest(ROOT/'assets/mascot/reference'/name)==h
# Exact rectangular extraction authorized by task; no redraw / recolor / AI alteration.
master=Image.open(ROOT/'assets/mascot/reference/mascot-pose-sheet-v0.1.png')
boxes={'guide':(66,153,357,494),'map':(413,153,685,494),'inspect':(756,153,1049,494),'record':(1104,153,1401,494),'think':(58,592,336,942),'ok':(409,592,698,942),'watch':(742,592,1048,942),'stop':(1062,592,1420,942)}
poses=ROOT/'assets/mascot/poses';poses.mkdir(exist_ok=True)
for name,box in boxes.items():master.crop(box).save(poses/(name+'-v1.1.png'))
(poses/'manifest.json').write_text(json.dumps({'source':'../reference/mascot-pose-sheet-v0.1.png','source_sha256':EXPECTED['mascot-pose-sheet-v0.1.png'],'reference_character_sha256':EXPECTED['mascot-character-sheet-v0.1.png'],'method':'Exact pixel crops; white background retained; no redraw.','crops':boxes},ensure_ascii=False,indent=2))
GREEN='#245b47';INK='#273c35';MUTED='#52665c';GOLD='#b98334';RED='#9c342f';BG='#f7f6f0'
W,H=595.276,841.89
FONT='/Library/Fonts/Arial Unicode.ttf'
scenes=[]
def new(ident):
 s={'id':ident,'elements':[]};scenes.append(s);return s

def rect(s,x,y,w,h,color):s['elements'].append(dict(kind='rect',x=x,y=y,w=w,h=h,color=color))
def text(s,x,y,w,h,t,size=11,color=INK,bold=False):s['elements'].append(dict(kind='text',x=x,y=y,w=w,h=h,t=t,size=size,color=color,bold=bold))
def image(s,x,y,w,h,p,alt):
 assert p.exists(),f'Missing raster artwork: {p}; import using scripts/import_illustration.py. No SVG replacement allowed.'
 s['elements'].append(dict(kind='image',x=x,y=y,w=w,h=h,path=p,alt=alt))
def line(s,pts,color=GREEN,width=1.4,dash=False,arrow=False):s['elements'].append(dict(kind='line',pts=pts,color=color,width=width,dash=dash,arrow=arrow))
def label(s,x,y,w,t,color=GREEN):
 rect(s,x,y,w,19,'#ffffff');rect(s,x,y,2,19,color);text(s,x+6,y+2,w-9,16,t,9.5,color,True)
def footer(s,p=None):
 line(s,[(42,769),(553,769)],'#c5d0c8',.6)
 text(s,42,779,415,29,(p['source'] if p else 'v1.1 專業圖解樣板｜封面＋P03、P05、P10')+'\n'+('相關頁：'+p['related'] if p else '原 v1 封面＋20 頁及輸出架構完整保留'),8.5,MUTED)
 text(s,490,779,65,32,p['id'] if p else 'v1.1',15,GREEN,True)
def blocks(s,p):
 for i,b in enumerate(p['blocks']):
  x=42+(i%2)*266;y=473+(i//2)*94
  rect(s,x,y,24,3,GOLD if i==1 else GREEN)
  text(s,x,y+9,245,21,f'0{i+1}  '+b['title'],12,GREEN,True)
  text(s,x,y+28,245,65,'\n'.join('• '+v for v in b['items']),10.5)
 rect(s,42,663,511,61,'#f8eae5');rect(s,42,663,3,61,RED)
 text(s,53,671,487,18,'！安全界線',11,RED,True)
 text(s,53,691,487,31,p['warning'],11,RED)
 text(s,42,736,410,20,p['tip'],10,GREEN)
 image(s,511,728,32,37,poses/'inspect-v1.1.png','官方角色原圖裁切：專注巡檢')
 footer(s,p)
plant=ASSET/'plant-overview-v1.1.png';cutaway=ASSET/'digester-comparison-v1.1.png';desulf=ASSET/'desulfurization-v1.1.png'
s=new('cover');rect(s,0,0,W,H,BG);rect(s,0,0,17,H,GREEN)
text(s,42,38,500,20,'BIOGAS  /  FIELD GUIDE                                    2026 · v1.1',10,GREEN,True)
text(s,42,83,510,125,'沼氣場\n健康檢查手冊',36,GREEN,True)
text(s,44,207,470,26,'看懂設備，讀懂趨勢，找到安全的下一步。',14)
image(s,25,252,550,367,plant,'半寫實全場鳥瞰：進料、厭氧槽、儲氣、脫硫、發電與出料')
text(s,42,625,420,28,'給農民、牧場負責人與非環工背景業主的巡檢助手。',12,GREEN)
image(s,475,617,65,76,poses/'guide-v1.1.png','由兩張官方原圖校驗的引導姿態裁切')
for i,(a,b) in enumerate([('01 導讀與快篩','P01–P03'),('02 生物系統','P04–P08'),('03 沼氣處理與安全','P09–P12'),('04 發電與實用工具','P13–P20')]):
 x=42+(i%2)*217;y=671+(i//2)*38;line(s,[(x,y),(x+192,y)],'#c5d0c8',.6);text(s,x,y+5,200,20,a+'  '+b,10.5,GREEN)
text(s,42,749,490,18,'會議討論版 · 設備示意非施工圖 · 技術與工安尚待專業審查',10,RED)
footer(s)
for ident,art in [('P03',plant),('P05',cutaway),('P10',desulf)]:
 p=next(p for p in DATA['pages'] if p['id']==ident);s=new(ident)
 rect(s,0,0,17,H, GREEN if ident=='P03' else (GOLD if ident=='P05' else '#497982'))
 text(s,42,32,470,18,p['chapter']+'  /  BIOGAS FIELD GUIDE',9.5,GREEN,True)
 text(s,508,29,48,40,ident,21,GREEN,True)
 text(s,42,64,520,42,p['title'],23,GREEN,True)
 text(s,42,108,510,36,p['key'],12)
 image(s,42,151,511,299,art,{'P03':'半寫實全場流程鳥瞰','P05':'相同槽型及視角的概念剖面對照','P10':'乾式吸附脫硫塔範例'}[ident])
 if ident=='P03':
  label(s,46,353,106,'進料與前處理');label(s,145,248,72,'厭氧槽');label(s,282,159,72,'儲氣');label(s,373,250,160,'氣體處理（含脫硫／脫水）');label(s,464,314,70,'發電機');label(s,351,412,174,'沼渣／沼液處理與接收')
  line(s,[(91,373),(146,361),(183,330)],'#9b682f',2,arrow=True)
  line(s,[(224,273),(316,234),(396,275),(479,328)],'#307b89',2,dash=True,arrow=True)
  line(s,[(257,344),(320,396),(399,403)],'#576b37',2,arrow=True)
  text(s,45,451,510,23,'實線棕：物料　虛線藍：沼氣　實線綠：出料｜儲氣、脫硫與脫水次序依案場設計。',9,MUTED)
 elif ident=='P05':
  label(s,54,154,174,'正常示意｜以本場基準判讀');label(s,318,154,208,'異常示意｜非單憑剖面診斷',GOLD)
  label(s,349,317,117,'泡沫／浮渣',GOLD);line(s,[(407,317),(435,303)],GOLD,1)
  label(s,416,398,106,'底部沉積',GOLD);line(s,[(416,408),(396,399)],GOLD,1)
  text(s,44,450,510,24,'概念剖面，非開槽觀察：以可用儀表、合規取樣與安全查核確認；不直接開槽。',9,MUTED)
 else:
  label(s,43,164,191,'乾式吸附式｜設備型式範例');label(s,50,334,120,'A 前端量測位置');label(s,412,241,120,'B 後端量測位置');line(s,[(155,334),(151,324)],GREEN,1);line(s,[(435,241),(435,222)],GREEN,1)
  line(s,[(82,357),(185,357)],'#307b89',2,arrow=True);line(s,[(416,289),(516,289)],'#307b89',2,arrow=True)
  text(s,45,451,510,24,'A／B 為量測位置示意，需工程確認；依案場核定的密閉採樣程序，由受訓人員執行。',9,MUTED)
 blocks(s,p)

def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
# Same absolute-positioned scene graph for browser and PDF.
css='''@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;background:#dde4de;color:#273c35;font-family:"Arial Unicode MS","PingFang TC",sans-serif}.toolbar{padding:16px;background:#245b47;color:white;display:flex;flex-wrap:wrap;gap:18px;align-items:center}.toolbar a{color:white}.page{position:relative;width:595.276pt;height:841.89pt;margin:22px auto;background:white;overflow:hidden;break-after:page;box-shadow:0 4px 24px #23352b25}.element{position:absolute}.text{white-space:pre-wrap;line-height:1.36;overflow-wrap:anywhere}.art{width:100%;height:100%;object-fit:contain}svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}@media print{body{background:white}.toolbar{display:none}.page{margin:0;box-shadow:none}.page:last-child{break-after:auto}}@media screen and (max-width:820px){.viewport{width:100%;overflow-x:auto}.page{margin:14px 0}}'''
parts=[];pdf=fitz.open();qa={'version':'v1.1-four-page-prototype','content_sha256':digest(ROOT/'content/handbook.json'),'mascot_original_hashes':EXPECTED,'text_fit':[],'images':[],'technical_review':'pending','browser_qa':'not yet run','v1_preserved':True}
for s in scenes:
 page=pdf.new_page(width=W,height=H);page.insert_font(fontname='handbook',fontfile=FONT)
 elems=[]
 for e in s['elements']:
  k=e['kind']
  if k=='line':
   pts=e['pts'];path=' '.join(('M' if i==0 else 'L')+f'{x},{y}' for i,(x,y) in enumerate(pts))
   elems.append(f'<svg viewBox="0 0 {W} {H}" aria-hidden="true"><path d="{path}" fill="none" stroke="{e["color"]}" stroke-width="{e["width"]}"'+(' stroke-dasharray="5 4"' if e['dash'] else '')+'/></svg>')
   shape=page.new_shape()
   for a,b in zip(pts,pts[1:]):shape.draw_line(a,b)
   shape.finish(color=rgb(e['color']),width=e['width'],dashes='[5 4] 0' if e['dash'] else None);shape.commit()
   if e['arrow']:
    a,b=pts[-2:];theta=math.atan2(b[1]-a[1],b[0]-a[0]);wings=[(b[0]-7*math.cos(theta+t),b[1]-7*math.sin(theta+t)) for t in [-.45,.45]]
    linepath=f'M{wings[0][0]},{wings[0][1]} L{b[0]},{b[1]} L{wings[1][0]},{wings[1][1]}'
    elems.append(f'<svg viewBox="0 0 {W} {H}" aria-hidden="true"><path d="{linepath}" fill="none" stroke="{e["color"]}" stroke-width="{e["width"]}"/></svg>')
    page.draw_polyline([wings[0],b,wings[1]],color=rgb(e['color']),width=e['width'])
   continue
  x,y,w,h=(e[n] for n in ['x','y','w','h']);r=fitz.Rect(x,y,x+w,y+h);style=f'left:{x}pt;top:{y}pt;width:{w}pt;height:{h}pt;'
  if k=='rect':
   page.draw_rect(r,color=None,fill=rgb(e['color']));elems.append(f'<div class="element" style="{style}background:{e["color"]}"></div>')
  elif k=='image':
   page.insert_image(r,filename=str(e['path']),keep_proportion=True)
   elems.append(f'<div class="element" style="{style}"><img class="art" src="{uri(e["path"])}" alt="{html.escape(e["alt"])}"></div>')
   im=Image.open(e['path']);dpi=round(min(im.width/(w/72),im.height/(h/72)))
   qa['images'].append({'page':s['id'],'asset':str(e['path'].relative_to(ROOT)),'pixels':im.size,'minimum_dpi':dpi,'sha256':digest(e['path'])})
  else:
   # Both renderers use 1.36 line height. Do not shrink text to force fit.
   font=fitz.Font(fontfile=FONT)
   wrapped=[]
   for paragraph in e['t'].split('\n'):
    current=''
    for char in paragraph:
     if current and font.text_length(current+char,fontsize=e['size'])>w:
      wrapped.append(current);current=''
     current+=char
    wrapped.append(current)
   result=page.insert_textbox(r,'\n'.join(wrapped),fontname='handbook',fontsize=e['size'],lineheight=1.36,color=rgb(e['color']))
   qa['text_fit'].append({'page':s['id'],'text':e['t'][:25],'remaining_pt':round(result,2)})
   assert result>=0,(s['id'],e['t'],result)
   elems.append(f'<div class="element text" style="{style}font-size:{e["size"]}pt;color:{e["color"]};font-weight:{700 if e["bold"] else 400}">{html.escape(e["t"])}</div>')
 parts.append(f'<article class="page" id="{s["id"]}" aria-label="{s["id"]}">'+''.join(elems)+'</article>')
pagehtml='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>沼氣場健康檢查手冊 v1.1｜四頁視覺樣板</title><style>'+css+'</style><header class="toolbar"><b>v1.1 四頁視覺樣板</b>'+''.join(f'<a href="#{s["id"]}">{s["id"]}</a>' for s in scenes)+'<a href="Biogas-Plant-Health-Check-v1.1-samples.pdf" download>下載 PDF</a><button onclick="print()">列印四頁</button><span>技術與工安待審 · 小螢幕請在頁面區左右滑動查看完整 A4 校樣</span></header><main class="viewport" tabindex="0" aria-label="A4 校樣，可左右捲動">'+''.join(parts)+'</main></html>'
(OUT/'samples.html').write_text(pagehtml)
(ROOT/'web/v1.1/index.html').write_text(pagehtml.replace('href="Biogas-Plant-Health-Check-v1.1-samples.pdf"','href="../../output/v1.1/Biogas-Plant-Health-Check-v1.1-samples.pdf"'))
pdfpath=OUT/'Biogas-Plant-Health-Check-v1.1-samples.pdf';pdf.subset_fonts();pdf.save(pdfpath,garbage=4,deflate=True);pdf.close()
reopened=fitz.open(pdfpath);assert len(reopened)==4
normalize=lambda s:''.join(s.split())
for i,ident in enumerate(['P03','P05','P10'],1):
 p=next(p for p in DATA['pages'] if p['id']==ident);t=normalize(reopened[i].get_text())
 for val in [p['title'],p['key'],p['warning'],p['source'],p['tip']]+[v for b in p['blocks'] for v in b['items']]:assert normalize(val) in t,(ident,val)
for i,p in enumerate(reopened):p.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(OUT/f'{scenes[i]["id"]}.png')
sheet=Image.new('RGB',(744*2,1053*2),'#dde4de')
for i,s in enumerate(scenes):
 im=Image.open(OUT/f'{s["id"]}.png');im.thumbnail((744,1053));sheet.paste(im,((i%2)*744,(i//2)*1053))
sheet.save(OUT/'contact-sheet.png')
qa['pdf_pages']=4;qa['pdf_full_original_text']='titles, keys, all block items, complete warnings, tips and sources verified';qa['pdf_fonts']=reopened[0].get_fonts();qa['raster_floor_dpi']=min(i['minimum_dpi'] for i in qa['images']);qa['html_embedded_images']=True
qa['renderer']='Shared scene graph -> native PDF (Arial Unicode embedded) / HTML. Browser print may differ; supplied PDF is native export.'
(OUT/'qa-report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in qa.items() if k not in ['text_fit','images','pdf_fonts']},ensure_ascii=False,indent=2))
