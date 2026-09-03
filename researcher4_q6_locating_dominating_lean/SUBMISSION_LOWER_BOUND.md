# Lean father/son infrastructure for locating-dominating lower bounds

## Result

This pinned Lean/Mathlib follow-up formalizes a central bridge in the
Honkala--Laihonen--Ranto family/excess proof. For any finite simple graph in
which distinct closed neighborhoods have intersection cardinality at most
two, and for any locating-dominating code, Lean proves:

- signatures are injective on every father's full set of two-signature sons,
  including codeword sons;
- each son has at most one father;
- an `i`-covered father has at most `Nat.choose i 2` sons; and
- for `3 <= i <= 6`, the father-plus-sons family has average excess at least
  `5/4`.

The proof constructs the signature injection into `powersetCard 2`. Equal
signatures at non-codewords are handled by locating domination. For a
codeword son, closed-neighborhood geometry forces the second signature
element to be the father and excludes any collision as a third common closed
neighbor. A separate theorem proves the final `Q_6` integer implication: if
`E + 64 = 7K`, `64 <= F + 2K`, and `5F <= 4E`, then `16 <= K`.

The existing Boolean `Q_6` module exports the son cap with its elementary
closed-neighborhood intersection hypothesis explicit.

## Reproducibility and boundary

The project pins Lean 4.33.1 and Mathlib `v4.33.1` at commit
`0df444a360eaa60ab8c11dca51a86af692955474`. After `lake clean`, the cache
restored 8,689 artifacts with no download and `lake build` completed all 8,711
jobs. Standalone replay of the new module exited zero. The structural theorems
print `[propext, Classical.choice, Quot.sound]`; the arithmetic theorems omit
`Classical.choice`. There is no `sorry`, `admit`, custom axiom, `unsafe`, or
`native_decide`.

SHA-256 of `LowerBoundInfrastructure.lean` is
`e4245cff7a296447be51ed307875983a0199a4b8e7d323e2380e70fb27fe7165`.
Local evidence commit: `9aa33a8`.
Committed Discovery Net contribution:
`bafkreiduoshg4imumfghrn2wwaiqgnj2i6mg5jbc3w6zkavllnxq3hb66e` at height
1599 (relation readback at indexed height 1600).

This contribution does not claim the complete universal lower bound. Two
bridges remain explicit:

1. a coordinate-level proof that two radius-one Hamming balls in the Boolean
   cube intersect in at most two points (direct nested-`Finset` reduction was
   not a small checker); and
2. the global classification into excess-zero vertices, couples, and unique
   father-plus-sons families, together with the minimum-subcode argument that
   rules out a fully covered codeword.

The exact primary source is Honkala, Laihonen, and Ranto, DMTCS 6(2), Theorem
15: https://dmtcs.episciences.org/322/pdf .
