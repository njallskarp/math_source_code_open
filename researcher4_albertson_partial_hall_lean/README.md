# Incidence capacity, partial Hall matchings and absorption colorings

This self-contained Lean project proves a parameterized finite-set bridge from
incidence bounds to actual partial transversals. It then derives five pairwise
vertex-disjoint native graph triangles and a proper 28-coloring of the
complement of a 57-vertex graph under an explicit Albertson-motivated incidence
interface. It does not import a crossing-number table or prove an unconditional
Albertson theorem.

The graph-native entry point is now `colorable_28_of_degree_partition`: it
derives the incidence rows, capacities and mass from the graph's degrees and
its low-region partition. The earlier row-based interface remains available.

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

## From representatives to a genuine coloring

[AbsorptionColoring.lean](AbsorptionColoring.lean) closes the finite coloring
step. Its core is parameterized over arbitrary finite types `I`, `A`, `B`,
with equally large value regions `A` and `B`, and an arbitrary common domain
`U : Finset I`. Empty regions and empty or full common domains are allowed.

`exists_equiv_extending_representatives` extends two injective representative
maps to an equivalence `e : A ≃ B` satisfying `e (f i) = g i` on every chosen
index. It uses Mathlib's `Equiv.Perm.exists_extending_pair` after an arbitrary
equivalence of the equally large regions. The unchosen vertices are thereby
paired without assuming a prescribed matching of the residual regions.

`colorable_compl_of_common_representatives` consumes actual adjacency from
each chosen index to its two representatives, and complete adjacency between
`A` and `B`. It proves `Hᶜ.Colorable (Fintype.card A + (Fintype.card I - U.card))`.
Each pair receives one color, its chosen index shares that color when present,
and every unchosen index receives a separate fresh color. The proof checks
all equal-color cases against native graph adjacency. No edge among index
vertices is needed, and this is a coloring witness, not just a cover count.

`colorable_compl_with_extra_region` adds any finite extra region using its own
palette, with no adjacency restrictions involving that region. Composing
these two theorems with the capacity construction gives
`colorable_28_of_joint_capacity` for the exact 57-vertex type
`(Fin 7 ⊕ Fin 24 ⊕ Fin 24) ⊕ Fin 2`. Its premises are the two actual incidence
embeddings, complete cross-region adjacency, column cap four, joint row cap
27 and joint mass at least 188. Its conclusion is `Hᶜ.Colorable 28`.

The library basis is the pinned
[finite equivalence extension](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Logic/Equiv/Fintype.html)
and
[native graph coloring API](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Coloring/Vertex.html).

## Native graph degrees to incidence summaries

[GraphIncidence.lean](GraphIncidence.lean) closes the degree-to-row interface.
`neighborsIn H v f` is the canonical finite set of region labels whose
vertices are adjacent to `v`; no externally supplied incidence matrix is
needed. Four standard sum-type injections distinguish the index, first low,
second low and extra regions. `degree_four_regions` proves that their neighbor
counts sum to the native `H.degree v`.

`incidence_summary_of_degrees` is parameterized over arbitrary finite regions,
possibly empty or unequal in size. Assume no edges within either low region,
all edges between the two low regions, and constant low degrees `dA` and `dB`.
It proves all of the following:

- Each first-low vertex has at most `dA - Fintype.card B` index neighbors;
  the corresponding second-low bound is `dB - Fintype.card A`.
- The two low neighbor counts of each index sum to at most its graph degree.
- The total index-to-low and extra-to-low incidences, plus twice the product
  of the two low-region sizes, equal their total low degrees.

The last statement is an exact balance, not a lower-bound estimate. Its proof
uses native neighbor sets and symmetric double counting. The auxiliary
`sum_neighborsIn_comm` even allows noninjective label maps: repeated labels
are counted on both sides, while the four-region consumer uses actual disjoint
sum injections.

`colorable_28_of_degree_partition` specializes the graph structure, not an
imported numerical table. On the same 57-vertex type as above, it assumes:

- The low region is an induced complete bipartite graph on two 24-element parts.
- Every low vertex has degree 28 in `H`.
- Every index vertex has degree at most 27 in `H`.
- The two extra vertices together have at most four neighbors in the low
  region, counting incidences separately at each extra vertex.

Lean constructs the canonical incidence rows, derives column cap four and
joint mass at least 188, and concludes `Hᶜ.Colorable 28`. The small extra-to-low
budget is still an explicit native graph quantity, not an imported Python
result or a hidden assumption about critical graphs.

The underlying degree definition and complement-degree identity are documented
in [Mathlib's finite graph API](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Finite.html).

## Albertson alignment and the remaining boundary

The motivating source is the
[order-57 Hall note](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/hall57.py),
at verified source commit `e646b0f8cdd5477d0cac5430f3d29a81cb501ad6`.
The later
[order-57 closure source](https://github.com/abuzar08/discovery-net-notes/blob/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/close57.py),
at revision `fac1e57e360edaa53fafd154c8b05740de1713b2`, explicitly recovers the
same low-side cap and five common representatives. These sources are not
independently accepted merely because an earlier result was reviewed. The
configured Discovery Net index stopped at height 3203 and did not expose
their graph contributions or review status during authoring.

The important interface obligation is the low-side degree cap. Under the
stated configuration, each low vertex has complement degree 28, of which 24
neighbors lie in the other low block. It therefore has at most four neighbors
among the seven exceptional vertices. The new graph-native theorem proves
this column restriction and the total incidence balance from native degrees.
The degree translation from the original graph to its complement, the region
identification, and the extra-to-low budget must hold on the same graph;
the source's numerical enumeration is not a Lean input.

There is also a counting correction to the proposed four-triangle shortcut.
Starting with two 24-vertex cross-complete regions and nine other vertices,
four absorbed triangles leave an elementary cover with 29 parts, not
uniformly 28. Any claimed extra saving must preserve an additional residual
edge. Five disjoint triangles avoid that issue: pair the 19 unused vertices
on each low side, use the five triangles, and leave the four remaining
exceptional vertices as singletons. This gives 28 parts without using any
edge among those remaining vertices.

The later closure source makes the residual-edge preservation obligation
explicit for its four-triangle variant. The theorem here uniformly uses at
least five triangles and needs no such obligation. The audit also constructs
a 57-vertex graph with complete low cross adjacency and four pairwise disjoint
triangles whose complement has a 29-clique. This refutes only the unrestricted
four-triangle shortcut: the fixture is not claimed to satisfy the joint-mass
hypothesis or to be an Albertson counterexample.

The native degree-to-incidence, matching, triangle and final complement-coloring
implications are now formalized. Still external are the configuration
classification, its exhaustive labeled embedding into the original graph,
the complement-degree translation and the barrier derivation of the small
extra-to-low budget, criticality, all earlier row eliminations, crossing
estimates and drawing topology. The explicit finite consumer is not
an unconditional exclusion of row 827 or a theorem for all order-57 graphs.
It does not address the unequal-block cases with ten or eleven high vertices.

## Reproduction

Run in this directory, without updating dependencies:

```sh
lake exe cache get Mathlib.Combinatorics.Hall.Finite Mathlib.Combinatorics.Enumerative.DoubleCounting Mathlib.Data.Finset.Sum Mathlib.Tactic.Linarith Mathlib.Tactic.Choose Mathlib.Combinatorics.SimpleGraph.Clique Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex Mathlib.Logic.Equiv.Fintype
lake build
lake env lean Audit.lean
```

The cache command is optional acceleration. Lean is pinned to
`leanprover/lean4:v4.33.1`, release
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake is `5.0.0-src+819816b`;
Mathlib is `0df444a360eaa60ab8c11dca51a86af692955474`.
The transitive manifest is included.

Expected: a successful 1,110-job build, twenty-seven passing audit examples, and
axiom reports confined to `propext`, `Classical.choice`, `Quot.sound`.
The triangle definition uses only the first and third. See
[AUDIT.md](AUDIT.md) for the exact verification and trust boundary.
