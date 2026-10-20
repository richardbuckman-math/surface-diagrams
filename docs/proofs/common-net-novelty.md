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
nets for its three cluster types. Its picture shows a selected set of 16.
The complete linked catalog contains 37 outlines shared by all three types,
with 47 fixed-cut variants. The previously reported discrepancy is resolved:
the picture selects nets exclusive to those three types, with one variant
each, rather than all nets covering those three. See the breakdown below.

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

## Resolved four-unit comparison

The [complete per-pattern catalog](https://lsusmath.rickmabry.org/rmabry/dodec/delta/commonNets-fiveDeltahedra-catalog1.pdf)
has 448 outline records. Parsing its entries and every numbered net reproduces
the five inventory totals 452, 280, 203, 98, 242, with complete nonduplicated
net-ID ranges. The three tetrahedron-cluster types are numbered 1, 2, and 3.

| Catalog class, all covering types 1/2/3 | Outlines | Variants per outline |
|---|---:|---:|
| Only those three types, one variant per type | 16 | 1 |
| Also type 5 | 14 | 1 |
| Also types 4 and 5 | 4 | 1 |
| Also type 4 | 1 | 1 |
| Only the three cluster types, six cut variants per type | 2 | 6 |

Thus there are 37 shared outlines, and 35 + 2*6 = 47 fixed-cut variants.
These agree exactly with the two local geometric implementations. The two
six-variant outlines are catalog IDs 005 and 405. The 16 IDs in the published
picture are exactly the first row's filtered IDs:

`6,12,13,23,28,97,105,155,164,216,309,323,342,374,376,447`.

For example, outline 011 covers types 1,2,3 **and** 5, so it qualifies as a
common net for the three clusters but is excluded by that exclusive filter.
The four nets covering all five deltahedra (IDs 73,316,337,346) likewise
belong to the full common catalog but not to the pictured 16.

This explains the apparent discrepancy without attributing a calculation
error to either program. The wording around the picture is broader than
the actual selection. We do not claim this fuller four-unit count as new.
The match is a calibration result, not proof of novelty for six units.

`catalog_compare.py` checks membership, subtotal sums, every listed net,
unique outline IDs, and all numbered per-surface inventories. A summary with
source URL and SHA-256 is committed under `experiments/common_nets/reference/`.
The downloaded source PDF is not redistributed. No one has been contacted.

## Reproduction and claims

```text
python -m experiments.common_nets.audit
python -m unittest tests.test_common_nets -v
```

The default input is `.preview/common-nets/tetrahedra.json`, generated by the
earlier enumeration. The output is `independent-audit.json` in the same folder.
`--small-only` checks the four- and five-unit cases without the six-unit bound.
Positive drawings and the original atlas remain separate from this audit.
To reparse the published catalog, after obtaining its source PDF:

```text
python -m experiments.common_nets.catalog_compare --pdf catalog.pdf --destination comparison.json
```

Current wording: **The five-unit construction is a rediscovery of Mabry's
net. The six-unit optimum of 19 has two agreeing geometric implementations
in a specified model; its novelty is unconfirmed.** The next mathematical
priority is an external check of the six-unit certificate and a more complete
literature search, rather than announcing novelty from search-engine silence.
The four-unit catalog now supplies a successful calibration.
