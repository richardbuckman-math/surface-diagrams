from dataclasses import asdict
from pathlib import Path
import hashlib,json,unittest
from surface_diagrams.clarity_derivation import factor_from_data,refine_sphere_moves,parallel_rounds,apply_edit,curve_class,word,PeripheralFactor
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.sphere_actions import sphere_chain_certificate

class ClarityDerivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
        cls.raw=json.loads((cls.folder/'certificate.json').read_text(encoding='utf-8'))
        def converted(s):
            t=dict(s)
            for k in ('factors','local_before','local_after'):
                if k in t:t[k]=tuple(factor_from_data(f) for f in t[k])
            return t
        cls.source=tuple(converted(s) for s in cls.raw['early_boundary']['stages'][:18])+tuple(converted(s) for s in cls.raw['named_full_route']['stages'][15:])
        cls.result=refine_sphere_moves(cls.source,cls.raw['early_boundary']['chart']['factor_certificates'])
        cls.stages=cls.result['stages'];cls.rounds=parallel_rounds(cls.stages)

    def test_disk_lantern_and_sphere_redraw_are_two_separate_moves(self):
        i=next(i for i,s in enumerate(self.stages) if s['kind']=='disk_lantern');disk=self.stages[i];redraw=self.stages[i+1]
        self.assertEqual(redraw['kind'],'sphere_redraw')
        self.assertEqual(exact_action(word(self.stages[i-1]),6),exact_action(word(disk),6))
        self.assertEqual(len(disk['individual_named_matches']),3)
        self.assertTrue(all(m['exact_disk_equal'] for m in disk['individual_named_matches']))
        self.assertEqual(disk['framed_balance_before_minus_after'],(0,1,0,0,1,0))
        self.assertEqual(disk['factors'][1].points,4);self.assertEqual(redraw['factors'][1].points,2)
        self.assertEqual(len(redraw['edit_before']),1);self.assertEqual(len(redraw['edit_after']),1)
        self.assertNotEqual(exact_action(word(disk),6),exact_action(word(redraw),6))
        self.assertEqual(redraw['factors'],self.source[14]['factors'])

    def test_every_sphere_move_only_redraws_the_same_factor_and_curve(self):
        for i,s in enumerate(self.stages[1:],1):
            if s['kind'] not in ('sphere_redraw','curve_redraw'):continue
            before=self.stages[i-1]
            self.assertEqual(len(before['factors']),len(s['factors']))
            self.assertEqual(tuple(f.id for f in before['factors']),tuple(f.id for f in s['factors']))
            if 'ledger_redraw' in s:
                a,b=before['ledger'],s['ledger'];self.assertEqual(before['factors'],s['factors'])
            else:
                self.assertEqual(len(s['edit_before']),1);self.assertEqual(len(s['edit_after']),1)
                a,b=s['edit_before'][0],s['edit_after'][0]
            self.assertEqual((a.id,a.power,a.half),(b.id,b.power,b.half))
            self.assertEqual(curve_class(a),curve_class(b))
            self.assertTrue(s['sphere_certificate']['certified']);self.assertEqual(s['lift_homology'],IDENTITY)
            self.assertNotIn('named_witness_ref',s)

    def test_framing_corrections_stay_in_a_separate_ledger(self):
        edits=[s for s in self.stages if s.get('source_index')==16 and s['family']=='redraw']
        self.assertEqual(len(edits),14);self.assertEqual(sum(s.get('framing_increment',0) for s in edits),6)
        self.assertEqual(edits[-1]['ledger'].power,6)
        self.assertTrue(all(len(s['factors'])==14 for s in edits))
        self.assertFalse(any(f.id=='boundary.corrections' for s in edits for f in s['factors']))
        negative=tuple(tuple(-x for x in r) for r in IDENTITY)
        self.assertTrue(any(s['uncorrected_curve_lift']==negative for s in edits))
        self.assertTrue(all(s['corrected_local_lift']==IDENTITY for s in edits))
        bad=[dict(c) for c in self.raw['early_boundary']['chart']['factor_certificates']]
        next(c for c in bad if c['boundary_power']==1)['boundary_power']=0
        with self.assertRaises(ValueError):refine_sphere_moves(self.source,bad)

    def test_peripheral_cleanup_is_after_its_own_redraw_and_is_disk_trivial(self):
        cleanup=[i for i,s in enumerate(self.stages) if s['kind']=='peripheral_cleanup']
        self.assertEqual(len(cleanup),2)
        for i in cleanup:
            self.assertEqual(self.stages[i-1]['kind'],'sphere_redraw')
            self.assertEqual(exact_action(word(self.stages[i-1]),6),exact_action(word(self.stages[i]),6))
            self.assertEqual(homology_action(word(self.stages[i-1])),IDENTITY)
        for bad in (1,3,True,2.0,-2):
            with self.assertRaises(ValueError):PeripheralFactor('bad',power=bad)
        self.assertEqual(PeripheralFactor('ok',power=6).word,())
        self.assertFalse(self.stages[-1]['factors']);self.assertIsNone(self.stages[-1]['ledger'])

    def test_parallel_rounds_have_disjoint_edits_and_literal_two_order_proofs(self):
        for r in self.rounds:
            if not r['simultaneous']:continue
            self.assertEqual(len(r['independence_witnesses']),r['move_count']*(r['move_count']-1)//2)
            self.assertTrue(all(w['literal_two_order_equality'] for w in r['independence_witnesses']))
            ops=[self.stages[c['move_index']] for c in r['cards']]
            touched=set()
            for op in ops:
                self.assertFalse(touched.intersection(op['touched_ids']));touched.update(op['touched_ids'])
            forward=r['before'];reverse=r['before']
            for op in ops:forward=apply_edit(forward,op)
            for op in reversed(ops):reverse=apply_edit(reverse,op)
            self.assertEqual(forward,reverse);self.assertEqual(forward,r['after'])
            self.assertEqual(word(forward),word(reverse))
        split=next(r for r in self.rounds if r['simultaneous'] and self.stages[r['first_move']]['kind']=='disk_split')
        self.assertEqual(split['move_count'],3)

    def test_all_parallel_move_panels_start_from_the_same_input(self):
        for r in self.rounds:
            for card in r['cards']:
                self.assertEqual(card['before'],r['before'])
                op=self.stages[card['move_index']]
                if r['simultaneous']:self.assertEqual(card['after'],apply_edit(r['before'],op))
                if op['family']=='redraw':
                    self.assertTrue(card['sphere_certificate']['certified']);self.assertEqual(card['lift_homology'],IDENTITY)

    def test_every_move_preserves_the_correct_disk_or_lifted_sphere_relation(self):
        for a,b in zip(self.stages,self.stages[1:]):
            if b['family']=='redraw':
                self.assertTrue(sphere_chain_certificate(reduce_word(word(a)+inverse_word(word(b))))['certified'])
                self.assertEqual(homology_action(word(a)),homology_action(word(b)))
            elif b['kind'] in ('global_conjugation','disk_cyclic_start'):
                g=tuple(b['frame']);self.assertEqual(exact_action(g+word(a)+inverse_word(g),6),exact_action(word(b),6))
            else:self.assertEqual(exact_action(word(a),6),exact_action(word(b),6))

    def test_the_preferred_longer_prefix_has_a_simpler_F2_arc_in_this_chart(self):
        d=json.loads((self.folder/'display-clear.json').read_text(encoding='utf-8'));s=d['summary'];g=s['geometry_preference']
        self.assertEqual((s['source_operations'],s['archived_source_operations']),(82,79))
        self.assertEqual((g['shorter79']['lengths']['F2'],g['clearer82']['lengths']['F2']),(12,4))
        self.assertEqual((g['shorter79']['total'],g['clearer82']['total']),(80,72))
        self.assertEqual((g['shorter79']['maximum'],g['clearer82']['maximum']),(30,30))
        self.assertFalse(s['mathematical_shortening_claimed'])

    def test_saved_certificates_and_display_metadata_reproduce(self):
        c=json.loads((self.folder/'clarity-certificate.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(json.dumps(self.stages,default=asdict)),c['stages'])
        self.assertEqual(json.loads(json.dumps(self.rounds,default=asdict)),c['parallel_rounds'])
        self.assertEqual((len(self.stages)-1,len(self.rounds),self.result['sphere_redraw_moves']),(98,69,13))
        self.assertEqual(c['summary']['source_sha256'],hashlib.sha256((self.folder/'certificate.json').read_bytes()).hexdigest())
        d=json.loads((self.folder/'display-clear.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['routes']['clearfull']),70)
        self.assertEqual(sum(len(s.get('parallel_moves',())) for s in d['routes']['clearfull']),98)
        self.assertEqual(self.raw['named_full_route']['summary']['graphical_steps'],79)
        self.assertTrue(all(not r['word'] for r in d['rows'] if r.get('peripheral')))

    def test_the_disk_lantern_retains_its_complete_point_pushing_data(self):
        s=next(s for s in self.stages if s['kind']=='disk_lantern')
        for item in s['complete_point_pushing']:
            self.assertEqual(exact_action(item['factor'].word,6),exact_action(item['split'].reconstructed_word,6))
        self.assertEqual(len(s['complete_point_pushing']),5)

if __name__=='__main__':unittest.main()
