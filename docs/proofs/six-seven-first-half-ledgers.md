# Full linking graph of the isolated first-half block

This audit changes no graphical proof, payload, PDF or reached route. The
complete named derivation remains82 operations. Reproduce the exact report with
`PYTHONPATH=src python examples/analyze_first_half_ledgers.py`.

The source is the retained endpoint of the two-donor audit98312ba, not a new
gather. Select, in their actual relative order,

```
Q_outer, T12^2, transportedP23, F3, P24, Q_S1, F9.
```

The square counts twice, so this is the previously considered eight-instance
block. Its product is pure. The full labeled crossing trace gives

```
       1  2  3  4  5
1      0  2  1  0  0
2      2  0  1  1  0
3      1  1  0  2  0
4      0  1  2  0  0
5      0  0  0  0  0
```

## Stronger necessary obstruction

The spectrum `(0:5,1:3,2:2)` alone did not exclude two three-point twists plus
one pair. The FULL weighted graph does: its two doubled edges12 and34 are
disjoint. In that proposed endform the doubled edges would meet. Equivalently,
the only possible triple supports are123 and234, and using both would give
weight at least2 on23, while the actual weight there is1.

More generally, a positive full twist supported on S contributes its positive
power to every pair in S. Exhaustive bounded positive clique-ledger enumeration
shows that **three or fewer positive full-twist records are impossible**. For
four records there are exactly two aggregated support/power ledgers:

```
R123 + P12 + P24 + P34^2,
R234 + P12^2 + P13 + P34.
```

The symbol `+` here records incidence only, not an ordered braid product.
Arbitrary supporting curves and their nonabelian winding are still unknown.
Equal enclosed sets are aggregated only for the invariant; this does not
combine actual factors or assert their curve classes agree. Every endform of
at most three records would have at most three distinct support sets, so the
necessary enumeration excludes it even if the same set occurs on distinct
curves. Powers, intermediate half splitting and other disk rewrites cannot
change this pure product's linking graph. Global conjugation merely permutes
its labels; all120 label permutations are checked in the regressions.

This is an obstruction for THIS ISOLATED product under disk product-preserving
moves/common conjugation. It is not a lower bound for the complete derivation.
Outside interactions, sphere changes, half-factor endforms and other positive
endforms remain available. No sphere move, cap or substitution is applied.

## One fixed geometric attempt fails

For the first allowed ledger, take the actual roundR123 (alternative.R2), a
round12 unit, the actual S1-daisy24 curve (two.root.1), and the square of the
actual O1234-daisy34 curve (two.outer.1). All24 orderings fail the faithful B5
product check. Each failure retains the first different meridian and both
images. This excludes only these unchanged curve classes and their24 orders,
not transported versions of either allowed ledger. The hypothetical34 square
has not been created or gathered in the actual factorization.

The report retains full point-pushing kernels, B4 shadows and reconstructions
for every selected/candidate factor and for the complete isolated product.
No strand is forgotten. `positive_linking_ledgers()` in linking_ledgers.py
returns only necessary incidence targets; it never claims a common disk chart.
Invalid matrices are rejected and exhausted enumeration raises
VerificationLimitError rather than reporting a false exclusion.

The next useful step needs a specific outside interaction or a joint chart for
one allowed four-record endform. Do not repeat the now-excluded two-roots-plus-
one-pair target, the older outer-plus-pair target, or these24 fixed-class orders.
