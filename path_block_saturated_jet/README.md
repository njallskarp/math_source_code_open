# A saturated whole-jet residue for path-block endpoints

## Result

Let `lambda` and `nu` be equal-width endpoint cycle types in the three-block
path-polytope formula.  Suppose an odd prime `p` is maximizing for both
endpoints with the same positive defect `e`.  For one endpoint `tau`, put

```text
q = #{a in tau : p divides a},        pi = 1-zeta_p.
```

Let `P_(tau,zeta)` and `P_(tau,1)` be the coefficient-polynomial waves coming
from the poles of

```text
F_tau(t) = 1 / ((1-t) product_(a in tau) (1-t^a))
```

at `zeta=zeta_p` and at `1`.  Divide each wave by its leading monomial, form
their quotient `H_tau`, substitute the inverse-degree variable `z=pi X`, and
truncate modulo `X^e`.  Then `H_tau(pi X)` is integral at `pi`, and its complete
residue jet depends only on `(q,e,p)`.  Explicitly, define the diagonal falling-
factorial transform

```text
D_d(sum_i f_i X^i) = sum_i (d-1)_i f_i X^i,
(a)_i = a(a-1)...(a-i+1).
```

The universal residue is

```text
J_(q,e,p)(X)
 = D_q((1-X^(p-1))^(-q) (1+X)^(-(e+1)))
   / D_(q+e+1)((1-X^(p-1))^(-q))       mod (p,X^e).       (1)
```

This is a whole-jet invariant, not a finite coefficient prefix.  Since every
falling factorial of length at least `p` is zero modulo `p`, (1) has the closed
rational form

```text
J_(q,e,p)(X) = N_(q,e,p)(X) / E_(q,e,p)(X) mod (p,X^e),   (2)

N = sum_(i=0)^(p-2) (-1)^i binom(e+i,i) (q-1)_i X^i
      - [p|q][p|e] X^(p-1),
E = 1 - q_bar [p|(q+e+1)] X^(p-1).
```

Terms of degree at least `e` are discarded, `q_bar` is `q` modulo `p`, and
brackets denote indicator functions.  Thus an apparently unbounded defect jet
is encoded by two polynomials of degree at most `p-1`.

If the two maximal cross waves cancel in all `e` relevant orders, their leading
coefficients are opposite and their normalized quotients are equal.  Therefore

```text
J_(m,e,p) = J_(c,e,p) in F_p[X]/(X^e)                    (3)
```

is necessary for full cancellation, where `m` and `c` are the respective
numbers of `p`-divisible parts.  Whenever (3) fails, a pole remains after the
endpoint determinant is applied, so the determinant-normalized equivariant
numerator evaluation is not a polynomial.

Unlike the earlier factorial-block-unit theorem, this statement has no
hypothesis on the `p`-valuations of `m(m+1)...(m+e)` and
`c(c+1)...(c+e)`.  It therefore supplies a genuine invariant on the saturated
stratum.

## Cyclotomic local proof

Write

```text
F_tau(zeta(1-u)) = u^(-q) C_zeta(u),
F_tau(1-u)       = u^(-(q+e+1)) C_1(u).
```

First consider a part `a` divisible by `p`.  After its vanishing factor is
removed and the constant term is normalized, its denominator factor is

```text
d_a(pi X)
 = (1-(1-pi X)^a)/(a pi X)
 = sum_(j=0)^(a-1) (-1)^j binom(a-1,j)/(j+1) pi^j X^j.  (4)
```

The `pi`-valuation of the `j`-th coefficient is at least

```text
j - (p-1) v_p(j+1).
```

If `s=v_p(j+1)`, then `j >= p^s-1 >= s(p-1)`.  Equality for positive `j`
occurs only at `s=1`, `j=p-1`.  Lucas' theorem gives
`binom(a-1,p-1)=1 mod p`.  Finally,

```text
p/pi^(p-1)
 = product_(h=1)^(p-1) (1-zeta^h)/(1-zeta)
 = (p-1)! = -1 mod pi,
```

so `pi^(p-1)/p=-1 mod pi`.  It follows from the entire polynomial (4), not
from a prefix computation, that

```text
d_a(pi X) = 1-X^(p-1) mod pi.                            (5)
```

This is independent of `a`, even when `p^2` divides `a`.  A part not divisible
by `p` has normalized denominator `1 mod pi` at `1`.  At `zeta`, its normalized
nonvanishing denominator is

```text
(1-zeta^a(1-pi X)^a)/(1-zeta^a) = 1+X mod pi.            (6)
```

The extra factor `1-t` contributes one more copy of (6).  Inverting all
denominators in (5)--(6) therefore proves the full formal-series congruences

```text
C_zeta(pi X)/C_zeta(0)
   = (1-X^(p-1))^(-q) (1+X)^(-(e+1)) mod pi,
C_1(pi X)/C_1(0)
   = (1-X^(p-1))^(-q)                    mod pi.          (7)
```

These congruences hold in the complete local power-series ring; no degree-by-
degree extrapolation is used.

For a pole of order `d`, if `C(u)=sum_i c_i u^i`, its coefficient wave is

```text
P(n) = sum_(i=0)^(d-1) c_i binom(n+d-i-1,d-i-1).         (8)
```

Substitute `n=y/pi`, divide by the leading monomial, and put `X=1/y`.  Reducing
the resulting integral series modulo `pi` changes (8) exactly into `D_d`.
Applying this once at `zeta` and once at `1` gives (1).  For `i>=p`, `(d-1)_i`
contains a multiple of `p`.  At `i=p-1`, it is `-1 mod p` exactly when `p|d`
and is zero otherwise.  Also

```text
binom(e+p-1,p-1) = [p|e] mod p.
```

These observations reduce (1) to (2).  Equation (3) follows by dividing the
two normalized cross-wave products after their leading coefficients cancel.

## An exact saturated witness

At a primitive fifth root, take

```text
lambda = (12,7,5,5,5,1),
nu     = (10,5,5,5,4,3,3).
```

Both types have width `35`, unique maximizing prime `5`, and common defect
`e=3`; their divisible counts are `(m,c)=(3,4)`.  Both rising blocks are
divisible by five:

```text
A = 3*4*5*6 = 360,       B = 4*5*6*7 = 840.
```

The products of nondivisible parts are `L_lambda=84` and `L_nu=36`, so
`A L_lambda = B L_nu = 30240`.  If
`D_tau(z)=product_(5 does not divide a)(1-z^a)`, direct reduction modulo
`Phi_5(z)` gives

```text
D_lambda = -1-2z-3z^2+z^3,
D_nu     =  1+2z+3z^2-z^3 = -D_lambda.
```

These are the exact leading-cancellation identities.  The old leading
obstruction is therefore silent.  The new whole-jet residues are

```text
J_(3,3,5) = 1+2X,        J_(4,3,5) = 1+3X mod X^3.
```

Hence the next pole coefficient survives.  Direct reconstruction in
`Q(zeta_5)` confirms exactly one leading cancellation: the nominal cross-pole
order is `10`, the actual order is `9`, the determinant zero has order `7`,
and a pole of order `2` remains.

## Exact explanation of the cube-root blind stratum

For the height-2095 family, `(p,e,m,c)=(3,14,8,6)`.  Formula (2) gives

```text
J_(8,14,3) = J_(6,14,3) = 1 mod X^14.
```

Thus the first saturated residue lattice cannot distinguish that family at
any of the fourteen relevant coefficients.  The previously observed three
exact cancellations are consistent with a structural loss of all information
modulo `pi`, rather than with an insufficiently long prefix.  Any continuation
on that family must pass to the next `pi`-adic layer (or use a different norm
or resultant invariant); extending the coefficient prefix in the same residue
field cannot help.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter.  The primary
checker uses only the standard library.  The independent checker pins SymPy
1.14.0 and imports no primary code.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
shasum -a 256 -c SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 independent_sympy_check.py
```

The primary verifier checks the full local-factor residue for 52 weights,
including weights divisible by `p^2`; compares the transformed and closed
forms of the universal jet in 1,996 parameter triples; reconstructs the exact
fifth-root witness; and confirms the cube-root blind stratum.  These finite
checks test the implementation but do not replace the displayed universal
proof.

## Literature and scope

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure in <https://arxiv.org/abs/2607.22008>.  Stapledon's equivariant
Ehrhart framework is developed in <https://arxiv.org/abs/1003.5875> and
<https://arxiv.org/abs/2311.17273>.  Rubinstein--Fel describe Sylvester waves
for restricted partitions in <https://arxiv.org/abs/math/0304356>.
O'Sullivan studies complete Laurent expansions of restricted-partition
products at roots of unity in <https://arxiv.org/abs/2001.08115>.

A targeted primary-source and graph search on 2026-09-04 found no path-block-
specific saturated residue (1), local identity (5), or compression (2).  This
is search-relative novelty, not a claim of historical priority.

The result gives a uniform necessary condition for full maximal-cross-wave
cancellation and excludes every parameter pair for which the two rational
residues differ.  It does not prove that equality of the residues is sufficient,
does not settle the cube-root blind stratum, and does not by itself classify all
equal-width endpoint pairs.  It concerns one determinant-normalized character
evaluation and does not imply whole-action effectiveness.

## Trust boundary

The theorem depends on the independently reviewed endpoint Hadamard formula
and prime-defect reduction, the displayed local valuation argument, Lucas'
theorem, and the exact wave transform (8).  The standard-library verifier uses
exact integers, `Fraction`, and arithmetic in
`Q[z]/(1+z+z^2+z^3+z^4)`.  The independent checker separately reconstructs
the witness using SymPy 1.14.0's algebraic-number field.  There is no floating
point, randomness, solver, external dataset, generated input, private state,
binary, large certificate, or omitted search dump.
