# Common tetrahedron-cluster nets: novelty and computational audit

20 October 2026. Status: reproducible computational findings, not a claim of
publication priority or an external expert review.

## Prior art found

The five-unit construction is **not new**. Rick Mabry's
[Common unfoldings of the 12-faced deltahedra](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common8V.html)
explicitly displays a net for all seven face-joined clusters of five regular
tetrahedra. His page describes that material as present before 14 November
2024, much of it earlier. The pictured net is often described there as a cobra.
Our twelve-triangle paper pattern, including its fixed hinge edges, agrees
exactly with a lattice transcription of that figure, modulo planar rotations,
reflection, and translation. `audit.mabry_five_reference()` stores that
transcription and its provenance. No new five-unit construction is claimed.

Mabry also explains why three additional twelve-triangle *outlines* can cover
the targets if the internal cuts may be changed for different targets. That
is a different puzzle from one sheet with fixed cuts. His negative result
for the long parallelogram addresses a question from Powarzynski and Spiegel,
*Elemente der Mathematik* 34 (1979), 140-146. Thus the smaller examples and
the failure of that particular strip have a substantial history.

The [four-unit page](https://lsusmath.rickmabry.org/rmabry/dodec/delta/common.html)
provides prior constructions and individual inventories of 452, 280, and 203
nets for its three cluster types. It reports 16 common nets. There is a
remaining count discrepancy, detailed below; do not silently use 16 as a
successful calibration of our intersection computation.

The [2024 survey by Valente-Matias and Araújo](https://www.gathering4gardner.org/g4g15gift/ExchangeArchive-CommonNetDatabase-G15-017-1.pdf)
is useful background but is not a complete priority search for this problem.
In particular, the separately indexed twelve-face Mabry page was missed by
our initial broad searches. This is a concrete reason not to infer novelty
from search-engine silence. The [polytet catalog](https://sicherman.net/polytets/index.html)
independently gives the familiar cluster counts; those counts are not new.

Targeted searches for common nets/unfoldings, polytets/pentatets,
pentatetrahedra, fourteen-face deltahedra, six tetrahedra, and the 19/23 bound
have not yet located a source for the six-unit extremal result. This remains
an incomplete literature search, not proof that the result is unpublished.

## Exact model

One volume unit is a regular tetrahedron. Clusters are joined along whole
faces, have no overlapping interiors, and are identified up to rigid motions
and reflection. There are seven five-unit and 23 six-unit types.

Paper consists of unit equilateral triangular panels. Cuts and hinges are
fixed for all target shapes. Only whole edges may hinge. Internal slits and
using either side of the sheet are allowed. No new cuts between targets,
interior-face creases, stretching, hidden layers, or overlapping panels are
allowed. The certificates establish folded end states, not continuous
collision-free folding paths. Novelty and optimality must retain this scope.

## Second implementation

`experiments/common_nets/audit.py` independently builds surface transitions
from shared **3D vertex coordinates** and all six vertex bijections per face.
It does not call `engine.neighbor`, `engine.attach`, or `engine.fold_net`.
It unfolds each source tree by explicit reflection of the third paper vertex.
The two implementations agree on all tested source-four-target combinations.

The audit deliberately shares the input cluster catalog, the edge-subset
spanning-tree enumerator in `verify_six.py`, and the exact determinant used
to check enumeration totals. It is a second geometric implementation, not
a wholly independent software stack and not an outside review.

The five-unit audit exhausts 6,000 source spanning trees and finds exactly
one common fixed-hinge paper net, up to planar symmetry. It has no internal
slit and is the same net already displayed by Mabry. Uniqueness within this
precise model is a checked computational statement; no novelty is asserted
for it without closer comparison with his full enumeration.

For six units, the new checker independently verifies the positive 19-target
net and completes these four source catalogs:

| Source ID, zero-based | Source spanning trees | Nonoverlapping unfoldings | Coverage bound |
|---:|---:|---:|---:|
| 5 | 25,645 | 16,329 | 19 |
| 0 | 25,935 | 21,029 | 19 |
| 1 | 26,224 | 16,942 | 19 |
| 9 | 26,397 | 16,882 | 19 |

Total: 104,201 source trees. Every surviving net fails at least four targets,
after every possible target root-face vertex bijection is considered. This
is not a time-limited search. The audit saves the exact input SHA-256 digest.

**Why four sources suffice.** A net folding into at least 20 of 23 targets
must fold into at least one of these four sources: only 19 targets lie
outside them. It would therefore appear in one of the four complete source
inventories, where the checker rules out coverage above 19. The explicit
19-target net attains the bound.

**Why source trees suffice.** If a connected common net had additional
hinges forming cycles, one could cut some of them to obtain a spanning tree
while retaining every folding. Each such tree unfolds uniquely, up to plane
isometry, from one fixed root face. This includes the fixed-slit cases.

## Unresolved four-unit discrepancy

The new checker exactly reproduces the individual inventory counts
203, 280, and 452. Its set intersection has 47 distinct fixed-hinge nets,
with 37 different triangular footprints. The original engine agrees.
Mabry's page reports and pictures 16 common nets.

Trying a fixed outward paper side does not remove the discrepancy. Nor does
merely ignoring the hinge decoration: 37 is still different from 16. Among
the 47, 35 have no internal slit and twelve have one. Do not claim that
slits, paper side, or a typo explains the difference without further evidence.
It may reflect another convention or a mistake in either enumeration.

Next compare the actual pictured patterns and the downloadable per-pattern
catalog with the computed intersection, and isolate a smallest explicit
disagreement with all three fold certificates. Only then ask the author
whether a restriction has been overlooked. No one has been contacted.

An unsent question for external review is: "Our single-surface inventories
agree with your 452/280/203 counts, but the fixed-cut intersection has 47
nets (37 outlines), rather than 16. Which additional condition should our
enumeration impose? We can supply a concrete net and face/hinge maps."

## Reproduction and claims

```text
python -m experiments.common_nets.audit
python -m unittest tests.test_common_nets -v
```

The default input is `.preview/common-nets/tetrahedra.json`, generated by the
earlier enumeration. The output is `independent-audit.json` in the same folder.
`--small-only` checks the four- and five-unit cases without the six-unit bound.
Positive drawings and the original atlas remain separate from this audit.

Current wording: **The five-unit construction is a rediscovery of Mabry's
net. The six-unit optimum of 19 has two agreeing geometric implementations
in a specified model; its novelty is unconfirmed.** The next mathematical
priority is resolving the four-unit comparison and obtaining an external
check, not announcing a new theorem on the basis of the search results.
