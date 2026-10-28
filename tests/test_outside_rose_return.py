from dataclasses import asdict,replace
from pathlib import Path
import json
import unittest
from examples.analyze_outside_rose_return import report
from surface_diagrams.outside_rose_return import return_outside_rose
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.puncture_boundary import BOUNDARY_WORD

class OutsideRoseReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=report()
        cls.root=Path(__file__).resolve().parents[1]

    def test_all_retained_states_and_adjacent_checks_are_positive_disk_sphere_lift_exact(self):
        r=self.r;maximum=0;count=0
        for stage in r['stages']:
            for s in (stage,)+stage.get('atomic_steps',()):
                fs=s['factors'];count+=1
                self.assertTrue(all(not f.half and f.power==1 for f in fs))
                self.assertEqual(exact_action(product(fs),5),exact_action(BOUNDARY_WORD*4,5))
                self.assertEqual(homology_action(product(fs)),IDENTITY)
                maximum=max(maximum,max(len(supported_class(f.mapping_class,5)) for f in fs))
        self.assertEqual((maximum,count),(19,17))
        self.assertEqual((r['graphical_operations'],r['adjacent_checks'],r['internal_named_adjacent_checks']),(9,7,1))
        self.assertEqual(len(r['state_sphere_lift_certificates']),count)
        for c in r['state_sphere_lift_certificates']:
            self.assertTrue(c['sphere_certificate']['certified']);self.assertEqual(c['chosen_lift'],IDENTITY)

    def test_actual_borrow_return_and_duplicate_pair_are_retained(self):
        s=self.r['stages'];w=s[1]['named_pattern_witness']
        self.assertEqual(w['cyclic_offset'],1)
        rose=w['canonical_rose'];self.assertEqual(s[1]['local_after'],rose[1:]+rose[:1])
        self.assertEqual(exact_action(product(rose),5),exact_action(product(s[1]['local_before']),5))
        self.assertEqual(s[3]['adjacent_moves'],2)
        self.assertEqual(tuple(f.id for f in s[4]['local_before']),('return.0','outside.rose.1','outside.rose.2'))
        restored=s[4]['local_after'][0]
        self.assertEqual(restored,Factor('return.restored.R124',(3,),1,3))
        d={f.id:f for f in self.r['factors']}
        self.assertEqual(exact_action(d['one.unit.Q1'].word,5),exact_action(d['return.1'].word,5))
        self.assertFalse(any(s['kind']=='disk_combine' for s in self.r['stages']))

    def test_all_named_inputs_outputs_framing_balances_and_local_lifts_match(self):
        for s in self.r['stages']:
            if 'named_pattern_witness' not in s:continue
            w=s['named_pattern_witness']
            for m in w['individual_matches']+w.get('output_presentations',()):
                self.assertTrue(m['exact_disk_equal'])
                self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
            self.assertEqual(exact_action(product(s['local_before']),5),exact_action(product(s['local_after']),5))
            self.assertTrue(w['sphere_certificate']['certified']);self.assertEqual(w['chosen_lift_discrepancy'],IDENTITY)
            expected=tuple(sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-
                           sum(f.power for f in s['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
            self.assertEqual(s['framed_balance_before_minus_after'],expected)
        for index in (7,9):
            s=self.r['stages'][index];before=s['local_before']
            wrong=before[:1]+before[2:]+before[1:2]
            self.assertNotEqual(exact_action(product(wrong),5),exact_action(product(s['local_after']),5))

    def test_positive_complement_and_existing_transported_pair_are_essential(self):
        w=self.r['stages'][9]['named_pattern_witness'];canonical=w['canonical']
        self.assertEqual(canonical[1].conjugator,(4,))
        wrong=(canonical[0],replace(canonical[1],conjugator=(-4,)),canonical[2])
        self.assertNotEqual(exact_action(product(wrong),5),exact_action(product(w['canonical_after']),5))
        self.assertEqual(w['existing_pair_match'][0]['actual'].id,'alternative.return.1')
        self.assertEqual(self.r['stages'][8]['adjacent_moves'],4)
        for m in w['internal_interchange_matches']:
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))
        self.assertEqual(exact_action(product(w['canonical_cabled_lantern']),5),exact_action(product(w['canonical_after']),5))

    def test_cyclic_start_is_explicit_inverse_prefix_conjugation(self):
        s=self.r['stages'][2];g=s['frame'];before=self.r['stages'][1]['factors']
        self.assertEqual(reduce_word(g+product(before)+inverse_word(g)),reduce_word(product(s['factors'])))
        self.assertTrue(s['exact_conjugation'])

    def test_exterior_is_visible_not_capped_and_endpoint_kernel_is_not_dropped(self):
        r=self.r;fs=r['factors']
        self.assertEqual(len(fs),17);self.assertEqual(sum(f.points==5 for f in fs),1)
        self.assertEqual(sum(f.points==3 for f in fs),7);self.assertEqual(sum(f.points==2 for f in fs),9)
        ext=next(f for f in fs if f.points==5)
        self.assertEqual(homology_action(ext.word),tuple(tuple(-int(i==j) for j in range(4)) for i in range(4)))
        self.assertEqual((r['sphere_moves'],r['exterior_caps']),(0,0))
        for k in r['endpoint_point_pushing']:
            self.assertEqual(exact_action(k['factor'].word,5),exact_action(k['split'].reconstructed_word,5))
        self.assertEqual(r['curve_intersections'],dict(maximum=70,total=1420,pairs=136))
        target=r['next_inner_root'];self.assertFalse(target['applied']);self.assertTrue(target['requires_transport'])
        for m in target['actual_pair_matches']:
            self.assertEqual(m['actual'].id,'return.inner24')
            self.assertEqual(exact_action(m['actual'].word,5),exact_action(m['pattern'].word,5))

    def test_saved_report_count_honesty_and_complete_proof_are_unchanged(self):
        r=self.r
        saved=json.loads((self.root/'docs/proofs/six-seven-outside-rose-return.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(json.dumps(r,default=asdict)),saved)
        self.assertEqual((r['source_working_operations'],r['working_prefix_operations']),(50,59))
        self.assertEqual(r['after_score'],dict(max_support_word=19,total_support_word=140,braid_letters=206))
        self.assertFalse(r['complete_shorter_derivation']);self.assertFalse(r['public_replay_changed'])
        c=json.loads((self.root/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
        self.assertEqual(c['named_full_route']['summary']['graphical_steps'],85)

    def test_wrong_chart_or_non_unit_source_is_rejected(self):
        fs=self.r['stages'][0]['factors']
        with self.assertRaises(ValueError):return_outside_rose(fs[:-1])
        index=next(i for i,f in enumerate(fs) if f.id=='outside.half.root')
        for replacement in (replace(fs[index],conjugator=(3,)),replace(fs[index],power=2),replace(fs[index],half=True)):
            with self.assertRaises(ValueError):return_outside_rose(fs[:index]+(replacement,)+fs[index+1:])
