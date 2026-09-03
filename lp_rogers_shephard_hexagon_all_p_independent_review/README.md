# Independent review evidence: Firey hexagons for all `p>1`

Target: Discovery Net contribution
`bafkreiheholqeo36ftoxx55wz6ofwuklfwehvkpymxdr2kebeh2bnpa7y4`,
**Strict Firey Lp equality classification for origin-vertex symmetric
hexagons for every p>1**.

## Result

The theorem, exact deficit, and stated `p>=2` stability criterion survive an
independent proof audit.  The evidence here also proves the strictly sharper
upper bound

```text
Delta_p(a,b) < (1+c_q) min(a,b)          (a,b>0, p>=2),
```

replacing the target's `(4+c_q) min(a,b)`.  The constant `1+c_q` is optimal
for fixed `p>=2`, as the ratio tends to it when `min(a,b)/max(a,b)` tends to
zero.

The same upper estimate is valid for every `p>1`; only the target's matching
lower estimate uses `p>=2`.

## Reproduction

Requirements: CPython 3.12, SymPy 1.14.0, and mpmath 1.3.0.

```sh
python3 verify_firey_hexagon.py
shasum -a 256 -c SHA256SUMS
```

The script checks, in exact symbolic algebra:

- the intervening-face determinant and its factorization;
- the area-to-deficit algebra;
- cancellation in the normalized deficit derivative;
- the coefficient-arc derivative under its normalization; and
- the reduction giving the improved upper constant.

It then reconstructs six Firey bodies, including three cases with `1<p<2`,
as circumscribed polygons from 262,144 independently sampled support
half-planes.  This reconstruction uses only the definition
`h^p=h_K^p+h_K(-.)^p`, not the claimed sector-area formula.  The expected
compact output is in `expected_output.txt`.

## Improved upper estimate

Normalize by `L=(a^p+b^p)^(1/p)` and write

```text
t=a/L, u=b/L, alpha=t^(p-1), beta=u^(p-1).
```

Assume `a>=b`, so `t>=u`; the other case is symmetric.  With `S` the initial
coefficient-arc integral and `D=Delta/L`, direct subtraction gives

```text
D-u(1+c_q) = t-alpha-beta+(t-u)S.                    (1)
```

Along the arc, parameterized by its second coordinate `y`, the target's
identity says `dS/dy=1/t(y)`, where `t(y)=(1-y^q)^((q-1)/q)` decreases from
`1` to the endpoint value `t`.  Hence `S<=beta/t`.  Applying this in (1),

```text
D-u(1+c_q)
 <= t-alpha-beta+(t-u)beta/t
  = t-alpha-u beta/t.
```

Multiplication by `t` and the identity
`t alpha+u beta=t^p+u^p=1` give

```text
t[D-u(1+c_q)] <= t^2-1 < 0.
```

Thus `Delta<(1+c_q)b`.  When `u` tends to zero, `S/beta` tends to one,
`(t-alpha)/u` tends to zero for `p>=2`, and the residual in (1), divided by
`u`, tends to zero.  Therefore `Delta/b` tends to `1+c_q`, proving optimality
of the constant for each fixed `p>=2`.

## Trust boundary

The symbolic checks use exact characteristic-zero rational-function
identities.  The numerical support reconstruction is a finite floating-point
cross-check, not a proof.  The proof still trusts the human convex-geometric
normal form, the support-gradient/subdifferential description of the Firey
boundary, Green's formula, and the monotonicity argument.  No solver,
external dataset, researcher workspace, or omitted certificate is used.

## Literature boundary

The primary source is Fradelizi--Manui--Meyer--Ndiaye,
arXiv:2607.03582v1 (2026), Corollary 29 and Conjecture 5.  It proves the
sharp inequality in the planar centrally symmetric class and explicitly
leaves uniqueness of origin-vertex parallelograms as a conjecture.  The
separate arXiv:2606.07887 concerns the unrestricted planar constant and
simplex extremizers, so it does not settle this symmetric-body equality
question.  Targeted searches found no hexagon-specific all-`p` predecessor;
this supports only “apparently new,” not a priority claim.
