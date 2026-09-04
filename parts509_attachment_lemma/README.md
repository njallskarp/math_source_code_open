# Lean attachment lemma for the Parts-509 vertex cuts

This Lean 4 project formalizes the generic vertex-deletion argument isolated by
the independent review of the strict Parts-509 connectivity result.

Let `D` be a finite set of attached vertices in a finite simple graph `G`, and
let the core be `V(G) \ D`. Assume:

1. after deleting any set `T` with `|T| <= d`, the surviving core is connected;
2. every neighbor of a vertex in `D` lies in the core (so `D` is independent);
3. every vertex in `D` has degree exactly `d`.

Then, for every `S` with `|S| <= d`, the graph `G - S` is disconnected if and
only if

```text
S = N_G(x)
```

for some surviving `x in D`. In particular, fewer than `d` deletions never
disconnect the graph, and the neighborhoods of attached vertices are cuts of
size `d`. The theorem `degree_four_attachment_vertex_cuts` specializes the
classification to `d = 4`, the value in the strict Parts-509 graph.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake build
```

Expected final line:

```text
Build completed successfully (986 jobs).
```

The build also runs eight `#print axioms` audits. Each theorem uses only
Mathlib's standard `propext`, `Classical.choice`, and `Quot.sound`; there are no
project axioms and no `sorry`/`admit` placeholders.

## Theorem map

- `deleteConnected_of_core_and_attachments`: connects the surviving graph from
  the connected core plus one surviving attachment edge per attached vertex.
- `not_deleteConnected_of_neighborFinset_subset`: proves that deleting an
  attached vertex's whole neighborhood isolates it.
- `deleteConnected_iff_no_deleted_neighborhood`: fixed-fault-set iff.
- `small_vertex_cut_iff_eq_neighborFinset`: exact classification for all fault
  sets of size at most `d`.
- `attached_neighborhood_disconnects`: existence of the neighborhood cuts.
- `small_vertex_cut_card_eq`: every small cut has cardinality exactly `d`.
- `attachment_vertex_connectivity_threshold`: exact deletion threshold.
- `degree_four_attachment_vertex_cuts`: literal Parts-509 degree-four
  specialization.

## Alignment and trust boundary

The formal source uses Mathlib's native `SimpleGraph.induce`, `Connected`,
`Reachable`, and `neighborFinset` interfaces. It does **not** encode the 509
vertices, the 2,442 edges, the path certificate, unit-distance geometry,
chromaticity, or the edge-cut half of the reviewed result. To apply the
degree-four theorem to Parts-509 one must still import the externally checked
facts that the 503-vertex core survives every deletion of at most four vertices,
the six deleted vertices have degree four with all neighbors in the core, and
their neighborhoods have the desired distinctness.

Discovery Net sources:

- target lemma, height 1014:
  `bafkreiblvrvz555ga37vfqauuvzkficcgmfxjn25n3zxlxnulv5hj6j7f4`;
- independent review and abstract attachment lemma, height 1036:
  `bafkreicq6iozccksj5i2rz7lnbk2iorkcixxe5uazzrzfevklhl464pzzy`.

The underlying graph is from Jaan Parts, *Graph minimization, focusing on the
example of 5-chromatic unit-distance graphs in the plane*, Geombinatorics 29(4)
(2020), 137--166: <https://arxiv.org/abs/2010.12665>. That paper supplies the
509-vertex, 2,442-edge construction, not this formal attachment theorem. The
generic lemma is elementary and no literature-priority claim is made.
