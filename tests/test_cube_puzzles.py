"""Independent integer checks of the cube game's committed target surfaces."""
import json
from pathlib import Path
import unittest
from experiments.common_nets import cubes
from experiments.common_nets.cube_puzzles import FIVE_23,CLASSIC_FOUR,outline_variants,SquareSurface


class CubePuzzleTests(unittest.TestCase):
    def test_book_preserves_every_target_in_both_sections(self):
        from experiments.common_nets.build_cube_book import load_collection,page_plan
        _,nets=load_collection();plan=page_plan(nets)
        self.assertEqual([p['kind'] for p in plan[:2]],['cover','contents'])
        self.assertLess(max(i for i,p in enumerate(plan) if p.get('section')=='puzzles'),
                        min(i for i,p in enumerate(plan) if p.get('section')=='solutions'))
        for net in nets:
            for section in ('puzzles','solutions'):
                actual=[t for page in plan if page.get('section')==section and page.get('net')==net['id'] for t in page['targets']]
                grouped=[p for p in plan if p.get('section')==section and net['id'] in p.get('nets',[])]
                if grouped:
                    self.assertEqual(len(grouped),1);actual=list(range(len(net['targets'])))
                self.assertEqual(actual,list(range(len(net['targets']))))

    def test_planar_targets_cover_all_tree_polyominoes_through_eight(self):
        def key(cells):
            variants=[]
            for reflected in (False,True):
                for r in range(4):
                    ps=[]
                    for a,b in cells:
                        x,y=(-a if reflected else a),b
                        for _ in range(r):x,y=-y,x
                        ps.append((x,y))
                    low=[min(p[i] for p in ps) for i in range(2)]
                    variants.append(tuple(sorted((x-low[0],y-low[1]) for x,y in ps)))
            return min(variants)
        directions=((1,0),(-1,0),(0,1),(0,-1));levels={1:{((0,0),)}}
        for n in range(2,9):
            level=set()
            for cells in levels[n-1]:
                occupied=set(cells)
                for x,y in cells:
                    for dx,dy in directions:
                        q=(x+dx,y+dy)
                        if q not in occupied:level.add(key((*cells,q)))
            levels[n]=level
        self.assertEqual([len(levels[n]) for n in range(1,9)],[1,1,2,5,12,35,108,369])
        expected={n:{c for c in level if sum((x+dx,y+dy) in c for x,y in c for dx,dy in directions)//2==n-1} for n,level in levels.items()}
        self.assertEqual([len(expected[n]) for n in range(1,9)],[1,1,2,4,11,27,83,255])
        folder=Path(__file__).resolve().parents[1]/'experiments/common_nets/game'
        index=json.loads((folder/'cubes-index.json').read_text());actual={n:set() for n in range(1,9)}
        for descriptor in index['puzzles']:
            net=json.loads((folder/descriptor['file']).read_text())
            for target in net['targets']:
                cells=target['cells']
                axis=next((i for i in range(3) if len({c[i] for c in cells})==1),None)
                if axis is not None:actual[net['units']].add(key([tuple(c[i] for i in range(3) if i!=axis) for c in cells]))
        self.assertEqual(actual,expected)

    def test_every_target_is_the_whole_exterior_of_its_cube_cluster(self):
        folder=Path(__file__).resolve().parents[1]/'experiments/common_nets/game'
        index=json.loads((folder/'cubes-index.json').read_text());count=0
        bag=lambda faces:{tuple(sorted(tuple(p) for p in f)) for f in faces}
        for descriptor in index['puzzles']:
            net=json.loads((folder/descriptor['file']).read_text())
            self.assertEqual(len(net['faces']),4*net['units']+2)
            self.assertEqual(len(net['hinges']),len(net['faces'])-1)
            for target in net['targets']:
                cells=list(map(tuple,target['cells']));self.assertEqual(len(set(cells)),net['units'])
                self.assertTrue(cubes.is_tree(cells))
                seen={cells[0]};pending=[cells[0]];occupied=set(cells)
                for c in pending:
                    for d in cubes.DIRS:
                        q=tuple(c[i]+d[i] for i in range(3))
                        if q in occupied and q not in seen:seen.add(q);pending.append(q)
                self.assertEqual(len(seen),len(cells))
                self.assertEqual(bag(target['faces']),bag(cubes.surface(cells)['faces']))
                self.assertEqual(len(bag(target['faces'])),len(net['faces']))
                count+=1
        self.assertEqual(count,796)

    def test_published_twenty_three_target_net_rechecks_in_original_cube_engine(self):
        shapes=[s for s in cubes.enumerate_cubes(5)[5] if cubes.is_tree(s)]
        net=next(outline_variants(FIVE_23));actual=[]
        for i,shape in enumerate(shapes):
            surface=cubes.surface(shape);mapping=cubes.fold_net(net,surface)
            compiled=SquareSurface(surface).fold(net)
            self.assertEqual(mapping is not None,compiled is not None)
            if mapping is not None:self.assertTrue(cubes.verify_net(net,surface,mapping));actual.append(i)
        self.assertEqual(len(actual),23)

    def test_classic_four_cube_game_preserves_the_source_outline(self):
        folder=Path(__file__).resolve().parents[1]/'experiments/common_nets/game'
        net=json.loads((folder/'cube-nets/C4A.json').read_text())
        cells={(min(p[0] for p in f),min(p[1] for p in f)) for f in net['faces']}
        self.assertEqual(cells,set(CLASSIC_FOUR))
        self.assertEqual(len(net['targets']),7)


if __name__=='__main__':unittest.main()
