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

## Run

Tested with Python 3.12.12, using only the standard library.

```bash
python3 verify_published_bound.py
python3 -m unittest -v test_published_bound.py
```

## Status and trust boundary

The continued-fraction and rounding bridge is independently exact. The numbers
are a reconstruction of an already published bound, not a novelty claim.

This small checker does **not** independently rerun Hercher's five-week search
or Barina's exhaustive convergence verification. It conditions on the interval
target implemented by Hercher's official program and on the cited published
computations. Hercher's search program uses ordinary floating-point values, so
that upstream numerical implementation remains inside the trust boundary. The
2026 corrigendum repairs the proof of Theorem 21; the interval used here comes
from Theorem 16 and the Corollary 29 search target.

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
