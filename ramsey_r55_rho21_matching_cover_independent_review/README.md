# Independent audit of the rho=21 bichromatic matching-cover normal form

This directory independently audits the four explicit survivor witnesses in
`ramsey_r55_symbolic_extension/rho21-bichromatic-matching-cover-certificate.json`.
The checker was written separately and does not import or execute the producer's
Python verifier.

Run with Python 3.11 or later from the repository root:

```sh
python3 ramsey_r55_rho21_matching_cover_independent_review/verify_independent.py \
  ramsey_r55_symbolic_extension/rho21-global-blue-k5-kernel-certificate.json \
  ramsey_r55_symbolic_extension/rho21-bichromatic-matching-cover-certificate.json
```

The audit reconstructs all 23 selected blue clauses from each multigraph,
checks the two demand vectors, checks all 20 distinct four-edge matchings in
each witness, reconstructs the 21 red clauses, checks every cross-color
intersection and selected degree, and exhaustively searches the two
selected-support graphs for a forced monochromatic `K5`. It also counts every
four-edge matching in each blue kernel and records a canonical SHA-256 for each
joint support system.
Two deterministic mutations confirm that duplicate columns and nonmatching
columns are rejected.

The universal equivalence is elementary and is audited separately: a residual
red four-set meets each selected blue clause at most once exactly when its four
edge occurrences have disjoint endpoints in the blue-clause multigraph. The
marked triangle for the red clause through the pivot must additionally avoid
all side-clause nodes, since each side clause already meets it at the pivot.
Subtracting that triangle's incidences from the exceptional red-degree profile
gives exactly the two demand cases, according as the unique red-degree-three
vertex lies inside or outside the triangle. Conversely, every distinct-column
demand cover decodes without choice to the selected red clauses.

Trust boundary: this verifies the universal incidence argument and the four
supplied partial-support witnesses. It does not enumerate all kernels or covers,
complete unspecified core edges, prove that selected clauses are the complete
sets of monochromatic `K4`s, construct a Ramsey core, or certify singular-DP
ancestry.
