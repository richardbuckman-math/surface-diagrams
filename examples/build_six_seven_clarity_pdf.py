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
    def new(self,*args,**kwargs):
        top=super().new(*args,**kwargs)
        self.c.setFillColor(HexColor('#f5f7fa'));self.c.rect(base.M-1,11,base.W-2*base.M-40,16,stroke=0,fill=1)
        self.c.setFillColor(HexColor('#18344a'));self.c.setFont(base.BODY,7)
        self.c.drawString(base.M,16,'30 October 2026 | Named relations; individual supports; all sphere moves labeled')
        return top


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
        '<b>What a step means.</b> A numbered step is a set of independent factor-interval edits. Moves a,b,... are listed one after another for printing, but each starts from the SAME step input and they may be performed in either order. Every proposed parallel pair has a literal two-order certificate. A singleton step contains one move. Some independent edits are deliberately shown in separate steps for readability.',
        '<b>These numbers do not claim a shorter proof.</b> This follows the longer '+str(summary['source_operations'])+'-operation source, with the simpler early prefix, delayed petals, lower half meeting and returned round 45 loan: the F2 half-twist neighborhood has length 4 rather than 12, and the half-neighborhood total at the matched checkpoint drops from 80 to 72. These are support lengths in this chart; the maximum stays 30. The shorter 79-operation route remains archived. More complicated or more tangled curves are not preferable merely because they use fewer arrows. Future research will prioritize simpler arc/curve supports and their interactions.',
        '<b>Delayed petals.</b> Keep the three-point root intact while the last two half twists are handled. Expand it only after those halves have combined, on its own step. This keeps 17 rows rather than 19 during the gather. The two actual half-twist classes are unchanged; this reduces diagram clutter, not arc complexity.',
        '<b>Framing ledger.</b> The ledger is separate from the main factor list. The represented word is ledger times main factorization. During the five-point rechart, each same-curve redraw records its boundary correction here. The SIX corrections are kept explicitly, redrawn as one peripheral powered curve, and only then cleared. An individual curve rechart can carry a deck sign; the ledger retains it. A single five-point cap would have -I and is never silently used.',
        '<b>Drawing conventions.</b> Read factors downward. All support diagrams keep the same unnumbered six-point grid: 18pt spacing and 1.26pt radius. Braids represent the pictured disk word and remain connected. Individual support pictures are not joint cut-system certificates. Parallel factor edits do not assert a simultaneous ambient isotopy of an entire joint cut system.'
    ]:top=book.text(text,base.M,top,base.W-2*base.M)-16
    top=book.new('Let the final half twists meet lower',
        'The same two arcs; a different meeting place; two more listed moves.',bookmark='lower-meeting')
    for text in [
        'The two remaining half twists already have the same arc. The old route carried the lower half twist upward through all six intervening factors. That made several surrounding curves wind more before the half twists could combine.',
        '<b>The new route.</b> Carry the upper half twist DOWN past the first five intervening factors. Independently, carry the lower half twist UP past the squared pair. Each carried half twist keeps its original arc; the crossed factors change by the displayed Hurwitz moves. These two carries act on disjoint factor intervals, so both start from the same input and either order gives exactly the same result.',
        'The halves are now adjacent near the bottom of that interval. Combine them THERE into their full twist. Only then carry the full twist upward through the five neighbors. This rejoins exactly the previous complete derivation; the retained three-point root still expands later on its own step.',
        '<b>What this improves.</b> While the two half twists remain, the exact closed-neighborhood crossing sum is at most 936 rather than 1094, and the largest pair has 36 crossings rather than 48. Several surrounding curves show less nested winding. The half arcs themselves are unchanged. These are closed-neighborhood counts, not intersections of the arcs or one jointly minimal drawing.',
        '<b>The tradeoff.</b> The support-word maximum in this local route is 18 rather than 17. Four listed moves and eleven adjacent checks replace two moves and six checks. The final full-twist carry restores the old endpoint geometry after the halves disappear. This is a choice about clarity during the half-twist part, not a shorter proof or a reduction in overall geometric complexity.'
    ]:top=book.text(text,base.M,top,base.W-2*base.M)-16
    top=book.new('Return the retained outer after borrowing 45',
        'Two final pair curves straighten; five more source moves; no new sphere move.',bookmark='late45-return')
    for text in [
        'Near the end, three standard unit exterior twists are already visible. The remaining four-point outer and four pair curves give a valid named daisy. Two of those pair curves still have nested winding, with support lengths 6 and 4.',
        '<b>The actual loan.</b> Expand that retained outer by a fully matched PC daisy, on its own presentation step. Its checked internal chart lends the actual round 45 full twist. All factors remain full positive twists; an inverse braid generator in the common chart is not a half-twist factor.',
        'An explicit cyclic start puts 45 first. Carry the SAME 45 through all TEN actual neighbors, including every donor leftover and all three earlier exteriors. Every adjacent move is reconstructed before normalization. A second explicit cyclic start gathers the changed donor daisy, and its named contraction RETURNS the original four-point outer literally.',
        '<b>The result.</b> Only the two wound pair curves change. Their support lengths fall from 6 to 2 and 4 to 2. The other SIX source records keep their actual curves and presentations. All 28 pairwise minimal CLOSED intersection counts remain the same. At the returned eight-record checkpoint, maximum/total support is 5/27 rather than 6/33; stored braid letters are 88 rather than 96.',
        '<b>The cost.</b> The temporary donor has ELEVEN rows instead of eight, with total support 42 rather than 33. Its largest individual support word stays at 6. Eight source moves and fourteen external adjacent checks replace three moves and two checks. The late donor-return and short 24 gather are genuinely independent and can share a step: both cards start from the SAME input, with a literal two-order certificate.',
        'The final five actual inputs then match the twice-modified D5 daisy in a complete common chart. Four standard unit exteriors remain visible, each with lift -I. Combining them, redrawing their FOURTH power on the sphere and clearing the already-peripheral power remain separate. Every one of the thirteen sphere-discrepancy WORDS is unchanged.',
        '<b>Scope.</b> These are support lengths in the chosen chart, not arc crossings, jointly minimal diagrams or whole-proof bounds. All half-twist classes and the earlier lower meeting stay unchanged. The previous 101-move/71-step certificate, payload, page source and PDF are pinned byte-for-byte, with a functional interactive archive.'
    ]:top=book.text(text,base.M,top,base.W-2*base.M)-16
    book.new('Contents','Independent steps, their individual moves, and complete redraw discrepancies.',bookmark='contents');contents=book.n
    section=None;appendices=[]
    for n,shown in enumerate(states[1:],1):
        round_data=proof['parallel_rounds'][n-1]
        source_indices=[proof['stages'][card['move_index']]['source_index'] for card in round_data['cards']]
        category=1 if max(source_indices)<=14 else 2 if max(source_indices)<=17 else 3 if max(source_indices)<summary['source_operations']-1 else 4
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
        'Priority: favor simpler arcs and curves and less tangled interactions, even when more moves are needed. Parallel steps require actual independence, not a smaller number of navigation labels.',
        'Round 45 loan source: six-seven-preferred-late45.json. The actual retained outer returns literally; all source input/output charts, signed PC balances and full nonabelian kernels AND shadows remain explicit. The half-meeting 101/71 edition is pinned as clarity-half-meeting-certificate.json / display-half-meeting.json / six-seven-named-half-meeting.pdf.'
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
