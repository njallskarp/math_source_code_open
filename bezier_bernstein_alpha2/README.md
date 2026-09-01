# The alpha = 2 Bezier-Bernstein asymptotic

This project develops the integer-parameter `alpha = 2` regime of Ulrich
Abel's open problem on the asymptotic behavior of Bernstein operators of
Bezier type.

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

## Checked result in this revision

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
operator into an expectation of an order statistic.  The asymptotic theorem
is not yet claimed in this revision.

## Verification

Pinned versions:

```text
Lean 4.33.1
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

## Scope and next step

The next proof layer is the one-dimensional difference reduction

```text
min(X,Y) = (X + Y - |X-Y|) / 2,
```

followed by a central limit theorem and a uniform-integrability argument for
`|X-Y| / sqrt(n)`.  Convergence in distribution alone is not sufficient for
the expectation limit.
