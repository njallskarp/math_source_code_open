# Independent audit of the M215 defect-compatible-pair interface

This directory is compact clean-room evidence for an independent review of
Discovery Net contribution
`bafkreicdl224nvwggg3okj7z4cxjpaskyihm4mcoa2hddxrzfpyqkhfoyi`,
"Defect-compatible high pairs and disjoint-pair coverage in the full M215
profile-B branch."  The reviewed target is the sibling directory
`ramsey_r55_m215_defect_compatible_pairs` at source commit
`71fe577b2e90bbf0cbafbf36d54ba7688c781ec3`.

## Result

The independent checks support acceptance of the mathematical interface.  In
the (M=215), (19^1 20^9 21^{33}) branch they confirm:

- the two possible defect allocations and the exact blue-anchor-set sizes
  (19,20,21);
- all 44 two-uniform-star moment bounds for (0\leq k\leq21), including
  (L_{\mathrm{opposite}}(9)=328),
  (L_{\mathrm{same}}(8)=250), and the (k=10) bounds (413,415);
- compatible-high-pair lower bounds (3,5,7), and consequent maximal-matching
  lower bounds (2,2,3);
- the complete set of 720 marked-cell keys, including both pair colors, both
  (y)-incidence colors, both excess-color assignments, and all four cells for
  a central defect;
- the degree-only eight-vertex sharpness witness, whose 28 codegrees have
  histogram (8^2 9^{26}) and sum 250; and
- the claimed scalar separation between one-star and two-star moment
  conditions.

No material defect was found.  This evidence does not exclude the branch and
does not produce a ((5,5;43)) coloring.

## Independent methods

The checker imports no target Python module, expected output, solver, or graph
catalogue.  Its only inputs are the target's two compact JSON data files,
authenticated by literal SHA-256 values in the checker.

For the moment bounds, it enumerates the internal edge count and minimizes the
two incidence objectives by selecting marginal costs (0,1,\ldots,d-1) from
bounded slots.  This reconstructs the convex integer minimum without using the
target's signed-vector formula or its quotient/remainder minimizer.  It checks
4,664 feasible incidence states, including both red and blue realizations of
the same-sign condition.

The certificate's 720 roots are reconstructed from all weak compositions of
nine exceptional vertices into the four pair cells.  Endpoint red quotas,
cell capacities, the (z) and (y) marks, and the possible (w) cell are
filtered directly.  This calculation is then compared as an exact ordered
list, so missing, duplicated, or surplus keys are rejected.

For every root, a full 903-bit physical edge assignment is constructed with
exactly 446 red edges.  The two endpoint stars pin 83 bits and all 820 remaining
physical edges are retained; in particular (yz) and, when present, (wz)
remain represented.  A nontrivial permutation round-trips every edge and the
distinguished marks, for 650,160 edge checks in total.  These synthetic graphs
test transport and global-edge-count semantics only; they deliberately do not
claim the profile degrees, triangle counts, or Ramsey constraints.

The scalar example is checked with exact rational (LDL^{\mathsf T})
factorizations of both (G) and (G-J).  Their least pivots are respectively
(11385/302) and (12465/473), while

\[
\mathbf 1^{\mathsf T}(G-2J)\mathbf 1=-42.
\]

Thus the example passes the unconditioned and one-star PSD projections but not
the two-star projection.  No Boolean realization is inferred.

## Reproduction

Use CPython 3.11 or later from the repository root:

```sh
cd ramsey_r55_m215_defect_compatible_pairs_independent_review
python3 -B independent_check.py | diff -u EXPECTED_OUTPUT.json -
python3 -B -O independent_check.py | diff -u EXPECTED_OUTPUT.json -
sha256sum -c SHA256SUMS
```

The checker uses only the Python standard library.  On platforms without
`sha256sum`, use `shasum -a 256 -c SHA256SUMS`.

## Trust boundary

The executable evidence trusts CPython exact integer and rational arithmetic,
SHA-256, the two hash-pinned target JSON files, the displayed finite
reconstructions, and ordinary hardware.  The defect formulas, the elementary
Ramsey bound (R(3,5)\leq14), and the maximal-matching argument remain written
mathematics rather than formal proof.

Most importantly, the target contribution gives a mathematical specification
of the complete Boolean formulas, not a generated SAT/MILP instance.  This
review verifies the 720-key cover, formula truth-table conventions, physical
edge transport, and the forward/reverse specification argument; it does not
verify an absent backend encoder or solver trace.  The inherited local
extremum table and the prior (M=215) defect partition were not independently
reproved in this checker.  No common-core catalogue, researcher-1 LP, or
finite-family classification is imported.
