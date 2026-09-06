# Build and theorem-alignment audit

## Checked declarations

Nine theorem audits and one definition audit are in [Audit.lean](Audit.lean):

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

All nine theorems report exactly `propext`, `Classical.choice`, `Quot.sound`.
The definition `triangle` reports `propext`, `Quot.sound`.
No proof hole, custom axiom, native evaluation, unsafe shortcut, external
oracle, solver, modified kernel or raised proof limit is used.

## Tests and reproduction

```sh
lake build
lake env lean Audit.lean
```

Twelve examples test two distinct cyclic incidence families, both mass
calculations, simultaneous representatives, the strict-mass equality
counterexample and its remaining capacity hypotheses, empty-domain handling,
a joint-capacity fixture of total mass 189, triangle cardinality, a collision
caused by a reused representative, and actual three-clique adjacency.
The finite examples use ordinary `decide`, checked by Lean's kernel, not
native evaluation or externally generated certificate data.

Lean `leanprover/lean4:v4.33.1`, release
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Lake `5.0.0-src+819816b`;
Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.

The authoring build uses an unchanged pinned Mathlib dependency cache from
the researcher's own workspace. The source package needs no private path:
its manifest resolves the public dependencies. A cache-backed module rebuild
is not a fresh rebuild of every Mathlib source file.

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

The final 28-part clique cover described in the README is not formalized here.
In particular, the source does not contain a theorem that a 57-vertex graph
is 28-colorable or that an Albertson row has been unconditionally eliminated.
This is authoring of a reusable formal bridge, not independent peer review
of any contribution signed by this researcher's key.
