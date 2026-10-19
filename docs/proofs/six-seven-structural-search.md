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

## Reverse half-lantern compression and a retained negative pair

An optional continuation, `three_root_half_lantern_compression()`, is exact
in the disk relative to the positive (24,3) endpoint. Move the earlier
P15 unit down across five factors, keeping it fixed and conjugating the
crossed factors. It now precedes the five-term C13 suffix. In that chart
write P for the unit pair twist, Ha/Hb for its half-lantern arcs, and C for
the complementary C13 root. The local exact disk relations are

```text
Ha Hb P^2 = C,     CP=PC,
P (Ha Hb P^2 Ha Hb) = C^2 P^-1.
```

The code checks the full six-term local disk action against the two-term
replacement, not just these abbreviated symbols. There are seven saved
states including all five adjacent moves. The final fourteen records have
four squared triple twists and one inverse pair. All five exact reference
sphere arcs are fixed and the lift homology is +I.

The signed upstairs counts are 14 positive nonseparating, 2 negative
nonseparating, and 4 positive separating units. Net (12,4) does **not**
identify a positive (12,4) factorization or a double Matsumoto construction.
Deleting the negative pair gives nonidentity homology. Every direct
fixed-neighbor transport of that inverse to an earlier positive pair was
checked: prefix.P45, new.P34, new.P26, residual.P34, and residual.P26 all have
different exact sphere classes from the transported inverse. The replay's
JSON retains each ordered intervening block and both compared classes.
Other routes remain open; this is not a global cancellation obstruction.
Moving the inverse to the other side gives an exact sphere/closed-genus-two
equation between thirteen positive factors and the positive P15 twist.
F3 moves P15's exact support class, a saved witness that these positive
factors are not all supported in a disk bounded by that target curve.

The three remaining ordinary roots at the positive endpoint were also used
as a small geometric filter, without a broad Hurwitz search. Each word of
length one to three using each root at most once, in every order and sign
(78 per target pair), failed the homology transport test for F3/F9 and
F6/F11. This says nothing about repeated-root words or pair twists.

For raw root pairs (C4,C5), (C4,C12), (C5,C12), the homology traces are
-4, -68, -12. Transporting the later root across the entire intervening
factor block instead gives traces -4, -4, +4. The last has (M-I)^2=0 but
both support partitions are {2,4,6}; the exact curves differ. It is not
the earlier PC cluster-lantern configuration of two different triple
partitions. None of the endpoint's existing pair curves, nor the direct
over/under pair arcs tested in the C5 chart, is fixed by that product.
Thus the parabolic matrix does not supply a geometric lantern certificate.

## A complementary PC rose exchanges C5 for C13

`three_root_petal_exchange()` moves C5 down unchanged through eight factors
in the signed compressed branch, stopping just before C13. At this position
C5 fixes P15's exact sphere class. Its complementary triple is {1,3,5}.
The whole squared twist can be recharted with lift +I; the unit-root
discrepancy has lift -I and is saved, not applied as an isolated equality.
The complementary conjugator is `g=(-5,2,-5,-4,-3,-2,-1)` after reduction.

Two cyclically ordered PC roses now end in the required P15 petal. The
last petal is the same positive twist as the retained inverse's unit in
B6, not just on the sphere. It moves past C13 and cancels exactly in the
disk. The fourteen-state continuation ends with seventeen positive records,
of type (24,3) upstairs: four half twists, ten full-pair units, and three
squared triple twists. The C5 separating ancestor is removed and C13 is
restored. All five exact sphere arcs and the lift sign are checked again.
This is another certified intermediate, not the requested complete derivation.

There is now a concrete transported local lantern. Write A for the
complementary C5 root and B for the C13 root. In the chart g of A, plain
T124 is **not** B; applying A to that model gives B, with the complete sphere
action and +I discrepancy checked. Set h=A g. The next relation is

```text
A B Q23 = P15 R46,
Q23=h T34 h^-1,  P15=h T12 h^-1,  R46=h T56 h^-1.
```

Its nontrivial disk discrepancy is retained. The five C5 petals at the
endpoint multiply to A^2 P15^-1. Two ordered uses of this lantern give
the prepared relation for that actual six-record suffix:

```text
(five C5 petals) B^2 = P15 R46^2 Q23^-1 (B^-1 Q23^-1 B).
```

The full discrepancy fixes each exact sphere reference arc and has lift +I;
its braid exponent sum is 20, so it cannot be a disk identity. The last two
inverse support classes differ. They must not be replaced by Q23^-2 or
treated as identical merely from their endpoint pair {2,3}. These local
relations are certified but have **not** been applied to the full endpoint.

Two short follow-up filters were checked on the prepared signed state:
neither inverse has a direct cancellation with a positive pair under the
fixed intervening-product transport, and neither C4 nor C12 preserves
either inverse's transported class during a single fixed-root downward
sweep. At the new positive endpoint, none of the 78 signed root words
using the three remaining roots at most once passes the F3/F9 or F6/F11
homology transport filter. These do not exclude other Hurwitz moves.

The local graphical replay now has 78 route states, four prepared-relation
panels, 71 support SVGs, and zero unavailable supports. Twenty-eight focused
tests pass, including each local move, the whole-square lift distinction,
the actual root chart, and the two different inverse curves. The final
exchange and prepared-relation panels were visually inspected. All pictures
remain individual support drawings, not cumulative joint certificates.

## A reverse PC lantern across three earlier stages

`three_root_cross_petal_lantern()` continues the positive petal-exchange
endpoint, rather than applying the prepared two-negative suffix relation.
It gathers prefix.P45, residual.P34, and C5.rose.1.1 (the first P35 petal).
Move each intervening neighbor down across residual.P34, so that P34 is
transported upward; then drag the P35 petal upward unchanged. The other
choice of direction leaves the wrong middle curve.

The gathered supports agree, in their actual order, with a PC rose in a
single chart. Its boundary twist is

```text
g T123 g^-1,  g=(-5,2,-5,-4,-3,-2,-1,2,1,4,3),
```

and encloses {3,4,5}. To reproduce the ordered PC rose model, append the
three-point half rotation (1,2,1) to g before calling `pc_rose_terms`.
This swaps the standard outer petals without changing T123. All three
support classes are checked on the sphere, and the whole replacement
fixes all five exact reference arcs with lift +I.

The replacement is genuinely sphere-only: its disk discrepancy sends the
boundary class of the first adjacent-point arc to a different class of
length 6050. The entire witness is retained. Expanding the full based disk
action reaches the existing bound; the disk loop witness proves nonidentity
without that expansion and without raising the bound.

The seventeen-state continuation ends with fifteen positive records,
including one ordinary three-point twist and three squared triples.
It is a **mixed** mapping-class factorization, not a new positive LF type
or a complete derivation. Moving that new ordinary root down with either
of the two consistent Hurwitz choices does not make it equal to any of
the three existing separator roots. In particular its complementary
{1,2,6} partition does not identify it with the transported C12 curve.

The local moves use `research_hurwitz_move()`: raw conjugators retain a
freely cancelling before/after word discrepancy. This is an exact disk
equality, stronger than an action match, with no large meridian expansion.
It avoids the public move checker’s expansion limit for this route without
changing the lab checker, increasing a cap, or accepting a failed check.
The separate sphere substitution still requires its five-arc and lift checks.

Two bounded negative filters are also recorded to prevent repetition:

* None of the 31 ordered nonempty C5-petal subsequences transports F11 to
  F6 or F9 to F3 by the inverse action arising when those petals move up.
  They all fail already in homology.
* For each of the three squared triples and each pair of the four half
  twists, gather the three factors in their original order, independently
  choosing either upward-Hurwitz direction for each later factor. Move
  the root square to the end unchanged. All 72 configurations fail the
  necessary homology condition H2=C(H1) for a reverse genus-two lantern.
  This is a finite local filter, not a global obstruction.

Next inspect the new {3,4,5} root against the nearby transported C4 root
{3,5,6}. Their shared pair {3,5} suggests a four-holed-sphere chart with
singleton clusters 4 and 6. The actual curves and the ordered relation
must be checked; the partitions alone do not supply that lantern.

All 30 focused sphere/structure/lift tests pass. The graphical replay has
95 route states and 85 support SVGs with no unavailable pictures; the final
three new columns were visually inspected. Dense disk support representatives
remain distinct from the simpler sphere classes used in the relation checks.

## The actual C4 cluster chart cancels another inverse pair

`three_root_cross_cluster_lantern()` starts at the cross-petal endpoint.
Let g be that endpoint's ordinary-root conjugator. Move F3 down across C4,
then set `h=g+(4,5,4,5)`. The two roots are represented by

```text
A=h T123 h^-1,
B=h (sigma3 T123 sigma3^-1) h^-1,
Q46=h T34 h^-1, P35=h T12 h^-1, O3456=h T1234 h^-1.
A B Q46 = O3456 P35.
```

The standard and transported lantern are checked in B6. The actual C4
square after the F3 move has the same sphere action as B², with +I lift.
That square rechart is applied before splitting; its nontrivial disk
discrepancy moves the 2--3 disk-arc boundary to a class of length 698.
There is no claim of disk equality for that rechart.

Split B² and replace A B by O3456 P35 Q46^-1. Bring new.P34 up unchanged
past the unused B, F3, and F6. It is exactly the positive Q46 in the disk,
so the cancellation uses an exact disk action check. No sphere rechart is
needed for this cancellation. The same is true for the later P35 petal:
bring C5.rose.2.1 up unchanged and combine the two equal P35 units in B6.
O3456 is drawn along its complementary P12, h T56 h^-1, on the sphere.
That unit step has lift +I and disk exponent discrepancy ten.

The 21-state continuation ends in fourteen positive records with one odd
three-point root and two squared triples. It is still mixed and is not
assigned a positive LF type. The full sphere identity and +I lift are
checked again. The next possible cluster is the transported leftover B
against the complementary side of the remaining C12 square; the intervening
ordered factors must be included, not inferred from their point partitions.

The small chart diagnostic that led here checked the three natural local
positions of C4: raw, F3(C4), and F3^-1(C4). For each it tried both standard
T124 arcs and A powers -3 through 3 after the unique endpoint-compatible
inside/outside cyclic placements. Only F3(C4) matched. The simplest match
uses h as above; the other uses the opposite T124 arc and A^-1. This is
a local chart check, not an exhaustive Hurwitz or common-chart search.

All 31 focused sphere/structure/lift tests pass. The graphical replay now
has 116 route states and 99 support SVGs with no unavailable drawings. Its
last three new columns were rendered and visually inspected; the pictures
remain individual disk representatives, not cumulative cut complexes.

## C12's short chart fails; a C13 chart gives a signed continuation

At the positive C4-cluster endpoint, two consistent downward sweeps of
the odd root give traces -20 and -4 against the C12 unit root. Only the
second is compatible with the complementary-root lantern homology model.
The fourteen endpoint-compatible short chart candidates (both T124 arcs,
A powers -3 through 3, with cyclic placements inside/outside) do not match
the actual C12 sphere class. None of the three natural pair supports in
the transported A chart is fixed by C12. This rules out these charts,
not every possible transported common chart.

C13 instead has an actual common chart with the odd root A before either
is changed: `h=A.conjugator+(1,2,1,2)`. Bring the C13 square up unchanged.
The model `h (3,) T123 (-3,) h^-1` encloses {3,4,6}, complementary to
C13's {1,2,5}. Its unit discrepancy fixes all five sphere arcs but has
lift -I. Recharting the entire square has +I; the unit change alone is
not applied as a lift equality.

`three_root_tail_cluster_lantern()` records seventeen stages. After splitting
the recharted square, the exact disk cluster lantern is

```text
A B Q45 = O3456 P36,
B=h T124 h^-1, Q45=h T34 h^-1,
O3456=h T1234 h^-1, P36=h T12 h^-1.
```

Rechart O3456 to h T56 h^-1 on the sphere (disk exponent discrepancy ten,
lift +I). This P12 matches the existing prefix P12 in the disk, so bring it
up and combine them. Fifteen signed records remain, including one ordinary
C13 root, one C12 square, and the essential inverse Q45. Every local disk
move and the final whole sphere action are checked. Omitting the inverse
changes the closed genus-two action. This is not a positive LF type or a
complete structural derivation.

Eight direct fixed-neighbor cancellation transports of Q45 to positive
pair factors fail; their exact sphere classes are saved in the result.
C12 does not preserve Q45's raw class or the class obtained by transporting
the inverse down through the intervening factors. Thus a PC rose of C12
cannot be assumed to have Q45 as a petal from endpoint containment alone.
Acting on Q45 by each actual F3/F6/F9/F11 half twist, in either sign, also
matches no positive pair. Extracting the halves in the ten orders
`F3`, `F9`, `F3/F6`, `F3/F11`, `F9/F6`, `F9/F11`, `F6/F3`, `F6/F9`,
`F11/F3`, `F11/F9` gives no immediate cancellation either.

The half-extraction diagnostic originally reached the 400000-letter disk
support bound. `sphere_supported_class()` now starts at the standard
boundary and acts directly in F5, reducing after each generator. The ten
specific routes above finish without that disk expansion; the largest
negative sphere class in this audit has length 333090. No bound was raised.
Tests compare the helper against independent disk reduction on short
examples including the sixth puncture, check peripheral whiskers, and
require bounded calculations to return unknown rather than an inequality.

Next test transports by the actual leftover C13 root against the Q45/C12
configuration. The signed continuation is available alongside the positive
checkpoint; it does not replace it or justify discarding the inverse.

All 34 focused sphere/structure/lift tests pass. The local graphical replay
contains 133 route states and 111 support SVGs, with no unavailable pictures.
The final three new columns were visually inspected, including the retained
red inverse. Dense disk representatives remain individual support pictures,
not cumulative joint cut-complex certificates.

## Exact fixedness from a three-point free-product chart

`three_point_curve_fixedness_certificate(T,w)` avoids constructing T(w).
Write delta=(1,2,3,4,5). For a twist on an interval starting at i, its
standardizing chart is g delta^(i-1), where g is its conjugator. Compute
the unoriented cyclic class of w in the inverse chart, with the existing
word bound. A bound failure is unknown, not a negative result.

Here is the criterion and its proof. In the T123 chart, put u=x1 x2 x3
and split F5 as F(x1,x2,x3)*F(x4,x5). T123 acts on the first factor by
conjugation by u and fixes the second. The same argument applies to every
positive power of the twist.

If the cyclic word lies in either free factor, its free conjugacy class is
fixed. Otherwise cut it at an outside-to-inside transition and form its
alternating nonempty free-product syllables. A mixed cyclically reduced
free-product word can be conjugate to another such word only by a cyclic
permutation of its syllables. Therefore, if the twist fixes the class,
each inside syllable has a finite orbit under conjugation by u. It must
commute with a power of u, hence belong to <u>; u has no proper root.
Conversely, if every inside syllable is a power of u, each is fixed and
the whole word is fixed. An unoriented fixed class has an oriented period
of at most two, so gives the same condition. This yields an exact negative
witness: the first inside syllable that is not a power of u.

Tests compare this criterion with direct sphere actions in 80 short
examples, covering all four intervals, two conjugators, two powers, and
curves through the sixth-puncture chart. They also test mixed outside
words and a would-be cyclic permutation that is not a finite orbit.

`three_root_tail_fixedness_audit()` checks the initial signed Q45 curve and
three repetitions of two adjacent forward Hurwitz moves with its C13
neighbor. The chart sizes are 146, 832, 4846, 28244. Every case has a
noncommuting inner syllable (-3,-1), so C12 changes the curve. At repetition
two, directly computing the C12-unit image exceeds the 400000-letter bound;
the normal-form certificate settles that same case without expanding the
image. The regression test requires both outcomes. These are diagnostic
positions, not new derivation steps or a cumulative drawing certificate.

The following bounded hypotheses also fail. Acting on Q45 by C13 powers
-3 through 3 gives neither a C12-invariant curve nor an existing positive
pair. Consider extracting selected factors from the ordered intervening
block F3, F6, new.P26, F9, residual.P26, F11 upward unchanged, each just
past the inverse. C12 is unchanged by these moves. Fifteen nonempty
subsequences preserving endpoints 4,5 fail by direct sphere action. Sixteen
with one 14 half and one 25 half instead give endpoints 1,2 and also fail
the new normal-form test. In the latter audit, combining the inverse C12
chart with the support conjugator before acting keeps the chart sizes
between 30 and 3930. The empty case was already checked. The other 32
subsequences give endpoint pairs 1,5 or 2,4, which straddle C12's two
sides; they cannot be petals. This excludes this extraction family, not
all Hurwitz routes or all curves with those endpoints.

Next return to the positive C4-cluster checkpoint. It has an unused
endpoint triangle P12/P23/P13 around {1,2,3}, with one P12 unit and two
P13 candidates. Verify the transported ordered PC rose geometrically
before any inverse substitution. Keep the signed C13 branch separately;
its inverse Q45 has not been cancelled and may not be omitted.

All 35 focused sphere/structure/lift tests pass. The report keeps its 133
derivation states and 111 support SVGs, plus four diagnostic positions
that are explicitly not derivation progress. The new support comparison
and result table were rendered and visually inspected.

## October 19 afternoon: rotate the half lantern to introduce new cycles

The endpoint-triangle proposal above does not work in the eight tested
gathered charts. Start with the positive fourteen-record C4-cluster endpoint,
use its one P12 unit, gather new.P26 (actually P23), then one of the two
P13 petals. For each later factor, either drag it upward unchanged or move
each intervening neighbor downward so that the later factor is conjugated.
This gives four choices per P13 petal. In all eight resulting products the
genus-two matrix M has M squared unequal to I. An ordinary three-point twist
has involutive homology, including after a hemisphere change. Thus none of
these particular ordered triples is a PC rose. This is a bounded local
failure, not an obstruction to every transported {1,2,3} chart. The earlier
wording "two P12 units" was a counting error; there is only one here.

A different local block does admit an exact disk compression.
`three_root_alternate_half_lantern()` starts again at that positive checkpoint,
before the signed C13 branch. Bring C5.rose.1.2, C5.rose.1.3, C5.rose.2.2
upward unchanged to positions 2,3,4 (zero indexed), immediately after the
prefix P35 square. Each takes eight adjacent Hurwitz moves. In the common
chart

```text
g = (-5,2,-5,-4,-3,-2,-1),
C = g T123 g^-1,  P = g T12 g^-1 = P15,
```

the five gathered pair units equal C squared followed by P inverse exactly
in B6. The inverse P is the original g T12 curve: the gathered middle petal
has acquired a conjugation and cannot simply be negated in its place.

Use the half-rotated chart g(1,2,1) for the standard PC half lantern. Its
two half twists both join marked points 1 and 3; its pair term is P squared.
Expand C squared by two copies of this three-term relation, then cancel
one unit of the final P square against the following inverse. Finally
replace cross.C4.unused by its three PC rose terms. These are four disk
substitutions after the 24 adjacent Hurwitz moves; the saved branch has
29 states including its initial checkpoint.

The eighteen positive records at the end comprise eight half twists,
nine full pair-twist units, and two squared triples, giving genus-two
counts (26,2). Four of the half twists are newly introduced, on {1,3},
so this escapes the earlier obstruction involving only the original six
half twists. No ordinary three-point root or negative factor remains.
The complete five-arc sphere action is identity and the separate lift
homology is +I. All new moves are disk-exact relative to the chosen
checkpoint; that does not undo earlier sphere-only discrepancies. There
is still no final standard boundary identity or full (6,7) derivation.

The new `disk_common_chart_certificate()` avoids a large based disk action
for a local relation with a common conjugator. For before/after factor
lists, remove g from each factor chart, formally reconstruct both products
as g(model)g^-1 by free cancellation, and check the faithful Artin action
of the model discrepancy. An incorrect local equality raises an error;
a bounded action is not accepted. The tests include a long common chart
around the elementary braid relation and require that the action sees
only its six-letter discrepancy, as well as rejecting a false relation.

Initial local follow-up failures: the four new halves form two repeated
classes Ha,Hb with homology vectors (1,0,1,0) and (1,-2,3,-2). Neither sign
of a single C5, C4, C12, or C13 ordinary-root action takes Ha to Hb in the
exact sphere support calculation. For each of the two remaining separators,
choose two of the four new half records (six choices), gather them in their
existing order using the two upward-move choices independently, and test
the reverse genus-two-lantern requirement H2 = C(H1) up to orientation.
All 2*6*4 = 48 gathered configurations fail already on homology. These are
not exhaustive Hurwitz routes. Next include original half twists and pair
twists in geometric transported configurations; do not repeat this family
or equate a (30,0) count with any known standard boundary relation.

The graphical builder includes the new branch separately after the signed
branch's failed fixedness audit. Its pictures use the shared surface
library and display individual support representatives only, not cumulative
joint cut-complex certificates or disk-only lab snapshots of the original.

Validation: all 37 focused sphere-action, structural-route, and genus-two
homology tests pass. The replay has 162 route states and 138 shared support
SVGs with zero unavailable drawings. Its final three new columns were
rendered and visually inspected, showing the retained inverse, its exact
cancellation, and the last ordinary-root expansion.

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
python examples/build_six_seven_three_root_research.py
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
