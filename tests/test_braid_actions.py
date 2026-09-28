import unittest
from surface_diagrams.braid_actions import (artin_action, reduce_word, inverse_word,
    hurwitz_move, action_checkpoints, conjugate_factors)
from surface_diagrams.braid_actions import arc_ray_word, loop_ray_word, free_homotopy_key
from surface_diagrams.braid_actions import act_on_loop_word
from surface_diagrams.braid_actions import substitute_factors
from surface_diagrams.braid_actions import audit_arc_transport
from surface_diagrams.braid_actions import arc_ray_segments
from surface_diagrams import Arc, Loop


class BraidActionTests(unittest.TestCase):
    def test_ray_segments_preserve_empty_steps_and_crossing_order(self):
        arc=Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down')
        segments=arc_ray_segments(6,arc)
        self.assertEqual(segments,((),(-4,-3),(),(2,3,4),(),(-5,-4,-3,-2),(),(3,4),(),(3,)))
        self.assertEqual(reduce_word(sum(segments,())),arc_ray_word(6,arc))
        reverse=Arc(4,1,tuple(reversed(arc.cuts)),direction='up')
        self.assertEqual(arc_ray_segments(6,reverse),
                         tuple(inverse_word(s) for s in reversed(segments)))
        self.assertEqual(arc_ray_segments(3,Arc(1,2)),((),))
        with self.assertRaises(ValueError): arc_ray_segments(3,Arc(0,2))

    def test_transport_audit_retains_boundary_base_path(self):
        arc=Arc(1,2)
        full_twist=(1,2)*3
        self.assertFalse(audit_arc_transport(3,full_twist,1,arc).matches)
        audit=audit_arc_transport(3,full_twist,1,arc,start_path=(1,2,3))
        self.assertTrue(audit.matches)
        self.assertEqual(audit.start_path,(1,2,3))
        self.assertNotEqual(audit.actual,((1,),(2,)))
        upper=audit_arc_transport(3,full_twist+(2,),1,Arc(1,3,direction='up'),
                                  start_path=(1,2,3))
        self.assertTrue(upper.matches)
        self.assertEqual(upper.transport,(2,))
        self.assertFalse(audit_arc_transport(3,full_twist,1,arc,start_path=(1,2)).matches)
        self.assertEqual(audit_arc_transport(3,(),1,arc,start_path=(3,-3)).start_path,())
        for path in ((4,-4),(0,),(True,)):
            with self.assertRaises(ValueError):
                audit_arc_transport(3,(),1,arc,start_path=path)

    def test_transport_audit_exposes_evidence_and_mismatches(self):
        upper=Arc(1,3,direction='up')
        audit=audit_arc_transport(3,(2,),1,upper)
        self.assertTrue(audit.matches)
        self.assertEqual(audit.transport,(2,))
        self.assertEqual(audit.actual,((1,),(2,3,-2)))
        self.assertEqual(audit.expected,audit.actual)
        wrong=audit_arc_transport(3,(-2,),1,upper)
        self.assertFalse(wrong.matches)
        self.assertEqual(wrong.actual,((1,),(3,)))
        self.assertEqual(wrong.expected,audit.expected)
        self.assertFalse(audit_arc_transport(3,(),1,Arc(2,3)).matches)
        self.assertTrue(audit_arc_transport(3,(),2,Arc(2,3)).matches)
        for index in (0,-1,3,True):
            with self.assertRaises(ValueError): audit_arc_transport(3,(),index,upper)
        with self.assertRaises(ValueError): audit_arc_transport(3,(3,),1,upper)

    def test_transport_audit_accepts_confirmed_factor_nine(self):
        arc=Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down')
        audit=audit_arc_transport(6,(-2,-3,4,2,-3,-2,-2),1,arc)
        self.assertTrue(audit.matches)
        self.assertEqual(audit.transport,(-4,-3,2,3,4,-5,-4,-3,-2,3,4,3))
        self.assertFalse(audit_arc_transport(6,(),1,arc).matches)

    def test_positive_conjugation_matches_nonempty_upper_transport(self):
        upper=arc_ray_word(3,Arc(1,3,direction='up'))
        self.assertEqual(upper,(2,))
        images=artin_action(3,(2,))
        self.assertEqual(images[0],(1,))
        self.assertEqual(images[1],reduce_word(upper+(3,)+inverse_word(upper)))
        # Same endpoint permutation does not determine the supported twist.
        above=artin_action(3,(2,1,-2))
        below=artin_action(3,(-2,1,2))
        self.assertNotEqual(above,below)

    def test_hurwitz_support_distinguishes_upper_and_lower_arc(self):
        moved=hurwitz_move(((1,),(2,)),0)
        self.assertEqual(moved,((2,),(-2,1,2)))
        images=artin_action(3,(-2,))
        self.assertEqual(images[0],(1,))
        lower=arc_ray_word(3,Arc(1,3,direction='down'))
        upper=arc_ray_word(3,Arc(1,3,direction='up'))
        self.assertEqual(images[1],reduce_word(lower+(3,)+inverse_word(lower)))
        self.assertNotEqual(images[1],reduce_word(upper+(3,)+inverse_word(upper)))

    def test_closed_path_key_matches_exhaustive_short_word_oracle(self):
        from itertools import product
        def oracle(word):
            word=reduce_word(word)
            while len(word)>1 and word[0]==-word[-1]:
                word=word[1:-1]
            if not word:
                return ()
            return min(w[i:]+w[:i] for w in (word,inverse_word(word))
                       for i in range(len(w)))
        for length in range(7):
            for word in product((-2,-1,1,2),repeat=length):
                self.assertEqual(free_homotopy_key(word),oracle(word),word)

    def test_closed_path_key_handles_long_periodic_and_nearly_periodic_words(self):
        periodic=(1,2)*25000
        self.assertEqual(free_homotopy_key(periodic),(-2,-1)*25000)
        almost=(1,)*50000+(2,)
        expected=(-2,)+(-1,)*50000
        self.assertEqual(free_homotopy_key(almost),expected)
        self.assertEqual(free_homotopy_key((3,)+almost+(-3,)),expected)

    def test_checked_substitution_splits_squared_three_point_twist(self):
        twist=(3,4)*3
        factors=((1,),twist*2,(-1,))
        result=substitute_factors(6,factors,1,2,(twist,twist))
        self.assertEqual(result,((1,),twist,twist,(-1,)))
        self.assertEqual(artin_action(6,sum(result,())),artin_action(6,sum(factors,())))
        self.assertEqual(substitute_factors(3,((1,2,1),),0,1,((2,1,2),)),((2,1,2),))
        self.assertEqual(substitute_factors(3,((1,),(-1,)),0,2,()),())

    def test_substitution_rejects_same_permutation_and_invalid_hidden_letters(self):
        with self.assertRaisesRegex(ValueError,'exact disk braid action'):
            substitute_factors(3,((1,1),),0,1,())
        with self.assertRaises(ValueError): substitute_factors(3,((1,),(4,-4)),0,1,((1,),))
        with self.assertRaises(ValueError): substitute_factors(3,((1,),),0,0,())
        with self.assertRaises(ValueError): substitute_factors(3,((1,),),True,1,())

    def test_boundary_twist_is_visible_based_but_not_on_closed_curve_class(self):
        original=loop_ray_word(3,Loop((0,2)))
        image=act_on_loop_word(3,(1,2)*3,original)
        self.assertNotEqual(image,original)
        self.assertEqual(free_homotopy_key(image),free_homotopy_key(original))
        self.assertEqual(act_on_loop_word(3,(1,-2),(-1,)),inverse_word(artin_action(3,(1,-2))[0]))
        with self.assertRaises(ValueError): act_on_loop_word(3,(),(4,))

    def test_loop_words_preserve_punctures_and_ignore_base_cut(self):
        loop=Loop((0,6,5,1))
        key=free_homotopy_key(loop_ray_word(6,loop))
        for shift in range(4):
            rotated=Loop(loop.cuts[shift:]+loop.cuts[:shift],start_up=shift%2==0)
            self.assertEqual(free_homotopy_key(loop_ray_word(6,rotated)),key)
        reversed_loop=Loop((0,1,5,6),start_up=False)
        self.assertEqual(loop_ray_word(6,reversed_loop),inverse_word(loop_ray_word(6,loop)))
        self.assertEqual(loop_ray_word(6,Loop((2,5))),(3,4,5))
        self.assertNotEqual(free_homotopy_key((1,2,3)),free_homotopy_key(()))
        with self.assertRaises(ValueError): loop_ray_word(5,loop)

    def test_closed_path_key_removes_conjugation_not_based_action(self):
        word=(1,2,-3)
        g=(3,2)
        self.assertEqual(free_homotopy_key(g+word+inverse_word(g)),free_homotopy_key(word))
        self.assertEqual(free_homotopy_key(inverse_word(word)),free_homotopy_key(word))
        self.assertNotEqual(free_homotopy_key((1,2)),free_homotopy_key((1,3)))

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
