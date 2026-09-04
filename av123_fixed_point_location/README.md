# Fixed-point locations in `Av(123)` at distance two

This Lean 4 project formalizes the finite-order reduction used in the proof
of the distance-two slice of the Birmajer--Gil--Tirrell--Weiner conjecture on
fixed points of `123`-avoiding permutations.

Permutations are represented by Mathlib's `Equiv.Perm (Fin n)`, with
zero-based positions and values.  `Avoids123 π` says that no indices
`i < j < k` have `π i < π j < π k`.

The structural theorems prove that if `a < b` are fixed points, then

- every position before `a` maps strictly above `a`;
- every position after `b` maps strictly below `b`;
- injectivity and finite-interval cardinalities give
  `a.val ≤ n - 1 - a.val - 1` and
  `n - 1 - b.val ≤ b.val - 1`.

For fixed points at distance two, the exported parity specializations are

```lean
theorem even_distance_two_fixed_point_locations {m : ℕ} (hm : 2 ≤ m)
    {π : Equiv.Perm (Fin (2 * m))} {a b : Fin (2 * m)}
    (havoid : Avoids123 π) (hgap : a.val + 2 = b.val)
    (hfixa : π a = a) (hfixb : π b = b) :
    (a.val = m - 2 ∧ b.val = m) ∨
      (a.val = m - 1 ∧ b.val = m + 1)

theorem odd_distance_two_fixed_point_locations {m : ℕ} (hm : 2 ≤ m)
    {π : Equiv.Perm (Fin (2 * m + 1))} {a b : Fin (2 * m + 1)}
    (havoid : Avoids123 π) (hgap : a.val + 2 = b.val)
    (hfixa : π a = a) (hfixb : π b = b) :
    a.val = m - 1 ∧ b.val = m + 1
```

In the primary paper's one-based notation, the even pairs are
`(m-1,m+1)` and `(m,m+2)`, while the odd pair is uniquely `(m,m+2)`.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean av123_fixed_point_location
lake build Av123FixedPointLocation
```

Expected final line:

```text
Build completed successfully (769 jobs).
```

The build prints axiom audits for all seven exported theorems.  Their axiom
sets are subsets of the standard Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound`.  The source declares no project axiom
and contains no `sorry`, `admit`, `native_decide`, or `unsafe` declaration.

## Theorem alignment

Birmajer--Gil--Tirrell--Weiner define
`S^(2)_(n,d)(123)` as the `123`-avoiding permutations with two fixed points
at distance `d`, and state their distance-refined count as Conjecture A.2.
The independently reviewed Discovery Net height-1430 result proves the
entire `d=2` slice.  Its proof first derives exactly the location alternatives
formalized here, before constructing block bijections and evaluating their
Catalan counts.

The assumptions here are slightly weaker: two specified fixed points are
enough; no separate “exactly two” hypothesis is used.  The conclusion is the
same location classification after translating between zero- and one-based
indexing.

Discovery Net references:

- reviewed distance-two theorem, height 1430:
  `bafkreifrhhj5ulujd5j27yq3yy5b5j3xnu2dztefpo7o6k7qyduq2yb3xe`;
- independent review, height 1432:
  `bafkreigshgcz6r5fmvhztixxf3n5gwa3pzqvdqvkfhiaszxmol43w534ja`;
- later full-distance ballot-hook theorem, height 1447:
  `bafkreia6ashk7bgas6pqscwngc2jjyrbgdv4xuwwfo5t4qnio2elfczsam`.

Primary source:

- Daniel Birmajer, Juan B. Gil, Jordan O. Tirrell, and Michael D. Weiner,
  *Pattern-avoiding stabilized-interval-free permutations*, Discrete
  Mathematics 348 (2025), 114329; Appendix A,
  https://arxiv.org/abs/2306.03155.

## Trust boundary

There is no external data or computation.  Lean proves the image-band
constraints, both finite-cardinality inequalities, and the exact even/odd
location alternatives.  It does not formalize the block-standardization
bijections, Catalan enumeration, reverse-complement count, the displayed
`d=2` formulas, or the later full ballot-hook proof of Conjecture A.2.
