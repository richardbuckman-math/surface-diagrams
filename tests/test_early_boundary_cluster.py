"""A positive, bounded geometric contraction toward the last disk equality."""
from collections import Counter
import json
from pathlib import Path
import unittest

from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.puncture_boundary import early_boundary_derivation, BOUNDARY_WORD
from surface_diagrams.early_boundary_cluster import positive_early_cluster


class EarlyBoundaryClusterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=early_boundary_derivation()['chart']['factors']
        cls.route=positive_early_cluster(cls.source)

    def test_every_disk_operation_stays_positive_and_bounded(self):
        r=self.route;expected=exact_action(BOUNDARY_WORD*4,5)
        self.assertEqual((len(r['stages']),r['graphical_steps'],r['sphere_move_count']),(8,7,0))
        for s in r['stages']:
            self.assertEqual(exact_action(product(s['factors']),5),expected)
            self.assertTrue(all(getattr(f,'sign',1)==1 for f in s['factors']))
            self.assertLessEqual(max(len(supported_class(f.mapping_class,5)) for f in s['factors']),20)
            self.assertNotIn('sphere',s['kind'])
            for a in s.get('atomic_steps',()):
                self.assertFalse(a['disk_word_certificate']['discrepancy'])
                self.assertEqual(exact_action(product(a['factors']),5),expected)
        self.assertEqual([s['adjacent_moves'] for s in r['stages'] if 'adjacent_moves' in s],[4,7])
        self.assertEqual(r['after_score'],dict(max_support_word=20,total_support_word=130,braid_letters=222))

    def test_exact_lantern_exposes_a_daisy_without_an_inverse(self):
        r=self.route;s=r['stages'][-1]
        self.assertEqual(s['kind'],'disk_cluster_lantern')
        self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
        self.assertEqual(len(r['factors']),18)
        outer=r['next_daisy']['outer'];self.assertEqual((outer.points,outer.id),(4,'early.O1345'))
        self.assertEqual(exact_action(outer.word,5),exact_action(tuple(x for t in r['next_daisy']['terms'] for x in t.word),5))
        self.assertFalse(r['next_daisy']['applied_to_replay']);self.assertFalse(r['complete_named_derivation'])
        self.assertNotIn('prefix.P45',[f.id for f in r['factors']])
        for bad in (self.source[:-1],self.source[:2]+(self.source[3],self.source[2])+self.source[4:]):
            with self.assertRaises(ValueError):positive_early_cluster(bad)

    def test_published_progress_phase_has_no_sphere_display_shortcuts(self):
        folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        display=json.loads((folder/'display-early.json').read_text())
        for actual,shown in zip(self.route['stages'],display['routes']['earlycluster']):
            for f,i in zip(actual['factors'],shown['factors']):
                row=display['rows'][i];self.assertFalse(row['sphere_rechart'])
                self.assertEqual(exact_action(f.word),exact_action(row['word']))
        self.assertEqual(len(display['routes']['earlycluster']),8)


if __name__=='__main__': unittest.main()
