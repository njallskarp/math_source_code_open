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

`AlbertsonPairMoments.lean` supplies the finite-graph structural layer needed
after the recurrence leaves the two order-55 rows:

- `card_edges_delete_two_add_degrees` proves the generic two-vertex deletion
  identity directly for Mathlib `SimpleGraph` edge finsets;
- `card_edges_delete_two_eq_sub_pairDefect` rewrites that identity in the
  complement-defect coordinates
  `D(u,v)=x(u)+x(v)+1[uv in E(H)]`, with complementarity required only on the
  selected pair;
- `unorderedPairTotal_pairDefect` and
  `unorderedPairTotal_pairDefect_sq` prove the parameterized first and second
  moments when `degree_H(v)+x(v)=d`;
- the four `r28_m768_*` and `r28_m769_*` specializations recover exactly
  `3471`, `51*S2+6072`, `3578`, and `51*S2+6387`.

The moment proofs use the ordered off-diagonal finset and divide its symmetric
sum by two. They are not profile enumeration and do not import factor
criticality, Hall's theorem, critical coloring, or drawing topology.

`AlbertsonConformalSeparator.lean` supplies the next matching-theoretic bridge
using Mathlib's native `SimpleGraph.Subgraph.IsMatching` representation:

- `matching_deletePairOfAdj` proves that deleting the endpoints of an edge of a
  matching leaves a matching;
- `matchingOffThree_of_matchingOffOne_of_adj` turns a near-perfect matching off
  `a`, containing the edge `w-d`, into a perfect matching off `a,w,d`;
- `conformalTriangle_of_singleton_triangle_separator` proves, over an arbitrary
  vertex type, that a factor-critical graph with a triangle separator leaving
  a singleton vertex contains a conformal triangle;
- `no_singleton_triangle_separator` is the contrapositive interface used in
  the Albertson complement analysis.

Factor-criticality, conformal triangles, and the separator condition are
defined by small predicates over `SimpleGraph` adjacency and matching
subgraphs. No finite enumeration, coloring representation, Tutte theorem,
crossing-number topology, or custom matching data structure is imported.

`AlbertsonUniformRows.lean` isolates the Hall-theoretic common-support bridge
requested by the independent reviews at Discovery Net heights 1821 and 1865:

- `HasTransversalOn N S` is a system of distinct representatives for the
  finite rows `N i`, `i in S`;
- `hasTransversalOn_of_card_eq_succ_of_ne` proves that `d+1` many
  `d`-element rows containing two unequal rows admit a transversal;
- `all_rows_eq_of_uniform_card_of_no_succ_transversal` proves, over arbitrary
  finite index and value types, that if `L` has at least `d+1` indices, every
  row on `L` has size `d`, and no `d+1` rows admit a transversal, then all rows
  on `L` are equal.

The proof applies Mathlib's finite-set Hall theorem. It formalizes exactly the
uniform-row consequence used in the common-support branches of the reviewed
two-clique arguments, but deliberately does not formalize their coloring,
contraction, conformal-triangle, or topological-clique cases.

`SparseAffineSupport` records the slope, intercept, denominator, and two active
integer endpoints of a rational supporting line. `certificate.json` is a compact
machine-readable instance of this schema. It records active supports for the
order-50, order-54, and order-55 tables, identifies the support used at every
sampling or deletion step, and retains the reviewed order-53 table hash as a
checkpoint.

The checked direct-sampling specializations are:

| input | sample | exact lower bound | ceiling |
| --- | ---: | ---: | ---: |
| `(n,m)=(54,726)` | 24 | `10759164/1771` | 6076 |
| `(n,m)=(53,714)` | 50 | `14046318/2303` | 6100 |
| `(n,m)=(53,715)` | 50 | `56455997/9212` | 6129 |
| `(n,m)=(55,768)` | 24 | `12374440/1771` | 6988 |
| `(n,m)=(56,781)` | 25 | `810423/115` | 7048 |

The exact convex deletion recurrence then gives:

| target | source support | exact lower bound | ceiling |
| --- | --- | ---: | ---: |
| `(n,m)=(55,768)` | order 54, endpoints 740/743 | `1080124/153` | 7060 |
| `(n,m)=(56,781)` | order 55, endpoints 752/754 | `369973/52` | 7115 |

The comparison value is `Z(28)=7098`. Thus the order-56 diagnostic clears the
comparison by 17, while the order-55 minimum-edge diagnostic remains 38 short.
The exact table first reaches 7098 at 770 edges for order 55: the values at
768, 769, and 770 edges are respectively 7060, 7092, and 7123.

These are conditional `r=28` mechanism diagnostics, not a claim that
Albertson's conjecture is proved for `r=28`. The edge inputs 768 and 781 are the
exact ceilings of the externally supplied critical-graph inequality
`2m >= (r-1)n + (2r-6)` at orders 55 and 56. The Lean file verifies this
arithmetic provenance, the two instantiated recurrence implications, and the
comparison arithmetic. It does not prove that graph-theoretic inequality or
construct the required drawings.

## Reproduction

Requirements: Git, Python 3.9 or later, and `elan`/Lean. The project pins Lean
and Mathlib to `v4.33.1`.

```sh
lake update
lake build
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

The build should end with `Build completed successfully`. The checker should
begin with `PASS sparse affine sampling certificate` and report:

```text
recursive_table_sha256=ee056ada7011df41bce287e59ba3c08100c73f988a4e23e444397818e8a5a70f
recursive_table_order53_sha256=55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43
checked_results_sha256=45727a04da0097d116299d12b199a3e17c11ddca1780e122100ce277118796bd
```

## Literature and graph alignment

- Discovery Net height 1761 states the integer-aware induced-sampling step and
  the order-54 value 6076.
- Height 1773 supplies an earlier fixed-row Lean formalization; the present
  theorem is parameterized in `n`, `s`, the affine coefficients, and all finite
  support data.
- Height 1813 supplies the reviewed convex-sampling recurrence and reference
  order-53 table hash reproduced by `verify.py`.
- Height 2503 is the parameterized sampling/deletion formalization extended by
  the present concrete recurrence instances.
- Height 2523 reduces the `r=28` frontier to `(55,768)` and `(55,769)` and
  states the pair-deletion and defect-moment identities. The present
  `SimpleGraph` module independently kernel-checks exactly those structural
  identities; its graph-theoretic hypotheses remain explicit.
- Height 1777 records the coloring observation that a conformal triangle in an
  order-`2r-1` critical complement would produce an `(r-1)`-coloring. The
  formalization does not import that coloring argument; absence of conformal
  triangles is an explicit hypothesis.
- Height 2583 states the unconditional singleton-triangle separator lemma and
  then uses additional finite component certificates to compress the two
  surviving `r=28` rows. `AlbertsonConformalSeparator.lean` formalizes only the
  unconditional matching lemma. The profile compression, component
  classification, and deletion-table calculations remain outside Lean.
- Height 1815 uses the uniform-row consequence to close the final `h=8`
  two-clique profile, and height 1821 independently verifies that use and asks
  for a parametric statement. Height 1849 reuses the same consequence in a
  broader two-clique dichotomy, independently accepted at height 1865. The
  new Hall module formalizes only this common-support kernel, not either full
  coloring-or-subdivision dichotomy.
- Büngener and Kaufmann, [*Improving the Crossing Lemma by Characterizing
  Dense 2-Planar and 3-Planar Graphs*](https://arxiv.org/abs/2409.01733), state
  the uniform affine crossing estimates used as checker inputs.
- Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682), states the critical-edge inequality
  used only to identify the two `r=28` diagnostic inputs.

## Trust boundary

Lean kernel-checks the support-counting identities, exact floor/ceiling
arithmetic, the parameterized sampling implication, and the abstract deletion
recurrence. It also checks finite-graph two-vertex deletion and both generic
defect moments over arbitrary finite vertex types. The only reported axioms are
Mathlib's standard `propext`, `Classical.choice`, and `Quot.sound`. Lean
additionally checks the two concrete
conditional recurrence bounds, `Z(28)=7098`, the 38-crossing residual gap at
order 55, the 17-crossing surplus at order 56, and all four exact order-55
moment formulas.

External hypotheses remain explicit: a drawing must supply crossing identifiers
with four distinct supported vertices; induced drawings must obey the local
crossing lower bound; the integer table `F` must actually lower-bound those
induced drawings; and each sparse support must be a valid minorant with the
claimed active endpoints. `verify.py` checks the published affine inputs, the
recursive table through order 56, every sparse support globally and at its
active endpoints, every displayed rational value, and both threshold windows.
It is ordinary exact Python rather than a proof-assistant kernel. Neither the
topology-to-support translation nor the cited published graph inequalities are
formalized here. For the pair-moment module, the assertions that a candidate
has 55 vertices, that its complement has 717 or 716 edges, that the excess sum
is 51 or 53, and that `degree_H(v)+x(v)=27` are explicit hypotheses. Connected
complement, Stehlík's theorem, factor-criticality, and matching/Hall constraints
are not formalized.

For the conformal-separator module, Lean kernel-checks the restriction of a
matching after deleting a matched edge and the deduction of a conformal
triangle from factor-criticality plus the singleton-separator condition. It
does not prove that the complement of a critical graph is factor-critical, or
that critical coloring excludes conformal triangles; those are explicit
predicate hypotheses. It also does not formalize the height-2583 finite
component classification or its subsequent profile counts.

For the uniform-row module, Lean kernel-checks the finite-family implication
from equal row cardinalities and the absence of a `d+1`-row system of distinct
representatives to equality of every row. The only reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`, inherited from Mathlib's Hall
theorem and finite-set infrastructure. Translating `HasTransversalOn` into a
matching in a particular complement-incidence graph is intentionally external,
as are all Albertson normal-form, coloring, contraction, subdivision, and
drawing-topology arguments.
