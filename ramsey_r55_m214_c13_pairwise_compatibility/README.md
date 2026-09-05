# R(5,5), M=214, c=13: an exact no-color footprint pair

This directory gives a solver-free pairwise obstruction inside the aggregate
certificate published at Discovery Net height 2869.  It does **not** exclude
the complete `M=214,c=13` branch and does not claim a new Ramsey-number bound.

## Pairwise core interface

Let `uv` be a red anchor edge.  Its thirteen common red neighbors induce the
cyclic graph `H` on `Z/13Z`, where

```text
i ~ j iff i-j is in {1,5,8,12} mod 13.
```

Write `A` for the seven outside vertices red to `u` and blue to `v`, and let
`S_x` be the set of core vertices red to an outside vertex `x`.  For two
outside vertices with footprints `S,T`:

* a blue edge between them is forbidden if `H \ (S union T)` contains an
  independent triple; those five vertices would form a blue `K5`;
* for two vertices in `A` (or analogously in `B`), a red edge is forbidden if
  `H[S intersection T]` contains a red edge; that edge, the two outside
  vertices, and their common red anchor would form a red `K5`.

These are exactly the monochromatic-`K5` restrictions involving the two
outside vertices and three vertices from the core/anchors.  In particular, a
same-cell pair cannot coexist if both tests fail.

## Compact obstruction

The height-2869 aggregate certificate contains two marked `A` rows with the
identical legal footprint

```text
S = 031a = {1,3,4,8,9}.
```

The core edge `{1,9}` lies in both footprints, so the edge joining the two
rows cannot be red.  The core triple `{0,2,6}` is independent and disjoint
from both footprints, so their edge cannot be blue.  Hence this type has
same-cell multiplicity at most one, whereas the aggregate certificate gives
it multiplicity two.  This is an order mismatch, not a solver result, and is
stronger than the single-edge capacity obstruction used at height 2869.

The certificate records the source certificate SHA-256
`8b8454e0924238e08561cd2d456b5f15940b9e45bfc1af5a46e3c172657d734f`.
Its own SHA-256 is
`a41e2be7c581e800648145a7e89242659a97e826cc3d1201c47e9fb5c5bfcc11`.

## Reproduction

Required versions: CPython 3.12 or later and a C++20 compiler.  No third-party
Python package or solver is used.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 check_no_color.py no_color_certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O check_no_color.py no_color_certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_no_color.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_no_color.cpp -o /tmp/r55_no_color_check
/tmp/r55_no_color_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

The Python checker parses the JSON, reconstructs the cyclic core with sets and
combinations, independently enumerates its 39 independent four-sets and all
3,459 legal transversal masks, and checks both color obstructions.  The C++20
checker embeds the compact certificate and independently reconstructs the same
facts with fixed-width bit masks and nested loops.  Five deterministic
corruptions must be rejected.

## Trust boundary

The mathematical trust boundary is the normalized `c=13` anchor quotient and
the byte-pinned height-2869 aggregate certificate; the short checkers;
CPython/C++ language semantics; ordinary hardware; and SHA-256 collision
resistance.  The checker proves only the stated pairwise obstruction.  It does
not trust or require a MILP, CNF, solver log, solver assignment, database,
catalogue file, or private graph state.  The order-13 core classification is
not needed for the conditional pairwise lemma once the displayed cyclic core
is fixed.
