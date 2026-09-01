# Complete CRT rank spectrum for odd cyclic syndrome maps

This directory proves a structural theorem for every odd length, extending
the previously certified length-21 spectrum and prime-23 dichotomy.  It gives
the rank of the binary cyclic syndrome map for each individual axis word and
a closed product formula counting all axis words of every possible rank.

## Setup

Let `n=2m+1` be odd.  For binary words `b,sigma in F_2^n`, with subscripts
read modulo `n`, define

```text
D_b(sigma)_s = sum_j (sigma_j + sigma_{j+s})(b_j + b_{j+s}),
1 <= s <= m.
```

Write `R=F_2[x]/(x^n-1)` and let `u -> u*` be reciprocity, induced by
`x -> x^{-1}`.  Because `n` is odd, `x^n-1` is square-free.  Apart from the
factor `x+1`, partition its monic irreducible factors into reciprocal orbits:

```text
reciprocal pairs {f,f*}, with deg(f)=d;
self-reciprocal factors f=f*, with deg(f)=d.
```

Every nontrivial self-reciprocal irreducible factor has even degree.  For an
axis word `b`, denote its residue modulo `f` by `b_f`.

## Rank theorem

For every binary axis word `b`,

```text
rank(D_b)
 = sum_{reciprocal pairs {f,f*}}
       d * 1[(b_f,b_f*) != (0,0)]
   + sum_{nontrivial self-reciprocal f}
       (d/2) * 1[b_f != 0].                                  (1)
```

This is an exact per-axis formula, not an asymptotic statement or a
computation limited to the tested lengths.

### Proof

Represent words by elements of `R` and set `C=sigma b*`.  Direct coefficient
comparison gives

```text
D_b(sigma)_s = C_s + C_{-s}.
```

Since `n` is odd, the nonzero indices form the pairs `{s,-s}`.  Therefore

```text
D_b(sigma)=0  if and only if  C=C*.                           (2)
```

The square-free Chinese remainder decomposition of `R` makes the constraints
in (2) independent across reciprocal-factor orbits.

On a reciprocal pair of degree `d`, the corresponding component is `K x K`,
where `K=F_(2^d)`, and reciprocity exchanges the two fields through an
isomorphism.  If both components of `b` vanish, (2) imposes no constraint.
Otherwise, multiplication by the nonzero component or components shows that
the fixed-point condition has binary codimension `d`: with two nonzero
components it is one field equation between two free field variables, and
with exactly one it forces one field variable to zero.

On a nontrivial self-reciprocal factor of degree `d`, reciprocity is the
nonidentity order-two automorphism of `K=F_(2^d)`.  Its fixed field is
`F_(2^(d/2))`.  A zero component of `b` imposes no constraint; a nonzero
component makes multiplication bijective, so (2) has codimension `d/2`.
The `x+1` component is fixed identically and contributes zero.  Adding these
independent codimensions proves (1).

## Complete rank enumerator

Let

```text
P_n(z) = sum_b z^rank(D_b),
```

where the sum runs over all `2^n` labeled binary axis words.  Formula (1) and
CRT independence immediately give

```text
P_n(z)
 = 2 product_{reciprocal pairs of degree d}
       (1 + (2^(2d)-1) z^d)
     product_{self-reciprocal factors of degree d, f != x+1}
       (1 + (2^d-1) z^(d/2)).                                (3)
```

For even-weight axis words the same enumerator is obtained by deleting the
leading factor `2`.  Indeed, the all-one word is supported only on the
`x+1` CRT component.  Thus complementation `b -> b+1` leaves `D_b` and every
nontrivial CRT component unchanged while exchanging even and odd weight.

Two earlier finite classifications become one-line consequences:

```text
n=21: 2(1+3z)(1+63z^3)(1+4095z^6)
n=23: 2(1+(2^22-1)z^11).
```

The first expands to ranks and labeled counts

```text
0:2, 1:6, 3:126, 4:378, 6:8190, 7:24570,
9:515970, 10:1547910,
```

and the second says that only the two constant length-23 axes have rank zero;
all other `8,388,606` labeled axes have rank 11.

## Exact surjectivity and image-size corollaries

The output space of `D_b` has dimension `m=(n-1)/2`.  The total of all
positive orbit increments in (1) is exactly `m`, because

```text
n-1 = sum_{reciprocal pairs} 2d + sum_{self-reciprocal factors} d.
```

Consequently `D_b` is surjective exactly when `b` is nonzero on every
nontrivial reciprocal-factor orbit.  The numbers of surjective labeled axes
are therefore

```text
all axes:
  2 product_{pairs of degree d}(2^(2d)-1)
    product_{self factors of degree d}(2^d-1),

even axes:
  product_{pairs of degree d}(2^(2d)-1)
    product_{self factors of degree d}(2^d-1).                 (4)
```

At the other extreme, (1) shows that `D_b` has rank zero exactly for the two
constant axes, at every odd length.

The rank enumerator also counts the total number of image points without any
matrix enumeration:

```text
sum_b |image(D_b)| = P_n(2).                                  (5)
```

For even axes the total is `P_n(2)/2`.  In particular:

| length | surjective even axes | total `(b,t)` with even `b`, `t in image(D_b)` |
|---:|---:|---:|
| 21 | 773,955 | 926,456,335 |
| 23 | 4,194,303 | 8,589,932,545 |

For a uniformly random axis, the CRT components are independent.  Thus the
mean rank and variance are also explicit sums of independent Bernoulli
contributions.  A reciprocal pair contributes a rank increment `d` with
probability `1-2^(-2d)`; a self-reciprocal factor contributes `d/2` with
probability `1-2^(-d)`.  This gives exact complexity statistics as well as an
individual-axis classification.

## Factorization-free arithmetic formula

Formula (3) can be computed directly from the divisors of `n`, without
factoring `x^n-1`.  For each divisor `q>1` of `n`, put

```text
o_q = ord_q(2).
```

The primitive `q`-th roots produce `phi(q)/o_q` irreducible factors of degree
`o_q`.  They are self-reciprocal exactly when

```text
2^(o_q/2) = -1 (mod q),                                      (6)
```

which necessarily requires even `o_q`.  If (6) holds, the contribution of
this divisor to the even-axis enumerator is

```text
(1 + (2^o_q-1) z^(o_q/2))^(phi(q)/o_q).                      (7)
```

Otherwise its irreducible factors form reciprocal pairs and contribute

```text
(1 + (2^(2o_q)-1) z^o_q)^(phi(q)/(2o_q)).                    (8)
```

Multiplying (7) or (8) over all `q|n`, `q>1`, gives the complete even-axis
rank enumerator.  The all-axis enumerator is twice this product.

### Exact rank-dichotomy classification

For odd `n>=3`, every nonconstant axis has full rank `(n-1)/2` if and only if

```text
n is prime and either
  ord_n(2) = n-1, or
  ord_n(2) = (n-1)/2 with (n-1)/2 odd.                        (9)
```

Proof: the enumerator has only ranks zero and `(n-1)/2` precisely when there
is one nontrivial reciprocal-factor orbit.  More than one divisor `q>1` gives
more than one orbit, so `n` must be prime.  For prime `n`, a single orbit is
either one self-reciprocal factor of degree `n-1`, giving the first condition,
or one reciprocal pair of degree `(n-1)/2`.  The latter pair is reciprocal
rather than two self-reciprocal factors exactly when its degree is odd,
giving the second condition.  Both conditions plainly produce one orbit.

`verify_arithmetic_formula.py` checks the divisor/order schema against actual
polynomial factorization for every odd length through 23.  It then verifies
the dimension, enumerator total, constant-axis kernel, full-rank coefficient,
and dichotomy criterion for all 499 odd lengths from 3 through 999.  This is
an exact finite audit of the general proof, not the source of the theorem.

## Independent computational certificate

`verify_rank_formula.py` uses only the Python standard library.  It:

1. factors `x^n+1` over `F_2` for every odd `3 <= n <= 23`;
2. classifies reciprocal and self-reciprocal factor orbits;
3. constructs the rank enumerator (3);
4. for every one of the 174,760 labeled axes at odd `n <= 17`, builds the
   binary matrix `D_b` directly and checks its row rank against (1);
5. independently checks `D_b=D_(b+1)` for every such axis; and
6. matches the previously published complete spectra at `n=21` and `n=23`;
   and
7. checks the surjective-axis and total-image-point corollaries at those two
   lengths.

The separate arithmetic checker validates formulas (6)--(9) and records a
SHA-256 digest of all 499 complete even-axis rank spectra in its expected
output.

The exhaustive direct-record stream has SHA-256

```text
55828a93fa8766183891e460f56806acc8e7b4a677e235666ae90934a2b987b4
```

## Reproduction

Tested with Python 3.12.12 on arm64 macOS.

```sh
python3 verify_rank_formula.py
python3 verify_arithmetic_formula.py
python3 verify_rank_formula.py > /tmp/rank-formula-output.txt
diff -u expected_output.txt /tmp/rank-formula-output.txt
python3 verify_arithmetic_formula.py > /tmp/arithmetic-output.txt
diff -u expected_arithmetic_output.txt /tmp/arithmetic-output.txt
shasum -a 256 -c SHA256SUMS
```

## Literature context and scope

The factor-orbit language is standard in the theory of self-reciprocal
factors of `x^n-1`; see Boripan--Jitman--Udomkavanich,
[*Self-Conjugate-Reciprocal Irreducible Monic Factors of
`x^n-1` over Finite Fields*](https://arxiv.org/abs/1804.06138), and
Wu--Yue--Fan,
[*Self-reciprocal and self-conjugate-reciprocal irreducible factors of
`x^n-lambda` over finite fields*](https://arxiv.org/abs/2001.04766).
The present theorem applies that decomposition to the specific cyclic
syndrome maps above.

Targeted graph and primary-source searches found no matching per-axis formula
(1) or full rank enumerator (3).  This is a search-relative novelty
assessment, not a claim of historical priority.  The theorem determines the
linear-algebraic rank obstruction at every odd length.  It does not by itself
prove positivity of exact-sum fibers, the remaining major step in the
sum-one-syndrome program, or settle the surrounding quaternary Legendre-pair
existence problem.
