"""Independent spanning-tree enumeration for the six-tetrahedron obstruction.

Uses combinations and union-find, not the frontier include/exclude search.
Each tree's planar unfolding is explicitly constructed. A rejection is a
duplicate triangular cell or an independently rechecked un-foldable target.
"""
import json
from itertools import combinations
from pathlib import Path
import time
if __package__:
    from .engine import attach, fold_net, spanning_tree_count
else:
    from engine import attach, fold_net, spanning_tree_count


def trees(adjacency):
    n=len(adjacency)
    edges=[(a,b) for a,neighbors in enumerate(adjacency) for b,_ in neighbors if a<b]
    for selected in combinations(range(len(edges)),n-1):
        roots=list(range(n))
        def find(i):
            while roots[i]!=i:i=roots[i]
            return i
        for e in selected:
            a,b=map(find,edges[e])
            if a==b:break
            roots[a]=b
        else:yield edges,selected


def unfold(adjacency,edges,selected):
    graph=[[] for _ in adjacency]
    for e in selected:
        a,b=edges[e];graph[a].append(b);graph[b].append(a)
    triangles=[((0,0),(1,0),(0,1))];faces=[0];rotations=[0]
    index={0:0};occupied={tuple(sorted(triangles[0]))};hinges=[]
    for i,face in enumerate(faces):
        for b in graph[face]:
            if b in index:continue
            edge=next(j for j,(a,_) in enumerate(adjacency[face]) if a==b)
            local=(edge-rotations[i])%3
            t=attach(triangles[i],local);key=tuple(sorted(t))
            if key in occupied:return None
            occupied.add(key);index[b]=len(faces)
            hinges.append((i,len(faces),local));faces.append(b);triangles.append(t)
            rotations.append(adjacency[face][edge][1])
    return dict(triangles=triangles,hinges=hinges)


def verify(path=Path('.preview/common-nets/tetrahedra.json')):
    started=time.monotonic();report=json.loads(path.read_text());level=report['levels']['6']
    surfaces=level['surfaces'];source=level['tree_search']['source'];adj=surfaces[source]['adjacency']
    rejections=[];overlapping=0;counts={};positive=None
    order=[i for i in range(len(surfaces)) if i!=source]
    # Check initially difficult targets first; this changes performance only.
    missing=[i for i in order if i not in level['net']['coverage']]
    order=missing+[i for i in order if i not in missing]
    for edges,selected in trees(adj):
        mask=sum(1<<e for e in selected);net=unfold(adj,edges,selected)
        if net is None:
            overlapping+=1;rejections.append((mask,'overlap'));continue
        for target in order:
            if fold_net(net,surfaces[target]) is None:
                rejections.append((mask,target));counts[target]=counts.get(target,0)+1;break
        else:
            positive=net;print('UNEXPECTED COMMON NET FOUND',flush=True);break
        if len(rejections)%4000==0:print('independent trees checked',len(rejections),flush=True)
    total=spanning_tree_count(adj)
    complete=positive is None and len(rejections)==total and len(set(m for m,_ in rejections))==total
    summary=dict(source=source,source_spanning_trees=total,checked=len(rejections),
                 planar_overlap_rejections=overlapping,target_rejections=counts,
                 independently_complete=complete,seconds=round(time.monotonic()-started,3))
    certificate=dict(summary=summary,source_edges=edges,rejections=rejections,
                     scope='Rigid unit equilateral-triangle panels, edge hinges; slits and two-sided folding allowed. End states, not continuous folding motions.')
    (path.parent/'six-unit-obstruction.json').write_text(json.dumps(certificate,separators=(',',':')))
    level['independent_obstruction_check']=summary
    # Extend both proposed nets' verified coverage to all targets they support.
    for net in level['two_net_cover']:
        net['mappings']=[fold_net(net,s) for s in surfaces]
        net['coverage']=[i for i,m in enumerate(net['mappings']) if m is not None]
    path.write_text(json.dumps(report,separators=(',',':')))
    print(summary,flush=True)
    return certificate


if __name__=='__main__':verify()
