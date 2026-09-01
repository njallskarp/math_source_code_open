# Certified global maximum for the small-hexadecagon fixed code

This directory independently reconstructs and locally certifies the `n=16`
candidate reported by Bernd Mulansky and Andreas Potschka for their fixed-code
zonogon nonlinear program.  The first-quarter code is `+--+-++-`.  Axial
symmetry gives the first-half code

```text
+--+-++-+--+-++-
```

and antipodality gives the full cyclic code

```text
+--+-++-+--+-++--++-+--+-++-+--+
```

whose negative-run composition is
`(2,1,1,2,1,2,1,2,1,1,2)`.

## Certified statement

Fix `phi_1=0`, `phi_17=pi`, and the first-half code above.  Put

```text
P(phi) = sum_{j=1}^{16} 2 sin((phi_{j+1}-phi_j)/2),
g1(phi) = sum_{j=2}^{16} (c_{j-1}-c_j) cos(phi_j) - (c_1+c_16),
g2(phi) = sum_{j=2}^{16} (c_{j-1}-c_j) sin(phi_j).
```

Let `F` be the 17-dimensional KKT system for `f=-P/2` subject to
`g1=g2=0`; scaling the objective by `1/2` does not change its maximizing
angles.  At 512-bit Arb precision, `verify_local_certificate.py` proves:

1. The Krawczyk image is strictly contained in the coordinatewise
   radius-`1e-110` box around the dyadic centers derived from
   `candidate.json`.  Therefore `F` has exactly one zero in that box.
2. Every angle gap is strictly positive throughout the box, so none of the
   ordering inequalities is active.
3. Interval `LDL^T` elimination of the KKT Jacobian has pivot signs
   `+++++++++++++++--` throughout the box.  In particular, the 15-by-15
   Lagrangian Hessian is positive definite and the constraint Jacobian has
   full row rank at the enclosed zero.

The enclosed zero is consequently a strict local maximizer of `P` on the
fixed-code equality manifold.  Arb encloses its perimeter by

```text
[3.136547716486607386085967031941228227298136765809232692789218203577745755473817628905857362542821159391634981 +/- 6.62e-109]
```

This is a local theorem.  It does **not** prove that the point is the unique
stationary point over the whole ordered-angle domain, the global maximizer
for this code, the best code, or the unrestricted longest small
hexadecagon.

## Boundary-exclusion theorem

The second certificate supplies a global reduction before any interval
subdivision.  Let `delta_1,...,delta_16 >= 0`, with sum `pi`, be the angle
gaps of any code-restricted zonogon NLP, and put

```text
p(delta) = 2 sum_j sin(delta_j/2),
p0 = 3.1365477164866073860859670319412282272981367658092326927892182035777457554738176289058573625428211593.
```

The local Arb certificate proves that the fixed-code candidate has perimeter
strictly greater than `p0`.  The following code-independent implications are
then certified for every `delta` with `p(delta) >= p0`:

```text
0.1908839833334 < delta_j < 0.2017683188778       for every j,
sum_j (delta_j-pi/16)^2 < 0.000032491.
```

Consequently, every point that can match the candidate lies in an open
capped simplex whose 15-dimensional volume is less than
`5.565e-26` times that of the original gap simplex.

The proof is short.  If one gap is fixed at `x`, Jensen's inequality applied
to the other 15 gaps gives

```text
p(delta) <= B(x) = 2 sin(x/2) + 30 sin((pi-x)/30).
```

Direct differentiation shows that `B` is strictly increasing before
`pi/16`, strictly decreasing afterwards, and strictly concave.  The two
rational cut points above satisfy `B(x)<p0`, so monotonicity excludes both
outer intervals.  On the resulting band, `h(x)=2 sin(x/2)` has
`h''(x) <= -sin(0.1908839833334/2)/2`; strong concavity and cancellation of
the linear terms at `pi/16` give the stated squared-distance bound.  Finally,
inclusion-exclusion for the capped simplex gives the volume ratio

```text
pi^(-15) sum_{k=0}^8 (-1)^k binom(16,k)
  (pi - 16 alpha - k(beta-alpha))^15.
```

This theorem applies to the angle-gap model independently of the chosen
code.  It does not bridge the unproved structural reduction from arbitrary
small hexadecagons to the full-diameter zonogon NLP.

## Fixed-code global-uniqueness theorem

Combining the boundary theorem with a separate certificate upgrades the
local result to a global theorem for the displayed fixed code.  Among all
ordered half-circle angles satisfying that code's two closure equations,
the Arb-enclosed KKT point is the unique global perimeter maximizer.

Here is the complete two-point argument.  Write

```text
r = pi/16,
x_j = delta_j-r,
s_j = phi_j-j*r = sum_{k<j} x_k,
f = -P.
```

Every point capable of matching the candidate has `||x||_2^2 < 0.000032491`
and all gaps in the certified band.  The Hessian of `f` is a weighted
Dirichlet path Laplacian, so throughout this convex region

```text
nabla^2 f >= m I,
m = 2 sin(alpha/2) sin^2(pi/32) > 0.0018311081.
```

For this code the nonzero closure coefficients occur at

```text
S = {1,3,4,5,7,8,9,11,12,13,15}.
```

They all have magnitude two, and the regular root sum is exactly
`sum_{j in S} exp(2*pi*i*j/16)=-1`.  The Dirichlet inequality and the sharp
radius give

```text
||s||_2 < 0.02907699459226224,
|sum_{j in S} exp(2*i*phi_j)| < 1.192874962187454,
sigma_min(Dg) > 4.4287978.
```

The full-negative-perimeter gradient satisfies

```text
||nabla f||_2 < sin(beta/2) sqrt(0.000032491) < 0.000574074,
```

and hence every KKT multiplier has `||y||_2 < 0.0001296231`.

Finally, if `u` and `v` are two feasible KKT points in this region and
`d=u-v`, the closure map has second directional derivative bounded by
`2||d||_2^2`.  Taylor's formula, including its factor `1/2`, and feasibility
at both endpoints give

```text
||Dg(u)d||_2 <= ||d||_2^2,
||Dg(v)d||_2 <= ||d||_2^2.
```

Strong convexity and the two stationarity equations would therefore require
`m <= ||y_u||_2+||y_v||_2`, whereas the independently certified margin is

```text
m - 2(0.0001296231) > 0.0015718618.
```

Thus the two KKT points coincide.  A fixed-code global maximizer exists by
compactness, has perimeter at least that of the certified candidate, lies in
the strict-gap region by the boundary theorem, and is a regular KKT point by
the singular-value bound.  It must therefore be the Arb-enclosed candidate.

This independently audits and sharpens Guo--Luo Lemmas 9.1--9.3.  It does
**not** establish unrestricted `n=16` optimality: their geometric saturation,
difference-body, and competing-code bridges remain outside the theorem.

### Relationship to the August 2026 proof candidate

A post-selection novelty sweep found Guo and Luo's very recent public
computer-assisted proof candidate for the `n=16,32,64` cases.  Its status is
explicitly non-peer-reviewed and its review request identifies near-regular
localization as a high-priority analytic bridge for independent checking.
Lemma 7.1 of its `n=16` audit uses the same one-gap Jensen mechanism with the
coarser threshold `L0=3.1365475`, band `(0.189,0.204)`, and Euclidean radius
`0.0065`.

Accordingly, the boundary theorem here should be read as an independent
machine-checked strengthening and audit of that bridge, not as an independent
discovery of the Jensen mechanism and not as validation of the proof
candidate's remaining geometric reductions.  It replaces the coarse
constants by the candidate-level threshold, the band
`(0.1908839833334,0.2017683188778)`, Euclidean radius below
`sqrt(0.000032491) < 0.005701`, and a certified simplex-volume reduction.
The source inspected was commit
`a45ff036f9dcd5b297fb4f77a3dea347b8debaac` of the
[proof-candidate repository](https://github.com/aster2024/reinhardt-powers-of-two-proof-candidates),
especially its
[`n=16` audit](https://github.com/aster2024/reinhardt-powers-of-two-proof-candidates/blob/main/cases/n16/reinhardt_n16_proof_audit.md)
and
[`review request`](https://github.com/aster2024/reinhardt-powers-of-two-proof-candidates/blob/main/docs/REVIEW_REQUEST.md).

## Reproduction

Python 3.12 was used for the recorded run.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python reconstruct_candidate.py
.venv/bin/python verify_local_certificate.py
.venv/bin/python verify_boundary_identities.py
.venv/bin/python verify_boundary_band_symbolic.py
.venv/bin/python verify_boundary_band_arb.py
.venv/bin/python -m unittest -v test_local_certificate.py
.venv/bin/python -m unittest -v test_boundary_band.py
.venv/bin/python verify_uniqueness_identities.py
.venv/bin/python verify_uniqueness_bridge_symbolic.py
.venv/bin/python verify_uniqueness_bridge_arb.py
.venv/bin/python -m unittest -v test_uniqueness_bridge.py
shasum -a 256 -c SHA256SUMS
```

`reconstruct_candidate.py` is a non-rigorous, 160-decimal-digit mpmath
Newton reconstruction starting at regular angles.  It independently matches
the published perimeter.  `verify_local_certificate.py` reimplements the
system with Arb balls, uses a fixed exact-dyadic approximate inverse in the
Krawczyk operator, and performs the interval inertia check.  The verifier
does not import the reconstruction formulas.

The boundary theorem has two independent numerical checkers.  The first is
dependency-free: it uses exact `Fraction` arithmetic, derives a rational
interval for `pi` from Machin's formula, and bounds every sine by alternating
Taylor partial sums.  The second evaluates the same obligations with
512-bit Arb balls.  `verify_boundary_identities.py` separately checks the
derivative and concavity identities exactly in SymPy.  The analytic Jensen,
strong-concavity, and capped-simplex arguments remain the human-readable
interpretation layer.

The global-uniqueness bridge has the same three-way separation.
`verify_uniqueness_bridge_symbolic.py` proves every numerical inequality with
only integer and `Fraction` arithmetic.  It encloses square roots by integer
square roots rather than importing a numerical library.
`verify_uniqueness_bridge_arb.py` independently recomputes the constants in
512-bit Arb balls.  `verify_uniqueness_identities.py` checks the full-objective
derivatives, complex closure derivatives, root-of-unity sum, and the Taylor
factor exactly in SymPy.  Neither numerical checker imports or runs the
Guo--Luo verifier.

## Formula audit

The paper defines `P=-f` but its displayed first derivative is the derivative
of `f=-P/2`.  Its displayed off-diagonal Hessian sine argument, and the sign
of the `y2` term on the Hessian diagonal, also differ from direct
differentiation of that displayed first derivative.  These are harmless for
the reported stationary angles but matter for a proof checker.  Both programs
here derive the Jacobian directly from the explicitly stated KKT residual;
the two implementations use different arithmetic libraries.

## Primary source

- Bernd Mulansky and Andreas Potschka, *A zonogon approach for computing
  small polygons of maximum perimeter*, Mathematical Programming (2025),
  [journal article](https://doi.org/10.1007/s10107-025-02244-x),
  [author preprint and source](https://arxiv.org/abs/2404.01841).

The journal also published a
[production correction](https://doi.org/10.1007/s10107-025-02257-6), which
does not concern the objective/Hessian formulas audited here.

The quarter code is Table 4 of the paper; the fixed-code NLP and the authors'
statement that uniqueness was not proved appear in Sections 4--5.
