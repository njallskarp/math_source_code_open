# Cyclotomic-unit obstruction for equal-cycle path-block endpoints

## Result

Let `lambda` and `nu` be endpoint cycle types for the three-block path
polytope, and write `r=len(lambda)` and `s=len(nu)`.  Assume that their
parts have the same positive sum.  Then, if `r=s`, the determinant-normalized
equivariant numerator evaluation is a polynomial **if and only if**

```text
lambda = nu = (d^r)
```

for one positive integer `d`.

The rectangular direction and the cases with unequal maximal-prime profiles
were proved in the earlier endpoint-Hadamard and prime-defect results.  The
new point is a cyclotomic-unit obstruction which rules out every remaining
nonrectangular pair having equally many cycles.  It is uniform in the width,
the number of cycles, the defect, and the maximizing prime; there is no finite
enumeration.

There is also a useful necessary condition without the hypothesis `r=s`.
Suppose a prime `p` is maximizing for both endpoints with common defect `e`.
Put

```text
m = r-e,                 c = s-e,
A = m(m+1)...(m+e),      B = c(c+1)...(c+e).
```

If the leading maximal `p`-cross coefficient cancels, then

```text
v_p(A) = v_p(B) = v,
A/p^v + B/p^v = 0  (mod p).                              (1)
```

Consequently failure of (1) is an exact, all-parameter nonvanishing
certificate for the cyclotomic cross jet.  When `r=s`, one has `m=c` and
`A=B`; for odd `p`, (1) would read `2A/p^v=0 (mod p)`, which is impossible.
For `p=2`, the two leading cross constants already have the same positive
real phase and cannot cancel.

This closes the equal-cycle stratum, but it does not close the remaining
equal-width problem with `r != s`.  In particular, the height-2095 cube-root
family has `(r,s,e,m,c)=(22,20,14,8,6)` and satisfies (1); the new invariant
therefore respects, rather than contradicts, its three exact cancellations.

## Proof

For a cycle type `tau`, set

```text
Q_tau(t) = product_(a in tau) (1-t^a),
F_tau(t) = 1 / ((1-t) Q_tau(t)).
```

The endpoint formula is

```text
h*_(lambda,nu)(t)
  = (1-t) Q_lambda(t) Q_nu(t) (F_lambda odot F_nu)(t),    (2)
```

where `odot` is coefficientwise (Hadamard) product.  First divide all parts
by their common gcd.  The known scaling identity preserves cycle counts and
polynomiality, and a reduced nonrectangular type has positive prime defect.

If the two prime-defect profiles differ, the prime-defect theorem supplies a
unique maximal cross pole, so (2) is not a polynomial.  It remains to consider
a common profile.  Choose a common maximizing prime `p`, let `e` be the common
defect, and let

```text
m = #{a in lambda : p divides a} = r-e,
c = #{b in nu     : p divides b} = s-e.
```

For the nondivisible parts define

```text
L_lambda = product_(p does not divide a) a,
D_lambda(z) = product_(p does not divide a) (1-z^a),
```

and analogously for `nu`.  At a primitive `p`-th root `zeta`, the two maximal
cross waves have common nominal pole order `m+s=r+c`.  Their leading
coefficient cancels only if

```text
r! (c-1)! L_lambda D_nu(zeta)
  + (m-1)! s! L_nu D_lambda(zeta) = 0.                   (3)
```

For `p=2`, both summands in (3) have the same positive real phase.  Hence
assume that `p` is odd.  Every factor in either `D` has cyclotomic norm `p`,
and both products have `e` factors.  Taking norms in (3), then returning to
(3), gives the two exact conditions

```text
A L_lambda = B L_nu,       D_nu(zeta) = -D_lambda(zeta), (4)
```

where `A` and `B` are the rising products displayed above.

Let `pi=1-zeta` and work in the localization of `Z[zeta]` at its prime above
`p`.  For every positive `a` not divisible by `p`,

```text
(1-zeta^a)/(a(1-zeta)) = 1  (mod pi).                    (5)
```

Indeed `(1-zeta^a)/(1-zeta)=1+zeta+...+zeta^(a-1)`, and reduction modulo
`pi` sends `zeta` to `1` and has residue field `F_p`.  Thus

```text
U_tau = product_(p does not divide a)
          (1-zeta^a)/(a(1-zeta))
```

is a cyclotomic unit at `pi` satisfying `U_tau=1 (mod pi)`, and

```text
D_tau(zeta) = pi^e L_tau U_tau.                           (6)
```

Substituting (6) into (4) eliminates `L_lambda,L_nu` and yields

```text
A U_nu = -B U_lambda.                                     (7)
```

The units have zero `pi`-valuation, while an integer `N` has
`pi`-valuation `(p-1)v_p(N)`.  Therefore (7) first forces
`v_p(A)=v_p(B)=v`.  Divide by `p^v` and reduce modulo `pi`; (5) gives exactly
(1).  This proves the general obstruction.

If `r=s`, then common defect gives `m=c`, hence `A=B`.  The normalized
residue in (1) is twice a nonzero element of `F_p`, impossible because `p` is
odd.  Thus the leading cross coefficient cannot cancel.  The determinant in
(2) has `m+c` zeros at `zeta`, whereas this surviving cross wave has pole
order `m+s=m+c+e`; a pole of order `e>0` remains.  Together with the profile,
binary-prime, scaling, and rectangular cases, this proves the classification.

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

The primary checker verifies the local-ring reduction algebra, the normalized
rising-factorial obstruction, and exact nondivisibility of the leading cross
numerator for three different equal-cycle examples with unique maximizing
primes `3,5,7`.  It also confirms that the height-2095 family passes the
necessary congruence and has its known exact leading cancellation.  These
examples test the implementation; the theorem is the symbolic argument above,
not an endpoint census.

## Literature and scope

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure in <https://arxiv.org/abs/2607.22008>.  Stapledon's equivariant
Ehrhart framework and rational character evaluations are in
<https://arxiv.org/abs/1003.5875> and <https://arxiv.org/abs/2311.17273>.
Bjoerner--Welker treat weighted Segre products in
<https://arxiv.org/abs/math/0312516>.  Rubinstein--Fel describe restricted
partition functions and their Sylvester waves in
<https://arxiv.org/abs/math/0304356>.

Targeted graph and primary-source searches on 2026-09-04 found no
family-specific equal-cycle endpoint classification or the normalized
rising-factorial congruence (1).  This is search-relative novelty, not a claim
of historical priority.

The result concerns one element's determinant-normalized character evaluation.
It does not imply whole-action effectiveness.  The unresolved core consists of
equal-width, unequal-cycle, common-profile pairs for which (1) holds and every
maximizing-prime cross jet would have to cancel through its full defect length.

## Trust boundary

The universal statement depends on the independently reviewed endpoint formula
and prime-defect reduction, plus the displayed local cyclotomic-unit argument.
The standard-library and independent SymPy checkers verify exact examples and
the algebraic reductions but do not replace the universal proof.  They trust
CPython integer arithmetic, SymPy's exact polynomial arithmetic, SHA-256, and
Git object integrity.  There is no floating point, randomness, solver,
generated input, private state, database, binary, large certificate, or omitted
finite search.
