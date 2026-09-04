# Endpoint Hadamard structure for three path blocks

## Result

Let `P_3^(a)` be the path block polytope with three blocks of `a`
nonnegative coordinates, block sums `R_1,R_2,R_3`, and inequalities

```text
R_1+R_2 <= 1,       R_2+R_3 <= 1.
```

Let an internal coordinate permutation `g=(sigma,tau,upsilon)` have cycle
types `lambda,mu,nu`, respectively.  Put

```text
Q_lambda(t) = product_(d in lambda) (1-t^d),
A_lambda(n) = [t^n] 1/((1-t)Q_lambda(t)).
```

Thus `A_lambda(n)` counts nonnegative cycle variables whose weighted sum is
at most `n`.  The evaluation of the equivariant `h*`-series at `g` is

```text
h*_g(t) = (1-t) Q_lambda(t) Q_nu(t)
          sum_(n>=0) A_lambda(n) A_nu(n) t^n.                 (1)
```

In particular, (1) is independent of the middle cycle type `mu`.  It turns
the internal-symmetry question into a Hadamard product of two weighted
polynomial-ring Hilbert series.

Formula (1) gives two all-width classifications.

1. If one endpoint is fixed coordinatewise and the other endpoint
   permutation is nonidentity, then `h*_g(t)` is not a polynomial.  More
   precisely, at every nontrivial root `zeta` of `Q_lambda`, it has a pole
   of exact order `a`.
2. Suppose one endpoint has rectangular cycle type `(d^r)`, where `a=dr`.
   Then `h*_g(t)` is a polynomial if and only if the other endpoint also
   has cycle type `(d^r)`.  In the polynomial case,

```text
h*_g(t) = sum_(j=0)^r binom(r,j)^2 t^(dj).                    (2)
```

There is also a uniform diagonal pole theorem.  Suppose both endpoints have
the same cycle type `lambda`.  Write `d=gcd(lambda)`, reduce the parts to
`bar(lambda)=lambda/d`, and let `r` be the number of cycles.  If
`bar(lambda)` is not `(1^r)`, put

```text
m = max_(k>=2) #{i : k divides bar(lambda)_i}.
```

For every `k` attaining this maximum, and every `xi` such that `xi^d` is a
primitive `k`-th root, `h*_g(t)` has a pole of exact order `r-m` at `xi`.
Consequently synchronized endpoint actions have polynomial equivariant
`h*` exactly for rectangular cycle types.  The middle action remains
arbitrary.

The exact check over every ordered pair of endpoint partitions through
width ten finds no polynomial cases beyond (2).  This supports, but does
not prove, the general classification conjecture that (2) lists all
polynomial internal conjugacy classes.

We use the following elementary partial-fraction fact below.  If rational
series have poles of orders `p,q` at `alpha,beta`, then the Hadamard product
of those two principal parts has a pole of order `p+q-1` at `alpha*beta`,
with nonzero leading coefficient.  This follows immediately by multiplying
the coefficient formulas
`binom(n+p-1,p-1)alpha^(-n)` and
`binom(n+q-1,q-1)beta^(-n)`.  Thus a uniquely maximal pole pairing cannot
cancel.

## Synchronized endpoint pole theorem

First use (5) below to divide all cycle lengths by their common gcd.  We may
therefore assume `gcd(lambda)=1`.  If `lambda` is nontrivial, then `m>=1`
and `m<r`.  Let `zeta` be a primitive `k`-th root for an order `k` attaining
`m`.  The endpoint series `1/((1-t)Q_lambda(t))` has pole order `r+1` at
`1`, pole order `m` at `zeta`, and pole order at most `m` at every other
nontrivial root.

In its Hadamard square, the two pairings `(zeta,1)` and `(1,zeta)` are
identical and add rather than cancel.  They give a pole of order `m+r` at
`zeta`.  Any pairing of two nontrivial roots has order at most
`2m-1 < m+r`, so this pole order is exact.  Formula (1) contributes a zero
of order `2m`, leaving a pole of exact order `r-m`.

Undoing the common scale replaces `t` by `t^d`; its derivative is nonzero
at roots of unity, so the pole order is unchanged.  The only case with no
witness is `bar(lambda)=(1^r)`, equivalently
`lambda=(d^r)`, and (2) gives its polynomial.  This proves the claimed
if-and-only-if classification for synchronized endpoint cycle types.

## Proof of the endpoint formula

For a fixed lattice point in the `q`-th dilation, let the exact middle-block
sum be `B`.  The middle block has

```text
p_mu(B) = [t^B] 1/Q_mu(t)
```

fixed coordinate choices.  The two endpoint choices are independent and
number `A_lambda(q-B)` and `A_nu(q-B)`.  Hence

```text
E_g(q) = sum_(B=0)^q p_mu(B) A_lambda(q-B) A_nu(q-B).
```

Taking the generating function in `q` gives

```text
E_g(t) = 1/Q_mu(t) * sum_(n>=0) A_lambda(n)A_nu(n)t^n.        (3)
```

The homogenized permutation determinant is

```text
det(I-t rho_tilde(g))
  = (1-t)Q_lambda(t)Q_mu(t)Q_nu(t).
```

Multiplying (3) by this determinant cancels `Q_mu` and proves (1).

## The exact one-sided pole

If the right endpoint is fixed, then `nu=(1^a)` and

```text
A_nu(n) = binom(n+a,a).
```

Writing `Theta=t d/dt`, coefficientwise multiplication by this binomial is
the differential operator

```text
sum A_lambda(n)binom(n+a,a)t^n
  = 1/a! product_(j=1)^a (Theta+j)
    (1/((1-t)Q_lambda(t))).                                 (4)
```

At a nonzero root `zeta != 1` where `Q_lambda` has zero order `c`, the
right side of (4) has pole order exactly `c+a`: every application of
`Theta+j` raises the pole order once and has nonzero leading coefficient.
The factor `Q_lambda` in (1) cancels exactly `c` orders, while `(1-t)^(a+1)`
is nonzero at `zeta`.  The remaining pole has exact order `a`.

## Rectangular endpoint cycles

For `lambda=nu=(d^r)`,

```text
A_lambda(n) = binom(floor(n/d)+r,r).
```

Consequently,

```text
sum A_lambda(n)^2 t^n
  = (1+t+...+t^(d-1))
    sum_(k>=0) binom(k+r,r)^2 t^(dk)

  = (1+t+...+t^(d-1))
    (sum_(j=0)^r binom(r,j)^2 t^(dj))/(1-t^d)^(2r+1).
```

Substitution in (1), using
`(1-t)(1+t+...+t^(d-1))=1-t^d`, proves (2).

Now suppose only the left endpoint is `(d^r)`.  If some right cycle length
is not divisible by `d`, take a primitive `d`-th root `zeta` (the case
`d=1` is handled by (4)).  The pole obtained by pairing the order-`r` pole
of the left series at `zeta` with the order-`s+1` pole of the right series
at `1` is the unique pole of top order `r+s` in the Hadamard product.  The
determinant in (1) has zero order only `r+c`, where `c<s` is the number of
right cycles divisible by `d`; a pole remains.

If every right cycle is divisible by `d`, divide all endpoint weights by
`d`.  For `lambda=d lambda'` and `nu=d nu'`, direct residue splitting gives

```text
h*_(lambda,nu)(t) = h*_(lambda',nu')(t^d).                    (5)
```

The left reduced type is coordinatewise fixed.  Equation (4) says (5) is
polynomial only when the right reduced type is also the identity, namely
when `nu=(d^r)`.  This completes the rectangular classification.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter; standard
library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
shasum -a 256 -c SHA256SUMS
```

The checker reconstructs the full formula for all 35 internal cycle-type
triples through width three, compares 32 definition-level fixed counts,
and performs exact rational divisibility on all 3,582 ordered endpoint
partition pairs through width ten.  Exactly 27 pairs are polynomial, all
the synchronized rectangular pairs predicted by (2).  It also checks all
128 nonidentity one-sided cases in that range.
It additionally constructs an exact cyclotomic pole witness for every one
of the 2,647 nonrectangular synchronized cycle types through width twenty;
these finite checks corroborate the uniform partial-fraction proof.

## Literature and novelty boundary

Jiang--Yang--Zhong introduce path block polytopes and establish their
ordinary Ehrhart structure: <https://arxiv.org/abs/2607.22008>.  Stapledon
defines the determinant-normalized equivariant Ehrhart series and allows
nonpolynomial evaluations: <https://arxiv.org/abs/1003.5875>.
Bjoerner--Welker treat weighted Segre products abstractly:
<https://arxiv.org/abs/math/0312516>.  D'Ali--Higashitani's graded-order-
polytope theorem concerns poset automorphisms:
<https://arxiv.org/abs/2505.07623>.

Targeted searches on 2026-09-04 found no primary source applying the
endpoint Hadamard cancellation, the exact one-sided pole theorem, or the
rectangular classification to path block polytopes.  Novelty is
search-relative only; no historical-priority claim is made.

## Trust boundary

The universal claims rest on (1), maximal root-of-unity pole order, the
differential pole calculation (4), and the scaling and binomial identities
(2),(5).  Finite computation is
corroboration and conjecture evidence, not proof of the unrestricted
classification.  The checker trusts CPython exact integer/list/tuple
semantics and SHA-256.  It uses no floating point, solver, randomness,
external data, generated input, or omitted certificate.
