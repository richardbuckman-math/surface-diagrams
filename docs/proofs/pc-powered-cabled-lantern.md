# Powered cabled PC lantern with the shared inner twist

Suppose the ordered, individually matched unit cabled PC lantern is

```
A B C = O I,
```

and the shared inner twist `I` commutes with `C`. For positive integers
`m,n,k`, the derived rule is

```
A^m B I^k C^n = A^(m-1) O I^(k+1) C^(n-1).
```

Zero remainder powers are omitted. This is a disk relation. All factors on both
sides are positive twists; signed letters in a common conjugator do not create
inverse twist factors. The local expansion splits one unit from each powered
root, commutes the shared inner block through `C`, applies the unit cabled
lantern, then merges the inner powers. Every decomposition, the commuting
adjacent check, and the unit lantern's internal interchange remain certified.
No source-centrality hypothesis is used.

The canonical unit chart uses `A=sigma3^-1 R123 sigma3`, `C=R123` and
`B=C T34 C^-1`. The cyclic inputs `A,C,T34` undergo one retained forward
Hurwitz interchange to give `A,B,C`; the outputs are `O=T1234` and `I=T12`.
A common chart transports every input and output, including its multiplicity.
The implementation is `powered_cabled_lantern()` in
`src/surface_diagrams/named_powered_cabled.py`. Tests cover 81 combinations of
root powers, inner powers and charts, plus wrong-order and omitted-inner cases.

## Actual working (6,7) application

At the original early fourteen-factor B5 source, keep both the actual123 and
routed124 roots squared. Start cyclically at the complete final124 square.
The first four actual inputs match powers `(2,1,1,2)` in common chart `(-4,-4)`.
Their outputs are the retained124 unit, the actual four-point outer, roundT12
squared, and the retained123 unit. Start cyclically after the retained124 unit.

These three actual operations replace the previous six, and the entire factor
tuple rejoins the old preferred disk-tail stage6 literally. Both original root
splits, the separate root/inner commutation and the displayed inner merge are
bypassed in the preferred replay. Their local expansion remains explicit in the
named rule. All four original halves remain literally unchanged. The changed
prefix has support maximum16; the complete positive disk tail stays within20.

The complete named proof is therefore82 operations rather than85:
`17 early + 63 positive disk-tail + combine + fourth-power sphere cap`.
External adjacent checks decrease108 to107 because one commuting crossing is
now internal to this generic rule. That crossing is retained, so this does not
claim a reduction in total atomic verification work.

Every actual powered input/output is matched separately. All eight normalized
inputs/outputs retain their full point-pushing kernels, B4 shadows and B5
reconstructions; the signed PC framing balance is `(0,0,1,1,0)`. The local disk
discrepancy, exact marked-sphere check and chosen `+I` lift discrepancy are
separate certificates. These marked-point checks do not assert a framed-hole
identity without the recorded PC corrections.

Both cyclic starts have explicit common frames checked by free-word equality
before presentation normalization. Four terminal standard exteriors remain
visible until the existing separate fourth-power sphere cap. No sphere move,
cap, half or negative factor is introduced by this shortcut.
