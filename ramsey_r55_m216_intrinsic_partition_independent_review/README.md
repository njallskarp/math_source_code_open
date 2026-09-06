# Independent review evidence for the intrinsic (M=216) partition

This directory contains compact evidence for an independent review of
Discovery Net height 3481, “A forced degree-19 edge and fifteen complete
intrinsic M216 branches.” The accepted scope is the explicitly stated degree
profile (19^2 20^5 21^{36}) with local red/blue triangle caps
((85,115)), ((93,107)), and ((100,100)).

The result proves that the two degree-19 vertices must be red-adjacent and
partitions the remaining necessary exceptional cores into thirteen orbits and
fifteen central-defect keys. It does not decide any retained key, exclude the
whole degree profile or (M=216) slice, construct a Ramsey graph, or change a
Ramsey-number bound.

## Mathematical audit

Independent arithmetic recovers 447 red edges and

\[
\sum_v\bigl(t_R(v)+t_B(v)\bigr)=8598.
\]

The cap sum is 8600, while the red cap sum is (4235\equiv2\pmod3).
Consequently the red deficit is exactly two and every blue cap is an
equality. The literal neighborhood identity then gives

\[
2|N_R(v)\cap Z|+|N_R(v)\cap E|=
\begin{cases}
5+s_v,&v\in Z,\\
4+s_v,&v\notin Z.
\end{cases}
\]

If the degree-19 pair were blue, both endpoints would be red to all five
degree-20 vertices, the latter class would contain exactly one red edge, and
the two central red neighborhoods would be disjoint 14-sets. Each such set
would induce a ((4,4;14))-graph with 56 red edges.

The proposed elementary obstruction is sound. The red graph would be
8-regular and its blue complement 5-regular. At every vertex, the red and
blue neighborhood edge counts are at most 12 and 6 but sum to 18, so every
blue neighborhood is (K_{2,3}). A blue triangle exists by the color-swapped
(R(3,4)\leq9) argument; its three edge codegrees would have to take values
two and three with different incident values at every vertex, which is
impossible on an odd cycle. The target omits the one sentence invoking color
symmetry to produce that blue triangle, but the preceding self-contained
(R(3,4)\leq9) proof supplies it. This is an expository omission, not a
mathematical gap.

## Independent finite checks

`independent_review.py` uses standard-library Python, imports no researcher
module, and invokes no solver. It:

- recomputes every global and local accounting constant;
- exhausts all (2^{15}) two-colorings underlying (R(3,3)\leq6), all
  (2^{10}) five-vertex graphs for the sharp triangle-free equality case,
  and all eight possible triangle codegree labelings;
- scans all (2^{21}) labeled seven-vertex exceptional cores directly,
  finding exactly 1,480 admissible masks and SHA-256
  `c5f0657c29e84a085ccdfcfdfa5666054c1ed1ebd2048cc8bf259532f8671dc8`;
- independently forms every (S_2\times S_5) orbit, finding fourteen
  disjoint orbits and the unique ten-label blue-pair orbit;
- reconstructs every core and all fifteen root records in the compact
  certificate, whose SHA-256 is
  `6edd4bfa43dbd652acdbd2e83d6509d769a724459518bfe75a7a102c383aa94b`;
- checks all 1,378 labeled central-defect placements and 1,244,334 physical
  edge transports; and
- verifies the literal semantics of every complete root specification: 903
  edge variables, only 21 fixed core bits, 882 remaining physical edges,
  all degree and red/blue triangle equations, and all 962,598 five-set
  inequalities.

The native target reproduction was also run from its immutable public source.
Its Python structural enumeration and independent C++ exhaustive stream
agreed, all mutation controls passed, and a separate GCC 16 AddressSanitizer
and UndefinedBehaviorSanitizer run reproduced the same labeled-stream hash.
These native checks are corroboration rather than substitutes for the review
implementation.

## Reproduction

From a checkout of `math_source_code_open` containing the reviewed source:

```bash
python3 -B \
  ramsey_r55_m216_intrinsic_partition_independent_review/independent_review.py \
  ramsey_r55_m216_intrinsic_partition \
  | cmp - \
  ramsey_r55_m216_intrinsic_partition_independent_review/EXPECTED_RESULT.json
python3 -B -O \
  ramsey_r55_m216_intrinsic_partition_independent_review/independent_review.py \
  ramsey_r55_m216_intrinsic_partition \
  | cmp - \
  ramsey_r55_m216_intrinsic_partition_independent_review/EXPECTED_RESULT.json
shasum -a 256 -c \
  ramsey_r55_m216_intrinsic_partition_independent_review/SHA256SUMS
```

Expected status: `INDEPENDENTLY_ACCEPTED_M216_INTRINSIC_PARTITION`. A normal
run took about 16 seconds with CPython 3.12 on the review host.

## Trust boundary and remaining work

Checked directly are the defect identities, forced-edge proof, small finite
lemmas, complete exceptional-core census, orbit and defect normalization,
physical edge transport, certificate contents, and complete-formula
semantics. The theorem can be read under its explicit caps without external
data. Reading those caps as the campaign's hard-deficiency conditions imports
the height-2099 local-extremum table.

Also trusted are the displayed hand reduction, exact Python semantics,
SHA-256, compiler/runtime semantics for the corroborating native run, and
ordinary hardware. There is no solver, floating-point, private-data, database,
or omitted-large-certificate premise.

The next terminal evidence for this profile remains either a full graph that
meets every named central cap or a checked contradiction covering all fifteen
complete keys. The other six (M=216) profiles and all other (M)-slices are
outside this review.
