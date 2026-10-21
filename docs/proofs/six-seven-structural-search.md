# Structural search for Richard's (6,7) derivation

## October 21: circular starting points and the 32-length checkpoint

Richard pointed out that factors lie around a circle and the starting point
can be changed. `cyclic_factorizations.rotate_factors()` now records this
exactly: if P=A B, the unchanged rotated list B,A has product A^-1 P A
(or B P B^-1). The shorter of these two explicit conjugators is retained.
A telescoping free-word certificate accompanies every rotation. This is a
global change of basepoint, not an assumed disk equality and not a hidden
sphere substitution. Disk equality requires the relevant commutation.
Tests include a noncentral counterexample and the actual (6,7) discrepancy,
which is sphere-trivial with +I genus-two lift but not disk-trivial.

All three six-strand interactive labs have a block-size input and Top ->
bottom / Bottom -> top buttons. The individual factor records, supports,
powers and words stay unchanged; only their order and the saved global
frame change. A complete exact disk action checks that frame before commit.
Selection follows its factor. Undo/redo, JSON export/import, persistent
sessions and the public browser backend preserve the new starting point.

The bounded simplifier now also considers the circular last/first Hurwitz
adjacency. Only two extra directed neighbors are needed, not every rotation
of every already adjacent pair. Its certificate separates the explicit
basepoint rotation from the subsequent local disk Hurwitz move. Pure
rotations are score-neutral; the strict descent does not loop through them.

A bounded two-step global-frame lookahead from the previous (36,6,48,8)
checkpoint found conjugations (2), then (3), reaching (35,7,49,8). A further
(2) reaches (32,6,46,6). Applying the combined frame (2,3,2) directly gives
the same final score, so the published forward replay adds ONE checked
whole-column conjugation, with cumulative frame (2,3,2,5,-3). Its eight
states retain three Hurwitz moves, three explicit global conjugations and
the initial exact disk support normalization. All thirteen original types
remain: six half twists and seven squared three-point twists. No sphere
substitution was used. Total braid letters fall 178 -> 154; conjugator sum
44 -> 32; maximum support cut visits 10 -> 6. The complete final disk action
and +I lift pass, and the downloadable JSON passes the real lab import.
No minimal pairwise geometric intersection or global optimality is claimed.

Bounded failures, to avoid repeating them: cross-seam fixed-factor slides
of length <=5, retaining all prefixes below 24 cut visits and conjugator
sum <=48, gave seven accepted seam-crossing prefixes and no gain from 36.
From 32, a four-layer beam (width10 plus up to4 seam-bearing states,
36 candidate operations per state, cut cap24 and sum cap38) evaluated 1,404
operations  / 1,042 distinct circular states without a further improvement.
These are work-bounded failures, not obstructions. Full probe inputs/results
are in ignored .preview/cyclic-slide-probe.json and cyclic-beam-third.json.

Validation: new cyclic/action/replay tests pass, including all block sizes,
positive and negative rotations, scope distinctions and rollback on invalid
input. Chrome checks the live controls, unchanged complete factor drawings,
selection, undo/redo, frame-preserving JSON import/export and 390px layout.
The updated precalculated viewer passes all 441 transition displays, connected
braid alignment/separators, an eight-column overview and mobile checks.
Default load remains seven requests  / 737,581 bytes locally; no browser Python
startup is added to that viewer. Existing lab and Node regressions and remote
CI are checked before final delivery.

Next: continue from 32, not the old36 checkpoint. Use the circular adjacency
for transported local lantern/half-lantern configurations and geometric
block decompositions, with explicit basepoint frames and every actual sphere
move labeled. The standard-block-to-positive-fifty bridge is STILL OPEN;
this simplification does not complete the structural derivation. Preserve
the pending (10,10) transcription and the user's untracked 8Boundaries.pdf.

## October 20: cylinder calibration, continuous braids, and a simpler (6,7)

Richard supplied an explicit convention: the half-twist arc 4--6 BELOW 5
has top-to-bottom braid (4,5,-4). It recovers as Arc(4,6,(),direction="down")
from the existing algebra; the display's added vertical support reflection
was the mismatch. Positive crossing signs and all algebraic source words
are unchanged. Compact-replay supports now render without that reflection.
The live lab's factor cards, support inspector and paired SVG export also
retain the source support orientation. Prefix/action-chart rendering is a
separate existing convention and was not changed by this support correction;
do not silently invert algebra actions to fix an individual support picture.

`docs/proofs/six-seven-compact/calibration.html` shows the exact arc and the
boundary of its neighborhood next to (4,5,-4) and (4,5,5,-4). The square of
the half twist equals that full twist by an exact disk action check. Browser
sampling checks the displayed arc lies below the marked row, not just that
its internal itinerary says "down". Points are numbered for inspection.

A genuine disk-exact simplification now starts the public compact viewer.
It keeps all thirteen factors: six half twists and seven squared three-point
twists. The checked route is an initial disk support normalization, followed
by Hurwitz (2->3), global conjugation (-3), global conjugation (5), Hurwitz
(6->7), Hurwitz (7->8), with zero-based positions. Individual conjugators are
normalized exactly after each operation. Its cumulative global frame is
(5,-3). It has NO sphere substitutions and preserves the same fibration.

Score (sum conjugator lengths, maximum length, sum cut visits, maximum visits):
(44,7,59,10) -> (36,6,48,8). Total braid letters fall from 178 to 162.
The score allows the worst conjugator to increase when the total decreases,
subject to the support cut cap. Pairwise minimal geometric intersections
were NOT computed, and no globally shortest representative is claimed.
A bounded adjacent/single-generator greedy descent reached this checkpoint;
do not repeat the five-move discovery from the original state.

The calculation module is `factorization_simplify.py`. Its replay retains
the exact adjacent Hurwitz/free-word certificates, global-conjugation
certificates, and exact disk support normalization classes. Its final full
based Artin action equals g * original_product * g^-1, and its lift is +I.
The saved `simplified-six-seven.json` passes the real lab's import check,
including the saved global frame. `simplification-certificate.json` preserves
all seven states. Download it from the compact page and keep exploring.

The viewer now defaults to this forward simplification. The separate longer
substitution route also defaults to forward from Richard's original (6,7),
with its previous reverse direction still available. Its 145 atomic moves,
54 groups, eleven chapters and fourteen explicit sphere moves are retained
losslessly. The explicit standard-block bridge is still UNCOMPUTED. This
increment does not claim a completed or shortest structural derivation.
Richard will check the typo in his (10,10); preserve that transcription.

Braids are now one vertically connected drawing per factorization, with
blue dotted factor separators and strand colors carried across every row.
`braid_stack.py` renders margin-free fragments using the existing crossing
renderer. Browser `connected-braid.js` only stacks/recolors those fragments;
it never invents crossing geometry, flips signs or reverses words. A Node
fixture compares its complete output byte-for-byte with the independent
Python stack, including negative crossings and empty factors. Stale word
or row-height metadata is rejected. Full continuous SVG download is provided.

Validation: the compact browser test visited every simple/research mode in
both research directions (438 transition displays), checked row/braid height
alignment and every separator, a seven-column simple overview, and a 390px
layout. The cylinder calibration, dense supports, and corrected live lab
were visually inspected. A real temporary lab imported the final JSON,
exercised undo/redo, and exported with mirror=0; no browser errors occurred.
The default route's assets are packed first: 732,836 bytes / seven requests
on initial local load, without a Python runtime. Timing depends on load.
Focused exact-action/replay/geometry tests and fourteen Node tests pass.
The complete regression suite and remote CI are checked before final report.

Next: continue from the (36,6,48,8) thirteen-factor checkpoint, using geometric
Hurwitz block slides or small lookahead and explicit global conjugation to
find further simplifications. Prefer short common charts and the user's
conjugator-length/curve-intersection goals over preserving the original
ordering. Connect useful local substitutions to the factor-level derivation
while keeping every sphere move explicit. Avoid restarting the long reverse
route as the default explanation. The separate standard-block extraction
remains open; the current (10,10) is pending Richard's correction.

## October 20: compact sphere charts and bounded support pictures

Richard asked to shorten the (6,7) derivation and cap intermediate curve
complexity, with (10,10) as a possible alternative starting point. The new
`docs/proofs/six-seven-compact/index.html` is a precalculated graphical replay:
11 chapters, 54 grouped transitions, and all 145 original atomic moves.
This is a shorter presentation, NOT a new shorter elementary derivation.
The explicit standard W0 W1 -> actual fifty-unit source bridge remains
UNCOMPUTED. Do not present chapter grouping as filling that gap.

The existing successful branch is now preserved in the page's
`source-route.json`, with its original report SHA and all fourteen sphere
steps. `frames.json` records a whole-column global conjugation at each of
146 states, linked by a source SHA. Each factor is then replaced by a
shorter disk-chart support ONLY after exact five-arc sphere and +I genus-two
lift checks. Every added sphere rechart is explicitly yellow-labeled,
separately from each column's global frame and the fourteen source sphere
moves. Full per-factor disk discrepancies are in `support-certificates.json`.
The final frame is identity and the final thirteen braid factors are
literally Richard's original words, not only sphere-equivalent supports.

Measured clutter: raw disk boundary classes reached 34,768 letters while
one corresponding sphere class has length 10; maximum source sphere class
length was 170. The old available support itineraries reached 1,176 cut
visits, with one unsupported picture. All newly retained pictures pass the
shared Arc/Loop renderer and have at most 40 horizontal cut visits. All but
ONE displayed factor presentation have at most 24. The exception is F10.2
at reverse state 111, an ordinary three-point root, with 40 visits. A
24-visit cap was not established there. Bounded nonexpanding support search,
single/two-generator/cyclic chart candidates and prefixes untwisting that
root failed to put EVERY simultaneous factor under 24. These are bounded
failures, not an obstruction theorem; do not repeat a broad search blindly.
Complementary triple roots can differ by -I upstairs; preserve the +I check.

`sphere_support_compact.py` supplies a work-bounded support shortener,
independent replacement verification, and telescoping certificates for
whole-column global conjugation. It never raises a requested drawing cap
automatically or claims a globally shortest braid. Build the page with
`python examples/build_six_seven_compact.py`; supplied cached candidates are
only hints, and are rechecked against each actual framed source. This
replay does not change the public interactive labs or claim cumulative
joint cut-complex certificates for these individual support pictures.

Assets load in 32-picture chunks on demand, without Python startup. Local
Chrome checks visited all 11 chapter, 54 group and 145 atomic transitions,
the twelve-column side-scroll overview, explicit sphere labels, and a
390px layout. No JavaScript errors or missing assets were found. Initial
local display took 159ms / 660,433 bytes / five requests (not an Internet
speed guarantee). All 677 SVG images were parsed; desktop, dense-root and
mobile views were visually inspected. Nine focused tests passed, including
fresh sphere/lift checks of every replacement and source-to-display links.

The saved twenty-factor (10,10) transcription still fails sphere closure
and homology, so it cannot supply a verified reverse seed. Nakamura's
primary source https://arxiv.org/pdf/1811.03708 gives a different (10,10)
from three alternate (4,3) blocks and one lantern. Its Remark 1 calls the
borrowed-twist intermediate a fake (6,7): it actually has type (8,6), and
requires a fourth lantern curve from another block. Deleting a (4,3) block
without tracking that borrowed factor does not establish a closed (6,7).
No literature factorization has been silently identified with Richard's
nonclosing transcription.

Next: seek actual route shortcuts by fusing the signed rose/half-lantern
excursions into transported local substitutions under a fixed chart/cut
budget. Prefer a common frame over each whole substitution, to avoid extra
chart changes. A source-encoded, exactly closing Nakamura (10,10) is another
possible seed, but its Hamada support curves must be transcribed before
using it. Keep the explicit W0 extraction gap visible throughout.

## October 20: explicit standard-block untwisting, extraction still open

The heartbeat's positive (24,3) checkpoint is older than the saved positive
fifty-unit branch and its standard W0 W1 recognition. Preserve all of them.
No new full (6,7) derivation or W0 block extraction is claimed by this increment.

`standard_block_routes.standard_block_untwisting(name,i)` now constructs
adjacent Hurwitz moves from sigma_i inverse * F * sigma_i to F, where
F is T, W0 or W1. It implements Auroux's Lemmas 6-7 constructively: expose
the chosen twist, sweep it through the block, cycle the other factors,
restore the transported support using centrality, then undo the exposing
moves. The centrality rechart is independently checked in the disk, on
the five sphere arcs, and in genus-two homology. It is labeled SPHERE MOVE
if the disk equality fails. T lifts to -I, not identity; W0 and W1 lift to I.

All fifteen block/generator combinations pass the exact replay guards.
T and W0 need one sphere move for generator 1 and disk equalities for
generators 2-5. All W1 examples are disk-exact. The graphical examples have
40 W0 states and 68 W1 states (including their starting state). They show
support arcs beside exact braids, changed intervals or complete vertical
factorizations, a step selector, and the full disk discrepancy for every
rechart. These are individual supports, not cumulative joint cut complexes.

Rebuild with `python examples/build_standard_block_untwisting.py`.
The checked page and certificates are in
`docs/proofs/standard-block-untwisting/index.html`, copied by the ordinary
site build. Repeated factor drawings are stored once in its display data.
The display JSON shrank from 1,475,038 to 77,167 bytes. Browser checks
cover all 108 displayed states and their image assets, full-factorization
toggles, explicit sphere labels/discrepancies, and a 390px layout; no
JavaScript errors or missing images were found. The desktop and mobile
views were visually inspected. Three focused engine regressions pass.

A narrow preliminary check used the actual standard-letter tail
U=1^4 3^4 A 55 A, A=43211234, and the 20-unit W0 target. Forty bounded
word-reversing probes (cyclic starts, reflected generator numbering,
left/right extraction) produced no positive residual certificate. All
terminated in at most 901 rewrites. This is not an obstruction to Hurwitz
equivalence or to an extraction involving earlier transported factors.
Do not turn it into a broad repeat of the exhausted greedy search.

Next: expose an actual twenty-unit standard block inside the fifty-unit
source, allowing transported earlier factors. Then apply this explicit
untwisting routine and check the thirty-unit remainder. Until extraction
is certified, the theorem-based bridge in the graphical PDF remains
UNCOMPUTED; this reusable reference-block replay does not fill it.

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

## Explicit sphere-move display convention

Every sphere-only transition must visibly say **SPHERE MOVE**, with its
before/after states and saved disk discrepancy, exact sphere-action check,
and separate lift check. Color alone is insufficient. State disk equality
as false, unknown, or independently proved rather than silently identifying
the disk braids. Sphere simplification of a displayed cut representative is
likewise explicitly identified and is not a factorization change.

## October 19 evening: two remaining separators and a coupled inverse transport

The 176 additional local reverse-genus-two-lantern configurations at the
positive (26,2) endpoint fail on homology. These use two of the eight actual
half records, at least one from F3/F6/F9/F11, and either remaining separator.
Gather the later half and separator after the earlier half, choosing either
upward-unchanged or fixed-neighbor-conjugated transport independently. The
48 new-half-only configurations were already excluded. This excludes only
these gathered positions, not arbitrary Hurwitz routes or splitting pair
twists into new half twists.

The actual adjacent separator roots instead share a useful geometric chart.
Both fix the round P12 and P34 sphere classes by the exact three-point
fixedness certificate. Write B for the remaining C13 root, with chart
`(-5,-5,-4,-3)` on T123. The C12 root's sphere support equals that of
`A=H56^-1 B H56`. The tested H56 powers -3,1,3 do not give that support;
power -1 does. Rechart the WHOLE C12 square to A squared and certify the
full discrepancy on the five sphere arcs and by +I homology. No unit
hemisphere-change assumption is used.

The short-chart ordered relation, checked on the sphere and in the closed
genus-two lift, is

```text
ABQ = K,   Q=T56,   K=T12 T34.
A^2 B^2 = (AB)(B^-1 A B B)
        = (K Q^-1)(B^-1 K Q^-1 B)
        = T12^2 T34^2 Q^-1 (B^-1 Q^-1 B).
```

K commutes with A, B, and Q in this four-holed-sphere chart. The saved
whole substitution also has its own five-arc action and +I lift checks;
its disk discrepancy has exponent sum 20, so it is certainly not an exact
B6 equality. The earlier whole-square rechart is a separate sphere step.

`three_root_last_separator_decomposition()` makes nine states. After the
two sphere steps, move the second inverse upward by dragging each preceding
neighbor DOWN unchanged. It crosses the first inverse Q, then T34 squared,
T12 squared, and F11. At that position its sphere class equals the nearby
residual.P26 support. Their disk support classes differ. The inverse's
replacement by the exact negative residual.P26 is therefore another
recorded sphere/+I step. The final positive/inverse cancellation itself is
free disk-word cancellation. Trying either inverse with F11 alone misses
this match: the interaction with the other inverse is essential.

Eighteen records remain, all two-point supported. Seventeen are positive;
the last is the round Q56 inverse. The signed count upstairs is 32 positive
and two negative nonseparating units. It is NOT a positive (30,0) relation.
The full signed word fixes the five sphere arcs and has lift homology +I.
Removing Q56 inverse gives nonidentity homology, as required: equivalently
the positive records multiply to positive P56. This is the next target
equation, not a standard exterior-boundary identity or the full requested
structural (6,7) derivation.

One direct based-disk comparison of this endpoint with `(12345)^6` reached
the unchanged 400000-letter bound. Its disk equality to the full twist is
unknown. Do not use the signed count or the sphere identity to decide it.
The test of the new route likewise uses the exact sphere-chain certificate
instead of trying to derive a sphere certificate by first expanding that
large disk point-push. The local disk cancellation is checked independently.

Next investigate the positive equation (seventeen records)=P56 using
transported PC roses and half lanterns, or other exact local decompositions.
Keep the positive (26,2) checkpoint intact. Individual support pictures in
the graphical replay are not cumulative joint cut-complex certificates.

Validation: all 38 focused sphere-action, structure, and genus-two homology
tests pass. The replay has 171 route states and 143 distinct support entries.
One intermediate disk drawing reaches the existing 2048-cut-visit bound and
is explicitly unavailable; its following checked sphere representative and
the final state render successfully. The final three columns were visually
inspected with the unavailable entry, sphere-only rechart, exact cancellation,
and essential final red inverse all visible. No computation cap was raised.

## A positive replacement removes the inverse, but does not finish the short derivation

Richard correctly asked whether the last inverse really has to remain.
It is essential if the other seventeen records are kept unchanged and no
replacement is made; it is not an obstruction to a longer positive word.

Put A=43211234 and R=5 A 5, using positive Artin generators. The standard
sphere relator R is identity on the sphere, but its genus-two lift has
homology -I. Squaring it instead gives

```text
5^-1 R^2 5 = A 55 A 55 = 1,
T56^-1 = 5^-2 = A 55 A.
```

`positive_inverse_pair_sphere_relation()` checks this explicitly and saves
the free disk-word derivation from R squared, the nontrivial disk discrepancy,
the exact sphere outer-action certificate, and the +I lift discrepancy.
The disk exponent discrepancy is -20, so it is certainly not a disk equality.
This is labeled **SPHERE MOVE**. The tempting eight-letter replacement A
alone is sphere-equivalent but has the wrong genus-two lift; the test
requires that discrepancy to be -I, rather than silently accepting it.

The eighteen positive half-twist units on the right are displayed as twelve
half twists and three full pair twists. `three_root_positive_sphere_expansion()`
appends this substitution to the saved signed endpoint. It has 32 entirely
positive records and genus-two counts (50,0); the full five-arc sphere check
and separate +I homology pass. This is an optional enlarged intermediate.
It does not identify that positive word with a standard boundary relation,
prove a Hurwitz equivalence to a known fibration, or finish the requested
short factor-level derivation. The useful short equation remains W=T56.

Global conjugation alone cannot remove the negative sign: g T56^-1 g^-1 is
still an inverse twist. It also transforms every existing factor and target
together, so it does not create a new direct support equality between them.
A consistent upward fixed-neighbor sweep of the final inverse through all
seventeen positive records, including possible half-twist support matches,
finds no direct cancellation. This is not an exhaustive Hurwitz obstruction.

There is now a definite disk diagnostic beyond the earlier based-action
bound: act on the unbased boundary of disk arc 1--2 using
`supported_class(ConjugatedTwist(product(signed_endpoint),1,2))`. Its exact
cyclic class has 33984 letters, unlike the two-letter reference. An exterior
boundary twist fixes such interior curve classes, so the signed endpoint
is noncentral in B6. No global conjugation can turn it into a power of the
central exterior-boundary twist. The computed class is saved locally as
`.preview/final-inverse-disk-witness.json`; this diagnostic does not apply
a sphere move or alter any derivation state.

The two new regression tests pass, including the wrong-lift rejection and
the complete positive endpoint's sphere and homology checks. The graphical
replay has 173 route states and 146 support entries (the same single older
disk-preview limitation remains). A focused two-column page is generated
as `positive-expansion.html`; both columns were rendered and visually inspected.
Every sphere-only transition, including this expansion, is explicitly labeled.

## The positive fifty-unit factorization is recognized by classification

Richard suggested the split 6*5+5*4=50. There is a genuine standard 30+20
target, but the literal words need a lift check. Put

```text
W0 = (1234554321)^2,  length 20, lift +I,
W1 = (12345)^6,       length 30, lift +I.
```

The alternative (1234)^5 is sphere-trivial but has lift -I. Hence its product
with W1 also has lift -I and cannot equal our positive source in closed genus
two. The standard twenty-unit W0 is a squared palindromic sphere relator.

More strongly, the classification hypotheses are satisfied by our actual
fifty-unit source. Expanding each full pair twist into its two half-twist
units is a formal exact disk equality. All fifty resulting genus-two twists
are positive and nonseparating. The source's complete sphere action and
separate +I lift are checked. The replacement block explicitly contains each
standard generator zeta1,...,zeta5 after expanding its powers, so its image
generates the full S6, not merely one transitive orbit.

[Auroux, Theorem 9, page 5](https://arxiv.org/pdf/math/0204285), states the
Siebert--Tian result as a Hurwitz normal form W0^k W1^epsilon, epsilon in {0,1}.
The count 50 then forces k=epsilon=1. Consequently our enlarged positive
factorization is Hurwitz equivalent to W0 W1 in closed genus two; its fibration
is the standard twenty-plus-thirty fiber sum. This conclusion uses the theorem
AND its verified hypotheses, not the count or total action alone.

`positive_fifty_standard_recognition()` saves the expanded source, five explicit
generator witnesses, source sphere/lift checks, standard target checks, and
the theorem reference. It distinguishes theorem-implied equivalence from an
explicit route: `explicit_hurwitz_route_found` and the full structural-derivation
flag remain false. The graphical target blocks are separate REFERENCE panels,
with repetition counts, not additional derivation states or unlabeled moves.

The next task is constructive: expose the standard W0 block using the eighteen
already inserted positive units and two suitable earlier units, then identify
the thirty-unit remainder by explicit checked moves. Auroux's Lemmas 6--7 give
useful Hurwitz invariance under global conjugation and untwisting of these
standard blocks. The original (6,7) derivation is not declared finished solely
from this nonconstructive recognition, and no exact disk equivalence is claimed.

The targeted recognition regression passes. The graphical replay retains its
173 move states and adds two separate reference panels; it has 148 support
entries with the same one older disk-preview limitation. The focused standard
target page was rendered and visually inspected with its repetition labels,
theorem scope, and the literal five-strand lift warning visible.

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
