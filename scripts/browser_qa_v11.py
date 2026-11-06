"""Browser QA for v1.1 samples and unmodified v1; writes only output/v1.1/browser/."""
from pathlib import Path
import functools,http.server,threading,json,hashlib
from playwright.sync_api import sync_playwright
import fitz
R=Path(__file__).resolve().parents[1];O=R/'output/v1.1/browser';O.mkdir(parents=True,exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
report={'status':'running','sample_html_sha256':hashlib.sha256((R/'output/v1.1/samples.html').read_bytes()).hexdigest(),'v1':{},'samples':{}}
def require(ok,message):
 if not ok:raise AssertionError(message)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1200,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  for route in ['/output/v1.1/samples.html','/web/v1.1/']:
   p.goto(base+route,wait_until='networkidle');p.evaluate('document.fonts.ready')
   require(p.locator('article.page').count()==4,'four sample pages')
   require(p.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'),'sample images')
   overflow=p.evaluate('''()=>Array.from(document.querySelectorAll('.text')).filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).map(e=>({page:e.closest('.page').id,text:e.textContent,scroll:e.scrollHeight,client:e.clientHeight}))''')
   report['samples'][route]={'text_overflow':overflow}
   for ident in ['cover','P03','P05','P10']:
    p.locator(f'.toolbar a[href="#{ident}"]').click();require(p.evaluate('location.hash')=='#'+ident,'anchor '+ident)
   link=p.locator('.toolbar a[download]').get_attribute('href')
   from urllib.parse import urljoin
   require(p.request.get(urljoin(p.url,link)).status==200,'PDF download link')
   require(not overflow,'sample text overflow: '+json.dumps(overflow,ensure_ascii=False))
  p.goto((R/'output/v1.1/samples.html').as_uri());p.evaluate('document.fonts.ready');require(p.locator('.page').count()==4,'offline pages')
  require(p.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'),'offline images')
  report['samples']['offline_file']=True
  for ident in ['cover','P03','P05','P10']:p.locator('#'+ident).screenshot(path=str(O/(ident+'-browser.png')))
  widths=[]
  for width in [390,768]:
   p.set_viewport_size({'width':width,'height':900})
   require(p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'document mobile overflow')
   # A4 proof stays at readable physical size inside an explicitly scrollable viewport.
   require(p.locator('.viewport').evaluate('e=>e.scrollWidth>e.clientWidth'),'proof horizontal scroll container')
   p.evaluate('scrollTo(0,0)');p.locator('.viewport').evaluate('e=>e.scrollLeft=0')
   p.screenshot(path=str(O/f'mobile-{width}.png'))
   p.locator('.viewport').evaluate('e=>e.scrollLeft=e.scrollWidth')
   require(p.locator('.viewport').evaluate('e=>e.scrollLeft>0'),'mobile scroll reaches right side')
   p.screenshot(path=str(O/f'mobile-{width}-right.png'));widths.append(width)
  report['samples']['mobile_proof_widths']=widths
  p.set_viewport_size({'width':1200,'height':1000});p.emulate_media(media='print')
  p.pdf(path=str(O/'samples-browser-print.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
  printed=fitz.open(O/'samples-browser-print.pdf');require(len(printed)==4,f'browser print pages {len(printed)}')
  require(all(abs(page.rect.width-595.28)<1 and abs(page.rect.height-841.89)<1 for page in printed),'A4 print dimensions')
  d=json.loads((R/'content/handbook.json').read_text());norm=lambda s:''.join(s.split())
  for i,ident in enumerate(['P03','P05','P10'],1):
   data=next(x for x in d['pages'] if x['id']==ident);t=norm(printed[i].get_text())
   for v in [data['title'],data['key'],data['warning'],data['source'],data['tip']]+[v for block in data['blocks'] for v in block['items']]:require(norm(v) in t,'browser PDF missing '+v)
  report['samples']['browser_print']='4 A4 pages; complete original text verified';printed.close()
  p.emulate_media(media='screen');p.goto(base+'/web/',wait_until='networkidle');p.wait_for_function('window.handbookReady===true')
  require(p.locator('.page').count()==21,'v1 page count')
  require(p.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)'),'v1 images')
  p.locator('#search').fill('發不動');require(p.locator('.page[hidden]').count()>0 and p.locator('.page:not([hidden])').count()>0,'v1 search')
  p.emulate_media(media='print');require(p.evaluate("Array.from(document.querySelectorAll('.page')).every(p=>getComputedStyle(p).display==='flex')"),'v1 filtered print')
  p.emulate_media(media='screen');p.locator('#search').fill('');p.locator('#mode').click();p.locator('#jump').select_option('P05');p.wait_for_function("document.querySelector('#P05').classList.contains('selected')")
  p.locator('#next').click();p.wait_for_function("document.querySelector('#P06').classList.contains('selected')")
  p.locator('#prev').click();p.wait_for_function("document.querySelector('#P05').classList.contains('selected')");p.locator('#mode').click()
  for width in [390,768]:
   p.set_viewport_size({'width':width,'height':900});require(p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'v1 mobile '+str(width))
  p.set_viewport_size({'width':1200,'height':1000});p.emulate_media(media='print');p.pdf(path=str(O/'v1-regression-print.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
  v1=fitz.open(O/'v1-regression-print.pdf');require(len(v1)==21,'v1 print 21 pages')
  for i,data in enumerate(d['pages'],1):
   t=norm(v1[i].get_text());require(norm(data['title']) in t and norm(data['warning']) in t,'v1 print text '+data['id'])
  v1.close();report['v1']={'pages':21,'search':True,'next_previous_jump':True,'print_ignores_search':True,'mobile_widths':[390,768],'pdf_titles_warnings':True}
  require(not errors,'browser console errors');report['page_errors']=errors;b.close();report['status']='passed'
except Exception as e:
 report['status']='failed';report['error']=str(e);raise
finally:
 server.shutdown();(O/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
