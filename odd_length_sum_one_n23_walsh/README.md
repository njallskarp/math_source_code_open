# Prime-23 rank theorem and exact sum-one hyperplanes

This directory advances the odd-length exact-sum syndrome program from
compressed length 21 to 23.  It proves the rank structure algebraically and
certifies exact-sum-one surjectivity with an exhaustive algorithm independent
of the earlier fixed-cardinality subset-XOR verifier.

## Setup

For `b,sigma in F_2^23`, with indices modulo 23, define

```text
D_b(sigma)_s = sum_j (sigma_j + sigma_{j+s})(b_j + b_{j+s}) in F_2,
1 <= s <= 11.
```

Let

```text
T_b = {D_b(sigma) : sum_j (-1)^sigma_j i^b_j = 1}.
```

The general odd-length parity theorem gives, for even-weight `b`,

```text
T_b subset {t in image(D_b) : sum_s t_s = wt(b)/2 (mod 2)}.    (1)
```

## Algebraic rank theorem

For every nonzero even-weight `b`,

```text
rank(D_b) = 11.                                                (2)
```

This is an ordinary algebraic proof, independent of the exhaustive census.
In the group algebra `R=F_2[x]/(x^23-1)`, reciprocal conjugation is denoted by
`*`.  If `C=sigma b*`, then

```text
D_b(sigma)_s = C_s + C_{-s},
```

so `D_b(sigma)=0` exactly when `C=C*`.

The order of 2 modulo 23 is 11, and

```text
Phi_23(x)
 = (x^11+x^9+x^7+x^6+x^5+x+1)
   (x^11+x^10+x^6+x^5+x^4+x^2+1),
```

where the two degree-11 factors are irreducible and reciprocal.  Consequently

```text
R is isomorphic to F_2 times K times K,   K=F_(2^11),
```

and reciprocal conjugation exchanges the two `K` components.  Even weight
means that `b` has zero `F_2` component.  After identifying the reciprocal
field factors, write

```text
b=(0,p,q),   sigma=(e,u,v).
```

The condition `sigma b* = (sigma b*)*` becomes the single field equation

```text
u q = v p.                                                     (3)
```

For nonzero `b`, `(p,q)` is not `(0,0)`, so (3) is a nonzero surjective
`K`-linear map from `K^2` to `K`.  Its kernel has binary dimension 11; the
free `F_2` component `e` makes `dim ker(D_b)=12`.  Rank-nullity proves (2).
The zero word has rank zero.  `verify_prime23_factorization.py` independently
checks the displayed factorization, reciprocity, irreducibility, and order.

## Exhaustive exact-sum theorem

For all 4,194,304 even axis words,

```text
T_b = {t in image(D_b) : sum_s t_s = wt(b)/2 (mod 2)}.          (4)
```

Thus the unrestricted odd-length sum-one conjecture is now computationally
proved through length 23.  The exact length-23 census is:

| quantity | value |
|---|---:|
| even labeled axis words | 4,194,304 |
| cyclic axis orbits | 182,362 |
| rank-0 orbits | 1 |
| rank-11 orbits | 182,361 |
| right-hand-side-zero orbits | 91,226 |
| right-hand-side-one orbits | 91,136 |
| labeled axis-syndrome pairs | 4,294,966,273 |
| orbit-syndrome pairs | 186,737,665 |
| exact-sum-one signed unit words | 1,828,114,918,084 |

Every nonzero axis word has a 1,024-point support by (2) and (4); the zero
word contributes the singleton syndrome zero.

## Independent algorithms

`verify_n23_walsh.cpp` visits one canonical member of every cyclic orbit.  It
obtains the exact fiber cardinality at all 2,048 syndromes by multiplying two
fixed-cardinality binary Krawtchouk coefficients and applying exact integer
Walsh inversion.  It checks nonnegativity, fixed-cardinality totals, (1), (2),
and equality (4) orbit by orbit.  The full 182,362-record canonical stream has
SHA-256

```text
d57ee070934d847b065474ce64ca439b71d8e2880594242bc9da70e62a34d023.
```

This is algorithmically independent of the subset-XOR implementation that
first explored length 23 in the graph review.  Conversely,
`independent_sample_check.py` uses direct fixed-cardinality subset-XOR dynamic
programming, with no Walsh transform or Krawtchouk coefficient.  It checks 508
deterministically spaced rotation orbits and 1,040,384 syndrome memberships;
its detailed support-stream digest is

```text
08198a4e96b8ef223404c03ad1977b76b0d71dac0abed4e6a94606002436b88a.
```

## Reproduction

Tested with Apple clang 17.0.0, Apple SDK 26.2, and Python 3.12.12 on arm64
macOS.  The exhaustive verifier uses signed 64-bit integer arithmetic; its
largest relevant binomial and transform values are far below the limit.

```sh
SDK_CPP="$(xcrun --show-sdk-path)/usr/include/c++/v1"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -isystem "$SDK_CPP" \
  verify_n23_walsh.cpp -o /tmp/verify_n23_walsh
/tmp/verify_n23_walsh
/tmp/verify_n23_walsh --stream | shasum -a 256
python3 verify_prime23_factorization.py
python3 independent_sample_check.py
shasum -a 256 -c SHA256SUMS
```

## Scope and novelty

This work directly answers the highest-impact finite-extension request in the
review of the through-21 theorem: the earlier exploratory length-23 run reused
the target algorithm, while this certificate uses exhaustive Walsh inversion.
The algebraic rank theorem is separate from that computation.  The surrounding
QLP context is Kotsireas--Winterhof,
[*Quaternary Legendre pairs*](https://arxiv.org/abs/2212.10953), and
Kotsireas--Koutschan--Winterhof,
[*Quaternary Legendre pairs II*](https://arxiv.org/abs/2408.16318).

Targeted graph and primary-source searches found no matching prime-23 rank
theorem or exact-syndrome census.  This is a search-relative novelty assessment,
not a historical-priority claim.  Equality (4) is a finite computer-assisted
theorem at length 23.  It does not prove sum-one equality for all odd lengths,
settle QLP-42, or impose missing higher-order autocorrelation equations.
