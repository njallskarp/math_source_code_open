# A short probability proof for the alpha = 2 formula

## Theorem

Fix `x` with `0 < x < 1`, put `sigma^2 = x(1-x)`, and let `f` be of
class `C^2` on `[0,1]`.  For

```text
J(n,k,x) = sum_{j=k}^n binom(n,j) x^j (1-x)^(n-j)
```

and

```text
B(n,2) f(x) = sum_{k=0}^n f(k/n) (J(n,k,x)^2-J(n,k+1,x)^2),
```

one has

```text
sqrt(n) (B(n,2) f(x)-f(x))
  -> -f'(x) sqrt(x(1-x)/pi).
```

This proof is an independent specialization and simplification of the general
positive-alpha theorem formalized by Kenta Kitamura in July 2026.  It is not a
claim of priority for the solution of Abel's open problem.

## 1. Exact order-statistic representation

Let `X_n,Y_n` be independent `Bin(n,x)` variables and put
`M_n=min(X_n,Y_n)`.  Since `J(n,k,x)=P(X_n >= k)`, independence gives

```text
P(M_n >= k) = J(n,k,x)^2.
```

Consequently

```text
P(M_n=k) = J(n,k,x)^2-J(n,k+1,x)^2,
B(n,2)f(x) = E[f(M_n/n)].
```

The squared-tail identity and its normalization are checked in
`BezierBernstein/OrderStatistic.lean`.

## 2. Difference reduction

For all real `a,b`,

```text
min(a,b) = (a+b-|a-b|)/2.
```

Therefore, with `D_n=X_n-Y_n`,

```text
E[M_n]-nx = -E|D_n|/2.                         (1)
```

The corresponding finite product-mass identity, including the normalization
and centering hypotheses, is checked in
`BezierBernstein/DifferenceIdentity.lean`.

## 3. CLT with the expectation bridge made explicit

Realize `X_n=sum_{i=1}^n B_i` and `Y_n=sum_{i=1}^n C_i`, where all
`B_i,C_i` are independent Bernoulli variables of parameter `x`.  The variables

```text
Z_i = B_i-C_i
```

are iid, have mean zero and variance `2 sigma^2`, and
`D_n=sum_{i=1}^n Z_i`.  Hence the one-dimensional central limit theorem gives

```text
W_n = D_n/sqrt(2 n sigma^2)  =>  Z,
```

where `Z` is standard normal.

Convergence in distribution alone does not imply convergence of absolute
moments.  Here the missing bridge follows from the exact second moment

```text
E[W_n^2] = 1.
```

Indeed, for every `K>0`, on the event `|W_n|>K` one has
`|W_n| <= W_n^2/K`, and therefore

```text
sup_n E[|W_n| 1_{|W_n|>K}] <= 1/K -> 0.
```

Thus the family `|W_n|` is uniformly integrable.  The continuous mapping
theorem and uniform integrability now give

```text
E|W_n| -> E|Z| = sqrt(2/pi).
```

It follows that

```text
E|D_n|/sqrt(n)
  = sqrt(2 sigma^2) E|W_n|
  -> 2 sqrt(sigma^2/pi).
```

Combining this with (1),

```text
sqrt(n) (E[M_n/n]-x) -> -sqrt(sigma^2/pi).       (2)
```

## 4. Quadratic Taylor remainder

Compactness and the `C^2` hypothesis give a constant `C` such that, for every
`t` in `[0,1]`,

```text
|f(t)-f(x)-f'(x)(t-x)| <= C (t-x)^2.             (3)
```

The minimum map is 1-Lipschitz for the sup norm, so

```text
|M_n-nx|^2
  <= max(|X_n-nx|,|Y_n-nx|)^2
  <= |X_n-nx|^2+|Y_n-nx|^2.
```

Taking expectations and using the binomial variance gives

```text
E[(M_n/n-x)^2] <= 2 sigma^2/n.                   (4)
```

Apply (3) with `t=M_n/n` and use (4).  The scaled expected remainder is at
most

```text
sqrt(n) C E[(M_n/n-x)^2] <= 2 C sigma^2/sqrt(n) -> 0.  (5)
```

Finally, take expectations in (3), use (2) for the linear term and (5) for
the remainder.  This proves the theorem.

## 5. Relation to the general powered-tail constant

Kitamura's general result writes the limit constant as

```text
mu(alpha) = integral_0^infinity
  ((1-Phi(t))^alpha-(1-Phi(t)^alpha)) dt,
```

where `Phi` is the standard normal CDF.  For `alpha=2`, this is the expectation
of the minimum of two independent standard normals.  If `G_1,G_2` are such a
pair, then

```text
E[min(G_1,G_2)]
  = -E|G_1-G_2|/2
  = -sqrt(2) E|Z|/2
  = -1/sqrt(pi).
```

Thus the general formula specializes to precisely the constant proved above.
Formalizing this exact evaluation of `mu(2)` is the next target.

## Primary sources and status

- Ulrich Abel, *Voronovskaja-type Formula for the Bezier Variant of the
  Bernstein Operators*, Constructive Theory of Functions, Sozopol 2010,
  pp. 401-402:
  https://www.math.bas.bg/mathmod/Proceedings_CTF/CTF-2010/files_CTF-2010/Open_problems.pdf
- Kenta Kitamura, complete Lean proof of the general positive-alpha theorem,
  immutable source commit:
  https://github.com/KitaKen1/bezier-bernstein-voronovskaja-lean/blob/3f35c631d215b3841242275bf3ed2c59ea153a2d/Voronovskaja.lean
- Formal Conjectures status-change pull request 4646, open as of 2026-09-01:
  https://github.com/google-deepmind/formal-conjectures/pull/4646

The general problem should therefore be treated as solved with a public
machine-checked proof, although the corresponding status-change pull request
has not yet merged.  The current package supplies an independent alpha = 2
reduction and targets the missing explicit Lean evaluation of `mu(2)`.
