"""Portrait vector PDF of the COMPLETE NAMED 101-step working (6,7) proof."""
from io import BytesIO
from pathlib import Path
from html import escape
import json
import build_six_seven_identity_pdf as base
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

ROOT=base.ROOT
OUT=ROOT/'output/pdf/six-seven-named.pdf'
PUBLIC=ROOT/'docs/proofs/six-seven-fifty-blocks/six-seven-named.pdf'

class NamedBook(base.Book):
    def __init__(self):
        super().__init__()
        self.c.setTitle('The working (6,7): complete named graphical derivation')
    def new(self,*args,**kwargs):
        top=super().new(*args,**kwargs)
        self.c.setFillColor(HexColor('#f5f7fa'));self.c.rect(base.M-1,11,base.W-2*base.M-40,16,stroke=0,fill=1)
        self.c.setFillColor(HexColor('#18344a'));self.c.setFont(base.BODY,7)
        self.c.drawString(base.M,16,'25 October 2026 | Named relations; individual supports; all sphere moves labeled')
        return top

def build():
    folder=ROOT/'docs/proofs/six-seven-fifty-blocks'
    data=json.loads((folder/'display-pure.json').read_text())
    certificate=json.loads((folder/'certificate.json').read_text())['named_full_route']
    shown=data['routes']['namedfull'];raw=certificate['stages']
    assert len(shown)==len(raw)==102
    book=NamedBook()
    top=book.new('The working (6,7): a complete named derivation',
        '101 graphical steps | Four explicit sphere moves | Portrait US Letter',bookmark='start')
    top=book.band('<b>VERY BRIEF SUMMARY.</b> Remove the incident half twists, use a five-point disk, turn the remaining positive factors into FOUR exterior twists by PC lanterns, roses, daisies and Hurwitz transports, then cap their fourth power.',top)
    top=book.text('The previously missing geometric boundary closure is now supplied. The final equality is obtained from actual named substitutions and factor transports, rather than a whole-product action recognition. All four sphere moves retain their disk discrepancies, exact sphere certificates and separately checked genus-two lift.',base.M,top,base.W-2*base.M)-15
    top=book.text('<b>What is still open.</b> This detailed route has 101 retained graphical steps: five fewer than the previous 106-step named proof and shorter than the earlier 177-step archive. It does not yet meet the goal of fewer than twenty meaningful operations. Reusable named patterns and fixed-factor drags are identified, with all adjacent checks retained in the certificates.',base.M,top,base.W-2*base.M)-15
    top=book.text('<b>How to read it.</b> Read each factorization downward. Curves are paired with the braid representing that exact support; blue marked-point dots continue at braid separators. Only the changed interval is printed at a move, with the unchanged factors counted above and below. Every actual SPHERE MOVE has a yellow banner. Individual supports are not cumulative joint cut-system certificates.',base.M,top,base.W-2*base.M)-15
    book.text('<b>Logical scope.</b> Common frames and cyclic starts are explicit conjugations. The terminal four-exterior product is central, so reversing those conjugations recovers the source equality without assuming it was central. Marked points are not framed boundaries; signed framing balances are retained for PC substitutions. A single five-point cap has lift -I; the sixth- and fourth-power caps used here have +I.',base.M,top,base.W-2*base.M)
    book.new('Contents','Full diagrams, named sub-derivations and sphere discrepancies.',bookmark='contents');contents_page=book.n
    top=book.new('What the steps will do',bookmark='plan')
    for title,text in [
        ('1. Reach the five-point chart.','Split the required squares, match and absorb the incident half twists, change the exterior point explicitly, and retain then separately cap the six framing corrections.'),
        ('2. Use the existing roots.','Borrow Q14 from the actual four-point daisy, transport it to match the original half twists, return the same Q14 and remove the last half pair. No auxiliary half twists are introduced.'),
        ('3. Extract two exterior twists.','Actual cabled lanterns and borrowed-petal configurations expose two visible exterior twists. Keep both while closing the residual factors.'),
        ('4. Return the borrowed root.','The actual 15, 14 and 45 curves form a transported PC rose. Return the resulting transported root across the old outer and close its daisy; an untransported root with the same enclosed points would fail.'),
        ('5. Align the four-point twists.','Two actual pair transports align the four-point curves. Combine them and use an explicit common disk frame to make their square round.'),
        ('6. Match two daisies and cap.','Three explicit petal swaps and two individually matched transported daisies give four identical exterior twists. Combine their fourth power, followed by a separate labeled sphere cap with +I lift.')]:
        top=book.text('<b>'+title+'</b> '+text,base.M,top,base.W-2*base.M)-15
    groups=[(0,17,'I. The fixed-point boundary chart'),(17,46,'II. Existing roots remove all half twists'),
            (46,68,'III. The first exterior and simpler inside daisy'),(68,76,'IV. Reach the second exterior twist'),
            (76,81,'V. Return the actual borrowed root'),(81,88,'VI. Align the four-point twists'),
            (88,97,'VII. Match the actual daisy petals'),(97,101,'VIII. Two daisies, four exteriors and the sphere cap')]
    for a,z,title in groups:
        book.section(title,'Actual ordered factor supports and their connected braids. All unchanged context is counted, and every retained move is shown.')
        if a in (0,76,97):book.checkpoint('Complete factorization before '+title.split('. ',1)[-1],data,shown[a]['factors'])
        for i in range(a,z):
            stage=shown[i+1];record=raw[i+1]
            extra=('Retained adjacent checks: '+str(record['adjacent_moves'])+'. ') if record.get('adjacent_moves') else ''
            if record.get('daisy_frame'):extra+='All five factors individually match the standard PC daisy in common chart '+str(tuple(record['daisy_frame']))+'. '
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
        'The new 23-operation named closure of the existing-root branch has 28 retained external adjacent checks, stays positive and never exceeds support-word maximum 16. Its rose and two final daisies also retain all internal named-pattern interchanges. Four actual exterior twists remain visible. The goal of an under-twenty complete derivation remains open.',
        'The archived 125-page/177-step PDF is preserved separately. This edition contains the new 101-step named proof, with no action-only boundary-recognition step.'
    ]:top=book.text(escape(text),base.M,top,base.W-2*base.M)-15
    top-=12
    top=book.text('<b>Independent jointly certified six-point sphere cut comparison</b>',base.M,top,base.W-2*base.M,'caption')-8
    svg=(folder/'early-sphere-cut.svg').read_text()
    book.image(svg,base.M,top-80,base.CW,70);book.image(svg,base.M+base.CW+base.GAP,top-80,base.CW,70)
    book.finish()
    overlay=BytesIO();c=canvas.Canvas(overlay,pagesize=(base.W,base.H));c.setFillColor(HexColor('#18344a'));c.setFont(base.BOLD,16);c.drawString(base.M,base.H-155,'Complete named diagram sequence');y=base.H-190
    for title,page in book.sections:
        c.setFont(base.BODY,10);c.drawString(base.M,y,title);c.drawRightString(base.W-base.M,y,str(page));y-=32
    c.setFont(base.BODY,8);c.drawString(base.M,y-15,'101 graphical steps retained. Four sphere moves labeled; full discrepancies in Section IX.');c.save();overlay.seek(0)
    reader=PdfReader(base.TMP/'six-seven-body.pdf');writer=PdfWriter();writer.clone_document_from_reader(reader);writer.pages[contents_page-1].merge_page(PdfReader(overlay).pages[0])
    with OUT.open('wb') as f:writer.write(f)
    PUBLIC.write_bytes(OUT.read_bytes())
    (base.TMP/'six-seven-named-page-index.json').write_text(json.dumps(book.index,indent=2),encoding='utf-8')
    verified=PdfReader(OUT);assert all(tuple(map(float,p.mediabox[2:]))==(612.,792.) for p in verified.pages)
    assert len(verified.pages)==book.n
    print('Saved',OUT,'pages',book.n,'bytes',OUT.stat().st_size,'steps',len(shown)-1,flush=True)
    return OUT

if __name__=='__main__':build()
