# Exact sum-one syndrome hyperplanes for the QLP-42 `q=41` branch

## Theorem

Let `b in F_2^21` be an axis word and let

```text
D_b(sigma)(s) = sum_j (sigma_j+sigma_(j+s))(b_j+b_(j+s)),
                                                        1 <= s <= 10
```

be the fourth-order family-`B` sign map.  Associate to `(b,sigma)` the
Gaussian unit word

```text
W_j = (-1)^sigma_j i^b_j.
```

For every even-weight `b`, define its exact-sum syndrome set

```text
T_b = { D_b(sigma) : sum_j W_j = 1 } subset F_2^10.       (1)
```

If `r=rank(D_b)`, then `T_b` is an affine subspace of `image(D_b)` with

```text
dim(T_b) = 0       if r=0,
dim(T_b) = r-1     if r>0.                                (2)
```

Thus `T_b` is one point at rank zero and is an affine hyperplane in the
`r`-dimensional sign image at every positive rank.  In particular,

```text
|T_b| = 1                  if r=0,
|T_b| = 2^(r-1)            if r>0.                         (3)
```

Odd-weight `b` cannot occur in (1), because an odd number of imaginary-axis
units cannot have imaginary sum zero.  The exhaustive rank distribution for
all even-weight words is:

| `r` | even axis words | rotation orbits | `dim(T_b)` | `|T_b|` | word-syndrome pairs |
|---:|---:|---:|---:|---:|---:|
| 0  | 1       | 1      | 0 | 1   | 1 |
| 1  | 3       | 1      | 0 | 1   | 3 |
| 3  | 63      | 9      | 2 | 4   | 252 |
| 4  | 189     | 9      | 3 | 8   | 1,512 |
| 6  | 4,095   | 195    | 5 | 32  | 131,040 |
| 7  | 12,285  | 585    | 6 | 64  | 786,240 |
| 9  | 257,985 | 12,285 | 8 | 256 | 66,044,160 |
| 10 | 773,955 | 36,855 | 9 | 512 | 396,264,960 |

Across all `2^20=1,048,576` even axis words there are exactly

```text
463,228,168 axis-word/syndrome pairs,
124,408,576,656 signed unit words with Gaussian sum 1.
```

The first total is the size of the exact frequency-zero interface that the
remaining reflected family-`A` sum constraints must meet.  It replaces an
apparent search over all `2^21` sign words for every `b` by a single affine
hyperplane.

## Exact-sum cardinalities

Put `w=wt(b)`.  If `sum_j W_j=1`, the real and imaginary coordinates give

```text
number of negative real-axis signs      = (20-w)/2,
number of negative imaginary-axis signs = w/2.             (4)
```

Conversely, (4) is sufficient for the Gaussian sum to equal one.  In
particular every exact-sum sign word has exactly ten negative signs.  The
syndrome set in (1) is therefore the image under `D_b` of one product of two
middle cardinality layers, one on each axis.

## Walsh--Krawtchouk certificate

For a character `lambda in F_2^10`, let `q=D_b^T lambda in F_2^21`.  If
`m_R(lambda)` and `m_I(lambda)` count the ones of `q` on the real and
imaginary axis positions, the Fourier transform of the exact-syndrome fiber
counts is

```text
K_((20-w)/2)(21-w, m_R(lambda))
  * K_(w/2)(w, m_I(lambda)),                                (5)
```

where

```text
K_k(n,m) = sum_t (-1)^t binom(m,t) binom(n-m,k-t)
```

is a binary Krawtchouk coefficient.  An exact inverse Walsh transform of
the 1,024 values in (5) gives the number of sign words above every syndrome.
The support is then checked for affine closure and the dimension in (2).

Run the exhaustive C++ certificate:

```bash
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  -isystem "$(xcrun --show-sdk-path)/usr/include/c++/v1" \
  verify_h_sum_syndromes.cpp -o verify_h_sum_syndromes
./verify_h_sum_syndromes
```

It canonicalizes every binary rotation orbit of length 21 and processes all
49,940 even-weight orbits.  Every Walsh coefficient, inverse fiber count,
binomial total, affine support, dimension, rank stratum, and table row is
checked with integer arithmetic.  Rotations preserve both the Gaussian sum
and the ten syndrome coordinates, so one representative proves the support
statement for its complete orbit while its orbit size recovers labeled-word
counts.

An implementation-independent sample audit uses direct subset enumeration:

```bash
python3 independent_sample_check.py
```

It constructs the two exact-cardinality subset-XOR sets without Walsh or
Krawtchouk transforms for 256 deterministic axis words, explicitly covers
all eight ranks, and checks affine closure and (2) directly.

No floating point, SAT/SMT status, randomized proof step, or heuristic search
enters the exhaustive result.  The C++ certificate was run with Apple clang
17.0.0 and the Python audit with Python 3.12.12 on arm64.

## Scope and next bridge

This theorem handles the exact equation `sum(H_B)=1` together with the
fourth-order `B` syndrome.  It does not yet impose `sum(H_A)=0`, either `S`
sum, or the full integer autocorrelations.  In the `q=41` shell,
`sum(H_A)=0` additionally forces `wt(b)=0 mod 4`; the present theorem is
stronger on the `B` side because it covers every even weight.

The next finite step is now sharply posed: compute the affine syndrome set
attained by reflected `H_A` signs under `sum(H_A)=0`, translate it by the
fourth-order residual, and test intersection with the hyperplane `T_b`.
The same construction can then be repeated for each of the six `S` sum
targets.

Primary context: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications* (arXiv:1302.0571);
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*
(arXiv:2408.16318); Kotsireas--Winterhof, *Quaternary Legendre Pairs*
(arXiv:2212.10953); and Jedwab--Pender, *Two constructions of quaternary
Legendre pairs of even length* (arXiv:2408.08472).  A targeted primary-source
and current-graph search found no matching exact-sum syndrome theorem;
apparent novelty is relative to that search, not a priority claim.
