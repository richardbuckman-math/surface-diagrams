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
The optimized six-unit **single-net maximum is 19 of the 23 shapes**. A second
net covers 14, including the four missing from the first; together they cover
all 23, with ten shapes supporting both. The earlier ribbon/branching pair
(15 and 13) remains in the generated historical data.

`optimize_six.py` proves the 19 bound by exhaustively handling four source
catalogs, totaling 104,201 spanning trees. Every net of each selected source
covers at most 19 targets. A net covering none of those four sources can
cover at most the remaining 19. This partitions all possibilities and, together
with the positive 19-target certificate, establishes the optimum in this model.

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

Cube shapes are counted up to the 24 proper rotations; chiral twins count
separately. The full enumerator reproduces 1, 1, 2, 8, 29, 166, 1023 through
seven cubes. Restricting to face-adjacency trees leaves 138 six-cube and 822
seven-cube shapes, with 26 and 30 exterior squares respectively.

An exact-cover search in straight-spine, paired-foot families finds:

* A 26-square net for **all 27 planar six-cube trees**.
* A 30-square net for **79 of the 83 planar seven-cube trees**.

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
```

The optional, bounded general search is
`python experiments/common_nets/cube_general_search.py`.

Outputs are in `.preview/common-nets/`, the illustrated PDF is under
`output/pdf/`, and the offline gallery archive is
`output/common-nets-gallery.zip`. Blue dashed lines are hinges; black boundaries
and red internal slits are cuts. Open `index.html`; clicking a target opens the
rotatable WebGL mesh. It needs no internet connection or third-party runtime.
Downloadable SVG images remain available when WebGL is unavailable.

## Primary references

* Aloupis et al., [Common Unfoldings of Polyominoes and Polycubes](https://erikdemaine.org/papers/Cubigami_CGGA2010full/paper.pdf):
  Cubigami, nonexistence of a net for all pentacubes, and a common net for all
  planar six-cube trees. One-sided/two-sided and chirality conventions must not
  be mixed. The abstract and full-text counting conventions differ; use the
  precisely defined generated catalogs for this experiment's denominators.
* [Rick Mabry's four-tetrahedron common nets](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common.html):
  earlier common nets of all three four-tetrahedron types.
* [George Sicherman's polytet catalog](https://sicherman.net/polytets/index.html):
  independent small-cluster counts, matching our enumeration through six.
