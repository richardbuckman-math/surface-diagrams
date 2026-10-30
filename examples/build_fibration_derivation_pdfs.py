"""Export the three checked derivations as separate vector Letter PDFs."""
from pathlib import Path
from html import escape
import json,shutil
from hashlib import sha256
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
import build_six_seven_identity_pdf as base
from build_six_seven_named_pdf import NamedBook
from build_fibration_derivations import TITLES,SCOPES
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'docs/proofs/fibration-derivations'
base.TMP=ROOT/'tmp/pdfs/fibration-derivations';base.TMP.mkdir(parents=True,exist_ok=True)

class Label:
    def __init__(self,s):self.s=s
    def __format__(self,fmt):return self.s

class Book(NamedBook):
    def __init__(self,slug,data):
        self.slug=slug;self.scope_text='';super().__init__(data,data['states'])
        self.point_pitch=18.;self.c.setTitle(TITLES[slug]);self.c.setAuthor('Richard Buckman - surface-diagrams')
    def new(self,*args,**kwargs):
        top=super().new(*args,**kwargs)
        self.c.setFillColor(HexColor('#f5f7fa'));self.c.rect(base.M-1,base.H-32,base.W-2*base.M+2,16,stroke=0,fill=1)
        self.c.rect(base.M-1,11,base.W-2*base.M-40,16,stroke=0,fill=1)
        self.c.setFillColor(HexColor('#18344a'));self.c.setFont(base.BOLD,9)
        self.c.drawString(base.M,base.H-25,'SURFACE DIAGRAMS / TYPE ('+self.slug.replace('-',',')+') / CHECKED DERIVATION')
        self.c.setFont(base.BODY,7);self.c.drawString(base.M,16,'30 October 2026 | Actual supports; construction and sphere redraws distinguished')
        return top
    def band(self,s,top,sphere=False):
        if s.startswith(('DISK MOVE:','SPHERE MOVE:','EXPLICIT GLOBAL')):s=self.scope_text
        return base.Book.band(self,s,top,sphere)

def build(slugs=('6-2','4-3','10-10')):
    results=[]
    for slug in slugs:
        d=json.loads((FOLDER/(slug+'.display.json')).read_bytes());r=json.loads((FOLDER/(slug+'.json')).read_bytes())
        b=Book(slug,d);top=b.new(TITLES[slug],str(r['operations'])+' recorded steps | '+str(r['listed_operations'])+' individual operations | '+str(r['adjacent_checks'])+' external adjacent checks',bookmark='start')
        intro={
        '6-2':['Let A be the full twist on123 and B the full twist on456. Let H be the ordered half twists14,25,36 and r=sigma5 sigma4 sigma3 sigma2 sigma1. The checked block-rotation identity is r^3=ABH. The SAME H exchanges A and B individually. Thus the six-point boundary twist is (ABH)^2, and the retained actual carries give A^2 B^2 H^2.',
               'This yields two squared triple twists and six unit half twists, type(6,2). The full six-point disk boundary twist has identity marked-sphere action and chosen+I lift. The disk derivation and those closure checks are separate.'],
        '4-3':['The proof begins with the SAME explicit positive Q45^4 compensation on the left of the squared five-point boundary twist. Two cabled PC daisies, with all parallel-copy framing corrections recorded, give eight positive ordinary triple roots. Their cyclic start and two combines expose the two half-lantern inputs.',
               'Expand the later input first. Each half lantern exposes a positive Q45^2 correction; it is carried upward across ONLY commuting ordinary roots. No half-twist arc is crossed by these ledger gathers. The two corrections combine to the SAME Q45^4 prefix. Cancel it from BOTH sides of the relation, as explicit algebraic bookkeeping, not a sphere cap or deletion from a fixed-product fibration.',
               'Five further adjacent Hurwitz checks and a matched combine give seven actual factors: four unit halves and three squared triples, type(4,3). They individually match the imported original A presentation. Its product is the squared five-point boundary twist, with a separate marked-sphere identity and chosen+I lift.'],
        '10-10':['Use the original EXACT algebraic A, B and C source blocks imported from the other project. Each has type(4,3) and product D5^2. Assemble B,A,C explicitly; this is a three-copy construction. Independent seven-factor rotations share one SAME input. Every subsequent source pull and both matching-half combines are checked before the sixth point is added on the LEFT.',
                 'The complete embedded target remains recorded. D5^6 is never assumed central in B6. The actual merged pair matches the saved local chart individually. First redraw ONLY the same pair curve from its complementary side, retaining factor identity, power, full disk discrepancy and separate sphere/+I checks. The following cabled half-lantern substitution is an EXACT DISK relation with its own complete named proof.',
                 'The final20 actual factors have type(10,10), identity marked-sphere action and chosen+I lift. Four later drawing edits in the old project fail closure; their exact data and nonidentity homology matrix are preserved separately. They are not used here. The older twenty dictated routes in this repository remain unchanged.']}
        for text in intro[slug]:top=b.text(escape(text),base.M,top,base.W-2*base.M)-15
        top=b.text('<b>Reading the diagrams.</b> Half-twist arcs have H labels; closed curves have T labels. Ordinary triple twists are temporary calculation factors. All factor grids have SIX UNNUMBERED points at18pt pitch and1.26pt radius. The connected braid represents the exact displayed factor words. Individual supports are not a joint cut-system or jointly minimal drawing.',base.M,top,base.W-2*base.M)-15
        b.text('<b>Certificate scope.</b> Faithful disk actions, raw free-word reconstructions, complete actual kernels AND shadows when the last strand is fixed, full actions for halves that move it, and separate sphere/lift checks remain in '+slug+'.json. Internal named-rule checks are retained separately from the external-check count. No unchosen framed-half-hole convention is asserted.',base.M,top,base.W-2*base.M)
        b.checkpoint('The explicit starting construction',d,d['states'][0]['factors'])
        available=base.CW-base.BW-72-10
        for i,s in enumerate(d['states'][1:],1):
            previous=d['states'][i-1];b.scope_text=s['scope'];b.flow_top=None
            cards=s['parallel_cards'] or [s]
            for j,card in enumerate(cards):
                label=str(i).zfill(3)+(chr(97+j) if len(cards)>1 else '')
                extra=('Every parallel card starts from the SAME21-factor input; literal two-order equality is retained. ' if len(cards)>1 else '')
                if s['kind']=='cancel_common_compensation':extra+='The equal positive prefix is canceled from BOTH SIDES of the proved relation. It is not removed from a fixed-product fibration. '
                if s['kind']=='construction_embedding':extra+='The source and target contexts differ; this is labeled as a construction. '
                indices=previous['factors']+card['factors']
                wide=any(2*b.grids[d['rows'][k]['support']]['side']*18>available+.01 for k in indices)
                if wide:
                    b.checkpoint('Step '+label+' - BEFORE: '+s['title'],d,previous['factors'])
                    top=b.new('Step '+label+' - scope',escape(s['title']));b.text(escape(s['scope']+' '+extra),base.M,top,base.W-2*base.M)
                    b.checkpoint('Step '+label+' - AFTER: '+s['title'],d,card['factors'])
                else:
                    b.move('D',Label(label),card['title'] if len(cards)>1 else s['title'],'sphere_rewrite' if s['kind']=='sphere_redraw' else s['kind'],d,previous['factors'],d,card['factors'],extra)
        b.checkpoint('Complete final type ('+slug.replace('-',',')+') factorization',d,d['states'][-1]['factors'])
        top=b.new('Closure certificates and precise scope',bookmark='certificates')
        text='The final product has the exact marked-sphere identity action and the separately checked chosen genus-two lift +I. This is not a claim of equality to the trivial disk braid, an unquotiented spherical-braid equality, a framed section lift, or an unproved identification with a particular literature curve chart.'
        top=b.text(text,base.M,top,base.W-2*base.M)-16
        top=b.text('Final chosen lift matrix: '+escape(str(r['terminal_chosen_lift'])),base.M,top,base.W-2*base.M,'small')-16
        top=b.text('Source-pinned full certificate: '+slug+'.json; graphical viewer: '+slug+'.html. Imported source manifest: ../fibration-sources/planar-mcg-2026-10-30/provenance.json. All sources, exact actual input/output matches, canonical PC daisies/half lanterns and parallel-copy corrections remain available with the repository.',base.M,top,base.W-2*base.M)-16
        for s in r['stages']:
            if s['kind']!='sphere_redraw':continue
            top=b.new('FULL SPHERE redraw discrepancy',escape(s['title']))
            top=b.band('Only the SAME actual curve is redrawn. The whole surrounding factorization is included in the complete disk discrepancy below.',top,True)
            w=s['full_disk_discrepancy'];top=b.text('<b>'+str(len(w))+' signed letters; full actual context retained</b>',base.M,top,base.W-2*base.M)-10
            for start in range(0,len(w),24):
                if top<65:top=b.new('FULL SPHERE discrepancy - continued')
                top=b.text(escape(' '.join(map(str,w[start:start+24]))),base.M,top,base.W-2*base.M,'small')-3
        b.finish();dest=ROOT/'output/pdf'/('derivation-'+slug+'.pdf');shutil.copyfile(base.TMP/'six-seven-body.pdf',dest);shutil.copyfile(dest,FOLDER/(slug+'.pdf'))
        reader=PdfReader(dest)
        if len(reader.pages)!=b.n or any(tuple(map(float,p.mediabox[2:]))!=(612.,792.) for p in reader.pages):raise ValueError('All pages must remain portrait Letter')
        result=dict(example=slug,pages=b.n,bytes=dest.stat().st_size,sha256=sha256(dest.read_bytes()).hexdigest(),point_pitch_pt=b.point_pitch,output=str(dest),page_index=b.index)
        results.append(result);print(json.dumps({k:v for k,v in result.items() if k!='page_index'}),flush=True)
    existing=json.loads((base.TMP/'page-index.json').read_bytes()) if (base.TMP/'page-index.json').exists() else []
    merged={x['example']:x for x in existing};merged.update({x['example']:x for x in results})
    (base.TMP/'page-index.json').write_text(json.dumps([merged[k] for k in ('6-2','4-3','10-10') if k in merged],indent=2),encoding='utf-8')
    return results
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--example',choices=('6-2','4-3','10-10'));args=parser.parse_args()
    build((args.example,) if args.example else ('6-2','4-3','10-10'))
