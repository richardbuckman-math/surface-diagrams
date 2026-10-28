# Clarity-first graphical derivation of the working (6,7)

Richard's October 28 priority is clarity and simpler arcs/curves, even when this
needs more moves. Sphere changes now redraw one existing arc or closed curve;
they never include a lantern substitution or peripheral deletion.

The preferred [interactive derivation](six-seven-fifty-blocks/index.html?phase=clearfull&step=0)
and [PDF](six-seven-fifty-blocks/six-seven-named.pdf) contain **98 listed moves in
69 certified independent steps**. This organization is not a mathematical
shortening. The complete named derivation remains solved.

## A longer, clearer source

The view uses the retained 82-operation source rather than the shorter
79-operation source. At the corresponding early half-twist checkpoint, the F2
neighborhood word has length 4 rather than 12; the total for the six half-twist
neighborhoods is 72 rather than 80. The maximum stays 30. These are support word
lengths in this chart, not minimal geometric intersections or a claim that all
curves have become simpler. The original 79-operation source and every earlier
local witness remain unchanged.

## Distinct actions in the pictures

1. Step 010 is an exact **disk lantern substitution**. Its actual inputs are
   individually matched in a common chart. It retains the four-point outer.
2. Step 011 is **only a sphere redraw** of that same outer from the complementary
   side. Its factor identity, position and power are unchanged.
3. Step 013 contains fourteen independent individual chart redraws. Four are
   already disk-equal presentations; ten are genuine sphere changes. The main
   factor list and all powers stay fixed.
4. The SIX framing corrections accumulate in a **separate ledger**, multiplied
   to the left of the main factorization. The ledger is explicit in the
   diagrams and every complete disk discrepancy. Some uncorrected local redraws
   have lift -I; their corrected discrepancies have +I. No correction is dropped.
5. Step 014 redraws the six-powered ledger curve around the remaining point.
   Step 015 separately clears the already-peripheral curve. Steps 068 and 069
   similarly separate the terminal fourth-power redraw and its cleanup. A unit
   exterior has lift -I; only the checked even powers are cleared.

There are thirteen genuine sphere-redraw moves, each with its full disk
discrepancy, exact marked-sphere action and separately checked corrected lift.
The sphere action is in the marked-sphere mapping class quotient, not an
unqualified spherical braid identity. The signed PC framing balances and full
nonabelian point-pushing kernels, shadows and reconstructions remain retained.

## What “in parallel” means

Each numbered step contains independent edits of disjoint factor intervals.
Every printed card starts from the SAME step input; the letters a,b,... are not
a dependency order. Every pair has a literal two-order equality certificate,
and the complete group rejoins the retained sequential trace. Common frames,
cyclic starts and peripheral cleanup are barriers. Redraw steps are never
mixed with substitution steps. This certifies independent factor-diagram edits;
it does not assert a simultaneous ambient isotopy of an entire joint cut system.

## Files and rebuilding

- `clarity-certificate.json` retains the 98-move trace, parallel cards, complete
  redraw discrepancies, framing ledger and independence witnesses.
- `display-clear.json` is a separate on-demand payload. The old base, early and
  pure payloads are unchanged; the default view does not fetch them.
- `examples/build_six_seven_clarity.py` rebuilds only the clear view from the
  retained certificates. The ordinary full-page builder calls it afterward.
- `examples/build_six_seven_named_pdf.py` exports the preferred clarity PDF;
  its previous source exporter remains available as `build_legacy_source()`.

All factor diagrams keep Richard's unnumbered six-point grid: 18pt pitch,
1.26pt radius. Curves and points scale together, and the connected braid style
is unchanged. The independent six-point/five-arc comparison is retained;
individual support diagrams are not cumulative joint-cut certificates.

Future research should first improve actual arc/curve geometry and their
interactions. Fewer operations are useful only when they preserve that clarity.
The old count-only priorities below the current HANDOFF section are historical.
