# Handoff: surface-diagrams

## Mesh migration dependency clarified, September 25

Inspected genus_mesh mark-site selection and mesh_marks.mark_mesh. The earlier
next-step wording understated the task: spokes are registered ParentCuts and
Attachments, not display decorations. Existing certification explicitly depends
on them. Updated the implementation plan with the required separate certified
perimeter system and route conversion, and the tutorial with the distinction
between auxiliary chart cuts and valid curve-complex arcs. Use reference arcs
for presentation; retain the old atlas for existing DiskRoutes. No geometry was
changed. Next substantive step: design the perimeter system's parent endpoint
incidence and cut-disk topology before changing mark coordinates.

## Mesh endpoint migration guard, September 24 evening

Added a final-drawing regression covering explicit P-to-Q and Q-to-P DiskRoutes
in all four genus-two views. It compares rendered path endpoints to the rendered
mark centers and verifies continuity between path pieces. The older test only
compared projection coordinates in the default view; this protects the boundary
between mesh projection and display during the planned migration. All five
genus-mark tests pass (24 seconds). Visually inspected a four-view route sheet
in .preview/mesh-mark-endpoints.svg/png. No rendering behavior changed: marks
still use the legacy upper band, and the symmetric placement work is unfinished.
Next: change the mesh embedding and mark vertices together, retaining these
endpoint/continuity checks and the existing certified-complement checks. Do not
replace displayed marks independently of explicit route endpoints or merely
hide reference spokes. Usage 72% to 73% weekly; preserve the 15% reserve.

## Signed braid reading gallery, September 24 midday

Added figure 22 with the same non-palindromic signed word (1,-2,-1) drawn
downward and upward. Smooth crossings, signed labels and endpoint identities
make the fixed upper-end crossing convention visible. Tutorial includes a
runnable comparison and explains that upward traversal does not invert signs.
Regenerated 22 SVG/TikZ examples and the TeX gallery; visually inspected figure
22. Eight visualization tests, tutorial HTML build and site/local-link checks
pass. No library behavior changed. Usage 70% to 71% weekly, 2% to 6% five-hour.
Next core work remains coherent mesh-mark/reference-spoke migration; optional
braid atom highlighting remains pending. Keep deferred diagram families deferred.

## Reproducible placement troubleshooting, September 24 morning

Added a runnable tutorial example for the explicit perimeter opening guard:
the invalid two-mark placement prints the expected error, and a corrected
upper/lower placement saves a valid SVG. Explains render-time validation,
stroke clearance, automatic placement and the difference between a rejected
drawing and an impossible abstract arc. Executed the exact Markdown code;
visually inspected the corrected SVG through a white-background raster.
Regenerated tutorial HTML; site build and local-link checks pass. No library
code changed. Prior db985b8 Tests and Documentation workflows both succeeded.
Next: migrate mesh-bound marks and reference spokes coherently with explicit
route endpoints; do not move marks cosmetically while retaining old endpoints.
Usage moved from 69% to 70% weekly and 1% to 4% five-hour; this small documentation
batch preserves the weekly reserve and remaining six-hour run shares.

## Explicit perimeter opening guard, September 24

Fixed a reproduced rendering error: on genus two with Type I boundary 6,
P=(8,-9), Q=(-97,0.5) are legal marked endpoints, but the deformed solid
perimeter entered the left genus opening. Explicit placements now validate
all perimeter segments against handle curves using conservative cubic error
bounds and half the curve stroke width. Crossings/touches/insufficient clearance
raise an explanatory ItineraryError; no route is silently moved. Bounding-box
rejection keeps checks cheap. Automatic perimeter placement is unchanged.

Sixteen reference tests pass, including this regression in all four views;
nine supplied marked-arc tests also pass. Tutorial regeneration leaves the
21 SVG/TikZ fixtures unchanged. The pre-fix reproduction and valid tutorial
mark drawing were visually inspected. All 228 Python tests pass (126 seconds); the
tutorial HTML and site build pass, including local-link checks.

The previous v0.1.0a4 release is confirmed published with wheel/source assets;
its Release, Tests and Documentation workflows passed. This fix is Unreleased.
Next: mesh-mark/reference-spoke migration remains open. This guard is only for
explicit perimeter deformations, not a global clipping or bordered-mesh solution.
Usage began 65% weekly / 4% five-hour, reached 68% / 23%; stop at this checkpoint
to preserve remaining scheduled shares and the 15% weekly reserve.


## Versioned alpha release batch, September 23 afternoon

Prepared 0.1.0a4: synchronized pyproject.toml, release-page version and release
instructions. Rewrote the release notes around the completed editor, ordered
factor panels, supplied action states, smooth/labelled braids, perimeter arcs,
symmetric reference marks and 21-example gallery. Documented changed perimeter
member numbering and solid defaults, and retained explicit mesh/catalog limits.

Local validation: 227 Python tests, 10 editor-controller tests, regenerated
21 SVG/TikZ tutorials without fixture changes, rebuilt site/local link check,
and visual inspection of the release page. No library geometry changed.
The local Python lacks the build frontend; the existing release workflow builds
wheel/source archives and validates metadata using build/twine on Python 3.12.

Publishing sequence: push version commit, verify Tests and Documentation CI,
then tag v0.1.0a4 and verify the Release workflow plus wheel/source assets at
https://github.com/richardbuckman-math/surface-diagrams/releases/tag/v0.1.0a4 .
If interrupted, inspect that exact release before retrying; never move a tag.
Next development: mesh-bound mark/reference-spoke presentation remains primary
surface work; supplied braid atom highlighting is the next braid refinement.
Keep Heegaard/bridge/trisection/Kirby deferred. Usage began at 59% weekly, 0%
five-hour; midpoint 60% / 7%, preserving the 15% reserve. No reset credits used.


## Symmetric marked-surface gallery, September 23 morning batch

Added tutorial figure 21 (SVG and TikZ): closed genus-two reference drawings
with one axial mark, a symmetric pair, and an axial mark plus pair, from above
and below. Reference numbers are hidden to focus the comparison on marks.
Tutorial gives executable recipes, selection for marks-only drawings, and
explains that this reference presentation does not migrate mesh-bound marks
or convert explicit DiskRoutes. No library geometry or certified topology changed.

Fifteen boundary/reference tests pass. New regression covers every automatic
mark count for genus 1-3 in all four views: symmetric pairs, axial odd mark,
member counts and exactly two perimeter incidences per mark. Regenerated all
21 tutorial figures, visually inspected figure 21, rebuilt tutorial HTML and
site with local links checked. git diff --check passes.

Next surface increment: resolve how the checked mesh display exposes its legacy
mark spokes without presenting them as the requested curve-complex reference
family; do not move explicit route endpoints. Atom highlighting and releases
remain separate outstanding work. Usage began at 55% weekly / 0% five-hour;
30 percentage points above the reserve shared across about 12 remaining runs.


## Editor generator-label toggle, September 23

Added Show generator labels below Crossing style in the braid editor. It reads
and writes braid.show_generators, defaults off for old recipes, preserves the
signed word and supports undo/redo plus save/reopen. Ten controller tests pass.
Verified the real checkbox and smooth labelled braid in the local editor on
port 8765, including a negative generator. Tutorial instructions updated.
The preceding recipe-schema fix f442f2d passed all GitHub jobs (Python 3.9/3.12,
controller, LaTeX and documentation); its local suite passed 226 Python tests.

Next: supplied atom highlighting for the optional braid view, or the separately
tracked mesh-mark migration. Keep exact DiskRoute endpoints unchanged during
surface presentation work. Check remote CI after every pushed batch.


## CI recipe-schema regression fix, September 23

User reported failed Tests run 35814966482 on b854881; Documentation deployed
successfully. Reproduced locally: 225 tests, three errors and one failure,
all from `braid: unknown fields ['show_generators']`. BraidDiagram's new field
was serialized by dataclasses.asdict, but documents._normalize still rejected
it. The earlier focused visual tests missed this integration dependency.

Added optional boolean show_generators to braid recipe validation and passed it
through construction. Old recipes default false; new ones retain the option.
Regression covers old/new JSON round trips, rendered inverse label and invalid
values. Document tests (25), editor-controller tests (9), and the full Python
suite (226 tests) pass locally. Remote CI will be checked after pushing.

Future additions to serialized drawing dataclasses must check recipe schemas,
round trips and generated Python, not just geometry tests. Next feature remains
the editor checkbox; recipe persistence is now implemented.


## Optional braid generator labels, September 23 scheduled batch

Added BraidDiagram(show_generators=True) and
FactorizationDiagram(braid_show_generators=True). Plain-text sN / sN^-1 labels
sit to the right of each actual crossing in traversal order. They work with
straight/smooth crossings and both directions, skip empty blocks/connectors,
and reserve horizontal space in SVG/TikZ. Defaults leave existing output alone.
No strand paths, colors, signs, endpoint identities or words change.

Validation: 28 focused visual/factorization tests pass, including mixed signs,
multiple-digit indices, both directions/styles, unchanged standalone paths,
label alignment in factor rows, identity blocks and boolean validation.
Regenerated tutorial figure 20 and its TikZ counterpart; visually inspected it
and a factor-aligned example with positive, identity and negative blocks.
Rebuilt tutorial HTML and site; local links and git diff --check pass.

Next braid increment: recipe persistence and editor toggle for generator labels;
then supplied atom highlighting. Mesh-bound mark symmetry and invalid reference
spokes remain the separate larger surface-display task from the last checkpoint.
Do not move explicit DiskRoute endpoints as a cosmetic shortcut.
Usage: 46% weekly / 0% five-hour used at start; 47% / 7% at midpoint.
About 39 weekly percentage points remained above the reserve for roughly 13
six-hour runs. Stopped after one bounded increment; no reset credits used.


## Closed-surface reference visibility, September 22 evening batch

Extended solid-default closed reference styling to GenusDiagram, exposed through
with_cut_system(closed_curve_style="solid"|"split") and with_curves(...).
Split retains the mesh's rear corridor halves; enclosing loops stay solid.
Removed the arbitrary cusp-plane splitter. Styling preserves every directed
mesh segment, labels, mark positions, parent numbering and explicit DiskRoute
output. Chained with_curves retains the chosen style.

Validation: focused tests cover all four views, segment/label preservation,
option validation and unchanged explicit route output. Regenerated genus-chain,
named-member and tutorial SVG/TikZ assets; inspected the genus 1/2/3 tutorial
raster on white. Tutorial HTML and site/local links rebuilt. Unrelated route
asset regeneration produced tiny numeric differences, which were discarded.
The full Python suite passed (223 tests); git diff --check passed.

Next bounded step: design the migration of mesh-bound marks and reference arcs
to symmetric perimeter/axial positions without moving explicit DiskRoute endpoints
or misrepresenting the checked cut system. This batch changes visibility only;
old mesh mark spokes and stroke-edge clearance are still outstanding.
Usage at start: 43% weekly used, 0% five-hour used; mid-batch 44% and 8%.
Rough run allowance was about three weekly percentage points (42 available
above the reserve, about 14 six-hour runs until reset). No reset credits used.


## Surface-slice reference drawings, September 22 user correction

Richard clarified figure 15: keep curves inside the outline; no arc ends in
another curve's interior; use front/rear Type I attachments; connect Type II
boundaries along the perimeter; place an unpaired mark on the axis and paired
marks symmetrically above/below. Visibility changes belong at real edges.
This supersedes the historical cusp-plane and spoke conventions below.

Implemented in `with_reference_arcs()`: replaced all Type II/mark spokes by
continuous inward-offset contour paths terminating only at rims or marks.
The left-pair arc crosses the end loop continuously; figure 15 has three top
and three bottom connections plus the left connection split at axial M.
Type I return arcs meet front/rear rim extrema. Closed loops default to solid;
`closed_curve_style="split"` dashes rear corridor halves, while enclosing loops
remain solid because their present geometry never crosses an edge. Automatic
mark pairs share x coordinates. Explicit supplied coordinates are preserved,
with local perimeter deformation and validation. Straight supplied MarkedArcs
retain their clear-band guard. Reference numbers after 2g+1 now identify the
perimeter segments; callers should query member_numbers instead of old IDs.
`pair_bank` remains accepted for compatibility but no longer chooses spokes.

Validation: 222 Python tests passed; nine supplied marked-arc tests passed again
after restoring the convex-band guard. Updated tests check front/rear rim
endpoints, continuous side connections, mark incidence, symmetry, closed-loop
visibility, selection and sampled containment in the actual outer silhouette.
Regenerated SVG/TikZ tutorials, visually inspected figures 13 and 15 on white,
rebuilt tutorial HTML and site, and passed the site's local-link validation.
`git diff --check` passed. The containment test checks path geometry at default
styles, not a universal stroke-clipping certificate for arbitrary custom styles.

Next: migrate the separate checked closed-surface `GenusDiagram` presentation
(its old cusp-plane visibility and mesh mark placements) to the same visual
convention without altering the abstract cellulation or supplied DiskRoutes.
If split enclosing loops are wanted, design paths that actually reach silhouette
edges; do not restore arbitrary dashed transitions on the current ellipses.
The certified bordered mesh and general bordered DiskRoutes remain unfinished.


## Editor crossing-style selector, September 22 scheduled batch

Added Straight/Smooth to the local editor's braid controls. Older recipes with
no crossing_style show Straight; changing style preserves the signed word.
Undo/redo and save/reopen retain the choice. Nine controller tests pass, including
the new backward-compatibility/history/save regression. Browser-verified the
actual selector, smooth rendering in both traversal directions, and undo/redo
against the local Python server. This verifies this flow, not the entire editor
manual acceptance checklist. No Python geometry changed in this batch.

Next bounded increment: optional right-hand generator labels for standalone
and factor-aligned braids; then supplied atom highlighting. Preserve export
parity and keep annotations independent of mathematical equality checking.


## Paced continuation and smooth braid crossings, September 22

Recurring continuation is active every six hours in task
01a09c1a-c080-7ed2-900a-739fd9cd2c0a. Read account usage at each run; reserve
15% weekly for interactive use and share the remainder across scheduled runs
until reset. Do not consume reset credits. Continue one bounded useful batch.

The braid derivation is complete as an explicit local-move certificate in
`.preview/braid-six-seven-proof.html`, with JSON and a complete move table.
An independent verifier checks the supplied SVG transcription and all 2,486
elementary moves (19 sphere substitutions), without a normal-form oracle.
Endpoint: `(sigma_4 sigma_5)^3 (sigma_1 sigma_2)^-3`, two complementary triple
twists. This is identity in the sphere mapping class group but the nontrivial
central element in the spherical braid group. Do not restart this research.

Tiny Bubbles Lab's factor-5 reference now loads in the in-app browser, although
web retrieval still fails. Observed: cubic S crossings with vertical end
tangents and uniform crossing height, underpass gaps, persistent colors,
numbered endpoint badges, right-hand generator labels, atom shading, scrolling
and zoom. Its cubic has linear vertical position and smoothstep horizontal
position. No third-party code/assets were copied.

Implemented the first static increment: `BraidDiagram(crossing_style="smooth")`
and `FactorizationDiagram(braid_crossing_style="smooth")`. Defaults remain
straight. Tutorial figure 20 compares the same six-strand word. Next bounded
batch: generator labels/atom annotation for the optional braid view, then
an editor style selector. JSON documents already preserve `crossing_style`;
keep browser-only zoom distinct from exports.

Validation: all 219 Python tests and eight editor JS tests pass; all twenty
SVG/TikZ tutorial figures regenerate; portable-site links pass. Visually
inspected the straight/smooth comparison. Initial suite failures exposed a
missing JSON field allowance (fixed) and relative PYTHONPATH in subprocess
tests (rerun with absolute repository src path). No remaining failures.


## Requested next braid view, September 21

Added the user-linked Tiny Bubbles Lab factor-5 braid display to the V3 plan as
an optional renderer alongside the current view. Inspect the exact reference
before choosing implementation details: retrieval was blocked today. Preserve
braid signs, strand identities, direction and factor-panel integration. See the
new next-task section in IMPLEMENTATION_PLAN.md for the link and acceptance work.


## Overnight batch 5, September 21

Clarified stale tutorial claims about Type II/marked-point reference spokes.
Added current boundary support and remaining variants to the plan, preserving
earlier checkpoints as history. Certified bordered cut systems and general
DiskRoutes remain unsupported. Documentation-only; rebuilt tutorial HTML and
checked portable-site links. Morning wrap-up: check remote CI, summarize the
five overnight batches, and delete the overnight automation at 8:05 a.m. Eastern.


## Overnight batch 4, September 21

`MarkedArc` accepts optional validated hex `color`; omitted colors inherit
Style.curve_color. Closed and bordered renderers honor it, including selections
and overlays. Tutorial figure 19 keeps P-Q red and R-S blue across all panels.
Nine focused marked-arc tests and 25 tutorial snippets pass; closed-surface
explicit/inherited color SVG/TikZ exports were checked separately. Regenerated
19 figure pairs and visually inspected the comparison. Next: editor visual
verification or improve marked-point label placement near the outer contour.


## Overnight batch 3, September 21

Tutorial figure 19 now isolates P-Q and R-S before showing their overlay on
identical surface geometry. Added a runnable comparison recipe and clarified
that these are input comparisons, not computed action states. All 25 tutorial
Python blocks pass; 19 SVG/TikZ figures regenerate and the new stack was visually
inspected. No library code changed. Next: editor visual verification or explicit
curve colors for bordered marked-arc overlays.


## Overnight batch 2, September 21

Bordered `.with_curves(..., allow_intersections=True)` now permits transverse
marked-arc overlays, retaining straight paths in all four views. Default
disjointness checking remains; overlaps and intervening marks remain invalid.
Selection and later additions retain the option; explicit False restores checks.
This is supplied surface geometry, without braid over/under data or computed
actions. Tutorial figure 19 was visually inspected; all 19 SVG/TikZ figures
regenerate, 24 tutorial snippets and eight focused marked-arc tests pass.
Next small batch: editor browser verification, or clearer curve identity/color
controls for supplied bordered families. Keep certified routing separate.


## Overnight batch 1, September 21

Added `family.with_labels(reference=False)` to hide reference numbers while
retaining colored guides and marked-point names. `.with_labels()` restores
numbers; selection and supplied arcs preserve this setting. Tutorial figure 18
now demonstrates the cleaner display. SVG was visually inspected; all 18
SVG/TikZ figures regenerate. Six marked-arc and eleven boundary-anchor tests
pass. Next small batch: editor browser verification or supplied intersecting
marked arcs (currently rejected), with explicit presentation-only semantics.


## Integration checkpoint, September 19

Merged the remote factorization/editor contribution with supplied bordered
marked arcs, preserving both. The tutorial now has 18 SVG/TikZ figures and
23 executable Python recipes; the marked-arc example is figure 18. Fixed the
missing TypeIBoundary import in the earlier factorization recipe. Browser
image decoding and portable-site local links pass. Eight editor JS tests pass.
All 212 Python tests pass. The first combined run had one Windows
connection-abort in an HTTP origin-rejection test; both its focused suite and
the complete suite passed on rerun.
The repeated one-time 9:16 automation was deleted; do not reschedule it.
Older checkpoints below describe validation at their respective commits.


## Bordered marked-arc display and active scope

Heegaard, bridge, trisection and Kirby families are deferred until a concrete
use case and excluded from core display completion. Updated controlling plan.
Bordered reference families now accept `.with_curves(MarkedArc(...))` for
supplied straight arcs in either clear mark band. Selection hides reference
members without dropping arcs or marks. Unknown endpoints, cross-band paths,
intervening marks, intersections and overlaps are rejected. Tutorial figure 18
shows mixed boundaries and upper/lower arcs, with and without guides.
Validation: 158 tests pass; sixteen SVG/TikZ tutorial figures regenerate.
General bordered DiskRoute bindings remain unfinished: the saved cusp-chart
prototype is not certified and has not been applied. Next: route locators and
supplied factor/action views, plus a justified boundary mesh construction.

## Local browser editor, September 13

Added an immutable version-1 `DiagramDocument` JSON recipe API and a dependency-
free, loopback-only browser editor. The editor supports horizontal planar point/
boundary rows, arc/loop itineraries, signed braid words, transported strand IDs,
labels, whole-recipe undo/redo, JSON open/save, and SVG/TikZ/reproducible-Python
downloads. All geometry remains in the existing library. See [EDITOR.md](EDITOR.md)
for usage, schema limits, security boundaries, and the manual acceptance checklist.

The original 171 Python tests plus 36 document/HTTP tests pass (207 total), as do
8 JavaScript controller tests using a minimal DOM double. Both document
kinds reproduce exact SVG/TikZ output when their generated Python is run. The
hosted browser could not open the local URL (`ERR_BLOCKED_BY_CLIENT`), so visual,
pointer, and file-dialog testing remains pending. Do not describe this as a
visually verified or release-ready editor. No Godot or Tiny Bubbles Lab deployment
is included in this contribution.

## Ordered factor/action diagrams, September 13

New presentation APIs: `FactorPanel` stores a distinct factor ID, support panel,
nonzero signed exponent, optional complete braid block, group label and supplied
after-state. `FactorizationDiagram` lays out application-ordered rows bottom to
top by default and prints their right-to-left product. An optional braid column
is continuous across rows; strand colors/endpoint IDs are transported without
resetting at a factor boundary. Crossings stay compact within tall rows. Complete
supplied state sequences form a second surface column. Missing states/blocks,
duplicate factor IDs and noncontiguous groups are rejected.

`BraidDiagram(direction="bottom-to-top")` adds upward traversal while preserving
the original fixed sign convention: positive means upper-left over upper-right.
Words are never reversed, simplified or exponentiated by these drawing APIs.
The existing top-to-bottom default and all prior tutorial SVG/TikZ files are
unchanged. Support geometry, cut itineraries, colors and visibility are reused.

Tutorial figures 16/17 demonstrate grouped planar factors with an adjacent braid
and bordered support/action-state panels. The LaTeX gallery now fits both page
dimensions, avoiding overflow from tall figures. Validation: 171 tests pass
(18 new), 17 SVG/TikZ tutorial recipes regenerate, the 17-page TikZ gallery
compiles without overfull boxes, and the portable documentation site's local
links pass. SVG and compiled TikZ examples were visually inspected.

These changes do not compute actions, certify braid lifts or equivalences, or
complete the bordered cut-system mesh. No Tiny Bubbles Lab deployment is part
of this branch. The drawing examples are supplied data, not verification of a
new mathematical relation.

## Tutorial site and catalog, September 13

Interrupted mixed-boundary batch verified: 153 tests pass and all 15 tutorial
figures regenerate. Portable site builder checks local HTML links. Twelve planned
relation/fibration pages live in docs/catalog/*.json. User supplied the existing
GitHub repository as publishing destination; GitHub Pages is primary, with an
optional GitLab CI configuration. Release version is 0.1.0a3. See RELEASING.md.


Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) first. It is the controlling
roadmap for the new work. This file is the short, frequently updated checkpoint.

## Mixed four-view boundary reference families

The common left Type II + top/bottom pairs + right Type I layout is now supported,
also with explicit plane marks, in all four views. Only same-end Type I/II
combinations remain excluded; the previous opposite-end restriction was overly
broad. Tutorial figure 15 shows this fixture and its stable member identities.

## Member selection for bordered factor panels

`family.select(*numbers)` isolates reference members while retaining geometry,
colors and surface marks; `family.member_numbers` lists available IDs. Empty
selection keeps the bare surface and marks. Tutorial figure 14 shows vertical
factor-support panels on a bordered genus surface. Actions are not computed.

## Explicit marked-point plane bindings

`with_reference_arcs(mark_positions={"P": (x,y), ...})` now places all named
surface marks explicitly in clear upper/lower vertical-plane bands and connects
them inward to the first chain member. IDs and spoke colors follow surface.marks
order. Missing/extra IDs, invalid bands, overlapping marks, marks on reference
curves and spokes crossing another spoke are rejected. Existing automatic
mesh-based mark positions are unchanged. Figure 13 demonstrates this API.
There are now thirteen main tutorial SVG/TikZ figures plus the disk diagnostic.
The certified marked bordered mesh remains unfinished.

## Side Type II spokes and independent presentation geometry

Standard side pairs now connect their inner a anchors to the midpoint of the
outer odd member's upper/lower branch, with inward-tangent cubic spokes. One pair
per side is supported, also mixed with top/bottom pairs and interior Type I rims.
Explicit exclusions: outer bank b for side pairs, repeated same-side pairs, Type I
end rims combined with side pairs, and marks. These cases need further bindings.
The supplied reference drawing no longer asks the closed-surface mesh to validate
it; direct even-wrap geometry avoids the unsupported height-150 closed mesh case.
The certified mesh validator itself is unchanged. Tutorial figure 12 includes a
mixed side/top example.

## Top/bottom Type II reference spokes

`with_reference_arcs(pair_bank="a")` now handles top/bottom Type II pairs, including
mixed Type I boundaries. Each rim gets a vertical-plane spoke to the first chain
member directly inward from its chosen a/b anchor; cubic targets are bisected
rather than snapped to sampled points. Spokes inherit target visibility and
receive persistent boundary-order numbers/colors. Side Type II and mark spokes
remain unfinished, as does the certified bordered mesh. Tutorial figure 12 now
collects the bordered reference families; figure 10 retains attachment guides.

## All Type I slot reference families

The reference drawing now accepts Type I boundaries at genus cusps as well as
outer ends. Odd corridor members use the actual two slot endpoints, opening into
arcs wherever a boundary is present. Even members around opened cusps use a
rounded offset enclosure of the hole/rim control hulls, keeping a small gap;
unopened holes retain the earlier tight wraps. This is presentation geometry,
not a certified bordered mesh. Type II and marked spokes remain unsupported.
Validation: 146 tests and 17 tutorial recipes pass; the updated figures were
visually inspected. The preceding end-boundary commit passed remote CI.

## Type I end reference arcs

`GenusSurface.with_reference_arcs()` draws the reference family for one or both
Type I end boundaries. Each end member becomes two vertical-plane arcs joining
actual rim anchors to the neighboring cusp; interior members retain their IDs,
colors, and cusp-aligned visibility. Both exports and all four views are covered.
This separate presentation API does not pretend to supply a certified bordered
cellulation. Type II connections and marks remain explicitly unsupported. Tutorial figure 10 now shows the end reference family.
The user's one-time 9:16 a.m. Eastern continuation fired during this work; do not
reschedule it.

## Boundary-plane endpoint bindings

`GenusSurface.boundary_anchors()` returns exact rim/vertical-plane attachments
with boundary IDs and a/b banks. `boundary_anchor(id, bank)` resolves one;
`boundary_guide()` draws a labeled SVG/TikZ inventory, now in tutorial figure 10.
The positions are the actual endpoints shared by both half-rims, not rim centers.
Bank letters track tangent orientation, not front/back or cut-disk banks.
These are presentation bindings only: connecting reference arcs, marked-point
bindings and certified Type I/II cellulations still need implementation.
The previous cusp-transition CI run passed (db2b04a).

## Numbered route input update

`CutAtlas.crossing_on_cut(number, segment=1, bank="+", position=.5)` matches
`system.diagram(show_segments=True)` labels such as `2.1+`. Segment/bank coordinates
are mesh-specific; bank signs are not visibility or twist signs. The torus tutorial
now uses this explicit input. Type I/II mesh bindings remain the next major gap.

## Current checkpoint: September 13, 4:15 continuation

The one-time continuation automation is paused. Endpoint commit a76f1c7 passed
remote CI; legend commit 1d8deaa was still queued at this run's start.
Circular planar boundaries now export to TikZ using transparent even-odd stroke
clipping, including Figure panels. The main LaTeX gallery includes all hole
scenarios. Tutorial generation now writes eleven TikZ pictures plus a compilable
`examples/output/tutorial/tutorial-gallery.tex`; CI compiles this document too.
All 140 tests and all 14 tutorial Python blocks pass locally. TeX compilation
is delegated to CI because no TeX executable is installed locally.
Next visual priorities: Type I/II cut-system bindings and accessible genus route
locators, then richer supplied factor/action states. Do not redo endpoint controls
or legends, which are complete. Calculation engines remain lower priority.

## Legend and intersecting-family update

`PlanarDiagram(show_legend=True)` adds stable curve IDs and color swatches below
the surface, in SVG and TikZ. Tutorial figures 04/05 use it; figure 05 also shows
individual components beside the overlay, preserving their supplied routes.
No intersection certification or automatic curve offsetting is implied.
Validation: 140 tests pass; all 14 tutorial blocks run; browser images load.
Remote run 34737479779 for the preceding endpoint commit was still queued.

## Latest visual update

Planar circular boundaries now support exact left/right curved arc endpoints via
`Arc.start_side` and `Arc.end_side`; omitted sides face the route. Invalid endpoint
hole crossings are rejected analytically. Tutorial figure 03 demonstrates explicit
outward-facing endpoints. All 139 tests and 14 tutorial Python blocks pass;
browser checks show all eleven images loading without page overflow. Continue with intersecting-family layouts and visual IDs.

## Resume here

**Visualization first: follow V0-V4, then C1-C4 in IMPLEMENTATION_PLAN.md.**

Richard's five use cases now control the work: planar and standard nonplanar
curves/cuts, vertical factorizations and adjacent braids, supplied visual
transformations, then homology/fundamental-group and Lefschetz-invariant engines.
The earlier R0 exact-core gate is superseded. Keep the architectural separation
but do not defer drawings while researching calculations.

Tutorial: docs/TUTORIAL.md and browser edition docs/TUTORIAL.html. Run
`python examples/tutorial.py` for eleven main SVGs, one detailed cut-disk SVG and eleven TikZ counterparts.
The extra handle arc and `handle_style` constructor option have been removed.
New presentation records: ColoredCurve, PlanarDiagram, BraidDiagram, Panel, Figure.
Genus cut systems use numbered rainbow colors. Independent planar overlays are
opt-in and do not certify intersections; supplied states are not computed actions.

**Current visual refinements:** balanced Type I end clearance is pushed in
`e4f7b32`. The four-view fixture now has a 44-unit right strip, comparable to its
44-unit inter-hole gap and roughly 43-unit opposite strip. The missing generated
LaTeX gallery update was also fixed; GitHub run 34735538354 passed all jobs.

The completed appearance batch changes the default to above/right, makes planar reference cuts
straight symmetry-axis intervals, tightens even genus cuts and applies Richard's
confirmed opposite visibility patterns (above view: odd solid below; even solid
above). `PlanarSurface.with_cut_system()` supplies the standard colored intervals.
`MarkedArc` supplies straight visual arcs between automatic marks while preserving
explicit DiskRoute itinerary behavior. See the tutorial for the two input types.

Validation: all 138 tests pass on Python 3.12; the three new appearance tests
also pass on Python 3.9. All fourteen tutorial Python blocks ran, and the
regenerated figures were visually inspected. CI now also
regenerates genus and tutorial figures in its Python 3.12 job so stale outputs
cannot be missed by the gallery-only generation step.

**Next action: V2/V3.** Finish Type I/II cut bindings and make genus
route locators easier to select. Gentle top/bottom undulation remains a minor
later refinement. Calculation engines remain behind requested visualizations.

The earlier visual-cycle status below is retained as a technical checkpoint:
P0-P3 complete, P4 partial, P5-P8 unfinished and rescheduled.

Current P4a checkpoint: standard_cuts.py now builds certified 2g+1 chains and
numbered boundary/mark spokes. See standard-chains.md. The validator now has
explicit Attachment records for spoke endpoints on chain edges.

Disk routing and numbered complementary-disk diagnostics now work in
`disk_routes.py` and `cut_diagrams.py`. Ten new tests cover repeated crossings,
reversal, boundary returns, explicit overlays and reconstruction after cutting
along a route. Six generated SVG examples are in examples/output/cut-disks-*;
the decorated disk preview was visually checked, including mark M.

Closed default-genus presentation binding now uses an explicit doubled holed
mesh with smooth cubic chain edges. Every curved triangle passes a whole-curve
Bernstein orientation certificate; harmonic cut-disk charts check every triangle.
Genus 1/2/3/5/7 pass all four views. Named cuts and disk routes render with explicit
front/back visibility. The smooth genus-two preview was inspected. The current
127-test suite passes on Python 3.12.14 and 3.9.7; the 16-view regression checks
include genus 1/2/3/5.
The additional genus-seven four-view check also passed.

Marked closed-genus surfaces now work with `GenusSurface(2, marks=('P', 'Q'))`.
Supplementary mesh paths attach at regular cut vertices and reach the actual
marked vertices; the validator checks the resulting disk boundaries. Four new
tests cover all views, stable walks, missing-spoke rejection, exact marked arc
endpoints and maximal automatic mark counts. The marked-cut preview was inspected.

Previous P4 next action, now prioritized in V2: extend the checked presentation
binding to Type I/II boundaries.
The experimental `genus_outer_mesh.py` now classifies top/bottom rim halves and
matching seams explicitly. Its unfinished integration is preserved in
`docs/checkpoints/top-pair-binding.patch`; see that directory's README for the
exact default-genus-two cusp failure and resume commands. The patch is not
applied to the public API, and the edge charts are not a surface certificate.
The two edge-chart tests pass on Python 3.9/3.12; the full Python 3.12 suite now
contains 129 tests. The saved patch passes `git apply --check`.
These are still explicitly unsupported by GenusSurface.cut_system(); the
standalone abstract decorated chain remains available. The former instruction to
finish all remaining P4-P8 work is superseded by the visualization-first roadmap above.
Closed route examples now include multiple handles, a separating loop producing
two once-bordered tori, repeated visits to a cut edge, disjoint handle loops,
and explicitly declared intersections. Their generated contact sheet was inspected:
the harmonic mesh projection is continuous but retains visible tangent changes
between carriers. Smooth presentation-wide routing remains a visual refinement;
do not describe these routes as globally smooth.
Do not mark P4 complete from closed examples alone. New binding modules and
records remain experimental. Projection flattening now uses positive rational
Bezier control hulls to bound every segment, separately from the whole-curve fold
certificate; midpoint-only flattening has been removed. Disconnected projected
pieces are rejected even when their sheet changes.

P3b adds `src/surface_diagrams/cut_systems.py`, 26 tests in
`tests/test_cut_systems.py`, and seven worked examples in
`examples/cut_system_examples.py` with checked-in `examples/output/cut-systems.json`.
It reconstructs full/cut surfaces, vertex links, boundary cycles and mark copies,
and checks parent walks and transverse intersections. All 93 tests pass on
Python 3.9.7 and 3.12.14. JSON reports regenerated identically twice; no SVG or
TikZ geometry changed. The new records are internal, not package-root exports.
Rendered binding, shared parent endpoints/edges, tangencies and triple parent
intersections are explicitly unsupported. P4 may extend these with exact
incidence contracts if its standard configurations require them.

P2 was recovered and committed as 79bf6bd; P3a specification as 577b18f.
Both were pushed before this implementation. Earlier P1/P2 visual checks below
remain historical evidence, not a new visual audit.

Repository root on Richard's machine: `C:\GitHub\surface-diagrams`.
Remote: `https://github.com/richardbuckman-math/surface-diagrams`.
All source links below are repository-relative so another AI can work from a clone.

## What has actually been checked

- Starting code commit: `1af585c` (merge after `97c9c6c`). Version: `0.1.0a2`.
- `python -m unittest discover -s tests` passed **44 tests** at planning time
  with the repository `.venv`.
- Earlier implementation work also verified 44 tests on Python 3.9.7 and 3.12.14,
  built a wheel, compiled 48 TikZ figures plus one multiple-inclusion page with
  Tectonic 0.17.0, and visually inspected the compiled contact sheet. These are
  historical checks, not evidence for future changes.
- The current worktree initially had no tracked changes; only `Figures/` was
  untracked. Richard explicitly authorized including all those diagrams.
- Located **114 original SVGs, 8,102,982 bytes**. All eight named references and
  the additional `BPlanarCutSystem.svg` were rendered and inspected. The other
  SVGs were inventoried, not individually interpreted or visually reviewed.
- [Figures/MANIFEST.json](../Figures/MANIFEST.json) records SHA-256 and byte size
  for every original SVG. The source SVGs are retained unchanged.
- P1 adds `genus_geometry.py`, slot-aware radii, automatically spaced pairs,
  sideways collars, and explicit hidden rim halves. It adds five untuned/override
  examples and a source-comparison generator. Current gallery: 53 scenarios.
- P1 verification: 52 tests pass on Python 3.9.7 and 3.12.14. The SVG genus gallery
  and original-versus-generated comparison were visually inspected. Existing
  TikZ output was regenerated from shared primitives; no exporter logic changed.
- September 11 refinement: 58 tests pass on Python 3.9.7 and 3.12.14. Python 3.9
  requires `PYTHONPATH` pointing to this checkout's `src` (it has no installed
  package). New tests
  cover all four views, boundary visibility including handle-tip boundaries,
  true trimmed hole overlap, mirrored occlusion, direct collar joins, and roomy
  side-pair defaults. The updated D3/D2A/E2 comparison and four-view sheet were
  visually inspected, along with all 17 genus gallery panels. Gallery now has
  57 scenarios. SVG and existing TikZ outputs were regenerated; Tectonic compiled
  the gallery successfully. No TikZ exporter code was changed, and this is not P7.
- The unfinished P2 diff was saved byte-for-byte through git diff and reversed
  out of the working tree. `git apply --check` confirms it can be restored.
  This was the historical P1 checkpoint. P2 has now incorporated that work;
  its obsolete patch has been removed from the current tree.
- P2: circular planar holes, rim-ended arcs, outline-aware clearance, transparent
  stroke clipping, and numbered row guides. All 67 tests pass on Python 3.9.7
  and 3.12.14 (nine additional P2 tests).
  All 14 new gallery scenarios were visually inspected; 1,182 hole-interior
  pixels per image were checked on transparent and colored outputs. Existing
  planar/curve/direction/genus SVG examples were unchanged. Gallery: 71 scenarios.
  New circular-hole TikZ output raises an explicit error pending P7; existing
  export tests still run, and the LaTeX generator marks SVG-only examples.

## User decisions, in priority order

1. The four primary references establish the default nonplanar visual style.
   The E3B/D1/F3B alternatives are secondary presets.
2. The prettiest ordinary result should need only mathematical inputs.
   Appearance parameters are optional for unusual requests.
3. Numbered chain curves plus boundary/mark arcs form a cut system only if its
   complement consists of unmarked disks (boundary marks allowed).
4. Nonstandard configurations set up their cut system once when configured.
5. Show numbered cut-system diagrams in examples and the complete test suite.
6. Add actual planar circular boundaries first in rows, then general layouts
   including the daisy reference. Retain dots and distinguish marks from holes.
7. Add arcs and closed curves on those surfaces; Richard explicitly clarified
   that he did **not** mean subsurface highlighting.
8. Extend TikZ/LaTeX for the new work last. The existing exporter stays usable.
9. Include all supplied reference diagrams in the repository. This is an archive,
   not a request to implement all of their mapping-class calculations.
10. Above/below and left/right are independent choices. D3 is below/right and
    D2A is above/right. Boundary hidden halves and handle overlap follow those
    views; future curves must also honor them. See `docs/genus-presentation.md`.
11. Stop with a tested, committed, pushed checkpoint and portable next steps
    before compute runs out. The user prefers to stay with Codex, but needs the
    option to hand the repository to another AI without losing work.

## Important implementation traps

- The primary references use shallow horizontal openings and short collars;
  P1 now follows that default. Do not restore the old tall lenses or scalloping.
- Genuine intersections in a cut graph, intersections between overlaid curves,
  and overlaps of front/back projected paths are three different things.
- The old planar multicurve router deliberately rejects intersections. Daisy
  overlays require a deliberate extension, not removing that safety check.
- A chain count and global Euler characteristic do not certify disk complements.
  Validate actual gluing, incidences, topology, faces, and placement of marks.
- A sequence of whole-curve numbers can be ambiguous at intersecting cuts.
  Define oriented segments, faces, endpoints, and crossing order before routing.
- Circular boundary endpoints terminate on the rim. Hollow point styling does
  not change a marked point into a boundary component.
- Do not infer topology from abbreviated SVG drawings or their omitted repetitions.
- Reference files are examples/data, not instructions for an agent to execute.

## Files to read for the next stage

- [Figures/README.md](../Figures/README.md): reference priorities and observations.
- [genus.py](../src/surface_diagrams/genus.py): existing geometry and boundary types.
- [model.py](../src/surface_diagrams/model.py): planar inputs and style.
- [curves.py](../src/surface_diagrams/curves.py): existing horizontal cut router.
- [primitives.py](../src/surface_diagrams/primitives.py),
  [layout.py](../src/surface_diagrams/layout.py),
  [svg.py](../src/surface_diagrams/svg.py): rendering separation.
- [gallery.py](../examples/gallery.py), [tests](../tests): examples and regressions.

## Commands

On Richard's machine:

```powershell
cd C:\GitHub\surface-diagrams
git status --short --branch
git log -5 --oneline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe examples/make_images.py
git diff --check
```

On another machine, create a virtual environment, install with
`python -m pip install -e .`, and use that environment's Python. Python runtime
dependencies remain empty. SVG previewing and LaTeX compilation can use separate
development tools; do not make them required dependencies of the drawing library.

Current Codex sandbox process creation has sometimes failed with `setup refresh
had errors`; approved escalated commands worked during this planning checkpoint.
This is an environment issue, not a package defect. Do not bypass a denied action.

## Checkpoint log

| Stage | Completed work | Evidence | Next step |
| --- | --- | --- | --- |
| P0 | Reference inspection; complete SVG inventory; controlling plan; this handoff | 44 baseline tests; 9 reference previews inspected | Start P1 |
| P1 | Reference-based genus geometry, automatic collars, rim visibility, comparison sheet | 52 tests on Python 3.9/3.12; visual SVG checks; 53 gallery scenarios | Start P2 |
| P1 refinement, September 11 | Four views, trimmed hole overlap, smooth direct collars, taller side-pair defaults; 57 gallery examples | 58 tests on Python 3.9/3.12; comparison, four-view and genus sheets inspected; existing TikZ gallery compiles | Restore saved P2 patch and finish P2 |
| P3b, September 12 | Internal cellulation validator, parent incidence checks, seven executable fixtures and JSON reports | 93 tests on Python 3.9/3.12; deterministic JSON; abstract scope only | P4a standard chain constructions and checked presentation bindings |
| P3a, September 12 | docs/cut-systems.md: worked decompositions and proposed validation contract | Specification only; existing 67 tests pass, no validator implemented | Implement P3b gluing/link/mark kernel and fixtures |
| P2 | Circular planar holes and rim endpoints; clipping and clearance; 14 examples; SVG-only export guard | 67 tests on Python 3.9/3.12; geometry and raster checks; old SVG examples unchanged | Start P3 specification and validator |

Append a row or update it at each meaningful checkpoint. Record the actual files,
commit, tests, failures, and next action. Never make a future AI infer status from
a large transcript. Keep the stage table in IMPLEMENTATION_PLAN.md in sync.

## Prompt for another AI

```text
Continue the surface-diagrams repository from its saved checkpoint.
First read docs/HANDOFF.md, docs/IMPLEMENTATION_PLAN.md, and Figures/README.md.
Inspect the actual repository status and reference SVGs; do not rely only on
this prompt. Resume the first unfinished stage in the plan and keep both
checkpoint documents current. The primary references are D3HyperellipticLifted,
D2AHyperellipticSurfaces, E2MCKHOddGenusLifted, and
E2MCKHOddGenusLiftedWithBoundaries, all in Figures/ as SVGs.
Make beautiful ordinary diagrams require minimal parameters. Build and certify
numbered cut systems whose complement consists of unmarked disks, then support
arcs and closed curves on standard genus and custom planar configurations.
Include ordinary and numbered-cut examples and substantive tests for every
supported configuration. Extend TikZ/LaTeX for the new features last.
Follow the saved plan's stage gates and preserve existing work. Ask only when
different mathematical interpretations require the author's decision. Record
progress and exact next actions before stopping or handing off. Do not claim
a stage complete until its acceptance tests and visual checks pass.
```

## Historical cusp-plane convention (superseded September 22)

Type I/II boundary and marked-point reference arcs must lie in the vertical
plane. Bind their endpoints to the actual boundary/mark geometry in that plane;
do not fan them through an arbitrary surface chart. Even genus wraps change
visibility on the projected line through the hole cusps, matching their odd
neighbors, rather than at y=0. This affects presentation visibility only and
preserves supplied curve itineraries and the checked cellulation.

Cusp-plane update validation: 142 tests pass, including transition checks in all
four viewing directions. Genus and tutorial outputs regenerated and inspected.
