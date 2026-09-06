# Complete four-vertex moments still admit the M214 relaxation

The full height-3401 \(M=214\) LP remains feasible after adjoining the
complete 64-state probability hull on **every** four-vertex set and
identifying all its triangle and existing five-edge footprint moments.
An exact rational point selects the inherited root 48 and has
\(\rho=3/14\), common-core aggregate \(S=5\), \(Q=117/7\), and red/blue
deficiency expectations summing to 301 and 303.

The entire preceding affine survivor family,
\(3/14\leq\rho\leq10/39\), has no lift to the new system. Thus this is
both a strict separator against the complete preceding relaxation and
an exact admissible survivor of the strengthened relaxation. No LP/Farkas
infeasibility certificate can exist for this stated strengthened system.

These are fractional pseudomodels. No Boolean root, complete M-slice,
order-43 Ramsey family, or Ramsey bound is decided. The new certificate
establishes one point; it does not establish the preceding interval for
the stronger lift.

## Precisely defined relaxation

Let \(P_3\) denote the complete LP stated at Discovery Net height 3401,
artifact `bafkreigjt2tptaqahfr6ufwuzskaubsr3nire65j4fyyssh55vutqcmlvu`.
It retains the entire height-3323 formula, every root-dependent suffix
from heights 3341 and 3367, all complete triangle probabilities, all
incident degree-star equalities, and both colors' codegree caps. It has
125,169 coordinates, 3,371,665 rows, and 1,893 equalities. Its 389-root
red-only selector and original labels are retained throughout. The newer
M215 two-color selector is not conjoined to it.

Physical vertices are \(0,\ldots,42\). The red edge bit is \(x_{uv}\).
The inherited coordinates have Boolean meanings

\[
z_{abc}=x_{ab}x_{ac}x_{bc},\qquad
m_{ab,h}=(1-x_{ah})(1-x_{bh}),
\]

\[
q_{ab,ij}=x_{ij}(1-x_{ai})(1-x_{bi})(1-x_{aj})(1-x_{bj}).
\]

All 37,023 centered wedge coordinates are present in \(P_3\), along
with all 12,341 red triangles and the inherited union of 74,513 footprints.
The pinned physical decoder reconstructs each coordinate's actual labels.

Define \(P_4\) by retaining **every row and domain of \(P_3\)**. For each
of the \(\binom{43}{4}=123,410\) ordered-by-label sets \(A\), introduce
64 masses \(p_{A,s}\), indexed by the six bits in lexicographic unordered
edge order. Require

\[
p_{A,s}\geq0,\qquad \sum_{s=0}^{63}p_{A,s}=1.
\]

For each of its four triples \(T\subset A\), identify all eight marginal
masses with the already shared three-edge atom masses of \(P_3\).
For every existing footprint whose four labels form \(A\), identify
\(q_{ab,ij}\) with the sum of the two states having \(ij\) red and
\(ai,bi,aj,bj\) blue; the edge \(ab\) is free.

The explicit presentation adds 7,898,240 coordinates, 7,898,240
nonnegativity rows, 123,410 normalizations, 3,949,120 triangle-marginal
equalities, and 74,513 footprint equalities. Including all inherited
rows, it has 8,023,409 coordinates, 15,416,948 rows, and 4,148,936
equalities. Redundant equations are retained in these counts. The upper
bound on each new mass follows from nonnegativity and normalization.

This is the complete four-vertex marginal hull joined to the stated
predecessor. It is not claimed to be a full Sherali--Adams level: products
of all global rows, five-vertex joint distributions, and other global
moment constraints have not been silently imposed.

## Soundness and exact local meaning

Every Boolean assignment satisfying the predecessor's intended graph
conditions lifts by assigning mass one to its actual six-edge state on
each four-set. Its triple marginals and footprint products then agree
identically. Thus the new rows are necessary without choosing a core,
selector, symmetry, or catalog beyond the predecessor's stated premises.

Conversely, on one four-set the displayed masses describe exactly the
convex hull of all 64 six-edge assignments. The equalities identify the
specified overlapping moments exactly. Local distributions on different
four-sets need not extend to one distribution on all 903 edge bits. That
missing global extension is part of the remaining gap, not a claim of
this certificate.

For clarity, on a triple \(a<b<c\), put
\(A=x_{ab},B=x_{ac},C=x_{bc}\), and

\[
u=m_{bc,a}+A+B-1,\quad
v=m_{ac,b}+A+C-1,\quad
w=m_{ab,c}+B+C-1.
\]

Its eight atom masses, in bit order \((A,B,C)\), are

\[
(1-A-B-C+u+v+w-z,\ A-u-v+z,\ B-u-w+z,\ u-z,
 C-v-w+z,\ v-z,\ w-z,\ z).
\]

The physical checker compares every four-set marginal to these formulas
using the edge, wedge, and triangle entries of the submitted full point.

## Strict separator of the entire preceding family

For distinct \(a,b,i,j\), let

\[
t_a=\Pr(x_{ij}=1,x_{ai}=x_{aj}=0),\qquad
t_b=\Pr(x_{ij}=1,x_{bi}=x_{bj}=0).
\]

These are already determined by the triple atoms. Every four-set
probability distribution satisfies

\[
\max(0,t_a+t_b-x_{ij})\leq q_{ab,ij}\leq\min(t_a,t_b).
\]

Indeed, the footprint is the intersection of these two events, both
contained in \(\{x_{ij}=1\}\). These classical conditional Fréchet bounds
are projections of \(P_4\), without any activation guard.

For the height-3401 family take \((a,b,i,j)=(2,30,15,16)\). Its fixed
triangle moments give

\[
x_{15,16}=1,\qquad t_{30}=\frac{6059}{141960},\qquad
q_{2,30;15,16}=\frac{14}{65}\rho.
\]

At the two endpoints the slack \(t_{30}-q\) is respectively

\[
-\frac{493}{141960},\qquad-\frac{137}{10920}.
\]

It is affine and strictly negative throughout the interval. Hence **no
member of the complete old affine family has any extension to \(P_4\)**.
Each endpoint has 32,437 existing footprints violating at least one of
the two upper bounds; this is a count of footprints, not separate rows.
The old points are verified against their entire named relaxation during
reproduction, not asserted feasible merely from the separator projection.

## Compact exact survivor and physical audit

`certificate.json` has 463 sparse six-edge probability templates and
4,371 nonzero template entries. All masses are integer multiples of

\[
1/D,\qquad D=11924982161809860064545376979382249165566676000.
\]

The certificate is 267,041 bytes, SHA-256
`3f3fe88ace02db3797d352e4766f807fd82adb3e72658e37e6d9e532e786ef0f`.
The expected-result SHA-256 is
`8b4b9409bc67eb4418d7929417725f3eda7be2d4d91552db37e4019197a73071`. Its key uses inherited vertex types and
fixed rational edge values. These are a compression scheme for this
one candidate, not a classification of Ramsey graphs or a global
symmetry assumption. All 123,410 physical four-sets are expanded and
checked, including every tie and every overlap.

`witness.py` inherits only fixed edge and selector values from the
hash-pinned predecessor producer. It overwrites every triangle, wedge,
and footprint coordinate using the new physical distributions. Each
four-set is written in physical label order as a sparse 64-state record.
The full expansion contains 1,903,846 nonzero masses.

`validate.py` imports neither the new producer, its template table, the
discovery LP, nor a solver. It consumes the expanded physical stream and
full point, checks nonnegativity and normalization, all four triangle
marginals for every set, every inherited footprint identification, and
all 3,371,665 predecessor rows. It uses integers at common scale \(D\),
plus exact `Fraction` parsing. Missing, duplicated, reordered, or extra
physical sets cannot be skipped.

The old 511,537,255-byte OPB is regenerated from public predecessor
source and identified by SHA-256
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`.
Every one of its 2,983,003 rows is evaluated. The remaining inherited
root-dependent rows are evaluated on all 389 physical root descriptions;
none is discarded because the certificate selects root 48.

The selected 13-vertex core, fixed edge values, and \(\rho=3/14\) are
choices of the **fractional witness**, not restrictions on the entire
relaxation or unproved assumptions about every graph in the branch.
The selected-core moments remain \(S=5,Q=117/7\). The old exact
blue-pair lower row is tight at this value. No interval or optimality
claim for \(P_4\) is made.

## Reproduction

From a complete checkout of the public repository, with Python 3.11 or
newer and its standard library (tested on CPython 3.12.12):

```sh
python3 -B ramsey_r55_m214_complete_four_vertex_moments/reproduce.py /tmp/new-r55-four-check
```

Use a new directory outside the source repository. The command reproduces
and checks the predecessor, runs the controls, expands the new certificate,
checks every old and new row, and compares the exact output with
`EXPECTED_RESULT.json`. Allow several minutes and a few GB of scratch
space for the inherited formulas and physical streams. No solver,
private input, omitted dataset, or downloaded certificate is required.

Expected status: `EXACT_COMPLETE_FOUR_VERTEX_LP_SURVIVOR`, with 123,410
four-sets, all 74,513 footprint equalities, and the two strict slacks above.
Expanded formulas, 90 MiB physical streams, vectors, logs and solver
outputs remain outside Git. All are reproducible from the compact source.

Additional controls and manifest check:

```sh
python3 -B ramsey_r55_m214_complete_four_vertex_moments/test_validate.py
python3 -O -B ramsey_r55_m214_complete_four_vertex_moments/test_validate.py
(cd ramsey_r55_m214_complete_four_vertex_moments && shasum -a 256 -c SHA256SUMS)
```

The controls cover 192 distributions, 768 triangle projections, 1,152
footprint events, 4,608 physical transports, the complete 384-instance
Boolean separator truth table, and rejection of ten malformed streams.
Normal and optimized modes agree. A fresh full recursive replay completed
in 274.863 seconds, exit zero, matching the expected result. Normal and
optimized producers emitted byte-identical full points, wedge files and
physical four-set streams.

## Optional discovery and provenance

`derive.py` creates a 31,000-variable, 19,659-row template search LP.
It fixes the inherited edge pattern and active footprints at \(\rho=3/14\),
retains the prior triangle/star discovery constraints, and couples all
four-set template marginals. It is only a witness-discovery restriction;
its feasibility or infeasibility alone says nothing about the complete
Ramsey branch. The physical full-relaxation checker is the evidence gate.

The published point was found with SoPlex 8.0.3, GMP 6.3.0, git revision
`13e2ab24`. Exact rational factorization produced the candidate; every
rational row and box was then independently evaluated by `Fraction`.
The discovery solve took 34.77 seconds on the production host.

```sh
python3 -B ramsey_r55_m214_complete_four_vertex_moments/derive.py --lp /tmp/four.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 \
  --int:ratfac_minstalls=0 --bool:ratfacjump=true \
  --real:feastol=1e-30 --real:opttol=1e-30 --real:fpfeastol=1e-30 \
  -s0 -g0 -v3 -t180 -X=/tmp/four.sol /tmp/four.lp
python3 -B ramsey_r55_m214_complete_four_vertex_moments/derive.py \
  --solution /tmp/four.sol --output /tmp/certificate.json
```

A different solve may choose a different rational table. Solver status,
time limits, floating tolerances and agreement between solvers are not
proof inputs to the published replay.

The producer, decoder, base OPB parser, star checker and part of the
discovery generator explicitly reuse author code from
[height-3401 source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_global_star_moments),
source commit `9a139b116fe5e03a66e493e18e37bf807cc81251`, and its pinned
predecessors. The generic old suffix audit removes only witness-specific
endpoint assertions, retaining every mathematical row. This is not a
new independent decoder or an external peer review.

Primary literature was checked live after the graph-grounded target was
selected: [Angeltveit--McKay](https://arxiv.org/html/2409.15709v2) for
Ramsey LP and gluing context, and
[Sherali--Adams--Driscoll](https://pubsonline.informs.org/doi/10.1287/opre.46.3.396)
for established Boolean-product relaxation methods. No historical
priority for marginal hulls, Fréchet bounds or degree products is claimed.

## Evidence boundary and next gate

Evidence: an exact rational full-relaxation survivor and a strict
projection separating the complete preceding affine family. Checked by
author-written integer/rational code; no external review or formalization
of this new result is claimed. Mathematical soundness of the inherited
Ramsey reduction retains its reviewed local-extrema/catalog boundary.
Trust includes those premises, the displayed unformalized proof, reused
and new checker code, CPython, SHA-256 and ordinary hardware.

Covered: all rows of the specified 389-root \(P_3\) and its complete
four-vertex marginal extension, with an explicit surviving point.
Uncovered: Boolean feasibility of any root, whole \(M=214\), adjacent
M-slices, low deficiency, and order-43 Ramsey existence.

Next falsifiable milestone: a proof-producing decision of one complete
Boolean M214 marked root, retaining its full variable core, every physical
edge and all inherited constraints. UNKNOWN, partial traces, or an
unforced fixed core do not qualify. The principal's updated report of
14:36 UTC recommends this pivot if the completed four-support layer
survives. This certificate meets that condition; the next pass should
move to the Boolean target after a fresh graph inspection. This is a
portfolio stopping decision, not a theorem that higher moments are
exhausted. The general two incremental-only-pass fallback remains in force
if the replacement mechanism fails to produce substantive progress.
