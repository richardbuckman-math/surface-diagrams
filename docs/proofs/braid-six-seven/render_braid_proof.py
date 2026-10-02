"""Verify an elementary proof and produce a readable HTML walkthrough."""
from pathlib import Path
import argparse,json,html,hashlib,sys
from collections import Counter
BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Verify the 2486-move sphere-braid certificate and regenerate its walkthrough')
parser.add_argument('--source-svg',type=Path,help='also verify transcription against the original BraidSixSeven.svg')
args=parser.parse_args()
data=json.loads((BASE/'braid-six-seven-proof.json').read_text())

def inverse(w):return tuple(-x for x in reversed(w))
def reduce(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return out
def artin(word):
    images=[[i] for i in range(1,7)]
    for x in word:
        i=abs(x)-1;a,b=images[i:i+2]
        images[i:i+2]=[reduce(a+b+list(inverse(a))),a] if x>0 else [b,reduce(list(inverse(b))+a+b)]
    return images

R=(1,2,3,4,5,5,4,3,2,1)
relators={r[i:]+r[:i] for r in (R,inverse(R)) for i in range(10)}
w=tuple(data['input']);rows=[];sphere=[];since=[]
for step,(pos,length,new,kind) in enumerate(data['moves'],1):
    new=tuple(new);old=w[pos:pos+length]
    assert len(old)==length
    if kind=='cancel':assert len(old)==2 and old[0]==-old[1] and not new
    elif kind=='commute':assert len(old)==2 and new==old[::-1] and abs(abs(old[0])-abs(old[1]))>1
    elif kind=='braid':assert len(old)==len(new)==3 and old!=new and artin(old)==artin(new)
    elif kind=='sphere':assert old+inverse(new) in relators
    else:raise AssertionError('Unknown rule')
    after=w[:pos]+new+w[pos+length:]
    row=(step,kind,pos,old,new,len(after));rows.append(row)
    if kind=='sphere':sphere.append((step,w,pos,length,new,after,since));since=[]
    else:since.append(row)
    w=after
assert w==tuple(data['output'])==(4,5)*3+(-2,-1)*3

# When supplied, verify the transcription against the original SVG as well.
source_hash='e6fc6f0d4a2788674b98e61944c99f735824607e4ea4af7038d565d404520747'
if args.source_svg is not None:
    import xml.etree.ElementTree as ET
    letters=[]
    for e in ET.parse(args.source_svg).getroot().iter():
        if e.get('class')=='letter' and e.get('x')=='363':
            digits=list(e);letters.append(int(digits[0].text)*(-1 if digits[1].text else 1))
    assert letters==data['input']
    assert hashlib.sha256(args.source_svg.read_bytes()).hexdigest()==source_hash

def word(w):
    if not w:return '<span class="empty">1</span>'
    return ' '.join(f'<span class="letter">{abs(x)}'+('<sup>−1</sup>' if x<0 else '')+'</span>' for x in w)
def table(rows):
    return '<table><thead><tr><th>Move</th><th>Rule</th><th>Position</th><th>Replace</th><th>With</th></tr></thead><tbody>'+''.join(f'<tr><td>{step}</td><td>{kind}</td><td>{pos+1}</td><td>{word(old)}</td><td>{word(new)}</td></tr>' for step,kind,pos,old,new,size in rows)+'</tbody></table>'
parts=['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>BraidSixSeven: a sphere-relation derivation</title><style>
body{font:17px/1.65 system-ui,sans-serif;color:#172a3a;background:#f6f8fb;margin:0}main{max-width:980px;margin:auto;padding:40px 24px}h1{font-size:2.1rem;line-height:1.2}h2{margin-top:2.4em}a{color:#075fad}section{background:white;border:1px solid #dce3eb;border-radius:10px;margin:22px 0;padding:22px}code,.word{font-family:ui-monospace,Consolas,monospace}.word{font-size:17px;line-height:2.2;overflow-wrap:anywhere}.letter{display:inline-block;white-space:nowrap;margin-right:.12em}sup{font-size:.7em}mark{background:#fff0af;padding:4px 0}summary{cursor:pointer;color:#075fad}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:7px;text-align:left;border-bottom:1px solid #e4e9ee}td:nth-child(4),td:nth-child(5){font-family:monospace}.result{font-size:1.4rem;border-left:5px solid #19746b;padding:16px;background:#edf8f4}.note{color:#46576a}.empty{font-style:italic}img{max-width:100%;max-height:640px}footer{margin-top:30px;font-size:14px;color:#46576a}</style><main>
<p class="note">Exact elementary derivation · top-to-bottom reading convention · September 22, 2026</p><h1>Two complementary triple twists</h1>
<p>The 178-letter product in <code>BraidSixSeven.svg</code> reduces, using ordinary braid moves and the sphere relation, to:</p>
<div class="result">(σ<sub>4</sub>σ<sub>5</sub>)<sup>3</sup> (σ<sub>1</sub>σ<sub>2</sub>)<sup>−3</sup>.</div>
<p>The first factor is a positive full twist on punctures 4, 5, 6. The second is a negative full twist on punctures 1, 2, 3. On the sphere these two triples are complementary sides of the same separating curve. Their Dehn twists therefore cancel in the mapping class group.</p>
<p><strong>Keep the groups distinct:</strong> this product represents the nontrivial central full twist in the spherical braid group. It is the identity in the sphere mapping class group, which additionally kills that central full twist.</p>
<img src="braid-six-seven-endpoint.svg" alt="Six-strand braid: six positive crossings on the right triple, followed by six negative crossings on the left triple.">
<h2>How to read and check the derivation</h2>
<p>A digit <code>i</code> means σ<sub>i</sub>; a superscript −1 means its inverse. Read each word from left to right, matching downward travel through the original diagram. Positions count letters starting at 1 in the current word.</p>
<p>We use the sphere relator <code>R = 1 2 3 4 5 5 4 3 2 1 = identity</code>. Every cyclic shift of R or its inverse is also an identity. If such a relator is <code>u v</code>, replace <code>u</code> by <code>v⁻¹</code>. The highlighted segment is the part being replaced.</p>
<p>There are 19 sphere substitutions below. Between them, expand the details to see every cancellation, commuting move, and signed braid move. This is a complete explicit proof, but not a claim of a shortest or elegant hand proof. The downloadable certificate has all 2,486 local moves; the independent verifier checks every replacement and, when given the original SVG, its transcription.</p>
<p><a href="braid-six-seven-proof.json">Machine-readable certificate</a> · <a href="braid-six-seven-proof.md">Complete move table</a> · <a href="render_braid_proof.py">Independent verifier and page generator</a></p>
<details><summary>Original 178-letter word</summary><div class="word">''',word(data['input']),'</div></details>']
for k,(step,before,pos,length,new,after,ordinary) in enumerate(sphere,1):
    parts.append(f'<section><h2>Sphere substitution {k} of {len(sphere)}</h2><p class="note">Move {step}; {len(before)} → {len(after)} letters.</p>')
    parts.append(f'<details><summary>{len(ordinary)} preceding ordinary braid moves</summary>'+table(ordinary)+'</details>')
    parts.append('<p>Replace '+word(before[pos:pos+length])+' by '+word(new)+'.</p>')
    parts.append('<div class="word">'+word(before[:pos])+' <mark>'+word(before[pos:pos+length])+'</mark> '+word(before[pos+length:])+'</div>')
    parts.append('<details><summary>Resulting word</summary><div class="word">'+word(after)+'</div></details></section>')
parts.append('<section><h2>Final ordinary braid moves</h2><details><summary>'+str(len(since))+' remaining moves</summary>'+table(since)+'</details><div class="word">'+word(w)+'</div><p>This is exactly (σ₄σ₅)³(σ₁σ₂)⁻³. No further sphere substitution is hidden in this last step.</p></section>')
parts.append('<h2>Why the mapping classes cancel</h2><p>A full twist on three punctures is the Dehn twist about the boundary of a disk containing those punctures. After capping the outer boundary, a disk containing punctures 1, 2, 3 has a complementary disk containing 4, 5, 6. Their common boundary is the same unoriented curve on the oriented sphere. Thus both positive full twists represent the same positive Dehn twist T. The displayed product is T T⁻¹ = identity.</p>')
parts.append('<footer>Original source SVG SHA-256: <code>'+source_hash+'</code><br>All local steps verified independently. Computation does not use the earlier Garside normal-form routine.</footer></main></html>')
(BASE/'braid-six-seven-proof.html').write_text(''.join(parts),encoding='utf-8')
sys.path.insert(0,str(BASE.parents[2]/'src'))
from surface_diagrams import BraidDiagram,save_svg,save_tikz
diagram=BraidDiagram(6,w,spacing=40,step=27)
save_svg(diagram,BASE/'braid-six-seven-endpoint.svg')
save_tikz(diagram,BASE/'braid-six-seven-endpoint.tikz')
print('Verified',len(rows),'elementary steps; sphere steps:',len(sphere))
if args.source_svg is not None: print('Verified transcription and SHA-256 of',args.source_svg)
print('Rendered',BASE/'braid-six-seven-proof.html')
