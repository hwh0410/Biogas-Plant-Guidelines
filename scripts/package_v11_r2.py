"""Package only a verified second-round build; no API or browser calls."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];O=R/'output/v1.1-r2';A=R/'assets/illustrations/v1.1-r2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'qa-report.json').read_text());assert report['browser']=='passed';assert report['html_sha256']==sha(O/'samples.html'),'QA stale'
expected={'mascot-character-sheet-v0.1.png':'b546e162beb2bdffdc25b128cc900cf60e572cc41c5adf081b42dc4cb7570a63','mascot-pose-sheet-v0.1.png':'9c694a3d5678751225be82cd69e5446a1b99a758682106333c79ae5b87cce06f'}
for name,h in expected.items():assert sha(R/'assets/mascot/reference'/name)==h
for asset in report['assets']:assert sha(R/asset['file'])==asset['sha256'],'Artwork changed after QA'
report['official_reference_hashes']=expected
report['pdf_sha256']=sha(O/'Biogas-Plant-Health-Check-v1.1-r2.pdf')
report['publication_limit']='Artwork about 194–232 effective dpi; style proof, not 300 dpi press-ready. AI equipment and instrument traces require professional review.'
(O/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
manifest={'version':'v1.1-r2','tool':'built-in image_gen.imagegen','character_method':'Both official PNGs passed as referenced_image_paths for every scene. New poses and shared lighting; no crop compositing.','references':expected,'assets':report['assets'],'external_billed_api_calls':False,'user_design_acceptance':'pending','professional_review':'pending'}
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(O/'v1.1-r2-bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.iterdir():
  if p.is_file() and p.suffix!='.zip':z.write(p,p.name)
 for p in A.rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(R)))
 for name in expected:
  p=R/'assets/mascot/reference'/name;z.write(p,str(p.relative_to(R)))
 for name in ['content/handbook.json','scripts/build_v11_r2.py','scripts/package_v11_r2.py','docs/v1.1-r2-design-review.md']:
  z.write(R/name,name)
print('Packaged verified r2: PDF, HTML, previews, PNG originals, both character references, prompts, QA and design notes.')
