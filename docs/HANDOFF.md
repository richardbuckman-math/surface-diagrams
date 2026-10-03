# Handoff: surface-diagrams

## October 3: individual exact F11/F12 arcs

The shared per-curve cut limit is now 2048. The original F11 and F12
meridian images recover individual exact arcs with 334–1502 cuts, although
their combined six-arc systems still exceed the 3072-node route limit. The
F11 x5 image, 3,763 letters and 1,502 cuts, routes individually in about
13 seconds; a regression checks its complete based meridian and SVG. The
inspector continues to label these as *individual* paths, never a jointly
verified six-arc diagram. All 294 tests pass; local and portable browser
screenshots confirmed the F11 x5 drawing and its explicit joint-view warning.
The portable site builds with local links checked. Next: publish and verify
remote checks and Pages, then seek a compact exact six-arc representation.

## October 3: exact joint cut system through F10

Raised the shared route budget to 3072 nodes and gave dense route comparisons
a node-scaled ceiling of at most eight million. The original (6,7) F10
prefix has 2,627 route nodes; its complete six-arc system now renders in about
one minute locally, with all six meridian words checked and all arcs routed
together. Local and portable browser screenshots confirmed the fitted
F9-before/F10-after pair and x6 trace. The new F10 regression and all 293
tests pass; the portable site builds with local links checked. Commit fbf49c8
was pushed, and remote Tests and Documentation passed. A compact exact
*joint* representation for F11 onward remains the next display problem.

## October 3: trace one arc in a later exact cut system

The prefix inspector's x1–x6 labels now toggle a single arc in both the
before and after six-arc diagrams. This makes the exact path change readable
inside the dense F8 drawing without losing the joint routing check. The
toggle restores all six colors and resets when moving to another factor.
Local and portable browser checks confirmed the selected x2 path and toggle;
the 28 factorization tests, JavaScript syntax, and portable site link check
pass. Commit b056204 is pushed, and remote Tests and Documentation passed;
the public lab exposed and responded to the new controls. F10 rendering is
now addressed in the section above.

## October 3: later exact six-arc cut systems

The shared noncrossing route solver now checks only edges completed by the
newly assigned cut interval, while preserving its full analytic intersection
and point-clearance checks. Its order propagation avoids copying every node
position for each pair comparison. The joint limit is 2048 route nodes; the
original factorization's F8 after-system (1,225 nodes) and F9 after-system
(1,675 nodes) both render with the exact shared Arc renderer. The F8 before
and after drawings were inspected in the local server and portable
browser-worker build. At this size the raw SVG
starts as a blank-looking viewport, so the prefix inspector now fits both
whole diagrams by default, keeps colored strokes visible at overview scale,
and offers original-size Start/Middle/End navigation. The individual arc and
full-word views remain available. Browser screenshots confirmed the fitted
pair and original-size detail; the portable site reproduced the fitted pair.
The full 292-test suite, JS syntax, site build
with local-link checks, and git diff check pass. Commit 89403a1 was pushed;
remote Tests and Documentation both passed, and the public lab showed the
fitted prefix controls. The joint node limit is still reached for F10 onward.

## October 2: compare individual prefix arcs

The individual-arc inspector now steps between x1–x6 and switches the selected
arc between its before and after image without closing. Request revisions and
stale-response guards still apply. A local static-browser check switched F8 x2
from its 1,039-letter after image to its 431-letter before image, then advanced
to x3 (287 letters); the SVG and label updated in place. JS syntax and site
local links passed. Next: push, verify remote CI and Pages, then return to a
joint late-prefix representation and robust support geometry.

## October 2: individual exact arcs beyond the joint route limit

The prefix inspector now offers View arc for each before/after meridian. A
separate endpoint draws that one based arc with the shared surface renderer
and checks its ray word against the complete exact meridian image; the modal
explicitly says this is not a jointly verified cut system. F8's after x2,
whose joint six-arc drawing exceeds the 1024-node limit, routes individually
in a scratch calculation (1,039 image letters, 23,953 SVG bytes, 2.65 s).
The public browser adapter exposes the same endpoint. The focused six-test set
and JS syntax passed. Local static-browser inspection
showed F8's after six-arc drawing still unavailable, while its 1,039-letter x2
image drew alone with the explicit joint-system caveat. The initial long-arc
viewport was blank above its centerline; it now centers vertically, offers
Start/Middle/End navigation, and collapses the full word. Browser screenshots
confirmed the start and middle views are readable. Next: push and verify the
live page and remote checks. Longer-term work: a mathematically checked joint
late-prefix representation.

## October 2: browser workspace persistence

The public (6,7) lab now saves its complete 60-step undo/redo history and
global frames in browser local storage after every accepted action. On reload,
the browser adapter uses the same session validator as the local Python server;
invalid saved data leaves the original factorization available with a warning.
The UI distinguishes browser storage from a server session file and explicitly
warns when storage is unavailable or full. A browser test on the local static
build moved F1 past F2, refreshed the page, and reopened the checked two-step
history with F2 first and Undo available; the restored page was visually
inspected. The adapter test also reopened the saved session and checked
invalid-data fallback; the local-link build and JS syntax checks passed. The
290-test run had two generated-script failures because its relative PYTHONPATH
did not survive a subprocess changing to a temporary directory; both passed
when rerun with an absolute PYTHONPATH, and all 28 factorization tests passed.
Next: deploy, verify remote CI and the public Pages URL. Longer-term work
remains exact late cut-system geometry and verified substitutions.

## October 2: public (6,7) lab on GitHub Pages

The interactive lab now has a static Pages build at `lab/index.html`. It runs
the same Python LabServer state, Hurwitz and substitution checks in a browser
worker using pinned Pyodide v314.0.7; no shared backend or user session file is
exposed. The site builder packages the source modules, copies the lab assets,
and links the lab from home and the (6,7) catalog page. Browser test on a local
static server loaded all 13 factors/178 letters, performed a checked Hurwitz
move and square-twist split, showed the changed continuous braid, and obtained
the sphere-action certificate. The public page explicitly tells visitors to
Export JSON before refreshing; local session persistence remains available in
the Python server. The browser-adapter unit test and local-link build passed.
Next: push, verify Pages deployment and the exact public URL in a clean browser,
then share it. Keep the two modes' persistence distinction clear.

## October 2: alpha release 0.1.0a6

Bumped package and site version to 0.1.0a6, with the completed lab, published
(6,7) proof, and catalog work grouped under that changelog heading. All 25
tutorial figures and TikZ counterparts regenerated without tracked changes;
the full 289-test suite passed and the portable site built with every local
link valid. Commit 639370f and annotated tag `v0.1.0a6` are pushed. Tests
and Documentation passed on main, the tag-triggered Tests passed, and the
Release workflow published the prerelease with both the universal wheel and
source archive. Next: return to the interactive lab's late exact cut-system
representation; retain full words and an explicit route-limit message until
a joint drawing can be verified.

## October 2: proof navigation

The published proof now has a 19-entry jump index with move numbers, word
lengths and return links. The verifier regenerated the page and again checked
all 2,486 moves, the original SVG transcription, and SHA-256. Browser test
clicked substitution 10 and reached its highlighted relator replacement.
The previous proof-publishing commit ba1aab1 deployed successfully on Pages;
Tests and Documentation CI passed. Next: publish this navigation increment,
verify CI, then return to the interactive lab's late cut-system representation.

## October 2: published (6,7) sphere-braid proof

Moved the completed 2,486-step proof from ignored previews into
docs/proofs/braid-six-seven. The portable verifier checks every cancellation,
commutation, braid move and all 19 sphere substitutions. With `--source-svg`,
it additionally checked the original Downloads/BraidSixSeven.svg transcription
and its SHA-256; both modes passed. The HTML walkthrough, certificate, move
table, endpoint SVG/TikZ, and README are now versioned. The (6,7) catalog
distinguishes the verified six-punctured-sphere mapping-class identity from
the still provisional full Lefschetz-fibration interpretation; the lab's
sphere certificate and site home link to the proof. Portable site build and
local-link check passed; browser inspection confirmed the proof introduction,
endpoint drawing, and updated catalog link. Remote checks pending. Next:
verify deployed Pages, then continue the interactive lab's exact geometry or
develop more concise proof navigation. Do not claim the late disk cut system
is drawn or that the spherical braid itself is trivial.

## October 2: revisitable exploration history

Added labeled history steps for checked Hurwitz moves, splits, combining,
global conjugation, simplification, import, and reset. The lab can revisit a
saved state and branch from it; history, frames, and labels truncate together.
The visible panel states clearly that Export JSON saves only the current
factorization. Old session files reopen with neutral labels rather than
invented operation names; a copied 48-state user workspace reopened at
position 47 with all 48 labels. Isolated browser test on 8025 split F1,
showed the new labeled step, and navigated back to the original 13-factor
state. Visual layout and JS syntax passed; full test suite in progress.
Next: restart main from its unchanged saved workspace, verify remote checks,
then continue exact late-cut-system representation or a readable proof view.

## October 2: selected braid interval

The selected mapping-class card now shades the corresponding vertical braid
interval. Browser inspection showed the highlight move from F1 to F2 while
the continuous strands and blue separators stayed legible. Standalone paired
SVG exports retain an unshaded braid (`fill="none"`), covered by the updated
factorization geometry test. Focused 26 tests and JS syntax passed. Next:
keep improving the route representation for late exact cut systems; the
simple common-whisker strategy was insufficient at F8.

## October 2: step through exact cut-system actions

Added Previous/Next controls in the exact prefix-action inspector. Browser
inspection on the saved main lab showed F1 before/after, advanced to F2 with
both six-arc diagrams and complete words, then advanced to F8: its before
drawing is available, while its after drawing correctly reports the 1024-node
limit and leaves the full exact words export enabled. The modal layout was
visually inspected; no saved exploration state changed. JS syntax passed.
A scratch probe found that stripping the common basepoint prefix leaves 1079
cuts after F8. Raising only the node cap led to a route-ordering search limit,
so a larger cap alone is not a verified improvement. Next: explore a compact,
mathematically checked multi-panel representation for these long cut systems,
retaining shared basepoint and disjointness evidence. Do not silently drop
arcs or label a numerical layout exact.

## October 2: checked global conjugation

Added a Global conjugation input to the (6,7) lab. A signed braid word acts
on every factor, and the server verifies the complete conjugated disk action.
The accumulated frame is stored with each undo/redo state, in exported JSON,
and in persistent sessions; import and reopen verify it against the original
product. The old 48-state saved workspace was copied to a temporary file and
reopened successfully with its position and history intact. Browser test on
8025 applied `1 -2` (178 to 218 displayed letters), undid and redid it, and
confirmed the exact sphere outer-action certificate still passes with an
86-letter common whisker. The main user workspace remained untouched during
the test. Full 288-test suite, JS syntax, and diff checks passed. Commit
f336971 was pushed; Tests and Documentation CI passed. The saved main lab
reopened on 8017 at its original 13 factors / 178 letters, with the new
control available. Next: improve compressed late-prefix cut-system routing
without drawing unverified arcs.

## October 2: export checked cut-system SVGs

Commit 029aabe was pushed; Tests and Documentation CI passed. The unchanged
saved main workspace was reopened on 8017. Save SVG buttons in the two exact
prefix cut-system panels and normalized sphere chart enable only when a
verified drawing is available. Browser test server8025/tab17 confirmed all
three controls enable with verified SVGs; JS syntax and diff checks passed.
Next: a useful intermediate-prefix sphere chart needs a rigorous jointly
noninterleaving route; the naive common-prefix normalization hit the route
ordering search bound, so do not show it as verified yet.

## October 2: normalized sphere identity chart

Commit 94575d0 (sphere outer-action certificate) was pushed; Tests and
Documentation CI passed. Main8017 reopened the unchanged persistent workspace
with the new Check sphere action button. The next batch adds
sphere_cut_system.py: after a successful inner-action certificate it removes
the common 58-letter basepoint whisker in F5, verifies the five resulting
images are exactly x1...x5, then routes their five Arc(0,j) representatives
together with the shared surface renderer. Puncture6 is at infinity. The
sphere modal now shows this normalized standard fan, visually inspected in
test browser port8025. It explicitly does not claim the disk arcs return or
settle the central order-two spherical braid. Full286 tests, JS syntax and
diff checks passed; commit 7eb52b9 was pushed and both CI checks passed.
Main8017 reopened. Next: try a
bounded sphere-chart normalization for intermediate prefixes while preserving
the exact basepoint word and honest chart failures.

## October 2: exact sphere outer-action certificate

The prior based-cut-system batch 8c580ce was pushed; Tests and Documentation
checks passed. Main8017 was restarted from the untouched saved workspace. New sphere_actions.py substitutes
x6=(x1...x5)^-1 into each exact meridian image of the full braid product.
The supplied (6,7) product's six images are all exactly one common inner
conjugation by a 58-letter word w in F5; its disk action is nontrivial. The
browser's Check sphere action modal displays the certificate, six checked
equations, and full JSON export. It explicitly separates this from the
previous 19-substitution sphere-braid derivation and from incomplete late
cut-system drawings. The UI now explicitly notes that outer action cannot
distinguish the central order-two spherical braid from identity. Non-inner results are labelled uncertified. Tests cover
the boundary relation, supplied product, Hurwitz invariance, central twist,
and nonidentity examples; browser test at port8025 visually confirmed the
certificate. Full284 tests, JS syntax and diff checks passed. Commit 94575d0
was pushed and both CI checks passed; main8017 restarted. Next: find a
compact geometric model for the common basepoint whisker and late cut-system
images, without weakening existing exactness and route guards.

## October 2: based cut-system images in the prefix inspector

The exact prefix-action inspector from dc605b1 is now live on the saved main
workspace and both GitHub checks passed. This next batch recovers a based
Arc(0,j) for each exact meridian image p x_j p^-1. The recovered ray word is
checked against the full based image, then all six arcs are drawn together by
the shared noninterleaving surface router with stable colors. The existing
cut_systems.py cellulation module was preserved; this lives in the separate
based_cut_system.py module. Browser test port8025 shows before/after F2 cut
systems and exact colored meridian words. For F13, the browser shows honest
768-cut warnings while preserving all exact words and their JSON export. The
source factorization can route the complete family through prefix7; later
prefixes exceed combined or per-arc limits. White-background raster previews
of prefixes2 and5 were visually inspected. Full281 tests, JS syntax and diff
check passed; 8c580ce was pushed and both CI checks passed. Next: improve
representation/compression of late based arcs without blindly raising route
limits; separately study the sphere quotient needed for visual identity.

## October 2: exact prefix-action inspector

Commit 45e0803 rendered the historical 578-cut F7 support and shortened
conjugated twists. It was pushed; Tests and Documentation GitHub checks passed.
Main port 8017 reopened the untouched persistent 48-state workspace and
visually displayed the original 13-factor, 178-letter state. The user-facing
tab is marked as a deliverable.

New in the next batch: a selected factor can show exact based images of all six
meridians immediately before and after it, plus color-coded puncture
permutations. The on-screen words abbreviate after64 letters; Save full exact
words as JSON exports the complete computation. This is exact disk action,
explicitly not a sphere quotient or yet a drawing of cut-system images. A
revision check rejects stale reads. Full278 tests, JS syntax check and diff
check passed. The test browser at port8025 showed F2's before/after images,
permutation change, and enabled full-word JSON export. Commit dc605b1 was pushed,
both GitHub checks passed, and main8017 reopened with the UI. The next
substantive step is the based cut-system rendering described above.

## October 2: render the saved 578-cut F7 support

Shared curves now allow768 cut visits and diagrams1024 route nodes. Lab spacing,
height and margin scale with the busiest cut; stroke1.5 and dot radius3.5 stay
fixed. Exact class, noninterleaving and analytic dot-clearance checks remain.
Dense routes (>128nodes) cap complete ordering attempts at200 and pairwise
comparison work at2million. A limit reports inconclusive search, not impossibility.
Dense cards show cut count and recommend inspector zoom. Recipe editor retains
its separate64-cut input cap.
Read-only audit:48 saved states,44 distinct supports; one F7 has578cuts. It now
renders in7-12seconds under production guards. Browser verified its lab badge,
inspector and readable separated strands at8x in test server8024 (exec42428/tab12; stale tab11 may remain),
using .preview/dense-lab-session.json, a copy of a historical state. Original
workspace never mutated. Earlier87-cut preview also visually checked.
Regression uses375-cut synthetic arc with376segments; checks expanded width,
fixed stroke/dots, containment samples, noninterleaving, and rejection beyond768.
Full277 tests passed after making header-only HTTP rejection tests send empty
bodies (unchanged status assertions; eliminates Windows early-close/body race).
No production HTTP behavior changed. Next bounded support-class search follows
local braid rewrites: max4096 initial letters,2million admitted letters, same
max_states count as local search, no excursion above initial boundary length.
Final support equality is checked; lab braid-action checks remain mandatory.
Saved raw F7 g53 -> g31; read-only whole product check362 ->290 passed using
the support-search proposal alone. Integrated browser simplification362 ->274 passed exact product checks; all13
support audits agree, F7 remains578cuts. Undo restored362; redo restored274.
Only copied test workspace was changed. Browser initially hung on reload; a
fresh test tab12 recovered, and API remained healthy throughout.
All24 focused lab tests pass after integration, including exact braid actions
for nonstandard half/Dehn/squared twists with a removable central prefix.
Require remote CI before declaring final batch done.
Preview HTTP8023 exec99055/tab10 and test8024 need cleanup after main deployment.
Main8017 last exec82024 runs previous batch. Restart from persistent workspace
only after validation. Next: verify CI and main UI; consider measured route
caching/performance, not another blind increase in capacity.

## September 30 morning: preserve history on unchanged simplification

Prior ccfc7c3 was pushed; Tests and Documentation passed. Live main tab9 was
verified with all48 saved history states reopening exactly, and core inspector
verified. Test tab8/server8021 were cleaned up. Those earlier pending items below
are completed.
New small interaction fix: Simplify factors does not append a duplicate state or
truncate redo when no representative changes. It reports that no shorter form
was found within the search bounds, preserving history. Regression exercises
simplify at an earlier history position followed by redo. No layout change.
At start weekly allowance98% used. Do not begin a large routing rewrite within
this remainder. Next substantial increment: a deliberate layout policy beyond
64 cut visits, retaining exact class and noninterleaving/clearance checks.


## Final September 30 checkpoint

Full suite275 passed after the based-meridian fallback; JS syntax check passed
for the added inspector core word. Inspector now spells out g · core · g^-1 and
shows the standard core including its power. All48 saved states can verify,
including35 (2.19s standalone). Main server70007 port8017 is starting with the
unchanged persistent workspace. Test server8021 has been stopped; tab8 needs
closure. Live tab9 should remain open after final reload/inspection. Final batch
commit/push and remote checks pending. Weekly allowance last read96% used; finish
verification before starting another substantial increment.


## September 30: exact action fallback verifies history state35

c7f8bfb Tests and Documentation passed remotely. Added an alternate exact Artin
calculation when prefix images exceed400000 letters: transport each based
meridian separately, applying generator substitutions in reverse order. This
uses free reduction only, NEVER cyclic/free-homotopy reduction. Each intermediate
meridian and the final image total retain the400000 bound. Differential tests
compare216 words and a central full braid (explicitly nonidentity as a based
action). All21 focused lab tests pass. Real saved history state35 now imports
strictly and verifies in2.19seconds; no limited-session exception is needed for it.
Main port8017 needs one final restart to remove the obsolete re-verification
notice. Preserve all48 history entries and current position47. Next: confirm main
UI says exact products verified, clean up8021/tab8, and check final remote CI.


## September 30: standard-support simplification and deployment

8b17074 remote Tests and Documentation both passed; the previous GitHub500
Pages failure was transient. Added exact standard-support recognition before
bounded simplification: matching the supporting class of a positive twist (or
two-point half-twist neighborhood) removes the full conjugator while preserving
type and power. This is an exact mapping-class support argument, not a claim of
global minimization. Regression checks central full braid conjugation for half,
Dehn, and squared Dehn twists against full Artin actions with max_states=1.
All20 lab tests pass. supported_class now caches128 results and uses the specific
VerificationLimitError for its computational bound.
Main server restarting under exec74000 from the unchanged48-state session,
port8017, live tab9; it now includes exact arcs and this simplification. Startup
rechecks all historical products and reports state35 as not reverified because
of its bound. Test server8021 exec28676/tab8 needs cleanup after main inspection.
Next substantive work: improve rendering beyond64 cut visits using a deliberate
layout policy, or add a user-visible move/proof log; do not drop geometry checks.


## September 30: exact half-twist arc recovery

Both support types now recover itineraries from exact supported boundary words.
For half twists, compute transported endpoint labels and find x_a t x_b t^-1
in a cyclic orientation of the neighborhood boundary. Convert t into ray runs,
trim endpoint turns, and verify the resulting Arc boundary exactly. The shared
route solver still checks rendering; no numerical sampling is used by lab
supports. F9 exactly matches the user's confirmed itinerary. 864 small conjugated
arcs were checked and rendered with sampling disabled. Browser inspected the
complex F7 after F9 crosses F8 and F7: all 13 supports agree, total206 letters.
Full suite274 passed. Large classes that provably cannot fit64 cut visits return
an explicit drawing-limit message while retaining their exact class in inspector.
Main server96870 currently runs the previous closed-loop-only batch and needs a
restart after this commit, using the unchanged48-state workspace file. The live
tab9 displays the persistent notice for history state35; no user states changed.
Test server8021 exec28676/tab8 remains for validation. Previous c35232b remote
Tests passed; Documentation build passed but deployment failed with GitHub500.
Next push will retry Pages naturally. Next useful simplification: recognize an
entire conjugator stabilizing a standard support, including central braid twists.


## September 30: exact boundary transport and closed support recovery

Previous afdd0db push confirmed; remote Tests and Documentation passed.
New supported_class transports only the closed support word, canonicalizing its
free homotopy class between reversed Artin substitutions. This is NOT a braid
equality test. Saved complex F7 yields its 1304-letter boundary class in 0.03s,
without expanding unrelated meridians. Inspector retains the exact expected class
even when geometry recovery fails. Closed twists now derive Loop cut itineraries
directly from exact boundary words; arcs still use checked numerical proposals.
Shared route solver remains mandatory for drawing. Browser checked initial
supports and F1-over-F2, with separated diagrams and continuous braid.
272 full tests passed before session recovery fix; 19 focused lab tests passed
after it. Differential test compares 432 cases against full Artin images;
36 transported loops render with numerical sampling disabled.
Main saved session has 48 history states, position 47 (current original factors).
Do not overwrite it using the older 15-state backup. Reopening exposed an older
history state exceeding exact verification limits. Added a specific limit error:
session reopening preserves such states with an explicit persistent notice;
malformed data and proven product mismatch still reject. JSON import remains
strict. Main startup under exec 96870 is rechecking the saved history.
Next: verify reopened main UI and remote checks; then investigate exact recovery
of half-twist arcs to reduce numerical recovery failures. Keep global shortest
conjugator and general daisy claims out of the UI.


## Final shared-renderer checkpoint, September 29

All 270 tests pass (168s); after switching simplification's final proof to a
locally verified rewrite chain, all 16 focused lab tests also pass. Full global
factor expansion can exceed the limit for the user's current F7 even when a
rewrite is small; the chain verifies each local braid rewrite/core transport
instead. Complete factorization replacement remains checked by exact action.
Read-only validation of the user's saved exploration: 398 -> 296 letters, same
exact product. This has NOT yet been applied to the main session; Simplify factors
is available. Saved main workspace has 15 history states (14 factors currently).
Main server was restarted from that file, exec 82721, port 8017, preserving history.
Numerical recovery now internally simplifies its proposal even for old records.
Browser verified F1/F2 shortening and the difficult F9/F7 shared renderer with
separated elliptic arcs. One Export JSON and one Load JSON button are present.
The standalone test server 8020 (exec 9863/tab 7) still needs cleanup. Main tab 4
needs reload to receive new UI; refresh only reads persisted server history.
Next: verify remote CI and live main UI, then improve bounded simplification or
reduce expensive itinerary recovery for the user's most complicated saved F7.
No global shortest-conjugator claim. Five-hour allowance nearly exhausted.

## September 29: shared Arc/Loop rendering and conjugated-twist simplification

Implemented the user's new priority. Factor.mapping_class delegates to reusable
ConjugatedTwist in mapping_classes.py; support_curve/support_drawing in
 twist_supports.py recover verified Arc/Loop itineraries and call the existing
PlanarSurface/render_svg pipeline. No handwritten support SVG fallback remains.
Numerical deformation proposes topology only. Initial F9 recovers exactly the
confirmed Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down').
The shared router now propagates forced endpoint orders between same-side edges;
all original noninterleaving/clearance checks remain. This makes the difficult
F9-over-F7 support render too. A finite small-loop regression compares the
optimized route search against the unpruned search. Public exports include
ConjugatedTwist, simplify_twist, support_curve, support_drawing.
Hurwitz moves simplify each crossed factor automatically while keeping the
dragged factor unchanged. Simplify factors handles already-saved explorations.
Bounded braid-relation/commutation/suffix-core transport search preserves type,
support size and power, can change the standard core, and exactly verifies its
result. No globally shortest claim. F1 crossing F2 reduces its new factor from
33 letters to 11 (core 3 becomes core 5); total becomes 180 rather than 202.
The source/UI have one export and one import action; relabeled Export JSON and
Load JSON to make the distinction explicit. Browser checked the shortened move.
Full suite 269 passed before one additional route regression; focused 16 tests
then passed. Final full suite and difficult-move browser checks in progress.
Main user server 8017 still runs the prior committed backend until deployment;
its session file must be preserved. Test server 8020, exec 9863, tab 7 uses its
own .preview/shared-support-session.json. Next: finish validation, push, then
restart main with .preview/factorization-workspace.json and leave it open.

## NEW USER PRIORITIES: shared support model and shorter conjugated factors

User reports two Save JSON buttons. Current lab HTML has exactly one; inspect
live UI before claiming a fix or deleting a different control.
User requires left-hand support diagrams to use the established library arc and
closed-curve rendering code. Current factorization_geometry.py is a bespoke
sampled-path SVG renderer within the package, not the existing Arc/Loop rendering
API. Build shared arc/closed-curve and mapping-class representations as needed;
connect the prototype to those rather than maintaining parallel drawing logic.
After Hurwitz moves, shorten the conjugated representation g T^k g^-1, preserving
half twist / Dehn twist / squared Dehn twist type. The standard core T may change.
Seek braid-relation cancellations within g and across core/inverse boundaries,
not only adjacent inverse cancellation. Verify every accepted representative by
exact Artin action; update both support and braid. Do not promise a globally
shortest conjugator unless established; bounded verified simplification is a
useful first increment. Preserve saved user workspace and migration compatibility.
This takes priority over alpha6 release or unrelated display work. At this user
turn five-hour usage is 99%; defer substantive implementation until reset rather
than consuming reset credits. No implementation of these new requests yet.

## Active morning checkpoint (September 29)

Main prototype: http://127.0.0.1:8017, browser tab 4 retained, exec session 43130.
It now runs ALL morning changes with --session .preview/factorization-workspace.json.
Use that file on restart: it preserves user work and undo history. Test-only
servers 8018/8019 were stopped and their tabs closed. The final main browser
screenshot confirms 13 original factors, boundary-word checks, Inspect support,
Combine neighbors, and automatic saving. All four implementation batches are
pushed; latest ee0d5f7 passed remote Tests and Documentation. Full suite 267 passed
before inverse-combine; all 13 lab tests including its new round-trip/rejection
assertions passed afterward, and final remote Tests passed. Remaining weekly
allowance is about 32%, but this five-hour window is nearly exhausted. Keep
working after reset under the user's all-quota-today instruction. Do not consume
reset credits. Local wheel smoke attempt used Anaconda setuptools 58.0.4, below the declared
>=61 build requirement; its UNKNOWN wheel is invalid and was NOT published.
For alpha6 use an isolated PEP 517 build with supported setuptools, not direct
build_meta under this older environment. Next: embedded support cleanup and/or an alpha6
release of the now-usable prototype. No general daisy/boundary-framed substitution.

## September 29 morning: inverse lantern combine

Combine neighbors now recognizes three adjacent unit pairwise twists whose
exact product equals the marked-point lantern candidate, in addition to equal
neighboring powers. A conjugated lantern split can therefore be reversed.
Every accepted replacement is checked by exact Artin action; wrong ordering is
covered by rejection tests. Browser round trip: 14 factors -> lantern split 16
-> combine 14, returning to 178 letters and matching support boundary checks.
All 13 focused lab tests pass; the previous full suite had 267 passing tests.
Support-audit commit 0f17741 passed both remote workflows. No general daisy or
framed-boundary substitution was added. Next: keep improving embedded support
geometry (boundary-word agreement alone does not rule out sampling crossings).

## September 29 morning: compare drawn support classes against exact action

Added factorization_audit.py: read upward puncture-ray crossings from coordinates
rounded exactly as the SVG, normalize the closed-support class (or arc neighborhood
boundary), and compare to the exact Artin image of the core enclosing loop.
All 13 initial factors plus both supports in F9-over-F7 agree, including rounded
coordinates. Each row now reports agreement/mismatch/unavailable; inspector shows
both normalized words and the limitation: agreement does NOT certify embeddedness
or resolve PDF correspondence. SVG exports retain the check. A wrong-side arc
regression fails the comparison; a puncture collision is flagged unavailable.
All 267 tests pass (117 seconds). Browser inspected F9 and both matching words.
6759742 durable-session commit passed both remote CI workflows. Main 8017 still
needs restart with its session file to receive this backend audit implementation;
all main workspace edits are now durably saved. Next: inverse lantern combining,
then improve embedded representatives without conflating homotopy with embedding.

## September 29 morning: durable sessions and complete SVG exports

Added --session FILE to the lab. It saves every accepted edit and undo/redo
position by atomic replacement, reopens and exactly verifies all history states,
and rolls back an edit if saving fails. Existing invalid files are not overwritten.
State limits now also protect reopening (powers, IDs, conjugator size, whole-state
letter counts after splits). SVG exports retain numerical-preview labels and
explicit missing-support warnings; a stale revision cannot export the wrong state.
All 266 tests pass (117 seconds); browser smoke test split F1, restarted the test
server, reopened 14 factors, and successfully undid back to 13 with redo available.
Main user server 8017 was confirmed untouched (revision 0, no undo) before upgrade.
It now runs with --session .preview/factorization-workspace.json, exec session
21178, and tab 4 is retained. Restart with that same session argument to preserve
work. Temporary test servers 8018/8019 and tabs 5/6 are agent-only checks.
Geometry/inspector commit 7fd221a passed both remote CI workflows.
Next: compare numerical support ray words to exact transported curve classes;
rendering successfully is not by itself a guarantee that sampled geometry is right.

## September 29 morning: complicated support rendering and inspector

The previous prototype commit 18ddbd6 passed both remote Tests and Documentation.
Support deformation now clips sampling to each moving disk and simplifies dense
sections in bounded chunks. F9 moved from position 9 to 7 now renders both crossed
supports instead of failing for F7 (about 19 seconds for F7, 5 for F8 locally).
This is still a sampled representative: crowded paths are not certified isotopy
normal forms. No claim of general reliable itinerary reconstruction is made.
Added Inspect support: a modal with 1x-8x zoom, scrollable thin-stroke drawing, and
full exact word/conjugator. Browser inspection exercised F9 up twice, both new
previews, inspector zoom and word disclosure. Test exploration is saved in
.preview/lab-inspector-checkpoint.json; test server 8018 holds revision 2. Main
8017 server has not been restarted or its user state modified in this increment.
All 263 tests pass (122 seconds) with absolute PYTHONPATH; two earlier subprocess
failures were solely caused by a relative PYTHONPATH in the test invocation.
Next: persist/recover work robustly, make exports retain preview warnings, and
improve support readability/topological validation beyond numerical sampling.
## TOP PRIORITY: interactive factorization lab, September 29 overnight

User superseded weekly pacing: work productively through remaining weekly quota
today, prioritizing a working drag/drop (6,7) factorization prototype by morning.
Updated recurring automation prompt to this priority; still six-hour ACTIVE.

New runnable app: python -m surface_diagrams.factorization_lab --port 8017.
Local browser UI stacks 13 planar supports beside a single continuous colored
braid, with blue dotted separators. Actual native browser drag F1 over F2 worked;
arrow moves use the same path. Dragged factor stays unchanged while crossed
factors are conjugated (down inverse Hurwitz, up forward). Every local algebraic
rewrite is checked via bounded exact Artin actions. Initial 13 words match the
earlier SVG factor-by-factor (178 letters). Square split/combine and marked-point
lantern split were exercised in browser. Half-twist splits, undo/redo, reset,
JSON save/reopen with exact product verification, and SVG export are implemented.
All 261 tests pass (89 seconds), including seven new lab tests. JS syntax checked.

Files: factorization_explorer.py (records/operations), factorization_geometry.py
(sampled support deformations and continuous braid), factorization_lab.py (local
server), lab_assets/ (UI). Docs: FACTORIZATION_LAB.md. Package assets and command
entry point added. Default prototype remains alpha5/unreleased code.

IMPORTANT LIMITATION / NEXT WORK: supports are numerical homeomorphism previews,
not certified itinerary reconstruction or PDF verification. Direct triple-twist
blocks fixed the first F1-over-F2 sampling failure; F1 moved over three factors
also renders. More complex F9 crossing F7 can still exceed the 200k sample cap
and show an explicit unavailable-preview message; exact braid remains usable.
Improve this robustness before adding peripheral examples. No general daisy or
framed-boundary lantern implementation. Combine currently equal adjacent powers.
The original PDF correspondence beyond confirmed items stays provisional.
The five-hour allowance approached exhaustion during this run; weekly allowance
still had about 48% left. Resume productively after reset, not old reserve pacing.

## Selectable factor-9 segments, September 29

The HTML audit now has a labeled segment selector. It highlights the chosen
rendered arc piece and matching table row, with a live textual description.
Overlays reuse the exported SVG arc commands instead of approximating geometry.
Browser checks covered segment 6 visually, segment 10, and clearing selection.
The new report regression verifies exact command reconstruction and segment
continuity; it and all 21 braid-action tests pass. Reproduce with
python examples/audit_factor_nine.py. Temporary inspection server stopped.
Next: expose the same segment-selection affordance for user-supplied itineraries
rather than keeping it specific to factor 9. General action replay remains pending.

## Segment-by-segment factor-9 report, September 28 evening

Added arc_ray_segments, retaining every segment's unreduced ray contribution,
including empty steps. arc_ray_word now flattens and reduces these contributions.
The factor-9 example writes an HTML report beside SVG/TikZ/JSON with ten segment
rows, side-of-row and gap/point endpoints, plus expandable actual/expected words.
Browser visual inspection confirmed the table and evidence expansion; temporary
server stopped. All 253 tests pass (153 seconds), including reversal/order and
empty-segment regression coverage. Run python examples/audit_factor_nine.py and
open .preview/factor-nine-transport-audit.html to reproduce it.
Next: add selected-segment highlighting to correlate this table with the drawing;
the report still checks supplied support data, not automatic geometric replay.

## Explicit starting base paths, September 28 afternoon

Extended audit_arc_transport with keyword start_path (a free-group word, not
a braid). Both expected endpoint meridians are conjugated by this supplied path;
the frozen evidence retains its reduced value. Validation rejects out-of-rank
letters before cancellation. Regression cases cover a boundary full twist,
incorrect/default paths, and nonempty start and arc transport together. All 20
focused tests and all 252 Python tests pass (210 seconds). Factor 9 still matches with the default empty path; regenerated
its SVG/TikZ/JSON and visually inspected the unchanged arc/braid comparison.
Next: compare additional supplied supports using explicit base paths; do not
infer a general geometric reconstruction or complete PDF verification from this API.

## Reusable anchored transport audit, September 28 morning

Added audit_arc_transport and frozen ArcTransportAudit evidence: transport,
actual/expected endpoint meridian pairs and matches. The scope is deliberately
anchored; mismatches can reflect base-path assumptions, not general inequivalence.
Tutorial examples 24/25 now use it. examples/audit_factor_nine.py applies it to
the confirmed itinerary and writes SVG/TikZ plus exact JSON evidence under
.preview/factor-nine-transport-audit.*. Visually inspected the supplied arc and
braid comparison. All 251 Python tests pass (93 seconds), including 19 focused
action tests. All 25 tutorial exports regenerate unchanged; site link checks pass.
Next: extend the audit to explicit start-base-path data, with tests for transported
first meridians, before interpreting mismatches for other PDF support curves.
General geometric reconstruction and the remaining PDF correspondences are pending.

## Nonempty support transport, September 28

Added tutorial figure 25 comparing upper/lower 1-to-3 support arcs with
conjugates (2,1,-2) and (-2,1,2). Generation verifies both meridian transport
comparisons and that the exact braid actions differ despite identical endpoint
permutations. The upper arc's nonempty ray word (2,) gives x2 x3 x2^-1.
All 17 focused braid-action tests pass. All 25 SVG/TikZ tutorial figures
regenerate; HTML and site builds pass link checks. Visually inspected the new
comparison: arcs remain within the outline and signed generator labels are clear.
Next: use these calibrated examples to factor out a reusable transport audit,
then apply it to the confirmed factor 9 and remaining supplied support data.
General geometric action/reconstruction remains unfinished.

## Hurwitz support correspondence, September 27 evening

Tutorial figure 24 pairs the support arcs for ((1,), (2,)) and its Hurwitz
move ((2,), (-2,1,2)) with their individual downward-read braids. The supplied
conjugated support is Arc(1,3,direction='down'). Generation verifies that its
empty ray transport matches A(-2)(x1)=x1 and A(-2)(x2)=x3, plus product equality.
A regression test rejects the upper arc's different transport word. All 16
braid-action tests pass; 24 tutorial SVG/TikZ figures regenerate; site and HTML
builds pass link checks. Visually inspected the final four-column SVG raster.
This is a checked small support example, not automatic geometric action replay.
Next: extend transport comparisons to a nonempty-ray support before attempting
the remaining six-point PDF factors. Keep factor-order conventions explicit.

## Checked Hurwitz tutorial, September 27 afternoon

Added tutorial figure 23: a computed Hurwitz move on ((1,), (2,)) and its
inverse, showing each factor and the continuous product. Gold outlines identify
the first factor in each product. Generation checks exact Artin actions for all
three rows and checks restoration of the original factors before export.
All 23 tutorial SVG/TikZ figures regenerate, the HTML/site build passes local
link checks, and all 15 braid-action tests pass. Visually inspected the new PNG:
labels, inverse crossing and first-factor outlines are clear. This illustrates
braid manipulation only; no transformed planar support curve is asserted.
Next: add geometric support correspondence to this small checked example before
attempting a full six-point action replay; remaining PDF support encodings still
need comparison.

## Long closed-curve comparisons, September 27 morning

Replaced exhaustive cyclic-rotation construction in free_homotopy_key with
linear candidate elimination. Exact keys agree with an exhaustive oracle on
every word of length 0 through 6 over four signed letters; periodic and nearly
periodic 50,000-letter cases also pass. All 247 Python tests pass.
The five adjacent-pair loops under the earlier SVG braid give based lengths
2182, 8476, 8156, 13470, 7614; all five closed classes change in the disk
convention. Local key calculations took under 0.03 seconds each, saved in
.preview/closed-curve-comparison.json. This uses the earlier SVG, not a newly
verified PDF transcription. No rendering geometry changed; geometric replay
remains outstanding. Next: compare the remaining supplied support encodings,
retaining based data for the disk identity test.

## Checked substitutions and seven squared-twist splits, September 27

Added substitute_factors with exact Artin-action comparison of a selected slice.
Rejects incorrect replacements even when permutation agrees; validates untouched
input letters too. All 245 Python tests pass (117 seconds). Thirteen focused tests cover square splitting, braid
relation replacement, cancellation, invalid slice and invalid hidden letters.
Applied separately to original SVG factors 1,4,5,8,10,12,13, each with a conjugated
12-letter alternating triple-twist core: seven verified splits yield 20 factors.
Saved the result to .preview/six-seven-squared-twists-split.json. PDF correspondence
of remaining support curves stays provisional. Added runnable
examples/verified_twist_split.py; visually inspected the first split alongside
its support curve and continuous braid. Renderer footer remains explicit that
it does not check equality; the separate substitution operation does that first.
Next: compare the remaining support encodings, and retain the distinction between
disk-equality substitutions and sphere/boundary-framed relations.

## Closed-loop ray words and actions, September 26 evening

Added loop_ray_word, free_homotopy_key (unoriented free-group conjugacy key),
and act_on_loop_word (exact substitution preserving based words). Eleven focused
action tests pass; the full suite passes all 243 tests (154 seconds). Coverage:
base-cut shifts, reversal, enclosed punctures, invalid cuts,
conjugation invariance and boundary full-twist visibility in based versus closed
path data. The latter prevents silently declaring disk identity from fixed
closed curves. Canonicalization checks all rotations; do not feed enormous words
without improving its algorithm. No general Dehn-twist or geometric image
renderer is claimed. Visually checked two base-cut descriptions of the same loop
in .preview/closed-loop-base-cuts.svg/png. Next: use these encodings to compare
closed factors from the PDF with their braid blocks; retain based arc information
for the user's disk-versus-sphere identity comparison.

## Factor 9 relative-path comparison, September 26

Added arc_ray_word for point-to-point Arc itineraries, counting directed crossings
of upward puncture rays. Factor 9 gives t=(-4,-3,2,3,4,-5,-4,-3,-2,3,4,3).
Its SVG block is exactly g sigma1 g^-1 with g=(-2,-3,4,2,-3,-2,-2).
Verified A(g)(x1)=x1 and A(g)(x2)=t x4 t^-1. This is exact endpoint/ray-word
agreement, not verification of all factors or the geometric action convention.
Eight action tests pass, including reversal and upper/lower ray conventions.
The full suite passes all 240 tests (87 seconds).
Created .preview/factor-nine-check.html with the confirmed arc, upward rays and
a segment-by-segment table; visually inspected the diagram. Next: extend this
ray encoding to closed support curves, then compare remaining factors and build
geometric action replay. Full global order/sign calibration remains explicit.


## Factor checkpoints and global conjugation, September 26

Added action_checkpoints (identity plus every prefix, immutable snapshots) and
conjugate_factors (explicit g f g^-1). Six action tests pass, including prefix
comparison, empty factors, return to identity, conjugation's expected changed
product and inverse operation. Shared incremental action avoids replaying prefixes.
Extracted factors from SVG section-rule boundaries and verified concatenation
matches the prior word exactly: lengths 12,9,5,22,12,13,11,18,15,16,13,18,14.
Generated .preview/disk-factor-checkpoints.html and JSON with all 14 states.
The report explicitly labels algebraic prefix order and provisional PDF matching;
it is not a geometric reference-arc replay. Next: establish geometric action
conventions and check factor 9 against its 15-letter braid block.

## Exact disk action foundation, September 26

Latest user priority is a trustworthy factorization/action explorer, including
disk and sphere comparison, Hurwitz moves, conjugation and later substitutions.
Confirmed: positive half twists on arcs; positive Dehn twists on closed curves;
written 2 means squared Dehn twist; factors applied 1 through 13; sphere target
is Mod(S^2,6). Disk outer boundary fixed. PDF is provisionally the earlier braid,
not yet checked factor by factor. Do not silently promote that match to verified.
Confirmed factor 9: Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down'). Its SVG at
.preview/factor-nine-confirmed.svg was rendered and visually inspected; it
matches the broad nested shape on the PDF, but no braid conversion is claimed.

Added braid_actions.py with reduced free-group words, explicit Artin action,
and forward/inverse Hurwitz operations preserving concatenated product. Four
tests cover braid relations, inverses, nontrivial boundary full twist, Hurwitz
inverses/product preservation and invalid inputs. docs/BRAID_ACTIONS.md records
the composition convention and its still-unresolved mapping to geometric base
loops/application order. Earlier 178-letter transcription has nonidentity disk
action, image lengths 2609,3157,8037,8259,13589,5999, saved in ignored preview JSON.
This is algebraic groundwork, not the requested visual action replay yet.
Next: fix geometric action conventions, derive/check factor 9's braid, then
produce per-factor reference-system images with inspectable transformations.
Validation: all 236 Python tests pass (96 seconds).
Alpha 5 release is published with wheel/source assets and all workflows green.

## Alpha 5 release batch, September 25 afternoon

Prepared v0.1.0a5 with standalone and factor-local crossing highlights, the
editor highlight control and perimeter-opening placement validation. Updated
package/site versions and release instructions; normalized legacy dash bytes
in CHANGELOG.md to valid UTF-8. All 232 Python tests (120 seconds), 12 editor
tests and the site/link build pass. Regenerating 22 SVG/TikZ figures leaves
them unchanged from the visually inspected implementation batches.
Publish the version tag through the existing checked release workflow and verify
its wheel/source assets. Next core task is the certified perimeter reference
system's endpoint incidence and cut-disk topology, not further highlight work.

## Factor-local crossing highlights, September 25 midday

FactorPanel now accepts highlight_crossings, using unique 1-based positions in
its supplied braid word. Shared outline geometry serves standalone and aligned
braids. Connector padding, identity blocks and initial-state rows are excluded
from indexing. Tests cover both directions, unchanged strands/labels, initial
states, invalid indices, duplicate positions and SVG/TikZ exports. Focused suites:
21 factorization and 9 visualization tests pass. Visually inspected a three-factor
example including an identity block. Gallery 16 demonstrates a highlighted factor.
Full suite: 232 Python tests pass; tutorial HTML/site/link builds pass.
Next: release the completed highlights together after checking CI;
the certified perimeter reference system remains the larger core geometry task.


## Editor crossing highlight control, September 25 morning

Added an inspector checkbox for persistent exported crossing highlights, synced
with the selected crossing and disabled for the empty word. Earlier/Later now
transports highlights with the moved crossings. All 12 editor tests pass,
including toggle, movement, undo/redo, JSON save/reopen and empty-word behavior.
Browser inspection at localhost confirmed the checkbox and moved highlight
render correctly. Tutorial updated; factor-panel highlights remain next.


## Crossing highlights and revised pacing, September 25

User explicitly replaced the 15% reserve with a plan to use all available quota
productively before weekly reset. Updated the active six-hour heartbeat prompt;
it now distributes the full remaining allowance and removes both old 15% cutoffs.
At this turn's start 25% weekly remained; reset September 26 at 09:18 Eastern.

Implemented optional standalone BraidDiagram.highlight_crossings: unique 1-based
word positions produce outline-only bands behind strands in either direction.
The recipe schema accepts and round-trips the selection. SVG/TikZ use the same
paths; default output is unchanged. Gallery 22 now highlights the first crossing
in both directions. Visually inspected the regenerated figure. Focused validation:
9 visualization tests and 26 document tests pass; tutorial/site/link builds pass.
All 231 Python tests pass. Editor word shortening prunes out-of-range highlights;
deleting a crossing removes its highlight and shifts later positions. All 11
editor tests pass, including deletion, word shortening and undo of highlights. Factor-panel highlights and
editor selection controls remain next; mesh topology work remains as below.

## Mesh migration dependency clarified, September 25

Inspected genus_mesh mark-site selection and mesh_marks.mark_mesh. The earlier
next-step wording understated the task: spokes are registered ParentCuts and
Attachments, not display decorations. Existing certification explicitly depends
on them. Updated the implementation plan with the required separate certified
perimeter system and route conversion, and the tutorial with the distinction
between auxiliary chart cuts and valid curve-complex arcs. Use reference arcs
for presentation; retain the old atlas for existing DiskRoutes. No geometry was
changed. Next substantive step: design the perimeter system's parent endpoint
incidence and cut-disk topology before changing mark coordinates.

## Mesh endpoint migration guard, September 24 evening

Added a final-drawing regression covering explicit P-to-Q and Q-to-P DiskRoutes
in all four genus-two views. It compares rendered path endpoints to the rendered
mark centers and verifies continuity between path pieces. The older test only
compared projection coordinates in the default view; this protects the boundary
between mesh projection and display during the planned migration. All five
genus-mark tests pass (24 seconds). Visually inspected a four-view route sheet
in .preview/mesh-mark-endpoints.svg/png. No rendering behavior changed: marks
still use the legacy upper band, and the symmetric placement work is unfinished.
Next: change the mesh embedding and mark vertices together, retaining these
endpoint/continuity checks and the existing certified-complement checks. Do not
replace displayed marks independently of explicit route endpoints or merely
hide reference spokes. Usage 72% to 73% weekly; preserve the 15% reserve.

## Signed braid reading gallery, September 24 midday

Added figure 22 with the same non-palindromic signed word (1,-2,-1) drawn
downward and upward. Smooth crossings, signed labels and endpoint identities
make the fixed upper-end crossing convention visible. Tutorial includes a
runnable comparison and explains that upward traversal does not invert signs.
Regenerated 22 SVG/TikZ examples and the TeX gallery; visually inspected figure
22. Eight visualization tests, tutorial HTML build and site/local-link checks
pass. No library behavior changed. Usage 70% to 71% weekly, 2% to 6% five-hour.
Next core work remains coherent mesh-mark/reference-spoke migration; optional
braid atom highlighting remains pending. Keep deferred diagram families deferred.

## Reproducible placement troubleshooting, September 24 morning

Added a runnable tutorial example for the explicit perimeter opening guard:
the invalid two-mark placement prints the expected error, and a corrected
upper/lower placement saves a valid SVG. Explains render-time validation,
stroke clearance, automatic placement and the difference between a rejected
drawing and an impossible abstract arc. Executed the exact Markdown code;
visually inspected the corrected SVG through a white-background raster.
Regenerated tutorial HTML; site build and local-link checks pass. No library
code changed. Prior db985b8 Tests and Documentation workflows both succeeded.
Next: migrate mesh-bound marks and reference spokes coherently with explicit
route endpoints; do not move marks cosmetically while retaining old endpoints.
Usage moved from 69% to 70% weekly and 1% to 4% five-hour; this small documentation
batch preserves the weekly reserve and remaining six-hour run shares.

## Explicit perimeter opening guard, September 24

Fixed a reproduced rendering error: on genus two with Type I boundary 6,
P=(8,-9), Q=(-97,0.5) are legal marked endpoints, but the deformed solid
perimeter entered the left genus opening. Explicit placements now validate
all perimeter segments against handle curves using conservative cubic error
bounds and half the curve stroke width. Crossings/touches/insufficient clearance
raise an explanatory ItineraryError; no route is silently moved. Bounding-box
rejection keeps checks cheap. Automatic perimeter placement is unchanged.

Sixteen reference tests pass, including this regression in all four views;
nine supplied marked-arc tests also pass. Tutorial regeneration leaves the
21 SVG/TikZ fixtures unchanged. The pre-fix reproduction and valid tutorial
mark drawing were visually inspected. All 228 Python tests pass (126 seconds); the
tutorial HTML and site build pass, including local-link checks.

The previous v0.1.0a4 release is confirmed published with wheel/source assets;
its Release, Tests and Documentation workflows passed. This fix is Unreleased.
Next: mesh-mark/reference-spoke migration remains open. This guard is only for
explicit perimeter deformations, not a global clipping or bordered-mesh solution.
Usage began 65% weekly / 4% five-hour, reached 68% / 23%; stop at this checkpoint
to preserve remaining scheduled shares and the 15% weekly reserve.


## Versioned alpha release batch, September 23 afternoon

Prepared 0.1.0a4: synchronized pyproject.toml, release-page version and release
instructions. Rewrote the release notes around the completed editor, ordered
factor panels, supplied action states, smooth/labelled braids, perimeter arcs,
symmetric reference marks and 21-example gallery. Documented changed perimeter
member numbering and solid defaults, and retained explicit mesh/catalog limits.

Local validation: 227 Python tests, 10 editor-controller tests, regenerated
21 SVG/TikZ tutorials without fixture changes, rebuilt site/local link check,
and visual inspection of the release page. No library geometry changed.
The local Python lacks the build frontend; the existing release workflow builds
wheel/source archives and validates metadata using build/twine on Python 3.12.

Publishing sequence: push version commit, verify Tests and Documentation CI,
then tag v0.1.0a4 and verify the Release workflow plus wheel/source assets at
https://github.com/richardbuckman-math/surface-diagrams/releases/tag/v0.1.0a4 .
If interrupted, inspect that exact release before retrying; never move a tag.
Next development: mesh-bound mark/reference-spoke presentation remains primary
surface work; supplied braid atom highlighting is the next braid refinement.
Keep Heegaard/bridge/trisection/Kirby deferred. Usage began at 59% weekly, 0%
five-hour; midpoint 60% / 7%, preserving the 15% reserve. No reset credits used.


## Symmetric marked-surface gallery, September 23 morning batch

Added tutorial figure 21 (SVG and TikZ): closed genus-two reference drawings
with one axial mark, a symmetric pair, and an axial mark plus pair, from above
and below. Reference numbers are hidden to focus the comparison on marks.
Tutorial gives executable recipes, selection for marks-only drawings, and
explains that this reference presentation does not migrate mesh-bound marks
or convert explicit DiskRoutes. No library geometry or certified topology changed.

Fifteen boundary/reference tests pass. New regression covers every automatic
mark count for genus 1-3 in all four views: symmetric pairs, axial odd mark,
member counts and exactly two perimeter incidences per mark. Regenerated all
21 tutorial figures, visually inspected figure 21, rebuilt tutorial HTML and
site with local links checked. git diff --check passes.

Next surface increment: resolve how the checked mesh display exposes its legacy
mark spokes without presenting them as the requested curve-complex reference
family; do not move explicit route endpoints. Atom highlighting and releases
remain separate outstanding work. Usage began at 55% weekly / 0% five-hour;
30 percentage points above the reserve shared across about 12 remaining runs.


## Editor generator-label toggle, September 23

Added Show generator labels below Crossing style in the braid editor. It reads
and writes braid.show_generators, defaults off for old recipes, preserves the
signed word and supports undo/redo plus save/reopen. Ten controller tests pass.
Verified the real checkbox and smooth labelled braid in the local editor on
port 8765, including a negative generator. Tutorial instructions updated.
The preceding recipe-schema fix f442f2d passed all GitHub jobs (Python 3.9/3.12,
controller, LaTeX and documentation); its local suite passed 226 Python tests.

Next: supplied atom highlighting for the optional braid view, or the separately
tracked mesh-mark migration. Keep exact DiskRoute endpoints unchanged during
surface presentation work. Check remote CI after every pushed batch.


## CI recipe-schema regression fix, September 23

User reported failed Tests run 35814966482 on b854881; Documentation deployed
successfully. Reproduced locally: 225 tests, three errors and one failure,
all from `braid: unknown fields ['show_generators']`. BraidDiagram's new field
was serialized by dataclasses.asdict, but documents._normalize still rejected
it. The earlier focused visual tests missed this integration dependency.

Added optional boolean show_generators to braid recipe validation and passed it
through construction. Old recipes default false; new ones retain the option.
Regression covers old/new JSON round trips, rendered inverse label and invalid
values. Document tests (25), editor-controller tests (9), and the full Python
suite (226 tests) pass locally. Remote CI will be checked after pushing.

Future additions to serialized drawing dataclasses must check recipe schemas,
round trips and generated Python, not just geometry tests. Next feature remains
the editor checkbox; recipe persistence is now implemented.


## Optional braid generator labels, September 23 scheduled batch

Added BraidDiagram(show_generators=True) and
FactorizationDiagram(braid_show_generators=True). Plain-text sN / sN^-1 labels
sit to the right of each actual crossing in traversal order. They work with
straight/smooth crossings and both directions, skip empty blocks/connectors,
and reserve horizontal space in SVG/TikZ. Defaults leave existing output alone.
No strand paths, colors, signs, endpoint identities or words change.

Validation: 28 focused visual/factorization tests pass, including mixed signs,
multiple-digit indices, both directions/styles, unchanged standalone paths,
label alignment in factor rows, identity blocks and boolean validation.
Regenerated tutorial figure 20 and its TikZ counterpart; visually inspected it
and a factor-aligned example with positive, identity and negative blocks.
Rebuilt tutorial HTML and site; local links and git diff --check pass.

Next braid increment: recipe persistence and editor toggle for generator labels;
then supplied atom highlighting. Mesh-bound mark symmetry and invalid reference
spokes remain the separate larger surface-display task from the last checkpoint.
Do not move explicit DiskRoute endpoints as a cosmetic shortcut.
Usage: 46% weekly / 0% five-hour used at start; 47% / 7% at midpoint.
About 39 weekly percentage points remained above the reserve for roughly 13
six-hour runs. Stopped after one bounded increment; no reset credits used.


## Closed-surface reference visibility, September 22 evening batch

Extended solid-default closed reference styling to GenusDiagram, exposed through
with_cut_system(closed_curve_style="solid"|"split") and with_curves(...).
Split retains the mesh's rear corridor halves; enclosing loops stay solid.
Removed the arbitrary cusp-plane splitter. Styling preserves every directed
mesh segment, labels, mark positions, parent numbering and explicit DiskRoute
output. Chained with_curves retains the chosen style.

Validation: focused tests cover all four views, segment/label preservation,
option validation and unchanged explicit route output. Regenerated genus-chain,
named-member and tutorial SVG/TikZ assets; inspected the genus 1/2/3 tutorial
raster on white. Tutorial HTML and site/local links rebuilt. Unrelated route
asset regeneration produced tiny numeric differences, which were discarded.
The full Python suite passed (223 tests); git diff --check passed.

Next bounded step: design the migration of mesh-bound marks and reference arcs
to symmetric perimeter/axial positions without moving explicit DiskRoute endpoints
or misrepresenting the checked cut system. This batch changes visibility only;
old mesh mark spokes and stroke-edge clearance are still outstanding.
Usage at start: 43% weekly used, 0% five-hour used; mid-batch 44% and 8%.
Rough run allowance was about three weekly percentage points (42 available
above the reserve, about 14 six-hour runs until reset). No reset credits used.


## Surface-slice reference drawings, September 22 user correction

Richard clarified figure 15: keep curves inside the outline; no arc ends in
another curve's interior; use front/rear Type I attachments; connect Type II
boundaries along the perimeter; place an unpaired mark on the axis and paired
marks symmetrically above/below. Visibility changes belong at real edges.
This supersedes the historical cusp-plane and spoke conventions below.

Implemented in `with_reference_arcs()`: replaced all Type II/mark spokes by
continuous inward-offset contour paths terminating only at rims or marks.
The left-pair arc crosses the end loop continuously; figure 15 has three top
and three bottom connections plus the left connection split at axial M.
Type I return arcs meet front/rear rim extrema. Closed loops default to solid;
`closed_curve_style="split"` dashes rear corridor halves, while enclosing loops
remain solid because their present geometry never crosses an edge. Automatic
mark pairs share x coordinates. Explicit supplied coordinates are preserved,
with local perimeter deformation and validation. Straight supplied MarkedArcs
retain their clear-band guard. Reference numbers after 2g+1 now identify the
perimeter segments; callers should query member_numbers instead of old IDs.
`pair_bank` remains accepted for compatibility but no longer chooses spokes.

Validation: 222 Python tests passed; nine supplied marked-arc tests passed again
after restoring the convex-band guard. Updated tests check front/rear rim
endpoints, continuous side connections, mark incidence, symmetry, closed-loop
visibility, selection and sampled containment in the actual outer silhouette.
Regenerated SVG/TikZ tutorials, visually inspected figures 13 and 15 on white,
rebuilt tutorial HTML and site, and passed the site's local-link validation.
`git diff --check` passed. The containment test checks path geometry at default
styles, not a universal stroke-clipping certificate for arbitrary custom styles.

Next: migrate the separate checked closed-surface `GenusDiagram` presentation
(its old cusp-plane visibility and mesh mark placements) to the same visual
convention without altering the abstract cellulation or supplied DiskRoutes.
If split enclosing loops are wanted, design paths that actually reach silhouette
edges; do not restore arbitrary dashed transitions on the current ellipses.
The certified bordered mesh and general bordered DiskRoutes remain unfinished.


## Editor crossing-style selector, September 22 scheduled batch

Added Straight/Smooth to the local editor's braid controls. Older recipes with
no crossing_style show Straight; changing style preserves the signed word.
Undo/redo and save/reopen retain the choice. Nine controller tests pass, including
the new backward-compatibility/history/save regression. Browser-verified the
actual selector, smooth rendering in both traversal directions, and undo/redo
against the local Python server. This verifies this flow, not the entire editor
manual acceptance checklist. No Python geometry changed in this batch.

Next bounded increment: optional right-hand generator labels for standalone
and factor-aligned braids; then supplied atom highlighting. Preserve export
parity and keep annotations independent of mathematical equality checking.


## Paced continuation and smooth braid crossings, September 22

Recurring continuation is active every six hours in task
01a09c1a-c080-7ed2-900a-739fd9cd2c0a. Read account usage at each run; reserve
15% weekly for interactive use and share the remainder across scheduled runs
until reset. Do not consume reset credits. Continue one bounded useful batch.

The braid derivation is complete as an explicit local-move certificate in
`.preview/braid-six-seven-proof.html`, with JSON and a complete move table.
An independent verifier checks the supplied SVG transcription and all 2,486
elementary moves (19 sphere substitutions), without a normal-form oracle.
Endpoint: `(sigma_4 sigma_5)^3 (sigma_1 sigma_2)^-3`, two complementary triple
twists. This is identity in the sphere mapping class group but the nontrivial
central element in the spherical braid group. Do not restart this research.

Tiny Bubbles Lab's factor-5 reference now loads in the in-app browser, although
web retrieval still fails. Observed: cubic S crossings with vertical end
tangents and uniform crossing height, underpass gaps, persistent colors,
numbered endpoint badges, right-hand generator labels, atom shading, scrolling
and zoom. Its cubic has linear vertical position and smoothstep horizontal
position. No third-party code/assets were copied.

Implemented the first static increment: `BraidDiagram(crossing_style="smooth")`
and `FactorizationDiagram(braid_crossing_style="smooth")`. Defaults remain
straight. Tutorial figure 20 compares the same six-strand word. Next bounded
batch: generator labels/atom annotation for the optional braid view, then
an editor style selector. JSON documents already preserve `crossing_style`;
keep browser-only zoom distinct from exports.

Validation: all 219 Python tests and eight editor JS tests pass; all twenty
SVG/TikZ tutorial figures regenerate; portable-site links pass. Visually
inspected the straight/smooth comparison. Initial suite failures exposed a
missing JSON field allowance (fixed) and relative PYTHONPATH in subprocess
tests (rerun with absolute repository src path). No remaining failures.


## Requested next braid view, September 21

Added the user-linked Tiny Bubbles Lab factor-5 braid display to the V3 plan as
an optional renderer alongside the current view. Inspect the exact reference
before choosing implementation details: retrieval was blocked today. Preserve
braid signs, strand identities, direction and factor-panel integration. See the
new next-task section in IMPLEMENTATION_PLAN.md for the link and acceptance work.


## Overnight batch 5, September 21

Clarified stale tutorial claims about Type II/marked-point reference spokes.
Added current boundary support and remaining variants to the plan, preserving
earlier checkpoints as history. Certified bordered cut systems and general
DiskRoutes remain unsupported. Documentation-only; rebuilt tutorial HTML and
checked portable-site links. Morning wrap-up: check remote CI, summarize the
five overnight batches, and delete the overnight automation at 8:05 a.m. Eastern.


## Overnight batch 4, September 21

`MarkedArc` accepts optional validated hex `color`; omitted colors inherit
Style.curve_color. Closed and bordered renderers honor it, including selections
and overlays. Tutorial figure 19 keeps P-Q red and R-S blue across all panels.
Nine focused marked-arc tests and 25 tutorial snippets pass; closed-surface
explicit/inherited color SVG/TikZ exports were checked separately. Regenerated
19 figure pairs and visually inspected the comparison. Next: editor visual
verification or improve marked-point label placement near the outer contour.


## Overnight batch 3, September 21

Tutorial figure 19 now isolates P-Q and R-S before showing their overlay on
identical surface geometry. Added a runnable comparison recipe and clarified
that these are input comparisons, not computed action states. All 25 tutorial
Python blocks pass; 19 SVG/TikZ figures regenerate and the new stack was visually
inspected. No library code changed. Next: editor visual verification or explicit
curve colors for bordered marked-arc overlays.


## Overnight batch 2, September 21

Bordered `.with_curves(..., allow_intersections=True)` now permits transverse
marked-arc overlays, retaining straight paths in all four views. Default
disjointness checking remains; overlaps and intervening marks remain invalid.
Selection and later additions retain the option; explicit False restores checks.
This is supplied surface geometry, without braid over/under data or computed
actions. Tutorial figure 19 was visually inspected; all 19 SVG/TikZ figures
regenerate, 24 tutorial snippets and eight focused marked-arc tests pass.
Next small batch: editor browser verification, or clearer curve identity/color
controls for supplied bordered families. Keep certified routing separate.


## Overnight batch 1, September 21

Added `family.with_labels(reference=False)` to hide reference numbers while
retaining colored guides and marked-point names. `.with_labels()` restores
numbers; selection and supplied arcs preserve this setting. Tutorial figure 18
now demonstrates the cleaner display. SVG was visually inspected; all 18
SVG/TikZ figures regenerate. Six marked-arc and eleven boundary-anchor tests
pass. Next small batch: editor browser verification or supplied intersecting
marked arcs (currently rejected), with explicit presentation-only semantics.


## Integration checkpoint, September 19

Merged the remote factorization/editor contribution with supplied bordered
marked arcs, preserving both. The tutorial now has 18 SVG/TikZ figures and
23 executable Python recipes; the marked-arc example is figure 18. Fixed the
missing TypeIBoundary import in the earlier factorization recipe. Browser
image decoding and portable-site local links pass. Eight editor JS tests pass.
All 212 Python tests pass. The first combined run had one Windows
connection-abort in an HTTP origin-rejection test; both its focused suite and
the complete suite passed on rerun.
The repeated one-time 9:16 automation was deleted; do not reschedule it.
Older checkpoints below describe validation at their respective commits.


## Bordered marked-arc display and active scope

Heegaard, bridge, trisection and Kirby families are deferred until a concrete
use case and excluded from core display completion. Updated controlling plan.
Bordered reference families now accept `.with_curves(MarkedArc(...))` for
supplied straight arcs in either clear mark band. Selection hides reference
members without dropping arcs or marks. Unknown endpoints, cross-band paths,
intervening marks, intersections and overlaps are rejected. Tutorial figure 18
shows mixed boundaries and upper/lower arcs, with and without guides.
Validation: 158 tests pass; sixteen SVG/TikZ tutorial figures regenerate.
General bordered DiskRoute bindings remain unfinished: the saved cusp-chart
prototype is not certified and has not been applied. Next: route locators and
supplied factor/action views, plus a justified boundary mesh construction.

## Local browser editor, September 13

Added an immutable version-1 `DiagramDocument` JSON recipe API and a dependency-
free, loopback-only browser editor. The editor supports horizontal planar point/
boundary rows, arc/loop itineraries, signed braid words, transported strand IDs,
labels, whole-recipe undo/redo, JSON open/save, and SVG/TikZ/reproducible-Python
downloads. All geometry remains in the existing library. See [EDITOR.md](EDITOR.md)
for usage, schema limits, security boundaries, and the manual acceptance checklist.

The original 171 Python tests plus 36 document/HTTP tests pass (207 total), as do
8 JavaScript controller tests using a minimal DOM double. Both document
kinds reproduce exact SVG/TikZ output when their generated Python is run. The
hosted browser could not open the local URL (`ERR_BLOCKED_BY_CLIENT`), so visual,
pointer, and file-dialog testing remains pending. Do not describe this as a
visually verified or release-ready editor. No Godot or Tiny Bubbles Lab deployment
is included in this contribution.

## Ordered factor/action diagrams, September 13

New presentation APIs: `FactorPanel` stores a distinct factor ID, support panel,
nonzero signed exponent, optional complete braid block, group label and supplied
after-state. `FactorizationDiagram` lays out application-ordered rows bottom to
top by default and prints their right-to-left product. An optional braid column
is continuous across rows; strand colors/endpoint IDs are transported without
resetting at a factor boundary. Crossings stay compact within tall rows. Complete
supplied state sequences form a second surface column. Missing states/blocks,
duplicate factor IDs and noncontiguous groups are rejected.

`BraidDiagram(direction="bottom-to-top")` adds upward traversal while preserving
the original fixed sign convention: positive means upper-left over upper-right.
Words are never reversed, simplified or exponentiated by these drawing APIs.
The existing top-to-bottom default and all prior tutorial SVG/TikZ files are
unchanged. Support geometry, cut itineraries, colors and visibility are reused.

Tutorial figures 16/17 demonstrate grouped planar factors with an adjacent braid
and bordered support/action-state panels. The LaTeX gallery now fits both page
dimensions, avoiding overflow from tall figures. Validation: 171 tests pass
(18 new), 17 SVG/TikZ tutorial recipes regenerate, the 17-page TikZ gallery
compiles without overfull boxes, and the portable documentation site's local
links pass. SVG and compiled TikZ examples were visually inspected.

These changes do not compute actions, certify braid lifts or equivalences, or
complete the bordered cut-system mesh. No Tiny Bubbles Lab deployment is part
of this branch. The drawing examples are supplied data, not verification of a
new mathematical relation.

## Tutorial site and catalog, September 13

Interrupted mixed-boundary batch verified: 153 tests pass and all 15 tutorial
figures regenerate. Portable site builder checks local HTML links. Twelve planned
relation/fibration pages live in docs/catalog/*.json. User supplied the existing
GitHub repository as publishing destination; GitHub Pages is primary, with an
optional GitLab CI configuration. Release version is 0.1.0a3. See RELEASING.md.


Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) first. It is the controlling
roadmap for the new work. This file is the short, frequently updated checkpoint.

## Mixed four-view boundary reference families

The common left Type II + top/bottom pairs + right Type I layout is now supported,
also with explicit plane marks, in all four views. Only same-end Type I/II
combinations remain excluded; the previous opposite-end restriction was overly
broad. Tutorial figure 15 shows this fixture and its stable member identities.

## Member selection for bordered factor panels

`family.select(*numbers)` isolates reference members while retaining geometry,
colors and surface marks; `family.member_numbers` lists available IDs. Empty
selection keeps the bare surface and marks. Tutorial figure 14 shows vertical
factor-support panels on a bordered genus surface. Actions are not computed.

## Explicit marked-point plane bindings

`with_reference_arcs(mark_positions={"P": (x,y), ...})` now places all named
surface marks explicitly in clear upper/lower vertical-plane bands and connects
them inward to the first chain member. IDs and spoke colors follow surface.marks
order. Missing/extra IDs, invalid bands, overlapping marks, marks on reference
curves and spokes crossing another spoke are rejected. Existing automatic
mesh-based mark positions are unchanged. Figure 13 demonstrates this API.
There are now thirteen main tutorial SVG/TikZ figures plus the disk diagnostic.
The certified marked bordered mesh remains unfinished.

## Side Type II spokes and independent presentation geometry

Standard side pairs now connect their inner a anchors to the midpoint of the
outer odd member's upper/lower branch, with inward-tangent cubic spokes. One pair
per side is supported, also mixed with top/bottom pairs and interior Type I rims.
Explicit exclusions: outer bank b for side pairs, repeated same-side pairs, Type I
end rims combined with side pairs, and marks. These cases need further bindings.
The supplied reference drawing no longer asks the closed-surface mesh to validate
it; direct even-wrap geometry avoids the unsupported height-150 closed mesh case.
The certified mesh validator itself is unchanged. Tutorial figure 12 includes a
mixed side/top example.

## Top/bottom Type II reference spokes

`with_reference_arcs(pair_bank="a")` now handles top/bottom Type II pairs, including
mixed Type I boundaries. Each rim gets a vertical-plane spoke to the first chain
member directly inward from its chosen a/b anchor; cubic targets are bisected
rather than snapped to sampled points. Spokes inherit target visibility and
receive persistent boundary-order numbers/colors. Side Type II and mark spokes
remain unfinished, as does the certified bordered mesh. Tutorial figure 12 now
collects the bordered reference families; figure 10 retains attachment guides.

## All Type I slot reference families

The reference drawing now accepts Type I boundaries at genus cusps as well as
outer ends. Odd corridor members use the actual two slot endpoints, opening into
arcs wherever a boundary is present. Even members around opened cusps use a
rounded offset enclosure of the hole/rim control hulls, keeping a small gap;
unopened holes retain the earlier tight wraps. This is presentation geometry,
not a certified bordered mesh. Type II and marked spokes remain unsupported.
Validation: 146 tests and 17 tutorial recipes pass; the updated figures were
visually inspected. The preceding end-boundary commit passed remote CI.

## Type I end reference arcs

`GenusSurface.with_reference_arcs()` draws the reference family for one or both
Type I end boundaries. Each end member becomes two vertical-plane arcs joining
actual rim anchors to the neighboring cusp; interior members retain their IDs,
colors, and cusp-aligned visibility. Both exports and all four views are covered.
This separate presentation API does not pretend to supply a certified bordered
cellulation. Type II connections and marks remain explicitly unsupported. Tutorial figure 10 now shows the end reference family.
The user's one-time 9:16 a.m. Eastern continuation fired during this work; do not
reschedule it.

## Boundary-plane endpoint bindings

`GenusSurface.boundary_anchors()` returns exact rim/vertical-plane attachments
with boundary IDs and a/b banks. `boundary_anchor(id, bank)` resolves one;
`boundary_guide()` draws a labeled SVG/TikZ inventory, now in tutorial figure 10.
The positions are the actual endpoints shared by both half-rims, not rim centers.
Bank letters track tangent orientation, not front/back or cut-disk banks.
These are presentation bindings only: connecting reference arcs, marked-point
bindings and certified Type I/II cellulations still need implementation.
The previous cusp-transition CI run passed (db2b04a).

## Numbered route input update

`CutAtlas.crossing_on_cut(number, segment=1, bank="+", position=.5)` matches
`system.diagram(show_segments=True)` labels such as `2.1+`. Segment/bank coordinates
are mesh-specific; bank signs are not visibility or twist signs. The torus tutorial
now uses this explicit input. Type I/II mesh bindings remain the next major gap.

## Current checkpoint: September 13, 4:15 continuation

The one-time continuation automation is paused. Endpoint commit a76f1c7 passed
remote CI; legend commit 1d8deaa was still queued at this run's start.
Circular planar boundaries now export to TikZ using transparent even-odd stroke
clipping, including Figure panels. The main LaTeX gallery includes all hole
scenarios. Tutorial generation now writes eleven TikZ pictures plus a compilable
`examples/output/tutorial/tutorial-gallery.tex`; CI compiles this document too.
All 140 tests and all 14 tutorial Python blocks pass locally. TeX compilation
is delegated to CI because no TeX executable is installed locally.
Next visual priorities: Type I/II cut-system bindings and accessible genus route
locators, then richer supplied factor/action states. Do not redo endpoint controls
or legends, which are complete. Calculation engines remain lower priority.

## Legend and intersecting-family update

`PlanarDiagram(show_legend=True)` adds stable curve IDs and color swatches below
the surface, in SVG and TikZ. Tutorial figures 04/05 use it; figure 05 also shows
individual components beside the overlay, preserving their supplied routes.
No intersection certification or automatic curve offsetting is implied.
Validation: 140 tests pass; all 14 tutorial blocks run; browser images load.
Remote run 34737479779 for the preceding endpoint commit was still queued.

## Latest visual update

Planar circular boundaries now support exact left/right curved arc endpoints via
`Arc.start_side` and `Arc.end_side`; omitted sides face the route. Invalid endpoint
hole crossings are rejected analytically. Tutorial figure 03 demonstrates explicit
outward-facing endpoints. All 139 tests and 14 tutorial Python blocks pass;
browser checks show all eleven images loading without page overflow. Continue with intersecting-family layouts and visual IDs.

## Resume here

**Visualization first: follow V0-V4, then C1-C4 in IMPLEMENTATION_PLAN.md.**

Richard's five use cases now control the work: planar and standard nonplanar
curves/cuts, vertical factorizations and adjacent braids, supplied visual
transformations, then homology/fundamental-group and Lefschetz-invariant engines.
The earlier R0 exact-core gate is superseded. Keep the architectural separation
but do not defer drawings while researching calculations.

Tutorial: docs/TUTORIAL.md and browser edition docs/TUTORIAL.html. Run
`python examples/tutorial.py` for eleven main SVGs, one detailed cut-disk SVG and eleven TikZ counterparts.
The extra handle arc and `handle_style` constructor option have been removed.
New presentation records: ColoredCurve, PlanarDiagram, BraidDiagram, Panel, Figure.
Genus cut systems use numbered rainbow colors. Independent planar overlays are
opt-in and do not certify intersections; supplied states are not computed actions.

**Current visual refinements:** balanced Type I end clearance is pushed in
`e4f7b32`. The four-view fixture now has a 44-unit right strip, comparable to its
44-unit inter-hole gap and roughly 43-unit opposite strip. The missing generated
LaTeX gallery update was also fixed; GitHub run 34735538354 passed all jobs.

The completed appearance batch changes the default to above/right, makes planar reference cuts
straight symmetry-axis intervals, tightens even genus cuts and applies Richard's
confirmed opposite visibility patterns (above view: odd solid below; even solid
above). `PlanarSurface.with_cut_system()` supplies the standard colored intervals.
`MarkedArc` supplies straight visual arcs between automatic marks while preserving
explicit DiskRoute itinerary behavior. See the tutorial for the two input types.

Validation: all 138 tests pass on Python 3.12; the three new appearance tests
also pass on Python 3.9. All fourteen tutorial Python blocks ran, and the
regenerated figures were visually inspected. CI now also
regenerates genus and tutorial figures in its Python 3.12 job so stale outputs
cannot be missed by the gallery-only generation step.

**Next action: V2/V3.** Finish Type I/II cut bindings and make genus
route locators easier to select. Gentle top/bottom undulation remains a minor
later refinement. Calculation engines remain behind requested visualizations.

The earlier visual-cycle status below is retained as a technical checkpoint:
P0-P3 complete, P4 partial, P5-P8 unfinished and rescheduled.

Current P4a checkpoint: standard_cuts.py now builds certified 2g+1 chains and
numbered boundary/mark spokes. See standard-chains.md. The validator now has
explicit Attachment records for spoke endpoints on chain edges.

Disk routing and numbered complementary-disk diagnostics now work in
`disk_routes.py` and `cut_diagrams.py`. Ten new tests cover repeated crossings,
reversal, boundary returns, explicit overlays and reconstruction after cutting
along a route. Six generated SVG examples are in examples/output/cut-disks-*;
the decorated disk preview was visually checked, including mark M.

Closed default-genus presentation binding now uses an explicit doubled holed
mesh with smooth cubic chain edges. Every curved triangle passes a whole-curve
Bernstein orientation certificate; harmonic cut-disk charts check every triangle.
Genus 1/2/3/5/7 pass all four views. Named cuts and disk routes render with explicit
front/back visibility. The smooth genus-two preview was inspected. The current
127-test suite passes on Python 3.12.14 and 3.9.7; the 16-view regression checks
include genus 1/2/3/5.
The additional genus-seven four-view check also passed.

Marked closed-genus surfaces now work with `GenusSurface(2, marks=('P', 'Q'))`.
Supplementary mesh paths attach at regular cut vertices and reach the actual
marked vertices; the validator checks the resulting disk boundaries. Four new
tests cover all views, stable walks, missing-spoke rejection, exact marked arc
endpoints and maximal automatic mark counts. The marked-cut preview was inspected.

Previous P4 next action, now prioritized in V2: extend the checked presentation
binding to Type I/II boundaries.
The experimental `genus_outer_mesh.py` now classifies top/bottom rim halves and
matching seams explicitly. Its unfinished integration is preserved in
`docs/checkpoints/top-pair-binding.patch`; see that directory's README for the
exact default-genus-two cusp failure and resume commands. The patch is not
applied to the public API, and the edge charts are not a surface certificate.
The two edge-chart tests pass on Python 3.9/3.12; the full Python 3.12 suite now
contains 129 tests. The saved patch passes `git apply --check`.
These are still explicitly unsupported by GenusSurface.cut_system(); the
standalone abstract decorated chain remains available. The former instruction to
finish all remaining P4-P8 work is superseded by the visualization-first roadmap above.
Closed route examples now include multiple handles, a separating loop producing
two once-bordered tori, repeated visits to a cut edge, disjoint handle loops,
and explicitly declared intersections. Their generated contact sheet was inspected:
the harmonic mesh projection is continuous but retains visible tangent changes
between carriers. Smooth presentation-wide routing remains a visual refinement;
do not describe these routes as globally smooth.
Do not mark P4 complete from closed examples alone. New binding modules and
records remain experimental. Projection flattening now uses positive rational
Bezier control hulls to bound every segment, separately from the whole-curve fold
certificate; midpoint-only flattening has been removed. Disconnected projected
pieces are rejected even when their sheet changes.

P3b adds `src/surface_diagrams/cut_systems.py`, 26 tests in
`tests/test_cut_systems.py`, and seven worked examples in
`examples/cut_system_examples.py` with checked-in `examples/output/cut-systems.json`.
It reconstructs full/cut surfaces, vertex links, boundary cycles and mark copies,
and checks parent walks and transverse intersections. All 93 tests pass on
Python 3.9.7 and 3.12.14. JSON reports regenerated identically twice; no SVG or
TikZ geometry changed. The new records are internal, not package-root exports.
Rendered binding, shared parent endpoints/edges, tangencies and triple parent
intersections are explicitly unsupported. P4 may extend these with exact
incidence contracts if its standard configurations require them.

P2 was recovered and committed as 79bf6bd; P3a specification as 577b18f.
Both were pushed before this implementation. Earlier P1/P2 visual checks below
remain historical evidence, not a new visual audit.

Repository root on Richard's machine: `C:\GitHub\surface-diagrams`.
Remote: `https://github.com/richardbuckman-math/surface-diagrams`.
All source links below are repository-relative so another AI can work from a clone.

## What has actually been checked

- Starting code commit: `1af585c` (merge after `97c9c6c`). Version: `0.1.0a2`.
- `python -m unittest discover -s tests` passed **44 tests** at planning time
  with the repository `.venv`.
- Earlier implementation work also verified 44 tests on Python 3.9.7 and 3.12.14,
  built a wheel, compiled 48 TikZ figures plus one multiple-inclusion page with
  Tectonic 0.17.0, and visually inspected the compiled contact sheet. These are
  historical checks, not evidence for future changes.
- The current worktree initially had no tracked changes; only `Figures/` was
  untracked. Richard explicitly authorized including all those diagrams.
- Located **114 original SVGs, 8,102,982 bytes**. All eight named references and
  the additional `BPlanarCutSystem.svg` were rendered and inspected. The other
  SVGs were inventoried, not individually interpreted or visually reviewed.
- [Figures/MANIFEST.json](../Figures/MANIFEST.json) records SHA-256 and byte size
  for every original SVG. The source SVGs are retained unchanged.
- P1 adds `genus_geometry.py`, slot-aware radii, automatically spaced pairs,
  sideways collars, and explicit hidden rim halves. It adds five untuned/override
  examples and a source-comparison generator. Current gallery: 53 scenarios.
- P1 verification: 52 tests pass on Python 3.9.7 and 3.12.14. The SVG genus gallery
  and original-versus-generated comparison were visually inspected. Existing
  TikZ output was regenerated from shared primitives; no exporter logic changed.
- September 11 refinement: 58 tests pass on Python 3.9.7 and 3.12.14. Python 3.9
  requires `PYTHONPATH` pointing to this checkout's `src` (it has no installed
  package). New tests
  cover all four views, boundary visibility including handle-tip boundaries,
  true trimmed hole overlap, mirrored occlusion, direct collar joins, and roomy
  side-pair defaults. The updated D3/D2A/E2 comparison and four-view sheet were
  visually inspected, along with all 17 genus gallery panels. Gallery now has
  57 scenarios. SVG and existing TikZ outputs were regenerated; Tectonic compiled
  the gallery successfully. No TikZ exporter code was changed, and this is not P7.
- The unfinished P2 diff was saved byte-for-byte through git diff and reversed
  out of the working tree. `git apply --check` confirms it can be restored.
  This was the historical P1 checkpoint. P2 has now incorporated that work;
  its obsolete patch has been removed from the current tree.
- P2: circular planar holes, rim-ended arcs, outline-aware clearance, transparent
  stroke clipping, and numbered row guides. All 67 tests pass on Python 3.9.7
  and 3.12.14 (nine additional P2 tests).
  All 14 new gallery scenarios were visually inspected; 1,182 hole-interior
  pixels per image were checked on transparent and colored outputs. Existing
  planar/curve/direction/genus SVG examples were unchanged. Gallery: 71 scenarios.
  New circular-hole TikZ output raises an explicit error pending P7; existing
  export tests still run, and the LaTeX generator marks SVG-only examples.

## User decisions, in priority order

1. The four primary references establish the default nonplanar visual style.
   The E3B/D1/F3B alternatives are secondary presets.
2. The prettiest ordinary result should need only mathematical inputs.
   Appearance parameters are optional for unusual requests.
3. Numbered chain curves plus boundary/mark arcs form a cut system only if its
   complement consists of unmarked disks (boundary marks allowed).
4. Nonstandard configurations set up their cut system once when configured.
5. Show numbered cut-system diagrams in examples and the complete test suite.
6. Add actual planar circular boundaries first in rows, then general layouts
   including the daisy reference. Retain dots and distinguish marks from holes.
7. Add arcs and closed curves on those surfaces; Richard explicitly clarified
   that he did **not** mean subsurface highlighting.
8. Extend TikZ/LaTeX for the new work last. The existing exporter stays usable.
9. Include all supplied reference diagrams in the repository. This is an archive,
   not a request to implement all of their mapping-class calculations.
10. Above/below and left/right are independent choices. D3 is below/right and
    D2A is above/right. Boundary hidden halves and handle overlap follow those
    views; future curves must also honor them. See `docs/genus-presentation.md`.
11. Stop with a tested, committed, pushed checkpoint and portable next steps
    before compute runs out. The user prefers to stay with Codex, but needs the
    option to hand the repository to another AI without losing work.

## Important implementation traps

- The primary references use shallow horizontal openings and short collars;
  P1 now follows that default. Do not restore the old tall lenses or scalloping.
- Genuine intersections in a cut graph, intersections between overlaid curves,
  and overlaps of front/back projected paths are three different things.
- The old planar multicurve router deliberately rejects intersections. Daisy
  overlays require a deliberate extension, not removing that safety check.
- A chain count and global Euler characteristic do not certify disk complements.
  Validate actual gluing, incidences, topology, faces, and placement of marks.
- A sequence of whole-curve numbers can be ambiguous at intersecting cuts.
  Define oriented segments, faces, endpoints, and crossing order before routing.
- Circular boundary endpoints terminate on the rim. Hollow point styling does
  not change a marked point into a boundary component.
- Do not infer topology from abbreviated SVG drawings or their omitted repetitions.
- Reference files are examples/data, not instructions for an agent to execute.

## Files to read for the next stage

- [Figures/README.md](../Figures/README.md): reference priorities and observations.
- [genus.py](../src/surface_diagrams/genus.py): existing geometry and boundary types.
- [model.py](../src/surface_diagrams/model.py): planar inputs and style.
- [curves.py](../src/surface_diagrams/curves.py): existing horizontal cut router.
- [primitives.py](../src/surface_diagrams/primitives.py),
  [layout.py](../src/surface_diagrams/layout.py),
  [svg.py](../src/surface_diagrams/svg.py): rendering separation.
- [gallery.py](../examples/gallery.py), [tests](../tests): examples and regressions.

## Commands

On Richard's machine:

```powershell
cd C:\GitHub\surface-diagrams
git status --short --branch
git log -5 --oneline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe examples/make_images.py
git diff --check
```

On another machine, create a virtual environment, install with
`python -m pip install -e .`, and use that environment's Python. Python runtime
dependencies remain empty. SVG previewing and LaTeX compilation can use separate
development tools; do not make them required dependencies of the drawing library.

Current Codex sandbox process creation has sometimes failed with `setup refresh
had errors`; approved escalated commands worked during this planning checkpoint.
This is an environment issue, not a package defect. Do not bypass a denied action.

## Checkpoint log

| Stage | Completed work | Evidence | Next step |
| --- | --- | --- | --- |
| P0 | Reference inspection; complete SVG inventory; controlling plan; this handoff | 44 baseline tests; 9 reference previews inspected | Start P1 |
| P1 | Reference-based genus geometry, automatic collars, rim visibility, comparison sheet | 52 tests on Python 3.9/3.12; visual SVG checks; 53 gallery scenarios | Start P2 |
| P1 refinement, September 11 | Four views, trimmed hole overlap, smooth direct collars, taller side-pair defaults; 57 gallery examples | 58 tests on Python 3.9/3.12; comparison, four-view and genus sheets inspected; existing TikZ gallery compiles | Restore saved P2 patch and finish P2 |
| P3b, September 12 | Internal cellulation validator, parent incidence checks, seven executable fixtures and JSON reports | 93 tests on Python 3.9/3.12; deterministic JSON; abstract scope only | P4a standard chain constructions and checked presentation bindings |
| P3a, September 12 | docs/cut-systems.md: worked decompositions and proposed validation contract | Specification only; existing 67 tests pass, no validator implemented | Implement P3b gluing/link/mark kernel and fixtures |
| P2 | Circular planar holes and rim endpoints; clipping and clearance; 14 examples; SVG-only export guard | 67 tests on Python 3.9/3.12; geometry and raster checks; old SVG examples unchanged | Start P3 specification and validator |

Append a row or update it at each meaningful checkpoint. Record the actual files,
commit, tests, failures, and next action. Never make a future AI infer status from
a large transcript. Keep the stage table in IMPLEMENTATION_PLAN.md in sync.

## Prompt for another AI

```text
Continue the surface-diagrams repository from its saved checkpoint.
First read docs/HANDOFF.md, docs/IMPLEMENTATION_PLAN.md, and Figures/README.md.
Inspect the actual repository status and reference SVGs; do not rely only on
this prompt. Resume the first unfinished stage in the plan and keep both
checkpoint documents current. The primary references are D3HyperellipticLifted,
D2AHyperellipticSurfaces, E2MCKHOddGenusLifted, and
E2MCKHOddGenusLiftedWithBoundaries, all in Figures/ as SVGs.
Make beautiful ordinary diagrams require minimal parameters. Build and certify
numbered cut systems whose complement consists of unmarked disks, then support
arcs and closed curves on standard genus and custom planar configurations.
Include ordinary and numbered-cut examples and substantive tests for every
supported configuration. Extend TikZ/LaTeX for the new features last.
Follow the saved plan's stage gates and preserve existing work. Ask only when
different mathematical interpretations require the author's decision. Record
progress and exact next actions before stopping or handing off. Do not claim
a stage complete until its acceptance tests and visual checks pass.
```

## Historical cusp-plane convention (superseded September 22)

Type I/II boundary and marked-point reference arcs must lie in the vertical
plane. Bind their endpoints to the actual boundary/mark geometry in that plane;
do not fan them through an arbitrary surface chart. Even genus wraps change
visibility on the projected line through the hole cusps, matching their odd
neighbors, rather than at y=0. This affects presentation visibility only and
preserves supplied curve itineraries and the checked cellulation.

Cusp-plane update validation: 142 tests pass, including transition checks in all
four viewing directions. Genus and tutorial outputs regenerated and inspected.
