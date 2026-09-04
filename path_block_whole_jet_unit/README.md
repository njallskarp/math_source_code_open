# A whole-jet unit obstruction for path-block endpoints

## Result

Let `lambda` and `nu` be equal-width endpoint cycle types in the three-block
path-polytope formula.  Suppose an odd prime `p` is maximizing for both
endpoints with the same positive defect `e`.  Put

```text
m = #{a in lambda : p divides a},     c = #{b in nu : p divides b},
A = m(m+1)...(m+e),                   B = c(c+1)...(c+e).
```

If `p` divides neither `A` nor `B`, then the two maximal `p`-cross waves
cannot cancel through the full defect-length jet.  Consequently the
determinant-normalized equivariant numerator evaluation is not a polynomial.

This is uniform in the width, the cycle counts, the prime, and the defect.
It is not a finite endpoint census or an extension of the known three-term
prefix.  Its invariant is the complete normalized defect jet modulo the
ramified uniformizer `pi=1-zeta_p`:

```text
K_(q,e)(X)
  = sum_(i=0)^(e-1) (-1)^i binom(e+i,i)
                       (q-1)(q-2)...(q-i) X^i    in F_p[X].       (1)
```

For an endpoint having `q` parts divisible by `p`, its whole normalized jet
reduces to `K_(q,e)`.  Thus full cross-wave cancellation would imply the
polynomial identity

```text
K_(m,e)(X) = K_(c,e)(X)  in F_p[X].                            (2)
```

When `e=1`, leading cancellation is already impossible: its cyclotomic-factor
condition would say `1-zeta^b=-(1-zeta^a)` for two nonzero residues, hence
`zeta^a+zeta^b=2`, contradicting the equality case of the triangle inequality.
Now assume `e>=2`.  The factorial-block unit hypothesis implies `e+1<p`.
Comparing the linear terms in the *single whole-jet identity* (2) then gives
`m=c (mod p)`.  Hence `A=B (mod p)`.  But exact leading cancellation also
forces `A+B=0 (mod p)`; this is impossible for odd `p` because `A` is a unit.

The unit condition is essential to this stated theorem.  When `p` divides
both rising blocks, division by their common valuation changes the residue
lattice and the last contradiction need not apply.  The height-2095
three-cancellation family has `(p,e,m,c)=(3,14,8,6)` and lies precisely in
that ramified boundary.

## Proof of the whole-jet reduction

For a cycle type `tau`, write

```text
F_tau(x) = 1 / ((1-x) product_(a in tau) (1-x^a)).
```

Let `zeta=zeta_p`, let `q` be the number of `p`-divisible parts, and put
`r=q+e`.  Define the analytic local factors by

```text
F_tau(zeta(1-u)) = u^(-q) C_zeta(u),
F_tau(1-u)       = u^(-(r+1)) C_1(u).
```

The extra denominator `1-x` is one of the `e+1` factors nonvanishing at
`zeta`.  Work in the localization of `Z[zeta]` at `pi=1-zeta` and substitute
`u=pi v`.  After division by constant terms, every `p`-divisible factor is
`1 modulo pi`, whereas every nonvanishing factor satisfies

```text
(1-zeta^a) / (1-zeta^a(1-pi v)^a) = (1+v)^(-1)  (mod pi).
```

Therefore the entire local power series, not merely a fixed prefix, obeys

```text
C_zeta(pi v)/C_zeta(0) = (1+v)^(-(e+1))  (mod pi),
C_1(pi v)/C_1(0)       = 1               (mod pi).       (3)
```

For a pole of order `q`, the coefficient wave is recovered exactly from
`C(u)=sum c_i u^i` by

```text
P(n) = sum_(i=0)^(q-1) c_i binom(n+q-i-1,q-i-1).          (4)
```

Set `n=y/pi`, divide (4) by its leading monomial, and retain the first `e`
inverse powers of `y`.  Equation (3) supplies
`(-1)^i binom(e+i,i)` and the binomial basis supplies the falling factorial
`(q-1)...(q-i)`, giving (1).  Because `p` divides neither `A` nor `B`, no
interval of `e+1` consecutive integers in either rising block contains a
multiple of `p`; in particular `e+1<p`.  All factorial denominators appearing
before degree `e` are consequently `p`-units, so this reduction takes place
in the local integral lattice without hidden denominators.

Let `P_(tau,zeta)` and `P_(tau,1)` denote the two waves and normalize
`P_(tau,zeta)/P_(tau,1)` by its leading coefficient.  Equations (3)--(4)
show that its complete defect jet is `K_(q,e)` modulo `pi`.  If the two cross
waves

```text
P_(lambda,zeta) P_(nu,1) + P_(lambda,1) P_(nu,zeta)
```

cancel in all `e` relevant orders, their leading coefficients are opposite
and their normalized whole jets are equal.  This proves (2).

If `e=1`, the necessary leading cyclotomic-factor identity is

```text
1-zeta^b = -(1-zeta^a)
```

for the unique nondivisible parts `a,b` modulo `p`.  It would give
`zeta^a+zeta^b=2`.  Since both summands have modulus one, equality in the
triangle inequality forces both to equal one, contrary to `p` dividing
neither `a` nor `b`.  Thus assume `e>=2`, so the coefficient of `X` occurs in
the full jet.  That coefficient in (1) is `-(e+1)(q-1)`, and (2) together
with `e+1<p` gives `m=c (mod p)`.  The earlier cyclotomic-unit leading
calculation says that leading cancellation requires

```text
A + B = 0 (mod p)                                             (5)
```

when both blocks are `p`-units.  Since a rising product depends only on its
initial residue, `m=c (mod p)` gives `A=B (mod p)`.  Equations (5) and
`p` odd would force the unit `A` to vanish modulo `p`, a contradiction.

Finally, the determinant in the endpoint formula has a zero of order `m+c`
at `zeta`.  The two maximal cross waves have nominal pole order
`m+s=r+c=m+c+e`; failure of full `e`-term cancellation leaves a pole after
determinant multiplication.  All other root pairings have smaller order by
the maximal-prime reduction.  This proves nonpolynomiality.

## A hard exact witness

The checker uses the equal-width pair

```text
lambda = (14,13,7,7,7,7,7,7,7,6,2,1),
nu     = (12,8,7,7,7,7,7,7,7,7,7,1,1).
```

Both have width `85`, unique maximizing prime `7`, and common defect `4`.
Here `(m,c)=(8,9)`, and the blocks `8...12` and `9...13` are 7-adic units.
The leading primitive-seventh-root cross coefficient cancels exactly, so the
earlier leading obstruction is silent.  Exact computation in
`Q[zeta_7]` finds that the next coefficient survives.  The whole-jet residues
are `K_(8,4)=1` and `K_(9,4)=1+2X+...` modulo 7, certifying that complete
cancellation is impossible.

This witness tests the implementation; the theorem is the valuation and
divisibility proof above, not a claim inferred from the example.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter.  The primary
checker uses only the standard library.  The independent checker pins SymPy
1.14.0 and imports no primary code.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
shasum -a 256 -c SHA256SUMS
python3 independent_sympy_check.py
```

## Literature and scope

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure in <https://arxiv.org/abs/2607.22008>.  Stapledon's equivariant
Ehrhart framework is developed in <https://arxiv.org/abs/1003.5875> and
<https://arxiv.org/abs/2311.17273>.  Rubinstein--Fel describe Sylvester waves
for restricted partitions in <https://arxiv.org/abs/math/0304356>.
O'Sullivan gives systematic Laurent expansions of restricted-partition
products at roots of unity in <https://arxiv.org/abs/2001.08115>.

A targeted graph and primary-source search on 2026-09-04 found no
path-block-specific whole-jet reduction (1) or the resulting factorial-block
unit obstruction.  This is search-relative novelty, not a claim of historical
priority.

The result excludes the complete unramified factorial-block stratum.  It does
not settle cases in which a maximizing prime divides both rising blocks;
those require a saturated jet lattice, a norm/resultant argument retaining
the common valuation, or an exact full-cancellation construction.  It also
concerns one determinant-normalized character evaluation and does not imply
whole-action effectiveness.

## Trust boundary

The universal theorem depends on the independently reviewed endpoint formula
and prime-defect reduction, the direct defect-one phase argument, the earlier
cyclotomic-unit leading calculation, and the displayed local valuation proof.
The primary checker reconstructs
the hard witness in the exact field `Q[zeta_7]` and verifies the finite-field
whole-jet polynomials.  The independent SymPy checker repeats the local-wave
calculation without importing primary code.  These exact examples corroborate
but do not replace the universal proof.  The package trusts CPython integer
and `Fraction` semantics, SymPy 1.14.0 exact algebra, SHA-256, and Git object
integrity.  There is no floating point, randomness, solver, external dataset,
generated input, private state, binary, large certificate, or omitted census.
