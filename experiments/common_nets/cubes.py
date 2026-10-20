"""Polycube enumeration and a finite search of symmetric-foot spine nets.

For a k-cube tree, the spine has 2k+2 squares and k pairs of feet, for 4k+2
panels in all. Every folding of this family is determined by a root face flag.
Perfect matchings of the remaining faces enumerate all valid foot positions.
This is a restricted-family optimum, never a claim about all possible nets.
"""
from collections import defaultdict
from itertools import permutations,product
from pathlib import Path
import json
if __package__:
    from .engine import cross,sub,dot
else:
    from engine import cross,sub,dot


def parity(perm):return -1 if sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2 else 1
ROTATIONS=tuple((p,s) for p in permutations(range(3)) for s in product((-1,1),repeat=3)
                if parity(p)*s[0]*s[1]*s[2]==1)
DIRS=tuple(tuple(sign if i==axis else 0 for i in range(3)) for axis in range(3) for sign in (-1,1))


def canonical(cells):
    best=None
    for p,s in ROTATIONS:
        points=[tuple(s[i]*v[p[i]] for i in range(3)) for v in cells]
        low=tuple(min(v[i] for v in points) for i in range(3))
        key=tuple(sorted(tuple(v[i]-low[i] for i in range(3)) for v in points))
        if best is None or key<best:best=key
    return best


def enumerate_cubes(maximum=7):
    levels={1:[((0,0,0),)]}
    for n in range(2,maximum+1):
        out=set()
        for cells in levels[n-1]:
            occupied=set(cells)
            for v in cells:
                for d in DIRS:
                    w=tuple(v[i]+d[i] for i in range(3))
                    if w not in occupied:out.add(canonical((*cells,w)))
        levels[n]=sorted(out)
        print(f'polycubes n={n}: {len(out)}',flush=True)
    return levels


def is_tree(cells):
    occupied=set(cells)
    edges=sum(tuple(v[i]+d[i] for i in range(3)) in occupied for v in cells for d in DIRS)//2
    return edges==len(cells)-1


def is_planar(cells):return any(len({v[i] for v in cells})==1 for i in range(3))


def surface(cells):
    occupied=set(cells);faces=[];owners=[]
    for owner,v in enumerate(cells):
        for axis in range(3):
            a,b=(axis+1)%3,(axis+2)%3
            for sign in (-1,1):
                w=tuple(v[i]+(sign if i==axis else 0) for i in range(3))
                if w in occupied:continue
                corners=[]
                for da,db in [(0,0),(1,0),(1,1),(0,1)]:
                    point=list(v);point[axis]+=sign==1;point[a]+=da;point[b]+=db
                    corners.append(tuple(point))
                normal=tuple(sign if i==axis else 0 for i in range(3))
                if dot(cross(sub(corners[1],corners[0]),sub(corners[2],corners[0])),normal)<0:
                    corners=list(reversed(corners))
                faces.append(corners);owners.append(owner)
    incidence=defaultdict(list)
    for f,corners in enumerate(faces):
        for e in range(4):incidence[tuple(sorted((corners[e],corners[(e+1)%4])))].append((f,e))
    adjacency=[[None]*4 for _ in faces]
    for entries in incidence.values():
        if len(entries)==2:pairs=[entries]
        elif len(entries)==4:
            groups=defaultdict(list)
            for f,e in entries:groups[owners[f]].append((f,e))
            if sorted(map(len,groups.values()))!=[2,2]:raise ValueError('Ambiguous voxel surface edge')
            pairs=list(groups.values())
        else:raise ValueError('Unexpected cube boundary incidence')
        for (a,i),(b,j) in pairs:
            assert faces[a][i]==faces[b][(j+1)%4]
            adjacency[a][i]=(b,j);adjacency[b][j]=(a,i)
    return dict(faces=faces,adjacency=adjacency,owners=owners)


def neighbor(state,parent_edge,child_edge,adj):
    f,r,h=state
    edge=(r+parent_edge)%4 if h==1 else (r-parent_edge-1)%4
    target,entry=adj[f][edge]
    rotation=(entry-child_edge)%4 if h==1 else (entry+1+child_edge)%4
    return (target,rotation,h)


def foot_patterns(surf,k,extension=False):
    adj=surf['adjacency'];n=len(adj);length=2*k+2;full=(1<<n)-1;patterns={}
    for f in range(n):
        for r in range(4):
            for h in (1,-1):
                states=[(f,r,h)];used=1<<f
                for _ in range(length-1):
                    state=neighbor(states[-1],1,3,adj)
                    if used>>state[0]&1:break
                    states.append(state);used|=1<<state[0]
                else:
                    pairs=[];by_face=defaultdict(list)
                    for col,state in enumerate(states):
                        up=neighbor(state,2,0,adj);down=neighbor(state,0,2,adj)
                        mask=(1<<up[0])|(1<<down[0])
                        if up[0]==down[0] or mask&used:continue
                        index=len(pairs);pairs.append((col,mask,up,down,False))
                        by_face[up[0]].append(index);by_face[down[0]].append(index)
                        if extension:
                            up2=neighbor(up,2,0,adj);down2=neighbor(down,0,2,adj)
                            large=mask|(1<<up2[0])|(1<<down2[0])
                            if bin(large).count('1')==4 and not large&used:
                                index=len(pairs);pairs.append((col,large,up2,down2,True))
                                for v in [up[0],down[0],up2[0],down2[0]]:by_face[v].append(index)
                    def cover(mask,columns,selected,extended=-1):
                        if mask==full:
                            if extension and extended<0:return
                            key=(columns,extended) if extension else columns
                            patterns.setdefault(key,dict(spine=list(states),pairs=list(selected)))
                            return
                        bit=(full^mask)&-(full^mask);v=bit.bit_length()-1
                        for index in by_face[v]:
                            p=pairs[index]
                            if p[4] and extended>=0:continue
                            if not p[1]&mask:
                                cover(mask|p[1],columns|(1<<p[0]),selected+[p],p[0] if p[4] else extended)
                    cover(used,0,[])
    return patterns


def make_net(k,pattern,extended=-1):
    length=2*k+2;cells=[(i,0) for i in range(length)]
    hinges=[(i,i+1,1,3) for i in range(length-1)]
    for col in range(length):
        if not (pattern>>col&1):continue
        for y,edge,entry in [(1,2,0),(-1,0,2)]:
            hinges.append((col,len(cells),edge,entry));cells.append((col,y))
            if col==extended:
                hinges.append((len(cells)-1,len(cells),edge,entry));cells.append((col,2*y))
    assert len(cells)==4*k+2
    return dict(cells=cells,hinges=hinges,pattern=pattern,
                triangles=None)


def fold_net(net,surf):
    size=len(surf['faces'])
    for f in range(size):
        for r in range(4):
            for h in (1,-1):
                mapping=[None]*size;mapping[0]=(f,r,h);mask=1<<f
                for parent,child,edge,entry in net['hinges']:
                    state=neighbor(mapping[parent],edge,entry,surf['adjacency'])
                    if mask>>state[0]&1:break
                    mapping[child]=state;mask|=1<<state[0]
                else:return mapping
    return None


def verify_net(net,surf,mapping):
    assert len(net['cells'])==len(surf['faces'])==len(mapping)
    assert len(set(map(tuple,net['cells'])))==len(mapping)
    assert sorted(s[0] for s in mapping)==list(range(len(mapping)))
    def corners(cell):
        x,y=cell;return [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
    def point(i,v):
        j=corners(net['cells'][i]).index(v);f,r,h=mapping[i]
        return tuple(surf['faces'][f][(r+h*j)%4])
    for a,b,edge,entry in net['hinges']:
        ac=corners(net['cells'][a]);bc=corners(net['cells'][b]);shared=set(ac)&set(bc)
        assert len(shared)==2
        assert shared=={ac[edge],ac[(edge+1)%4]}
        assert shared=={bc[entry],bc[(entry+1)%4]}
        for v in shared:assert point(a,v)==point(b,v)
    return True


def run(destination=Path('.preview/common-nets/cubes.json')):
    levels=enumerate_cubes(7);output={}
    for k in (6,7):
        shapes=[cells for cells in levels[k] if is_tree(cells)]
        surfaces=[surface(cells) for cells in shapes]
        coverage=defaultdict(list);foldings=[]
        for i,surf in enumerate(surfaces):
            patterns=foot_patterns(surf,k);foldings.append(patterns)
            for pattern in patterns:coverage[pattern].append(i)
        best=max(coverage,key=lambda p:(len(coverage[p]),-p))
        planar={i for i,cells in enumerate(shapes) if is_planar(cells)}
        planar_best=max(coverage,key=lambda p:(len(planar&set(coverage[p])),len(coverage[p]),-p))
        chosen=list(dict.fromkeys([best,planar_best]));nets=[]
        for pattern in chosen:
            net=make_net(k,pattern);net['coverage']=coverage[pattern]
            net['mappings']=[None]*len(shapes)
            for i in net['coverage']:
                mapping=fold_net(net,surfaces[i]);assert mapping is not None
                verify_net(net,surfaces[i],mapping);net['mappings'][i]=mapping
            nets.append(net)
        output[k]=dict(units=k,total_polycubes=len(levels[k]),eligible_tree_shapes=len(shapes),
                       planar_tree_shapes=len(planar),shapes=shapes,surfaces=surfaces,nets=nets,
                       tested_foot_patterns=len(coverage),best_family_coverage=len(coverage[best]),
                       best_planar_coverage=len(planar&set(coverage[planar_best])),
                       universal_net_found=len(coverage[best])==len(shapes),
                       scope='Maximum in symmetric paired-foot spine family only; not all possible nets. Mirror shapes counted separately; folding may use either side.')
        extended=defaultdict(list)
        for i,surf in enumerate(surfaces):
            for pattern in foot_patterns(surf,k,extension=True):extended[pattern].append(i)
        choice=max(extended,key=lambda p:(len(extended[p]),-p[0],-p[1]))
        extra=make_net(k,*choice);extra['coverage']=extended[choice]
        extra['mappings']=[None]*len(shapes)
        for i in extra['coverage']:
            mapping=fold_net(extra,surfaces[i]);assert mapping is not None
            verify_net(extra,surfaces[i],mapping);extra['mappings'][i]=mapping
        output[k]['extended_family_best']=extra
        output[k]['extended_family_patterns']=len(extended)
        destination.write_text(json.dumps(output,separators=(',',':')))
        print(f'cubes {k}: best={len(coverage[best])}/{len(shapes)}, planar={len(planar&set(coverage[planar_best]))}/{len(planar)} patterns={len(coverage)}',flush=True)
    return output


if __name__=='__main__':run()
