# An exact selector family survives the nine M214 cuts

The complete four-vertex moment LP at Discovery Net height 3423 remains
feasible after all nine known selector exclusions. We give a compact exact
rational point and determine its entire selector fiber. With its physical
moments fixed, any set of selector exclusions leaves a feasible point if
and only if at least three selectors remain available.

This identifies a weakness of the guarded selector formulation. Every
point in this family violates a common anchor edge unit. A compact rank-one
Chvátal–Gomory certificate derives that unit from the original formulation.
We also give and check all 83 equations for the exact convex hull of the
anchor-unit/selector interface. They exclude the entire new family. The
complete LP with these 83 equations is **undecided**.

These are fractional pseudomodels, not Ramsey graphs or feasible Boolean
roots. No additional Boolean root, entire M-slice, adjacent slice, or
Ramsey bound is decided here.

## Exact domain

Let \(P_4\) be the [complete height-3423 formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_four_vertex_moments),
artifact `bafkreigvxxxxmc3jecxijw7nk3ph72q6mwbu7tneart7b7mxrltgn5ooxi`.
It retains the complete height-3323 OPB, all height-3341 and height-3367
suffixes, and the height-3401 complete triangle, degree-star and codegree
rows. It then joins the 64-state probability hull on every physical
four-vertex set, sharing every triple marginal and all existing
five-edge footprint coordinates.

All inherited variables, including the 389 selectors, have domain
\([0,1]\). Selecting root 48 and the special blue-defect vertex in the
previous certificate were properties of that witness, not additional
equations defining \(P_4\). No original row or domain is removed here.
This remains the old red-only M214 cover, without conjoining newer
two-color covers or unlisted cuts.

Using zero-based root indices, impose

\[
Z=\{48,128,129,201,202,299,300,375,376\},\qquad y_r=0\quad(r\in Z).
\]

The presentation writes each cut as \(-y_r\geq0\), since selector
nonnegativity is already present. The complete \(c=13,k=0\) exclusion is
[height 3485](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_c13_k0_weighted_cell_exclusion),
independently accepted at height 3521, with corrected review text at
height 3523. Root 375 was already excluded at
3445, reviewed at 3453; root 376 has the earlier exclusion at 3465,
reviewed at 3479. Those mathematical reductions retain their explicit
catalog-completeness premise. Literal feasibility of the stated LP with
these zero coordinates does not require trusting the exclusions.

| System | Variables | Rows | Equalities |
| --- | ---: | ---: | ---: |
| Complete \(P_4\) | 8,023,409 | 15,416,948 | 4,148,936 |
| \(P_4\) plus nine cuts | 8,023,409 | 15,416,957 | 4,148,936 |
| Plus the 83 anchor equations below | 8,023,409 | 15,417,040 | 4,149,019 |

These are presentation counts, including redundant rows. The last system
is a concrete next target, not a claimed feasible or infeasible system.

## Five exact probability tables

Partition the physical vertices into
\(E=\{2,\ldots,14\}\) and \(C=\{0,1,15,\ldots,42\}\), of sizes 13 and
30. These classes encode this candidate, not a symmetry assumption on all
graphs. Edge probabilities depend only on the endpoint classes:

\[
a=p_{EE}=\frac{20}{39},\qquad
b=p_{EC}=\frac6{13},\qquad
c=p_{CC}=\frac{15}{29}.
\]

Let \(J_{H;s}\) be the probability of two red edges with center class
\(H\in\{E,C\}\) and \(s\) exceptional leaves. Use

\[
u=\frac{2229}{10000},\quad v=\frac{2161}{10000},\quad
t_1=\frac{1031}{10000},\quad t_2=\frac{1041}{10000},
\]

\[
J_{E;2}=\frac{19a-30u}{11},\quad J_{E;1}=u,\quad
J_{E;0}=\frac{19b-12u}{29},
\]

\[
J_{C;2}=\frac{20b-29v}{12},\quad J_{C;1}=v,\quad
J_{C;0}=\frac{20c-13v}{28}.
\]

Here \(t_q\) is the red triangle probability when exactly \(q\) of
its vertices are in \(E\). Complete the two free values by

\[
t_3=\frac{93-360t_2-435t_1}{66},\qquad
t_0=\frac{100-78t_2-377t_1}{406}.
\]

The wedge formulas solve all degree-star equalities. The triangle
formulas give red local triangle totals 93 on \(E\) and 100 on \(C\).
Red degrees are respectively 20 and 21. The checked blue local totals
are \(1389/13\) and 100; red and blue deficiency sums remain 301 and 303.

For four vertices, order the six edge bits as
\((01,02,03,12,13,23)\). Define Walsh coefficients by

\[
\widehat p(\varnothing)=1,\qquad \widehat p(\{e\})=1-2p_e,
\]

\[
\widehat p(\{e,f\})=1-2p_e-2p_f+4J_{H;s}
\quad\text{when }e,f\text{ meet},
\]

\[
\widehat p(T)=1-2\sum_{e\in T}p_e+4\sum_{h\in V(T)}J_h-8t_q
\quad\text{when }T\text{ is a triangle}.
\]

Set all other coefficients to zero, including disjoint edge pairs.
There are 23 specified coefficients. Walsh inversion gives the masses

\[
p(s)=\frac1{64}\sum_T\widehat p(T)(-1)^{|s\cap T|}.
\]

`construct.py` uses only the four fractions in `parameters.json` to
produce the five tables, indexed by the number of exceptional vertices
and written in exceptional-first order. Positivity is checked exactly;
the minimum of all 320 masses is \(226211/60320000>0\).

The 6,178-byte `certificate.json` contains their integer numerators at
common denominator \(D=2533440000\). Its SHA-256 is
`6da7466019c96be2af879b98bc7164a5208479cb8921f8c00c91e0bd2809e231`.
The checker transports the tables to every physical labeling and
recovers edges, red triangles, blue wedges and five-edge footprints by
their probability definitions. The old point and its averaging were
discovery aids; neither is a proof input for this certificate.

## The entire selector fiber

With these physical moments fixed, the exact set of selector values
allowed by \(P_4\) is

\[
\mathcal Y=\left\{y:\ 0\leq y_r\leq\frac6{13}\ (0\leq r<389),
\quad\sum_{r=0}^{388}y_r=1\right\}.
\]

Necessity: every root has the physical guarded unit
\(x_{0,2}-y_r\geq0\), and this point has \(x_{0,2}=6/13\).
Nonnegativity and the selector-sum equality are original constraints.

Sufficiency: the checker evaluates each base inequality over the entire
independent box \([0,6/13]^{389}\), by minimizing each selector term at
the appropriate endpoint. Every minimum is nonnegative. Every base
equality without selectors holds exactly; the sole equality containing
selectors is verified as precisely \(\sum_r y_r=1\). All root-dependent
suffix inequalities hold over that same box, and all remaining P3/P4
constraints are checked on the fixed physical moments. Thus no omitted
selector coupling can narrow the displayed fiber.

For the nine cuts, choose \(y_r=1/380\) for \(r\notin Z\), and zero
otherwise. A common denominator for the full point is 48,135,360,000.
More generally, if a set of zero cuts leaves \(m\) coordinates available,
this fixed-moment family survives exactly when \(m\geq3\):
\(2(6/13)<1\), whereas uniform mass \(1/m\leq1/3<6/13\) works for
every \(m\geq3\). Hence selector zero cuts alone cannot exclude the
complete LP while at least three roots remain. With fewer roots, this
family fails; feasibility of different physical moments is not decided.

## A checked integer separator and the complete anchor interface

Sum all 389 guards \(x_{0,2}-y_r\geq0\) with multiplier \(1/389\),
then add the equality \(\sum_r y_r=1\) with multiplier \(1/389\).
This gives

\[
x_{0,2}\geq\frac1{389}.
\]

The remaining coefficient is integral. Since \(x_{0,2}\) is Boolean
in the original problem, one Chvátal–Gomory rounding gives

\[
x_{0,2}\geq1.
\]

`anchor_cg.json` records the exact multipliers, canceled coefficients
and rounded right side. The checker audits the 389 physical premises
in the complete OPB and verifies the arithmetic. Every member of the
new fiber violates the rounded inequality by \(7/13\). The rounding
step is essential: this is not a Farkas implication from the continuous
LP, which the new point satisfies.

For a fuller repair, let \(A\) be the 83 edges incident to anchors 0
or 1, and let \(b_{r,e}\in\{0,1\}\) be the unit fixed by root \(r\).
Add all equations

\[
x_e=\sum_{r=0}^{388}b_{r,e}y_r\qquad(e\in A).
\]

Together with the selector simplex, these describe exactly the convex
hull of the 389 pairs consisting of a root's anchor pattern and its
one-hot selector vector: every feasible point is explicitly their
convex combination, and conversely each combination satisfies the
equations. Setting the nine selectors to zero restricts the hull to the
380 retained labels. This is an exact hull of the anchor interface,
not of the complete root polytopes.

These equations imply the old guarded anchor units. All 389 roots have
51 common anchor units; after the cuts there are 53. The new family
violates all 53 common units, and its uniform-selector representative
violates all 83 equations. `emit_links.py` emits the equations from the
hash-pinned parent producer. Independently, `check.py` reconstructs and
audits all 32,287 physical root units and every coefficient of the
emitted 83 rows. The emitted file SHA-256 is
`f2bef9213e141982f863601df3dc57d07ee20b1d5f0b9bcb559799a2187bafa1`.

## Reproduction and trust boundary

From a complete checkout of this repository, with Python 3.10 or newer
and its standard library (tested on CPython 3.12), use a new scratch
directory outside the source checkout:

```sh
python3 -B ramsey_r55_m214_postcut_selector_fiber/reproduce.py /tmp/new-r55-selector-check
(cd ramsey_r55_m214_postcut_selector_fiber && shasum -a 256 -c SHA256SUMS)
```

Allow several minutes and roughly 2 GB of scratch space. No solver,
private data, downloaded catalog, or omitted proof file is required.
The command reconstructs the compact tables and anchor equations,
checks controls, regenerates the complete inherited base through five
hash-pinned public builders, checks the full stated system, and compares
the exact output with `EXPECTED_RESULT.json`. Intermediate parent OPBs
are deleted during regeneration. Formulas and logs stay outside Git.

The retained OPB has 2,983,003 rows, 87 equalities, and 511,537,255 bytes;
its SHA-256 is
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`.
Every literal row is parsed and checked, including all selectors.
The remaining rows are checked directly from their complete physical
definitions: 903 red codegrees, 21,762 coupled columns, 264,560 hull
facets, 98,728 triangle-atom inequalities, 1,806 degree-star equalities,
903 blue codegrees, and every P4 row. The last layer includes all
123,410 physical four-sets, 7,898,240 nonnegative masses, 3,949,120
triple-marginal equalities and 74,513 footprint identifications.

The compact expected status is
`EXACT_COMPLETE_P4_POSTCUT_SURVIVOR_AND_SELECTOR_FIBER`, with selector
cap `6/13`, minimum retained roots `3`, 83 checked anchor equations and
rank-one CG separation gap `7/13`. Controls exhaust 24,576 physical
four-state transports and reject 18 corruptions, including damaged
probabilities, coordinates, base rows, anchor links and CG multipliers.
The fresh full replay passed. Normal and optimized full checks and
controls produced byte-identical results; checks do not depend on Python
assertions.

The new checker imports no producer, solver, or old checker. It is
author-written, with the inherited formula and mathematical definitions
reused explicitly. Exact computation remains conditional on this
unformalized decoder/checker, CPython, SHA-256 and ordinary hardware.
The published proof is not an external review. The Ramsey meaning of
the inherited reduction and imported cuts retains its reviewed
local-extrema/catalog boundary; the literal rational feasibility and
integer rounding arithmetic can be checked without that catalog.

Primary literature was checked after graph-grounded target selection:
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2),
[McKay's Ramsey catalog page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
[Balas's disjunctive-programming treatment](https://link.springer.com/book/10.1007/978-3-030-00148-3),
and [Chvátal's publication list](https://users.encs.concordia.ca/~chvatal/publ.html).
No priority is claimed for symmetry averaging, Walsh inversion,
selector convex hulls or integer rounding. The contribution is the
exact full-system certificate and quantified selector failure here.

## Next falsifiable milestone

Decide the complete \(P_4\) plus the nine cuts and all 83 anchor
equations by an exact full-system survivor or independently checkable
infeasibility certificate, after refreshing the live graph and principal
strategy. The current family is rigorously excluded by that interface;
feasibility of the strengthened system remains open. Do not automatically
increase moment order. Two consecutive passes yielding only incremental
rows, without a strict family separator, full-system survivor or
complete-family effect, trigger a pivot to the next principal-ranked
exact target.
