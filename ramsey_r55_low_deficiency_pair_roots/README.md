# Optimal pair roots for the R(5,5;43) deficiency-at-most-six branch

## Result

Let `G` be a red/blue coloring of `K_43` with no monochromatic `K_5`.
Fix a vertex `u` and a color `c`, and put

```text
H = G_c[N_c(u)],  d = |H|,  t = e(H).
```

The exact local extrema are

```text
U(18..24) = 85,92,100,107,114,122,132.
```

Suppose this side has deficiency at most six, so `t >= U(d)-6`.  There
is a `c`-neighbour `v` of `u` with

```text
q = |N_c(u) intersect N_c(v)| >= q0(d),
q0(18..24) = 9,10,10,10,10,11,11.
```

More precisely, at least

```text
r(18..24) = 3,1,2,4,5,1,4
```

vertices `v` in `H` have `H`-degree at least `q0(d)`.

Proof: `H` is a `(4,5;d)` graph.  Each vertex of `H` has degree at most
13 because its neighbourhood is a `(3,5)` graph and `R(3,5)=14`.  If `x`
vertices have degree at least `q0` and all others have degree at most
`q0-1`, then

```text
2t <= 13x + (d-x)(q0-1).
```

Take `q0=ceil(2(U(d)-6)/d)` and solve this inequality for `x`; the two
displayed tables result.

For a selected partner, write `e=d_c(v)`.  Since every global color degree
lies in `18..24`, and the common neighborhood is a `(3,5;q)` graph, the
remaining 41 vertices have the four exact cell sizes

```text
common c          q
u-only c          d-1-q
v-only c          e-1-q
neither c         43-d-e+q.
```

The complete `(3,5;q)` catalog counts for `q=9..13` are
`290,313,105,12,1`.  Therefore the whole deficiency-at-most-six branch is
covered by 189 scalar `(d,e,q)` cells and at most 18,767 coarse rooted
templates after replacing the common neighborhood by its catalog isomorphism
type.  The cover is complete but not disjoint: a coloring can have several
eligible roots and partners, and not every coarse template need extend.

## Optimality and limitation

The lower threshold `q0(d)` cannot be increased using only the facts that
`H` is a `(4,5;d)` graph and `e(H)>=U(d)-6`.  `SHARP_WITNESSES.json` contains
one explicit graph for every `d=18,...,24` with exactly this maximum degree.
The checker decodes each graph, applies its listed edge deletions, and directly
checks `K_4`-freeness, absence of an independent five-set, its edge count, its
deficiency, and its maximum degree.  The final witnesses have

```text
d       18  19  20  21  22  23  24
edges   79  92  98 101 108 119 126
delta    6   0   2   6   6   3   6
Delta    9  10  10  10  10  11  11
```

Thus any improvement must use additional global coupling, local isomorphism
type, or constraints between several partners.  This is a branch-complete
search reduction with exact limitation witnesses, not an exclusion of the
low-deficiency branch and not an `R(5,5;43)` construction.

## Reproduction

With CPython 3.11 or newer and no third-party dependency:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py | cmp - EXPECTED_TEST_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 independent_networkx_check.py \
  | cmp - EXPECTED_NETWORKX_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The optional primary-catalog audit uses the five files linked by Brendan
McKay's catalog page:

```bash
for q in 9 10 11 12 13; do
  curl -L --fail --silent --show-error \
    "https://users.cecs.anu.edu.au/~bdm/data/r35_${q}.g6" \
    -o "/tmp/r35_${q}.g6"
done
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --catalog-dir /tmp \
  | cmp - EXPECTED_CATALOG_OUTPUT.txt
```

The audit requires the pinned file hashes, all 721 record counts, their
orders, triangle-freeness, and absence of independent five-sets.

## Sources and trust boundary

- V. Angeltveit and B. D. McKay, *R(5,5) <= 46*,
  [arXiv:2409.15709v2](https://arxiv.org/abs/2409.15709), describes the
  near-extremal local-graph/gluing method and records the current `(4,5)`
  census.
- V. Angeltveit and B. D. McKay, *R(5,5) <= 48*,
  [arXiv:1703.08768v2](https://arxiv.org/abs/1703.08768), completed the
  extremal `(4,5;24)` catalog.
- B. D. McKay's [primary Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  supplies the `(3,5)` and edge-extremal `(4,5)` graph6 files.

The displayed averaging proof and cell partition are human-checkable.  The
checker uses exact CPython integers and exhaustive subset tests for the seven
embedded limitation witnesses.  NetworkX 3.6 supplies a second graph6 decoder
and maximal-clique algorithm for the same witnesses.  The optional catalog audit checks each
record's defining property, but the completeness and nonisomorphism of the
primary catalogs and the classical theorem `R(3,5)=14` remain external trust
boundaries.  Ordinary Python/NetworkX semantics and SHA-256 are used for provenance.  The timed-out exploratory
43-vertex SAT calculations are not included and support no claim.
