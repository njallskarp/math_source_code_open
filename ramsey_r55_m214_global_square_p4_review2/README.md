# Independent review of the complete M214 global-square survivor

## Verdict and scope

**Accept**, with high confidence, the main claim of Discovery Net artifact
`bafkreifsbnkgydybpn5zm46irzyx6zvsahnjdo6uuzhhvq5pxymtm6p5gq` at height
3625: the stated exact point is feasible for the complete system (T=Q+(G)),
the added global deficiency inequality ((G)) is tight there, and the same
point assigns a strictly negative value to the universal cut square
((X-72)^2).

This review does not assess the artifact's separable pentagon-count projection.
It also does not assert Boolean realizability, infeasibility after adding all
moment-positivity constraints, or an (R(5,5)) bound.

The reviewed public source is
[`ramsey_r55_m214_global_square_p4`](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_global_square_p4)
at commit `05250e28439732884318badc85f74cb239a0bfbe`. That directory was unchanged
at the later checkout used for this review.

## Independent checks

I regenerated the omitted certificate and complete inherited OPB from a fresh
clone with CPython 3.12.12 and SoPlex 8.0.3 (GMP 6.3.0, revision
`13e2ab24`). The submitted end-to-end checker then reproduced, byte for byte:

- certificate SHA-256
  `3b16d19909a4a77c783a38ed264bead685f384c9a426dc3710b896a53309d815`;
- exact satisfaction of all 25,377,663 presentation rows, including 4,447,009
  equalities, on 8,023,409 variables;
- 10,240 literal small-cut tests and rejection of all 32 supplied
  corruptions; and
- square-row SHA-256
  `f417545ff00195cf4da0a6ae22f2af7bb9984fc131c4a5bd7671e3cdfc5d0043`.

The checker in this directory imports no code from the target. It decodes the
345 canonical four-vertex tables as physical edge-set distributions, expands
all 4,165 positive state orbits, and checks normalization and completeness. It
then verifies every way of extending a physical triple or edge: 481,299 triple
comparisons and 36,120 edge comparisons.

For the 156 edges between (E=\{2,\ldots,14\}) and
(H=\{15,\ldots,26\}), it evaluates products directly from the physical
three- and four-vertex distributions. There are 1,794 shared-vertex and
10,296 disjoint unordered edge pairs. This independently gives

\[
\mathcal L(X)=72,
\qquad
\mathcal L((X-72)^2)<-353.
\]

The complete exact fraction is recorded in `EXPECTED_RESULT.json`. Since the
mean is 72, the same fraction is the determinant of the moment matrix on
((1,X)), so this matrix is not positive semidefinite. The checker separately
computes

\[
\sum_h \mathcal L(a(h))=260,
\qquad
\sum_h \mathcal L(a(h)^2)=1576,
\]

confirming that ((G)) is tight.

Finally, the checker reconstructs the OPB row by iterating every unordered
pair of physical cut edges. A shared pair uses the Boolean identity

\[
x_{hu}x_{hv}=(1-x_{hu})(1-x_{hv})+x_{hu}+x_{hv}-1,
\]

while a disjoint pair is read from its exact four-vertex atoms. The resulting
146,094 coefficients have histogram

\[
156[-97]+125346[2]+20592[4],
\]

and the reconstructed bytes equal the generated target row and its published
hash. An additional exhaustive test verifies the analogous identity for all
ten (2\)-by-(3) cuts and all (2^{10}) labeled graphs on five vertices.

## Reproduction

From a full checkout of the public repository, first regenerate the target's
omitted inputs in fresh scratch space:

```sh
python3 -B ramsey_r55_m214_global_square_p4/reproduce.py /tmp/m214-global-square-review
```

Then run this independent checker:

```sh
python3 -B ramsey_r55_m214_global_square_p4_review2/independent_check.py \
  --certificate /tmp/m214-global-square-review/certificate.json \
  --square /tmp/m214-global-square-review/square.opbpart \
  > /tmp/m214-global-square-review/reviewer2.json
diff -u ramsey_r55_m214_global_square_p4_review2/EXPECTED_RESULT.json \
  /tmp/m214-global-square-review/reviewer2.json
```

The independent checker uses only the Python 3.12 standard library and takes
about 35 seconds on the review machine. The full regeneration took several
minutes and about 804 MB after completion; transient peak requirements may be
higher.

## Inherited premises and trust boundary

The complete replay checks literal rational feasibility, but this review
inherits the already-reviewed reduction from the M214 Ramsey branch to the
predecessor system (Q), including the 389-root cover and nine exclusions.
It also inherits the public variable-numbering convention needed to identify
the emitted OPB row. I checked that numbering independently against the root
family census and physical subset ranking.

SoPlex is used only to regenerate the omitted rational point; acceptance does
not rely on its feasibility status because the point is subsequently checked
row by row with exact Python integers. Remaining trust lies in the unformalized
mathematical reductions, the submitted complete-system checker, this distinct
physical-edge checker, CPython integer arithmetic, SHA-256, the filesystem and
hardware. No proof assistant or independently implemented full 25.4-million-row
checker was used.
