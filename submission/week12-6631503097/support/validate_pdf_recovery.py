from pathlib import Path
import json, hashlib, io, subprocess, datetime
import pymupdf as fitz
from pypdf import PdfReader
from PIL import Image,ImageChops,ImageStat
R=Path('submission/week12-6631503097'); Q=Path('tmp/pdf-recovery-qa'); results={}
for label,path in [('damaged',Path('tmp/pdf-recovery-preserved/damaged-original.pdf')),('committed',Path('tmp/pdf-recovery-preserved/committed-original.pdf')),('regenerated',R/'Wk12_6631503097.pdf')]:
 b=path.read_bytes(); result={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'utf8_replacement_sequences':b.count(b'\xef\xbf\xbd')}
 for engine in ['pypdf','pymupdf']:
  try:
   d=PdfReader(path,strict=True) if engine=='pypdf' else fitz.open(path)
   pages=d.pages if engine=='pypdf' else d
   texts=[p.extract_text() or '' for p in pages] if engine=='pypdf' else [p.get_text() for p in pages]
   result[engine]={'pages':len(pages),'total_text_characters':sum(map(len,texts)),'sample_text':{str(i+1):texts[i][:1200] for i in [0,len(pages)//2,len(pages)-1]}}
  except Exception as e:result[engine]={'error':str(e)}
 results[label]=result
p=R/'Wk12_6631503097.pdf';d=fitz.open(p);assert len(d)==34
reader=PdfReader(p,strict=True);assert len(reader.pages)==34
nodes=json.loads((R/'support/final-report-content.json').read_text());shots=[n for n in nodes if n['kind']=='screenshot']; embedded=[];pagechecks=[]
for i,page in enumerate(d):
 pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 variance=sum(ImageStat.Stat(image).var);assert variance>10
 text=page.get_text();assert len(text.strip())>30
 pagechecks.append({'page':i+1,'text_characters':len(text),'render_variance':variance,'images':len(page.get_images())})
 if i+1 in [1,10,20,34]:pix.save(Q/f'page-{i+1:02}.png')
 for item in page.get_images():
  data=d.extract_image(item[0]);im=Image.open(io.BytesIO(data['image'])).convert('RGB');embedded.append((i+1,im))
assert len(embedded)==len(shots)==15
imagechecks=[]
for node,(pg,im) in zip(shots,embedded):
 original=Image.open(R/node['path']).convert('RGB');match=im.size==original.size and ImageChops.difference(im,original).getbbox() is None
 assert match,node['path'];imagechecks.append({'page':pg,'original':node['path'],'pixels_match':match})
text='\n'.join(p.get_text() for p in d)
terms=['lecture answers','Task 0','Task 1','Task 2','Task 3','Task 4','Audit the AI','Explain in Plain English','Prompt Problem','XZ','References','reflection']
sections={t:t.lower() in text.lower() for t in terms};assert all(sections.values())
assert p.stat().st_size<20*1024*1024
results.update({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_pages':pagechecks,'required_sections':sections,'screenshots':imagechecks,'under_20_mib':True,'rendered_pages':[1,10,20,34],'visual_review':'pending'})
(R/'evidence/pdf-recovery/validation.json').write_text(json.dumps(results,indent=2)+'\n')
(Q/'extracted-text.txt').write_text(text)
print(json.dumps({k:v for k,v in results.items() if k not in ['all_pages','screenshots']},indent=2))
