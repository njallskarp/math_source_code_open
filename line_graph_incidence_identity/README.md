# Line-graph incidence identity in Lean

This pinned Lean project formalizes the standard unsigned-incidence identity

```text
Bᵀ B = A(L(G)) + 2I,
```

and, over a ring, its equivalent form

```text
A(L(G)) = Bᵀ B - 2I.
```

The statement uses Mathlib's `SimpleGraph`, `SimpleGraph.lineGraph`,
`SimpleGraph.incMatrix`, and `SimpleGraph.adjMatrix` definitions.  It applies
to every finite simple graph and every semiring; no connectedness, minimum
degree, or cyclomatic-number hypothesis is needed.

## Formal interface

Mathlib's `incMatrix` has one column for every unordered vertex pair.  The
definition

```lean
edgeIncMatrix R G : Matrix V G.edgeSet R
```

restricts it to the actual edge subtype, producing the usual vertex-by-edge
unsigned incidence matrix.

The principal exported theorems are:

- `edgeIncMatrix_transpose_mul_apply_eq_card_inter`: each Gram entry is the
  cardinality of the two edges' common-endpoint finset, cast into the
  coefficient semiring;
- `edgeIncMatrix_transpose_mul`: `Bᵀ B = A(L(G)) + 2I` over any semiring; and
- `lineGraph_adjMatrix_eq_transpose_mul_sub`:
  `A(L(G)) = Bᵀ B - 2I` over any ring.

Supporting lemmas prove that actual simple-graph edges have two endpoints,
that adjacent line-graph vertices share exactly one endpoint, and that
distinct nonadjacent ones share none.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean LineGraphIncidence.lean
```

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Expected results with the committed manifest:

- Mathlib cache: 8,690 artifacts;
- clean project build: 1,348 jobs completed successfully;
- standalone replay: exit zero and eight printed axiom audits, each containing
  only `propext`, `Classical.choice`, and `Quot.sound`.

Source SHA-256:

```text
b6673841bcf580118bb536ad38b2e63e54f48c937fe8113338298a78f50059e1  LineGraphIncidence.lean
```

## Theorem alignment and trust boundary

The identity is the incidence-matrix bridge used inside Discovery Net theorem
`bafkreidda33y73kew5yuemp3kvyp75son2t4754aqjlbirq5alfzo3trey`, accepted by
corrected review
`bafkreia7262slp7qmuxpylmcdgdqu7pgcz24fuzhm2rj5ortvw7gn5g4tu`.
It is also stated as the unsigned-graph baseline in
[Alomari--Abudayah--Germina--Sander](https://doi.org/10.1515/spma-2022-0176).

Lean proves the matrix equality directly from Mathlib's graph and matrix
definitions.  It does **not** formalize spectral inertia, the equality of
nonzero spectra of `BᵀB` and `BBᵀ`, signless Laplacians, cyclomatic number,
subdivision reduction, kernel enumeration, or the target's bound on
line-graph signature.  Consequently this project formalizes one reusable
structural bridge of that theorem, not its computer-assisted classification.

The source reads no external data and uses no solver, certificate, floating
point, plugin, custom axiom, `sorry`, `admit`, `unsafe`, or `native_decide`.
