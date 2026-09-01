# Fourth-order rank classification in the QLP-42 `q=41` branch

## Theorem

Continue the exact `q=41` setup from the third-order axis theorem.  Thus
`H_A(0)=0`, the axes of the other 20 entries of `H_A` are reflected, and
`H_B` is a length-21 word of Gaussian units.  Write `a in F_2^10` for the
reflected `A` axes and `b in F_2^21` for the `B` axes.  The third-order
equations uniquely prescribe the ten reflected sign XORs in each of `H_A`
and `S_A`, while leaving one sign per reflected pair free.

Put `pi=1+i`.  The complete lift of these equations modulo `pi^4` eliminates
exactly

```text
429,978,992 of 2,147,483,648 labeled axis pairs,
20,491,184 of   102,277,120 B-rotation axis orbits.
```

Consequently the exact survivor counts are

```text
1,717,504,656 labeled axis pairs,
   81,785,936 B-rotation axis orbits.
```

The classification is controlled by a binary linear map depending only on
`b`.  For `sigma in F_2^21`, define

```text
D_b(sigma)(s) = sum_j (sigma_j+sigma_(j+s))
                        (b_j+b_(j+s)),       1 <= s <= 10.       (1)
```

Equivalently, column `j` of `D_b` has coordinate `s` equal to
`b_(j+s)+b_(j-s)`.  Let `U_H(a)` and `U_S(a)` be the images in `F_2^10` of
flipping the ten free reflected-pair signs of `H_A` and `S_A`.  After the
third-order XORs are inserted, the remaining fourth-order residuals are
vectors `r_H(a,b)` and `r_S(a,b,c)`, where `c` is one of the four possible
unit phases at the exceptional `S_A(0)=pi*c` cell.  A pair `(a,b)` lifts
modulo `pi^4` if and only if

```text
r_H(a,b)   is in U_H(a) + image(D_b),
r_S(a,b,c) is in U_S(a) + image(D_b) for at least one c.          (2)
```

The `H` and `S` sign variables are independent in every quarter-turn local
state, so the two memberships in (2) may be solved independently.  The
exact rank strata are:

| rank of `D_b` | `b` words | `b` rotation orbits | possible labeled pairs | surviving labeled pairs | surviving axis orbits |
|---:|---:|---:|---:|---:|---:|
| 0  | 2         | 2      | 2,048         | 0             | 0 |
| 1  | 6         | 2      | 6,144         | 0             | 0 |
| 3  | 126       | 18     | 129,024       | 0             | 0 |
| 4  | 378       | 18     | 387,072       | 672           | 32 |
| 6  | 8,190     | 390    | 8,386,560     | 43,344        | 2,064 |
| 7  | 24,570    | 1,170  | 25,159,680    | 368,928       | 17,568 |
| 9  | 515,970   | 24,570 | 528,353,280   | 132,031,872   | 6,287,232 |
| 10 | 1,547,910 | 73,710 | 1,585,059,840 | 1,585,059,840 | 75,479,040 |

In particular, every rank-10 pair lifts, while ranks at most three are
completely excluded.  The finer machine-readable table is `rank_table.tsv`.

## Fourth-order expansion

Encode a Gaussian unit by `z=(-1)^sigma i^beta`.  Direct expansion gives

```text
z = 1 + beta*pi + (sigma+beta)*pi^2
      + (sigma+beta+sigma*beta)*pi^3       (mod pi^4).
```

For a length-21 unit word `W`, put

```text
c_beta(s) = sum_j beta_j beta_(j+s),
E_beta(s) = wt(beta)+c_beta(s),
D_beta(s) = sum_j (sigma_j+sigma_(j+s))
                  (beta_j+beta_(j+s)).
```

Then

```text
PAF(W,s) = 1 + E_beta(s)*pi^2
             + (E_beta(s)+D_beta(s))*pi^3       (mod pi^4).       (3)
```

The extra `E_beta` in the third coefficient is an easy-to-miss integral
carry: the number of axis transitions is even, and its half-count converts
the cancelled linear `pi` terms into a `pi^3` term.  The verifier checks
(3) exhaustively on all `4^5` unit words of odd length five and both
independent shifts, in addition to direct length-21 checks.

Flipping signs changes (3) linearly.  For family `B` its ten-bit image is
exactly (1).  For the reflected `A` words it gives `U_H(a)` and `U_S(a)`.
The certificate tests (2) through orthogonal complements: a vector `r`
belongs to `U+V` precisely when it pairs trivially with `U^perp intersect
V^perp`.  This turns the complete enumeration into exact ten-bit linear
algebra.

## Reproduction and trust boundary

Run:

```bash
python3 verify_q41_fourth_order_rank.py
```

The standard-library-only certificate:

- reconstructs the eight quarter-turn local states and verifies independent
  `S,H` signs;
- checks all four unit expansions modulo `pi^4`;
- exhaustively verifies (3) in 2,048 exact Gaussian PAF cases;
- constructs the affine `A` residual systems for all `2^10` reflected axes;
- enumerates all `2^21` words `b`, grouped into exactly 99,880 cyclic
  rotation orbits, and computes the exact rank and image of every `D_b`;
- compares the affine formula against 200 deterministic direct length-21
  Gaussian computations;
- verifies every row of `rank_table.tsv` and the displayed totals.

All Gaussian arithmetic and all linear algebra are exact.  There is no
floating point, SAT status, randomized proof step, or heuristic search in
the classification.  The deterministic pseudorandom sample is only an
independent audit of formulas already used exhaustively.

This result classifies the fourth-order autocorrelation residue lift of all
third-order axis pairs.  It does **not** impose the four exact global sum
equations or the full integer autocorrelations, and it does not assert that
any survivor extends to a QLP-42 solution.  Intersecting these fourth-order
sign systems with the previously classified exact-sum layer is a separate
next step.

Primary context: Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; and Jedwab--Pender,
*Two constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>.  A targeted primary-source and current
Discovery Net search found no matching fourth-order `q=41` rank
classification.  This is a scoped novelty assessment, not a priority claim.
