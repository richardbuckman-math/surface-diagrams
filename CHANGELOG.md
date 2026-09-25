# Changelog

## Unreleased

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
