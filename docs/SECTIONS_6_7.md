# Searching for sections of the supplied (6,7) factorization

The supplied 13 factors comprise six half twists and seven squared twists
around three branch points. Under the double cover of the six-point sphere,
they become six nonseparating and seven separating positive Dehn twists on a
closed genus-two surface. The exact sphere-action certificate says their
product projects to the identity. The integral five-chain homology calculation
in `hyperelliptic_homology.py` gives `+I` for the 178-letter product. By the
genus-two [Birman–Hilden exact sequence](https://celebratio.org/Birman_JS/article/471/),
the only other lift of the sphere identity is the hyperelliptic involution,
which acts by `-I` on homology. Thus the supplied product is the identity in
the **closed genus-two mapping class group**. This establishes the monodromy
relation, not a section.

The six half twists exchange branch-point pairs in this order:
`(3,6), (1,4), (2,5), (3,6), (1,4), (2,5)`. Every branch point moves, so a
fixed Weierstrass point gives no immediate section. The three two-element
orbits are prospective degree-two multisections, subject to checking their
extensions through singular fibers. The simple extra point at infinity also
fails: the full braid is not a power of the disk full twist, so its canonical
lift fixing that seventh point is nontrivial. This does not rule out a section
whose point moves in the chosen planar presentation.

The six nonseparating vanishing-cycle classes span a primitive rank-two
sublattice of `H_1(Sigma_2; Z)`, and all their pairwise algebraic
intersections are divisible by four. Their quotient in fiber homology is
`Z^2`. Without a section, an extra final-handle relation may reduce the
homology of the total space; this quotient is only a comparison invariant.

There is a strong lead in [Szabó's September 2026 calculation of Xiao's
degree-four fibration](https://arxiv.org/pdf/2609.34042), especially Theorem B
and Section 9.5. His distinct ordered factorization also has type `(6,7)` and
three repeated branch-point pairs. He states that Xiao's fibration has a
**smooth section but no holomorphic section**, with the smooth marked-point
verification left to the reader. The pair pattern, intersection divisibility,
and rank-two quotient match our data, but the factor orders differ. We have
not established Hurwitz equivalence, so his section cannot yet be assigned to
the supplied factorization.

For an exact search, choose a point `p` off all thirteen vanishing cycles and
lift the twists to `Mod(Sigma_2, p)`. Their product is a point push `P_gamma`.
Draw a filling set of arcs and curves based at `p`, apply every pointed twist,
and use the resulting exact itineraries to read `gamma`. If `gamma=1`, the
pointed relation constructs a section. Repeat over meaningful complementary
regions and under checked Hurwitz changes; a visual coincidence alone is not
enough. [Baykur–Hamada](https://arxiv.org/pdf/2610.01776), Sections 2.1–2.3,
also give an invariant obstruction in the vanishing-cycle quotient: a nonzero
obstruction rules out sections, but zero in that quotient alone does not prove
one exists.

Once a marked lift succeeds, replace `p` by a boundary circle. If the product
in `Mod(Sigma_2^1)` is `t_delta^k`, the section has self-intersection `-k`
with the usual positive-twist convention. [Akhmedov–Monden](https://arxiv.org/pdf/1809.09542)
prove every type `(6,7)` genus-two fibration is minimal, excluding a `-1`
section; the [Smith–Stipsicz bound](https://arxiv.org/abs/1104.1037) excludes
nonnegative square for a nontrivial fibration. Any section here must therefore
have square at most `-2`. Neither the existence nor the square of a section of
the **supplied** factorization has been certified.
