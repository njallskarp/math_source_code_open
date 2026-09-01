# Odd-length exact-sum syndrome parity and sum-one hyperplanes through 21

This directory separates a general structural theorem from a finite
surjectivity phenomenon suggested by the QLP-42 `q=41` branch.  It also gives
an exhaustive direct-subset reproduction of the previously certified
length-21 sum-one syndrome hyperplanes.

## General parity theorem

Let `n=2m+1` be odd and let `b,sigma` be binary words indexed modulo `n`.
Define

```text
D_b(sigma)_s = sum_j (sigma_j + sigma_{j+s})(b_j + b_{j+s}) in F_2,
1 <= s <= m.
```

Write `w=wt(b)`.  If the associated Gaussian unit word has exact sum

```text
sum_j (-1)^sigma_j i^b_j = X + iY,
```

then every syndrome `t=D_b(sigma)` satisfies

```text
sum_s t_s = (w mod 2)(n-X-Y)/2 + (w-Y)/2                 (mod 2).  (1)
```

This is a proof, not a computational conjecture.  The coefficient of
`sigma_k` in the sum of the `m` syndrome coordinates is

```text
sum_{s=1}^m (b_{k+s}+b_{k-s}) = w+b_k                    (mod 2),
```

because the `2m` shifted indices cover every position except `k`.  Hence

```text
sum_s D_b(sigma)_s = (w mod 2) wt(sigma) + b dot sigma.
```

The exact Gaussian sum fixes

```text
wt(sigma)=(n-X-Y)/2,   b dot sigma=(w-Y)/2,
```

which proves (1).

For the central target `X+iY=1`, feasibility forces even `w`, and (1) becomes

```text
sum_s t_s = w/2 (mod 2).                                 (2)
```

## Exhaustive finite theorem

For every odd `n` in

```text
3,5,7,9,11,13,15,17,19,21
```

and every even-weight `b in F_2^n`, direct exhaustive computation proves

```text
{D_b(sigma) : sum_j (-1)^sigma_j i^b_j = 1}
 = {t in image(D_b) : sum_s t_s = wt(b)/2 (mod 2)}.       (3)
```

The exact axis-word, rotation-orbit, labeled-syndrome, and orbit-syndrome
counts are in `sum_one_census.tsv`.  Equation (3) is therefore a finite
theorem through length 21.  It motivates, but does not prove, the conjecture
that (3) holds for every odd length.

At `n=21`, the checker visits all 49,940 even-axis rotation orbits and directly
constructs every support using fixed-cardinality subset-XOR dynamic
programming.  It uses neither Krawtchouk coefficients nor a Walsh transform.
Its canonical stream is byte-identical to the earlier exhaustive certificate:

```text
SHA-256 03494099cbe4c7baff54bb27ebb1808af123badc133cf24d6b544bb441d9b2e7.
```

This is an exhaustive second-algorithm reproduction, strengthening the prior
256-axis sampled subset-XOR audit.

## Sharp boundary: other exact targets

The tempting extension of (3) to every exact target is false.  The smallest
odd length where it fails is `n=5`.  Take `b=00001` and target `4+i`.  The
target forces the all-positive sign word, so its support is `{00}`, whereas
the parity slice in `image(D_b)=F_2^2` is `{00,11}`.

`verify_general_parity_and_counterexample.py` checks all 4,473,920 axis/sign
assignments for odd lengths through 11.  It verifies the general containment
(1), proves that every exact-target fiber fills its parity slice at `n=3`, and
finds 160 proper subsets among 352 target fibers already at `n=5`.  The full
census is in `all_target_census.tsv`.

## Algorithms and reproduction

`verify_sum_one_subset_xor.cpp` represents a syndrome set by a 1,024-bit
bitset.  For each real or imaginary axis class, a descending-cardinality
dynamic program constructs the XOR support of all subsets of the required
size.  XOR convolution combines the two classes.  Cyclic rotation is used
only after proving that it preserves both the target sum and every syndrome.

Tested with Apple clang 17.0.0, Apple SDK 26.2, and Python 3.12.12 on arm64
macOS.  An AddressSanitizer/UndefinedBehaviorSanitizer build was also run.

```sh
SDK_CPP="$(xcrun --show-sdk-path)/usr/include/c++/v1"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -isystem "$SDK_CPP" \
  verify_sum_one_subset_xor.cpp -o /tmp/verify_sum_one_subset_xor
/tmp/verify_sum_one_subset_xor
/tmp/verify_sum_one_subset_xor --q41-stream | shasum -a 256
python3 verify_general_parity_and_counterexample.py
shasum -a 256 -c SHA256SUMS
```

## Context, novelty, and scope

The QLP motivation and the unresolved length-42 case are described in
Kotsireas--Winterhof, [*Quaternary Legendre
pairs*](https://arxiv.org/abs/2212.10953), and Kotsireas--Koutschan--Winterhof,
[*Quaternary Legendre pairs II*](https://arxiv.org/abs/2408.16318).  A targeted
search found no statement of (1), no general sum-one equality theorem, and no
matching small-length census.  This is evidence of graph-level novelty and a
search-relative novelty assessment, not a historical-priority claim.

The parity identity (1) is fully proved.  Equality (3) is computationally
proved only for the ten displayed lengths.  Its unrestricted odd-length form
remains a conjecture.  None of these statements proves existence or
nonexistence of a quaternary Legendre pair of length 42 or imposes the missing
higher-order and integral autocorrelation equations.
