"""Vector PDF: the working (6,7), every saved move, and independent boundary closure."""
from io import BytesIO
from pathlib import Path
from hashlib import sha256
from html import escape
import json,re,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from surface_diagrams.braid_stack import braid_fragment_svg, stack_row_height
from surface_diagrams.compact_svg import compact_support_svg
from surface_diagrams.visuals import RAINBOW
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import toColor,HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing,Group,Circle,Ellipse,Rect,String
from reportlab.graphics.svgpath import SvgPath
from reportlab.graphics import renderPDF
from pypdf import PdfReader,PdfWriter

OUT=ROOT/'output/pdf/six-seven-identity.pdf'
PUBLIC=ROOT/'docs/proofs/six-seven-fifty-blocks/six-seven-identity.pdf'
TMP=ROOT/'tmp/pdfs';TMP.mkdir(parents=True,exist_ok=True);OUT.parent.mkdir(parents=True,exist_ok=True)
FONT=Path('C:/Windows/Fonts')
if (FONT/'arial.ttf').exists():
 for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
else:Body='Helvetica'
BODY='Body' if (FONT/'arial.ttf').exists() else 'Helvetica';BOLD='Bold' if BODY=='Body' else 'Helvetica-Bold'
pdfmetrics.registerFontFamily(BODY,normal=BODY,bold=BOLD,italic=BODY,boldItalic=BOLD)
W,H=letter;M=30;GAP=20;CW=(W-2*M-GAP)/2;BW=46;SCALE=BW/86
styles={name:ParagraphStyle(name,fontName=BODY,fontSize=size,leading=leading,textColor='#18344a') for name,size,leading in [('body',10,14),('small',7.5,10),('heading',18,22),('caption',9,12),('label',6.5,8)]}
styles['heading'].fontName=BOLD

def plain(s):
 return str(s).translate(str.maketrans({'\u2010':'-','\u2011':'-','\u2012':'-','\u2013':'-','\u2014':'-','\u2212':'-','\u2192':'->','\u03c3':'sigma','\u2019':"'"}))

def vector(svg):
 root=ET.fromstring(svg);x,y,w,h=map(float,root.attrib['viewBox'].split());assert x==y==0
 drawing=Drawing(w,h);down=Group(transform=(1,0,0,-1,0,h));drawing.add(down)
 def number(value,default=0,ref=1):
  if value is None:return default
  if value.endswith('%'):return float(value[:-1])*ref/100
  return float(re.sub(r'(px|pt)$','',value))
 def add(parent,node,inherited):
  tag=node.tag.rsplit('}',1)[-1]
  if tag in ('title','desc'):return
  props=dict(inherited);props.update(node.attrib)
  if tag=='g':
   group=Group();trans=node.get('transform','')
   for op,arg in re.findall(r'(translate|scale|matrix)\(([^)]+)\)',trans):
    vals=list(map(float,arg.replace(',',' ').split()))
    if op=='translate':group.translate(vals[0],vals[1] if len(vals)>1 else 0)
    elif op=='scale':group.scale(vals[0],vals[1] if len(vals)>1 else vals[0])
    else:group.transform=tuple(vals)
   parent.add(group)
   for child in node:add(group,child,props)
   return
  color=lambda key,default:None if props.get(key,default)=='none' else toColor(props.get(key,default))
  kw=dict(fillColor=color('fill','black'),strokeColor=color('stroke','none'),strokeWidth=number(props.get('stroke-width'),1))
  if tag=='path':shape=SvgPath(node.attrib['d'],**kw)
  elif tag=='circle':shape=Circle(number(node.get('cx')),number(node.get('cy')),number(node.get('r')),**kw)
  elif tag=='ellipse':shape=Ellipse(number(node.get('cx')),number(node.get('cy')),number(node.get('rx')),number(node.get('ry')),**kw)
  elif tag=='rect':shape=Rect(number(node.get('x')),number(node.get('y')),number(node.get('width'),ref=w),number(node.get('height'),ref=h),rx=number(node.get('rx')),ry=number(node.get('rx')),**kw)
  elif tag=='text':
   shape=String(0,0,''.join(node.itertext()),fontName=BODY,fontSize=number(props.get('font-size'),8),fillColor=kw['fillColor'],textAnchor=props.get('text-anchor','start'))
   group=Group(shape,transform=(1,0,0,-1,number(node.get('x')),number(node.get('y'))));parent.add(group);return
  else:raise ValueError('Unsupported SVG primitive '+tag)
  if props.get('stroke-dasharray') and props['stroke-dasharray']!='none':shape.strokeDashArray=list(map(float,props['stroke-dasharray'].replace(',',' ').split()))
  if props.get('stroke-linecap')=='round':shape.strokeLineCap=1
  if props.get('stroke-linejoin')=='round':shape.strokeLineJoin=1
  parent.add(shape)
 for node in root:add(down,node,{})
 return drawing

class Book:
 def __init__(self):
  self.c=canvas.Canvas(str(TMP/'six-seven-body.pdf'),pagesize=(W,H),pageCompression=1)
  self.c.setTitle('The working (6,7): a verified graphical identity certificate');self.c.setAuthor('Richard Buckman - surface-diagrams')
  self.n=0;self.forms={};self.index=[];self.sections=[];self.flow_top=None
 def text(self,s,x,top,width,style='body'):
  p=Paragraph(plain(s),styles[style]);_,height=p.wrap(width,H);p.drawOn(self.c,x,top-height);return top-height
 def new(self,title,subtitle='',bookmark=None):
  if self.n:self.c.showPage()
  self.n+=1;self.flow_top=None;self.c.setFillColor(HexColor('#f5f7fa'));self.c.rect(0,0,W,H,stroke=0,fill=1)
  self.c.setFillColor(HexColor('#18344a'));self.c.setFont(BOLD,9);self.c.drawString(M,H-25,'SURFACE DIAGRAMS / WORKING (6,7) / VERIFIED IDENTITY')
  top=self.text('<b>'+escape(plain(title))+'</b>',M,H-42,W-2*M,'heading')
  if subtitle:top=self.text(subtitle,M,top-9,W-2*M,'caption')
  self.c.setStrokeColor(HexColor('#b8cbd9'));self.c.line(M,31,W-M,31)
  self.c.setFont(BODY,7);self.c.drawString(M,16,'21 October 2026 | Individual supports; joint cut certificates labeled separately')
  self.c.drawRightString(W-M,16,str(self.n));self.index.append(dict(page=self.n,title=plain(title)))
  if bookmark:self.c.bookmarkPage(bookmark);self.c.addOutlineEntry(plain(title),bookmark,level=0)
  return top-16
 def image(self,svg,x,y,width,height):
  k=sha256(svg.encode()).hexdigest()
  if k not in self.forms:
   d=vector(svg);name='figure'+str(len(self.forms));self.c.beginForm(name,0,0,d.width,d.height);renderPDF.draw(d,self.c,0,0);self.c.endForm();self.forms[k]=(name,d.width,d.height)
  name,sw,sh=self.forms[k];scale=min(width/sw,height/sh)
  self.c.saveState();self.c.translate(x+(width-sw*scale)/2,y+(height-sh*scale)/2);self.c.scale(scale,scale);self.c.doForm(name);self.c.restoreState()
 def band(self,s,top,sphere=False):
  height=Paragraph(plain(s),styles['small']).wrap(W-2*M-20,H)[1]+16
  self.c.setFillColor(HexColor('#fff0ce' if sphere else '#e5eff6'));self.c.roundRect(M,top-height,W-2*M,height,5,stroke=0,fill=1)
  self.text(s,M+10,top-8,W-2*M-20,'small');return top-height-10
 def height(self,row):return max(34,stack_row_height(row['word'],compact=True)*SCALE+4)
 def row(self,data,row,x,top,order,position,width=CW):
  h=self.height(row);self.c.setFillColor(HexColor('#ffffff'));self.c.rect(x,top-h,width,h,stroke=0,fill=1)
  lw=72 if width==CW else 100
  identity=row['id'] if len(row['id'])<=25 else row['id'][:23]+'..'
  label=f'<b>{position+1}. {escape(identity)}</b><br/>{escape(row["label"])}'
  if row.get('sphere_rechart'):label+='<br/>SPHERE CHART'
  self.text(label,x+3,top-3,lw-5,'label')
  self.image(compact_support_svg(data['supports'][row['support']]),x+lw,top-h+2,width-BW-lw-10,h-4)
  fragment=braid_fragment_svg(row['word'],order=order,compact=True)
  # Labels occupy the left support column only. Add straight lead-ins to
  # the shared crossing fragment, so the braid reaches both row edges.
  # Crossing paths and their over/under gaps are unchanged, not stretched.
  pad=(h/SCALE-fragment['height'])/2
  lead=lambda colors,a,b:''.join(f'<path d="M {13+12*i} {a} V {b}" stroke="{RAINBOW[colors[i]]}" stroke-width=".8" fill="none"/>' for i in range(6))
  body=fragment['svg'].split('>',1)[1].rsplit('</svg>',1)[0]
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="86" height="{h/SCALE}" viewBox="0 0 86 {h/SCALE}">'+lead(order,0,pad)+f'<g transform="translate(0 {pad})">'+body+'</g>'+lead(fragment['exit_order'],pad+fragment['height'],h/SCALE)+'</svg>'
  self.image(svg,x+width-BW-3,top-h,BW,h)
  self.c.setStrokeColor(HexColor('#2563eb'));self.c.setDash(2,3);self.c.line(x+width-BW-5,top-h,x+width-1,top-h);self.c.setDash()
  # Paint on the page, outside the form's clip box: the endpoint disks must
  # remain whole even at the top and bottom of a connected braid strip.
  self.c.setFillColor(HexColor('#006fff'))
  for edge in (top,top-h):
   for i in range(6):self.c.circle(x+width-BW-3+(13+12*i)*SCALE,edge,1.9*SCALE,stroke=0,fill=1)
  return top-h,fragment['exit_order']
 def checkpoint(self,title,data,ids):
  pos=0;order=tuple(range(6));part=0
  while pos<len(ids):
   part+=1;top=self.new(title+(' - continued' if part>1 else ''),'FULL ORDERED FACTORIZATION. Read downward. Braids remain connected, with strand colors retained; disjoint crossings may share a level.')
   y=top
   while pos<len(ids) and y-self.height(data['rows'][ids[pos]])>45:
    y,order=self.row(data,data['rows'][ids[pos]],M,y,order,pos,width=W-2*M);pos+=1
 def move(self,section,number,title,kind,da,ia,db,ib,extra=''):
  before=[da['rows'][i] for i in ia];after=[db['rows'][i] for i in ib]
  key=lambda r:(r['id'],tuple(r['word']),r['label'],r.get('sphere_rechart',False))
  p=0
  while p<min(len(before),len(after)) and key(before[p])==key(after[p]):p+=1
  tail=0
  while tail<min(len(before),len(after))-p and key(before[-tail-1])==key(after[-tail-1]):tail+=1
  local_a=before[p:len(before)-tail if tail else len(before)];local_b=after[p:len(after)-tail if tail else len(after)]
  orders=[]
  for rows in (before,after):
   order=list(range(6))
   for row in rows[:p]:
    for g in row['word']:i=abs(g)-1;order[i],order[i+1]=order[i+1],order[i]
   orders.append(tuple(order))
  cursors=[0,0];part=0
  while part==0 or cursors[0]<len(local_a) or cursors[1]<len(local_b):
   part+=1;heading=f'{section} - step {number:03d}'+(' - continued' if part>1 else '')
   context=f'{p} unchanged displayed factors above; {tail} below. Only the changed interval is shown. '+extra
   measure=lambda s:Paragraph(plain(s),styles['small']).wrap(W-2*M,H)[1]
   remaining=max(sum(self.height(r) for r in local_a[cursors[0]:]),sum(self.height(r) for r in local_b[cursors[1]:]))
   needed=92+measure(escape(plain(title)))+measure(context)+remaining
   packed=part==1 and self.flow_top is not None and self.flow_top-needed>=45
   if packed:
    top=self.flow_top;self.c.setStrokeColor(HexColor('#c2d2df'));self.c.line(M,top+7,W-M,top+7)
    top=self.text('<b>'+heading+'</b>',M,top,W-2*M,'caption')-4
    top=self.text(escape(plain(title)),M,top,W-2*M,'small')-7
   else:top=self.new(heading,escape(plain(title)))
   sphere=kind=='sphere_rewrite'
   scope='SPHERE MOVE: exact sphere action and +I lift checked; disk discrepancy retained.' if sphere else 'EXPLICIT GLOBAL CONJUGATION: a change of the whole product by the recorded frame.' if kind=='global_conjugation' else 'EXACT DISK BOUNDARY RELATION: independently calculated based Artin actions agree.' if kind=='disk_boundary_relation' else 'DISK MOVE: exact local free-word, based-action, or supported-class certificate retained.'
   if packed:
    self.c.setFillColor(HexColor('#fff0ce' if sphere else '#e5eff6'));self.c.roundRect(M,top-30,W-2*M,30,5,stroke=0,fill=1)
    self.text(scope,M+10,top-7,W-2*M-20,'small');top-=38
   else:top=self.band(scope,top,sphere)
   top=self.text(context,M,top,W-2*M,'small')-(8 if packed else 12)
   if p==len(before)==len(after):
    bottom=self.text('No displayed row changes. The exact certificate records the change of source presentations.',M,top,W-2*M)
    self.flow_top=bottom-18;break
   self.text('<b>Before</b>',M,top,CW,'caption');self.text('<b>After</b>',M+CW+GAP,top,CW,'caption');top-=(16 if packed else 20)
   bottoms=[]
   for side,rows in enumerate((local_a,local_b)):
    y=top
    if not rows:self.text('Identity / no factors in this interval.',M+side*(CW+GAP),y,CW,'caption')
    while cursors[side]<len(rows) and y-self.height(rows[cursors[side]])>45:
     j=cursors[side];y,orders[side]=self.row(da if side==0 else db,rows[j],M+side*(CW+GAP),y,orders[side],p+j);cursors[side]+=1
    bottoms.append(y)
   self.flow_top=min(bottoms)-18
 def section(self,title,description):
  self.sections.append((title,self.n+1));top=self.new(title,bookmark='section'+str(len(self.sections)))
  self.text(description,M,top,W-2*M)
 def finish(self):self.c.save()


def assets(folder):
 d=json.loads((folder/'display.json').read_text())
 if 'supports' not in d:
  a=json.loads((folder/'assets-index.json').read_text());d['supports']=[]
  for start in range(0,a['counts']['supports'],a['chunk_size']):d['supports']+=json.loads((folder/'assets'/('supports-'+str(start//a['chunk_size'])+'.json')).read_text())
 return d


def build():
 oldroot=ROOT/'docs/proofs/six-seven-compact';newroot=ROOT/'docs/proofs/six-seven-fifty-blocks'
 old=assets(oldroot);new=assets(newroot);cert=json.loads((newroot/'certificate.json').read_text())
 book=Book();top=book.new('The working (6,7): a verified graphical identity','A forward derivation with connected braid strips, every sphere move identified, and an independent boundary-action ending.',bookmark='start')
 top=book.band('BRIEF SUMMARY: (6,7) -> fifty -> an actual standard twenty plus thirty -> two verified sphere identities.',top)
 top=book.text('The new 154-letter representative is our working (6,7). Join it to the saved calculation chart, follow the checked named substitutions to fifty positive units, and isolate a standard twenty in seven Hurwitz moves and one sphere rechart. Rewrite the remaining thirty on a five-point disk; its exact based action is the double outer-boundary twist. Cap that double boundary and close the twenty independently.',M,top,W-2*M)-20
 top=book.text('<b>Proof scope.</b> The ending is an exact factor-level identity certificate using a faithful disk-action calculation. It is not a purely elementary Hurwitz normal form W0 W1. The isolated thirty has permutation orbit sizes 3,2,1, so it cannot alone be Hurwitz-equivalent to W1. The classification theorem is not used as an identity proof.',M,top,W-2*M)-20
 top=book.text('<b>How to read the figures.</b> Each support is drawn with the shared Arc/Loop library and paired with the braid that represents that pictured support. Blue dots separate factors, and braid strand colors continue downward. A yellow SPHERE SUPPORT CHART label means the display is an explicitly certified sphere representative. Actual sphere derivation moves are labeled SPHERE MOVE. Raw factors, disk discrepancies, global frames and lift checks are retained in the online certificates.',M,top,W-2*M)-20
 book.text('<b>Navigation.</b> This detailed book retains every old atomic substitution instead of hiding it in a group. Its front section is a brief explanation; the subsequent pages give the complete diagrams. The online view offers chapter/group navigation and side-scrolling columns. The final disk cut-system comparison is jointly certified; the other drawings are individual factor supports.',M,top,W-2*M)
 book.new('Contents','Section pages are listed below. PDF bookmarks provide direct section navigation.',bookmark='contents')
 contents_page=book.n
 top=book.new('What the steps establish',bookmark='explanation')
 for title,text in [
  ('1. Start from the working (6,7).','Three inverse adjacent Hurwitz moves, an explicit global change of chart, and exact disk support presentations join the working seed to the saved source. This does not use a sphere identity.'),
  ('2. Reach the actual positive fifty.','The preserved 145 atomic moves use transported PC lantern/half-lantern substitutions, disk Hurwitz moves and explicitly recorded sphere changes. The previous inverse pair is replaced using a squared sphere relation, preserving the genus-two lift.'),
  ('3. Extract the standard twenty.','Move F3 upward past the transported {5,6} pair. Rechart that pair as round T56 on the sphere, then move it unchanged past six neighbors. The resulting Q A Q A block is a disk conjugate of W0, where A=43211234 and Q=55. Its closure is checked independently.'),
  ('4. Close the thirty in a five-point chart.','Put point 6 at infinity. One pair loop becomes its complementary four-point loop; its expanded disk-core length increases by ten. The exact ordered five-point model has forty positive core letters and the same action on all five based meridians as the double outer-boundary twist. That is a faithful disk braid equality.'),
  ('5. Cap the double boundary.','The double cap is a separate sphere move with trivial genus-two lift discrepancy. A single five-point boundary twist has lift -I and would be wrong. No closure hypothesis for the starting word is used in the final disk-action calculation.')]:
  top=book.text('<b>'+title+'</b> '+text,M,top,W-2*M)-20
 working=new['routes']['working'];extract=new['routes']['extract'];thirty=new['routes']['thirty']
 book.section('I. The working (6,7) and the calculation chart','The working 154-letter factorization joins the literal saved source by checked disk operations and one explicit global conjugation. No sphere substitution occurs in this joining phase.')
 book.checkpoint('The working (6,7): complete factorization',new,working[0]['factors'])
 for i,s in enumerate(working[1:],1):book.move('I',i,s['title'],s['kind'],new,working[i-1]['factors'],new,s['factors'])
 book.section('II. The named-substitution route to fifty','All 145 saved atomic moves are retained in their forward order. Column chart frames and display-only sphere replacements are retained separately from the actual derivation moves.')
 n=len(old['states'])
 for i,s in enumerate(old['forward']['atomic']):
  before=old['states'][n-1-i];after=old['states'][n-2-i]
  extra='Display frames: before g='+(' '.join(map(str,before['frame'])) or 'identity')+'; after g='+(' '.join(map(str,after['frame'])) or 'identity')+'.'
  book.move('II',i+1,s['title'],s['kind'],old,before['factors'],old,after['factors'],extra)
 book.checkpoint('The actual positive fifty: complete factorization',new,extract[0]['factors'])
 book.section('III. Isolate an actual standard twenty','Seven disk Hurwitz moves and one explicit sphere rechart isolate the twenty at the bottom. It is a disk conjugate of W0. The remaining thirty is not assumed to be W1.')
 for i,s in enumerate(extract[1:],1):book.move('III',i,s['title'],s['kind'],new,extract[i-1]['factors'],new,s['factors'])
 book.checkpoint('The isolated standard twenty',new,extract[-1]['factors'][new['split']:])
 book.section('IV. The thirty and its exact disk-boundary ending','First remove the independently verified standard twenty in an explicit sphere move. The remaining proof does not assume the thirty product is identity. Every chart change is checked locally, the ordered disk product is checked on all five based meridians, and the final double cap is explicit.')
 for i,s in enumerate(thirty[1:],1):book.move('IV',i,s['title'],s['kind'],new,thirty[i-1]['factors'],new,s['factors'])
 book.section('V. The six-point sphere cut-system certificate','The visible comparison uses all six marked points and five consecutive-point arcs. There is no boundary-to-first-point arc. The independent faithful five-point disk calculation is retained as algebraic backup, with point 6 at infinity.')
 top=H-190;svg=(newroot/'sphere-cut.svg').read_text()
 book.text('<b>Calculated product, on the sphere</b>',M,top,CW,'caption');book.text('<b>Reference six-point sphere chain</b>',M+CW+GAP,top,CW,'caption')
 book.image(svg,M,top-95,CW,75);book.image(svg,M+CW+GAP,top-95,CW,75)
 y=book.text('All five adjacent-point arcs are recovered from the action and jointly certified. The separate disk calculation has the following equal actual/reference meridian images:',M,top-115,W-2*M)
 proof=cert['thirty_boundary']['stages'][-2]['disk_action_certificate']
 for i,image in enumerate(proof['actual'],1):y=book.text('x'+str(i)+' -> '+escape(' '.join(map(str,image))),M,y-8,W-2*M,'small')
 y=book.band('SPHERE MOVE: a five-point curve is complementary to a singleton curve.',y-15,True)
 book.text('The singleton twist is trivial in the marked-sphere mapping class group, so (sigma1 sigma2 sigma3 sigma4)^5 caps to that identity. Spherical braids retain a central order-two rotation, which is quotiented out when passing to sphere mapping classes. The chosen genus-two lift of this single twist is -I. Its square caps with +I, preserving the lifted identity in this proof. A framed inner boundary cannot be discarded this way. Both disk discrepancies and lift matrices are saved in sphere-cut-certificate.json.',M,y,W-2*M,'small')
 book.section('VI. Sources, limitations and downloadable certificates','The new ending is an independent exact boundary-action proof. The classification theorem is not used to infer identity. A shorter geometric derivation and an elementary full W0 W1 Hurwitz route remain separate improvements.')
 top=H-175
 for text in [
  'Graphical working seed and saved substitution route: https://richardbuckman-math.github.io/surface-diagrams/docs/proofs/six-seven-compact/index.html',
  'New twenty extraction, thirty boundary proof and certificates: https://richardbuckman-math.github.io/surface-diagrams/docs/proofs/six-seven-fifty-blocks/index.html',
  'Auroux, Fiber sums of genus 2 Lefschetz fibrations, https://arxiv.org/pdf/math/0204285. Lemmas 6-7 concern standard-block invariance; Theorem 9 recognizes transitive positive identity factorizations. Its identity hypothesis must not be reversed.',
  'Scope: sphere mapping-class action and the separately checked closed genus-two lift. No hidden disk equality, cumulative joint support drawing, or unperformed elementary Hurwitz normal form is claimed.',
  'Source SHA256: '+cert['source_sha256'],
  'All 177 atomic transitions in the linked chain are retained: 5 working-chart joins, 145 saved substitutions, 8 twenty-extraction moves, 1 explicit twenty closure, and 18 thirty-closure steps.'
 ]:top=book.text(escape(text),M,top,W-2*M,'body')-18
 book.finish()
 overlay=BytesIO();c=canvas.Canvas(overlay,pagesize=(W,H));c.setFillColor(HexColor('#18344a'));c.setFont(BOLD,16);c.drawString(M,H-160,'Complete diagram sequence')
 y=H-205
 for title,page in book.sections:
  c.setFont(BODY,14);c.drawString(M,y,title);c.drawRightString(W-M,y,str(page));y-=43
 c.setFont(BODY,8);c.drawString(M,y-15,'All atomic moves retained. Sphere moves labeled explicitly; certificates in Section VI.');c.save();overlay.seek(0)
 reader=PdfReader(TMP/'six-seven-body.pdf');writer=PdfWriter();writer.clone_document_from_reader(reader)
 writer.pages[contents_page-1].merge_page(PdfReader(overlay).pages[0])
 with OUT.open('wb') as f:writer.write(f)
 PUBLIC.write_bytes(OUT.read_bytes())
 (TMP/'six-seven-page-index.json').write_text(json.dumps(book.index,indent=2),encoding='utf-8')
 verified=PdfReader(OUT)
 assert len(verified.pages)==book.n
 assert all(tuple(map(float,p.mediabox[2:]))==(612.,792.) for p in verified.pages)
 assert 'SPHERE MOVE' in '\n'.join(p.extract_text() or '' for p in verified.pages)
 print('Saved',OUT,'pages',len(verified.pages),'bytes',OUT.stat().st_size,'vector forms',len(book.forms),flush=True)

if __name__=='__main__':build()
