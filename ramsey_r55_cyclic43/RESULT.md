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

The bound is sharp for the closed ball because each center itself has exactly
two monochromatic `K5`s. Explicit perturbations also show sharpness at every
exact radius one, two, and three; the radius-four through radius-six computation
is a lower-bound search and does not claim an exact-radius witness at those
three distances.

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

Context for the current `43 <= R(5,5) <= 46` range and modern computational
methods is provided by Angeltveit and McKay,
[`R(5,5) <= 46`](https://doi.org/10.1002/jgt.70029). Authoritative Ramsey graph
data are maintained on Brendan McKay's
[Ramsey graphs data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
