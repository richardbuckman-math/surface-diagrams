# Can the specified (10,10) split off a (4,3)?

The new question concerns the **Lefschetz fibration**, not merely its type or
the fact that its monodromy product is the identity. For the exact imported
twenty-factor source, no reverse fiber-sum equivalence has been established
here. No indecomposability theorem has been established either. This audit
applies ZERO moves and preserves every published proof, factor, viewer and PDF.

## The precise target

Taking a fiber sum of a (6,7) fibration and a (4,3) fibration gives type
(10,10). The gluing map is part of that construction. The reverse question is
whether our specific fibration can be written

\[
  F_{10,10}\cong F_{6,7}\mathbin{\#_\phi} A_{4,3}
\]

for some actual summands and gluing map. The genus-two geography constraints
force these two types whenever a (10,10) admits a nontrivial decomposition
into relatively minimal genus-two fibrations; see the last case in
[Akhmedov--Monden's proof of Theorem 1](https://arxiv.org/pdf/1809.09542).
This conditional statement does not say that every (10,10) decomposes.

For genus at least two, fibration isomorphism corresponds to Hurwitz moves
and simultaneous conjugation of the ordered monodromy factors.
[Huang, Section 2](https://arxiv.org/html/2602.20451#S2) reviews this correspondence.
A concrete reverse proof must therefore expose a genuine seven-factor
(4,3) identity block, leaving thirteen factors of type (6,7), through such
equivalences. A lantern substitution can change the fibration even though
both resulting products are identities: geometrically it can be a rational
blowdown. [Nakamura, Sections 2.2 and 3](https://arxiv.org/html/1811.03708#S3)
explains this and calls his two-copy intermediate a “fake (6,7)”: completing
its lantern uses a vanishing cycle from the additional summand.

## Exact source and first obstruction

The source is `fibration-derivations/10-10.json:factors`, SHA256
`2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e`.
This is the checked original algebraic construction, not its four incompatible
drawing edits and not the older twenty-route dictation.

Every separating factor acts as I on integral homology. Thus an unchanged,
order-preserving seven-factor (4,3) subword would require the product of its
four nonseparating transvections to be I. **All210 choices fail** that full
Sp(4,Z) equality. Consequently all25200 literal choices of four halves and
three separating factors fail. The certificate retains every matrix.

This only excludes extraction using unchanged cycles in this circular order.
Cyclic starts do not evade it, since they conjugate the selected product.
General Hurwitz moves can change the cycles and are not excluded.

## A necessary condition throughout the Hurwitz orbit

The actual nonseparating homology vectors span a saturated rank-three lattice
in Z4. Their integral quotient is Z. All monodromy generators fix the
primitive vector

\[
 v=(0,-1,1,0),\qquad v^\perp=\{a_1+b_2=0\}.
\]

This is a **monodromy coinvariant calculation**, not an asserted computation
of the total-space fundamental group or a section. An unframed construction
can have an additional capping relation in its group presentation; see
[Baykur--Korkmaz, Section 2.3](https://arxiv.org/html/1510.00089#S2.SS3).
The coinvariant module itself is preserved by Hurwitz moves and global
conjugation, so it remains an invariant of fibration isomorphism.

The saturated quotient \(v^\perp/\mathbb Z v\) is a symplectic rank-two
lattice. Choose \(p=(0,1,0,0)\), \(q=(-1,0,0,1)\); then \(p\cdot q=1\).
A cycle \(a\) projects to \((x,y)=(a_2+b_1,-a_1)\), and its transvection is

\[
 \begin{pmatrix}1+xy&-x^2\\y^2&1-xy\end{pmatrix}.
\]

If \(d=\gcd(x,y)\), this matrix is conjugate in SL(2,Z) to the
\(d^2\)-th power of a primitive positive transvection. The JSON retains each
actual induced matrix and a full integral conjugator, as well as an independent
unimodular basis witness for the saturated hyperplane.

These ten widths, in actual nonseparating order, are

```
1, 9, 1, 1, 1, 1, 16, 4, 1, 1.
```

Their sum is36. In the standard SL(2,Z) presentation
\(S^4=1, S^2=(ST)^3\), abelianization gives \(s=-3t\) and \(12t=0\).
Therefore a closed four-transvection subfactorization must have width sum
divisible by12. Among our210 four-element choices, the35 that pass have
**exactly widths9,1,1,1**.

This restriction survives arbitrary Hurwitz moves: each conjugating generator
fixes v and acts unimodularly on the quotient, preserving each transported
cycle's divisibility d. Global conjugation transports the primitive fixed
line and quotient with it. Hence any (4,3) summand must contain the unique
width-nine cycle (currently `four_three_B.3`) and three width-one cycles.
The width-sixteen and width-four lantern outputs must both belong to the
(6,7) side. This is a necessary condition, not a reverse equivalence.

## What the initial geometric candidate does not prove

Two adjacent-nonseparating inverse interchanges give one necessary integral
identity on the cycles labeled `four_three_B.3`, `four_three_A.6`,
`four_three_C.5`, `four_three_C.6`. Their full nonabelian relation still
matters. In the twenty-factor tuple, the second interchange has three
separating neighbors between its actors.

The direct carry and two opposite separating-gap preparations are rejected
before application at actual support27,28,46 respectively (bound20). Every
raw local equality and normalized preview match is retained. Their preview
prefixes are not reached routes or gathered blocks. No seven-factor identity,
summand, new (6,7), or completed connection follows from the homology hit.

## Why uniqueness needs a separate proof

Our monodromy coinvariants Z already distinguish this imported construction
from Nakamura's displayed (10,10) monodromy. In his Section3 calculation, the
vanishing cycles imply the homology relators

```
a1+a2=0, b1+b2=0, a1+a2+b2=0, a1+2a2-b1=0.
```

Those generate all of Z4, so his coinvariants vanish. The certificate checks
that determinant/rank statement. This comparison concerns the monodromies;
it neither identifies our total-space group nor asserts a section lift.
In particular, matching type cannot identify these two fibrations.

For (4,3), the known Baykur--Korkmaz, Hamada and Xiao factorizations describe
isomorphic fibrations by [Huang, Theorem1.1](https://arxiv.org/html/2602.20451#S1).
That theorem identifies those examples; it is not a classification of all
(4,3) factorizations. Even uniqueness of individual summands would not
specify the fiber-sum gluing map or imply cancellation of a common summand.

[Full necessary-test certificate](ten-ten-fiber-sum-audit.json).
Reproduce with `python examples/analyze_ten_ten_summand.py`.
