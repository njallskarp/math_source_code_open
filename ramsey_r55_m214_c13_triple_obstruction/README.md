# A triple incompatibility in the \(M=214,c=13\) interface

## Result and scope

This directory proves a reusable third-order footprint lemma and gives a
compact obstruction inside the exact individual-interface certificate
committed at Discovery Net height 2969.

For three outside footprints \(S_x,S_y,S_z\), suppose every pairwise union
misses an independent core triple and the common intersection contains a red
core edge. A blue edge on any outside pair would create a blue \(K_5\), so all
three outside edges are forced red. The common red core edge then completes a
red \(K_5\). Such a triple of footprint types cannot coexist in any completion.

The height-2969 footprint selection contains

\[
S_0=\texttt{1c48},\qquad
S_{10}=\texttt{0e2c},\qquad
S_{18}=\texttt{1f42}.
\]

For all three pairs, \(\{0,4,7\}\) is an independent core triple disjoint from
the pairwise footprint union. Their common intersection is the red core edge
\(\{10,11\}\). Hence all eight colorings of the three outside edges are
excluded: seven use at least one forbidden blue edge, and the all-red coloring
creates a red \(K_5\).

This is a precise obstruction to extending the published height-2969 witness
through the three-outside layer. It does **not** exclude the unpinned
\(M=214,c=13\) cell, decide the full \(M=214\) branch, construct a Ramsey
graph, or improve any Ramsey-number bound.

## Affine family and minimality

The maps \(i\mapsto ai+b\), with
\(a\in\{1,5,8,12\}\) and \(b\in\mathbb Z/13\mathbb Z\), are 52 automorphisms
of the displayed cyclic core. They carry the explicit obstruction to 52
distinct unordered forbidden triples.

The four-premise Boolean proof is deletion-minimal as a standalone
certificate. Removing any one of the three pairwise blue prohibitions permits
exactly the coloring with that pair blue and the other two red. Removing the
common-edge red-triple prohibition permits the all-red coloring. This is
certificate-level minimality, not a claim of minimum proof size in the full
\(M=214\) system.

The elementary proof is given in [PROOF.md](PROOF.md).

## Certificate and exact verification

`certificate.json` records the three source indices and footprints, the three
independent-triple witnesses, the common red edge, and byte-pinned provenance
for the height-2969 certificate. The Python verifier reconstructs the cyclic
core, its 26 edges, 78 independent triples, 39 independent four-sets, the
three transversal checks, the eight edge colorings, deletion minimality, and
all 52 affine images.

The independent C++20 checker embeds the mathematical data rather than
parsing the JSON. It reconstructs the same facts with fixed-width masks,
nested loops, and a separate affine-orbit implementation.

Tested versions are CPython 3.12.12 and GNU g++ 16.2.0. From this directory,
run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_certificate.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
g++-16 -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion \
  -Wshadow -Werror independent_check.cpp -o /tmp/r55_c13_triple_check
/tmp/r55_c13_triple_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

The expected compact result is 52 affine images, eight rejected edge
colorings, four deletion models, and status
`VERIFIED TRIPLE-INCOMPATIBILITY OBSTRUCTION`.

## Trust boundary

Trusted are the normalized cyclic-core interpretation inherited from the
cited \(c=13\) dependencies, the elementary proof in `PROOF.md`, the compact
certificate, either verifier and its language toolchain, ordinary hardware,
and SHA-256 collision resistance. The checkers reconstruct every mathematical
predicate used by this result.

No SAT/MILP verdict, generated formula, raw search output, catalog file,
database, private graph state, binary, log, or credential is part of the
claim. Core-catalog uniqueness is unnecessary because this obstruction is
verified directly in the explicit cyclic representative already used by the
source certificate.

## Source calibration

[Brendan McKay's primary Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
currently lists one Ramsey\((3,5)\) graph at order 13. This calibrates the
inherited cyclic-core setting, but the present lemma neither reproves nor
depends on catalog uniqueness: both checkers verify the displayed core and
the explicit obstruction directly.

## Next falsifiable step

Add all triple-incompatibility hyperedges to the unpinned footprint-selection
stage across every E-marking, together with the 13 common-core triangle-slice
equations. The next successful milestone must be either a new exact selection
and edge lift surviving that layer or a stable-set/Hall obstruction covering
all marking cases; another fixed-selection obstruction alone should end this
incremental mechanism.
