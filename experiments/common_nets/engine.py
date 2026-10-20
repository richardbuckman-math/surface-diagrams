"""Exact regular-tetrahedron clusters and certified common edge nets.

Independent experiment: no dependency on the mapping-class package. Integer
coordinates share a power-of-three denominator, so tetrahedron reflection,
congruence keys, separating axes and surface incidence are exact.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations, permutations
from math import sqrt
import json
from pathlib import Path
import time

DENOMINATOR = 3**10
ORIGIN_TET = tuple(sorted(tuple(DENOMINATOR*x for x in p) for p in
                         [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]))
PERMS4 = tuple(permutations(range(4)))


def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def squared(a,b): return dot(sub(a,b),sub(a,b))


@lru_cache(maxsize=None)
def face_records(tet):
    result=[]
    for omitted in range(4):
        face=tuple(tet[i] for i in range(4) if i!=omitted)
        normal=cross(sub(face[1],face[0]),sub(face[2],face[0]))
        if dot(normal,sub(tet[omitted],face[0]))>0:
            face=(face[0],face[2],face[1])
        result.append((tuple(sorted(face)),face,tet[omitted]))
    return tuple(result)


def surface(cluster):
    found={}
    for tet in cluster:
        for key, oriented, opposite in face_records(tet):
            if key in found: del found[key]
            else: found[key]=oriented
    faces=tuple(found[k] for k in sorted(found))
    edges=defaultdict(list)
    for i,f in enumerate(faces):
        for e in range(3): edges[tuple(sorted((f[e],f[(e+1)%3])))].append((i,e))
    if any(len(v)!=2 for v in edges.values()):
        raise ValueError('Nonmanifold boundary edge')
    adjacency=[[None]*3 for _ in faces]
    for pair in edges.values():
        (a,i),(b,j)=pair
        if faces[a][i]!=faces[b][(j+1)%3]: raise ValueError('Surface orientation mismatch')
        adjacency[a][i]=(b,j);adjacency[b][j]=(a,i)
    vertices=set(v for f in faces for v in f)
    if len(vertices)-len(edges)+len(faces)!=2: raise ValueError('Boundary is not a sphere')
    return dict(faces=faces,adjacency=adjacency)


@lru_cache(maxsize=200000)
def canonical(cluster):
    """Congruence under rigid motions AND reflection, using exact distances."""
    vertices=sorted(set(v for tet in cluster for v in tet))
    index={v:i for i,v in enumerate(vertices)}
    distance=[[squared(a,b) for b in vertices] for a in vertices]
    cells=[tuple(index[v] for v in tet) for tet in cluster]
    best=None
    for tet in cells:
        for perm in PERMS4:
            frame=tuple(tet[i] for i in perm)
            labels=[tuple(distance[v][j] for j in frame) for v in range(len(vertices))]
            key=tuple(sorted(tuple(sorted(labels[i] for i in cell)) for cell in cells))
            if best is None or key<best:best=key
    return best


@lru_cache(maxsize=200000)
def disjoint_interiors(a,b):
    """Separating-axis theorem with integer arithmetic; touching is allowed."""
    for axis in range(3):
        aa=[v[axis] for v in a];bb=[v[axis] for v in b]
        if max(aa)<=min(bb) or max(bb)<=min(aa):return True
    def separates(axis):
        if axis==(0,0,0):return False
        aa=[dot(v,axis) for v in a];bb=[dot(v,axis) for v in b]
        return max(aa)<=min(bb) or max(bb)<=min(aa)
    for tet in (a,b):
        for _,f,_ in face_records(tet):
            if separates(cross(sub(f[1],f[0]),sub(f[2],f[0]))):return True
    ae=[sub(v,u) for u,v in combinations(a,2)]
    be=[sub(v,u) for u,v in combinations(b,2)]
    return any(separates(cross(u,v)) for u in ae for v in be)


def enumerate_polytets(maximum=6):
    levels={1:[(ORIGIN_TET,)]}
    for n in range(2,maximum+1):
        unique={}
        for cluster in levels[n-1]:
            boundary=defaultdict(list)
            for tet in cluster:
                for key,f,opposite in face_records(tet):boundary[key].append((f,opposite))
            for occurrences in boundary.values():
                if len(occurrences)!=1:continue
                face,opposite=occurrences[0]
                sums=[2*sum(v[i] for v in face) for i in range(3)]
                if any(x%3 for x in sums):raise ValueError('Increase coordinate denominator')
                v=tuple(sums[i]//3-opposite[i] for i in range(3))
                candidate=tuple(sorted((*face,v)))
                if any(not disjoint_interiors(t,candidate) for t in cluster):continue
                grown=tuple(sorted((*cluster,candidate)))
                key=canonical(grown)
                if key in unique:continue
                try:surface(grown)
                except ValueError:continue
                unique[key]=grown
        levels[n]=list(unique.values())
        print(f'polytets n={n}: {len(unique)}',flush=True)
    return levels


def neighbor(state,edge,adjacency):
    face,rotation,hand=state
    actual=(rotation+edge)%3 if hand==1 else (rotation-edge-1)%3
    target,entry=adjacency[face][actual]
    return (target,entry if hand==1 else (entry+1)%3,hand)


def attach(triangle,edge):
    a,b=triangle[edge],triangle[(edge+1)%3]
    c=triangle[(edge+2)%3]
    third=(a[0]+b[0]-c[0],a[1]+b[1]-c[1])
    return (b,a,third)


def ribbon_cells(bits,faces):
    triangles=[((0,0),(1,0),(0,1))]
    triangles.append(attach(triangles[-1],0))
    used={tuple(sorted(t)) for t in triangles}
    for i in range(faces-2):
        bit=(bits>>(faces-3-i))&1
        t=attach(triangles[-1],1+bit)
        k=tuple(sorted(t))
        if k in used:return None
        triangles.append(t);used.add(k)
    return triangles


def ribbon_words(surf):
    adj=surf['adjacency'];n=len(adj);full=(1<<n)-1;answers={}
    def walk(states,used,word):
        if used==full:
            answers.setdefault(word,states);return
        for bit in range(2):
            nxt=neighbor(states[-1],1+bit,adj)
            if used>>nxt[0]&1:continue
            walk(states+[nxt],used|(1<<nxt[0]),(word<<1)|bit)
    # Store states in local coordinates whose first edge is the entering edge.
    for face in range(n):
        for rot in range(3):
            for hand in (1,-1):
                state=(face,rot,hand)
                nxt=neighbor(state,0,adj)
                walk([state,nxt],(1<<face)|(1<<nxt[0]),0)
    return answers


def ribbon_search(surfaces):
    n=len(surfaces[0]['faces']);valid={}
    for word in range(1<<(n-2)):
        cells=ribbon_cells(word,n)
        if cells:valid[word]=cells
    coverage=defaultdict(list);witnesses=[]
    for i,s in enumerate(surfaces):
        words=ribbon_words(s);witnesses.append(words)
        for word in words.keys() & valid.keys():coverage[word].append(i)
    def score(word):
        cells=valid[word];vertices=[v for t in cells for v in t]
        xs=[v[0]+v[1]/2 for v in vertices];ys=[v[1] for v in vertices]
        area=(max(xs)-min(xs)+1)*(max(ys)-min(ys)+1)
        return (-len(coverage[word]),area,word)
    best=min(coverage,key=score)
    return dict(word=best,coverage=coverage[best],triangles=valid[best],
                hinges=[(i,i+1,0 if i==0 else 1+((best>>(n-2-i))&1)) for i in range(n-1)],
                mappings=[witnesses[i].get(best) for i in range(len(surfaces))],
                common_ribbons=sum(len(c)==len(surfaces) for c in coverage.values()),
                valid_ribbon_words=len(valid))


def spanning_tree_count(adj):
    """Kirchhoff minor, with exact fraction-free Gaussian elimination."""
    n=len(adj)-1
    a=[[0]*n for _ in range(n)]
    for i in range(n):
        a[i][i]=len(adj[i])
        for j,_ in adj[i]:
            if j<n:a[i][j]-=1
    previous=1
    for k in range(n-1):
        pivot=a[k][k]
        if not pivot:raise ValueError('Unexpected zero Kirchhoff pivot')
        for i in range(k+1,n):
            for j in range(k+1,n):a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//previous
        previous=pivot
        for i in range(k+1,n):a[i][k]=0
    return a[-1][-1]


def common_tree_search(surfaces,seconds=180,minimum=None):
    """Search a fixed hinge tree, with planar slits and either paper side allowed.

    Target possibilities are propagated simultaneously. The source tree is
    enumerated by deterministic include/exclude frontier decisions, not by
    permuting face-placement order. Timeout is explicitly not an impossibility.
    A lower minimum permits failed targets, but the chosen source is always
    required. That threshold search alone is not a global coverage optimum.
    """
    started=time.monotonic();n=len(surfaces[0]['faces'])
    minimum=len(surfaces) if minimum is None else minimum
    allowed_losses=len(surfaces)-minimum
    if not 1<=minimum<=len(surfaces):raise ValueError('Invalid target coverage threshold')
    source=min(range(len(surfaces)),key=lambda i:spanning_tree_count(surfaces[i]['adjacency']))
    adj=surfaces[source]['adjacency'];others=[i for i in range(len(surfaces)) if i!=source]
    triangles=[((0,0),(1,0),(0,1))];states=[(0,0,1)];hinges=[]
    occupied={tuple(sorted(triangles[0]))};stats=dict(nodes=0,complete_source_trees=0,source=source,
                                                   source_spanning_trees=spanning_tree_count(adj))
    initial=[[(1<<f,((f,r,h),)) for f in range(n) for r in range(3) for h in (1,-1)] for _ in others]
    answer=None
    def dfs(used,excluded,possibilities):
        nonlocal answer
        stats['nodes']+=1
        if stats['nodes']%1024==0 and time.monotonic()-started>seconds:raise TimeoutError
        if len(states)==n:
            stats['complete_source_trees']+=1
            mappings=[None]*len(surfaces);mappings[source]=list(states)
            for i,opts in zip(others,possibilities):
                if opts:mappings[i]=list(opts[0][1])
            answer=dict(triangles=list(triangles),hinges=list(hinges),mappings=mappings,
                        coverage=[i for i,m in enumerate(mappings) if m is not None])
            return True
        frontier=[]
        for parent,state in enumerate(states):
            for edge in range(3):
                nxt=neighbor(state,edge,adj)
                edge_id=tuple(sorted((state[0],nxt[0])))
                if not (used>>nxt[0]&1) and edge_id not in excluded:
                    frontier.append((edge_id,parent,edge,nxt))
        if not frontier:return False
        edge_id,parent,edge,nxt=min(frontier)
        t=attach(triangles[parent],edge);key=tuple(sorted(t))
        if key not in occupied:
            grown=[];lost=0
            for i,opts in zip(others,possibilities):
                if not opts:
                    grown.append(None);lost+=1
                    if lost>allowed_losses:break
                    continue
                kept=[]
                for mask,placement in opts:
                    target=neighbor(placement[parent],edge,surfaces[i]['adjacency'])
                    if not (mask>>target[0]&1):kept.append((mask|(1<<target[0]),placement+(target,)))
                if not kept:
                    lost+=1
                    if lost>allowed_losses:break
                grown.append(kept or None)
            if len(grown)==len(others) and lost<=allowed_losses:
                triangles.append(t);states.append(nxt);occupied.add(key);hinges.append((parent,len(states)-1,edge))
                if dfs(used|(1<<nxt[0]),excluded,grown):return True
                hinges.pop();occupied.remove(key);states.pop();triangles.pop()
        return dfs(used,excluded|{edge_id},possibilities)
    completed=True
    try:dfs(1,frozenset(),initial)
    except TimeoutError:completed=False
    return dict(found=answer,exhausted=completed and answer is None,completed=completed,
                seconds=round(time.monotonic()-started,3),**stats)


def verify_net(net,surf,mapping):
    """Independent full face-bijection and edge/vertex agreement check."""
    triangles=[tuple(map(tuple,t)) for t in net['triangles']];faces=surf['faces']
    assert len(triangles)==len(faces)==len(mapping)
    assert len(set(tuple(sorted(t)) for t in triangles))==len(triangles)
    assert sorted(s[0] for s in mapping)==list(range(len(faces)))
    assert len(net['hinges'])==len(faces)-1
    def image(i,vertex):
        local=triangles[i].index(vertex);f,r,h=mapping[i]
        return faces[f][(r+h*local)%3]
    for a,b,edge in net['hinges']:
        shared=set(triangles[a]) & set(triangles[b])
        assert len(shared)==2
        assert shared=={triangles[a][edge],triangles[a][(edge+1)%3]}
        for vertex in shared:assert image(a,vertex)==image(b,vertex)
    # Area / volume follow from face bijection onto a nonoverlapping cluster.
    return True


def fold_net(net,surf,check=True):
    """Try every oriented root flag; the rest is forced by the hinge tree."""
    size=len(surf['faces'])
    assert len(net['triangles'])==size
    assert len(net['hinges'])==size-1
    for face in range(size):
        for rotation in range(3):
            for hand in (1,-1):
                mapping=[None]*size;mapping[0]=(face,rotation,hand);used=1<<face
                for parent,child,edge in net['hinges']:
                    state=neighbor(mapping[parent],edge,surf['adjacency'])
                    if used>>state[0]&1:break
                    mapping[child]=state;used|=1<<state[0]
                else:
                    if check:verify_net(net,surf,mapping)
                    return mapping
    return None


def run(maximum,destination,seconds=180):
    levels=enumerate_polytets(maximum);result={}
    for n,clusters in levels.items():
        surfaces=[surface(c) for c in clusters]
        ribbon=ribbon_search(surfaces)
        search=None;net=ribbon
        if len(ribbon['coverage'])<len(clusters):
            search=common_tree_search(surfaces,seconds)
            if search['found']:net=search['found']
        for i in net['coverage']:verify_net(net,surfaces[i],net['mappings'][i])
        result[n]=dict(units=n,faces=len(surfaces[0]['faces']),shapes=len(clusters),clusters=clusters,
                       surfaces=surfaces,net=net,ribbon_statistics={k:v for k,v in ribbon.items()
                         if k in ['common_ribbons','valid_ribbon_words','coverage']},tree_search=search)
        if len(net['coverage'])<len(clusters):
            remaining=[i for i in range(len(clusters)) if i not in net['coverage']]
            completion=common_tree_search([surfaces[i] for i in remaining],seconds)
            if completion['found']:
                other=completion['found']
                # Search indices belong to the remaining subcatalog; recheck
                # against the full catalog rather than relabel partial maps.
                other['mappings']=[fold_net(other,s) for s in surfaces]
                other['coverage']=[i for i,m in enumerate(other['mappings']) if m is not None]
                result[n]['two_net_cover']=[net,other]
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(json.dumps(dict(model='face-glued regular tetrahedra; mirror pairs identified',
                         coordinate_denominator=DENOMINATOR,levels=result),separators=(',',':')))
        print(f'n={n} faces={len(surfaces[0]["faces"])} coverage={len(net["coverage"])}/{len(clusters)} '
              f'ribbons={ribbon["common_ribbons"]} tree_search={None if search is None else {k:v for k,v in search.items() if k!="found"}}',flush=True)
    return result


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--maximum',type=int,default=6)
    p.add_argument('--seconds',type=float,default=180)
    p.add_argument('--output',type=Path,default=Path('.preview/common-nets/tetrahedra.json'))
    a=p.parse_args();run(a.maximum,a.output,a.seconds)
