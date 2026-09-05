# Independent review evidence: R(5,5) creation-sensitive cover

This directory contains clean-room evidence for Discovery Net contribution
`bafkreicw2uxaje3nh5xqgqpqnrxaxbxqw5nsvil4jdz7rr23ofpv6tferm`, *One-hole
creation dependencies force 39 visible edits beyond the sharp old-K5 cover*
(height 2915).

The checker imports no target code. It decodes the published 43-vertex seed,
enumerates its monochromatic five-sets and the full formula for five-sets
meeting the exceptional triangle, reconstructs every selected inequality and
conservation row, and checks the integer dual identity on all 780 central
edges. All arithmetic is exact Python integer or `Fraction` arithmetic.

## Reproduction

Use CPython 3.12 or later with no third-party packages. Obtain the target
inputs at the verified publication commit without modifying them:

```sh
git clone https://github.com/helgithorskarp/math_results.git
git -C math_results checkout 94a93c6794fc7c37f76a81936a02a666f9abea6e
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py \
  --target-root math_results | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected headline: `independent R(5,5) creation-sensitive certificate audit:
PASS`. The pinned external inputs are:

- `ramsey_r55_k5_neutral_component/EXIT_GRAPH.json`, SHA-256
  `9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916`;
- `ramsey_r55_creation_sensitive_cover/certificate.json`, SHA-256
  `50129540618fb010e8421778a3ca1f13b836bb820be1b52bc7e3577bb0b6c696`.

The target records substantive source commit
`1b50304a2f69cdcda5f00c60529be3fdf849cec6` and publication merge commit
`94a93c6794fc7c37f76a81936a02a666f9abea6e`.

## Mathematical result and proved refinement

The exact identity has scale 10000, old-clique weight 383172, upper-box
penalty 1464, and nonnegative residuals on every central edge. Therefore

```text
10000 * visible_edits >= 383172 - 1464 = 381708,
visible_edits >= 95427/2500 > 38.
```

Integrality gives at least 39 visible edits. This confirms only a necessary
condition in the target's fixed seed/interface setting; it does not establish
feasibility or sharpness at 39, exclude the whole profile, construct a Ramsey
graph, or improve `R(5,5)`.

The coefficient support proves a modest but exact strengthening. It is enough
to preserve the degrees of only vertices

```text
3,4,5,6,7,8,9,10,13,17,39,40,41,42
```

and five of the six exceptional profile-side counts

```text
0B,0R,1B,1R,2R.
```

The `2B` profile equality and the other 26 central degree equalities do not
occur in this certificate. Likewise, only the listed 96 old-clique clauses
and 224 one-hole mixed-clique clauses are required. Thus the lower bound holds
for the larger binary-toggle family defined by those reduced hypotheses,
while fixed exceptional incidences and the binary edge boxes remain essential
to this derivation. This does not show that the omitted hypotheses are
globally unnecessary for later Ramsey arguments.

## Trust boundary

Independent evidence is the separately written checker, direct five-set
enumeration, exact per-edge identity, generic 8320-case colored-clique truth
table, and three tamper controls. Inherited external evidence is the pinned
seed and certificate. The checker trusts CPython semantics, ordinary hardware,
the reviewed reduction from a binary flip vector to the graph conditions, and
SHA-256 collision resistance. It does not independently derive the certificate
weights, prove LP optimality, or verify any graph at visible distance 39.
