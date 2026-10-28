import json,unittest
from pathlib import Path
from dataclasses import asdict
from examples.analyze_fixed_half_gather import report
from surface_diagrams.mapping_classes import exact_action

class FixedHalfGatherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()
    def test_scoped_inverse_cuts_retain_free_words_and_nonabelian_obstruction(self):
        r=self.r;self.assertTrue(r['actual_half_equality']['equal']);self.assertFalse(r['block_half_commutation']['equal'])
        self.assertEqual(r['block_half_commutation']['first_difference']['meridian'],1)
        self.assertEqual(len(r['ordered_block']),6);self.assertEqual(len(r['inverse_gather_cuts']),7)
        self.assertTrue(all(not c['half_equality']['equal'] and not c['free_word_discrepancy'] and not c['applied'] for c in r['inverse_gather_cuts']))
        s=r['commutator_split'];self.assertEqual((len(s.kernel_loop),len(s.shadow_word)),(40,46))
        self.assertEqual(exact_action(r['full_commutator'],5),exact_action(s.reconstructed_word,5))
    def test_geometry_growth_and_rejected_complementary_crossing_are_exact(self):
        r=self.r;a,b=r['closed_matrix_before'],r['closed_matrix_after'];self.assertEqual((a['total'],b['total'],a['maximum'],b['maximum']),(512,1094,20,48))
        self.assertEqual(len(r['changed_pairs']),42);self.assertTrue(all(p['delta']>0 for p in r['changed_pairs']))
        inner={'F6','F11'}|{f.id for f in r['ordered_block']};before={p['ids']:p['number'] for p in a['pairs']}
        self.assertTrue(all(p['number']==before[p['ids']] for p in b['pairs'] if set(p['ids'])<=inner or not (set(p['ids'])&inner)))
        path=r['complementary_side'];self.assertEqual(len(path['retained_prefix']),6);self.assertEqual(path['rejected_candidate']['score']['maximum'],47);self.assertFalse(path['reached_matching_gather'])
        self.assertTrue(all(s['score']['maximum']<=20 for s in path['retained_prefix']))
    def test_unapplied_joint_donor_and_saved_source_pinned_report_reproduce(self):
        r=self.r;d=r['donor_target'];self.assertTrue(d['parent_match']['equal']);self.assertTrue(d['first_half_match']['equal']);self.assertTrue(d['actual_square_match']['equal'])
        self.assertFalse(d['root_actual_unit_matches']);self.assertFalse(d['second_half_existing_matches']);self.assertFalse(d['applied'])
        for split in d['full_daisy_splits']:self.assertEqual(exact_action(split.source_word,5),exact_action(split.reconstructed_word,5))
        saved=json.loads((Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fixed-half-gather.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(json.dumps(r,default=asdict)),saved);self.assertFalse(r['public_replay_changed'])

if __name__=='__main__':unittest.main()
