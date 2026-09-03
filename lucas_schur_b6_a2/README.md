# The canonical Lucas `(a,b)=(2,6)` family

## Exact theorem

Let `F_0=0`, `F_1=1`, and

```text
F_(n+1)=e1 F_n+e2 F_(n-1)
```

in `Z[e1,e2]`.  Write `{n choose r}_F` for the associated Lucas
binomial.  For every integer `c>=6`, set

```text
D_c={3c+2 choose 2}_F-{c+6 choose 6}_F.                 (1)
```

This is the forced-sign normalization of the canonical comparison
`(a,b,c,d)=(2,6,c,3c)`.  It has weighted degree `6c`, where
`deg(e1)=1` and `deg(e2)=2`.

**Theorem.**  For every `c>=6`, `D_c` is Schur-positive in two
variables.  More precisely,

```text
[s_(6c-r,r)]D_c = 0       for 0<=r<=2,
[s_(6c-r,r)]D_c > 0       for 3<=r<=3c.                 (2)
```

If the coefficient in (2) is denoted by `d_(c,r)`, then

```text
d_(c,3)=1,
d_(c,r)>=binom(6c-8,r-4)-binom(6c-8,r-5)>0
                                                for 4<=r<=3c, (3)
```

where a binomial coefficient with lower index `-1` is zero.

The proof is a genuine KOH/Schur-basis argument.  It derives an exact
ten-step recurrence and proves its remainder Schur-positive for every
parameter.  It neither invokes nor depends on any width-five theorem.

## Homogeneous KOH recurrence

Let `B(n,r)` denote the homogeneous two-variable lift of the Gaussian
binomial `[n choose r]_q`; it has degree `r(n-r)`, and
`B(n,1)=h_(n-1)`.  Zeilberger's KOH identity, grouped by the eleven
partitions of six, gives

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

The two summands inside each parenthesis account for two KOH
partitions with the same exponent.  Iterating the width-two KOH
identity fifteen times gives

```text
B(3c+2,2)
 = sum_(0<=j<=14) e2^(2j)h_(6c-4j)
   +e2^30 B(3c-28,2).                                   (5)
```

Put

```text
H_c=B(c+6,6)-B(3c+2,2).                                 (6)
```

Using `h_a h_b-h_(a+b)=e2 h_(a-1)h_(b-1)` on the exponent-two
terms of (4)--(5) yields, for every `c>=16`,

```text
H_c=e2^30 H_(c-10)+e2^3 K_c,                             (7)
```

where the following is an explicit all-parameter formula:

```text
K_c
 = h_(c-3)h_(5c-3)
 + e2 h_(2c-4)h_(4c-4)
 + e2^3 (B(c-2,2)h_(4c-4)+B(3c-4,2))
 + e2^5 h_(c-4)h_(2c-6)h_(3c-6)
 + e2^9 (B(c-3,3)h_(3c-6)+B(2c-5,3))
 + e2^11 B(c-4,2)B(2c-6,2)
 + e2^17 B(c-4,4)h_(2c-8)
 - sum_(2<=j<=14)e2^(2j-3)h_(6c-4j).                    (8)
```

Thus (8) is not an experimental guess: it is the exact KOH remainder.
The checker `verify_layers.py` reconstructs (4), (5), and (8) from
q-Pascal recurrences and verifies (7) as a polynomial identity.

## Exact Schur layers of the remainder

The degree of `K_c` is

```text
N=6c-6.
```

Every symmetric homogeneous polynomial in two variables has a unique
lower-half expansion, so write

```text
K_c=sum_(0<=r<=3c-3) k_c(r)e2^r h_(N-2r).                (9)
```

Equivalently,

```text
k_c(r)=[q^r](1-q)K_c(q,1).                              (10)
```

There is a compact exact formula for every coefficient in (10).  With
negative arguments assigned value zero, define

```text
P(n)=#{(a,b,d,e,f) in N^5:2a+3b+4d+5e+6f=n},
V(n)=#{a in N:2a=n},

g_c(i)=P(i)-V(i)
       -sum_(1<=nu<=6)P(i-c-nu)
       +sum_(1<=mu<nu<=6)P(i-2c-mu-nu).                 (11)
```

Only zero, one, or two numerator factors of the Gaussian product can
activate through degree `3c`; three have degree at least `3c+6`.
Consequently,

```text
g_c(i)=[q^i](1-q)H_c(q,1),                 0<=i<=3c,
k_c(r)=g_c(r+3)-g_(c-10)(r-27).            0<=r<=3c-3.  (12)
```

The second term in (12) is zero when its index is negative.

## Restricted-partition quasipolynomial

Define

```text
T(n)=#{(a,b,d,e,f) in N^5:a+2b+3d+3e+5f=n},             (13)
```

again with `T(n)=0` for `n<0`.  Splitting the parities of the
multiplicities of parts three and five gives

```text
P(2n)  =T(n)+T(n-4),
P(2n+1)=T(n-1)+T(n-2).                                  (14)
```

The exact period-30 quasipolynomial is

```text
T(n)=n^4/2160+7n^3/540+n^2/8+alpha_(n mod 3)n
     +beta_(n mod 30),                                  (15)
```

where

```text
540 alpha = 279,239,259                                  (16)
```

in residue order modulo three, and, in residue order beginning at zero,

```text
2160 beta =
 2160, 905, 928,2025, 608,1225,2160, 473,1360,1593,
 1040,1225,1728, 905, 928,2025,1040, 793,2160, 473,
 1360,2025, 608,1225,1728, 905,1360,1593,1040, 793.      (17)
```

Both universal certificate programs prove (15)--(17) by summing the
thirty residue polynomials and checking the rational identity

```text
sum_(n>=0)T(n)z^n=1/((1-z)(1-z^2)(1-z^3)^2(1-z^5)).     (18)
```

In particular, for every `n>=0`, (15) lies between the two quartics
obtained by using respectively

```text
(alpha,beta)=(239/540,473/2160)
and             (279/540,1).                             (19)
```

## Uniform adjacent-layer certificate

For every complete even/odd pair in (9), set

```text
A_j=k_c(2j),                  C_j=2k_c(2j)-k_c(2j+1).    (20)
```

The key all-parameter inequalities are

```text
A_j>=0,                       C_j>=0.                    (21)
```

Write `c=2t+rho`, where `rho` is zero or one.  The exclusive domains
for `j` are

```text
rho             0          1
A domain      j<3t-1      j<3t+1
C domain      j<3t-1      j<3t.                          (22)
```

For odd `c`, the final `A` is the unpaired middle layer.

Substitute (14) termwise into (11)--(12).  Every term becomes an
integer multiple of

```text
T(j+u t+v),                                             (23)
```

where `u,v` are explicit integers reconstructed by both checkers.  The
only endpoint correction is `+1` in `C_j` for `0<=j<=12`: before layer
30, the two width-two `V` terms in (12) have not yet both activated.

For `t>=60`, collect zero, the endpoint in (22), `j=13`, and every
activation threshold at which an argument in (23) becomes nonnegative.
The ordered thresholds partition all four parity/quantity cases into
132 affine cells.  Successive threshold gaps are at least one and stay
ordered for all `t=60+x`, `x>=0`.

There are 18 initial constant cells, checked at their exact integer
values.  On each of the other 114 cells, use the lower choice in (19)
for a positive occurrence of `T` and the upper choice for a negative
occurrence.  This gives a rigorous quartic lower bound `L(t,j)` for
`A_j` or `C_j`.  On a cell `a(t)<=j<=b(t)`, substitute

```text
t=60+x,
j=a(t)+(b(t)-a(t))z,                 x>=0, 0<=z<=1.       (24)
```

Writing the resulting polynomial in the degree-four Bernstein basis
in `z` produces 570 coefficient polynomials.  Every coefficient lies
in `QQ_+[x]`; hence (21) holds for every `t>=60`.  Direct exact
evaluation proves the finite complement `16<=c<120`.

The SymPy implementation's canonical record of all cells and
Bernstein polynomials has SHA-256

```text
ea8e69d642ad4d74cc3d0b83c3b35ace1061317414013c41e366c17113da35da. (25)
```

The independent standard-library `Fraction` implementation uses a
separate sparse polynomial engine and compact record format.  Its
certificate SHA-256 is

```text
bf6aa6ac2e9bb155677d9b5a21b0525d8c3a82e51aecf89ead8f0dc6d582015b. (26)
```

## Lucas transport and positive Schur pairing

Let `tau(e1)=e1` and `tau(e2)=-e2`.  Then `tau(h_n)=F_(n+1)`, and it
sends homogeneous Gaussian binomials to Lucas binomials.  Since
`D_c=-tau(H_c)`, (7) becomes

```text
D_c=e2^30 D_(c-10)+e2^3 R_c,              c>=16,         (27)
R_c=tau(K_c)
   =sum_(0<=r<=3c-3)(-1)^r k_c(r)e2^r F_(N-2r+1).        (28)
```

For

```text
ell(n,r)=[s_(n-r,r)]F_(n+1),                              (29)
```

the Lucas recurrence and the one-box Pieri rule give, for every
`m>=3`,

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

Equations (21) and (30) make every block in (31) Schur-positive.  If
`c` is even, the last pair has `m=3`; if `c` is odd, the last pair has
`m=5` and is followed by the nonnegative middle term
`k_c(3c-3)e2^(3c-3)F_1`.  Thus every endpoint is covered and `R_c` is
Schur-positive.

The ten direct bases `D_6,...,D_15` are Schur-positive by exact
q-Pascal/Schur calculation.  Induction in (27) proves the theorem.

Finally, `g_c(0)=g_c(1)=g_c(2)=0` and `g_c(3)=g_c(4)=1`.  For
`c>=16`, the first pair of the Schur-positive remainder contribution
`e2^3 R_c` is therefore

```text
e2^3(F_(6c-5)-e2 F_(6c-7))
 =e2^3(F_(6c-5)-2e2 F_(6c-7))+e2^4 F_(6c-7).            (32)
```

The second term contains every two-row shape with second part from
four through `3c`, while the first supplies coefficient one at second
part three.  All later blocks of the remainder, and the shifted prior
term in (27), are Schur-positive.  The standard ballot lower bound

```text
ell(n,r)>=binom(n,r)-binom(n,r-1)>0                      (33)
```

applied to (32) proves (2)--(3) for `c>=16`.  For the ten bases, the
checker verifies these statements directly.

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
affine cells: 132; exact initial cells: 18; Bernstein polynomials: 570
certificate SHA-256: ea8e69d642ad4d74cc3d0b83c3b35ace1061317414013c41e366c17113da35da
independent certificate SHA-256: bf6aa6ac2e9bb155677d9b5a21b0525d8c3a82e51aecf89ead8f0dc6d582015b
least nonzero Lucas Schur coefficient: (1, 6, 3)
```

All arithmetic is exact.  There is no floating point, randomness,
interpolation, modular reconstruction, or external generated proof
data.  `verify_symbolic.py` and `verify_fraction.py` independently
prove the universal affine-cell certificate.  `verify_layers.py`
checks KOH, q-Pascal, restricted-partition, endpoint, recurrence, and
positive-pair reconstruction.  `verify_sparse.py` starts from the
Sagan--Savage lucasnomial recurrence in sparse `Z[e1,e2]` and verifies
literal polynomial identities.  The proof trusts CPython integer and
`Fraction` arithmetic; the first certificate additionally trusts
SymPy rational-polynomial arithmetic.  The finite execution ranges of
the last two checkers are audits, not the source of the universal
quantifier, which is supplied by (15)--(24).

This result should remain provisional until an independent researcher
rebuilds the 132 activation cells, the two quasipolynomial bounds, all
570 Bernstein polynomials, the pairing, and both endpoint regimes.

## Primary-source and graph status

* François Bergeron, *A (q,t)-Overview of q-Analogs*,
  arXiv:2608.30979, states the Lucas comparison and reports bounded
  verification: https://arxiv.org/abs/2608.30979
* Bruce Sagan and Carla Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  arXiv:0911.3159, supplies the lucasnomial polynomial framework:
  https://arxiv.org/abs/0911.3159
* Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, arXiv:1709.06187, proves the ordinary Gaussian
  comparison for `a<=3` using KOH, not the Lucas-Schur theorem here:
  https://arxiv.org/abs/1709.06187
* Fabrizio Zanello, *Zeilberger's KOH theorem and the strict
  unimodality of q-binomial coefficients*, arXiv:1311.4480, records the
  KOH method used in (4): https://arxiv.org/abs/1311.4480

Targeted live primary-source searches on 2026-09-03 found no
Lucas-Schur theorem for the canonical `(2,6)` family.  The committed
Discovery Net at target-selection height 1662 contained no width-six
Lucas result or active collision.  The novelty claim is only
“apparently new relative to the searched primary sources and committed
graph,” not a claim of historical priority.
