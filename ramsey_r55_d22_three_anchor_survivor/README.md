# Ramsey R(5,5): a three-anchor limitation witness

This package gives an exact limitation witness in the order-43 `d=22`,
deficiency-six branch. It has 452 red edges, degree profile
`20^8 21^26 22^9`, and three simultaneous full valid anchors `0,3,9`.
The two nonzero anchors are mutually adjacent red neighbors of root `0`, each
with red degree ten inside its 22-vertex anchor core.

All six red/blue neighborhoods satisfy their complete local Ramsey conditions:

```text
(0,R,22,108,6), (0,B,20,100,0),
(3,R,21, 99,8), (3,B,21, 96,11),
(9,R,21, 97,10),(9,B,21, 97,10).
```

The witness is not an `R(5,5;43)` graph. It has 269 red and 200 blue
monochromatic five-cliques. More sharply, 24 red and 12 blue five-cliques use
no edge unseen by all three anchors. The first examples are recorded in
`PROOF.md` and checked edge by edge.

This exposes a structural boundary of the two-anchor diagonal method. With
three anchors an edge is unseen exactly when its endpoint signatures are
bitwise complements, but a five-set can be mixed in every coordinate without
containing complementary signatures. Such a five-set lies in no single anchor
neighborhood even though all ten of its edges are individually visible across
the six neighborhoods. The explicit coloring realizes both red and blue
defects of this fully visible mixed-signature type.

Thus a family-wide exclusion cannot follow merely from adding a third full
anchor and controlling the 96 triply unseen edges. It must couple edges that
are exposed in different anchor neighborhoods. No claim is made that all
`d=22,t>=108` cores admit this extension, and no Ramsey-number bound follows.

## Exact replay

The primary checker uses only the Python standard library:

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
```

The independent checker uses NetworkX graph objects, its graph6 decoder,
complement operation, maximal-clique enumeration, and a separate reconstruction:

```sh
uv run --no-project --cache-dir /tmp/r55-three-anchor-nx-cache \
  --with networkx==3.6.1 --python python3 independent_check.py \
  | cmp - EXPECTED_INDEPENDENT.json
```

`search.py` is optional discovery code using python-sat 1.9.dev15 and
Glucose42. The SAT model and solver verdict are outside the proof boundary;
only the explicit cross matrix is accepted after definition-level replay.

## Compact invariants

- three anchor profiles listed above;
- three-bit cell sizes `6,4,4,6,5,6,6,3` in binary order;
- 96 edges unseen by all three anchors;
- fully visible defects: 24 red and 12 blue;
- all defects: 269 red and 200 blue;
- red-edge SHA-256:
  `1a976bedb69fa94cdf0500e4087bf4e395585812c298b3095794468e004b279f`;
- monochromatic-five-set SHA-256:
  `ae684be7d326bbd9b0f70903f02d8a21ac6488a6d1a4751b7228b5b74f6fc8ed`.

## Trust boundary and provenance

The certificate is the compact graph6 data, six explicit core deletions, and
the 22-by-20 cross matrix. The standard checker reconstructs every asserted
edge, degree, neighborhood, signature, unseen edge, and five-set. The NetworkX
checker uses a distinct graph representation and maximal-clique enumeration;
matching full-list hashes give entry-level agreement. Trusted are the short
source, ordinary Python/runtime and hardware, and SHA-256 collision resistance;
the independent replay additionally trusts NetworkX 3.6.1. No SAT solver is
trusted.

The graph6 inputs originate in [Brendan McKay's `(4,5)` Ramsey
data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), but every property
of the particular records used here is checked directly. Catalog completeness
is not used. Primary methodological context is Angeltveit and McKay,
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709), arXiv:2409.15709v2.
These primary sources were checked live on 2026-09-05. No novelty is claimed
for the general pointed-neighborhood framework.
