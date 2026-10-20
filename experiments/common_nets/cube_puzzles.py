"""Checked classic outlines and bounded larger square-panel puzzle examples.

Every positive target is rechecked by cubes.verify_net. Larger-net sampling
selects examples, not optima. Chiral cube shapes remain separate targets.
"""
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import random
from types import SimpleNamespace

from . import cubes
from .extend_tetrahedra import random_tree

SOURCE='https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf'
SHORT_SOURCE='https://erikdemaine.org/papers/Cubigami_CGGA2010/paper.pdf#page=2'
# Source Fig. 3 photo, read as unit squares. Internal hinge choices below
# are explicitly checked tree adaptations, rather than inferred from colors.
CLASSIC_FOUR=[(1,4)]+[(x,3) for x in range(4)]+[(x,2) for x in range(2,6)]+[(x,1) for x in range(1,5)]+[(x,0) for x in range(2,6)]+[(5,-1)]
# Section 3.3, first 22-panel example, printed on PDF page 9.
CLASSIC_FIVE=[(x,0) for x in range(6)]+[(0,-1),(3,-1),(1,1)]+[(x,1) for x in range(4,12)]+[(5,2),(8,2),(10,2),(8,0),(10,0)]
# Section 3.3, second 22-panel example, printed on PDF page 10.
PLANAR_FIVE=[(3,3)]+[(x,2) for x in range(1,7)]+[(x,1) for x in (0,2,3,4,5)]+[(x,0) for x in range(6)]+[(x,-1) for x in (0,2,4,5)]
# Earlier proceedings version, page 2, explicit 23-target drawing. Its
# colored-square coordinates were read from the PDF vector rectangles.
FIVE_23=[(x,0) for x in range(5)]+[(x,1) for x in range(4,13)]+[(1,-1),(1,1)]+[(x,y) for x in (6,8,11) for y in (0,2)]


class SquareSurface:
    """Precompiled face flags; topology independent of 3D coordinates."""
    def __init__(self,surface):
        self.surface=surface
        self.flags=[(f,r,h) for f in range(len(surface['faces'])) for r in range(4) for h in (1,-1)]
        lookup={s:i for i,s in enumerate(self.flags)}
        self.bits=[1<<s[0] for s in self.flags]
        self.next=[[lookup[cubes.neighbor(s,e,(e+2)%4,surface['adjacency'])] for e in range(4)] for s in self.flags]

    def fold(self,net):
        for root,bit in enumerate(self.bits):
            used=bit;placed=[root]
            for a,b,e,_ in net['hinges']:
                state=self.next[placed[a]][e]
                if used&self.bits[state]:break
                placed.append(state);used|=self.bits[state]
            else:
                mapping=[self.flags[i] for i in placed]
                cubes.verify_net(net,self.surface,mapping)
                return mapping
        return None


def net_key(net):
    """Fixed cut/hinge pattern, modulo planar rotations and reflection."""
    cells=net['cells'];corners=lambda c:[c,(c[0]+1,c[1]),(c[0]+1,c[1]+1),(c[0],c[1]+1)]
    hinge_edges=[(corners(cells[a])[e],corners(cells[a])[(e+1)%4]) for a,_,e,_ in net['hinges']]
    variants=[]
    for reflect in (False,True):
        for r in range(4):
            def xy(p):
                x,y=p
                if reflect:x=-x
                for _ in range(r):x,y=-y,x
                return x,y
            squares=[[xy(p) for p in corners(c)] for c in cells]
            low=[min(p[i] for s in squares for p in s) for i in range(2)]
            shift=lambda p:(p[0]-low[0],p[1]-low[1])
            variants.append((tuple(sorted(tuple(sorted(shift(p) for p in s)) for s in squares)),
                             tuple(sorted(tuple(sorted(shift(xy(p)) for p in edge)) for edge in hinge_edges))))
    return min(variants)


def paper_graph(cells):
    cells=list(map(tuple,cells));where={c:i for i,c in enumerate(cells)}
    return [(i,where[(x+dx,y+dy)]) for i,(x,y) in enumerate(cells) for dx,dy in ((1,0),(0,1)) if (x+dx,y+dy) in where]


def paper_net(cells,edges,selected):
    graph=[[] for _ in cells]
    for i in selected:
        a,b=edges[i];graph[a].append(b);graph[b].append(a)
    order=[0];where={0:0};hinges=[]
    for a,source in enumerate(order):
        for target in graph[source]:
            if target in where:continue
            dx,dy=(cells[target][i]-cells[source][i] for i in range(2))
            e={(0,-1):0,(1,0):1,(0,1):2,(-1,0):3}[dx,dy]
            where[target]=len(order);hinges.append((a,len(order),e,(e+2)%4));order.append(target)
    if len(order)!=len(cells):return None
    return dict(cells=[cells[i] for i in order],hinges=hinges)


def outline_variants(cells):
    """All spanning hinge trees of an outline; extra shared edges are slits."""
    edges=paper_graph(cells);n=len(cells)
    for selected in combinations(range(len(edges)),n-1):
        roots=list(range(n))
        def find(i):
            while roots[i]!=i:i=roots[i]
            return i
        for e in selected:
            a,b=map(find,edges[e])
            if a==b:break
            roots[a]=b
        else:yield paper_net(cells,edges,selected)


def unfold_surface(surface,edges,selected):
    graph=[[] for _ in surface['faces']]
    for i in selected:
        a,b=edges[i];graph[a].append(b);graph[b].append(a)
    order=[0];states=[(0,0,1)];cells=[(0,0)];where={0:0};occupied={(0,0)};hinges=[]
    for a,source in enumerate(order):
        for target in graph[source]:
            if target in where:continue
            e=next(e for e in range(4) if cubes.neighbor(states[a],e,(e+2)%4,surface['adjacency'])[0]==target)
            dx,dy=((0,-1),(1,0),(0,1),(-1,0))[e];cell=(cells[a][0]+dx,cells[a][1]+dy)
            if cell in occupied:return None
            occupied.add(cell);where[target]=len(order);order.append(target);cells.append(cell)
            states.append(cubes.neighbor(states[a],e,(e+2)%4,surface['adjacency']))
            hinges.append((a,len(order)-1,e,(e+2)%4))
    return dict(cells=cells,hinges=hinges)


def certify(net,checks):
    mappings=[check.fold(net) for check in checks]
    net.update(coverage=[i for i,m in enumerate(mappings) if m is not None],mappings=mappings)
    return net


def reference_net(cells,checks,goal,limit=10000,required=0):
    best=None;score=-1;tested=0
    # Check the long bar first; this quickly rejects unsuitable hinge trees.
    for net in outline_variants(cells):
        tested+=1
        if checks[required].fold(net) is not None:
            certify(net,checks)
            if len(net['coverage'])>score:
                best=net;score=len(net['coverage']);print('reference',len(cells),'panels',score,'targets at',tested,flush=True)
            if score>=goal:break
        if tested>=limit:break
    if best is None:raise ValueError('No checked folding found for source outline')
    best['outline_variants_tested']=tested
    return best


def spine_examples(checks,units,keep=2):
    pool=defaultdict(set)
    for i,check in enumerate(checks):
        if not cubes.is_planar(check.surface['cluster']):continue
        for p in cubes.foot_patterns(check.surface,units):pool[p,-1].add(i)
        if units>=5:
            for p in cubes.foot_patterns(check.surface,units,extension=True):pool[p].add(i)
    chosen=[];covered=set();seen=set()
    for _ in range(keep):
        if not pool:break
        pattern=max(pool,key=lambda p:(len(pool[p]-covered),len(pool[p]),-p[0],-p[1]))
        covered.update(pool.pop(pattern));net=cubes.make_net(units,*pattern);key=net_key(net)
        if key not in seen:certify(net,checks);chosen.append(net);seen.add(key)
    return chosen


def spatial_examples(surfaces,checks,units,attempts=120,keep=2):
    rng=random.Random(20261021+units);ids=[i for i,s in enumerate(surfaces) if not cubes.is_planar(s['cluster'])]
    if not ids:return []
    sample=sorted(set(rng.sample(ids,min(80,len(ids)))));pool=[];seen=set()
    for trial in range(attempts):
        source=rng.choice(sample);s=surfaces[source]
        edges,selected=random_tree(SimpleNamespace(faces=s['faces'],adjacency=s['adjacency']),rng)
        net=unfold_surface(s,edges,selected)
        if net is None:continue
        key=net_key(net)
        if key in seen:continue
        seen.add(key);covered={i for i in sample if checks[i].fold(net) is not None}
        pool.append((len(covered),trial,net,covered))
        pool.sort(key=lambda p:(-p[0],p[1]));pool=pool[:8]
    selected=[];covered=set()
    for _ in range(min(keep,len(pool))):
        choice=max(pool,key=lambda p:(len(p[3]-covered),p[0],-p[1]));pool.remove(choice);covered.update(choice[3])
        selected.append(certify(choice[2],checks))
    print('spatial',units,[len(n['coverage']) for n in selected],flush=True)
    return selected


def complete_planar(row,units):
    """Supply the few targets absent from the broad spine-family examples."""
    planar={i for i,c in enumerate(row['shapes']) if cubes.is_planar(c)}
    covered=set().union(*(set(n['coverage']) for n in row['nets']))
    missing=sorted(planar-covered)
    if not missing:return
    surfaces=row['surfaces'];checks=[SquareSurface(s) for s in surfaces]
    from .cube_general_search import search
    result=search([surfaces[i] for i in missing],seconds=15)
    proposed=[]
    if result['found']:
        squares=result['found']['squares'];cells=[(min(p[0] for p in s),min(p[1] for p in s)) for s in squares];hinges=[]
        def corners(c):return [c,(c[0]+1,c[1]),(c[0]+1,c[1]+1),(c[0],c[1]+1)]
        for a,b,e,_ in result['found']['hinges']:
            edge={squares[a][e],squares[a][(e+1)%4]}
            ac=corners(cells[a]);entry=next(j for j in range(4) if {ac[j],ac[(j+1)%4]}==edge)
            hinges.append((a,b,entry,(entry+2)%4))
        proposed.append(dict(cells=cells,hinges=hinges))
    else:
        # A bounded two-target search is not an impossibility result. Each
        # target still supplies its own checked nonoverlapping edge net.
        rng=random.Random(20261021)
        for i in missing:
            s=surfaces[i]
            for _ in range(500):
                edges,selected=random_tree(SimpleNamespace(faces=s['faces'],adjacency=s['adjacency']),rng)
                net=unfold_surface(s,edges,selected)
                if net is not None:proposed.append(net);break
            else:raise ValueError('No planar source unfolding found in bounded sample')
    for net in proposed:
        certify(net,checks);net.update(id='C%d%s'%(units,chr(65+len(row['nets']))),
            label='Planar %d-cube completion'%units,
            note='Additional fixed-cut net for planar shapes missing from the broad spine examples. Only its checked target list is claimed.')
        row['nets'].append(net)
    actual=set().union(*(set(n['coverage']) for n in row['nets']))
    assert planar<=actual
    print('completed planar',units,len(planar),'targets; added',[len(n['coverage']) for n in proposed],flush=True)


def run():
    path=Path('.preview/common-nets/cube-puzzles-through-eight.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        report=json.loads(path.read_text())
        if report.get('version',0)<2:
            row=report['levels']['5'];checks=[SquareSurface(s) for s in row['surfaces']]
            net=reference_net(FIVE_23,checks,23);assert len(net['coverage'])==23
            net.update(label='Published 23-target five-cube net',note='Aloupis et al., earlier proceedings version, page 2. The pictured tree net is checked against all 27 tree-shaped pentacubes.',source=SHORT_SOURCE)
            row['nets'][1]['label']='Published planar five-cube outline'
            row['nets']=[net]+row['nets']
            for i,entry in enumerate(row['nets']):entry['id']='C5'+chr(65+i)
            report['version']=2;path.write_text(json.dumps(report,separators=(',',':')))
        if report.get('version',0)<3:
            complete_planar(report['levels']['8'],8)
            report['version']=3;path.write_text(json.dumps(report,separators=(',',':')))
        return report
    cache=path.with_name('cube-levels-through-eight.json')
    if cache.exists():levels={int(n):[tuple(map(tuple,c)) for c in rows] for n,rows in json.loads(cache.read_text()).items()}
    else:
        levels=cubes.enumerate_cubes(8);cache.write_text(json.dumps(levels,separators=(',',':')))
    assert [len(levels[n]) for n in range(1,9)]==[1,1,2,8,29,166,1023,6922]
    checkpoint=path.with_name('cube-puzzles-work.json')
    report=json.loads(checkpoint.read_text()) if checkpoint.exists() else dict(levels={},source=SOURCE,version=2)
    for n in range(1,9):
        if str(n) in report['levels']:continue
        shapes=[c for c in levels[n] if cubes.is_tree(c)];surfaces=[dict(cubes.surface(c),cluster=c) for c in shapes]
        checks=[SquareSurface(s) for s in surfaces];nets=[]
        def add(net,label,note,source=None):
            net['label']=label;net['note']=note
            if source:net['source']=source
            nets.append(net)
        if n==1:
            from .verify_six import trees
            found={}
            for edges,selected in trees(surfaces[0]['adjacency']):
                net=unfold_surface(surfaces[0],edges,selected)
                if net is not None:found.setdefault(net_key(net),net)
            assert len(found)==11,len(found)
            for i,key in enumerate(sorted(found)):
                add(certify(found[key],checks),'Cube net %d / 11'%(i+1),'One of the eleven standard edge nets of a single cube.')
        elif n==4:
            net=reference_net(CLASSIC_FOUR,checks,len(shapes));assert len(net['coverage'])==7
            add(net,'Classic Cubigami7 outline','Knuth and Miller outline; checked fixed tree hinges, with internal slits.',SOURCE+'#page=3')
            for net in spine_examples(checks,n,1):add(net,'Four-cube alternative','Paired-foot spine example; only its listed targets are claimed.')
        elif n==5:
            net=reference_net(FIVE_23,checks,23);assert len(net['coverage'])==23
            add(net,'Published 23-target five-cube net','Aloupis et al., earlier proceedings version, page 2. Checked against all 27 tree-shaped pentacubes.',SHORT_SOURCE)
            for cells,label,goal in [(CLASSIC_FIVE,'Published five-cube outline',22),(PLANAR_FIVE,'Published planar five-cube outline',11)]:
                net=reference_net(cells,checks,goal)
                add(net,label,'Aloupis et al., Section 3.3; checked fixed tree hinges. Coverage below is computed, not inferred from the source caption.',SOURCE+('#page=10' if cells is PLANAR_FIVE else '#page=9'))
            for net in spine_examples(checks,n,1):add(net,'Planar five-cube alternative','Paired-foot spine example; only its listed targets are claimed.')
        else:
            for i,net in enumerate(spine_examples(checks,n,2)):
                add(net,'Planar %d-cube net %s'%(n,chr(65+i)),'Selected spine-family example, not a universal or optimal net.')
            if n>=6:
                for i,net in enumerate(spatial_examples(surfaces,checks,n)):
                    add(net,'Spatial %d-cube net %s'%(n,chr(65+i)),'Bounded sample of source trees; full listed coverage is checked, with no optimality claim.')
        for i,net in enumerate(nets):net['id']='C%d%s'%(n,chr(65+i))
        report['levels'][str(n)]=dict(shapes=shapes,surfaces=surfaces,nets=nets,total_polycubes=len(levels[n]),
                                     tree_shapes=len(shapes),planar_tree_shapes=sum(cubes.is_planar(c) for c in shapes))
        print('cube puzzles',n,len(shapes),'shapes',[(net['label'],len(net['coverage'])) for net in nets],flush=True)
        checkpoint.write_text(json.dumps(report,separators=(',',':')))
    path.write_text(json.dumps(report,separators=(',',':')))
    return run()


if __name__=='__main__':run()
