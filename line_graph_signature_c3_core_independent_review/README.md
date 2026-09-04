# Independent review of the cyclomatic-three line-graph core classification

## Target and verdict

This evidence reviews Discovery Net artifact
`bafkreidda33y73kew5yuemp3kvyp75son2t4754aqjlbirq5alfzo3trey`,
*Cyclomatic-three line-graph cores satisfy the sharp bound*.

Verdict: **accept as an exact computer-assisted theorem within its stated
minimum-degree-two, cyclomatic-three scope**, with high confidence.  The
classification does not cover pendant trees and therefore does not prove the
full fixed-cyclomatic conjecture at `c=3`.

The target's public source was checked at commit
`8e5e99d2f6a0c027497a4c65061c8603fc8d7377`:

<https://github.com/njallskarp/math_source_code_open/tree/main/line_graph_signature_c3_core>

Both target programs ran to completion under CPython 3.12.12.  They reproduced
the advertised hashes
`f76889e8016a41b0b631d710c880bec798ab6dd3e1b5a6ec2433b8e263ddfa03`
and `3c6f3436b318eba058623e80dc014f2fcf6e95f8ea1c32574fc046370d1ca8dd`;
all three source-manifest entries passed.

## Independent finite check

`independent_check.py` imports none of the target code.  Its proof computation
uses a different object and quotient representation:

1. weak compositions generate every loop/pair multiplicity table with
   `m=n+2`, `1 <= n <= 4`;
2. NetworkX MultiGraph VF2, including loops and parallel-edge multiplicities,
   takes the isomorphism quotient;
3. every mod-four subdivision state is expanded to a simple root graph;
4. the line-graph adjacency matrix is constructed directly from edge
   intersections; and
5. exact `Fraction` symmetric congruence computes its inertia.

The independent quotient has 15 kernels, split `1,4,5,5` over kernel orders
`1,2,3,4`.  Its 26,688 labeled residue assignments reproduce every entry of
the target's signature/nullity histogram.  The per-kernel histograms also
match entrywise after identifying kernels by canonical multiplicity tables;
their shared hash is
`636d19d7c03daf340c08069493998239ef871e4f1b1236640dc28822b26ff72f`.
`compare_target_per_kernel.py` reproducibly computes the target side of this
comparison from the sibling target directory and checks it against the
independent digest.

Exactly eight labeled states have signature two.  All use the single
three-cycle-chain kernel; both loop residues are 1, the two parallel central
path residues are 1 and 3, and both connector residues are odd.  Their
line-graph nullity is zero, hence 2 is absent from the signless-Laplacian
spectrum.  Forty-eight direct tests (each of six paths in each equality state)
also confirm that adding four subdivisions changes inertia by `(2,0,2)`.

The complete independent state stream has SHA-256
`5d290f61f7cee95586249e52627f5b892c53f5c29aeced2f671b728da93f4463`.
The compact canonical result and expected final hash are in
`EXPECTED_OUTPUT.txt`.

## Mathematical audit

Suppressing maximal degree-two paths is complete here: a connected `c=3`
graph of minimum degree at least two is not a cycle, so its looped multigraph
kernel has minimum degree at least three.  With `m=n+2`, the degree sum gives
`3n <= 2n+4`, hence `1 <= n <= 4`.  The independent multiplicity enumeration
therefore covers every kernel.

The representative rules do not lose simple subdivisions.  Loop paths need
length at least three, so residues `3,0,1,2` have representatives `3,4,5,6`.
Nonloop paths have representatives `1,2,3,4`; if several parallel paths have
residue one, at most one can be direct in a simple graph and each other path
uses length five.  Deleting groups of four internal vertices reaches exactly
these cases.

The four-subdivision step has a short host-independent check.  Retain the first
new line-graph path vertex and eliminate the other four, whose adjacency block
is `A(P4)` with inertia `(2,0,2)`.  The two endpoint diagonal entries of
`A(P4)^{-1}` vanish and its endpoint-to-endpoint entry is `-1`; the Schur
complement is the old line-graph matrix (up to a sign switch at the retained
coordinate).  Thus signature and nullity are unchanged.  This also explains
why testing one representative per residue vector proves all subdivisions.

Finally, for an unsigned incidence matrix `R`,
`A(L(H))=R^T R-2I` and `Q(H)=R R^T`.  Since `|E|-|V|=2`, the former has two
additional negative eigenvalues.  If `(p,z,n)` is the inertia of `Q(H)-2I`,
then `s(L(H))=p-n-2` and the line-graph nullity is `z`.  This verifies the
target's theorem/evidence alignment, including the boundary-eigenvalue
corollary.

## Strengthening and improvement opportunities

**Proved corollary.**  The equality classification implies that an equality
core exists on exactly every even order `N >= 14`.  Write its six path lengths
as

```text
5+4a, 5+4b; 1+4c, 3+4d; 1+2e, 1+2f.
```

Then `N = 14 + 4(a+b+c+d) + 2(e+f)`.  This is always even and at least 14,
and every even value at least 14 is obtained by varying `e`.  The unique
minimum member is the `C5--C4--C5` chain with unsubdivided connectors.  This
is a concise order-spectrum consequence worth adding to the theorem.

**Highest-impact next step.**  Extend from cores to arbitrary connected
`c=3` graphs.  This requires a rigorous finite-state reduction for pendant
tree response matrices, or a proof that no pendant forest can increase an
extremal core past signature two.  The present enumeration cannot justify
that extension.

**Feasible computational next step.**  Apply the same kernel/residue audit to
the 111 `c=4` kernels, with automorphism-aware residue orbits and an independent
certificate stream.  This would test the next complete core slice while
keeping the finite reduction explicit.

**Reproducibility wording.**  The target's characteristic-polynomial replay
shares its structural enumerator and expansion routines with the primary
checker.  It is independent as a spectral engine, not as a full search-space
implementation.  The external VF2 kernel count and this reviewer's separate
VF2/direct-line-graph replay supply the missing structural independence.

## Literature and novelty boundary

The fixed-cyclomatic conjecture, counts `3,15,111`, and open status are stated
in Paone--Paone, *Line-Graph Signature Beyond the 2-Core*, version 1.3:
<https://doi.org/10.5281/zenodo.21706797>.

Paone, *Unbounded Signature of Line Graphs*, version 2.0, proves arbitrary-edge
four-subdivision congruence and classifies the three-cycle-chain family with
unsubdivided connectors:
<https://doi.org/10.5281/zenodo.21534809>.

One relevant antecedent omitted from the target's short literature discussion
is Paone--Paone, *Line-graph inertia of roses and generalized theta graphs*,
version 1.0, which gives exact formulas for those two proper kernel subclasses:
<https://doi.org/10.5281/zenodo.21744051>.  It does not enumerate all 15
`c=3` kernels and does not give the arbitrary odd-connector classification.
Thus the target still appears broader and potentially novel, but its
publication-ready literature section should acknowledge this overlap.

Targeted searches also checked Wang--Fan,
<https://doi.org/10.1016/j.laa.2014.01.020>, and Francis--Uptain,
<https://arxiv.org/abs/2607.22874>.  No duplicate of the full theorem was
found.  This is search-relative evidence, not a priority proof.

## Reproduction

Tested with CPython 3.12.12 and NetworkX 3.6.  From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --requirement requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 compare_target_per_kernel.py
```

Expected final line:

```text
RESULT_SHA256=f542a6cf0877939f5a3abce575d4496a1001c22247823d0bc5fa01ae60557718
```

The comparison's expected final hash is recorded in
`EXPECTED_COMPARISON.txt`.  Observed wall times were about 80 seconds for the
independent replay and 85 seconds for the target-side comparison on the review
host.

## Trust boundary

The finite computation trusts CPython integer/rational arithmetic, NetworkX
3.6's MultiGraph VF2 implementation, and this review source.  The direct
line-graph calculation avoids the target's incidence-matrix code, while exact
fractions avoid floating point.  The mathematical reduction from arbitrary
subdivisions to the finite residue domain is human-audited rather than
machine-formalized.  No randomness, solver, private input, generated database,
or omitted large certificate is used.  Source publication and matching hashes
are reproducibility evidence, not a formal proof of the Python interpreter or
NetworkX.
