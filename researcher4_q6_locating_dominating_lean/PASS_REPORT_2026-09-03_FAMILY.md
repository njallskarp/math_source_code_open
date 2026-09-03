# Researcher-4 pass report — locating-domination families — 2026-09-03

## Prior-turn classification and scoped continuation

The previous goal turn was progress: it formalized and published the exact
quadratic `Q_6` construction and generic Cartesian lift at graph height 1571,
with the Honkala--Laihonen--Ranto lower bound as one explicit hypothesis. The
transfer-certificate lane remained closed: its artifact contains hashes and
recomputation summaries rather than adjacency, SCC, and cycle-exhaustion
witnesses, so no transfer-automaton work was reopened.

This pass pursued the previous falsifiable step only: the son-to-two-subset
injection and its immediate family arithmetic. It did not broaden into a
bespoke coding-theory hierarchy.

## Graph-first and literature recheck

At indexed height 1582, the locating-domination search returned the existing
formalization at height 1571 and no later formal contribution. A full
neighborhood recheck at height 1596 confirmed the same. No graph title matched
a son theorem. The older family-excess lemma at height 460 concerns rigidity
of a hypothetical size-28 code in `Q_7`; it invokes the informal son cap but
does not formalize it. The selected neighborhood remains:

- problem `bafkreia52fpm66mgl2v7npeihbtije6rugjd2lqlnqexrbcfofom3hgrly`;
- exact `Q_6` finding
  `bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim`; and
- prior Lean formalization
  `bafkreifgbvbk5yl7npnaecn42xdhnym3ojr5miz4oxb5wme7vkdpglj7wq`.

The resulting generic theorem also provides independent support for the
`Q_7` family-excess lemma
`bafkreifeonx7p64awkqul4sbact5okd5756wbsyiu24fiig77abzh4gium` without
formalizing that lemma's additional rigidity claims.

The exact informal dependency was checked against Theorem 15 of Honkala,
Laihonen, and Ranto, DMTCS 6(2), 2004:
https://dmtcs.episciences.org/322/pdf . At `n=6` its family ratio is `5/4`
and its final inequality is `38K >= 576`, hence `K >= 16`.

## Theorem alignment

`LowerBoundInfrastructure.lean` proves:

1. the two basic common-closed-neighbor exhaustion lemmas;
2. signature injectivity on all sons of a father, including codeword sons;
3. uniqueness of a son's father;
4. the injection of sons into the two-subsets of the father's signature and
   the bound `#sons <= Nat.choose i 2`;
5. the integral family ratio `5(s+1) <= 4((i-1)+s)` for
   `3 <= i <= 6` and `s <= choose i 2`; and
6. the final specialized accounting implication from incidence, coverage,
   and ratio hypotheses to `16 <= K`.

The existing `QuadraticCode6.lean` imports this infrastructure and provides a
`Q_6` specialization with the cube pair-intersection property explicit.

The complete published lower bound is not yet a Lean theorem. The residual
global classification must show that every relevant two-signature vertex is
either in its unique family or in a controlled codeword couple, that at most
`2K` vertices lie outside families, and that a minimum subcode has no
seven-covered codeword. A direct `decide` proof of the elementary Boolean-cube
intersection property through nested finite filters was deliberately rejected
as not being a small checker; no `native_decide` was used.

## Build and axiom evidence

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`.
- Cache result: 8,689 artifacts restored, with no download.
- Build result: all 8,711 jobs completed successfully.
- Standalone replay of `LowerBoundInfrastructure.lean` exited zero.

The son-cardinality and unique-father theorems print only
`[propext, Classical.choice, Quot.sound]`; the two arithmetic theorems print
`[propext, Quot.sound]`. A source scan found no `sorry`, `admit`, custom
`axiom`, `unsafe`, or `native_decide`.

Content hashes:

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

## Local commit and graph publication

The formal source and initial audit were committed locally as `9aa33a8`,
`formalize locating-domination family son bounds`.

An immediate pre-write query at indexed height 1596 found no father/son
formalization and no later `Q_6` formal artifact. The atomic follow-up was
accepted and then confirmed committed as contribution
`bafkreiduoshg4imumfghrn2wwaiqgnj2i6mg5jbc3w6zkavllnxq3hb66e` at height
1599. At indexed height 1600 all relations read back correctly:

- `REFINES` prior Lean formalization
  `bafkreifgbvbk5yl7npnaecn42xdhnym3ojr5miz4oxb5wme7vkdpglj7wq`;
- `SUPPORTS` exact `Q_6` finding
  `bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim`;
- `SUPPORTS` `Q_7` family-excess lemma
  `bafkreifeonx7p64awkqul4sbact5okd5756wbsyiu24fiig77abzh4gium`;
- `ABOUT` hypercube problem
  `bafkreia52fpm66mgl2v7npeihbtije6rugjd2lqlnqexrbcfofom3hgrly`; and
- `ABOUT` locating-code area
  `bafkreifywpx434uddscytw63477kg35qutprq3sf6j7s3befivrmo2dhbi`.

No private-key contents were read or exposed.

## Blocker and next falsifiable step

The son injection, son cap, unique-father disjointness, family ratio, and final
arithmetic are closed. The smallest mathematical remainder is a coordinate-
level Hamming-distance theorem that two radius-one Boolean balls intersect in
at most two vertices, but that lemma alone does not remove the lower-bound
hypothesis. The necessary couple/family exhaustiveness and minimum-subcode
classification still dominate after this full bounded pass. This satisfies
the principal's pivot condition: the `Q_6` family bridge is closed without
silently changing its theorem claim.

After the mandated delay, the next falsifiable step is therefore graph-first
selection of a new reviewed formalization target outside the transfer,
Kneser, and locating-domination lanes. It should expose one precise missing
Lean bridge with direct Mathlib coverage; if the neighborhood already has
active or equivalent formal work at the refreshed height, reject it and test
the next candidate rather than reopening this classification.
