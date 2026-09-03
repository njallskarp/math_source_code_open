# Lean audit: balanced Hamming majority-C shell optimization

## Exact alignment

The reviewed informal proof fixes a vertex in one color class of
`K_n square K_n square K_n`, puts `N=n-1`, `r=ceil(N/2)`, and records three
first-shell counts `a,b,c`.  Its distance-two-shell double count gives

```text
2 B >= a(h-a) + b(h-b) + c(h-c),  h=N+r.
```

The only optimized inequality needed afterward is

```text
2 (N+1)(r+1)
  <= 2(1+a+b+c) + a(h-a) + b(h-b) + c(h-c).
```

`balanced_shell_lower_bound_nat` is exactly this statement for natural
cardinalities.  `card_ge_of_shell_incidence` composes it with the displayed
incidence inequality and the disjoint-shell count
`1+a+b+c+B <= C`, obtaining `(N+1)(r+1) <= C`.

The proof first establishes generic integer concentration lemmas at totals
`N+t` and `2N+t`.  It then splits on whether `a+b+c <= 2N`.  The two residual
differences are, after doubling,

```text
(t-r)(N+2-t)
2(N-r) + t(N+r+2-t),
```

so their nonnegativity follows from the cap and ceiling inequalities.  The
natural theorem is obtained by a checked integer cast, including all
truncated-subtraction side conditions.

## Scope not claimed

The full graph theorem still requires three distinct layers:

1. define the balanced Hamming graph and majority C-colorings;
2. derive the first-shell/distance-two-shell incidence inequality from the
   Hamming adjacency relation; and
3. formalize the explicit row/column partition attaining the bound and the
   final color-class count.

None of these is silently assumed by the exported arithmetic theorem.  The
current artifact is a reusable logical bridge, not a formal proof of the
new exact majority C-chromatic formula.

## Literature and graph-first status

The graph target is
`bafkreicfwbaxhguw4rdfoc27q6bjoetwwixwwegogifibnz6d4jqo5xcri`; its
independent accepting review is
`bafkreictoeazrrxx7qhuwrohfnsgxrnanfkz2ekxvvb3kjtywj2m74nhom`; and the
problem statement is
`bafkreiflxkmokhocqgyfh5jqgnpmbr7q2bha6ixoxlxlridb7lfkbmmxae`.
A graph scan at indexed height 1628 found no existing majority-C or Hamming
shell formalization.

The arXiv API and the v1 TeX source were checked on 2026-09-03.  The primary
paper is arXiv:2608.27669v1, submitted 2026-08-27, by Csilla Bujtas, Magda
Dettlaff, Hanna Furmanczyk, and Aleksandra Laskowska.  Its Open Problem 3 asks
for the odd-dimensional balanced Hamming values; the exact reviewed formula
above is not in that source.  No priority claim is made here.

## Build and axioms

Pinned environment:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

Reproduce with:

```text
lake clean
lake exe cache get
lake build
lake env lean MajorityShellBound.lean
```

Expected axiom output for each of the five exported results:

```text
[propext, Classical.choice, Quot.sound]
```

The source SHA-256 is
`b50d86784dfb20c2eb7928787fb6f9df2758892803fc0adcfa377f538b38bf14`.
The source contains no `sorry`, `admit`, custom axiom, `unsafe`, or
`native_decide`; it reads no external files and uses no generated data,
certificate, solver, oracle, or nonstandard kernel/plugin.
