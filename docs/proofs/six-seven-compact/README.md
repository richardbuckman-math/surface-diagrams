# Compact (6,7) research route

Open [the graphical replay](index.html). It starts with a checked forward simplification of the original thirteen
factors: three Hurwitz moves, three global conjugations, and exact disk support
normalizations. Its conjugator score decreases from (44,7) to (32,6), with
154 braid letters. Richard designates this ending as the working (6,7).
Download the resulting factorization as JSON for the lab. The alternative longer
research route retains eleven chapters, fifty-four grouped transitions and
the complete 145-move replay in both directions. Braids connect vertically
with blue dotted factor separators and continuous strand colors. The standard-block extraction remains open;
this is not a completed explicit derivation from W0 W1.

[The new twenty-block extraction](../six-seven-fifty-blocks/index.html) isolates
an actual disk conjugate of W0 from the positive fifty using seven Hurwitz
moves and one sphere rechart. The remaining thirty has permutation orbits
of sizes 3,2,1, so it cannot alone be Hurwitz-equivalent to the transitive W1.
The closure page now gives a different direct proof: explicit chart changes
put that thirty on a five-point disk, where its faithful Artin action is
exactly a double outer-boundary twist. Its final cap is separately checked
on the sphere and in the genus-two lift. A jointly certified disk cut-system
comparison is shown. This does not construct an elementary W0 W1 Hurwitz
normal form or claim that the isolated thirty equals W1 as a factorization.

Rebuild from the repository root:

```sh
python examples/build_six_seven_compact.py
```

`source-route.json` retains the successful reverse branch. `frames.json`
contains explicit whole-column global conjugations. All used support
replacements are independently checked and stored in
`support-certificates.json`, including disk discrepancies, exact sphere
checks and the genus-two lift. Every drawn support passes the shared
surface renderer and a hard forty-cut-visit ceiling. Forty is a bound for
this presentation, not a minimality theorem. Additional sphere recharts
and original sphere moves are both visible in the page.

The longer route starts with the literal original thirteen words in its
forward direction. Its reverse direction ends there. The separate
simplification is disk-exact up to its explicitly recorded global frame. These are individual support pictures, not cumulative joint
cut-complex certificates. The browser downloads requested asset chunks
only, and performs no algebra initialization.

[Arc–braid cylinder calibration](calibration.html) checks the below-5 arc
against sigma4 sigma5 sigma4-inverse and its squared full twist.
