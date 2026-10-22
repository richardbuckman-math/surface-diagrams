"""Success-only memoization must preserve bounds, scope, and fresh outputs."""
import unittest
from unittest.mock import patch
from surface_diagrams import sphere_actions as sphere
from surface_diagrams.mapping_classes import VerificationLimitError


class SphereCertificateCacheTests(unittest.TestCase):
    def setUp(self):
        with sphere._sphere_chain_cache_lock: sphere._sphere_chain_cache.clear()

    def test_second_exact_check_uses_a_fresh_copy_of_the_success(self):
        word=(1,2,-2,-1)
        with patch.object(sphere,'sphere_curve_action',wraps=sphere.sphere_curve_action) as action:
            first=sphere.sphere_chain_certificate(word)
            self.assertEqual(action.call_count,10)
            first['certified']=False;first['scope']='modified caller output'
            again=sphere.sphere_chain_certificate(list(word))
            self.assertEqual(action.call_count,10)
        self.assertTrue(again['certified'])
        self.assertNotEqual(first['scope'],again['scope'])
        self.assertNotIn('lift_homology',again)

    def test_limits_and_strict_types_cannot_be_bypassed_by_a_cache_hit(self):
        word=(1,-1)
        self.assertTrue(sphere.sphere_chain_certificate(word,max_letters=40)['certified'])
        with self.assertRaises(VerificationLimitError):sphere.sphere_chain_certificate(word,max_letters=1)
        for invalid in (True,0,-1,1.0):
            with self.assertRaises(ValueError):sphere.sphere_chain_certificate(word,max_letters=invalid)
        for bad in ((True,-1),(1.0,-1),(6,-6)):
            with self.assertRaises(ValueError):sphere.sphere_chain_certificate(bad,max_letters=40)
        self.assertEqual(len(sphere._sphere_chain_cache),1)

    def test_failures_are_not_cached_and_capacity_is_bounded(self):
        self.assertFalse(sphere.sphere_chain_certificate((1,))['certified'])
        self.assertFalse(sphere._sphere_chain_cache)
        for n in range(1,132):self.assertTrue(sphere.sphere_chain_certificate((1,-1)*n)['certified'])
        self.assertEqual(len(sphere._sphere_chain_cache),sphere._SPHERE_CHAIN_CACHE_SIZE)
        self.assertNotIn(((1,-1),400000),sphere._sphere_chain_cache)
        self.assertIn(((1,-1)*131,400000),sphere._sphere_chain_cache)


if __name__=='__main__':unittest.main()
