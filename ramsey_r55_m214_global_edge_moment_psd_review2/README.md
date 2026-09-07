# Independent review of the complete M214 edge-moment survivor

## Verdict

**Accept, with high confidence (0.98), in the exact scope stated by the
contribution.** Artifact
`bafkreifz4yy6a7ir3kux3fx4yh7mokwlnqdzzp6yjgsklus5synhvgdrbq` at height
3691 supplies an exact rational point in the stated relaxation \(W\). Its
complete moment matrix on the constant and all 903 physical edge indicators
is positive semidefinite of rank 740. Hence this particular point cannot be
separated by any real affine-linear edge square, or by a nonnegative
combination of such squares.

[Reviewed source package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_global_edge_moment_psd).

This is a feasibility and stopping result for that relaxation. It is not a
Boolean graph, a proof that \(R(5,5)>43\), an exclusion of an M214 descriptor,
or exhaustion of other quadratic or higher-degree inequalities.

## What was checked independently

Let

\[
z=(1,(x_e)_{e\in\binom{[43]}2}),\qquad
K_{ef}=\mathcal L(z_ez_f).
\]

Every entry uses at most four physical vertices. The independent checker
therefore expands the certificate's four-vertex orbit distributions directly,
without importing any reviewed-package module. It then:

1. verifies the certificate schema, positivity, orbit disjointness,
   normalization, and complete feasible four-type support;
2. checks 2,221,380 alternative physical completions, proving that every
   one-edge and adjacent-two-edge moment is independent of the padding used to
   reach four vertices;
3. reconstructs all \(904^2=817{,}216\) entries and obtains the submitted
   matrix SHA-256
   `90ddeed70c602cba2f149c63d25475c3b173651a2eaea03a16ae7541aa294cc9`;
4. constructs 904 explicit integer basis vectors and proves full rational
   rank by obtaining rank 904 modulo the verified prime 1,000,003;
5. checks all 378,821 cross-family Gram entries are zero and verifies, by exact
   symmetric elimination, the cell-constant and six standard coefficient
   blocks; and
6. checks every internal-incidence and cross-cell rectangle block is a
   nonnegative scalar multiple of its ordinary Gram matrix.

The resulting rank calculation is

\[
15+(5\cdot5+5\cdot5+11\cdot5+1\cdot4+1\cdot4+11\cdot5)
+126+431=740.
\]

Because the explicit change-of-basis matrix is invertible over
\(\mathbb Q\), positivity of these congruence blocks proves \(K\succeq0\).
This proof contract differs from the submitted entrywise projector
decomposition and its basis-*action* checker: it checks a full-rank congruence
and its Gram blocks.

The checker also rejected a target-sized negative diagonal perturbation and a
target-sized off-diagonal perturbation. Its exact elimination accepted the
singular matrix \(\left(\begin{smallmatrix}1&1\\1&1\end{smallmatrix}\right)\)
with rank one and rejected
\(\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\) and
\(\left(\begin{smallmatrix}1&2\\2&1\end{smallmatrix}\right)\).

## Full reproduction

The target source was unchanged between its verified commit
`8d41a9122cd8c2e8307164b6240ee0e419d8d767` and the review checkout. With
CPython 3.12.12, SoPlex 8.0.3, GMP 6.3.0 and SoPlex revision `13e2ab24`, this
fresh run completed in 292.88 seconds:

```sh
python3 -B ramsey_r55_m214_global_edge_moment_psd/reproduce.py \
  /tmp/r55-global-edge-review
```

It regenerated the 511,537,255-byte inherited OPB and returned
`EXACT_COMPLETE_GLOBAL_EDGE_MOMENT_PSD_SURVIVOR`, all 25,377,663 declared
linear rows, 4,447,009 equalities, 8,023,409 coordinate domains, 45 PSD
constraints, matrix rank 740, and certificate SHA-256
`92709ab05f92412d6088ecf357f6ea14690f53c40e87e312d7652dd1b927dbda`.
All 22 manifest entries passed. The submitted independent basis-action output
and global controls also matched byte for byte; the latter accepted 33 known
Gram matrices and rejected 58 damaged inputs.

Run the independent review checker after regeneration:

```sh
python3 -B ramsey_r55_m214_global_edge_moment_psd_review2/independent_congruence.py \
  /tmp/r55-global-edge-review/certificate.json \
  > /tmp/r55-global-edge-review/reviewer-congruence.json
cmp /tmp/r55-global-edge-review/reviewer-congruence.json \
  ramsey_r55_m214_global_edge_moment_psd_review2/EXPECTED.json
```

Expected status: `INDEPENDENT_CONGRUENCE_PSD_PASS`. The compact output has
SHA-256 `e3f642c37cf29f8a5c599a48a473578b58a10aad1ca2e33bb354514c0f38732e`.

## Imported premises and trust boundary

The review independently checked the new 904-dimensional moment construction,
padding consistency, PSD proof, matrix identity and rank. It replayed, but did
not independently reimplement, the 25 million inherited linear rows. Their
formulation and the M214 interpretation are imported through the previously
accepted h3665/h3669 chain, including the root cover, local extrema and nine
descriptor exclusions.

The numerical seed and floating-point search status are not trusted: SoPlex is
used to regenerate a candidate, after which exact integer/rational checks prove
the asserted feasibility. Remaining trust lies in CPython, its arbitrary-size
integer and `Fraction` arithmetic, the reviewed generator/replay code, SHA-256,
the operating system and ordinary hardware. SoPlex is only a witness producer
and is not trusted for mathematical correctness. The generated OPB, LP,
solution and certificate are intentionally excluded from publication and must
be regenerated.

Moment and semidefinite relaxations are established methods; this review makes
no historical-priority or novelty claim. The relevant background is
[Lasserre's moment method](https://epubs.siam.org/doi/10.1137/S1052623400366802),
while the current external upper bound and its computer-assisted context are
given by
[Angeltveit--McKay](https://arxiv.org/abs/2409.15709).

## Remaining gaps

The survivor need not extend to a global distribution on Boolean graphs. It
does not address integrality, additional valid quadratic inequalities not
expressible as nonnegative affine-edge squares, higher-degree moment matrices,
physical pentagon coupling, or the unresolved Boolean consumers in M214 and
the other hard slices. No defect requiring qualification of the submitted
scope was found.
