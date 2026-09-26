# Exact disk-braid action: initial implementation

`surface_diagrams.braid_actions` computes reduced free-group words, independently
of the SVG/TikZ renderer. It does not yet draw images of reference arcs or convert
a planar arc's cut itinerary into a braid word.

```python
from surface_diagrams.braid_actions import artin_action, hurwitz_move

factors = ((1, 2, -1), (-2,))
before = artin_action(3, sum(factors, ()))
changed = hurwitz_move(factors, 0)
after = artin_action(3, sum(changed, ()))
assert before == after
```

The algebraic convention is explicit: positive generator i sends x_i to
x_i x_(i+1) x_i^-1 and x_(i+1) to x_i, fixing all other generators.
For words u,v, A(uv)=A(u) composed with A(v). Do not equate this with the
renderer’s application order without identifying the geometric base loops and
the appropriate action/pullback convention first.

Forward Hurwitz replaces (u,v) by (v,v^-1 u v); its inverse replaces (u,v)
by (u v u^-1,u). Indices are zero-based factor positions. Output factors are
freely reduced words; no braid normal form or new planar supports are produced.
The caller supplies the strand count when evaluating the resulting action.

The disk calculation retains the boundary action. In particular a full twist
on three strands conjugates each free generator by x_1 x_2 x_3; it is not
reported as identity. No sphere quotient is applied by this module. Images
can become very long; this is a correctness-first implementation, not yet a
compressed representation or a graphical proof certificate.

The six-strand PDF/braid correspondence remains provisional until the support
curves are checked against the earlier transcription. Matching the final group
action alone would not verify every individual factor correspondence.
