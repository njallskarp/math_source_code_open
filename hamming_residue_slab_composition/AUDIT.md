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
lake build ResidueSlabComposition HammingLift
lake env lean ResidueSlabComposition.lean
lake env lean HammingLift.lean
rg -n '\bsorry\b|\badmit\b|native_decide|^\s*unsafe\b|^\s*axiom\b' \
  ResidueSlabComposition.lean HammingLift.lean
```

## Expected evidence

- clean build: success (`3036` jobs in the audited workspace);
- both standalone Lean replays: exit status zero;
- eighteen `#print axioms` reports: only `propext`, `Classical.choice`, and
  `Quot.sound`, with some declarations using a subset;
- source scan: no match for `sorry`, `admit`, `native_decide`, `unsafe`, or a
  project-defined `axiom`.

Source SHA-256 values:

```text
ResidueSlabComposition.lean  ca70fbb6e5c7a4719a6e139f5aa4919638cffffc0e87c3cfb3ef17c5321c3fb2
HammingLift.lean              552c9a6382c7eef5b529926f289c31f076f16b63b49bfe4535873cf32f20ae73
```

The `.lake` directory and all generated build products are excluded from the
published source.

## Theorem and scope audit

Lean constructs the residue-slab coloring and proves its surjectivity, fiber
size, abstract line containment, exact number of colors, exact scheme deficit,
and optimal quotient count under the reviewed remainder condition. It then
identifies the appended line graph with Mathlib's Cartesian graph product and
proves the concrete lifted same-color-neighbor bound
`(|I|-1)+(s-1)` on `completeGraph I □ (G □ completeGraph (Fin p))`.

The base clique-fiber coloring remains an explicit hypothesis. The cyclic
rectangle constructor, separate shell upper bound, and explicit parameter
family are not encoded.
