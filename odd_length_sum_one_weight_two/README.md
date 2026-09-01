# Infinite exact sum-one theorem for unit-separated weight-two axes

This directory proves an infinite-family positivity theorem for the odd-length
exact-sum syndrome program.  It replaces Walsh-coefficient bounds by a direct
reflection-pair decomposition and gives every nonzero fiber multiplicity in
closed form.

## Theorem

Let `n=2m+1` be odd.  Let the binary axis word `b` have ones at two positions
whose difference `d` is coprime to `n`.  Define

```text
D_b(sigma)_s = sum_j (sigma_j+sigma_(j+s))(b_j+b_(j+s)) in F_2,
1 <= s <= m.
```

For the exact Gaussian target

```text
sum_j (-1)^sigma_j i^b_j = 1,
```

the syndrome support is exactly

```text
{t in F_2^m : sum_s t_s = 1}.                               (1)
```

Thus every allowed syndrome is attained.  Moreover, after translating and
decimating indices to put the two ones of `b` at positions `0,1`, define

```text
p_0 = 1,
p_s = 1 + t_1 + ... + t_s,   1 <= s <= m-1,
h(t) = number of s in {1,...,m-1} with p_s=1.
```

Then the exact number of signed words in the fiber over an allowed `t` is

```text
2^(h(t)+1) binom(m-1-h(t), floor((m-1-h(t))/2)).              (2)
```

Formula (2) is always positive and is an ordinary combinatorial theorem, not
an asymptotic or computer-assisted assertion.

## Reflection-pair proof

Translation and multiplication of indices by the inverse of `d` preserve the
exact Gaussian sum and permute the syndrome coordinates, so it suffices to
take `b_0=b_1=1` and all other `b_j=0`.

Exact sum one forces exactly one negative imaginary position among `0,1` and
exactly `m-1` negative real positions among the other `2m-1` positions.  Put

```text
a_j = sigma_j + sigma_(j+1).
```

A direct expansion of the syndrome gives

```text
t_s = a_(-s) + a_s.
```

Now introduce reflection-pair parities around the midpoint of the two marked
positions:

```text
p_s = sigma_(-s) + sigma_(1+s),   0 <= s <= m.
```

Then

```text
t_s = p_(s-1) + p_s.                                        (3)
```

The imaginary constraint gives `p_0=1`.  At `s=m`, the two reflected
positions coincide, so `p_m=0`.  Therefore (3) is consistent exactly when
`sum_s t_s=1`, and every such syndrome uniquely determines
`p_1,...,p_(m-1)`.

For `1<=s<=m-1`, the positions `-s` and `1+s` form disjoint real-position
pairs.  If `p_s=1`, that pair contains exactly one negative sign and has two
assignments.  If `p_s=0`, it contributes either zero or two negative signs.
One real position, `m+1`, is fixed by the reflection and is free.  If `h` of
the pairs have parity one and `z=m-1-h` have parity zero, the real-weight
generating polynomial is

```text
2^h x^h (1+x^2)^z (1+x).
```

Its coefficient at the required real weight `m-1` is

```text
2^h binom(z,floor(z/2)).
```

Finally, the marked imaginary pair has two assignments, proving (2).

Because every odd-parity vector occurs, the syndrome map has full rank `m`
(the odd-parity vectors span `F_2^m`).  Thus (1) is precisely the full parity
slice inside the image.  As an independent algebraic cross-check, in
`F_2[x]/(x^n-1)` the axis is a monomial times `1+x^d`; it is nonzero at every
nontrivial `n`-th root because `gcd(d,n)=1`, so the odd-length CRT rank formula
also gives rank `m`.

Summing (2) over all allowed syndromes also gives the identity

```text
sum_{h=0}^{m-1} binom(m-1,h) 2^(h+1)
  binom(m-1-h,floor((m-1-h)/2))
= 2 binom(2m-1,m-1),                                         (4)
```

with the right side counting the exact-sum-one sign words directly.

## Exact independent verification

`verify_weight_two.py` uses only the Python standard library and arbitrary-
precision integers.  For every odd length from 3 through 21 it enumerates the
exact fixed-cardinality sign words, evaluates `D_b` from its defining double
sum, and compares every fiber—not only aggregate counts—with (2).  It also
checks the coordinate permutation reducing every unit separation `d` to the
adjacent case on every binary basis word.  The compact expected output records
a digest of all 2,046 fiber records.

This computation validates the implementation and indexing conventions.  The
general theorem follows from the reflection proof, not from the tested range.

## Reproduction

Tested with Python 3.12.12 on arm64 macOS; there are no third-party
dependencies.

```sh
python3 verify_weight_two.py
python3 verify_weight_two.py > /tmp/weight-two-output.txt
diff -u expected_output.txt /tmp/weight-two-output.txt
shasum -a 256 -c SHA256SUMS
```

## Context, novelty, and scope

The surrounding sequence-design context is Kotsireas--Winterhof,
[*Quaternary Legendre Pairs*](https://arxiv.org/abs/2212.10953),
Kotsireas--Koutschan--Winterhof,
[*Quaternary Legendre Pairs II*](https://arxiv.org/abs/2408.16318), and
Jedwab--Pender,
[*Two constructions of quaternary Legendre pairs of even
length*](https://arxiv.org/abs/2408.08472).

The group-algebra factorization and reciprocal-orbit language are standard;
the reflection-pair fiber formula (2), its positivity consequence, and its
application to this exact-sum syndrome map were not found in targeted graph or
primary-literature searches.  This is a search-relative novelty assessment,
not a historical-priority claim.

The result proves the sum-one conjecture for every unit-separated weight-two
axis at every odd length, including every weight-two axis at odd prime length.
It does not prove positivity for higher axis weights, nonunit separations at
composite length, or all odd-length axes, and it does not settle QLP-42.
