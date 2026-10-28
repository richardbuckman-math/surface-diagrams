# Direct sphere lantern with the original F1 square intact

The complete named proof now has79 operations instead of82. The first sphere
lantern is reached directly, without splitting the original separating factor
F1, preconditioning F2 with one root, or combining two matched half twists.
This changes the actual prefix and rejoins the old full step14 literally at
new step11. Everything after that join is identical, merely renumbered.

## A direct three-factor named rule

In a standard six-point chart let `C=T123` and `H=H34`. The actual input pattern
is

```
C^2, C^-1 H C, H.
```

The two half twists are DISTINCT. The first factor remains a single square
throughout the replay. On the genus-two cover that square is the original
separating twist; it is not replaced by two temporary root factors.

The direct sphere relation is

```
C^2 (C^-1 H C) H = T12 T56.
```

Its full-twist PC parent is the ordinary cabled lantern

```
C T34 (H^-1 C H) = T12 T1234.
```

The two left products freely reduce to the SAME word `C H C H`. Thus this is a
reusable direct form of that lantern, with the parent retained explicitly.
On the marked sphere the outer1234 curve is the complementary56 curve. This
last replacement retains a NONZERO disk discrepancy, an exact marked-sphere
certificate and a SEPARATE chosen +I genus-two lift check. It is not an ordinary
disk braid equality or a cap of an exterior twist.

The parent's signed PC framing balance is retained. No framed-hole convention
for either half twist is chosen or asserted. Single-point PC corrections are
recorded at the full-twist parent, rather than assigning fictitious hole
framings to the half factors. Both whole substitution and complementary-curve
step retain their separate discrepancies and lift certificates.

## Actual working prefix

Begin with the same working source and the same first two inverse Hurwitz
moves. Split only F8 and F10. Carry their required root units upward as before.
The transported actual F7 has the same checked disk representative as in the
old route, but F2 was never preconditioned by C1. Carry this SAME F7 upward
through SIX neighbors instead of seven. It never crosses an F1 root because
F1 is still the original square.

The adjacent inputs are now exactly

```
F1 squared, original F2, transported F7.
```

Every input separately matches the direct canonical pattern in common chart
`(2,3,2,5,-3,-3,4,1,2,3,4,5,1,2,3,4,5)`. Every output separately matches the
existing two routed pair twists. Full actual point-pushing kernels, B5 shadows
and B6 reconstructions are retained. In this chart the full-twist parent's
signed framing balance is `(0,1,0,0,1,0)`.

The entire factor tuple rejoins old step14 LITERALLY at new11. The old step15
frame, step16 puncture-to-boundary chart with SIX explicit corrections and
step17 cap become new12/13/14 and are otherwise unchanged. The first lantern's
new full disk discrepancy replaces its old one; all FOUR sphere moves stay
visible and individually lifted. No auxiliary half, inverse twist factor or
extra sphere move is introduced.

## Counts and bounds

The early prefix is14 operations instead of17. Its external adjacent checks
fall14->12: both the old root preconditioning crossing and the old crossing
of F7 with the temporary F1 root disappear from the actual route. All six
remaining gather checks and their raw free-word/presentation certificates are
retained. This is not a regrouping of the old navigation arrows.

The six-strand prefix's support maximum stays30, exactly its previous maximum.
The subsequent positive B5 tail is unchanged at63 operations,107 external
adjacent checks and support maximum20. Therefore the complete route is

```
14 early + 63 disk tail + combine + fourth-power sphere cap = 79.
```

The four terminal standard exteriors remain until their existing separate
fourth-power cap. The early six framing corrections still have their different
visible cap. Four sphere moves and zero action-only boundary recognitions
remain. The complete named closure is solved; under twenty remains open.
