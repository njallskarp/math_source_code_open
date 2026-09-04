# Reproducibility and axiom audit

## Pinned environment

- Lean toolchain: `leanprover/lean4:v4.33.1`
- Lean version: `4.33.1`
- Lean commit: `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib release input: `v4.33.1`
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`

The exact dependency closure is recorded in `lake-manifest.json`.

## Commands

```sh
lake update
lake exe cache get
lake clean strong_seymour_block_hall
lake build
lake env lean BlockHallCompression.lean
rg -n '\bsorry\b|\badmit\b|native_decide|^\s*unsafe\b|^\s*axiom\b' \
  BlockHallCompression.lean
shasum -a 256 BlockHallCompression.lean
```

## Expected evidence

- The clean project build reports
  `Build completed successfully (1010 jobs)`.
- The standalone replay exits zero.
- Nine `#print axioms` commands report only `propext`,
  `Classical.choice`, and `Quot.sound`.
- The forbidden-placeholder scan produces no matches.

The audited source hash is:

```text
6fe955a4d39165f26e6ba8f18a3c2c3dd4bdc5d877d94de095428e76f7866cfe  BlockHallCompression.lean
```

## Logical boundary

The kernel checks a theorem about arbitrary finite complete-or-empty bipartite
block relations and invokes Mathlib's finite Hall theorem for the matching
existence step. It does not check the external translation from a transitive
tournament blow-up to such a relation, nor the finite enumeration used for the
six-cluster order minimum.
