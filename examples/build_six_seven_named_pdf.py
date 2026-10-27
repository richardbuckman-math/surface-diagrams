"""Portrait vector PDF of the COMPLETE NAMED 90-step working (6,7) proof."""
from io import BytesIO
from pathlib import Path
from html import escape
import json,re,xml.etree.ElementTree as ET
import build_six_seven_identity_pdf as base
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

ROOT=base.ROOT
OUT=ROOT/'output/pdf/six-seven-named.pdf'
PUBLIC=ROOT/'docs/proofs/six-seven-fifty-blocks/six-seven-named.pdf'

def support_grid(svg):
    """Keep the exact curve, but remove point numbers and register its grid."""
    svg=re.sub(r'<text\b[^>]*class="marked-point-label"[^>]*>.*?</text>','',svg,flags=re.S)
    svg=base.compact_support_svg(svg)
    root=ET.fromstring(svg);width,height=map(float,root.attrib['viewBox'].split()[2:]);marks=[]
    def visit(node,sx=1,sy=1,tx=0,ty=0):
        transform=node.get('transform','')
        for op,args in re.findall(r'(translate|scale)\(([^)]+)\)',transform):
            v=list(map(float,args.replace(',',' ').split()))
            if op=='translate':tx+=sx*v[0];ty+=sy*(v[1] if len(v)>1 else 0)
            else:sx*=v[0];sy*=v[1] if len(v)>1 else v[0]
        if re.sub(r'(translate|scale)\([^)]+\)','',transform).strip():raise ValueError('Unsupported support-grid transform')
        if node.get('class')=='marked-point':
            marks.append((sx*float(node.get('cx'))+tx,sy*float(node.get('cy'))+ty,abs(sx)*float(node.get('r'))))
        for child in node:visit(child,sx,sy,tx,ty)
    visit(root);marks.sort()
    if len(marks)!=6:raise ValueError('The named proof requires six marked points')
    pitch=marks[1][0]-marks[0][0];cy=marks[0][1];radius=marks[0][2]
    if pitch<=0 or any(abs(x-marks[0][0]-i*pitch)>1e-5 or abs(y-cy)>1e-5 or abs(r-radius)>1e-5 for i,(x,y,r) in enumerate(marks)):
        raise ValueError('The source marked-point grid is not uniform')
    cx=(marks[0][0]+marks[-1][0])/2
    return dict(svg=svg,width=width,height=height,cx=cx,cy=cy,pitch=pitch,
                side=max(cx,width-cx)/pitch,vertical=max(cy,height-cy)/pitch,
                radius_ratio=radius/pitch)

class NamedBook(base.Book):
    def __init__(self,data,states):
        super().__init__()
        self.c.setTitle('The working (6,7): complete named graphical derivation')
        supports={data['rows'][i]['support'] for state in states for i in state['factors']}
        self.grids={i:support_grid(data['supports'][i]) for i in supports}
        self.svg_grids={data['supports'][i]:g for i,g in self.grids.items()}
        # One physical pitch throughout the PDF, including full-page checkpoints.
        available=base.CW-base.BW-72-10
        self.point_pitch=min(18.,available/(2*max(g['side'] for g in self.grids.values())))
        if any(abs(g['radius_ratio']-.07)>1e-5 for g in self.grids.values()):raise ValueError('Inconsistent source dot size')
    def height(self,row):
        return max(super().height(row),2*self.grids[row['support']]['vertical']*self.point_pitch+4)
    def support(self,svg,x,y,width,height):
        g=self.svg_grids[svg];scale=self.point_pitch/g['pitch']
        # Anchor the six dots, rather than centering each curve's changing bounds.
        self.image(g['svg'],x+width/2-g['cx']*scale,
                   y+height/2-(g['height']-g['cy'])*scale,
                   g['width']*scale,g['height']*scale)
    def new(self,*args,**kwargs):
        top=super().new(*args,**kwargs)
        self.c.setFillColor(HexColor('#f5f7fa'));self.c.rect(base.M-1,11,base.W-2*base.M-40,16,stroke=0,fill=1)
        self.c.setFillColor(HexColor('#18344a'));self.c.setFont(base.BODY,7)
        self.c.drawString(base.M,16,'27 October 2026 | Named relations; individual supports; all sphere moves labeled')
        return top

def build():
    folder=ROOT/'docs/proofs/six-seven-fifty-blocks'
    data=json.loads((folder/'display-pure.json').read_text())
    certificate=json.loads((folder/'certificate.json').read_text())['named_full_route']
    shown=data['routes']['namedfull'];raw=certificate['stages']
    assert len(shown)==len(raw)==91
    book=NamedBook(data,shown)
    top=book.new('The working (6,7): a complete named derivation',
        '90 graphical steps | Four explicit sphere moves | Portrait US Letter',bookmark='start')
    top=book.band('<b>VERY BRIEF SUMMARY.</b> Remove the incident half twists, use a five-point disk, turn the remaining positive factors into FOUR exterior twists by PC lanterns, roses, daisies and Hurwitz transports, then cap their fourth power.',top)
    top=book.text('The previously missing geometric boundary closure is now supplied. The final equality is obtained from actual named substitutions and factor transports, rather than a whole-product action recognition. All four sphere moves retain their disk discrepancies, exact sphere certificates and separately checked genus-two lift.',base.M,top,base.W-2*base.M)-15
    top=book.text('<b>What is still open.</b> This detailed route has 90 retained graphical steps: one fewer than the previous91-step proof and eleven fewer than the101-step version and shorter than the earlier 177-step archive. It does not yet meet the goal of fewer than twenty meaningful operations. Reusable named patterns and fixed-factor drags are identified, with all adjacent checks retained in the certificates.',base.M,top,base.W-2*base.M)-15
    top=book.text('<b>How to read it.</b> Read each factorization downward. Curves are paired with the braid representing that exact support; blue marked-point dots continue at braid separators. The unnumbered support points use the same size and spacing in every factor. Only the changed interval is printed at a move, with the unchanged factors counted above and below. Every actual SPHERE MOVE has a yellow banner. Individual supports are not cumulative joint cut-system certificates.',base.M,top,base.W-2*base.M)-15
    book.text('<b>Logical scope.</b> Common frames and cyclic starts are explicit conjugations. The terminal four-exterior product is central, so reversing those conjugations recovers the source equality without assuming it was central. Marked points are not framed boundaries; signed framing balances are retained for PC substitutions. A single five-point cap has lift -I; the sixth- and fourth-power caps used here have +I.',base.M,top,base.W-2*base.M)
    book.new('Contents','Full diagrams, named sub-derivations and sphere discrepancies.',bookmark='contents');contents_page=book.n
    top=book.new('What the steps will do',bookmark='plan')
    for title,text in [
        ('1. Reach the five-point chart.','Split the required squares, match and absorb the incident half twists, change the exterior point explicitly, and retain then separately cap the six framing corrections.'),
        ('2. Use the existing roots.','Borrow Q14 from the actual four-point daisy, transport it to match the original half twists, return the same Q14 and remove the last half pair. A cyclic start after the square and outer bypasses a standalone commutation; the short-side drag crosses that outer and later rejoins the same Q15 state. No auxiliary half twists are introduced.'),
        ('3. Extract two exterior twists.','Actual cabled lanterns and borrowed-petal configurations expose two visible exterior twists. Keep both while closing the residual factors.'),
        ('4. Return the loan as six actual pairs.','Use the positive T45 common frame, commute the central exterior and transport the same outer upward by inverse Hurwitz moves. The actual six pairs match the expanded PC rose without a preliminary petal reorder or a temporary three-point root.'),
        ('5. Carry the first outer upward.','Choose the cyclic cut before gathering the first daisy, then carry the same outer UP through its petals. This changes the actual route and avoids dragging it through the second outer. Return the extra square unit; all five inputs match the transported PC daisy.'),
        ('6. Close the second daisy in its cyclic order.','Start at the new exterior, move the extra petal past only two central exteriors, and match the actual cyclic PC daisy. All individual inputs, seven internal interchanges, the internal cyclic conjugation and complete nonabelian kernels are retained. Four exterior twists remain visible, then combine and undergo the separate fourth-power sphere cap with +I lift.')]:
        top=book.text('<b>'+title+'</b> '+text,base.M,top,base.W-2*base.M)-15
    groups=[(0,17,'I. The fixed-point boundary chart'),(17,45,'II. Existing roots remove all half twists'),
            (45,66,'III. The first exterior and simpler inside daisy'),(66,74,'IV. Reach the second exterior twist'),
            (74,79,'V. Return the loan as an expanded rose'),(79,85,'VI. Carry the first outer upward'),
            (85,88,'VII. Close the second daisy in cyclic order'),(88,90,'VIII. Four exteriors and the sphere cap')]
    for a,z,title in groups:
        book.section(title,'Actual ordered factor supports and their connected braids. All unchanged context is counted, and every retained move is shown.')
        if a in (0,74,88):book.checkpoint('Complete factorization before '+title.split('. ',1)[-1],data,shown[a]['factors'])
        for i in range(a,z):
            stage=shown[i+1];record=raw[i+1]
            extra=('Retained adjacent checks: '+str(record['adjacent_moves'])+'. ') if record.get('adjacent_moves') else ''
            if record.get('daisy_frame'):extra+='All five factors individually match the standard PC daisy in common chart '+str(tuple(record['daisy_frame']))+'. '
            if record.get('inverse_hurwitz_transport'):extra+='Inverse transport: the same outer moves upward and is conjugated at each crossed petal. '
            if record.get('named_pattern_witness',{}).get('internal_cyclic_start',{}).get('shift'):extra+='Named PC daisy in its checked cyclic order; every input and the full internal conjugation are retained. '
            if stage['kind']=='disk_cyclic_start':extra+='Explicit common conjugation; its full braid frame is saved. '
            if stage['kind']=='sphere_rewrite':extra+='SPHERE MOVE: full disk discrepancy appears in Appendix IX; chosen lift is +I. '
            book.move(title.split('.',1)[0],i+1,stage['title'],stage['kind'],data,shown[i]['factors'],data,stage['factors'],extra)
    book.section('IX. Sphere discrepancies and certificates','The following are ALL FOUR sphere operations in this named route. They are not disk braid equalities. Each discrepancy is written in signed generator indices; the exact sphere certificate and +I lift are retained online.')
    for i,stage in enumerate(raw):
        if stage['kind']!='sphere_rewrite':continue
        top=book.new('SPHERE MOVE at step '+str(i),base.plain(stage['title']))
        top=book.band('Exact sphere action certified. Chosen genus-two lift discrepancy: +I. This is not an equality in the ordinary disk braid group.',top,True)
        word=list(stage['disk_discrepancy'])
        top=book.text('<b>FULL DISK DISCREPANCY</b> ('+str(len(word))+' signed braid letters):',base.M,top,base.W-2*base.M)-8
        for start in range(0,len(word),24):
            if top<70:top=book.new('SPHERE DISCREPANCY - continued')
            top=book.text(escape(' '.join(map(str,word[start:start+24]))),base.M,top,base.W-2*base.M,'small')-4
    top=book.new('Certificates and exact scope')
    for text in [
        'Complete named graphical route: https://richardbuckman-math.github.io/surface-diagrams/docs/proofs/six-seven-fifty-blocks/index.html?phase=namedfull',
        'Full raw certificates: https://richardbuckman-math.github.io/surface-diagrams/docs/proofs/six-seven-fifty-blocks/certificate.json',
        'The independent six-point sphere cut comparison has six marked points and five consecutive-point arcs. It is separately jointly certified; the individual factor supports in this book are not joint cut complexes.',
        'The older23-operation closure remains available as a separate chapter. A positive T45 frame bounds the unreordered six-pair rose. An earlier cyclic cut lets the first outer pass upward through its own petals, avoiding the second outer. The second actual daisy is matched in cyclic order, with its full internal common conjugation and four nonabelian petal kernels retained. This saves one operation and two external adjacent checks from91. The new fourteen-operation closure stays within support maximum18; the whole disk tail stays within20. Four actual exterior twists remain visible. The under-twenty complete derivation remains open.',
        'The archived 125-page/177-step PDF is preserved separately. This edition contains the new 90-step named proof, with no action-only boundary-recognition step.'
    ]:top=book.text(escape(text),base.M,top,base.W-2*base.M)-15
    top-=12
    top=book.text('<b>Independent jointly certified six-point sphere cut comparison</b>',base.M,top,base.W-2*base.M,'caption')-8
    svg=(folder/'early-sphere-cut.svg').read_text()
    book.image(svg,base.M,top-80,base.CW,70);book.image(svg,base.M+base.CW+base.GAP,top-80,base.CW,70)
    book.finish()
    overlay=BytesIO();c=canvas.Canvas(overlay,pagesize=(base.W,base.H));c.setFillColor(HexColor('#18344a'));c.setFont(base.BOLD,16);c.drawString(base.M,base.H-155,'Complete named diagram sequence');y=base.H-190
    for title,page in book.sections:
        c.setFont(base.BODY,10);c.drawString(base.M,y,title);c.drawRightString(base.W-base.M,y,str(page));y-=32
    c.setFont(base.BODY,8);c.drawString(base.M,y-15,'90 graphical steps retained. Four sphere moves labeled; full discrepancies in Section IX.');c.save();overlay.seek(0)
    reader=PdfReader(base.TMP/'six-seven-body.pdf');writer=PdfWriter();writer.clone_document_from_reader(reader);writer.pages[contents_page-1].merge_page(PdfReader(overlay).pages[0])
    with OUT.open('wb') as f:writer.write(f)
    PUBLIC.write_bytes(OUT.read_bytes())
    (base.TMP/'six-seven-named-page-index.json').write_text(json.dumps(book.index,indent=2),encoding='utf-8')
    verified=PdfReader(OUT);assert all(tuple(map(float,p.mediabox[2:]))==(612.,792.) for p in verified.pages)
    assert len(verified.pages)==book.n
    print('Saved',OUT,'pages',book.n,'bytes',OUT.stat().st_size,'steps',len(shown)-1,flush=True)
    return OUT

if __name__=='__main__':build()
