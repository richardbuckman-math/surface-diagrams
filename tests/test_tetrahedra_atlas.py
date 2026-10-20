"""Complete larger catalogs, honest sampled nets, and lossless page plans."""
import unittest
from experiments.common_nets import engine
from experiments.common_nets.extend_tetrahedra import EXPECTED_COUNTS,sample_puzzles
from experiments.common_nets.build_tetrahedra_atlas import choose_puzzles,page_plan,puzzle_palette


class LargerTetrahedronTests(unittest.TestCase):
    def test_complete_counts_and_surfaces_through_eight(self):
        levels=engine.enumerate_polytets(8)
        self.assertEqual([len(levels[n]) for n in range(1,9)],EXPECTED_COUNTS)
        for n in (7,8):
            for cluster in levels[n]:
                self.assertEqual(len(engine.surface(cluster)['faces']),2*n+2)
                self.assertTrue(all(isinstance(x,int) for tet in cluster for v in tet for x in v))

    def test_bounded_puzzle_search_retains_exact_certificates(self):
        levels=engine.enumerate_polytets(4)
        surfaces=[engine.surface(c) for c in levels[4]]
        result=sample_puzzles(surfaces,attempts=35,seed=17,keep=3)
        self.assertFalse(result['optimality_proved'])
        self.assertEqual(result['attempts'],35)
        self.assertGreater(len(result['candidates']),0)
        for net in result['candidates']:
            self.assertIn(net['source'],net['coverage'])
            for i,surface in enumerate(surfaces):
                mapping=net['mappings'][i]
                self.assertEqual(mapping is not None,i in net['coverage'])
                if mapping:self.assertTrue(engine.verify_net(net,surface,mapping))

    def test_plan_never_drops_or_adds_puzzle_targets(self):
        rows={}
        for n,count in enumerate(EXPECTED_COUNTS,1):
            first=dict(coverage=list(range(min(count,35))))
            second=dict(coverage=list(range(max(0,count-25),count)))
            rows[str(n)]=dict(shapes=count,net=first,two_net_cover=[first,second],
                             puzzle_search=dict(candidates=[first,second]))
        report=dict(levels=rows)
        puzzles=choose_puzzles(report);plan=page_plan(report,puzzles)
        self.assertEqual([p['kind'] for p in plan[:3]],['cover','contents','puzzle_intro'])
        self.assertLess(next(i for i,p in enumerate(plan) if p.get('section')=='solutions'),
                        next(i for i,p in enumerate(plan) if p['kind']=='small_catalog'))
        for n in range(5,9):
            actual=[i for page in plan if page['kind']=='catalog' and page['units']==n for i in page['indices']]
            self.assertEqual(actual,list(range(EXPECTED_COUNTS[n-1])))
        for puzzle in puzzles:
            if puzzle['units']<=4:continue
            for section in ('puzzles','solutions'):
                actual=[i for page in plan if page['kind'] in ('puzzle','puzzle_targets')
                        and page['section']==section and page['puzzle']['id']==puzzle['id'] for i in page['indices']]
                self.assertEqual(actual,puzzle['net']['coverage'])

    def test_puzzle_palettes_are_stable_independent_and_disjoint(self):
        net=puzzle_palette('P8A',18,'net')
        target=puzzle_palette('P8A:4',18,'target')
        self.assertEqual(net,puzzle_palette('P8A',18,'net'))
        self.assertEqual(len(set(net)),18)
        self.assertFalse(set(net)&set(target))
        self.assertNotEqual(target,puzzle_palette('P8A:5',18,'target'))


if __name__=='__main__':unittest.main()
