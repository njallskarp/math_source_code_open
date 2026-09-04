# The complete cubic-root lift through the second ramified layer

## Result

This package lifts the saturated path-block endpoint jet from its residue field
to the complete quotient by `pi^3` at a primitive cube root.  It does not extend
the jet one coefficient at a time.

Let `zeta` be a primitive cube root, `pi=1-zeta`, and let `tau` be an endpoint
cycle type.  Put

```text
q = #{a in tau : 3 divides a},       e = #tau-q.
```

For the restricted-partition series

```text
F_tau(t)=1/((1-t) product_(a in tau)(1-t^a)),
```

let `P_(tau,zeta)` and `P_(tau,1)` be its coefficient-polynomial waves at
`zeta` and `1`.  Normalize each by its leading monomial, take their quotient
`H_tau`, and substitute the inverse-degree variable `z=pi X`.

The complete formal series `H_tau(pi X) mod pi^3` is the quotient of two
polynomials of degree at most five, uniformly in the pole orders, defect,
width, and individual cycle lengths.  The construction below gives those
polynomials exactly.

As an application, for every `t>=0` in the height-2095 family

```text
lambda_t = (9,6,[3(2t+1)]^3,3^3 ; 7,4^2,2^4,1^7),
nu_t     = (3(t+2),3(2t+1),3(3t+1),3^3 ; 11,7,4^4,1^8),
```

the entire defect-14 difference satisfies

```text
H_(lambda_t)(pi X)-H_(nu_t)(pi X)
       = pi^2 X^3                  mod (pi^3,X^14).       (1)
```

Thus the first residue layer at height 2273 is blind, but the next nonzero
associated-graded layer is the single monomial `X^3`.  Formula (1) holds for
the all-parameter family, not just for checked values of `t`.

## Universal local factors modulo `pi^3`

The exact relation in `Z[zeta]` is

```text
pi^2-3pi+3=0.
```

For a cycle length `a=3k`, remove the vanishing linear factor and normalize
the constant term:

```text
d_a(pi X)
 = (1-(1-pi X)^a)/(a pi X)
 = sum_(j=0)^(a-1) (-1)^j binom(a-1,j) pi^j X^j/(j+1).
```

The same valuation estimate used for the first residue layer now leaves only
degrees zero, one, and two modulo `pi^3`.  Indeed, for `j>=3`,

```text
j-2 v_3(j+1) >= 3.
```

At degree one,

```text
-(3k-1)pi/2 = -pi mod pi^3,
```

because the difference is a multiple of `3pi`.  At degree two,

```text
binom(3k-1,2)pi^2/3
 = ((3k-1)(3k-2)/2)(pi-1)
 = pi-1 mod pi^3,
```

because `(3k-1)(3k-2)/2=1 mod 9`.  Therefore every positive multiple of
three has the same *whole* local factor

```text
V(X)=1-pi X+(pi-1)X^2 mod pi^3.                           (2)
```

This remains true when `9` divides `a`; the quotient `k` has disappeared.

For `3` not dividing `a`, define the normalized factors

```text
U_a(X)
 = 1-(a-1)pi X/2 +(a-1)(a-2)pi^2 X^2/6,                 (3)

E_a(X)
 = 1 + sum_(j=1)^3 (-1)^(j+1)
       zeta^a binom(a,j) pi^j X^j/(1-zeta^a).            (4)
```

All omitted terms in (3)--(4) have `pi`-valuation at least three.  Here `U_a`
is the factor at `1`, and `E_a` is the nonvanishing factor at `zeta`.  Include
the extra weight `a=1` belonging to `1-t` and put

```text
Gamma_zeta(X) = V(X)^(-q) product_(3 does not divide a) E_a(X)^(-1),
Gamma_1(X)    = V(X)^(-q) product_(3 does not divide a) U_a(X)^(-1),   (5)
```

where both products range over `{1} union tau`.  Equations (2)--(5) give the
entire normalized analytic local series modulo `pi^3`.

## The bounded whole-wave transform

For `Gamma(X)=sum gamma_i X^i` and a pole of order `d`, define

```text
T_d(Gamma)
 = sum_(i=0)^(d-1) gamma_i (d-1)_i X^i
       product_(h=1)^(d-i-1)(1+h pi X)       mod pi^3.    (6)
```

This is the exact binomial-basis reconstruction after substituting
`n=y/pi`, normalizing the leading monomial, and setting `X=1/y`.  Consequently

```text
H_tau(pi X)
 = T_q(Gamma_zeta)(X)/T_(q+e+1)(Gamma_1)(X) mod pi^3.     (7)
```

Although (6) is written without an artificial cutoff, it has degree at most
five modulo `pi^3`.  If `i>=6`, the falling factorial `(d-1)_i` contains two
multiples of three and hence has `pi`-valuation at least four.  If `3<=i<=5`,
it contains one multiple of three, so every positive-degree correction from
the last product raises the valuation to at least three.  If `i<=2`, only the
first two correction degrees can survive.  Hence no term of degree greater
than five remains.  Equation (7) is therefore a width-uniform rational
encoding of an arbitrarily long jet.

## Derivation for the all-parameter family

The nondivisible parts of `lambda_t` and `nu_t` are fixed, their divisible
counts are respectively eight and six, and every `t`-dependent part is
divisible by three.  By (2), changing `t` cannot change either lifted quotient
in (7) modulo `pi^3`.  It is therefore enough to reduce the two fixed rational
transforms once, at `t=0`.  Exact arithmetic in
`Q[zeta]/(zeta^2+zeta+1)` gives (1).

The coefficients of `X^0,X^1,X^2` in the difference vanish exactly, while
the scaled coefficient of `X^3` has `pi`-valuation two and residue one after
division by `pi^2`.  Every other coefficient through `X^13` has valuation at
least three.  Combined with the exact leading identities already established
for this family, this recovers three and only three leading cross-wave
cancellations.  The nominal cross pole has order `28`, the endpoint
determinant has zero order `14`, and the residual pole has order `11`.

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

The primary checker verifies 2,460 coefficients from complete normalized
factors of weights `3,6,...,120`, including all multiples of nine in that
range; compares the lifted rational transform against the original exact
coefficient waves; checks the entire fourteen-term associated-graded
difference for parameters `0,...,12`; and tests the uniform degree-five bound
through pole order `61`.  Those finite checks test the implementation but do
not replace the valuation proof or the parameter-independence argument.

## Literature and scope

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure in <https://arxiv.org/abs/2607.22008>.  Stapledon's equivariant
Ehrhart framework is developed in <https://arxiv.org/abs/1003.5875> and
<https://arxiv.org/abs/2311.17273>.  Rubinstein--Fel describe Sylvester waves
for restricted partitions in <https://arxiv.org/abs/math/0304356>.
O'Sullivan studies complete Laurent expansions of restricted-partition
products at roots of unity in <https://arxiv.org/abs/2001.08115>.

A targeted graph and primary-source search on 2026-09-04 found no path-block-
specific ramified lift (2)--(7), uniform degree-five compression, or
associated-graded identity (1).  This is search-relative novelty, not a claim
of historical priority.

This result explains the entire next local layer for cube-root endpoint waves
and closes the prescribed bounded lift for the height-2095 family.  It is not
a classification of equality in (7), does not settle all residue-blind endpoint
pairs, and does not imply whole-action effectiveness.  Further progress should
seek an arity-independent valuation or resultant criterion across arbitrary
endpoint pairs, not another fixed `pi`-adic layer of this family.

## Trust boundary

The theorem uses the independently reviewed endpoint Hadamard formula and
prime-defect reduction, the displayed local valuation arguments, and exact
binomial-basis reconstruction.  The standard-library verifier represents
`Q(zeta_3)` as rational pairs modulo `zeta^2+zeta+1` and computes local
valuations from exact norms.  The independent checker separately constructs
SymPy 1.14.0's algebraic-number field and reconstructs all fourteen normalized
coefficients.  There is no floating point, randomness, solver, external
dataset, generated input, private state, binary, large certificate, or omitted
search dump.
