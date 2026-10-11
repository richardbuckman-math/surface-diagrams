"""Keep the small convention calibration tied to its exact braid action."""

from pathlib import Path
from tempfile import TemporaryDirectory
import runpy
import unittest
from xml.etree import ElementTree

from surface_diagrams.braid_actions import artin_action, inverse_word
from surface_diagrams.boundary_playground import new_project


class LanternHandednessExampleTests(unittest.TestCase):
    @staticmethod
    def _module():
        path = Path(__file__).resolve().parents[1] / 'examples' / 'lantern_handedness.py'
        return runpy.run_path(str(path))

    def test_three_point_lantern_and_inverse_have_opposite_first_arc_sides(self):
        example = self._module()
        target = new_project(3)
        lantern = target.split(0, 'lantern')
        self.assertEqual([f.word for f in lantern.factors],
                         [(1, 1), (2, 1, 1, -2), (2, 2)])
        self.assertEqual(artin_action(3, target.word), artin_action(3, lantern.word))
        self.assertNotEqual(artin_action(3, target.word),
                            artin_action(3, inverse_word(target.word)))
        first_arc = example['first_arc']
        self.assertEqual(first_arc(()).cuts, ())
        self.assertEqual(first_arc(target.word).cuts, (3,))
        self.assertEqual(first_arc(inverse_word(target.word)).cuts, (3,))
        self.assertTrue(first_arc(target.word).initial_up)
        self.assertFalse(first_arc(inverse_word(target.word)).initial_up)

    def test_every_lantern_prefix_has_the_expected_complete_chain(self):
        example = self._module()
        split = new_project(3).split(0, 'lantern')
        words = ((), split.factors[0].word,
                 split.factors[0].word + split.factors[1].word,
                 split.word, new_project(3).word)
        observed = [tuple((arc.start, arc.end, arc.cuts, arc.direction)
                          for arc in example['chain_arcs'](word)) for word in words]
        self.assertEqual(observed, [
            ((0, 1, (), 'default'), (1, 2, (), 'default'), (2, 3, (), 'default')),
            ((0, 1, (2,), 'up'), (1, 2, (), 'default'), (2, 3, (0,), 'up')),
            ((0, 1, (3,), 'up'), (1, 2, (3,), 'down'), (2, 3, (), 'default')),
            ((0, 1, (3,), 'up'), (1, 2, (), 'default'), (2, 3, (), 'default')),
            ((0, 1, (3,), 'up'), (1, 2, (), 'default'), (2, 3, (), 'default')),
        ])
        self.assertEqual(artin_action(3, words[3]), artin_action(3, words[4]))

    def test_generated_pictures_use_the_real_planar_arc_renderer(self):
        example = self._module()
        with TemporaryDirectory() as folder:
            sequences = example['build_demo'](folder)
            self.assertEqual(tuple(sequences), ('lantern-f0', 'lantern-f1',
                                               'lantern-f2', 'lantern-f3',
                                               'lantern-direct'))
            for slug, arcs in sequences.items():
                self.assertEqual(len(arcs), 3)
                svg = Path(folder, f'{slug}.svg').read_text(encoding='utf-8')
                root = ElementTree.fromstring(svg)
                ns = '{http://www.w3.org/2000/svg}'
                self.assertEqual(len(root.findall(f'{ns}circle')), 3)
                self.assertEqual(len(root.findall(f'{ns}text')), 6)
                # One renderer background plus three white point-label plates.
                self.assertEqual(len(root.findall(f'{ns}rect')), 4)
                paths = root.findall(f"{ns}path[@class='arc']")
                self.assertEqual(len(paths), 3)
                self.assertTrue(all('scale(1 -1)' in path.attrib['transform']
                                    for path in paths))
                self.assertIn('outer-boundary', svg)
            html = Path(folder, 'index.html').read_text(encoding='utf-8')
            self.assertIn('PC lantern relation', html)
            self.assertIn('PC = puncture-capped', html)
            self.assertIn("Richard's display orientation", html)
            self.assertIn('T₁₂₃ = T₁₂ T₁₃ T₂₃', html)
            self.assertIn('The display flip', html)


if __name__ == '__main__':
    unittest.main()
