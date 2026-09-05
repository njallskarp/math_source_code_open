# Theorem alignment and trust audit

All declarations are in namespace `AlbertsonNeighborhoodObstruction` and use
native Mathlib graphs, colorings, induced subgraphs, sets, and chromatic number.
The vertex-deleted graph is exactly `G.induce {x | x ≠ a}`. The two original
modules import Mathlib directly. The new component module imports the
reservoir module and Mathlib connectivity, not another campaign project.

## Native singleton-component module

| Declaration | Exact role |
|---|---|
| `neighborSet_subset_of_singleton_component` | Derive actual neighborhood containment from a singleton component after deleting a set. |
| `card_add_card_le_of_singleton_overlap` | Bound two finite sets confined to a common set plus one point and disjoint inside the common set. |
| `disjoint_clique_neighbors_of_singleton_components` | Extract containment and nonadjacency from native components, then apply the chromatic-drop theorem. |
| `degree_add_degree_le_of_singleton_components` | Bound the actual combined complement degree by the clique size plus two. |

The singleton hypothesis is an equality between the support of the actual
component containing a surviving vertex and the singleton containing that
vertex. The induced graph is the complement restricted to vertices outside
the union of the clique and the extra vertex's singleton. Component support is Mathlib's
native reachability-quotient support, not a custom encoding.

The final theorem assumes a finite vertex type, positive finite chromatic
number, an actual complement clique, chromatic drop at its vertices, and two
distinct surviving vertices with singleton supports. Its conclusion uses
native `SimpleGraph.degree`. `Audit.lean` type-checks the four-clique
specialization with bound six, retaining all graph hypotheses. This is not
an instantiated example graph or an independently checked enumeration.

The only new counting step is finite inclusion-exclusion on the actual
neighborhoods: their union lies in the clique plus one vertex and their
intersection lies in that single vertex. The set-cardinality helper is
separate from the graph theorem and does not import a numerical degree table.

## Preserved reservoir module

| Declaration | Exact role |
|---|---|
| `extendDeletionColoring` | Extend a deletion coloring when a color is absent from the deleted vertex's neighbors. |
| `exists_neighbor_of_color` | Every color of an insufficient palette occurs on a neighbor. |
| `exists_reservoir_same_color` | Find a same-colored representative in the supplied reservoir. |
| `exists_reservoir_injection` | Independent complement vertices sharing a clique neighbor inject into the reservoir. |
| `reservoir_card_bound` | Bound actual finite-set cardinalities. |
| `not_common_neighbor_of_singleton_reservoir` | Exclude a common clique neighbor with a one-vertex reservoir. |
| `disjoint_clique_neighbors_of_singleton_reservoir` | Prove disjointness using supplied deletion colorings. |
| `disjoint_clique_neighbors_of_chromatic_drop` | Supply those colorings from native chromatic-drop inequalities. |

The injection theorem assumes a finite palette smaller than the original
chromatic number, an actual deletion coloring, a complement clique containing
the deleted vertex, an independent complement set of its neighbors, and
neighborhood containment in the union of the clique and reservoir. It concludes
an embedding of the independent set into the reservoir.

The final wrapper assumes an arbitrary positive finite chromatic number,
strict drop at every vertex of the clique, and the actual clique, distinctness,
nonadjacency and singleton-reservoir containment premises. Its conclusion is
disjointness of the two neighbor sets inside the clique. Mathlib's
`chromaticNumber_le_iff_colorable` closes coloring existence. No fixed order,
special deletion cover, class size, matching or Stehlík hypothesis appears.

## Preserved folding module

| Declaration | Exact role |
|---|---|
| `foldHom` | Construct the native fold into a vertex-deleted graph. |
| `chromaticNumber_delete_eq_of_neighborSet_subset` | Prove chromatic equality from neighborhood inclusion. |
| `not_neighborSet_subset_of_chromatic_drop` | Exclude inclusion under strict chromatic drop. |
| `neighborSet_subset_of_compl_domination` | Translate complement domination to neighborhood inclusion. |
| `exists_compl_neighbor_not_adjacent` | Produce a complement non-domination witness. |
| `not_isClique_of_neighborSet_subset` | Exclude a clique containing a nonempty complement neighborhood. |

This source is byte-for-byte unchanged from height 2953. Its graph need not
be finite; its chromatic number is extended-natural. No finite-palette premise
is added to the earlier theorems.

## Boundary checks

- Representatives are actual vertices with proved color equality and
  membership, not asserted capacities. Injectivity follows from proper
  coloring on the specified clique in the original graph.
- Only the palette must be finite for the injection. Finiteness of the two
  sets enters the cardinality corollary. Empty or overlapping sets are allowed
  when the hypotheses hold.
- The singleton consequence explicitly requires distinctness and complement
  nonadjacency. The contradiction between sizes two and one follows from the
  generic theorem, not a separately assumed scalar inequality.
- Strict chromatic drop supplies the final colorings once the positive finite
  chromatic value is supplied. Criticality of an arbitrary graph is not proved.
- The earlier clique-barrier theorem retains nonempty-neighborhood and
  criticality premises. Criticality does not exclude isolated complement
  vertices.
- Native singleton supports now imply neighborhood containment and the
  complement nonedge. No decoder or assertion about component counts is
  used to obtain these facts.
- The degree endpoint does not require adjacency to the extra vertex or
  complement connectivity. The upper bound remains valid even if either
  singleton has no complement neighbors.
- The finite degree theorem exposes decidable equality and adjacency through
  ordinary Mathlib instances; they do not encode a generated graph or oracle.

## Verification

Pinned Lean 4.33.1, Lake `5.0.0-src+819816b`, and Mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474`.

```sh
lake build
lake env lean Audit.lean
```

Both the current workspace build and a fresh isolated publication-directory
build passed without project warnings, 1008 jobs each. All three project
modules were recompiled in the fresh location. All 18 declarations, including
both constructors, were audited in both locations. Each depends exactly on
`propext`, `Classical.choice`, and `Quot.sound`. The four-clique specialization
also type-checks in both locations. Only pinned own-workspace dependency
caches were reused.

Singleton-component source SHA-256:

```text
491efb8c09af9c3b1245f80102c94afdf21a850939e747313d0453f059ed3130
```

Preserved reservoir source SHA-256:

```text
7e34e564981067fd638f22251b87b59f0d41c6c2a48e2ee247cff6e71d2cc18d
```

Preserved folding source SHA-256:

```text
0833b3835a66a4e36820239380577d99501f7cb84a710861eae1ad3dd4fe03a2
```

Trust comprises Lean's kernel, those standard axioms, pinned Mathlib proofs,
and the ordinary toolchain. This is a classical existence proof, not an
executable coloring search. No `sorry`, `admit`, custom axiom, unsafe shortcut,
`native_decide`, external data, solver output, or generated certificate is used.

## Unformalized application interface

For height 2933, the actual critical graph, its finite chromatic value, clique
and existence of two native singleton components must be supplied. The
current source closes the resulting neighborhood, nonedge, disjointness and
degree-bound implications. The original folding source closes non-domination
and its clique consequence.

No barrier extraction, separator-enumeration soundness, subsequent degree-excess
calculation, Gallai spectrum, crossing estimate, topology or complete
order-58 elimination is imported or certified. This is scoped formalization
authoring, not an independent review of those claims.
