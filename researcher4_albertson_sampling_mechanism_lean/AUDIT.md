# Verification audit

Audit date: 2026-09-05.

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
lake build
```

Observed result after adding the threshold-inversion module:
`Build completed successfully (1507 jobs).`

The source contains no `sorry`, `admit`, declaration of a new axiom, or unsafe
declaration. Explicit `#print axioms` commands cover the generic counting,
sampling, rounding, sparse-support, deletion, and numerical theorems. Their
output contains only `propext`, `Classical.choice`, and `Quot.sound` (some
arithmetic lemmas use only a subset).

The axiom audit now also covers the generic `SimpleGraph` two-vertex deletion
identity, its complement-defect rewrite, both parameterized defect moments, and
all four exact order-55 moment specializations. These theorems report the same
three standard Mathlib axioms and no others.

The deletion-threshold audit covers the parameterized theorem
`deletionEdgeThreshold_le_iff` and its order-55/order-56 diagnostic
specializations. The theorem characterizes the exact least edge count at which
an affine deletion ceiling reaches any positive target, despite the natural
subtraction in the numerator. All five printed declarations report only
`propext`, `Classical.choice`, and `Quot.sound`. A standalone compilation and
the full 1507-job project build both completed without warning. The source
SHA-256 is
`5dfd35d2f63f156eb5935dfb7c1f4c6879a210896d284e300ca7c3325914f104`.

The conformal-separator audit covers `matching_deletePairOfAdj`,
`matchingOffThree_of_matchingOffOne_of_adj`,
`IsFactorCritical.exists_adj`,
`conformalTriangle_of_singleton_triangle_separator`, and
`no_singleton_triangle_separator`. The first, second, fourth, and fifth report
only `propext`, `Classical.choice`, and `Quot.sound`; the neighbor-existence
lemma reports only `propext`.

The Hall/common-support audit covers
`hasTransversalOn_of_card_eq_succ_of_ne` and
`all_rows_eq_of_uniform_card_of_no_succ_transversal`, together with the new
at-least-degree kernel and its exact-cardinality conclusion. All four report
only `propext`, `Classical.choice`, and `Quot.sound`. A targeted build completed
successfully with 1010 jobs and no warning. The strengthened module SHA-256 is
`81b4f6c84937b36469dd49f856c8d14a8f0c2dc2fbcddd1561f0a1c04b9686e5`.

The two-contraction audit covers the concrete contracted-row membership and
cardinality lemmas, symmetric-difference containment, pair rigidity, and the
composed family theorem `all_rows_eq_of_two_contraction_obstructions`. Every
exported theorem reports only `propext`, `Classical.choice`, and `Quot.sound`.
The targeted build completed successfully with 1011 jobs and no warning. Its
source SHA-256 is
`daf032e3a920f9fa9014cfa8521361e27c0a5cd4b9500f5a4a9794514a90e648`.

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
It additionally exhausts a grid of small orders, slopes, intercepts, scales,
positive targets, and edge counts to check the exact iff proved by
`deletionEdgeThreshold_le_iff`; the affine thresholds 770 and 781 must equal
the independently scanned table thresholds.

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

`AlbertsonDeletionThreshold.lean` adds no graph or drawing assumption. It is a
pure arithmetic corollary of the already formalized affine recurrence formula:
under `n>4`, positive slope and scale, and positive target, its threshold is
both sufficient and necessary. The diagnostic values only identify where the
two supplied supports reach the external comparison value; validity and local
applicability of those supports retain the trust boundary above.

The separate graph module closes the elementary structural consequences stated
at Discovery Net height 2523. For a finite complement graph `H`, integer
weights `x`, and `degree_H(v)+x(v)=d`, Lean proves

```text
sum_{u<v} D(u,v) = (n-1) sum_v x(v) + |E(H)|
sum_{u<v} D(u,v)^2 = (n-4) sum_v x(v)^2
                         + (sum_v x(v))^2
                         + 2d sum_v x(v) + |E(H)|.
```

Here `sum_{u<v}` is implemented invariantly as half the ordered off-diagonal
sum; `D` is symmetric because simple-graph adjacency is symmetric. At
`n=55,d=27`, the supplied edge and excess totals reduce these formulas to the
four numbers in height 2523. The graph theorem does not prove those supplied
totals, connected-complement/factor-critical structure, Stehlík's coloring
theorem, or any matching/Hall constraint. Those are explicit external bridges.

`AlbertsonConformalSeparator.lean` uses the standard meaning of a
factor-critical graph as a matching saturating the complement of each deleted
vertex. A conformal triangle is encoded as three mutually adjacent vertices
whose complement is exactly the vertex set of a matching subgraph. The final
theorem assumes factor-criticality and absence of conformal triangles; it does
not derive either property from critical coloring. It proves only the
unconditional singleton-separator obstruction and makes no claim about the
height-2583 finite component certificate, the three/eight profile counts, or
crossing-number bounds.

`AlbertsonUniformRows.lean` formalizes the exact finite-family statement used
by the reviewed common-support step. The obstruction hypothesis says directly
that every `d+1`-element index subset lacks an injective choice into its rows;
it is not hidden behind an informal matching-number predicate. Lean checks
Hall's inequalities for every subfamily and now proves both the exact-size and
at-least-size versions.

`AlbertsonTwoContraction.lean` represents a contracted two-point colour class
by an `Option.none` tag and the remaining singleton classes by `Option.some`.
Lean proves the representation loses at most one compatible class, applies the
at-least-size Hall theorem to each deficient contraction, and proves that two
distinct contracted pairs force equality of the original equal-size rows. It
does not formalize the conversion from a specific complement graph into this
finite-family interface, the simultaneous matchings used for coloring, or the
final topological `K_r` routings.
