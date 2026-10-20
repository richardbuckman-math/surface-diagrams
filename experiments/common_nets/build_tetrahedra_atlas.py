"""Complete one-to-eight shape catalog and separate, certified puzzle plates."""
from hashlib import sha256
from html import escape
import json
from math import ceil
from pathlib import Path
import shutil
import zipfile

from .extend_tetrahedra import EXPECTED_COUNTS


def choose_puzzles(report):
    puzzles=[]
    for n in range(1,9):
        row=report['levels'][str(n)]
        if n<=5:
            nets=[row['net']]
        elif n==6:
            nets=row['two_net_cover']
        else:
            pool=row['puzzle_search']['candidates']
            first=pool[0]
            second=max(pool[1:],key=lambda net:(len(set(net['coverage'])-set(first['coverage'])),len(net['coverage'])))
            nets=[first,second]
        for i,net in enumerate(nets):
            puzzles.append(dict(units=n,letter=chr(65+i),id='P%d%s'%(n,chr(65+i)),net=net))
    return puzzles


def page_plan(report,puzzles):
    plan=[dict(kind='cover'),dict(kind='small_catalog')]
    for n in range(5,9):
        total=report['levels'][str(n)]['shapes']
        for start in range(0,total,24):
            plan.append(dict(kind='catalog',units=n,indices=list(range(start,min(start+24,total)))))
    plan += [dict(kind='puzzle_intro'),dict(kind='small_puzzles')]
    for puzzle in puzzles:
        if puzzle['units']<=4:continue
        indices=puzzle['net']['coverage']
        plan.append(dict(kind='puzzle',puzzle=puzzle,indices=indices[:9]))
        for start in range(9,len(indices),24):
            plan.append(dict(kind='puzzle_targets',puzzle=puzzle,indices=indices[start:start+24]))
    plan.append(dict(kind='notes'))
    return plan


def build():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A3,landscape
    from reportlab.lib.colors import HexColor
    from reportlab.graphics import renderPDF,renderSVG
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from pypdf import PdfWriter
    from .figures import net_drawing,shape_drawing,color
    root=Path(__file__).resolve().parents[2]
    source=root/'.preview/common-nets/tetrahedra-through-eight.json'
    report=json.loads(source.read_text())
    assert [report['levels'][str(n)]['shapes'] for n in range(1,9)]==EXPECTED_COUNTS
    puzzles=choose_puzzles(report)
    plan=page_plan(report,puzzles)
    output=root/'output/pdf/tetrahedra-one-through-eight.pdf'
    output.parent.mkdir(parents=True,exist_ok=True)
    gallery=root/'.preview/tetrahedra-one-through-eight'
    gallery.mkdir(exist_ok=True)
    w,h=landscape(A3)
    canvas=Canvas(str(output),pagesize=(w,h),pageCompression=1)
    canvas.setTitle('Tetrahedra, one through eight: complete catalog and puzzle nets')
    canvas.setAuthor('Richard Buckman - computational common-net experiment')
    ink=HexColor('#17344e')
    styles={size:ParagraphStyle('s%d'%size,fontName='Helvetica',fontSize=size,leading=size*1.38,textColor=ink) for size in (9,10,11,12,14,18)}
    models={};assets={};gallery_catalog={};gallery_puzzles={};manifest=[]

    def text(value,x,y,width,size=11):
        p=Paragraph(value,styles[size]);_,height=p.wrap(width,1000)
        if y-height<34:raise ValueError('Text leaves page: '+value[:80])
        p.drawOn(canvas,x,y-height)
        return y-height

    def title(value,subtitle,page,bookmark=None,level=0):
        if page>1:canvas.showPage()
        canvas.setFillColor(HexColor('#fbfcfe'));canvas.rect(0,0,w,h,fill=1,stroke=0)
        canvas.setFillColor(ink);canvas.setFont('Helvetica-Bold',25);canvas.drawString(35,h-45,value)
        text(subtitle,35,h-64,w-70,11)
        canvas.setFont('Helvetica',9)
        canvas.drawString(35,18,'One unit = one regular tetrahedron | mirrors identified | exact folded end states')
        canvas.drawRightString(w-35,18,'%d / %d'%(page,len(plan)))
        if bookmark:
            canvas.bookmarkPage(bookmark)
            canvas.addOutlineEntry(value,bookmark,level=level,closed=False)

    def save_asset(name,drawing,surface=None,mapping=None,model_title=''):
        if name in assets:return
        renderSVG.drawToFile(drawing,str(gallery/name));assets[name]=True
        if surface is not None:
            points=[p for f in surface['faces'] for p in f]
            low=[min(p[i] for p in points) for i in range(3)]
            high=[max(p[i] for p in points) for i in range(3)]
            center=[(a+b)/2 for a,b in zip(low,high)];scale=max(b-a for a,b in zip(low,high))
            palette={m[0]:i for i,m in enumerate(mapping)} if mapping else {i:i for i in range(len(surface['faces']))}
            models[name]=dict(title=model_title,faces=[[[round((p[i]-center[i])/scale,9) for i in range(3)] for p in f] for f in surface['faces']],
                              colors=[[round(v,5) for v in (color(palette[i]).red,color(palette[i]).green,color(palette[i]).blue)] for i in range(len(surface['faces']))])

    def picture(n,i,x,y,width,height,puzzle=None):
        row=report['levels'][str(n)];surface=row['surfaces'][i]
        mapping=puzzle['net']['mappings'][i] if puzzle else None
        name=('%s-shape-%03d.svg'%(puzzle['id'],i+1) if puzzle else 'tetra-%d-shape-%03d.svg'%(n,i+1))
        drawing=shape_drawing(surface,mapping,width,height)
        renderPDF.draw(drawing,canvas,x,y)
        label='%d-%03d'%(n,i+1)
        text(label,x,y-2,width,10)
        save_asset(name,drawing,surface,mapping,'%d tetrahedra - shape %03d%s'%(n,i+1,' / '+puzzle['id'] if puzzle else ''))
        if not puzzle:gallery_catalog.setdefault(n,[]).append((name,label))
        else:gallery_puzzles.setdefault(puzzle['id'],[]).append((name,label))

    def grid(n,indices,puzzle=None,columns=6,rows=4):
        cw=(w-70)/columns;ch=650/rows
        for k,i in enumerate(indices):
            x=35+(k%columns)*cw;y=h-122-(k//columns+1)*ch+22
            picture(n,i,x,y,cw-12,ch-27,puzzle)

    def net_picture(puzzle,x,y,width,height):
        drawing=net_drawing(puzzle['net'],width,height)
        renderPDF.draw(drawing,canvas,x,y)
        save_asset(puzzle['id']+'-net.svg',drawing)
        return drawing._slits

    catalog_ranges={n:[] for n in range(1,9)};puzzle_ranges={p['id']:[] for p in puzzles}
    for page,item in enumerate(plan,1):
        kind=item['kind'];meta=dict(page=page,kind=kind)
        if kind=='cover':
            title('Tetrahedra: one through eight','A complete shape catalog, followed by selected common nets for making puzzles.',page,'cover')
            text('523 shapes. Two ways to explore them.',40,h-130,580,18)
            text('Part I pictures every face-glued cluster through eight units, counting mirror pairs once. '
                 'Part II gives selected puzzle nets, followed by <b>only the shapes that each particular net makes</b>. '
                 'Every matching shape is listed, with the same catalog ID in both sections.',40,h-175,540,14)
            y=h-320
            for n,count in enumerate(EXPECTED_COUNTS,1):
                text('<b>%d unit%s</b> &nbsp; %d shape%s &nbsp; %d exterior triangles'%(n,'' if n==1 else 's',count,'' if count==1 else 's',2*n+2),50,y,520,12);y-=31
            sample=next(p for p in puzzles if p['units']==8)
            net_picture(sample,640,340,490,300)
            text('A selected 18-triangle net for eight units',675,323,450,12)
            text('<b>Cut solid black lines and any red internal lines. Fold blue dashed hinges.</b> '
                 'Panel colors match the target faces in Part II. Downloadable SVGs and rotatable models accompany this PDF.',640,265,480,12)
            text('Seven- and eight-unit nets are useful sampled examples; no optimality is claimed. '
                 'The five-unit cobra net is already known from Rick Mabry. These computations certify folded shapes, '
                 'not collision-free folding motions. Templates omit tabs and thickness allowances.',40,125,w-80,11)
        elif kind=='small_catalog':
            title('Part I - Complete catalog: one through four units','All six shapes at these volumes. IDs give the number of units followed by the shape number.',page,'catalog')
            values=[(1,0),(2,0),(3,0)]+[(4,i) for i in range(3)]
            for k,(n,i) in enumerate(values):
                picture(n,i,40+(k%3)*370,390-(k//3)*310,345,280)
                catalog_ranges[n].append(page)
        elif kind=='catalog':
            n=item['units'];indices=item['indices'];row=report['levels'][str(n)]
            first=indices[0]==0
            title('Complete catalog - %d tetrahedra'%n,
                  '%d shapes in all; %d triangular panels on each surface. Shapes %03d-%03d.'%(row['shapes'],row['faces'],indices[0]+1,indices[-1]+1),
                  page,'catalog-%d'%n if first else None,1)
            grid(n,indices,columns=4,rows=2) if n==5 else grid(n,indices)
            catalog_ranges[n].append(page);meta.update(units=n,indices=indices)
        elif kind=='puzzle_intro':
            title('Part II - Puzzle nets and their matching shapes','Each puzzle is separate: keep its own fixed cuts and hinges for every target shown after it.',page,'puzzles')
            y=h-135
            for n in range(1,9):
                selected=[p for p in puzzles if p['units']==n]
                description='; '.join('%s: %d targets'%(p['id'],len(p['net']['coverage'])) for p in selected)
                text('<b>%d tetrahedra</b> &nbsp; %s'%(n,description),45,y,w-90,14);y-=43
            text('The first four puzzles are together on the next page. Each larger puzzle begins with a large net '
                 'and up to nine target shapes; continuation pages contain all its remaining targets. '
                 'No unmatched shapes are mixed into a puzzle.',45,285,w-90,14)
            text('Catalog colors distinguish faces. Puzzle colors instead identify panels of that puzzle\'s net, '
                 'so the same catalog shape may have different colors in two puzzles. Mirror pairs count as one shape; '
                 'the printed side need not always face outward.',45,183,w-90,12)
        elif kind=='small_puzzles':
            title('Puzzle nets P1A-P4A','One net for each volume; each makes every shape at its volume. Solid edges are cuts; blue dashed edges are hinges.',page)
            for k,puzzle in enumerate(p for p in puzzles if p['units']<=4):
                y=h-115-(k+1)*160+22;n=puzzle['units']
                net_picture(puzzle,40,y,400,140)
                text('<b>%s</b> - %d units'%(puzzle['id'],n),45,y-2,360,11)
                for j,i in enumerate(puzzle['net']['coverage']):picture(n,i,500+j*205,y,190,135,puzzle)
                puzzle_ranges[puzzle['id']].append(page)
        elif kind in ('puzzle','puzzle_targets'):
            puzzle=item['puzzle'];n=puzzle['units'];net=puzzle['net'];row=report['levels'][str(n)]
            label='Puzzle %s - %d tetrahedra'%(puzzle['id'],n)
            subtitle='%d matching shapes out of %d catalog shapes. Every shape on these puzzle pages is certified for this fixed net.'%(len(net['coverage']),row['shapes'])
            title(label+(' / targets continued' if kind=='puzzle_targets' else ''),subtitle,page,
                  puzzle['id'] if kind=='puzzle' else None,1)
            if kind=='puzzle':
                slits=net_picture(puzzle,40,245,510,450)
                text('<b>%s</b> &nbsp; %d panels; %d internal slit%s.'%(puzzle['id'],row['faces'],slits,'' if slits==1 else 's'),50,225,480,12)
                status=('Known five-unit cobra net (Rick Mabry).' if n==5 else
                        'Six-unit Net A attains the checked 19-target maximum.' if n==6 and puzzle['letter']=='A' else
                        'This companion supplies the four targets missing from P6A.' if n==6 else
                        'Selected from %d sampled source trees; not proved optimal.'%row['puzzle_search']['attempts'])
                text(status,50,186,480,11)
                for k,i in enumerate(item['indices']):
                    picture(n,i,595+(k%3)*185,540-(k//3)*165,174,139,puzzle)
                if len(net['coverage'])>9:text('All remaining targets follow on the next page(s).',50,119,480,11)
            else:grid(n,item['indices'],puzzle)
            puzzle_ranges[puzzle['id']].append(page)
            meta.update(puzzle=puzzle['id'],units=n,indices=item['indices'])
        else:
            title('Checks, scope, and sources','A complete catalog is different from an exhaustive search for the best possible puzzle net.',page,'notes')
            paragraphs=[
                '<b>Catalog.</b> All 523 clusters through eight units are enumerated by attaching a regular tetrahedron to an exposed whole face. Integer arithmetic checks disjoint interiors and exact congruence, with mirrors identified. The counts 1,1,1,3,7,23,89,398 agree with the published polytet catalog. Each surface has 2n+2 exterior triangular panels at these volumes.',
                '<b>Puzzle checks.</b> Each selected net is tested against every shape at its volume. A bijection to all exterior faces and equality of both endpoints of every hinge are checked exactly. A second, vertex-based folding implementation agrees. Only certified matching shapes appear in each puzzle\'s list.',
                '<b>Search scope.</b> The six-unit 19-target maximum has a finite computational upper-bound certificate in this fixed-cut model. Seven- and eight-unit examples come from a deterministic bounded sample of source trees. Their complete coverage lists are exact, but those lists are not claims of optimality. Other interesting nets may cover different or larger collections.',
                '<b>Physical scope.</b> Fixed internal slits and either side of the paper are allowed. There are no extra creases through triangle interiors, hidden layers, stretching, or panel overlaps. The checks establish folded end states, not continuous collision-free assembly. Manufacturing clearances, tabs, magnets and material thickness are outside this mathematical template.',
                '<b>Prior work.</b> Rick Mabry\'s four-unit common nets and five-unit cobra net predate this experiment. The complete four-unit catalog agrees with our 37 outlines / 47 fixed-cut variants; the pictured 16 are a selected subset. No publication priority is claimed for the larger results.',
                '<b>Sources.</b> <link href="https://sicherman.net/polytets/index.html" color="#155e96">George Sicherman: Catalogue of Polytets</link>. '
                '<link href="https://lsusmath.rickmabry.org/rmabry/dodec/delta/common.html" color="#155e96">Rick Mabry: four-unit common nets</link>. '
                '<link href="https://lsusmath.rickmabry.org/rmabry/dodec/delta/common8V.html" color="#155e96">Rick Mabry: twelve-face common nets</link>.',
                '<b>Files.</b> The PDF embeds the exact catalog, selected puzzle certificates, and a page manifest. The companion offline gallery lets you rotate every shape and download individual SVG nets. Open index.html after unzipping. No network connection is required.'
            ]
            y=h-130
            for paragraph in paragraphs:y=text(paragraph,45,y,w-90,12)-24
        manifest.append(meta)
    canvas.save()
    # Make the exact catalog and coverage lists travel with the illustrations.
    metadata=dict(pages=len(plan),catalog_shapes=sum(EXPECTED_COUNTS),counts=EXPECTED_COUNTS,
                  catalog_pages={str(n):sorted(set(pages)) for n,pages in catalog_ranges.items()},
                  puzzles=[dict(id=p['id'],units=p['units'],coverage=len(p['net']['coverage']),
                                target_ids=[i+1 for i in p['net']['coverage']],pages=puzzle_ranges[p['id']]) for p in puzzles],
                  page_manifest=manifest,input_sha256=sha256(source.read_bytes()).hexdigest())
    writer=PdfWriter(clone_from=output)
    writer.add_attachment('tetrahedra-through-eight.json',source.read_bytes())
    writer.add_attachment('atlas-manifest.json',json.dumps(metadata,indent=2).encode())
    temporary=output.with_suffix('.tmp.pdf')
    with temporary.open('wb') as f:writer.write(f)
    temporary.replace(output)
    (gallery/'atlas-manifest.json').write_text(json.dumps(metadata,indent=2))
    shutil.copyfile(source,gallery/source.name)
    shutil.copyfile(output,gallery/output.name)

    def cards(values):
        return '<div class="grid">'+''.join('<figure><a href="%s"><img loading="lazy" src="%s" alt="Shape %s"></a><figcaption>%s</figcaption></figure>'%(name,name,label,label) for name,label in values)+'</div>'
    html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tetrahedra one through eight</title>
<style>body{font:17px/1.55 system-ui;max-width:1200px;margin:24px auto;padding:18px;color:#17344e;background:#fbfcfe}h1{line-height:1.2}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}figure{margin:0;background:white;padding:10px;text-align:center}.grid img{width:100%;height:150px;object-fit:contain}.net{width:100%;max-height:400px;object-fit:contain}section{margin:45px 0}a{color:#155e96}summary{font-size:22px;cursor:pointer}dialog{box-sizing:border-box;width:min(900px,92vw);max-width:calc(100vw - 24px);border:1px solid #cbd5e1;border-radius:12px;padding:20px;color:#17344e;background:#fbfcfe}dialog::backdrop{background:#12263b99}#model-canvas{width:100%;height:min(430px,55vh);touch-action:none}button{font:inherit;margin:4px;padding:7px 12px}</style>
<h1>Tetrahedra: one through eight units</h1><p>Complete catalog: 523 shapes, with mirror pairs counted once. Puzzle sections list only certified matches for their own fixed net. Click a shape to rotate it; click a net to download its SVG.</p>
<p><a href="tetrahedra-one-through-eight.pdf" download>Download PDF</a> | <a href="atlas-manifest.json">Page and puzzle index</a></p>
<h2>Part I - Complete catalog</h2>'''
    for n,values in gallery_catalog.items():
        html+='<section><details><summary>%d tetrahedra - all %d shapes</summary>%s</details></section>'%(n,len(values),cards(values))
    html+='<h2>Part II - Puzzle nets and their matching shapes</h2><p>Blue dashed lines are hinges. Black boundaries and red internal edges are cuts. Seven- and eight-unit examples are not claimed optimal. The five-unit construction is Mabry\'s known cobra net. Folded end states are checked; continuous folding paths are not certified.</p>'
    for p in puzzles:
        html+='<section><h2>%s - %d tetrahedra, %d matching shapes</h2><a href="%s-net.svg" download><img class="net" src="%s-net.svg" alt="Net %s"></a>%s</section>'%(p['id'],p['units'],len(p['net']['coverage']),p['id'],p['id'],p['id'],cards(gallery_puzzles[p['id']]))
    html+='''<dialog id="viewer" aria-labelledby="viewer-title"><h2 id="viewer-title"></h2><p id="viewer-status">Drag to rotate. This is a shape viewer, not a folding animation.</p><canvas id="model-canvas" aria-label="Rotatable target polyhedron"></canvas><div><button id="viewer-left">Turn left</button><button id="viewer-right">Turn right</button><button id="viewer-above">View above</button><button id="viewer-below">View below</button><a id="viewer-download" download>Download SVG</a><button id="viewer-close">Close</button></div></dialog>'''
    html+='<script type="application/json" id="models">'+json.dumps(models,separators=(',',':'))+'</script><script src="viewer.js"></script>'
    (gallery/'index.html').write_text(html,encoding='utf-8')
    shutil.copyfile(Path(__file__).parent/'viewer.js',gallery/'viewer.js')
    archive=root/'output/tetrahedra-one-through-eight-gallery.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for name in list(assets)+['index.html','viewer.js',output.name,source.name,'atlas-manifest.json']:
            z.write(gallery/name,name)
    metadata.update(svg_count=len(assets),pdf_sha256=sha256(output.read_bytes()).hexdigest())
    (gallery/'build-manifest.json').write_text(json.dumps(metadata,indent=2))
    print(json.dumps(dict(pdf=str(output),pages=len(plan),shapes=sum(EXPECTED_COUNTS),puzzles=[(p['id'],len(p['net']['coverage'])) for p in puzzles],svg_count=len(assets),archive=str(archive))),flush=True)
    return metadata


if __name__=='__main__':build()
