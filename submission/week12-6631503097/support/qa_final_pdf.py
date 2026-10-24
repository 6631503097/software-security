from pathlib import Path
import json,hashlib,re
import pymupdf as fitz
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];Q=Path('tmp/week12-final-qa');D=fitz.open(R/'Wk12_6631503097.pdf');issues=[];pages=[];links=[]
for i,page in enumerate(D):
 text=page.get_text();images=page.get_images();pages.append({'page':i+1,'text_characters':len(text),'images':len(images),'width':page.rect.width,'height':page.rect.height})
 if len(text.strip())<30 and not images:issues.append({'page':i+1,'type':'blank'})
 for block in page.get_text('dict')['blocks']:
  if block['type']==0:
   x0,y0,x1,y1=block['bbox']
   if min(x0,y0)<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:issues.append({'page':i+1,'type':'clipping','bbox':block['bbox']})
 for link in page.get_links():
  if link.get('uri'):links.append(link['uri'])
 page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(Q/f'page-{i+1:02}.png')
for start in range(0,len(D),12):
 sheet=Image.new('RGB',(1000,1110),'#dbe3e9');draw=ImageDraw.Draw(sheet)
 for k in range(start,min(start+12,len(D))):
  im=Image.open(Q/f'page-{k+1:02}.png');im.thumbnail((238,335));x=(k-start)%4*250+(250-im.width)//2;y=(k-start)//4*370+22;sheet.paste(im,(x,y));draw.text((x,y-17),f'Page {k+1}',fill='black')
 sheet.save(Q/f'review-{start//12+1}.png')
text='\n'.join(p.get_text() for p in D);(Q/'pdf-text.txt').write_text(text)
terms=['lecture answers','Task 0','Task 1','Task 2','Task 3','Task 4','Audit the AI','Explain in Plain English','Prompt Problem','XZ','References','No SLSA level','336aaf8'];checks={s:s.lower() in text.lower() for s in terms}
report=json.loads((R/'support/final-report-content.json').read_text());shots=[n for n in report if n['kind']=='screenshot'];assert len(shots)==15;originals=json.loads((R/'evidence/final-qa/existing-file-audit.json').read_text());old={f['path']:f['sha256'] for f in originals['files']};imagecheck=[]
for item in shots:
 p=R/item['path'];actual=hashlib.sha256(p.read_bytes()).hexdigest();imagecheck.append({'path':item['path'],'sha256':actual,'matches_preexisting_original':old.get(item['path'],actual)==actual});assert imagecheck[-1]['matches_preexisting_original']
links_ok=all(any(u in l for l in links) for u in ['pip.pypa.io/en/stable/cli/pip_install/','slsa.dev/spec/v1.2/build-provenance','github.com/6631503097/software-security/commit/336aaf8'])
result={'page_count':len(D),'pdf_sha256':hashlib.sha256((R/'Wk12_6631503097.pdf').read_bytes()).hexdigest(),'pdf_bytes':(R/'Wk12_6631503097.pdf').stat().st_size,'pages':pages,'layout_issues':issues,'required_section_text_checks':checks,'embedded_image_count':sum(p['images'] for p in pages),'accepted_screenshots':imagecheck,'link_count':len(links),'representative_links_intact':links_ok,'visual_review':'Pending final rendered-page inspection'};(R/'evidence/final-qa/pdf-structure-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['pages','accepted_screenshots']},indent=2));assert not issues and all(checks.values()) and links_ok
