import L2Hexagon.FrontierSupport
import Mathlib.Analysis.SpecialFunctions.Complex.Arg

/-!
# First pieces of the complete exposed-face atlas

This file closes three structural gaps in the boundary classification.

* A vector in the open first sign chamber has the fixed Sector I vertex as
  its unique exposed point.  The proof uses only the two checked coordinate
  bounds and strict positivity of the normal coordinates.
* Central symmetry transports the two checked upper curved singleton faces
  to exact lower-half singleton faces.
* Every exposed face with a nonzero normal lies in the topological frontier.
  Together with the supporting-normal theorem, this gives an exact exhaustion
  of the frontier by all nonzero exposed faces.  The remaining finite-atlas
  step is to classify an arbitrary nonzero normal into the six transition rays
  and the open sign chambers.
-/

open Real Set Filter

namespace L2Hexagon

/-! ## The open first sign chamber -/

/-- In the open first sign chamber the fixed Sector I vertex attains the
prescribed vector support. -/
theorem sectorOneVertex_supporting_vector {a b : ℝ} {u : Plane}
    (ha : 0 < a) (hb : 0 < b) (hu0 : 0 < u 0) (hu1 : 0 < u 1) :
    inner ℝ (sectorOneVertex a b) u = normalizedFireySupportVec a b u := by
  have hpair : 0 ≤ inner ℝ (sectorOneVertex a b) u := by
    rw [sectorOneVertex, inner_planeVector_apply]
    exact add_nonneg (mul_nonneg (by linarith) hu0.le)
      (mul_nonneg (by linarith) hu1.le)
  rw [normalizedFireySupportVec,
    normalizedFireySupportVecSq_eq_sectorOnePairing_of_signs
      ha.le hb.le hu0.le hu1.le,
    Real.sqrt_sq_eq_abs, abs_of_nonneg hpair]

/-- Every support face whose normal lies in the open first sign chamber is
the singleton fixed Sector I vertex. -/
theorem exposedFace_sectorOneVector_eq_singleton {a b : ℝ} {u : Plane}
    (ha : 0 < a) (hb : 0 < b) (hu0 : 0 < u 0) (hu1 : 0 < u 1) :
    normalizedExposedFace a b u = {sectorOneVertex a b} := by
  ext x
  simp only [normalizedExposedFace, Set.mem_ofPred_eq, Set.mem_singleton_iff]
  constructor
  · rintro ⟨hx, hsupport⟩
    have hx0 : x 0 ≤ 1 + a := firstCoord_le_of_mem_normalizedLpSumTwo ha hx
    have hx1 : x 1 ≤ 1 + b := secondCoord_le_of_mem_normalizedLpSumTwo hb hx
    have hvertex := sectorOneVertex_supporting_vector ha hb hu0 hu1
    have hpair : x 0 * u 0 + x 1 * u 1 =
        (1 + a) * u 0 + (1 + b) * u 1 := by
      have hpair' := hsupport.trans hvertex.symm
      rw [PiLp.inner_apply, Fin.sum_univ_two, Real.inner_apply, Real.inner_apply] at hpair'
      have hvcoord : inner ℝ (sectorOneVertex a b) u =
          (1 + a) * u 0 + (1 + b) * u 1 := by
        rw [sectorOneVertex, inner_planeVector_apply]
      rw [hvcoord] at hpair'
      nlinarith
    have hx0eq : x 0 = 1 + a := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hx0) hu0.le,
        mul_nonneg (sub_nonneg.mpr hx1) hu1.le]
    have hx1eq : x 1 = 1 + b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hx0) hu0.le,
        mul_nonneg (sub_nonneg.mpr hx1) hu1.le]
    ext i
    fin_cases i
    · simpa [sectorOneVertex, planeVector] using hx0eq
    · simpa [sectorOneVertex, planeVector] using hx1eq
  · rintro rfl
    exact ⟨sectorOneVertex_mem_normalizedLpSumTwo a b,
      sectorOneVertex_supporting_vector ha hb hu0 hu1⟩

/-! ## Lower curved singleton faces -/

/-- The lower face opposite an open Sector II normal is the negative of the
canonical upper curved point. -/
theorem exposedFace_neg_sectorTwo_eq_singleton {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a))) :
    normalizedExposedFace a b (-planeDirection θ) =
      {-planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ)} := by
  rw [normalizedExposedFace_neg,
    exposedFace_sectorTwo_eq_singleton ha hb hθ]
  simp

/-- The lower face opposite an open Sector III normal is the negative of the
canonical upper curved point. -/
theorem exposedFace_neg_sectorThree_eq_singleton {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2 + arctan (b / a)) π) :
    normalizedExposedFace a b (-planeDirection θ) =
      {-planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ)} := by
  rw [normalizedExposedFace_neg,
    exposedFace_sectorThree_eq_singleton ha hb hθ]
  simp

/-! ## Positive scaling of normals -/

/-- Positive part commutes with multiplication by a nonnegative scalar. -/
theorem positivePart_mul_of_nonneg {c x : ℝ} (hc : 0 ≤ c) :
    positivePart (c * x) = c * positivePart x := by
  unfold positivePart
  by_cases hx : 0 ≤ x
  · rw [max_eq_left hx, max_eq_left (mul_nonneg hc hx)]
  · have hx' : x ≤ 0 := le_of_not_ge hx
    rw [max_eq_right hx', max_eq_right (mul_nonpos_of_nonneg_of_nonpos hc hx')]
    ring

/-- The prescribed squared support is homogeneous of degree two under
nonnegative scaling of its vector argument. -/
theorem normalizedFireySupportVecSq_smul_of_nonneg {a b c : ℝ} {u : Plane}
    (hc : 0 ≤ c) :
    normalizedFireySupportVecSq a b (c • u) =
      c ^ 2 * normalizedFireySupportVecSq a b u := by
  rw [normalizedFireySupportVecSq_eq_positiveParts,
    normalizedFireySupportVecSq_eq_positiveParts]
  simp only [real_inner_smul_right]
  simp_rw [positivePart_mul_of_nonneg hc]
  rw [show -(c * inner ℝ (planeVector 1 0) u) =
      c * (-inner ℝ (planeVector 1 0) u) by ring,
    show -(c * inner ℝ (planeVector a b) u) =
      c * (-inner ℝ (planeVector a b) u) by ring,
    show -(c * inner ℝ (planeVector 0 1) u) =
      c * (-inner ℝ (planeVector 0 1) u) by ring]
  simp_rw [positivePart_mul_of_nonneg hc]
  ring

/-- The prescribed support is positively homogeneous of degree one. -/
theorem normalizedFireySupportVec_smul_of_nonneg {a b c : ℝ} {u : Plane}
    (hc : 0 ≤ c) :
    normalizedFireySupportVec a b (c • u) =
      c * normalizedFireySupportVec a b u := by
  rw [normalizedFireySupportVec,
    normalizedFireySupportVecSq_smul_of_nonneg hc,
    Real.sqrt_mul (sq_nonneg c), Real.sqrt_sq_eq_abs,
    abs_of_nonneg hc]
  rfl

/-- Multiplying a normal by a positive scalar does not change its exposed
face.  This is the ray reduction used by the finite chamber atlas. -/
theorem normalizedExposedFace_smul_of_pos {a b c : ℝ} {u : Plane}
    (hc : 0 < c) :
    normalizedExposedFace a b (c • u) = normalizedExposedFace a b u := by
  ext x
  simp only [normalizedExposedFace, Set.mem_ofPred_eq]
  rw [real_inner_smul_right, normalizedFireySupportVec_smul_of_nonneg hc.le]
  constructor
  · rintro ⟨hx, heq⟩
    exact ⟨hx, (mul_left_cancel₀ hc.ne' heq)⟩
  · rintro ⟨hx, heq⟩
    exact ⟨hx, by rw [heq]⟩

/-! ## Polar reduction of arbitrary upper-half normals -/

/-- Regard a plane vector as the complex number with the same coordinates. -/
noncomputable def planeComplex (u : Plane) : ℂ := ⟨u 0, u 1⟩

@[simp] theorem planeComplex_re (u : Plane) : (planeComplex u).re = u 0 := rfl

@[simp] theorem planeComplex_im (u : Plane) : (planeComplex u).im = u 1 := rfl

/-- A nonzero plane vector is its complex norm times the unit direction at
its principal argument. -/
theorem eq_complexNorm_smul_planeDirection_arg {u : Plane} (hu : u ≠ 0) :
    u = ‖planeComplex u‖ • planeDirection (Complex.arg (planeComplex u)) := by
  have hz : planeComplex u ≠ 0 := by
    intro hz
    apply hu
    ext i
    fin_cases i
    · have := congr_arg Complex.re hz
      simpa using this
    · have := congr_arg Complex.im hz
      simpa using this
  ext i
  fin_cases i
  · change u 0 = ‖planeComplex u‖ * cos (Complex.arg (planeComplex u))
    exact (Complex.norm_mul_cos_arg (planeComplex u)).symm
  · change u 1 = ‖planeComplex u‖ * sin (Complex.arg (planeComplex u))
    exact (Complex.norm_mul_sin_arg (planeComplex u)).symm

/-- The principal argument of a nonzero upper-half vector lies on the closed
upper half-circle, and its polar scaling is strictly positive. -/
theorem complexArg_mem_upperHalf {u : Plane} (hu : u ≠ 0) (hu1 : 0 ≤ u 1) :
    Complex.arg (planeComplex u) ∈ Icc 0 π ∧ 0 < ‖planeComplex u‖ := by
  have hz : planeComplex u ≠ 0 := by
    intro hz
    apply hu
    ext i
    fin_cases i
    · have := congr_arg Complex.re hz
      simpa using this
    · have := congr_arg Complex.im hz
      simpa using this
  exact ⟨⟨Complex.arg_nonneg_iff.2 (by simpa using hu1),
      Complex.arg_le_pi _⟩, norm_pos_iff.mpr hz⟩

/-! ## The finite upper-normal atlas -/

/-- Boundary points exposed by normals on the closed upper half-circle.  It
contains three open smooth pieces, the fixed Sector I vertex, and all four
transition faces encountered from angle `0` through angle `π` (the first and
last are opposite closing faces). -/
noncomputable def normalizedUpperNormalBoundary (a b : ℝ) : Set Plane :=
  (-sectorThreeOneJump a b) ∪
    {sectorOneVertex a b} ∪
    sectorOneTwoJump a b ∪
    (fun θ ↦ planeVector (sectorTwoBoundaryX a b θ)
      (sectorTwoBoundaryY a b θ)) ''
        Ioo (π / 2) (π / 2 + arctan (b / a)) ∪
    sectorTwoThreeJump a b ∪
    (fun θ ↦ planeVector (sectorThreeBoundaryX a b θ)
      (sectorThreeBoundaryY a b θ)) ''
        Ioo (π / 2 + arctan (b / a)) π ∪
    sectorThreeOneJump a b

/-- The middle transition normal is the positive radius multiple of its unit
angular direction. -/
theorem middleRadius_smul_planeDirection_middleAngle {a b : ℝ} (ha : 0 < a) :
    middleRadius a b • planeDirection (π / 2 + arctan (b / a)) =
      middleNormal a b := by
  ext i
  fin_cases i
  · change middleRadius a b * cos (π / 2 + arctan (b / a)) = -b
    exact middleRadius_mul_cos_middleAngle ha
  · change middleRadius a b * sin (π / 2 + arctan (b / a)) = a
    exact middleRadius_mul_sin_middleAngle ha

/-- The unit middle direction has the already classified middle jump face. -/
theorem exposedFace_middleDirection_eq_sectorTwoThreeJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b
        (planeDirection (π / 2 + arctan (b / a))) =
      sectorTwoThreeJump a b := by
  have hscale := normalizedExposedFace_smul_of_pos
    (a := a) (b := b)
    (u := planeDirection (π / 2 + arctan (b / a)))
    (middleRadius_pos (a := a) (b := b) ha)
  rw [middleRadius_smul_planeDirection_middleAngle ha] at hscale
  have hmiddle : normalizedExposedFace a b (middleNormal a b) =
      sectorTwoThreeJump a b := by
    change {x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x (middleNormal a b) =
        normalizedFireySupportVec a b (middleNormal a b)} = _
    exact exposedFace_middleNormal_eq_sectorTwoThreeJump ha hb
  rw [hmiddle] at hscale
  exact hscale.symm

/-- The four endpoint directions of the upper angular interval recover the
checked transition faces. -/
theorem exposedFace_planeDirection_zero {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b (planeDirection 0) =
      -sectorThreeOneJump a b := by
  simpa [planeDirection, planeE1, planeVector] using
    exposedFace_planeE1_eq_neg_sectorThreeOneJump ha hb

theorem exposedFace_planeDirection_pi_div_two {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b (planeDirection (π / 2)) =
      sectorOneTwoJump a b := by
  have hdir : planeDirection (π / 2) = planeE2 := by
    ext i
    fin_cases i <;> simp [planeDirection, planeE2, planeVector]
  rw [hdir]
  change {x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x planeE2 = normalizedFireySupportVec a b planeE2} = _
  exact exposedFace_planeE2_eq_sectorOneTwoJump ha hb

theorem exposedFace_planeDirection_pi {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedExposedFace a b (planeDirection π) =
      sectorThreeOneJump a b := by
  have hdir : planeDirection π = -planeE1 := by
    ext i
    fin_cases i <;> simp [planeDirection, planeE1, planeVector]
  rw [hdir]
  change {x | x ∈ normalizedLpSumTwo a b ∧
      inner ℝ x (-planeE1) = normalizedFireySupportVec a b (-planeE1)} = _
  exact exposedFace_neg_planeE1_eq_sectorThreeOneJump ha hb

/-- Every face exposed by a unit normal on the closed upper half-circle lies
in the explicit finite upper-normal atlas. -/
theorem exposedFace_planeDirection_subset_upperNormalBoundary
    {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b) (hθ : θ ∈ Icc 0 π) :
    normalizedExposedFace a b (planeDirection θ) ⊆
      normalizedUpperNormalBoundary a b := by
  intro x hx
  have hφ := generatorAngle_mem_Ioo ha hb
  rcases lt_trichotomy θ (π / 2) with hfirst | hfirst | hfirst
  · rcases eq_or_lt_of_le hθ.1 with hzero | hzero
    · subst θ
      rw [exposedFace_planeDirection_zero ha hb] at hx
      simp only [normalizedUpperNormalBoundary, mem_union]
      exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inl (Or.inl hx)))))
    · have hcos : 0 < cos θ := Real.cos_pos_of_mem_Ioo ⟨by linarith [pi_pos], hfirst⟩
      have hsin : 0 < sin θ := Real.sin_pos_of_pos_of_lt_pi hzero
        (hfirst.trans (by linarith [pi_pos]))
      rw [exposedFace_sectorOneVector_eq_singleton ha hb hcos hsin] at hx
      simp only [normalizedUpperNormalBoundary, mem_union]
      exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inl (Or.inr hx)))))
  · subst θ
    rw [exposedFace_planeDirection_pi_div_two ha hb] at hx
    simp only [normalizedUpperNormalBoundary, mem_union]
    exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inr hx))))
  · rcases lt_trichotomy θ (π / 2 + arctan (b / a)) with hmiddle | hmiddle | hmiddle
    · rw [exposedFace_sectorTwo_eq_singleton ha hb ⟨hfirst, hmiddle⟩] at hx
      rcases Set.mem_singleton_iff.mp hx with rfl
      simp only [normalizedUpperNormalBoundary, mem_union]
      exact Or.inl (Or.inl (Or.inl (Or.inr ⟨θ, ⟨hfirst, hmiddle⟩, rfl⟩)))
    · subst θ
      rw [exposedFace_middleDirection_eq_sectorTwoThreeJump ha hb] at hx
      simp only [normalizedUpperNormalBoundary, mem_union]
      exact Or.inl (Or.inl (Or.inr hx))
    · rcases eq_or_lt_of_le hθ.2 with hpi | hpi
      · subst θ
        rw [exposedFace_planeDirection_pi ha hb] at hx
        simp only [normalizedUpperNormalBoundary, mem_union]
        exact Or.inr hx
      · rw [exposedFace_sectorThree_eq_singleton ha hb ⟨hmiddle, hpi⟩] at hx
        rcases Set.mem_singleton_iff.mp hx with rfl
        simp only [normalizedUpperNormalBoundary, mem_union]
        exact Or.inl (Or.inr ⟨θ, ⟨hmiddle, hpi⟩, rfl⟩)

/-- Every nonzero upper-half normal exposes only points in the finite atlas;
positive homogeneity reduces it to the preceding angular theorem. -/
theorem exposedFace_upperHalf_subset_upperNormalBoundary
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) {u : Plane}
    (hu : u ≠ 0) (hu1 : 0 ≤ u 1) :
    normalizedExposedFace a b u ⊆ normalizedUpperNormalBoundary a b := by
  obtain ⟨hθ, hc⟩ := complexArg_mem_upperHalf hu hu1
  rw [eq_complexNorm_smul_planeDirection_arg hu,
    normalizedExposedFace_smul_of_pos hc]
  exact exposedFace_planeDirection_subset_upperNormalBoundary ha hb hθ

/-! ## Exhaustion by all nonzero exposed faces -/

/-- An angular unit direction is never zero. -/
theorem planeDirection_ne_zero (θ : ℝ) : planeDirection θ ≠ 0 := by
  intro hzero
  have hx := congr_arg (fun x : Plane ↦ x 0) hzero
  have hy := congr_arg (fun x : Plane ↦ x 1) hzero
  simp [planeDirection, planeVector] at hx hy
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- A point attaining support at a nonzero normal cannot lie in the interior,
so every such exposed face is contained in the frontier. -/
theorem normalizedExposedFace_subset_frontier_of_ne_zero {a b : ℝ}
    {u : Plane} (hu : u ≠ 0) :
    normalizedExposedFace a b u ⊆ frontier (normalizedLpSumTwo a b) := by
  intro x hx
  rw [(isClosed_normalizedLpSumTwo a b).frontier_eq]
  refine ⟨hx.1, ?_⟩
  intro hxint
  have hnhds : normalizedLpSumTwo a b ∈ nhds x :=
    mem_interior_iff_mem_nhds.mp hxint
  obtain ⟨ε, hε, hball⟩ := Metric.mem_nhds_iff.mp hnhds
  let t : ℝ := ε / (2 * ‖u‖)
  have hunorm : 0 < ‖u‖ := norm_pos_iff.mpr hu
  have ht : 0 < t := div_pos hε (by positivity)
  have hdist : dist (x + t • u) x < ε := by
    rw [dist_eq_norm, add_sub_cancel_left, norm_smul, Real.norm_eq_abs,
      abs_of_pos ht]
    change ε / (2 * ‖u‖) * ‖u‖ < ε
    rw [div_mul_eq_mul_div]
    have hunorm0 : ‖u‖ ≠ 0 := ne_of_gt hunorm
    calc
      ε * ‖u‖ / (2 * ‖u‖) = ε / 2 := by field_simp
      _ < ε := by linarith
  have hy := hball hdist
  have hbound := hy u
  have hinner : inner ℝ (x + t • u) u =
      normalizedFireySupportVec a b u + t * ‖u‖ ^ 2 := by
    rw [inner_add_left, inner_smul_left, hx.2, real_inner_self_eq_norm_sq]
    simp only [starRingEnd_apply, star_trivial]
  rw [hinner] at hbound
  have : 0 < t * ‖u‖ ^ 2 := mul_pos ht (sq_pos_of_pos hunorm)
  linarith

/-- The frontier is exactly exhausted by the exposed faces at all nonzero
normals.  This theorem is topological and independent of the subsequent
finite sign-chamber classification. -/
theorem frontier_normalizedLpSumTwo_eq_iUnion_nonzero_exposedFaces
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    frontier (normalizedLpSumTwo a b) =
      ⋃ u : {u : Plane // u ≠ 0}, normalizedExposedFace a b u.1 := by
  ext x
  constructor
  · intro hx
    obtain ⟨u, hu, hxu⟩ :=
      exists_nonzero_normal_mem_exposedFace_of_mem_frontier ha hb hx
    exact Set.mem_iUnion.2 ⟨⟨u, hu⟩, hxu⟩
  · intro hx
    obtain ⟨u, hxu⟩ := Set.mem_iUnion.1 hx
    exact normalizedExposedFace_subset_frontier_of_ne_zero u.2 hxu

/-- Every point of the explicit upper-normal atlas lies on the frontier. -/
theorem normalizedUpperNormalBoundary_subset_frontier
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    normalizedUpperNormalBoundary a b ⊆ frontier (normalizedLpSumTwo a b) := by
  intro x hx
  simp only [normalizedUpperNormalBoundary, mem_union] at hx
  rcases hx with (((((h01 | h2) | h3) | h4) | h5) | h6)
  · rcases h01 with h0 | h1
    · apply normalizedExposedFace_subset_frontier_of_ne_zero
        (planeDirection_ne_zero 0)
      rw [exposedFace_planeDirection_zero ha hb]
      exact h0
    · have hone : planeVector 1 1 ≠ (0 : Plane) := by
        intro h
        have := congr_arg (fun y : Plane ↦ y 0) h
        norm_num [planeVector] at this
      apply normalizedExposedFace_subset_frontier_of_ne_zero hone
      rw [exposedFace_sectorOneVector_eq_singleton ha hb
        (by simp [planeVector]) (by simp [planeVector])]
      exact h1
  · apply normalizedExposedFace_subset_frontier_of_ne_zero
      (planeDirection_ne_zero (π / 2))
    rw [exposedFace_planeDirection_pi_div_two ha hb]
    exact h2
  · rcases h3 with ⟨θ, hθ, rfl⟩
    apply normalizedExposedFace_subset_frontier_of_ne_zero (planeDirection_ne_zero θ)
    rw [exposedFace_sectorTwo_eq_singleton ha hb hθ]
    exact Set.mem_singleton _
  · apply normalizedExposedFace_subset_frontier_of_ne_zero
      (planeDirection_ne_zero (π / 2 + arctan (b / a)))
    rw [exposedFace_middleDirection_eq_sectorTwoThreeJump ha hb]
    exact h4
  · rcases h5 with ⟨θ, hθ, rfl⟩
    apply normalizedExposedFace_subset_frontier_of_ne_zero (planeDirection_ne_zero θ)
    rw [exposedFace_sectorThree_eq_singleton ha hb hθ]
    exact Set.mem_singleton _
  · apply normalizedExposedFace_subset_frontier_of_ne_zero (planeDirection_ne_zero π)
    rw [exposedFace_planeDirection_pi ha hb]
    exact h6

/-- Negation preserves the frontier of the centrally symmetric exact body. -/
theorem neg_mem_frontier_normalizedLpSumTwo_iff {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {x : Plane} :
    -x ∈ frontier (normalizedLpSumTwo a b) ↔
      x ∈ frontier (normalizedLpSumTwo a b) := by
  constructor
  · intro hx
    obtain ⟨u, hu, hxu⟩ :=
      exists_nonzero_normal_mem_exposedFace_of_mem_frontier ha hb hx
    have hxface : x ∈ normalizedExposedFace a b (-u) := by
      rw [normalizedExposedFace_neg, Set.mem_neg]
      simpa using hxu
    exact normalizedExposedFace_subset_frontier_of_ne_zero (neg_ne_zero.mpr hu) hxface
  · intro hx
    obtain ⟨u, hu, hxu⟩ :=
      exists_nonzero_normal_mem_exposedFace_of_mem_frontier ha hb hx
    have hxface : -x ∈ normalizedExposedFace a b (-u) := by
      rw [normalizedExposedFace_neg, Set.mem_neg]
      simpa using hxu
    exact normalizedExposedFace_subset_frontier_of_ne_zero (neg_ne_zero.mpr hu) hxface

/-- Complete canonical frontier atlas: the frontier is the upper-normal atlas
and its pointwise negative.  In particular it is exhausted by the two smooth
curved families, the two opposite fixed vertices, and the six classified jump
segments. -/
theorem frontier_normalizedLpSumTwo_eq_upperNormalBoundary_union_neg
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    frontier (normalizedLpSumTwo a b) =
      normalizedUpperNormalBoundary a b ∪ -normalizedUpperNormalBoundary a b := by
  ext x
  constructor
  · intro hx
    obtain ⟨u, hu, hxu⟩ :=
      exists_nonzero_normal_mem_exposedFace_of_mem_frontier ha hb hx
    by_cases hu1 : 0 ≤ u 1
    · exact Or.inl (exposedFace_upperHalf_subset_upperNormalBoundary ha hb hu hu1 hxu)
    · have hnegFace : -x ∈ normalizedExposedFace a b (-u) := by
        rw [normalizedExposedFace_neg, Set.mem_neg]
        simpa using hxu
      have hupper := exposedFace_upperHalf_subset_upperNormalBoundary ha hb
        (neg_ne_zero.mpr hu) (by simpa using le_of_not_ge hu1) hnegFace
      exact Or.inr (by rw [Set.mem_neg]; simpa using hupper)
  · rintro (hx | hx)
    · exact normalizedUpperNormalBoundary_subset_frontier ha hb hx
    · rw [Set.mem_neg] at hx
      have hneg := normalizedUpperNormalBoundary_subset_frontier ha hb hx
      exact (neg_mem_frontier_normalizedLpSumTwo_iff ha hb).mp (by simpa using hneg)

#print axioms sectorOneVertex_supporting_vector
#print axioms exposedFace_sectorOneVector_eq_singleton
#print axioms exposedFace_neg_sectorTwo_eq_singleton
#print axioms exposedFace_neg_sectorThree_eq_singleton
#print axioms normalizedFireySupportVecSq_smul_of_nonneg
#print axioms normalizedFireySupportVec_smul_of_nonneg
#print axioms normalizedExposedFace_smul_of_pos
#print axioms eq_complexNorm_smul_planeDirection_arg
#print axioms complexArg_mem_upperHalf
#print axioms exposedFace_middleDirection_eq_sectorTwoThreeJump
#print axioms exposedFace_planeDirection_subset_upperNormalBoundary
#print axioms exposedFace_upperHalf_subset_upperNormalBoundary
#print axioms normalizedExposedFace_subset_frontier_of_ne_zero
#print axioms frontier_normalizedLpSumTwo_eq_iUnion_nonzero_exposedFaces
#print axioms normalizedUpperNormalBoundary_subset_frontier
#print axioms neg_mem_frontier_normalizedLpSumTwo_iff
#print axioms frontier_normalizedLpSumTwo_eq_upperNormalBoundary_union_neg

end L2Hexagon
