"""Wanna San / 6631503097: binary-safe final PDF and evidence validation."""
from pathlib import Path
import hashlib,io,json,datetime,re
import pymupdf as fitz
from pypdf import PdfReader
from PIL import Image,ImageChops,ImageStat,ImageDraw
R=Path(__file__).resolve().parents[1];Q=Path('tmp/week12-approved-qa');Q.mkdir(parents=True,exist_ok=True);E=R/'evidence/final-submission-review';E.mkdir(exist_ok=True)
p=R/'Wk12_6631503097.pdf';doc=fitz.open(p);reader=PdfReader(p,strict=True)
assert len(doc)==len(reader.pages)==34
texts=[page.get_text() for page in doc];other=[page.extract_text() or '' for page in reader.pages];assert all(len(t.strip())>30 for t in texts+other)
text='\n'.join(texts);checks={s:s.lower() in text.lower() for s in ['lecture answers','Task 0','Task 1','Task 2','Task 3','Task 4','Audit the AI','Explain in Plain English','Prompt Problem','XZ','References','reflection','No SLSA level']};assert all(checks.values())
assert not any(x in text.lower() for x in ['student review required','suggested answer','rewrite in your own words','suggested reflection','suggested rationale'])
final=json.loads((R/'support/finalization.json').read_text())
for field in ['reflection','eipe','strongest_defense','audit']:assert final[field] in (R/'week12-tasks0-2.md').read_text()
if final.get('pr_url'):assert final['pr_url'] in text
shots=[n for n in json.loads((R/'support/final-report-content.json').read_text()) if n['kind']=='screenshot'];assert len(shots)==15
embedded=[];pages=[];issues=[]
for i,page in enumerate(doc):
 pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);variance=sum(ImageStat.Stat(im).var);assert variance>10
 pix.save(Q/f'page-{i+1:02}.png');pages.append({'page':i+1,'text_characters':len(texts[i]),'render_variance':variance,'images':len(page.get_images())})
 for block in page.get_text('dict')['blocks']:
  if block['type']==0:
   a,b,c,d=block['bbox']
   if min(a,b)<-1 or c>page.rect.width+1 or d>page.rect.height+1:issues.append({'page':i+1,'bbox':block['bbox']})
 for item in page.get_images():
  data=doc.extract_image(item[0]);embedded.append((i+1,Image.open(io.BytesIO(data['image'])).convert('RGB')))
assert not issues;assert len(embedded)==15
matches=[]
for node,(pg,im) in zip(shots,embedded):
 original=Image.open(R/node['path']).convert('RGB');assert im.size==original.size and ImageChops.difference(im,original).getbbox() is None
 matches.append({'page':pg,'path':node['path'],'pixels_match':True,'sha256':hashlib.sha256((R/node['path']).read_bytes()).hexdigest()})
old=json.loads((R/'evidence/environment/instructor-sha256.json').read_text());assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest()==h for path,h in old.items())
assert p.stat().st_size<20*1024*1024
for start in range(0,len(doc),12):
 sheet=Image.new('RGB',(1000,1110),'#dbe3e9');draw=ImageDraw.Draw(sheet)
 for k in range(start,min(start+12,len(doc))):
  im=Image.open(Q/f'page-{k+1:02}.png');im.thumbnail((238,335));x=(k-start)%4*250+(250-im.width)//2;y=(k-start)//4*370+22;sheet.paste(im,(x,y));draw.text((x,y-17),f'Page {k+1}',fill='black')
 sheet.save(Q/f'review-{start//12+1}.png')
result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'page_count':len(doc),'readers':['PyMuPDF','pypdf strict=True'],'extracted_text_characters':sum(map(len,texts)),'first_middle_last_text':{str(i+1):texts[i] for i in [0,17,33]},'required_sections':checks,'pages':pages,'screenshots':matches,'instructor_hashes_unchanged':True,'under_20_mib':True,'personal_responses_approved':True,'drafting_instructions_absent':True,'pr_url':final.get('pr_url'),'visual_review':'pending'}
(E/'pdf-validation.json').write_text(json.dumps(result,indent=2)+'\n');(Q/'extracted-text.txt').write_text(text)
print(json.dumps({k:v for k,v in result.items() if k not in ['pages','screenshots','first_middle_last_text']},indent=2))
