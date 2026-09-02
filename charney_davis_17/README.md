# The 17-vertex Charney--Davis admissible-edge obstruction

This Lean project checks the exact algebraic and graph-theoretic interfaces in
an admissible-edge approach to the first vertex-count boundary not covered by
the known small-`gamma_1` results for flag generalized homology 5-spheres.

## Mathematical scope

Let `Delta` be a flag generalized homology 5-sphere with 17 vertices and write

```text
h_Delta(t) = sum_{i=0}^3 gamma_i(Delta) t^i (1+t)^(6-2i).
```

For a valid admissible edge contraction, the standard h-polynomial recurrence
is

```text
h_Delta(t) = h_{Delta/e}(t) + t h_{link_Delta(e)}(t).
```

Evaluation at `t=-1` proves exactly

```text
gamma_3(Delta) = gamma_3(Delta/e) + gamma_2(link_Delta(e)).
```

Thus the known nonnegativity for the 16-vertex contraction and for the
3-dimensional edge link proves the Charney--Davis inequality whenever an
admissible edge exists. A negative 17-vertex counterexample must have every
edge contained in an induced four-cycle.

The Lean development proves:

- `gammaThree_eq_of_hPolynomial_recurrence`;
- `charneyDavis_of_admissibleEdge_data`;
- `edgeInInducedFourCycle_iff_crossNeighborhood`;
- `not_exists_admissibleEdge_iff_contractionIrreducible`;
- `negative_gammaThree_forces_contractionIrreducible`.

The follow-up file `CharneyDavisPolarReduction.lean` proves the next exact
reduction.  A hypothetical negative 17-vertex counterexample has polar size
exactly three.  The exact complement-triangle count then forces
`(gamma_2, gamma_3) = (5,-6)`: its one-skeleton complement is triangle-free
with degree sequence `3^16 4^1`, and the sum of vertex-link `gamma_2` values
is two.  Each minimum-antipode 13-vertex link is a nonsuspension flag homology 4-sphere with
`gamma_1 = 3` and `0 <= gamma_2 <= 2`.  See
[`POLAR_REDUCTION.md`](POLAR_REDUCTION.md) for the proof dependencies and the
exact third-antipode escape which blocks a direct reuse of the published
two-antipode contraction argument.

The cross-neighborhood theorem gives an exact local criterion: an edge `uv`
lies in an induced four-cycle precisely when the exclusive neighborhoods of
`u` and `v` contain an adjacent cross-pair.

## Formal trust boundary

The file introduces no custom axioms and passes all external mathematical
input as hypotheses. Lean proves the polynomial recurrence consequence,
nonnegativity implication, induced-cycle characterization, and
minimal-counterexample obstruction.

The following literature theorems are not yet represented in Mathlib and are
not claimed as machine-checked here:

1. contraction of an admissible edge in a flag generalized homology sphere
   again gives a flag generalized homology sphere of the same dimension;
2. its edge link is a flag generalized homology sphere two dimensions lower;
3. the h-polynomial edge-subdivision recurrence applies to that contraction;
4. the Labbé--Nevo 16-vertex and Davis--Okun 3-sphere nonnegativity inputs.

This identifies the smallest missing formal bridge: a definition of finite
flag generalized homology spheres, links, and admissible contraction, followed
by the topology-preservation theorem. Mathlib v4.33.1 contains abstract
simplicial complexes but no integrated link/homology-sphere/contraction API.

## Reproduction

Pinned versions:

```text
Lean 4.33.1
Lake 5.0.0-src+819816b
Mathlib v4.33.1
```

Run:

```bash
lake update
lake exe cache get
lake build
sha256sum -c SHA256SUMS
```

The build prints the axiom audit for every exported theorem. The source uses
no `sorry`, `admit`, custom axioms, `unsafe`, or `native_decide`.

## Primary sources

- Ruth Charney and Michael Davis, *The Euler characteristic of a
  nonpositively curved, piecewise Euclidean manifold*, Pacific J. Math. 171
  (1995): <https://msp.org/pjm/1995/171-1/pjm-v171-n1-p04-p.pdf>
- Michael Davis and Boris Okun, *Vanishing theorems and conjectures for the
  L2-homology of right-angled Coxeter groups*:
  <https://arxiv.org/abs/math/0102104>
- Frank Lutz and Eran Nevo, *Stellar theory for flag complexes*:
  <https://arxiv.org/abs/1302.5197>
- Jean-Philippe Labbé and Eran Nevo, *Bounds for entries of gamma-vectors of
  flag homology spheres*: <https://arxiv.org/abs/1612.01169>

## Novelty and status

The formalization is an independently checked packaging of a contraction
reduction implicit in the cited literature, not a claimed resolution of the
17-vertex case and not a priority claim. Its research value is to expose the
exact residual class and the precise unformalized topological bridge.
