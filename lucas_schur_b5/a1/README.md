# The canonical Lucas `(a,b)=(1,5)` boundary and all `a=1` rays

## Results

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1) = e1 F_n + e2 F_(n-1)                           (1)
```

in `Z[e1,e2]`, and write `{n choose r}_F` for the associated Lucas
binomial.

**General boundary theorem.** For all integers `2<=b<=c`,

```text
A_(b,c) = {b+c choose b}_F - F_(bc+1)                    (2)
```

belongs to `N[e1,e2]`.  Hence every canonical Lucas
Bergeron--Vessenes comparison with `a=1` is elementary-positive and
therefore Schur-positive in two variables.

The requested width-five specialization is

```text
D_k = {k+5 choose 5}_F - F_(5k+1),             k>=5.      (3)
```

If `c_(k,r)=[s_(5k-r,r)]D_k`, then

```text
c_(k,0)=c_(k,1)=0,
c_(k,2)=1,
c_(k,r)>0                         for 2<=r<=floor(5k/2).  (4)
```

Thus (3) closes the remaining canonical `b=5` boundary ray without a
finite exception or an affine-cell certificate.

## KOH transport and the general theorem

For a partition `lambda=(lambda_1,lambda_2,...)` of `b`, put

```text
Y_j = lambda_1+...+lambda_j,       Y_0=0,
E_lambda = 2 sum_i binom(lambda_i,2).                     (5)
```

Parts and partial sums after the end of the partition are interpreted
as zero and `b`, respectively.  Zeilberger's KOH identity is

```text
Gaussian(b+c,b)
 = sum_(lambda partition b) q^(E_lambda)
   product_(j>=1)
   Gaussian(j(c+2)-Y_(j-1)-Y_(j+1), lambda_j-lambda_(j+1)).  (6)
```

Every exponent `E_lambda` is even.  The unique zero exponent occurs for
`lambda=(1^b)`; its only factor is `Gaussian(bc+1,1)`.

Homogenize (6) in two variables and apply the involution

```text
tau(e1)=e1,                       tau(e2)=-e2.             (7)
```

It sends homogeneous Gaussian binomials to Lucas binomials.  A shift
`q^E` homogenizes to `e2^E`, and (5) makes
`tau(e2^E)=(-e2)^E=e2^E`.  The `(1^b)` summand becomes `F_(bc+1)`.
Removing it proves the exact all-parameter identity

```text
A_(b,c)
 = sum_(lambda partition b, lambda != (1^b)) e2^(E_lambda)
   product_(j>=1)
   {j(c+2)-Y_(j-1)-Y_(j+1)
      choose lambda_j-lambda_(j+1)}_F.                    (8)
```

The recurrence (1) and the Sagan--Savage lucasnomial recurrence show
that every factor in (8) lies in `N[e1,e2]`.  All displayed powers of
`e2` are also positive.  This proves the general boundary theorem.
The proof is algebraic transport of the full KOH decomposition; it is
not inference from finite computation.

## Explicit width-five identity

The seven partitions of five give exponents

```text
20, 12, 8, 6, 4, 2, 0
```

for `(5),(4,1),(3,2),(3,1,1),(2,2,1),(2,1,1,1),(1^5)`.
Substitution in (6)--(8) gives

```text
{k+5 choose 5}_F
 = F_(5k+1)
   + e2^2  F_(k-1) F_(4k-1)
   + e2^4  F_(2k-3) F_(3k-3)
   + e2^6  {k-2 choose 2}_F F_(3k-3)
   + e2^8  F_(k-3) {2k-4 choose 2}_F
   + e2^12 {k-3 choose 3}_F F_(2k-5)
   + e2^20 {k-3 choose 5}_F.                              (9)
```

Lucas binomials outside their natural lower-index range are zero.  For
the canonical range `k>=5`, every factor and every coefficient on the
right belongs to `N[e1,e2]`.  Removing the first term proves (3)
elementary-positive directly.

## Exact eight-step positive recurrence

For `k>=13`, the last lucasnomial in (9) is

```text
{k-3 choose 5}_F = D_(k-8)+F_(5k-39).
```

Consequently

```text
D_k = e2^20 D_(k-8) + R_k,                     k>=13,     (10)
```

where

```text
R_k = e2^2  F_(k-1) F_(4k-1)
    + e2^4  F_(2k-3) F_(3k-3)
    + e2^6  {k-2 choose 2}_F F_(3k-3)
    + e2^8  F_(k-3) {2k-4 choose 2}_F
    + e2^12 {k-3 choose 3}_F F_(2k-5)
    + e2^20 F_(5k-39).                                   (11)
```

Thus `R_k` is elementary-positive.  Formula (9) proves the eight bases
`D_5,...,D_12` directly, while (10)--(11) give the requested exact
all-parameter recurrence.  The direct identity (9) is stronger than
the induction because it remains positive without separating bases.

## Strict Schur support and a ballot lower bound

The first summand of `D_k` in (9) is

```text
e2^2 F_(k-1)F_(4k-1).                                   (12)
```

It already supplies every allowable two-row Schur shape.  To make this
quantitative, define

```text
ell(n,j)=[s_(n-j,j)]F_(n+1).                              (13)
```

The Delannoy expansion of `F_(n+1)` gives

```text
ell(n,j) >= binom(n,j)-binom(n,j-1)>0,       0<=2j<=n,    (14)
```

with `binom(n,-1)=0`.

Fix `2<=r<=floor(5k/2)` and put

```text
u=r-2,                n=4k-2,                j=min(u,n-u). (15)
```

The leading Schur term of `F_(k-1)` is `s_(k-2)`.  If `u<=n/2`,
the `s_(n-u,u)` term of `F_(4k-1)` reaches second part `u` in the
Pieri product with horizontal-strip parameter zero.  If `u>n/2`, use
`j=n-u` and horizontal-strip parameter

```text
t=2u-n.
```

Then `0<=t<=k-2` by `u<=floor((5k-4)/2)`, while
`t=n-2j`.  The two-variable Pieri rule therefore again reaches second
part `u`.  After the `e2^2` shift in (12), both cases give

```text
c_(k,r) >= ell(4k-2,j)
          >= binom(4k-2,j)-binom(4k-2,j-1)>0.             (16)
```

At `r=2`, only the leading terms of the two factors in (12) contribute,
with coefficient one; every later summand of (9) begins at `e2^4`.
All terms in (9) begin at `e2^2`, proving the two zeros in (4).

## Reproducibility and trust boundary

Two deterministic standard-library programs use different exact
representations.

* `verify_koh.py` uses immutable integer coefficient tuples and the
  q-Pascal recurrence.  It generates partitions rather than storing a
  KOH table, verifies the general KOH identity in 92 cases with
  `2<=b<=9` and `b<=c<=16`, proves that the zero-exponent summand is
  uniquely `(1^b)`, and checks (9) through `k=100`.  The canonical
  seven-partition structural record has SHA-256
  `2ed9293c891669589170bf172bbec8b54860bf69ef2d295be84d65c125566a94`.
* `verify_sparse.py` constructs lucasnomials directly in `Z[e1,e2]`
  from the Sagan--Savage recurrence.  It verifies (9) as a literal
  polynomial identity, elementary positivity, (4), and the ballot
  bound (16) through `k=40`, and checks (10)--(11) for `13<=k<=40`.

The universal proof is (6)--(8), not either finite run.  The width-five
recurrence and strict-support proof are the algebraic deductions
(9)--(16).  The checkers independently audit KOH transcription and the
Lucas image.  Both use CPython arbitrary-precision integers only; there
is no floating point, randomness, CAS, solver, interpolation, modular
reconstruction, or generated external certificate.  The recorded
environment is CPython 3.12.12.

Run from the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a1/verify_koh.py
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b5/a1/verify_sparse.py
(cd lucas_schur_b5 && sha256sum -c SHA256SUMS)
```

## Primary sources and graph status

Fabrizio Zanello records the exact KOH formula (6) as Lemma 2.3 in
*On Bergeron's positivity problem for q-binomial coefficients*,
arXiv:1709.06187:

https://arxiv.org/abs/1709.06187

Bruce Sagan and Carla Savage supply the positive lucasnomial polynomial
framework and recurrence used after transport:

https://arxiv.org/abs/0911.3159

François Bergeron's 2026 overview states the Lucas comparison and
reports bounded verification, not the general boundary theorem or (9):

https://arxiv.org/abs/2608.30979

The ordinary Gaussian `a=1` comparison is immediate from Gaussian
unimodality, as Zanello notes.  That observation does not imply the
present elementary-positive Lucas image: the decisive extra fact is
the even KOH exponent (5), which prevents sign reversal under (7).

A targeted primary-source search on 2026-09-03 found no external
general Lucas `a=1` theorem or canonical `(1,5)` identity.  At graph
target-selection height 1600 there was no `(1,5)` or `a=1 boundary`
contribution.  The responsible novelty statement is only “apparently
new relative to the searched primary sources and committed graph,” not
a historical-priority claim.

The interior `b=5` synthesis is
`bafkreia7higbufees2ntkqacoshnmayfhkevtlv4t56dzr4ts3lbsxa5zq`
at height 1589.  Combining it with (3) proves the full canonical
`b=5` slice, subject to the synthesis's stated provisional review status
for its `(2,5)` constituent.
