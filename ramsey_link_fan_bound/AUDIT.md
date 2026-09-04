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

`OneFlipWitness.lean` separately defines:

```lean
Violated value assignment support
SelectedUnsatisfiable reds blues
Monochromatic color value support
oneFlip color w z pivot
IsBlueWitness color w z B
blueDefectClauses color w blues
```

Here `color : V -> V -> Bool` and an assignment is simply `V -> Bool`.
`SelectedUnsatisfiable` says literally that every assignment violates a
selected all-true red support or all-false blue support.  No clause parser or
external satisfiability result is hidden in the definition.

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

The one-flip proof constructs the valuation that clones `color w` except at
`z`, proves no red support can be violated, and extracts a blue violated
support from `SelectedUnsatisfiable`.  The local no-extension hypotheses rule
out a blue support avoiding both `w` and `z`; hence the support is the required
one-edge-defect witness.  Mathlib's `Finset.card_le_card_of_injOn` then turns
witness incompatibility into the common-link cardinality bound.  Erasing `w`
from a unique red four-set gives the exact lower bound three.

## What remains external

The project deliberately stops before the surrounding Ramsey and SAT
representation layer.  In particular, it does not derive the finite-set
hypotheses from:

- a red/blue coloring of `K_42`;
- the HOL4 or published proof of `R(4,5)=25`;
- derivation of `SelectedUnsatisfiable` from a concrete signed extension
  subsystem;
- derivation of the two local no-extension hypotheses from clique-freeness;
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
lake build                         757 jobs completed successfully
lake env lean RamseyLinkFanBound.lean
                                   success
lake env lean OneFlipWitness.lean  success
```

All fifteen audited declarations report only Lean's standard axioms
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
685d9e3b6df9cd99e3d5f50799dfd9e1e17364f6aecd7710fafadbe735cb7705
```

are the SHA-256 values of `RamseyLinkFanBound.lean` and
`OneFlipWitness.lean`, respectively.
