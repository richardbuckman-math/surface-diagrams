import json,unittest
from pathlib import Path
from dataclasses import asdict,replace
from hashlib import sha256
import xml.etree.ElementTree as ET
from surface_diagrams.factorization_explorer import product
from surface_diagrams.braid_actions import reduce_word,inverse_word
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.sphere_actions import sphere_curve_action
from surface_diagrams.point_pushing import split_fixed_last_strand
from examples.analyze_ten_ten_short_target import report,SOURCE,PIN,OUTPUT
from examples.build_ten_ten_short_target import pictures,picture

ROOT=Path(__file__).resolve().parents[1]

class TenTenShortTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_source_pin_and_complete_report_reproduce(self):
        self.assertEqual(sha256((ROOT/SOURCE).read_bytes()).hexdigest(),PIN)
        self.assertEqual(json.loads(json.dumps(self.r,default=asdict)),json.loads((ROOT/OUTPUT).read_bytes()))

    def test_six_actual_records_and_the_explicit_missing_positive_half(self):
        r=self.r;by={f.id:f for f in r['source_factors']}
        self.assertEqual(r['source_positions'],tuple(zip(('four_three_B.1','four_three_B.2','four_three_B.3','four_three_B.4','four_three_C.5','four_three_C.6'),(3,4,5,6,18,19))))
        for f in r['six_literal_source_records']:self.assertEqual(f,by[f.id])
        h=r['missing_half'];g=(-5,)*4+(-2,)*2
        self.assertEqual(exact_action(h.word,6),exact_action(g+by['four_three_C.5'].word+inverse_word(g),6))
        self.assertTrue(h.half);self.assertEqual(h.power,1)
        self.assertEqual(supported_class(h.mapping_class,6),(-6,-5,-6,-5,-6,-5,-6,5,6,5,6,5,6,-3,-2,-3,2,3))
        self.assertTrue(all(homology_action(f.word)!=homology_action(h.word) for f in by.values() if f.half))
        self.assertFalse(r['source_ancestry_supplied']);self.assertEqual(r['current_half_homology_matches'],())

    def test_full_reference_hurwitz_replay_keeps_every_context_and_raw_word(self):
        r=self.r;states=r['chosen_internal_reference_states'];events=r['reference_previews'][2]['bounded_prefix_preview']
        self.assertEqual(len(states),5)
        self.assertEqual(tuple((x['raw_move']['source'],x['raw_move']['target']) for x in events),((4,5),(5,6),(4,5),(6,5)))
        self.assertEqual(tuple(x['raw_score']['maximum'] for x in events),(12,18,18,18))
        for before,e,after in zip(states,events,states[1:]):
            raw=e['raw_move'];a,b=sorted((raw['source'],raw['target']))
            self.assertEqual(before[:a],after[:a]);self.assertEqual(before[b+1:],after[b+1:])
            self.assertEqual(raw['local_before'],before[a:b+1]);self.assertEqual(raw['local_after'],after[a:b+1])
            x,y=before[a:b+1]
            expected=(replace(y,conjugator=reduce_word(x.word+y.conjugator)),x) if raw['source']<raw['target'] else (y,replace(x,conjugator=reduce_word(inverse_word(y.word)+x.conjugator)))
            self.assertEqual(after[a:b+1],expected)
            self.assertEqual(reduce_word(product(before)+inverse_word(product(after))),())
            self.assertEqual(raw['disk_word_certificate']['discrepancy'],())
            self.assertLessEqual(max(len(supported_class(f.mapping_class,6)) for f in after),e['preapplication_bound'])

    def test_every_individual_endpoint_match_and_complete_disk_sphere_lift_identity(self):
        r=self.r
        self.assertEqual(len(r['all_seven_individual_reference_matches']),7)
        for a,b in zip(r['target_factors'],r['chosen_internal_reference_states'][-1]):self.assertEqual(exact_action(a.word,6),exact_action(b.word,6))
        for c in r['reference_and_target_certificates']:
            w=product(c['factors']);self.assertEqual(exact_action(w,6),exact_action(r['reference_boundary'].word,6))
            self.assertEqual(homology_action(w),IDENTITY)
            s=c['sphere'];self.assertTrue(s['certified']);self.assertEqual(len(s['arc_pairs']),5)
            self.assertEqual(s['reference_classes'],s['image_classes'])
            self.assertEqual(c['full_disk_discrepancy'],reduce_word(w+inverse_word(r['reference_boundary'].word)))
        self.assertFalse(r['target_sphere_character']['nonidentity_sphere_proved'])
        self.assertEqual(len(r['target_sphere_character']['rectangle_characters']),30)

    def test_failed_reference_prefixes_are_rejected_before_application(self):
        direct,inverse,selected=self.r['reference_previews']
        self.assertEqual((len(direct['bounded_prefix_preview']),direct['failure']['raw_score']['maximum']),(0,22))
        self.assertEqual((len(inverse['bounded_prefix_preview']),inverse['failure']['raw_score']['maximum']),(1,106))
        for x in (direct,inverse):
            self.assertFalse(x['selected']);self.assertFalse(x['whole_preview_passed'])
            self.assertTrue(x['failure']['rejected_before_application']);self.assertFalse(x['source_twenty_applied'])
        self.assertTrue(selected['whole_preview_passed']);self.assertTrue(selected['selected'])

    def test_complete_nonabelian_kernels_and_shadows_and_inverse_embedding(self):
        r=self.r
        for q in r['full_product_point_pushing']:
            n=q['strands'];a=q['actual'];b=q['reference']
            split=split_fixed_last_strand(a['source_word'],n)
            self.assertEqual(split,a['split']);self.assertEqual(split.kernel_loop,b['split'].kernel_loop)
            self.assertEqual(len(split.kernel_loop),8);self.assertEqual(len(split.shadow_word),44)
            self.assertEqual(exact_action(split.reconstructed_word,n),exact_action(split.source_word,n))
            self.assertEqual(exact_action(split.shadow_word,n-1),exact_action(b['split'].shadow_word,n-1))
        inapplicable=0
        for q in r['every_actual_factor_stabilizer_or_full_action']:
            e=q['embedding'];self.assertTrue(all(abs(x)>=2 for x in e['B6_word']))
            self.assertEqual(e['B6_images'],((1,),)+tuple(tuple((1 if x>0 else -1)*(abs(x)+1) for x in row) for row in e['B5_images']))
            for k in ('full_B6_stabilizer_data','full_B5_stabilizer_data'):
                d=q[k]
                if not d['applicable']:
                    inapplicable+=1;self.assertNotIn('split',d)
                    self.assertEqual(d['full_faithful_images'],exact_action(d['source_word'],d['strands']))
                else:self.assertEqual(exact_action(d['split'].reconstructed_word,d['strands']),exact_action(d['source_word'],d['strands']))
        self.assertGreater(inapplicable,0)

    def test_nearby_zero_character_matrix_identity_is_still_sphere_nonidentity(self):
        r=self.r['nearby_unselected_target'];w=product(r['factors'])
        self.assertEqual(homology_action(w),IDENTITY)
        self.assertFalse(r['character']['nonidentity_sphere_proved'])
        e=r['full_sphere_nonidentity_witness']
        self.assertEqual(sphere_curve_action(w,e['pair'],max_letters=50000),e['full_image'])
        self.assertNotEqual(e['full_image'],e['reference_class']);self.assertEqual(len(e['full_image']),5834)
        i=r['first_differing_meridian']-1;self.assertNotEqual(r['B2_images'][i],r['C2_images'][i])

    def test_no_twenty_factor_equivalence_or_supply_is_claimed(self):
        r=self.r;self.assertTrue(r['standalone_target_relation_complete']);self.assertTrue(r['known_C_Hurwitz_equivalence_complete'])
        self.assertEqual(r['source_twenty_actual_moves'],0)
        for k in ('source_twenty_target_gathered','whole_twenty_modified_sphere_relation_assumed','source_twenty_reverse_equivalence_proved','preferred_proof_changed','adopted','source_ancestry_supplied'):self.assertFalse(r[k])

    def test_two_exact_panels_retain_uniform_unnumbered_six_point_grids(self):
        _,items=pictures()
        for name,title,stage in items:
            svg=picture(stage,title);self.assertEqual(svg,(ROOT/'docs/proofs/ten-ten-short-target'/(name+'.svg')).read_text(encoding='utf-8'))
            root=ET.fromstring(svg);self.assertEqual(root.get('data-records'),'7')
            self.assertNotIn('marked-point-label',svg)
            dots=[n for n in root.iter() if n.get('class')=='marked-point'];self.assertEqual(len(dots),42)
            for row in (n for n in root if n.get('data-factor')):
                v=next(n for n in row if n.tag.endswith('svg'))
                scale=float(v.get('width'))/float(v.get('viewBox').split()[2])
                marks=sorted((float(n.get('cx')),float(n.get('r'))) for n in v.iter() if n.get('class')=='marked-point')
                self.assertEqual(len(marks),6)
                for (x,r),(y,_) in zip(marks,marks[1:]):self.assertAlmostEqual((y-x)*scale,24);self.assertAlmostEqual(r*scale,1.68)

if __name__=='__main__':unittest.main()
