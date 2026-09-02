import L2Hexagon.UpperHalfAssembly

/-!
# Boundary parametrization behind the planar support-area formula

For a twice differentiable support function `h`, with displayed first and
second derivatives `k` and `l`, the canonical normal-angle boundary point is

`gamma(theta) = h(theta) n(theta) + k(theta) t(theta)`,

where `n(theta)=(cos theta,sin theta)` and
`t(theta)=(-sin theta,cos theta)`.  In coordinates this is

`gamma_x = h cos - k sin`,  `gamma_y = h sin + k cos`.

The first theorem package below checks directly that

`gamma' = (h+l)t` and `det(gamma,gamma') = h(h+l)`.

The second package specializes this identity to the genuinely curved Sector II
support.  It proves that the displayed coordinate path has oriented density
exactly `sectorTwoCurvature`, whose integral was evaluated previously.  This is
an exact boundary-line-integral precursor.  It does not identify the path with
the boundary of the halfspace-defined Firey body and does not invoke Green's
theorem or claim a Lebesgue-area identity.
-/

open Real Set MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- First coordinate of the canonical support boundary point `h n + k t`. -/
noncomputable def supportBoundaryX (h k : ℝ → ℝ) (θ : ℝ) : ℝ :=
  h θ * cos θ - k θ * sin θ

/-- Second coordinate of the canonical support boundary point `h n + k t`. -/
noncomputable def supportBoundaryY (h k : ℝ → ℝ) (θ : ℝ) : ℝ :=
  h θ * sin θ + k θ * cos θ

/-- First coordinate of the derivative `(h+l)t`. -/
noncomputable def supportBoundaryDX (h l : ℝ → ℝ) (θ : ℝ) : ℝ :=
  -(h θ + l θ) * sin θ

/-- Second coordinate of the derivative `(h+l)t`. -/
noncomputable def supportBoundaryDY (h l : ℝ → ℝ) (θ : ℝ) : ℝ :=
  (h θ + l θ) * cos θ

/-- Differentiating the first boundary coordinate gives the tangential speed. -/
theorem hasDerivAt_supportBoundaryX {h k l : ℝ → ℝ} {θ : ℝ}
    (hh : HasDerivAt h (k θ) θ) (hk : HasDerivAt k (l θ) θ) :
    HasDerivAt (supportBoundaryX h k) (supportBoundaryDX h l θ) θ := by
  unfold supportBoundaryX supportBoundaryDX
  exact ((hh.mul (Real.hasDerivAt_cos θ)).sub
    (hk.mul (Real.hasDerivAt_sin θ))).congr_deriv (by ring)

/-- Differentiating the second boundary coordinate gives the tangential speed. -/
theorem hasDerivAt_supportBoundaryY {h k l : ℝ → ℝ} {θ : ℝ}
    (hh : HasDerivAt h (k θ) θ) (hk : HasDerivAt k (l θ) θ) :
    HasDerivAt (supportBoundaryY h k) (supportBoundaryDY h l θ) θ := by
  unfold supportBoundaryY supportBoundaryDY
  exact ((hh.mul (Real.hasDerivAt_sin θ)).add
    (hk.mul (Real.hasDerivAt_cos θ))).congr_deriv (by ring)

/-- The canonical boundary point pairs with the normal to give `h`. -/
theorem supportBoundary_normal_pairing (h k : ℝ → ℝ) (θ : ℝ) :
    supportBoundaryX h k θ * cos θ + supportBoundaryY h k θ * sin θ = h θ := by
  unfold supportBoundaryX supportBoundaryY
  calc
    (h θ * cos θ - k θ * sin θ) * cos θ +
        (h θ * sin θ + k θ * cos θ) * sin θ =
      h θ * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = h θ := by rw [Real.sin_sq_add_cos_sq]; ring

/-- The canonical boundary point pairs with the tangent to give `k`. -/
theorem supportBoundary_tangent_pairing (h k : ℝ → ℝ) (θ : ℝ) :
    -supportBoundaryX h k θ * sin θ + supportBoundaryY h k θ * cos θ = k θ := by
  unfold supportBoundaryX supportBoundaryY
  calc
    -(h θ * cos θ - k θ * sin θ) * sin θ +
        (h θ * sin θ + k θ * cos θ) * cos θ =
      k θ * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = k θ := by rw [Real.sin_sq_add_cos_sq]; ring

/-- The oriented boundary density is `h(h+h'')`. -/
theorem supportBoundary_orientedDensity (h k l : ℝ → ℝ) (θ : ℝ) :
    supportBoundaryX h k θ * supportBoundaryDY h l θ -
        supportBoundaryY h k θ * supportBoundaryDX h l θ =
      h θ * (h θ + l θ) := by
  unfold supportBoundaryX supportBoundaryY supportBoundaryDX supportBoundaryDY
  calc
    (h θ * cos θ - k θ * sin θ) * ((h θ + l θ) * cos θ) -
        (h θ * sin θ + k θ * cos θ) * (-(h θ + l θ) * sin θ) =
      h θ * (h θ + l θ) * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = h θ * (h θ + l θ) := by rw [Real.sin_sq_add_cos_sq]; ring

/-- The explicit second derivative of the Sector II support. -/
noncomputable def sectorTwoSupportSecondDerivative (a b θ : ℝ) : ℝ :=
  sectorTwoBoundaryDerivative a b θ / √(sectorTwoSq a b θ) -
    sectorTwoBoundary a b θ ^ 2 / (√(sectorTwoSq a b θ)) ^ 3

/-- The displayed Sector II first derivative differentiates to the displayed second derivative. -/
theorem hasDerivAt_sectorTwoSupportDerivative {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    HasDerivAt (sectorTwoSupportDerivative a b)
      (sectorTwoSupportSecondDerivative a b θ) θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  have hsqrt : √(sectorTwoSq a b θ) ≠ 0 := (Real.sqrt_pos.2 hpos).ne'
  have hquot := (hasDerivAt_sectorTwoBoundary a b θ).div
    (hasDerivAt_sectorTwoSupport hb θ) hsqrt
  unfold sectorTwoSupportDerivative at hquot ⊢
  unfold sectorTwoSupport at hquot
  unfold sectorTwoSupportSecondDerivative
  exact hquot.congr_deriv (by field_simp [hsqrt])

/-- Sector II tangential speed, `h+h''`. -/
noncomputable def sectorTwoBoundarySpeed (a b θ : ℝ) : ℝ :=
  sectorTwoSupport a b θ + sectorTwoSupportSecondDerivative a b θ

/-- First coordinate of the canonical Sector II support boundary point. -/
noncomputable def sectorTwoBoundaryX (a b θ : ℝ) : ℝ :=
  supportBoundaryX (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ

/-- Second coordinate of the canonical Sector II support boundary point. -/
noncomputable def sectorTwoBoundaryY (a b θ : ℝ) : ℝ :=
  supportBoundaryY (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ

/-- First derivative coordinate of the canonical Sector II boundary path. -/
noncomputable def sectorTwoBoundaryDX (a b θ : ℝ) : ℝ :=
  -sectorTwoBoundarySpeed a b θ * sin θ

/-- Second derivative coordinate of the canonical Sector II boundary path. -/
noncomputable def sectorTwoBoundaryDY (a b θ : ℝ) : ℝ :=
  sectorTwoBoundarySpeed a b θ * cos θ

/-- The Sector II boundary `x`-coordinate has the displayed derivative. -/
theorem hasDerivAt_sectorTwoBoundaryX {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    HasDerivAt (sectorTwoBoundaryX a b) (sectorTwoBoundaryDX a b θ) θ := by
  change HasDerivAt
    (supportBoundaryX (sectorTwoSupport a b) (sectorTwoSupportDerivative a b))
    (-sectorTwoBoundarySpeed a b θ * sin θ) θ
  simpa [sectorTwoBoundarySpeed, supportBoundaryDX] using
    (hasDerivAt_supportBoundaryX (hasDerivAt_sectorTwoSupport hb θ)
      (hasDerivAt_sectorTwoSupportDerivative hb θ))

/-- The Sector II boundary `y`-coordinate has the displayed derivative. -/
theorem hasDerivAt_sectorTwoBoundaryY {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    HasDerivAt (sectorTwoBoundaryY a b) (sectorTwoBoundaryDY a b θ) θ := by
  change HasDerivAt
    (supportBoundaryY (sectorTwoSupport a b) (sectorTwoSupportDerivative a b))
    (sectorTwoBoundarySpeed a b θ * cos θ) θ
  simpa [sectorTwoBoundarySpeed, supportBoundaryDY] using
    (hasDerivAt_supportBoundaryY (hasDerivAt_sectorTwoSupport hb θ)
      (hasDerivAt_sectorTwoSupportDerivative hb θ))

/-- The Sector II support times its tangential speed is the checked curvature density. -/
theorem sectorTwoSupport_mul_boundarySpeed_eq_curvature {a b : ℝ}
    (hb : 0 < b) (θ : ℝ) :
    sectorTwoSupport a b θ * sectorTwoBoundarySpeed a b θ =
      sectorTwoCurvature a b θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  have hsqrt : √(sectorTwoSq a b θ) ≠ 0 := (Real.sqrt_pos.2 hpos).ne'
  have hsqrtSq : (√(sectorTwoSq a b θ)) ^ 2 = sectorTwoSq a b θ :=
    Real.sq_sqrt hpos.le
  have hsqrtFourth : (√(sectorTwoSq a b θ)) ^ 4 = sectorTwoSq a b θ ^ 2 := by
    calc
      (√(sectorTwoSq a b θ)) ^ 4 = (√(sectorTwoSq a b θ) ^ 2) ^ 2 := by ring
      _ = sectorTwoSq a b θ ^ 2 := by rw [hsqrtSq]
  have hdet := sectorTwo_gramDet a b θ
  unfold sectorTwoBoundarySpeed sectorTwoSupportSecondDerivative sectorTwoSupport
    sectorTwoCurvature sectorTwoBoundaryDerivative at ⊢
  field_simp [hsqrt, hpos.ne']
  rw [hsqrtFourth]
  nlinarith [hdet]

/-- The oriented density of the canonical Sector II boundary path. -/
noncomputable def sectorTwoBoundaryOrientedDensity (a b θ : ℝ) : ℝ :=
  sectorTwoBoundaryX a b θ * sectorTwoBoundaryDY a b θ -
    sectorTwoBoundaryY a b θ * sectorTwoBoundaryDX a b θ

/-- The actual differentiated Sector II boundary path has oriented density `sectorTwoCurvature`. -/
theorem sectorTwoBoundaryOrientedDensity_eq_curvature {a b : ℝ}
    (hb : 0 < b) (θ : ℝ) :
    sectorTwoBoundaryOrientedDensity a b θ = sectorTwoCurvature a b θ := by
  rw [sectorTwoBoundaryOrientedDensity, sectorTwoBoundaryX, sectorTwoBoundaryY,
    sectorTwoBoundaryDX, sectorTwoBoundaryDY]
  calc
    supportBoundaryX (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ *
          (sectorTwoBoundarySpeed a b θ * cos θ) -
        supportBoundaryY (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ *
          (-sectorTwoBoundarySpeed a b θ * sin θ) =
        sectorTwoSupport a b θ * sectorTwoBoundarySpeed a b θ := by
          simpa [sectorTwoBoundarySpeed, supportBoundaryDX, supportBoundaryDY] using
            supportBoundary_orientedDensity (sectorTwoSupport a b)
              (sectorTwoSupportDerivative a b) (sectorTwoSupportSecondDerivative a b) θ
    _ = sectorTwoCurvature a b θ := sectorTwoSupport_mul_boundarySpeed_eq_curvature hb θ

/-- The exact oriented line-density integral along the curved Sector II boundary arc. -/
theorem integral_sectorTwoBoundaryOrientedDensity {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2..π / 2 + arctan (b / a),
      sectorTwoBoundaryOrientedDensity a b θ) =
        (1 + b) * arctan (b / a) := by
  calc
    (∫ θ in π / 2..π / 2 + arctan (b / a),
      sectorTwoBoundaryOrientedDensity a b θ) =
        ∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ := by
          apply intervalIntegral.integral_congr
          intro θ _
          exact sectorTwoBoundaryOrientedDensity_eq_curvature hb θ
    _ = (1 + b) * arctan (b / a) := integral_sectorTwoCurvature ha hb

/-- Squared norm of the derivative of the Sector III moving coordinate pair. -/
noncomputable def sectorThreeDerivativeNormSq (a b θ : ℝ) : ℝ :=
  cos θ ^ 2 + sectorThreeZ a b θ ^ 2

/-- Derivative of `sectorThreeBoundary`. -/
noncomputable def sectorThreeBoundaryDerivative (a b θ : ℝ) : ℝ :=
  sectorThreeDerivativeNormSq a b θ - sectorThreeSq a b θ

/-- The positive support represented by the Sector III support square. -/
noncomputable def sectorThreeSupport (a b θ : ℝ) : ℝ :=
  √(sectorThreeSq a b θ)

/-- The derivative of the Sector III support. -/
noncomputable def sectorThreeSupportDerivative (a b θ : ℝ) : ℝ :=
  sectorThreeBoundary a b θ / √(sectorThreeSq a b θ)

/-- The explicit second derivative of the Sector III support. -/
noncomputable def sectorThreeSupportSecondDerivative (a b θ : ℝ) : ℝ :=
  sectorThreeBoundaryDerivative a b θ / √(sectorThreeSq a b θ) -
    sectorThreeBoundary a b θ ^ 2 / (√(sectorThreeSq a b θ)) ^ 3

/-- The oriented curvature density of the Sector III boundary arc. -/
noncomputable def sectorThreeCurvature (a b θ : ℝ) : ℝ :=
  (1 + a) ^ 2 / sectorThreeSq a b θ

theorem hasDerivAt_sectorThreeW (a b θ : ℝ) :
    HasDerivAt (sectorThreeW a b) (sectorThreeZ a b θ) θ := by
  unfold sectorThreeW sectorThreeZ
  exact (((Real.hasDerivAt_cos θ).const_mul (1 + a)).add
    ((Real.hasDerivAt_sin θ).const_mul b)).congr_deriv (by ring)

theorem hasDerivAt_sectorThreeZ (a b θ : ℝ) :
    HasDerivAt (sectorThreeZ a b) (-sectorThreeW a b θ) θ := by
  unfold sectorThreeW sectorThreeZ
  exact (((Real.hasDerivAt_sin θ).const_mul (-(1 + a))).add
    ((Real.hasDerivAt_cos θ).const_mul b)).congr_deriv (by ring)

/-- The derivative of the Sector III support square is twice `h h'`. -/
theorem hasDerivAt_sectorThreeSq (a b θ : ℝ) :
    HasDerivAt (sectorThreeSq a b) (2 * sectorThreeBoundary a b θ) θ := by
  unfold sectorThreeSq sectorThreeBoundary
  exact (((Real.hasDerivAt_sin θ).pow 2).add
    ((hasDerivAt_sectorThreeW a b θ).pow 2)).congr_deriv (by ring)

/-- The derivative of the Sector III endpoint quantity. -/
theorem hasDerivAt_sectorThreeBoundary (a b θ : ℝ) :
    HasDerivAt (sectorThreeBoundary a b) (sectorThreeBoundaryDerivative a b θ) θ := by
  unfold sectorThreeBoundary sectorThreeBoundaryDerivative sectorThreeDerivativeNormSq
    sectorThreeSq
  exact (((Real.hasDerivAt_sin θ).mul (Real.hasDerivAt_cos θ)).add
    ((hasDerivAt_sectorThreeW a b θ).mul
      (hasDerivAt_sectorThreeZ a b θ))).congr_deriv (by ring)

/-- Sector III never has zero support when `a>0`. -/
theorem sectorThreeSq_pos {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    0 < sectorThreeSq a b θ := by
  rw [sectorThreeSq_reflect]
  exact sectorTwoSq_pos (a := b) ha (3 * π / 2 - θ)

/-- The two Sector III moving coordinate vectors have determinant square `(1+a)^2`. -/
theorem sectorThree_gramDet (a b θ : ℝ) :
    sectorThreeSq a b θ * sectorThreeDerivativeNormSq a b θ -
        sectorThreeBoundary a b θ ^ 2 = (1 + a) ^ 2 := by
  have htrig := Real.sin_sq_add_cos_sq θ
  unfold sectorThreeSq sectorThreeDerivativeNormSq sectorThreeBoundary
    sectorThreeW sectorThreeZ
  nlinarith [sq_nonneg
    (sin θ * (-(1 + a) * sin θ + b * cos θ) -
      cos θ * ((1 + a) * cos θ + b * sin θ) + (1 + a))]

/-- The Sector III square-root support has the displayed derivative. -/
theorem hasDerivAt_sectorThreeSupport {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    HasDerivAt (sectorThreeSupport a b) (sectorThreeSupportDerivative a b θ) θ := by
  have hpos := sectorThreeSq_pos (b := b) ha θ
  unfold sectorThreeSupport sectorThreeSupportDerivative
  exact ((hasDerivAt_sectorThreeSq a b θ).sqrt hpos.ne').congr_deriv (by
    field_simp [(Real.sqrt_pos.2 hpos).ne'])

/-- The Sector III displayed first derivative has the displayed second derivative. -/
theorem hasDerivAt_sectorThreeSupportDerivative {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    HasDerivAt (sectorThreeSupportDerivative a b)
      (sectorThreeSupportSecondDerivative a b θ) θ := by
  have hpos := sectorThreeSq_pos (b := b) ha θ
  have hsqrt : √(sectorThreeSq a b θ) ≠ 0 := (Real.sqrt_pos.2 hpos).ne'
  have hquot := (hasDerivAt_sectorThreeBoundary a b θ).div
    (hasDerivAt_sectorThreeSupport ha θ) hsqrt
  unfold sectorThreeSupportDerivative at hquot ⊢
  unfold sectorThreeSupport at hquot
  unfold sectorThreeSupportSecondDerivative
  exact hquot.congr_deriv (by field_simp [hsqrt])

/-- Sector III tangential speed, `h+h''`. -/
noncomputable def sectorThreeBoundarySpeed (a b θ : ℝ) : ℝ :=
  sectorThreeSupport a b θ + sectorThreeSupportSecondDerivative a b θ

/-- First coordinate of the canonical Sector III support boundary point. -/
noncomputable def sectorThreeBoundaryX (a b θ : ℝ) : ℝ :=
  supportBoundaryX (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ

/-- Second coordinate of the canonical Sector III support boundary point. -/
noncomputable def sectorThreeBoundaryY (a b θ : ℝ) : ℝ :=
  supportBoundaryY (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ

/-- First derivative coordinate of the canonical Sector III boundary path. -/
noncomputable def sectorThreeBoundaryDX (a b θ : ℝ) : ℝ :=
  -sectorThreeBoundarySpeed a b θ * sin θ

/-- Second derivative coordinate of the canonical Sector III boundary path. -/
noncomputable def sectorThreeBoundaryDY (a b θ : ℝ) : ℝ :=
  sectorThreeBoundarySpeed a b θ * cos θ

theorem hasDerivAt_sectorThreeBoundaryX {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    HasDerivAt (sectorThreeBoundaryX a b) (sectorThreeBoundaryDX a b θ) θ := by
  change HasDerivAt
    (supportBoundaryX (sectorThreeSupport a b) (sectorThreeSupportDerivative a b))
    (-sectorThreeBoundarySpeed a b θ * sin θ) θ
  simpa [sectorThreeBoundarySpeed, supportBoundaryDX] using
    (hasDerivAt_supportBoundaryX (hasDerivAt_sectorThreeSupport ha θ)
      (hasDerivAt_sectorThreeSupportDerivative ha θ))

theorem hasDerivAt_sectorThreeBoundaryY {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    HasDerivAt (sectorThreeBoundaryY a b) (sectorThreeBoundaryDY a b θ) θ := by
  change HasDerivAt
    (supportBoundaryY (sectorThreeSupport a b) (sectorThreeSupportDerivative a b))
    (sectorThreeBoundarySpeed a b θ * cos θ) θ
  simpa [sectorThreeBoundarySpeed, supportBoundaryDY] using
    (hasDerivAt_supportBoundaryY (hasDerivAt_sectorThreeSupport ha θ)
      (hasDerivAt_sectorThreeSupportDerivative ha θ))

/-- Sector III support times tangential speed is its curvature density. -/
theorem sectorThreeSupport_mul_boundarySpeed_eq_curvature {a b : ℝ}
    (ha : 0 < a) (θ : ℝ) :
    sectorThreeSupport a b θ * sectorThreeBoundarySpeed a b θ =
      sectorThreeCurvature a b θ := by
  have hpos := sectorThreeSq_pos (b := b) ha θ
  have hsqrt : √(sectorThreeSq a b θ) ≠ 0 := (Real.sqrt_pos.2 hpos).ne'
  have hsqrtSq : (√(sectorThreeSq a b θ)) ^ 2 = sectorThreeSq a b θ :=
    Real.sq_sqrt hpos.le
  have hsqrtFourth : (√(sectorThreeSq a b θ)) ^ 4 = sectorThreeSq a b θ ^ 2 := by
    calc
      (√(sectorThreeSq a b θ)) ^ 4 = (√(sectorThreeSq a b θ) ^ 2) ^ 2 := by ring
      _ = sectorThreeSq a b θ ^ 2 := by rw [hsqrtSq]
  have hdet := sectorThree_gramDet a b θ
  unfold sectorThreeBoundarySpeed sectorThreeSupportSecondDerivative sectorThreeSupport
    sectorThreeCurvature sectorThreeBoundaryDerivative at ⊢
  field_simp [hsqrt, hpos.ne']
  rw [hsqrtFourth]
  nlinarith [hdet]

/-- Oriented density of the canonical Sector III boundary path. -/
noncomputable def sectorThreeBoundaryOrientedDensity (a b θ : ℝ) : ℝ :=
  sectorThreeBoundaryX a b θ * sectorThreeBoundaryDY a b θ -
    sectorThreeBoundaryY a b θ * sectorThreeBoundaryDX a b θ

theorem sectorThreeBoundaryOrientedDensity_eq_curvature {a b : ℝ}
    (ha : 0 < a) (θ : ℝ) :
    sectorThreeBoundaryOrientedDensity a b θ = sectorThreeCurvature a b θ := by
  rw [sectorThreeBoundaryOrientedDensity, sectorThreeBoundaryX, sectorThreeBoundaryY,
    sectorThreeBoundaryDX, sectorThreeBoundaryDY]
  calc
    supportBoundaryX (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ *
          (sectorThreeBoundarySpeed a b θ * cos θ) -
        supportBoundaryY (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ *
          (-sectorThreeBoundarySpeed a b θ * sin θ) =
        sectorThreeSupport a b θ * sectorThreeBoundarySpeed a b θ := by
          simpa [sectorThreeBoundarySpeed, supportBoundaryDX, supportBoundaryDY] using
            supportBoundary_orientedDensity (sectorThreeSupport a b)
              (sectorThreeSupportDerivative a b) (sectorThreeSupportSecondDerivative a b) θ
    _ = sectorThreeCurvature a b θ := sectorThreeSupport_mul_boundarySpeed_eq_curvature ha θ

/-- Sector III curvature is reflected Sector II curvature with swapped parameters. -/
theorem sectorThreeCurvature_reflect (a b θ : ℝ) :
    sectorThreeCurvature a b θ = sectorTwoCurvature b a (3 * π / 2 - θ) := by
  unfold sectorThreeCurvature sectorTwoCurvature
  rw [sectorThreeSq_reflect]

/-- Exact oriented line-density integral along the curved Sector III boundary arc. -/
theorem integral_sectorThreeBoundaryOrientedDensity {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2 + arctan (b / a)..π,
      sectorThreeBoundaryOrientedDensity a b θ) =
        (1 + a) * (π / 2 - arctan (b / a)) := by
  have hangle := arctan_div_swap ha hb
  calc
    (∫ θ in π / 2 + arctan (b / a)..π,
      sectorThreeBoundaryOrientedDensity a b θ) =
        ∫ θ in π / 2 + arctan (b / a)..π, sectorThreeCurvature a b θ := by
          apply intervalIntegral.integral_congr
          intro θ _
          exact sectorThreeBoundaryOrientedDensity_eq_curvature ha θ
    _ = ∫ θ in π / 2 + arctan (b / a)..π,
          sectorTwoCurvature b a (3 * π / 2 - θ) := by
            apply intervalIntegral.integral_congr
            intro θ _
            exact sectorThreeCurvature_reflect a b θ
    _ = ∫ η in 3 * π / 2 - π..
          3 * π / 2 - (π / 2 + arctan (b / a)), sectorTwoCurvature b a η := by
            rw [intervalIntegral.integral_comp_sub_left]
    _ = ∫ η in π / 2..π / 2 + arctan (a / b), sectorTwoCurvature b a η := by
            congr 1
            · ring
            · rw [hangle]
              ring
    _ = (1 + a) * arctan (a / b) := integral_sectorTwoCurvature hb ha
    _ = (1 + a) * (π / 2 - arctan (b / a)) := by rw [hangle]

#print axioms hasDerivAt_supportBoundaryX
#print axioms hasDerivAt_supportBoundaryY
#print axioms supportBoundary_normal_pairing
#print axioms supportBoundary_tangent_pairing
#print axioms supportBoundary_orientedDensity
#print axioms hasDerivAt_sectorTwoSupportDerivative
#print axioms hasDerivAt_sectorTwoBoundaryX
#print axioms hasDerivAt_sectorTwoBoundaryY
#print axioms sectorTwoSupport_mul_boundarySpeed_eq_curvature
#print axioms sectorTwoBoundaryOrientedDensity_eq_curvature
#print axioms integral_sectorTwoBoundaryOrientedDensity
#print axioms hasDerivAt_sectorThreeSupport
#print axioms hasDerivAt_sectorThreeSupportDerivative
#print axioms hasDerivAt_sectorThreeBoundaryX
#print axioms hasDerivAt_sectorThreeBoundaryY
#print axioms sectorThreeSupport_mul_boundarySpeed_eq_curvature
#print axioms sectorThreeBoundaryOrientedDensity_eq_curvature
#print axioms integral_sectorThreeBoundaryOrientedDensity

end L2Hexagon
