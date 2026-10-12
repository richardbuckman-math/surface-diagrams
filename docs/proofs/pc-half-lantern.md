# Puncture-capped half lantern

In a disk with three marked points, write $H_{12}$ for the positive half twist
on the arc joining points 1 and 2, and $T_{ij}$ for a positive Dehn twist
enclosing the indicated pair. Products are in the playground's top-to-bottom
order. The puncture-capped lantern gives

$$
T_{123}=T_{12}T_{13}T_{23}.
$$

Split $T_{12}=H_{12}^2$, then make two Hurwitz moves:

$$
\begin{aligned}
T_{123}
 &=H_{12}\,H_{12}\,T_{13}\,T_{23}\\
 &=H_{12}\,T_{23}\,H_{12}\,T_{23}\\
 &=H_{12}\,(T_{23}H_{12}T_{23}^{-1})\,T_{23}\,T_{23}.
\end{aligned}
$$

The first move uses $H_{12}T_{13}H_{12}^{-1}=T_{23}$. In the second,
the middle $T_{23}$ moves past the half twist, conjugating that half twist.
The two neighboring $T_{23}$ factors then combine:

$$
\boxed{T_{123}=H_{12}\,(T_{23}H_{12}T_{23}^{-1})\,T_{23}^{2}.}
$$

In the project's braid generators this is

$$
(\sigma_1\sigma_2)^3
=\sigma_1\,(\sigma_2^2\sigma_1\sigma_2^{-2})\,\sigma_2^4.
$$

Each line, and the direct three-factor substitution, is checked by the exact
Artin action in $B_3$. Conjugating the whole relation transports it to any
three-point support in a larger marked disk. The playground preserves that
conjugator when applying the substitution.

Turning a marked point into an inner boundary is a **proposed uncapping**.
The displayed braid equality still certifies the relation only after all
inner boundaries are capped to punctures. In this particular relation, if
point 3 alone becomes an inner boundary, the ordinary lantern relation gives
the precise correction:

$$
T_{123}T_3=H_{12}\,(T_{23}H_{12}T_{23}^{-1})\,T_{23}^{2}.
$$

Here $T_3$ is the positive twist parallel to the third inner boundary.
This framed equality follows from the ordinary lantern and the same two
Hurwitz moves, but it is not yet certified by the playground's calculation
engine. See [Margalit and McCammond, *Geometric presentations for the pure
braid group*, Theorem 5.1](https://web.math.ucsb.edu/~mccammon/papers/pure-braids.pdf)
for the distinction between punctures and inner boundaries.
