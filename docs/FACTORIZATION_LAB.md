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

A saved local session can reopen when an older history state exceeds the exact
verification limit. A persistent notice identifies those states as not reverified;
malformed records and proven mismatches still reject. Importing a JSON
factorization continues to require a successful exact product check.
