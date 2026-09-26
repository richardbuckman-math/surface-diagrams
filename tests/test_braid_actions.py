import unittest
from surface_diagrams.braid_actions import artin_action, reduce_word, inverse_word, hurwitz_move


class BraidActionTests(unittest.TestCase):
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
