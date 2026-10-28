"""Visual comparison of already reached early- and late-petal states; no PDF edit."""
from pathlib import Path
from hashlib import sha256
from html import escape
import json,re,textwrap
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
from surface_diagrams.compact_svg import compact_support_svg
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.mapping_classes import exact_action

OUT=ROOT/'docs/proofs/half-neighborhood-comparison'

def support_grid(svg):
    # Standard-library registration only: importing this research builder must
    # not require the optional PDF exporter dependencies.
    svg=compact_support_svg(re.sub(r'<text\b[^>]*class="marked-point-label"[^>]*>.*?</text>','',svg,flags=re.S))
    root=ET.fromstring(svg);width,height=map(float,root.get('viewBox').split()[2:]);marks=[]
    def visit(n,sx=1,sy=1,tx=0,ty=0):
        transform=n.get('transform','')
        for op,args in re.findall(r'(translate|scale)\(([^)]+)\)',transform):
            v=list(map(float,args.replace(',',' ').split()))
            if op=='translate':tx+=sx*v[0];ty+=sy*(v[1] if len(v)>1 else 0)
            else:sx*=v[0];sy*=v[1] if len(v)>1 else v[0]
        if re.sub(r'(translate|scale)\([^)]+\)','',transform).strip():raise ValueError('Unsupported SVG transform')
        if n.get('class')=='marked-point':marks.append((sx*float(n.get('cx'))+tx,sy*float(n.get('cy'))+ty,abs(sx)*float(n.get('r'))))
        for child in n:visit(child,sx,sy,tx,ty)
    visit(root);marks.sort()
    if len(marks)!=6:raise ValueError('Keep six marked points')
    pitch=marks[1][0]-marks[0][0];cy=marks[0][1];radius=marks[0][2];cx=(marks[0][0]+marks[-1][0])/2
    if pitch<=0 or any(abs(x-marks[0][0]-i*pitch)>1e-5 or abs(y-cy)>1e-5 or abs(r-radius)>1e-5 for i,(x,y,r) in enumerate(marks)):raise ValueError('Nonuniform source grid')
    return dict(svg=svg,width=width,height=height,cx=cx,cy=cy,pitch=pitch,side=max(cx,width-cx)/pitch,vertical=max(cy,height-cy)/pitch)

def comparison_data():
    source=ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json'
    audit=ROOT/'docs/proofs/six-seven-half-neighborhood-geometry.json'
    c=json.loads(source.read_text(encoding='utf-8'));r=json.loads(audit.read_text(encoding='utf-8'))
    early=c['named_full_route']['stages'][31:40];late=r['late_daisy_stages'];matches=[]
    if early[0]['factors']!=late[0]['factors'] or early[-1]['factors']!=late[-1]['factors']:raise ValueError('Keep both full joins')
    for i in range(8):
        a={f['id']:factor_from_data(f) for f in early[i]['factors'] if f['half']}
        b={f['id']:factor_from_data(f) for f in late[i]['factors'] if f['half']}
        if set(a)!=set(b):raise ValueError('Half ancestry changed')
        for name,f in a.items():
            equal=exact_action(f.word,5)==exact_action(b[name].word,5)
            if not equal:raise ValueError('The comparison changed an actual half-twist class')
            matches.append(dict(stage=i,id=name,early_word=f.word,late_word=b[name].word,exact_B5_equal=equal))
    report=dict(source_sha256=sha256(source.read_bytes()).hexdigest(),audit_sha256=sha256(audit.read_bytes()).hexdigest(),
        pictured_stages=(1,4,7),actual_half_matches=matches,literal_complete_joins=True,
        scope='The two actual half-twist classes are IDENTICAL at all eight matched checkpoints. The delayed variant reduces petal-row clutter; it does not simplify these arcs or prove lower arc intersections. No preferred derivation, payload or PDF is changed.')
    return early,late,report

def panel(stage,title):
    rows=[]
    for raw in stage['factors']:
        f=factor_from_data(raw);g=support_grid(number_support_points(support_svg(f,6)));scale=24/g['pitch']
        rows.append((f,g,scale,max(66,2*g['vertical']*24+12)))
    height=115+sum(r[3] for r in rows)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="{height}" viewBox="0 0 560 {height}" data-records="{len(rows)}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="18" y="30" font-family="sans-serif" font-size="19" fill="#18344a">{escape(title)}</text>',
        f'<text x="18" y="55" font-family="sans-serif" font-size="14">{len(rows)} factor records; two actual half twists</text>',
        '<text x="18" y="78" font-family="sans-serif" font-size="12">Gold = half-twist arc. Unnumbered six-point grid; pitch 24px.</text>']
    y=100
    for f,g,scale,h in rows:
        parts.append(f'<g data-factor="{escape(f.id)}"><rect x="8" y="{y}" width="544" height="{h}" fill="'+('#fff3cf' if f.half else '#f4f7fa')+'" stroke="white"/>')
        for j,line in enumerate(textwrap.wrap(f.id,width=23,break_long_words=True,break_on_hyphens=False)):
            parts.append(f'<text x="18" y="{y+22+j*15}" font-family="monospace" font-size="12">{escape(line)}</text>')
        parts.append(f'<text x="18" y="{y+h-9}" font-family="sans-serif" font-size="12">'+('H' if f.half else 'T'+str(f.points))+('^'+str(f.power) if f.power>1 else '')+'</text>')
        inner=g['svg'].split('>',1)[1].rsplit('</svg>',1)[0]
        svg='<svg x="'+str(390-g['cx']*scale)+'" y="'+str(y+h/2-g['cy']*scale)+'" width="'+str(g['width']*scale)+'" height="'+str(g['height']*scale)+'" viewBox="0 0 '+str(g['width'])+' '+str(g['height'])+'">'+inner+'</svg>'
        if g['side']*24>160:raise ValueError('Keep the comparison curve inside its panel')
        parts.append(svg);parts.append('</g>');y+=h
    return ''.join(parts)+'</svg>'

def write_utf8(path,text):
    with path.open('w',encoding='utf-8',newline='\n') as stream:stream.write(text)

def build():
    early,late,report=comparison_data();OUT.mkdir(exist_ok=True)
    labels={1:'After early expansion / delayed root split',4:'After the same short-side square transport',7:'Immediately before the half twists combine'}
    sections=[]
    for i in report['pictured_stages']:
        cards=[]
        for name,stages,title in [('early',early,'Early petals'),('late',late,'Delayed petals')]:
            filename=name+'-'+str(i)+'.svg';write_utf8(OUT/filename,panel(stages[i],title))
            cards.append(f'<figure><figcaption>{title} · checkpoint {i}</figcaption><a href="{filename}">Open full-size SVG</a><img src="{filename}" alt="{title}: actual factor supports at checkpoint {i}"></figure>')
        sections.append('<section><h2>'+labels[i]+'</h2><div class="pair">'+''.join(cards)+'</div></section>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Early versus delayed petal diagrams</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}section{margin:28px 0}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.pair{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Early versus delayed petals: factor-diagram comparison</h1><p class="scope">Research comparison only. The preferred complete derivation is unchanged. The two actual half-twist classes are identical at all eight matched checkpoints; gold highlights their arcs. Delaying the daisy leaves fewer petal rows while these halves are handled. This is a readability comparison, not an arc-simplification or shorter-proof claim.</p><p>Each picture uses the same unnumbered six-point grid, at 24px pitch and 1.68px radius. Individual supports are not a joint-cut drawing. Exact normal-form intersections refer to their closed neighborhoods, not the arcs shown here.</p><p><a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Preferred complete derivation</a> · <a href="comparison.json">Exact actual-half matches and source hashes</a> · <a href="../six-seven-half-neighborhood-geometry.json">Full geometry audit and retained late stages</a></p>'''
    write_utf8(OUT/'index.html',html+''.join(sections)+'</main></html>')
    write_utf8(OUT/'comparison.json',json.dumps(report,separators=(',',':')))
    print('Saved6 source-exact support panels;16 actual-half B5 matches; public derivation unchanged')
    return report

if __name__=='__main__':build()
