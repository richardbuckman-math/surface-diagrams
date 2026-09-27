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

`action_checkpoints(strands, factors)` returns the identity state followed by
each concatenated-prefix action, including checkpoints for empty factors.
`conjugate_factors(factors, g)` replaces every factor f by g f g^-1. Its total
product is g P g^-1, generally not P; inverse conjugation restores the original
freely reduced factors. Neither operation computes new planar support curves.

The six-strand PDF/braid correspondence remains provisional until the support
curves are checked against the earlier transcription. Matching the final group
action alone would not verify every individual factor correspondence.

## Arc ray words

`arc_ray_word(points, arc)` reads a point-to-point Arc against upward rays.
An upper segment crossing ray j left-to-right contributes j; crossing it
right-to-left contributes -j. Lower segments contribute no letters, and endpoint
rays at the endpoints are excluded. Reversing the arc inverts this word.
This is relative path data, not a general arc-to-braid conversion.

For the confirmed factor 9 itinerary, the result is
(-4,-3,2,3,4,-5,-4,-3,-2,3,4,3). The earlier SVG block has the exact form
`g + (1,) + inverse_word(g)`, with g=(-2,-3,4,2,-3,-2,-2).
The action sends x1 to x1 and x2 to t x4 t^-1 for this same ray word t.
This verifies the endpoint/transport-word comparison under the stated convention;
other factors and the geometric action replay still need checking.

## Closed support curves

`loop_ray_word(points, loop)` reads a closed itinerary against the same upward
rays. For example, `Loop((2, 5))` on six points gives `(3, 4, 5)`. The output
retains a traversal and starting cut. `free_homotopy_key(word)` removes cyclic
conjugation and identifies reversed traversal for an unoriented closed path.
It does not certify that an arbitrary supplied itinerary is embedded, calculate
a Dehn twist, or apply sphere relations. Canonicalization currently examines all
cyclic rotations and is intended for manageable support words, not huge outputs.

`act_on_loop_word(strands, braid, word)` substitutes Artin images and returns
the exact reduced based word. Comparing its `free_homotopy_key` with the original
tests the closed-path class in this algebraic convention. Keep the based word:
a disk full twist can change it by conjugation while leaving the closed-path
class unchanged. Thus agreement of closed curves alone is insufficient for the
disk identity check; based reference data must remain available.

## Checked substitutions

`substitute_factors(strands, factors, start, stop, replacement)` accepts a
replacement only if its exact Artin action agrees with the selected factor
slice. Indices are zero-based and stop is excluded. An empty replacement permits
checked cancellation. The operation validates disk braid equality, not a sphere
relation or a boundary-framed lantern relation; supplying such a substitution
requires its own conventions and encoding first. It does not discover relations.

Run `python examples/verified_twist_split.py` to draw the independently checked
replacement `(sigma3 sigma4)^6` by two copies of `(sigma3 sigma4)^3`.
The diagram renderer still displays supplied support curves; equality checking
happens in the substitution function before the example is drawn.
