from dataclasses import asdict,replace
from pathlib import Path
import json,unittest
from tests import test_named_early_powered_daisy as historical_source
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.named_powered_cabled import powered_cabled_lantern,shorten_powered_cabled_start
from surface_diagrams.puncture_boundary import BOUNDARY_WORD


class PoweredCabledStartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        historical_source.EarlyPoweredDaisyTests.setUpClass()
        cls.old=historical_source.EarlyPoweredDaisyTests.r
        cls.r=shorten_powered_cabled_start(cls.old['stages'])
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'

    def test_generic_rule_for_81_root_inner_power_and_chart_cases(self):
        for m in (1,2,3):
            for n in (1,2,3):
                for k in (1,2,3):
                    for chart in ((),(1,-2),(4,4,-3)):
                        p=powered_cabled_lantern(m,n,k,chart=chart)
                        self.assertEqual(exact_action(product(p['inputs']),5),exact_action(product(p['outputs']),5))
                        self.assertTrue(all(f.power>0 and not f.half for f in p['outputs']))
                        self.assertEqual(len(p['outputs']),2+(m>1)+(n>1))
                        self.assertTrue(p['retained_left_decomposition']['exact_free_word_equality'])
                        self.assertTrue(p['retained_right_decomposition']['exact_free_word_equality'])
                        self.assertTrue(p['retained_inner_merge']['exact_free_word_equality'])
                        self.assertFalse(p['actual_standalone_root_splits']);self.assertFalse(p['actual_standalone_inner_merge'])
                        self.assertEqual(reduce_word(product(p['retained_shared_inner_crossing']['local_before'])),reduce_word(product(p['retained_shared_inner_crossing']['local_after'])))

    def test_all_four_actual_powered_inputs_and_outputs_match_individually(self):
        s=self.r['replacement_interval'][2];w=s['named_pattern_witness'];p=w['powered_cabled_lantern']
        self.assertEqual([f.power for f in s['local_before']],[2,1,1,2])
        self.assertEqual([f.power for f in s['local_after']],[1,1,2,1])
        self.assertEqual(p['common_chart'],(-4,-4));self.assertTrue(w['every_actual_input_matched'])
        for m in w['individual_matches']+w['output_presentation_matches']:
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
        self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))

    def test_cyclic_frames_are_free_word_exact_and_all_original_halves_stay_literal(self):
        r=self.r;original=tuple(f for f in r['replacement_interval'][0]['factors'] if f.half)
        for s,c in zip(r['replacement_interval'],r['state_sphere_lift_certificates']):
            self.assertEqual(tuple(f for f in s['factors'] if f.half),original)
            self.assertEqual(exact_action(product(s['factors']),5),exact_action(BOUNDARY_WORD*4,5))
            self.assertEqual(homology_action(product(s['factors'])),IDENTITY)
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)
        for s in (r['replacement_interval'][1],r['replacement_interval'][3]):
            self.assertEqual(reduce_word(s['frame']+product(s['local_before'])+inverse_word(s['frame'])),reduce_word(product(s['local_after'])))
        source=r['replacement_interval'][0]['factors'][-1]
        self.assertEqual(reduce_word(r['replacement_interval'][3]['frame']+r['replacement_interval'][1]['frame']),replace(source,power=1).word)
        self.assertTrue(r['original_halves_unchanged'])

    def test_literal_join_counts_and_final_exteriors(self):
        r=self.r
        self.assertEqual((r['previous_whole_named_steps'],r['whole_named_steps'],r['graphical_steps']),(85,82,63))
        self.assertEqual((r['previous_operations'],r['replacement_operations']),(6,3))
        self.assertEqual((r['previous_adjacent_checks'],r['adjacent_checks'],r['added_internal_shared_inner_checks']),(108,107,1))
        self.assertEqual((r['extension_peak_support_word'],r['actual_peak_support_word']),(16,20))
        self.assertTrue(r['literal_rejoin']);self.assertEqual(r['stages'][3]['factors'],self.old['stages'][6]['factors'])
        self.assertEqual(r['stages'][4:],self.old['stages'][7:])
        self.assertEqual(len(r['factors']),4);self.assertTrue(all(f==Factor(f.id,(),1,5) for f in r['factors']))

    def test_full_normalized_kernels_shadows_and_signed_framing_are_retained(self):
        s=self.r['replacement_interval'][2];w=s['named_pattern_witness'];p=w['powered_cabled_lantern']
        canonical=p['canonical_inputs']+p['canonical_outputs']
        self.assertEqual(len(w['complete_point_pushing']),8)
        for f,split,expected in zip(w['normalized_actual_inputs_and_outputs'],w['complete_point_pushing'],canonical):
            self.assertFalse(split.kernel_loop)
            self.assertEqual(exact_action(f.word,5),exact_action(split.reconstructed_word,5))
            self.assertEqual(exact_action(split.shadow_word,4),exact_action(expected.word,4))
        self.assertEqual(s['framed_balance_before_minus_after'],(0,0,1,1,0))
        self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)

    def test_wrong_order_and_omitted_inner_factor_fail(self):
        p=powered_cabled_lantern(2,2,1);fs=p['inputs']
        wrong=fs[1:2]+fs[:1]+fs[2:]
        self.assertNotEqual(exact_action(product(wrong),5),exact_action(product(p['outputs']),5))
        self.assertNotEqual(exact_action(product(fs[:2]+fs[3:]),5),exact_action(product(p['outputs']),5))
        self.assertEqual(p['outputs'][2].power,2)

    def test_current_public_route_is82_and_historical85_component_is_unchanged(self):
        c=json.loads((self.folder/'certificate.json').read_text(encoding='utf-8'))
        metadata={k:v for k,v in self.r.items() if k not in ('stages','factors')}
        self.assertEqual(json.loads(json.dumps(metadata,default=asdict)),c['named_powered_cabled_shortening'])
        self.assertEqual(c['named_early_powered_daisy_shortening']['whole_named_steps'],85)
        s=c['named_full_route']['summary'];self.assertEqual((s['graphical_steps'],s['sphere_moves'],s['action_only_boundary_recognitions']),(82,4,0))
        self.assertEqual(s['route_parts'],[17,63,1,1]);self.assertFalse(s['complete_under_twenty_derivation'])
        d=json.loads((self.folder/'display-pure.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['routes']['namedfull']),83);self.assertTrue(d['routes']['namedfull'][19]['powered_cabled_lantern'])
        html=(self.folder/'index.html').read_text(encoding='utf-8');self.assertIn('82 retained steps',html)
        self.assertIn('EXACT DISK POWERED CABLED PC LANTERN',html)

    def test_invalid_powers_and_changed_sources_are_rejected(self):
        for bad in (True,0,-1,1.5):
            for position in range(3):
                args=[2,2,1];args[position]=bad
                with self.assertRaises(ValueError):powered_cabled_lantern(*args)
        with self.assertRaises(ValueError):shorten_powered_cabled_start(self.old['stages'][:-1])


if __name__=='__main__':unittest.main()
