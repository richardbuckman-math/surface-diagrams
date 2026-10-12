"""Build the portable documentation site: python examples/build_site.py."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import shutil
import sys
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public'
CSS = '''body{margin:0;background:#f3f5f4;color:#20342e;font:17px/1.6 system-ui,sans-serif}main,nav{max-width:1080px;margin:auto;padding:24px}nav{display:flex;gap:24px;flex-wrap:wrap}a{color:#126c60}h1{font:normal 46px/1.15 Georgia,serif}h2{font:normal 30px Georgia,serif;margin-top:42px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}.card,section{background:white;border:1px solid #d8e2dc;border-radius:12px;padding:24px;margin-bottom:20px}.badge{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#64664d}img{max-width:100%;height:auto}pre{overflow:auto;background:#e9efeb;padding:16px}footer{margin-top:48px;color:#586c62}a:focus-visible{outline:3px solid #c07a21} @media(max-width:600px){h1{font-size:34px}main,nav{padding:16px}}'''

def page(path, title, body, prefix=''):
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    nav = ''.join('<a href="{}{}">{}</a>'.format(prefix, url, label) for url,label in [('index.html','Surface diagrams'),('docs/TUTORIAL.html','Tutorial'),('gallery.html','Gallery'),('relations/index.html','Relations'),('fibrations/index.html','Lefschetz fibrations'),('releases.html','Releases')])
    dest.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' | Surface diagrams</title><style>'+CSS+'</style><nav aria-label="Main">'+nav+'</nav><main><h1>'+escape(title)+'</h1>'+body+'<footer>Surface diagrams · SVG and TikZ · Mathematical catalog in development</footer></main></html>',encoding='utf-8')

def build():
    if str(ROOT/'src') not in sys.path:
        sys.path.insert(0, str(ROOT/'src'))
    from surface_diagrams.boundary_playground_geometry import factorization_svg
    from surface_diagrams.fibration_lab_seeds import SEEDS
    from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
    from surface_diagrams.sphere_actions import sphere_inner_certificate

    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'docs', OUT/'docs', dirs_exist_ok=True)
    shutil.copytree(ROOT/'examples'/'output', OUT/'examples'/'output', dirs_exist_ok=True)
    lab_assets = ROOT/'src'/'surface_diagrams'/'lab_assets'
    lab_out = OUT/'lab'
    lab_out.mkdir(exist_ok=True)
    for name in ('lab.css', 'lab.js', 'sphere-cuts.js', 'public-lab.js', 'public-lab-worker.mjs', 'public-lab-backend.py'):
        shutil.copy2(lab_assets/name, lab_out/name)
    lab_html = (lab_assets/'index.html').read_text(encoding='utf-8')
    lab_html = lab_html.replace('<script src="lab.js"></script>',
                                '<script src="public-lab.js"></script><script src="lab.js"></script>')
    (lab_out/'index.html').write_text(lab_html, encoding='utf-8')
    xiao_html = (lab_assets/'xiao-4-3.html').read_text(encoding='utf-8')
    xiao_html = xiao_html.replace('<script src="../lab.js"></script>',
                                  '<script src="../public-lab.js"></script><script src="../lab.js"></script>')
    xiao_out = lab_out/'xiao-4-3'
    xiao_out.mkdir(exist_ok=True)
    (xiao_out/'index.html').write_text(xiao_html, encoding='utf-8')
    with ZipFile(lab_out/'surface_diagrams.zip', 'w', ZIP_DEFLATED) as archive:
        for source in sorted((ROOT/'src'/'surface_diagrams').glob('*.py')):
            archive.write(source, 'surface_diagrams/'+source.name)
    boundary_assets = ROOT/'src'/'surface_diagrams'/'boundary_assets'
    boundary_out = OUT/'boundary-lab'
    boundary_out.mkdir(exist_ok=True)
    for name in ('index.html', 'boundary.css', 'boundary.js', 'public.js',
                 'worker.mjs', 'backend.py', 'pc-lantern.html',
                 'pc-lantern.css', 'pc-cuts.js', 'pc-public.js',
                 'pc-worker.mjs', 'pc-backend.py'):
        shutil.copy2(boundary_assets/name, boundary_out/name)
    for script in (ROOT/'examples').glob('*.py'):
        shutil.copy2(script, OUT/'examples'/script.name)
    entries = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'docs'/'catalog').glob('*.json'))]
    page('relations/pc-daisy-rose.html', 'Puncture-capped daisy and rose', '''
<p>A derivation in the marked disk, with products read in the playground’s top-to-bottom order. A twist enclosing one puncture is trivial. Framed inner boundaries require additional boundary twists.</p>
<section><h2>The four-point daisy</h2>
<p>Write T₁₂₃₄ for the twist enclosing all four marked points. Let U₂₄ and U₁₄ be pair twists whose curves pass under the intervening points, and U₁₂₄ the three-point twist passing under point 3. Two puncture-capped lantern substitutions give</p>
<pre>T₁₂₃₄ T₁₂ = T₁₂₃ T₃₄ U₁₂₄
U₁₂₄ = U₂₄ U₁₄ T₁₂.</pre>
<p>The first lantern treats {1,2}, {3}, and {4} as its three entries. The second splits the under-going curve around {1,2,4}. Substitute the second equation into the first, then cancel T₁₂ on the right:</p>
<pre>T₁₂₃₄ = T₁₂₃ T₃₄ U₂₄ U₁₄.</pre>
<p>The final product has only positive twists. In the project’s braid convention, the under-going factors are</p>
<pre>U₂₄ = σ₃⁻¹ σ₂² σ₃
U₁₄ = σ₃⁻¹ σ₂⁻¹ σ₁² σ₂ σ₃.</pre>
<p>Both lantern steps and the final identity have been checked by the complete Artin action in the disk braid group B₄.</p></section>
<section><h2>General daisy and pairwise rose</h2>
<p>For n marked points, let U(i,n) be the twist on points i and n whose support passes under points i+1 through n−1. Its braid word is</p>
<pre>U(i,n) = (σₙ₋₁⁻¹ … σᵢ₊₁⁻¹) σᵢ² (σᵢ₊₁ … σₙ₋₁).</pre>
<p>Apply the puncture-capped lantern to the entries {1,…,n−2}, {n−1}, {n}, then apply the (n−1)-point daisy inside the under-going twist on {1,…,n−2,n}. A repeated twist on {1,…,n−2} cancels on the right, leaving</p>
<pre>T(1,…,n) = T(1,…,n−1) U(n−1,n) U(n−2,n) … U(1,n).</pre>
<p>Iterate until only pair twists remain. This gives n(n−1)/2 pairwise factors, the puncture-capped rose. For four points, expanding T₁₂₃ by the three-point PC lantern produces</p>
<pre>T₁₂₃₄ = T₁₂ T₁₃(PC) T₂₃ T₃₄ U₂₄ U₁₄.</pre>
<p>The implementation checks these formulas by exact disk braid action for 3–6 points. This finite check supplements the lantern induction; a support drawing alone is not an algebraic certificate.</p></section>
<p><a href="../boundary-lab/index.html">Explore the four-point substitutions in the playground</a> · <a href="https://github.com/richardbuckman-math/surface-diagrams/blob/main/docs/proofs/pc-daisy-rose.md">Read the source with full notation</a></p>
<p>Background: <a href="https://margalit.droppages.net/papers/pure-braids.pdf">Margalit and McCammond, <em>Geometric presentations for the pure braid group</em></a>, Section 4.</p>
''', '../')
    page('relations/pc-half-lantern.html', 'Puncture-capped half lantern', '''
<p>Start with the three-point puncture-capped lantern. Products are read from top to bottom, as in the <a href="../boundary-lab/index.html">interactive playground</a>.</p>
<section><h2>Split and move</h2>
<p>Let H₁₂ be the positive half twist on the arc from point 1 to point 2. Split T₁₂ into two copies of H₁₂, then make the two indicated Hurwitz moves:</p>
<pre>T₁₂₃ = T₁₂ T₁₃ T₂₃
      = H₁₂ H₁₂ T₁₃ T₂₃
      = H₁₂ T₂₃ H₁₂ T₂₃
      = H₁₂ (T₂₃ H₁₂ T₂₃⁻¹) T₂₃ T₂₃.</pre>
<p>The first move uses H₁₂ T₁₃ H₁₂⁻¹ = T₂₃. The next move pulls the middle closed-curve twist past the half twist, conjugating the latter. Combine the final neighbors:</p>
<pre>T₁₂₃ = H₁₂ (T₂₃ H₁₂ T₂₃⁻¹) T₂₃².</pre>
<p>In braid generators, the final product is σ₁ · (σ₂² σ₁ σ₂⁻²) · σ₂⁴, equal to (σ₁σ₂)³ by the complete Artin action in B₃. Conjugating the whole formula transports it to any three-point support in a larger marked disk.</p></section>
<section><h2>Uncapping a point</h2><p>In this factorization the two half-twist arcs end at points 1 and 2. The playground lets you draw point 3 as an inner boundary, and blocks uncapping points 1 and 2. The displayed equality is verified after capping all inner boundaries.</p><p>If point 3 alone becomes a boundary, the ordinary framed lantern supplies the correction:</p>
<pre>T₁₂₃ T₃ = H₁₂ (T₂₃ H₁₂ T₂₃⁻¹) T₂₃².</pre>
<p>T₃ is the positive twist parallel to that inner boundary. This follows mathematically from the framed lantern and the same Hurwitz moves; the playground does not yet check it in a framed mapping-class engine. See <a href="https://web.math.ucsb.edu/~mccammon/papers/pure-braids.pdf">Margalit and McCammond, Theorem 5.1</a>, for punctures versus inner boundaries.</p></section>
<p><a href="../boundary-lab/index.html">Explore the checked half-lantern walkthrough</a> · <a href="https://github.com/richardbuckman-math/surface-diagrams/blob/main/docs/proofs/pc-half-lantern.md">Read the source with full notation</a></p>
''', '../')
    for category, title in [('relations','Mapping class relations'),('fibrations','Lefschetz fibrations')]:
        cards = []
        for e in (e for e in entries if e['category']==category):
            cards.append('<article class="card"><span class="badge">'+escape(e['status'])+'</span><h2><a href="'+e['slug']+'.html">'+escape(e['title'])+'</a></h2><p>'+escape(e['description'])+'</p></article>')
            detail=(' · verified marked-disk factorization' if e.get('pc_proof_url') else
                    ' · verified puncture-capped B3 factorization' if e['slug']=='lantern' else
                    ' · verified braid certificate available' if e.get('proof_url') else
                    ' · no verified factorization supplied yet')
            body = '<p class="badge">'+escape(e['status']+detail)+'</p><p>'+escape(e['description'])+'</p>'
            if e.get('pc_proof_url'):
                body+='<p><a href="'+escape(e['pc_proof_url'])+'">Read the puncture-capped derivation and exact braid words</a></p>'
                body+='<p><a href="../boundary-lab/index.html">Try the checked substitutions in the boundary-twist playground</a></p>'
            if e.get('proof_url'):
                body+='<p><a href="../'+escape(e['proof_url'])+'">Read the complete sphere-braid derivation and certificate</a></p>'
            if e['slug']=='6-7':
                body+='<p><a href="../lab/index.html">Open the interactive (6,7) factorization lab</a></p>'
            if category=='relations' and e['slug']=='lantern':
                body+='<p><a href="../boundary-lab/pc-lantern.html">Open the PC lantern lab with cumulative cut arcs</a></p>'
            if category=='fibrations' and e['slug'] in ('4-3','6-2','10-10'):
                body+='<p><a href="../fibration-lab/'+e['slug']+'.html">Open the source-backed factorization study</a></p>'
            if category=='fibrations' and e['slug']=='4-3':
                body+='<p><a href="../lab/xiao-4-3/index.html">Explore Xiao’s seven factors interactively</a></p>'
            body += ''.join('<section><h2>'+escape(k)+'</h2><p>'+escape(v)+'</p></section>' for k,v in e['sections'].items())
            body += '<p>Future formats will use common curve and factor IDs, an explicit multiplication order, and documented correspondences. A drawing alone does not verify an equivalence.</p>'
            page(category+'/'+e['slug']+'.html',e['title'],body,'../')
        page(category+'/index.html',title,'<p>Browse the planned library. Each entry has space for derivations and equivalent presentations.</p><div class="grid">'+''.join(cards)+'</div>','../')
    for seed in SEEDS:
        sources=''.join('<li><a href="'+escape(url)+'">'+escape(url)+'</a></li>'
                        for url in seed.source_urls)
        body='<p class="badge">'+escape(seed.status)+'</p>'
        body+='<section><h2>Source and conventions</h2><p>'+escape(seed.source_note)+'</p><ul>'+sources+'</ul></section>'
        body+='<section><h2>Sections</h2><p>'+escape(seed.section_note)+'</p></section>'
        if seed.factors:
            word=tuple(letter for factor in seed.factors for letter in factor.word)
            if not sphere_inner_certificate(word)['certified'] or homology_action(word)!=IDENTITY:
                raise ValueError(seed.slug+' seed failed its closed genus-two identity checks')
            svg_path=OUT/'fibration-lab'/(seed.slug+'.svg')
            svg_path.parent.mkdir(parents=True,exist_ok=True)
            svg_path.write_text(factorization_svg(seed.factors,6),encoding='utf-8')
            body+='<section><h2>Seven-factor normalized representative</h2><p>The exact six-strand disk word has '+str(len(word))+' letters. Its action on the six-punctured sphere is inner and its genus-two homology action is +I, certifying the closed genus-two identity. The printed branch braids at two factors require an involution correction before they represent positive separating twists; see the source note.</p><p><a href="'+seed.slug+'.svg">Open the paired surface and braid SVG</a></p><a href="'+seed.slug+'.svg"><img src="'+seed.slug+'.svg" alt="Normalized '+escape(seed.slug)+' factorization and continuous braid"></a>'
            if seed.slug=='4-3':
                body+='<p><a href="../lab/xiao-4-3/index.html">Open the interactive Xiao (4,3) lab</a></p>'
            body+=''.join('<details><summary>'+escape(factor.id)+' · '+escape(factor.label)+'</summary><pre>'+escape(' '.join(map(str,factor.word)))+'</pre></details>' for factor in seed.factors)
            body+='</section>'
        else:
            body+='<section><h2>Factor workspace</h2><p>An ordered, verified disk-braid encoding is still needed before drag-and-drop Hurwitz moves can be enabled. The source relation and section information above are available now.</p></section>'
        page('fibration-lab/'+seed.slug+'.html',seed.title+' study',body,'../')
    figures=[]
    for p in sorted((OUT/'examples/output/tutorial').glob('*.svg')):
        url=p.relative_to(OUT).as_posix()
        label=p.stem.replace('-',' ')
        tikz=p.with_suffix('.tikz')
        figures.append('<article class="card"><h2>'+escape(label)+'</h2><a href="'+url+'"><img loading="lazy" src="'+url+'" alt="'+escape(label)+'"></a><p><a href="'+url+'">SVG</a>'+(' · <a href="'+tikz.relative_to(OUT).as_posix()+'">TikZ</a>' if tikz.exists() else '')+'</p></article>')
    page('gallery.html','Illustrated gallery','<p>Runnable examples from the <a href="docs/TUTORIAL.html">tutorial</a>. These show implemented drawing features; the mathematical catalog is planned separately.</p>'+''.join(figures))
    page('index.html','Draw surfaces. Explore factorizations.','<p>A Python library and growing mathematical atlas for surface diagrams, relations and Lefschetz fibrations.</p><div class="grid"><section><h2><a href="docs/TUTORIAL.html">Start with the tutorial</a></h2><p>Runnable Python recipes and SVG/TikZ output.</p></section><section><h2><a href="gallery.html">Explore the gallery</a></h2><p>Planar curves, braids, genus surfaces and bordered reference families.</p></section><section><h2><a href="lab/index.html">Try the (6,7) factorization lab</a></h2><p>Drag Hurwitz moves, split and combine factors, and inspect the exact action in your browser.</p></section><section><h2><a href="boundary-lab/pc-lantern.html">Explore the PC lantern lab</a></h2><p>Compare three planar twists, their cumulative cut arcs, and one continuous braid.</p></section><section><h2><a href="boundary-lab/index.html">Factor a boundary twist</a></h2><p>Start with three, four, or five marked points, try checked substitutions, and move factors through one another.</p></section><section><h2><a href="docs/proofs/braid-six-seven/braid-six-seven-proof.html">Check the (6,7) sphere proof</a></h2><p>19 sphere substitutions with a machine-checkable move certificate.</p></section><section><h2><a href="relations/index.html">Relations</a></h2><p>Lantern, half lantern, rose and daisy.</p></section><section><h2><a href="fibrations/index.html">Lefschetz fibrations</a></h2><p>MCK, hyperelliptic, BK, numbered examples and Gurtas.</p></section></div>')
    page('releases.html','Versioned releases','<p>Development version: 0.1.0a6. This is alpha software; catalog entries are under development.</p><p><a href="https://github.com/richardbuckman-math/surface-diagrams/releases">Published release downloads</a> · <a href="docs/RELEASING.md">Release procedure</a></p>')
    check_links()
    print('Built site and checked local links:', OUT)

def check_links():
    missing=[]
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key,value in attrs:
                if key in ('href','src') and value:
                    url=urlsplit(value)
                    if not url.scheme and not url.netloc and url.path:
                        target=source.parent/unquote(url.path)
                        if not target.exists(): missing.append((source.relative_to(OUT),value))
    for source in OUT.rglob('*.html'):
        Links().feed(source.read_text(encoding='utf-8'))
    if missing: raise ValueError('Broken local links: '+repr(missing))

if __name__=='__main__':
    build()
