import unittest

from surface_diagrams.braid_actions import artin_action
from surface_diagrams.braid_schedule import commuting_layers, layered_braid_paths
from surface_diagrams.model import Style
from surface_diagrams.visuals import _braid_paths


class BraidScheduleTests(unittest.TestCase):
    def test_independent_crossings_share_one_layer(self):
        layers = commuting_layers(4, (1, -3))
        self.assertEqual(tuple(layer.letters for layer in layers), ((1, -3),))
        self.assertEqual(tuple(layer.positions for layer in layers), ((1, 2),))

        paths, order = layered_braid_paths(4, (layers[0].letters,), (24, 0),
                                          28, ('a', 'b', 'c', 'd'),
                                          Style(curve_width=1.3), 'smooth')
        self.assertEqual(len(paths), 4)
        self.assertEqual(order, (1, 0, 3, 2))
        # There is exactly one broken underpass for each of the two crossings.
        self.assertEqual(sum(sum(command[0] == 'M' for command in path.commands) == 2
                             for path in paths), 2)

    def test_layering_only_commutes_distant_generators(self):
        cases = (
            (5, (1, 2, 4, 3)),
            (6, (2, -4, 1, 3, -5, 2, 4)),
            (6, (1, 3, 5, -2, 4, -1)),
        )
        for strands, word in cases:
            with self.subTest(word=word):
                layers = commuting_layers(strands, word)
                self.assertEqual(sorted(position for layer in layers for position in layer.positions),
                                 list(range(1, len(word) + 1)))
                for layer in layers:
                    self.assertTrue(all(abs(abs(a) - abs(b)) > 1
                                        for i, a in enumerate(layer.letters)
                                        for b in layer.letters[i + 1:]))
                grouped_word = tuple(letter for layer in layers for letter in layer.letters)
                self.assertEqual(artin_action(strands, grouped_word), artin_action(strands, word))

    def test_single_crossing_layers_match_classic_renderer(self):
        style = Style(curve_width=1.3)
        word = (None, 1, -2, 1, None)
        for ys in ((120, 96, 72, 48, 24, 0), (0, 24, 48, 72, 96, 120)):
            for crossing_style in ('straight', 'smooth'):
                with self.subTest(ys=ys, crossing_style=crossing_style):
                    classic = _braid_paths(3, word, ys, 28, ('red', 'blue', 'green'),
                                           style, crossing_style)
                    compact = layered_braid_paths(3, (None if i is None else (i,) for i in word),
                                                  ys, 28, ('red', 'blue', 'green'),
                                                  style, crossing_style)
                    self.assertEqual(compact, classic)

    def test_invalid_parallel_crossings_are_rejected(self):
        style = Style(curve_width=1.3)
        with self.assertRaisesRegex(ValueError, 'disjoint'):
            layered_braid_paths(4, ((1, 2),), (24, 0), 28,
                                ('red',), style)
        with self.assertRaisesRegex(ValueError, 'disjoint'):
            layered_braid_paths(4, ((1, -1),), (24, 0), 28,
                                ('red',), style)
        with self.assertRaisesRegex(ValueError, 'smaller'):
            commuting_layers(4, (4,))


if __name__ == '__main__':
    unittest.main()
