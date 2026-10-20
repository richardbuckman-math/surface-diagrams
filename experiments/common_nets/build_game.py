"""Prepare browser-sized meshes and hinge targets from exact folding maps."""
import json
from hashlib import sha256
from math import atan2,sqrt
from pathlib import Path

from .build_tetrahedra_atlas import choose_puzzles,puzzle_palette
from .engine import verify_net


def sub(a,b):return [x-y for x,y in zip(a,b)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def unit(a):
    length=sqrt(dot(a,a))
    return [x/length for x in a]
def frame(t):
    u=unit(sub(t[1],t[0]));d=sub(t[2],t[0]);v=unit([d[i]-dot(d,u)*u[i] for i in range(3)])
    return [u,v,cross(u,v)]


def target_mesh(net,surface,mapping,with_cells=False):
    square=net.get('cells') is not None
    if square:
        from .cubes import verify_net as verify_cube
        verify_cube(net,surface,mapping)
    else:verify_net(net,surface,mapping)
    sides=4 if square else 3
    faces=[[surface['faces'][f][(r+h*j)%sides] for j in range(sides)] for f,r,h in mapping]
    basis=frame(faces[0]);origin=faces[0][0];length=sqrt(dot(sub(faces[0][1],origin),sub(faces[0][1],origin)))
    flat=([[[x,y,0],[x+1,y,0],[x+1,y+1,0],[x,y+1,0]] for x,y in net['cells']] if square else
          [[[x+y/2,y*sqrt(3)/2,0] for x,y in t] for t in net['triangles']])
    out_basis=frame(flat[0]);out_origin=flat[0][0]
    def point(p):
        xyz=[dot(sub(p,origin),u)/length for u in basis]
        return [out_origin[i]+sum(xyz[k]*out_basis[k][i] for k in range(3)) for i in range(3)]
    mesh=[[point(p) for p in f] for f in faces]
    normals=[unit(cross(sub(t[1],t[0]),sub(t[2],t[0]))) for t in mesh]
    angles=[]
    for hinge in net['hinges']:
        a,b,e=hinge[:3]
        axis=unit(sub(mesh[a][(e+1)%sides],mesh[a][e]))
        angles.append(atan2(dot(axis,cross(normals[a],normals[b])),dot(normals[a],normals[b])))
    if with_cells:
        from itertools import product
        cells=[]
        for c in surface['cluster']:
            vertices=[point([c[i]+d[i] for i in range(3)]) for d in product((0,1),repeat=3)]
            cells.append([round(min(p[i] for p in vertices)) for i in range(3)])
        return flat,mesh,angles,cells
    return flat,mesh,angles


def build():
    root=Path(__file__).resolve().parents[2]
    source=root/'.preview/common-nets/tetrahedra-through-eight.json'
    report=json.loads(source.read_text());puzzles=[]
    for p in choose_puzzles(report):
        n=p['units'];net=p['net'];targets=[]
        for i in net['coverage']:
            flat,mesh,angles=target_mesh(net,report['levels'][str(n)]['surfaces'][i],net['mappings'][i])
            targets.append(dict(id='%d-%03d'%(n,i+1),faces=mesh,angles=angles,
                                colors=puzzle_palette('%s:%d'%(p['id'],i),len(flat),'target')))
        puzzles.append(dict(id=p['id'],units=n,faces=flat,hinges=net['hinges'],
                            colors=puzzle_palette(p['id'],len(flat),'net'),targets=targets))
    data=dict(version=1,source_sha256=sha256(source.read_bytes()).hexdigest(),
              scope='Fixed whole-triangle panels; numerical interaction with exact folded-end-state source certificates. Continuous collision-free folding is not checked.',
              puzzles=puzzles)
    path=Path(__file__).parent/'game/data.json';path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data,separators=(',',':')),encoding='utf-8')
    print('Saved',len(puzzles),'nets /',sum(len(p['targets']) for p in puzzles),'challenges;',path.stat().st_size,'bytes')
    return data


def build_cubes():
    from .cube_puzzles import run
    report=run();folder=Path(__file__).parent/'game';nets=folder/'cube-nets';nets.mkdir(exist_ok=True)
    index=dict(version=1,family='cubes',puzzles=[],source=report['source'],catalog={})
    for number,row in report['levels'].items():
        n=int(number)
        from .cubes import is_planar
        covered=set().union(*(set(net['coverage']) for net in row['nets']))
        planar={i for i,c in enumerate(row['shapes']) if is_planar(c)}
        index['catalog'][number]=dict(tree_shapes=row['tree_shapes'],planar_tree_shapes=len(planar),
                                      represented_shapes=len(covered),represented_planar=len(covered&planar))
        for net in row['nets']:
            targets=[]
            for i in net['coverage']:
                flat,mesh,angles,cells=target_mesh(net,row['surfaces'][i],net['mappings'][i],with_cells=True)
                targets.append(dict(id='C%d-%03d'%(n,i+1),faces=[[[round(v) for v in p] for p in t] for t in mesh],
                                    angles=angles,cells=cells,colors=[[round(v,5) for v in c] for c in puzzle_palette('%s:%d'%(net['id'],i),len(flat),'target')]))
            label=net['label']
            entry=dict(id=net['id'],family='cubes',allowMirrors=False,units=n,label=label,note=net['note'],
                       faces=flat,hinges=[h[:3] for h in net['hinges']],targets=targets,
                       colors=[[round(v,5) for v in c] for c in puzzle_palette(net['id'],len(flat),'net')])
            if net.get('source'):
                entry['source']=net['source']
                if n==5 and 'Published planar' in label:entry['source']=report['source']+'#page=10'
            name='cube-nets/'+net['id']+'.json';(folder/name).write_text(json.dumps(entry,separators=(',',':')))
            index['puzzles'].append(dict(id=net['id'],units=n,label=label,file=name,targetCount=len(targets)))
    (folder/'cubes-index.json').write_text(json.dumps(index,separators=(',',':')))
    print('Saved',len(index['puzzles']),'cube nets /',sum(p['targetCount'] for p in index['puzzles']),'challenges')
    return index


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--cubes',action='store_true');args=parser.parse_args()
    build_cubes() if args.cubes else build()
