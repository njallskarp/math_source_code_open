# Block-Hall compression in Lean

This pinned Lean project formalizes the finite matching bridge behind the
quotient-weight Hall test for complete-or-empty block relations. It was selected
from the independently reviewed Strong Seymour six-cluster frontier in Discovery
Net.

## Main theorem

Let finite source vertices `A` and target vertices `B` be assigned to quotient
blocks `I` and `J`. Let `Q i j` say that every vertex of source block `i` is
adjacent to every vertex of target block `j`. The expanded relation is therefore

```text
a ~ b  iff  Q (leftBlock a) (rightBlock b).
```

The project proves:

- `vertexHall_iff_blockHall`: ordinary Hall inequalities for every
  `S ⊆ A` are equivalent to the inequalities checked only on unions of whole
  source blocks,

  ```text
  |leftBlock⁻¹(U)| ≤ |rightBlock⁻¹(Γ(U))|  for every U ⊆ I;
  ```

- `blockHall_iff_cutHall`: these inequalities are equivalent to the dual
  target-cut inequalities

  ```text
  |leftBlock⁻¹(F(V))| ≤ |rightBlock⁻¹(V)|  for every V ⊆ J,
  ```

  where `F(V) = {i : every Q-neighbor of i lies in V}`;

- `blockNeighbors_cutSources_blockNeighbors`: the quotient closure preserves
  the neighbor set, `Γ(F(Γ(U))) = Γ(U)`; and

- `blockHall_iff_exists_injective` and
  `cutHall_iff_exists_injective`: either compressed family is equivalent to an
  actual injective matching `f : A → B` with `Q (leftBlock a) (rightBlock (f a))`.

The final equivalences invoke Mathlib's kernel-checked finite form of Hall's
marriage theorem.

No nonemptiness assumption on quotient blocks is needed for the Hall
equivalence: empty source blocks only add redundant quotient inequalities. The
separate theorem `vertexNeighbors_blockPreimage` records the stronger exact
neighbor-set equality for arbitrary quotient sets under surjectivity of
`leftBlock`.

## Reproduction

```sh
lake update
lake exe cache get
lake clean strong_seymour_block_hall
lake build
lake env lean BlockHallCompression.lean
```

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Expected result: the clean project build reports
`Build completed successfully (1010 jobs)` and the standalone replay exits
zero. The replay prints nine axiom audits, each containing only `propext`,
`Classical.choice`, and `Quot.sound`.

Source SHA-256:

```text
6fe955a4d39165f26e6ba8f18a3c2c3dd4bdc5d877d94de095428e76f7866cfe  BlockHallCompression.lean
```

## Theorem alignment

The primary source, Bai--Li--Park,
[“Towards a strengthening of the second neighborhood conjecture”](https://arxiv.org/abs/2607.18047v2),
defines complete matchings and applies Hall's theorem in Theorem 2.1. Its Remark
3.1 supplies the concrete six-cluster quotient and the six sufficient
inequalities for the order-36 no-strong-vertex construction.

The universal quotient-weight compression is not stated in that paper.
Discovery Net lemma
`bafkreidtb5vbrtchsfpojtvpgyyiqfoifmgsdqelg6ua5scxpqgmwuqs7i`
(height 2093), building on accepted review
`bafkreiaid3vz6b6hbc63itbfq5y5rdi6khnwnjwgy24kmo2wgtpmemn2va`
(height 2079), states the arbitrary-quotient block-Hall criterion, the dual
cut identity, and the tournament-specific sink reduction. This project
kernel-checks the complete-or-empty block matching core: block compression,
cut duality at the inequality level, closure, and existence of a matching.

When the quotient weights are the actual fiber sizes,
`|leftBlock⁻¹(U)|` and `|rightBlock⁻¹(Γ(U))|` are exactly the weighted sums in
the graph lemma.

## Trust boundary

Lean does **not** formalize here:

- tournaments, transitive blow-ups, first or exact second out-neighborhoods;
- the claim that only the terminal vertex of a transitive fiber can be strong;
- the concrete Dzitsoev quotient or its six obstruction subsets;
- the exact maximum-deficiency equality as an equality of integer maxima; or
- the exhaustive minimum-order and uniqueness computations.

Those are explicit external mathematical or computational bridges. The source
reads no external data and uses no generated certificate, solver, oracle,
floating point, plugin, `native_decide`, custom axiom, `unsafe` definition,
`sorry`, or `admit`.
