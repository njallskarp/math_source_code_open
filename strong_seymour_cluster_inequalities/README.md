# Strong Seymour cluster inequalities in Lean

This pinned Lean project proves the exact integer minimization lemma isolated
by an accepted Discovery Net review of the Bai--Li--Park blow-up construction.
It is a small Presburger-arithmetic result, separate from both the tournament
construction and the computer verification of the order-14 theorem.

## Main theorem

For positive natural numbers `(a,b,c,d,e,f)`, define feasibility by the six
strict inequalities

```text
c + d < b + e + f,     c < e + f,
e + f < a + b + d,     b + f < a,
a + b + d < c + f,     a + b < c.
```

`cluster_total_ge_36` proves that every feasible tuple satisfies

```text
36 <= a + b + c + d + e + f.
```

`cluster_total_eq_36_iff` sharpens this to an exact equality classification:

```text
feasible and total = 36  iff  (a,b,c,d,e,f) = (7,3,11,3,9,3).
```

The file also proves the displayed tuple feasible and records several sharp
component lower bounds.  All proofs use Lean's verified `omega` tactic.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean StrongSeymourCluster.lean
```

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib v4.33.1, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Expected results with the committed manifest:

- Mathlib cache: 8,690 artifacts;
- clean project build: 3 jobs completed successfully; and
- standalone replay: exit zero and five printed axiom audits, each containing
  only `propext`, `Classical.choice`, and `Quot.sound` (with
  `cluster_total_ge_36` not requiring `Classical.choice`).

Source SHA-256:

```text
28e67ea73500dee2a397efe9bfd6048f282684326ef539d3de6f9f7362598758  StrongSeymourCluster.lean
```

## Theorem alignment and trust boundary

The inequalities are transcribed from Remark 3.1 of Bai--Li--Park,
[“Towards a strengthening of the second neighborhood conjecture”](https://arxiv.org/abs/2607.18047).
That remark gives these sufficient inequalities and the feasible choice
`(7,3,11,3,9,3)`, leading to their 36-vertex tournament.  The graph artifact
under review additionally asserts that 36 is the minimum possible total for
this six-cluster inequality system and that equality is unique.  This project
kernel-checks exactly that auxiliary assertion; it makes no claim that the
minimum or uniqueness was stated in the paper.

Discovery Net references:

- target lemma, height 1445:
  `bafkreihw2ey3zdfjhlhvpyat6h7ogxlgsif2felg3r7ett6g2puqp2625e`;
- accepted independent review, height 1475:
  `bafkreifgktmka7lfqspouj3jelugvauf4h7i7adki4ikq3nkzc3nhq2yc4`; and
- problem statement, height 1440:
  `bafkreicoploedp7v3y4u23f2ae3otetmoazhug4hiqy2iurooepslgdnyq`.

Lean does **not** formalize here:

- tournaments, second neighborhoods, or strong Seymour vertices;
- the six-cluster blow-up construction;
- the proof that satisfying these inequalities makes that construction a
  counterexample;
- the order-at-most-14 theorem or its SAT/DRAT certificates; or
- any claim about tournament orders 15 through 35.

Those are explicit external mathematical or computational bridges.  The Lean
file reads no external data and uses no generated certificate, solver, oracle,
floating point, plugin, or nonstandard kernel feature.  It contains no
`sorry`, `admit`, custom axiom, `unsafe`, or `native_decide`.
