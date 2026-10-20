"""Build the short illustrated common-net atlas and an offline SVG gallery."""
from pathlib import Path
import json
from html import escape
from hashlib import sha256
import zipfile
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.graphics import renderPDF,renderSVG
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from figures import net_drawing,shape_drawing,color

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'.preview/common-nets'


class Atlas:
    def __init__(self,path):
        self.w,self.h=landscape(A3);self.c=Canvas(str(path),pagesize=(self.w,self.h));self.page=0
        self.c.setTitle('Common nets: one through six tetrahedra, then six and seven cubes')
        self.style=ParagraphStyle('text',fontName='Helvetica',fontSize=11,leading=15,textColor=HexColor('#263b50'))
    def text(self,text,x,y,width,size=None):
        style=self.style
        if size:style=ParagraphStyle('small',parent=style,fontSize=size,leading=size*1.35)
        p=Paragraph(text,style);_,height=p.wrap(width,1000);p.drawOn(self.c,x,y-height)
        if y-height<30:raise ValueError('Text leaves the page')
        return y-height
    def new(self,title,subtitle):
        if self.page:self.c.showPage()
        self.page+=1;self.c.setFillColor(HexColor('#f7fafc'));self.c.rect(0,0,self.w,self.h,fill=1,stroke=0)
        self.c.setFillColor(HexColor('#12304b'));self.c.setFont('Helvetica-Bold',24);self.c.drawString(35,self.h-43,title)
        self.text(subtitle,35,self.h-61,self.w-70)
        self.c.setFont('Helvetica',9);self.c.drawString(35,18,'Common-net experiment | 20 October 2026 | rigid panels; foldings are checked end states')
        self.c.drawRightString(self.w-35,18,str(self.page))
    def drawing(self,d,x,y):renderPDF.draw(d,self.c,x,y)


def svg(d,name):
    path=DEST/name;renderSVG.drawToFile(d,str(path));return name


def cube_selected(row):
    return row.get('extended_family_best',row['nets'][0])


def build():
    tetra=json.loads((DEST/'tetrahedra.json').read_text());cubes=json.loads((DEST/'cubes.json').read_text())
    optimization=tetra['levels']['6'].get('single_net_optimization',{})
    if not (optimization.get('globally_optimal') and optimization.get('best')==19
            and optimization.get('global_upper_bound')==19
            and len(optimization.get('complete_sources',[]))==4
            and sum(s['tested'] for s in optimization.get('source_results',[]))==104201):
        raise ValueError('Run optimize_six.py to complete the 19-target bound before building this atlas')
    if len(tetra['levels']['6']['two_net_cover'][0]['coverage'])!=19:
        raise ValueError('The atlas expects the optimized net first; rerun optimize_six.py')
    output=ROOT/'output/pdf/common-nets-triangles-and-cubes.pdf';output.parent.mkdir(parents=True,exist_ok=True)
    atlas=Atlas(output);sections=[];all_images=[];models={}
    def model_asset(filename,surf,mapping):
        points=[p for f in surf['faces'] for p in f]
        low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
        center=[(a+b)/2 for a,b in zip(low,high)];size=max(b-a for a,b in zip(low,high))
        ids={m[0]:i for i,m in enumerate(mapping)}
        models[filename]=dict(faces=[[[round((p[i]-center[i])/size,8) for i in range(3)] for p in f] for f in surf['faces']],
                              colors=[[round(x,4) for x in (color(ids[i]).red,color(ids[i]).green,color(ids[i]).blue)] for i in range(len(surf['faces']))])
    def remember(name):all_images.append(name);return name
    def shape_asset(row,net,index,kind):
        name=f'{kind}-{row["units"]}-shape-{index+1:03d}.svg'
        drawing=shape_drawing(row['surfaces'][index],net['mappings'][index],190,135)
        model_asset(name,row['surfaces'][index],net['mappings'][index])
        remember(svg(drawing,name));return drawing,name
    atlas.new('Triangular Cubigami: the first four volumes',
        'One volume unit is a regular tetrahedron. Mirror pairs count once; either side of the paper may face outward. '
        'The first genuinely different shapes appear at four units.')
    y=atlas.h-110
    for k in range(1,5):
        row=tetra['levels'][str(k)];net=row['net'];drawing=net_drawing(net,405,145)
        name=remember(svg(drawing,f'tetra-{k}-net-A.svg'))
        atlas.text(f'<b>{k} unit{"s" if k!=1 else ""}: {row["faces"]} triangles, '
                   f'{row["shapes"]} shape{"s" if row["shapes"]!=1 else ""}, one net</b>',35,y,1090)
        atlas.drawing(drawing,35,y-156)
        cards=[]
        for i in net['coverage']:
            pic,filename=shape_asset(row,net,i,'tetra');atlas.drawing(pic,485+(i%3)*220,y-151)
            atlas.text(f'Shape {i+1}',510+(i%3)*220,y-151,180,9)
            cards.append((filename,f'Shape {i+1}'))
        sections.append(dict(title=f'{k} tetrahedra',summary=f'{row["shapes"]} shapes; all covered by one net.',nets=[(name,'Net A')],cards=cards))
        y-=169
    atlas.text('Cut the solid lines, including any RED internal slits. Score and fold BLUE dashed lines. '
               'Numbers and colors identify panels. These templates omit glue tabs.',35,61,1100,10)

    row=tetra['levels']['5'];net=row['net']
    atlas.new('Five tetrahedra: one net makes all seven shapes',
              'Twelve equilateral triangles. Each of the seven surface bijections is checked, including every hinged edge. '
              'This is where the first branching common net is needed in our search: no ribbon net covers all seven.')
    drawing=net_drawing(net,490,390);name=remember(svg(drawing,'tetra-5-net-A.svg'))
    atlas.drawing(drawing,35,300);atlas.text('ONE NET - ALL SEVEN SHAPES',115,291,420)
    atlas.text(f'Internal slits: {drawing._slits}. A red line is a cut, not a crease. '
               'For a mirrored shape, turn the paper over. Colors are panel identifiers; '
               'they do not imply the printed side is always outside.',45,242,470)
    cards=[]
    for i in range(7):
        pic,filename=shape_asset(row,net,i,'tetra');x=565+(i%3)*200;y=555-(i//3)*178
        atlas.drawing(pic,x,y);atlas.text(f'Shape {i+1}',x+55,y-3,160,10);cards.append((filename,f'Shape {i+1}'))
    sections.append(dict(title='5 tetrahedra',summary='One 12-triangle net folds into all seven shapes. No common ribbon exists; this net branches.',nets=[(name,'Net A')],cards=cards))

    row=tetra['levels']['6'];nets=row['two_net_cover']
    atlas.new('Six tetrahedra: two nets cover all 23 shapes',
              'Fourteen triangles per net. The best single net covers 19 of the 23 types; an exhaustive bound rules out 20 or more in this model. '
              'Net A is that optimal single puzzle. Net B supplies the missing shapes. For A/B pictures, colors show Net A.')
    names=[]
    for j,net in enumerate(nets):
        drawing=net_drawing(net,535,150);name=remember(svg(drawing,f'tetra-6-net-{"AB"[j]}.svg'));names.append((name,'Net '+'AB'[j]))
        atlas.drawing(drawing,35+j*557,atlas.h-276)
        atlas.text(f'<b>Net {"AB"[j]}:</b> {len(net["coverage"])} shapes; {drawing._slits} internal slits.',50+j*557,atlas.h-278,515,10)
    cards=[]
    for i in range(23):
        choice=next(j for j,n in enumerate(nets) if i in n['coverage']);net=nets[choice]
        pic=shape_drawing(row['surfaces'][i],net['mappings'][i],170,98)
        filename=remember(svg(pic,f'tetra-6-shape-{i+1:03d}.svg'))
        model_asset(filename,row['surfaces'][i],net['mappings'][i])
        x=36+(i%6)*187;y=atlas.h-416-(i//6)*118
        atlas.drawing(pic,x,y);labels='/'.join('AB'[j] for j,n in enumerate(nets) if i in n['coverage'])
        atlas.text(f'Shape {i+1} - {labels}',x+27,y-3,155,9);cards.append((filename,f'Shape {i+1} - net {labels}'))
    sizes=[len(n['coverage']) for n in nets];overlap=len(set(nets[0]['coverage'])&set(nets[1]['coverage']))
    sections.append(dict(title='6 tetrahedra',summary=f'Two nets cover all 23. Net A covers {sizes[0]}, net B covers {sizes[1]}; {overlap} shapes support both. '
                         'The single-net maximum is 19 in the stated model. For A/B pictures, colors show Net A.',nets=names,cards=cards))

    for key in ['6','7']:
        row=cubes[key];net=cube_selected(row);k=int(key);covered=net['coverage'];cards=[]
        name=remember(svg(net_drawing(net,1100,180,'square'),f'cube-{k}-net.svg'))
        chunks=[covered[:36]]+[covered[i:i+54] for i in range(36,len(covered),54)]
        for part,indices in enumerate(chunks):
            atlas.new(f'{k} cubes: a verified common net'+(' - continued' if part else ''),
                      f'{len(covered)} covered shapes out of {row["eligible_tree_shapes"]} tree-like {k}-cube shapes '
                      f'with {4*k+2} exterior squares. These covered examples are planar. '
                      + ('All 27 planar six-cube trees are covered. ' if k==6 else 'This is 79 of the 83 planar seven-cube trees. ')
                      + 'A net covering all three-dimensional cases has NOT been found.')
            top=atlas.h-115
            if part==0:
                atlas.drawing(net_drawing(net,1100,150,'square'),35,top-145);top-=180
            height=115 if part else 112
            for j,i in enumerate(indices):
                pic=shape_drawing(row['surfaces'][i],net['mappings'][i],115,85)
                filename=f'cube-{k}-shape-{i+1:03d}.svg'
                model_asset(filename,row['surfaces'][i],net['mappings'][i])
                if filename not in all_images:remember(svg(pic,filename));cards.append((filename,f'Shape {i+1}'))
                x=35+(j%9)*124;y=top-100-(j//9)*height
                atlas.drawing(pic,x,y);atlas.text(f'Shape {i+1}',x+21,y-3,105,9)
        sections.append(dict(title=f'{k} cubes',summary=f'{len(covered)}/{row["eligible_tree_shapes"]} eligible tree-like shapes. '
                             +(f'All {row["planar_tree_shapes"]} planar cases.' if k==6 else f'{len(covered)}/{row["planar_tree_shapes"]} planar cases.')
                             +' This is a partial result for the requested 3D problem.',nets=[(name,f'{4*k+2}-square net')],cards=cards))

    atlas.new('Scope, verification and what remains',
              'Small templates and complete finite checks, with the limits stated explicitly.')
    items=[
        '<b>Triangle model.</b> Face-to-face unions of congruent regular tetrahedra, with disjoint interiors. '
        'Mirrors are identified. Nets use rigid unit equilateral triangles and hinges only along whole edges. '
        'Internal slits and turning the paper over are allowed. Extra folds through triangle interiors, stretching, '
        'layering faces, and overlapping panels are excluded. A tree of n tetrahedra has 2n+2 exterior triangles; '
        'a tree of n cubes has 4n+2 exterior squares.',
        '<b>Positive certificates.</b> Integer coordinates make tetrahedron reflections, congruence tests, '
        'interior separation and mesh incidence exact. Every reported folding is a bijection onto the target boundary faces. '
        'The endpoints of each hinged edge agree exactly in 3D. All planar panels are distinct. '
        'These checks certify the folded end states, not a collision-free folding motion.',
        '<b>Six-unit obstruction.</b> A chosen six-tetrahedron surface has 25,645 dual spanning trees. '
        'A second implementation enumerates them by edge subsets and union-find: 9,316 overlap in the plane, '
        'and each of the other 16,329 fails at least one target after every oriented root face is tried. '
        'This rules out one common net within the stated model; two nets suffice. '
        'The rejection list is saved as six-unit-obstruction.json. This is a reproducible computational result, not a literature claim.',
        '<b>Single-net optimum: 19.</b> The exact maximization completes four source catalogs, totaling 104,201 spanning trees. '
        'Every net of each source covers at most 19 targets. A net that covers none of the four sources can cover at most '
        'the other 19 targets. Therefore no net covers 20 or more; Net A attains 19. The four source shapes are pictured below. '
        'This is an exhaustive computational bound in the stated model.',
        '<b>Cube scope.</b> Six-cube trees have 26 exterior squares; seven-cube trees have 30. '
        'The candidate nets here cover planar families, not all 138 or 822 three-dimensional tree-like shapes. '
        'The general 3D six- and seven-cube searches remain open in this project. '
        'The literature already shows that one net cannot cover all tree-like pentacubes, so equal area is only a necessary condition.',
        '<b>Sources.</b> Aloupis et al., <i>Common Unfoldings of Polyominoes and Polycubes</i>: '
        '<link href="https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf" color="#175a9e">erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf</link>. '
        'Rick Mabry, common nets of the three four-tetrahedron shapes: '
        '<link href="https://lsusmath.rickmabry.org/rmabry/dodec/delta/common.html" color="#175a9e">lsusmath.rickmabry.org/rmabry/dodec/delta/common.html</link>. '
        'George Sicherman, independent cluster counts: '
        '<link href="https://sicherman.net/polytets/index.html" color="#175a9e">sicherman.net/polytets/index.html</link>.',
        '<b>Files.</b> The offline gallery includes each net and each pictured target as a separate SVG, '
        'plus tetrahedra.json, cubes.json and six-unit-obstruction.json. Blue dashed edges are hinges; '
        'red interior edges are slits; solid exterior edges are cuts. Panel colors in folded shapes correspond to the net. '
        'These are mathematical templates without tabs or thickness allowances.',
    ]
    y=atlas.h-112
    for item in items:y=atlas.text(item,35,y,1100)-22
    row=tetra['levels']['6']
    for j,i in enumerate(row['single_net_optimization']['complete_sources']):
        net=next(n for n in row['two_net_cover'] if i in n['coverage'])
        atlas.drawing(shape_drawing(row['surfaces'][i],net['mappings'][i],210,130),95+j*270,82)
        atlas.text(f'Upper-bound source: shape {i+1}',100+j*270,77,240,9)
    atlas.c.save()
    # Embed the exact data with the short visual atlas.
    from pypdf import PdfWriter
    writer=PdfWriter(clone_from=output)
    for filename in ['tetrahedra.json','cubes.json','six-unit-obstruction.json']:
        writer.add_attachment(filename,(DEST/filename).read_bytes())
    temporary=output.with_suffix('.tmp.pdf')
    with temporary.open('wb') as stream:writer.write(stream)
    temporary.replace(output)
    content=[]
    for s in sections:
        nets=''.join(f'<figure><a href="{f}" download><img src="{f}" alt="{escape(label)}"></a><figcaption>{escape(label)} - click to download SVG</figcaption></figure>' for f,label in s['nets'])
        cards=''.join(f'<figure><a href="{f}" target="_blank"><img loading="lazy" src="{f}" alt="{escape(label)}"></a><figcaption>{escape(label)}</figcaption></figure>' for f,label in s['cards'])
        content.append(f'<section><h2>{escape(s["title"])}</h2><p>{escape(s["summary"])}</p><div class="nets">{nets}</div><div class="shapes">{cards}</div></section>')
    html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Common nets - triangles and cubes</title>
<style>body{font:17px/1.5 system-ui;margin:24px auto;max-width:1250px;padding:0 18px;color:#17304b;background:#f7fafc}h1{font-size:35px}section{margin:48px 0;border-top:1px solid #cbd5e1;padding-top:18px}.notice{padding:18px;background:#e5edf8;border-radius:12px}.nets{display:flex;flex-wrap:wrap;gap:24px}.nets figure{flex:1;min-width:280px}.nets img{width:100%;max-height:360px}.shapes{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}figure{margin:0;text-align:center;background:white;padding:12px;border-radius:8px}.shapes img{width:100%;height:140px}figcaption{font-size:14px}a{color:#155e96}</style>
<h1>Common nets: triangles first, then cubes</h1><div class="notice">One volume unit = one regular tetrahedron. Mirrors count once. Blue dashed = hinge; black = boundary cut; red = internal slit. Clicking a net downloads its vector SVG. Foldings are verified end states; no continuous folding motion is claimed.</div>
<p><a href="common-nets-triangles-and-cubes.pdf" download>Download the short illustrated PDF</a> | <a href="tetrahedra.json" download>Triangle certificates</a> | <a href="cubes.json" download>Cube certificates</a> | <a href="six-unit-obstruction.json" download>Six-unit obstruction</a></p>'''+''.join(content)+'''<section><h2>Remaining problem</h2><p>The general three-dimensional six- and seven-cube problems are still open here. The displayed cube nets cover the stated planar subsets. Equal surface area alone does not establish a common unfolding.</p></section>'''
    html+='''<style>.nets img,.shapes img{object-fit:contain}dialog{box-sizing:border-box;width:min(900px,92vw);max-width:calc(100vw - 24px);border:1px solid #cbd5e1;border-radius:12px;padding:20px;color:#17304b;background:#f7fafc}dialog::backdrop{background:#12263b99}#model-canvas{width:100%;height:min(430px,55vh);touch-action:none}dialog button,dialog a{font:inherit;margin:4px;padding:7px 12px}dialog h2{margin:0 0 10px}</style>
<dialog id="viewer" aria-labelledby="viewer-title"><h2 id="viewer-title"></h2><p id="viewer-status">Drag to rotate. Face colors correspond to the net. This is a shape viewer, not a folding animation.</p><canvas id="model-canvas" aria-label="Rotatable target polyhedron"></canvas><div><button id="viewer-left" type="button">Turn left</button><button id="viewer-right" type="button">Turn right</button><button id="viewer-above" type="button">View above</button><button id="viewer-below" type="button">View below</button><a id="viewer-download" download>Download SVG</a><button id="viewer-close" type="button">Close</button></div></dialog>'''
    html+='<script type="application/json" id="models">'+json.dumps(models,separators=(',',':'))+'</script>'
    html+='<script src="viewer.js"></script>'
    (DEST/'viewer.js').write_bytes((Path(__file__).parent/'viewer.js').read_bytes())
    (DEST/'index.html').write_text(html,encoding='utf-8')
    (DEST/output.name).write_bytes(output.read_bytes())
    archive=ROOT/'output/common-nets-gallery.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for filename in sorted(set(all_images+['index.html','viewer.js',output.name,'tetrahedra.json','cubes.json','six-unit-obstruction.json'])):
            z.write(DEST/filename,filename)
    (DEST/'gallery-manifest.json').write_text(json.dumps(dict(pdf_pages=atlas.page,svg_count=len(all_images),pdf_sha256=sha256(output.read_bytes()).hexdigest()),indent=2))
    print(json.dumps(dict(pdf=str(output),pages=atlas.page,gallery=str(DEST/'index.html'),archive=str(archive),svg_count=len(all_images))))


if __name__=='__main__':build()
