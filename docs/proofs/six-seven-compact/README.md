# Compact (6,7) research route

Open [the graphical replay](index.html). It starts with a checked forward simplification of the original thirteen
factors: three Hurwitz moves, two global conjugations, and exact disk support
normalizations. Its conjugator score decreases from (44,7) to (36,6). Download
the resulting factorization as JSON for the lab. The alternative longer
research route retains eleven chapters, fifty-four grouped transitions and
the complete 145-move replay in both directions. Braids connect vertically
with blue dotted factor separators and continuous strand colors. The standard-block extraction remains open;
this is not a completed explicit derivation from W0 W1.

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
