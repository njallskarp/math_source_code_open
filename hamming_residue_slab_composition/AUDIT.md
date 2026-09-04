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
lake clean hamming_residue_slab_composition
lake build ResidueSlabComposition
lake env lean ResidueSlabComposition.lean
rg -n 'sorry|admit|native_decide|unsafe|axiom ' ResidueSlabComposition.lean
```

## Expected evidence

- clean build: success (`3007` jobs in the audited workspace);
- standalone Lean replay: exit status zero;
- nine `#print axioms` reports: only `propext`, `Classical.choice`, and
  `Quot.sound`, with some declarations using a subset;
- source scan: no match for `sorry`, `admit`, `native_decide`, `unsafe`, or a
  project-defined `axiom`.

The `.lake` directory and all generated build products are excluded from the
published source.

## Theorem and scope audit

Lean constructs the residue-slab coloring and proves its surjectivity, fiber
size, abstract line containment, exact number of colors, exact scheme deficit,
and optimal quotient count under the reviewed remainder condition. The base
partition is an explicit hypothesis. The cyclic rectangle constructor,
concrete Hamming graph/lift, majority threshold, upper-bound dependency, and
explicit family specialization are not encoded.
