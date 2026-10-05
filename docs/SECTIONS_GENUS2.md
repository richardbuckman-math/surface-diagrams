# Sections in the genus-two factorization labs

A positive relation in the closed genus-two mapping class group gives a
Lefschetz fibration, but does not specify a section. A lift of its ordered
vanishing-cycle twists to a genus-two surface with boundary, with product
`t_delta_1^k_1 ... t_delta_r^k_r`, gives `r` disjoint sections with squares
`-k_1, ..., -k_r`. The location of each boundary and the exact framed relation
must be checked; a picture of a point away from the cycles is not enough.
[Baykur–Korkmaz, Section 2.2](https://arxiv.org/pdf/1510.00089) state this
convention.

| Fibration | Relation available here | Section evidence |
| --- | --- | --- |
| `(4,3)` | Seven normalized six-strand factors pass the exact sphere-action check and have `+I` closed genus-two homology action. | Three disjoint `(-1)`-sections are given by the three-boundary lift in Huang, Remark 4.1. The package has not independently checked that framed lift. |
| `(6,2)` | Matsumoto's framed eight-factor relation is documented, but its curves are not encoded as package braid factors. | Its one-boundary relation gives one `(-1)`-section; Hamada proves four disjoint `(-1)`-sections in genus two. |
| `(10,10)` | Nakamura's 20-factor construction is documented, but its curve factors are not encoded as package braid factors. | No section is certified here. Nakamura proves the total space minimal, excluding a `(-1)`-section; sections of other squares are unresolved by these records. |
| Supplied `(6,7)` | Its thirteen-factor closed genus-two identity is independently verified in this package. | No section of this **specific ordered factorization** is certified. See [the detailed search note](SECTIONS_6_7.md). |

For `(4,3)`, [Baykur–Korkmaz, Theorem 7](https://arxiv.org/pdf/1510.00089)
give `t_e t_x1 t_x2 t_x3 t_d t_c t_x4 = t_delta`, already yielding one
`(-1)`-section. [Huang, Theorem 1.1 and Remark 4.1](https://arxiv.org/pdf/2602.20451)
prove that the Baykur–Korkmaz, Hamada, and Xiao factorizations describe
isomorphic fibrations and exhibit a lift with three boundary components.
[Akhmedov, Section 8 and Appendix B](https://arxiv.org/pdf/2609.17634)
give Xiao's ordered Artin strings. Two printed disk braids require a central
hyperelliptic-involution correction to lift to the **geometric** separating
twists. [The source records](../src/surface_diagrams/fibration_lab_seeds.py)
keep both the printed braids and normalized positive factors. The normalization
is an equality upstairs on the closed genus-two surface; the disk braids differ.
The source obtains its strings by numerical branch continuation, then checks
their algebraic braid relations exactly. The package checks the normalized
product's sphere action and genus-two homology; it does not yet encode the
three-boundary section lift.

For `(6,2)`, [Baykur–Korkmaz, Section 3.3](https://arxiv.org/pdf/1510.00089)
record Matsumoto's `(t_B0 t_B1 t_B2 t_c)^2 = t_delta` in the one-boundary
genus-two mapping class group. [Hamada, Theorem 2](https://arxiv.org/pdf/1610.08458)
constructs four disjoint `(-1)`-sections of the genus-two
Matsumoto–Cadavid–Korkmaz fibration. A six-strand encoding must specify the
curves and prove the ordered product before an interactive seed can carry this
section data.

For `(10,10)`, [Nakamura, Section 3](https://arxiv.org/pdf/1811.03708)
constructs the closed genus-two relation from three copies of a `(4,3)`
relation, Hurwitz moves, and a lantern substitution. His minimality result
rules out a `(-1)`-section. An explicit marked-point or boundary-framed lift
would be needed to claim any other section.

For the supplied `(6,7)` relation, [Szabó, Section 9.5](https://arxiv.org/pdf/2609.34042)
states that Xiao's degree-four fibration admits a smooth section but no
holomorphic section; he leaves the marked-point verification to the reader.
Matching type and some branch-point data do not establish equivalence with the
supplied ordered factors. That section assertion therefore cannot be
transferred to our `(6,7)` lab without a checked equivalence or a direct
marked-point lift.
