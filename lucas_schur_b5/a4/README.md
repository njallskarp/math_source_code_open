# The canonical Lucas `(a,b)=(4,5)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)
```

in `Z[e1,e2]`, and let `{n choose r}_F` be the associated Lucas
binomial.  The canonical `(a,b)=(4,5)` comparison is

```text
G_k = {5k+4 choose 4}_F - {4k+5 choose 5}_F,       k >= 2.       (1)
```

The orientation is the conjecture's forced sign: `(-1)^(a+1)=-1`.
Both terms have weighted degree `20k`, where `deg(e1)=1` and
`deg(e2)=2`.

**Theorem.** For every `k>=2`, `G_k` is Schur-positive in two variables.
More precisely,

```text
[s_(20k-r,r)]G_k = 0       for 0 <= r <= 4,
[s_(20k-r,r)]G_k > 0       for 5 <= r <= 10k.       (2)
```

This proves the complete canonical `(a,b)=(4,5)` family.  The proof is
an exact Schur-layer argument: a lower-half Gaussian product expansion,
restricted-partition quasipolynomials, and the two-row Lucas kernel
reduce the theorem to 88 affine cells.  Exact rational Bernstein
certificates prove all of those cells at once.

## Gaussian Schur layers

Define the ordinary Gaussian difference in the opposite orientation to
(1):

```text
J_k(q) = Gaussian(4k+5,5) - Gaussian(5k+4,4).               (3)
```

If its homogeneous two-variable lift has expansion

```text
Jhat_k = sum_(0 <= i <= 10k) g_k(i) s_(20k-i,i)
       = sum_i g_k(i) e2^i h_(20k-2i),                      (4)
```

then symmetry of degree `20k` gives

```text
g_k(i) = [q^i](1-q)J_k(q),                  0 <= i <= 10k.  (5)
```

Let, with value zero on negative arguments,

```text
P(n) = #{(a,b,c,d) in N^4 : 2a+3b+4c+5d=n},
Q(n) = #{(a,b,c)   in N^3 : 2a+3b+4c=n}.                   (6)
```

The Gaussian product formula says

```text
(1-q)J_k(q)
 = product_(nu=1..5)(1-q^(4k+nu)) / product_(r=2..5)(1-q^r)
   - product_(nu=1..4)(1-q^(5k+nu)) / product_(r=2..4)(1-q^r).  (7)
```

The two denominator series obey `P(n)-Q(n)=P(n-5)`.  Through degree
`10k`, at most two nonconstant factors from the first numerator can
occur, because its three smallest exponents sum to `12k+6>10k`.
At most one from the second numerator can occur, because its two
smallest exponents sum to `10k+3>10k`.  Consequently (7) gives the exact
all-parameter Schur-layer formula

```text
g_k(i) = P(i-5)
         - sum_(nu=1..5) P(i-4k-nu)
         + sum_(1<=mu<nu<=5) P(i-8k-mu-nu)
         + sum_(nu=1..4) Q(i-5k-nu),          0 <= i <= 10k. (8)
```

The pair term in (8) is the new feature at width five: it begins inside
the lower half and cannot be discarded as it was at width four.

## Parity reduction and quasipolynomials

Define

```text
T(n) = #{(a,b,c,d) in N^4 : a+2b+3c+5d=n},
R(n) = #{(a,b,c)   in N^3 : a+2b+3c=n},                    (9)
```

again with value zero for `n<0`.  Splitting the parity of the numbers of
parts of sizes three and five in `P` gives

```text
P(2n)   = T(n)+T(n-4),
P(2n+1) = T(n-1)+T(n-2).                                  (10)
```

Indeed, an even total has the two odd-part multiplicities either both
even or both odd; in the latter case removing one part of each size
removes eight.  An odd total removes either one part of size three or
one part of size five.  Similarly,

```text
Q(2n)=R(n),              Q(2n+1)=R(n-1).                  (11)
```

Both functions in (9) have especially small exact quasipolynomials:

```text
T(n) = n^3/180 + 11n^2/120 + 9n/20 + epsilon_(n mod 30),
R(n) = (n^2+6n)/12 + eta_(n mod 6).                        (12)
```

In order of residues beginning at zero, the numerators of the periodic
terms are

```text
360 epsilon =
  360,163,248,243,136,275,288,163,248,171,
  280,203,288,163,176,315,208,203,288, 91,
  320,243,208,203,216,235,248,243,208,131;

12 eta = 12,5,8,9,8,5.                                   (13)
```

Thus

```text
91/360 <= epsilon_r <= 1,          5/12 <= eta_r <= 1.     (14)
```

These formulas are not inferred from interpolation.  The symbolic
checker sums each of the 30 and six residue-class polynomials using the
closed rational series for `sum m^d z^m`, `0<=d<=3`, and verifies in
`QQ(z)` that the results are exactly

```text
1/((1-z)(1-z^2)(1-z^3)(1-z^5)),
1/((1-z)(1-z^2)(1-z^3)),                                  (15)
```

respectively.  This proves (12)--(13) for every `n>=0`.

## Exact adjacent-layer formulas

Set

```text
A_j = g_k(2j+1),              C_j = 2g_k(2j+1)-g_k(2j+2).  (16)
```

The key claim is

```text
A_j >= 0 and C_j >= 0                 for 0 <= j < 5k.     (17)
```

Here is a compact complete specification of (16).  For a coefficient
vector `p=[p_a,...,p_b]`, write

```text
X(alpha;p,a:b) = sum_(s=a..b) p_s X(j-alpha*t-s),           (18)
```

where `X` is `T` or `R`, and every negative argument is zero.  Both
parities have the common base terms

```text
A_base = T(j-2)+T(j-6),
C_base = 2T(j-2)+2T(j-6)-T(j-3)-T(j-4).                    (19)
```

For `k=2t`, formulas (8), (10), and (11) give

```text
A = A_base
    -T(4; [1,1,2,2,2,1,1], 0:6)
    +R(5; [1,1,1,1],         0:3)
    +T(8; [1,2,3,4,4,3,2,1], 1:8),

C = C_base
    -T(4; [1,0,2,2,2,1,2], 0:6)
    +R(5; [1,0,1,2],         0:3)
    +T(8; [1,1,2,4,4,3,3,2], 1:8).                        (20)
```

For `k=2t+1`, they give

```text
A = A_base
    -T(4; [1,1,2,2,2,1,1], 2:8)
    +R(5; [1,2,1],           3:5)
    +T(8; [1,2,3,4,4,3,2,1], 5:12),

C = C_base
    -T(4; [1,0,2,2,2,1,2], 2:8)
    +R(5; [-1,1,3,1],        2:5)
    +T(8; [1,1,2,4,4,3,3,2], 5:12).                       (21)
```

The vector entries in (20)--(21) are ordered by the indicated support.
These identities are literal reorganizations of (8), not estimates.

## Complete affine-cell certificate

For `t>=7`, every translate in (19)--(21) activates at an affine
boundary `j=alpha*t+s`.  Include the domain boundaries

```text
0 <= j <= 10t-1       when k=2t,
0 <= j <= 10t+4       when k=2t+1.                         (22)
```

Sorting all activation boundaries partitions the four cases

```text
(even k,A), (even k,C), (odd k,A), (odd k,C)
```

into `22,22,21,23` cells, respectively: 88 cells in total.  The checker
verifies symbolically that this order is stable and every cell is
nonempty for all `t>=7`; hence the cells cover (22) without gaps or
overlaps.

On one cell `L(t)<=j<=U(t)`, the active terms in (20) or (21) are fixed.
Replace each active `T` and `R` by the polynomial part in (12).  For a
positive translate use the lower periodic bound in (14), and for a
negative translate use the upper bound.  This produces a rigorous cubic
lower bound `B(t,j)` for `A_j` or `C_j`.

Put

```text
t=7+x,                    j=L(t)+(U(t)-L(t))z,
x>=0,                     0<=z<=1.                         (23)
```

Write the resulting cubic in the degree-three Bernstein basis:

```text
B = sum_(r=0..3) b_r(x) binom(3,r) z^r(1-z)^(3-r).         (24)
```

Exact expansion in `QQ[x,z]` proves that all 352 coefficient
polynomials `b_r(x)` lie in `QQ_+[x]`.  Every Bernstein basis element is
nonnegative on `[0,1]`, so (24) proves (17) for both parities and every
`t>=7`.

The cases not covered by (23) are exactly `2<=k<=14`.  Direct evaluation
of the integer formula (8) verifies (17) for every pair in those bases.
This completes the universal proof of (17).  The canonical JSON record
of the 88 cell bounds and 352 Bernstein polynomials has SHA-256

```text
f5f0756fce46c6c69c319a5895369ed15fd5a1cd14c7e36a3052250c9a8a13a4. (25)
```

Run `verify_symbolic.py --show-certificate` to emit that record.  The
default run reconstructs it, checks every rational coefficient and the
digest, and verifies (15) and all finite bases.

## Lucas image and positive pairing

Let `tau(e1)=e1`, `tau(e2)=-e2`.  It takes `h_n` to `F_(n+1)` and
homogeneous Gaussian binomials to Lucas binomials.  Since (1) is the
negative of the `tau` image of (3), equation (4) gives

```text
G_k = sum_(0 <= i <= 10k)
        (-1)^(i+1) g_k(i)e2^i F_(20k-2i+1).                (26)
```

The zeroth layer is zero.  Pair layer `2j+1` with layer `2j+2` and put
`B_j=g_k(2j+2)=2A_j-C_j`.  Then

```text
G_k = sum_(0 <= j < 5k) e2^(2j+1)
        (A_j F_(20k-4j-1)-B_j e2 F_(20k-4j-3)).            (27)
```

For every `m>=3`, the two-row Lucas kernel is Schur-positive:

```text
F_m-2e2F_(m-2) >=_s 0.                                    (28)
```

Indeed, if `ell(n,r)=[s_(n-r,r)]F_(n+1)`, the Lucas recurrence and
one-box Pieri give

```text
[s_(m-1-r,r)](F_m-2e2F_(m-2))
 = ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2) >= 0.              (29)
```

By (17), each parenthesis in (27) is

```text
A_j(F_m-2e2F_(m-2)) + C_j e2F_(m-2),                       (30)
```

and is Schur-positive.  The final pair has `m=3`, so (28) applies
without an exceptional endpoint.  This proves (1).

Finally, (8) gives `g_k(0)=...=g_k(4)=0`, `g_k(5)=1`, and `g_k(6)=0`
for every `k>=2`.  Thus the first nonzero block in (27) is exactly

```text
e2^5 F_(20k-9).                                             (31)
```

The positive recurrence for `ell` shows that this term contains every
allowable two-row shape with second part from `5` to `10k`.  No earlier
block contributes below second part five, proving the strict statement
(2).

An entirely explicit coefficient formula is

```text
[s_(20k-r,r)]G_k
 = sum_(0 <= i <= r) (-1)^(i+1) g_k(i)ell(20k-2i,r-i),      (32)
```

where (8), (10)--(13), and the finite Delannoy formula for `ell` involve
only integer arithmetic.

## Reproducibility and trust boundary

Three deterministic exact implementations are included.

* `verify_symbolic.py` uses SymPy 1.14.0 over `QQ`; it verifies the
  rational generating-function identities, the complete affine-cell
  partition, all 352 Bernstein coefficient polynomials, the finite
  bases, and certificate digest (25).
* `verify_layers.py` uses only CPython arbitrary-precision integers.  It
  independently constructs both Gaussian polynomials by q-Pascal,
  constructs `P,Q` by coin-change recurrences, checks (8) entrywise,
  builds the Lucas Schur kernel from its Pieri recurrence, and compares
  (26) with the positive block reconstruction (30).
* `verify_sparse.py` uses a different representation: sparse
  polynomials in `Z[e1,e2]`.  It constructs Lucas binomials directly
  from the Sagan--Savage recurrence and verifies (26) as a literal
  polynomial identity before independently extracting Schur
  coefficients.

The recorded environment is CPython 3.12.12 and SymPy 1.14.0. This public
copy preserves the exact hash-manifested source. A corrected independent
review at height 1547 rebuilt the certificate and accepted the theorem with
high confidence.

All arithmetic is exact.  There is no floating point, randomness,
solver status, modular reconstruction, interpolation, or finite cutoff
inside the universal certificate.  The human-readable reduction to
(8), (17), and (27) and the exact symbolic certificate together prove
the theorem; the two finite implementations are independent
corroboration and boundary audits.

## Primary-source and graph status

* François Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  states the Lucas comparison and reports bounded verification only:
  https://arxiv.org/abs/2608.30979
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves the ordinary conjecture for
  `a<=3`, not the present `a=4` Lucas family:
  https://arxiv.org/abs/1709.06187
* Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the Lucas-binomial polynomial framework and
  recurrence: https://arxiv.org/abs/0911.3159

Fresh targeted arXiv API searches on 2026-09-03 returned no result for
“lucanomial AND Schur” or “Lucas binomial AND Schur.”  The committed
Discovery Net at height 1524 contained no `(4,5)`, `b=5`, or “width
five” Lucas result.  The novelty claim is therefore only “apparently new
relative to the searched primary sources and committed graph,” not a
historical-priority claim.

At the target-selection height 1524, the complete canonical `b=4`
theorem at height 1515 had no incoming review, objection, or
reproduction.  At height 1525 it received a high-confidence independent
acceptance and reproduction
(`bafkreifttnbh5tj3ju4wtjzsd2isihrb36jg3ptaovyijbbfmjuhfpls3a`).
The present proof does not extrapolate from that theorem: only the earlier
independently reviewed kernel lemma (28), reproved coefficientwise in
(29), is reused.
