"""Print the checked cube game collection, with puzzles before color-key solutions."""
from html import escape
import json
from pathlib import Path
import shutil


def page_plan(nets):
    plan=[dict(kind='cover'),dict(kind='contents')]
    for section in ('puzzles','solutions'):
        plan.append(dict(kind='intro',section=section))
        for small,units in (('single',(1,)),('small',(2,3))):
            plan.append(dict(kind=small,section=section,nets=[n['id'] for n in nets if n['units'] in units]))
        for net in nets:
            if net['units']<4:continue
            plan.append(dict(kind='net',section=section,net=net['id'],targets=list(range(min(9,len(net['targets']))))))
            for start in range(9,len(net['targets']),24):
                plan.append(dict(kind='targets',section=section,net=net['id'],targets=list(range(start,min(start+24,len(net['targets']))))))
    plan.append(dict(kind='notes'))
    return plan


def load_collection():
    folder=Path(__file__).parent/'game'
    index=json.loads((folder/'cubes-index.json').read_text())
    nets=[json.loads((folder/n['file']).read_text()) for n in index['puzzles']]
    return index,nets


def build():
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A3,landscape
    from reportlab.lib.colors import HexColor
    from reportlab.graphics import renderPDF
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from pypdf import PdfWriter
    from .cubes import surface
    from .figures import net_drawing,shape_drawing,color

    root=Path(__file__).resolve().parents[2]
    index,nets=load_collection();by_id={n['id']:n for n in nets}
    plan=page_plan(nets);count=sum(len(n['targets']) for n in nets)
    output=root/'output/pdf/cubes-cubigami-puzzles-and-solutions.pdf'
    output.parent.mkdir(parents=True,exist_ok=True)
    w,h=landscape(A3);canvas=Canvas(str(output),pagesize=(w,h),pageCompression=1)
    canvas.setTitle('Cubes and Cubigami: one through eight - puzzles and solutions')
    canvas.setAuthor('Richard Buckman - computational common-net experiment')
    ink=HexColor('#17344e')
    styles={size:ParagraphStyle('cube-%s'%size,fontName='Helvetica',fontSize=size,leading=size*1.35,textColor=ink) for size in (9,10,11,12,14,18)}
    game='https://richardbuckman-math.github.io/surface-diagrams/tetrahedra/index.html'
    models={}

    def text(value,x,y,width,size=11):
        p=Paragraph(value,styles[size]);_,height=p.wrap(width,1000)
        if y-height<36:raise ValueError('Text leaves page: '+value[:90])
        p.drawOn(canvas,x,y-height)
        return y-height

    def title(value,subtitle,page,bookmark=None,level=0):
        if page>1:canvas.showPage()
        canvas.setFillColor(HexColor('#fbfcfe'));canvas.rect(0,0,w,h,fill=1,stroke=0)
        canvas.setFillColor(ink);canvas.setFont('Helvetica-Bold',24);canvas.drawString(35,h-45,value)
        text(subtitle,35,h-65,w-70,11)
        canvas.setFont('Helvetica',9)
        canvas.drawString(35,18,'One unit = one cube | fixed hinges and cuts | chiral twins separate | checked end states')
        if page!=2:
            canvas.drawRightString(w-115,18,'Contents');canvas.linkRect('','contents',(w-168,12,w-110,30),thickness=0)
        canvas.drawRightString(w-35,18,'%d / %d'%(page,len(plan)))
        if bookmark:
            canvas.bookmarkPage(bookmark);canvas.addOutlineEntry(value,bookmark,level=level,closed=False)

    def palette_for(net,section):
        return [tuple(getattr(color(i),c) for c in ('red','green','blue')) for i in range(len(net['faces']))] if section=='solutions' else net['colors']

    def net_picture(net,x,y,width,height,section='puzzles'):
        data=dict(cells=[f[0][:2] for f in net['faces']],hinges=net['hinges'])
        drawing=net_drawing(data,width,height,kind='square',palette=palette_for(net,section))
        renderPDF.draw(drawing,canvas,x,y)
        return drawing._slits

    def target_picture(net,i,x,y,width,height,section):
        target=net['targets'][i];key=(net['id'],i)
        if key not in models:
            surf=surface([tuple(c) for c in target['cells']])
            faces={frozenset(f):j for j,f in enumerate(surf['faces'])}
            mapping=[(faces[frozenset(map(tuple,f))],0,1) for f in target['faces']]
            if len({m[0] for m in mapping})!=len(surf['faces']):raise ValueError('Nonbijective target picture')
            models[key]=(surf,mapping)
        surf,mapping=models[key]
        palette=palette_for(net,section) if section=='solutions' else target['colors']
        renderPDF.draw(shape_drawing(surf,mapping,width,height,palette=palette),canvas,x,y)
        text(target['id'],x,y-3,width,10)

    def pages_for(section,net):
        return [i for i,p in enumerate(plan,1) if p.get('section')==section and
                (p.get('net')==net['id'] or net['id'] in p.get('nets',[]))]

    def page_range(pages):return str(pages[0]) if pages[0]==pages[-1] else '%d-%d'%(pages[0],pages[-1])

    def destination(section,net):
        return section+'-'+('single' if net['units']==1 else 'small' if net['units']<4 else net['id'])

    for page,item in enumerate(plan,1):
        kind=item['kind'];section=item.get('section','')
        if kind=='cover':
            title('Cubes and Cubigami: puzzles and solutions','One through eight cubes | 35 fixed-cut nets | 796 net-target challenges',page,'cover')
            text('One net. Many possible shapes.',45,h-135,530,18)
            text('<b>Part I - Puzzles.</b> Fold each cool-colored net into its warm-colored targets. The target colors are independently randomized and give no panel-matching key.<br/><br/>'
                 '<b>Part II - Solutions.</b> The identical nets and target lists, now with matching panel colors.<br/><br/>'
                 'This collection includes all 11 single-cube nets, the classic seven-shape four-cube outline, a published 23-shape five-cube net, '
                 'and larger examples through eight cubes. The 241-target eight-cube net is a useful challenge set; it is not claimed universal.',45,h-180,530,14)
            net_picture(by_id['C4A'],640,395,480,300)
            text('C4A - the classic Cubigami7 outline',665,370,460,12)
            text('This adaptation fixes a tree of hinges and internal slits. It does not reproduce the commercial hinge mechanism exactly.',640,335,480,11)
            for k,i in enumerate((0,3,6)):target_picture(by_id['C4A'],i,635+k*170,135,155,145,'puzzles')
            text('Across the collection, every planar tree-shaped cube cluster through eight is represented. Spatial coverage is partial at six, seven and eight. '
                 'A shape can occur under more than one net. All cubes have unit edges; each n-cube target has 4n+2 exterior squares.',45,215,530,12)
            text('<b>Cut solid black and red lines. Fold blue dashed hinges.</b> No tabs or thickness allowances are included. '
                 'The checks certify folded end states, not collision-free assembly.',45,115,w-90,11)
        elif kind=='contents':
            title('Contents','Click a row to jump to its puzzle or solution. Every page has a Contents link.',page,'contents')
            xcols=(40,425,810)
            for col,values in enumerate((nets[:15],nets[15:25],nets[25:])):
                x=xcols[col]
                text('<b>Net / targets</b>',x,h-117,245,12);text('<b>Puzzle</b>',x+250,h-117,60,11);text('<b>Solution</b>',x+316,h-117,65,11)
                y=h-155
                for net in values:
                    text('<b>%s</b> &nbsp; %d cube%s / %d target%s'%(net['id'],net['units'],'' if net['units']==1 else 's',len(net['targets']),'' if len(net['targets'])==1 else 's'),x,y,244,11)
                    for sec,dx in (('puzzles',250),('solutions',316)):
                        text(page_range(pages_for(sec,net)),x+dx,y,62,10)
                        canvas.linkRect('',destination(sec,net),(x+dx,y-19,x+dx+60,y+1),thickness=0)
                    y-=34
            text('<b>How to use the collection</b> &nbsp; page 3',820,270,330,12)
            canvas.linkRect('','puzzles',(820,243,1150,273),thickness=0)
            text('<b>Checks, coverage and sources</b> &nbsp; page %d'%len(plan),820,225,330,12)
            canvas.linkRect('','notes',(820,198,1150,228),thickness=0)
            text('C4A is the classic seven-shape set. C5A is the published 23-shape set. C8A and C8B have 241 and 237 targets. '
                 'The remaining alternatives add different shapes and layouts.',820,170,330,11)
        elif kind=='intro':
            title('Part I - Puzzles' if section=='puzzles' else 'Part II - Solutions',
                  'Independent target colors hide the solution.' if section=='puzzles' else 'Matching colors reveal the panel correspondence.',page,section)
            y=h-130
            for n in range(1,9):
                row=index['catalog'][str(n)];group=[net for net in nets if net['units']==n]
                text('<b>%d cube%s</b> &nbsp; %d nets; %d distinct targets represented / %d tree shapes. All %d planar tree shapes represented.'%
                     (n,'' if n==1 else 's',len(group),row['represented_shapes'],row['tree_shapes'],row['planar_tree_shapes']),45,y,w-90,14);y-=43
            y=text('Choose one net and work only on its listed targets. Keep every blue dashed hinge attached and cut every red internal slit. '
                   'Flat layouts on different pages are alternatives; do not change cuts between targets of the same puzzle. '
                   'Templates are scaled to fit the page, rather than printed at one common unit-edge size.',45,315,w-90,14)-25
            y=text(('Use shape and geometry to solve the puzzle. The cool net palette and warm target palette are unrelated. '
                    'Solutions later in the book use the net palette on each folded shape.' if section=='puzzles' else
                    'A panel keeps its color from the flat net to the folded target. Colors indicate one checked solution, '
                    'but other valid panel assignments may exist.')+' Reflected spatial cube shapes are distinct targets when they are not related by rotation.',45,y,w-90,12)-25
            text('Play these same targets online: drag either view to rotate it; double-click a hinge and use the wheel, slider or key pair to fold. '
                 '<link href="%s#C4A" color="#155e96">Open the folding game</link>.'%game,45,y,w-90,12)
        elif kind in ('single','small'):
            label='All eleven single-cube nets' if kind=='single' else 'Two- and three-cube alternatives'
            title(section.title()+' - '+label,'Each card pairs one fixed net with every target it makes in this collection.',page,section+'-'+kind,1)
            cols,rows=(4,3) if kind=='single' else (2,2)
            cw=(w-70)/cols;ch=(h-155)/rows
            for k,ident in enumerate(item['nets']):
                net=by_id[ident];x=35+(k%cols)*cw;y=h-120-(k//cols+1)*ch
                text('<b>%s</b> &nbsp; %s'%(ident,escape(net['label'])),x+8,y+ch-10,cw-18,10)
                net_picture(net,x+4,y+36,cw*.60,ch-70,section)
                for j in range(len(net['targets'])):
                    tw=cw*.37/len(net['targets'])
                    target_picture(net,j,x+cw*.62+j*tw,y+43,tw-6,ch-90,section)
        elif kind in ('net','targets'):
            net=by_id[item['net']];first=kind=='net';total=len(net['targets'])
            title('%s %s - %s%s'%(section.title(),net['id'],net['label'],'' if first else ' / targets continued'),
                  '%d cubes; %d exterior square panels; %d listed targets. '%(net['units'],len(net['faces']),total)+
                  ('Unrelated target colors; no folding key.' if section=='puzzles' else 'Matching net/target colors show a checked solution.'),
                  page,destination(section,net) if first else None,1)
            if first:
                slits=net_picture(net,35,275,510,420,section)
                text('<b>%s</b> &nbsp; %d fixed hinges; %d internal slit%s.'%(net['id'],len(net['hinges']),slits,'' if slits==1 else 's'),45,250,490,12)
                text(escape(net['note']),45,215,490,11)
                text('<link href="%s#%s" color="#155e96">Play this net online</link>'%(game,net['id']),45,145,490,12)
                if net.get('source'):text('<link href="%s" color="#155e96">Primary source for this outline</link>'%escape(net['source']),45,115,490,11)
                if total>9:text('The remaining %d targets follow on the next page(s).'%(total-9),45,80,490,11)
                for k,i in enumerate(item['targets']):target_picture(net,i,590+(k%3)*187,545-(k//3)*200,177,170,section)
            else:
                for k,i in enumerate(item['targets']):target_picture(net,i,38+(k%6)*193,570-(k//6)*166,180,140,section)
        else:
            title('Checks, coverage, and sources','The same checked game data generates every picture and target list in this book.',page,'notes')
            paragraphs=[
                '<b>What is covered.</b> All 35 included nets and all 796 net-target challenges appear in both Puzzles and Solutions. '
                'A challenge counts a net together with a target; targets shared between nets count more than once. '
                'Across the collection, every planar tree cluster through eight is represented. Spatial coverage at six/seven/eight is 36/138, 86/822 and 265/5154 tree shapes.',
                '<b>Same exterior area.</b> All displayed clusters have a tree as their cube face-adjacency graph. Their boundary has 6n-2(n-1)=4n+2 square faces. '
                'For example, the 2-by-2 block of four cubes has fewer exterior panels and belongs to a different net size. It is not part of the seven-target 18-panel family.',
                '<b>Geometry checks.</b> Integer cube coordinates determine each exterior square exactly. A bijection between all net panels and all exterior faces is checked, '
                'with shared hinge endpoints equal. The browser independently rebuilds each solution from signed hinge angles. Reflected cube shapes remain separate under proper rotations. '
                'Independent polyomino enumeration checks complete planar coverage through eight.',
                '<b>Larger examples.</b> C8A and C8B cover 241 and 237 targets. Two extra nets supply the planar shapes that these miss. '
                'Selected spatial nets add further challenges. No largest possible set, universal eight-cube net or exhaustive common-net search is claimed.',
                '<b>Physical model.</b> Rigid unit-square panels and ideal hinges are assumed. Internal slits are fixed. The computations establish final folded shapes, '
                'not a collision-free continuous motion. The game allows panels to pass through each other. Paper thickness, tabs and joint fabrication need separate design.',
                '<b>Classic examples.</b> C4A transcribes the Knuth/Miller Cubigami7 outline in Aloupis et al., Figure 3, using a checked tree-hinge adaptation. '
                'C5A transcribes the earlier short paper\'s explicit 23-target net (page 2); C5B and C5C use the full paper\'s 22-target and 11-planar-target drawings. '
                'Our target counts are recomputed with the rotation/chirality convention above; no novelty is claimed for these published examples.',
                '<b>Primary sources.</b> Aloupis et al., <link href="https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf" color="#155e96">Common Unfoldings of Polyominoes and Polycubes (full paper)</link>; '
                '<link href="https://erikdemaine.org/papers/Cubigami_CGGA2010/paper.pdf" color="#155e96">earlier short paper</link>. '
                'The PDF embeds the exact exported game collection and a page manifest. Source photographs are not reproduced.'
            ]
            y=h-127
            for paragraph in paragraphs:y=text(paragraph,45,y,w-90,12)-22
    canvas.save()
    writer=PdfWriter(clone_from=str(output))
    writer.add_attachment('cube-game-collection.json',json.dumps(dict(index=index,nets=nets),separators=(',',':')).encode())
    writer.add_attachment('page-manifest.json',json.dumps(plan,indent=2).encode())
    with output.open('wb') as stream:writer.write(stream)
    published=root/'docs/puzzles'/output.name;published.parent.mkdir(exist_ok=True);shutil.copyfile(output,published)
    print('Saved',output,len(plan),'pages;',len(nets),'nets;',count,'challenges in each section')
    return output


if __name__=='__main__':build()
