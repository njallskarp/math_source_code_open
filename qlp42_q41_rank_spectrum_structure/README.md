# Group-algebra explanation of the QLP-42 `q=41` rank spectrum

## Structural theorem

Let `b in F_2^21` be the family-`B` axis word in the fourth-order `q=41`
QLP-42 reduction, and define

```text
D_b(sigma)(s) = sum_j (sigma_j+sigma_(j+s))(b_j+b_(j+s)),
                                                        1 <= s <= 10.
```

The previously enumerated rank spectrum

```text
0, 1, 3, 4, 6, 7, 9, 10
```

and all of its word counts have a complete group-algebra explanation.  If
`epsilon,delta,eta` are binary indicators described below, then

```text
rank(D_b) = epsilon + 3*delta + 6*eta.                    (1)
```

Consequently the ranks and counts are forced to be

| rank | length-21 axis words | cyclic rotation orbits |
|---:|---:|---:|
| 0  | 2         | 2 |
| 1  | 6         | 2 |
| 3  | 126       | 18 |
| 4  | 378       | 18 |
| 6  | 8,190     | 390 |
| 7  | 24,570    | 1,170 |
| 9  | 515,970   | 24,570 |
| 10 | 1,547,910 | 73,710 |

Thus the rank table in the fourth-order classification is theoretical, not
an unexplained output of the `2^21` enumeration.

## Polynomial model

Work in

```text
R = F_2[x]/(x^21-1) = F_2[x]/(x^21+1)
```

and let star be the involution `x -> x^(-1)`.  Identify a word with its
polynomial.  The coefficient of `x^s` in

```text
L_b(sigma) = b*sigma^star + b^star*sigma                  (2)
```

is

```text
sum_j sigma_j b_(j+s) + sum_j sigma_(j+s)b_j
 = sum_j (sigma_j+sigma_(j+s))(b_j+b_(j+s)),
```

because the two diagonal terms cancel in characteristic two.  The constant
coefficient of (2) is zero and the coefficients at `s` and `-s` agree, so
its ten independent coefficients are exactly `D_b(sigma)`.

Over `F_2`, the square-free factorization is

```text
x^21+1 =
 (x+1)
 (x^2+x+1)
 (x^3+x+1)(x^3+x^2+1)
 (x^6+x^4+x^2+x+1)(x^6+x^5+x^4+x^2+1).                 (3)
```

The first two factors are self-reciprocal.  The degree-three factors form a
reciprocal pair, as do the degree-six factors.  The Chinese remainder
theorem therefore decomposes (2) into four independent blocks.

- On the `F_2` block from `x+1`, star is trivial and
  `b*sigma+b*sigma=0`.  This block always has rank zero; the coordinate of
  `b` supplies the global factor two in every word count.
- On the `F_4` block, star is the Frobenius `t -> t^2`, and
  `L_b(s)=b*s^2+b^2*s`.  It has rank zero for `b=0` and rank one for each of
  the three nonzero values.  This is the contribution `epsilon`.
- On a reciprocal pair `K x K` of factor degree `d`, identify the two fields
  through reciprocity.  Star swaps the components and the image coordinate
  is equivalent to
  `L_(u,v)(p,q)=u*q+v*p`.  The map is zero at `(u,v)=(0,0)` and otherwise
  surjects onto `K`, contributing rank `d`.  For `d=3` there are 63 nonzero
  pairs, giving `3*delta`; for `d=6` there are 4,095, giving `6*eta`.

Ranks add across the CRT product, proving (1).  The number of words with a
given triple is therefore

```text
2 * (1 or 3) * (1 or 63) * (1 or 4095),                  (4)
```

and expanding (4) gives the eight displayed word counts.

## Rotation orbits without necklace traversal

Burnside's lemma needs only the divisors of 21.  Of the 20 nonidentity
rotations, 12 have fixed words of period one, six have fixed words of period
three, and two have fixed words of period seven.  Formula (1) gives the
fixed-word rank distributions

```text
period 1: rank 0 -> 2,
period 3: rank 0 -> 2, rank 1 -> 6,
period 7: rank 0 -> 2, rank 3 -> 126.
```

Thus for every rank `r`,

```text
orbits_r = (words_r + 12*fixed_1(r)
                    + 6*fixed_3(r) + 2*fixed_7(r))/21,
```

which gives the orbit column above.  This also explains why all higher-rank
words have full rotation orbit size 21.

## Exact certificate

Run:

```bash
python3 verify_q41_rank_spectrum.py
```

The standard-library-only verifier:

- multiplies the six factors in (3), proves each factor irreducible using
  Frobenius/gcd tests, and verifies the reciprocal pairing;
- exhausts the four `F_4` values, all 64 values in the paired `F_8` block,
  and all 4,096 values in the paired `F_64` block, reconstructing the local
  rank distributions `1+3`, `1+63`, and `1+4095`;
- enumerates all `2^21` words by their CRT zero/nonzero indicators and checks
  the product counts in (4);
- directly compares the original ten-by-21 binary matrix rank against (1)
  on 65,048 deterministic words, including boundary words;
- derives the period-one, period-three, and period-seven fixed distributions
  and verifies `rank_orbit_table.tsv` through Burnside's lemma.

No floating point, external algebra package, SAT/SMT result, randomized proof
step, or heuristic claim enters the certificate.  The direct sample is an
additional audit; the complete proof and counts come from the exact CRT
decomposition and exhaustive finite-field block checks.

## Scope and relevance

This lemma explains the rank spectrum of the fourth-order sign map.  It does
not by itself decide which axis pairs satisfy the affine residuals, exact
Gaussian sums, or full autocorrelations.  Combined with the exact
multiplicity theorem, it shows that the possible lift multiplicities are
forced by the three reciprocal CRT blocks.  It also gives a natural basis
for the next exact-sum sieve: kernel constraints can be organized blockwise
over `F_4`, paired `F_8`, and paired `F_64` instead of treated as opaque
ten-bit matrices.

Primary context: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications* (arXiv:1302.0571);
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*
(arXiv:2408.16318); Kotsireas--Winterhof, *Quaternary Legendre Pairs*
(arXiv:2212.10953); and Jedwab--Pender, *Two constructions of quaternary
Legendre pairs of even length* (arXiv:2408.08472).  A targeted primary-source
and current-graph search found no matching structural rank decomposition;
apparent novelty is relative to that search, not a priority claim.
