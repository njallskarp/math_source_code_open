# Complete star-event constraints still admit an exact M214 moment point

The complete M214 four-vertex relaxation remains feasible after all nine
selector exclusions, all 83 anchor links, the 11,970 anchor-zero forbidden
states, and **every star-event inequality at every vertex and four-set**.
The exact point selects root 278 alone. All 25,054,990 presentation rows
are checked; no inherited row or domain is removed.

A global identity separates this point without adding moment coordinates:
multiply each prescribed degree equation by a three-vertex state indicator.
The point violates 237,486 of the resulting 296,184 identities. One explicit
identity has discrepancy greater than 3. The full LP with this entire new
identity family added remains **undecided**.

This is an exact rational pseudomodel, not a 43-vertex Ramsey graph. It
excludes no Boolean root or complete M-slice and changes no Ramsey bound.

## Complete systems and provenance

Let \(P_4\) be the complete formulation at Discovery Net h3423,
[definition and original source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_four_vertex_moments),
artifact `bafkreigvxxxxmc3jecxijw7nk3ph72q6mwbu7tneart7b7mxrltgn5ooxi`.
It retains the full h3323 OPB, all h3341/h3367 suffixes, the h3401
triangle/star/codegree layer, and every four-state hull, shared triple
marginal and existing footprint identification. Inherited coordinates
remain in \([0,1]\); all four-state masses are nonnegative and normalized.

As in [h3531](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_postcut_selector_fiber),
impose the nine zero-based selector exclusions

\[
Z=\{48,128,129,201,202,299,300,375,376\},\qquad y_r=0\quad(r\in Z),
\]

and all 83 equations linking an anchor-incident edge to the corresponding
selector-weighted root bit. Call this complete system \(L\). Its 389
labels are the original red-only root cover; a different cover is not
silently conjoined. The old witness's root-48 selection is not an LP row.

[H3559](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_anchor_linked_p4_survivor),
artifact `bafkreieuqktjnvhbpy2qmmacmwpcc224ueupivyyhd7sxgrqvp7u2d2hxu`,
provided an exact point in \(L\) and the complete family \(F_0\) of
11,970 anchor-zero forbidden-state rows. Its
[independent review h3565](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_m214_anchor_linked_p4_survivor_review1)
accepted the point and proved a one-row nonnegative-sum compression of
\(F_0\). That review did not decide the strengthened LP.

Here every variable \(x_{uv}\) is the red edge moment. For a four-set
\(A\), write \(p_{A,0}\) and \(p_{A,63}\) for its all-blue and
all-red masses. Define \(G\) to contain, for every \(h\notin A\),

\[
p_{A,0}\leq\sum_{v\in A}x_{hv},\qquad
p_{A,63}+\sum_{v\in A}x_{hv}\leq4.
\tag{1}
\]

There are exactly \(2\cdot43\binom{42}{4}=9,625,980\) such rows.
They use only existing coordinates. Put \(S=L+F_0+G\).

| System | Variables | Rows | Equalities | Decision here |
| --- | ---: | ---: | ---: | --- |
| \(L\) | 8,023,409 | 15,417,040 | 4,149,019 | previously feasible |
| \(L+F_0\) | 8,023,409 | 15,429,010 | 4,149,019 | exact feasible |
| \(S=L+F_0+G\) | 8,023,409 | 25,054,990 | 4,149,019 | exact feasible |
| \(S+D_3\), defined below | 8,023,409 | 25,351,174 | 4,445,203 | undecided |

Counts retain redundant rows and equations. Zero cuts are inequalities
\(-p\geq0\) against existing nonnegativity. In \(L\), the star at
anchor 0 is fixed, with both color neighborhoods of size 21. Its rows
in (1) imply \(F_0\), so dropping those 11,970 redundant rows from
\(S\) gives an equivalent 25,043,020-row presentation. The checker
retains and verifies them explicitly.

## Soundness of the complete star family

In a literal Ramsey graph, if \(A\) is all blue, at least one edge from
\(h\) to \(A\) is red; otherwise their five vertices form a blue
\(K_5\). If \(A\) is not all blue, its indicator is zero and the
first inequality is immediate. The red statement follows by exchanging
colors. Taking expectations proves (1) for all moment lifts and their
convex combinations. This argument has no catalog premise.

The same point satisfies all 9,625,980 rows, including all 223,860 rows
at each of the 43 anchors. The minimum slack is zero; 11,979 blue and
11,970 red rows are tight. Thus adjoining more members or taking linear
combinations of this **complete stated family** cannot remove this point.
This does not assert completeness of all possible star constraints or
five-vertex marginal consistency.

## Exact compact point

`certificate.json` sets \(y_{278}=1\) and every other selector to zero.
The root is \((C77,12,0,BB)\), with anomalous vertices 29 and 30.
The nine classes used only to compress this candidate are

\[
\{0\},\ \{1\},\ \{2,\ldots,7\},\ \{8,\ldots,13\},\ \{14\},
\]

\[
\{15,\ldots,26\},\ \{27,28\},\ \{29,30\},\ \{31,\ldots,42\}.
\]

The certificate has all 345 feasible four-class multisets and 2,675
positive canonical state orbits, expanding to 4,169 positive template
states. Missing states are zero. Six-edge bit order is
\((01,02,03,12,13,23)\); physical vertex permutations transport these
bits. Every probability is an integer multiple of \(1/D\), where

\[
D=10806049276781730514351569627534221489874004706641900800.
\]

The 171,629-byte certificate has SHA-256
`a457fd08c54515ae68ff2526ef79d4f74adaf21074babaea53927d3917a49b1c`.

Red degrees are 20 on \(E=\{2,\ldots,14\}\) and 21 elsewhere.
Red triangle totals are 93 on \(E\), and 100 elsewhere. Blue totals
are 107 on \(E\), 99 at 29 and 30, and 100 elsewhere. Every red
deficiency is seven; every blue deficiency is seven except eight at
29 and 30. The deficiency sums remain 301 and 303.

The decoder constructs all 903 edge moments, 12,341 red triangle moments,
37,023 blue centered wedges and 74,513 existing footprints, as well as
all 7,898,240 four-state masses. It checks every shared triple and exact
footprint event. Class symmetry and root selection restrict discovery
only: the feasibility proof evaluates the full physical system.

The point belongs to the fully selected continuous root-278 LP even
after adjoining \(F_0+G\). Consequently the convex hull of the union
of these unchanged selected-root LPs contains it. No claim concerns the
convex hull of Boolean Ramsey graphs or stronger physical disjunctions.

## A global degree identity with a strict separator

Let \(A\) be a triple, \(h\in A\), and \(s\in\{0,\ldots,7\}\)
its exact three-edge state. Let \(I_{A,s}\) be the state indicator,
\(q_{A,s}\) its probability, and \(k_s(h)\) the number of red edges
incident to \(h\) inside that state. Write \(d_h=20\) on \(E\)
and \(d_h=21\) elsewhere. Every graph with these prescribed degrees
satisfies

\[
\sum_{w\notin A}\Pr(I_{A,s}=1,\ x_{hw}=1)
=(d_h-k_s(h))q_{A,s}.
\tag{2}
\]

Indeed, multiply the literal equation
\(\sum_{w\ne h}x_{hw}=d_h\) by \(I_{A,s}\). Its two terms inside
\(A\) sum to \(k_s(h)I_{A,s}\); then take expectations. No division
by \(q_{A,s}\) is used, so zero-probability states are included.
Each left summand has only four vertices. Existing shared marginals
express \(q_{A,s}\) on any four-set containing \(A\), so (2) is
a linear identity in the current P4 coordinates. Blue-degree identities
follow by subtracting from \(40q_{A,s}\); they need no separate rows.

Let \(D_3\) be all \(3\cdot8\binom{43}{3}=296,184\) identities
(2). This is the complete stated triple-state family with the degree
center in the triple. Conditioning on triples not containing the center,
or on four-vertex events, is outside this family.

For the supplied point take \(A=\{14,27,29\}\), \(h=27\),
and the all-blue state \(s=0\). Then \(q_{A,0}=1/2\),
\(k_0(27)=0\), and the right side of (2) is \(21/2\). The left
side is

\[
\frac{1242110165208620933641330894112124455508944592792675}
{90960010747320963925518262858032167423181857800016}.
\]

The discrepancy, left minus right, is

\[
\frac{287030052361750812423389134102786697565535085892507}
{90960010747320963925518262858032167423181857800016}>3.
\tag{3}
\]

Thus even the upper half of (2) strictly separates an exact point in
the complete \(S\). It is not a Farkas consequence of \(S\).
The new identity is valid for every prescribed-degree graph lift, whether
or not the graph is Ramsey. A full physical census finds 237,486
violated identities in \(D_3\); this is a diagnostic of one pseudomodel,
not 237,486 Boolean exclusions.

`emit_degree.py` expresses the right marginal using the least vertex
\(b\notin A\), here \(b=0\). Its single separating equality has
164 nonzero coefficients and SHA-256
`d59e2f376c97232300532c004409f29a518868694cf7888175f731b0e10f4070`.
The checker independently reconstructs every coefficient and evaluates
the row exactly. It also verifies all 43 literal prescribed-degree rows
in the inherited OPB, at row numbers 1,974,561 through 1,974,603.

This closes a complete-relaxation decision by feasibility and supplies a
strict global separator at the same moment order. Feasibility of
\(S+D_3\) is not claimed in either direction.

## Reproduction and exact coverage

From a full checkout, use Python 3.10 or newer and its standard library,
with a new scratch directory outside the source checkout:

```sh
python3 -B ramsey_r55_m214_complete_star_p4_survivor/reproduce.py /tmp/new-r55-complete-star
(cd ramsey_r55_m214_complete_star_p4_survivor && shasum -a 256 -c SHA256SUMS)
```

Expected status: `EXACT_COMPLETE_ALL_STAR_P4_SURVIVOR`, with 25,054,990
checked rows, 9,625,980 global star rows, zero violated anchor-zero rows,
237,486 violated next-target identities, and the exact gap (3).
Allow several minutes and roughly 2 GB of scratch space. No solver,
network, private file, or external catalog is needed to check the point.

The reproducer regenerates the full 511,537,255-byte inherited OPB using
five hash-pinned builders. Its SHA-256 is
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`.
It regenerates the 83 links, the 11,970 forbidden rows and the single
degree separator, then byte-compares all results with the expected files.
The complete global star family is checked by literal physical enumeration
in `check.py`, so a large star-row file is unnecessary for reproduction.

Every one of the 2,983,003 retained OPB rows, including all 87 equalities,
is checked with integers at scale \(D\). Semantic coefficient checks
cover all 32,287 root units, 11,970 source five-set clauses and 43 degree
equations: 44,300 source rows. No selector-inactive suffix is skipped.
The audit covers 903 red codegrees, 21,762 coupled columns, 264,560 moment
hull facets, 98,728 triangle-atom rows, 1,806 global star equalities and
903 blue codegrees. The P4 layer checks all 123,410 four-sets, 7,898,240
nonnegative atoms, 3,949,120 triple marginals and 74,513 footprint
identifications. All 296,184 next-target identities are evaluated as
physical sums over every outside vertex, independently of the discovery
class quotient.

Controls check 529,920 physical state transports, 2,048 fixed-star Boolean
implications, all 10,240 five-vertex/star/color cases and 245,760 literal
conditioned-degree cases. Complete small-domain comparisons check every
coefficient of 280 star rows and 240 conditioned-degree rows. Twenty-five
malformed or altered inputs are rejected. Normal and assertion-disabled
controls agree byte for byte; proof checks use explicit exceptions.
The fresh full reproduction passed with exactly the expected result.

Optional complete row emission, into scratch only:

```sh
python3 -B ramsey_r55_m214_complete_star_p4_survivor/emit_stars.py --output /tmp/all-star-rows.opbpart
python3 -B ramsey_r55_m214_complete_star_p4_survivor/emit_degree.py --output /tmp/all-triple-degree-rows.opbpart
```

The latter generates the next undecided family, not rows satisfied by
this point. Large formulas, solver files, logs and intermediate points
are deliberately absent from the public package.

## Optional discovery, literature and trust boundary

`discover.py` adds all physical star-event rows modulo the candidate's
nine classes to the hash-pinned h3559 discovery model. It has 8,558
variables and 17,699 deduplicated rows: 34 new anchor-zero rows and 5,090
new star rows beyond the old model. The h3341/h3367 suffixes are checked
after candidate discovery. Infeasibility of this restricted model would
not decide the unrestricted \(S\).

```sh
python3 -B ramsey_r55_m214_complete_star_p4_survivor/discover.py --base /tmp/new-r55-complete-star/m214-3323.opb --lp /tmp/all-stars.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 --int:ratfac_minstalls=0 --bool:ratfacjump=true --real:feastol=0 --real:opttol=0 -s0 -g0 -v3 -t180 -X=/tmp/all-stars.sol /tmp/all-stars.lp
python3 -B ramsey_r55_m214_complete_star_p4_survivor/discover.py --base /tmp/new-r55-complete-star/m214-3323.opb --solution /tmp/all-stars.sol --certificate /tmp/rediscovered-point.json
```

Discovery used SoPlex 8.0.3, GMP 6.3.0, revision `13e2ab24`, taking
8.49 seconds and 14,615 iterations for the final solve. Exact rational
factorization, followed by direct rational row checking, supplies the
candidate. Solver status and floating residuals are not proof evidence.
Different solver versions can produce a different feasible point.
The [official SoPlex source](https://github.com/scipopt/soplex) describes
the exact solver; relevant algorithm references are Gleixner–Steffy–Wolter,
*Iterative Refinement for Linear Programming* (2016), and Gleixner–Steffy,
*Linear programming using limited-precision oracles* (2020).

Primary literature was checked after graph selection. Current context is
[Angeltveit–McKay, \(R(5,5)\le46\)](https://arxiv.org/abs/2409.15709).
Multiplication by Boolean state indicators and relinearization are
classical: Sherali–Adams, *A Hierarchy of Relaxations between the Continuous
and Convex Hull Representations for Zero-One Programming Problems*,
SIAM J. Discrete Math. 3(3), 411–430 (1990), DOI 10.1137/0403036.
No general-method priority or new hierarchy-level theorem is claimed.
The result is the explicit certificate, complete stated row-family
insufficiency and quantified separator against this graph-grounded LP.

The final checker imports no producer, solver or predecessor module.
Its decoder and inherited row routines are adapted from the author's
h3559 checker, independently accepted at h3565; the all-star audit,
degree census and coefficient verification are new. Reuse is disclosed:
this is author verification, not an independent external review of the
new contribution. External review is pending.

Literal feasibility and the star/degree arguments have no catalog or
solver trust premise. Their interpretation as necessary conditions for
all canonical M214 Ramsey candidates imports the reviewed root-cover,
local-extrema and nine-exclusion premises. Remaining trust is in those
imports, the unformalized reduction/checkers, hash-pinned regeneration,
CPython exact arithmetic, SHA-256 and ordinary hardware. No proof-assistant
formalization or Boolean root decision is supplied.

**Next falsifiable milestone:** decide the complete \(S+D_3\) by an
exact full-system survivor or independently checkable infeasibility
certificate, after refreshing the graph and principal strategy. Do not
continue an anchor-by-anchor cut ladder or automatically increase moment
order. Two consecutive passes yielding only incremental rows without a
strict separator, complete-system survivor or complete-family effect
trigger a pivot to the next principal-ranked exact target.
