# PC daisy extraction with a repeated petal

This is a derived PC daisy rule in the marked disk. It accepts a powered
petal directly, keeps the spare positive twist visible, and applies for any
integer multiplicity `m >= 2`.

Write the individually matched ordered unit daisy as

```
A Q C = D.
```

Here `A` and `C` are the ordered prefix and suffix, `Q` is the selected pair
petal, and `D` is the daisy's outer twist. Then

```
A Q^m C = D (C^-1 Q^(m-1) C).
```

The formula follows by replacing `D` with `A Q C` and freely cancelling
`C C^-1`. No source-product centrality or sphere identity is assumed. The
inverse letters in the spare twist's conjugator are not negative twist
factors. Both outputs remain positive. This statement is in the marked disk;
it does not assert an uncorrected relation for framed holes.

`named_repeated_petal.repeated_petal_daisy()` constructs the rule from the
canonical PC daisy and retained internal Hurwitz interchanges. It retains the
explicit power split and every same-ancestry spare transport as its local
expansion. Independent tests cover all pair-petal positions for three-, four-
and five-point daisies, multiplicities2/3/4 and three common frames:81 generic
cases. Wrong suffix orientation and wrong ordered inputs are rejected by
faithful disk comparisons.

## Applied shortening of the working (6,7)

At the previous complete proof's step80, the actual first daisy already has
input multiplicities `(1,1,2,1,1)`. Every full powered input matches the general
rule separately, in the same transported daisy chart. Apply it with `m=2`.
The two outputs are the third standard exterior and the actual spare pair
`direct.E2`, with normalized chart `(-4,-4,-3)`, coreT23. The entire factor tuple
rejoins the previous post-daisy step84 **literally**.

The new replay never forms two unit factors or performs the two separate
petal carries. One direct PC daisy application replaces those three operations
and the old unit-daisy contraction. The complete named route therefore has
**86 operations instead of89**, with parts `17 + 67 + 1 + 1`. It still has four
explicit sphere operations and zero action-only boundary recognitions. The
under-twenty goal remains open.

Count the verification layers honestly:106 external adjacent disk checks
remain, versus108 before. The two displaced checks remain inside the generic
rule's explicit expansion; there are14 retained internal named checks versus12.
The total adjacent verification count is unchanged. This shortening is at the
level of reusable named substitutions, not a claim of fewer atomic Hurwitz
crossings. Full signed framing balance, separate local sphere/+I checks, all
normalized nonabelian kernels and B4 shadows, and the literal join are saved in
`certificate.json` under `named_repeated_petal_shortening`.

The four final exteriors remain visible. Their separate fourth-power sphere
cap is unchanged, as is the different earlier cap of six framing corrections.
No new half twist, negative factor, sphere move or cap appears. The complete
positive disk tail retains support maximum20.
