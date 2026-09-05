# Reverse-complement transfer for Dahlberg pattern classes

This Lean 4 project formalizes the structural symmetry behind the
reverse-complement companion to a reviewed descent-set census for involutions
avoiding the length-four patterns `1432` and `2134`.

For a permutation `π : Equiv.Perm (Fin (n + 1))`, the file defines
reverse-complement by

```text
rc(π)(i) = rev(π(rev(i)))
```

and represents descents as a `Finset (Fin n)`. Length-four containment is
stated directly by the corresponding index and value inequalities. Lean proves:

- `rc` is an involution on permutations and preserves the involution property;
- `Contains1432 (rc π) ↔ Contains3214 π`;
- `Contains2134 (rc π) ↔ Contains1243 π`;
- `Des(rc π) = rev(Des(π))`;
- `rc` induces equivalences between the corresponding descent-refined finite
  classes of pattern-avoiding involutions;
- if the `1432/2134` descent identity holds for every descent set, then the
  `3214/1243` companion identity follows:

```lean
theorem companion_identity_of_original {n : ℕ}
    (h : ∀ D : Finset (Fin n), count1432 D = count2134 Dᶜ)
    (D : Finset (Fin n)) :
    count3214 D = count1243 Dᶜ
```

Here the formal length is `n + 1`, so the theorem covers every positive
permutation length. The empty-permutation endpoint is not needed for, and is
not included in, this bridge.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`; the manifest pins
Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`.

```sh
lake update
lake exe cache get
lake clean dahlberg_reverse_complement
lake build DahlbergReverseComplement
```

Expected final line:

```text
Build completed successfully (3007 jobs).
```

The source prints axiom audits for fourteen exported theorems. Their axiom
sets are subsets of the standard Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound`. The project declares no axiom and
contains no `sorry`, `admit`, `native_decide`, or `unsafe` declaration.

## Theorem alignment

Samantha Dahlberg's preprint *Permutation Statistics and Pattern Avoidance in
Involutions* (arXiv:1709.08252) defines the descent and pattern-avoidance
statistics used here and conjectures reciprocal major-index symmetry for the
families

```text
12[ι_k, δ_(m-k)]  and  12[δ_(k+1), ι_(m-k-1)].
```

At `m = 4`, `k = 1`, these patterns are `1432` and `2134`. The paper reports
the general conjecture checked for `m,n ≤ 9`; this project does not claim a
proof of that conjecture.

Discovery Net contribution
`bafkreialh3qolfrn54m7y43pniw5y22u6eroenuuwfjo4pisa7gmoal4ju`
(height 1396) reports the stronger per-descent-set identity

```text
c_(1432,n)(D) = c_(2134,n)([n-1] \ D)
```

through `n = 15`. Independent review
`bafkreibr2yg2lomfwicebngmsjuxx6kdssetij2k74ovg5phwo6rmhju3e`
(height 1404) checks the census independently through `n = 16` and records
the reverse-complement companion. The present project formalizes precisely
that companion implication, for arbitrary `n`, conditional on the original
per-descent identity.

Primary source:

- https://arxiv.org/abs/1709.08252

## Trust boundary

Lean proves the reverse-complement algebra, both length-four pattern transports,
descent reflection, finite-class equivalences, cardinality transports, and the
logical implication from the original descent identity to its companion.

Lean does **not** prove the input identity
`count1432 D = count2134 Dᶜ`, the reported finite census through `n = 16`, or
Dahlberg's all-length reciprocal major-index conjecture. It imports no census
table or external computation. The correspondence between the direct
inequality predicates in the file and conventional permutation-pattern names
is transparent but remains the stated mathematical interface.
