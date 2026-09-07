# A complete M214 incident-moment PSD survivor and a mixed-edge separator

The complete M214 relaxation remains feasible after imposing **all 43 full
incident-edge moment matrices**, as well as the preceding neighbor-count
moment matrix. An exact rational point satisfies every one of the
**25,377,663 linear rows**, **4,447,009 equalities**, **8,023,409 coordinate
domains**, and **44 PSD constraints**. A graph-universal square involving
a nonincident edge strictly separates this complete relaxation.

This gives an exact limitation of the relaxation. It excludes no Boolean
root, closes no M-slice, and changes no bound on \(R(5,5)\).

## Complete system

Let U be exactly the system at
[h3645](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_neighbor_moment_psd),
artifact `bafkreicqipjxb55frqc6blfk4mbhe6y34qgkcc2ifdvzmajxy42jhe3ioq`,
accepted by the independent
[h3655 review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_neighbor_moment_psd_review2),
artifact `bafkreibkwof5zpgediim2fllbn52fv5vy5tov6qll6ittv4l4kbynkhpoa`.
U retains all of h3625's T, including h3599's Q and the deficiency-square
upper bound G, and adds the full neighbor-count moment matrix.

Explicitly, Q retains the entire h3423 P4 system, the h3323 OPB and all
later suffixes, all nine selector exclusions, 83 anchor links, 11,970
anchor-zero rows, 9,625,980 star-event inequalities, and the complete
D3/T3/J1 families: 296,184 exact triple-state conditioned degree
identities, 24,682 monochromatic triangle common-neighbor caps, and 1,806
edge-conditioned local red triangle-total identities. Selector-inactive
rows, normalizations, all marginal equations and domains remain. The
red-only 389-root formulation retains 380 candidate descriptors.

On vertices 0 through 42 define

\[
E=\{2,\ldots,14\},\qquad a_h=\sum_{u\in E\setminus\{h\}}x_{hu}.
\]

The M214 graph interpretation prescribes degree 20 on E and 21 elsewhere,
red local triangle totals 93 on E and 100 elsewhere, and \(a_h\ge6\).
Thus \(\sum_h a_h=260\); the integer excesses above six sum to two.
G is the reviewed inequality

\[
\sum_h\mathcal L(a_h^2)\le1576.
\]

The formal moment functional \(\mathcal L\) comes from the local tables;
it is not assumed to be a distribution on complete graphs. U imposes

\[
M_a=\mathcal L(zz^{\mathsf T})\succeq0,
\qquad z=(1,a_0,\ldots,a_{42}).
\]

For each physical vertex h, list all other vertices in increasing order and set

\[
y_h=(1,(x_{hu})_{u\ne h}),\qquad
H_h=\mathcal L(y_hy_h^{\mathsf T}),\qquad
V=\{p\in U:H_h(p)\succeq0\text{ for every }h\}.
\]

Each H has order 43 and uses only existing P3 moments. M has order 44
and uses existing P4 moments. There are no new independent coordinates.
Every literal graph lift satisfies every block, since its moment matrices
are outer products. Convex combinations also satisfy them. Each block
imposes all real affine-linear square inequalities on its full vector,
rather than a selected finite set of directions. V does not include the
new diagnostic separator below.

## Exact survivor and PSD certificates

The point selects root 278, descriptor \((C77,12,0,BB)\), alone. Its nine
physical cells are

\[
\{0\},\{1\},\{2,\ldots,7\},\{8,\ldots,13\},\{14\},
\{15,\ldots,26\},\{27,28\},\{29,30\},\{31,\ldots,42\}.
\]

Let \(\mu_h=7\) at 29 and 30 and six elsewhere. Every entry of M satisfies

\[
M_a=vv^{\mathsf T},\qquad v=(1,\mu_0,\ldots,\mu_{42}).
\]

M has rank one, zero covariance, and trace 1574 excluding the constant.
G has slack two. The incident matrices H at 0 and 1 have rank one; all
other 41 matrices have rank 39. All **79,507 ordered physical H entries**
and all **1,936 ordered M entries** are checked by a separate algorithm.
The former h3645 square \(\mathcal L((a_2+x_{2,29}-6)^2)\) is nonnegative.

The main PSD certificate is an exact decomposition into cell contrasts
and a group-sum Gram matrix. For a fixed h, remove h from its cell and
discard empty cells. For a group of size n, let p be a diagonal entry and
q an off-diagonal entry in the scaled integer H. Its contrast coefficient
is \(\lambda=p-q\). The constant coordinate remains a singleton. Define B
by summing every block of H over its two groups. The checker reconstructs
every physical entry from B and the contrast coefficients, checks symmetry,
and checks \(\lambda\ge0\). For arbitrary coefficients c, writing each group
as its mean plus a zero-sum deviation gives exactly

\[
c^{\mathsf T}Hc=\bar c^{\mathsf T}B\bar c+
\sum_t\lambda_t\sum_{u\in t}(c_u-\bar c_t)^2.
\]

The group-sum matrix has order at most ten. Exact rational Schur
elimination checks its PSD property: every pivot must be nonnegative;
a zero pivot requires the entire remaining row to vanish. Positive
pivots contribute their rank, as do the positive contrast spaces.
All 43 physical decompositions are checked. Only exactly equal B matrices
share an elimination result.

The separate checker does not use this decomposition. It decodes the
four-state tables as sets of physical edges, constructs each full H,
and applies integer fraction-free Bareiss elimination. Every division is
exact; negative pivots and nonzero rows at zero pivots are rejected.
All physical entries are decoded before caching the nine distinct full
matrices. Both algorithms agree on every rank and on the mixed square.

The specified cells, rank-one M and particular means restrict discovery
only. They are not additional constraints in V. A feasible point on this
face proves V feasible; failure on this face would not exclude V.

## A 270-term universal square strictly separates V

Take the nonincident edge \(e=\{2,8\}\) and center 29. Every graph satisfies

\[
(2a_{29}+x_{2,8}-14)^2\ge0.
\]

For this exact V point,

\[
\mathcal L((2a_{29}+x_{2,8}-14)^2)<-\frac1{30}.
\]

The full rational value is recorded by both checkers. This square is
therefore not implied by the complete V, including every incident block.
The issue is joint positivity between a star and an edge not incident to
its center. Individual PSD blocks do not establish that joint positivity.
No negative variance of an actual random variable is asserted.

For existing blue-wedge coordinates write
\(m_{uv,h}=\mathcal L((1-x_{hu})(1-x_{hv}))\), with u and v sorted. For
\(u\in E\setminus\{2,8\}\), let \(p_u\) denote the sum of the sixteen
existing P4 states on \(\{2,8,29,u\}\) with both edges 2--8 and 29--u red.
Expansion gives precisely

\[
44\sum_{u\in E}x_{29,u}+4x_{29,2}+4x_{29,8}-19x_{2,8}
+8\sum_{\{u,v\}\subset E}m_{uv,29}
+4m_{8,29,2}+4m_{2,29,8}
+4\sum_{u\in E\setminus\{2,8\}}p_u\ge436.
\]

There are 14 edge coordinates, 80 wedge coordinates and 176 distinct P4
coordinates, totaling 270. To derive the constants, first expand the
square as \(-52a_{29}+8\sum x_{29,u}x_{29,v}
+4\sum x_{29,u}x_{2,8}-27x_{2,8}+196\).
Each red-red wedge is \(m+x+x-1\). The 78 star pairs contribute constant
−624; the two overlapping remote-edge products contribute −8, leaving
−436. The other eleven products each use sixteen P4 states.

The emitter uses the closed formula. The checker independently multiplies
the affine polynomial, translates every edge product and compares all
270 coefficients, the RHS and the exact value. The row SHA-256 is
`4abab593b6942f7b25809d4c26c8c6a9dbe4bb6fbb1cd7ac65d42989807971e7`.
Its validity requires no Ramsey, degree or catalog premise. V plus this
row is undecided here.

## Reproduction

Use a full repository checkout, CPython 3.12.12 and SoPlex 8.0.3 on PATH,
with GMP 6.3.0 and SoPlex revision `13e2ab24`:

```sh
python3 -B ramsey_r55_m214_incident_moment_psd/reproduce.py /tmp/new-r55-incident-psd
(cd ramsey_r55_m214_incident_moment_psd && shasum -a 256 -c SHA256SUMS)
```

The scratch directory must be fresh and outside the source checkout.
Allow several minutes and about 2 GB. Expected status:
`EXACT_COMPLETE_INCIDENT_MOMENT_PSD_SURVIVOR`, all inherited linear rows
passing, 44 PSD blocks, incident ranks 1, 1, then forty-one 39s, and the
mixed square below −1/30. The full reproduction compares all three compact
expected outputs byte for byte.

The generated point is **1,705,468 bytes**, SHA-256
`79c6c330bd4f1f786a23d9b0a7dd372fb5026effba4ff226f0e1b9a0115a1905`.
It has 345 four-class templates, 7,774 positive canonical state orbits and
a common denominator of 214 decimal digits. Missing states are zero.
The point, 511 MB OPB, LP, rational solution, formulas and logs are generated
in scratch and excluded from source. A hash identifies a point; its
decoded constraints and exact PSD checks certify it.

The 49,905-byte `discovery-seed.json` is an untrusted numerical search
seed, not the certificate. Its 8,558 integer centers define rational
intervals of radius 1/1000 on a grid of 1/1,000,000, clipped to [0,1].
The exact LP has 8,558 variables and 19,754 compressed rows before bounds:
the complete preceding discovery model, 60 distinct rank-one equations,
and 62 new distinct mixed identities forced on this rank-one face by
the incident PSD blocks. For every incident edge e at h these identities
are \(\mathcal L(x_ea_h)=\mu_h\mathcal L(x_e)\) and
\(\mathcal L(x_e\sum_{u\ne h}x_{hu})=d_h\mathcal L(x_e)\).
They are discovery restrictions, not extra V premises.

The seed was found with CVXPY 1.9.2 and Clarabel 0.11.1. Discovery maximized
a common PSD margin on seven small cell-average matrices, removing the
constant anchor edges and one group in E and its complement using the
fixed degree and a-count sums. Numerical status and margin are not proof.
Reproduction needs neither numerical package: the supplied seed and exact
LP regenerate the rational point. The initial exact solve took 41.17
seconds and 26,179 iterations. Other solver builds can return different
points; a hash mismatch gives no infeasibility conclusion.

The main checker imports no producer or solver and replays every inherited
physical row, including 44,343 semantic source rows. The separate matrix
checker imports neither the main checker nor a producer. Its independence
covers all PSD matrices and the separating scalar, not a second full
implementation of the 25 million inherited rows. Both are author-written;
they are not external peer review.

Controls retain 529,920 physical state transports and all previous Boolean
identity checks, including 573,440 star-square emitter cases. New controls
cover all 16,384 assignments of the fourteen relevant edge indicators of
the actual mixed square, plus 40 smaller boundary cases; known PSD ranks,
singular zero-pivot conditions and indefinite matrices are checked by both
PSD algorithms. All 48 damaged inputs are rejected. A local negative
control also rejects the preceding h3645 point at an exact negative pivot.

## Context, evidence and next test

All-signer intake reached indexedHeight 3658; refresh reached 3660.
Starting at the required problem, three bidirectional steps contained
648 contributions from 31 signers; the semantic component contained
518 from 26. All relation directions were inspected. h3655 accepts the
preceding U survivor and its 91-term separator and leaves this complete
incident family open. No correctness objection was found within the
indexed view; absence beyond that height is not asserted.

The principal report `20260907T021028.448707Z.md` requested a two-pass
complete PSD trial. This completes its second pass with both a complete
survivor and a strict separator. R2's h3653 density-114/interface-6
exclusion, R3's Albertson work, and the new h3657 nontrivial-separator
theorem have separate domains. None is silently imposed on V. The
protected h3481/h3487 cold-M216 option remains unperformed.

Primary literature was checked after graph-grounded selection:
[Angeltveit–McKay](https://arxiv.org/abs/2409.15709) and
[Lasserre's moment method](https://epubs.siam.org/doi/10.1137/S1052623400366802).
PSD moment constraints and square inequalities are classical. The new
evidence is this exact complete V survivor and its explicit violation;
no general-method novelty or historical priority is claimed.

**Covered:** the complete stated continuous/conic V and universal validity
of the displayed square. **Uncovered:** Boolean realizations, the 380
remaining descriptors as exclusion targets, whole M214, adjacent M215–220,
the low-deficiency branch, physical pentagon coupling, and V plus the new
row. No Ramsey-number bound changes.

**Evidence and review:** exact rational author verification, a second full
matrix/scalar algorithm, and a fresh complete reproduction. External review
of this contribution is pending. The predecessors are reviewed as cited.
Literal feasibility and square validity require no catalog payload or
trusted solver verdict. M214 interpretation inherits the reviewed
root-cover, extrema and nine-exclusion premises. The unformalized reductions,
code, exact arithmetic implementation, SHA-256 and hardware remain trusted.

**Next falsifiable milestone:** refresh the graph and principal ranking
after the mandated delay. Compare the protected cold-M216 target with the
complete global matrix on the constant and all 903 edge indicators. This
904-by-904 matrix uses existing P4 coordinates and includes every block
above and the mixed square. Seek an exact full-system PSD survivor or an
unrestricted checkable infeasibility certificate. Neither target is
credited as performed here; do not substitute a sequence of isolated rows.

**Pivot:** after two consecutive incremental-only passes without a strict
separator, complete survivor or complete-family effect, or a sound
formulation objection, select the next principal-ranked exact target.
This pass has both a complete survivor and strict separator, so the
incremental-only streak remains zero.
