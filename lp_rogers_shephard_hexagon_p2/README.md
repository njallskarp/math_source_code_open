# `L_2` Rogers--Shephard strictness for centrally symmetric hexagons

This directory studies the `p=q=2` six-vertex specialization of Conjecture 5
in Fradelizi, Manui, Meyer, and Ndiaye,
[*L_p-Rogers--Shephard type inequalities for L_p-zonoids and symmetric
bodies*](https://arxiv.org/abs/2607.03582).

The proved paper-level result is:

> If `K⊂R²` is a full-dimensional centrally symmetric convex hexagon with
> the origin as a vertex, then
> `area(K ⊕₂ (-K)) < (π/2+2) area(K)`.

After affine normalization to
`K=[0,e₁]+[0,(a,b)]+[0,e₂]`, `a,b>0`, and writing
`φ=arctan(b/a)`, the exact calculation is

```text
area(K) = 1+a+b,
area(K ⊕₂ (-K))
  = 2(1+a+b)+(1+b)φ+(1+a)(π/2-φ),
(π/2+2)area(K)-area(K ⊕₂ (-K))
  = aφ+b(π/2-φ)>0.
```

See [`PAPER_PROOF.md`](PAPER_PROOF.md) for the proof and the precise scope.

## Lean verification

The Lean development checks:

- `three_positive_parts_sq_identity`;
- `threeSegmentSupport_sq_add_reflection_sq`;
- `inner_le_positivePart_of_mem_segment`;
- `exists_mem_segment_inner_eq_positivePart`;
- `inner_le_threeSegmentSupport_of_mem`;
- `exists_mem_threeSegmentZonotope_inner_eq_support`;
- `setSupportFunction_threeSegmentZonotope`;
- `hasDerivAt_sectorTwoSupport`;
- `sectorTwoSupport_sq_sub_derivative_sq`;
- `sectorTwo_gramDet`;
- `sectorTwoSq_pos`;
- `sectorTwoDensity_eq_curvature_sub_boundaryDerivative`;
- `sectorTwoU_pos_on_sector`;
- `hasDerivAt_sectorTwoPhaseRatio`;
- `hasDerivAt_sectorTwoCurvaturePrimitive`;
- `sectorTwoPhaseRatio_pi_div_two_add`;
- `sectorTwoCurvaturePrimitive_endpoints`;
- `integral_sectorTwoCurvature`;
- `sectorTwoBoundary_change`;
- `integral_sectorTwoDensity_eq_curvature_sub`;
- `integral_sectorTwoDensity`;
- `sectorThreeSq_reflect`;
- `sectorThreeBoundary_reflect`;
- `sectorThreeDensity_reflect`;
- `arctan_div_swap`;
- `integral_sectorThreeDensity`;
- `planeDirection_add_pi`;
- `normalizedFireySupportSq_periodic`;
- `normalizedFireySupportSq_eq_positiveParts`;
- `normalizedFireySupportSq_eq_sectorOneSq_on_sector`;
- `normalizedFireySupportSq_eq_sectorTwoSq_on_sector`;
- `normalizedFireySupportSq_eq_sectorThreeSq_on_sector`;
- `sectorOneSq_eq_sectorTwoSq_pi_div_two`;
- `sectorTwoSq_eq_sectorThreeSq_boundary`;
- `hasDerivAt_sectorOneSupport`;
- `hasDerivAt_sectorOnePrimitive`;
- `integral_sectorOneDensity`;
- `integral_normalizedUpperDensity`;
- `hasDerivAt_supportBoundaryX` and `hasDerivAt_supportBoundaryY`;
- `supportBoundary_normal_pairing` and `supportBoundary_tangent_pairing`;
- `supportBoundary_orientedDensity`;
- `sectorTwoBoundaryOrientedDensity_eq_curvature`;
- `integral_sectorTwoBoundaryOrientedDensity`;
- `sectorThreeBoundaryOrientedDensity_eq_curvature`;
- `integral_sectorThreeBoundaryOrientedDensity`;
- `sectorOneTwo_transitionDet`;
- `sectorTwoThree_transitionDet`;
- `sectorThreeOne_transitionDet`;
- `normalizedUpperBoundaryOrientedTotal_eq`;
- `integral_normalizedUpperDensity_eq_boundaryOrientedTotal`;
- `normalizedFireySupportVec_rpow_half`;
- `three_positive_parts_sq_ge_first_tail` and
  `three_positive_parts_sq_ge_last_head`;
- `inner_twoGeneratorBoundaryPoint_le`;
- `sectorTwoEllipsoidPoint_eq_boundaryPoint` and
  `sectorThreeEllipsoidPoint_eq_boundaryPoint`;
- `sectorTwoBoundaryPoint_mem_normalizedLpSumTwo` and
  `sectorThreeBoundaryPoint_mem_normalizedLpSumTwo`;
- `sectorTwoBoundaryPoint_supporting` and
  `sectorThreeBoundaryPoint_supporting`;
- `setSupportFunction_normalizedLpSumTwo_sectorTwo` and
  `setSupportFunction_normalizedLpSumTwo_sectorThree`;
- `sectorOneVertex_supporting` and
  `setSupportFunction_normalizedLpSumTwo_sectorOne`;
- `setSupportFunction_normalizedLpSumTwo_upperHalf`;
- `normalizedFireySupportVec_neg` and `neg_mem_normalizedLpSumTwo`;
- `convex_normalizedLpSumTwo`;
- `sectorOneTwoJump_subset_normalizedLpSumTwo`,
  `sectorTwoThreeJump_subset_normalizedLpSumTwo`, and
  `sectorThreeOneJump_subset_normalizedLpSumTwo`;
- `normalizedFireySupportVecSq_neg_small`;
- `le_firstCoord_of_mem_of_vertical_support`;
- `exposedFace_planeE2_eq_sectorOneTwoJump`;
- `normalizedFireySupportVecSq_middlePlus_expansion` and
  `normalizedFireySupportVecSq_middleMinus_expansion`;
- `inner_middleTangent_le_of_middle_support` and
  `neg_b_mul_middleRadius_le_inner_middleTangent_of_middle_support`;
- `exposedFace_middleNormal_eq_sectorTwoThreeJump`;
- `normalizedFireySupportVecSq_coordinateSwap` and
  `normalizedFireySupportVec_coordinateSwap`;
- `coordinateSwap_mem_normalizedLpSumTwo_iff` and
  `closingSymmetry_mem_normalizedLpSumTwo_iff`;
- `closingSymmetry_mem_sectorOneTwoJump_iff`;
- `exposedFace_neg_planeE1_eq_sectorThreeOneJump`;
- `normalizedExposedFace_neg`;
- `exposedFace_neg_planeE2_eq_neg_sectorOneTwoJump`,
  `exposedFace_neg_middleNormal_eq_neg_sectorTwoThreeJump`, and
  `exposedFace_planeE1_eq_neg_sectorThreeOneJump`;
- `normalizedFireySupportVec_eq_sectorTwoSupport` and
  `normalizedFireySupportVec_eq_sectorThreeSupport`;
- `sectorTwo_supportGap_isLocalMin` and
  `sectorThree_supportGap_isLocalMin`;
- `exposedFace_sectorTwo_eq_singleton` and
  `exposedFace_sectorThree_eq_singleton`;
- `exposedFace_sectorOneVector_eq_singleton`;
- `normalizedFireySupportVec_smul_of_nonneg` and
  `normalizedExposedFace_smul_of_pos`;
- `eq_complexNorm_smul_planeDirection_arg` and
  `exposedFace_upperHalf_subset_upperNormalBoundary`;
- `normalizedExposedFace_subset_frontier_of_ne_zero`;
- `frontier_normalizedLpSumTwo_eq_iUnion_nonzero_exposedFaces`; and
- `frontier_normalizedLpSumTwo_eq_upperNormalBoundary_union_neg`;
- `sectorTwoBoundarySpeed_pos` and `sectorThreeBoundarySpeed_pos`;
- `strictAntiOn_sectorTwoBoundaryX` and
  `strictAntiOn_sectorThreeBoundaryX`;
- `injOn_sectorTwoBoundaryPoint` and
  `injOn_sectorThreeBoundaryPoint`;
- `injective_sectorTwoArcPath` and `injective_sectorThreeArcPath`;
- `sectorTwoBoundaryOrientedDensity_pos` and
  `sectorThreeBoundaryOrientedDensity_pos`;
- `generatorAngle_mem_Ioo`;
- `normalizedDeficit_pos`;
- `normalized_bound_sub_area_formula`;
- `normalized_area_formula_lt_bound`.

The support theorem is set-level: for the actual Minkowski sum
`[0,u]+[0,v]+[0,w]`, the subtype-indexed supremum of `inner x ξ` is the sum
of the three positive generator pairings.  In the normalized Euclidean plane,
Lean now specializes this literal set support and its reflection to the exact
Sector I, II, and III squared-support formulas on their closed angular
intervals.  It checks `π`-periodicity of the set-level squared support and
agreement of adjacent sector squares at both sign-change endpoints.  Lean
also checks the Sector II square-root derivative, the
pointwise determinant decomposition, and the exact integral reduction

```text
∫ (h²-(h')²) = ∫ (1+b)²/F - ab,
```

including the endpoint correction `ab`.  Lean also proves `U>0` throughout the closed second
sector, differentiates the branch-correct primitive
`-(1+b) arctan(cos θ/U(θ))`, evaluates both endpoint phases, and closes the
full exact contribution

```text
∫_{π/2}^{π/2+φ} (h²-(h')²) = (1+b)φ-ab.
```

The orientation-reversing substitution `η=3π/2-θ`, together with the checked
identity `arctan(a/b)=π/2-arctan(b/a)`, transports that theorem without
duplicating its calculus and proves the full third-sector contribution

```text
∫_{π/2+φ}^{π} (h²-(h')²) = (1+a)(π/2-φ)-ab.
```

For Sector I, Lean differentiates
`h=(1+a)cos θ+(1+b)sin θ`, checks a genuine primitive of the nonconstant
density, and proves

```text
∫₀^{π/2} (h²-(h')²) = 2(1+a)(1+b).
```

Finally, `normalizedUpperDensity` is one explicit piecewise function on
`[0,π]`.  Lean proves its interval integrability on all three pieces, applies
interval additivity twice, and obtains

```text
∫₀^π normalizedUpperDensity
  = 2(1+a+b)+(1+b)φ+(1+a)(π/2-φ).
```

The current Formal Conjectures entry defines `lpSum` literally as the
intersection of all halfspaces

```text
{x | forall u, inner x u <=
  (supportFunction K u ^ p + supportFunction L u ^ p) ^ (1/p)}.
```

At `p=2`, `normalizedFireySupportVecSq` is exactly the radicand for arbitrary
vector directions, and `normalizedFireySupportVec_rpow_half` proves that the
source real-power convention is exactly its square root.  Thus
`normalizedLpSumTwo` is the literal source halfspace intersection, not an
angular surrogate.

The set-level support restriction and the scalar integral evaluations are
separate checked theorems; a planar support-area theorem is still required to
assemble them into a Lebesgue-area statement.

The new boundary modules make that remaining bridge substantially more
geometric.  For a twice differentiable scalar support `h`, Lean defines the
canonical normal-angle boundary point

```text
gamma(θ)=h(θ)(cos θ,sin θ)+h'(θ)(-sin θ,cos θ)
```

coordinatewise and proves

```text
gamma'(θ)=(h(θ)+h''(θ))(-sin θ,cos θ),
det(gamma(θ),gamma'(θ))=h(θ)(h(θ)+h''(θ)).
```

It then checks the actual Sector II and Sector III square-root support
derivatives through second order, proves that their canonical boundary paths
have oriented densities equal to the previously integrated curvature terms,
and evaluates both arc integrals.  Sector I gives the constant boundary point
`(1+a,1+b)` and zero arc density.  The one-sided support derivatives jump at
the three sign boundaries; Lean proves that the corresponding straight
segment determinants are exactly

```text
1+b,  a+b,  1+a.
```

Adding the two curved arcs, the constant first arc, and these three jumps gives
the complete upper-half oriented-boundary total and Lean proves it equals the
already checked `∫₀^π (h²-(h')²)`.  Thus the endpoint corrections are now
explained as literal boundary segments, not merely algebraic cancellation.

`HalfspaceBody.lean` closes the next global geometric bridge.  The
three-positive-parts identity proves, in every vector direction, that the full
Firey square dominates both curved-sector ellipsoidal quadratic supports.  A
reusable two-coordinate Cauchy--Schwarz theorem therefore places each
ellipsoidal support point in every defining halfspace.  Lean identifies these
points exactly with the previously integrated canonical Sector II and III arc
coordinates.  The actual arc points consequently belong to
`normalizedLpSumTwo`, attain equality at their displayed normals, and the
subtype-supremum support function of the literal body equals the prescribed
Firey support on both curved sectors.

The fixed Sector I vertex and its opposite are also proved to belong to the
body.  The halfspace intersection is proved convex, so each of the three
literal jump segments lies in it.  This is genuine body-level membership and
support attainment; it does not yet assert that these paths exhaust the whole
topological boundary or that their line integral is Lebesgue area.

`ExposedFaces.lean` closes the first complete transition-face classification.
For the vertical normal `e₂`, Lean proves the exact set equality

```text
{x in normalizedLpSumTwo(a,b) : inner(x,e₂)=1+b}
  = segment((1+a,1+b),(a,1+b)).
```

The difficult reverse inclusion does not use an unformalized support
derivative or a limiting argument.  If a point on the supporting line had
first coordinate below `a`, the defining halfspace in a small direction
`(-t,1)` would give

```text
1+b-a*t+t*(a-x₀) <= sqrt(t²+(1+b-a*t)²),
```

whose square is contradictory after choosing
`0<t<=a-x₀` and `a*t<=b/2`.  The module also proves support attainment by the
fixed Sector I vertex, assembles literal support equality over all of
`[0,pi]`, and proves central symmetry of the exact halfspace body.

`MiddleExposedFace.lean` closes the second transition face.  At the generator
sign-change normal `n=(-b,a)`, put `v=(a,b)` and
`s=sqrt(a^2+b^2)`.  Lean derives the exact adjacent-chamber expansions

```text
H(n+t v)^2=(s+a*s*t)^2+t^2*(a^2+b^2)*(1+b)^2,
H(n-t v)^2=(s+b*s*t)^2+t^2*(a^2+b^2)*(1+a)^2.
```

Explicit small positive perturbations force every point on the supporting
line to satisfy `-b*s <= inner(x,v) <= a*s`.  The one-sided canonical boundary
points attain these endpoint values, and equality of the normal and tangent
pairings determines a planar point.  Consequently Lean proves

```text
{x in normalizedLpSumTwo(a,b) : inner(x,(-b,a))=s}
  = sectorTwoThreeJump(a,b).
```

This uses neither a support derivative limit nor a hidden area definition.

`ClosingExposedFace.lean` closes the third upper-half transition face by an
exact symmetry argument.  The coordinate swap `S(x,y)=(y,x)` transports the
prescribed Firey support and maps `normalizedLpSumTwo(b,a)` onto
`normalizedLpSumTwo(a,b)`.  Composing it with negation transports the already
classified vertical face for parameters `(b,a)` to the closing face.  Lean
also checks the endpoint and segment maps, and proves

```text
{x in normalizedLpSumTwo(a,b) :
    inner(x,-e1)=normalizedFireySupportVec(a,b,-e1)}
  = sectorThreeOneJump(a,b).
```

Thus all three upper-half derivative-jump exposed faces are classified
exactly.

`LowerFacesAndCurvedUniqueness.lean` packages central symmetry as the literal
face identity `Face(-u)=-Face(u)` and transports the three upper-half
classifications to all three lower-half jump faces.  It also proves that the
exposed face at every interior Sector II or Sector III normal is the singleton
containing the checked canonical point.  The proof differentiates the
nonnegative support gap

```text
t ↦ h(t)-inner(x,n(t))
```

at its local minimum, obtains the tangent pairing, and combines that with the
supporting normal pairing.  The two orthogonal pairings determine the planar
point.  Transition normals are excluded explicitly and remain governed by the
six segment-valued face theorems.

`FrontierSupport.lean` closes the compactness and supporting-normal bridge for
the literal halfspace body.  It proves

- `norm_sq_le_normalizedFireySupportVecSq` and
  `ball_zero_one_subset_normalizedLpSumTwo`, hence the origin is an interior
  point;
- `isClosed_normalizedLpSumTwo`, `isBounded_normalizedLpSumTwo`, and
  `isCompact_normalizedLpSumTwo`;
- `exists_mem_inner_eq_normalizedFireySupportVec`, by an explicit split into
  the three generator-sign chambers and central symmetry;
- `setSupportFunction_normalizedLpSumTwo_allDirections`; and
- `exists_nonzero_normal_mem_exposedFace_of_mem_frontier`.

The last theorem applies geometric Hahn--Banach to the compact convex body
with nonempty interior.  Thus every frontier point belongs to a literal
exposed face for a nonzero normal.  Supporting-hyperplane existence is no
longer an assumption.

`FrontierAtlas.lean` completes the finite partition and topological frontier
exhaustion.  It proves the missing open Sector I singleton face and exact
lower-half curved singleton faces; positive homogeneity and ray invariance of
exposed faces; the polar reduction

```text
u = ‖u₀+i u₁‖ planeDirection(arg(u₀+i u₁));
```

and all seven cases on the closed upper angular interval, including its four
transition directions.  It also proves that every face at a nonzero normal is
contained in the frontier.  The final theorem
`frontier_normalizedLpSumTwo_eq_upperNormalBoundary_union_neg` identifies the
frontier with the explicit upper-normal atlas and its pointwise negative.
Together these are precisely the two open curved pairs, the two opposite
Sector I vertices, and all six classified jump segments.  Frontier coverage
is therefore no longer an assumption.

`CyclicBoundaryPath.lean` packages that atlas as a genuine bundled topological
path rather than a set-valued boundary description.  It proves continuity of
the two canonical curved parametrizations from the already checked coordinate
derivatives, defines a five-piece path from the Sector I vertex to its
negative (first jump, Sector II arc, middle jump, Sector III arc, closing
jump), and concatenates it with its pointwise negative.  The resulting
`normalizedCyclicBoundaryPath` is closed by construction.  The final theorem
`range_normalizedCyclicBoundaryPath` proves the exact set identity

```text
Set.range (normalizedCyclicBoundaryPath a b ha hb)
  = frontier (normalizedLpSumTwo a b).
```

Thus endpoint matching, global continuity, and image equality with the actual
halfspace body's topological frontier are now checked.  No area or desired
formula is hidden in the path definition.

`SimplePathOrientation.lean` proves the first embeddedness and orientation
step without appealing to a Jordan theorem.  On both curved sectors the
tangential speed `h+h''` is strictly positive.  Since `sin(theta)>0` on the
relevant angular intervals, the first Cartesian coordinate has strictly
negative derivative.  It follows that each canonical boundary-point map is
injective on its closed angular interval and each bundled curved arc path is
injective.  The module also proves that both pointwise oriented determinant
densities are strictly positive.  These are exact per-piece results; they do
not yet assert cross-piece disjointness or injectivity of the full cyclic
concatenation.

`UpperPathInjectivity.lean` supplies the global upper-chain simple-path bridge.
Its reusable theorem says that concatenating two injective paths whose ranges
meet only at their common endpoint preserves injectivity.  The module proves
all three straight jump paths are injective and classifies every pairwise
range intersection among the five upper pieces using strict monotonicity of
the curved first coordinates and exact endpoint gaps.  Recursive application
of the concatenation theorem yields `injective_normalizedUpperBoundaryPath`:
the complete five-piece upper-normal path is injective.  Intersections between
that path and its pointwise negative, and hence injectivity modulo endpoints
of the closed cyclic path, remain explicit downstream obligations.

An API audit found Mathlib's general curve-integral infrastructure, but no
planar Green/Jordan theorem, convex support-function theory, mixed-area theory,
or theorem identifying a closed convex boundary integral with planar Lebesgue
area.  The smallest remaining analytic-geometry bridge is now to prove that
the checked cyclic path is injective except at its common initial/final
endpoint, establish positive orientation, and identify its already checked
oriented integral with twice Lebesgue area.  The present development supplies
exact halfspace membership, support equality, compactness, supporting normals,
the complete normal-chamber partition and frontier coverage, all six jump-face
classifications, curved-sector singleton faces, central symmetry,
coordinatewise differentiability, oriented-density, endpoint, jump, integral,
and periodicity precursors.  It does not assume the missing Green/Jordan or
area theorem.  The affine normal-form theorem for an arbitrary centrally
symmetric origin-vertex hexagon also remains outside Lean.

Pinned environment:

- Lean `v4.33.1`;
- Mathlib `v4.33.1`;
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`;
- Lake `5.0.0-src+819816b`.

Reproduce with:

```bash
lake update
lake build
python3 -m pip install -r requirements.txt
python3 verify_symbolic.py
```

The SymPy script checks only exact rational-function differentiation,
endpoint identities, and algebraic assembly.  It does not certify the
geometric area formula or any arctangent branch choice.  Expected output:

```text
exact sector endpoint identities: OK
exact curvature antiderivatives: OK
exact area assembly: OK
exact deficit assembly: OK
```

The source uses no `sorry`, `admit`, custom axioms, `unsafe`, or
`native_decide`.  The files print the axioms of all exported theorems.

## Novelty calibration

The source paper proves the inequality for all planar centrally symmetric
bodies and conjectures uniqueness of the parallelogram equality cases.  A
targeted search refreshed on 2026-09-02 found no treatment of the strict centrally
symmetric hexagon subcase.  This is search-relative evidence, not a priority
claim and not an exhaustive bibliographic review.  The result does not solve
the authors' full equality conjecture.

The separate paper [arXiv:2606.07887](https://arxiv.org/abs/2606.07887)
settles equality for a different planar `L_p` Rogers--Shephard inequality;
its simplex equality cases do not resolve the symmetric-body conjecture
studied here.

Likewise, Kotrbatý--Mouamine
[arXiv:2607.20387](https://arxiv.org/abs/2607.20387), Theorem 1.2, proves the
general Firey `L_p` Rogers--Shephard inequality and its simplex equality
cases.  That theorem does not subsume Corollary 29's improved symmetric-body
bound.  In the planar `p=q=2` case its constant is `pi+2`, whereas Corollary
29 has the strictly smaller constant `pi/2+2`.  This exact constant comparison
corrects a Discovery Net review that suggested the general theorem implied
the strict symmetric-hexagon result.

The later paper
[arXiv:2608.24081](https://arxiv.org/abs/2608.24081) studies volume-to-projection
inequalities for `L_p`-sums and determinant-power analogues.  Its statement and
text do not address the parallelogram uniqueness conjecture or the strict
symmetric-hexagon regime considered here.

An independent Discovery Net review
(`bafkreig77oiopn6zq4l37ahdoqqwucmuhevkhp7uqi5v5qet37oh3x5foi`) verified
the strict theorem and corrected the near-equality wording: finite zero
deficit lies on `a=0` or `b=0`, but affine-normalized near-equality also
includes reciprocal boundary regimes such as `a→∞` with `b` fixed.  See
`PAPER_PROOF.md` for the corrected quantitative statement.
