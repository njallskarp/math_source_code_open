# The complete Schur-positive Lucas `b = 4`, `a = 2` family

## Exact target and status

Let `F_0 = 0`, `F_1 = 1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)
```

in `Z[e1,e2]`, and write `{n choose k}_F` for the associated Lucas
binomial.  The canonical `(a,b)=(2,4)` Lucas--Bergeron--Vessenes
comparison is

```text
D_c = {2c+2 choose 2}_F - {c+4 choose 4}_F,       c >= 4.       (1)
```

Both terms have degree `4c` when `deg(e1)=1` and `deg(e2)=2.  This note
proves

```text
D_c is Schur-positive for every c >= 4.                         (T)
```

The proof first derives an exact all-parameter KOH recurrence and then
proves positivity of its remainder by pairing adjacent layers in the
two-row Schur decomposition.  In fact, the coefficients on
`s_(4c-r,r)` are strictly positive for every `3 <= r <= 2c`.

This is a genuinely Schur-basis reduction.  In particular, `D_4` already
has coefficient `-1` on `e2^8` in `Z[e1,e2]`, so the elementary-positive
mechanism used for `b=3` cannot prove (1).

## The two KOH identities

Homogenize Gaussian polynomials in two variables, and let `tau` be the
involution

```text
tau(e1) = e1,          tau(e2) = -e2.
```

It sends the homogenized `q`-integer `h_(n-1)` to `F_n` and Gaussian
binomials to Lucas binomials.  Applying `tau` to the KOH decompositions for
the two partitions of `2` and the five partitions of `4` gives

```text
{2c+2 choose 2}_F
  = F_(4c+1) + e2^2 {2c choose 2}_F,                         (2)

{c+4 choose 4}_F
  = F_(4c+1)
    + e2^2 F_(c-1) F_(3c-1)
    + e2^4 {2c-2 choose 2}_F
    + e2^6 {c-2 choose 2}_F F_(2c-3)
    + e2^12 {c-2 choose 4}_F.                               (3)
```

For (3), the summands correspond respectively to

```text
(1,1,1,1), (2,1,1), (2,2), (3,1), (4).
```

Indeed, the ordinary KOH summands are

```text
[4c+1]_q,
q^2 [c-1]_q [3c-1]_q,
q^4 Gaussian(2c-2,2),
q^6 Gaussian(c-2,2) [2c-3]_q,
q^12 Gaussian(c-2,4).
```

All five shifts are even, so no sign is lost under `tau`.  Formula (3) is
therefore not an assertion of termwise positivity for the difference (1):
the problem is the cancellation between (2) and (3).

## Six-step recurrence

The width-two identity iterates as

```text
{r+2 choose 2}_F
  = sum_(0 <= j <= floor(r/2)) e2^(2j) F_(2r-4j+1).          (4)
```

Consequently,

```text
e2^2 {2c choose 2}_F - e2^4 {2c-2 choose 2}_F
  = e2^2 F_(4c-3).                                          (5)
```

The Lucas addition identity gives

```text
F_(4c-3) - F_(c-1)F_(3c-1) = e2 F_(c-2)F_(3c-2).            (6)
```

Subtracting (3) from (2), using (5)--(6), and extracting the `(4)` KOH
tail proves the following polynomial identity.

**KOH recurrence.**  For every `c >= 10`,

```text
D_c = e2^12 D_(c-6) + e2^3 R_c,                             (7)
```

where

```text
R_c = F_(c-2)F_(3c-2)
      - e2^3 {c-2 choose 2}_F F_(2c-3)
      - e2^9 {2c-10 choose 2}_F.                            (8)
```

Multiplication by `e2^j=s_(j,j)` merely shifts both parts of a two-row
Schur function by `j`.  Thus (7) is already a Schur recurrence once the
coefficients of `R_c` are made explicit.

## Ballot-Delannoy Schur kernel

Define

```text
ell(n,r) = [s_(n-r,r)] F_(n+1),
```

with value zero if `r < 0` or `2r > n`.  Let

```text
Del(a,b) = sum_(0 <= j <= min(a,b)) 2^j binom(a,j)binom(b,j).
```

Then

```text
ell(n,r) = Del(n-r,r) - Del(n-r+1,r-1).                     (9)
```

Equivalently, the entire kernel is generated without subtraction by

```text
ell(0,0) = 1,
ell(n,r) = ell(n-1,r) + ell(n-1,r-1) + ell(n-2,r-1),         (10)
```

for `0 <= 2r <= n`, with out-of-range terms zero.

To see (9), expand

```text
F_(n+1) = sum_j binom(n-j,j) e1^(n-2j)e2^j.
```

The coefficient of `x^(n-r)y^r` after `e1=x+y`, `e2=xy` is the
Delannoy number `Del(n-r,r)`.  In two variables a Schur coefficient is
the difference of two consecutive monomial coefficients, which gives
(9).  Recurrence (10) also follows directly from the Lucas recurrence and
the one-box Pieri rule.

For later use define the product kernel

```text
P(u,v;r) = [s_(u+v-r,r)] F_(u+1)F_(v+1).                   (11)
```

The two-row Pieri rule `h_p h_q = sum_(0<=k<=min(p,q))
s_(p+q-k,k)` makes it completely explicit:

```text
P(u,v;r)
  = sum_(i,j) ell(u,i)ell(v,j)
      * 1[0 <= r-i-j <= min(u-2i,v-2j)].                    (12)
```

There is also an independent triangular description.  Put

```text
H_c(q) = Gaussian(c+4,4) - Gaussian(2c+2,2),
```

and let `h(c,i)` be the coefficient of `s_(4c-i,i)` in its homogeneous
two-variable lift (equivalently, the `i`th first difference of the
coefficient sequence of `H_c(q)`).  Since `D_c = -tau(H_c)`, Bergeron's
Lucas image of a two-row Schur function gives

```text
d(c,r) = sum_(0 <= i <= r)
           (-1)^(i+1) h(c,i) ell(4c-2i,r-i).                (12a)
```

This alternating formula and the positive-remainder recurrence below are
two exact constructions of the same Schur coefficients.

## Explicit all-parameter Schur recurrence

Write

```text
D_c = sum_(0 <= r <= 2c) d(c,r) s_(4c-r,r),
R_c = sum_(0 <= u <= 2c-3) rho(c,u) s_(4c-6-u,u).
```

Expanding the two width-two binomials in (8) by (4), and applying
(9)--(12), gives

```text
rho(c,u)
  = P(c-3,3c-3;u)
    - sum_(0 <= j <= floor((c-4)/2))
        P(2c-8-4j,2c-4;u-3-2j)
    - sum_(0 <= j <= c-6)
        ell(4c-24-4j,u-9-2j).                               (13)
```

Every out-of-range `ell` or `P` is zero.  Combining (7) and (13) yields
the promised coefficient recurrence

```text
d(c,r) = d(c-6,r-12) + rho(c,r-3),                          (14)
```

again with out-of-range coefficients zero.

Equations (9), (12), (13), and (14) are an explicit finite all-parameter
Schur expansion algorithm involving only binomial coefficients, addition,
and multiplication.  The next section proves the key inequality

```text
rho(c,u) >= 0 for c >= 10 and 0 <= u <= 2c-3.               (15)
```

and, more strongly, proves `rho(c,u) >= 1` throughout this range.

## Positive adjacent-layer pairing

Apply `tau` to (8) and put `K_c=tau(R_c)`.  Since both negative terms in
(8) have odd `e2`-degree, their signs reverse:

```text
K_c = h_(c-3)h_(3c-3)
      + e2^3 Gaussian(c-2,2) h_(2c-4)
      + e2^9 Gaussian(2c-10,2).                             (16)
```

Thus `K_c` is Schur-positive in a particularly explicit way.  Write

```text
K_c = sum_(0 <= r <= 2c-3) k(c,r)e2^r h_(4c-6-2r).
```

The width-two expansion and the Pieri rule in (16) give the interval-count
formula

```text
k(c,r)
  = 1[0 <= r <= c-3]
    + number of j such that
        0 <= j <= floor((c-4)/2) and
        3+2j <= r <= 2c-5-2j
    + 1[r is odd and 9 <= r <= 2c-3].                       (17)
```

Because `tau(e2^r h_n)=(-1)^r e2^r F_(n+1)`, this becomes

```text
R_c = sum_r (-1)^r k(c,r)e2^r F_(4c-5-2r).                 (18)
```

We need one uniform character inequality.  For every `m >= 3`,

```text
F_m - 2e2 F_(m-2) is Schur-positive.                        (19)
```

Indeed, its coefficient on `s_(m-1-r,r)` is, by (10),

```text
ell(m-2,r) + ell(m-3,r-2) + ell(m-4,r-2),
```

which is nonnegative.  Consequently, whenever `0 <= b <= 2a`,

```text
a F_m - b e2 F_(m-2)
  = a(F_m-2e2 F_(m-2)) + (2a-b)e2 F_(m-2)                  (20)
```

is Schur-positive.

It remains only to check that adjacent coefficients in (17) satisfy this
simple bound.  For `0 <= j <= c-2`, formula (17) is equivalently

```text
k(c,2j)
  = 1[2j <= c-3] + max(0,min(j-1,c-j-2)),

k(c,2j+1)
  = 1[2j+1 <= c-3] + max(0,min(j,c-j-2))
    + 1[4 <= j <= c-2].                                    (21)
```

For `0 <= j <= c-3`, these formulas give

```text
k(c,2j+1) <= 2 k(c,2j).                                    (22)
```

For completeness: the pairs for `j=0,1` are `(1,1)` and `(1,2)`.
When `2 <= j <= c-4`, the odd entry is at most the even entry plus two,
while the even entry is at least two.  The final such pair, `j=c-3`, is
again `(1,2)`.  This proves (22) without an asymptotic or omitted boundary
case.

Pair the terms of (18) at indices `2j,2j+1`.  Equations (20)--(22) prove
Schur positivity of every pair through `j=c-4`.  The pair at `j=c-3`
must also absorb the final nonzero odd layer, since (21) ends in

```text
(k(c,2c-6),k(c,2c-5),k(c,2c-4),k(c,2c-3)) = (1,2,0,1).
```

Its complete contribution is the fixed shifted polynomial

```text
e2^(2c-6) (F_7 - 2e2 F_5 - e2^3 F_1)
  = e2^(2c-6) (s_6 + 8s_(5,1) + 18s_(4,2) + 9s_(3,3)),     (23)
```

which is Schur-positive.  This proves (15).  Moreover, the first pair is
`F_(4c-5)-e2 F_(4c-7)=e1 F_(4c-6)`, whose coefficient on every allowable
two-row shape is positive.  Hence `rho(c,u) >= 1` for all `c >= 10` and
all `0 <= u <= 2c-3`.

Finally, direct Schur coefficient arrays for the six bases
`D_4,...,D_9` are listed below.  Each list runs from `r=0` through `r=2c`:

```text
c=4: [0,0,0,1,17,112,359,562,298]
c=5: [0,0,0,1,25,265,1553,5489,11881,14776,7072]
c=6: [0,0,0,1,33,481,4080,22331,82570,209273,357921,382208,169687]
c=7: [0,0,0,1,41,761,8464,62932,330380,1260272,3536152,7277787,
      10713402,10379464,4392776]
c=8: [0,0,0,1,49,1105,15216,143148,975355,4978186,19411857,58412092,
      135830579,241830481,320163336,289330066,118298681]
c=9: [0,0,0,1,57,1513,24848,282948,2372843,15193467,75994995,
      301241491,954191962,2422106612,4911365195,7857954618,
      9615754202,8250609000,3287685543]
```

The recurrence (7), the strict positivity of `R_c`, and these bases prove
the theorem (T).

## Independent exact verification

Three checkers exercise different parts of the argument.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_recurrence.py --max-c 60
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_schur_kernel.py --max-c 300 --explicit-max-c 50
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b4/a2/verify_pairing.py --max-c 300
```

`verify_recurrence.py` uses sparse integer dictionaries in `Z[e1,e2]`,
constructs Lucas binomials with the Sagan--Savage recurrence, verifies
(2)--(8) by exact polynomial equality, converts independently to the
two-row Schur basis, and checks signs.

`verify_schur_kernel.py` never constructs a Lucas binomial in
`Z[e1,e2]`.  It constructs ordinary Gaussian coefficients by `q`-Pascal
recurrence, applies the triangular Schur/Lucas involution exactly, builds
the ballot-Delannoy and Pieri kernels, and checks (9), (13), and (14).
It performs the exact counterexample search through the requested bound.

`verify_pairing.py` independently obtains `K_c` from ordinary Gaussian
polynomials, checks the interval formula (17), reconstructs every Schur
coefficient using the nonnegative adjacent-pair decomposition, and checks
the six stated base arrays.

The written identities and inequalities prove the result for every
parameter; the finite checks audit formulas, indices, and boundary cases.
There is no floating point, randomness, modular reconstruction, or solver.

## Primary context and novelty boundary

- Francois Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  records the Lucas Schur-positivity conjecture and bounded verification:
  https://arxiv.org/abs/2608.30979
- Bruce Sagan and Carla Savage, *Combinatorial interpretations of binomial
  coefficient analogues related to Lucas sequences*, supplies Lucas-binomial
  positivity and recurrence machinery: https://arxiv.org/abs/0911.3159
- Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, proves the ordinary Gaussian `a=2` case and states the KOH
  formula used here: https://arxiv.org/abs/1709.06187

Targeted primary-source and Discovery Net searches found no Lucas `b=4`
Schur recurrence or proof.  The novelty statement is therefore limited to
the searched sources and is not a historical-priority claim.

The earlier `b=3` Lucas lemma has since received two independent accepting
reviews on Discovery Net.  Nothing here enlarges that lemma's scope.
