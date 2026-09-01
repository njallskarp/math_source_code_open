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

This independently audits and sharpens Guo--Luo Lemmas 9.1--9.3.  By itself
it does **not** establish unrestricted `n=16` optimality.  The following
sections audit the geometric saturation bridge, competing-code exclusion,
and symmetry quotient separately.

## Difference-body reconstruction and saturation theorem

The fourth certificate independently audits Guo--Luo Lemmas 3.1, 4.1, and
6.1.  It proves the following geometric bridge.  Let `P` be a
perimeter-maximizing convex small hexadecagon and let `Z=P-P`.  Once the
standard strict-32-edge reduction is made, every vertex of `Z` lies on the
unit circle.  The prior Arb-enclosed fixed-code point and the reconstruction
lemma supply a rigorous feasible perimeter above `p0`, so the sharper
candidate-level deficit can be used instead of the proof candidate's rounded
lower bound.

### Reconstruction and perturbation

Label half of the vertices of a strict centrally symmetric 32-gon by
`z_0,...,z_15`, put `z_16=-z_0`, and define `e_j=z_{j+1}-z_j`.  For a sign
code `c_j` the exact closure condition is

```text
sum_j c_j e_j = sum_j a_j z_j = 0,
a_0 = -(c_0+c_15),
a_j = c_{j-1}-c_j  for 1 <= j <= 15.
```

Selecting `f_j=c_j e_j`, sorting by polar direction, and taking cumulative
sums reconstructs a strictly convex 16-gon.  Zero sum rules out an angular
gap of at least `pi`, while strictness of `Z` makes all 32 directions
`{f_j,-f_j}` distinct.  The cyclic edge merge of the reconstructed polygon
and its negative is exactly the edge list of `Z`; therefore its difference
body is `Z`, and the polygon is unique up to translation.  Since `Z` lies in
the unit disk, the reconstructed polygon has diameter at most one.

If two half-vertices `r,s` lie inside the disk, the closure-preserving
velocities are

```text
v_r = a_s h, v_s = -a_r h                 if a_r a_s != 0,
v_r = h                                   if a_r = 0,
v_s = h                                   if a_s = 0 and a_r != 0.
```

Strict cyclic order and genuine-vertex inequalities are open.  The exact
incidence checker proves that one of the 16 half edges changes in every
coefficient, adjacency, and endpoint case.  Choosing `h` outside the finite
set of affected edge directions makes at least one norm strictly convex, so
a local perimeter maximum has at most one interior half-vertex; if it has
one, its closure coefficient is nonzero.

The checker first verifies the summation-by-parts formula for all 32,768
codes normalized by `c_0=+1`.  The motion depends only on the two positions
and two coefficient values in `{-2,0,2}`, reducing the complete perturbation
audit to `120*9=1080` exact cases.  This includes 261 cyclic-endpoint and 144
adjacent-pair cases.  No solver is used.

### Sharper saturation contradiction

Cauchy's perimeter formula over the 32 normal cones and the candidate-level
lower bound give

```text
64 sin(pi/32)-p(Z) < 0.000001549.
```

Jensen localization and the nonnegative deficit decomposition then imply

```text
0.18 < omega_j < 0.21,
r_j > 0.99999,
|eta_j-phi_j| < 0.0042,
d_RP1(phi_j,phi_k) > 0.1716  for distinct half-vertices.
```

Suppose one interior vertex `z_r` remained.  Uniform radial contraction
`d_j=-z_j` preserves the homogeneous closure equation and has active disk
derivative `-2`; the block `a_r I_2` has determinant four.  This gives MFCQ
without an auxiliary linear solve.  At the interior vertex the KKT equation
fixes the projective multiplier direction as `eta_r`.  At a second index
`j` with `a_j!=0`, tangent projection eliminates the disk multiplier and
gives

```text
|sin(eta_r-phi_j)|
  = sin(omega_j/2)/sin(omega_r/2) * |sin(eta_j-phi_j)|
  < 0.0049.
```

Using `sin d >= 2d/pi` on the projective interval yields

```text
d_RP1(phi_r,phi_j) < 0.0119,
```

contradicting the certified separation above.  Hence every difference-body
vertex is saturated.

The dependency-free verifier proves all scalar bounds with `Fraction`, a
Machin interval for `pi`, and alternating Taylor enclosures.  A separate
512-bit Arb implementation obtains the same margins.  Exact SymPy checks
cover the cyclic summation by parts, normal-cone integral, perimeter
gradient, tangent projection, radial MFCQ derivative, and rank block.

This does not yet prove the unrestricted optimum.  It validates the
reconstruction, perturbation-feasibility, and saturation bridges.  The next
section independently audits the finite competing-code exclusion; the final
dihedral/congruence quotient remains separate.

## Competing-code exclusion theorem

Assume the saturation conclusion above and let
`c=(c_0,...,c_15)` be a half-code.  Multiplying every sign by `-1` negates the
closure residual and loses no solutions, so normalize `c_0=+1`.  There are
then exactly `2^15=32768` codes.  Put `r=pi/16`,
`zeta=exp(i*r)`, `delta_j=r+x_j`, and

```text
s_j = x_0+...+x_(j-1),
a_j = c_(j-1)-c_j                         (1 <= j <= 15),
b_c = (zeta-1) sum_(j=0)^15 c_j zeta^j.
```

The saturated closure equation has the exact expansion

```text
0 = G_c = b_c + i sum_(j=1)^15 a_j zeta^j s_j + R_c(s),
|R_c(s)| <= sum_(j=1)^15 s_j^2.
```

Let `D` be the 15-by-15 Dirichlet path Laplacian.  Its inverse is checked
symbolically to be

```text
(D^-1)_(jk) = min(j,k)(16-max(j,k))/16.
```

Since `||x||_2^2=s^T D s`, the linear term has sharp energy-norm bound
`sigma_c ||x||_2`, where

```text
sigma_c^2 = lambda_max(B_c D^-1 B_c^T)
```

and column `j` of the real 2-by-15 matrix `B_c` represents
`i a_j zeta^j`.  Moreover,

```text
||s||_2^2 <= C ||x||_2^2,
C = 1/(4 sin^2(pi/32)).
```

Thus a necessary condition for a code to support any saturated point in the
candidate-level region `||x||_2^2 < rho2=0.000032491` is

```text
|b_c| <= sqrt(rho2) sigma_c + C rho2.                 (*)
```

The dependency-free certificate proves the contrapositive of `(*)` in three
structural stages.  If `k` is the number of internal sign switches, then
`sigma_c <= 2 sqrt(C k)` leaves 1,494 codes.  Replacing this by the exact
trace bound for `B_c D^-1 B_c^T` leaves 32.  Computing the upper eigenvalue
of that 2-by-2 Gram matrix leaves exactly 16.  The respective excluded-code
margins in `|b_c|-sqrt(rho2)sigma-C rho2` exceed

```text
0.0030, 0.0028, 0.0047.
```

The final 16 codes are exactly the normalized formal dihedral orbit of

```text
+--+-++-+--+-++-.
```

The exact route encloses `pi` by Machin's formula, every root coordinate by
alternating rational Taylor sums, and every square root by integer square
roots.  A separate 512-bit Arb implementation skips the trace screen and
recomputes the spectral inequality directly for all 1,494 first-stage
survivors; it obtains the same 16 codes and the same conservative margins.
Exact SymPy checks independently verify the cyclotomic residual, the vertex
summation-by-parts form, the Dirichlet Green kernel, and the linearization.
No solver or floating-point prescreen is used.

Together with the boundary localization and saturation theorems, this rules
out every normalized competing half-code outside that formal orbit at the
candidate perimeter level.  The next section proves that the formal orbit is
indeed one polygon-congruence class.

## Symmetry/congruence quotient theorem

The formal 16-code orbit does not merely identify sign strings.  Acting
simultaneously on the code and on the labeled difference body proves that all
sixteen survivors reconstruct congruent polygons.

Write the full centrally symmetric vertex and edge lists modulo 32 as

```text
V_(j+16)=-V_j,
E_j=V_(j+1)-V_j,
E_(j+16)=-E_j,
C_(j+16)=-C_j.
```

The selected polygon-edge sequence `F_j=C_j E_j` is 16-periodic.  Its first
sixteen entries, sorted by direction, reconstruct the polygon uniquely up to
translation.

For a cyclic shift `s`, choose the rotation `A` that restores the normalized
starting vertex and define

```text
V'_j=A V_(j+s),       C'_j=epsilon C_(j+s),
```

where `epsilon` makes `C'_0=+1`.  Then

```text
E'_j=A E_(j+s),
F'_j=epsilon A F_(j+s).
```

Thus the new selected-edge multiset is that of `epsilon A P`; global sign is
just central inversion.  Closure transforms as `G'=epsilon A G`, while the
gap sequence is permuted by `delta'_j=delta_(j+s)`.

For a reflected index action, choose an orientation-reversing orthogonal map
`A` restoring the starting vertex and put

```text
V'_j=A V_(s-j+1),     C'_j=epsilon C_(s-j).
```

The endpoint convention is now explicit:

```text
E'_j=-A E_(s-j),
F'_j=-epsilon A F_(s-j),
delta'_j=delta_(s-j).
```

Hence reflection also preserves closure, perimeter, the candidate-level
neighborhood, and reconstruction up to an allowed Euclidean isometry and
translation.  In both cases `V'_0` is normalized, `V'_16=-V'_0`, odd shifts
cross the antipodal endpoint correctly, and the normalized full code remains
antiperiodic.

For the displayed representative there is a stronger exact identity

```text
C_(s-j) = -C_(j+15-s)       modulo 32.
```

Consequently the normalized dihedral orbit is already the normalized cyclic
shift orbit.  Its sixteen elements have unique canonical shift witnesses
`s=0,...,15`; all 64 shift/reflection actions give four witnesses per code.
The dependency-free checker verifies every action in the free signed-edge
module, including closure and selected-edge-multiset equivariance.  An
independent SymPy checker proves the same 64 identities over
`ZZ[a,b,c,d,x_0,...,x_15,y_0,...,y_15]`, checks every gap permutation, and
verifies the antiperiodic shift relations `R^16=-I`, `R^32=I`.  Orthogonality
is not assumed by either algebraic identity checker; it enters only when
interpreting `A` as a congruence.

Combining this quotient with the fixed-code uniqueness, saturation, and code
exclusion results proves a conditional uniqueness theorem: **among global
competitors whose difference body has 32 strict vertices, the certified
candidate is the unique maximizer up to translation, rotation, reflection,
central inversion, and cyclic relabeling.**  The unrestricted theorem still
requires an independent audit of the strict-32-edge reduction; no claim here
closes that remaining hypothesis.

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
The competing-code theorem independently audits Lemma 8.1 with that sharper
radius.  Its switch-count and trace reductions are not present in the proof
candidate, and its exact checker uses Taylor root enclosures rather than the
candidate verifier's nested-radical implementation.  These distinctions do
not constitute a priority claim for the underlying finite exclusion idea.
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
.venv/bin/python verify_saturation_cases.py
.venv/bin/python verify_saturation_identities.py
.venv/bin/python verify_saturation_bounds_symbolic.py
.venv/bin/python verify_saturation_bounds_arb.py
.venv/bin/python -m unittest -v test_saturation_bridge.py
.venv/bin/python verify_code_exclusion_exact.py
.venv/bin/python verify_code_exclusion_arb.py
.venv/bin/python verify_code_exclusion_identities.py
.venv/bin/python -m unittest -v test_code_exclusion.py
.venv/bin/python verify_symmetry_quotient_exact.py
.venv/bin/python verify_symmetry_quotient_sympy.py
.venv/bin/python -m unittest -v test_symmetry_quotient.py
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

The saturation bridge adds a fourth separation of responsibilities.
`verify_saturation_cases.py` is an exact integer incidence checker;
`verify_saturation_bounds_symbolic.py` and
`verify_saturation_bounds_arb.py` independently certify the quantitative
inequalities; and `verify_saturation_identities.py` checks the analytic
identities in SymPy.  The human-readable geometric interpretation uses
standard planar Minkowski edge merging, Cauchy's perimeter formula, openness
of strict convexity, and the KKT theorem under MFCQ.  These are the remaining
non-formalized mathematical trust boundary.

The code-exclusion certificate again separates arithmetic routes.
`verify_code_exclusion_exact.py` implements the switch, trace, and spectral
screens using fixed integer intervals derived from rational Machin/Taylor
bounds.  `verify_code_exclusion_arb.py` independently applies the universal
screen and then direct 2-by-2 Arb spectral bounds.  The compact outputs list
all 16 survivors, while `verify_code_exclusion_identities.py` checks the
algebraic reduction and Green kernel.  The human-readable Taylor-remainder
argument remains a non-programmatic trust boundary.

The quotient certificate uses no numerical arithmetic.  The dependency-free
checker works with exact signed basis edges and records one canonical cyclic
witness for every survivor.  The independent SymPy checker works with two
generic coordinates for every half edge and a generic linear map.  The
remaining interpretation is the standard geometric fact that an orthogonal
map and central inversion preserve congruence and that a strictly convex
polygon is determined up to translation by its cyclic edge list.

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
