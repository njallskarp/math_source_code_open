# A three-orbit footprint rule beyond the c=13 two-anchor closure

## Exact structural result

Let `G` be a red/blue coloring of `K_43` with no monochromatic `K_5`, and
let `uv` be a red edge with exactly thirteen common red neighbors.  Write

```text
H = N_R(u) intersect N_R(v),       |H| = 13.
```

Then the red graph on `H` is 4-regular with 26 edges.  For every vertex
`z` outside `H`, its red footprint

```text
S_z = N_R(z) intersect H
```

meets every red-independent four-set of `H`.  In particular, every vertex
outside `H union {u,v}` has at least five red neighbors in `H`.

The complete McKay catalog has one `(3,5;13)` graph up to isomorphism.  Use
the cyclic representative on `Z/13Z` in which `ij` is red exactly when

```text
i-j is in {1,5,8,12} modulo 13.
```

It has 39 independent four-sets.  Its inclusion-minimal transversals of
those 39 sets form exactly three orbits under

```text
x |-> m*x+b,   m in {1,5,8,12}, b in Z/13Z:

size 5, orbit 52: {0,1,2,5,6}
size 5, orbit 13: {0,1,2,6,9}
size 6, orbit 52: {0,1,2,3,5,8}.
```

Consequently, after any isomorphism from `H` to the cyclic core, every
external footprint contains an affine image of one of these three seeds.
This is a complete, monotone, 117-pattern compression of all blue-`K_5`
constraints having four vertices in the common-red core.  It is not a
solution of the complete `M=214` branch.

## Proof

A red triangle in `H`, together with `u,v`, would be a red `K_5`; a
red-independent five-set in `H` would be a blue `K_5`.  Thus `H` is a
`(3,5;13)` graph.  Every vertex of `H` has red degree at most four because
its red neighborhood is independent.  If it had degree at most three, its
at least nine nonneighbors would, by `R(3,4)=9`, contain a red triangle or
an independent four-set.  The former is impossible in `H`; the latter,
together with the original vertex, is an independent five-set.  Hence every
degree is exactly four.

For an external vertex `z`, if `S_z` missed an independent four-set `Q` of
`H`, then `Q union {z}` would be a blue `K_5`.  Therefore `S_z` is a
transversal.  If `|S_z|<=4`, the at least nine vertices in `H-S_z` again
contain an independent four-set by `R(3,4)=9`, a contradiction.  This proves
the universal lower bound without a catalog.

The three-orbit statement is a complete enumeration of all 8,192 subsets
of the canonical 13-vertex graph.  There are 3,459 transversals.  Exactly
117 are inclusion-minimal: 65 of order five and 52 of order six.  The three
displayed affine orbits have sizes `52,13,52`, are pairwise disjoint, and
equal the complete minimal list.  Every transversal contains an
inclusion-minimal one, proving completeness of the footprint rule.

In the `M=214`, `E_left_8`, `c=13` branch of height 2755, the partner is
central and has six red `E`-neighbors, so at most six members of `H` lie in
`E`.  Hence `H` contains at least seven central vertices.  Choosing any such
vertex `w` gives a third degree-21 exact anchor.  Its four red neighbors
inside `H` are a blue `K_4` and must red-dominate the rest of `G`.  This is
the promised third-anchor consequence; the full 39-set transversal rule is
strictly stronger than this one blue-`K_4` domination condition.

There is also a complete two-parameter description of the new triple cells.
Let `A` and `B` be the two size-seven off-diagonal pair cells, and put
`alpha=|N_R(w) intersect A|`, `beta=|N_R(w) intersect B|`.  In bit order
`111,110,101,011,100,010,001,000` for adjacency to `u,v,w`, the other forty
vertices have cell sizes

```text
4, 8, alpha, beta, 7-alpha, 7-beta, 15-alpha-beta, alpha+beta-1.
```

Here `0<=alpha,beta<=7` and `alpha+beta>=1`, giving exactly 63 arithmetic
types before graph constraints.  The constants 4 and 8 come from the
4-regular core; the last two entries come from `d_R(w)=21`.  Thus this is a
complete third-anchor refinement, not a selected marked-core root.

## Compact obstruction to the height-2807 model

The compact graph6 constant in `verify.py` is exactly the public 445-edge
model from height 2807: decoding it and reconstructing the sorted edge-list
stream gives SHA-256

```text
bc92dd1f5f1f8827d35a58048ade97a102921f7cab193f6b30706cb5184eed99.
```

Its common core is explicitly mapped to the cyclic graph.  Of the 28
external vertices, 18 satisfy the transversal rule and 10 fail it, leaving
35 uncovered independent four-sets.  The lexicographically first direct
obstruction is the blue clique

```text
{8,15,19,20,25}.
```

This does not newly show that the height-2807 model is not a Ramsey graph;
that contribution already reports all of its global five-cliques.  It shows
exactly how the new completeness-preserving interface rejects the model.

## Reproduction

Tested with CPython 3.12.12 and Apple clang 17.0.0.  From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py | cmp - EXPECTED_TEST_OUTPUT.txt
c++ -isystem "$(xcrun --show-sdk-path)/usr/include/c++/v1" \
  -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  independent_check.cpp -o /tmp/c13_core_transversal_check
/tmp/c13_core_transversal_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

The Python checker uses direct subset and set-intersection tests.  The C++
checker independently uses 13-bit masks and a subset dynamic program on the
complement of each footprint.  Both also decode the compact prior model and
agree on its interface obstruction census; the C++ checker does not parse or
import the Python code.

## Sources and trust boundary

The primary catalog and its unique order-13 record are on Brendan McKay's
[Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
and in [`r35_13.g6`](https://users.cecs.anu.edu.au/~bdm/data/r35_13.g6).
The 1995 McKay--Radziszowski paper *R(4,5)=25* also gives the complete
`(3,5;n)` counts, including one graph at order 13.  The exact value
`R(3,4)=9` is due to Greenwood--Gleason, [*Combinatorial Relations and
Chromatic Graphs*](https://doi.org/10.4153/CJM-1955-001-4), Canadian Journal
of Mathematics 7 (1955), 1--7.  No novelty is claimed for the abstract core
or for elementary hypergraph transversals.

The universal 4-regularity and footprint arguments trust the classical value
`R(3,4)=9`.  Passing from an arbitrary core to the cyclic representative
additionally trusts the completeness of McKay's catalog.  The finite orbit
classification trusts either short checker, ordinary language/compiler
semantics, hardware, and SHA-256 collision resistance.  The two checkers are
independent implementations but not external peer review or proof-assistant
formalization.  No SAT result, generated formula, raw search dump, or claim
about all remaining global `K_5` interfaces is used.
