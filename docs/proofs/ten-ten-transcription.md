# Twenty-factor (10,10) transcription lab

Richard supplied twenty routes on October 17, 2026. They are entered in his
top-to-bottom order in [the lab](../../lab/ten-ten/index.html). This is separate
from the catalog's literature record for Nakamura's (10,10) example; no
identification with that example has been established.

## Conventions and one explicit assumption

The six marked points are numbered left to right. “Up through k” means cross
the open gap after point k from below to above; “down through k” crosses from
above to below. Thus the first closed itinerary `(2,4,5,6)` surrounds points
3, 4, 6. Factors and braid words are read from top to bottom using the lab's
existing positive generator convention, with A(uv) = A(u) composed with A(v).
The new lab displays above and below as dictated, without the older labs'
vertical display reflection.

F7 was dictated as “half twist squared; up through 3, down through 6, back to
start.” That closed route encloses three points (4,5,6), rather than being an
arc joining two points. Pending confirmation, it is provisionally encoded as
the squared Dehn twist around 4,5,6, exactly like F18. This gives ten half
twists and ten squared three-point Dehn twists, corresponding to the stated
(10,10) count under the genus-two branched-cover convention. This assumption
is visible in the lab and retained in exports. A literal squared half twist
would require a two-endpoint arc that the supplied route does not specify.

## What has been checked

All twenty routes pass the shared Arc/Loop routing checks. Each braid factor
has exactly the same unoriented free boundary class as its dictated closed
curve, or the boundary of a neighborhood of its dictated arc. Matching uses
the whole free-group word, including winding, rather than just a set of
enclosed labels. The braid encodings were recovered by shortening these
boundary words to standard supports; no search runs when the lab opens.

The product has 254 freely reduced factor-word letters in total and braid
exponent sum 130. Its exact six-strand disk action is nontrivial. Capping the
disk boundary also gives a **nontrivial sphere outer action** for this
transcription. Its genus-two homology action is

```
-14   19   19  -20
 12  -15  -16   16
 -9   12   13  -12
 15  -19  -19   21
```

This is not +I. Consequently this exact transcription is not yet a closed
genus-two identity. Counting factors does not establish closure. The lab
retains this failure instead of supplying a certificate for the intended
relation. F7's provisional three-point squared twist acts trivially on this
homology, so confirming its label alone will not resolve the discrepancy
among the currently transcribed half-twist factors.

## Working in the lab

The support inspector includes the original dictation. “Original dictation”
lists all twenty routes even after edits. Hurwitz moves, splitting powers,
PC lantern and half-lantern substitutions, combining, global conjugation,
undo, JSON import/export, SVG export, and cumulative disk/sphere cut
inspectors use the same engine as the other labs. Edits preserve this seed's
exact disk product (or its saved global conjugate); they cannot turn a
nonclosing product into an identity. Correcting a source transcription is a
separate seed revision, not a Hurwitz move.

Sphere cut rows compare a forward prefix with an inverse suffix based at
the standard final chart. They agree at the meeting point only when the
explicit check succeeds. The charts do not assume the sphere identity.

Browser storage is separate from the (6,7) and Xiao (4,3) workspaces, and
imports and persisted sessions are checked against this seed. To run locally:

```powershell
$env:PYTHONPATH='src'
python -m surface_diagrams.factorization_lab --seed 10-10 --no-browser
```

The executable source and original routes are in
`src/surface_diagrams/ten_ten.py`. Tests cover the route correspondences,
closure failure, exact preservation under editing, and session isolation.
