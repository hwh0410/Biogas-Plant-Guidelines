"""Import approved local raster artwork without enabling any billed API."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('asset',choices=['plant-overview','digester-comparison','desulfurization'])
p.add_argument('source',type=Path);p.add_argument('--provenance',required=True)
a=p.parse_args();im=Image.open(a.source);assert im.format=='PNG' and min(im.size)>=1024,'Require original PNG, at least 1024 px shortest edge'
root=Path(__file__).resolve().parents[1];target=root/'assets/illustrations'/f'{a.asset}-v1.1.png'
assert not target.exists(),'Refusing to overwrite existing artwork; version it explicitly'
shutil.copy2(a.source,target)
meta={'asset':target.name,'source':str(a.source),'provenance':a.provenance,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'pixels':im.size,'review':'pending'}
target.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print(target)
