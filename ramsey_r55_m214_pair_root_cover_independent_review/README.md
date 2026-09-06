# Independent review evidence for the complete (M=214) pair-root interface

This directory contains the independently written checker used for the
review of the inseparable Discovery Net interface cluster at heights 3062,
3130, 3148, 3160, and 3170.  The primary target is the height-3148 theorem
that 389 marked pair-incidence roots cover all five intrinsic (M=214)
families; the upstream pair-selection arguments and the downstream integrated
OPB are checked because they are load-bearing parts of that equivalence.

The verdict supported here is deliberately narrow: **the intrinsic branch,
the 389-root union, and the generated selector-gated OPB have the claimed
pointwise equivalence, conditional on the stated inherited premises.**  No
root is solved, no model is constructed, no UNSAT proof is supplied, and no
new bound on (R(5,5)) follows from this review.

## Independent checks

`independent_review.py` is standard-library Python and imports no researcher
module.  It checks:

- the two-unit excess classification and all five reanchoring cases;
- the pre-upgrade partner bounds (9,9,9,9,8);
- all (2^{15}) labeled graphs on six vertices relevant to the defect lemma,
  and all 232 graphs on seven vertices having at most two edges;
- the seven signed triangle coefficients and the strict integer margin
  [
  D\geq1569>8\cdot196=1568;
  ]
- the SHA-256, level census, order, edge counts, (K_4)-freeness, and
  independence-number condition for all 70 order-14 records at levels
  (22,23,58,59,60) in the live public `r45extreme` archive;
- the 389 roots by an independent four-bin-composition enumeration, including
  every descriptor digest, all 83 anchor units, all 43 (E)-incidence
  equalities, and every partition condition;
- one independent physical 903-edge transport and residual-signature sort for
  every root; these 389 synthetic graphs test equivariance only and are not
  Ramsey graphs;
- every one of the 2,044,421 OPB constraints, reconstructed without importing
  the generator: 962,598 five-sets in both colors, 12,341 four-row triangle
  conjunctions, 129 physical star rows, the one-hot row, and all 69,731
  guarded root rows; and
- that every inactive guard is a Boolean tautology and every active guard is
  exactly its independently reconstructed physical root condition.

The reviewed source identities are pinned by file hashes in the checker.  The
corresponding source commits are:

- five-family cover: `11df9442ceb2f31de190dbc0e6fc840d33399e39`;
- all-family codegree-nine theorem: `f395891991246b75a42ba741f25dbd79da65bfb7`;
- 389-root normalization: `9a9d4c3234d3fbe196ff4b413df831c587bd7653`;
- integrated OPB: `2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b`; and
- prior semantic reproduction: `7703376cdca2326dc06993acc5ad976823125f09`.

## Reproduction

From a checkout of `math_source_code_open` containing the pinned files:

```bash
set -o pipefail
curl -fL https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz \
  -o /tmp/r45extreme-review.tar.gz
python3 -B ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output /tmp/r55-m214-pair-roots.opb
python3 -B \
  ramsey_r55_m214_pair_root_cover_independent_review/independent_review.py \
  --source . \
  --formula /tmp/r55-m214-pair-roots.opb \
  --catalog /tmp/r45extreme-review.tar.gz \
  | cmp - \
  ramsey_r55_m214_pair_root_cover_independent_review/EXPECTED_RESULT.json
python3 -B -O \
  ramsey_r55_m214_pair_root_cover_independent_review/independent_review.py \
  --source . \
  --formula /tmp/r55-m214-pair-roots.opb \
  --catalog /tmp/r45extreme-review.tar.gz \
  | cmp - \
  ramsey_r55_m214_pair_root_cover_independent_review/EXPECTED_RESULT.json
shasum -a 256 -c \
  ramsey_r55_m214_pair_root_cover_independent_review/SHA256SUMS
```

The generated OPB is 172,788,992 bytes with SHA-256
`469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f`.
It is operational state and is intentionally not committed here.  A normal
run took about 20 seconds with CPython 3.12 on the review host.

## What was checked and what remains imported

The displayed incidence arithmetic, finite lemmas, pair-cell enumeration,
physical relabeling, root descriptors, guard semantics, and complete OPB byte
stream were checked independently.  Native researcher checkers were also
replayed separately, including the full C++ row checker, but their success is
not substituted for the independent checks above.

Imported premises are the already established intrinsic (M=214) branch
derivation, the classical value (R(3,5)=14), and Brendan McKay's public
statement that the relevant extreme (R(4,5))-graph levels form complete
sets.  The archive verification confirms the data actually downloaded; it
does not independently reprove that catalogue's completeness.  Also trusted
are CPython's exact integer semantics, SHA-256, ordinary hardware, and the
unformalized theorem-to-encoding argument.

There is no solver trust boundary because no solver verdict is used.  The
remaining mathematical gap is terminal: produce and independently check a
full model, or produce and replay a standard UNSAT proof for this exact
formula.  This evidence alone proves neither outcome.
