import json,unittest
from pathlib import Path
from examples.build_half_neighborhood_comparison import comparison_data,panel

class HalfNeighborhoodComparisonTests(unittest.TestCase):
    def test_all_actual_half_matches_and_source_hashes_reproduce(self):
        early,late,r=comparison_data()
        saved=json.loads((Path(__file__).resolve().parents[1]/'docs/proofs/half-neighborhood-comparison/comparison.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads(json.dumps(r)),saved)
        self.assertEqual(len(r['actual_half_matches']),16)
        self.assertTrue(all(m['exact_B5_equal'] for m in r['actual_half_matches']))
        self.assertEqual(early[0]['factors'],late[0]['factors']);self.assertEqual(early[-1]['factors'],late[-1]['factors'])

    def test_pictured_routes_keep_every_actual_factor_and_two_half_arcs(self):
        import xml.etree.ElementTree as ET
        early,late,r=comparison_data();folder=Path(__file__).resolve().parents[1]/'docs/proofs/half-neighborhood-comparison'
        for i in r['pictured_stages']:
            for name,stages,title in [('early',early,'Early petals'),('late',late,'Delayed petals')]:
                svg=panel(stages[i],title);self.assertEqual((folder/(name+'-'+str(i)+'.svg')).read_text(encoding='utf-8'),svg)
                root=ET.fromstring(svg);groups=[g for g in root.iter() if g.get('data-factor')]
                self.assertEqual([g.get('data-factor') for g in groups],[f['id'] for f in stages[i]['factors']])
                self.assertEqual(sum(f['half'] for f in stages[i]['factors']),2)
                self.assertFalse(any(n.get('class')=='marked-point-label' for n in root.iter()))

if __name__=='__main__':unittest.main()
