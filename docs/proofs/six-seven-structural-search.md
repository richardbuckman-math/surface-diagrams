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

## Two separating roots give an exact transport of original half twists

Write `C10=(sigma2^-1 sigma3^-1) T456 (sigma3 sigma2)` and
`C13=sigma5^-1 T345 sigma5`, so that their squares
are the original separating factors F10 and F13. A new exact geometric
identity is

```text
(C10 C13) F3 (C10 C13)^-1 = F9
```

on the six-marked sphere and in the closed genus-two lift. Here F3 and F9
are the **original supplied half twists**, both with endpoints `{1,4}`.
This was checked by equality of their complete sphere curve classes,
then independently by the sphere outer action of the half-twist discrepancy
and its +I homology action. The disk discrepancy is nontrivial and is retained
by `sphere_root_half_transport()`; this is not a disk braid equality.
Reversing the order of C10 and C13 fails the geometric class check.

This gives a concrete seventeen-state route:

1. Split F10 and F13 into their two ordinary three-point roots.
2. Move F10.1 up past F9, then move F13.1 up to immediately before that
   transported F9. Each adjacent Hurwitz step is checked in the disk.
3. The altered F9 is now `(C10 C13)^-1 F9 (C10 C13)`, hence is F3 on the
   sphere. Rechart it as the original F3 record. The exact common F5 whisker
   for this local sphere discrepancy is `(1,1,2,3,-4,-3,-2,-1)`; its disk
   action is nonidentity, and its closed genus-two lift is identity.
4. Move that unchanged half twist upward to the original F3 and combine
   them into one ordinary pair twist. These remaining steps preserve the
   new full disk product exactly.

The endpoint has fourteen **mixed** factors, with four ordinary three-point
roots still present. It is not a complete derivation or a shorter (n,s)
positive Lefschetz factorization. Splitting the separating factors into
roots leaves the hypotheses of the earlier modulo-16 obstruction, so this
transport does not contradict it.

Run `python examples/build_six_seven_root_research.py` for the local graphical
route at `.preview/six-seven-root-transport/index.html`, the complete saved
records and discrepancies in `certificate.json`, and 28 distinct checked
individual support pictures. All seventeen states are drawn, with the one
sphere-only step marked purple. These are individual disk-chart supports,
not a joint cut-system certificate or an importable disk-only lab session.

The original roots supplied forty homology-compatible signed two-root
transport cases. Only the displayed transport and its inverse matched exact
sphere classes. In the resulting fourteen-factor state, twenty further
homology-compatible one/two-root cases among the remaining halves produced
no exact class match. These finite tests do not rule out longer transports
or substitutions introducing other curves.

## A named cluster lantern explains that transport

The two roots above fit an exact **PC lantern with clusters of sizes 2,2,1**.
Set

```text
Q = T2345,
O = T23456,
P25 = (sigma2^-1 sigma3^-1) T45 (sigma3 sigma2),
P34 = T34.
```

Then

```text
C10 C13 Q = O P25 P34                        (exact in the marked disk).
```

The inner clusters are `{2,5}`, `{3,4}`, and `{6}`. The common chart transport
is `(sigma2^-1 sigma3^-1)`: it carries the standard inner pair clusters
`{4,5}` and `{2,3}` to the two routed pairs above. The exact left supports
are `{2,5,6}`, `{3,4,6}`, `{2,3,4,5}`. All four twists O, P25, P34, Q commute
pairwise, checked by their complete disk actions. If point 6 is restored to
a framed inner boundary, the genuine boundary lantern includes T6 on the
right; the multiplicity difference at every other point is zero.

This identifies the **simpler disk conjugator**

```text
R = P25 P34 Q^-1,
R F3 R^-1 = F9                              (exact in B6).
```

Thus the earlier sphere-only transport by C10 C13 has a named local
explanation and an exact disk representative involving one inverse twist.
The local lantern and both arc pictures are now drawn above the seventeen
columns in the research snapshot. The seventeen-column route itself still
contains its explicitly marked sphere step; it has not been silently changed
into a disk-only session.

**Lift sign matters.** O acts trivially on the marked sphere but its genus-two
lift has homology -I, the hyperelliptic involution. Dropping O from the unsquared
lantern would therefore give the wrong closed-genus-two equality. Squaring
avoids that error:

```text
(C10 C13)^2 Q^2 = O^2 P25^2 P34^2            (exact in B6),
(C10 C13)^2 Q^2 =     P25^2 P34^2            (sphere and closed genus two).
```

The disk discrepancy in the second line is exactly O²; its sphere whisker is
`(-1,-1)` and its lift homology is +I. `root_pair_lantern()` retains these
separate certificates. This is a usable transported squared-lantern relation,
**not yet a substitution applied to all thirteen original factors**. In the
saved endpoint, the four ordinary roots have different transported classes;
they cannot simply be declared to be `(C10 C13)^2`.

There are nevertheless **two separately transported copies** of C10 C13
available. In the seventeen-state endpoint, the exact individual root classes
are

```text
F10.1, F13.1 = H3^-1 (C10, C13) H3,
F10.2, F13.2 = C13^-1 (C10, C13) C13.
```

These equalities are checked in B6 factor by factor, not inferred from the
products. Moving F13.2 upward across F12 and F11 (two disk Hurwitz moves)
puts the four roots consecutively in rows 9–12. Each adjacent pair can then
use its own transported **unsquared** cluster lantern. That would introduce
two inverse Q twists; it requires signed factor records and has not yet been
performed in the saved positive-factor route.

The two transported O twists may only be omitted as a **paired** sphere/lift
step, with their full disk discrepancy retained: each separately lifts to the
deck involution. The complementary pairs of the two inverse Q supports are
`{4,6}` and `{1,6}`. Together with the existing positive `{1,4}` pair twist,
these suggest a specific signed PC-lantern configuration to check next.
The endpoint sets alone do not prove that the three routed curves form it.

## Applying both transported cluster lanterns

`root_cluster_lantern_route()` now implements the prepared continuation.
Its eight states start at the previous fourteen-factor endpoint, make the
two indicated disk Hurwitz moves, and apply each pair's **own** transported
PC lantern. Each replacement is checked against the complete ordered B6
action, locally and in the full product. It introduces two inverse Q twists.
`SignedResearchFactor` retains a positive support for the existing shared
Arc/Loop drawing code while its braid word includes the sign. These records
are a research format, not positive-factor lab workspaces.

Both transported five-point O factors are omitted in **one** sphere step.
The full disk discrepancy has 376 reduced letters; its complete sphere outer
action is identity and its lift homology is +I. Each separate O has lift -I.
Their individual omission would therefore give an incorrect genus-two
identity, even though it is legal on the marked sphere. The certificate
retains the two actual transported peripheral factors and the full discrepancy.

For a clearer picture, set

```text
P16 = (sigma1 sigma2 sigma3 sigma4) T56
      (sigma4^-1 sigma3^-1 sigma2^-1 sigma1^-1).
```

Its curve is exactly the sphere complement of Q2345, checked by the F5 curve
class rather than the endpoints alone. Replacing each transported Q^-1 with
its transported P16^-1 is legal both on the sphere and in closed genus two.
Each step has its own nontrivial disk discrepancy (32 and 38 reduced letters)
and +I lift certificate. The final sixteen-factor state consists of five
squared three-point twists, four half twists, five positive pair twists, and
two negative pair twists. It is **not** a new positive Lefschetz factorization
or a completed derivation of (6,7).

The natural next endpoint triangle fails a substantive check. For the positive
pair F3+F9 and the two complementary negative pair supports, orient the lifted
arc classes as

```text
v14 = (0,-1, 1,0),
v46 = (0, 1,-2,1),
v16 = (2, 2,-1,1).

Intersection matrix = [[0,-1,-3], [1,0,3], [3,-3,0]].
```

A common chart of the three pair curves in a pointed PC lantern would have
all three absolute algebraic intersections equal to one upstairs. Two are
three here, so **these actual routed classes do not form that lantern**.
Endpoint sets `{1,4}`, `{4,6}`, `{1,6}` alone had suggested it incorrectly.
The same continuation also admits no immediate positive/negative pair
cancellation from transporting either negative across its intervening block
to one of the five positive pair twists (ten exact sphere curve checks).
This is only a finite failure of those specific arrangements, not an
obstruction to a different derivation.

The graphical builder now draws both routes: seventeen earlier states and
eight continuation states, with 44 distinct support SVGs and no unavailable
support pictures. Red rows explicitly mark inverse twists; purple columns
mark sphere-only moves. The saved JSON includes all signed records, local
substitutions, and disk/sphere/lift certificates. The pictures are still
individual supports, not certified joint cut complexes. The complete
structural derivation remains open.

## A second original pair: an exact three-root disk transport

The supplied roots give another geometric identity:

```text
(C8 C10 C1) F2 (C8 C10 C1)^-1 = F7            (exact in B6).
```

This is separate from the old H34 consolidation and the F3/F9 two-root route.
After C1 acts on F2, its arc has the simple exact representative
`D = (-3,-5) H45 (5,3)`. Then C8 C10 transports D to original F7.
`three_root_half_transport()` retains both disk checks and the sphere/lift
checks. A second transport C10 C12 C1 works on the sphere but not in B6;
it is explained by the complementary-root relation below, not assumed equal
as a disk word.

Only five ordered positive three-root configurations passed the homology
filter for the two remaining original endpoint pairs: for F2/F7,
`(8,10,1)` and `(10,12,1)`; for F6/F11, `(12,1,4)`, `(12,5,4)`,
`(12,8,4)`. Testing their eight sign choices found just the two F2/F7
matches, both with positive signs. These are finite filtered configurations,
not a nonexistence claim for other transports.

One small symmetry family also failed before exact geometric testing: the
standard six-point rotation squared, corrected on the left by zero through
three original separating roots, never had the simultaneous homology images
F2-to-F6 and F3-to-F7. This excludes only that finite correction family,
not a different order-three symmetry or equivalence with Xiao's model.

The eighteen-state replay `three_root_transport_consolidation()` applies
the first transport to the actual ordered factorization. C1 begins before
F2, so split F1 and move its second root down across F2 first. Extract one
root each from F8 and F10 before F7. The altered F7 is now exactly D, with
conjugator `(-5,-3)` versus D's `(-3,-5)`; these commute in B6. Rechart it
by that disk equality, move it next to D, and combine the halves. Every
whole state has the original complete B6 action. The fifteen-record endpoint
has six ordinary three-point roots; it is not a Lefschetz factorization.

## A named inverse sphere lantern is now exposed

The first three endpoint records are C1, D², and D^-1 C1 D. Their product is
exactly `(C1 D)^2`. The common chart

```text
k = (-3,4) (1,2,3,4,5)^2
```

carries the standard T123 and H34 to C1 and D, respectively, checked in B6.
`three_root_prefix_lantern()` applies the sphere genus-two lantern to replace
this prefix by two positive pair twists, with endpoint pairs {4,5} and {1,2}.
The local sphere outer action and +I lift are checked and its nontrivial disk
discrepancy is saved. This is an actual application of a named relation to
the supplied factorization, not merely a homology analogy. Four odd ordinary
roots remain later in the fourteen-record word; it is not an (8,6)
Lefschetz factorization.

F9 and F11 at the earlier fifteen-record endpoint have algebraic intersection
zero. Nevertheless F9 moves the exact sphere support class of F11. They are
not geometrically disjoint, so that apparent second inverse-lantern shortcut
fails. The moved-curve witness is retained in the replay certificate.

## One cluster lantern and a PC half lantern remove the temporary inverse

There is another exact cluster lantern, with inner clusters {3,4}, {2,6}, {5}:

```text
Q2346 = (-2,-3,-5) T2345 (5,3,2),
P34   = (-2,-3,4) T23 (-4,3,2),
P26   = (-2,-3,4) T56 (-4,3,2),
O     = T23456,

C8 C10 Q2346 = O P34 P26                     (exact in B6).
```

Restoring the capped point 5 as a framed boundary adds T5 on the right.
The original C8 and C12 also satisfy

```text
C10^-1 C8 C10 = C12                          (sphere only; lift discrepancy -I),
(C10^-1 C8 C10)^2 = C12^2                    (sphere and closed genus two).
```

The first equality is an exact sphere curve rechart, with a nontrivial disk
discrepancy. Its minus sign must not be discarded in an unsquared lift.
`f2_f7_cluster_lantern()` retains these separate certificates.

The twenty-state `three_root_lantern_reduction()` applies this cluster lantern
to the adjacent F8.1/F10.1 roots in the fourteen-record endpoint, in their
common chart D^-1. It introduces Q^-1. The O omission and F8.2-to-C12 rechart
are performed in **one** sphere step: each component has lift -I, while the
combined full-state discrepancy has +I. Move that C12 root down and combine
it with F12 into a cube. Rechart the inverse Q along its complementary {1,5}
pair, retaining the disk discrepancy.

The remaining original C13 square has a useful complementary triple chart:

```text
C13.complement = g T456 g^-1,
g = (-5) (1,2,3,4,5)^2 (4,5)^2.
```

Its unit differs from original C13 by the deck involution, but their squares
are equal on the sphere and in closed genus two. Rechart the **whole square**
at once, then use the PC half lantern on each of its two units. The squared
pair term in that chosen chart has **exactly the same B6 unit twist** as the
temporary negative pair. Drag the last squared pair up through the intervening
factors and cancel its negative neighbor, leaving one positive pair twist.
Every extraction and cancellation is checked by complete local disk actions.

All eighteen endpoint records are positive again. There are two odd-root
records left: F10.2 is one ordinary three-point root, and F12.root+F12 has
power three. Thus this is still a mixed intermediate, not a complete
derivation of (6,7) and not a new positive Lefschetz factorization. Its final
sphere identity is independently checked by the five-arc criterion below,
and its genus-two lift has homology +I.

A next local relation is certified:

```text
C10 C12 P15 = P34 P26                         (sphere and closed genus two),
```

where P15 is the unit of the chosen C13 half-lantern's pair term. Its disk
discrepancy is explicitly retained. This has **not** been applied to the
endpoint: the actual two root records, in the common chart
`S=(P15^2)^-1`, are

```text
S (C12 C10 C12^-1) S^-1,
S C12^3 S^-1.
```

Both individual disk equalities are checked. Replacing the first by
S C10 S^-1 would be incorrect. Reversing the root-pair order transports the
third lantern curve as well; resolve that actual geometry before cancelling
a positive P15. Endpoint labels alone do not settle the remaining step.

There are two pairs of duplicated new half supports:
`C13.HL1.1 = C13.HL2.1` and `C13.HL1.2 = C13.HL2.2`.
Neither new support equals an original remaining half. The homology vectors
of the two new halves are `(1,3,-3,3)` and `(1,1,-1,1)`, while F11 has
`(-1,-5,5,-5)`. This suggests Ha(Hb)=F11 on homology, but the exact sphere
curve check **fails**. Do not treat that homological match as a transport.

Run `examples/build_six_seven_three_root_research.py` for the graphical replay:
18 disk states, two prefix-lantern states, and twenty subsequent reduction
states, with 44 individual support SVGs and no unavailable pictures. Equal
disk support classes reuse a single image independently of twist power,
so the negative and positive unit visibly match at cancellation. Only the
first eighteen states are importable equivalent disk-lab snapshots; the later
sphere states are explicitly marked research records. All diagrams use the
shared surface library and the approved vertical convention.

## Residual root lantern: a positive (24,3) intermediate

`three_root_residual_lantern()` continues the eighteen-record mixed endpoint
above through seventeen saved states. Write A=C10, B=C12 and let S be its
saved common chart. Its actual odd-root records are S(BAB^-1)S^-1 and
SB^3S^-1. Split the cube into units, then move the first B unit up across
F11. The adjacent pair is S(BA)S^-1, so use the **B-conjugate** of the
certified residual relation ABP=R1R2:

```text
BA = (B R1 B^-1) (B R2 B^-1) (B P B^-1)^-1.
```

All three replacement factors use chart SB. The replacement's 174-letter
reduced disk discrepancy is retained, has exact trivial sphere action, and
has lift homology +I. Combine the two unused B units into a squared triple
twist. This removes the last odd-root records without assuming AB=BA.

Transport the new inverse pair toward the earlier `prefix.P12` by dragging
each intervening neighbor downward. The inverse curve is thereby conjugated
and moves upward. Its exact sphere support class now equals that positive
pair's. Rechart the inverse along the positive pair in a separate sphere
step, retaining its 84-letter nontrivial disk discrepancy and +I lift.
The adjacent +1 and -1 units then cancel by exact disk action.

The endpoint has eighteen positive records, expanding in the double cover
to 24 nonseparating and 3 separating Dehn twists. All five exact reference
sphere arcs are fixed and the closed genus-two homology action is +I.
Thus this is a positive genus-two (24,3) factorization reached by the
certified named substitutions, not merely a candidate with matching counts.
It is **not yet** a complete structural derivation of the original (6,7)
to a recognized exterior-boundary identity. No disk identity is inferred
from these sphere checks.

The alternative gathering move, dragging A down across F11 before using
the same transported relation, did not expose a directly cancellable
positive pair among the eight available ones. The successful choice moves
B up. This is a local geometric failure, not a global impossibility result.
At the successful positive endpoint, exact duplicate sphere supports are
only Ha1/Ha2, Hb1/Hb2, and P15.after-cancellation/C13.HL1.3. Combining them
still requires valid transport across the intervening factors.

The graphical builder now includes this continuation as a fourth horizontal
board, with arrows between vertical factorization columns: 57 total states,
56 individual support pictures, zero unavailable supports. Purple columns
mark disk-discrepant sphere steps; red rows mark temporary inverses. The
certificate JSON saves every state and local check. These individual
support drawings are not cumulative joint cut-complex certificates.

## Sphere identity without expanding a disk point-push

The final positive endpoint's full based disk action exhausted the existing
400000-letter bound. That is a disk computation limit, not evidence against
the sphere identity. Raising the cap is unnecessary here.

`sphere_chain_certificate()` checks the exact sphere classes of the five arcs
between consecutive marked points and verifies that their endpoints are fixed.
Their union is a tree through all six points, with disk complement on the
sphere. Straighten the preserved arc classes simultaneously and apply the
disk Alexander trick; the sphere mapping class is therefore identity.
Each arc is identified by its exact two-point-neighborhood boundary class,
using F5 reduction after each braid generator. No based disk whisker is expanded.

The final five classes all equal the reference classes. This is a complete
exact sphere action check, distinct from both a numerical joint placement
certificate and the separately required genus-two lift sign. Like the existing
outer-action check it does not distinguish the central order-two spherical
braid. Tests include a pure nonidentity fixing the first arc, a separating
Torelli example, endpoint permutations, known sphere identities, and bounds
that return unknown rather than a false result.

## Check a stabilizer geometrically before Torelli factoring

Let N be the product of the six original half twists in their supplied
order, omitting the seven separating factors. Its homology action is I,
but its exact sphere action moves **each** of the five standard adjacent-point
arcs. Their image boundary-class lengths in the fixed F5 chart are
`722, 3610, 170, 3568, 1438`, respectively. The same audit also moved every
original factor's support class. Thus homology alone cannot supply one of
these curves as the stabilizer input to the Brendle–Margalit algorithm.
This does not prove that N has no invariant symmetric curve.

`sphere_curve_action()` performs the exact free-homotopy calculation directly
in F5, normalizing after each generator and avoiding expansion of unrelated
based meridians. It agrees with the full based action on independently checked
short examples, including curves enclosing the chart's sixth puncture. A word
bound returns `VerificationLimitError`, never a claimed inequality.

## Reproduction and next steps

Run from the repository with its `src` on PYTHONPATH:

```text
python examples/analyze_six_seven_structure.py
python examples/build_six_seven_root_research.py
python -m unittest tests.test_sphere_actions tests.test_six_seven_structure tests.test_hyperelliptic_homology -q
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
5. **Continue from the saved two-root transport, rather than repeating it.**
   Account for the four remaining ordinary root factors around the combined
   `{1,4}` pair twist. Test actual subword stabilizers before applying a
   Torelli factoring algorithm, or identify a transported local squared-lantern
   configuration that includes newly introduced curves. Keep the explicit
   disk discrepancy attached to the sphere recharting step.

Sources for the comparison and possible methods:
[Szabó, Sections 6 and 8](https://arxiv.org/html/2609.34042v1),
[Brendle–Margalit, Factoring in the hyperelliptic Torelli group](https://www.maths.gla.ac.uk/~tbrendle/papers/factor.pdf).
The computations and obstruction above use the repository's exact supplied
factor records; they do not assume equivalence with either source.
