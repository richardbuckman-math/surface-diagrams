# An explicit connection after taking homology

The imported (10,10) monodromy **does connect in Sp(4,Z)** to the original
thirteen-factor (6,7) monodromy together with a conjugate of the checked
(4,3) monodromy. This answers the homological version of the question.
The corresponding Lefschetz-fibration decomposition remains **open**.
The particular previously saved curve lift is now ruled out: all 120 choices
of three separating factors fail an exact marked-sphere character, although
their Sp(4,Z) products are I. A different geometric candidate is required.

The certificate applies the integral homology representation to the exact
published twenty-factor input. It retains all twenty matrices during 134
formal adjacent matrix Hurwitz operations, followed by one common integral
symplectic conjugation. Each factor in the final seven- and thirteen-factor
matrix blocks matches its stated target individually. No geometric curve
move, gathered curve block or lantern substitution is applied.

## The two matrix blocks

The starting necessary target is the previously saved four-half homology
identity on B.3, A.6, C.5 and C.6. Its geometric gap lifts were already
rejected before application or retained as unbounded diagnostics. They are
not being promoted to a reached geometric route here.

For the matrix calculation only, assign B.1, B.2 and B.4 to that block.
They are separating twists and act as I. The formal matrix gather keeps
every other factor and conjugates its matrix by the actual Hurwitz formula.
The selected seven-matrix product is I, and so is the residual thirteen-matrix
product. Both sets of nonseparating vectors span saturated rank-two lattices.
Their integral symplectic areas are 3 and 4, respectively.

The six residual vectors, before the final internal matrix normalization, are

```
(1,  1,  1, -1)   B.7
(1,  7,  3, -1)   B.5
(3, 24, 10, -3)   B.6
(1, 10,  4, -1)   A.7
(0,  3,  1,  0)   new.half-lantern.2
(-2, 1, -1,  2)   new.half-lantern.3
```

One internal interchange, a carry across two half matrices and the intervening
separator identities, and an expanded cyclic start put this block into the
original (6,7) form. In the integral pair basis

```
a=(1,4,2,-1), b=(0,3,1,0), a.b=4,
```

the resulting six unoriented coefficients are exactly

```
(1,0), (0,1), (1,-3), (1,-2), (-2,3), (1,-1).
```

These are the coefficients of the project's original six vanishing classes.
All seven separator slots also match, since their matrices are I. A separate
internal matrix interchange and cyclic start identify the selected four-half
block with the checked (4,3) matrix factorization.

## The integral changes of chart

The certificate supplies full integral symplectic matrices, rather than only
an isomorphism between the two rank-two subspaces. They map the normalized
selected and residual blocks to their original (4,3) and (6,7) targets:

```
C4 = [ 0  1 -1 -4 ]       C6 = [ 1  0  0 -2 ]
     [ 0  1  0 -4 ]            [ 2 -1  2  0 ]
     [ 1  0  1  0 ]            [ 0  0  1  2 ]
     [-1  0 -1  1 ]            [ 0  0  0 -1 ]
```

With J the standard integral symplectic form, both satisfy C^t J C=J.
Every actual target factor is matched by conjugating its complete 4x4 matrix.
After the one common conjugation C6, the complete twenty-matrix word is

```
G rho(A4,3) G^-1  followed by  rho(F6,7),

G = C6 C4^-1 = [ 1 -1 -1 -2 ]
               [ 0 -1 -2 -4 ]
               [-1  1  2  2 ]
               [ 0  0 -1 -1 ].
```

Here rho is the homology representation. G specifies the gluing at this
linear level. It does not specify a complete mapping-class gluing lift.
The original (6,7) target is `factorization_explorer.initial_factors`, not
a newly extracted factorization or a new preferred presentation.

## The particular curve lift fails beyond homology

The earlier expanding sphere-curve test had 23 nonidentity witnesses and 97
UNKNOWN results at its word bound. A different quotient now settles all 120
choices for that same unselected class target; none is a sphere identity.
The old raw reports and their UNKNOWN flags are preserved as historical data.
Their bounds are not increased, and no previous failed carry is applied.

For a pure disk braid let L_ij be its integral labeled pair-linking numbers.
For four distinct labels define

```
chi(a,b,c,d) = L_ab + L_cd - L_ac - L_bd.
```

The sphere braid presentation adds the point-around-all-others relation.
Passing to the marked-sphere mapping class group also kills the central
full twist; see [Bellingeri's lecture notes, slides 10 and 14](https://www.mun.ca/aac/media/production/memorial/academic/faculty-of-science/mathematics-and-statistics/atlantic-algebra-centre/media-library/aacminicourses/paolobell/aac2.pdf).
In linking coordinates their conjugates are vertex-star vectors and the
all-ones vector. The displayed character annihilates each of those vectors.
It therefore descends to the pure marked-sphere mapping class group. This
deduction gives a necessary test: a nonzero value proves nonidentity, while
zero remains inconclusive. It does not identify the central spherical braid
or determine a genus-two lift sign.

The certificate reconstructs the known unbounded class target algebraically,
without curve simplification, and retains all twenty records. Every choice
of three of its ten separators has a nonzero character. For B.1/B.2/B.4,
the same three identity matrices used in the formal split, one witness is

```
chi(1,2,3,5) = L12 + L35 - L13 - L25 = 0 + 2 - 0 - (-4) = 6.
```

This rules out only those 120 seven-factor words with their fixed four
hypothetical half classes and saved separator classes. Other curve changes,
other lifts of the matrix data and general Hurwitz decompositions remain
unexcluded. Pair-linking characters are not arc crossings or drawing bounds.

## What is still missing

The homology representation sends every separating twist to I and loses
Torelli information. It also identifies many distinct nonseparating curves.
Thus a seven-matrix identity is not a seven-factor genus-two identity.
The 134 checks here are **matrix checks**, not134 bounded geometric moves,
external curve checks or a shortening of any published derivation.

To answer the original question affirmatively, a new candidate needs full actual
seven-factor sphere and chosen+I certificates, all changed twenty-factor
contexts, a verified residual thirteen-factor relation and a complete
Hurwitz/global certificate at the curve level. The previously rejected
support27/28/46 carries and unbounded140 target remain rejected/unapplied.
No new sphere redraw, lantern substitution, section lift, total-space group
claim, uniqueness theorem or indecomposability conclusion follows here.

Both published fibration derivations and all their source charts, graphics
and PDFs remain unchanged. The earlier
[necessary fiber-sum audit](ten-ten-fiber-sum-audit.md) retains its exact scope.

[Full matrix certificate](ten-ten-homology-connection.json).
Reproduce with `python examples/analyze_ten_ten_homology_connection.py`.
