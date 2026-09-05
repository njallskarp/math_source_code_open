# Ramsey R(5,5): a degree-compatible width-two survivor

This package supplies an exact limitation witness in the order-43, `d=22`,
deficiency-six branch.  It satisfies the complete local constraints at two
anchors, has 452 red edges and degree profile `20^8 21^26 22^9`, and assigns
the 210 two-anchor diagonal edges so that all 413 distinct residual clauses of
width one or two hold.  Every remaining monochromatic `K5` uses at least three
diagonal edges.

This strengthens the unit-versus-binary limitation at Discovery Net height
2837.  It does not construct an `R(5,5;43)` graph and does not exclude the full
`d=22,t>=108` family.  It shows that an exclusion mechanism confined to
one-edge and two-edge diagonal clauses is insufficient, even when the same
assignment must realize the hard branch's degree and edge constraints.

## Exact replay

The primary checker uses only the Python standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 controls.py | diff -u EXPECTED_CONTROLS.txt -
shasum -a 256 -c SHA256SUMS
```

The independent checker uses NetworkX's graph6 decoder, complement operation,
and maximal-clique enumeration:

```sh
uv run --no-project --cache-dir /tmp/r55-width2-cache \
  --with networkx==3.6.1 --python python3 independent_check.py \
  | diff -u EXPECTED_INDEPENDENT.json -
```

## Optional discovery replay

`direct_search.py` encodes diagonal status directly as the XOR of partner
incidences.  For every mixed five-set it enumerates the partner-bit patterns
with exactly one or two diagonal edges and adds the corresponding conditional
no-`K5` clause.  The reference formula has 440 primary variables, 237,636 base
clauses and 68,608 additional conditional clauses.

```sh
uv run --no-project --cache-dir /tmp/r55-width2-cache \
  --with python-sat==1.9.dev15 --python python3 direct_search.py \
  --seconds 600 --solver glucose42
```

The solver is discovery-only.  The stored model's mathematical properties are
reconstructed from `WITNESS.json` without trusting the encoding or verdict.

## Compact invariants

- two-anchor cell sizes `(10,11,10,10)` and 210 diagonal edges;
- local profiles `(22,108,6)`, `(20,100,0)`, `(21,99,8)`, `(21,98,9)`;
- 413 distinct width-at-most-two clauses, all satisfied;
- minimum surviving monochromatic-`K5` width: three;
- defect profile: red `141,20,1` and blue `93,53,58` at widths `3,4,6`;
- red-edge SHA-256:
  `1910c00f11e247f45ccea2508784d01eb87f5ac3e7511b1ee134566a06e6df73`;
- residual-clause SHA-256:
  `99055acf33e8349550ac37701c30ef8f9360e183409ef213f31a04619683829c`.

## Trust boundary

The witness plus the elementary diagonal-clause reduction are the certificate.
The standard-library verifier exhaustively reconstructs every degree,
neighborhood, residual clause and monochromatic five-set.  The independent
checker uses a separate graph representation and clique enumeration.  Trusted
are the short source, CPython/NetworkX semantics, ordinary hardware, and
SHA-256 collision resistance.  Python-sat, its cardinality encoding and its
SAT verdict are outside the proof boundary.  The embedded cores are checked
directly for every property used; their catalog provenance additionally trusts
McKay's primary Ramsey graph data.

