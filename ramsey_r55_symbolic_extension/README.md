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

## A 74-clause subset-minimal extension obstruction

`signed-k4-mus.json` isolates 74 of the 2,313 signed \(K_4\) clauses for
authoritative order-42 graph 0.  The core contains 37 red and 37 blue clauses,
uses all 42 variables, and is subset-minimal unsatisfiable.  Its certificate
contains a 41-addition DRUP refutation and 74 distinct single-clause-deletion
witnesses.

Download the authoritative input, generate the certificate with the pinned
solver version, and check it without solver dependencies:

```bash
curl -fsS https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6 -o r55_42some.g6
python3 -m pip install -r requirements-mus-generation.txt
python3 generate_signed_k4_mus.py r55_42some.g6 > regenerated.json
python3 verify_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
python3 test_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
```

The verifier reconstructs the graph and all signed \(K_4\) clauses directly,
checks every DRUP addition by unit propagation, and checks every deletion
witness against the retained clauses.
