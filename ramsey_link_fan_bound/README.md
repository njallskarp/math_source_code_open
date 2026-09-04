# Ramsey-link fan and one-flip witness bridges in Lean

This pinned Lean project formalizes the finite cardinality bridge in the
reviewed `m <= 26` bound for a first singular `3+3` Davis--Putnam fan in a
hypothetical 44-clause signed-`K_4` Ramsey-extension obstruction.

## Main theorem

`ramsey_link_fan_arity_le_26` works with finite types of vertices and clauses.
It assumes four pairwise-disjoint clause categories inside a 44-clause
selection:

1. at least 11 selected clauses of the main color;
2. exactly `m` side clauses;
3. exactly three one-flip witness clauses; and
4. extra clauses covering `rho - 3` remaining link vertices, with each extra
   clause covering at most four of them.

It also assumes the two Ramsey-link upper bounds and complementary-degree
identity

```text
rho <= 24,  blueDegree <= 24,  rho + blueDegree = 41.
```

Lean then proves

```text
m <= 26.
```

The proof separately exports:

- a generic finite bi-union cover-capacity theorem;
- a four-way pairwise-disjoint cardinality theorem;
- the interval `17 <= rho <= 24`;
- the exact inequality
  `m + ceil((rho - 3)/4) <= 30` and its subtraction form; and
- the degree strata `m <= 26`, `m <= 25`, and `m <= 24` for the ranges
  `17..19`, `20..23`, and `24`.

The custom `ceilDivFour n = (n+3)/4` is the standard ceiling division by four;
Lean proves the cover lower bound from Mathlib's `Finset` bi-union theorem.

## One-flip common-link theorem

`OneFlipWitness.lean` adds the finite Boolean-support bridge that produces the
three witness clauses assumed above.  It defines pure red/blue clause
violation and the one-flip clone valuation directly, without a general CNF or
Davis--Putnam library.

`exists_blue_witness_of_common_red_link` proves that every common red-link
vertex `z` forces a selected blue support `B` such that

```text
z in B,  w notin B,  color(w,z) = red,
and color(w,v) = blue for every v in B \ {z}.
```

`card_common_red_link_le_blueDefectClauses` chooses these witnesses and proves
the choice injective, so the number of blue defect clauses is at least the
common-link size.  The exact specialization
`unique_red_four_clause_forces_three_blue_defects` shows that a unique selected
red four-set through `w` forces at least three selected blue defect clauses.

The proof assumes directly that every Boolean valuation violates a selected
support, that selected red supports are monochromatic, and the two local
no-monochromatic-extension consequences at `w`.  These are the exact finite
interfaces supplied by the surrounding Ramsey argument.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean RamseyLinkFanBound.lean
lake env lean OneFlipWitness.lean
```

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Expected results with the committed manifest:

- Mathlib cache: 8,690 artifacts;
- clean project build: 757 jobs completed successfully; and
- standalone replays: exit zero and fifteen printed axiom audits, each
  containing only `propext`, `Classical.choice`, and `Quot.sound` (four of the
  arithmetic declarations do not require `Classical.choice`).

Source SHA-256:

```text
28bf3f73f26bcd02287f938e31f7f23001a39d05fe02809761e9745f8222a98b  RamseyLinkFanBound.lean
685d9e3b6df9cd99e3d5f50799dfd9e1e17364f6aecd7710fafadbe735cb7705  OneFlipWitness.lean
```

## Theorem alignment and trust boundary

The formalized fan conclusion and degree-stratified inequality are the finite
counting step in Discovery Net lemma
`bafkreia7anjykjq3ky6fd4tjmhvkgtxbnwokx5oonkonvn55x6wmustgti`, accepted by
review `bafkreidm36n4leivfplrkfvcdgeb252urkhwd3qqggav3c66nsjparcbaa`.
The new Boolean-support module formalizes the common-link witness and
cardinality subtheorems of its dependency
`bafkreicmyw65o4vnwqwsvr36tf2skqr2a53nynioskfbuwtvtosaac4m4a`.

The bound `R(4,5)=25`, from which the two link-cardinality bounds arise, is the
theorem of [McKay--Radziszowski](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
and has separately been formalized in HOL4 by
[Gauthier--Brown](https://doi.org/10.4230/LIPIcs.ITP.2024.16).  This Lean
development does not import or reprove their formalization.

Lean does **not** formalize here:

- red/blue Ramsey colorings or the theorem `R(4,5)=25`;
- minimal unsatisfiability or Davis--Putnam reduction;
- the existence and shape of the first singular `3+3` fan;
- derivation of the finite unsatisfiability and local no-extension interfaces
  from a Ramsey graph; or
- the broader claim `R(5,5)=43`.

Instead, those graph/SAT results enter through explicit finite-set and
Boolean-valuation hypotheses.  Lean now verifies the one-flip construction,
witness existence and injection, as well as every subsequent cover and
arithmetic step.  The source reads no external data and uses no certificate,
solver, oracle, floating point, plugin, custom axiom, `sorry`, `admit`,
`unsafe`, or `native_decide`.
