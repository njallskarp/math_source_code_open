# Exact current lower bounds for a nontrivial Collatz cycle

This directory checks a rigorous literature corollary and an elementary exact
strengthening. It is a synthesis of published results, not a proof of the Collatz
conjecture and not a claim of priority for Hercher's odd-entry bound.

## Result

For the shortcut map

\[
C(n)=\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd},
\end{cases}
\]

let a hypothetical nontrivial cycle contain `K` odd entries and `L` even
entries. The checked consequences are:

- `K >= 137,500,000,001`;
- `K + L >= 217,932,343,851` shortcut-map entries;
- `2K + L >= 355,432,343,852` entries under the classical map whose odd
  branch is `3n+1`.

## Proof chain

1. Barina's peer-reviewed 2025 computation verifies convergence for every
   positive integer `n < 2^71`. Hence Hercher's `X_0` is at least `2^71-1`,
   which exceeds `1536 * 2^60`.
2. Corrected Corollary 29 of Hercher (2023, corrigendum 2026) states that
   `X_0 >= 1536 * 2^60` forces every nontrivial cycle to contain
   `K > 1.375 * 10^11` odd entries. Since `K` is integral,
   `K >= 137,500,000,001`.
3. Going once around a shortcut cycle gives `2^(K+L) > 3^K`: every odd
   transition is strictly greater than multiplication by `3/2`, while every
   even transition is multiplication by `1/2`.
4. Exact integer arithmetic gives
   `3^1,063,887 > 2^1,686,221` and
   `3^190,537 < 2^301,994`. These inequalities bracket `log_2(3)` tightly
   enough that both rational bounds give
   `floor(137,500,000,001 * log_2(3)) = 217,932,343,850`.
   Therefore `K+L >= 217,932,343,851`. This is the strongest integer
   conclusion obtainable from `K+L > K log_2(3)` at the least allowed `K`.
5. A shortcut odd transition combines one classical odd transition and its
   forced following even transition. The classical cycle length is therefore
   `(K+L)+K`, giving at least `355,432,343,852` entries.

The Python and Ruby programs perform independent big-integer checks without
floating-point arithmetic.

## Reproduction

```sh
python3 verify_cycle_lower_bound.py
python3 -m unittest -v test_cycle_lower_bound.py
ruby verify_cycle_lower_bound.rb
```

Tested with Python 3.12.12 and Apple Ruby 2.6.10p210.

## Sources

- David Barina, "Improved verification limit for the convergence of the
  Collatz conjecture," *Journal of Supercomputing* 81 (2025), 810,
  <https://doi.org/10.1007/s11227-025-07337-0>.
- Christian Hercher, "There are no Collatz m-Cycles with m <= 91,"
  *Journal of Integer Sequences* 26 (2023), Article 23.3.5,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html>.
- Christian Hercher, corrigendum dated June 14, 2026,
  <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf>.
