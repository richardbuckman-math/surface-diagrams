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

Undo/redo retain up to 60 states. Reset is undoable. Save JSON preserves exact
factor records and words; Open JSON validates the records and verifies equality
with the starting product before loading. Save SVG exports the current paired
surface/braid view, including labels for numerical previews and any missing
preview. Without `--session`, save work before stopping the server; history is
kept only in memory. A JSON factor export holds the current factorization;
the session file holds the whole undo/redo workspace and is reopened via
`--session`, rather than the Open JSON button.

Select a factor and choose **Inspect support** for a larger drawing with 1×–8×
zoom, scrolling, and the full exact braid word and conjugator. Escape or Close
returns to the stacked view. The inspector keeps strokes thin while enlarging
the drawing, making nearby strands easier to distinguish.

Each row also reports a boundary-word comparison. The program reads upward
puncture-ray crossings from the actual rounded SVG polyline and compares its
free homotopy class with the exact Artin image of the standard enclosing loop.
For a half-twist arc, it compares the boundary of the arc's neighborhood.
The inspector's **Boundary-word comparison** disclosure shows both normalized
words. Disagreement or a puncture collision is explicitly flagged, and exports
retain the result. Agreement checks the represented boundary class; it does
not certify embeddedness, separation of nearby strands, or PDF correspondence.

## Geometric preview limits

The support curves are numerical representatives produced by local half
rotations applied to standard arcs or enclosing curves. Complete triple twists
use a direct local full rotation to reduce unnecessary geometric stretching.
Sampling is restricted to the disk where each local rotation moves points, and
dense sections are simplified in bounded chunks. This permits the previously
failing F9-over-F7 move to display both affected supports; particularly crowded
representatives can still take several seconds and benefit from the inspector.
This is separate from the exact algebraic verification; the numerical drawings
are not certified normal forms or automatically recovered PDF itineraries.
Small upper/lower cases calibrate the sign convention. Complicated moves can
exceed the sampling budget; that row then states that the preview is unavailable,
while its exact braid remains usable. Undo can restore the previous drawing.

The prototype caps states at 80 factors and 3500 braid letters, and stops exact
verification if free-group images exceed its computation limit. It never labels
a limit failure as a successful verification. The service binds to loopback,
requires a session token for changes, and does not serve arbitrary local files.
