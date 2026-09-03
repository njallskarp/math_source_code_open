# The canonical Lucas `(a,b)=(3,6)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1)=e1 F_n+e2 F_(n-1)
```

in `Z[e1,e2]`.  Write `{n choose r}_F` for the associated Lucas
binomial.  For every integer `c>=6`, set

```text
E_c={c+6 choose 6}_F-{2c+3 choose 3}_F.                 (1)
```

This is the forced-sign normalization of the canonical comparison
`(a,b,c,d)=(3,6,c,2c)`.  It has weighted degree `6c`, where
`deg(e1)=1` and `deg(e2)=2`.

**Theorem.**  For every `c>=6`, `E_c` is Schur-positive in two
variables.  More precisely,

```text
[s_(6c-r,r)]E_c = 0       for 0<=r<=3,
[s_(6c-r,r)]E_c > 0       for 4<=r<=3c.                 (2)
```

If the coefficient in (2) is denoted by `e_(c,r)`, then

```text
e_(c,4)=1,
e_(c,r)>=binom(6c-10,r-5)-binom(6c-10,r-6)>0
                                                for 5<=r<=3c. (3)
```

The proof derives an exact ten-step KOH recurrence and proves its
remainder Schur-positive for every parameter.  It is independent of
the provisional canonical `(2,6)` theorem and of every width-five
certificate.

## Homogeneous KOH recurrence

Let `B(n,r)` denote the homogeneous two-variable lift of the Gaussian
binomial `[n choose r]_q`; it has degree `r(n-r)`, and
`B(n,1)=h_(n-1)`.  The width-six KOH identity is

```text
B(c+6,6)
 = h_(6c)
 + e2^2 h_(c-2)h_(5c-2)
 + e2^4 h_(2c-4)h_(4c-4)
 + e2^6 (B(c-2,2)h_(4c-4)+B(3c-4,2))
 + e2^8 h_(c-4)h_(2c-6)h_(3c-6)
 + e2^12 (B(c-3,3)h_(3c-6)+B(2c-5,3))
 + e2^14 B(c-4,2)B(2c-6,2)
 + e2^20 B(c-4,4)h_(2c-8)
 + e2^30 B(c-4,6).                                      (4)
```

Five iterations of the width-three KOH identity give

```text
B(2c+3,3)
 = sum_(0<=j<=4)e2^(6j)
     (h_(6c-12j)+e2^2 h_(2c-4j-2)h_(4c-8j-2))
   +e2^30 B(2c-17,3).                                   (5)
```

Put

```text
H_c=B(c+6,6)-B(2c+3,3).                                 (6)
```

The two tails in (4)--(5) align after lowering `c` by ten.  Hence, for
every `c>=16`,

```text
H_c=e2^30 H_(c-10)+e2^4 K_c.                            (7)
```

For an explicit formula for `K_c`, first put

```text
Delta_c=e2^(-2)(h_(c-2)h_(5c-2)-h_(2c-2)h_(4c-2))
       =-sum_(c-1<=u<=2c-2)e2^(u-2)h_(6c-4-2u).          (8)
```

The second expression proves that the apparent negative power in the
first is harmless.  Direct subtraction of (5) from (4) yields

```text
K_c
 = Delta_c+h_(2c-4)h_(4c-4)
 + e2^2 (B(c-2,2)h_(4c-4)+B(3c-4,2)-h_(6c-12))
 + e2^4 (h_(c-4)h_(2c-6)h_(3c-6)
          -h_(2c-6)h_(4c-10))
 + e2^8 (B(c-3,3)h_(3c-6)+B(2c-5,3)-h_(6c-24))
 + e2^10 (B(c-4,2)B(2c-6,2)-h_(2c-10)h_(4c-18))
 - e2^14 h_(6c-36)
 + e2^16 (B(c-4,4)h_(2c-8)-h_(2c-14)h_(4c-26))
 - e2^20 h_(6c-48)
 - e2^22 h_(2c-18)h_(4c-34).                            (9)
```

Thus (7)--(9) are exact all-parameter KOH identities, not guessed
recurrences.  `verify_layers.py` reconstructs (4), (5), and (9) from
q-Pascal recurrences and checks (7) as a literal polynomial identity.

## Exact Schur layers of the remainder

The degree of `K_c` is

```text
N=6c-8.
```

Write its unique lower-half expansion as

```text
K_c=sum_(0<=r<=3c-4)k_c(r)e2^r h_(N-2r).                (10)
```

Equivalently,

```text
k_c(r)=[q^r](1-q)K_c(q,1).                              (11)
```

With negative arguments assigned value zero, define

```text
P(n)=#{(a,b,d,e,f) in N^5:2a+3b+4d+5e+6f=n},
Q(n)=#{(a,b) in N^2:2a+3b=n},

g_c(i)=P(i)-Q(i)
       -sum_(1<=nu<=6)P(i-c-nu)
       +sum_(1<=mu<nu<=6)P(i-2c-mu-nu)
       +sum_(1<=nu<=3)Q(i-2c-nu).                       (12)
```

Through lower-half degree `3c`, at most two numerator factors of the
width-six Gaussian and at most one numerator factor of the width-three
Gaussian can activate.  Therefore

```text
g_c(i)=[q^i](1-q)H_c(q,1),                 0<=i<=3c,
k_c(r)=g_c(r+4)-g_(c-10)(r-26),            0<=r<=3c-4.  (13)
```

The second term in (13) is zero when its index is negative.

## Restricted-partition quasipolynomials

Define, with value zero at negative arguments,

```text
T(n)=#{(a,b,d,e,f) in N^5:a+2b+3d+3e+5f=n},
U(n)=#{(a,b) in N^2:a+3b=n}.                            (14)
```

Splitting parity gives

```text
P(2n)  =T(n)+T(n-4),       P(2n+1)=T(n-1)+T(n-2),
Q(2n)  =U(n),              Q(2n+1)=U(n-1).              (15)
```

The exact quasipolynomials are

```text
T(n)=n^4/2160+7n^3/540+n^2/8+alpha_(n mod 3)n
     +beta_(n mod 30),
U(n)=n/3+gamma_(n mod 3),                                (16)
```

where

```text
540 alpha = 279,239,259,
3 gamma   = 3,2,1,                                        (17)

2160 beta =
 2160, 905, 928,2025, 608,1225,2160, 473,1360,1593,
 1040,1225,1728, 905, 928,2025,1040, 793,2160, 473,
 1360,2025, 608,1225,1728, 905,1360,1593,1040, 793.      (18)
```

Both universal checkers prove these formulas by summing their residue
polynomials and verifying

```text
sum_(n>=0)T(n)z^n=1/((1-z)(1-z^2)(1-z^3)^2(1-z^5)),
sum_(n>=0)U(n)z^n=1/((1-z)(1-z^3)).                      (19)
```

No interpolation is used.  In particular,

```text
239n/540+473/2160
 <= T(n)-(n^4/2160+7n^3/540+n^2/8)
 <= 279n/540+1,

n/3+1/3 <= U(n) <= n/3+1.                               (20)
```

## Uniform adjacent-layer certificate

For every complete even/odd pair in (10), set

```text
A_j=k_c(2j),                  C_j=2k_c(2j)-k_c(2j+1).    (21)
```

The universal inequalities are

```text
A_j>=0,                       C_j>=0.                    (22)
```

Write `c=2t+rho`, where `rho` is zero or one.  The exclusive domains
for `j` are

```text
rho             0          1
A domain      j<3t-1      j<3t
C domain      j<3t-2      j<3t.                          (23)
```

For even `c`, the final `A` is the unpaired middle layer.

Substituting (15) into (12)--(13) expresses every quantity in (21) as
a signed sum of terms `T(j+ut+v)` and `U(j+ut+v)`.  Both certificate
programs reconstruct these affine terms directly and compare them with
(12)--(13) through `c=200`.

For `t>=60`, zero, the endpoints in (23), and every activation
threshold partition the four parity/quantity cases into 134 stable
affine cells.  There are 16 initial constant cells, checked at exact
integer values.  On each of the other 118 cells, use the appropriate
lower or upper bound in (20) according to the sign of each occurrence.
This gives a rigorous quartic lower bound `L(t,j)`.

On a cell `a(t)<=j<=b(t)`, substitute

```text
t=60+x,
j=a(t)+(b(t)-a(t))z,                 x>=0, 0<=z<=1.       (24)
```

Writing the result in the degree-four Bernstein basis in `z` produces
590 coefficient polynomials.  Every coefficient lies in `QQ_+[x]`, so
(22) holds for all `t>=60`.  Direct exact evaluation proves the finite
complement `16<=c<120`.

The SymPy implementation's canonical certificate record has SHA-256

```text
4fab7d452d715e6070e9fdbb07e1d0388dd8037cda6bc0e1ec35e436718741cd. (25)
```

The independent standard-library `Fraction` implementation uses a
separate sparse polynomial engine and compact record format.  Its
certificate SHA-256 is

```text
0c44943d1ed5f03f72644d7d2876768948251d7f7145ec4d6eada6ea60eb211a. (26)
```

## Lucas transport and positive Schur pairing

Let `tau(e1)=e1` and `tau(e2)=-e2`.  Then `tau(h_n)=F_(n+1)`, and it
sends homogeneous Gaussian binomials to Lucas binomials.  Since
`E_c=tau(H_c)` and the recurrence shifts are even, (7) becomes

```text
E_c=e2^30 E_(c-10)+e2^4 R_c,              c>=16,         (27)
R_c=tau(K_c)
   =sum_(0<=r<=3c-4)(-1)^r k_c(r)e2^r F_(N-2r+1).        (28)
```

For

```text
ell(n,r)=[s_(n-r,r)]F_(n+1),                              (29)
```

the Lucas recurrence and one-box Pieri rule give, for every `m>=3`,

```text
[s_(m-1-r,r)](F_m-2e2 F_(m-2))
 =ell(m-2,r)+ell(m-3,r-2)+ell(m-4,r-2)>=0.               (30)
```

Let `B_j=k_c(2j+1)=2A_j-C_j` and `m=N-4j+1`.  Pairing consecutive
terms of (28) gives

```text
e2^(2j)(A_j F_m-B_j e2 F_(m-2))
 =e2^(2j)(A_j(F_m-2e2 F_(m-2))+C_j e2 F_(m-2)).          (31)
```

Equations (22) and (30) make every complete block Schur-positive.  If
`c` is odd, the last pair has `m=3`.  If `c` is even, it is followed by
the nonnegative middle term `k_c(3c-4)e2^(3c-4)F_1`.  Thus every
endpoint is covered and `R_c` is Schur-positive.

The ten direct bases `E_6,...,E_15` are Schur-positive by exact
q-Pascal/Schur calculation.  Induction in (27) proves the theorem.

For `c>=16`, `k_c(0)=k_c(1)=1`.  The first pair of the remainder
contribution is

```text
e2^4(F_(6c-7)-e2 F_(6c-9))
 =e2^4(F_(6c-7)-2e2 F_(6c-9))+e2^5 F_(6c-9).            (32)
```

The standard ballot estimate

```text
ell(n,r)>=binom(n,r)-binom(n,r-1)>0                      (33)
```

applied to the second term proves (2)--(3) for `c>=16`, because all
later blocks and the shifted prior term are Schur-positive.  The exact
base calculation verifies the same claims for `6<=c<=15`.

## Reproduction and trust boundary

Run from this directory with CPython 3.12 and SymPy 1.14.0:

```bash
python3 verify_symbolic.py
python3 verify_fraction.py
python3 verify_layers.py --max-c 100
python3 verify_sparse.py --max-c 40
shasum -a 256 -c SHA256SUMS
```

Expected compact output includes

```text
affine cells: 134; exact initial cells: 16; Bernstein polynomials: 590
certificate SHA-256: 4fab7d452d715e6070e9fdbb07e1d0388dd8037cda6bc0e1ec35e436718741cd
independent certificate SHA-256: 0c44943d1ed5f03f72644d7d2876768948251d7f7145ec4d6eada6ea60eb211a
least nonzero Lucas Schur coefficient: (1, 6, 4)
```

All arithmetic is exact.  There is no floating point, randomness,
interpolation, modular reconstruction, solver, external generated
proof data, or large certificate file.  `verify_symbolic.py` and
`verify_fraction.py` independently prove the universal affine-cell
certificate.  `verify_layers.py` checks KOH, q-Pascal, restricted
partitions, the recurrence, the positive pairing, strict support, and
all endpoints.  `verify_sparse.py` starts from the Sagan--Savage
lucasnomial recurrence in sparse `Z[e1,e2]` and verifies literal
polynomial identities.  The proof trusts CPython integer and
`Fraction` arithmetic; the first certificate additionally trusts
SymPy rational-polynomial arithmetic.  The finite execution ranges of
the last two checkers audit the universal proof rather than supply its
quantifier.

This theorem should remain provisional until an independent researcher
rebuilds the 134 activation cells, both quasipolynomial bounds, all 590
Bernstein polynomials, the pairing, and the two endpoint regimes.

## Primary-source and graph status

* François Bergeron, *A (q,t)-Overview of q-Analogs*,
  arXiv:2608.30979, states the Lucas comparison and reports bounded
  verification: https://arxiv.org/abs/2608.30979
* Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the lucasnomial framework:
  https://arxiv.org/abs/0911.3159
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves the ordinary Gaussian
  comparison for `a<=3` using KOH, not the Lucas-Schur theorem here:
  https://arxiv.org/abs/1709.06187
* Fabrizio Zanello, *Zeilberger's KOH theorem and the strict
  unimodality of q-binomial coefficients*, arXiv:1311.4480, records the
  KOH method: https://arxiv.org/abs/1311.4480

Targeted live primary-source searches on 2026-09-03 found no
Lucas-Schur theorem for the canonical `(3,6)` family.  The committed
Discovery Net at target-selection height 1690 contained no `(3,6)`
Lucas contribution or active Lucas collision.  The preceding `(2,6)`
theorem at height 1677 had not yet received independent review, and the
present proof does not use it.  The novelty claim is only “apparently
new relative to the searched primary sources and committed graph,” not
a claim of historical priority.
