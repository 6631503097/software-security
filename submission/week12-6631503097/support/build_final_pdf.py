"""Wanna San / 6631503097: render the evidence-driven report without editing screenshots."""
from pathlib import Path
import json,re,textwrap,html
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,NextPageTemplate,Preformatted,KeepTogether
from reportlab import rl_config
rl_config.useA85 = 0  # lossless stream encoding; preserve original screenshot pixels
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
R=Path(__file__).resolve().parents[1]
font='/System/Library/Fonts/Supplemental/Arial.ttf';bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf';mono='/System/Library/Fonts/Supplemental/Andale Mono.ttf'
for name,path in [('Body',font),('BodyBold',bold),('Mono',mono)]:pdfmetrics.registerFont(TTFont(name,path))
NAVY=colors.HexColor('#14314A');TEAL=colors.HexColor('#007C83');GRAY=colors.HexColor('#52616D');LIGHT=colors.HexColor('#F1F5F8')
styles={'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=14,spaceAfter=8,textColor=NAVY,splitLongWords=1),
'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=17,leading=21,spaceBefore=15,spaceAfter=10,textColor=NAVY,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=11.5,leading=15,spaceBefore=10,spaceAfter=6,textColor=TEAL,keepWithNext=True),
'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,spaceAfter=5,textColor=GRAY),
'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.4,leading=11,textColor=NAVY,splitLongWords=1),
'headcell':ParagraphStyle('headcell',fontName='BodyBold',fontSize=8.4,leading=11,textColor=colors.white),
'code':ParagraphStyle('code',fontName='Mono',fontSize=7.4,leading=10,backColor=LIGHT,borderPadding=7,spaceBefore=5,spaceAfter=10),
'caption':ParagraphStyle('caption',fontName='BodyBold',fontSize=12,leading=16,spaceAfter=8,textColor=NAVY),
'cover':ParagraphStyle('cover',fontName='BodyBold',fontSize=31,leading=37,textColor=NAVY,spaceAfter=20)}
def normal(s):return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ').replace('\u2019',"'").replace('\u2018',"'").replace('\u201c','"').replace('\u201d','"')
def safe(s):
 s=html.escape(normal(s))
 # Only actual web URLs become links; source transcript text remains exact in Markdown.
 return re.sub(r'(https?://[^\s<>]+)',lambda m:'<link href="'+m.group(0)+'" color="#007C83">'+m.group(0)+'</link>',s)
def para(s,key='body'):return Paragraph(safe(s).replace('\n','<br/>'),styles[key])
def page(canvas,doc):
 w,h=doc.pageTemplate.pagesize;canvas.setPageSize((w,h));canvas.saveState();canvas.setStrokeColor(TEAL);canvas.setLineWidth(1);canvas.line(38,h-34,w-38,h-34);canvas.setFillColor(GRAY);canvas.setFont('Body',8);canvas.drawString(40,h-25,'KOSEN69 | Week 12 - Software Supply-Chain Security');canvas.drawRightString(w-40,22,f'Wanna San | 6631503097 | {doc.page}');canvas.restoreState()
bodyw,bodyh=A4;ew,eh=landscape(A3)
class Report(BaseDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='h1':
   key='section-'+str(self.seq.nextf('section'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,level=0,closed=False)
output=R/'Wk12_6631503097.pdf';doc=Report(str(output),pagesize=A4,title='Week 12 - Software Supply-Chain Security - Wanna San 6631503097',author='Wanna San (AI-assisted drafting disclosed)',subject='Verified Tasks 0-4 and student-review pending written sections',leftMargin=42,rightMargin=42,topMargin=48,bottomMargin=40)
doc.addPageTemplates([PageTemplate(id='Body',frames=Frame(42,40,bodyw-84,bodyh-88,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=page,pagesize=A4),PageTemplate(id='Evidence',frames=Frame(38,38,ew-76,eh-84,id='evidence',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=page,pagesize=landscape(A3))])
story=[];lastshot=False;images=[]
for n in json.loads((R/'support/final-report-content.json').read_text()):
 kind=n['kind']
 if kind!='screenshot' and lastshot:story += [NextPageTemplate('Body'),PageBreak()];lastshot=False
 if kind=='cover':
  story += [Spacer(1,70),para(n['subtitle'],'h2'),Paragraph(safe(n['title']),styles['cover']),para('Week 12 assignment report','h1'),Spacer(1,20)]
  for label,key in [('Student','student'),('Student ID','student_id'),('Group','group'),('Date','date')]:story.append(para(label+': '+n[key]))
  story += [Spacer(1,25),para(n['status'],'h2'),para('Observed technical results are complete. Suggested personal text is clearly labeled and requires student review. Branch push, pull request, quiz and course-portal submission are not represented as completed.'),Spacer(1,25),para('Evidence pages retain complete original screenshots. No authentication secrets are included.','small'),PageBreak()]
 elif kind=='section':
  if n['text'].startswith('3. Task 0'):story.append(PageBreak())
  story.append(para(n['text'],'h1'))
 elif kind=='heading':story.append(para(n['text'],'h2'))
 elif kind=='paragraph':story.append(para(n['text']))
 elif kind in ['code','quote']:
  # Visual wraps only; exact source text and command JSON remain preserved.
  text=normal(n['text']);lines=[]
  width=91 if kind=='code' else 91
  for line in text.splitlines():lines += textwrap.wrap(line,width=width,expand_tabs=False,replace_whitespace=False,drop_whitespace=False,break_long_words=True,break_on_hyphens=False) or ['']
  story.append(Preformatted('\n'.join(lines),styles['code'],maxLineLength=1000))
 elif kind=='table':
  cols=len(n['headers']);available=bodyw-84
  widths=([available*.29,available*.71] if cols==2 else [available/cols]*cols)
  rows=[[para(x,'headcell') for x in n['headers']]]+[[para(str(x),'cell') for x in row] for row in n['rows']]
  t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#D7E1E7'))]));story += [t,Spacer(1,9)]
 elif kind=='screenshot':
  story += [NextPageTemplate('Evidence'),PageBreak(),para(n['caption'],'caption')]
  path=R/n['path'];im=PILImage.open(path);iw,ih=im.size;scale=min((ew-76)/iw,(eh-142)/ih);story.append(Image(str(path),width=iw*scale,height=ih*scale,hAlign='CENTER'));story.append(Spacer(1,5));story.append(para(n['path']+' | Original full-screen PNG; see source for full resolution.','small'));lastshot=True;images.append(n['path'])
doc.build(story)
print('Generated:',output)
print('Embedded originals:',len(images))
