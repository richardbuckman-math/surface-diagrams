from dataclasses import asdict,replace
from pathlib import Path
import json,unittest
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.named_unsplit_sphere import unsplit_sphere_lantern,shorten_unsplit_first_lantern
from surface_diagrams.puncture_boundary import early_boundary_derivation
from surface_diagrams.sphere_actions import sphere_chain_certificate


class UnsplitFirstSphereLanternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=early_boundary_derivation()['stages'][:18]
        cls.r=shorten_unsplit_first_lantern(cls.old)
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'

    def test_generic_rule_retains_its_full_twist_PC_parent_and_separate_complement_lift(self):
        for chart in ((),(1,-2),(5,4,-3),(2,3,2,5,-3,-3,4)):
            p=unsplit_sphere_lantern(chart)
            self.assertEqual(p['parent_free_word_discrepancy'],())
            self.assertEqual(exact_action(product(p['inputs']),6),exact_action(product(p['full_twist_PC_parent']),6))
            self.assertEqual(exact_action(product(p['full_twist_PC_parent']),6),exact_action(product(p['parent_disk_outputs']),6))
            self.assertNotEqual(exact_action(product(p['inputs']),6),exact_action(product(p['outputs']),6))
            self.assertTrue(p['sphere_certificate']['certified']);self.assertEqual(p['chosen_lift_discrepancy'],IDENTITY)
            self.assertTrue(p['complement_sphere_certificate']['certified']);self.assertEqual(p['complement_chosen_lift'],IDENTITY)
            self.assertFalse(p['source_centrality_assumed']);self.assertFalse(p['framed_hole_half_twist_convention_asserted'])

    def test_actual_square_and_two_DISTINCT_half_inputs_match_one_common_chart(self):
        s=self.r['stages'][11];w=s['named_pattern_witness'];before=s['local_before']
        self.assertEqual(tuple(f.id for f in before),('F1','F2','F7.disk'))
        self.assertEqual(tuple((f.power,f.half) for f in before),((2,False),(1,True),(1,True)))
        self.assertNotEqual(exact_action(before[1].word,6),exact_action(before[2].word,6))
        for m in w['individual_matches']+w['output_matches']:
            self.assertTrue(m['exact_disk_equal']);self.assertEqual(exact_action(m['actual'].word,6),exact_action(m['pattern'].word,6))
        self.assertTrue(w['old_prefix_disk_product_equal'])
        self.assertEqual(before[0],self.old[0]['factors'][0])

    def test_literal_joins_and_count_savings_are_actual_route_changes(self):
        r=self.r
        self.assertEqual((r['previous_graphical_steps'],r['graphical_steps'],r['previous_whole_named_steps'],r['whole_named_steps']),(17,14,82,79))
        self.assertEqual((r['old_prefix_adjacent_checks'],r['new_prefix_adjacent_checks']),(14,12))
        self.assertEqual((r['changed_prefix_peak_support_word'],r['previous_prefix_peak_support_word']),(30,30))
        self.assertTrue(r['literal_rejoin']);self.assertEqual(r['stages'][11]['factors'],self.old[14]['factors'])
        self.assertEqual(r['stages'][12:],tuple(self.old[15:]))
        self.assertTrue(r['original_F1_square_unsplit']);self.assertTrue(r['actual_target_halves_distinct'])
        self.assertFalse(any(s['kind']=='disk_combine' for s in r['stages'][:12]))
        self.assertFalse(any('F1.' in f.id for s in r['stages'][:12] for f in s['factors']))

    def test_every_pre_lantern_disk_state_and_atomic_neighbor_preserves_the_whole_product(self):
        target=exact_action(product(self.old[0]['factors']),6)
        for s in self.r['stages'][:11]:
            for a in (s,)+tuple(s.get('atomic_steps',())):
                self.assertEqual(exact_action(product(a['factors']),6),target)
        retained=[a for s in self.r['stages'][:12] for a in (s,)+tuple(s.get('atomic_steps',()))]
        self.assertEqual(len(retained),len(self.r['state_sphere_lift_certificates']))
        for s,c in zip(retained,self.r['state_sphere_lift_certificates']):
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
            self.assertEqual(homology_action(product(s['factors'])),IDENTITY)

    def test_six_neighbor_drag_keeps_F7_fixed_and_retains_both_certificate_layers(self):
        s=self.r['stages'][10];self.assertEqual(s['adjacent_moves'],6)
        source=next(f for f in self.r['stages'][9]['factors'] if f.id=='F7.disk')
        for a in s['atomic_steps']:
            self.assertEqual(a['disk_word_certificate']['discrepancy'],())
            self.assertTrue(all(a['individual_presentation_matches']))
            self.assertEqual(next(f for f in a['factors'] if f.id=='F7.disk'),source)
            for raw,shown in zip(a['raw_factors'],a['factors']):self.assertEqual(exact_action(raw.word,6),exact_action(shown.word,6))

    def test_actual_full_nonabelian_splits_and_parent_framing_balance_are_retained(self):
        w=self.r['stages'][11]['named_pattern_witness'];p=w['unsplit_sphere_lantern']
        self.assertEqual(p['parent_signed_framing_balance'],(0,1,0,0,1,0))
        self.assertEqual(len(w['complete_actual_point_pushing']),5)
        for row in w['complete_actual_point_pushing']:
            self.assertEqual(exact_action(row['factor'].word,6),exact_action(row['split'].reconstructed_word,6))
        self.assertTrue(any(row['split'].kernel_loop for row in w['complete_actual_point_pushing']))
        self.assertFalse(self.r['framed_hole_half_twist_convention_asserted'])

    def test_wrong_order_and_changed_sources_do_not_silently_pass(self):
        p=unsplit_sphere_lantern();a,b,c=p['inputs'];wrong=(a,c,b)
        self.assertFalse(sphere_chain_certificate(product(wrong)+inverse_word(product(p['outputs'])))['certified'])
        with self.assertRaises(ValueError):shorten_unsplit_first_lantern(self.old[:-1])
        bad=[dict(s) for s in self.old];bad[2]['factors']=(replace(bad[2]['factors'][0],power=1),)+bad[2]['factors'][1:]
        with self.assertRaises(ValueError):shorten_unsplit_first_lantern(bad)

    def test_public79_keeps_the_historical82_components_and_four_sphere_moves(self):
        c=json.loads((self.folder/'certificate.json').read_text(encoding='utf-8'))
        metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
        self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),c['named_unsplit_first_lantern'])
        self.assertEqual(c['named_powered_cabled_shortening']['whole_named_steps'],82)
        summary=c['named_full_route']['summary'];self.assertEqual(summary['graphical_steps'],79)
        self.assertEqual(summary['route_parts'],[14,63,1,1]);self.assertEqual(summary['sphere_moves'],4)
        self.assertEqual(summary['action_only_boundary_recognitions'],0);self.assertFalse(summary['complete_under_twenty_derivation'])
        self.assertEqual(tuple(i for i,s in enumerate(c['named_full_route']['stages']) if s['kind']=='sphere_rewrite'),(11,13,14,79))
        d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'));self.assertEqual(len(d['routes']['namedfull']),80)
        self.assertTrue(d['routes']['namedfull'][11]['unsplit_sphere_lantern'])
        self.assertNotIn('_named_early',d['routes'])
        html=(self.folder/'index.html').read_text(encoding='utf-8');self.assertIn('79 retained steps',html)
        self.assertIn('two DISTINCT half twists',html)


if __name__=='__main__':unittest.main()
