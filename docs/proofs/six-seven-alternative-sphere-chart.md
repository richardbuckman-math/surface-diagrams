# Optional point-four sphere-chart audit

This is a checked research calculation, **not applied to the published replay**.
The complete named proof remains106 steps and the existing-root branch39.
Neither PDF, diagram payload nor graphical proof changes. This audit does
not provide the missing shorter named closure.

Reproduce it with `python examples/analyze_alternative_sphere_chart.py`.
The [saved certificate](six-seven-alternative-sphere-chart.json) retains
all source factors, Schreier records, disk discrepancies, sphere actions,
chosen lift checks, explicit correction factors and local lantern matches.

## Choosing the exterior point

Let D denote the five-point disk exterior twist. The source is the reached
operation39 ordered factorization with independently checked D^4 action.
All factors are full twists, so they fix each sphere point.

For an internal point j, this chosen framed puncture chart sends the old
exterior to three new exteriors. A k-point twist containing j contributes
k-2 exteriors per positive unit. Thus the predicted normalized exponent is
12 minus the sum of those corrections. Keeping the original exterior point6
instead leaves D^4. Powers of repeated factors are counted.

| Exterior sphere point | Retained correction power | Normalized disk power | Total framed power |
| --- | ---: | ---: | ---: |
| 1 | 7 | 5 | 12 |
| 2 | 7 | 5 | 12 |
| 3 | 8 | 4 | 12 |
| **4** | **9** | **3** | **12** |
| 5 | 7 | 5 | 12 |
| 6 (unchanged) | 0 | 4 | 4 |

This incidence calculation selects point4 for an actual exact rechart. It
is not an equivalence test, a shortest-braid calculation, or a claim that the
full framed product has only three exterior twists.

## SPHERE MOVE: point4 becomes exterior; keep all nine corrections

The explicit common frame is sigma5 sigma4. Old points1,2,3 stay1,2,3;
old4 becomes exterior6, old5 becomes4, and old6 becomes5. Schreier rewriting
tracks the new exterior point; no strand is forgotten.

The normalized fourteen positive factors have exactly D^3 based disk action.
**Nine positive D corrections remain as a separate explicit factor D^9.**
The corrected product is therefore D^9 times the displayed normalized
product, with independently checked D^12 based disk action.

The old visible exterior has not been silently discarded. Its complementary
singleton contributes three of the nine retained boundary corrections;
every component correction is listed in the certificate.

This is a sphere rechart, not a disk braid equality. The complete coupled
disk discrepancy is retained and its writhe is -160. Its five-arc sphere
action is certified, and the chosen genus-two lift is separately +I.
The normalized D^3 part and correction D^9 part each have -I lift. Removing
either odd part would lose that lift check. **No boundary cap is performed.**

## An adjacent cabled PC lantern

In the new normalized chart, actual factors F12.1, F10.2, next.0 are adjacent.
Their supporting point sets are235,135,12, respectively. Point sets alone
were not used as the certificate.

They separately equal the following cyclic cabled PC lantern inputs in the
single common chart

`h = (-1,-1,2,1,1,2,3,3,4)`:

- R = round T234;
- S = sigma1 R sigma1 inverse;
- Q = round T12.

The exact canonical relation is R S Q = T1234 T34. The certificate retains
all three individual common-chart matches and both exact disk-presentation
checks for the replacement. The h-frame fixes the actual12 pair; it is not
a free change to any other part of the factorization.

Applying this one local disk relation leaves thirteen normalized positive
factors, **still preceded by the same D^9 correction factor**. The normalized
product has D^3 action and the corrected product D^12. The normalized
support maximum/total is18/107, with192 braid letters. This is not an overall
complexity improvement over the public operation39 endpoint12/90; the value
of the optional chart is the actual adjacent named configuration.

## Remaining gap

The two four-point curves now contain1235 and1345 and have minimal
intersection2. The current24 pair nevertheless fails the exterior-lantern
necessary commutation check in every one of the six orders. No compatible
triple or second exterior extraction is claimed.

Neither sign of a unit14 transport on that pair fixes this configuration;
a squared positive transport hits the exact-action bound and stays unknown.
The eight specific unit14/unit23 transports of either outer curve all raise
the outer intersection to6 or10. These are limited rejected routes, not an
orbit exclusion. A correct transported24 petal or a different named residual
closure remains to be found before this chart can shorten the full proof.
