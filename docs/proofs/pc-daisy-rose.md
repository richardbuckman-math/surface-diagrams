# Puncture-capped daisy and rose derivations

Write $T_A$ for a positive Dehn twist about a curve enclosing the marked
points in $A$. The superscript `under` below specifies the route of a curve
whose endpoints are separated by other marked points. Products are written in
the lab's top-to-bottom factor order. These are identities in a **marked
disk**: the twist around one marked point is trivial. Framed inner boundaries
would contribute their own boundary twists.

For four points, put $U_{24}=T_{24}^{\mathrm{under}}$,
$U_{14}=T_{14}^{\mathrm{under}}$, and let
$U_{124}=T_{124}^{\mathrm{under}}$ go under point 3. Two instances of the
puncture-capped lantern relation give

$$
T_{1234}T_{12}=T_{123}T_{34}U_{124},
\qquad
U_{124}=U_{24}U_{14}T_{12}.
$$

The first lantern treats the disk enclosing points 1 and 2 as one entry,
alongside points 3 and 4. The second splits the under-going curve around
1, 2, and 4. Substitution gives

$$
T_{1234}T_{12}=T_{123}T_{34}U_{24}U_{14}T_{12}.
$$

Cancel $T_{12}$ on the right:

$$
\boxed{T_{1234}=T_{123}T_{34}U_{24}U_{14}.}
$$

Thus an inverse twist appears only during cancellation, not among the final
positive factors. In the project's signed braid generators, the two
under-going factors are

$$
U_{24}=\sigma_3^{-1}\sigma_2^2\sigma_3,
\qquad
U_{14}=\sigma_3^{-1}\sigma_2^{-1}\sigma_1^2\sigma_2\sigma_3.
$$

The exact Artin action checks both lantern steps and the resulting four-factor
identity in $B_4$, before taking a sphere quotient or using a support image.

For $n\geq3$, define

$$
U_{i,n}=(\sigma_{n-1}^{-1}\cdots\sigma_{i+1}^{-1})
\sigma_i^2(\sigma_{i+1}\cdots\sigma_{n-1}).
$$

The same argument yields the recursive PC daisy relation

$$
T_{1\ldots n}=T_{1\ldots n-1}
U_{n-1,n}U_{n-2,n}\cdots U_{1,n}.
$$

Specifically, apply the capped lantern to the entries
$\{1,\ldots,n-2\},\{n-1\},\{n\}$, then apply the
$(n-1)$-point formula inside the under-going twist about
$\{1,\ldots,n-2,n\}$. The repeated
$T_{1\ldots n-2}$ is at the right and cancels. Starting with the two-point
twist and iterating gives $\binom n2$ pairwise twists, a puncture-capped
rose factorization. For four points, the lab instead expands the leading
$T_{123}$ using its existing three-point PC lantern, so the visible rose is

$$
T_{12}\,T_{13}^{\mathrm{PC}}\,T_{23}\,T_{34}\,U_{24}\,U_{14}.
$$

The substitutions are available in the boundary-twist playground for four
and five marked points. Each replacement is checked against the full disk
Artin action, and the support drawings are made by the common surface
library. The general identity was checked in code for three through six
points; that finite check supplements the lantern induction above.

The mapping-class interpretation of pure braid twists and lantern relations
is developed by [Margalit and McCammond, *Geometric presentations for the pure
braid group*](https://margalit.droppages.net/papers/pure-braids.pdf), especially
their swing/Dehn-twist presentation in Section 4. The precise under-going
word order here follows this project's braid convention and was independently
checked by its exact action engine.
