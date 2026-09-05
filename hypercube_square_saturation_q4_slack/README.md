# A strict Q4 compatibility slack for square-saturated hypercubes

Let `Q_d` be the `d`-dimensional hypercube, and let
`sat(Q_d,Q_2)` be the minimum number of edges in a square-saturated spanning
subgraph.  This note proves the following strict improvement of the local
three-cube lower-bound method.

## Theorem

For every integer `d >= 4`,

```text
sat(Q_d,Q_2) >= 504 d 2^d / (287 d + 721).
```

Consequently,

```text
liminf_(d -> infinity) sat(Q_d,Q_2) / 2^d >= 504/287
                                                     > 7/4.
```

The inequality is real-valued; an integer lower bound is obtained by taking
the ceiling.  This does not determine `sat(Q_7,Q_2)`: both the old and new
bounds round to 166 there.

## 1. The inherited three-cube slack

Fix a square-free edge set in `Q_3`.  A square is *active* when exactly three
of its edges are selected.  Write

- `t` for the number of active squares;
- `r` for the number of distinct missing edges of those squares;
- `q=t-r`;
- `b` for the selected-edge incidences on inactive squares.

The six square faces have adjacency graph `K_{2,2,2}`.  The local lemma from
the reviewed dependency is

```text
sigma := b + 2q - t/2 >= 0.                         (1)
```

We need its equality cases, which also follow directly from that proof.  If
`t=0`, equality forces `b=0`, hence the edge set is empty.  For `t=1,2,3`,
the minimum face-boundary sizes `4,6,6` make (1) strict.  For `t=5`, the face
opposite the unique inactive face forces `q>=1`; for `t=6`, `q=3`; these cases
are strict as well.  Thus every nonempty equality pattern has

```text
(t,q,b)=(4,0,2).
```

Its selected-edge count is seven: the six squares contain
`3t+b=14` selected-edge incidences, and every cube edge lies in two squares.
Therefore:

```text
sigma=0  iff  the Q3 pattern is empty or is a seven-edge equality pattern.
                                                               (2)
```

The verifier enumerates the 4,096 labeled `Q_3` edge sets and independently
checks that there are 49 equality patterns: the empty pattern and 48 labeled
seven-edge patterns.

## 2. Strict compatibility in Q4

Consider a nonempty square-free edge set `F` in `Q_4`.  Suppose all eight
three-dimensional facets had zero slack.  By (2), each facet is empty or has
seven selected edges.  If `k` facets are nonempty, count incidences between
selected edges and facets.  Every `Q_4` edge lies in exactly three facets, so

```text
7k = 3|F|.                                           (3)
```

Since `1 <= k <= 8`, equation (3) leaves only `k=3` or `k=6`.

If `k=3`, a selected edge would have to lie in all three nonempty facets.  If
two are opposite there is no such edge; otherwise three compatible facets
with distinct fixed coordinates intersect in exactly one edge.  Thus
`|F|<=1`, contradicting (3), which requires `|F|=7`.

If `k=6`, there are two empty facets, and every selected edge must avoid both.
If they are opposite facets in one coordinate, only the eight edges in that
coordinate avoid them.  If their fixed coordinates are distinct, the two
corresponding edge directions contribute at most four edges each, and each of
the other two directions contributes at most two, for a total of at most 12.
Both bounds contradict (3), which requires `|F|=14`.

Hence at least one facet has positive slack.  Since `2 sigma` is an integer,

```text
sum_(C a Q3 facet of H) sigma(C) >= 1/2              (4)
```

for every nonempty square-free four-cube `H`.

## 3. Global double count

Let `G` be square-saturated in `Q_d`, `d>=4`, and put

```text
N=d 2^(d-1),  E=|E(G)|,  M=N-E.
```

Let `T` be the number of active squares.  For an omitted edge `e`, let `w(e)`
be its number of active-square witnesses.  Set

```text
A=T-M,
B=(d-1)E-3T,
P=sum_e binom(w(e),2),
D=(d-1)A-2P=sum_e (w(e)-1)(d-1-w(e)).
```

Saturation gives `A>=0`; incidence counting gives `B>=0`; and
`1<=w(e)<=d-1` gives `D>=0`.  We also have

```text
B+3A=(d-1)E-3M.                                     (5)
```

Sum `sigma` over all three-subcubes and call the result `S`.  Every square is
in `d-2` three-subcubes, and every pair of witnesses for the same omitted edge
spans a unique three-subcube.  Therefore

```text
S=(d-2)B+2P-(d-2)T/2.                               (6)
```

Let `X` be the number of four-subcubes containing a selected edge.  Every
selected edge is in `binom(d-1,3)` four-subcubes.  A square-free edge set in
`Q_4` has at most 24 edges: its 24 squares contain at most three selected edges
each, while every edge is counted in three squares.  Consequently

```text
X >= E binom(d-1,3)/24.                              (7)
```

Each three-subcube is a facet of `d-3` four-subcubes.  Summing (4) and using
(7) gives

```text
(d-3)S >= X/2,
S >= E(d-1)(d-2)/288.                               (8)
```

Equations (6) and the definition of `D` yield

```text
(d-2)(B+3A)
 = (d-2)T/2 + S + D + (2d-5)A
 >= (d-2)M/2 + S.
```

Together with (8),

```text
B+3A >= M/2 + E(d-1)/288.                           (9)
```

Combining (5) and (9), then substituting `M=N-E`, gives

```text
287(d-1)E >= 1008M,
(287d+721)E >= 1008N,
E >= 504 d 2^d/(287d+721).
```

This proves the theorem.

## Reproduction

Requires CPython 3.12 or later and no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
shasum -a 256 -c SHA256SUMS
```

`verify.py` uses exact integers and rational numbers.  It checks the complete
labeled `Q_3` local table, reconstructs all globally compatible selections of
local equality patterns on the eight `Q_4` facets, and separately verifies the
facet-capacity certificate used in the human proof.  These finite checks
corroborate the local ingredients; the all-`d` theorem is the displayed
combinatorial argument.

## Trust boundary and scope

The universal result trusts the human incidence and double-counting proof.
The checker trusts CPython and this source, uses no solver, floating point,
randomness, external data, generated certificate, or omitted search, and does
not by itself prove the universal quantifiers.  The result strengthens only a
lower bound for square saturation; it supplies no new construction or exact
value.

## Literature boundary

Johnson and Pinto introduced the modern `(Q_d,Q_m)` saturation framework,
proved `sat(Q_d,Q_2)=O(2^d)`, and obtained the earlier semisaturation lower
bound.  Morrison, Noel, and Scott proved `sat(Q_d,Q_m)=Theta(2^d)` for fixed
`m`.  Choi and Guan studied the earlier critical-squarefree problem.  A focused
primary-source search on 2026-09-05 found no `7/4` lower bound, `504/287`
constant, or this `Q_4` compatibility argument.  This is a search-relative
novelty assessment, not a historical-priority claim.

- J. R. Johnson and T. Pinto, *Saturated Subgraphs of the Hypercube*,
  <https://arxiv.org/abs/1406.1766>.
- N. Morrison, J. A. Noel, and A. Scott, *Saturation in the Hypercube and
  Bootstrap Percolation*, <https://arxiv.org/abs/1408.5488>.
- S.-Y. Choi and P. Guan, *Minimum critical squarefree subgraph of a
  hypercube*, *Congressus Numerantium* 189 (2008), 57–64,
  <https://combinatorialpress.com/cn/vol189/>.
