# The cubic endpoint residue module

## Result

This package gives an arity-independent equality criterion for the complete
primitive-cubic endpoint-wave transform modulo the third power of the ramified
prime.  It is the structural continuation of the degree-five transform proved
in `path_block_cubic_lift`; it does not extend a coefficient prefix or enumerate
endpoint partitions.

Let `zeta` be a primitive cube root, `pi=1-zeta`, and

```text
R = Z[zeta]/(pi^3),             S = R[X]/(X^6).
```

For an endpoint cycle type `tau`, let

```text
q = #{a in tau : 3 divides a},
e = #{a in tau : 3 does not divide a},
n_r = #{a in tau : a = r mod 9}       (r=1,2,4,5,7,8).
```

Assume `q>0`, so that the primitive-cubic wave is present.  Define

```text
b = n_2+n_5+n_8                         mod 3,
c = n_4+2n_5+2n_7+n_8                  mod 3,

rho(d) = d                              if 1 <= d <= 5,
         6+((d-6) mod 9)                if d >= 6.
```

Then the complete normalized endpoint transform `H_tau(pi X) mod pi^3` is
determined by the five-entry signature

```text
Sigma(tau) = (e mod 27, b, c, rho(q), rho(q+e+1)).        (1)
```

More precisely, (1) gives an exact cross-product test for equality, described
below.  It handles the small-pole boundary as well as arbitrary cycle count and
arbitrarily large cycle lengths.

## The finite local module

For `3` not dividing `a`, put

```text
U_a = 1-(a-1)pi X/2 +(a-1)(a-2)pi^2 X^2/6,

E_a = 1 + sum_(j=1)^3 (-1)^(j+1)
            zeta^a binom(a,j) pi^j X^j/(1-zeta^a),
```

and put

```text
V = 1-pi X+(pi-1)X^2.
```

All expressions in this section lie in `S`.  Let

```text
g_r = (E_r^(-1),U_r^(-1))       for r=1,2,4,5,7,8,
g_0 = (V^(-1),V^(-1)),
h_2 = g_2 g_1^(-1),
h_4 = g_4 g_1^(-1).
```

The local factors depend only on the cycle length modulo nine, and direct
expansion gives

```text
g_1 = g_1,
g_2 = g_1 h_2,
g_4 = g_1 h_4,
g_5 = g_1 h_2 h_4^2,
g_7 = g_1 h_4^2,
g_8 = g_1 h_2 h_4.                                      (2)
```

These generators have the exact independent orders

```text
ord(g_1)=27,   ord(g_0)=9,   ord(h_2)=ord(h_4)=3.        (3)
```

Consequently the group of all normalized local endpoint pairs is

```text
<g_1,h_2,h_4,g_0> = C_27 x C_3 x C_3 x C_9,             (4)
```

of order `2187`.  Including the extra weight `1` from the factor `1-t`, the
two analytic local series have the unique normal form

```text
(Gamma_zeta,Gamma_1)
    = g_1^(e+1) h_2^b h_4^c g_0^q.                       (5)
```

Thus two endpoint types have the same complete local pair if and only if their
four residues `(e mod 27,b,c,q mod 9)` agree.  This is an exact finite-module
classification, not merely a sufficient congruence.

For transparency, `R` has 27 elements.  If an element is written as
`a+b*zeta`, reduction modulo `pi^3` has the canonical representative

```text
a_0 + b_0*zeta,
a_0 = a mod 3,
b_0 = b-2(a-a_0) mod 9.
```

Expanding (2)--(3) in this model proves all relations.  The verifier also
checks that the `27*3*3*9=2187` displayed normal forms are distinct.  One can
read off independence without a table: write each coefficient uniquely as
`u_0+u_1*pi+u_2*pi^2`, with `u_i` in `{0,1,2}`.  Four coefficient digits of
the second component distinguish all 81 triples `(b,c,q)`, and, after removing
them, three coefficient digits of the first component distinguish all 27
powers of `g_1`.  The exact digit projections are implemented in `verify.py`.

## The whole-transform equality criterion

For `Gamma=sum gamma_i X^i` and pole order `d`, define

```text
T_d(Gamma)
 = sum_(i=0)^(d-1) gamma_i (d-1)_i X^i
       product_(h=1)^(d-i-1)(1+h*pi*X)       mod pi^3,   (6)
```

where `(d-1)_i` is a falling factorial.  The predecessor theorem shows that
`T_d` has degree at most five and

```text
H_tau(pi X) = T_q(Gamma_zeta)/T_(q+e+1)(Gamma_1) mod pi^3.  (7)
```

There is a second uniform compression:

```text
T_(d+9)(Gamma) = T_d(Gamma)                  for d>=6.   (8)
```

Indeed, the falling factorials in (6) are polynomials in `d` with integral
coefficients, hence are periodic modulo 9.  Also

```text
product_(r=1)^9 (1+(d+r)pi X) = 1 mod pi^3:
```

the linear elementary sum is divisible by nine, the quadratic elementary sum
is divisible by three, and every higher term contains `pi^3`.  Terms with
`i>=6` already vanish.  This proves (8), while `rho` retains the genuinely
different orders `1,...,5`.

Given a signature `sigma`, form the local pair from (5), and set

```text
N_sigma = T_(sigma_4)(Gamma_zeta),
D_sigma = T_(sigma_5)(Gamma_1).
```

Both have degree at most five and constant coefficient one.  Therefore, for
any endpoint types `lambda,nu` with cubic waves,

```text
H_lambda(pi X) = H_nu(pi X) mod pi^3

if and only if

N_Sigma(lambda) D_Sigma(nu)
  = N_Sigma(nu) D_Sigma(lambda)              in R[X].    (9)
```

The cross products in (9) have degree at most ten.  Equations (1)--(9) are an
explicit, all-parameter decision procedure requiring only four small residue
counts, two clipped pole orders, and eleven coefficients in a 27-element ring.

The transform is not injective on local signatures.  On the stable stratum
where both pole orders are at least six, the `2187` local signatures yield
exactly `386` rational transforms.  This exact count is a diagnostic of the
nontrivial collision locus; the theorem and equality test do not rely on a
partition census.

## Two checks at opposite scales

The nonrectangular equal-width pair

```text
(6,5,1)   and   (7,3,2)
```

has common signature `(2,1,2,1,4)`.  In fact its normalized cubic transforms
are equal **exactly over `Q(zeta)`**, not only modulo `pi^3`.

Here each endpoint has one part divisible by three, so its primitive-cubic
coefficient wave has degree zero and becomes `1` after leading normalization.
At `1`, include the extra weight from `1-t`; the two four-weight lists are

```text
(1,6,5,1)   and   (1,7,3,2).
```

Both have sum `13` and sum of squares `63`.  For a weight `w`, the normalized
removed denominator is

```text
d_w(u)=(1-(1-u)^w)/(w*u).
```

Through degree three, direct expansion gives

```text
log d_w(u)
 = -(w-1)u/2
   +(w-1)(w-5)u^2/24
   +(w-1)(w-3)u^3/24             mod u^4.
```

Thus the normalized fourfold local series through its complete required jet
depends only on the number of weights and their first two power sums.  The
normalized identity waves agree, as do the constant cubic waves, proving the
exact rational-transform identity.  Direct binomial-basis reconstruction gives
the same descending normalized identity-wave coefficient vector on both sides:

```text
(1, 39/2, 111, 689/4).
```

This is an explicit nonrectangular
counterexample to injectivity of the endpoint transform, though not to the
earlier nonpolynomiality theorem: its leading cross coefficients have the
same rather than opposite phase.

For the height-2095 all-parameter family, the two fixed signatures begin

```text
left:  (14,1,1,8,...),
right: (14,1,0,6,...).
```

The criterion reconstructs the previously proved difference

```text
H_left(pi X)-H_right(pi X) = pi^2 X^3 mod (pi^3,X^14).
```

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

The primary checker verifies 120 weight-shift identities, the six residue
relations and exact generator orders, all 2187 distinct local normal forms,
39,366 transform-period identities, all 2187 stable signatures and their 386
rational classes, 108 separating coordinate-digit projections, the small-pole
nonrectangular moment identity, and the height-2095
associated-graded difference.  These are exhaustive calculations in a fixed
27-element algebra, not an enumeration of endpoint partitions.

## Literature and scope

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure in <https://arxiv.org/abs/2607.22008>.  Stapledon's equivariant
Ehrhart framework is developed in <https://arxiv.org/abs/1003.5875> and
<https://arxiv.org/abs/2311.17273>.  Rubinstein--Fel give explicit restricted-
partition/Sylvester-wave formulas in <https://arxiv.org/abs/math/0304356>.
O'Sullivan treats complete Laurent expansions of restricted-partition products
at roots of unity in <https://arxiv.org/abs/2001.08115>.

A graph search and a targeted primary-source search on 2026-09-04 found no
path-block-specific quotient (4), residue signature (1), pole-period identity
(8), or cross-product criterion (9).  Novelty is search-relative, not a claim
of historical priority.

This theorem classifies equality at the complete `pi^3` layer for the cubic
wave.  It does not classify equality over the full cyclotomic integer ring,
prove polynomiality of an equivariant numerator, handle endpoints with no
cubic pole, or establish whole-action effectiveness.  It closes the bounded
cubic residue-module phase; further same-author work should not add another
fixed ramified layer without independent review or a new all-prime invariant.

## Trust boundary

The proof depends on the previously established degree-five cubic transform,
the displayed local-factor reductions, and exact arithmetic in
`Z[zeta]/(pi^3)`.  The universal content is the modulo-nine factor reduction,
the finite-module presentation, the block-of-nine proof of transform
periodicity, and the degree-ten cross-product identity.  The standard-library
checker exhausts the fixed finite algebra and hashes a compact report.  The
independent SymPy checker reconstructs the small-pole pair directly from exact
coefficient waves in `Q(zeta)` and verifies all eleven exact equalities without
importing primary code.

There is no floating point, randomness, solver, external dataset, generated
input, private state, database, binary, large certificate, raw endpoint census,
or omitted search dump.
