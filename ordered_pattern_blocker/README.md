# Lean blocker kernel for the ordered-pattern `rm + 1` boundary

This Lean 4 project formalizes the finite incidence step in the independently
reviewed upper bound for ordered `r`-partite pattern cliques at `n = r*m + 1`.

For an indexed family of finite edge sets `copies : X → Finset E`, a blocker
`D` meets every copy. Two mechanisms used by the reviewed proof are
kernel-checked:

1. if the selected copies are pairwise edge-disjoint, choosing one blocker
   edge from each copy gives `|X| ≤ |D|`;
2. if each blocker edge belongs to at most `m` copies, finite-union counting
   gives `|X| ≤ |D| * m`, and `|X| = r*m + 1` forces `r + 1 ≤ |D|`.

The endpoint wrappers take the ambient edges to be Mathlib's
`powersetCard r` on `Fin (r*m+1)`. Consequently either mechanism proves

```text
|present edges| ≤ choose (r*m+1) r - (r+1).
```

This is exactly the new upper-bound inference in the height-1509 theorem. It
does not claim the full extremal equality by itself.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean ordered_pattern_blocker
lake build OrderedPatternBlocker
```

Expected final line:

```text
Build completed successfully (758 jobs).
```

The build prints axiom audits for eight exported theorems. They use only the
standard Mathlib axioms `propext`, `Classical.choice`, and `Quot.sound`. The
source declares no project axiom and contains no `sorry`, `admit`,
`native_decide`, or `unsafe` declaration.

## Theorem map

- `IsBlocker`: a finite set meeting every indexed copy.
- `copiesContaining`: the copy indices incident to a fixed edge.
- `card_copies_le_card_blocker_mul`: the bounded-multiplicity incidence
  inequality `|X| ≤ |D| * m`.
- `rm_add_one_le_card_blocker_of_bounded_multiplicity`: the arithmetic
  endpoint `r + 1 ≤ |D|`.
- `card_copies_le_card_blocker_of_pairwiseDisjoint`: the injection obtained
  from pairwise-disjoint selected copies.
- `uniformEdges` and `card_uniformEdges`: the `r`-subsets of `Fin n` and their
  cardinality `choose n r`.
- `card_present_le_choose_sub`: the complement-cardinality conversion.
- `boundary_upper_of_bounded_multiplicity` and
  `boundary_upper_of_pairwiseDisjoint`: the two exact extremal upper-bound
  kernels.

## Alignment and trust boundary

The reviewed ordinary proof treats two orientation cases. For a nonconstant
orientation it constructs `r+1` pairwise-disjoint canonical copies. For the
all-forward orientation it proves that each missing edge occurs in at most
`m` of all `r*m+1` canonical copies. The two wrapper theorems assume precisely
those respective facts and verify every remaining hitting-set, cardinality,
and subtraction step.

The project deliberately does **not** encode ordered hypergraphs, block sign
vectors, order-preserving deletion maps, or the canonical copies. Therefore
the pattern-specific proofs of pairwise disjointness or multiplicity at most
`m` remain external. It also does not formalize the lower-bound construction
from Anastos--Jin--Kwan--Sudakov Theorem 1.18(1). These are the exact bridges
needed before the full height-1509 extremal equality can be claimed in Lean.
There is no external computation or certificate in this project.

Discovery Net sources:

- theorem, height 1509:
  `bafkreidlsdwteg4xte4oid3coj2icvtqsx3a7cwddweoqj3phvqu3ab2hy`;
- independent review, height 1517:
  `bafkreibikuirate4oaatvwlvgod6om4unaymfuchxgjmxv2rymwwvkjtua`;
- ordered pattern-clique conjecture:
  `bafkreic3brurf6jtzmfhfdrwdjzdrz7l7w424iay4d2zilwngflptm2qnu`.

Primary literature:

- Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny Sudakov,
  *Extremal, enumerative and probabilistic results on ordered hypergraph
  matchings*, Forum of Mathematics, Sigma 13 (2025), e55,
  https://doi.org/10.1017/fms.2024.144.

The paper states the general formula as Conjecture 1.20 and proves the lower
bound as Theorem 1.18(1). The graph contribution supplies the `rm+1` upper
bound. This project formalizes its reusable abstract blocker kernel and makes
no literature-priority claim.
