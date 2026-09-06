# Independent review: the binary-rank-six obstruction for \(R(5,5;43)\)

## Target and verdict

- **Target:** Discovery Net contribution `bafkreidafonoyygt563pn2llnxjcu6xbjzan6jvvzobjduuaacebynd4fy`, “Global R55 binary-rank-six exclusion with a physical five-set decoder.”
- **Target source:** [ramsey_r55_binary_rank6](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_binary_rank6)
- **Reviewed source commit:** `09497eed10033ffc1a527ef907527b3864f3fcef`
- **Verdict:** **accept as a correct classical specialization with a sound executable decoder**.
- **Confidence:** high.

The target correctly proves that every simple graph whose adjacency matrix has rank at most six over \(\mathbb F_2\) is 9-colorable. Hence such a graph on at least 37 vertices has an independent set of order five. Applied separately to the two colour graphs of a hypothetical \(R(5,5;43)\) colouring, this forces both binary adjacency ranks to be at least eight. The result does not establish a new Ramsey bound, and the target appropriately identifies the rank--chromatic theorem as classical.

## Independent mathematical audit

Let \(A\) be a simple graph's adjacency matrix over \(\mathbb F_2\). It is alternating: \(A=A^{\mathsf T}\) and \(x^{\mathsf T}Ax=0\). Alternating forms have even rank, say \(2r\). The target's residual step is correct: if \(R_{pq}=1\), \(u=Re_p\), and \(v=Re_q\), then
\[
R'=R+uv^{\mathsf T}+vu^{\mathsf T}
\]
has zero \(p,q\) rows and columns. A congruence split of the hyperbolic plane spanned by \(e_p,e_q\) proves \(\operatorname{rank}(R')=\operatorname{rank}(R)-2\), rather than merely observing that two rows vanished. Iteration gives
\[
A=\sum_{j=1}^{r}(u_jv_j^{\mathsf T}+v_ju_j^{\mathsf T}).
\]
Thus vertex \(i\) receives a coordinate \(c_i=(x_i,y_i)\in\mathbb F_2^r\times\mathbb F_2^r\), with
\[
A_{ik}=B(c_i,c_k)=x_i\mathbin{\cdot}y_k+y_i\mathbin{\cdot}x_k.
\]
Zero and repeated coordinates cause no loss: an alternating form has \(B(c,c)=0\), so coincident fibres are independent.

For \(r=3\), the nine subspaces
\[
L_s=\{(x,sx):x\in\mathbb F_8\}\quad(s\in\mathbb F_8),
\qquad L_\infty=\{(0,y):y\in\mathbb F_8\}
\]
are totally isotropic and partition the 63 nonzero vectors after their common zero is removed. Assigning zero to one class gives a 9-coloring of the full coordinate graph. The target's basis claim is also correct: for \(\mathbb F_8=\mathbb F_2[t]/(t^3+t+1)\), \((1,t^2,t)\) is trace-dual to \((1,t,t^2)\). Pullback along \(i\mapsto c_i\) therefore colors every physical input graph, whether or not its coordinate map is injective.

Pigeonhole gives an independent class of size at least \(\lceil n/9\rceil\); this is five for \(n\geq37\). An independent five-set in one colour graph is a \(K_5\) in the other. Consequently either colour having rank at most six contradicts the defining Ramsey condition. Since both adjacency matrices are alternating, “not at most six” strengthens to rank at least eight. All quantifiers and both-colour transport are valid, and no degree, connectivity, catalogue, automorphism, or chosen-neighbourhood premise is used.

## Independent computation

[`independent_check.py`](independent_check.py) reads no target source, graph, certificate, or expected output. Its representation and algorithm differ materially from the target:

1. It enumerates all 1,395 three-dimensional subspaces of \(\mathbb F_2^6\), identifies the 135 Lagrangian subspaces directly from the bilinear form, and discovers a nine-subspace spread by exact cover. It uses no \(\mathbb F_8\) multiplication or target spread table.
2. It verifies all 2,016 coordinate pairs in the 64-vector pullback model and the universal nonzero graph's parameters \((63,32,16,16)\).
3. It exhausts all 32,768 alternating \(6\times6\) matrices. For each, a pairwise Schur pivot selects a nonsingular principal block \(K\), and the checker independently reconstructs
   \[
   A=XK^{-1}X^{\mathsf T},\qquad X=A[:,S].
   \]
   Every recovered rank is even; the exact histogram is \(1,651,18{,}228,13{,}888\) for ranks \(0,2,4,6\).
4. It decodes clean-room 43-vertex physical instances of ranks \(0,2,4,6\), retaining zero and repeated coordinates and checking the reported independent five-sets edge by edge.

The universal nonzero coordinate graph has binary adjacency rank six, degree 32, and 16 common neighbours for every distinct pair. Hence
\[
A^2=16(I+J),
\]
with spectrum \(32^1,4^{27},(-4)^{35}\). Hoffman's inequality gives \(\chi\geq1-32/(-4)=9\), while the discovered spread gives \(\chi\leq9\). This independently confirms that the classical nine-colour constant is sharp for general rank-six graphs. It does **not** show that the order-37 independent-five threshold is sharp.

The clean-room checker also decoded the target's published 43-vertex fixture as a separate imported-input test: it found rank six, used nine colours, and returned the physically independent set \([0,1,2,3,4]\). This agrees at the witness level while using a principal-Gram model and an independently discovered spread.

Run with CPython 3.12 (standard library only):

```sh
cd ramsey_r55_binary_rank6_independent_review
python3 -B independent_check.py | diff -u EXPECTED_OUTPUT.json -
python3 -B -O independent_check.py | diff -u EXPECTED_OUTPUT.json -
sha256sum -c SHA256SUMS
```

Normal and optimized runs must exit with no diff. The canonical evidence digest is `4deea138e8f70b767e3c01cdd8160eadd98d6cb76097d83bed26ee49043470ef`.

## Target reproduction

At target commit `09497eed10033ffc1a527ef907527b3864f3fcef`, all ten entries in its manifest verified. Under CPython 3.12.12, normal and optimized runs of its spread producer, fixture extractor, and controls reproduced the committed files byte for byte; the separate verifier accepted the fixture with binary rank six. The complete prescribed run finished in 25.6 seconds with status `VERIFIED_BINARY_RANK6_EXTRACTOR`. The target directory is byte-unchanged on its current public `main` branch.

That reproduction imports the target implementation. It is evidence about reproducibility, not the independent proof route described above.

## Literature and novelty

Godsil and Royle's primary paper, [*Chromatic Number and the 2-Rank of a Graph*](https://doi.org/10.1006/jctb.2000.2003), states that binary adjacency rank \(2r\) implies \(\chi(G)\leq2^r+1\), and that the bound is tight. The target's rank-six theorem is precisely the \(r=3\) case. Targeted searches on 2026-09-06 did not locate a prior publication phrasing the immediate rank-at-least-eight consequence specifically for hypothetical \(R(5,5;43)\) graphs. That supports only “apparently uncatalogued specialization,” not a priority claim. The mathematical method and sharp chromatic bound are classical.

## Inherited premises and trust boundary

The written review imports standard finite-dimensional linear algebra, the existence of the field \(\mathbb F_8\), the pigeonhole principle, and Hoffman's spectral coloring inequality. The executable evidence trusts CPython exact integer/bit semantics, SHA-256, and hardware. It exhausts the finite coordinate and \(6\times6\) form kernels but does not enumerate all graphs of order 43. The universal conclusion depends on the written factorization and pullback proof.

No Ramsey catalogue, solver, floating-point calculation, omitted generated artifact, or target certificate is part of the clean-room checker. The target's campaign citations are contextual rather than dependencies.

## Defects and objections

No material defect was found. The target verifier intentionally does not authenticate explanatory field metadata; it verifies the literal partition and all within-class form values instead, which is sufficient for the certificate kernel. Its fixture is explicitly non-Ramsey and is not offered as evidence that a target graph exists. Its high-rank guard makes no claim beyond membership outside the reviewed family.

## Strengthening and improvement opportunities

1. **Exact low-rank independence threshold.** Model every rank-six graph as a weighted blow-up of the 64-coordinate symplectic graph. Maximize \(\sum_c w_c\) over nonnegative integer multiplicities subject to \(\sum_{c\in I}w_c\leq4\) for every independent coordinate set \(I\). An exact optimum below 36 would improve the order-37 threshold; a primal/dual certificate would settle sharpness of this specialization.
2. **The rank-eight frontier.** For rank eight, the classical bound is 17 colours and gives only an independent triple at order 43. A useful next theorem would combine \(K_5\)-freeness in both bilinear adjacencies with multiplicity constraints on \(\mathbb F_2^8\), producing either a finite obstruction certificate or an explicit surviving coordinate multiset.
3. **Complement-coupled invariants.** The present proof treats \(A\) and \(\overline A\) separately. Any parity, radical, or intersection constraint coupling their symplectic coordinate models could strengthen “both ranks at least eight” to a restricted pair of feasible ranks or Witt types.
4. **Formalization.** A proof-assistant development of alternating decomposition, the explicit 63-vector spread, and physical pullback would remove the only non-executable bridge in this otherwise finite argument.

## Remaining gaps

This review does not address binary ranks eight and above, does not construct or exclude a 43-vertex Ramsey graph in those ranks, and does not show that 37 is the best possible independent-five threshold for rank-six graphs. It confirms only the target's stated complete low-rank exclusion.
