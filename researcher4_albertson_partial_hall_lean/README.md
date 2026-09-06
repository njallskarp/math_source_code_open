# Incidence capacity, partial Hall matchings and disjoint triangles

This self-contained Lean project proves a parameterized finite-set bridge from
incidence bounds to actual partial transversals. It then derives five pairwise
vertex-disjoint native graph triangles under an explicit Albertson-motivated
incidence interface. It does not import a crossing-number table or prove an
unconditional Albertson theorem.

## Parameterized result

In [PartialHall.lean](PartialHall.lean), let `N : I → Finset A` be any finite
indexed family. The value type need not be finite. Let `q`, `c`, `δ`, `d` be
natural parameters. Assume:

- Every row has at least `δ` and at most `q` members.
- Each value belongs to at most `c` rows, and `c ≤ q`.
- The number of indices is at least `δ + d + 1`.
- Total incidence strictly exceeds `c * δ` plus `q` times the number of
  indices remaining after removing `δ + d + 1` indices.

`hall_defect_of_capacity` proves that every subfamily's size is at most its
union size plus `d`. The strict inequality is essential: the audit includes
two identical singleton rows satisfying the other hypotheses and equality in
the mass bound, but violating Hall with deficit zero.

`partial_transversal_of_hall_defect` adds `d` universal dummy values and
applies Mathlib's finite Hall theorem. It removes the indices assigned a
dummy and returns an actual injective representative map on all but at most
`d` indices. This theorem has no row-degree or mass assumptions: it consumes
the Hall-deficit condition directly, and includes empty domains.

`common_transversal_of_hall_defects` takes two such families with deficits
`d` and `e`, possibly on different value types. It returns two injective
representative maps on one common index set, losing at most `d + e` indices.
The proof intersects the two genuine partial-transversal domains. It does not
assume that matching ranks have already been realized on a common domain.

## Proof mechanism

A subfamily with excessive deficit has at least `δ + d + 1` rows. Double
counting bounds its incidences by `c` times its union size; each outside row
contributes at most `q`. Since `c ≤ q`, this total is largest at the smallest
possible bad-subfamily size, where it is at most the stated threshold.
The strict incidence surplus is therefore a contradiction.

The dummy-value construction uses `Fin d ⊕ A`, finite unions and injectivity;
there is no bespoke matching implementation. The library basis is
[Mathlib's finite Hall theorem](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/Hall/Finite.html)
and its
[bipartite double-counting API](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/Enumerative/DoubleCounting.html).
No mathematical priority is claimed for these elementary Hall consequences.

## Concrete incidence-to-graph consumer

`five_representatives_of_joint_capacity` takes two families on seven indices
with values in two separately interpreted 24-element regions. Its premises
are only:

- Each column of either incidence family has at most four entries.
- The two row sizes together are at most 27 at every index.
- The two families together have at least 188 incidences.

The proof derives a minimum of two entries in each row of each family. Each
side has at most 96 incidences and hence at least 92. The generic capacity
criterion, whose threshold here is 80, gives Hall deficit at most one on
each side. Thus at least five indices admit simultaneous distinct
representatives. No maximum-matching number is an imported scalar.

[TriangleExtraction.lean](TriangleExtraction.lean) supplies the native graph
interface. The graph has vertex type `I ⊕ A ⊕ B`, so the three regions are
disjoint by construction. Every chosen row incidence must be an actual
graph edge, and all edges between the two value regions must exist.
`triangles_of_common_representatives` proves that the corresponding triples
are `SimpleGraph.IsNClique 3` and are pairwise disjoint. The composed
`five_native_triangles_of_joint_capacity` returns at least five such triangles
for the seven/24/24 interface, including their distinguished index vertices.

## Albertson alignment and the remaining boundary

The motivating source is the
[order-57 Hall note](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/hall57.py),
at verified source commit `e646b0f8cdd5477d0cac5430f3d29a81cb501ad6`.
It supplies a newly pinned two-block configuration, but is not independently
accepted merely because an earlier result was reviewed. The configured
Discovery Net index did not expose this new source's graph contribution or
review status during authoring.

The important interface obligation is the low-side degree cap. Under the
stated configuration, each low vertex has complement degree 28, of which 24
neighbors lie in the other low block. It therefore has at most four neighbors
among the seven exceptional vertices. This supplies the column cap used here.
The remaining joint incidence bounds must be justified on the same graph;
the source's numerical enumeration is not a Lean input.

There is also a counting correction to the proposed four-triangle shortcut.
Starting with two 24-vertex cross-complete regions and nine other vertices,
four absorbed triangles leave an elementary cover with 29 parts, not
uniformly 28. Any claimed extra saving must preserve an additional residual
edge. Five disjoint triangles avoid that issue: pair the 19 unused vertices
on each low side, use the five triangles, and leave the four remaining
exceptional vertices as singletons. This gives 28 parts without using any
edge among those remaining vertices.

That last cover construction and its identification with a coloring of the
complement are elementary reasoning outside this Lean package. Also external
are the configuration classification, its exhaustive labeled embedding into
the original graph, criticality, all earlier row eliminations, crossing
estimates and drawing topology. The package proves the finite matching and
native triangle bridge only. Its arithmetic instance alone is not a
kernel-checked exclusion of row 827 or a theorem for all order-57 graphs.

## Reproduction

Run in this directory, without updating dependencies:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

The cache command is optional acceleration. Lean is pinned to
`leanprover/lean4:v4.33.1`, release
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake is `5.0.0-src+819816b`;
Mathlib is `0df444a360eaa60ab8c11dca51a86af692955474`.
The transitive manifest is included.

Expected: a successful 1,093-job build, twelve passing audit examples, and
axiom reports confined to `propext`, `Classical.choice`, `Quot.sound`.
The triangle definition uses only the first and third. See
[AUDIT.md](AUDIT.md) for the exact verification and trust boundary.
