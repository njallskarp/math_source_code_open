# Exact constrained multiplicity of `Cyclic(43)`

## Computational theorem

Let `Cyclic(43)` be the red/blue coloring of `K43` whose red chord lengths are

```text
1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21.
```

Among every coloring obtained by changing an arbitrary subset of its red edges
to blue, the exact minimum number of monochromatic copies of `K5` is **2**.

This resolves the first question in Section 7 of Ge, Jayasooriya, Qiu, Sun, and
Yuan, *Study of Exoo's Lower Bound for Ramsey number R(5,5)*,
[arXiv:2212.12630v3](https://arxiv.org/abs/2212.12630), within precisely the
red-to-blue perturbation family stated there. It does not determine the global
Ramsey multiplicity of `K5` and does not determine `R(5,5)`.

## Exact encoding

There are 473 initially red edges. Associate a Boolean variable `x_e` to each,
where `x_e = 1` means that edge `e` is changed to blue. For each five-vertex set
`S`, let `R(S)` be the initially red edges induced by `S`.

- `S` is blue after the changes exactly when every `x_e` for `e` in `R(S)` is
  true. The unit soft clause `OR(-x_e : e in R(S))` is violated exactly then.
- The seed has exactly 43 red copies of `K5`. For each such `S`, the additional
  unit soft clause `OR(x_e : e in R(S))` is violated exactly when it stays red.

The seed has no blue `K5`, so `R(S)` is nonempty for every `S`. The resulting
formula has 473 variables and 962,641 unit-weight soft clauses: one possible
blue state for each of the 962,598 five-sets and one red state for each of the
43 seed red cliques. Its MaxSAT cost is therefore identically the number of
monochromatic `K5`s, not merely a bound or proxy.

## Upper-bound certificate

The primary certificate changes these 18 length-one edges to blue:

```text
(0,1), (1,2), (2,3),
(8,9), (9,10), (10,11), (11,12),
(17,18), (18,19), (19,20),
(25,26), (26,27), (27,28), (28,29),
(34,35), (35,36), (36,37), (37,38).
```

Direct enumeration of all 962,598 five-sets finds no blue `K5` and exactly two
red ones:

```text
(0,20,21,22,42)
(0,20,21,41,42)
```

The solver-free `--verify` mode independently performs this recount from
[`certificate.json`](certificate.json).

## Lower-bound computation and replication

Two exact core-guided MaxSAT runs returned optimum 2 and produced different
optimal colorings:

1. PySAT RC2 with the Glucose 4 backend and adaptation enabled.
2. PySAT Fu-Malik/WMSU1 with the MiniSat 2.2 backend.

The second result is stored in [`certificate-fm.json`](certificate-fm.json); its
coloring has no red `K5` and exactly two blue `K5`s. Both certificates were then
recounted with the solver-free verifier.

The upper bound of 2 is independently checkable using only Python's standard
library. Optimality relies on the two PySAT MaxSAT runs. They use distinct
MaxSAT algorithms and SAT backends but share the PySAT formula construction and
do not emit a standalone DRAT/LRAT proof; this is the remaining computational
trust boundary.

## Relevance and novelty scope

The 2023 source posed the constrained minimum as an open question and mentioned
an unpublished two-clique `K43` coloring without claiming optimality in this
family. Searches of arXiv, the authors' data page, and public source repositories
did not locate a prior exact resolution of the stated perturbation problem.
Accordingly, this result is described as **apparently new to the searched
sources**, not as a priority claim.

The result rules out the entire monotone red-to-blue neighborhood of this major
42-vertex construction as a route to a zero-clique coloring on 43 vertices. The
two optimal certificates are also concrete near-solutions for future searches
that allow blue-to-red changes and other non-monotone moves.

## Exact unrestricted local rigidity through radius six

The next search layer allows arbitrary edge reversals, including blue-to-red
changes. Both structurally different optimum-2 certificates are locally rigid:

> Every coloring at Hamming distance at most six from either certificate has
> at least two monochromatic copies of `K5`.

The bound is sharp on every individual sphere of radius one through six. The
geodesic bridge below supplies an explicit two-clique coloring at each exact
radius, while the exhaustive computation supplies the matching lower bound.

For each base coloring, the two original monochromatic cliques contain 14
distinct edges. Any improving perturbation must touch at least one of those
edges; otherwise both original cliques survive. This reduces the exact search to
all 903 single-edge changes, 12,537 improvement-relevant two-edge changes, and
5,607,287 improvement-relevant three-edge changes.

The computation enumerates all five-sets once and uses the exact Boolean
inclusion-exclusion expansion of the clique-count function:

```text
M(T) = M(empty)
     + sum(single-edge deltas)
     + sum(pair interactions)
     + sum(triple interactions),
```

which is exact for `|T| <= 3`. A minimizing perturbation from each run is then
recounted directly over all 962,598 five-sets. The persisted results are:

- [`local-rigidity-primary.json`](local-rigidity-primary.json)
- [`local-rigidity-fm.json`](local-rigidity-fm.json)
- [`local-rigidity-radius3-primary.json`](local-rigidity-radius3-primary.json)
- [`local-rigidity-radius3-fm.json`](local-rigidity-radius3-fm.json)

This is a local exclusion result, not evidence that no distant one-clique or
zero-clique coloring exists. Its practical implication is that a successful
non-monotone search cannot make a shallow repair of either optimum: it must leave
both Hamming balls of radius six.

### Forced-witness search for radii four through six

For a partial edge-reversal set `T`, suppose its coloring has at least two
monochromatic witnesses `A` and `B`. Any extension of `T` that ends with at most
one monochromatic `K5` must reverse an as-yet unchanged edge in
$E(A) \cup E(B)$: otherwise both witnesses survive. With a total radius at most six, an
extension cannot reverse all ten currently equal-colored edges of a witness and
make it monochromatic in the other color. Branching on this at-most-20-edge
hitting set at every state is therefore exhaustive. States reached in different
orders are memoized by their sorted reversal sets.

For the primary certificate, the radius-six search expanded 5,192,120 distinct
depth-six states and considered 6,797,733 candidate branches in total. For the
Fu-Malik certificate it expanded 5,261,019 distinct depth-six states and
considered 6,548,804 branches. Neither search found a coloring with zero or one
monochromatic `K5`; since the centers have two, the exact minimum in each closed
radius-six ball is two. The C++ source is
[`local_rigidity_bounded.cpp`](local_rigidity_bounded.cpp), with persisted
outputs in [`local-rigidity-radius6-primary.json`](local-rigidity-radius6-primary.json)
and [`local-rigidity-radius6-fm.json`](local-rigidity-radius6-fm.json).

SHA-256 digests:

```text
e7ea42ffcef7c23b00336cbdb27f12203ee2e0ad93afd2a8d6093fe0071ce308  local_rigidity_bounded.cpp
a0addcbe7aaae06ac3d67aec330d191ce393ce4423993a642efabffc1d4a4233  local-rigidity-radius6-primary.json
37c0a740ac7ee06a9fb20204ade77f323781a9528f4596aefe57f5b5315e6131  local-rigidity-radius6-fm.json
```

### A geodesic optimum-plateau bridge

The primary and Fu-Malik optimum certificates differ on exactly 15 edges. There
is an ordering of those 15 reversals for which every intermediate coloring has
exactly two monochromatic copies of `K5`:

```text
(30,31), (9,10), (4,5), (26,27), (21,22),
(0,1), (38,39), (17,18), (12,13), (34,35),
(29,30), (8,9), (3,4), (25,26), (20,21).
```

Since the path length equals the Hamming distance, it is geodesic. Every edge
in the bridge has cyclic length one. Direct enumeration of all 962,598
five-sets at each of the 15 steps confirms a monochromatic count of two and
confirms that the endpoint is exactly the primary certificate. Consequently:

- the exact minimum on every individual Hamming sphere of radius one through
  six around either certificate is two;
- the two apparently different MaxSAT optima lie in the same
  single-edge-connected component of the optimum-2 coloring plateau;
- the monochromatic defect pair can be transported through the coloring by
  length-one reversals without increasing the objective.

The bridge and its witnesses are stored in
[`plateau-bridge.json`](plateau-bridge.json), generated by
[`plateau_path.py`](plateau_path.py). Searches of the cited primary paper and
official Ramsey data did not locate this local-landscape description, so it is
reported as apparently new to the searched sources rather than as a priority
claim.

```text
891d364aa10305efa6b0c78b62a420aad73f161018c37c1a56118dda3037d9cc  plateau_path.py
2166af94a8646525095c28936abe29d10fc2c2885fc78c0777a3c1eb1e3200cf  plateau-bridge.json
ae755d23c0ee09a38c94f90f58201339735bf9231cb8f97af9660a2bb2d42c2c  defect-orbit-primary.json
```

### A maximal 37-step neutral defect orbit

Starting from the primary certificate, the constant-two transport continues
for 37 distinct length-one reversals. Write $e_i=\{i,i+1\}$ with indices modulo
43. The reversed edge positions have the closed form

$$
p_{2k}=42+17k \pmod {43},\qquad
p_{2k+1}=37+17k \pmod {43}.
$$

The 19 even-indexed and 18 odd-indexed positions are individually distinct
because 17 is invertible modulo 43. An overlap would require
$a-b\equiv-18\pmod {43}$ with $0\leq a\leq18$ and $0\leq b\leq17$, which is
impossible. Thus the first 37 positions are distinct. The next prescribed
position is

$$
p_{37}=37+17\cdot18\equiv42=p_0\pmod {43},
$$

so the neutral transport asks to reuse its first edge.

Exact enumeration confirms two monochromatic `K5`s after each of the 37
reversals. At the terminal coloring, all 866 unused edges were tested. None
preserves a count of two: the minimum is four, attained uniquely by `(21,22)`.
Thus this is a maximal Hamming-increasing constant-two path under the specified
transport rule, and its endpoint has a strict barrier in every unused-edge
direction. It is not a proof that no other constant-two path can branch earlier.

The compact recurrence, terminal witnesses, and complete unused-edge count
histogram are in
[`defect-orbit-primary.json`](defect-orbit-primary.json). The separate
globally-best one-step probe chooses the unique four-clique exit and then rises
through counts 7, 10, 13, 15, and 17 over its next five steps; this is a search
diagnostic, not an optimal barrier theorem.

### Radius-five exclusion tube around the 37-edge defect orbit

The forced-witness search was run independently through radius five around all
38 vertices of the maximal neutral defect orbit. Every center has exact
closed-ball minimum two. Consequently, any coloring with zero or one
monochromatic `K5` is at Hamming distance at least six from every orbit vertex.

The overlap count uses the following general prefix-chain lemma. Let

$$
C_L=\{1^k0^{L-k}:0\leq k\leq L\}\subseteq\{0,1\}^L.
$$

The number of words at distance exactly $d$ from $C_L$ is

$$
h_L(d)=(L-2d+1)\left(\binom Ld-\binom L{d-1}\right),
\qquad 0\leq d\leq\lfloor L/2\rfloor,
$$

where $\binom L{-1}=0$. To prove this, let a word have $s$ ones and let
$Y_k$ be the number of ones minus zeros in its first $k$ positions. Its
distance to the $k$th prefix is $s-Y_k$, so its distance from $C_L$ is
$s-\max_kY_k$. For fixed $d$ and $s$, the required walk maximum is $s-d$.
The reflection principle gives
$\binom Ld-\binom L{d-1}$ such walks, independently of $s$, and the admissible
values are exactly $d\leq s\leq L-d$. This proves the formula. Brute-force
enumeration for every $L\leq12$ independently checks the implementation.

For the defect orbit, $L=37$ and the other $903-37=866$ edge coordinates are
independent. Hence the exact tube size is

$$
\sum_{d=0}^{5}h_{37}(d)\sum_{j=0}^{5-d}\binom{866}{j}
=186{,}056{,}295{,}651{,}406.
$$

This is about 37.39 times one radius-five ball after overlaps are removed. The
38 searches considered 20,061,001 candidate branches and expanded 16,294,833
distinct depth-five states in total. Per-center data are stored in
[`defect-orbit-tube-radius5.json`](defect-orbit-tube-radius5.json), generated by
[`defect_orbit_tube.py`](defect_orbit_tube.py). The prefix-chain formula is a
general combinatorial lemma; no priority claim is made for it. The computational
result is a local exclusion theorem around one path, not a global bound for all
colorings of `K43`.

```text
bc6fe77f30ad114d1a8e52b836ed76f9b603527abf3dfacd572ac08649975a97  defect_orbit_tube.py
c386b14fe48a8c3213ec85e0b37fcf520cf54f4f758f38249e5deae72fb03ef1  defect-orbit-tube-radius5.json
```

### Radius-six exclusion tube around the optimum bridge

The forced-witness search was run independently through radius six around all
16 vertices of the geodesic bridge. Every center has exact closed-ball minimum
two. Therefore any coloring with zero or one monochromatic `K5` lies at Hamming
distance at least seven from every bridge vertex.

The union size can be counted without enumerating its colorings. Separate the
15 bridge coordinates from the other 888 edge coordinates. For a subset $A$ of
the bridge coordinates, let $d(A)$ be its minimum distance to one of the 16
prefixes along the geodesic. The distribution of $d(A)$ over all $2^{15}$
subsets is

```text
d       0    1     2     3     4     5     6     7
count  16  196  1080  3500  7280  9828  8008  2860
```

Hence the number of distinct colorings in the radius-six tube is

$$
\sum_{A\subseteq[15]}\ \sum_{j=0}^{6-d(A)}\binom{888}{j}
=11{,}711{,}422{,}789{,}686{,}316.
$$

A single radius-six ball in the 903-dimensional coloring cube has
$745{,}544{,}064{,}249{,}503$ vertices, so the tube covers about 15.71 times that
volume after overlaps are removed. The 16 searches considered 108,834,738
candidate branches in total. Full per-center counts and the overlap certificate
are in [`bridge-tube-radius6.json`](bridge-tube-radius6.json), generated by
[`bridge_tube.py`](bridge_tube.py). This is a local exclusion theorem, not a
global lower bound on the number of monochromatic cliques in all `K43`
colorings.

```text
8a3e59b426f52ebe51c75bfccb7c9b380038abe8b88f4820b2f3967573e67ed7  bridge_tube.py
5a9998cddebc2dc9a73bd6dc2c71d71047191d9ded10e7bd87bb3fb2c48e48fb  bridge-tube-radius6.json
```

Context for the current `43 <= R(5,5) <= 46` range and modern computational
methods is provided by Angeltveit and McKay,
[`R(5,5) <= 46`](https://doi.org/10.1002/jgt.70029). Authoritative Ramsey graph
data are maintained on Brendan McKay's
[Ramsey graphs data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
