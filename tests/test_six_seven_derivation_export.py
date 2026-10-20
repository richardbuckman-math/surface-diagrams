"""Lossless route selection and scope guards for the graphical PDF exporter."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    'six_seven_derivation_export',
    Path(__file__).resolve().parents[1] / 'examples/build_six_seven_derivation_pdf.py')
export = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(export)


def half(name, first):
    return dict(id=name, conjugator=[], first=first, points=2, power=1, half=True)


class ReverseDerivationExportTests(unittest.TestCase):
    def report(self, move=None):
        initial = [half('a', 1), half('b', 3)]
        moved = list(reversed(initial))
        report = {}
        for i, (key, _, _) in enumerate(export.PHASES):
            before = initial if i == 0 else moved
            # The real report also crosses from unsigned to explicit +1 records.
            before = [{**r, 'sign': 1} for r in before] if i else before
            stages = [dict(kind='start', title='shared endpoint', factors=before)]
            if i == 0:
                stages.append(dict(kind='disk_hurwitz', title='commute a and b',
                                   factors=moved, **(move or {})))
            report[key] = dict(stages=stages)
        report['tail_cluster_lantern'] = dict(stages=[dict(factors=[half('wrong branch', 5)])])
        return report

    def test_only_connected_successful_branch_is_reversed(self):
        report = self.report()
        steps = export.reverse_route(report)
        self.assertEqual(len(steps), 1)
        self.assertEqual([r['id'] for r in steps[0]['before']], ['b', 'a'])
        self.assertEqual([r['id'] for r in steps[0]['after']], ['a', 'b'])
        self.assertFalse(steps[0]['sphere'])
        report[export.PHASES[3][0]]['stages'][0]['factors'][0]['first'] = 5
        with self.assertRaisesRegex(ValueError, 'Disconnected'):
            export.reverse_route(report)

    def test_sphere_move_requires_both_certificates_and_inverts_discrepancy(self):
        report = self.report(dict(disk_discrepancy=[1, -2, 3]))
        applied = report['route']['stages'][1]
        applied['kind'] = 'sphere_rewrite'
        with self.assertRaisesRegex(ValueError, 'sphere certificate'):
            export.reverse_route(report)
        applied['sphere_certificate'] = dict(certified=True)
        with self.assertRaisesRegex(ValueError, 'lift check'):
            export.reverse_route(report)
        applied['lift_homology'] = deepcopy(export.IDENTITY4)
        step = export.reverse_route(report)[0]
        self.assertTrue(step['sphere'])
        self.assertEqual(step['reverse_disk_discrepancy'], [-3, 2, -1])
        self.assertIn('SPHERE MOVE', export.certificate_scope(step))

    def test_changed_interval_reconstructs_insertions_deletions_and_replacements(self):
        a, b, c, d = [half(x, i) for i, x in enumerate('abcd', 1)]
        for before, after in [([a,b,c], [a,d,c]), ([a,b,c], [a,c]),
                              ([a,c], [a,b,c]), ([a,b], []), ([], [a,b]),
                              ([a,b], [b,a]), ([a], [{**a, 'sign':1}])]:
            p, e1, e2 = export.changed_interval(before, after)
            recovered = before[:p] + after[p:e2] + before[e1:]
            self.assertEqual(list(map(export.normalized, recovered)),
                             list(map(export.normalized, after)))

    def test_artin_exponent_counts_crossings_not_generator_indices(self):
        self.assertEqual(export.artin_exponent([5, 4, -1]), 1)
        self.assertEqual(export.artin_exponent([1, 1, -5, -4]), 0)


if __name__ == '__main__':
    unittest.main()
