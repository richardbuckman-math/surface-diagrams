# Closed-curve intersections in the marked disk

`disk_intersection.disk_curve_intersection(a, b, strands=n)` computes the
minimal number of crossings of two closed supporting curves. Its inputs are
full `ConjugatedTwist` records, so their simplicity is supplied by an explicit
homeomorphism of a standard circle. Half-twist arcs are rejected: an arc and
the boundary of its neighborhood have different crossing counts. Powers of
a twist do not change its supporting curve. This is a disk calculation; it
makes no sphere move or framed-boundary substitution.

First apply the inverse of the left conjugator to both curves. The left curve
is now the round boundary of consecutive punctures `i,...,j`. Let
`z=x_i ... x_j`. Cutting there gives the group splitting

```
A *_<z> B,
A = <x_i,...,x_j>,
B = <z, x_l for l outside [i,j]>.
```

The right curve's exact free-homotopy word is reduced in this amalgam. A run
of inside letters lies in the shared edge group exactly when it is a literal
integer power of `z`. An outside-vertex word lies in that edge group exactly
when only powers of the separate edge marker remain. BOTH directions are
handled; a word reducing from the outside vertex to the edge must be allowed
to merge the neighboring inside syllables. A third tag E retains an edge
power without bouncing indefinitely between the two vertex labels.

Adjacent syllables in the same vertex group are multiplied and freely
reduced. Edge syllables are absorbed into a neighbor. At the ends, combine
the last and first syllables cyclically, repeating these reductions. A word
remaining in one vertex group is represented on one side of the cut and has
intersection zero. Otherwise the final alternating, non-edge cyclic syllables
are crossings of the separating cut. Their count is the geometric intersection
number. The implementation re-embeds every final syllable into the original
free group and verifies the unchanged cyclic path class.

The topological justification is the usual cyclic normal-form/dual-tree
interpretation of crossings of a separating curve; see the introductory
surface discussion in [Peter Scott, *The symmetry of intersection numbers in
group theory*](https://arxiv.org/abs/math/9712212). Only this elementary surface
fact is used, not the general Theorem3.1 corrected later in that paper.
The [correction](https://doi.org/10.2140/gt.1998.2.333) concerns that general
interpretation theorem. The API uses no theorem asserting that matching
intersection counts establishes a mapping-class relation.

The algorithm operates directly on words and does not enumerate routes or
possible drawings. Deques avoid repeated removal from the start of the cyclic
syllable list. Explicit word and accumulated work bounds raise
`VerificationLimitError`; they never return zero or a false obstruction.
The certificate includes the transported word, edge word, edge marker and
final cyclic syllables. Validation precedes all computation.

Validation includes standard nested/disjoint/overlapping examples;300
independent symmetry and exact Dehn-twist commutation comparisons;45 tests
of the exact formula `i(T_a^m(b),b)=|m| i(a,b)^2` for m=-1,1,2;
common-braid invariance; powers; cyclic rotation/conjugation; edge-group
cancellation; range/type validation; and explicit bound failures.

For the newly published pure endpoints, all361 pair counts (171+190) take
about0.13seconds on this machine. The first pure endpoint has pairwise
maximum48 and total1324; after the two positive lantern contractions,
the maximum temporarily becomes72 and total2116. A subsequently accepted
fixed-square drag across five neighbors lowers these to36 and1220. These counts are independent of a common
chart conjugation. They show why a shorter conjugator or support word alone
can be misleading about the complexity of the whole collection.

A concrete geometric check: before the final square unwinding, round
O1234, F13.1 and F12.1 have pairwise crossings6,2,2, despite their tempting
endpoint sets. Thus that configuration is not a direct cluster lantern.
Transporting F13.1 by F12.1 inverse reduces its crossings with O to2, but
carrying the actual root up across the intervening pair makes that pair's
support length30, beyond the retained20 bound. This transport is recorded
as a probe, not applied to the graphical route. The accepted square unwinding
also reduces the three pairwise counts to2,2,2, but the actual middle curve
is still different from the constructed exact exterior-lantern target.
Pairwise counts alone also
do not certify compatibility of a triple; the full ordered equality remains
necessary. Run `python examples/analyze_pure_intersections.py` for the matrix
and explicit normal-form witness.
