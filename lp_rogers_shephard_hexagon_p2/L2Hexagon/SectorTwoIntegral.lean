import L2Hexagon.NormalizedDeficit
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# The curved Sector II endpoint correction

On the second support sector of the normalized hexagon, put `B = 1 + b` and

`F(θ) = (a cos θ + B sin θ)² + cos² θ`.

Thus `F = h²` for the Firey support on this sector.  This file proves the
exact differential identity

`F - (F'/2)²/F = B²/F - (F'/2)'`

and integrates its total-derivative term.  At the endpoints
`π/2` and `π/2 + φ`, where `a sin φ = b cos φ`, the change of `F'/2` is
exactly `ab`.  Consequently the sector density integral is the curvature
integral minus `ab`.

The curvature integral is evaluated by the phase primitive

`-(1+b) arctan (cos θ / U(θ))`.

The proof checks that `U` stays strictly positive on the entire closed sector,
so the quotient and the arctangent branch are legitimate.  The planar
support-area theorem that identifies this density integral with Lebesgue area
is intentionally outside this module's claim.
-/

open Real Set MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- First moving coordinate in the Sector II support-square representation. -/
noncomputable def sectorTwoU (a b θ : ℝ) : ℝ :=
  a * cos θ + (1 + b) * sin θ

/-- Derivative of `sectorTwoU`. -/
noncomputable def sectorTwoV (a b θ : ℝ) : ℝ :=
  -a * sin θ + (1 + b) * cos θ

/-- The squared support `h²` on Sector II. -/
noncomputable def sectorTwoSq (a b θ : ℝ) : ℝ :=
  sectorTwoU a b θ ^ 2 + cos θ ^ 2

/-- The squared norm of the derivative of the two-coordinate support vector. -/
noncomputable def sectorTwoDerivativeNormSq (a b θ : ℝ) : ℝ :=
  sectorTwoV a b θ ^ 2 + sin θ ^ 2

/-- The quantity `h h' = F'/2` written without a square root. -/
noncomputable def sectorTwoBoundary (a b θ : ℝ) : ℝ :=
  sectorTwoU a b θ * sectorTwoV a b θ - cos θ * sin θ

/-- The derivative of `sectorTwoBoundary`. -/
noncomputable def sectorTwoBoundaryDerivative (a b θ : ℝ) : ℝ :=
  sectorTwoDerivativeNormSq a b θ - sectorTwoSq a b θ

/-- The positive support represented by the Sector II support square. -/
noncomputable def sectorTwoSupport (a b θ : ℝ) : ℝ :=
  √(sectorTwoSq a b θ)

/-- The derivative of the Sector II support, written as `(F'/2)/√F`. -/
noncomputable def sectorTwoSupportDerivative (a b θ : ℝ) : ℝ :=
  sectorTwoBoundary a b θ / √(sectorTwoSq a b θ)

/-- The support-area density written in terms of `F = h²` and `F'/2 = h h'`. -/
noncomputable def sectorTwoDensity (a b θ : ℝ) : ℝ :=
  sectorTwoSq a b θ - sectorTwoBoundary a b θ ^ 2 / sectorTwoSq a b θ

/-- The determinant or curvature term on Sector II. -/
noncomputable def sectorTwoCurvature (a b θ : ℝ) : ℝ :=
  (1 + b) ^ 2 / sectorTwoSq a b θ

/-- The phase ratio whose arctangent linearizes the Sector II curvature. -/
noncomputable def sectorTwoPhaseRatio (a b θ : ℝ) : ℝ :=
  cos θ / sectorTwoU a b θ

/-- An antiderivative of the Sector II curvature on the genuine sector. -/
noncomputable def sectorTwoCurvaturePrimitive (a b θ : ℝ) : ℝ :=
  -(1 + b) * arctan (sectorTwoPhaseRatio a b θ)

theorem hasDerivAt_sectorTwoU (a b θ : ℝ) :
    HasDerivAt (sectorTwoU a b) (sectorTwoV a b θ) θ := by
  unfold sectorTwoU sectorTwoV
  exact (((Real.hasDerivAt_cos θ).const_mul a).add
    ((Real.hasDerivAt_sin θ).const_mul (1 + b))).congr_deriv (by ring)

theorem hasDerivAt_sectorTwoV (a b θ : ℝ) :
    HasDerivAt (sectorTwoV a b) (-sectorTwoU a b θ) θ := by
  unfold sectorTwoU sectorTwoV
  exact (((Real.hasDerivAt_sin θ).const_mul (-a)).add
    ((Real.hasDerivAt_cos θ).const_mul (1 + b))).congr_deriv (by ring)

/-- The numerator in the quotient derivative collapses to the constant `1+b`. -/
theorem sectorTwoU_mul_sin_add_cos_mul_V (a b θ : ℝ) :
    sectorTwoU a b θ * sin θ + cos θ * sectorTwoV a b θ = 1 + b := by
  unfold sectorTwoU sectorTwoV
  calc
    (a * cos θ + (1 + b) * sin θ) * sin θ +
        cos θ * (-a * sin θ + (1 + b) * cos θ) =
      (1 + b) * (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = 1 + b := by rw [Real.sin_sq_add_cos_sq]; ring

/-- Derivative of the phase quotient wherever its denominator is nonzero. -/
theorem hasDerivAt_sectorTwoPhaseRatio {a b θ : ℝ}
    (hU : sectorTwoU a b θ ≠ 0) :
    HasDerivAt (sectorTwoPhaseRatio a b)
      (-(1 + b) / sectorTwoU a b θ ^ 2) θ := by
  have hquot := (Real.hasDerivAt_cos θ).div (hasDerivAt_sectorTwoU a b θ) hU
  unfold sectorTwoPhaseRatio
  exact hquot.congr_deriv (by
    field_simp [hU]
    have hidentity := sectorTwoU_mul_sin_add_cos_mul_V a b θ
    linarith)

/-- The phase primitive differentiates to the exact curvature wherever `U ≠ 0`. -/
theorem hasDerivAt_sectorTwoCurvaturePrimitive {a b θ : ℝ}
    (hU : sectorTwoU a b θ ≠ 0) :
    HasDerivAt (sectorTwoCurvaturePrimitive a b) (sectorTwoCurvature a b θ) θ := by
  have hratio := hasDerivAt_sectorTwoPhaseRatio (a := a) (b := b) (θ := θ) hU
  have hatan := (Real.hasDerivAt_arctan (sectorTwoPhaseRatio a b θ)).comp θ hratio
  unfold sectorTwoCurvaturePrimitive sectorTwoCurvature sectorTwoSq sectorTwoPhaseRatio
  exact hatan.const_mul (-(1 + b)) |>.congr_deriv (by
    simp only [sectorTwoPhaseRatio]
    field_simp [hU])

theorem hasDerivAt_sectorTwoBoundary (a b θ : ℝ) :
    HasDerivAt (sectorTwoBoundary a b) (sectorTwoBoundaryDerivative a b θ) θ := by
  unfold sectorTwoBoundary sectorTwoBoundaryDerivative sectorTwoDerivativeNormSq sectorTwoSq
  exact (((hasDerivAt_sectorTwoU a b θ).mul (hasDerivAt_sectorTwoV a b θ)).sub
    ((Real.hasDerivAt_cos θ).mul (Real.hasDerivAt_sin θ))).congr_deriv (by ring)

/-- The derivative of the support square is twice the endpoint quantity `h h'`. -/
theorem hasDerivAt_sectorTwoSq (a b θ : ℝ) :
    HasDerivAt (sectorTwoSq a b) (2 * sectorTwoBoundary a b θ) θ := by
  unfold sectorTwoSq sectorTwoBoundary
  exact (((hasDerivAt_sectorTwoU a b θ).pow 2).add
    ((Real.hasDerivAt_cos θ).pow 2)).congr_deriv (by ring)

/-- The two moving coordinate vectors have constant squared determinant `(1+b)²`. -/
theorem sectorTwo_gramDet (a b θ : ℝ) :
    sectorTwoSq a b θ * sectorTwoDerivativeNormSq a b θ -
        sectorTwoBoundary a b θ ^ 2 = (1 + b) ^ 2 := by
  have htrig := Real.sin_sq_add_cos_sq θ
  unfold sectorTwoSq sectorTwoDerivativeNormSq sectorTwoBoundary sectorTwoU sectorTwoV
  nlinarith [sq_nonneg
    ((a * cos θ + (1 + b) * sin θ) * sin θ +
      cos θ * (-a * sin θ + (1 + b) * cos θ) - (1 + b))]

/-- The Sector II squared support never vanishes when `b > 0`. -/
theorem sectorTwoSq_pos {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    0 < sectorTwoSq a b θ := by
  have hnonneg : 0 ≤ sectorTwoSq a b θ := by
    unfold sectorTwoSq
    positivity
  by_contra hnot
  have hzero : sectorTwoSq a b θ = 0 := le_antisymm (le_of_not_gt hnot) hnonneg
  have hdet := sectorTwo_gramDet a b θ
  have hB : 0 < (1 + b) ^ 2 := sq_pos_of_pos (by linarith)
  rw [hzero, zero_mul, zero_sub] at hdet
  nlinarith [sq_nonneg (sectorTwoBoundary a b θ)]

/-- The square-root support has the claimed derivative on every Sector II parameter line. -/
theorem hasDerivAt_sectorTwoSupport {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    HasDerivAt (sectorTwoSupport a b) (sectorTwoSupportDerivative a b θ) θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  unfold sectorTwoSupport sectorTwoSupportDerivative
  exact ((hasDerivAt_sectorTwoSq a b θ).sqrt hpos.ne').congr_deriv (by
    field_simp [(Real.sqrt_pos.2 hpos).ne'])

/-- The square-root expression really yields `h²-(h')² = sectorTwoDensity`. -/
theorem sectorTwoSupport_sq_sub_derivative_sq {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    sectorTwoSupport a b θ ^ 2 - sectorTwoSupportDerivative a b θ ^ 2 =
      sectorTwoDensity a b θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  unfold sectorTwoSupport sectorTwoSupportDerivative sectorTwoDensity
  rw [Real.sq_sqrt hpos.le]
  field_simp [(Real.sqrt_pos.2 hpos).ne', hpos.ne']
  rw [Real.sq_sqrt hpos.le]
  ring

/-- Pointwise determinant decomposition of the Sector II support-area density. -/
theorem sectorTwoDensity_eq_curvature_sub_boundaryDerivative {a b : ℝ}
    (hb : 0 < b) (θ : ℝ) :
    sectorTwoDensity a b θ =
      sectorTwoCurvature a b θ - sectorTwoBoundaryDerivative a b θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  have hdet := sectorTwo_gramDet a b θ
  unfold sectorTwoDensity sectorTwoCurvature sectorTwoBoundaryDerivative
  field_simp [hpos.ne']
  nlinarith

/-- The left endpoint value `h h' = -a(1+b)`. -/
theorem sectorTwoBoundary_pi_div_two (a b : ℝ) :
    sectorTwoBoundary a b (π / 2) = -a * (1 + b) := by
  simp [sectorTwoBoundary, sectorTwoU, sectorTwoV]
  ring

/-- At the right sector endpoint, the generator sign-change relation forces `h h' = -a`. -/
theorem sectorTwoBoundary_pi_div_two_add {a b φ : ℝ}
    (hφ : a * sin φ = b * cos φ) :
    sectorTwoBoundary a b (π / 2 + φ) = -a := by
  have harg : π / 2 + φ = φ + π / 2 := by ring
  have hU' : a * -sin φ + (1 + b) * cos φ = cos φ := by
    linarith
  have hφsin := congrArg (fun z : ℝ => z * sin φ) hφ
  rw [harg]
  simp only [sectorTwoBoundary, sectorTwoU, sectorTwoV,
    Real.sin_add_pi_div_two, Real.cos_add_pi_div_two]
  rw [hU']
  calc
    cos φ * (-a * cos φ + (1 + b) * -sin φ) - -sin φ * cos φ =
        -a * cos φ ^ 2 - b * cos φ * sin φ := by ring
    _ = -a * cos φ ^ 2 - a * sin φ * sin φ := by rw [hφsin]
    _ = -a * (sin φ ^ 2 + cos φ ^ 2) := by ring
    _ = -a := by rw [Real.sin_sq_add_cos_sq]; ring

/-- The arctangent generator angle satisfies the right-endpoint sign-change relation. -/
theorem generatorAngle_sin_relation {a b : ℝ} (ha : 0 < a) :
    a * sin (arctan (b / a)) = b * cos (arctan (b / a)) := by
  have hc : cos (arctan (b / a)) ≠ 0 := (Real.cos_arctan_pos _).ne'
  have ht := Real.tan_mul_cos hc
  rw [Real.tan_arctan] at ht
  rw [← ht]
  field_simp [ha.ne']

/-- The phase denominator is strictly positive on the whole closed Sector II interval. -/
theorem sectorTwoU_pos_on_sector {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    0 < sectorTwoU a b θ := by
  let t := θ - π / 2
  have hφ := generatorAngle_mem_Ioo ha hb
  have ht0 : 0 ≤ t := by
    dsimp [t]
    linarith [hθ.1]
  have htφ : t ≤ arctan (b / a) := by
    dsimp [t]
    linarith [hθ.2]
  have htmem : t ∈ Ioo (-(π / 2)) (π / 2) := by
    constructor
    · linarith [Real.pi_div_two_pos]
    · exact lt_of_le_of_lt htφ hφ.2
  have hφmem : arctan (b / a) ∈ Ioo (-(π / 2)) (π / 2) := by
    constructor
    · linarith [hφ.1, Real.pi_div_two_pos]
    · exact hφ.2
  have htan : tan t ≤ tan (arctan (b / a)) :=
    Real.strictMonoOn_tan.monotoneOn htmem hφmem htφ
  rw [Real.tan_arctan] at htan
  have hcos : 0 < cos t := Real.cos_pos_of_mem_Ioo htmem
  have hsinle : a * sin t ≤ b * cos t := by
    rw [← Real.tan_mul_cos hcos.ne']
    calc
      a * (tan t * cos t) ≤ a * ((b / a) * cos t) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right htan hcos.le) ha.le
      _ = b * cos t := by field_simp [ha.ne']
  have hθform : θ = π / 2 + t := by
    dsimp [t]
    ring
  rw [hθform]
  simp only [sectorTwoU, Real.cos_add, Real.sin_add, Real.cos_pi_div_two,
    Real.sin_pi_div_two, zero_mul, one_mul, zero_sub, add_zero]
  nlinarith

/-- The phase ratio vanishes at the left endpoint. -/
theorem sectorTwoPhaseRatio_pi_div_two (a b : ℝ) :
    sectorTwoPhaseRatio a b (π / 2) = 0 := by
  simp [sectorTwoPhaseRatio]

/-- At the right endpoint the phase ratio is the negative generator slope. -/
theorem sectorTwoPhaseRatio_pi_div_two_add {a b : ℝ} (ha : 0 < a) :
    sectorTwoPhaseRatio a b (π / 2 + arctan (b / a)) = -(b / a) := by
  let φ := arctan (b / a)
  have hrelation : a * sin φ = b * cos φ := by
    simpa [φ] using generatorAngle_sin_relation (b := b) ha
  have hU : a * -sin φ + (1 + b) * cos φ = cos φ := by
    linarith
  have hcos : cos φ ≠ 0 := by
    have hc := (Real.cos_arctan_pos (b / a)).ne'
    simpa [φ] using hc
  have harg : π / 2 + φ = φ + π / 2 := by ring
  rw [show arctan (b / a) = φ by rfl, harg]
  simp only [sectorTwoPhaseRatio, sectorTwoU, Real.cos_add_pi_div_two,
    Real.sin_add_pi_div_two]
  rw [hU]
  rw [show -sin φ / cos φ = -(tan φ) by
    rw [Real.tan_eq_sin_div_cos]
    ring]
  simp [φ]

/-- Endpoint values of the phase primitive across Sector II. -/
theorem sectorTwoCurvaturePrimitive_endpoints {a b : ℝ} (ha : 0 < a) :
    sectorTwoCurvaturePrimitive a b (π / 2 + arctan (b / a)) -
        sectorTwoCurvaturePrimitive a b (π / 2) =
      (1 + b) * arctan (b / a) := by
  rw [sectorTwoCurvaturePrimitive, sectorTwoCurvaturePrimitive,
    sectorTwoPhaseRatio_pi_div_two_add ha, sectorTwoPhaseRatio_pi_div_two,
    Real.arctan_neg]
  simp
  ring

/-- The determinant curvature integrates to the exact angular contribution `(1+b)φ`. -/
theorem integral_sectorTwoCurvature {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ) =
      (1 + b) * arctan (b / a) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  have hle : π / 2 ≤ π / 2 + arctan (b / a) := by linarith
  have hcurv : IntervalIntegrable (sectorTwoCurvature a b) volume
      (π / 2) (π / 2 + arctan (b / a)) := by
    have hcontF : Continuous (sectorTwoSq a b) := by
      unfold sectorTwoSq sectorTwoU
      fun_prop
    apply Continuous.intervalIntegrable
    unfold sectorTwoCurvature
    apply Continuous.div continuous_const
    · exact hcontF
    · intro θ
      exact (sectorTwoSq_pos (a := a) hb θ).ne'
  have hftc :
      (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ) =
        sectorTwoCurvaturePrimitive a b (π / 2 + arctan (b / a)) -
          sectorTwoCurvaturePrimitive a b (π / 2) := by
    apply intervalIntegral.integral_eq_sub_of_hasDerivAt
    · intro θ hθ
      rw [uIcc_of_le hle] at hθ
      exact hasDerivAt_sectorTwoCurvaturePrimitive
        (sectorTwoU_pos_on_sector ha hb hθ).ne'
    · exact hcurv
  rw [hftc, sectorTwoCurvaturePrimitive_endpoints ha]

/-- The endpoint correction across Sector II is exactly `ab`. -/
theorem sectorTwoBoundary_change {a b : ℝ} (ha : 0 < a) :
    sectorTwoBoundary a b (π / 2 + arctan (b / a)) -
        sectorTwoBoundary a b (π / 2) = a * b := by
  rw [sectorTwoBoundary_pi_div_two_add (generatorAngle_sin_relation ha),
    sectorTwoBoundary_pi_div_two]
  ring

/--
The exact Sector II integral reduction.  The support-area density integral is
the curvature integral minus the nonzero endpoint correction `ab`.
-/
theorem integral_sectorTwoDensity_eq_curvature_sub {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoDensity a b θ) =
      (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ) - a * b := by
  have hcurv : IntervalIntegrable (sectorTwoCurvature a b) volume
      (π / 2) (π / 2 + arctan (b / a)) := by
    have hcontF : Continuous (sectorTwoSq a b) := by
      unfold sectorTwoSq sectorTwoU
      fun_prop
    apply Continuous.intervalIntegrable
    unfold sectorTwoCurvature
    apply Continuous.div continuous_const
    · exact hcontF
    · intro θ
      exact (sectorTwoSq_pos (a := a) hb θ).ne'
  have hboundary : IntervalIntegrable (sectorTwoBoundaryDerivative a b) volume
      (π / 2) (π / 2 + arctan (b / a)) := by
    apply Continuous.intervalIntegrable
    unfold sectorTwoBoundaryDerivative sectorTwoDerivativeNormSq sectorTwoSq
      sectorTwoU sectorTwoV
    fun_prop
  have hftc :
      (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoBoundaryDerivative a b θ) =
        sectorTwoBoundary a b (π / 2 + arctan (b / a)) -
          sectorTwoBoundary a b (π / 2) := by
    exact intervalIntegral.integral_eq_sub_of_hasDerivAt
      (fun θ _ => hasDerivAt_sectorTwoBoundary a b θ) hboundary
  calc
    (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoDensity a b θ) =
        ∫ θ in π / 2..π / 2 + arctan (b / a),
          sectorTwoCurvature a b θ - sectorTwoBoundaryDerivative a b θ := by
            apply intervalIntegral.integral_congr
            intro θ _
            exact sectorTwoDensity_eq_curvature_sub_boundaryDerivative hb θ
    _ = (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ) -
          ∫ θ in π / 2..π / 2 + arctan (b / a),
            sectorTwoBoundaryDerivative a b θ := by
              rw [intervalIntegral.integral_sub hcurv hboundary]
    _ = (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoCurvature a b θ) -
          a * b := by
            rw [hftc, sectorTwoBoundary_change ha]

/-- The complete exact Sector II contribution, including its endpoint correction. -/
theorem integral_sectorTwoDensity {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoDensity a b θ) =
      (1 + b) * arctan (b / a) - a * b := by
  rw [integral_sectorTwoDensity_eq_curvature_sub ha hb,
    integral_sectorTwoCurvature ha hb]

#print axioms sectorTwoU_mul_sin_add_cos_mul_V
#print axioms hasDerivAt_sectorTwoPhaseRatio
#print axioms hasDerivAt_sectorTwoCurvaturePrimitive
#print axioms hasDerivAt_sectorTwoBoundary
#print axioms hasDerivAt_sectorTwoSupport
#print axioms sectorTwoSupport_sq_sub_derivative_sq
#print axioms sectorTwo_gramDet
#print axioms sectorTwoSq_pos
#print axioms sectorTwoDensity_eq_curvature_sub_boundaryDerivative
#print axioms sectorTwoU_pos_on_sector
#print axioms sectorTwoPhaseRatio_pi_div_two_add
#print axioms sectorTwoCurvaturePrimitive_endpoints
#print axioms integral_sectorTwoCurvature
#print axioms sectorTwoBoundary_change
#print axioms integral_sectorTwoDensity_eq_curvature_sub
#print axioms integral_sectorTwoDensity

end L2Hexagon
