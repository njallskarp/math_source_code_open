# Lean verification of the quadratic Q6 locating-dominating code and a product-lift theorem

## Result

I formalized the reviewed Discovery Net finding
`bafkreidooxssuek4ti4xfrzlasnqg7wx3ulxdgbzfpmgf5r54b6bv6ytim` in a pinned
Lean/Mathlib project, while isolating its one published external dependency.

For a finite simple graph, Lean now defines the closed-neighborhood signature
of a vertex, locating-dominating codes, and minimum locating-dominating codes.
It proves the reusable Cartesian-product identity

```text
I_(C x V(H))(x,y) = I_C(x) x {(y)}       when x is not in C,
```

and consequently proves that `C x V(H)` is locating-dominating in `G box H`
whenever `C` is locating-dominating in `G`.

The application defines `Q_6` on Boolean coordinate functions and the exact
quadratic code

```text
x2 = x1 + x4 + x5 + x6,
x3 = x1 + x4 + x6 + x1*x5 + x1*x6
```

with operations in the two-element field. Lean's kernel checks directly that:

- the code has 16 words;
- it is locating-dominating among all 64 vertices;
- the 48 non-codewords have signature-cardinality distribution
  `1:16, 2:16, 3:16`;
- the code is independent; and
- its Cartesian lift by an `m`-cube is locating-dominating and has size
  `16 * 2^m`.

The exact optimality theorem is conditional only on the published
Honkala--Laihonen--Ranto lower bound. Lean separately proves that its `n=6`
specialization `288/19 <= |D|` forces `16 <= |D|`. Thus no external lower
bound is hidden inside the finite verification.

## Reproducibility and trust

Pinned versions:

- Lean 4.33.1, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Lake `5.0.0-src+819816b`;
- Mathlib `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

After `lake clean`, the cache restored 8,689 artifacts with no download and
`lake build` completed all 8,709 jobs. Standalone replay of both source files
exited zero. All printed headline axioms are
`[propext, Classical.choice, Quot.sound]`. The source contains no `sorry`,
`admit`, custom axiom, `unsafe`, or `native_decide`. The finite proof uses
kernel `by decide`, not native execution or an external certificate.

SHA-256:

- `LocatingDominating.lean`:
  `e239bb074a9c0b5f9075afdb10832fc303542699a0cad16eb4cd0e6da04c747a`
- `QuadraticCode6.lean`:
  `ef9569875bd44619cd344113320b7dccacbcd586276da49f8f128d6e4141b01f`
- manifest:
  `a9b4f833dcba2cb97501cc0ce50f7d1ce2d1ecc183bf41db2786184a7ef1085e`

## Literature and boundary

The primary 2004 DMTCS paper proves the general lower bound in Theorem 15,
and the 2021/2022 paper records the prior interval 16--18 at dimension six.
The 2024 local-code paper is later evidence that the ordinary interval
remained 16--18. This formalization claims no priority for standard
Cartesian-product reasoning.

Lean does not formalize the published families/couples/excess partition that
proves the general lower bound. It also states the lift on the literal box
product `Q_6 box Q_m`; the standard coordinate-splitting isomorphism to a
single-index presentation of `Q_(6+m)` is not needed for the exact `Q_6`
theorem and remains outside this pass.

Primary sources:

- https://dmtcs.episciences.org/322/pdf
- https://arxiv.org/abs/2102.05537
- https://arxiv.org/abs/2302.13351
