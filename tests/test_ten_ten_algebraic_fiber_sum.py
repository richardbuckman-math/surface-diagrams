"""Verify the exact algebraic route and its committed certificate."""

import json
from pathlib import Path
import runpy
import unittest

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor


ROOT = Path(__file__).resolve().parents[1]


def records_to_words(records):
    return [
        (factor.id, factor.word)
        for factor in (
            Factor(**dict(record, conjugator=tuple(record["conjugator"])))
            for record in records
        )
    ]


class AlgebraicFiberSumTests(unittest.TestCase):
    def test_pinned_certificate_and_adjacent_identities(self):
        builder = runpy.run_path(str(ROOT / "examples/analyze_ten_ten_algebraic_fiber_sum.py"))
        data = (ROOT / builder["OUTPUT"]).read_bytes()
        self.assertEqual(builder["certificate_bytes"](ROOT), data)
        report = json.loads(data)
        current = records_to_words(report["all_twenty_source_factors"])
        count = 0
        for block in report["algebraic_blocks"]:
            self.assertEqual(current, records_to_words(block["input_factors"]))
            for source, target in block["formal_adjacent_indices"]:
                self.assertEqual(abs(source - target), 1)
                index = min(source, target)
                (a_id, a), (b_id, b) = current[index:index + 2]
                if source < target:
                    after = [(b_id, reduce_word(a + b + inverse_word(a))), (a_id, a)]
                else:
                    after = [(b_id, b), (a_id, reduce_word(inverse_word(b) + a + b))]
                self.assertEqual(reduce_word(a + b), reduce_word(after[0][1] + after[1][1]))
                current[index:index + 2] = after
                count += 1
            self.assertEqual(current, records_to_words(block["output_factors"]))
        self.assertEqual(count, 46)
        self.assertEqual(current, records_to_words(report["symbolic_endpoint"]))
        first, second = report["summands"]
        self.assertEqual(first["factors"], report["symbolic_endpoint"][3:10])
        self.assertEqual(second["factors"], report["symbolic_endpoint"][:3] + report["symbolic_endpoint"][10:])
        self.assertEqual([first["type"], second["type"]], [[4, 3], [6, 7]])
        self.assertTrue(all(summand["closure"]["sphere"]["certified"] for summand in (first, second)))
        self.assertEqual(report["source_diagram_moves_applied"], 0)
        self.assertFalse(report["bounded_diagram_route_proved"])
        self.assertEqual(report["rejected_diagram_prefix"][-1]["maximum"], 21)
