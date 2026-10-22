"""Exact, positive arc eliminations and the separate framed-boundary lift."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import framed_outer_certificate
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.early_boundary_pure import purify_early_cluster, contract_pure_clusters


class EarlyPurificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        saved=json.loads((cls.folder/'certificate.json').read_text())
        cls.source=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator'])))
                         for f in saved['early_positive_cluster']['factors'])
        cls.route=purify_early_cluster(cls.source)

    def test_every_operation_and_adjacent_check_is_positive_disk_exact_and_bounded(self):
        r=self.route;expected=exact_action(BOUNDARY_WORD*4,5)
        self.assertEqual((r['graphical_steps'],r['adjacent_checks'],r['sphere_move_count']),(24,46,0))
        for state in r['stages']:
            for checked in (state,)+state.get('atomic_steps',()):
                fs=checked['factors']
                self.assertEqual(exact_action(product(fs),5),expected)
                self.assertTrue(all(getattr(f,'sign',1)==1 for f in fs))
                self.assertLessEqual(max(len(supported_class(f.mapping_class,5)) for f in fs),20)
                self.assertNotIn('sphere',checked['kind'])
                if 'disk_word_certificate' in checked:self.assertFalse(checked['disk_word_certificate']['discrepancy'])
            if 'local_before' in state:
                self.assertEqual(exact_action(product(state['local_before']),5),
                                 exact_action(product(state['local_after']),5))
        self.assertFalse(r['complete_named_derivation'])

    def test_chapters_remove_the_actual_matched_halves_in_order(self):
        r=self.route
        self.assertEqual({k:len(v)-1 for k,v in r['phases'].items()},dict(earlypair=7,earlydaisy=6,earlypure=11))
        self.assertEqual([r['stages'][i]['half_twists'] for i in (0,7,13,24)],[8,6,2,0])
        self.assertEqual({f.id for f in r['stages'][13]['factors'] if f.half},{'F6','F11'})
        self.assertTrue(all(not f.half for f in r['factors']))
        self.assertEqual(len(r['factors']),19)
        self.assertEqual(r['stages'][7]['score'],dict(max_support_word=12,total_support_word=104,braid_letters=208))
        self.assertEqual(r['after_score'],dict(max_support_word=17,total_support_word=152,braid_letters=196))
        for left,right in (('earlypair','earlydaisy'),('earlydaisy','earlypure')):
            self.assertEqual(r['phases'][left][-1]['factors'],r['phases'][right][0]['factors'])

    def test_cyclic_start_and_common_frame_are_explicit_and_use_the_central_disk_product(self):
        stages=self.route['stages']
        cyclic=[i for i,s in enumerate(stages) if s['kind']=='disk_cyclic_start']
        frames=[i for i,s in enumerate(stages) if s['kind']=='global_conjugation']
        self.assertEqual(len(cyclic),1);self.assertEqual(len(frames),1)
        i=cyclic[0];old=stages[i-1]['factors'];self.assertEqual(stages[i]['factors'],old[1:]+old[:1])
        i=frames[0];frame=stages[i]['frame'];self.assertEqual(frame,(3,4,4))
        for a,b in zip(stages[i-1]['factors'],stages[i]['factors']):
            self.assertEqual(a.id,b.id)
            self.assertEqual(exact_action(frame+a.word+inverse_word(frame),5),exact_action(b.word,5))

    def test_next_actual_daisy_petal_is_a_target_not_a_claimed_route(self):
        target=self.route['next_lantern']
        self.assertFalse(target['applied_to_replay']);self.assertTrue(target['requires_gathering'])
        self.assertEqual(exact_action(product(target['local_before']),5),
                         exact_action(product(target['local_after']),5))
        self.assertEqual(exact_action(target['daisy_terms'][-1].word,5),
                         exact_action(target['local_before'][-1].word,5))
        self.assertEqual(exact_action(product(target['daisy_terms']),5),
                         exact_action(target['source_root'].word,5))

    def test_positive_five_hole_relation_has_independently_checked_inner_framings(self):
        r=self.route;units=tuple(replace(f.mapping_class,power=1) for f in r['factors'] for _ in range(f.power))
        self.assertEqual(framed_outer_certificate(5,units,4),(6,5,7,7,5))
        self.assertEqual(r['framed_boundary']['inner_powers'],(6,5,7,7,5))
        # All pair counts can agree while the ordered product is wrong.
        bad=list(units);bad[0],bad[2]=bad[2],bad[0]
        with self.assertRaisesRegex(ValueError,'Exact capped braid action'):
            framed_outer_certificate(5,bad,4)
        with self.assertRaises(ValueError):purify_early_cluster(self.source[:-1])
        wrong=self.source[:8]+(replace(self.source[8],power=1),)+self.source[9:]
        with self.assertRaises(ValueError):purify_early_cluster(wrong)

    def test_two_pure_lanterns_have_a_bounded_exact_route_and_explicit_publication_scope(self):
        r=contract_pure_clusters(self.route['factors']);expected=exact_action(BOUNDARY_WORD*4,5)
        self.assertEqual((r['graphical_steps'],r['adjacent_checks'],r['first_contraction']),(12,15,6))
        self.assertFalse(r['applied_to_public_replay']);self.assertFalse(r['complete_named_derivation'])
        public=json.loads((self.folder/'certificate.json').read_text())['pure_cluster_contractions']
        self.assertTrue(public['applied_to_public_replay'])
        self.assertEqual(r['after_score'],dict(max_support_word=12,total_support_word=119,braid_letters=232))
        self.assertEqual(sum(s['kind']=='disk_cluster_lantern' for s in r['stages']),2)
        for stage in r['stages']:
            for s in (stage,)+stage.get('atomic_steps',()):
                self.assertEqual(exact_action(product(s['factors']),5),expected)
                self.assertTrue(all(not f.half for f in s['factors']))
                self.assertLessEqual(max(len(supported_class(f.mapping_class,5)) for f in s['factors']),20)
            if 'local_before' in stage:
                self.assertEqual(exact_action(product(stage['local_before']),5),
                                 exact_action(product(stage['local_after']),5))
        target=r['next_exterior_lantern']
        self.assertFalse(target['current_middle_already_matches']);self.assertFalse(target['applied_to_replay'])
        self.assertEqual(exact_action(product(target['local_before']),5),exact_action(product(target['local_after']),5))
        self.assertEqual(r['stages'][-1]['adjacent_moves'],5)
        self.assertEqual(r['stages'][6]['factors'][3],Factor('pure.O1234',(),1,4))
        with self.assertRaises(ValueError):contract_pure_clusters(self.source)

    def test_missing_middle_curve_page_is_an_exact_unapplied_target(self):
        import re
        html=(self.folder/'exterior-target.html').read_text(encoding='utf-8')
        self.assertIn('TARGET ONLY',html);self.assertIn('No sphere cap',html)
        data=json.loads(re.search(r'const targetData=(.*?);\nfor',html).group(1))
        columns=data['columns'];target=contract_pure_clusters(self.route['factors'])['next_exterior_lantern']
        self.assertEqual(exact_action(columns['present'][0]['word'],5),exact_action(target['actual_middle'].word,5))
        self.assertEqual(exact_action(columns['needed'][0]['word'],5),exact_action(target['local_before'][1].word,5))
        self.assertNotEqual(exact_action(columns['present'][0]['word'],5),exact_action(columns['needed'][0]['word'],5))
        self.assertEqual(exact_action(tuple(x for f in columns['left'] for x in f['word']),5),
                         exact_action(tuple(x for f in columns['right'] for x in f['word']),5))
        self.assertEqual(columns['right'][0]['id'],'outer.boundary')
        self.assertTrue(all(f['support'].startswith('<svg') for fs in columns.values() for f in fs))

    def test_published_chapters_preserve_disk_supports_and_do_not_slow_the_initial_payload(self):
        r=self.route;shown=json.loads((self.folder/'display-pure.json').read_text())
        phases=dict(r['phases'],earlycontracts=contract_pure_clusters(r['factors'])['stages'])
        self.assertEqual(set(shown['routes']),set(phases))
        for name,phase in phases.items():
            self.assertEqual(len(phase),len(shown['routes'][name]))
            for actual,display in zip(phase,shown['routes'][name]):
                self.assertEqual(display['kind'],actual['kind'])
                for f,j in zip(actual['factors'],display['factors']):
                    row=shown['rows'][j];self.assertFalse(row['sphere_rechart'])
                    self.assertEqual(exact_action(f.word),exact_action(row['word']))
        base=(self.folder/'display.json').read_bytes()
        self.assertEqual(len(base),943823)
        self.assertEqual(sha256(base).hexdigest()[:16],'05e6c888cf352a48')


if __name__=='__main__':unittest.main()
