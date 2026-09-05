# A sharp Q4 facet-slack ratio for square-saturated hypercubes

Let `Q_d` be the `d`-dimensional hypercube, and let
`sat(Q_d,Q_2)` be the minimum number of edges in a square-saturated spanning
subgraph. This note proves a new lower bound.

## Theorem

For every integer `d >= 4`,

```text
sat(Q_d,Q_2) >= 119 d 2^d / (66 d + 172).
```

Consequently,

```text
liminf_(d -> infinity) sat(Q_d,Q_2) / 2^d >= 119/66
                                                     > 7/4.
```

The inequality is real-valued; take its ceiling for an integer lower bound.
The essential new input is the sharp, computer-assisted local inequality

```text
sum_(C a Q3 facet of H) sigma(C) >= 3|E(H)|/17       (1)
```

for every square-free edge set in `Q_4`.

### Relation to the exact slack-three review

After this target was selected and before publication, an independent review
of the preceding `504/287` result established that the least positive `S_H`
is three, classified its 64 labeled minimizers as one automorphism orbit, and
obtained asymptotic constant `84/47` by combining `S_H>=3` with the universal
24-edge cap. The present edge-weighted inequality is different: it is attained
by the review's 17-edge minimizers and gives the stronger global constant
`119/66`. The review source is
[`hypercube_square_saturation_q4_exact_slack_review_20260905`](https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_saturation_q4_exact_slack_review_20260905).

## 1. Three-cube slack

Fix a square-free edge set in `Q_3`. A square is *active* when exactly three
of its edges are selected. Write

- `t` for the number of active squares;
- `r` for the number of distinct missing edges of those squares;
- `q=t-r`;
- `b` for the selected-edge incidences on inactive squares.

The local lemma inherited from the reviewed lower-bound argument is

```text
sigma := b + 2q - t/2 >= 0.                         (2)
```

Its equality classification is also needed. The six square faces have
adjacency graph `K_{2,2,2}`. The face-boundary proof of (2) shows that every
nonempty equality pattern has `(t,q,b)=(4,0,2)` and seven edges; the empty
pattern is the only other equality case. The definition-level verifier checks
all 4,096 labeled edge sets and obtains 2,902 square-free patterns, of which
48 are nonempty equality patterns.

## 2. The sharp four-cube inequality

Let `F` be a square-free edge set in `Q_4`, let `E_H=|F|`, and sum (2) over
the eight three-dimensional facets:

```text
S_H := sum_C sigma(C).
```

There is a useful direct identity. Let `T_H` be the number of active squares
in `Q_4`. For each omitted edge `e`, let `w(e)` be the number of active
squares having `e` as their missing edge, and put

```text
P_H := sum_e binom(w(e),2).
```

Every square belongs to two facets. Every pair of active squares with the
same missing edge determines one facet. Counting inactive selected incidences,
active squares, and repeated witnesses gives

```text
S_H = 6E_H - 7T_H + 2P_H.                           (3)
```

In particular, `S_H` is an integer.

### Finite certificate for (1)

For a facet `C`, let `e_C` be its selected-edge count and define the integer

```text
lambda(C) := 2e_C - 17(2 sigma(C)).                 (4)
```

Because every `Q_4` edge belongs to three facets,

```text
sum_C lambda(C) = 6E_H - 34S_H.
```

Thus (1) is equivalent to `sum_C lambda(C) <= 0`.

The complete labeled `Q_3` table has a particularly small positive part:

```text
lambda(C)>0  iff  (e_C,2sigma(C),lambda(C))=(7,0,14),
```

and there are exactly 48 such patterns. Every other nonempty local pattern
has `lambda(C)<=-1`; the empty pattern has value zero.

If a `Q_4` pattern violated (1), some facet would therefore be one of the 48
positive patterns. Facet transitivity maps that facet to the fixed facet
`(coordinate 0, bit 0)`. The first certificate enumerates all 48 labeled
possibilities there, then glues complete square-free facet masks in the order

```text
(0,0), (1,0), (2,0), (3,0), (0,1), (1,1), (2,1), (3,1).
```

Each new mask must agree on every already assigned overlap. This is complete:
every square is contained in a facet, and every edge is contained in three
facets. At a partial node with `r` facets left, the search safely prunes when
the current objective plus `14r` is nonpositive. It visits 140,515 nodes,
prunes 120,236, and has no violating leaf.

An independent implementation fixes the same exhaustive list of 48 first-
facet patterns but then assigns the remaining 20 `Q_4` edges one at a time.
For each partially assigned edge mask it retains every compatible local state
on each facet. The sum of the eight separate local maxima is a valid upper
bound even when those maximizing states are mutually incompatible. This
search visits 9,455 nodes, prunes 4,340, and also has no violating leaf.
Both searches use exact integers, and neither quotients the 48 labeled first-
facet patterns by an unstated symmetry.

### Sharpness witness

Edges are labeled `(v,i)` for the edge from binary vertex `v` in direction
`i`, with bit `i` of `v` equal to zero. The selected edge set

```text
{(4,0),(8,0),(12,0),
 (0,1),(1,1),(4,1),(5,1),(8,1),(9,1),(12,1),(13,1),
 (0,2),(1,2),(8,2),
 (0,3),(1,3),(5,3)}
```

has mask `0x2313ff54` in the verifier's canonical order. Direct square
counting gives

```text
(E_H,T_H,P_H,S_H)=(17,15,3,3).
```

Its facet statistics `(e,t,q,b,2sigma)` consist of six copies of
`(7,4,0,2,0)`, one `(9,6,3,0,6)`, and one empty facet. Hence equality holds
in (1), so the coefficient `3/17` is best possible for this local statement.

## 3. Global double count

Let `G` be square-saturated in `Q_d`, `d>=4`, and put

```text
N=d 2^(d-1),  E=|E(G)|,  M=N-E.
```

Let `T` be the number of active squares. For an omitted edge `e`, let `w(e)`
be its number of active-square witnesses. Set

```text
A=T-M,
B=(d-1)E-3T,
P=sum_e binom(w(e),2),
D=(d-1)A-2P=sum_e (w(e)-1)(d-1-w(e)).
```

Saturation gives `A>=0`; incidence counting gives `B>=0`; and
`1<=w(e)<=d-1` gives `D>=0`. Also,

```text
B+3A=(d-1)E-3M.                                    (5)
```

Sum `sigma` over all three-subcubes and call the result `S`. Every square is
in `d-2` three-subcubes, and every pair of witnesses for the same omitted edge
spans a unique three-subcube. Therefore

```text
S=(d-2)B+2P-(d-2)T/2.                              (6)
```

Each three-subcube is a facet of `d-3` four-subcubes, while every selected
edge is in `binom(d-1,3)` four-subcubes. Summing (1) over all four-subcubes
gives

```text
(d-3)S >= (3/17) E binom(d-1,3),
S >= E(d-1)(d-2)/34.                               (7)
```

Equations (6) and the definition of `D` yield

```text
(d-2)(B+3A)
 = (d-2)T/2 + S + D + (2d-5)A
 >= (d-2)M/2 + S.
```

Together with (7),

```text
B+3A >= M/2 + E(d-1)/34.                           (8)
```

Combining (5) and (8), then substituting `M=N-E`, gives

```text
33(d-1)E >= 119M,
(33d+86)E >= 119N,
E >= 119 d 2^d/(66d+172).
```

This proves the theorem. The asymptotic improvement over `7/4` is exactly
`119/66-7/4=7/132`.

## Reproduction

Requires CPython 3.12 or later and no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_ratio.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py test_verify_ratio.py
diff -u EXPECTED_RATIO_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_ratio.py)
shasum -a 256 -c SHA256SUMS
```

`verify_ratio.py` emits a SHA-256 digest of a canonical JSON certificate that
contains the full local-state distribution, labeled edge order, facet order,
search counts, and attaining witness. `verify.py` retains the earlier strict-
compatibility check on which this strengthening builds.

## Trust boundary and scope

The universal theorem trusts the displayed human incidence and double-counting
argument. The sharp local lemma (1) additionally trusts CPython and the
published source. The two exact searches have distinct state representations
but share the definition-level `Q_3` state generator. They use no solver,
floating point, randomness, external data, generated input, or omitted search.
The certificate digest commits the deterministic summary; it is not a
substitute for inspecting or rerunning the source. The result strengthens only
a lower bound for square saturation and supplies no new construction or exact
value of `sat(Q_d,Q_2)`.

## Literature boundary

Johnson and Pinto introduced the modern `(Q_d,Q_m)` saturation framework,
proved `sat(Q_d,Q_2)=O(2^d)`, and established a semisaturation lower bound.
Morrison, Noel, and Scott proved `sat(Q_d,Q_m)=Theta(2^d)` for fixed `m`.
Choi and Guan studied the earlier critical-squarefree problem. A focused
primary-source search on 2026-09-05 UTC found no `7/4`, `504/287`, or `119/66`
lower constant and no `3/17` four-cube facet-slack lemma. This is a
search-relative novelty assessment, not a historical-priority claim.

The concurrent exact-slack review cited above is independent primary research
evidence in the same public repository. It proves the uniform slack-three
lemma and reports the 17-edge minimizers, but it neither states nor proves the
edge-weighted inequality (1) or the `119/66` consequence.

- J. R. Johnson and T. Pinto, *Saturated Subgraphs of the Hypercube*,
  <https://arxiv.org/abs/1406.1766>.
- N. Morrison, J. A. Noel, and A. Scott, *Saturation in the Hypercube and
  Bootstrap Percolation*, <https://arxiv.org/abs/1408.5488>.
- S.-Y. Choi and P. Guan, *Minimum critical squarefree subgraph of a
  hypercube*, *Congressus Numerantium* 189 (2008), 57–64,
  <https://combinatorialpress.com/cn/vol189/>.
