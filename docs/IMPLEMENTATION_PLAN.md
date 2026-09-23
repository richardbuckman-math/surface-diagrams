# Visualization-first development plan

Controlling plan, updated September 12, 2026. Richard's latest instruction makes
**all requested visualizations, including cut systems, higher priority than the
calculation engines**. The earlier R0-R7 calculation-led sequence is superseded.
The shared core/calculation/rendering separation remains useful, but building a
general exact core is not a gate before improving drawings.

Read the [tutorial](TUTORIAL.md), [architecture](ARCHITECTURE.md),
[research notes](RESEARCH_NOTES.md), and [handoff](HANDOFF.md). The older
[P0-P8 visual plan](archive/IMPLEMENTATION_PLAN-visual-cycle-2026-09-12.md) preserves
reference-specific acceptance criteria. Preserve all original reference SVGs.

## Active display scope (September 13)

Heegaard, bridge, trisection/relative, and Kirby diagram families are deferred
until Richard supplies a concrete use case. Do not implement or count them
toward completion of the core display work. V4 currently means export parity
and polish for surfaces, relations, braids and Lefschetz-fibration presentations.

## Surface spacing guideline (Richard's latest refinement)

Use roughly comparable visible widths for the strips between consecutive genus
holes, between a hole and the outer end, and between holes and the top/bottom
surface edges. Boundary openings should have a comparable visual scale. Exact
equality is unnecessary; avoid a squeezed strip next to an otherwise roomy
surface. In particular, a Type I end rim must not be pulled inward by an adjacent
top/bottom collar. Measure the strip from the rim's inner edge to the nearest
hole, and compare it with the inter-hole gap and opposite end clearance.

Immediate work: correct both ends and verify all four viewing directions,
including the current four-view gallery fixture, mixed boundaries and changed
proportions. Preserve boundary IDs, actual contour attachments and transparency.
A gently undulating top/bottom contour that follows the genus holes is a desired
minor refinement, explicitly lower priority than spacing, endpoint controls and
cut-system drawings. No exact scalloping amplitude is prescribed now.

After this correction continue V1-V3 visual work; calculation engines remain later.

Further confirmed presentation requirements: default above/right view; planar
reference cuts are straight consecutive symmetry-axis intervals, including the
outer end intervals (only the first starts at the left boundary); even genus
cuts closely follow the holes rather than large enclosing ellipses. Closed reference curves default to solid. The optional split style dashes rear
corridor halves; enclosing loops remain solid without invented transitions. Straight mark-to-mark visual arcs take precedence over the
bent diagnostic-disk projection when no explicit itinerary is being requested.
Keep explicit DiskRoute inputs faithful to their supplied itineraries.

## User-facing priorities

| Use case | Visual deliverable first | Calculation deliverable later |
| --- | --- | --- |
| 1: planar mapping classes | Arcs/loops, colored reference cuts and supplied images, intersecting families, vertical factors and adjacent braids | Automatic twist/half-twist actions, identity/equality checks and covering correspondences |
| 2: standard nonplanar surfaces | Standard rainbow cut systems, arcs/loops, all standard boundary placements, vertical supplied action states | Automatically act on a rigid reference system and compare products |
| 3: transformations of products | Before/after Hurwitz moves, substitutions and admissible cyclic shifts with explicit supplied factors | Compute transformed support curves and verify the relation/equivalence involved |
| 4: homology and fundamental group | Colored basis and supplied matrix/generator illustrations | Exact homology, basis changes, induced actions, fundamental-group presentations |
| 5: Lefschetz fibrations | Factorizations with vanishing-cycle labels and space for a calculation trace | Signature and other invariants under explicit fibration hypotheses |

Braids are also drawings: do not defer their visual representation until braid
normal forms are implemented. The same applies to manually specified factor
substitutions, cut-system images and cover correspondences.

## Visualization milestones

| Stage | Work | Acceptance gate |
| --- | --- | --- |
| V0: tutorial and immediate corrections | Runnable illustrated tutorial; remove the nonsensical extra handle arc; document actual input conventions and gaps | Every displayed recipe runs; no pretend calculation APIs; removed option absent from active gallery |
| V1: planar diagrams | Left/right boundary anchors for curved arcs, intersecting families, colored cut systems, labels and input previews | Point-to-point, boundary-to-point and boundary-to-boundary examples; standard endpoints at left/right rims; preserve route and color identities |
| V2: nonplanar diagrams | Finish standard Type I/II cut bindings and routes; smooth practical route drawing; more accessible numbered-side locators | All requested standard templates carry their cuts and curves with correct front/back geometry; both surface and cut-disk previews agree |
| V3: factors and visual transformations | Thesis-style vertical factor/action rows, adjacent braid/base/lifted views, supplied Hurwitz/substitution/cyclic-move sequences | Stable factor IDs, grouping and cut colors across rows; explicit multiplication convention; accurate supplied correspondences |
| V4: exports and display polish | SVG/TikZ parity for the core surface, braid and factorization visuals | Necessary labels, crossings and boundary data are retained; representability is distinguished from validity/equivalence |

V1-V3 can be improved incrementally together when a single worked example needs
them. Calculations must not pull effort away from unfinished requested visuals.
Each batch names a concrete drawing and its acceptance examples, rather than
attempting every future diagram family in one universal abstraction.

## What this tutorial delivery adds

- Eleven main SVG tutorial figures, one detailed cut-disk SVG and eleven TikZ counterparts; circular-hole
  figures also export to TikZ; CI compiles both the main and tutorial galleries.
- Optional planar ID/color legends and individual component panels alongside
  intersecting overlays are demonstrated in tutorial figures 04/05.
- `ColoredCurve` and `PlanarDiagram`: disjoint colored families by default;
  independently routed overlays with explicit `allow_intersections=True`.
- `BraidDiagram`: signed crossings with transparent underpass gaps and persistent
  strand colors/labels. This draws words; it does not solve equality.
- `Panel` and `Figure`: aligned columns and vertical rows, including mixed genus,
  planar, disk-chart and braid panels, using the existing exporters.
- Rainbow numbered genus cut systems. The old extra handle arc, its constructor
  option and gallery example are removed.

Current limitations are explicit: overlay mode does not certify pairwise
intersections and may produce coincident pieces; Type I/II route bindings
are unsupported. Mesh side IDs remain technical and chart-dependent. Automatic
mapping-class action, Hurwitz transformations, homology and signature engines
are not implemented by these presentation features.

V3 progress: `FactorPanel` and `FactorizationDiagram` now provide application-order
rows, stable factor IDs distinct from support curves, signed-power labels,
contiguous groups, complete supplied action-state columns and a continuous
adjacent braid with persistent strand identities. The default is bottom-to-top
with an explicit right-to-left product. Standalone braids also accept upward
traversal without mirroring crossing signs. Tutorial figures 16/17 and their
SVG/TikZ exports cover planar and bordered examples. These are supplied
presentations; automatic transformations and certified lifts remain later work.

Curved circular-boundary arcs now use exact left/right rim anchors, with optional
`start_side` and `end_side` controls and analytical endpoint-hole clearance checks.

## Next V3 task: optional Tiny Bubbles Lab braid display

September 22 checkpoint: the reference is now inspected in the in-app browser.
Smooth cubic crossings with vertical joins and split underpasses are available
through `crossing_style="smooth"` and factor-panel `braid_crossing_style`.
Tutorial figure 20 compares styles. Remaining parts of the observed display:
generator labels, atom highlighting, endpoint badges, scroll/zoom controls,
and optional editor integration. Implement these incrementally; the first
geometry option does not claim to reproduce the complete reference UI.

The September 22 scheduled batch exposes Straight/Smooth in the local editor.
Its selected value, undo/redo and both traversal directions were browser-checked;
controller coverage includes old recipes and JSON save/reopen. Generator labels
and atom highlighting remain the next static display increments.

Richard requested this additional braid-display option on September 21:
[Tiny Bubbles Lab, simplified crossing audit, factor 5](https://tiny-bubbles-lab.joshgay.chatgpt.site/research-journal/2026-09-09-simplified-crossing-audit/#factor-5).

Schedule this with the next braid/factorization visualization work, ahead of
calculation engines. First inspect the referenced factor-5 display and its
available implementation to identify the geometry, crossing treatment, labels,
and any interaction it actually uses. Retrieval was blocked (HTTP 403 and browser
tool failure) when this task was recorded; do not infer its design from the URL.

Implement the observed presentation as an optional braid view, retaining the
existing display default. Reuse signed braid words, strand identities/colors,
application direction and factor IDs, so the same data can drive both views.
Include it in standalone braid examples and adjacent factorization panels where
appropriate. Confirm sign and endpoint conventions against the reference, and
show both display options in the tutorial. Verify SVG/TikZ parity for static
features; document any interactive-only behavior explicitly. Check reuse rights
before incorporating external source or assets. This is a rendering task, not
a request to add automatic braid simplification or equality calculations.

## Endpoint and identity requirements

Most ordinary arcs join marked points. Cut systems additionally need
boundary-to-point and boundary-to-boundary arcs. Standard boundary attachments
should be at the leftmost/rightmost rim positions, not top/bottom. Nonstandard
configurations may later request arbitrary explicit anchors. Treat a circle
rim, a dot marker and a notched boundary as different endpoint conventions.

Keep stable cut IDs and rainbow colors across supplied action states; do not
reassign a cut's color from its changing position or endpoint order. Labels remain
necessary for larger systems. Factor identity is separate from its support curve,
exponent, product, and its position in the displayed sequence.

A drawing of a twist-support curve does not apply the twist. A caption does not
prove identity. The image-of-reference-system/torsor idea remains the proposed
future equality mechanism when its stabilizer is proved trivial, with a supported
isotopy/normalization algorithm. An ordinary Heegaard meridian system does not
have that rigidity merely because it is called a cut system.

## Later calculation roadmap

| Stage | Input and deliverable | Required care |
| --- | --- | --- |
| C1 | Exact curve actions, braids, mapping classes and reference-system images | Declare endpoint/isotopy conventions and supported normalization domains; compare known relations and nontrivial actions |
| C2 | Hurwitz/substitution checks, factorizations, general cover/lift machinery | Distinguish same product, conjugacy and Hurwitz equivalence; cyclic shifts need conditions; liftability and boundary admissibility are separate |
| C3 | Homology, basis changes and surface fundamental-group presentations | Exact integer matrices, basepoints, ordered oriented bases and retained versus removed marked points |
| C4 | Lefschetz signature and related invariants | Oriented fiber/base, vanishing cycles, signs, global monodromy and completion data; begin with a referenced algorithm and known examples |

Signature computation is a concrete algorithmic prospect, not a promise that
arbitrary factor lists specify a Lefschetz fibration. Ozbagci and the
Cengel-Karakurt reformulation are candidates recorded in RESEARCH_NOTES.md.
Computing a presentation for a specified surface fundamental group is feasible;
recognizing arbitrary 4-manifold groups is a separate problem and not promised.

## Architecture and research that remain useful

Keep one repository and distribution, with core records shared by rendering and
calculation. Introduce records only as actual drawings/operations need them; avoid
a package-wide move or a plugin framework. Coordinate investigations (normal
strands, Dehn-Thurston, Dylan Thurston's note) can inform future contracts without
blocking present visualization work. Richard's separately reported work is still
to be located; do not overwrite it or claim to have reviewed it.

Preserve the notched-boundary proposal: allowed fractional rotations can admit
lifts excluded by pointwise-fixed boundary conventions. Retain full twist and
endpoint transport, and specify isotopies before asserting a relation. Covers may
have arbitrary genus bases and marked points; separate their eventual computation
from a supplied diagram of a concrete example.

Heegaard/trisection systems reuse surface curves; bridge and Kirby diagrams also
need tangles/crossing/framing data. Relative versions need explicit structures,
not a universal `relative=True`. Their visualizations do not require automatic
manifold recognition or a move-search engine.

## Checks and completion discipline

Preserve reference geometry, topology, transparency and endpoint requirements.
Run relevant tests and inspect regenerated images. Verify TikZ only after SVG
geometry is correct; compile examples when a TeX toolchain is available. Keep
unsupported cases explicit. Continue scoped commits and pushes under Richard's
standing authorization, and update HANDOFF.md with actual progress.

## Surface-slice convention (September 22, supersedes cusp-plane styling)

Arcs and curves must remain within the surface outline. An arc may cross a
curve but cannot end in its interior. Type I handle-return arcs use front/rear
rim points. Type II connections form continuous boundary-to-boundary perimeter
arcs, including the side-pair arc crossing the outer closed loop. Marks split
these arcs: a lone mark lies on the axis, paired marks above/below. Closed curves
may be solid; visibility changes must occur only at actual silhouette edges.

### Earlier incremental checkpoints (superseded by the current status below)

Boundary-plane progress: exact named rim attachments and their labeled guide are
implemented in all views. Next bind connecting reference arcs and marked-point
spokes to those attachments, then complete the bordered cellulation.

Type I end-boundary reference families are now drawn by `with_reference_arcs()`.
Next extend to fixed boundaries at genus cusps, then Type II arcs and marks.
The checked bordered mesh is still a separate unfinished requirement.

All Type I slots now have supplied vertical-plane reference-family drawings.
Next: Type II boundary connections and marked-point spokes; certified bordered
mesh bindings remain distinct from these presentation diagrams.

Standard top/bottom Type II spokes and one inner-bank pair per side now have
supplied drawings. Remaining boundary variants and marked-point spokes must be
bound explicitly; the reference renderer no longer relies on a closed mesh.

### Current boundary presentation status, September 22

`with_reference_arcs()` now follows the surface-slice convention: front/rear
Type I attachments, continuous inward-offset perimeter arcs, automatic axial
and paired marks, and solid enclosing loops. The split option retains rear
corridor dashing only. Explicit supplied mark coordinates remain supported.
Selection, labels, SVG and TikZ share the same geometry. Figure 15 is rebuilt.

The checked closed-surface `GenusDiagram` now shares the solid/split reference
style while preserving mesh walks, labels and explicit DiskRoute visibility.
Next: migrate its mesh-bound mark display to the symmetry convention while
preserving its abstract cellulation and explicit DiskRoute endpoints. Add an edge-crossing version of enclosing loops if a split
wrap display is needed; never reuse the old arbitrary cusp-plane transition.
Repeated pairs on one side, a Type I rim sharing an end with a Type II pair,
general bordered DiskRoutes and the certified bordered mesh remain unfinished.

### Braid annotation progress, September 23

Optional right-hand signed generator labels now work for standalone and
factor-aligned braids in both traversal directions and SVG/TikZ. Python options:
show_generators and braid_show_generators. Recipe/editor controls and atom
highlighting are next; they do not depend on the mathematical action engine.
