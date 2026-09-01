import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Tactic

/-!
# The first absolute moment of the centered Gaussian of variance two

This file evaluates the one-dimensional Gaussian constant used by the
`alpha = 2` order-statistic reduction.  The proof is analytic: after passing
to the density, evenness reduces the integral to a half-line integral and
Mathlib's exact primitive for `x * exp (-b * x^2)` closes the calculation.
-/

open MeasureTheory ProbabilityTheory Real Set

namespace BezierBernstein

/-- The real half-line primitive underlying the first absolute Gaussian moment. -/
theorem integral_Ioi_mul_exp_neg_mul_sq {b : ℝ} (hb : 0 < b) :
    ∫ x : ℝ in Ioi 0, x * Real.exp (-b * x ^ 2) = (2 * b)⁻¹ := by
  rw [← RCLike.ofReal_inj (K := ℂ), ← integral_ofReal]
  convert integral_mul_cexp_neg_mul_sq (b := (b : ℂ)) (by simpa using hb) using 1
  · congr 1
    ext x
    simp
  · simp

/-- The positive-half-line first moment of the centered Gaussian of variance two. -/
theorem integral_Ioi_mul_gaussianPDFReal_zero_two :
    ∫ x : ℝ in Ioi 0, x * gaussianPDFReal 0 2 x = (√π)⁻¹ := by
  have hprimitive := integral_Ioi_mul_exp_neg_mul_sq (b := (1 / 4 : ℝ)) (by norm_num)
  have hexp :
      (∫ x : ℝ in Ioi 0, x * Real.exp (-(x ^ 2) / (2 * 2))) = 2 := by
    convert hprimitive using 1
    · apply setIntegral_congr_fun measurableSet_Ioi
      intro x hx
      ring_nf
    · norm_num
  have hsqrt : √(2 * π * (2 : ℝ)) = 2 * √π := by
    rw [show 2 * π * (2 : ℝ) = 4 * π by ring, Real.sqrt_mul (by positivity : 0 ≤ (4 : ℝ))]
    norm_num
  calc
    (∫ x : ℝ in Ioi 0, x * gaussianPDFReal 0 2 x) =
        (√(2 * π * (2 : ℝ)))⁻¹ *
          ∫ x : ℝ in Ioi 0, x * Real.exp (-(x ^ 2) / (2 * 2)) := by
      rw [← integral_const_mul]
      apply setIntegral_congr_fun measurableSet_Ioi
      intro x hx
      simp only [gaussianPDFReal, sub_zero, NNReal.coe_ofNat]
      ring
    _ = (√π)⁻¹ := by rw [hexp, hsqrt]; field_simp

/-- The exact first absolute moment of `N(0,2)`. -/
theorem integral_abs_gaussianReal_zero_two :
    ∫ x : ℝ, |x| ∂gaussianReal 0 2 = 2 / √π := by
  rw [integral_gaussianReal_eq_integral_smul (by norm_num : (2 : NNReal) ≠ 0)]
  simp only [smul_eq_mul]
  calc
    (∫ x : ℝ, gaussianPDFReal 0 2 x * |x|) =
        ∫ x : ℝ, |x| * gaussianPDFReal 0 2 (|x|) := by
      apply integral_congr_ae
      filter_upwards with x
      rw [mul_comm]
      congr 1
      simp [gaussianPDFReal, sq_abs]
    _ = 2 * ∫ x : ℝ in Ioi 0, x * gaussianPDFReal 0 2 x := by
      simpa only using
        (integral_comp_abs (f := fun x : ℝ => x * gaussianPDFReal 0 2 x))
    _ = 2 / √π := by rw [integral_Ioi_mul_gaussianPDFReal_zero_two]; ring

/-- The difference of two independent standard Gaussians, realized on their product space,
has the centered Gaussian law of variance two. -/
theorem map_sub_standardGaussian_prod :
    ((gaussianReal 0 1).prod (gaussianReal 0 1)).map
        (fun p : ℝ × ℝ => p.1 - p.2) =
      gaussianReal 0 2 := by
  let μ : Measure ℝ := gaussianReal 0 1
  let P : Measure (ℝ × ℝ) := μ.prod μ
  have hind0 :
      IndepFun (fun p : ℝ × ℝ => p.1) (fun p : ℝ × ℝ => p.2) P :=
    indepFun_prod (X := id) (Y := id) measurable_id measurable_id
  have hind :
      IndepFun (fun p : ℝ × ℝ => p.1) (fun p : ℝ × ℝ => -p.2) P :=
    hind0.comp measurable_id measurable_neg
  have hx : P.map (fun p : ℝ × ℝ => p.1) = gaussianReal 0 1 := by
    simp [P, μ]
  have hy : P.map (fun p : ℝ × ℝ => -p.2) = gaussianReal 0 1 := by
    change P.map ((fun y : ℝ => -y) ∘ fun p : ℝ × ℝ => p.2) = gaussianReal 0 1
    rw [← Measure.map_map (by fun_prop) (by fun_prop)]
    simp [P, μ, gaussianReal_map_neg]
  have hsum := gaussianReal_add_gaussianReal_of_indepFun hind hx hy
  have hfun :
      (fun p : ℝ × ℝ => p.1) + (fun p : ℝ × ℝ => -p.2) =
        fun p : ℝ × ℝ => p.1 - p.2 := by
    funext p
    simp [sub_eq_add_neg]
  rw [hfun] at hsum
  norm_num at hsum
  simpa [P, μ] using hsum

/-- Product-space form of the exact absolute-difference moment. -/
theorem integral_abs_sub_standardGaussian_prod :
    ∫ p : ℝ × ℝ, |p.1 - p.2|
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1)) = 2 / √π := by
  calc
    (∫ p : ℝ × ℝ, |p.1 - p.2|
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1))) =
        ∫ z : ℝ, |z| ∂(((gaussianReal 0 1).prod (gaussianReal 0 1)).map
          (fun p : ℝ × ℝ => p.1 - p.2)) := by
      rw [integral_map (by fun_prop) (by fun_prop)]
    _ = ∫ z : ℝ, |z| ∂gaussianReal 0 2 := by rw [map_sub_standardGaussian_prod]
    _ = 2 / √π := integral_abs_gaussianReal_zero_two

/-- The exact first moment of the minimum of two independent standard Gaussians. -/
theorem integral_min_standardGaussian_prod :
    ∫ p : ℝ × ℝ, min p.1 p.2
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1)) = -1 / √π := by
  let μ : Measure ℝ := gaussianReal 0 1
  let P : Measure (ℝ × ℝ) := μ.prod μ
  have hid : Integrable (fun x : ℝ => x) μ := by
    exact (memLp_id_gaussianReal' (p := (1 : ENNReal)) (by simp)).integrable (by simp)
  have hfst : Integrable (fun p : ℝ × ℝ => p.1) P := hid.comp_fst μ
  have hsnd : Integrable (fun p : ℝ × ℝ => p.2) P := hid.comp_snd μ
  have hadd : Integrable (fun p : ℝ × ℝ => p.1 + p.2) P := by
    change Integrable ((fun p : ℝ × ℝ => p.1) + fun p : ℝ × ℝ => p.2) P
    exact hfst.add hsnd
  have habs : Integrable (fun p : ℝ × ℝ => |p.1 - p.2|) P := by
    have hdiff : Integrable (fun p : ℝ × ℝ => p.1 - p.2) P := by
      change Integrable ((fun p : ℝ × ℝ => p.1) - fun p : ℝ × ℝ => p.2) P
      exact hfst.sub hsnd
    exact hdiff.abs
  have hfst_int : ∫ p : ℝ × ℝ, p.1 ∂P = 0 := by
    change (∫ p : ℝ × ℝ, p.1 ∂μ.prod μ) = 0
    calc
      (∫ p : ℝ × ℝ, p.1 ∂μ.prod μ) =
          μ.real univ • ∫ x : ℝ, x ∂μ := by
        simpa using (integral_fun_fst (μ := μ) (ν := μ) (fun x : ℝ => x))
      _ = 0 := by simp [μ]
  have hsnd_int : ∫ p : ℝ × ℝ, p.2 ∂P = 0 := by
    change (∫ p : ℝ × ℝ, p.2 ∂μ.prod μ) = 0
    calc
      (∫ p : ℝ × ℝ, p.2 ∂μ.prod μ) =
          μ.real univ • ∫ x : ℝ, x ∂μ := by
        simpa using (integral_fun_snd (μ := μ) (ν := μ) (fun x : ℝ => x))
      _ = 0 := by simp [μ]
  calc
    (∫ p : ℝ × ℝ, min p.1 p.2 ∂P) =
        ∫ p : ℝ × ℝ, (p.1 + p.2 - |p.1 - p.2|) / 2 ∂P := by
      apply integral_congr_ae
      filter_upwards with p
      rcases le_total p.1 p.2 with h | h
      · rw [min_eq_left h, abs_of_nonpos (sub_nonpos.mpr h)]
        ring
      · rw [min_eq_right h, abs_of_nonneg (sub_nonneg.mpr h)]
        ring
    _ = ((∫ p : ℝ × ℝ, p.1 + p.2 ∂P) -
          ∫ p : ℝ × ℝ, |p.1 - p.2| ∂P) / 2 := by
      rw [integral_div, integral_sub hadd habs]
    _ = ((∫ p : ℝ × ℝ, p.1 ∂P) + (∫ p : ℝ × ℝ, p.2 ∂P) -
          ∫ p : ℝ × ℝ, |p.1 - p.2| ∂P) / 2 := by
      rw [integral_add hfst hsnd]
    _ = -1 / √π := by
      rw [hfst_int, hsnd_int]
      simp only [zero_add, zero_sub]
      dsimp only [P, μ]
      change -(∫ p : ℝ × ℝ, |p.1 - p.2|
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1))) / 2 = -1 / √π
      rw [integral_abs_sub_standardGaussian_prod]
      ring

/-- The minimum constant obtained from a centered `N(0,2)` difference. -/
theorem neg_half_integral_abs_gaussianReal_zero_two :
    -(∫ x : ℝ, |x| ∂gaussianReal 0 2) / 2 = -1 / √π := by
  rw [integral_abs_gaussianReal_zero_two]
  ring

#print axioms integral_Ioi_mul_exp_neg_mul_sq
#print axioms integral_Ioi_mul_gaussianPDFReal_zero_two
#print axioms integral_abs_gaussianReal_zero_two
#print axioms map_sub_standardGaussian_prod
#print axioms integral_abs_sub_standardGaussian_prod
#print axioms integral_min_standardGaussian_prod
#print axioms neg_half_integral_abs_gaussianReal_zero_two

end BezierBernstein
