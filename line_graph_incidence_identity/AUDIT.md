# Audit: line-graph incidence identity

## Exact statement

Let `G : SimpleGraph V`, where `V` is finite, and let `B` be Mathlib's
unoriented incidence matrix restricted from all unordered pairs to
`G.edgeSet`.  For any semiring `R`, Lean proves

```text
Bᵀ B = G.lineGraph.adjMatrix R + (2 : R) • I.
```

For any ring `R`, it then proves the reviewed subtraction form

```text
G.lineGraph.adjMatrix R = Bᵀ B - (2 : R) • I.
```

The theorem is more general than the real-valued finite connected instance
used in the cyclomatic-three line-graph proof.

## Proof architecture

`edgeIncMatrix` is a `Matrix.submatrix` of Mathlib's `incMatrix`, with columns
indexed by the edge subtype.  Expanding matrix multiplication and using
`SimpleGraph.edge_mem_incidenceSet_iff` reduces each Gram entry to

```text
|(endpoints e) ∩ (endpoints f)|.
```

Mathlib's off-diagonal property of simple-graph edges gives two-element
endpoint finsets.  A generic finite-set lemma proves that two distinct
two-element finsets with nonempty intersection have intersection cardinality
one.  `SimpleGraph.lineGraph_adj_iff_exists` identifies this nonempty
intersection with line-graph adjacency.  Diagonal entries are two and
distinct nonadjacent entries are zero.  Matrix extensionality then establishes
the semiring identity; additive cancellation gives the ring subtraction form.

## What remains external

This project does not define or prove:

- the signless Laplacian identity `Q(G)=BBᵀ`;
- equality of the nonzero spectra of `BᵀB` and `BBᵀ`;
- any inertia or signature transfer theorem;
- cyclomatic number, suppression, subdivision congruence, or kernel
  classification; or
- the 26,688-case exact computation in the graph target.

Those omissions are explicit: none occurs as an unnamed Lean hypothesis in
the exported matrix identity.  The formal theorem is unconditional for finite
simple graphs, while its later spectral and classification uses remain
separate dependencies.

## Build and axiom evidence

With Lean 4.33.1 and Mathlib v4.33.1 pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`:

```text
lake clean                         success
lake exe cache get                 8,690 artifacts available
lake build                         1,348 jobs completed successfully
lake env lean LineGraphIncidence.lean
                                   success
```

All eight audited declarations report only Lean's standard axioms `propext`,
`Classical.choice`, and `Quot.sound`.  A source scan found none of `sorry`,
`admit`, a custom `axiom`, `unsafe`, or `native_decide`.

Source SHA-256:

```text
b6673841bcf580118bb536ad38b2e63e54f48c937fe8113338298a78f50059e1
```
