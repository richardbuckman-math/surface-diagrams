# Interactive factorization prototype

Run from an installed checkout:

```powershell
$env:PYTHONPATH='C:/GitHub/surface-diagrams/src'
python -m surface_diagrams.factorization_lab --port 8017
```

For a durable workspace that automatically saves every edit and undo/redo step:

```powershell
python -m surface_diagrams.factorization_lab --port 8017 --session .preview/my-factorization-session.json
```

Use an existing parent directory. Reusing the same file reopens the exploration
and its undo history after verifying every saved state's exact product. Writes
replace the session file atomically; a save failure rejects the edit and leaves
the previous state available. An invalid existing file is never overwritten.
The page states whether the current server is saving a session file.

The browser opens a local interface with the 13 original factors from the
178-letter `BraidSixSeven.svg`. The source words match the earlier transcription
factor by factor. The remaining PDF support correspondence is still provisional.

Drag a planar diagram onto another factor's row. The selected factor moves to
that position and stays unchanged; every factor crossed is conjugated. Arrow
buttons provide the same operations without dragging. Moving down uses
`(u,v) -> (u v u^-1,u)`; moving up uses `(v,u) -> (u,u^-1 v u)`.
Each local replacement is verified with exact Artin actions before it is accepted.
The right column is one continuous braid: colors follow strands across blue
dotted factor separators. Read both columns from top to bottom.

Select a row to use the split menu:

- A squared twist can split into two equal unsquared twists.
- A two-point twist can split into two half twists.
- A three-point twist can split into three pairwise twists using the
  marked-point disk version of the lantern relation. A power repeats this
  replacement. This does not include framed inner-boundary twists.

Combine joins a selected factor with its following neighbor when they are
verified powers of the same supported twist. Two identical half twists combine
into a Dehn twist. It can also recombine three neighboring pairwise twists into
a three-point twist when their exact product matches the marked-point lantern
candidate. Select the first of the three and choose **Combine neighbors**.
This reverses a lantern split, including after a common conjugation. Other
combinations are rejected without changing the state.
General daisy and framed-boundary substitutions are not implemented.

Undo/redo retain up to 60 states. Reset is undoable. Export JSON preserves exact
factor records and words; Load JSON validates the records and verifies equality
with the starting product before loading. Save SVG exports the current paired
surface/braid view, including shared support checks and any missing
preview. Without `--session`, save work before stopping the server; history is
kept only in memory. A JSON factor export holds the current factorization;
the session file holds the whole undo/redo workspace and is reopened via
`--session`, rather than the Load JSON button.

Select a factor and choose **Inspect support** for a larger drawing with 1×–8×
zoom, scrolling, and the full exact braid word and conjugator. Escape or Close
returns to the stacked view. The inspector keeps strokes thin while enlarging
the drawing, making nearby strands easier to distinguish.

**Inspect prefix action** shows the exact images of the six based meridians
immediately before and after the selected factor. Colored numbers show the
puncture permutation; the accompanying words preserve winding and base paths,
so the permutation alone is never presented as an identity test. Long words are
abbreviated on screen; **Save full exact words as JSON** exports all six complete
images on both sides. The six colored arcs share a basepoint at the left outer
rim. Each recovered arc's ray word is checked against the full exact meridian
image before the shared surface router draws the family together. When a curve
exceeds 768 cut visits or the family exceeds 1024 route nodes, the drawing is
marked unavailable and the exact words remain accessible. Each accepted
before/after drawing has a **Save SVG** button for standalone inspection. These are disk
actions, without imposing the sphere relation; a final nontrivial disk action
does not decide whether the factorization is the identity on the sphere.

**Check sphere action** computes the entire product's exact six-meridian disk
action, imposes `D = x1 x2 x3 x4 x5 x6 = 1`, and checks whether the resulting
five-generator free-group action is one common inner conjugation. For the
supplied (6,7) product it finds a 58-letter word `w` and verifies all six
equations: each image is `w xi w^-1`, with `x6=(x1...x5)^-1`. Thus the sphere
outer action is the identity, while the disk action is not. The modal shows
the witness, abbreviated images, and a five-puncture chart in which removing
the verified common basepoint path `w` returns all five visible arcs to the
standard cut system. Puncture 6 is at infinity in that chart. The chart uses
the shared noninterleaving Arc renderer and appears only after the exact
inner-action certificate succeeds. Its **Save SVG** button exports the chart;
the JSON export contains every complete
word and expected image. This is an action certificate, not the separate
19-substitution braid-relations derivation: the outer action alone does not
distinguish the central order-two spherical braid from the identity. It is
also not a claim that the late disk cut systems have been drawn. If a common conjugator is not found, the tool reports
no certificate rather than asserting nonidentity.

Each row reports the boundary class of its recovered `Arc` or `Loop`, compared
with the exact Artin image of the standard enclosing loop. The inspector shows
the itinerary and both normalized boundary words. Half twists use the boundary
of the arc's neighborhood. Drawing uses `PlanarSurface.with_curves` and the
existing SVG renderer, including its noninterleaving and clearance checks.

## Shared support and mapping-class API

`ConjugatedTwist` stores a standard core and its conjugator independently of
factor IDs and browser state. `support_curve` recovers an ordinary library
`Arc`/`Loop` for the six-marked-point prototype; `support_drawing` uses the shared
surface renderer. The initial F9 recovers exactly the user's confirmed itinerary.
Arcs and closed curves now derive their cut itineraries directly from exact
transported boundary words. For an arc, recovery finds the two endpoint meridians
and the path between them in its neighborhood boundary word. Its boundary class
must agree exactly before rendering. The exact check transports
only the supported closed word, avoiding expansion of unrelated meridians. It
retains the exact class in the inspector even when geometry recovery fails. Ambiguous recovery, routing limits,
and clearance failures are reported explicitly; there is no sampled-SVG fallback.
This does not establish correspondence with every drawing in the original PDF.

After a Hurwitz move, each crossed factor is simplified automatically. The dragged
factor stays unchanged. **Simplify factors** applies the same bounded search to
all current factors, with undo. Search uses braid relations, commuting letters,
and verified removal of conjugator suffixes which stabilize or relocate the
standard core. It preserves half-twist / Dehn-twist type, support size, and power.
The core's position may change. Every local rewrite is verified, including exact Artin checks of core transports.
This avoids expanding an enormous common conjugator just to verify a short
rewrite. Factorization replacements retain their complete-product action check.
This is a bounded search for a shorter representative, not a global shortest-word
claim. For example, F1 dragged past F2 now leaves an 11-letter half twist instead
of the raw 33-letter conjugation.

```python
from surface_diagrams import ConjugatedTwist, simplify_twist, support_drawing

twist = ConjugatedTwist((1, 2), first=1, points=2, half=True)
shorter = simplify_twist(twist)  # standard half twist at position 2
svg = support_drawing(shorter)
```

The prototype caps states at 80 factors and 3500 braid letters, and stops exact
verification if free-group images exceed its computation limit. It never labels
a limit failure as a successful verification. The service binds to loopback,
requires a session token for changes, and does not serve arbitrary local files.

Enter a signed braid word in **Global conjugation g** to replace each factor
`F` by `g F g⁻¹`. This changes the complete disk product by conjugacy; it is
not an exact-product-preserving Hurwitz move. The lab verifies the full new
disk action and records the accumulated global frame alongside each undo state.
Exported JSON includes `global_conjugator`, and import and session reopening
check that the recorded frame accounts for the product. Simplification of the
individual factors remains bounded and does not claim a shortest word.

The **Exploration history** panel names each new checked operation and can
revisit any retained step. Branching from an older step discards its redo
branch; up to 60 states are retained. A local `--session` file saves the labels
with the factor and frame history. Older session files reopen with neutral
"Earlier saved state" labels because their original operations were not
recorded. Export JSON saves the current factorization and frame only, not the
complete undo history.

A saved local session can reopen when an older history state exceeds the exact
verification limit. A persistent notice identifies those states as not reverified;
malformed records and proven mismatches still reject. Importing a JSON
factorization continues to require a successful exact product check.

Simplification also recognizes an exact standard support before the bounded
rewrite search. A positive supported twist (with its type and power fixed) is
determined by that support, so this can remove the entire conjugator, including
a central full braid twist. A half twist uses its two-point neighborhood class.
This shortcut uses exact support equality; lab replacements still receive their
existing exact braid-action checks. The general search is not globally minimal.

When growing prefix actions hit the computation bound, exact braid verification
tries transporting each based meridian separately in reverse composition order.
It retains base paths and never uses the unoriented curve-class comparison for
braid equality. Intermediate words and final images remain bounded.

Dense supports allow up to 768 cut visits per curve (1024 route nodes per
diagram). The lab widens crowded cut intervals while retaining fixed dot and
stroke sizes, and scales the outer ellipse with the spacing. Use inspector zoom
for these larger drawings. Exact class, noninterleaving, and dot-clearance checks
remain mandatory; the route search can still report its bounded-search limit.
The separate recipe editor retains its existing 64-cut input limit.

Dense diagrams (more than 128 route nodes) use at most 200 complete ordering
attempts and two million pairwise crossing comparisons. Reaching a limit reports
that the search is inconclusive; it does not assert that the curve is impossible.
Dense cards show their cut count and recommend inspector zoom.

The exact prefix-action inspector has Previous/Next controls to follow the
cut system factor by factor. Each panel shows the six based arcs when the
shared router accepts them; later steps retain all exact meridian words and
disable SVG export for a drawing that could not be verified. In the supplied
factorization, the six-arc drawing after F8 exceeds the 1024-node limit.
Selecting a factor also shades its matching interval in the continuous braid;
the standalone paired SVG has no selection shading.

After local braid rewrites, a bounded support-class search tries a shorter route
back to a standard core. Accepted candidates keep twist type and power and pass
an exact support comparison; lab operations still check exact braid actions.
The search admits at most two million boundary letters, starts only on classes
of at most 4096 letters, and never explores above the initial boundary length.
It can shorten a conjugator through changes of supported presentation, but it
does not promise a globally shortest answer.
