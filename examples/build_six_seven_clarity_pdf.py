"""Export clarity-first parallel rounds with separate sphere redraw diagrams."""
from pathlib import Path
from html import escape
from io import BytesIO
import json,hashlib
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import build_six_seven_identity_pdf as base
from build_six_seven_named_pdf import NamedBook

class MoveLabel:
    def __init__(self,label):self.label=label
    def __format__(self,spec):return self.label

class ClearBook(NamedBook):
    presentation_kind=''
    def move_key(self,row):return row['clarity_row_index']
    def text(self,s,*args,**kw):
        if s.startswith('SPHERE MOVE:'):s='SPHERE REDRAW ONLY: the same curve or arc, with the same factor and power. Framing ledger retained separately.'
        if s.startswith('DISK MOVE:') and self.presentation_kind=='peripheral_cleanup':s='PERIPHERAL CLEANUP: the curve has already been redrawn around one point; its even powered twist is trivial in the chosen lift.'
        return super().text(s,*args,**kw)


def build():
    root=base.ROOT;folder=root/'docs/proofs/six-seven-fifty-blocks'
    data=json.loads((folder/'display-clear.json').read_text(encoding='utf-8'))
    proof=json.loads((folder/'clarity-certificate.json').read_text(encoding='utf-8'))
    for i,row in enumerate(data['rows']):row['clarity_row_index']=i
    states=data['routes']['clearfull'];summary=data['summary']
    assert summary['source_sha256']==hashlib.sha256((folder/'certificate.json').read_bytes()).hexdigest(),'Rebuild the clarity payload after changing its source'
    book=ClearBook(data,[dict(factors=list(range(len(data['rows']))))])
    top=book.new('The working (6,7): a clearer graphical derivation',
        str(summary['listed_moves'])+' listed moves in '+str(summary['parallel_steps'])+' independent steps | Clarity before count',bookmark='start')
    top=book.band('<b>READ THE PICTURES AS THREE DIFFERENT ACTIONS.</b> A blue disk substitution changes factors by a named identity. A yellow sphere redraw changes only the drawing of the same curve or arc. A peripheral cleanup is shown on a separate line, after its curve is already peripheral.',top)
    for text in [
        '<b>What a step means.</b> A numbered step is a set of independent factor-interval edits. Moves a,b,... are listed one after another for printing, but each starts from the SAME step input and they may be performed in either order. Every proposed parallel pair has a literal two-order certificate. A singleton step contains one move.',
        '<b>These numbers do not claim a shorter proof.</b> This follows the longer 82-operation prefix route: the F2 half-twist neighborhood has length 4 rather than 12, and the half-neighborhood total at the matched checkpoint drops from 80 to 72. These are support lengths in this chart; the maximum stays 30. The shorter 79-operation route remains archived. More complicated or more tangled curves are not preferable merely because they use fewer arrows. Future research will prioritize simpler arc/curve supports and their interactions.',
        '<b>Framing ledger.</b> The ledger is separate from the main factor list. The represented word is ledger times main factorization. During the five-point rechart, each same-curve redraw records its boundary correction here. The SIX corrections are kept explicitly, redrawn as one peripheral powered curve, and only then cleared. An individual curve rechart can carry a deck sign; the ledger retains it. A single five-point cap would have -I and is never silently used.',
        '<b>Drawing conventions.</b> Read factors downward. All support diagrams keep the same unnumbered six-point grid: 18pt spacing and 1.26pt radius. Braids represent the pictured disk word and remain connected. Individual support pictures are not joint cut-system certificates. Parallel factor edits do not assert a simultaneous ambient isotopy of an entire joint cut system.'
    ]:top=book.text(text,base.M,top,base.W-2*base.M)-16
    book.new('Contents','Independent steps, their individual moves, and complete redraw discrepancies.',bookmark='contents');contents=book.n
    section=None;appendices=[]
    for n,shown in enumerate(states[1:],1):
        round_data=proof['parallel_rounds'][n-1]
        source_indices=[proof['stages'][card['move_index']]['source_index'] for card in round_data['cards']]
        category=1 if max(source_indices)<=14 else 2 if max(source_indices)<=17 else 3 if max(source_indices)<81 else 4
        titles={1:'I. Prepare and apply the disk lantern',2:'II. Sphere redraws and the separate framing ledger',3:'III. Positive disk transports and named relations',4:'IV. The terminal redraw and peripheral cleanup'}
        if category!=section:
            section=category;book.section(titles[category],
                'Every substitution and sphere redraw is separate. Independent moves share a step number; their individual diagrams remain visible.')
        moves=shown['parallel_moves'];letters=', '.join(m['letter'] for m in moves)
        for card_index,m in enumerate(moves):
            parallel=len(moves)>1;label=str(n).zfill(3)+(m['letter'] if parallel else '')
            extra=('PARALLEL STEP '+str(n)+': moves '+letters+' are independent and each starts from the SAME input. Both orders are certified. ' if parallel else '')
            if m['kind'] in ('sphere_redraw','curve_redraw'):extra+='REDRAW ONLY: factor identity, position, power and sphere curve are retained. '
            if m['framing_increment']:extra+='Separate framing ledger: add '+str(m['framing_increment'])+' boundary twist(s); no factor is inserted into the main diagram. '
            before=m['before'];after=m['after'];ia=before['factors'];ib=after['factors']
            if ia==ib and before['ledger']!=after['ledger']:
                ia=[] if before['ledger'] is None else [before['ledger']]
                ib=[] if after['ledger'] is None else [after['ledger']]
                extra+='THIS ROW IS THE SEPARATE FRAMING LEDGER; the main factor list is unchanged. '
            elif before['ledger'] is not None or after['ledger'] is not None:
                def led(x):return 'empty' if x is None else data['rows'][x]['label']
                extra+='Ledger before: '+led(before['ledger'])+'; ledger after: '+led(after['ledger'])+'. '
            book.presentation_kind=m['kind'];kind='sphere_rewrite' if m['kind']=='sphere_redraw' else m['kind']
            book.move(str(category),MoveLabel(label),m['title'],kind,data,ia,data,ib,extra)
            if m['kind']=='sphere_redraw':appendices.append((label,m))
    book.section('V. Full sphere-redraw discrepancies','Every genuine sphere redraw is listed below. Each has the same geometric curve, an explicit full disk discrepancy, exact marked-sphere action and corrected chosen +I lift. The framing ledger is included in the full word.')
    for label,m in appendices:
        top=book.new('SPHERE REDRAW at step '+label,escape(m['title']))
        top=book.band('Drawing change only; no lantern or other substitution is included. The corrected full discrepancy has exact sphere action and chosen +I lift.',top,True)
        values=[('FULL DISK DISCREPANCY including ledger',m['disk_discrepancy'])]
        if m['corrected_local_disk_discrepancy']:values.append(('LOCAL CURVE DISCREPANCY with its explicit framing correction',m['corrected_local_disk_discrepancy']))
        for title,w in values:
            top=book.text('<b>'+title+'</b> ('+str(len(w))+' signed letters)',base.M,top,base.W-2*base.M)-9
            for start in range(0,len(w),24):
                if top<65:top=book.new('SPHERE REDRAW discrepancy - continued')
                top=book.text(escape(' '.join(map(str,w[start:start+24]))),base.M,top,base.W-2*base.M,'small')-4
    top=book.new('Certificates and scope')
    for text in [
        'Preferred graphical route: https://richardbuckman-math.github.io/surface-diagrams/docs/proofs/six-seven-fifty-blocks/index.html?phase=clearfull',
        'Clarity certificates: clarity-certificate.json. The archived 79-operation source, the longer early prefix, and all their named-pattern witnesses remain unchanged in certificate.json / named_full_route.',
        str(summary['listed_moves'])+' moves are displayed in '+str(summary['parallel_steps'])+' certified independent steps. This is a presentation structure, not a mathematical-shortening claim. All source Hurwitz checks, named witnesses, signed PC balances and nonabelian kernels remain referenced.',
        'The first lantern is now an exact disk substitution with its four-point outer retained. The following sphere move only redraws that ONE outer curve as its complementary pair. Framing corrections in the later chart are held in a separate explicit ledger. Peripheral deletion always follows its own curve redraw.',
        'The thirteen genuine sphere redraws retain full discrepancies and corrected lifts. Four other chart redraws are already disk equalities. No standalone odd exterior cap is used. The archive 125-page/177-step PDF remains unchanged.',
        'Priority: favor simpler arcs and curves and less tangled interactions, even when more moves are needed. Parallel steps require actual independence, not a smaller number of navigation labels.'
    ]:top=book.text(escape(text),base.M,top,base.W-2*base.M)-16
    top=book.text('<b>Independent jointly certified six-point / five-arc comparison</b>',base.M,top-8,base.W-2*base.M,'caption')-8
    if top<140:top=book.new('Independent six-point / five-arc comparison')
    svg=(folder/'early-sphere-cut.svg').read_text(encoding='utf-8')
    book.image(svg,base.M,top-80,base.CW,70);book.image(svg,base.M+base.CW+base.GAP,top-80,base.CW,70)
    book.finish()
    overlay=BytesIO();c=canvas.Canvas(overlay,pagesize=(base.W,base.H));c.setFillColor(HexColor('#18344a'));c.setFont(base.BOLD,16);c.drawString(base.M,base.H-155,'Clarity-first diagram sequence');y=base.H-190
    for title,page in book.sections:
        c.setFont(base.BODY,10);c.drawString(base.M,y,title);c.drawRightString(base.W-base.M,y,str(page));y-=36
    c.setFont(base.BODY,8);c.drawString(base.M,y-15,str(summary['listed_moves'])+' moves; '+str(summary['parallel_steps'])+' independent steps. No shortening claim.');c.save();overlay.seek(0)
    reader=PdfReader(base.TMP/'six-seven-body.pdf');writer=PdfWriter();writer.clone_document_from_reader(reader)
    writer.pages[contents-1].merge_page(PdfReader(overlay).pages[0])
    output=root/'output/pdf/six-seven-named.pdf'
    with output.open('wb') as f:writer.write(f)
    (folder/'six-seven-named.pdf').write_bytes(output.read_bytes())
    (base.TMP/'six-seven-clear-page-index.json').write_text(json.dumps(book.index,indent=2),encoding='utf-8')
    print('Saved clarity PDF',book.n,'pages,',summary['listed_moves'],'moves,',summary['parallel_steps'],'parallel steps')
    return output


if __name__=='__main__':build()
