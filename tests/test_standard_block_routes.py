"""Exact replay guards for standard-block untwisting."""
import unittest
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.standard_block_routes import standard_block_factors,standard_block_untwisting


class StandardBlockRoutesTests(unittest.TestCase):
    def test_all_fifteen_routes_replay_with_scope_checks(self):
        for name in ('T','W0','W1'):
            for generator in range(1,6):
                with self.subTest(block=name,generator=generator):
                    route=standard_block_untwisting(name,generator)
                    self.assertFalse(route['complete_structural_derivation_found'])
                    self.assertEqual(route['stages'][-1]['factors'],standard_block_factors(name))
                    self.assertEqual(reduce_word(route['source_word']),reduce_word((-generator,)+route['target_word']+(generator,)))
                    expected=homology_action(route['target_word'])
                    for stage in route['stages']:
                        self.assertEqual(homology_action(product(stage['factors'])),expected)
                        if stage['kind']=='disk_hurwitz':
                            self.assertEqual(abs(stage['source']-stage['target']),1)
                            self.assertFalse(reduce_word(product(stage['local_before'])+inverse_word(product(stage['local_after']))))
                            self.assertFalse(stage['disk_word_certificate']['discrepancy'])
                        elif stage['kind'] in ('sphere_rewrite','disk_rewrite'):
                            self.assertTrue(stage['sphere_certificate']['certified'])
                            self.assertEqual(homology_action(stage['disk_discrepancy']),IDENTITY)
                            self.assertEqual(exact_action(product(stage['local_before']))==exact_action(product(stage['local_after'])),stage['disk_equality'])
                    self.assertEqual(route['sphere_move_count'],int(name!='W1' and generator==1))
                    self.assertEqual(route['all_moves_exact_in_disk'],not route['sphere_move_count'])

    def test_the_ten_unit_block_is_not_mislabeled_identity_upstairs(self):
        route=standard_block_untwisting('T',1)
        self.assertEqual(route['product_lift_homology'],tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertNotEqual(route['product_lift_homology'],IDENTITY)

    def test_invalid_reference_requests_are_rejected(self):
        for generator in (True,0,6,-1,1.5):
            with self.assertRaises(ValueError):standard_block_untwisting('W0',generator)
        with self.assertRaises(ValueError):standard_block_factors('source-6-7')


if __name__=='__main__':unittest.main()
