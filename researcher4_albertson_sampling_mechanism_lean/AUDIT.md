# Verification audit

Audit date: 2026-09-04.

## Versions

- Lean toolchain: `leanprover/lean4:v4.33.1`
- Mathlib requirement: tag `v4.33.1`
- Exact dependency revisions: recorded in `lake-manifest.json`
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
recursive_table_sha256=55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43
reviewed_order53_m714: bound=14046318/2303; ceiling=6100
reviewed_order53_m715: bound=56455997/9212; ceiling=6129
one_vertex_deletion_schema_test: bound=246382/47; ceiling=5243
reviewed_order54_m726: bound=10759164/1771; ceiling=6076
r28_order55_m768_diagnostic: bound=12374440/1771; ceiling=6988
r28_order56_m781_diagnostic: bound=810423/115; ceiling=7048
checked_results_sha256=3688b109567c18dbb6dd22593cc8ac87d27e74edba33c0376a5ae5db54c31806
```

The checker rebuilds the integer lower-bound tables through order 53 from the
five uniform lines (including zero), computes exact lower convex hulls, verifies
the reviewed table hash, checks the support against every order-50 table entry
and at both active endpoints, and checks every mean, rational bound, and ceiling.
It also exhausts all sample sizes for each `r=28` direct diagnostic and confirms
the recorded sample size maximizes the exact rational bound.

## Statement alignment

The Lean result is conditional by design. It proves the finite implication from
local inequalities and two-/four-vertex supports to a global crossing-count
bound. It does not equate the abstract crossing identifiers with geometric
crossings in an optimal drawing. It also does not formalize the external
uniform crossing inequalities, the critical-edge inequality, or the claim that
the recursively generated table is a graph crossing-number lower-bound table.
Those inputs are represented by theorem hypotheses and independently checked
certificate data. Thus the formalization closes the combinatorial and integer
rounding bridge without claiming a topological graph theory formalization.
