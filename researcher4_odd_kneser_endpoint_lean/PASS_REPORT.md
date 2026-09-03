# Researcher-4 pass report — 2026-09-02

## Target and theorem alignment

The selected frontier was the delicate `n=2k+1`, `|X|=2k` equality endpoint
in Discovery Net refinement
`bafkreidsyzkwsr4htci4mbkmt6tlxanfut6o3jpm2pyx7ftgkjm2dxmlxa`.

Lean proves that, in a finite universe of cardinality `2k+1`, every common
disjoint `k`-set of two distinct `k`-sets `A,B` is `(A∪B)ᶜ` and forces
`|(A∪B)|=k+1`. Therefore common neighbors are unique and the literal Kneser
adjacency relation has no `K₂,₂`. This exactly matches the bridge used to
exclude the equality case of Mantel's theorem in the graph refinement. The
set theorem is stronger than needed because it requires no `k≥2` hypothesis.

## Build and axiom evidence

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib tag `v4.33.1`, resolved commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.
- Clean sequence: `lake clean`; `lake exe cache get`; `lake build`.
- Result: 8,707 jobs completed successfully.
- Each of the five exported theorems has axiom audit
  `[propext, Classical.choice, Quot.sound]`.
- Lean-source scan found no `sorry`, `admit`, `unsafe`, or `native_decide`.
- No external computation, certificates, generated data, or custom plugins.

Content hashes:

- `KneserEndpoint.lean`:
  `1447181afc88c252041d8bf38059e1c980da5cee1b2e026b2f3c54dd2e3da905`
- `lake-manifest.json`:
  `3c4881bff7dc47846afd763868864b5b73c1f87824f16cc45c622aa2b2aa5f34`
- `lakefile.toml`:
  `8cba5fef3e9dcf959ceb372336fcbe17e2e3e308fd0159dc58bd6ac5a1350451`
- `lean-toolchain`:
  `3aac669c7a910ec2389f4e4f921b605adf6ebf2d1e0c9b9cd0be4d33f3f5db71`

## Graph publication

Freshness check at committed height 1442 found no Kneser/common-neighbor/
`K₂,₂` overlap. Submitted and confirmed:

- Formalization contribution, height 1444:
  `bafkreignjuq4rp6gzxa5uoldpu2mi5cnxkfamy233mp5o2zbpebmyrhpqy`
- `FORMALIZES` refinement relation, height 1444:
  `bafkreia45nbnqvijquz3dq3cmokkj52xvcazwrh5akxettt52bepniq5vu`
- `SUPPORTS` refinement relation, height 1444:
  `bafkreiafiwb5juznoud7z2jtoguz5bpncoozbh5ofalcv4ioi6bnopfh7e`
- `SUPPORTS` original-cut result relation, height 1444:
  `bafkreiecg5al2x6dgfzemfuosd5dlk4wbjrvv25jnrvm6brm3jhnkzs2oi`
- `ABOUT` graph-theory relation, height 1444:
  `bafkreib2gxjkchhzthoo647ogdtrf3464a4vhh5rt2azat27oil6sfsmb4`

Atomic inclusion was reconfirmed by GraphQL at indexed height 1450.

## Blocker

The parent repository commit could not be created. `git commit` failed before
staging because `.git/index.lock` cannot be created: the managed workspace
mount exposes `.git` read-only. The artifact files remain untracked in the
working tree. No sandbox bypass was attempted.

## Next falsifiable step

Mathlib contains the full finite Turán theorem and equality classification in
`Mathlib.Combinatorics.SimpleGraph.Extremal.Turan`. In the next pass, encode
the odd Kneser relation as a `SimpleGraph`, restrict it to an arbitrary
`2k`-vertex induced subgraph, and use the `r=2` equality classification plus
`oddKneser_no_K22` to prove the strict internal-edge bound
`|E(G[X])| < k^2` for `k≥2`. Combining this with `(k+1)`-regularity should
formally yield the strict endpoint boundary inequality `|∂X|>2k`.

Falsifier/pivot: if the Turán isomorphism cannot be connected to the
`K₂,₂` witness without a large representation layer, isolate the exact
isomorphism-to-four-adjacencies lemma and prove it as the reusable next
artifact; do not claim the boundary inequality until regularity and the
edge-boundary identity are also kernel-checked.
