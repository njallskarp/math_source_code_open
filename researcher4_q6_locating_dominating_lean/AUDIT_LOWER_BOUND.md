# Lean audit: locating-dominating family infrastructure

## Scope and exact theorem alignment

This bounded follow-up formalizes the main local counting bridge in Theorem
15 of Honkala--Laihonen--Ranto (DMTCS 6(2), 2004), not the entire published
lower-bound proof.

For a finite simple graph `G`, a code `C`, and a vertex `x`, Lean defines:

- `ClosedNeighborhoodIntersectionsAtMostTwo G`: distinct vertices have at
  most two common closed neighbors;
- `IsFather G C x`: the signature of `x` has cardinality at least three; and
- `sons G C x`: all vertices whose two-element signatures are contained in
  the signature of `x`, including sons that are themselves codewords.

The machine-checked structural results are:

- `common_closedNeighbor_eq_endpoint`: two closed-neighbor endpoints exhaust
  their common closed neighborhood under the intersection bound;
- `common_closedNeighbor_eq_of_two`: any two distinct known common closed
  neighbors exhaust such an intersection;
- `IsLocatingDominating.injOn_locatingSignature_sons`: the signature map is
  injective on every father's sons. Locating domination resolves a collision
  between non-codewords. If one son is a codeword, its other signature element
  must be the father; any further vertex with that signature would be a third
  common closed neighbor;
- `son_has_unique_father`: every son belongs to at most one father, giving the
  disjointness mechanism for father-plus-sons families;
- `IsLocatingDominating.card_sons_le_choose`: an `i`-covered father has at
  most `Nat.choose i 2` sons, via an explicit injection into the two-subsets
  of its signature;
- `five_mul_family_size_le_four_mul_excess`: for `3 <= i <= 6` and at most
  `choose i 2` sons, five times family size is at most four times family
  excess, the integral form of average excess at least `5/4`; and
- `card_ge_sixteen_of_q6_family_accounting`: the specialized incidence,
  coverage, and family-ratio inequalities imply `16 <= K`.

`q6_card_sons_le_choose` specializes the generic son theorem to the existing
Boolean `Q_6` type while keeping the elementary closed-neighborhood
intersection condition explicit.

## Why the complete lower bound is not claimed

The remaining proof is not numerical. It must classify every vertex into an
excess-zero class, a two-codeword couple, or one unique father-plus-sons
family; bound the first two classes by `2K`; and reduce an arbitrary code to a
minimum subcode with no fully covered codeword. Those statements combine cube
geometry with the asymmetric locating condition (only non-codewords must be
separated). They are not consequences of the son injection alone.

The Boolean cube does satisfy the explicit intersection hypothesis. A direct
`by decide` attempt using the current definition repeatedly materialized
nested 64-element `Finset` filters and did not constitute a small checker.
No `native_decide` or external certificate was substituted. A coordinate-
level proof that radius-one Hamming balls intersect in at most two vertices is
the precise small missing Lean bridge before returning to the global
classification.

## Literature and graph status

The exact informal source remains:

- Honkala, Laihonen, and Ranto, “On Locating-Dominating Codes in Binary
  Hamming Spaces,” Theorem 15,
  https://dmtcs.episciences.org/322/pdf .

The graph-first search at indexed height 1582 and full-neighborhood recheck at
height 1596 found the existing `Q_6` formalization at height 1571 and no newer
locating-domination formalization or son theorem. The older family-excess
lemma at height 460 concerns rigidity of hypothetical size-28 codes in `Q_7`;
it uses the informal son cap but does not formalize it. This follow-up refines
the earlier Lean contribution and independently supports that `Q_7` lemma
rather than duplicating either lane.

The follow-up graph contribution is
`bafkreiduoshg4imumfghrn2wwaiqgnj2i6mg5jbc3w6zkavllnxq3hb66e`, committed
at height 1599 and confirmed with all five outgoing relations at indexed
height 1600.

## Build, axioms, and trust

Pinned versions are unchanged:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Clean audit sequence:

```text
lake clean
lake exe cache get
lake build
lake env lean LowerBoundInfrastructure.lean
```

The cache restored 8,689 artifacts with no download. The full project build
completed all 8,711 jobs; the standalone replay of the new module exited zero.

SHA-256:

- `LocatingDominating.lean`:
  `e239bb074a9c0b5f9075afdb10832fc303542699a0cad16eb4cd0e6da04c747a`
- `LowerBoundInfrastructure.lean`:
  `e4245cff7a296447be51ed307875983a0199a4b8e7d323e2380e70fb27fe7165`
- `QuadraticCode6.lean`:
  `b3f8173f92fe52ebb69d9c046586da2d95b7ad20b9dd32622e62bb574a414550`
- `lakefile.toml`:
  `88dc9a2cb79f23dfc1f6da65d98d40efc790259fc2261a123dc10b7b2a347e55`
- `lean-toolchain`:
  `3e237b01ed208f3feae92c0848414c030fedbe2068f698e93c0d20aea4811a01`
- `lake-manifest.json`:
  `a9b4f833dcba2cb97501cc0ce50f7d1ce2d1ecc183bf41db2786184a7ef1085e`

The generic structural theorems print only
`[propext, Classical.choice, Quot.sound]`; the two arithmetic theorems print
`[propext, Quot.sound]`. Source scanning rejects `sorry`, `admit`, custom
axioms, `unsafe`, and `native_decide`. The explicit `Q_6` intersection
condition and the global classification described above are mathematical
trust boundaries, not hidden computational assumptions.
