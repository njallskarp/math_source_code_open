# Symbolic one-vertex extension obstructions for \(R(5,5)\)

This directory develops exact algebraic certificates for extending a
Ramsey\((5,5,42)\) coloring by one vertex.  The first result identifies the
precise Sherali--Adams degree at which the signed \(K_4\) extension clauses
become visible.

## Reproduce

```bash
python3 derive_sa_visibility.py
python3 verify_sa_visibility.py
python3 test_sa_visibility.py
```

Both implementations use `fractions.Fraction`; no graph enumeration,
floating-point solver, or external package is involved.  The derivation uses
multilinear polynomial arithmetic.  The verifier instead uses conditional
expectations and a 16-row truth table.

The checked output is recorded in `sa-visibility-certificate.json`.
