import unittest
from surface_diagrams.braid_actions import (artin_action, reduce_word, inverse_word,
    hurwitz_move, action_checkpoints, conjugate_factors)
from surface_diagrams.braid_actions import arc_ray_word
from surface_diagrams import Arc


class BraidActionTests(unittest.TestCase):
    def test_confirmed_factor_nine_ray_word_matches_conjugated_meridians(self):
        arc=Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down')
        transport=arc_ray_word(6,arc)
        self.assertEqual(transport,(-4,-3,2,3,4,-5,-4,-3,-2,3,4,3))
        g=(-2,-3,4,2,-3,-2,-2)
        images=artin_action(6,g)
        self.assertEqual(images[0],(1,))
        self.assertEqual(images[1],reduce_word(transport+(4,)+inverse_word(transport)))
        reverse=Arc(4,1,tuple(reversed(arc.cuts)),direction='up')
        self.assertEqual(arc_ray_word(6,reverse),inverse_word(transport))

    def test_ray_word_side_and_direction(self):
        self.assertEqual(arc_ray_word(4,Arc(1,4,direction='up')),(2,3))
        self.assertEqual(arc_ray_word(4,Arc(1,4,direction='down')),())
        with self.assertRaises(ValueError): arc_ray_word(4,Arc(0,3))

    def test_checkpoints_retain_identity_and_empty_factors(self):
        factors=((1,-2),(),(2,-1))
        history=action_checkpoints(3,factors)
        self.assertEqual(len(history),4)
        for i,state in enumerate(history):
            self.assertEqual(state,artin_action(3,sum(factors[:i],())))
        self.assertEqual(history[1],history[2])
        self.assertEqual(history[0],history[-1])
        self.assertNotEqual(history[0],history[1])
        with self.assertRaises(ValueError): action_checkpoints(3,((3,),))

    def test_global_conjugation_changes_product_as_declared(self):
        factors=((1,),(-2,),())
        g=(2,1)
        changed=conjugate_factors(factors,g)
        expected=g+sum(factors,())+inverse_word(g)
        self.assertEqual(artin_action(3,sum(changed,())),artin_action(3,expected))
        self.assertNotEqual(artin_action(3,expected),artin_action(3,sum(factors,())))
        self.assertEqual(conjugate_factors(changed,inverse_word(g)),factors)
        self.assertEqual(changed[-1],())

    def test_relations_and_inverse(self):
        self.assertEqual(artin_action(3,(1,2,1)),artin_action(3,(2,1,2)))
        self.assertEqual(artin_action(4,(1,3)),artin_action(4,(3,1)))
        for word in ((1,-2,1,2),(-1,2,-1),()):
            self.assertEqual(artin_action(3,word+inverse_word(word)),((1,),(2,),(3,)))

    def test_full_twist_retains_disk_boundary_action(self):
        boundary=(1,2,3)
        expected=tuple(reduce_word(boundary+(i,)+inverse_word(boundary)) for i in range(1,4))
        self.assertEqual(artin_action(3,(1,2)*3),expected)
        self.assertNotEqual(expected,artin_action(3,()))

    def test_hurwitz_preserves_action_and_has_inverse(self):
        factors=((1,2,-1),(-2,),(),(1,))
        for index in range(3):
            for backward in (False,True):
                moved=hurwitz_move(factors,index,inverse=backward)
                self.assertEqual(artin_action(3,sum(factors,())),artin_action(3,sum(moved,())))
                restored=hurwitz_move(moved,index,inverse=not backward)
                self.assertEqual(restored,factors)

    def test_validation(self):
        for word in ((0,),(True,),(3,)):
            with self.assertRaises(ValueError): artin_action(3,word)
        with self.assertRaises(ValueError): hurwitz_move(((1,),),0)
        self.assertEqual(reduce_word((1,2,-2,-1)),())
