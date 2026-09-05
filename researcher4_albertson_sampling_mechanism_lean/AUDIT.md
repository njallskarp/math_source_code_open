# Verification audit

Audit date: 2026-09-04.

## Versions

- Lean toolchain: `leanprover/lean4:v4.33.1`
- Mathlib requirement: tag `v4.33.1`
- Exact dependency revisions: recorded in `lake-manifest.json`
- Checker runtime used for this audit: CPython 3.12.12
- Exact checker: Python standard library only (`fractions.Fraction`, integer
  arithmetic, and `math.comb`)

## Lean build

Command:

```sh
lake build AlbertsonSamplingMechanism
```

Observed result: `Build completed successfully (971 jobs).`

The source contains no `sorry`, `admit`, declaration of a new axiom, or unsafe
declaration. Explicit `#print axioms` commands cover the generic counting,
sampling, rounding, sparse-support, deletion, and numerical theorems. Their
output contains only `propext`, `Classical.choice`, and `Quot.sound` (some
arithmetic lemmas use only a subset).

## Independent certificate check

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

Observed compact output:

```text
PASS sparse affine sampling certificate
recursive_table_sha256=ee056ada7011df41bce287e59ba3c08100c73f988a4e23e444397818e8a5a70f
recursive_table_order53_sha256=55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43
reviewed_order53_m714: bound=14046318/2303; ceiling=6100
reviewed_order53_m715: bound=56455997/9212; ceiling=6129
one_vertex_deletion_schema_test: bound=246382/47; ceiling=5243
r28_order55_m768_recursive: bound=1080124/153; ceiling=7060
r28_order56_m781_recursive: bound=369973/52; ceiling=7115
reviewed_order54_m726: bound=10759164/1771; ceiling=6076
r28_order55_m768_diagnostic: bound=12374440/1771; ceiling=6988
r28_order56_m781_diagnostic: bound=810423/115; ceiling=7048
r28_order55_threshold: first_edges=770; value=7123
r28_order56_threshold: first_edges=781; value=7115
checked_results_sha256=45727a04da0097d116299d12b199a3e17c11ddca1780e122100ce277118796bd
```

The checker rebuilds the integer lower-bound tables through order 56 from the
five uniform lines (including zero), computes exact lower convex hulls, verifies
both the new full hash and reviewed order-53 checkpoint, and checks the active
supports against every entry of the order-50, order-54, and order-55 tables and
at both endpoints. It checks every mean, rational bound, ceiling, gain, and
comparison result. It also exhausts all sample sizes for each direct diagnostic,
verifies the exact first edge count reaching 7098 at orders 55 and 56, and runs
small definition-level tests of ceiling and lower-hull interpolation.

## Statement alignment

The Lean result is conditional by design. It proves the finite implication from
local inequalities and two-/four-vertex supports to a global crossing-count
bound. It does not equate the abstract crossing identifiers with geometric
crossings in an optimal drawing. It also does not formalize the external
uniform crossing inequalities, the critical-edge inequality, or the claim that
the recursively generated table is a graph crossing-number lower-bound table.
Those inputs are represented by theorem hypotheses and independently checked
certificate data. The concrete Lean theorems
`r28_order55_recursive_bound` and `r28_order56_recursive_bound` instantiate the
generic deletion recurrence while retaining certificate validity and every
local table bound as explicit hypotheses. Lean proves that the second value
7115 exceeds `Z(28)=7098`, but does not internalize the Python proof that the
selected supports are valid minorants. Thus the formalization closes the finite
implication and arithmetic comparison without claiming a topological graph
theory formalization or a complete `r=28` theorem.
