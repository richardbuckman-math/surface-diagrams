"""Integrity of the published compact replay and its linked exact certificates."""
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import unittest
from xml.etree import ElementTree

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import initial_factors
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import ConjugatedTwist
from surface_diagrams.six_seven_structure import SignedResearchFactor
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.sphere_support_compact import reframe_factors
from surface_diagrams.twist_supports import support_curve

ROOT = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-compact'


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


class CompactReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.display = load('display.json')
        cls.certificates = load('support-certificates.json')['replacements']
        cls.source = load('source-route.json')

    def test_grouping_retains_every_move_and_every_sphere_step(self):
        d = self.display
        self.assertEqual(len(d['states']), len(d['atomic']) + 1)
        for groups in (d['groups'], d['chapters']):
            cursor = 0
            for group in groups:
                self.assertEqual(group['start'], cursor)
                self.assertGreater(group['end'], cursor)
                sphere = [i+1 for i in range(cursor, group['end']) if d['atomic'][i]['sphere']]
                self.assertEqual(group['sphere_steps'], sphere)
                cursor = group['end']
            self.assertEqual(cursor, len(d['atomic']))
        self.assertEqual(sum(m['sphere'] for m in d['atomic']), 14)
        self.assertFalse(d['summary']['complete_structural_derivation_found'])
        self.assertEqual(d['summary']['standard_block_bridge'], 'UNCOMPUTED')

    def test_each_displayed_factor_is_linked_to_its_actual_framed_source(self):
        phases = list(self.source)
        phases.remove('provenance')
        # Source JSON deliberately stores forward chronological phases.
        forward = []
        for phase in phases:
            stages = self.source[phase]['stages']
            forward.extend(s['factors'] for s in stages[bool(forward):])
        states = list(reversed(forward))
        self.assertEqual(len(states), len(self.display['states']))
        for records, shown in zip(states, self.display['states']):
            original = tuple(SignedResearchFactor(**r) for r in records)
            framed = reframe_factors(original, shown['frame'])['factors']
            self.assertEqual(len(framed), len(shown['factors']))
            for f, ri in zip(framed, shown['factors']):
                row = self.display['rows'][ri]
                cert = self.certificates[row['certificate']]
                self.assertEqual(cert['source'], json.loads(json.dumps(asdict(f.mapping_class))))
                displayed = SignedResearchFactor(**row['factor'])
                self.assertEqual(displayed.mapping_class, ConjugatedTwist(**cert['candidate']))
                self.assertEqual(displayed.sign, f.sign)
                self.assertEqual(displayed.id, f.id)
                self.assertEqual(row['sphere_rechart'], not cert['disk_equal'])
                self.assertLessEqual(row['cuts'], 40)
        self.assertEqual(self.display['states'][-1]['frame'], [])
        self.assertEqual(len(self.display['states'][-1]['factors']), 13)
        final = [SignedResearchFactor(**self.display['rows'][i]['factor'])
                 for i in self.display['states'][-1]['factors']]
        self.assertEqual([f.word for f in final], [f.word for f in initial_factors()])

    def test_every_replacement_has_a_fresh_sphere_and_lift_check(self):
        for cert in self.certificates:
            word = tuple(cert['disk_discrepancy'])
            source = ConjugatedTwist(**cert['source'])
            candidate = ConjugatedTwist(**cert['candidate'])
            self.assertEqual(word, reduce_word(source.word + inverse_word(candidate.word)))
            self.assertTrue(sphere_chain_certificate(word)['certified'])
            self.assertEqual(homology_action(word), IDENTITY)
            curve = support_curve(ConjugatedTwist(**cert['candidate']))
            self.assertEqual(cert['cuts'], len(curve.cuts))
            self.assertLessEqual(len(curve.cuts), cert['max_cuts'])

    def test_asset_chunks_are_complete_valid_svg_and_hash_matches_source(self):
        index = load('assets-index.json')
        for kind, count in index['counts'].items():
            images = []
            for start in range(0, count, index['chunk_size']):
                images.extend(load('assets/' + kind + '-' + str(start // index['chunk_size']) + '.json'))
            self.assertEqual(len(images), count)
            for svg in images:
                root = ElementTree.fromstring(svg)
                self.assertTrue(root.tag.endswith('svg'))
                self.assertIn('viewBox', root.attrib)
        digest = sha256((ROOT / 'source-route.json').read_bytes()).hexdigest()
        self.assertEqual(digest, self.display['summary']['source_sha256'])
        self.assertEqual(digest, load('frames.json')['source_sha256'])


if __name__ == '__main__':
    unittest.main()
