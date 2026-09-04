# Three exact maximal-root jet cancellations for path-block endpoints

## Result

Let `zeta` be a primitive cube root of unity.  For every integer `t >= 0`,
consider the following endpoint cycle types (superscripts denote
multiplicity):

```text
lambda_t = (9, 6, [3(2t+1)]^3, 3^3 ; 7, 4^2, 2^4, 1^7),
nu_t     = (3(t+2), 3(2t+1), 3(3t+1), 3^3 ; 11, 7, 4^4, 1^8).
```

The semicolon only separates the parts divisible by three from the other
parts.  Both partitions have width `63+18t`.  Their prime-defect profiles are

```text
delta_lambda = delta_nu = 14,
P_lambda = P_nu = {3}.
```

Thus three is the **unique** maximizing prime on both sides.  Nevertheless,
the two maximal cross waves at `zeta` cancel in their first three consecutive
pole orders.

More precisely, put

```text
F_tau(x) = 1 / ((1-x) product_(a in tau) (1-x^a))
```

and let `P_(tau,alpha)(n)` be the coefficient polynomial belonging to the
pole of `F_tau` at `alpha`.  The relevant cross polynomial is

```text
R_t(n) = P_(lambda_t,zeta)(n) P_(nu_t,1)(n)
       + P_(lambda_t,1)(n) P_(nu_t,zeta)(n).
```

Each summand nominally has degree 27.  If the first is normalized as

```text
L n^27 (1+a_1/n+a_2/n^2+a_3/n^3+...),
```

then the second has leading coefficient `-L` and normalized coefficients
`b_i`.  Exact expansion in `Q(zeta)` gives

```text
a_1-b_1 = 0,
a_2-b_2 = 0,
a_3-b_3 = (40895-2520t(t+1))(1+2zeta)/12.                 (1)
```

The last quantity never vanishes for integral `t`: `t(t+1)` is even, so
`2520t(t+1)` is divisible by 5040, whereas `40895` is not.  Hence `R_t` has
degree exactly 24, or pole order 25.  The determinant factor has a zero of
order `8+6=14` at `zeta`.  Every nontrivial--nontrivial pole pairing has order
at most `8+6-1=13`, so none can affect the surviving cross term.  The
equivariant numerator therefore has a primitive-cube-root pole of exact order
11 for every `t >= 0`.

This is not a counterexample to the conjectural classification of polynomial
evaluations: every member is nonpolynomial.  It is an all-parameter
counterexample to any proposed proof asserting that one of the first three
maximal cross-jet orders must survive.  A successful uniform argument must use
at least the fourth normalized coefficient, the complete defect-length jet,
or a genuinely different root/profile invariant.

## Exact derivation

The numbers of cube-divisible parts are `m=8` and `c=6`; the cycle counts are
`r=22` and `s=20`, so both defects are 14 and the nominal cross order is

```text
m+s = r+c = 28.
```

For the nondivisible parts, write `L_tau` for their product and
`D_tau(z)=product(1-z^a)`.  Directly,

```text
L_lambda = 1792,              L_nu = 19712 = 11 L_lambda,
D_nu(zeta) = -D_lambda(zeta),
22! 5! L_lambda = 7! 20! L_nu.
```

The last two identities are exactly the leading-cross cancellation criterion.
For a cube-root pole, define

```text
S_tau = sum_(a=2 mod 3) a - sum_(a=1 mod 3) a - 1.
```

Here `S_lambda=-15`, `S_nu=-21`, and

```text
(m-1)S_lambda = -105 = (c-1)S_nu,
```

which, together with equal width, cancels the next normalized coefficient.
For the cube-divisible parts divided by three, the two multisets are

```text
X_t = (3,2,(2t+1)^3,1^3),
Y_t = (t+2,2t+1,3t+1,1^3).
```

They satisfy

```text
sum X_t - sum Y_t = 4,
7(sum x^2 - 19) = 84t(t+1) = 6(sum y^2 - 9).              (2)
```

Substitution of (2) in the second local cumulant cancels the third pole order.
One further exact local expansion gives (1).

For completeness, if

```text
F_tau(alpha(1-u)) = u^(-q) sum_(i>=0) g_i u^i,
```

then the coefficient wave is reconstructed by the finite identity

```text
P_(tau,alpha)(n)
  = sum_(i=0)^(q-1) g_i binom(n+q-i-1,q-i-1).              (3)
```

The primary verifier implements (3) in the exact field
`Q[zeta]/(zeta^2+zeta+1)`.  Its local-series engine uses only the displayed
rational functions, and its all-parameter assertions are the algebraic
identities above, not an endpoint census.

Finally, maximality is uniform in `t`.  On the left, exactly seven parts are
even (the six fixed even nondivisible parts and the fixed part 6), while eight
parts are divisible by three.  Any prime other than two or three divides at
most the three repeated variable parts plus one fixed exceptional part.  On
the right, exactly five parts are even and six are divisible by three.  For
the three variable quotients

```text
t+2,  2t+1,  3t+1,
```

the pairwise gcds divide `3`, `5`, and `1`, respectively; no prime other than
three can divide all three, and no fixed nondivisible part closes the gap to
six.  Therefore `{3}` remains the unique maximizing-prime set on both sides.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter.  The primary
checker uses only the standard library.  The independent checker pins SymPy
1.14.0.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
shasum -a 256 -c SHA256SUMS
python3 independent_sympy_check.py
```

Expected primary digest:
`3aa648bca24091d42d11eb62dcf24334499770e5cb5bdf0d051c3dc508ff63d0`.

The independent SymPy calculation imports no primary-verifier code.  It
reconstructs the four required local coefficients at `t=0` and confirms three
cancellations, actual cross order 25, determinant order 14, and residual order
11.

## Literature and scope boundary

Jiang--Yang--Zhong introduce path block polytopes and their ordinary Ehrhart
structure: <https://arxiv.org/abs/2607.22008>.  Stapledon defines the
determinant-normalized equivariant Ehrhart series and permits rational,
nonpolynomial character evaluations: <https://arxiv.org/abs/1003.5875> and
<https://arxiv.org/abs/2311.17273>.  Björner--Welker study weighted Segre
products abstractly: <https://arxiv.org/abs/math/0312516>.

Those sources do not supply this path-block endpoint formula or maximal-root
jet family.  Novelty is search-relative; no historical-priority claim is made.
The construction refines the height-2049 prime-defect reduction and answers a
mechanism question raised by its independent height-2065 review.  It does not
settle the equal-width polynomiality classification.

## Trust boundary

The universal statement rests on the explicit multisets, the elementary prime
counts and gcd bounds, the leading and subleading identities, equations
(1)--(3), and exact arithmetic in `Q(zeta)`.  The standard-library verifier
checks the complete wave polynomial for parameters `0` through `12`; those
sample checks corroborate but do not replace the displayed all-parameter
algebra.  It trusts CPython integer and `Fraction` semantics plus SHA-256.  The
independent check additionally trusts SymPy 1.14.0 exact algebraic-number
arithmetic.  There is no floating point, randomness, solver, external dataset,
generated input, private state, large certificate, binary, or omitted search
dump.
