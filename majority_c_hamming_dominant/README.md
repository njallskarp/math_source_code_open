# Dominant-factor majority C-colourings of Hamming graphs

This directory proves a sharp formula for a strongly imbalanced family of
Hamming graphs.  It is a self-contained contribution to the problem of
determining majority C-chromatic numbers of imbalanced Hamming graphs.

Let

```text
G = K_{n_1} square K_{n_2} square ... square K_{n_d},
n_1 >= n_2 >= ... >= n_d >= 2,
N_i = n_i - 1,                 S = N_2 + ... + N_d.
```

A majority C-colouring is a partition into nonempty colour classes such that
every vertex has at least half of its neighbours in its own class.  If

```text
N_1 >= S + 2,
```

then

```text
chi_bar_>=(G) = product_{i=2}^d n_i.
```

When `d >= 3`, every colouring attaining this maximum consists of the full
`K_{n_1}` fibres, up to relabelling colours.  In dimension three this is the
parameter range complementary to the previously established near-triangle
range `ceil((N_1+N_2+N_3)/2) >= N_1`.

The proof is in [DOMINANT_FACTOR_THEOREM.md](DOMINANT_FACTOR_THEOREM.md).

## Reproduction

CPython 3.12 or later; standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_dominant_factor.py
```

Expected output:

```text
dominant pairs checked: 19900
coarse shell profiles checked: 66670000
structured parameter tuples checked: 1027
structured shell profiles checked: 394709
K5xK2xK2 candidate subsets checked: 20349
K5xK2xK2 feasible size-5 subsets: 4
minimum doubled strict-margin (S>=2): 2
all exact checks passed
```

The complete stdout SHA-256 is recorded in `SHA256SUMS` after the verifier
source hash.

## Evidence and trust boundary

The theorem is proved by an exact first/second-shell incidence inequality and
elementary concavity.  The verifier uses only arbitrary-precision Python
integers.  It exhausts the two-variable inequality reduction through
`N_1=201`, audits millions of bounded coordinate profiles in dimensions two
through five, and directly enumerates every subset of orders four and five in
the boundary graph `K_5 square K_2 square K_2`.

The computation checks conventions, endpoint arithmetic, and a small graph; it
does not prove the universal theorem.  There is no floating point, randomness,
solver, network input, or external data.

## Literature boundary

Bujtas, Dettlaff, Furmanczyk, and Laskowska introduced the product problem and
explicitly ask for the three- and four-dimensional imbalanced Hamming cases in
Open Problem 2 of *Majority C-coloring in Cartesian products* (2026):

<https://arxiv.org/abs/2608.27669>

Their Proposition 15 supplies the dominant-fibre lower bound but not the upper
bound or equality classification proved here.  Targeted searches on 2026-09-04
found that primary source and the introductory paper
<https://arxiv.org/abs/2604.20752>, but no matching dominant-factor theorem.
This is search-relative novelty, not a historical-priority claim.
