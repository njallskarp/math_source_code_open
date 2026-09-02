import L2Hexagon.SectorThreeIntegral
import L2Hexagon.SetLevelSupport
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# Set-level support formulas for the normalized sectors

This file connects the actual normalized three-segment zonotope in the
Euclidean plane to the scalar Sector I, II, and III support squares.  The support
is the literal subtype-indexed supremum from `SetLevelSupport.lean`; no desired
sector formula is built into its definition.

The main results state the exact squared Firey-support formulas under the
corresponding generator-sign hypotheses and on the actual closed angular
sectors.  The planar support-area theorem remains outside this module.
-/

open Real Set

namespace L2Hexagon

/-- The Euclidean plane used for the normalized zonotope. -/
abbrev Plane := EuclideanSpace ℝ (Fin 2)

/-- A two-coordinate vector in the Euclidean plane. -/
noncomputable def planeVector (x y : ℝ) : Plane := !₂[x, y]

/-- The standard unit direction at angle `θ`. -/
noncomputable def planeDirection (θ : ℝ) : Plane := planeVector (cos θ) (sin θ)

/-- The actual normalized zonotope `[0,e₁]+[0,(a,b)]+[0,e₂]`. -/
noncomputable def normalizedZonotope (a b : ℝ) : Set Plane :=
  threeSegmentZonotope (planeVector 1 0) (planeVector a b) (planeVector 0 1)

/-- The literal `p=2` support square of the zonotope and its reflection. -/
noncomputable def normalizedFireySupportSq (a b θ : ℝ) : ℝ :=
  setSupportFunction (normalizedZonotope a b) (planeDirection θ) ^ 2 +
    setSupportFunction (normalizedZonotope a b) (-planeDirection θ) ^ 2

/-- The positive linear support expression on Sector I. -/
noncomputable def sectorOneSupport (a b θ : ℝ) : ℝ :=
  (1 + a) * cos θ + (1 + b) * sin θ

/-- The derivative of the Sector I support expression. -/
noncomputable def sectorOneDerivative (a b θ : ℝ) : ℝ :=
  -(1 + a) * sin θ + (1 + b) * cos θ

/-- The literal squared support expression on Sector I. -/
noncomputable def sectorOneSq (a b θ : ℝ) : ℝ :=
  sectorOneSupport a b θ ^ 2

/-- Coordinate inner products in the chosen Euclidean-plane model. -/
theorem inner_planeVector (x y r s : ℝ) :
    inner ℝ (planeVector x y) (planeVector r s) = x * r + y * s := by
  rw [PiLp.inner_apply, Fin.sum_univ_two]
  simp [planeVector, mul_comm]

/-- Unit directions separated by `π` are negatives in the Euclidean-plane model. -/
theorem planeDirection_add_pi (θ : ℝ) :
    planeDirection (θ + π) = -planeDirection θ := by
  unfold planeDirection planeVector
  ext i
  fin_cases i <;> simp [Real.cos_add_pi, Real.sin_add_pi]

/-- The reflected squared Firey support is `π`-periodic at the set level. -/
theorem normalizedFireySupportSq_add_pi (a b θ : ℝ) :
    normalizedFireySupportSq a b (θ + π) = normalizedFireySupportSq a b θ := by
  rw [normalizedFireySupportSq, normalizedFireySupportSq, planeDirection_add_pi, neg_neg]
  ring

/-- Periodicity of the actual set-level reflected squared Firey support. -/
theorem normalizedFireySupportSq_periodic (a b : ℝ) :
    Function.Periodic (normalizedFireySupportSq a b) π :=
  normalizedFireySupportSq_add_pi a b

/-- The set-level support square reduces to the three signed generator pairings. -/
theorem normalizedFireySupportSq_eq_positiveParts (a b θ : ℝ) :
    normalizedFireySupportSq a b θ =
      (positivePart (cos θ) + positivePart (a * cos θ + b * sin θ) +
          positivePart (sin θ)) ^ 2 +
        (positivePart (-cos θ) + positivePart (-(a * cos θ + b * sin θ)) +
          positivePart (-sin θ)) ^ 2 := by
  rw [normalizedFireySupportSq, normalizedZonotope,
    setSupportFunction_threeSegmentZonotope,
    setSupportFunction_threeSegmentZonotope]
  simp only [threeSegmentSupport, planeDirection, inner_planeVector, inner_neg_right]
  congr 1 <;> ring_nf

/-- Under the Sector I signs, the actual set-level Firey support square is `sectorOneSq`. -/
theorem normalizedFireySupportSq_eq_sectorOneSq_of_signs {a b θ : ℝ}
    (hcos : 0 ≤ cos θ) (hmiddle : 0 ≤ a * cos θ + b * sin θ)
    (hsin : 0 ≤ sin θ) :
    normalizedFireySupportSq a b θ = sectorOneSq a b θ := by
  rw [normalizedFireySupportSq_eq_positiveParts]
  unfold positivePart sectorOneSq sectorOneSupport
  rw [max_eq_left hcos, max_eq_left hmiddle, max_eq_left hsin,
    max_eq_right (neg_nonpos.mpr hcos), max_eq_right (neg_nonpos.mpr hmiddle),
    max_eq_right (neg_nonpos.mpr hsin)]
  ring

/-- Under the Sector II signs, the actual set-level Firey support square is `sectorTwoSq`. -/
theorem normalizedFireySupportSq_eq_sectorTwoSq_of_signs {a b θ : ℝ}
    (hcos : cos θ ≤ 0) (hmiddle : 0 ≤ a * cos θ + b * sin θ)
    (hsin : 0 ≤ sin θ) :
    normalizedFireySupportSq a b θ = sectorTwoSq a b θ := by
  rw [normalizedFireySupportSq_eq_positiveParts]
  unfold positivePart sectorTwoSq sectorTwoU
  rw [max_eq_right hcos, max_eq_left hmiddle, max_eq_left hsin,
    max_eq_left (neg_nonneg.mpr hcos),
    max_eq_right (neg_nonpos.mpr hmiddle), max_eq_right (neg_nonpos.mpr hsin)]
  ring

/-- Under the Sector III signs, the actual set-level Firey support square is `sectorThreeSq`. -/
theorem normalizedFireySupportSq_eq_sectorThreeSq_of_signs {a b θ : ℝ}
    (hcos : cos θ ≤ 0) (hmiddle : a * cos θ + b * sin θ ≤ 0)
    (hsin : 0 ≤ sin θ) :
    normalizedFireySupportSq a b θ = sectorThreeSq a b θ := by
  rw [normalizedFireySupportSq_eq_positiveParts]
  unfold positivePart sectorThreeSq sectorThreeW
  rw [max_eq_right hcos, max_eq_right hmiddle, max_eq_left hsin,
    max_eq_left (neg_nonneg.mpr hcos),
    max_eq_left (neg_nonneg.mpr hmiddle), max_eq_right (neg_nonpos.mpr hsin)]
  ring

/-- The three generator pairings are nonnegative on the closed first sector. -/
theorem sectorOne_generator_signs {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc 0 (π / 2)) :
    0 ≤ cos θ ∧ 0 ≤ a * cos θ + b * sin θ ∧ 0 ≤ sin θ := by
  have hcos : 0 ≤ cos θ :=
    Real.cos_nonneg_of_mem_Icc ⟨by linarith [hθ.1, Real.pi_div_two_pos], hθ.2⟩
  have hsin : 0 ≤ sin θ :=
    Real.sin_nonneg_of_mem_Icc ⟨hθ.1, by linarith [hθ.2, Real.pi_pos]⟩
  have hmiddle : 0 ≤ a * cos θ + b * sin θ :=
    add_nonneg (mul_nonneg ha.le hcos) (mul_nonneg hb.le hsin)
  exact ⟨hcos, hmiddle, hsin⟩

/-- The literal set-level support square restricts to the Sector I formula. -/
theorem normalizedFireySupportSq_eq_sectorOneSq_on_sector {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hθ : θ ∈ Icc 0 (π / 2)) :
    normalizedFireySupportSq a b θ = sectorOneSq a b θ := by
  obtain ⟨hcos, hmiddle, hsin⟩ := sectorOne_generator_signs ha hb hθ
  exact normalizedFireySupportSq_eq_sectorOneSq_of_signs hcos hmiddle hsin

/-- The three generator pairings have the Sector II signs on its closed angle interval. -/
theorem sectorTwo_generator_signs {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    cos θ ≤ 0 ∧ 0 ≤ a * cos θ + b * sin θ ∧ 0 ≤ sin θ := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφlt : arctan (b / a) < π / 2 := by simpa [generatorAngle] using hφ.2
  have hθpi : θ ≤ π := by linarith [hθ.2]
  have hcos : cos θ ≤ 0 :=
    Real.cos_nonpos_of_pi_div_two_le_of_le hθ.1 (by linarith [hθpi, Real.pi_pos])
  have hsin : 0 ≤ sin θ :=
    Real.sin_nonneg_of_mem_Icc ⟨by linarith [hθ.1, Real.pi_pos], hθpi⟩
  let t := θ - π / 2
  have ht0 : 0 ≤ t := by
    dsimp [t]
    linarith [hθ.1]
  have htφ : t ≤ arctan (b / a) := by
    dsimp [t]
    linarith [hθ.2]
  have htmem : t ∈ Ioo (-(π / 2)) (π / 2) := by
    constructor
    · linarith [Real.pi_div_two_pos]
    · exact lt_of_le_of_lt htφ hφlt
  have hφmem : arctan (b / a) ∈ Ioo (-(π / 2)) (π / 2) :=
    ⟨by linarith [hφ.1, Real.pi_div_two_pos], hφlt⟩
  have htan : tan t ≤ b / a := by
    have hmono := Real.strictMonoOn_tan.monotoneOn htmem hφmem htφ
    simpa using hmono
  have hcost : 0 < cos t := Real.cos_pos_of_mem_Ioo htmem
  have hsinle : a * sin t ≤ b * cos t := by
    rw [← Real.tan_mul_cos hcost.ne']
    calc
      a * (tan t * cos t) ≤ a * ((b / a) * cos t) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right htan hcost.le) ha.le
      _ = b * cos t := by field_simp [ha.ne']
  have hθform : θ = π / 2 + t := by
    dsimp [t]
    ring
  have hmiddle : 0 ≤ a * cos θ + b * sin θ := by
    rw [hθform]
    simp only [Real.cos_add, Real.sin_add, Real.cos_pi_div_two,
      Real.sin_pi_div_two, zero_mul, one_mul, zero_sub, add_zero]
    linarith
  exact ⟨hcos, hmiddle, hsin⟩

/-- The literal set-level support square restricts to the Sector II formula. -/
theorem normalizedFireySupportSq_eq_sectorTwoSq_on_sector {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    normalizedFireySupportSq a b θ = sectorTwoSq a b θ := by
  obtain ⟨hcos, hmiddle, hsin⟩ := sectorTwo_generator_signs ha hb hθ
  exact normalizedFireySupportSq_eq_sectorTwoSq_of_signs hcos hmiddle hsin

/-- The three generator pairings have the Sector III signs on its closed angle interval. -/
theorem sectorThree_generator_signs {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    cos θ ≤ 0 ∧ a * cos θ + b * sin θ ≤ 0 ∧ 0 ≤ sin θ := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by simpa [generatorAngle] using hφ.1
  have hcos : cos θ ≤ 0 :=
    Real.cos_nonpos_of_pi_div_two_le_of_le (by linarith [hθ.1])
      (by linarith [hθ.2, Real.pi_pos])
  have hsin : 0 ≤ sin θ :=
    Real.sin_nonneg_of_mem_Icc ⟨by linarith [hθ.1, Real.pi_pos], hθ.2⟩
  let t := π - θ
  have ht0 : 0 ≤ t := by
    dsimp [t]
    linarith [hθ.2]
  have hangle := arctan_div_swap ha hb
  have htangle : t ≤ arctan (a / b) := by
    dsimp [t]
    rw [hangle]
    linarith [hθ.1]
  have hanglemem := generatorAngle_mem_Ioo hb ha
  have hanglepos : 0 < arctan (a / b) := by
    simpa [generatorAngle] using hanglemem.1
  have hanglelt : arctan (a / b) < π / 2 := by
    simpa [generatorAngle] using hanglemem.2
  have htmem : t ∈ Ioo (-(π / 2)) (π / 2) :=
    ⟨by linarith [ht0, Real.pi_div_two_pos], lt_of_le_of_lt htangle hanglelt⟩
  have hanglemem' : arctan (a / b) ∈ Ioo (-(π / 2)) (π / 2) :=
    ⟨by linarith [hanglepos, Real.pi_div_two_pos], hanglelt⟩
  have htan : tan t ≤ a / b := by
    have hmono := Real.strictMonoOn_tan.monotoneOn htmem hanglemem' htangle
    simpa using hmono
  have hcost : 0 < cos t := Real.cos_pos_of_mem_Ioo htmem
  have hsinle : b * sin t ≤ a * cos t := by
    rw [← Real.tan_mul_cos hcost.ne']
    calc
      b * (tan t * cos t) ≤ b * ((a / b) * cos t) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right htan hcost.le) hb.le
      _ = a * cos t := by field_simp [hb.ne']
  have hθform : θ = π - t := by
    dsimp [t]
    ring
  have hmiddle : a * cos θ + b * sin θ ≤ 0 := by
    rw [hθform, Real.cos_pi_sub, Real.sin_pi_sub]
    linarith
  exact ⟨hcos, hmiddle, hsin⟩

/-- The literal set-level support square restricts to the Sector III formula. -/
theorem normalizedFireySupportSq_eq_sectorThreeSq_on_sector {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    normalizedFireySupportSq a b θ = sectorThreeSq a b θ := by
  obtain ⟨hcos, hmiddle, hsin⟩ := sectorThree_generator_signs ha hb hθ
  exact normalizedFireySupportSq_eq_sectorThreeSq_of_signs hcos hmiddle hsin

/-- Sector I and II squared-support expressions agree at their shared endpoint. -/
theorem sectorOneSq_eq_sectorTwoSq_pi_div_two (a b : ℝ) :
    sectorOneSq a b (π / 2) = sectorTwoSq a b (π / 2) := by
  simp [sectorOneSq, sectorOneSupport, sectorTwoSq, sectorTwoU]

/-- Sector II and III squared-support expressions agree at their sign-change endpoint. -/
theorem sectorTwoSq_eq_sectorThreeSq_boundary {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    sectorTwoSq a b (π / 2 + arctan (b / a)) =
      sectorThreeSq a b (π / 2 + arctan (b / a)) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  have hφlt : arctan (b / a) < π / 2 := by
    simpa [generatorAngle] using hφ.2
  calc
    sectorTwoSq a b (π / 2 + arctan (b / a)) =
        normalizedFireySupportSq a b (π / 2 + arctan (b / a)) :=
      (normalizedFireySupportSq_eq_sectorTwoSq_on_sector ha hb
        ⟨by linarith [hφpos], le_rfl⟩).symm
    _ = sectorThreeSq a b (π / 2 + arctan (b / a)) :=
      normalizedFireySupportSq_eq_sectorThreeSq_on_sector ha hb
        ⟨le_rfl, by linarith [hφlt]⟩

#print axioms inner_planeVector
#print axioms planeDirection_add_pi
#print axioms normalizedFireySupportSq_periodic
#print axioms normalizedFireySupportSq_eq_positiveParts
#print axioms normalizedFireySupportSq_eq_sectorOneSq_of_signs
#print axioms sectorOne_generator_signs
#print axioms normalizedFireySupportSq_eq_sectorOneSq_on_sector
#print axioms normalizedFireySupportSq_eq_sectorTwoSq_of_signs
#print axioms normalizedFireySupportSq_eq_sectorThreeSq_of_signs
#print axioms sectorTwo_generator_signs
#print axioms normalizedFireySupportSq_eq_sectorTwoSq_on_sector
#print axioms sectorThree_generator_signs
#print axioms normalizedFireySupportSq_eq_sectorThreeSq_on_sector
#print axioms sectorOneSq_eq_sectorTwoSq_pi_div_two
#print axioms sectorTwoSq_eq_sectorThreeSq_boundary

end L2Hexagon
