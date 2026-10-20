# Common nets: triangle panels, then six and seven cubes

This independent experiment does not import the mapping-class or surface
rendering package. Richard asked for a triangular analogue of Cubigami, working
up by volume, then common nets for six and seven cubes. One volume unit here is
a **regular tetrahedron**, glued to others along whole faces. Triangle-cluster
mirror pairs are identified; the net may be turned over.

## Checked findings, 20 October 2026

| Tetrahedra | Exterior triangles | Shapes, mirrors identified | Nets used to cover all |
|---:|---:|---:|---:|
| 1 | 4 | 1 | 1 |
| 2 | 6 | 1 | 1 |
| 3 | 8 | 1 | 1 |
| 4 | 10 | 3 | 1 |
| 5 | 12 | 7 | 1 |
| 6 | 14 | 23 | 2 |

The five-unit net has a branching hinge tree; no ribbon net covers all seven.
It is a rediscovery of [Mabry's published five-unit net](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common8V.html),
not a new construction. The exact paper pattern and fixed hinges match.

The complete catalog now extends through **eight** tetrahedra: **89** shapes at
seven units and **398** at eight, for **523** shapes altogether through eight.
`extend_tetrahedra.py` samples 500 source spanning trees per new volume and
checks each retained candidate against every shape using both folding kernels
and exact face/hinge certificates. Selected seven-unit nets cover **40** and
**36** shapes; eight-unit nets cover **101** and **98**. These are useful
examples, with no optimality claim; the two nets at each volume are not claimed
to cover that volume's entire catalog.

`build_tetrahedra_atlas.py` now produces a **73-page** puzzle book with linked
contents. Puzzles come first: cool net colors and independently randomized warm
target colors hide the face correspondence. Solutions repeat the same targets
with the original matching colors. The complete 523-shape catalog follows.
Stable shape IDs link all three sections. The PDF embeds exact JSON data and
a page manifest. Its offline gallery contains 1,187 SVGs and rotatable targets;
solutions start collapsed. Fixed internal slits are explicitly marked in red.
The previous 49-page atlas remains available as an earlier output.

The static browser game at `game/index.html` has all **321 net/target
challenges** from the selected 11 nets. Drag each camera independently;
double-click a hinge and scroll, or use its key pair / slider / buttons.
Shift supplies the last four pairs on 17-hinge nets. Snapping steps through
polytet crease angles; undo/redo and browser-local progress are included.
Show solution animates the verified fold and reveals matching colors without
earning a solved mark. The site build publishes it at `/tetrahedra/`.

`build_game.py` checks the original exact mappings and prepares numerical
meshes and signed crease angles. Rendering-free `geometry.mjs` reconstructs
all 321 targets in tests, preserving rigid panels and both hinge endpoints.
Success tests whole triangle surfaces up to rigid placement, panel reassignment
and reflection, with a 0.012-edge-length vertex tolerance. It does not require
the particular stored solution. Continuous panel collisions remain unmodeled.

The optimized six-unit **single-net maximum is 19 of the 23 shapes**. A second
net covers 14, including the four missing from the first; together they cover
all 23, with ten shapes supporting both. The earlier ribbon/branching pair
(15 and 13) remains in the generated historical data.

`optimize_six.py` proves the 19 bound by exhaustively handling four source
catalogs, totaling 104,201 spanning trees. Every net of each selected source
covers at most 19 targets. A net covering none of those four sources can
cover at most the remaining 19. This partitions all possibilities and, together
with the positive 19-target certificate, establishes the optimum in this model.
The second geometric implementation in `audit.py` agrees with the six-unit
bound and finds the unique five-unit fixed-hinge net in its 6,000 source trees.
The four-unit comparison is now reconciled with Mabry's complete catalog:
37 shared outlines give 47 fixed-cut variants. His pictured 16 are the subset
exclusive to the three tetrahedron-cluster types, with one variant each.
`catalog_compare.py` validates all 448 catalog entries and the pictured IDs.
See [the novelty/audit note](../../docs/proofs/common-net-novelty.md) before
making any claim of novelty; no six-unit publication priority is established.

In this **rigid triangular-panel, whole-edge hinge model**, no single net can
cover all 23 six-unit targets. This is a finite computational result, not a
claimed literature theorem. A second, independently implemented enumeration
checks every one of the 25,645 spanning trees of one target's dual graph:

* 9,316 overlap in the triangular lattice.
* Each of the remaining 16,329 fails at least one target after every root face,
  rotation, and choice of paper side is tried.
* The number of independently enumerated trees equals the exact Kirchhoff
  determinant. There are no duplicate tree masks.

Any connected common edge net can have hinges removed to leave a tree, so the
enumeration includes nets with additional hinges too. A tree is unfolded with
one fixed source face and orientation; all other placements differ by plane
isometries. Target foldings are forced once a root face flag is chosen. The
source and seven rejecting targets already give an eight-shape obstruction.
The full rejection list is in generated `six-unit-obstruction.json`.

Every positive certificate is checked by a separate face/edge verifier. It
requires a bijection onto all exterior faces, exact agreement at both endpoints
of each hinge, and no repeated planar triangle. Cluster geometry, congruence,
reflection and separating-axis tests use integers. Denominator `3**10` is a
coordinate representation, not a geometric approximation.

These checks establish **folded end states**, not continuous collision-free
folding motions. Extra creases inside triangle panels, stretching, hidden
layers and overlapping panels are excluded. No manufacturing allowances or
glue tabs are supplied.

## Cube results and remaining gap

The online game now includes **35 cube nets and 796 net/target challenges**,
alongside the original 321 tetrahedron challenges. Choose **Cubes / Cubigami**
in the family selector. The classic four-cube Cubigami7 outline uses a checked
fixed tree-hinge adaptation with internal cuts and covers all seven tree-shaped
tetracubes. The published five-cube patterns cover 23, 22, and 11 targets;
together they cover all 27 tree-shaped pentacubes. Further alternatives and
selected spatial examples extend to eight cubes. The eleven standard single-
cube nets are all included. No commercial hardware or source photographs are
redistributed.

`build_cube_book.py` produces the companion **113-page** cube book with linked
contents, independent puzzle colors first, and matching-color solutions last.
All 35 nets and every one of their 796 targets occur in both sections. Net IDs
and target IDs match the game; each net page links directly to its online
puzzle. The PDF embeds the exported collection and a lossless page manifest.
It is published at `docs/puzzles/cubes-cubigami-puzzles-and-solutions.pdf`;
the earlier tetrahedron book remains unchanged.

| Cubes | Tree-shaped catalog | Planar tree shapes | Included nets | Distinct targets represented |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 11 | 1 |
| 2 | 1 | 1 | 2 | 1 |
| 3 | 2 | 2 | 2 | 2 |
| 4 | 7 | 4 | 2 | 7 |
| 5 | 27 | 11 | 4 | 27 |
| 6 | 138 | 27 | 4 | 36 |
| 7 | 822 | 83 | 4 | 86 |
| 8 | 5,154 | 255 | 6 | 265 |

Across the included nets, **every planar tree-shaped cluster through eight
cubes is available**. This is a collection, not a single universal unfolding.
The two broad eight-cube nets cover 241 and 237 targets; source-specific
supplements cover the remaining two planar types. A bounded 15-second common-
net search for that pair did not finish a common construction; two individually
checked nets complete the collection instead. Do not infer nonexistence.
Non-planar coverage at six through eight remains partial.

`cube_puzzles.py` enumerates proper-rotation classes, verifies each retained
fold map exactly, transcribes the published outlines, and samples larger
source trees. `python -m experiments.common_nets.build_game --cubes` exports
the browser data. Its family index and individual net files load on demand;
entering a cube link does not load the tetrahedron collection. Square panels
use quarter-turn stops; triangle stops are preserved. Cube chirality is
distinguished by the success test. Print current flat patterns with **Download
net SVG**, including the fixed red internal cuts and blue hinges.

Python tests independently regenerate all planar polyominoes through eight,
filter their adjacency trees (counts 1,1,2,4,11,27,83,255), and compare them with
the game. Every exported target is checked as exactly the exterior of its
connected integer cube cluster. Node tests reconstruct all 1,117 cube/triangle
foldings from their hinge angles and preserve every endpoint and panel edge.

The classic-source drawings are in Aloupis et al.'s
[full paper](https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf)
(Figure 3 and Section 3.3) and
[earlier version](https://erikdemaine.org/papers/Cubigami_CGGA2010/paper.pdf#page=2)
(the explicit 23-target pattern). Source geometry is credited; target coverage
is recalculated, rather than copied from captions with different conventions.

Cube shapes are counted up to the 24 proper rotations; chiral twins count
separately. The full enumerator reproduces 1, 1, 2, 8, 29, 166, 1023 through
seven cubes. Restricting to face-adjacency trees leaves 138 six-cube and 822
seven-cube shapes, with 26 and 30 exterior squares respectively.

An exact-cover search in straight-spine, paired-foot families finds:

* A 26-square net for **all 27 planar six-cube trees**.
* A 30-square net for **79 of the 83 planar seven-cube trees**.

A supplementary 30-square net covers 28 planar seven-cube trees, including
the four missing from the first. The two nets together cover **all 83 planar
seven-cube trees**, with overlap 24. Generate its separate illustrated page
and exact certificates with `python -m experiments.common_nets.complete_planar_cubes`.
The original seven-page atlas remains unchanged.

These do **not** solve the complete three-dimensional problems. All displayed
cube targets have full face/hinge certificates. Two bounded general searches
used a straight bar and four nonplanar targets: each timed out at 75 seconds
(998,912 and 766,464 nodes) without a common net. This is not evidence of
impossibility and must never be presented as such.

Next try a constructive multi-band family or transported common-net extension
that can fold into nonplanar clusters. Do not merely repeat the same timed-out
five-target search or call the planar family a solution of the full problem.

## Reproduce

Use Python with `reportlab` and `pypdf` for the atlas; the calculation engines
use only the standard library. From the repository root:

```powershell
python experiments/common_nets/engine.py --maximum 6
python experiments/common_nets/verify_six.py
python experiments/common_nets/optimize_six.py
python experiments/common_nets/cubes.py
python experiments/common_nets/build_gallery.py
python -m experiments.common_nets.audit
python -m experiments.common_nets.extend_tetrahedra --attempts 500
python -m experiments.common_nets.build_tetrahedra_atlas
python -m experiments.common_nets.build_game
python -m experiments.common_nets.build_game --cubes
python -m experiments.common_nets.build_cube_book
node --test tests/common_net_game.test.mjs
node --test tests/cube_fold_game.test.mjs
```

The optional, bounded general search is
`python experiments/common_nets/cube_general_search.py`.

Outputs are in `.preview/common-nets/`, the illustrated PDF is under
`output/pdf/`, and the offline gallery archive is
`output/common-nets-gallery.zip`. Blue dashed lines are hinges; black boundaries
and red internal slits are cuts. Open `index.html`; clicking a target opens the
rotatable WebGL mesh. It needs no internet connection or third-party runtime.
Downloadable SVG images remain available when WebGL is unavailable.

The revised one-through-eight deliverables are
`output/pdf/tetrahedra-puzzles-and-solutions.pdf` and
`output/tetrahedra-puzzles-and-solutions-gallery.zip`. The published PDF is
copied to `docs/puzzles/`. The extension reads the
existing optimized one-through-six data, preserving those earlier certificates;
it writes `.preview/common-nets/tetrahedra-through-eight.json` separately.

## Primary references

* Aloupis et al., [Common Unfoldings of Polyominoes and Polycubes](https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf):
  Cubigami, nonexistence of a net for all pentacubes, and a common net for all
  planar six-cube trees. One-sided/two-sided and chirality conventions must not
  be mixed. The abstract and full-text counting conventions differ; use the
  precisely defined generated catalogs for this experiment's denominators.
* [Rick Mabry's four-tetrahedron common nets](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common.html):
  earlier common nets of all three four-tetrahedron types.
* [Rick Mabry's twelve-face common nets](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common8V.html):
  the already known net for all seven five-tetrahedron clusters, and the
  important distinction between fixed cuts and cuts changed between targets.
* [George Sicherman's polytet catalog](https://sicherman.net/polytets/index.html):
  independent small-cluster counts, matching our enumeration through eight.
