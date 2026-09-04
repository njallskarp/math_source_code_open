# Lean two-layer lift for square-saturated graphs

This Lean 4 project formalizes the reusable product-lift theorem isolated by
the independent review of the 432-edge square-saturated subgraph of `Q₈`.

Let `G₀` and `G₁` be square-saturated spanning subgraphs of a finite host `H`,
and let `D` be an independent dominating set in the intersection graph
`G₀ ⊓ G₁`. Put `G₀` and `G₁` in two disjoint layers and add the vertical edge
over exactly the vertices in `D`. The theorem
`twoLayer_productLift_squareSaturated` proves that the resulting graph is
square-saturated in the two-layer host. The exact edge count is

```text
|E(G₀)| + |E(G₁)| + |D|.
```

The corollary `productLift_squareSaturated` is the reviewed one-base-graph
statement, and `edge_budget_208_16` checks its `2 * 208 + 16 = 432`
specialization.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake build
```

Expected final line:

```text
Build completed successfully (1188 jobs).
```

The build prints axiom audits for eleven declarations. They use only the
standard Mathlib axioms `propext`, `Classical.choice`, and `Quot.sound`; the
source declares no project axiom and contains no `sorry` or `admit`.

## Theorem map

- `SquareWitness`, `SquareFree`, `SquareSaturatedIn`: a four-vertex
  three-edge witness interface equivalent to adding an omitted edge and
  creating a square.
- `twoLayerLift`: an actual Mathlib `SimpleGraph (Sum V V)` with horizontal
  graphs `G₀,G₁` and vertical matching indexed by `D`.
- `squareFree_twoLayerLift`: horizontal square-freeness plus independence in
  `G₀ ⊓ G₁` excludes every four-cycle in the lift.
- `twoLayer_productLift_squareSaturated`: generalized two-layer saturation
  theorem using domination in `G₀ ⊓ G₁` for every missing vertical edge.
- `productLift_squareSaturated`: reviewed same-graph specialization.
- `twoLayerHostIso`: identifies the host with Mathlib's box product
  `H □ K₂` (represented as the complete graph on `Bool`).
- `card_edgeFinset_twoLayerLift`: exact edge count, derived using Mathlib's
  handshaking lemma.
- `edge_budget_208_16`: arithmetic endpoint used by the reviewed `Q₈`
  construction.

## Alignment and trust boundary

The formal theorem is stronger than the reviewed product-lift lemma because
the two horizontal layers may differ; this generalization was stated and
proved informally in the independent review. The proof is otherwise exact:
the lift is a `SimpleGraph`, square-freeness quantifies over genuine
four-vertex cycles, saturation supplies the three selected edges completing
each omitted host edge, and the edge formula counts the graph's native
`edgeFinset`.

The project does **not** encode the explicit 208-edge `Q₇` graph, prove that
its syndrome-7 coset is an independent dominating set of size 16, or verify
the 432-edge invariant lower-bound CNFs/DRAT traces. Those finite data and the
restricted lower bound remain external. Mathlib does not currently supply a
named hypercube graph, so identifying `Q_{d+1}` with `Q_d □ K₂` also remains an
application-level definition, although `twoLayerHostIso` proves the product
identification abstractly.

Discovery Net sources:

- target lemma, height 757:
  `bafkreick6ujgbme65d2yufxgx26ni7fzqavyvykadfqlslzzzdhafyxviu`;
- independent review, height 773:
  `bafkreieeh3vjjxgcyr5bdmym5czml5v6ub7h4rhiuyvutpl6pblgzvhpki`.

Literature context:

- J. Robert Johnson and Trevor Pinto, *Saturated Subgraphs of the
  Hypercube*, arXiv:1406.1766.
- Natasha Morrison, Jonathan A. Noel, and Alex Scott, *Saturation in the
  Hypercube and Bootstrap Percolation*, arXiv:1408.5488.

These papers define hypercube saturation and prove general/asymptotic bounds.
The searched primary sources do not state this independent-dominating-set
product lift. No literature-priority claim is made here.
