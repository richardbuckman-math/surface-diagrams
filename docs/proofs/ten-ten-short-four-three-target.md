# A genuine (4,3) target using six existing curves

There is now a complete seven-factor **(4,3) relation** using six curves
literally present in the published (10,10), together with one specified
additional half-twist class. Its product is checked faithfully in the disk,
on the marked sphere, and in the chosen genus-two lift. This supplies a
concrete geometric target for the reverse connection.

It is **not yet an extracted summand**. The missing half has not been
produced or gathered through Hurwitz moves on the twenty-factor input.
The Lefschetz-fibration decomposition remains **open**.

[The two support panels](ten-ten-short-target/index.html) show the known
C block and the target. [The complete certificate](ten-ten-short-four-three-target.json)
retains every word, ordered factor, internal crossing and point-pushing
kernel. The [published (10,10) derivation](fibration-derivations/10-10.html)
is unchanged.

## The ordered target

Use the exact twenty factors in `fibration-derivations/10-10.json`, with
SHA256 `2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e`.
The proposed seven-factor word is

```
B.1 B.2 B.3 B.4 Hstar C.5 C.6.
```

B.1, B.2, B.3, B.4, C.5 and C.6 are the literal source records at
zero-based positions 3, 4, 5, 6, 18 and 19. Three are positive separating
twists and three are positive half twists. Define the fourth half by

```
g = sigma5^-4 sigma2^-2,
Hstar = g C.5 g^-1.
```

Negative letters occur only in the conjugator; Hstar is a positive unit
half twist. Its homology vector is `(1,-6,-2,-1)` in the saved chart.
None of the ten current half factors has its transvection matrix, so
Hstar is an additional desired class, not an existing source factor.
Calling its proposed ancestry A.6 does not supply that ancestry.

The exact disk support word of Hstar is

```
(-6,-5,-6,-5,-6,-5,-6,5,6,5,6,5,6,-3,-2,-3,2,3).
```

The seven support lengths in order are `3,7,12,3,18,6,8`. The target has
maximum 18, total 57 and 96 stored braid letters. These are individual
support-word metrics, not arc crossings, a jointly minimal drawing or a
whole-proof complexity bound.

## Recognition by the known C relation

Take the independently checked original C block from
`10-10.json:source_exact_blocks.2`. Embed it by adding a point on the LEFT,
shifting every generator and first index by one. Its product is
`D(2..6)^2`.

Apply these four adjacent Hurwitz operations **inside that standalone
reference block**, using zero-based source/target positions:

```
(4,5), (5,6), (4,5), (6,5).
```

For source position less than target, `[a,b]` becomes
`[a b a^-1,a]`; for the reverse direction it becomes `[b,b^-1 a b]`.
The full raw free-word discrepancy is empty for every operation before
any individual presentation is compared. The four raw support maxima are
`12,18,18,18`, all bounded by 20 before acceptance. Every untouched
reference factor remains literal at each crossing.

The endpoint matches the target in all seven individual faithful B6
actions. Reference C.1, C.2, C.3, C.4 and C.7 match target B.1, B.2, B.3,
B.4 and Hstar; C.5 and C.6 match their corresponding literal target
records. This is a recognition map, not an ancestry transfer in the
twenty-factor source.

Two alternate internal reference proofs were also checked. The direct
two-crossing proposal rejects its first crossing at raw support 22.
The inverse-prepared proposal passes one preview at 18 but rejects the
next at 106. Neither rejected proposal is selected or applied. The full
four-crossing forward-prepared proof is the bounded one retained here.
These finite comparisons do not exclude other reference proofs.

## Disk, sphere, lift and nonabelian checks

The target and all five chosen reference states have full faithful B6
product equal to `D(2..6)^2`. The complete discrepancy word is retained;
this is braid equality, not a claim of raw free cancellation. The embedded
five-point boundary is never assumed central in B6.

The target first passes all thirty pure marked-sphere linking characters.
Separately, all five sphere-chain arcs are fixed by the full product, and
the chosen integral homology action is +I. These three assertions are
retained independently; a zero linking character alone would be
inconclusive. No unquotiented spherical-braid equality, framed-section
lift or total-space group calculation is inferred.

Every factor has its complete fixed-last-strand nonabelian kernel and
shadow, with reconstruction, when that split applies. Halves moving the
last strand retain their full faithful action instead. The full product
is pure and has a complete F5 kernel in B6. All source words also lie in
the explicitly embedded B5 subgroup with a literally vertical first
strand. The inverse embedding is verified on every meridian, giving a
complete F4 kernel and B4 shadow for the embedded product. Both product
kernels have eight letters and their stored shadows have 44; the actual
and reference nonabelian kernels agree literally and the full shadow
actions agree. This inverse embedding is not an applied deletion or
sphere move.

A nearby target demonstrates why exact curve recognition matters.
Replacing B.2 with actual C.2 and putting it before B.1 retains Sp4
product I and all thirty zero sphere characters. Nevertheless the full
sphere image of arc `(1,2)` differs, with 5,834 letters. B.2 and C.2 have
the same labeled support and linking data but different faithful disk
actions. This particular nearby word is not a relation.

## What remains

There are **zero moves on the actual twenty-factor input** in this
certificate. Hstar needs an actual ancestry-preserving supply and a
bounded gather of the complete seven-factor block. Every donor and crossed
neighbor must be tracked; changing only a hypothetical A.6 entry does not
preserve the whole source product. A successful construction must also
retain the residual thirteen factors, prove their full (6,7) closure and
provide the complete Hurwitz/global-conjugation certificate.

The four internal reference moves prove that this standalone target is
isomorphic to the known C (4,3) factorization. They do not connect the
original (10,10) to a fiber sum. No lantern substitution is used as an
isomorphism, and no preferred proof, payload, viewer or PDF is changed.
