"""Bounded unrestricted square-hinge search, beyond the planar spine family."""
import json
from pathlib import Path
import random
import time
if __package__:
    from . import cubes
else:
    import cubes


def attach(square,edge):
    a,b=square[edge],square[(edge+1)%4]
    step=(b[1]-a[1],a[0]-b[0])
    return (b,a,(a[0]+step[0],a[1]+step[1]),(b[0]+step[0],b[1]+step[1]))


def search(surfaces,seconds=60):
    n=len(surfaces[0]['faces']);adj=surfaces[0]['adjacency'];start=time.monotonic()
    triangles=[((0,0),(1,0),(1,1),(0,1))];states=[(0,0,1)];hinges=[]
    occupied={tuple(sorted(triangles[0]))}
    initial=[[(1<<f,((f,r,h),)) for f in range(n) for r in range(4) for h in (1,-1)] for _ in surfaces[1:]]
    answer=None;nodes=0
    def dfs(used,excluded,possibilities):
        nonlocal answer,nodes
        nodes+=1
        if nodes%256==0 and time.monotonic()-start>seconds:raise TimeoutError
        if len(states)==n:
            answer=dict(squares=list(triangles),hinges=list(hinges),source_mapping=list(states),
                        target_mappings=[list(v[0][1]) for v in possibilities]);return True
        frontier=[]
        for parent,state in enumerate(states):
            for edge in range(4):
                nxt=cubes.neighbor(state,edge,0,adj)
                key=tuple(sorted((state[0],nxt[0])))
                if not used>>nxt[0]&1 and key not in excluded:frontier.append((key,parent,edge,nxt))
        if not frontier:return False
        key,parent,edge,nxt=min(frontier)
        polygon=attach(triangles[parent],edge);cell=tuple(sorted(polygon))
        if cell not in occupied:
            grown=[]
            for s,opts in zip(surfaces[1:],possibilities):
                keep=[]
                for mask,placement in opts:
                    t=cubes.neighbor(placement[parent],edge,0,s['adjacency'])
                    if not mask>>t[0]&1:keep.append((mask|(1<<t[0]),placement+(t,)))
                if not keep:break
                grown.append(keep)
            if len(grown)==len(surfaces)-1:
                triangles.append(polygon);states.append(nxt);occupied.add(cell);hinges.append((parent,len(states)-1,edge,0))
                if dfs(used|(1<<nxt[0]),excluded,grown):return True
                hinges.pop();occupied.remove(cell);states.pop();triangles.pop()
        return dfs(used,excluded|{key},possibilities)
    exhausted=True
    try:dfs(1,frozenset(),initial)
    except TimeoutError:exhausted=False
    return dict(found=answer,exhausted=exhausted,nodes=nodes,seconds=round(time.monotonic()-start,3))


def run():
    path=Path('.preview/common-nets/cubes.json');report=json.loads(path.read_text())
    results={};rng=random.Random(20261020)
    for k in ('6','7'):
        row=report[k]
        nonplanar=[i for i,c in enumerate(row['shapes']) if not cubes.is_planar(c)]
        rng.shuffle(nonplanar)
        targets=[0]+nonplanar[:4]
        result=search([row['surfaces'][i] for i in targets],seconds=75)
        result['target_indices']=targets
        results[k]=result
        print('general cubes',k,{key:value for key,value in result.items() if key!='found'},flush=True)
        Path('.preview/common-nets/cube-general-search.json').write_text(json.dumps(results,separators=(',',':')))


if __name__=='__main__':run()
