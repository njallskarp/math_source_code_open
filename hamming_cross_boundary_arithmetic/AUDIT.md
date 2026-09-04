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
lake clean hamming_cross_boundary_arithmetic
lake build HammingCrossBoundaryArithmetic
lake env lean HammingCrossBoundaryArithmetic.lean
rg -n 'sorry|admit|native_decide|unsafe|axiom ' \
  HammingCrossBoundaryArithmetic.lean README.md AUDIT.md lakefile.toml \
  lean-toolchain lake-manifest.json
```

## Expected evidence

- clean build: success (`3007` jobs in the audited workspace);
- standalone Lean replay: exit status zero;
- fifteen `#print axioms` reports: only `propext`, `Classical.choice`, and
  `Quot.sound`, with several theorems using a strict subset;
- source scan: no theorem proof uses `sorry`, `admit`, `native_decide`, an
  `unsafe` declaration, or a project-defined axiom. Matches in this audit's
  description and scan command are documentary only.

The `.lake` directory and all generated build products are excluded from the
published source.

## Scope audit

Lean checks fifteen arithmetic theorems covering the corner incidence and
part count, the general layer quotient identity, the pair-remainder
specialization, and every displayed arithmetic specialization of the explicit
family. The cyclic cell cover, line containment, Hamming graph model, color
lift, majority condition, and upper-bound theorem are not encoded and remain
the explicit unformalized bridge.
