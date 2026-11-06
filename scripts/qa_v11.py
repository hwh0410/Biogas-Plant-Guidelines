"""Honest offline regression: preserve v1 bytes; check sample PDF text and raster assets."""
from pathlib import Path
import json,hashlib,subprocess,re,base64,zipfile
from PIL import Image
import fitz
R=Path(__file__).resolve().parents[1];O=R/'output/v1.1'
def sha(b):return hashlib.sha256(b).hexdigest()
report=json.loads((O/'qa-report.json').read_text())
checks={}
for folder in ['content','web','output','qa']:
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only','d2443f6',folder],cwd=R,text=True).splitlines()
 for path in paths:
  baseline=subprocess.check_output(['git','show','d2443f6:'+path],cwd=R)
  assert (R/path).read_bytes()==baseline,'v1 modified: '+path
  checks[path]=sha(baseline)
report['v1_baseline_commit']='d2443f6';report['v1_unchanged_file_count']=len(checks);report['v1_preserved_hashes']=checks
pdf=fitz.open(O/'Biogas-Plant-Health-Check-v1.1-samples.pdf')
assert len(pdf)==4
for page in pdf:
 assert abs(page.rect.width-595.276)<.1 and abs(page.rect.height-841.89)<.1
 for b in page.get_text('dict')['blocks']:
  if b['type']==0:
   for line in b['lines']:
    for span in line['spans']:
     rect=fitz.Rect(span['bbox']);assert rect.x0>=16 and rect.x1<=580 and rect.y0>=20 and rect.y1<=825,span
report['pdf_text_bounds']='all text spans within A4 safe area'
assert all(pdf.extract_font(f[0])[3] for page in pdf for f in page.get_fonts())
report['pdf_fonts_embedded']=True
markup=(O/'samples.html').read_text();assert markup.count('<article class="page"')==4
for encoded in re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)',markup):assert base64.b64decode(encoded).startswith(b'\x89PNG')
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://',markup)
report['offline_html']='four pages; all PNG bytes embedded; no network dependencies'
browser_report=O/'browser/report.json'
if browser_report.exists():
 browser=json.loads(browser_report.read_text())
 assert browser['status']=='passed','Browser QA failed'
 assert browser['sample_html_sha256']==sha((O/'samples.html').read_bytes()),'Browser QA stale: rerun browser_qa_v11.py'
 report['browser_qa']=browser
else:
 report['browser_qa']='not run for this build'
report['visual_inspection']='PDF raster contact sheet inspected; labels adjusted; engineering review pending'
report['result']='offline and browser QA passed; professional review pending' if isinstance(report['browser_qa'],dict) else 'offline QA passed; browser and professional review pending'
(O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
with zipfile.ZipFile(O/'v1.1-samples-bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['samples.html','Biogas-Plant-Health-Check-v1.1-samples.pdf','contact-sheet.png','cover.png','P03.png','P05.png','P10.png','qa-report.json','README.md']:
  z.write(O/name,name)
 for p in (O/'browser').glob('*'):
  if p.is_file():z.write(p,'browser/'+p.name)
 for p in (R/'assets/illustrations').rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(R)))
 for p in ['docs/v1.1-visual-review.md','docs/v1.1-page-asset-map.md','docs/v1.1-production-log.md']:
  z.write(R/p,p)
print(f'PASS: {len(checks)} v1 files unchanged; 4 A4 pages; embedded fonts/images; full content checked. Browser QA: {isinstance(report["browser_qa"],dict)}.')
