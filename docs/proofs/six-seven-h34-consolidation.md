# First factor-level consolidation in the (6,7) relation

This is a checked intermediate step toward a structural derivation, **not** a
derivation of the whole (6,7) relation. The supplied product has 13 factors:
seven squared three-point Dehn twists and six half twists. Its disk braid is
not the identity. The complete product represents the identity mapping class
of the six-punctured sphere, but the corresponding spherical braid is its
nontrivial central full twist.

Split the seven squared three-point twists F1, F4, F5, F8, F10, F12, and F13
into two ordinary copies each. Apply the puncture-capped half lantern to the
first copies of F1 and F8. Their first terms are both **exactly** the standard
half twist H34 in the disk braid group, even though F8's original support is
written with a conjugator. Apply the three-point puncture-capped lantern to
F5's first copy; its third term is exactly T34.

Now move the F8 half twist upward through 13 intervening factors by adjacent
Hurwitz moves. The moved H34 remains fixed; each crossed factor is conjugated.
The two neighboring H34 factors combine into T34. Move F5's T34 upward through
nine factors in the same way, then combine the two neighboring T34 factors:

```text
H34, H34, T34  →  T34, T34  →  T34².
```

The arrows here suppress the intervening factors, which change under the
Hurwitz moves. The [replayable lab session](https://richardbuckman-math.github.io/surface-diagrams/lab/six-seven-h34-session.json)
records all 35 states, including the original product and every adjacent move.
Use **Load H₃₄ derivation steps** in the [(6,7) lab](https://richardbuckman-math.github.io/surface-diagrams/lab/index.html),
then open Exploration history and select any step. Every substitution and move
preserves the complete exact disk Artin action; the saved session is checked
again when loaded. The final product starts with a standard T34². Its full
sphere outer action is still trivial, as it must be.

This consolidation by itself does not simplify the rest of the product into
the two complementary triple twists of the known sphere-braid certificate.
The next search should trace the other half-lantern petals and the remaining
pair twists through additional Hurwitz moves, testing candidate PC daisy and
rose substitutions without replacing exact checks by visual resemblance.
