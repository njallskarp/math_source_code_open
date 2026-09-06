# Build and theorem-alignment audit

## Checked declarations

Eighteen theorem audits and two definition audits are in [Audit.lean](Audit.lean):

| Declaration | Checked content |
| --- | --- |
| `sum_rows_le_union_capacity` | Actual finite incidence double count and column cap. |
| `hall_defect_of_capacity` | Parameterized incidence surplus excludes excessive Hall deficiency. |
| `partial_transversal_of_hall_defect` | Dummy-value Hall construction and a realized partial transversal. |
| `common_transversal_of_hall_defects` | Two injective choices on a common domain. |
| `five_common_representatives` | Seven indices, column cap four, row minimum two and side mass above 80. |
| `five_representatives_of_joint_capacity` | Derives those inputs from joint mass and row/column bounds. |
| `triangle` | Native three-region finite vertex set. |
| `disjoint_triangles` | Injectivity prevents every cross-triangle vertex collision. |
| `triangles_of_common_representatives` | Actual native graph edges yield disjoint three-cliques. |
| `five_native_triangles_of_joint_capacity` | Complete finite incidence-to-triangle composition. |
| `exists_equiv_extending_representatives` | Full pairing extending two injective maps between equally large finite regions. |
| `colorable_compl_of_common_representatives` | Parameterized proper coloring with one saved color per absorbed index. |
| `colorable_compl_with_extra_region` | Arbitrary extra vertices use a separate palette; no extra adjacency assumptions. |
| `colorable_28_of_joint_capacity` | The incidence interface yields a native 28-coloring of the 57-vertex graph's complement. |
| `neighborsIn` | Canonical adjacency rows obtained directly from a graph. |
| `card_filter_sum_regions` | Exact finite neighbor-count split on a sum type. |
| `sum_neighborsIn_comm` | Symmetric incidence double count for arbitrary finite label maps. |
| `degree_four_regions` | Native graph degree equals the sum of four regional neighbor counts. |
| `incidence_summary_of_degrees` | Parameterized row/column bounds and exact incidence balance from graph degrees and low-region structure. |
| `colorable_28_of_degree_partition` | Native degree/partition hypotheses imply a 28-coloring without external incidence rows or a supplied mass bound. |

All eighteen theorems and `neighborsIn` report exactly
`propext`, `Classical.choice`, `Quot.sound`.
The definition `triangle` reports `propext`, `Quot.sound`.
No proof hole, custom axiom, native evaluation, unsafe shortcut, external
oracle, solver, modified kernel or raised proof limit is used.

## Tests and reproduction

```sh
lake build
lake env lean Audit.lean
```

Twenty-seven examples test two distinct cyclic incidence families, both mass
calculations, simultaneous representatives, the strict-mass equality
counterexample and its remaining capacity hypotheses, empty-domain handling,
a joint-capacity fixture of total mass 189, triangle cardinality, a collision
caused by a reused representative, and actual three-clique adjacency. The new
tests cover empty coloring regions, an identity extension, a genuine
57-vertex joint-capacity graph with isolated extra vertices, and a sharp
four-triangle boundary graph. In the latter graph, Lean checks complete low
cross adjacency, four actual pairwise disjoint triangles, and a 29-clique in
the complement, hence failure of 28-colorability. This fixture does not claim
the joint-mass premise and is not an Albertson counterexample.

Six further examples test a graph whose low degrees are exactly 28 and
whose index degrees are at most 27. Its extra-to-low incidence total is three,
and its index-to-low incidence total is 189. The full degree-partition theorem
applies to this actual graph. The fixture's removed row incidences are spread
over two columns and restored by two distinct extra vertices, so it meets the
degree interface rather than just the weaker row interface. A seventh example
invokes the parameterized summary with empty and unequal regions. These
fixtures do not assert criticality or a Tutte-barrier classification.

The finite examples use ordinary `decide`, checked by Lean's kernel, not
native evaluation or externally generated certificate data.

Lean `leanprover/lean4:v4.33.1`, release
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake `5.0.0-src+819816b`;
Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.

During the preceding absorption-coloring pass, the original dependency cache
was absent. Its
broken link was preserved locally, and the manifest's exact dependency
revisions were restored into this project's ignored `.lake` directory.
A targeted official cache request restored 1,085 dependency modules; the
finite-equivalence extension modules and the new author source compiled
locally. The original toolchain and dependency manifest hashes are unchanged.
The degree-to-incidence continuation reuses that restored pinned cache.
The full 1,110-job build and audit pass in both the authoring project and a
fresh isolated publication copy. This is not a rebuild of every Mathlib
source file. The source package needs no private path or external certificate.

## External-data and mathematical boundary

There is no imported Python output, row table, graph catalogue or generated
data. The examples are literal Lean definitions, not witnesses claimed to
realize the entire Albertson configuration. The author did not execute the
upstream row enumeration or independently review its classification.

The generic finite theorems are unconditional under their explicit premises.
The seven/24/24 graph consumer uses the standard sum type as its exact vertex
model; a labeled induced configuration in a different ambient graph needs its
own identification with that model. Neither full criticality nor a drawing
model is hidden in a free scalar.

The final complement-coloring bridge is now formalized, including extension
of the partial pairing and a separate palette for the two extra vertices.
The result is a conditional native graph theorem, not an unconditional
Albertson row elimination. The graph-to-region identification, complement-degree
translation and small extra-to-low budget still need to follow from the
accepted upstream configuration on the same ambient graph. The incidence
rows, row/column bounds and mass are now derived in Lean from those native
graph hypotheses. The complete closure-source text at
`fac1e57e360edaa53fafd154c8b05740de1713b2` was inspected, with SHA-256
`736ba9df66d8daf0c88ce233bfe1b392fe94051f0082e984e5d2b906c22f936f`
for `close57.py`; its program and upstream enumeration were not executed or
certified by this project. The later unequal-block cases are not inputs.
This is authoring of a reusable formal bridge, not independent peer review
of any contribution signed by this researcher's key.
