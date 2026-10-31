import json,unittest
from pathlib import Path
from hashlib import sha256
from dataclasses import replace
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action,_multiply,_twist
from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import product,Factor
from surface_diagrams.sphere_linking import sphere_linking_character
from surface_diagrams.ten_ten_homology_connection import homological_sum_connection
from surface_diagrams.ten_ten_summand_audit import pairing
from examples.analyze_ten_ten_homology_connection import report,encode,SOURCE,PIN,OUTPUT

ROOT=Path(__file__).resolve().parents[1]

def transpose(m):return tuple(zip(*m))
def vector(m,v):return tuple(sum(m[i][j]*v[j] for j in range(4)) for i in range(4))
def symplectic_inverse(m):
    j=((0,0,1,0),(0,0,0,1),(-1,0,0,0),(0,-1,0,0))
    return _multiply(_multiply(tuple(tuple(-x for x in row) for row in j),transpose(m)),j)
def word(records):
    p=IDENTITY
    for r in records:p=_multiply(p,r['matrix'])
    return p

class TenTenHomologyConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=report()

    def test_source_and_entire_certificate_are_reproducible(self):
        self.assertEqual(sha256((ROOT/SOURCE).read_bytes()).hexdigest(),PIN)
        self.assertEqual(json.loads(json.dumps(self.r,default=encode)),json.loads((ROOT/OUTPUT).read_bytes()))
        self.assertEqual(self.r['formal_matrix_adjacent_checks'],134)

    def test_every_formal_adjacent_move_retains_the_entire_matrix_context(self):
        states=self.r['matrix_states'];events=self.r['matrix_hurwitz_events']
        self.assertEqual(len(states),len(events)+1)
        self.assertEqual(tuple(r['matrix'] for r in states[0]),tuple(homology_action(f.word) for f in self.r['input_factors']))
        for before,event,after in zip(states,events,states[1:]):
            a,b=sorted((event['source'],event['target']))
            self.assertEqual(b,a+1);self.assertEqual(before[:a],after[:a]);self.assertEqual(before[b+1:],after[b+1:])
            self.assertEqual(before[a:b+1],event['local_before']);self.assertEqual(after[a:b+1],event['local_after'])
            x,y=before[a:b+1]
            if event['source']<event['target']:
                expected=(_multiply(_multiply(x['matrix'],y['matrix']),symplectic_inverse(x['matrix'])),x['matrix'])
            else:
                expected=(y['matrix'],_multiply(_multiply(symplectic_inverse(y['matrix']),x['matrix']),y['matrix']))
            self.assertEqual(tuple(r['matrix'] for r in after[a:b+1]),expected)
            self.assertEqual(tuple(r['id'] for r in after[a:b+1]),(y['id'],x['id']))
            self.assertEqual(word(before[a:b+1]),word(after[a:b+1]))
            self.assertEqual(len(after),20);self.assertEqual(word(after),IDENTITY)
            self.assertEqual(sorted(r['id'] for r in before),sorted(r['id'] for r in after))
            for r in after:self.assertEqual(r['matrix'],_twist(r['vector'],1) if r['half'] else IDENTITY)

    def test_two_identity_matrix_blocks_have_the_claimed_integral_lattices(self):
        s=self.r['selected_seven'];r=self.r['residual_thirteen']
        self.assertEqual((len(s),sum(x['half'] for x in s)),(7,4))
        self.assertEqual((len(r),sum(x['half'] for x in r)),(13,6))
        self.assertEqual(word(s),IDENTITY);self.assertEqual(word(r),IDENTITY)
        for k in ('selected_lattice','residual_lattice'):
            self.assertEqual(self.r[k],dict(lattice_rank=2,free_rank=2,torsion=()))
        self.assertEqual(pairing(*self.r['selected_to_original_four_three']['source_pair']),-3)
        self.assertEqual(pairing(*self.r['residual_to_original_six_seven']['source_pair']),4)

    def test_integral_global_maps_preserve_the_full_symplectic_form_and_match_every_factor(self):
        J=((0,0,1,0),(0,0,0,1),(-1,0,0,0),(0,-1,0,0))
        for name,state,target in (('selected_to_original_four_three','selected_normalized_matrices','target_four_three'),
                                  ('residual_to_original_six_seven','residual_normalized_matrices','target_six_seven')):
            q=self.r[name];m=q['matrix'];mi=q['inverse']
            self.assertTrue(all(int(x)==x for row in m for x in row))
            self.assertEqual(_multiply(m,mi),IDENTITY);self.assertEqual(_multiply(_multiply(transpose(m),J),m),J)
            for actual,expected in zip(self.r[state],self.r[target]):
                self.assertEqual(_multiply(_multiply(m,actual['matrix']),mi),homology_action(expected.word))
        self.assertEqual(tuple(x['matrix'] for x in self.r['after_global_conjugation']),self.r['target_twenty_matrices'])
        self.assertEqual(word(self.r['after_global_conjugation']),IDENTITY)

    def test_geometric_equivalence_and_torelli_information_are_never_claimed(self):
        self.assertEqual(self.r['applied_geometric_moves'],0)
        self.assertFalse(self.r['full_seven_factor_sphere_identity_proved'])
        self.assertFalse(self.r['full_residual_sphere_identity_proved'])
        self.assertFalse(self.r['fibration_equivalence_proved'])
        self.assertTrue(all(not e['geometric_move_applied'] for e in self.r['matrix_hurwitz_events']))
        with self.assertRaises(ValueError):homological_sum_connection(self.r['input_factors'][:-1])
        bad=list(self.r['input_factors']);bad[0]=replace(bad[0],power=1)
        with self.assertRaises(ValueError):homological_sum_connection(bad)

    def test_new_sphere_characters_resolve_the_particular_120_words_without_word_expansion(self):
        r=self.r['known_target_sphere_obstruction']
        self.assertEqual((r['test_count'],r['nonidentity_sphere_count'],r['unknown_count']),(120,120,0))
        self.assertEqual(r['applied_geometric_moves'],0);self.assertFalse(r['bounded_geometric_route'])
        for q in r['algebraic_reconstruction_of_known_unapplied_target']:
            self.assertEqual(q['disk_word_certificate']['discrepancy'],())
        for q in r['separating_triple_tests']:
            self.assertEqual(homology_action(product(q['factors'])),IDENTITY)
            c=q['sphere_character'];self.assertTrue(c['nonidentity_sphere_proved'])
            a,b,e,f=c['nonzero_character']['labels'];m=c['disk_linking']['linking_matrix']
            self.assertEqual(c['nonzero_character']['value'],m[a-1][b-1]+m[e-1][f-1]-m[a-1][e-1]-m[b-1][f-1])
            self.assertTrue(c['zero_is_inconclusive']);self.assertFalse(c['genus_two_lift_sign_claimed'])

    def test_sphere_character_kills_every_kernel_relation_and_detects_torelli_examples(self):
        sphere_relation=(1,2,3,4,5,5,4,3,2,1)
        full_twist=tuple(range(1,6))*6
        controls=[sphere_relation,full_twist,product(self.r['target_four_three']),product(self.r['target_six_seven'])]
        # Conjugation by arbitrary disk braids permutes the vertex-star
        # relations. The six examples include every possible vertex.
        for i in range(6):
            g=tuple(range(i,0,-1))
            controls.append(g+sphere_relation+inverse_word(g))
        for w in controls:
            c=sphere_linking_character(w);self.assertFalse(c['nonidentity_sphere_proved'])
            self.assertTrue(all(r['value']==0 for r in c['rectangle_characters']))
        sep=Factor('separating',(),1,3,power=2)
        self.assertEqual(homology_action(sep.word),IDENTITY)
        self.assertTrue(sphere_linking_character(sep.word)['nonidentity_sphere_proved'])
        with self.assertRaises(ValueError):sphere_linking_character((1,))
        with self.assertRaises(ValueError):sphere_linking_character((),3)

if __name__=='__main__':unittest.main()
