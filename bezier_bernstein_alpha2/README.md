# The alpha = 2 Bezier-Bernstein asymptotic

This project develops a short, independent order-statistic proof and reusable
Lean lemmas for the integer-parameter `alpha = 2` regime of Ulrich Abel's
problem on the asymptotic behavior of Bernstein operators of Bezier type.

Important status correction: Kenta Kitamura published a complete Lean proof
of the more general positive-`alpha` theorem in July 2026.  The associated
Formal Conjectures status-change pull request remained open when rechecked on
2026-09-01.  This project therefore
does not claim to solve a currently open problem or claim priority.  Its
contribution is the explicit specialization `muAlpha 2 = -1/sqrt(pi)`, a
compact independent proof route, and reusable formal layer-cake lemmas.

For

```text
J(n,k,x) = sum_{j=k}^n binom(n,j) x^j (1-x)^(n-j),
```

the operator has weights

```text
J(n,k,x)^2 - J(n,k+1,x)^2.
```

If `X_n,Y_n` are independent `Bin(n,x)` variables, these weights are exactly
the law of `min(X_n,Y_n)`.  The intended asymptotic theorem, for fixed
`0 < x < 1` and `f` of class `C^2` on `[0,1]`, is

```text
sqrt(n) * (B(n,2) f x - f x)
  -> -f'(x) * sqrt(x * (1-x) / pi).
```

## Checked results

`BezierBernstein/OrderStatistic.lean` proves over an arbitrary commutative
ring that the mass of the three disjoint cases defining `min(X,Y)=k` equals
the difference of consecutive squared tails:

```text
minPairMass n p k = tailMass n p k ^ 2 - tailMass n p (k+1) ^ 2.
```

It also proves that these masses telescope:

```text
sum_{k=0}^n minPairMass n p k = tailMass n p 0 ^ 2.
```

Thus normalized input masses produce normalized squared-tail differences.
Together these are the exact finite identities that convert the `alpha = 2`
operator into an expectation of an order statistic.

`BezierBernstein/DifferenceIdentity.lean` additionally proves the exact
finite product-mass reduction

```text
pairMinMoment n p
  = totalMass n p * firstMoment n p - pairAbsDiffMoment n p / 2,
```

and its normalized centered form.  See `PAPER_PROOF.md` for the complete short
probability proof of the asymptotic and its explicit uniform-integrability and
Taylor-remainder bounds.  The full asymptotic has not yet been formalized in
this package.

`BezierBernstein/GaussianAbs.lean` checks the explicit Gaussian constant by an
independent analytic route.  Its exported theorems include:

```text
integral_abs_gaussianReal_zero_two:
  integral |x| against N(0,2) = 2 / sqrt(pi)

map_sub_standardGaussian_prod:
  law(G1 - G2) = N(0,2)

integral_min_standardGaussian_prod:
  E[min(G1,G2)] = -1 / sqrt(pi)
```

Here `G1,G2` are the coordinate variables on the product of two standard
Gaussian probability spaces.  The calculation uses Mathlib's exact half-line
primitive for `x * exp (-b*x^2)`, not numerical integration.

`BezierBernstein/MuAlphaTwo.lean` closes the literal-definition alignment gap.
It reproduces Kitamura's definition under the local descriptive name
`poweredGaussianMomentConstant`, proves the two exact product-space tail laws,
and uses Mathlib's layer-cake theorem only after proving integrability.  Its
main exported theorems are:

```text
integral_min_standardGaussian_prod_eq_cdf_tails:
  E[min(G1,G2)]
    = integral_0^infinity (1-Phi(t))^2 dt
      - integral_0^infinity (1-Phi(t)^2) dt

poweredGaussianMomentConstant_two_eq_integral_min:
  poweredGaussianMomentConstant 2 = E[min(G1,G2)]

poweredGaussianMomentConstant_two:
  poweredGaussianMomentConstant 2 = -1 / sqrt(pi)
```

The second integrand above is exactly `1 - (cdf ... t)^2`, matching the
parsing of the immutable upstream definition.  At exponent `2`, Lean's
`Real.rpow_two` bridges the real-power convention to ordinary squaring.

## Verification

Pinned versions:

```text
Lean 4.33.1
Lake 5.0.0-src+819816b
Mathlib v4.33.1
Mathlib commit 0df444a360eaa60ab8c11dca51a86af692955474
```

Build with:

```bash
lake update
lake exe cache get
lake build
```

The source contains no `sorry`, `admit`, custom axioms, `unsafe`, or
`native_decide`.  The exported theorem axiom audit is printed during the
build and reports only Mathlib's standard `propext`, `Classical.choice`, and
`Quot.sound` axioms.

## Source

Ulrich Abel, "Voronovskaja-type Formula for the Bezier Variant of the
Bernstein Operators," *Constructive Theory of Functions, Sozopol 2010*,
pp. 401-402:

https://www.math.bas.bg/mathmod/Proceedings_CTF/CTF-2010/files_CTF-2010/Open_problems.pdf

General positive-`alpha` Lean proof, Kenta Kitamura, immutable commit:

https://github.com/KitaKen1/bezier-bernstein-voronovskaja-lean/blob/3f35c631d215b3841242275bf3ed2c59ea153a2d/Voronovskaja.lean

Formal Conjectures status-change pull request:

https://github.com/google-deepmind/formal-conjectures/pull/4646

## Scope and status

The Gaussian/order-statistic value and the literal CDF-tail alignment are now
checked.  In particular, the project proves

```text
muAlpha 2 = integral_0^infinity (1-Phi(t))^2 dt
          - integral_0^infinity (1-Phi(t)^2) dt
          = E[min(G1,G2)]
          = -1/sqrt(pi).
```

This does not reprove or supersede Kitamura's general theorem.  It supplies a
checked explicit constant evaluation and independent product-space route for
its `alpha = 2` specialization.  Convergence in distribution alone remains
insufficient for the expectation limit; `PAPER_PROOF.md` records the required
uniform-integrability bridge.
