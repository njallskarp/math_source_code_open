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

For the same incidence matrix over any commutative ring, provided
`|V| <= |E|`, Lean also proves

```text
charpoly(Bᵀ B) = X^(|E| - |V|) * charpoly(B Bᵀ).
```

Over a field this implies equality of the algebraic root multiplicity at every
nonzero scalar and an exact zero-root surplus of `|E| - |V|`.  The specialized
hypothesis `|E| = |V| + 2` gives a surplus of two.

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

The characteristic-polynomial factorization is the rectangular `AB`/`BA`
identity already supplied by Mathlib as `Matrix.charpoly_mul_comm_of_le`, with
`A = Bᵀ`.  Polynomial root-multiplicity addition then isolates the `X` factor:
it contributes no multiplicity away from zero and contributes exactly its
exponent at zero.

## What remains external

This project does not define or prove:

- an identification of `BBᵀ` with a separately defined signless Laplacian;
- ordered real eigenvalues or an inertia/signature transfer theorem;
- cyclomatic number, suppression, subdivision congruence, or kernel
  classification; or
- the 26,688-case exact computation in the graph target.

Those omissions are explicit: none occurs as an unnamed Lean hypothesis in
the exported identities.  The Gram identity is unconditional for finite
simple graphs, and the spectral bridge assumes only the displayed cardinality
inequality (plus a field for root multiplicities).  Its later inertia and
classification uses remain separate dependencies.

## Build and axiom evidence

With Lean 4.33.1 and Mathlib v4.33.1 pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`:

```text
lake clean                         success
lake exe cache get                 8,690 artifacts available
lake build                         1,793 jobs completed successfully
lake env lean LineGraphIncidence.lean
                                   success
```

All thirteen audited declarations report only Lean's standard axioms `propext`,
`Classical.choice`, and `Quot.sound`.  A source scan found none of `sorry`,
`admit`, a custom `axiom`, `unsafe`, or `native_decide`.

Source SHA-256:

```text
fb4293e47298bc316d1575559909ce6c1481fc2c373f75ddcac462f787a43453
```
