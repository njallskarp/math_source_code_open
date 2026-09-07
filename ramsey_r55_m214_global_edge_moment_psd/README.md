# An exact M214 survivor of the complete global edge-moment matrix

The complete stated M214 relaxation remains feasible after imposing the
moment matrix on the constant and **all 903 physical edge indicators**.
An exact rational point satisfies all **25,377,663 linear rows**,
**4,447,009 equalities**, **8,023,409 variable domains**, and the complete
**904-by-904 PSD matrix**. Its exact rank is **740**. All 44 preceding PSD
blocks are retained and checked as well, giving 45 declared PSD constraints.

Consequently **every affine-linear edge square is nonnegative at this
point**. No additional nonnegative combination of such squares can separate
it. This exhausts the affine-edge-square route for this complete base
relaxation. It does not exhaust integrality, other valid quadratic
inequalities, higher-degree moments or Boolean consumers. No graph family
or whole M-slice is excluded, and no bound on \(R(5,5)\) changes.

## Complete system and theorem

Let V be exactly the complete system at
[h3665](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_incident_moment_psd),
artifact `bafkreigjxsbx2ywc6ckt6sorx7c5wrrjktuudhxqlags46uoaqcwfpryay`.
The independent
[h3669 review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_incident_moment_psd_review2),
artifact `bafkreiaeqkiwja4fjmk4xoumiiyi4hq5wnr6rei433m6hpcr32grxvzqpa`,
accepts both its complete survivor and its 270-term mixed-square violation.

V retains the entire h3645 U, h3625 T and h3599 Q chain. In particular it
retains the full h3323 OPB, all later P4 and column-hull suffixes, every
selector-inactive row, nine descriptor exclusions, 83 anchor links, 11,970
anchor-zero rows, 9,625,980 star-event inequalities, 296,184 exact
triple-state conditioned degree identities, 24,682 same-color triangle
common-neighbor caps, 1,806 edge-conditioned local triangle identities,
all marginal and normalization equations, and every coordinate domain.
The red-only 389-descriptor formulation has 380 remaining descriptors.

On labels 0 through 42 define

\[
E=\{2,\ldots,14\},\qquad
a_h=\sum_{u\in E\setminus\{h\}}x_{hu}.
\]

The M214 graph interpretation has degree 20 on E and 21 elsewhere, red
local triangle totals 93 on E and 100 elsewhere, and \(a_h\ge6\).
Thus \(\sum_h a_h=260\); the nonnegative integer excesses above six sum
to two. The inherited G row is \(\sum_h\mathcal L(a_h^2)\le1576\).
V includes the full neighbor-count matrix on \((1,a_0,\ldots,a_{42})\)
and, for every h, the full incident matrix on \((1,(x_{hu})_{u\ne h})\).

Let \(\mathcal E=\binom{\{0,\ldots,42\}}2\), listed lexicographically, and put

\[
z=(1,(x_e)_{e\in\mathcal E}),\qquad
K(p)_{ef}=\mathcal L_p(z_ez_f),\qquad
W=\{p\in V:K(p)\succeq0\}.
\]

The leading index denotes the constant. Every matrix entry uses at most
four vertices, so the existing P4 coordinates determine it. No independent
moment coordinate is added. Diagonal products use \(x_e^2=x_e\).

**Exact theorem:** the regenerated rational point belongs to W, with
\(\operatorname{rank}K=740\). In particular, for every real b and real
edge coefficient vector c,

\[
\mathcal L\left(\left(b+\sum_{e\in\mathcal E}c_ex_e\right)^2\right)
=(b,c)K(b,c)^{\mathsf T}\ge0.
\]

Every literal graph lift satisfies the PSD condition because its matrix
is \(zz^{\mathsf T}\); convex combinations also satisfy it. The supplied
formal moment functional need not be induced by any distribution on
complete graphs. This theorem is exact feasibility of W, not a Ramsey graph.

## Supplied point

The point selects root 278, descriptor \((C77,12,0,BB)\), alone, and uses
the nine cells

\[
\{0\},\{1\},\{2,\ldots,7\},\{8,\ldots,13\},\{14\},
\{15,\ldots,26\},\{27,28\},\{29,30\},\{31,\ldots,42\}.
\]

Its neighbor-count matrix is still the rank-one matrix
\(vv^{\mathsf T}\), where \(v=(1,\mu_0,\ldots,\mu_{42})\), with
\(\mu_{29}=\mu_{30}=7\) and all other means six. Its trace excluding
the constant is 1574, so G has slack two. The 43 incident matrices have
ranks 1, 1, followed by forty-one 39s. Both former diagnostic squares,
including \(\mathcal L((2a_{29}+x_{2,8}-14)^2)\), are now nonnegative.
Their exact values and coefficient checks remain in the output.

The particular root, cells, means and rank-one neighbor matrix restrict
discovery only. They are not additional premises of W. A full feasible
point on this face establishes W's feasibility; restricted failure would
not establish unrestricted infeasibility.

## Exact PSD decomposition of every physical entry

The main certificate expresses K as a sum of PSD operators. It checks
**all 817,216 ordered physical entries** against that sum. This avoids
relying on a representation-classification theorem to infer coverage.

Partition edge coordinates by the cells containing their endpoints, and
give the constant its own orbit. There are 43 such coordinate groups.
For each orbit o let \(b_o\) be its indicator vector and \(N_o\) its size.
The cell-sum block is \(B^0_{op}=b_o^{\mathsf T}Kb_p\). Its contribution is

\[
\sum_{o,p}\frac{B^0_{op}}{N_oN_p}b_ob_p^{\mathsf T}.
\]

For a vertex cell i of size \(n_i\ge2\), write
\(P_i=I-\mathbf1\mathbf1^{\mathsf T}/n_i\). This is an orthogonal
projection onto zero-sum vertex vectors. For each other cell j, define
\(J_{i,j}v\) on its cross edges by the coefficient \(v_u\) at edge
\(\{u,w\}\), with \(u\in i,w\in j\). The internal copy, present only
when \(n_i\ge3\), has coefficient \(v_u+v_w\) on \(\{u,w\}\subset i\).
All other edge coordinates, including the constant, have coefficient zero.
On zero-sum v these maps satisfy

\[
\|J_{i,j}v\|^2=d_{i,j}\|v\|^2,
\qquad d_{i,j}=\begin{cases}n_j,&j\ne i,\\n_i-2,&j=i.\end{cases}
\]

For one literal difference \(v=e_a-e_b\), form the exact block
\(B^i_{jk}=(J_{i,j}v)^{\mathsf T}K(J_{i,k}v)/2\). Its contribution is

\[
\sum_{j,k}\frac{B^i_{jk}}{d_{i,j}d_{i,k}}
J_{i,j}P_iJ_{i,k}^{\mathsf T}.
\]

This is PSD when \(B^i\) is PSD, by the PSD property of \(B^i\otimes P_i\).
The checker reconstructs its entries using the exact intersection count
of the endpoints of each physical pair of edges.

Two scalar projector families complete the sum:

- For internal edges of a cell with \(n_i\ge4\), the projector is
  \(I-bb^{\mathsf T}/\binom{n_i}2-J_{i,i}P_iJ_{i,i}^{\mathsf T}/(n_i-2)\).
  Its range is the kernel of the vertex-edge incidence matrix. Its rank is
  \(n_i(n_i-3)/2\). It is multiplied by
  \(K_{ab,ab}-2K_{ab,ac}+K_{ab,cd}\) for four distinct cell vertices.
- For edges between distinct cells i and j of sizes at least two, the
  projector is \(P_i\otimes P_j\), of rank \((n_i-1)(n_j-1)\). Its
  coefficient is \(K_{ac,ac}-K_{ac,ad}-K_{ac,bc}+K_{ac,bd}\), where
  a,b are distinct in i and c,d distinct in j.

The internal projector formula follows from the displayed isometry factor:
the constant and internal standard ranges are orthogonal, and subtracting
their orthogonal projections leaves another orthogonal projection. Thus
each residual term is PSD when its scalar is nonnegative.

The supplied cell-sum block has rank 15. The six standard blocks have
orders 9,9,9,8,8,9, ranks 5,5,5,4,4,5, and multiplicities 5,5,11,1,1,11.
There are four internal and fifteen cross-cell residuals, all strictly
positive. Their dimensions sum to 126 and 431. Therefore

\[
\operatorname{rank}K=15+168+126+431=740.
\]

Every small PSD block is checked by exact rational Schur elimination,
including the nonzero-row obstruction at a zero pivot. Every physical
matrix entry is compared to the displayed sum, with only 2,320 repeated
orbit/intersection patterns cached. The complete identity matrix passes
the same decomposition with rank 904.

## Separate spanning-basis verification

`independent_global.py` imports no main checker, decomposition or producer.
It decodes canonical states as physical edge sets, pads queried events to
four vertices, and independently reconstructs the entire matrix. It uses
a different proof contract: exact matrix actions on a complete basis.

The basis consists of 43 orbit indicators, all 304 standard-copy vertex
differences, 126 internal incidence-kernel vectors obtained by rational
row reduction, and 431 four-edge rectangles between cells. Indicator
supports, injectivity of the standard maps, free kernel coordinates and
rectangle coordinates establish independence within the families. The
checker verifies all **378,821 pairs from different families are
orthogonal**. The dimensions sum to 904, so the basis spans the full space.

Every one of the **817,216 basis-image coordinates** is checked. Constant
and standard images must obey their complete small-block formulas. All
internal and rectangle basis vectors must be eigenvectors with the
appropriate common nonnegative scalar, obtained from their actual images.
The small blocks are independently decomposed into positive rank-one
residual terms and reconstructed exactly. This proves the same rank 740.

The two decoders agree on the complete matrix SHA-256
`90ddeed70c602cba2f149c63d25475c3b173651a2eaea03a16ae7541aa294cc9`.
The canonical stream has header `904 D` followed by a newline, then each
row of the integer matrix \(DK\), separated by single spaces and terminated
by a newline; D is the certificate's common denominator. The hash is an
identity check, not a substitute for the exact PSD proofs.

## Reproduction and controls

From a full repository checkout, use CPython 3.12.12 and SoPlex 8.0.3,
GMP 6.3.0, SoPlex revision `13e2ab24`, with `soplex` on PATH:

```sh
python3 -B ramsey_r55_m214_global_edge_moment_psd/reproduce.py /tmp/new-r55-global-psd
(cd ramsey_r55_m214_global_edge_moment_psd && shasum -a 256 -c SHA256SUMS)
```

Use a fresh scratch directory outside the source checkout. Allow several
minutes and about 2 GB. Expected status:
`EXACT_COMPLETE_GLOBAL_EDGE_MOMENT_PSD_SURVIVOR`, all inherited rows
passing, 45 declared PSD constraints, global rank 740 and the matrix hash
above. The reproduction compares four compact expected outputs byte for
byte. Independent matrix checking alone is:

```sh
python3 -B ramsey_r55_m214_global_edge_moment_psd/independent_global.py \
  /tmp/new-r55-global-psd/certificate.json
```

The generated point is **1,835,332 bytes**, SHA-256
`92709ab05f92412d6088ecf357f6ea14690f53c40e87e312d7652dd1b927dbda`.
It has 345 four-class templates, 7,774 positive canonical state orbits
and a common denominator with 231 decimal digits. Missing states are zero.
The full point, 511 MB inherited OPB, LP, matrix, rational solution,
formulas and logs are generated in scratch and omitted from source.

The 49,866-byte numerical seed specifies untrusted rational search boxes
of radius 1/1000 around centers on the 1/1,000,000 grid, clipped to [0,1].
The exact discovery LP has 8,558 variables and 20,334 compressed rows
before bounds: the preceding complete discovery model, 60 rank-one
neighbor equations, and 642 distinct global edge/a and edge/degree null
identities. The latter include the preceding 62 incident identities.
All physical h and edge e are covered under the stated cell symmetry.
Their null directions are forced on the chosen rank-one search face;
they are not asserted to hold on every unrestricted W point with these
particular means. The full W check retains all inherited physical rows.

CVXPY 1.9.2 and Clarabel 0.11.1 were used only to discover the seed.
Seven numerical PSD blocks (orders 15,5,5,5,4,4,5) and nineteen scalar
conditions result after removing fixed anchor edges and the known degree
and a-count null directions. No numerical solver status proves anything.
Reproduction needs neither numerical package: the seed and exact LP
regenerate the rational point. The initial exact SoPlex solve took 46.96
seconds and 24,774 iterations. Different builds may return different
points; a hash mismatch is not an infeasibility certificate.

The inherited controls retain 48 rejected corruptions, 529,920 physical
state transports and the prior Boolean identity tests. The new global
controls check 33 known Gram matrices, including zero, identity,
deterministic outer-product and independent-Bernoulli matrices, with cell
sizes spanning the 1/2/3/4 boundaries. They cover the full 904-dimensional
identity and reject 58 malformed, asymmetric or indefinite inputs.
Both global algorithms check 822,588 entries/image coordinates across
these controls; normal and optimized global controls agree. The preceding
h3665 point also reconstructs exactly but is rejected at a negative exact
PSD pivot, as its mixed-square violation requires.

The main physical 904-matrix construction and PSD check took about five
seconds on the author machine. The independent verification avoids a dense
904-dimensional rational factorization by checking sparse basis actions.
Neither checker relies on floating-point eigenvalues. The separate global
checker is not a second implementation of the 25 million inherited linear
rows; those are replayed in full by the adapted main checker.

## Graph context, scope and stopping decision

All-signer intake reached indexedHeight 3676 after the human 60-minute
boundary. Three bidirectional steps from the required problem contained
651 contributions from 31 signers; the semantic traversal contained 520
from 26. New h3669 accepts V's full survivor and mixed separator. New
h3667 accepts the global separator-through-19 theorem. A later query
returned indexedHeight 3677 while the route was at 3688: no absence beyond
3677 was inferred. The new h3677 binary cut-rank obstruction was read in
full and has a separate Boolean family. None of these cut theorems is
silently added to W.

The principal report `20260907T043051.969142Z.md` explicitly selects this
complete 904-dimensional test and says a complete survivor ends the
affine-square route. R2 retains its active interface-7 density-114 consumer;
R3 remains on Albertson review standby. This work does not duplicate
either lane.

Primary literature was checked after graph-grounded selection:
[Angeltveit–McKay](https://arxiv.org/abs/2409.15709) and
[Lasserre's moment method](https://epubs.siam.org/doi/10.1137/S1052623400366802).
PSD moment methods are classical. The contribution is this exact full W
survivor and its independently checkable complete matrix certificate,
without a general-method or historical-priority claim.

**Covered:** the entire stated W and all real affine-linear squares in
the 903 physical edge indicators. **Uncovered:** Boolean realizations,
exclusion of the 380 remaining descriptors, whole M214, adjacent M215–220,
the low-deficiency branch, other valid quadratic inequalities, higher-degree
moments, physical pentagon coupling and separate separator/cut-rank gates.

**Evidence and review:** exact author verification, a distinct complete
matrix/basis-action checker and a fresh full reproduction. External review
of this new result is pending. The predecessors are reviewed as cited.
Literal feasibility and matrix positivity need no catalog payload or
trusted solver verdict. M214 interpretation inherits the reviewed root,
extrema and nine-exclusion premises. Unformalized reductions, code, exact
arithmetic implementations, SHA-256 and ordinary hardware remain trusted.

**Stopping decision:** this complete survivor ends the current
affine-edge-square mechanism. Further squares in the same physical edge
variables cannot remove this point. The two-pass allowance is not a
requirement to spend a second pass after a complete disposition.

**Next falsifiable milestone:** after the mandated delay and fresh graph
and principal intake, reassess toward a complete Boolean family, with the
first canonical h3481/h3487 M216 key the protected option. Implement its
complete native encoding and require an exact survivor or independently
checkable unrestricted exclusion. This next consumer has not been run.
The generic two-incremental-pass pivot rule remains, with streak zero;
the stronger complete-survivor stopping rule already applies here.
