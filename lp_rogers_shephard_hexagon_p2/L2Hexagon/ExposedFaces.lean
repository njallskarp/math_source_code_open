import L2Hexagon.HalfspaceBody

/-!
# Exposed transition faces of the exact halfspace body

The first transition normal is the vertical vector `e₂`.  Informally, for
`a,b > 0`, the exact exposed face is

`{x ∈ normalizedLpSumTwo a b | ⟪x,e₂⟫ = 1+b}
  = [(1+a,1+b),(a,1+b)]`.

The nontrivial inclusion is proved directly from the defining halfspaces.
The `e₁` halfspace gives the upper first-coordinate bound.  For the lower
bound, if `x₀<a`, test the halfspace in a small direction `(-t,1)`.  In that
sign chamber the squared Firey support is exactly

`t² + (1+b-a*t)²`.

Choosing `0<t≤a-x₀` and `a*t≤b/2` makes the defining inequality contradict
its own square.  This avoids an appeal to support derivatives or a limiting
argument and records the equality case in an algebraic form suitable for the
other two transition faces.
-/

open Real Set

namespace L2Hexagon

/-- The first coordinate direction. -/
noncomputable def planeE1 : Plane := planeVector 1 0

/-- The second coordinate direction. -/
noncomputable def planeE2 : Plane := planeVector 0 1

/-- The exact normalized support at the first coordinate direction. -/
theorem normalizedFireySupportVec_planeE1 {a b : ℝ} (ha : 0 < a) :
    normalizedFireySupportVec a b planeE1 = 1 + a := by
  have hsq : normalizedFireySupportVecSq a b planeE1 = (1 + a) ^ 2 := by
    rw [normalizedFireySupportVecSq_eq_positiveParts]
    simp only [planeE1, inner_planeVector]
    unfold positivePart
    norm_num
    rw [max_eq_left ha.le, max_eq_right (neg_nonpos.mpr ha.le)]
    ring
  rw [normalizedFireySupportVec, hsq, Real.sqrt_sq_eq_abs,
    abs_of_pos (by linarith)]

/-- The exact normalized support at the vertical transition direction. -/
theorem normalizedFireySupportVec_planeE2 {a b : ℝ} (hb : 0 < b) :
    normalizedFireySupportVec a b planeE2 = 1 + b := by
  have hsq : normalizedFireySupportVecSq a b planeE2 = (1 + b) ^ 2 := by
    rw [normalizedFireySupportVecSq_eq_positiveParts]
    simp only [planeE2, inner_planeVector]
    unfold positivePart
    norm_num
    rw [max_eq_left hb.le, max_eq_right (neg_nonpos.mpr hb.le)]
    ring
  rw [normalizedFireySupportVec, hsq, Real.sqrt_sq_eq_abs,
    abs_of_pos (by linarith)]

/-- On Sector I, the fixed vertex attains the exact halfspace support. -/
theorem sectorOneVertex_supporting {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hθ : θ ∈ Icc 0 (π / 2)) :
    inner ℝ (sectorOneVertex a b) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  obtain ⟨hcos, _, hsin⟩ := sectorOne_generator_signs ha hb hθ
  have hsupport : 0 ≤ sectorOneSupport a b θ := by
    unfold sectorOneSupport
    exact add_nonneg (mul_nonneg (by linarith) hcos)
      (mul_nonneg (by linarith) hsin)
  have hsq := normalizedFireySupportSq_eq_sectorOneSq_on_sector ha hb hθ
  rw [normalizedFireySupportVec, normalizedFireySupportVecSq_planeDirection, hsq,
    sectorOneSq, Real.sqrt_sq_eq_abs, abs_of_nonneg hsupport]
  simp [sectorOneVertex, planeDirection, inner_planeVector, sectorOneSupport]

/-- The literal support function of the exact halfspace body equals the
prescribed Firey support throughout the closed first sector. -/
theorem setSupportFunction_normalizedLpSumTwo_sectorOne {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hθ : θ ∈ Icc 0 (π / 2)) :
    setSupportFunction (normalizedLpSumTwo a b) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  let x := sectorOneVertex a b
  have hx : x ∈ normalizedLpSumTwo a b := sectorOneVertex_mem_normalizedLpSumTwo a b
  have hattain : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) :=
    sectorOneVertex_supporting ha hb hθ
  have hgreatest : IsGreatest
      ((fun y : Plane ↦ inner ℝ y (planeDirection θ)) '' normalizedLpSumTwo a b)
      (normalizedFireySupportVec a b (planeDirection θ)) := by
    constructor
    · exact ⟨x, hx, hattain⟩
    · rintro _ ⟨y, hy, rfl⟩
      exact hy (planeDirection θ)
  exact hgreatest.isLUB.ciSup_set_eq ⟨x, hx⟩

/-- The exact halfspace body has the prescribed support on the complete
closed upper half-circle, obtained by assembling the three checked sectors. -/
theorem setSupportFunction_normalizedLpSumTwo_upperHalf {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b) (hθ : θ ∈ Icc 0 π) :
    setSupportFunction (normalizedLpSumTwo a b) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  by_cases hfirst : θ ≤ π / 2
  · exact setSupportFunction_normalizedLpSumTwo_sectorOne ha hb ⟨hθ.1, hfirst⟩
  · by_cases hsecond : θ ≤ π / 2 + arctan (b / a)
    · exact setSupportFunction_normalizedLpSumTwo_sectorTwo ha hb
        ⟨le_of_not_ge hfirst, hsecond⟩
    · exact setSupportFunction_normalizedLpSumTwo_sectorThree ha hb
        ⟨le_of_not_ge hsecond, hθ.2⟩

/-- The defining support is even, as expected for the reflected Firey body. -/
theorem normalizedFireySupportVec_neg (a b : ℝ) (ξ : Plane) :
    normalizedFireySupportVec a b (-ξ) = normalizedFireySupportVec a b ξ := by
  unfold normalizedFireySupportVec normalizedFireySupportVecSq
  rw [neg_neg]
  congr 1
  ring

/-- The exact halfspace body is centrally symmetric. -/
theorem neg_mem_normalizedLpSumTwo {a b : ℝ} {x : Plane}
    (hx : x ∈ normalizedLpSumTwo a b) :
    -x ∈ normalizedLpSumTwo a b := by
  intro ξ
  calc
    inner ℝ (-x) ξ = inner ℝ x (-ξ) := by
      rw [inner_neg_left, inner_neg_right]
    _ ≤ normalizedFireySupportVec a b (-ξ) := hx (-ξ)
    _ = normalizedFireySupportVec a b ξ := normalizedFireySupportVec_neg a b ξ

/-- In the small negative-horizontal sign chamber the Firey support has the
Sector II quadratic form, stated for arbitrary vector directions rather than
angles. -/
theorem normalizedFireySupportVecSq_neg_small {a b t : ℝ}
    (ht : 0 ≤ t) (hat : a * t ≤ b) :
    normalizedFireySupportVecSq a b (planeVector (-t) 1) =
      t ^ 2 + (1 + b - a * t) ^ 2 := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  have hgen : 0 ≤ -(a * t) + b := by linarith
  simp only [inner_planeVector]
  unfold positivePart
  norm_num
  rw [max_eq_right (by linarith : -t ≤ 0), max_eq_left hgen,
    max_eq_left ht, max_eq_right (by linarith : -b + a * t ≤ 0)]
  ring

/-- The Sector II endpoint at the vertical transition has the expected
Cartesian coordinates. -/
theorem sectorTwoBoundaryPoint_pi_div_two {a b : ℝ} (hb : 0 < b) :
    planeVector (sectorTwoBoundaryX a b (π / 2))
        (sectorTwoBoundaryY a b (π / 2)) =
      planeVector a (1 + b) := by
  ext i
  fin_cases i
  · rw [sectorTwoBoundaryX_eq_ellipsoid hb,
      sectorTwoSupport_pi_div_two hb]
    simp [sectorTwoU, planeVector]
    field_simp [ne_of_gt (by linarith : 0 < 1 + b)]
  · rw [sectorTwoBoundaryY_eq_ellipsoid hb,
      sectorTwoSupport_pi_div_two hb]
    simp [sectorTwoU, planeVector]

/-- Membership in the exact body bounds the first coordinate above by the
Sector I vertex coordinate. -/
theorem firstCoord_le_of_mem_normalizedLpSumTwo {a b : ℝ} (ha : 0 < a)
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b) :
    x 0 ≤ 1 + a := by
  have h := hx planeE1
  rw [normalizedFireySupportVec_planeE1 ha] at h
  simpa [planeE1, PiLp.inner_apply, Fin.sum_univ_two, planeVector] using h

/-- A point on the vertical supporting line cannot lie to the left of the
Sector II endpoint.  This is the equality-case estimate which avoids taking
a directional limit. -/
theorem le_firstCoord_of_mem_of_vertical_support {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {x : Plane}
    (hx : x ∈ normalizedLpSumTwo a b)
    (hvertical : inner ℝ x planeE2 = 1 + b) :
    a ≤ x 0 := by
  have hx1 : x 1 = 1 + b := by
    simpa [planeE2, PiLp.inner_apply, Fin.sum_univ_two, planeVector] using hvertical
  by_contra hnot
  have hdelta : 0 < a - x 0 := sub_pos.2 (lt_of_not_ge hnot)
  let t : ℝ := min (b / (2 * a)) (a - x 0)
  have hquot : 0 < b / (2 * a) := div_pos hb (by positivity)
  have ht : 0 < t := lt_min hquot hdelta
  have ht_delta : t ≤ a - x 0 := min_le_right _ _
  have ht_quot : t ≤ b / (2 * a) := min_le_left _ _
  have hat_half : a * t ≤ b / 2 := by
    have hmul := mul_le_mul_of_nonneg_left ht_quot ha.le
    field_simp [ha.ne'] at hmul ⊢
    nlinarith
  have hat : a * t ≤ b := by linarith
  have hP : 0 < 1 + b - a * t := by linarith
  have hP_one : 1 < 1 + b - a * t := by linarith
  have hhalf := hx (planeVector (-t) 1)
  rw [normalizedFireySupportVec, normalizedFireySupportVecSq_neg_small ht.le hat] at hhalf
  have hleft : inner ℝ x (planeVector (-t) 1) =
      (1 + b - a * t) + t * (a - x 0) := by
    rw [PiLp.inner_apply, Fin.sum_univ_two, hx1]
    simp [planeVector]
    ring
  rw [hleft] at hhalf
  have hleft_pos : 0 < (1 + b - a * t) + t * (a - x 0) := by
    positivity
  have hrad : 0 ≤ t ^ 2 + (1 + b - a * t) ^ 2 := by positivity
  have hsquare := (sq_le_sq₀ hleft_pos.le (Real.sqrt_nonneg _)).2 hhalf
  rw [Real.sq_sqrt hrad] at hsquare
  have hstrict : t ^ 2 + (1 + b - a * t) ^ 2 <
      ((1 + b - a * t) + t * (a - x 0)) ^ 2 := by
    have hPdelta : a - x 0 < (1 + b - a * t) * (a - x 0) := by
      nlinarith [mul_pos (by linarith : 0 < (1 + b - a * t) - 1) hdelta]
    have ht_lt : t < 2 * (1 + b - a * t) * (a - x 0) := by linarith
    have hfactor : 0 < 2 * (1 + b - a * t) * (a - x 0) +
        t * (a - x 0) ^ 2 - t := by
      nlinarith [sq_nonneg (a - x 0)]
    have hmul := mul_pos ht hfactor
    nlinarith
  linarith

/-- The first upper-half transition segment is exactly the exposed face of
the exact halfspace body at the vertical normal. -/
theorem exposedFace_planeE2_eq_sectorOneTwoJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    {x | x ∈ normalizedLpSumTwo a b ∧
        inner ℝ x planeE2 = normalizedFireySupportVec a b planeE2} =
      sectorOneTwoJump a b := by
  ext x
  constructor
  · rintro ⟨hx, hsupp⟩
    rw [normalizedFireySupportVec_planeE2 hb] at hsupp
    have hx1 : x 1 = 1 + b := by
      simpa [planeE2, PiLp.inner_apply, Fin.sum_univ_two, planeVector] using hsupp
    have hlo : a ≤ x 0 := le_firstCoord_of_mem_of_vertical_support ha hb hx hsupp
    have hhi : x 0 ≤ 1 + a := firstCoord_le_of_mem_normalizedLpSumTwo ha hx
    unfold sectorOneTwoJump
    rw [sectorTwoBoundaryPoint_pi_div_two hb]
    refine ⟨x 0 - a, 1 + a - x 0, sub_nonneg.2 hlo, sub_nonneg.2 hhi, ?_, ?_⟩
    · ring
    · ext i
      fin_cases i
      · simp [sectorOneVertex, planeVector]
        ring
      · simp [sectorOneVertex, planeVector, hx1]
        ring
  · intro hxjump
    have hxbody := sectorOneTwoJump_subset_normalizedLpSumTwo hb hxjump
    refine ⟨hxbody, ?_⟩
    rw [normalizedFireySupportVec_planeE2 hb]
    unfold sectorOneTwoJump at hxjump
    rw [sectorTwoBoundaryPoint_pi_div_two hb] at hxjump
    rcases hxjump with ⟨r, s, hr, hs, hrs, rfl⟩
    calc
      inner ℝ (r • sectorOneVertex a b + s • planeVector a (1 + b)) planeE2 =
          r * (1 + b) + s * (1 + b) := by
            rw [inner_add_left, real_inner_smul_left, real_inner_smul_left]
            simp [planeE2, sectorOneVertex, inner_planeVector]
      _ = 1 + b := by nlinarith

#print axioms normalizedFireySupportVecSq_neg_small
#print axioms setSupportFunction_normalizedLpSumTwo_sectorOne
#print axioms setSupportFunction_normalizedLpSumTwo_upperHalf
#print axioms neg_mem_normalizedLpSumTwo
#print axioms le_firstCoord_of_mem_of_vertical_support
#print axioms exposedFace_planeE2_eq_sectorOneTwoJump

end L2Hexagon
