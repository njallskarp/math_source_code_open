# Lean audit: balanced Hamming majority-C shell bounds

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

`HammingShellIncidence.lean` formalizes that displayed incidence inequality
for an arbitrary finite coordinate index and arbitrary finite or infinite
coordinate value types with decidable equality.  With

```text
L_i = {u in C : changeSupport v u = {i}},
B   = {w in C : hammingDist v w = 2},
```

and `h <= |internalNeighbors C u|` for every `u in C`, it proves

```text
sum_i |L_i| * (h - |L_i|) <= 2 * |B|.
```

The proof has two independently reusable ingredients.  First, every selected
neighbor of `u in L_i` is either the center, another member of `L_i`, or a
member of `B`, so at least `h-|L_i|` incidences leave for `B`.  Second, a word
in `B` is adjacent to at most two directed first-shell words: their directions
must be among its two changed coordinates, and adjacency in a fixed direction
uniquely determines the first-shell word.  Mathlib's `Finset` bipartite
degree-sum identity then completes the double count.

`HammingFin3LowerBound.lean` supplies every remaining set-theoretic premise
of the single-class lower bound.  Evaluation at coordinate `i` is injective
on `L_i`, because all other coordinates equal the center; hence
`|L_i| <= n-1`.  Projection from the directed first shell to its words is a
bijection onto the internal neighbors of the center, giving

```text
|internalNeighbors C v| = sum_i |L_i|.
```

Finally, the center, internal-neighbor shell, and distance-two shell are
pairwise disjoint subsets of `C`.  Specializing to `Fin 3 -> Fin n` and using
`Fin.sum_univ_three`, the theorem `fin3_card_ge_of_internal_degree` composes
these facts with `hamming_shell_incidence` and
`card_ge_of_shell_incidence`.  Its exact statement is

```text
2 <= n,
v in C,
forall u in C, n - 1 + n / 2 <= |internalNeighbors C u|
  ==> n * (n / 2 + 1) <= |C|.
```

Here `n-1+n/2 = ceil(3(n-1)/2)` and
`n*(n/2+1) = (N+1)(ceil(N/2)+1)` for `N=n-1`, so the formal theorem matches
the class-size lower bound in the reviewed proof without a parity gap.

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

The full graph theorem still requires two distinct layers:

1. define the majority C-coloring partition interface and lift the nonempty
   class bound to the global upper bound on the number of colors; and
2. formalize the explicit row/column construction attaining that bound and
   the final color-class/floor identities.

Neither layer is silently assumed.  The current artifact kernel-checks the
complete lower bound for one nonempty class, not the full exact majority
C-chromatic formula.

## Literature and graph-first status

The graph target is
`bafkreicfwbaxhguw4rdfoc27q6bjoetwwixwwegogifibnz6d4jqo5xcri`; its
independent accepting review is
`bafkreictoeazrrxx7qhuwrohfnsgxrnanfkz2ekxvvb3kjtywj2m74nhom`; and the
problem statement is
`bafkreiflxkmokhocqgyfh5jqgnpmbr7q2bha6ixoxlxlridb7lfkbmmxae`.
A graph scan at indexed height 1628 found no existing majority-C or Hamming
shell formalization.  The arithmetic bridge was submitted at height 1651 as
`bafkreid34vausp5f5igoj23nezy75cvirmoijx3s7alpup7klwp5vnya7a`.

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
lake env lean HammingShellIncidence.lean
lake env lean HammingFin3LowerBound.lean
```

Expected axiom output for each of the five arithmetic results and the three
audited incidence results, and for each of the four audited specialization
results:

```text
[propext, Classical.choice, Quot.sound]
```

Source SHA-256 values are
`b50d86784dfb20c2eb7928787fb6f9df2758892803fc0adcfa377f538b38bf14`
for `MajorityShellBound.lean` and
`8edc33ce9f96ff3b198ab1cf39ba7dd89c457547ffca3a63559211b7ad957edc`
for `HammingShellIncidence.lean`, and
`49cec09387eaf1eff052b32aa83ad319e668c941f3f89930ae46e524a2ba6f55`
for `HammingFin3LowerBound.lean`.  The sources contain no `sorry`, `admit`,
custom axiom, `unsafe`, or `native_decide`; they read no external files and
use no generated data, certificate, solver, oracle, or nonstandard
kernel/plugin.
