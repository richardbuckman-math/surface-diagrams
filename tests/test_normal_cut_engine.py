import unittest

from surface_diagrams import CertifiedCutSystem, calculate_cut_system
from surface_diagrams.chain_cut_system import chain_arcs
from surface_diagrams.curves import Arc
from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.normal_gluing import TerminalVisit
from surface_diagrams.normal_strands import NormalTriangleError


class NormalCutEngineTests(unittest.TestCase):
    @staticmethod
    def _chain(count):
        return chain_arcs(exact_action(product(initial_factors()[:count])))

    def test_f1_result_exposes_ordered_geometry_and_full_labeled_paths(self):
        arcs = self._chain(1)
        result = calculate_cut_system(arcs)
        self.assertIsInstance(result, CertifiedCutSystem)
        self.assertEqual(result.arcs, arcs)
        self.assertEqual(result.owners, (1, 2, 3, 4, 5, 6))
        self.assertEqual(result.points, 6)
        self.assertEqual(len(result.triangles), 14)
        self.assertEqual(tuple(triangle.triangle_id
                               for triangle in result.triangles[:4]),
                         (('upper', 0), ('lower', 0),
                          ('upper', 1), ('lower', 1)))
        self.assertEqual(tuple(path.owner for path in result.paths), result.owners)
        self.assertEqual(tuple(len(path.crossings) for path in result.paths),
                         (0, 0, 14, 0, 0, 14))
        self.assertEqual(sum(map(len, result.ray_orders.values())), 22)
        self.assertEqual(sum(map(len, result.cut_orders.values())), 6)
        self.assertEqual(result.ray_orders['upper', 3][0].owner, 6)
        self.assertEqual(result.cut_orders[2][0].owner, 6)
        with self.assertRaises(TypeError):
            result.cut_orders[2] = ()

        # A caller may supply selected owners when every omitted arc is a
        # straight chain edge. Owner labels still refer to the original arcs.
        selected = calculate_cut_system(arcs, owners=(6, 3))
        self.assertEqual(selected.owners, (6, 3))
        self.assertEqual(tuple(path.owner for path in selected.paths), (6, 3))
        self.assertEqual(selected.ray_orders, result.ray_orders)
        self.assertEqual(selected.cut_orders, result.cut_orders)

    def test_f11_result_certifies_every_exact_labeled_itinerary(self):
        result = calculate_cut_system(self._chain(11))
        self.assertEqual(len(result.triangles), 14)
        self.assertEqual(sum(map(len, result.ray_orders.values())), 10745)
        self.assertEqual(sum(map(len, result.cut_orders.values())), 4683)
        self.assertEqual(tuple(len(path.crossings) for path in result.paths),
                         (3439, 709, 5207, 291, 4392, 1390))
        for path in result.paths:
            connections = tuple(connection for connection in result.connections
                                if connection.owner == path.owner)
            self.assertEqual(path.start, connections[0].first)
            self.assertEqual(path.end, connections[-1].second)
            self.assertEqual(path.crossings, tuple(
                connection.second for connection in connections
                if not isinstance(connection.second, TerminalVisit)))

    def test_invalid_or_ambiguous_inputs_do_not_produce_certificate(self):
        with self.assertRaisesRegex(ValueError, 'points must be at least two'):
            calculate_cut_system((Arc(1, 2),), points=1)
        with self.assertRaisesRegex(ValueError, 'distinct one-based'):
            calculate_cut_system((Arc(1, 2),), owners=(1, 1))
        with self.assertRaisesRegex(NormalTriangleError, 'expected one or more'):
            calculate_cut_system(())
        with self.assertRaisesRegex(NormalTriangleError,
                                    'unresolved comparison'):
            calculate_cut_system((Arc(1, 3, direction='up'),) * 2)
        with self.assertRaisesRegex(NormalTriangleError,
                                    'omitted arc is not an edge-parallel'):
            calculate_cut_system(self._chain(1), owners=(3,))


if __name__ == '__main__':
    unittest.main()
