# Formalization audit

## Exact interface

`ClusterFeasible a b c d e f` requires all six natural numbers to be positive
and encodes, in order, the six strict inequalities printed in Bai--Li--Park,
Remark 3.1.  There are no hidden hypotheses.

The audited declarations are:

```lean
cluster_component_lower_bounds
cluster_total_ge_36
cluster_total_eq_36_unique
published_cluster_tuple_feasible
cluster_total_eq_36_iff
```

Together they prove the lower bound 36, the unique equality tuple, and direct
feasibility of that tuple.  The proof layer is Presburger arithmetic over
`Nat`, discharged by Lean's `omega` tactic.

## What is and is not formalized

Formalized:

- the exact positive-integral inequality system;
- lower bounds `b,d,f >= 3`, `a >= 7`, `c >= 11`, and `e+f >= 12`;
- total cluster size at least 36;
- feasibility of `(7,3,11,3,9,3)`; and
- uniqueness of that tuple at total 36.

Not formalized:

- the tournament blow-up represented by the variables;
- the implication from the inequalities to absence of a strong Seymour
  vertex;
- the order-at-most-14 result or any SAT encoding/certificate; or
- an exclusion of arbitrary counterexamples of orders 15 through 35.

This is therefore a formalization of the exact integer optimization bridge,
not an end-to-end formalization of a tournament theorem.

## Verification record

With Lean 4.33.1 and Mathlib v4.33.1 pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`:

```text
lake clean                         success
lake exe cache get                 8,690 artifacts available
lake build                         3 jobs completed successfully
lake env lean StrongSeymourCluster.lean
                                   success
```

The five audited declarations report only Lean's standard axioms:

```text
cluster_total_ge_36:
  propext, Quot.sound
other four declarations:
  propext, Classical.choice, Quot.sound
```

The source scan found none of `sorry`, `admit`, a custom `axiom`, `unsafe`, or
`native_decide`.  There is no external executable or data boundary.

```text
28e67ea73500dee2a397efe9bfd6048f282684326ef539d3de6f9f7362598758
```

is the SHA-256 of `StrongSeymourCluster.lean`.
