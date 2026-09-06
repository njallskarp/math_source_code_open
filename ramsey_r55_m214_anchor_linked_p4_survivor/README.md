# An exact P4 survivor with all anchor links and an integral selector

The complete M214 four-vertex moment LP remains feasible after the nine
selector exclusions and all 83 anchor equations. The exact fractional
moment point here has **one selector equal to one**, choosing zero-based
root 278, \((C77,12,0,BB)\). Every other selector is zero.

Thus the remaining obstruction at this point is not fractional activation
of the 389 root labels. Even the convex hull of the existing continuous
root LPs contains this point. Boolean feasibility of root 278 remains
open; this is not a Ramsey graph or a new Boolean exclusion.

We identify a strict strengthening at the same moment order: all 11,970
monochromatic-four masses forbidden in the two neighborhoods of canonical
anchor 0 must vanish. The certified point violates 3,813 of those rows.
One violated blue mass exceeds \(11/100\). The complete LP after adjoining
these rows is **undecided**.

## Precisely stated systems

Let \(P_4\) denote the complete formulation at Discovery Net height 3423,
[public definition and original certificate](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_four_vertex_moments),
artifact `bafkreigvxxxxmc3jecxijw7nk3ph72q6mwbu7tneart7b7mxrltgn5ooxi`.
It retains the full height-3323 OPB, every height-3341/3367 suffix, all
height-3401 triangle/star/codegree constraints, and all four-vertex
probability hulls with shared triples and existing footprints. No original
row or domain is removed. Its 389 labels remain the original red-only
M214 cover; unrelated newer covers and cuts are not silently conjoined.

As in [height 3531](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_postcut_selector_fiber),
impose the nine zero-based exclusions

\[
Z=\{48,128,129,201,202,299,300,375,376\},\qquad y_r=0\quad(r\in Z),
\]

and all 83 equations

\[
x_e=\sum_{r=0}^{388}b_{r,e}y_r
\qquad(e\text{ incident to anchor }0\text{ or }1),
\]

where \(b_{r,e}\) is the anchor bit specified by root \(r\). Call the
resulting complete LP \(L\). All inherited coordinates have domain
\([0,1]\); the new four-state masses are nonnegative and normalized.
The old root-48 witness convention is not a restriction on \(P_4\).

| Presentation | Variables | Rows | Equalities |
| --- | ---: | ---: | ---: |
| Complete \(P_4\) | 8,023,409 | 15,416,948 | 4,148,936 |
| \(L=P_4+9+83\) | 8,023,409 | 15,417,040 | 4,149,019 |
| \(L\) plus all new forbidden-state rows | 8,023,409 | 15,429,010 | 4,149,019 |

Counts include redundant equations. Zero cuts are written as inequalities
\(-v\geq0\), using the existing nonnegativity domain. The last system
is the next falsifiable target, not a claimed infeasible system.

## Exact physical point

The certificate uses these nine classes solely to compress this candidate:

\[
\{0\},\ \{1\},\ \{2,\ldots,7\},\ \{8,\ldots,13\},\ \{14\},
\]

\[
\{15,\ldots,26\},\ \{27,28\},\ \{29,30\},\ \{31,\ldots,42\}.
\]

They encode the \(c=12,k=0\) anchor pattern. The selected root is
\((C77,12,0,BB)\): its two anomalous vertices are 29 and 30. The
certificate sets \(y_{278}=1\) and every other selector to zero, so it
satisfies all nine cuts and the complete anchor equations exactly.

There are 345 feasible four-class multisets. For each, `certificate.json`
records positive masses on canonical six-edge state orbits under
permutations within equal classes. It contains 3,076 orbit entries,
expanding to 4,699 nonzero state entries across the 345 templates.
Missing states have mass zero. Edge-bit order is
\((01,02,03,12,13,23)\); state 0 is all blue and state 63 all red.
Classes are placed in increasing class order before physical transport.
All probabilities are integer multiples of

\[
1/D,\quad
D=125368991767988746642012018235328661030993837537249251106759096554753901781865052800.
\]

The 281,881-byte certificate has SHA-256
`576f7675a093293dcfb8f03f4bf11540ecfacb485b21d608844d29183e734715`.
This is a compact exact primal certificate; no solver or external catalog
is needed to check it.

The checker expands every physical four-set, decodes all 903 edges,
12,341 red triangles, 37,023 blue centered wedges, and 74,513 existing
five-edge footprints from their probability definitions. The 26,411 newer
wedge coordinates are included. Every four-set shares its four full
three-edge marginal distributions with the same physical triple moments.
Every existing footprint equals its precise two-state event probability.

Red degrees are 20 on \(E=\{2,\ldots,14\}\) and 21 elsewhere. Red
triangle totals are respectively 93 and 100. Blue triangle totals are 107
on \(E\), 99 at 29 and 30, and 100 at every other vertex. Equivalently,
all red deficiencies are seven; all blue deficiencies are seven except
eight at 29 and 30. Their sums remain 301 and 303. The exceptional-neighbor
counts are six everywhere except seven at 29 and 30, as the selected root
requires. These are moments, not literal graph triangle counts.

## What the one-hot survivor rules out

For each retained root, define

\[
Q_r=\{(x,z,m,q,p,y)\in L:y_r=1\}.
\]

Selector nonnegativity and their sum-one equation force all other
selectors to zero in \(Q_r\). The exact certificate lies in
\(Q_{278}\). Therefore

\[
\operatorname{conv}\left(\bigcup_{r\notin Z}Q_r\right)\ne\varnothing.
\]

More specifically, that convex hull still contains this very point.
Hence further convexification of **these existing continuous root LPs**
cannot yield a contradiction or remove the point. This does not concern
the convex hull of Boolean Ramsey graphs, stronger root systems, or new
disjunctions on physical edge assignments. It identifies a precise limit
of selector repair with the current row library.

The full decoder and row audit matter: merely finding a feasible symmetric
search LP would not prove the displayed containment.

## A complete forbidden-state strengthening at the same moment order

All 389 normalized roots have the same anchor-zero star. Its two
21-vertex neighborhoods are

\[
N_R(0)=\{1,\ldots,7\}\cup\{15,\ldots,28\},
\qquad
N_B(0)=\{8,\ldots,14\}\cup\{29,\ldots,42\}.
\]

This is checked against every physical root unit. The 83 anchor equations
and selector simplex fix these 42 edge values even when selectors are
fractional.

For every four-set \(A\subset N_R(0)\), an all-red state on \(A\)
together with vertex 0 would form a red \(K_5\). Similarly, an all-blue
state on \(A\subset N_B(0)\) would form a blue \(K_5\). Every canonical
Ramsey graph, and every convex combination of their moment lifts, satisfies

\[
p_{A,63}=0\quad(A\in\tbinom{N_R(0)}4),\qquad
p_{A,0}=0\quad(A\in\tbinom{N_B(0)}4).
\]

These are \(2\binom{21}{4}=11,970\) rows, using only existing P4
coordinates. They complete exactly this anchor-zero neighborhood family;
no claim is made to complete all five-vertex moment consistency.

`emit_forbidden.py` emits the full family by enumerating physical
four-sets. The independent checker derives the star from all 389 roots,
uses a combinatorial subset-rank formula to reconstruct every emitted
variable, and audits all 11,970 corresponding original five-set clauses
inside the retained OPB. Together with the 32,287 audited anchor units,
this checks 44,257 source rows semantically, as well as checking every
base row for feasibility. The 2,048-case Boolean control verifies the
underlying fixed-star/five-clause implication in both colors.

The new point has 3,813 positive forbidden blue masses and zero positive
forbidden red masses for anchor 0. In particular,

\[
p_{\{39,40,41,42\},0}=
\frac{652999482457240645298711994224426575470284590794411979469915505515258922049561}
{5936031807196436867519508439172758571543268822786422874373063283842514288914065}
>\frac{11}{100}.
\]

Thus even one of the new zero rows is a strict separator of a certified
point of the complete \(L\). The emitted family SHA-256 is
`5c1a658ea797e95ab7cb9076373bd6f055220a923c445c00ac38854210f44318`.
The new rows follow from the Boolean graph interpretation; they are not
Farkas consequences of \(L\), which this exact point satisfies.

## Full verification and reproduction

From a complete checkout of this repository, with Python 3.10 or newer
and its standard library (tested on CPython 3.12), use a fresh directory
outside the source checkout:

```sh
python3 -B ramsey_r55_m214_anchor_linked_p4_survivor/reproduce.py /tmp/new-r55-linked-check
(cd ramsey_r55_m214_anchor_linked_p4_survivor && shasum -a 256 -c SHA256SUMS)
```

Allow several minutes and roughly 2 GB scratch space. The command emits
and checks the 83 anchor equations and 11,970 next-target rows, runs the
controls, regenerates the complete inherited OPB from five hash-pinned
public builders, checks the provided exact point, and byte-compares the
result with `EXPECTED_RESULT.json`. The next-target rows are checked for
physical validity and separation; they are not falsely reported as
satisfied by the point. Generated formulas and logs stay outside Git.

Expected status:
`EXACT_COMPLETE_ANCHOR_LINKED_P4_INTEGRAL_SELECTOR_SURVIVOR`,
with root 278 alone selected, 15,417,040 checked rows, 44,257 semantic
source rows, and 3,813 violated new blue-forbidden states. Controls check
529,920 physical state transports, 2,048 Boolean implication cases and
21 rejected corruptions. The fresh full reproduction passed. Normal and assertion-disabled full
checks and controls produced byte-identical results; checks remain active
with Python assertions disabled.

The retained OPB has 98,758 variables, 2,983,003 rows, 87 equalities and
511,537,255 bytes; SHA-256
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`.
Every literal row is evaluated with integers at common scale \(D\).
The checker also evaluates all 903 red codegrees, 21,762 coupled columns,
264,560 moment-hull facets, 98,728 triangle-atom inequalities, 1,806
star equalities, 903 blue codegrees, and every four-state row. That last
layer includes all 123,410 physical four-sets, 7,898,240 nonnegative
masses, 3,949,120 triangle-marginal equations and 74,513 footprint
identifications. No selector-inactive suffix is skipped.

Additional assertion-disabled replay against regenerated files:

```sh
python3 -O -B ramsey_r55_m214_anchor_linked_p4_survivor/check.py --opb /tmp/new-r55-linked-check/m214-3323.opb --links /tmp/new-r55-linked-check/anchor-links.opbpart --forbidden /tmp/new-r55-linked-check/forbidden.opbpart
python3 -O -B ramsey_r55_m214_anchor_linked_p4_survivor/controls.py --links /tmp/new-r55-linked-check/anchor-links.opbpart --forbidden /tmp/new-r55-linked-check/forbidden.opbpart
```

## Optional discovery and provenance

`discover.py` generates an 8,558-variable, 12,575-row search restriction,
fixing selector 278 and imposing the nine-class symmetry. It includes
all local 2/3/4 distributions, marginal equations, global degree/star/
triangle/codegree conditions, five-set edge clauses and the complete
retained OPB. The h3341/h3367 suffixes are checked afterward on the
candidate. Infeasibility of this restricted search would not decide the
complete LP. No solver verdict replaces the physical checker.

```sh
python3 -B ramsey_r55_m214_anchor_linked_p4_survivor/discover.py --base /tmp/new-r55-linked-check/m214-3323.opb --lp /tmp/root278.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 --int:ratfac_minstalls=0 --bool:ratfacjump=true --real:feastol=0 --real:opttol=0 -s0 -g0 -v3 -t180 -X=/tmp/root278.sol /tmp/root278.lp
python3 -B ramsey_r55_m214_anchor_linked_p4_survivor/discover.py --base /tmp/new-r55-linked-check/m214-3323.opb --solution /tmp/root278.sol --certificate /tmp/root278-certificate.json
```

Discovery used SoPlex 8.0.3, GMP 6.3.0, revision `13e2ab24`. The successful
exact solve took 6.82 seconds and 14,564 iterations. A preceding output
with tiny nonzero rational defects was rejected by exact checking;
zero feasibility/optimality tolerances triggered an exact rational basis
factorization. Different valid solver outputs are possible. Reproduction
of the published certificate needs neither SoPlex nor a search run.

The new checker imports no producer or solver. Its geometry and some
physical row routines are explicitly adapted from the author's h3531
checker; this is reuse, not independent-author review. The optional
producer uses the hash-pinned h3531 geometry, and the anchor-link emitter
and five base builders are pinned in `reproduce.py`.

Primary context checked after graph-grounded target selection:
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) for Ramsey LP and
gluing, and [Balas](https://link.springer.com/book/10.1007/978-3-030-00148-3)
for disjunctive convexification. Moment probability hulls, conditioning on
fixed bits, forbidden-state restrictions and one-hot disjunctions are
classical. No priority is claimed for these methods or a Ramsey bound.

## Evidence boundary and next gate

**Exact result:** a full-system rational survivor of \(L\) with integral
selector 278, and a complete, physically justified 11,970-row family
strictly separating that point at the same moment order.

**Covered:** every stated P4 row and domain, nine cuts, all 83 links,
one exact point of the fully selected root-278 LP, and all forbidden
monochromatic-four events in anchor 0's two neighborhoods.

**Uncovered:** the complete LP with the new forbidden states, Boolean
feasibility of root 278 or any retained root, whole M214, adjacent slices,
low-deficiency branches and order-43 Ramsey existence. The retained
Boolean census remains 380; no new root is excluded.

**Evidence and dependencies:** exact author-written physical checks and
compact certificate, with an unformalized probability-lifting proof.
The named P4 formulation, original root labels and guarded units are
explicit dependencies. The predecessor h3531 certificate and its anchor
interface have now received separate independent acceptances at h3543 and
h3547; those reviews do not review this new point. Literal feasibility and the elementary forbidden
state implication need no catalog. The Ramsey interpretation of the
upstream reduction and nine exclusions retains its reviewed extrema and
catalog-completeness premises. Trust includes the reused and new code,
CPython, hashes and ordinary hardware. Independent review of this new
result is pending; no proof-assistant formalization is claimed.

**Next falsifiable milestone:** after refreshing the graph and principal,
an exact full-system survivor or checked infeasibility certificate for
\(L\) plus all 11,970 forbidden-state rows. Merely refining selectors of
the unchanged continuous root LPs cannot remove the present point.

**Pivot condition:** two consecutive incremental-only passes without a
strict separator, full-system survivor or complete-family effect, or a
sound objection invalidating the formulation. Do not increase moment
order automatically or count another unchecked solver status as progress.
