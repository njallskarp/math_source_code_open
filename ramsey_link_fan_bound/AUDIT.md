# Formalization audit

## Exact interface

The main theorem is parameterized by arbitrary finite clause and vertex types.
The four relevant categories are represented by `Finset C`, while
`piece : C -> Finset V` records the target vertices covered by each extra
clause.  Its hypotheses are a literal finite-set transcription of the reviewed
count:

```text
|selected| = 44,  |red| >= 11,  |side| = m,  |witness| = 3;
red, side, witness, extra are pairwise disjoint;
their union is contained in selected;
|target| = rho - 3;
target is covered by the pieces of extra;
every piece has cardinality at most 4;
rho + blueDegree = 41;
rho <= 24 and blueDegree <= 24.
```

There are no hidden graph, coloring, or CNF assumptions.

## Proof architecture

`card_le_card_mul_of_biUnion_cover` uses Mathlib's
`Finset.card_biUnion_le_card_mul` to prove the generic finite cover-capacity
bound.  `covering_clauses_lower_bound` specializes it to capacity four and
ceiling form.  `card_four_pairwise_disjoint_le` obtains the exact sum of the
four category cardinalities by three applications of
`Finset.card_union_of_disjoint`.

The remaining declarations prove the complementary-degree interval, combine
the cover and disjoint-union bounds into

```text
m + ceil((rho - 3)/4) <= 30,
```

derive the reviewed subtraction form and three degree strata, and finally
prove `m <= 26`.

## What remains external

The project deliberately stops before the surrounding Ramsey and SAT
representation layer.  In particular, it does not derive the finite-set
hypotheses from:

- a red/blue coloring of `K_42`;
- the HOL4 or published proof of `R(4,5)=25`;
- an unsatisfiable signed extension subsystem;
- singular Davis--Putnam fan structure; or
- one-flip witness clauses.

Thus this is the exact reusable incidence/counting bridge, not an end-to-end
formalization of the Ramsey theorem or its obstruction search.

## Verification record

With Lean 4.33.1 and Mathlib v4.33.1 pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`:

```text
lake clean                         success
lake exe cache get                 8,690 artifacts available
lake build                         755 jobs completed successfully
lake env lean RamseyLinkFanBound.lean
                                   success
```

All eleven audited declarations report only Lean's standard axioms
`propext`, `Classical.choice`, and `Quot.sound`.  The following four require
only `propext` and `Quot.sound`:

```text
ceilDivFour_le_of_le_mul_four
ceilDivFour_sub_three
fan_arity_sub_bound
fan_arity_le_26
```

The source scan found none of `sorry`, `admit`, a custom `axiom`, `unsafe`, or
`native_decide`.  There is no external executable or data boundary.

```text
28bf3f73f26bcd02287f938e31f7f23001a39d05fe02809761e9745f8222a98b
```

is the SHA-256 of `RamseyLinkFanBound.lean`.
