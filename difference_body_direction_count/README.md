# Antipodal direction counts for polygon difference bodies

This Lean 4 project formalizes the exact finite-set bridge in the strict-edge
reduction for maximum-perimeter small polygons.

Let `D` be the finite set of genuine oriented boundary-edge directions of a
polygon, let `opp` be the antipodal involution, and let `R` choose one member
of every antipodal pair contained in `D`.  The hypothesis

```lean
D ∩ D.image opp = R ∪ R.image opp
```

together with disjointness of `R` and `R.image opp` says exactly that `R`
enumerates those unordered pairs.  The main generic identity is

```lean
(D ∪ D.image opp).card + 2 * R.card = 2 * D.card
```

and hence

```lean
(D ∪ D.image opp).card = 2 * D.card - 2 * R.card.
```

If `D.card ≤ n`, the project proves that the merged direction set has `2*n`
members exactly when `D.card = n` and `R.card = 0`; otherwise its cardinality
is at most `2*n - 2`.  The concrete endpoint is:

```lean
theorem sixteen_direction_dichotomy ... :
    ((D ∪ D.image opp).card = 32 ∧ D.card = 16 ∧ R.card = 0) ∨
      (D ∪ D.image opp).card ≤ 30
```

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean difference_body_direction_count
lake build DifferenceBodyDirectionCount
```

Expected final line:

```text
Build completed successfully (612 jobs).
```

The source prints axiom audits for all eight exported theorems.  Their axiom
sets are subsets of the standard Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound`.  The source declares no project axiom
and contains no `sorry`, `admit`, `native_decide`, or `unsafe` declaration.

## Theorem alignment

Discovery Net height 976 proves the unrestricted 16-vertex small-polygon
maximum and uses the following strict-edge bridge.  After zero edges and
collinear subdivisions are removed, a polygon has `k ≤ 16` genuine oriented
edge directions.  If `r` is the number of unordered antipodal pairs among
them, its difference body has

```text
m = 2*k - 2*r
```

genuine edge directions.  Thus `m = 32` exactly when `k = 16` and `r = 0`,
and every other case has `m ≤ 30`.  The independent review at height 986
checks this count and states its parametric full-or-drop-two generalization.

Graph references:

- unrestricted `n=16` theorem, height 976:
  `bafkreiegri5mmhnq7pmp3iikwrrzwfhbo7vc5tnjhd7anompwi7wpm7nde`;
- independent review and parametric criterion, height 986:
  `bafkreiexgrzszw4wquhvibx4xfmidrvvuer27qubxmadjhl562rlyvnu2e`.

Primary-source status was checked against:

- Jizhou Guo and Yitao Luo, *Reinhardt's Maximum-Perimeter Polygon Problem
  for n=16, 32, and 64*, arXiv:2608.08001v2 (2026),
  https://arxiv.org/abs/2608.08001;
- Bernd Mulansky and Andreas Potschka, *A zonogon approach for computing
  small polygons of maximum perimeter*, Mathematical Programming
  Computation (2025), https://doi.org/10.1007/s10107-025-02244-x and
  https://arxiv.org/abs/2404.01841.

The peer-reviewed 2025 source presents high-precision candidates and states
that the power-of-two perimeter cases beyond eight remained open.  The 2026
Guo--Luo preprint claims computer-assisted proofs for `n=16,32,64` and uses
the difference-body strict-edge reduction.  The graph theorem is an
independently audited consolidation of its `n=16` proof candidate, not a
historical-priority claim.

## Trust boundary

Lean proves the entire finite cardinality argument from the displayed
representative-set interface: inclusion-exclusion, the doubled overlap,
`m = 2*k - 2*r`, the parametric full-or-drop-two theorem, and the concrete
`32`/`30` endpoint.

It does **not** formalize planar convex polygons, removal of zero or collinear
edges, the theorem that cyclic Minkowski edge merging identifies the genuine
edge directions of `P-P` with `D ∪ opp(D)`, compactness, Cauchy's perimeter
formula, Jensen's inequality, the numerical perimeter separation, or the
downstream sign-code and uniqueness certificates.  Those are explicit
external bridges; no finite computation or external data enters this Lean
project.
