# Optional thirty-half sphere ending

The second-exterior research endpoint has a certified optional sphere ending
with **thirty positive half twists and a connected endpoint graph**. It is
**not** a derivation to the standard thirty word. The complete named proof
remains 106 steps; no public graphical replay or PDF changes.

The full reproducible records are in
[six-seven-alternative-thirty.json](six-seven-alternative-thirty.json).
Run `examples/analyze_alternative_thirty.py` to regenerate them.

First the two visible exterior twists are brought together by three retained
adjacent disk checks and combined into their square. The two subsequent
sphere operations are separate and explicitly labeled in the report.

1. **SPHERE MOVE: cap BOTH exterior twists together.** The full and local
   disk discrepancies are retained, with writhe 40. The marked-sphere action
   is exactly trivial and the separately checked chosen genus-two lift is
   `+I`. A single exterior cap has `-I`; the two were not deleted separately.
2. **SPHERE MOVE: complement the remaining four-point curve.** Its conjugator
   is retained while standard `T1234` becomes `T56`. The actual endpoints
   are 2 and 6. Full and local discrepancies have writhe 10, exact trivial
   marked-sphere action and separately checked `+I` lift. The disk mapping
   classes differ.

Each of the fourteen remaining full-pair records is then expanded into its
positive halves. One squared record supplies four halves. All fourteen
ordered local expansions retain freely cancelling disk-word certificates.
The result has thirty unit positive halves, trivial marked-sphere action,
`+I` lift and a connected six-vertex endpoint graph. The audit asserts marked-sphere mapping classes and the separately checked
chosen lift. No identity in the spherical braid group before its central
quotient, or framed-hole identity, is asserted.

The chosen disk product has the following pair-linking matrix. Entries count
half the signed crossings between the actual labeled strands; they are
computed independently from the complete braid word.

| Strand | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 2 | 1 | 1 | 1 | 0 |
| 2 | 2 | 0 | 2 | 2 | 2 | 1 |
| 3 | 1 | 2 | 0 | 1 | 1 | 0 |
| 4 | 1 | 2 | 1 | 0 | 1 | 0 |
| 5 | 1 | 2 | 1 | 1 | 0 | 0 |
| 6 | 0 | 1 | 0 | 0 | 0 | 0 |

The standard disk word `(12345)^6` has every off-diagonal entry equal to one.
Here the fifteen entries above the diagonal contain four zeros, seven ones
and four twos. A disk Hurwitz move preserves the whole ordered product,
**including a move between individual halves**. Disk global conjugation only
permutes its pair-linking labels. Consequently neither disk-only Hurwitz
moves nor disk global conjugations can turn this chosen lift into that
standard disk full twist. Splitting the pairs alone does not bypass this
obstruction. Further explicitly certified sphere changes remain possible;
no sphere-Hurwitz orbit exclusion is claimed.

The matrix difference suggests a precise positive sphere template: replace
a peripheral five-petal point-2 star by a peripheral point-6 star. This is
saved under `point_star_probe.next_peripheral_star_substitution` as **TARGET
ONLY**, with `applied=false` and `requires_transport=true`. Both canonical
stars have trivial marked-sphere action and `-I` lift. Their **coupled SPHERE
substitution** has `+I` lift and a full nonzero disk discrepancy, despite
writhe zero. Its pair-linking change would repair the displayed matrix, but
that is not an ordered braid equality or a reached substitution.

None of the eight unchanged cyclic point-2 star subsequences already realizes
that peripheral configuration. After point 2 is moved to strand 6 in a
separate diagnostic frame, all five petal shadows vanish, but their complete
nonabelian point-pushing product loops do not match the peripheral loop.
The report retains every individual Schreier split and all eight product
loops. This is a finite failure for these unchanged subsequences, not a
claim about arbitrary transports or half-twist Hurwitz moves.

The next useful move must either expose an actual peripheral star with its
full ordered certificate, or make a different specific positive geometric
simplification. Connected endpoints, matching length and a repaired linking
matrix are only necessary checks. The full proof and both prior research
endpoints remain available unchanged.

Validation: 32 focused tests cover both explicit sphere moves, separate lift
checks, all half expansions, linking signs and labeled tracking, nontrivial
half Hurwitz/global-frame invariance, unknown handling, the unapplied coupled
star template and all eight retained nonabelian failures. No new graphical
artifact was produced, so no UI or PDF reinspection is needed.