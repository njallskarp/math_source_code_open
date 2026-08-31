# Exact reconstruction of the published Collatz cycle bound

This directory reconstructs the delicate continued-fraction step behind the
published 2025 statement that a nontrivial positive Collatz cycle would contain
at least

- `217,976,794,617` entries for the shortcut map, and
- `355,504,839,929` entries for the classical map.

It also records a correction to the weaker bounds previously contributed to
Discovery Net. Those weaker numbers are valid consequences of the rounded
premise `K > 1.375e11`, but they are not the current published lower bound.

## Mathematical certificate

Let `K` be the number of odd entries and `N = K + L` the total number of
entries under the shortcut map. Hercher's computer-assisted Corollary 29
targets the mean-reciprocal threshold `A = 4.37e21`. Together with Theorem 16,
the resulting Diophantine interval is

```text
log_2(3) < N/K < log_2(3) + 1/(3*A*ln(2)).
```

The verifier proves, by rigorous rational bounds for `ln(2)` and `ln(3)`, that

```text
103768467013/65470613321
  < log_2(3)
  < 217976794617/137528045312
  < log_2(3) + 1/(3*A*ln(2))
  < 114208327604/72057431991.
```

The first/target and target/last pairs have cross-determinant one. By the
Farey-neighbor lemma, any rational strictly between either pair has denominator
at least the sum of the neighboring denominators. Consequently the least
possible denominator in the displayed open interval is exactly
`K = 137,528,045,312`, attained by the target fraction. Its numerator is
`N = 217,976,794,617`, and expanding each shortcut odd step adds `K`, yielding

```text
N + K = 355,504,839,929.
```

The proof uses the positive atanh series

```text
ln(x) = 2 * sum_(k>=0) z^(2k+1)/(2k+1),  z=(x-1)/(x+1),
```

with an exact geometric tail bound. No floating-point arithmetic or enormous
integer powers are used.

## Exact stability window and next jump

For the parameterized interval

```text
log_2(3) < N/K < log_2(3) + 1/(3*A*ln(2)),
```

the published bound is locally constant over a large exact range of integer
`A`. The checker isolates each transcendental transition threshold between two
consecutive integers. The current phase begins at

```text
A = 4,358,487,209,795,430,953,243
```

and persists through

```text
A = 51,012,555,828,807,148,352,152.
```

Hercher's target `A = 4,370,000,000,000,000,000,000` is only about `0.263%`
above the phase-entry threshold. On the other hand, the method cannot make its
next discrete improvement until `A` reaches

```text
51,012,555,828,807,148,352,153,
```

about `11.67` times the current target. From there through

```text
A = 380,764,284,831,658,724,601,024,
```

the least admissible upper semiconvergent is

```text
1411629234715/890638885193,
```

which would force at least `890,638,885,193` odd entries,
`1,411,629,234,715` shortcut entries, and `2,302,268,119,908` classical
entries. This is a conditional phase diagram for the existing
mean-reciprocal/continued-fraction method, not a claim that the stronger
mean-reciprocal premise has been proved.

## Run

Tested with Python 3.12.12, using only the standard library, and Lean 4.33.1.

```bash
python3 verify_published_bound.py
python3 -m unittest -v test_published_bound.py
lean lean/CollatzFareyBounds.lean
```

The Lean toolchain is pinned in `lean-toolchain`. The Lean file uses no Mathlib,
no `sorry`, no `admit`, no custom axioms, and no `native_decide`. Its six main
theorems formalize the exact denominator, shortcut-length, and classical-length
consequences for the current and next rational phases. `#print axioms` reports
only Lean's standard `propext` and `Quot.sound`, introduced through the
kernel-bundled `omega` tactic.

## Status and trust boundary

The continued-fraction and rounding bridge is independently exact. The numbers
are a reconstruction of an already published bound, not a novelty claim. Lean
checks the discrete rational-interval-to-length bridge and the closed
determinant/witness arithmetic.

Neither checker independently reruns Hercher's five-week search
or Barina's exhaustive convergence verification. It conditions on the interval
target implemented by Hercher's official program and on the cited published
computations. Hercher's search program uses ordinary floating-point values, so
that upstream numerical implementation remains inside the trust boundary. The
2026 corrigendum repairs the proof of Theorem 21; the interval used here comes
from Theorem 16 and the Corollary 29 search target. Lean also does not formalize
the atanh-series derivation of the logarithmic endpoint inequalities; the exact
Python checker remains the bridge for those analytic comparisons.

Primary sources retrieved 2026-08-31:

- D. Barina, “Improved verification limit for the convergence of the Collatz
  conjecture,” *Journal of Supercomputing* 81 (2025), 810.
  <https://doi.org/10.1007/s11227-025-07337-0>
  PDF SHA-256: `764fd732ad79545e71440f74bf738bf315b479eb404f68bae2c3b109785a5d06`.
- C. Hercher, “There are no Collatz m-Cycles with m <= 91,” *Journal of
  Integer Sequences* 26 (2023), Article 23.3.5.
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.pdf>
  PDF SHA-256: `ca214153465c69d0927ee43fc62ad617da6345e68301026b6811f3f9d244d6a3`.
- Hercher's official Corollary 29 program:
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/collatz_cycle.cpp>
  SHA-256: `aee76b12281e69f0ded6bc7e527f88c71453b10acbe5e1b19bca86fd69a2c372`.
- Hercher corrigendum (2026):
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf>
  SHA-256: `718b75103f306898d6d457f3fae10b652efc6227b94e64f0bafadaddb53bc76b`.
