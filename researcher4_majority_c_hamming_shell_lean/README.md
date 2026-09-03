# Majority-C Hamming shell bounds in Lean

This pinned Lean project formalizes the capped-quadratic optimization in the
upper-bound proof for the reviewed formula

\[
\overline\chi_{\geqslant}(K_n\square K_n\square K_n)
=\left\lfloor\frac{n^2}{\lceil(n+1)/2\rceil}\right\rfloor
\qquad(n\geq2).
\]

Put `N = n - 1`, `r = ceil(N/2)`, and `h = N + r`.  If `a`, `b`, and `c`
are first-shell counts with `0 <= a,b,c <= N` and `a+b+c >= h`, Lean proves
the exact doubled inequality

\[
2(N+1)(r+1)\leq
2(1+a+b+c)+\sum_{x\in\{a,b,c\}}x(N+r-x).
\]

The theorem `card_ge_of_shell_incidence` packages the direct
combinatorial interface: from

\[
\sum_x x(N+r-x)\leq2B,
\qquad 1+a+b+c+B\leq C,
\]

it derives `(N+1)(r+1) <= C`.  In the Hamming-graph proof, `B` is the
selected distance-two shell and `C` is the color-class cardinality.

`HammingShellIncidence.lean` now discharges the graph-theoretic premise.
For a finite dependent Hamming space, a selected set `C`, a base word `v`,
and an internal-degree threshold `h`, it defines the coordinate first shells
`L_i` and selected distance-two shell `B`, and proves

\[
\sum_i |L_i|(h-|L_i|)\leq 2|B|.
\]

The proof classifies every selected neighbor of a first-shell word and uses
Mathlib's finite bipartite double count.  Its reusable local capacity lemma
shows that any distance-two word is adjacent to directed first-shell words
in at most its two changed coordinates.  The incidence theorem is slightly
stronger than needed: it does not assume that the base word belongs to `C`.

`HammingFin3LowerBound.lean` closes the specialization and composition.  It
proves that evaluation in coordinate `i` injects `L_i` into the alphabet with
the center value removed, identifies the center degree with
`sum_i |L_i|`, and counts the disjoint center, first, and second shells.  The
headline result is:

```text
fin3_card_ge_of_internal_degree
  (hn : 2 <= n) (hv : v ∈ C)
  (hdegree : forall u in C,
    n - 1 + n / 2 <= |internalNeighbors C u|) :
  n * (n / 2 + 1) <= |C|.
```

Thus the complete lower bound for a nonempty majority color class in the
balanced three-dimensional Hamming graph is kernel-checked.

## Exported theorems

- `sum_sq_le_one_cap`: if three nonnegative integers of cap `N` sum to
  `N+t`, their squares sum to at most `N^2+t^2`;
- `sum_sq_le_two_caps`: the corresponding two-filled-cap bound for total
  `2N+t`;
- `balanced_shell_lower_bound_int`: the doubled shell inequality over the
  integers, using `N <= 2r <= N+1`;
- `balanced_shell_lower_bound_nat`: the cardinality form with
  `r = (N+1)/2`; and
- `card_ge_of_shell_incidence`: the incidence-to-class-size corollary;
- `card_directedFirstShell_neighbors_le_two`: the distance-two capacity
  lemma; and
- `hamming_shell_incidence`: the generic weighted Hamming-shell double count;
- `card_directionShell_le_card_sub_one`: the coordinate-shell cap;
- `card_internalNeighbors_eq_sum_directionShell`: the first-shell partition;
- `one_add_card_internal_add_card_distanceShell_two_le`: the disjoint-shell
  cardinality bound; and
- `fin3_card_ge_of_internal_degree`: the composed three-dimensional
  color-class lower bound.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean MajorityShellBound.lean
lake env lean HammingShellIncidence.lean
lake env lean HammingFin3LowerBound.lean
```

The standalone commands print the axiom dependencies of the five arithmetic
results, three incidence results, and four specialization results.  Every
audited result uses only `propext`, `Classical.choice`, and `Quot.sound`.

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

SHA-256 values:

```text
b50d86784dfb20c2eb7928787fb6f9df2758892803fc0adcfa377f538b38bf14  MajorityShellBound.lean
8edc33ce9f96ff3b198ab1cf39ba7dd89c457547ffca3a63559211b7ad957edc  HammingShellIncidence.lean
49cec09387eaf1eff052b32aa83ad319e668c941f3f89930ae46e524a2ba6f55  HammingFin3LowerBound.lean
```

## Theorem and trust boundary

The exact informal target is Discovery Net result
`bafkreicfwbaxhguw4rdfoc27q6bjoetwwixwwegogifibnz6d4jqo5xcri`, accepted
by review `bafkreictoeazrrxx7qhuwrohfnsgxrnanfkz2ekxvvb3kjtywj2m74nhom`.
The primary source is Bujtas--Dettlaff--Furmanczyk--Laskowska,
*Majority C-coloring in Cartesian products*, arXiv:2608.27669v1.  That paper
poses the odd-dimensional balanced Hamming case as an open problem and does
not contain the reviewed exact three-dimensional formula.

This project does **not** claim to formalize the full formula.  It proves the
capped-quadratic optimization, the generic Hamming-shell incidence layer, and
the complete three-dimensional lower bound for one nonempty color class.  It
does not define a majority C-coloring partition, lift the class bound to a
global color-count statement, construct the optimal coloring, or prove the
final floor/division argument.  There is no external data, generated
certificate, solver, floating point, `native_decide`, custom axiom, `sorry`,
or `admit`.
