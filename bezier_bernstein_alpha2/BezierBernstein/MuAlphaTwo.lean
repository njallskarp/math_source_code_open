import BezierBernstein.GaussianAbs
import Mathlib.Probability.CDF
import Mathlib.MeasureTheory.Integral.Layercake

/-!
# Identification of Kitamura's `muAlpha 2` with a Gaussian minimum

The definition `poweredGaussianMomentConstant` below is definitionally the
`muAlpha` definition at Kenta Kitamura's immutable source commit
`3f35c631d215b3841242275bf3ed2c59ea153a2d`.  We give it a local descriptive
name because that external single-file development is not a dependency of this
project.

The main result identifies its `alpha = 2` specialization with the expectation
of the minimum of two independent standard Gaussians.  The layer-cake step is
carried out explicitly, including integrability and both tail-event laws.
-/

open Filter MeasureTheory ProbabilityTheory Real Set

namespace BezierBernstein

/-- Kitamura's literal powered-Gaussian first-moment constant. -/
noncomputable def poweredGaussianMomentConstant (alpha : ℝ) : ℝ :=
  (∫ t in Ioi 0, (1 - cdf (gaussianReal 0 1) t) ^ alpha) -
    ∫ t in Ioi 0, 1 - cdf (gaussianReal 0 1) t ^ alpha

/-- The positive standard-Gaussian tail is one minus its cdf. -/
theorem standardGaussian_measureReal_Ioi (t : ℝ) :
    (gaussianReal 0 1).real (Ioi t) = 1 - cdf (gaussianReal 0 1) t := by
  rw [← compl_Iic, measureReal_compl measurableSet_Iic, probReal_univ,
    ProbabilityTheory.cdf_eq_real]

/-- Reflection symmetry identifies the closed negative tail with the positive cdf value. -/
theorem standardGaussian_measureReal_Ici_neg (t : ℝ) :
    (gaussianReal 0 1).real (Ici (-t)) = cdf (gaussianReal 0 1) t := by
  have hmap :
      (gaussianReal 0 1).map (fun x : ℝ => -x) = gaussianReal 0 1 := by
    simpa using (gaussianReal_map_neg (μ := (0 : ℝ)) (v := (1 : NNReal)))
  calc
    (gaussianReal 0 1).real (Ici (-t)) =
        ((gaussianReal 0 1).map (fun x : ℝ => -x)).real (Ici (-t)) := by
      rw [hmap]
    _ = (gaussianReal 0 1).real ((fun x : ℝ => -x) ⁻¹' Ici (-t)) := by
      rw [measureReal_def, Measure.map_apply (by fun_prop) measurableSet_Ici]
      rfl
    _ = (gaussianReal 0 1).real (Iic t) := by
      congr 2
      ext x
      simp
    _ = cdf (gaussianReal 0 1) t :=
      (ProbabilityTheory.cdf_eq_real _ _).symm

/-- Positive-tail law of the minimum of two independent standard Gaussians. -/
theorem standardGaussianProd_measureReal_min_gt (t : ℝ) :
    ((gaussianReal 0 1).prod (gaussianReal 0 1)).real
        {p : ℝ × ℝ | t < min p.1 p.2} =
      (1 - cdf (gaussianReal 0 1) t) ^ 2 := by
  have hset : {p : ℝ × ℝ | t < min p.1 p.2} = Ioi t ×ˢ Ioi t := by
    ext p
    simp
  rw [hset, measureReal_prod_prod, standardGaussian_measureReal_Ioi]
  ring

/-- Negative-tail law of the minimum of two independent standard Gaussians. -/
theorem standardGaussianProd_measureReal_min_lt_neg (t : ℝ) :
    ((gaussianReal 0 1).prod (gaussianReal 0 1)).real
        {p : ℝ × ℝ | min p.1 p.2 < -t} =
      1 - cdf (gaussianReal 0 1) t ^ 2 := by
  have hset :
      {p : ℝ × ℝ | min p.1 p.2 < -t} = (Ici (-t) ×ˢ Ici (-t))ᶜ := by
    ext p
    simp only [Set.mem_ofPred_eq, Set.mem_compl_iff, Set.mem_prod, Set.mem_Ici,
      min_lt_iff, not_and_or, not_le]
  rw [hset, measureReal_compl (measurableSet_Ici.prod measurableSet_Ici), probReal_univ,
    measureReal_prod_prod, standardGaussian_measureReal_Ici_neg]
  ring

/-- Integrability needed before applying layer cake to the Gaussian minimum. -/
theorem integrable_min_standardGaussian_prod :
    Integrable (fun p : ℝ × ℝ => min p.1 p.2)
      ((gaussianReal 0 1).prod (gaussianReal 0 1)) := by
  let mu : Measure ℝ := gaussianReal 0 1
  let P : Measure (ℝ × ℝ) := mu.prod mu
  have hid : Integrable (fun x : ℝ => x) mu := by
    exact (memLp_id_gaussianReal' (p := (1 : ENNReal)) (by simp)).integrable (by simp)
  have hfst : Integrable (fun p : ℝ × ℝ => p.1) P := hid.comp_fst mu
  have hsnd : Integrable (fun p : ℝ × ℝ => p.2) P := hid.comp_snd mu
  have habs : Integrable (fun p : ℝ × ℝ => |p.1 - p.2|) P := by
    have hdiff : Integrable (fun p : ℝ × ℝ => p.1 - p.2) P := by
      change Integrable ((fun p : ℝ × ℝ => p.1) - fun p : ℝ × ℝ => p.2) P
      exact hfst.sub hsnd
    exact hdiff.abs
  have hformula :
      Integrable (fun p : ℝ × ℝ => (p.1 + p.2 - |p.1 - p.2|) / 2) P := by
    have hadd : Integrable (fun p : ℝ × ℝ => p.1 + p.2) P := by
      change Integrable ((fun p : ℝ × ℝ => p.1) + fun p : ℝ × ℝ => p.2) P
      exact hfst.add hsnd
    exact (hadd.sub habs).div_const 2
  apply hformula.congr
  filter_upwards with p
  rcases le_total p.1 p.2 with h | h
  · rw [min_eq_left h, abs_of_nonpos (sub_nonpos.mpr h)]
    ring
  · rw [min_eq_right h, abs_of_nonneg (sub_nonneg.mpr h)]
    ring

/-- Layer cake identifies the expectation of the Gaussian minimum with the two cdf tails. -/
theorem integral_min_standardGaussian_prod_eq_cdf_tails :
    (∫ p : ℝ × ℝ, min p.1 p.2
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1))) =
      (∫ t in Ioi 0, (1 - cdf (gaussianReal 0 1) t) ^ 2) -
        ∫ t in Ioi 0, 1 - cdf (gaussianReal 0 1) t ^ 2 := by
  let P : Measure (ℝ × ℝ) := (gaussianReal 0 1).prod (gaussianReal 0 1)
  let M : ℝ × ℝ → ℝ := fun p => min p.1 p.2
  have hM : Integrable M P := by
    simpa [M, P] using integrable_min_standardGaussian_prod
  have hpos : Integrable (fun p => max (M p) 0) P := hM.pos_part
  have hneg : Integrable (fun p => max (-M p) 0) P := hM.neg_part
  have hpos_layer :=
    hpos.integral_eq_integral_meas_lt
      (Eventually.of_forall fun p => le_max_right (M p) 0)
  have hneg_layer :=
    hneg.integral_eq_integral_meas_lt
      (Eventually.of_forall fun p => le_max_right (-M p) 0)
  have hpos_tail :
      (∫ t in Ioi 0, P.real {p : ℝ × ℝ | t < max (M p) 0}) =
        ∫ t in Ioi 0, (1 - cdf (gaussianReal 0 1) t) ^ 2 := by
    apply integral_congr_ae
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
    have hset : {p : ℝ × ℝ | t < max (M p) 0} = {p | t < M p} := by
      ext p
      simp only [Set.mem_ofPred_eq]
      constructor
      · intro h
        rcases (lt_max_iff.mp h) with hM | h0
        · exact hM
        · exact False.elim ((not_lt_of_ge (le_of_lt ht)) h0)
      · intro h
        exact lt_of_lt_of_le h (le_max_left _ _)
    rw [hset]
    simpa [M, P] using standardGaussianProd_measureReal_min_gt t
  have hneg_tail :
      (∫ t in Ioi 0, P.real {p : ℝ × ℝ | t < max (-M p) 0}) =
        ∫ t in Ioi 0, 1 - cdf (gaussianReal 0 1) t ^ 2 := by
    apply integral_congr_ae
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
    have hset : {p : ℝ × ℝ | t < max (-M p) 0} = {p | M p < -t} := by
      ext p
      simp only [Set.mem_ofPred_eq]
      constructor
      · intro h
        rcases (lt_max_iff.mp h) with hM | h0
        · linarith
        · exact False.elim ((not_lt_of_ge (le_of_lt ht)) h0)
      · intro h
        have htM : t < -M p := by linarith
        exact lt_of_lt_of_le htM (le_max_left _ _)
    rw [hset]
    simpa [M, P] using standardGaussianProd_measureReal_min_lt_neg t
  calc
    (∫ p : ℝ × ℝ, M p ∂P) =
        ∫ p : ℝ × ℝ, (max (M p) 0 - max (-M p) 0) ∂P := by
      apply integral_congr_ae
      filter_upwards with p
      exact (max_zero_sub_max_neg_zero_eq_self (M p)).symm
    _ = (∫ p : ℝ × ℝ, max (M p) 0 ∂P) -
        ∫ p : ℝ × ℝ, max (-M p) 0 ∂P := integral_sub hpos hneg
    _ = _ := by rw [hpos_layer, hneg_layer, hpos_tail, hneg_tail]

/-- The literal upstream constant at `alpha = 2` is the Gaussian-minimum expectation. -/
theorem poweredGaussianMomentConstant_two_eq_integral_min :
    poweredGaussianMomentConstant 2 =
      ∫ p : ℝ × ℝ, min p.1 p.2
        ∂((gaussianReal 0 1).prod (gaussianReal 0 1)) := by
  rw [poweredGaussianMomentConstant]
  simp_rw [Real.rpow_two]
  exact integral_min_standardGaussian_prod_eq_cdf_tails.symm

/-- Explicit evaluation of Kitamura's powered-Gaussian constant at `alpha = 2`. -/
theorem poweredGaussianMomentConstant_two :
    poweredGaussianMomentConstant 2 = -1 / √π := by
  rw [poweredGaussianMomentConstant_two_eq_integral_min,
    integral_min_standardGaussian_prod]

#print axioms standardGaussian_measureReal_Ioi
#print axioms standardGaussian_measureReal_Ici_neg
#print axioms standardGaussianProd_measureReal_min_gt
#print axioms standardGaussianProd_measureReal_min_lt_neg
#print axioms integrable_min_standardGaussian_prod
#print axioms integral_min_standardGaussian_prod_eq_cdf_tails
#print axioms poweredGaussianMomentConstant_two_eq_integral_min
#print axioms poweredGaussianMomentConstant_two

end BezierBernstein
