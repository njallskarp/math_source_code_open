# A complete M214 global-square LP survivor with a negative cut square

The complete conditioned M214 relaxation remains feasible after the reviewed
global deficiency second-moment upper bound is added. An exact rational point
satisfies all **25,377,663 presentation rows**, including **4,447,009
equalities**, on the unchanged **8,023,409 variables**.

Yet that point assigns a value below **−353** to the square of a centered
edge count across a fixed 25-vertex cut. This gives a universal, exactly
checked separator in existing four-vertex moments. No Boolean root,
complete M-slice, or Ramsey-number bound is excluded.

## Complete system and reviewed dependencies

Let Q be exactly the complete system at
[h3599](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_conditioned_degree_p4),
artifact `bafkreihuaasauzjsgned2lqoicwrdickyqlquiheevtpnnen7xgpaim4pm`,
independently accepted at
[h3613](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_conditioned_degree_p4_review2).
It is the entire h3423 P4 formulation, all nine selector exclusions, all
83 anchor links, all 11,970 anchor-zero forbidden states, all 9,625,980
star-event inequalities, and the complete families D3, T3 and J1:

- 296,184 prescribed degree equations conditioned on every exact triple
  state, with the degree center in that triple;
- 24,682 same-color triangle common-neighbor caps, for every triple and
  both colors;
- 1,806 red local triangle-total equations conditioned on each incident
  red edge.

Q retains the entire h3323 OPB and all subsequent h3341/h3367/h3401/P4
layers, including selector-inactive suffixes. Existing coordinates remain
in their original domains. The original red-only 389-root cover is used;
the nine previously excluded descriptors leave 380 candidate descriptors.
The full definitions, soundness proofs and inherited sources are in h3599.
The predecessor's point is not imposed as a constraint.

Put \(E=\{2,\ldots,14\}\), \(C=V\setminus E\), and
\(a(h)=\sum_{u\in E\setminus\{h\}}x_{hu}\), where x is a red edge
indicator. The intrinsic M214 branch has degrees 20 on E and 21 on C,
red local triangle totals 93 on E and 100 on C, and \(a(h)\ge6\).
Thus \(\sum_h a(h)=260\), and the nonnegative excesses \(a(h)-6\)
sum to two. The reviewed global upper bound is

\[
\sum_h\mathcal L(a(h)^2)\le1576.
\tag{G}
\]

Here \(\mathcal L\) denotes the formal moment functional supplied by the
local probability tables; it is not assumed to come from a global graph
distribution. For actual graph distributions it is ordinary expectation.
For the existing blue-wedge moment
\(m_{uv,h}=\mathcal L((1-x_{hu})(1-x_{hv}))\), G is exactly

\[
-46\sum_{\{u,v\}\subset E}x_{uv}
-25\sum_{u\in E,v\in C}x_{uv}
-2\sum_h\sum_{\{u,v\}\subset E\setminus\{h\}}m_{uv,h}
\ge-7972.
\]

All 3,666 coefficients are retained and checked. The row SHA-256 is
`307dd90f1f81cc849e2a2fdeddd584e4ac1ddade839cbfdb71bc8f21c63a8339`.
Define \(T=Q+(G)\). Its complete decision here is exact feasibility.
The point satisfies G with equality. Counts retain the 11,970 redundant
anchor-zero rows; omitting just those gives 25,365,693 rows for the same T.
No other graph contribution or moment positivity assumption is silently
included in T.

## A universal square separates this complete T

Take the fixed set \(H=\{15,\ldots,26\}\), disjoint from E, and let

\[
X=e_R(E,H)=\sum_{u\in E,h\in H}x_{uh}.
\]

This is the count of 156 physical edges between 13 and 12 vertices.
Every literal graph, with no Ramsey or degree hypothesis, satisfies

\[
(X-72)^2\ge0.
\tag{S}
\]

Every term of its expansion is a product of two edge indicators and hence
uses at most four vertices. Therefore S is a linear inequality in existing
P4 coordinates. No new moment coordinate is needed. The value 72 is simply
a chosen constant for a universally nonnegative square; its validity does
not depend on selecting a particular root.

For the supplied T point,

\[
\mathcal L(X)=72,\qquad
\mathcal L((X-72)^2)=\mathcal L(X^2)-5184<-353.
\]

The full exact rational values appear in `EXPECTED_RESULT.json` and
`EXPECTED_INDEPENDENT.json`. A separate physical edge-set decoder obtains
the same fractions. The implied two-by-two moment matrix

\[
\begin{pmatrix}1&72\\72&\mathcal L(X^2)\end{pmatrix}
\]

has negative determinant, so it cannot be positive semidefinite. This is an
exact certificate of missing global moment positivity, not a claim that a
real random variable has negative variance. The point's total
\(\sum_h\mathcal L(a(h)^2)=1576\) shows that G alone does not repair it.

For complete coefficient verification, the square is emitted as

\[
1596-97\sum_{e\in E\times H}x_e
+2\sum_{h\in H}\sum_{\{u,v\}\subset E}m_{uv,h}
+2\sum_{h\in E}\sum_{\{u,v\}\subset H}m_{uv,h}
+2\sum_{\substack{\{e,f\}\subset E\times H\\e\cap f=\varnothing}}
\mathcal L(x_ex_f)\ge0.
\tag{S'}
\]

Among the \(\binom{156}{2}=12,090\) edge pairs, 1,794 share a vertex
and 10,296 are disjoint. Replacing each shared red wedge by
\(m+x_e+x_f-1\) gives constant \(5184-2\cdot1794=1596\) and edge
coefficient \(1-144+2(12+11)=-97\). Disjoint edge products are sums of
four-state probabilities. The 5,148 two-E/two-H four-sets each supply
28 nonzero atom coefficients, giving 144,144 atom terms. With 1,794
wedges and 156 edges, S' has exactly **146,094 nonzero coefficients**.

`emit_square.py` constructs these coefficients by the closed cut formula.
`check.py` independently expands every unordered pair of the 156 edges,
compares every coefficient, and evaluates the emitted row exactly. Its
SHA-256 is
`f417545ff00195cf4da0a6ae22f2af7bb9984fc131c4a5bd7671e3cdfc5d0043`.
The large row file is generated only in scratch.

Since S is valid for every graph lift but violated by a fully checked T
point, it is not a linear consequence of T. The same point shows the stated
full LP cannot exclude the normalized M214 family. It says nothing about
Boolean realizability, the convex hull of physical Ramsey graphs, or
feasibility after all global moment-positivity constraints are added.

## Point representation and exact reproduction

The point selects \(y_{278}=1\), all other selectors zero, with descriptor
\((C77,12,0,BB)\) and anomalies 29 and 30. It uses the same nine classes as
h3599, all 345 four-class templates, and 4,165 positive canonical state
orbits. Its common denominator has 244 decimal digits. Missing orbit states
are zero. Edge bit orders are \((01,02,12)\) on triples and
\((01,02,03,12,13,23)\) on four-sets; class-preserving permutations
transport physical edges, not just state labels.

The complete 1,043,378-byte point is regenerated locally; its SHA-256 is
`3b16d19909a4a77c783a38ed264bead685f384c9a426dc3710b896a53309d815`.
The point, 511 MB inherited OPB, discovery model, solution, emitted square
row and logs are omitted from the public source package. The public producer
and compact exact expected outputs supply the complete regeneration route.
The hash alone is not mathematical evidence.

From a full repository checkout, with CPython 3.12.12 and its standard
library, plus SoPlex 8.0.3 on PATH (GMP 6.3.0, revision `13e2ab24`):

```sh
python3 -B ramsey_r55_m214_global_square_p4/reproduce.py /tmp/new-r55-global-square
(cd ramsey_r55_m214_global_square_p4 && shasum -a 256 -c SHA256SUMS)
```

Use a fresh scratch directory outside the source checkout. Allow several
minutes and approximately 2 GB scratch space. Expected status:
`EXACT_COMPLETE_GLOBAL_SQUARE_P4_SURVIVOR`, with all 25,377,663 rows
satisfied, G tight, cut mean 72 and cut square below −353.

The candidate producer uses the hash-pinned complete Q discovery builder,
then adds G. It has 8,558 variables and 19,632 discovery rows under the
candidate's nine-class symmetry and root-278 restriction. Some inherited
suffix rows are checked only in the subsequent full physical audit.
Infeasibility of the restricted discovery model could not exclude T.

SoPlex uses exact rational input/solve/check modes, zero feasibility and
optimality tolerances, internal presolve and equilibrium scaling. The
initial final solve took 30.21 seconds and 16,874 iterations. Solver status
and floating residuals are not proof evidence. The producer directly checks
every compressed rational row, then the separate physical checker validates
the entire unrestricted system on the decoded point. Different solver builds
may produce different bytes without implying infeasibility. SoPlex is needed
to regenerate the omitted point; checking an existing point is solver-free:

```sh
python3 -B ramsey_r55_m214_global_square_p4/check.py \
  --certificate /tmp/new-r55-global-square/certificate.json \
  --opb /tmp/new-r55-global-square/m214-3323.opb \
  --links /tmp/new-r55-global-square/anchor-links.opbpart \
  --forbidden /tmp/new-r55-global-square/forbidden.opbpart \
  --degree-separator /tmp/new-r55-global-square/degree-separator.opbpart \
  --deficiency-separator /tmp/new-r55-global-square/deficiency-separator.opbpart \
  --square /tmp/new-r55-global-square/square.opbpart
python3 -B ramsey_r55_m214_global_square_p4/independent_square.py \
  /tmp/new-r55-global-square/certificate.json
```

The old degree separator and global upper-bound row are now satisfied;
the new cut-square row is a diagnostic separator, not a row claimed to be
satisfied by T.

The full checker imports no producer, solver or predecessor executable.
It checks every inherited OPB row, every inactive-root suffix, every shared
physical triple marginal and footprint, every S/D3/T3/J1 row, all G
coefficients, and all 146,094 new square coefficients. The 44,343 semantic
source-row checks and inherited physical coverage remain intact.

Controls retain the previous transport and Boolean-identity audits and add
all 10,240 combinations of a two-by-three cut and a labeled graph on five
vertices, checking every emitted square coefficient against the literal
square. Thirty-two corruptions are rejected. Normal and optimized controls
match. The second scalar checker decodes canonical tables as edge sets and
uses direct red-edge products, rather than the main checker's blue-wedge
expansion. Its scope is the cut scalar, not a second implementation of the
entire LP. The fresh complete reproduction compares all expected output bytes.

## Bounded pentagon-count composition probe

The principal requested a bounded cold-profile or composition probe after
the current gate. The reviewed
[h3615 pentagon incidence theorem](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_pentagon_incidence)
and its [h3619 independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_global_pentagon_incidence_review1)
provide such a probe without repeating their structural proof.

`pentagon_projection.py` defines and checks the following complete **count
projection only**. Integer nonnegative histograms \(N_{c,q}\), for
\(q=0,\ldots,13\) and each color c, count same-color codegrees; integers
\(W_R,W_B,P\) count joined-edge pentagons by anchor color and pentagons.
For M214 the edge counts are 445 red and 458 blue, the triangle counts are
1,403 red and 1,463 blue, and the degree-square term is \(\sigma=13\).
Thus histogram totals are 445/458 and their q-weighted sums are 4209/4389.

Retain all histogram domains and these totals, the local bounds
\(W_c\ge\sum_qL(q)N_{c,q}\) with \(L(0..9)=0\) and
\(L(10..13)=(2,4,7,12)\), the trivial upper bounds
\(W_c\le\sum_q\binom q5N_{c,q}\), both color caps \(W_c\le26P\),
and the global inequalities

\[
903+3\sigma+\sum_{c,q}(L(q)-2(q-9))N_{c,q}
\le W_R+W_B\le52P.
\]

Also retain \(18\le P\le\binom{43}{5}\) and
\(W_R+W_B\le\binom{43}{7}\). No physical pentagon placements or shared
vertex constraints are part of this named projection.

An exact integer survivor has only

\[
N_{R,9}=241,\quad N_{R,10}=204,\quad
N_{B,9}=191,\quad N_{B,10}=267,
\]

\[
W_R=408,\qquad W_B=534,\qquad P=21.
\]

The correction term is zero and W=942. The projected minimum integer P is
exactly 21: the blue lower bound gives \(W_B\ge2(4389)-18(458)=534\),
while \(W_B\le26P\); the displayed witness attains the resulting integer
minimum. Twenty-one abstract pentagon records can also meet the separate
per-record incidence capacities, as checked in the script. These records
are not physical graphs or compatible placements.

This is a negative result for composition at that explicit aggregate level.
It is neither a model of the full h3615 graph domain nor a certified extension
of the P4 point by physical pentagons. No such realization or coupling is
claimed. The main T survivor and the count-projection survivor have separate
scopes. Six damaged aggregate inputs are rejected; expected output is
`EXACT_M214_PENTAGON_PROJECTION_SURVIVOR`.

## Literature, review boundary and next exact target

Primary literature was refreshed after graph selection:
[Angeltveit–McKay, R(5,5) at most 46](https://arxiv.org/abs/2409.15709),
Sherali–Adams (1990), DOI 10.1137/0403036, and the
[official SoPlex source](https://github.com/scipopt/soplex).
Nonnegative squares and positive semidefinite moment matrices are classical.
The campaign already has a different reviewed scalar PSD separator in the
M215 profile-B interface h3413/h3433. It is not the current complete M214
LP or a premise of this cut-square computation. No general-method or
historical-priority claim is made. The new evidence is the exact T survivor
and its explicit universal negative square.

The graph intake reached indexedHeight 3620 across signers and was refreshed
through 3624. H3613 accepts the predecessor, with independent new-row checks
and an inherited full replay. The principal report initially available had
cutoff 3596; its successor, read before publication, has cutoff 3624 and
explicitly retains the active Q+(G) decision. It also preserves a bounded
cold-M216 option after the active gates. The separate pentagon-count probe
answers the earlier composition advice, not that unperformed M216 option.
R2's h3607 equality boundary and r3's Albertson publication work have separate
domains. Their tasks are not reopened by this contribution.

This result is author-checked; external review is pending. The main checker
adapts the h3599 implementation; that reuse is disclosed. Literal rational
feasibility and nonnegative-square soundness require no Ramsey catalog or
trusted solver verdict. The M214 Ramsey interpretation retains the reviewed
root-cover, local-extrema and nine-exclusion imports. The separate pentagon
projection imports the reviewed h3615/h3619 bounds. Remaining trust is the
unformalized reductions and code, exact Python arithmetic, hash-pinned
production, SHA-256 and hardware. There is no proof-assistant formalization.

**Next falsifiable milestone:** decide the complete T with the entire
44-by-44 moment matrix of \((1,a(0),\ldots,a(42))\) positive semidefinite.
Every matrix entry uses existing P4 coordinates. This is the complete family
\(\mathcal L((b+\sum_hc_ha(h))^2)\ge0\) for all coefficients, containing
the cut separator here. Require an exact full-system survivor with a checked
rational PSD certificate, or a checkable infeasibility certificate with
unrestricted coverage. Refresh the graph and principal advice first; do not
restart a cut-by-cut ladder or infer full infeasibility from a symmetric
root-278 restriction.

All Boolean completions, the 380 remaining descriptors, every whole M-slice,
adjacent M215–220 slices and the low-deficiency branch remain undecided here.
Two consecutive incremental-only passes without a strict separator, complete
survivor or complete-family effect trigger a pivot to the next principal-ranked
exact target. This pass provides both a complete survivor and a global strict
separator, plus the separately scoped bounded composition probe.
