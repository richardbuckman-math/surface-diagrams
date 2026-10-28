from dataclasses import asdict,replace
import json,unittest
from pathlib import Path
from examples.analyze_half_neighborhood_geometry import build_report,neighborhood_statistics
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.mapping_classes import VerificationLimitError,exact_action

class HalfNeighborhoodGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=build_report()

    def test_shared_endpoint_arcs_are_measured_only_as_closed_neighborhoods(self):
        a=Factor('H12',(),1,2,1,True);b=Factor('H23',(),2,2,1,True);certs={}
        r=neighborhood_statistics((a,b),certs)
        self.assertEqual((r['pair_sum'],r['pair_maximum'],r['half_pair_maximum']),(2,2,2))
        self.assertEqual(len(r['pairs']),1)
        self.assertTrue(all(not x['left'].half and not x['right'].half for x in certs.values()))

    def test_closed_pair_counts_are_common_chart_invariant_and_power_unweighted(self):
        fs=(Factor('H12',(),1,2,1,True),Factor('T23',(),2,2))
        a=neighborhood_statistics(fs,{})
        moved=tuple(replace(f,conjugator=(2,-1,3)+f.conjugator) for f in fs)
        self.assertEqual(a['pair_sum'],neighborhood_statistics(moved,{})['pair_sum'])
        self.assertEqual(a['pair_sum'],neighborhood_statistics((fs[0],replace(fs[1],power=4)),{})['pair_sum'])
        with self.assertRaises(ValueError):neighborhood_statistics((replace(fs[0],power=2),fs[1]),{})

    def test_exhaustion_is_not_reported_as_zero(self):
        with self.assertRaises(VerificationLimitError):
            neighborhood_statistics((Factor('H12',(),1,2,1,True),Factor('T23',(),2,2)),{},max_letters=1)

    def test_saved_report_and_literal_complete_join_reproduce(self):
        saved=json.loads((Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-half-neighborhood-geometry.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(json.dumps(self.report,default=asdict)),saved)
        r=self.report;late=r['late_daisy_stages']
        self.assertEqual(late[0]['factors'],r['late_daisy_complete_input'])
        self.assertEqual(late[-1]['factors'],r['late_daisy_complete_output'])
        self.assertTrue(r['literal_complete_joins']);self.assertFalse(r['applied_to_public_replay'])
        early=r['routes']['current_early'];late_metrics=r['routes']['late_daisy']
        self.assertEqual((early['moves'],late_metrics['moves']),(8,9))
        self.assertEqual((early['summary']['pair_sum_peak'],late_metrics['summary']['pair_sum_peak']),(252,208))
        for k in ('half_support_peak','half_pair_peak','pair_peak'):
            self.assertEqual(early['summary'][k],late_metrics['summary'][k])

    def test_actual_half_words_and_full_neighborhood_kernels_are_retained(self):
        for c in self.report['half_neighborhood_certificates']:
            h=c['actual_half'];n=c['closed_neighborhood'];split=c['closed_neighborhood_split']
            self.assertTrue(h.half);self.assertFalse(n.half)
            self.assertEqual(c['actual_half_word'],h.word)
            self.assertEqual(exact_action(h.word+h.word,5),exact_action(n.word,5))
            self.assertEqual(exact_action(n.word,5),exact_action(split.reconstructed_word,5))

if __name__=='__main__':unittest.main()
