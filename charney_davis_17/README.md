# The frozen 17-vertex Charney--Davis proof package

This directory is the audit package for the following proof candidate.

> **Theorem.** If `Delta` is a finite flag generalized homology 5-sphere over
> a field and has 17 vertices, then `gamma_3(Delta) >= 0`.

The mathematical expansion of this project is frozen. The argument is not
being generalized or extended while it awaits qualified independent review.
The claim should be cited as an **independent-audit candidate**, not as an
independently accepted theorem.

Start with [`AUDIT.md`](AUDIT.md). It contains the complete short proof,
normalization conventions, exact statements of the external inputs, a
dependency table, the Lean trust boundary, and an adversarial bridge-by-bridge
check. [`REVIEW_REQUEST.md`](REVIEW_REQUEST.md) is the reviewer checklist.

## Package map

- `CharneyDavis17.lean`: h-polynomial recurrence and admissible-edge
  formalization. This is useful corroboration but is not needed by the
  shortest consolidated proof.
- `CharneyDavisPolarReduction.lean`: machine-checked polynomial extraction and
  integer squeeze used by the consolidated proof.
- `POLAR_REDUCTION.md`: historical derivation notes, retained for provenance;
  `AUDIT.md` supersedes it as the normative theorem statement.
- `audit_check.py`: dependency-free adversarial checks for the complement
  identity, the rigid integer profile, and the degree-four link arithmetic.
- `SHA256SUMS`: hashes for the source and audit files.

## Reproduction

Pinned versions:

```text
Lean 4.33.1
Lake 5.0.0-src+819816b
Mathlib v4.33.1
Python 3.11 or later (standard library only)
```

Run:

```bash
lake update
lake exe cache get
lake build
python3 audit_check.py
sha256sum -c SHA256SUMS
```

The Lean build prints the axiom audit. The source has no `sorry`, `admit`,
custom axiom, `unsafe` declaration, or `native_decide`.

## Primary sources

- Charney--Davis (1995):
  <https://msp.org/pjm/1995/171-1/pjm-v171-n1-p04-p.pdf>
- Davis--Okun, Theorem 11.2.1:
  <https://arxiv.org/abs/math/0102104>
- Gal, especially Definition 1.2.1, Corollary 2.2.2, and Corollary 2.2.3:
  <https://arxiv.org/abs/math/0501046>
- Labbé--Nevo, especially Lemmas 2.1--2.3, 3.2, 3.4 and Corollary 4.3:
  <https://arxiv.org/abs/1612.01169>
