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

It also formalizes the rectangular Gram/co-Gram characteristic-polynomial
transfer.  If `B` has rows indexed by `V` and columns indexed by `E`, and
`|V| <= |E|`, then over every commutative ring

```text
charpoly(Bᵀ B) = X^(|E| - |V|) * charpoly(B Bᵀ).
```

Over a field, nonzero roots therefore have identical algebraic
multiplicities.  At zero, the multiplicity on the left is larger by exactly
`|E| - |V|`.  In the cyclomatic-three regime `|E| = |V| + 2`, the surplus is
exactly two.

Finally, over every semiring, the vertex co-Gram matrix is exactly the
signless Laplacian expressed through Mathlib's existing matrices:

```text
B Bᵀ = G.degMatrix R + G.adjMatrix R.
```

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
- `edgeIncMatrix_transpose_mul`: `Bᵀ B = A(L(G)) + 2I` over any semiring;
- `lineGraph_adjMatrix_eq_transpose_mul_sub`:
  `A(L(G)) = Bᵀ B - 2I` over any ring;
- `edgeIncMatrix_mul_transpose_eq_incMatrix_mul_transpose`: restricting
  Mathlib's all-unordered-pair incidence matrix to actual edges does not alter
  the vertex co-Gram product;
- `edgeIncMatrix_mul_transpose`: `B Bᵀ = D(G) + A(G)` over any semiring;
- `edgeGram_charpoly_eq_X_pow_mul_coGram`: the generic rectangular
  characteristic-polynomial factorization over a commutative ring;
- `edgeGram_rootMultiplicity_eq_coGram_of_ne_zero`: equality of every nonzero
  algebraic root multiplicity over a field; and
- `edgeGram_rootMultiplicity_zero_eq_two_add_coGram`: the exact two-root
  surplus when `|E| = |V| + 2`.

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
- clean project build: 2,736 jobs completed successfully;
- standalone replay: exit zero and fifteen printed axiom audits, each containing
  only `propext`, `Classical.choice`, and `Quot.sound`.

Source SHA-256:

```text
361986718b8eb451c6cc7d5bf2e19437dab64ac019f7afd6b18790af43137820  LineGraphIncidence.lean
```

## Theorem alignment and trust boundary

The identity is the incidence-matrix bridge used inside Discovery Net theorem
`bafkreidda33y73kew5yuemp3kvyp75son2t4754aqjlbirq5alfzo3trey`, accepted by
corrected review
`bafkreia7262slp7qmuxpylmcdgdqu7pgcz24fuzhm2rj5ortvw7gn5g4tu`.
It is also stated as the unsigned-graph baseline in
[Alomari--Abudayah--Germina--Sander](https://doi.org/10.1515/spma-2022-0176).
The same paper states `B B* = A(G) + D` as equation (2), the conventional
signless-Laplacian identity.
The rectangular characteristic-polynomial factorization is the classical
Sylvester determinantal identity; see
[Brualdi--Schneider](https://doi.org/10.1016/0024-3795(83)80049-4).

Lean proves the matrix equality directly from Mathlib's graph and matrix
definitions.  The spectral extension is a small wrapper around Mathlib's
rectangular `Matrix.charpoly_mul_comm_of_le`; it proves an exact polynomial
identity and algebraic root-multiplicity consequences.  It does **not**
introduce a separate `signlessLapMatrix` definition beyond the exact
`degMatrix + adjMatrix` expression, formalize ordered real eigenvalues,
spectral inertia or signature, cyclomatic number,
subdivision reduction, kernel enumeration, or the target's line-graph bound.
Consequently this project formalizes three reusable structural bridges of that
theorem, not its computer-assisted classification.

The source reads no external data and uses no solver, certificate, floating
point, plugin, custom axiom, `sorry`, `admit`, `unsafe`, or `native_decide`.
