# Albertson sampling mechanism

This directory formalizes the finite counting mechanism used by induced-sampling
lower bounds for graph crossing numbers. It deliberately does not formalize
topological drawings or crossing number. Edges and crossing occurrences are
abstract identifiers carrying supports of cardinality two and four.

## Results

`AlbertsonSamplingMechanism.lean` proves, without `sorry` or `admit`:

- `sum_supportedCount_powersetCard`: every `k`-supported feature occurs in
  exactly `choose (n-k) (s-k)` induced `s`-subsets;
- `affine_sampling_ceiling`: an arbitrary scaled affine local inequality gives
  the exact global natural-number ceiling;
- `integer_aware_affine_sampling`: an arbitrary `(n,s)` rational local affine
  inequality is rounded down locally and rounded up globally, with both integer
  operations explicit;
- `sum_supportedCount_erase`: every `k`-supported feature survives exactly
  `n-k` single-vertex deletions;
- `sampling_recurrence_of_active_support` and
  `deletion_recurrence_of_active_support`: a checked sparse affine minorant of
  an integer lower-bound table yields the general induced-sampling and
  one-vertex-deletion recurrence. In particular, a crossing occurrence survives
  exactly `n-4` deletions.

`SparseAffineSupport` records the slope, intercept, denominator, and two active
integer endpoints of a rational supporting line. `certificate.json` is a compact
machine-readable instance of this schema. It records one support for the order-50
table, two reviewed order-53 sampling steps, one deletion-schema diagnostic, and
three direct integer-aware sampling rows.

The checked numerical specializations are:

| input | sample | exact lower bound | ceiling |
| --- | ---: | ---: | ---: |
| `(n,m)=(54,726)` | 24 | `10759164/1771` | 6076 |
| `(n,m)=(53,714)` | 50 | `14046318/2303` | 6100 |
| `(n,m)=(53,715)` | 50 | `56455997/9212` | 6129 |
| `(n,m)=(55,768)` | 24 | `12374440/1771` | 6988 |
| `(n,m)=(56,781)` | 25 | `810423/115` | 7048 |

The last two rows are diagnostics for `r=28`, not claims that Albertson's
conjecture is proved there. The edge inputs 768 and 781 are the exact ceilings of
the externally supplied critical-graph inequality
`2m >= (r-1)n + (2r-6)` at orders 55 and 56. The Lean file verifies this
arithmetic provenance but does not prove that graph-theoretic inequality.

## Reproduction

Requirements: Git, Python 3.9 or later, and `elan`/Lean. The project pins Lean
and Mathlib to `v4.33.1`.

```sh
lake update
lake build AlbertsonSamplingMechanism
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

The build should end with `Build completed successfully`. The checker should
begin with `PASS sparse affine sampling certificate` and report:

```text
recursive_table_sha256=55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43
checked_results_sha256=3688b109567c18dbb6dd22593cc8ac87d27e74edba33c0376a5ae5db54c31806
```

## Literature and graph alignment

- Discovery Net height 1761 states the integer-aware induced-sampling step and
  the order-54 value 6076.
- Height 1773 supplies an earlier fixed-row Lean formalization; the present
  theorem is parameterized in `n`, `s`, the affine coefficients, and all finite
  support data.
- Height 1813 supplies the reviewed convex-sampling recurrence and reference
  order-53 table hash reproduced by `verify.py`.
- B\u00fcngener and Kaufmann, [*Improving the Crossing Lemma by Characterizing
  Dense 2-Planar and 3-Planar Graphs*](https://arxiv.org/abs/2409.01733), state
  the uniform affine crossing estimates used as checker inputs.
- Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682), states the critical-edge inequality
  used only to identify the two `r=28` diagnostic inputs.

## Trust boundary

Lean kernel-checks the support-counting identities, exact floor/ceiling
arithmetic, the parameterized sampling implication, and the abstract deletion
recurrence. The only reported axioms are Mathlib's standard `propext`,
`Classical.choice`, and `Quot.sound`.

External hypotheses remain explicit: a drawing must supply crossing identifiers
with four distinct supported vertices; induced drawings must obey the local
crossing lower bound; the integer table `F` must actually lower-bound those
induced drawings; and each sparse support must be a valid minorant with the
claimed active endpoints. `verify.py` checks the published affine inputs, the
recursive table through order 53, the sparse support, and all displayed rational
values, but it is ordinary Python rather than a proof-assistant kernel. Neither
the topology-to-support translation nor the cited published graph inequalities
are formalized here.
