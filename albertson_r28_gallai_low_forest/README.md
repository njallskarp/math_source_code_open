# Gallai low-forest compression at the Albertson r=28 frontier

This directory combines the classical low-vertex theorem for critical graphs
with the two singleton components in the height-2583 separator profile.

## Theorem

Let `G` be a 28-critical graph on 55 vertices satisfying the height-2583
separator conclusion.  Put

    x_v = d_G(v)-27,
    L = G[{v:x_v=0}].

Then:

1. The four profiles with 52 low vertices are impossible.  Explicitly, this
   eliminates

       row 768: 0^52 1 25^2,       0^52 2 24 25;
       row 769: 0^52 3 25^2,       0^52 4 24 25.

2. The four profiles with 51 low vertices are also impossible.  Their edge
   floor first forces `L` to contain a unique `K_26` block and then a disjoint
   `K_25` block, but those blocks have at least 625 edges whereas the degree
   identity permits at most 615.

Consequently row 768 is eliminated outright.  The height-2583 row-769 list
compresses from eight profiles to exactly these three unresolved profiles:

    0^50 1^3 25^2,
    0^50 1^2 2 24 25,
    0^49 1^4 24 25.

## Proof

Gallai's theorem says that the subgraph induced by the degree-`k-1` vertices
of a `k`-critical graph is a Gallai forest: every block is a clique or an odd
cycle.  Here those are precisely the excess-zero vertices.

Let `W={w_1,w_2}` be the two singleton components of `H-B`, where
`H=complement(G)`.  They have no `H`-edge between them and no `H`-edge to the
49-vertex component `C`.  Thus `w_1w_2` is a `G`-edge and both vertices are
joined in `G` to all of `C`.

Every clique block of `L` has size at most 26.  Indeed, a larger block contains
a low vertex of `C` because `B` has only four vertices.  Such a vertex would
have at least 26 neighbors in the block and both neighbors in `W`, contradicting
its total degree 27.

There is at most one `K_26` block.  Each such block contains at least 22 low
vertices of `C`.  Every one of them already has its 25 block neighbors and
both vertices of `W`, so it is nonadjacent in `G` to every other high vertex.
There is at least one such high vertex `z`, and `d_H(z)<=26`.  Two `K_26`
blocks would give `z` at least 44 distinct neighbors in `H`, a contradiction.

For a Gallai forest with `c` components, the block identity is

    |V(L)| = c + sum_Q (|Q|-1).

Write `u_Q=|Q|-1`.  A clique block contributes `u_Q(u_Q+1)/2` edges, while an
odd-cycle block contributes no more than that.  Convexity therefore gives the
following relaxed maxima:

    |V(L)|=52, at most one K_26:  325+300+3 = 628;
    |V(L)|=51, no K_26:           300+300+3 = 603.

These bounds even relax block-tree realizability and vertex degrees.

On the other hand, if `R=V(G)-V(L)`, the degree identity and the forced edge
`w_1w_2` give

    e(L) = m - sum_{v in R} d_G(v) + e(G[R])
         >= m - sum_{v in R}(27+x_v) + 1.

For every 52-low profile this floor is 637 at row 768 or 636 at row 769,
contradicting 628.

For every 51-low profile the floor is at least 609, which exceeds 603 and
therefore forces the unique `K_26`.  If there were no `K_25` block, the same
convex packing, now with remaining increments at most 23, would give

    e(L) <= 325+276+3 = 604,

again below 609.  Hence a `K_25` block is also present.  It cannot share a cut
vertex with the `K_26`, since that vertex would have internal degree at least
`25+24=49`; so the two blocks are disjoint and contribute at least
`325+300=625` edges.  The exact degree identity also gives the upper bound

    e(L) <= m - sum_{v in R}(27+x_v) + binom(4,2),

which is 615 on row 768 and 614 on row 769.  This contradiction eliminates
all four 51-low profiles.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_gallai_low_forest
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 audit.py | diff -u EXPECTED_AUDIT.txt -
shasum -a 256 -c SHA256SUMS
```

The primary checker performs an exact dynamic-programming optimization over
all block-increment partitions and all eleven profiles.  The independent
audit evaluates the two extremal partitions and degree floors in closed form.

## Provenance and trust boundary

The low-vertex theorem is due to Tibor Gallai, *Kritische Graphen, II*, 1963,
pp. 373--395; a scan is maintained by the Repository of the Hungarian Academy
of Sciences at <https://real.mtak.hu/201455/>.  A modern primary-source
statement appears as Theorem 1.3 in Kostochka--Rabern--Stiebitz,
<https://kostochk.web.illinois.edu/docs/accepted/dm-rs.pdf>.

The block packing, degree identity, and profile eliminations are unconditional
under the stated separator/profile hypotheses.  Applying them to all possible
Albertson counterexamples remains review-gated on the height-2569 finite
component classification inherited by height 2583.  The height-2583 local
singleton-triangle lemma has a Lean formalization at height 2599, but that
formalization explicitly does not check the finite classification.

The checkers use exact Python integers, deterministic finite dynamic
programming, and SHA-256.  They do not re-prove Gallai's theorem, the
height-2569/2583 separator classification, the published crossing estimates,
Stehlik's factor-criticality theorem, or drawing topology.  No `r=27` terminal
theorem, `cr(24,132)>=165`, local crossing conjecture, solver, floating point,
or labeled graph enumeration is used.
