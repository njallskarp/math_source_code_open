# Build and axiom audit

Audit date: 2026-09-04.

Pinned environment:

- Lean `v4.33.1`, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

The following clean build and standalone replay both exited zero:

```sh
lake update
lake exe cache get
lake clean
lake build MPLCOrder4
lake env lean MPLCOrder4.lean
```

The clean build ended with `Build completed successfully (997 jobs).`  The job
count is recorded as audit evidence, not promised as stable output.

All thirteen `#print axioms` reports contain only a subset of:

```text
propext
Classical.choice
Quot.sound
```

In particular, `certificate30_checks` uses only `propext`; the endpoint
`thirty_mem_orderFourSpectrum` uses `propext`, `Classical.choice`, and
`Quot.sound`.

A source scan found no `sorry`, `admit`, `native_decide`, `unsafe`
declaration, or project axiom.  The finite check is reduced by Lean's ordinary
kernel through `by decide`.

Lean source SHA-256:

```text
53402270d634f0f0c592fb7e9d87dc8cdf137a916335ca814e698e7a27cdfadd
```

The upstream Python verifier was independently replayed only as a provenance
cross-check.  It reports 30 selected words, minimum pairwise Hamming distance
2, all 256 universe words covered, coverage histogram
`{1:165, 2:61, 3:17, 4:13}`, and canonical selected-word SHA-256
`aaeef4b34fc12ef5fcebeac6f1b46c072ec6260dc57c254e18d3dfc3f6c7f073`.
That Python execution is not in the theorem's trust boundary because the same
finite obligations are checked from the embedded list in Lean.
