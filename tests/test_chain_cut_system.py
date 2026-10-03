import unittest

from surface_diagrams.based_cut_system import based_arc_ray_word
from surface_diagrams.braid_actions import free_homotopy_key, inverse_word, reduce_word, arc_ray_word
from surface_diagrams.chain_cut_system import (chain_arc, chain_arc_drawing,
                                               chain_arcs, chain_cut_system_drawing,
                                               chain_words)
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.visuals import RAINBOW


class ChainCutSystemTests(unittest.TestCase):
    def test_identity_is_boundary_to_first_then_adjacent_point_chain(self):
        words, endpoints = chain_words(tuple((i,) for i in range(1, 7)))
        self.assertEqual(endpoints, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)))
        self.assertEqual(words[1], (1, 2))
        arcs = chain_arcs(tuple((i,) for i in range(1, 7)))
        self.assertEqual(tuple((arc.start, arc.end) for arc in arcs), endpoints)
        self.assertTrue(all(not arc.cuts for arc in arcs))
        self.assertTrue(all(arc.is_straight(6) for arc in arcs))
        svg = chain_cut_system_drawing(tuple((i,) for i in range(1, 7)))
        self.assertIn('<svg', svg)
        for color in RAINBOW[:6]:
            self.assertIn(color, svg)

    def test_each_transported_edge_has_exact_two_point_boundary_class(self):
        factors = initial_factors()
        for prefix in range(13):
            images = exact_action(product(factors[:prefix]))
            words, endpoints = chain_words(images)
            arcs = chain_arcs(images)
            self.assertEqual(tuple((arc.start, arc.end) for arc in arcs), endpoints)
            first = based_arc_ray_word(arcs[0])
            self.assertEqual(reduce_word(first + (arcs[0].end,) + inverse_word(first)), words[0])
            for i in range(1, 6):
                arc = arcs[i]
                path = arc_ray_word(6, arc)
                boundary = (arc.start,) + path + (arc.end,) + inverse_word(path)
                self.assertEqual(free_homotopy_key(boundary), free_homotopy_key(words[i]))

    def test_one_late_edge_can_draw_when_other_edges_exceed_the_limit(self):
        images = exact_action(product(initial_factors()))
        with self.assertRaisesRegex(ValueError, '2048'):
            chain_arcs(images)
        self.assertEqual((chain_arc(images, 3).start, chain_arc(images, 3).end), (3, 4))
        self.assertIn(RAINBOW[3], chain_arc_drawing(images, index=3))

    def test_tenth_prefix_routes_the_chain_jointly(self):
        images = exact_action(product(initial_factors()[:10]))
        arcs = chain_arcs(images)
        nodes = sum(len(arc.cuts) + 2 for arc in arcs)
        self.assertGreater(nodes, 1024)
        self.assertLessEqual(nodes, 3072)
        svg = chain_cut_system_drawing(images)
        self.assertIn('<svg', svg)
        for color in RAINBOW[:6]:
            self.assertIn(color, svg)

    def test_rejects_non_meridians_and_wrong_edge(self):
        with self.assertRaises(ValueError):
            chain_words(((1,),))
        with self.assertRaises(ValueError):
            chain_words(((-1,), (2,), (3,), (4,), (5,), (6,)))
        with self.assertRaises(ValueError):
            chain_arc_drawing(tuple((i,) for i in range(1, 7)), index=6)
