import json
import unittest

from surface_diagrams.boundary_playground import BoundaryProject, import_project, new_project
from surface_diagrams.braid_actions import artin_action
from surface_diagrams.factorization_explorer import Factor


class BoundaryPlaygroundTests(unittest.TestCase):
    def test_three_point_half_lantern_hurwitz_walk(self):
        start = new_project(3)
        lantern = start.split(0, 'lantern')
        self.assertEqual([f.word for f in lantern.factors],
                         [(1, 1), (2, 1, 1, -2), (2, 2)])
        halves = lantern.split(0, 'halves')
        first_move = halves.move(1, 2)
        self.assertEqual([f.word for f in first_move.factors],
                         [(1,), (2, 2), (1,), (2, 2)])
        second_move = first_move.move(1, 2)
        result = second_move.combine(2)
        self.assertEqual([f.word for f in result.factors],
                         [(1,), (2, 2, 1, -2, -2), (2, 2, 2, 2)])
        self.assertTrue(result.factors[0].half)
        self.assertTrue(result.factors[1].half)
        self.assertEqual((result.factors[2].points, result.factors[2].power,
                          result.factors[2].half), (2, 2, False))
        for state in (start, lantern, halves, first_move, second_move, result):
            self.assertEqual(artin_action(3, state.word), artin_action(3, start.target_word))
        self.assertEqual(import_project(json.loads(json.dumps(result.to_dict()))), result)

    def test_five_point_square_split_and_combine(self):
        start = new_project(5, 2)
        self.assertEqual(start.target_word, (1, 2, 3, 4) * 10)
        split = start.split(0, 'powers')
        self.assertEqual([f.word for f in split.factors], [(1, 2, 3, 4) * 5] * 2)
        self.assertEqual(artin_action(5, split.word), artin_action(5, start.word))
        self.assertEqual([f.id for f in split.move(0, 1).factors], ['T.2', 'T.1'])
        self.assertEqual(split.combine(0).word, start.word)

    def test_checked_drag_is_reversible(self):
        start = new_project(3).split(0, 'lantern')
        moved = start.move(0, 2)
        self.assertEqual(moved.factors[-1], start.factors[0])
        self.assertEqual(artin_action(3, moved.word), artin_action(3, start.word))
        returned = moved.move(2, 0)
        self.assertEqual([f.id for f in returned.factors], [f.id for f in start.factors])
        for actual, original in zip(returned.factors, start.factors):
            self.assertEqual(artin_action(3, actual.word), artin_action(3, original.word))

    def test_import_rejects_changed_target_and_word(self):
        start = new_project(3)
        document = start.to_dict()
        altered = json.loads(json.dumps(document))
        altered['factors'][0]['word'][0] = 2
        with self.assertRaisesRegex(ValueError, 'word disagrees'):
            import_project(altered)
        altered = json.loads(json.dumps(document))
        altered['factors'] = [dict(id='other', conjugator=[], first=1,
                                   points=2, power=1, half=False, word=[1, 1])]
        with self.assertRaisesRegex(ValueError, 'does not equal'):
            import_project(altered)
        altered = json.loads(json.dumps(document))
        altered['format'] = 'surface-diagrams-factorization-v1'
        with self.assertRaisesRegex(ValueError, 'boundary playground'):
            import_project(altered)
        altered = json.loads(json.dumps(document))
        altered['factors'][0]['points'] = None
        with self.assertRaisesRegex(ValueError, 'support'):
            import_project(altered)
        altered = json.loads(json.dumps(document))
        altered['points'] = 6
        with self.assertRaisesRegex(ValueError, '3 or 5'):
            import_project(altered)

    def test_invalid_operation_never_changes_state(self):
        start = new_project(3)
        with self.assertRaises(ValueError):
            start.split(0, 'halves')
        with self.assertRaises(ValueError):
            start.move(0, 1)
        with self.assertRaises(ValueError):
            start.combine(0)
        with self.assertRaises(ValueError):
            BoundaryProject(3, 1, (Factor('wrong', (), 1, 2),))
        with self.assertRaises(ValueError):
            new_project(4)
        self.assertEqual(start, new_project(3))


if __name__ == '__main__':
    unittest.main()
