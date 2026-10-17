# Structural search for Richard's (6,7) derivation

October 17, 2026. **The complete factor-level derivation remains open.**
The existing 2,486-rewrite sphere proof establishes the identity but is not the
requested explanation by Hurwitz moves and named curve substitutions. The
earlier H34 consolidation also remains an intermediate step.

## A globally excluded shortcut, without a Hurwitz search

Two (4,3) factorizations have type (8,6). The familiar genus-two lantern
with its four boundary curves in two parallel nonseparating pairs changes
(8,6) to (6,7). This makes reversing one lantern and recognizing two smaller
blocks a natural hypothesis. It fails for the supplied factorization under
Hurwitz moves and simultaneous conjugation alone.

In coordinates `(a1,a2,b1,b2)`, the original nonseparating classes are:

| Factor | Class | Coordinates in the basis A=F2, B=F3 |
|---|---|---|
| F2 | (3,2,0,1) | (1,0) |
| F3 | (0,-1,1,0) | (0,1) |
| F6 | (3,5,-3,1) | (1,-3) |
| F7 | (3,4,-2,1) | (1,-2) |
| F9 | (-6,-7,3,-2) | (-2,3) |
| F11 | (3,3,-1,1) | (1,-1) |

Their signed algebraic intersection matrix is:

```text
       F2  F3  F6  F7  F9 F11
 F2     0   4 -12  -8  12  -4
 F3    -4   0  -4  -4   8  -4
 F6    12   4   0   4 -12   8
 F7     8   4  -4   0  -4   4
 F9   -12  -8  12   4   0  -4
 F11    4   4  -8  -4   4   0
```

**Reason.** Let d be the gcd of all pairings; here d=4. A Hurwitz move
replaces a vanishing class v by `v ± <v,u>u` and swaps the two positions.
For another class w, the change in `<v,w>` is
`± <v,u><u,w>`, divisible by d². The pairing of v with u does not change.
All seven separating twists act trivially on homology, so moves involving
them do not affect the classes. Track the original factor IDs and transport
orientations: every pairing is therefore invariant modulo 16 through any
number of Hurwitz moves. A changed orientation only negates a row and column;
zero/nonzero and the residue up to sign remain invariant. Simultaneous
conjugation preserves all pairings exactly.

Every off-diagonal entry above is nonzero modulo 16. Hence no two distinct
original nonseparating factors can ever become algebraically disjoint, or
equal, in this Hurwitz orbit. The two nonseparating interior curves of the
standard inverse lantern have algebraic intersection zero. Thus **no
Hurwitz-only rearrangement can expose that reverse lantern**. This excludes
one strategy globally, rather than only to a finite search depth. It does
not exclude chains, substitutions introducing new curves, different
geometric constructions, or a structural derivation of the relation.

The rank-two lattice and divisibility by four were already recorded in the
older homology tests. The new deduction is the modulo-16 ancestry obstruction
and its application to the reverse-lantern shortcut.

## A checked sphere lantern with the correct scope

Write `C=T123` (one ordinary three-point twist) and `H=H34`. On the sphere
with six marked points:

```text
H · (C H C^-1) · C² = T12 · T56.
```

Equivalently `(H C)²=T12 T56`. Its closed genus-two lift is precisely the
lantern just discussed: `T12` and `T56` lift to squares of two disjoint
nonseparating twists, while `C²` lifts to one separating twist. The two
interior nonseparating classes are `(1,1,0,0)` and `(-1,1,0,0)`, with zero
intersection.

`sphere_genus_two_lantern()` checks the complete sphere outer action and
the +I homology action of the discrepancy; together these exclude the
hyperelliptic involution. Its disk action is explicitly nontrivial. The
sphere certificate's common F5 whisker is `(1,2,3,4)`. The implementation
retains the disk discrepancy, rather than treating this as a puncture-capped
disk or framed-boundary lantern. Transport by a common conjugator is tested.

## The width-four rank-two monodromy

All six classes span the primitive lattice `L=<A,B>` with `<A,B>=4`.
On this lattice, a positive twist about `pA+qB` has matrix

```text
U(p,q) = [[1+4pq, -4p²], [4q², 1-4pq]].
```

The six matrices, in the order of the table, multiply exactly to I. Each
is congruent to I modulo 4, and consecutive primitive coefficient pairs,
including the last and first, have determinant ±1. They give a concrete
six-cusp, level-four pattern to investigate, rather than an arbitrary
six-twist problem. **This does not prove equality of the generated subgroup
with Gamma(4), nor an equivalence with Xiao's geometric factorization.**

The primitive orthogonal complement has basis
`E=(0,3,1,0)`, `F=(-1,2,0,1)` with `<E,F>=4`; every original factor fixes
E and F pointwise on homology. These provide further necessary constraints
when transporting curves through original factors. They do not establish
a covering map, sections, or the fundamental group of the total space.

## Reproduction and next steps

Run from the repository with its `src` on PYTHONPATH:

```text
python examples/analyze_six_seven_structure.py
python -m unittest tests.test_six_seven_structure tests.test_hyperelliptic_homology -q
```

The new tests check both Hurwitz directions, simultaneous conjugation, an
orientation-changing presentation of the same half twist, the full six
restricted matrices and fixed complement, and the sphere/disk/lift distinction.

1. **Prioritize a nonliftable intermediate or a relation introducing new
   cycles.** The modulo-16 obstruction explains why searching ever longer
   Hurwitz routes among the original six halves cannot expose the ordinary
   genus-two lantern. Do not repeat that search.
2. **Use the rank-two modular pattern to organize the separating correction.**
   Normalize the six parabolics in the displayed basis and investigate a
   geometric lift of their six-cusp relation. A homology identity is only a
   guide; all seven separating curve classes must still be accounted for.
3. **Compare geometric transports, not only endpoint partitions, with
   Szabó's degree-four model.** The older endpoint agreement is not a curve
   equality. The separating partitions need transport as the factor order is
   changed. The older five-of-seven multiset overlap does not rule out such
   moves.
4. **Investigate squared-lantern/Torelli factoring where its hypotheses hold.**
   Brendle–Margalit's factoring algorithm requires a symmetric
   nonseparating-curve stabilizer; homology I alone does not supply that.
   Check the stabilizer geometrically before applying it. The boundary catalog
   is useful only when an exact local relation matches the transported curves.

Sources for the comparison and possible methods:
[Szabó, Sections 6 and 8](https://arxiv.org/html/2609.34042v1),
[Brendle–Margalit, Factoring in the hyperelliptic Torelli group](https://www.maths.gla.ac.uk/~tbrendle/papers/factor.pdf).
The computations and obstruction above use the repository's exact supplied
factor records; they do not assume equivalence with either source.
