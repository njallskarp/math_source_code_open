# Exact sign-lift multiplicities in the QLP-42 `q=41` fourth-order layer

This directory sharpens the preceding all-sums classification from existence
to exact multiplicity.  For every fourth-order axis pair surviving all four
Gaussian sum equations, it counts every compatible choice of signs in
`H_A`, `H_B`, `S_A`, and `S_B`.  All calculations are exact integer
calculations; the result is a computational classification, not a proof that
any surviving lift extends through the still-unimposed higher-order equations.

## Classification

Let `L_c(a,b)` be the number of sign lifts of a labeled axis pair `(a,b)` in
canonical case `c`.  Summing `L_c` over all labeled surviving axis pairs gives:

| case | representative | labeled axis pairs | distinct positive `L_c` | min `L_c` | max `L_c` | total labeled sign lifts |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | `(1,0,5,0)`  | 217,261,758 | 21,199 | 13,409,280 | 14,995,685,376 | 138,874,947,997,804,032 |
| 1 | `(3,0,4,1)`  | 193,424,322 | 30,455 | 55,296,000 | 29,330,767,872 | 183,697,028,358,985,344 |
| 2 | `(3,0,3,-2)` | 192,720,234 | 32,653 | 11,796,480 | 46,154,121,216 | 186,769,077,059,884,032 |
| 3 | `(3,2,3,2)`  | 159,187,665 | 27,806 | 46,080,000 | 17,179,869,184 | 122,504,001,698,695,680 |
| 4 | `(3,2,2,3)`  | 159,187,665 | 27,806 | 46,080,000 | 17,179,869,184 | 122,504,001,698,695,680 |
| 5 | `(4,1,2,-1)` | 146,998,278 | 36,964 | 53,760,000 | 14,763,950,080 | 99,012,961,706,367,744 |

Thus feasibility is highly nonuniform: even within a fixed canonical case,
positive fibers occupy tens of thousands of distinct cardinalities.  Case 2
has both the largest single fiber and the largest total number of labeled
sign lifts.  Cases 3 and 4 have identical multiplicity distributions
pointwise, strengthening the earlier identity of their survivor sets.

Exact refinements by `rank(D_b)` and `wt(b)` are committed in
`rank_sign_lifts.tsv` and `weight_sign_lifts.tsv`.  Only ranks 9 and 10 occur,
as forced by the preceding feasibility classification.

## Multiplicity factorization

The zero-direction lemma for reflected family A makes the residual fourth-
order syndrome independent of its pair-sign choices.  Hence, for the unique
residual syndromes `h(a,b)` and `s(a,b)`, the exact fiber factors as

```text
L_c(a,b) = N_HA(a) N_HB(b,h(a,b)) N_SA,c(a) N_SB,c(b,s(a,b)).
```

The two family-A factors are elementary binomial counts.  In family B, fix
the real and imaginary positions.  Requiring an exact Gaussian sum fixes the
number of negative signs on each axis; counting fixed-cardinality subsets by
their `D_b` syndrome gives the other two factors.  The primary program obtains
all 1,024 syndrome multiplicities simultaneously through integer Krawtchouk
coefficients and a length-1,024 Walsh transform.

The exhaustive calculation checks 178,812,928 family-B fiber entries and
3,670,016 family-A counts.  Its canonical full multiplicity-histogram stream
has SHA-256

```text
d9647ab523c722e5a231821299ff07fb5482470092f5dbeea4d29b5df0b3c272
```

## Independent audit

`independent_sample_check.py` uses a different algorithm: direct
fixed-cardinality subset-XOR dynamic programming, with no Walsh transform.
On the independently selected 132 family-B rotation orbits from the preceding
certificate it verifies 811,008 case multiplicities over 135,168 axis pairs.
It also brute-forces all 1,024 family-A pair-sign choices for 32 audit pairs.
Both programs produce the same sampled multiplicity-stream SHA-256:

```text
d9f650cf40abd0460e806d5ebf78cf47941d48b6beffa3730a5bc74f91af9859
```

## Reproduction

Tested with Apple clang 17.0.0, Apple SDK 15.5, Python 3.13.5, and NumPy
2.2.2 on arm64 macOS.

```sh
SDK_CPP="$(xcrun --show-sdk-path)/usr/include/c++/v1"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -isystem "$SDK_CPP" \
  ../qlp42_q41_s_b_syndromes/classify_s_b_syndromes.cpp \
  -o /tmp/classify_s_b_syndromes
python3 classify_exact_sum_multiplicity.py \
  --s-b-binary /tmp/classify_s_b_syndromes
python3 independent_sample_check.py
shasum -a 256 -c SHA256SUMS
```

`classify_exact_sum_multiplicity.py --table` emits the complete multiplicity
histogram whose digest is given above.  The program pins the exact SHA-256 of
the preceding all-sums classifier, and that classifier in turn pins the
lower-level fourth-order and exact-syndrome sources.
