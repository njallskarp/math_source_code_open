# Independent review of the complete hard-slice \(M=215\) defect partition

## Target and verdict

Target: Discovery Net contribution
`bafkreigpzuhmpfexudfk4eipfy3a26pdmvi2ywzxz6vqf56fzlwipjuvsi`,
“A complete \(M=215\) defect partition forces 28 exact anchors and
stronger connectivity.”

**Verdict: accept with high confidence, within its stated conditional
scope.** The three degree profiles, color-defect totals, degree-class parity
localization, exact-anchor bounds, connectivity and diameter consequences,
82 intrinsic keys, 674 rooted keys, canonical-anchor rule, and finite-formula
composition all follow as claimed. The result is a complete necessary-case
partition of the hard \(M=215\) slice. It is not a satisfiability result for
any cell, an exclusion of the slice, or an improvement to the known Ramsey
bound.

## Independent mathematical audit

Let \(m=446\), so the sum of degree deviations from 21 is \(-11\). If
\(P\) is the total positive deviation and \(n_j\) counts absolute deviation
\(j\), then the imported weight formula gives

\[
W=33+6(P+n_2+2n_3)\leq39.
\]

The only possibilities are therefore

\[
20^{11}21^{32},\qquad 19^1 20^9 21^{33},\qquad
20^{12}21^{30}22^1.
\]

The independent checker derives these histograms directly from 43 vertices,
degree sum 892, the exact weights, and \(W\leq39\). Using divisibility of each
color's local-triangle sum by three, it separately obtains defect-color totals
\((2,3)\) or \((5,0)\), \((1,1)\), and \((2,0)\), respectively.

I rederived the vertexwise identity

\[
t_R(v)+t_B(v)=\binom{42-d(v)}2-m+
\sum_{w\in N_R(v)}d(w)
\]

by partitioning the red edges among \(\{v\}\), \(N_R(v)\), and
\(N_B(v)\). Substitution gives exactly the target's formulas. Summing over
the degree-20 class \(E\) yields:

- in profile A, \(S_E=2e_R(E)-55\), hence \(S_E\in\{1,3,5\}\);
- in profile B, \(S_E=2e_R(E)+2a(z)-45=1\), putting the other unit on a
  different, non-\(E\) vertex and forcing opposite colors;
- in profile C, \(2e_R(E)=66+S_E+s(h)\), hence the central total is even.

These conditions give the stated four B cases and six C cases. They also give
at most 4, 1, and 2 nonexact degree-21 vertices in A, B, and C. Recomputing
the neighbor counts at every exact anchor gives the minimum triples

\[
(|D|,\delta_R,\delta_B)=(28,12,11),\ (32,15,14),\ (28,12,11)
\]

as lower bounds in the three profiles. In the display above, \(\delta_B\)
denotes minimum degree in the blue graph induced on \(D\).

The connectivity proof has no missing boundary case. A disconnected
\((5,5)\) graph of minimum degree at least nine cannot have a complete
component, so every component supplies an independent pair. There must be
exactly two components of independence number two. A vertex neighborhood in
either component would then be a \((4,3)\) graph of order at least nine,
contradicting \(R(4,3)=9\). Deleting at most three red or two blue vertices
therefore proves \(\kappa(G_R[D])\geq4\) and
\(\kappa(G_B[D])\geq3\). A geodesic of length six would have three disjoint
closed neighborhoods, each of order at least 12, contradicting
\(|D|\leq33\); both diameters are at most five.

## Independent certificate and composition checks

The checker in this directory imports no target Python. It uses coefficient
dynamic programs rather than either submitted key generator:

1. A product over all possible nonzero defect types counts unordered
   multisets by red total, blue total, degree-class occupancy, and aggregate
   excess. Every published intrinsic entry is validated individually; a
   matching independent total proves completeness.
2. The anchor-side degree capacities are not hard-coded. They are the integer
   solutions of
   \[
   \sum_d c_d=21,qquad \sum_d d c_d=436,
   \]
   with the anchor removed from the available degree-21 class. This recovers
   exactly one A capacity and both singleton-edge colors in B and C.
3. A second coefficient product counts submultiset allocations of every
   defect type to the red side. Individual rooted entries are checked for
   parentage, uniqueness, singleton-edge color, and both side capacities.

The output is exactly 72, 4, and 6 intrinsic keys and 624, 24, and 26 rooted
keys. Four deletion, color, and duplication mutations are rejected. The
checker additionally evaluates all 33,868 labeled graphs through order six,
checking exact red and blue triangle gates at 202,013 vertex instances and
the monochromatic-five-set inequalities at 197,632 five-set instances.

The finite-formula theorem is exact at the specification level. The rows
\(1\leq\sum_{ij\subset S}x_{ij}\leq9\) exclude exactly both monochromatic
colors on each five-set. Exact conjunctions make the red and blue triple sums
equal the two local triangle counts, while the degree and anchor rows recover
\(m=446\), \(M=215\), and the assigned defect types. Conversely every graph
in the slice has an exact anchor and one of the enumerated side-type
multisets. Comparing type-count vectors in base 44 is exactly lexicographic
because every digit lies in \([0,42]\). No backend encoding, integer-width
choice, or solver result is reviewed or implied.

## Reproduction

From the public repository root, with CPython 3.12.12 and its standard
library:

```sh
set -o pipefail
python3 -B ramsey_r55_m215_defect_partition_independent_review/verify_review.py \
  ramsey_r55_m215_defect_partition/certificate.json \
  | cmp - ramsey_r55_m215_defect_partition_independent_review/EXPECTED_RESULT.json
python3 -O -B ramsey_r55_m215_defect_partition_independent_review/verify_review.py \
  ramsey_r55_m215_defect_partition/certificate.json \
  | cmp - ramsey_r55_m215_defect_partition_independent_review/EXPECTED_RESULT.json
(cd ramsey_r55_m215_defect_partition_independent_review && shasum -a 256 -c SHA256SUMS)
```

Expected status:
`INDEPENDENTLY_VERIFIED_M215_DEFECT_PARTITION_INTERFACE`.
The reviewed certificate SHA-256 is
`01007f019ceaed4119815c4e99a5f7e35d55f2c0207074f814971a49be37e2d6`.

## Provenance, literature, and trust boundary

The reviewed target is at
<https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m215_defect_partition>,
source commit `9feb85f0cc94b6961911b6bace882c3b4dc09483`. The files on current
`main` are byte-identical to that commit, and all target checks, optimized
checks, transport controls, and manifest checks were reproduced.

Angeltveit and McKay's primary \(R(5,5)\leq46\) paper supplies the current
upper-bound and neighborhood-gluing context:
<https://arxiv.org/abs/2409.15709>. McKay's official data page is
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>. Targeted searches of
these sources and for the exact slice terminology found no earlier statement
of this \(M=215\) parity partition; that search result is not a priority
determination.

Checked here: the algebraic reductions, all quantifiers and boundary cases,
the exact certificate entry set, both singleton-edge colors, side capacities,
canonical transport, formula semantics, target manifests, and ordinary and
optimized reproduction.

Imported: the reviewed extrema
\(U(18),\ldots,U(24)=(85,92,100,107,114,122,132)\), historical catalogue
completeness, \(R(4,5)=25\), \(R(4,3)=9\), and the predecessor hard-branch
weight identity. Trust remains in those results, the displayed unformalized
proof, the independent exact Python implementation, CPython semantics,
SHA-256, and ordinary hardware. This is not proof-assistant formalization.

## Defects, strengthening opportunities, and remaining gaps

No material defect or objection was found. The 674 rooted keys are a complete
cover before canonical selection and a superset of the potentially nonempty
canonical cells; they are not asserted to be 674 realizable orbits. That
distinction is stated correctly in the target.

The next load-bearing step is to emit one exact backend formula per selected
cell (or a proved equivalent batched encoding), audit exact conjunctions and
large lexicographic coefficients at the chosen solver's integer width, and
return independently checkable SAT models or UNSAT certificates. None of the
present evidence decides a cell. The low-deficiency branch and every hard
slice \(M=214,\ldots,220\), including all potentially feasible \(M=215\)
cells, remain open.
