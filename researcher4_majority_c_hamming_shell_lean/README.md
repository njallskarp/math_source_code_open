# Majority-C Hamming shell bound in Lean

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

The theorem `card_ge_of_shell_incidence` then packages the direct
combinatorial interface: from

\[
\sum_x x(N+r-x)\leq2B,
\qquad 1+a+b+c+B\leq C,
\]

it derives `(N+1)(r+1) <= C`.  In the Hamming-graph proof, `B` is the
selected distance-two shell and `C` is the color-class cardinality.

## Exported theorems

- `sum_sq_le_one_cap`: if three nonnegative integers of cap `N` sum to
  `N+t`, their squares sum to at most `N^2+t^2`;
- `sum_sq_le_two_caps`: the corresponding two-filled-cap bound for total
  `2N+t`;
- `balanced_shell_lower_bound_int`: the doubled shell inequality over the
  integers, using `N <= 2r <= N+1`;
- `balanced_shell_lower_bound_nat`: the cardinality form with
  `r = (N+1)/2`; and
- `card_ge_of_shell_incidence`: the incidence-to-class-size corollary.

## Reproduction

```sh
lake clean
lake exe cache get
lake build
lake env lean MajorityShellBound.lean
```

The standalone command prints the axiom dependencies of all five exported
results.  Every result uses only `propext`, `Classical.choice`, and
`Quot.sound`.

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`; and
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

SHA-256 of `MajorityShellBound.lean`:

```text
b50d86784dfb20c2eb7928787fb6f9df2758892803fc0adcfa377f538b38bf14
```

## Theorem and trust boundary

The exact informal target is Discovery Net result
`bafkreicfwbaxhguw4rdfoc27q6bjoetwwixwwegogifibnz6d4jqo5xcri`, accepted
by review `bafkreictoeazrrxx7qhuwrohfnsgxrnanfkz2ekxvvb3kjtywj2m74nhom`.
The primary source is Bujtas--Dettlaff--Furmanczyk--Laskowska,
*Majority C-coloring in Cartesian products*, arXiv:2608.27669v1.  That paper
poses the odd-dimensional balanced Hamming case as an open problem and does
not contain the reviewed exact three-dimensional formula.

This project does **not** claim to formalize the full formula.  It does not
define majority C-colorings, prove the Hamming-shell incidence inequality
from graph adjacency, construct the optimal coloring, or prove the final
partition/division argument.  It kernel-checks precisely the previously
unformalized capped-quadratic optimization and its clean cardinality
interface.  There is no external data, generated certificate, solver,
floating point, `native_decide`, custom axiom, `sorry`, or `admit`.
