# Changelog

## Unreleased

- Export the verified before/after disk cut systems and normalized sphere
  identity chart as standalone SVGs from their inspectors.

- Display the certified final sphere cut system in a five-puncture chart after
  removing the exact common basepoint whisker; the sixth puncture is at infinity.

- Certify the (6,7) product's sphere outer action as trivial: after imposing
  the boundary relation, all six exact meridian images share one verified
  58-letter conjugator, despite a nontrivial disk action.

- Draw six exact based meridian arcs together before and after the selected
  factor when the shared noninterleaving router accepts them; retain exact
  words and show an explicit warning when route limits are reached.

- Inspect the exact six-meridian disk action before and after any selected
  factor, with a colored puncture permutation and downloadable full words.

- Search exact support classes for shorter conjugated twist presentations while
  preserving type and power; keep all lab braid-action checks.

- Render denser lab supports with up to 768 cut visits, widening crowded gaps
  while retaining fixed strokes, dots, and all geometric checks.

- Recover both arc and closed-curve supports directly from exact boundary words,
  retaining the shared noninterleaving route checks and explicit drawing limits.
- Recognize standard supports to remove complete stabilizing conjugators, and
  show the standard core alongside its conjugator in the support inspector.
- Retry large exact actions by transporting based meridians separately; preserve
  session history with an explicit notice if verification still reaches a limit.
- Reuse shared Arc/Loop surface rendering in the lab, with exact class-checked
  itinerary recovery and faster propagation of route ordering constraints.
- Add reusable conjugated-twist records and verified bounded simplification,
  including changes of standard core; automatically simplify crossed factors.
- Clarify Export JSON / Load JSON and add Simplify factors for saved explorations.

- Add the interactive (6,7) Factorization Lab: drag-and-drop checked Hurwitz
  moves, stacked planar supports and a continuous braid with factor separators.
- Support checked square/half-twist/marked-point lantern splits, inverse lantern
  combining, equal-power combining, undo/redo, JSON reopening and SVG export.
- Add durable session files with atomic saves and verified undo-history recovery.
- Add zoomable support inspection and compare itinerary boundary words with
  exact transported classes. PDF correspondence remains provisional.
- Retain numerical deformation helpers for independent diagnostics; the lab's
  support rendering uses exact topology instead of numerical proposals.

## 0.1.0a5 - 2026-09-25

- Extend crossing highlights to factor-local braid positions and add an editor
  checkbox with undo/redo and highlights that follow reordered crossings.

- Add optional standalone braid crossing outlines with `highlight_crossings`,
  using 1-based word positions in either direction, with SVG/TikZ and JSON support.

- Reject explicit marked-point placements that bend a solid perimeter arc
  through or too close to a genus opening, even when its endpoints are valid.

## 0.1.0a4 — 2026-09-23

- Add a local browser editor with versioned JSON recipes, undo/redo, and
  reproducible SVG, TikZ and Python exports.
- Add application-ordered factorization panels, supplied action states and
  continuous factor-aligned braids. These display supplied data without
  computing actions, lifts or equality.
- Add optional smooth braid crossings and signed generator labels, with editor
  controls and JSON save/reopen support. Fix generator-label recipe round trips.
- Replace bordered reference spokes by continuous perimeter arcs ending at rims
  or marks. Type I handle-return arcs attach at front/rear rim points.
- Add automatic axial and symmetric paired marks in the reference presentation.
- Default closed reference curves to solid; optional rear corridor dashing no
  longer creates arbitrary visibility transitions on enclosing loops.
- Support supplied colored marked arcs, optional transverse intersections,
  reference-member selection and optional number labels.
- Expand the tutorial/gallery to 21 SVG/TikZ examples, including four-view
  mixed boundaries, symmetric genus marks and smooth labelled braids.

### Compatibility and remaining work

- Perimeter reference members replace the old boundary/mark spokes. Their
  numbers after 2g+1 have changed; use `member_numbers` rather than old IDs.
- Closed reference curves now default to solid. Set `closed_curve_style="split"`
  for rear corridor dashing; enclosing loops stay solid in either mode.
- The separate checked mesh still uses its original marked-point locations and
  spokes. Explicit DiskRoute endpoints and itineraries are unchanged.
- General bordered DiskRoutes and the certified bordered mesh remain unfinished.
  Catalog derivations/factorizations remain placeholders. Heegaard, bridge,
  trisection and Kirby families are deferred until a concrete use case.

## 0.1.0a3

- Support opposite-end Type I and Type II reference families in all four views,
  including explicit marks; preserve the same-end exclusion.
- Add the mixed-boundary tutorial figure, SVG and TikZ exports.
- Add a portable tutorial/gallery site and GitLab Pages pipeline.
- Add planned pages for lantern, half lantern, rose and daisy relations, and
  MCK, hyperelliptic, BK, (4,3), (6,2), (6,7), (10,10) and Gurtas fibrations.
- Add version-tagged release packaging. Mathematical derivations and
  equivalence verification remain future work.
