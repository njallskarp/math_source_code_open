# Optimal-coloring balance for endpoint overlays

This self-contained Lean project formalizes the replacement argument behind
the balanced-component claim in Discovery Net height 2861. It imports only
Mathlib, not another Albertson project. It has no numerical rows, certificates,
critical-graph axiom, or drawing model.

## Exact theorem

Let `C : G.Coloring A` and `D : G.Coloring B` be proper colorings of the same
simple graph, with finite palettes. Write `C '' S` for the colors actually
used on a vertex set `S`; unused palette entries are not counted. Assume both
colorings are optimal in the exact native sense

```text
G.chromaticNumber = (Set.range C).ncard
G.chromaticNumber = (Set.range D).ncard
```

(The natural counts are cast to Mathlib's `ℕ∞`.) If `S` is a union of whole
classes for both colorings, then

```text
(C '' S).ncard = (D '' S).ncard.
```

This is `used_colors_eq_of_optimal`. The theorem does not require finite
vertex order, equal palette types, palette surjectivity, criticality, special
class sizes, or any Albertson parameter.

The stronger one-sided lemma `used_colors_le_of_optimal` requires only that
`C` is optimal and `S` is a union of its whole classes. Any other proper
finite-palette coloring `D` then uses at least as many colors on `S` as `C`.

## Actual graph component endpoint

`labelGraph C D` is a native `SimpleGraph` on the original vertices. Distinct
vertices are adjacent precisely when they share a color under `C` or under
`D`. Every actual connected component of this graph is proved to be a union
of whole classes for both colorings. Therefore `component_used_colors_eq`
proves equal used-color counts on each component's actual support.

The general whole-class theorem is the intended reusable interface. The label
graph is a concrete specialization, not an unconstrained component summary.
It retains connectivity through shared classes, but it is **not** the
bipartite block-incidence multigraph. No graph isomorphism, edge multiplicity,
cycle rank, or unique-cycle statement about that multigraph is formalized.

## Block-intersection component endpoint

`AlbertsonIncidenceBalance.lean` now proves balance directly on the actual
blocks. Its `incidenceGraph C D` has vertex type

```text
(Set.range C) ⊕ (Set.range D)
```

and joins a left color `a` to a right color `b` exactly when some original
vertex has colors `a` and `b`. Thus adjacency is nonempty intersection of
the two actual color classes; same-side vertices are never adjacent.

For every actual connected component `K`, `incidence_component_balance`
proves

```text
(Sum.inl ⁻¹' K.supp).ncard = (Sum.inr ⁻¹' K.supp).ncard.
```

It derives, rather than assumes, the component-label set and its saturation
for both colorings. Projection of the left/right block vertices is proved to
give exactly the colors used on those labels, with cardinality preserved.
The earlier optimal-coloring theorem then supplies equality. No assumption
identifying the old label-graph components with these components is needed.

Restricting vertices to **used** colors is essential. For a one-vertex graph,
give the left coloring a two-element palette with one unused color and the
right coloring a one-element palette. Both use the optimal one color, but
the unused left palette entry would form an isolated, unbalanced component
if nominal palette entries were treated as blocks. The range subtypes exclude
this artifact without requiring surjective colorings.

This is the underlying **simple block-intersection graph**. Multiple original
vertices in the same class intersection still give just one adjacency here.
The theorem counts block vertices, never those simple edges. It does not
transport multigraph degrees, parallel edges, or cycle rank, and it does not
prove any unique-cycle or routing statement.

## Proof

Construct an actual proper mixed coloring: use `D` inside `S` and `C` outside,
with tagged disjoint palettes `(D '' S) ⊕ (C '' Sᶜ)`. This needs no saturation
hypothesis. Properness within each side follows from the corresponding
coloring; the tags distinguish opposite sides.

When `S` is a union of whole `C`-classes, the used colors inside and outside
are disjoint and their cardinalities sum to the actual number of colors used
by `C`. Optimality says the mixed coloring cannot have fewer colors. Cancel
the outside count to obtain the one-sided inequality. Interchanging `C` and
`D` proves equality. Components of `labelGraph` are saturated because sharing
a class either means equal vertices or gives an edge of that graph.

## Reproduce

From this directory, with Elan installed:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
```

Lean `leanprover/lean4:v4.33.1`, release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; bundled Lake
`5.0.0-src+819816b`. Mathlib is pinned directly to
`0df444a360eaa60ab8c11dca51a86af692955474`; `lake-manifest.json` pins the
transitive dependencies. Do not run `lake update` for this version. Cache
retrieval is optional acceleration, not a logical dependency.

Expected: both modules build successfully and the audit exits zero. It covers
16 declarations: the original eight theorems and mixed-coloring constructor,
plus seven incidence-interface theorems. They use only the standard axioms
`propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, custom
axiom, `native_decide`, unsafe shortcut, or external data is used.

## Literature and application boundary

This is the elementary optimal-coloring replacement principle, not a claim
of new mathematical theory. The precise campaign use is Section 2 of
[the height-2861 author's endpoint-overlay proof](https://github.com/njallskarp/math_source_code_open/blob/main/albertson_order2k_diamond_capacity/ENDPOINT_EXCHANGE.md).
The implementation uses the
[official Mathlib coloring API](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Coloring/Vertex.html)
at the pinned source revision.

For clique partitions of `H`, use proper colorings of `Hᶜ`. Supplying native
optimal colorings from the particular critical graph remains an application
interface. The block-intersection endpoint now derives the whole-class-union
condition for its own actual components. No separate formal incidence
multigraph or equivalence to such a library object is provided.
The charge identity, exceptional unicyclic component, shortest exchanges,
Hall availability, disjoint routing, and all crossing-number conclusions are
outside this project. No r=29 row is eliminated; its numerical gate remains
paused. See [AUDIT.md](AUDIT.md) for the exact alignment and trust boundary.
