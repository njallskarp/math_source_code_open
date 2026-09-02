import L2Hexagon.LowerFacesAndCurvedUniqueness
import Mathlib.Analysis.LocallyConvex.Separation
import Mathlib.Analysis.InnerProductSpace.Dual

/-!
# Compactness and supporting normals for the exact halfspace body

This file supplies the topological precursor needed for frontier exhaustion.
The defining Firey support dominates the Euclidean norm, so the open unit ball
lies in the exact halfspace body.  Coordinate halfspaces make the body bounded,
and its literal intersection-of-halfspaces definition makes it closed.

We also prove that the prescribed support is attained in every vector
direction, by splitting the upper half-plane into the same three generator-sign
chambers as the angular development and using central symmetry below it.
Geometric Hahn--Banach can therefore turn every frontier point into membership
in a literal `normalizedExposedFace` for a nonzero normal.
-/

open Real Set

namespace L2Hexagon

/-! ## A uniform inradius and compactness -/

/-- The squared Firey support dominates the Euclidean norm square. -/
theorem norm_sq_le_normalizedFireySupportVecSq (a b : ℝ) (ξ : Plane) :
    ‖ξ‖ ^ 2 ≤ normalizedFireySupportVecSq a b ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  let x := inner ℝ (planeVector 1 0) ξ
  let y := inner ℝ (planeVector a b) ξ
  let z := inner ℝ (planeVector 0 1) ξ
  have hpx : 0 ≤ positivePart x := by unfold positivePart; exact le_max_right _ _
  have hpy : 0 ≤ positivePart y := by unfold positivePart; exact le_max_right _ _
  have hpz : 0 ≤ positivePart z := by unfold positivePart; exact le_max_right _ _
  have hnx : 0 ≤ positivePart (-x) := by unfold positivePart; exact le_max_right _ _
  have hny : 0 ≤ positivePart (-y) := by unfold positivePart; exact le_max_right _ _
  have hnz : 0 ≤ positivePart (-z) := by unfold positivePart; exact le_max_right _ _
  have hxparts : positivePart x ^ 2 + positivePart (-x) ^ 2 = x ^ 2 := by
    rcases le_total 0 x with hx | hx
    · simp [positivePart, max_eq_left hx, max_eq_right (neg_nonpos.mpr hx)]
    · simp [positivePart, max_eq_right hx, max_eq_left (neg_nonneg.mpr hx)]
  have hzparts : positivePart z ^ 2 + positivePart (-z) ^ 2 = z ^ 2 := by
    rcases le_total 0 z with hz | hz
    · simp [positivePart, max_eq_left hz, max_eq_right (neg_nonpos.mpr hz)]
    · simp [positivePart, max_eq_right hz, max_eq_left (neg_nonneg.mpr hz)]
  have hpos : positivePart x ^ 2 + positivePart z ^ 2 ≤
      (positivePart x + positivePart y + positivePart z) ^ 2 := by
    nlinarith [mul_nonneg hpx hpy, mul_nonneg hpx hpz, mul_nonneg hpy hpz,
      sq_nonneg (positivePart y)]
  have hneg : positivePart (-x) ^ 2 + positivePart (-z) ^ 2 ≤
      (positivePart (-x) + positivePart (-y) + positivePart (-z)) ^ 2 := by
    nlinarith [mul_nonneg hnx hny, mul_nonneg hnx hnz, mul_nonneg hny hnz,
      sq_nonneg (positivePart (-y))]
  have hnorm : ‖ξ‖ ^ 2 = x ^ 2 + z ^ 2 := by
    rw [EuclideanSpace.norm_sq_eq, Fin.sum_univ_two]
    simp [x, z, inner_planeVector_apply, sq_abs]
  rw [hnorm, ← hxparts, ← hzparts]
  linarith

/-- The prescribed Firey support is at least the Euclidean norm in every
direction. -/
theorem norm_le_normalizedFireySupportVec (a b : ℝ) (ξ : Plane) :
    ‖ξ‖ ≤ normalizedFireySupportVec a b ξ := by
  unfold normalizedFireySupportVec
  apply le_sqrt_of_sq_le
  · unfold normalizedFireySupportVecSq
    positivity
  · exact norm_sq_le_normalizedFireySupportVecSq a b ξ

/-- The open unit ball about the origin lies in the exact halfspace body. -/
theorem ball_zero_one_subset_normalizedLpSumTwo (a b : ℝ) :
    Metric.ball (0 : Plane) 1 ⊆ normalizedLpSumTwo a b := by
  intro x hx ξ
  have hxnorm : ‖x‖ < 1 := by simpa [Metric.mem_ball, dist_eq_norm] using hx
  calc
    inner ℝ x ξ ≤ ‖x‖ * ‖ξ‖ := real_inner_le_norm x ξ
    _ ≤ ‖ξ‖ := mul_le_of_le_one_left (norm_nonneg ξ) hxnorm.le
    _ ≤ normalizedFireySupportVec a b ξ :=
      norm_le_normalizedFireySupportVec a b ξ

/-- The exact halfspace body has nonempty interior, uniformly in the
parameters. -/
theorem zero_mem_interior_normalizedLpSumTwo (a b : ℝ) :
    (0 : Plane) ∈ interior (normalizedLpSumTwo a b) := by
  rw [mem_interior_iff_mem_nhds]
  exact Filter.mem_of_superset
    (Metric.isOpen_ball.mem_nhds (Metric.mem_ball_self zero_lt_one))
    (ball_zero_one_subset_normalizedLpSumTwo a b)

theorem interior_normalizedLpSumTwo_nonempty (a b : ℝ) :
    (interior (normalizedLpSumTwo a b)).Nonempty :=
  ⟨0, zero_mem_interior_normalizedLpSumTwo a b⟩

/-- The exact body is closed as an intersection of closed halfspaces. -/
theorem isClosed_normalizedLpSumTwo (a b : ℝ) :
    IsClosed (normalizedLpSumTwo a b) := by
  rw [normalizedLpSumTwo]
  have heq : {x : Plane | ∀ ξ : Plane,
      inner ℝ x ξ ≤ normalizedFireySupportVec a b ξ} =
      ⋂ ξ : Plane, {x : Plane |
        inner ℝ x ξ ≤ normalizedFireySupportVec a b ξ} := by
    ext x
    simp
  rw [heq]
  exact isClosed_iInter fun ξ ↦ isClosed_le
    (continuous_id.inner (continuous_const : Continuous fun _ : Plane ↦ ξ))
    continuous_const

/-- The second coordinate is bounded above by its vertical support value. -/
theorem secondCoord_le_of_mem_normalizedLpSumTwo {a b : ℝ} (hb : 0 < b)
    {x : Plane} (hx : x ∈ normalizedLpSumTwo a b) :
    x 1 ≤ 1 + b := by
  have h := hx planeE2
  rw [normalizedFireySupportVec_planeE2 hb] at h
  simpa [planeE2, PiLp.inner_apply, Fin.sum_univ_two, planeVector] using h

/-- Coordinate bounds give a simple global Euclidean norm bound. -/
theorem norm_le_of_mem_normalizedLpSumTwo {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {x : Plane}
    (hx : x ∈ normalizedLpSumTwo a b) :
    ‖x‖ ≤ 2 + a + b := by
  have hx0hi : x 0 ≤ 1 + a := firstCoord_le_of_mem_normalizedLpSumTwo ha hx
  have hx1hi : x 1 ≤ 1 + b := secondCoord_le_of_mem_normalizedLpSumTwo hb hx
  have hneg := neg_mem_normalizedLpSumTwo hx
  have hx0lo : -(1 + a) ≤ x 0 := by
    have := firstCoord_le_of_mem_normalizedLpSumTwo ha hneg
    change -(x 0) ≤ 1 + a at this
    linarith
  have hx1lo : -(1 + b) ≤ x 1 := by
    have := secondCoord_le_of_mem_normalizedLpSumTwo hb hneg
    change -(x 1) ≤ 1 + b at this
    linarith
  have hA : 0 ≤ 1 + a := by linarith
  have hB : 0 ≤ 1 + b := by linarith
  have hx0sq : (x 0) ^ 2 ≤ (1 + a) ^ 2 := by
    simpa only [sq_abs] using
      (sq_le_sq₀ (abs_nonneg (x 0)) hA).mpr (abs_le.2 ⟨hx0lo, hx0hi⟩)
  have hx1sq : (x 1) ^ 2 ≤ (1 + b) ^ 2 := by
    simpa only [sq_abs] using
      (sq_le_sq₀ (abs_nonneg (x 1)) hB).mpr (abs_le.2 ⟨hx1lo, hx1hi⟩)
  have hnormsq : ‖x‖ ^ 2 = (x 0) ^ 2 + (x 1) ^ 2 := by
    rw [EuclideanSpace.norm_sq_eq, Fin.sum_univ_two]
    simp [sq_abs]
  have hR : 0 ≤ 2 + a + b := by linarith
  apply (sq_le_sq₀ (norm_nonneg x) hR).mp
  rw [hnormsq]
  nlinarith [mul_nonneg hA hB]

theorem isBounded_normalizedLpSumTwo {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Bornology.IsBounded (normalizedLpSumTwo a b) :=
  isBounded_iff_forall_norm_le.2 ⟨2 + a + b,
    fun _ hx ↦ norm_le_of_mem_normalizedLpSumTwo ha hb hx⟩

/-- The exact normalized halfspace body is compact. -/
theorem isCompact_normalizedLpSumTwo {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    IsCompact (normalizedLpSumTwo a b) :=
  Metric.isCompact_iff_isClosed_bounded.2
    ⟨isClosed_normalizedLpSumTwo a b, isBounded_normalizedLpSumTwo ha hb⟩

/-! ## Support attainment in every vector direction -/

/-- In the first sign chamber the fixed vertex pairing is exactly the
prescribed squared support. -/
theorem normalizedFireySupportVecSq_eq_sectorOnePairing_of_signs
    {a b : ℝ} {ξ : Plane} (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hx : 0 ≤ ξ 0) (hy : 0 ≤ ξ 1) :
    normalizedFireySupportVecSq a b ξ =
      inner ℝ (sectorOneVertex a b) ξ ^ 2 := by
  have hm : 0 ≤ a * ξ 0 + b * ξ 1 := by
    exact add_nonneg (mul_nonneg ha hx) (mul_nonneg hb hy)
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero]
  unfold positivePart
  rw [max_eq_left hx, max_eq_left hy, max_eq_left hm,
    max_eq_right (neg_nonpos.mpr hx), max_eq_right (neg_nonpos.mpr hy),
    max_eq_right (neg_nonpos.mpr hm)]
  unfold sectorOneVertex
  rw [inner_planeVector_apply]
  ring

/-- In the second sign chamber the prescribed square is the indicated
two-generator ellipsoid support. -/
theorem normalizedFireySupportVecSq_eq_sectorTwoVector_of_signs
    {a b : ℝ} {ξ : Plane} (hx : ξ 0 ≤ 0) (hy : 0 ≤ ξ 1)
    (hm : 0 ≤ a * ξ 0 + b * ξ 1) :
    normalizedFireySupportVecSq a b ξ =
      twoGeneratorSupportSq (planeVector 1 0)
        (planeVector a b + planeVector 0 1) ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero,
    inner_add_left, twoGeneratorSupportSq]
  unfold positivePart
  rw [max_eq_right hx, max_eq_left hy, max_eq_left hm,
    max_eq_left (neg_nonneg.mpr hx), max_eq_right (neg_nonpos.mpr hy),
    max_eq_right (neg_nonpos.mpr hm)]
  ring

/-- In the third sign chamber the prescribed square is the other
two-generator ellipsoid support. -/
theorem normalizedFireySupportVecSq_eq_sectorThreeVector_of_signs
    {a b : ℝ} {ξ : Plane} (hx : ξ 0 ≤ 0) (hy : 0 ≤ ξ 1)
    (hm : a * ξ 0 + b * ξ 1 ≤ 0) :
    normalizedFireySupportVecSq a b ξ =
      twoGeneratorSupportSq (planeVector 0 1)
        (planeVector 1 0 + planeVector a b) ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero,
    inner_add_left, twoGeneratorSupportSq]
  unfold positivePart
  rw [max_eq_right hx, max_eq_left hy, max_eq_right hm,
    max_eq_left (neg_nonneg.mpr hx), max_eq_right (neg_nonpos.mpr hy),
    max_eq_left (neg_nonneg.mpr hm)]
  ring

/-- A two-generator Sector II point belongs to every defining halfspace. -/
theorem sectorTwoVectorBoundaryPoint_mem {a b : ℝ} {n : Plane}
    (hn : 0 < twoGeneratorSupportSq (planeVector 1 0)
      (planeVector a b + planeVector 0 1) n) :
    twoGeneratorBoundaryPoint (planeVector 1 0)
        (planeVector a b + planeVector 0 1) n ∈ normalizedLpSumTwo a b := by
  intro ξ
  calc
    inner ℝ (twoGeneratorBoundaryPoint (planeVector 1 0)
        (planeVector a b + planeVector 0 1) n) ξ ≤
        √(twoGeneratorSupportSq (planeVector 1 0)
          (planeVector a b + planeVector 0 1) ξ) :=
      inner_twoGeneratorBoundaryPoint_le hn
    _ ≤ √(normalizedFireySupportVecSq a b ξ) :=
      Real.sqrt_le_sqrt (twoGeneratorSupportSq_sectorTwo_le_firey a b ξ)
    _ = normalizedFireySupportVec a b ξ := rfl

/-- A two-generator Sector III point belongs to every defining halfspace. -/
theorem sectorThreeVectorBoundaryPoint_mem {a b : ℝ} {n : Plane}
    (hn : 0 < twoGeneratorSupportSq (planeVector 0 1)
      (planeVector 1 0 + planeVector a b) n) :
    twoGeneratorBoundaryPoint (planeVector 0 1)
        (planeVector 1 0 + planeVector a b) n ∈ normalizedLpSumTwo a b := by
  intro ξ
  calc
    inner ℝ (twoGeneratorBoundaryPoint (planeVector 0 1)
        (planeVector 1 0 + planeVector a b) n) ξ ≤
        √(twoGeneratorSupportSq (planeVector 0 1)
          (planeVector 1 0 + planeVector a b) ξ) :=
      inner_twoGeneratorBoundaryPoint_le hn
    _ ≤ √(normalizedFireySupportVecSq a b ξ) :=
      Real.sqrt_le_sqrt (twoGeneratorSupportSq_sectorThree_le_firey a b ξ)
    _ = normalizedFireySupportVec a b ξ := rfl

/-- Every direction in the closed upper half-plane has an explicit point of
the exact body attaining the prescribed support. -/
theorem exists_supportingPoint_upperHalf {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (ξ : Plane) (hy : 0 ≤ ξ 1) :
    ∃ x ∈ normalizedLpSumTwo a b,
      inner ℝ x ξ = normalizedFireySupportVec a b ξ := by
  by_cases hx : 0 ≤ ξ 0
  · refine ⟨sectorOneVertex a b, sectorOneVertex_mem_normalizedLpSumTwo a b, ?_⟩
    have hm : 0 ≤ a * ξ 0 + b * ξ 1 :=
      add_nonneg (mul_nonneg ha.le hx) (mul_nonneg hb.le hy)
    have hp : 0 ≤ inner ℝ (sectorOneVertex a b) ξ := by
      rw [sectorOneVertex, inner_planeVector_apply]
      exact add_nonneg (mul_nonneg (by linarith) hx) (mul_nonneg (by linarith) hy)
    rw [normalizedFireySupportVec,
      normalizedFireySupportVecSq_eq_sectorOnePairing_of_signs ha.le hb.le hx hy,
      Real.sqrt_sq_eq_abs, abs_of_nonneg hp]
  · have hx' : ξ 0 < 0 := lt_of_not_ge hx
    by_cases hm : 0 ≤ a * ξ 0 + b * ξ 1
    · let p := planeVector 1 0
      let q := planeVector a b + planeVector 0 1
      have hn : 0 < twoGeneratorSupportSq p q ξ := by
        unfold p q twoGeneratorSupportSq
        simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero,
          inner_add_left]
        nlinarith [sq_pos_of_neg hx']
      refine ⟨twoGeneratorBoundaryPoint p q ξ,
        sectorTwoVectorBoundaryPoint_mem hn, ?_⟩
      rw [inner_twoGeneratorBoundaryPoint_self hn, normalizedFireySupportVec,
        normalizedFireySupportVecSq_eq_sectorTwoVector_of_signs hx'.le hy hm]
    · have hm' : a * ξ 0 + b * ξ 1 < 0 := lt_of_not_ge hm
      let p := planeVector 0 1
      let q := planeVector 1 0 + planeVector a b
      have hn : 0 < twoGeneratorSupportSq p q ξ := by
        unfold p q twoGeneratorSupportSq
        simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero,
          inner_add_left]
        nlinarith [sq_pos_of_neg (add_neg hx' hm')]
      refine ⟨twoGeneratorBoundaryPoint p q ξ,
        sectorThreeVectorBoundaryPoint_mem hn, ?_⟩
      rw [inner_twoGeneratorBoundaryPoint_self hn, normalizedFireySupportVec,
        normalizedFireySupportVecSq_eq_sectorThreeVector_of_signs hx'.le hy hm'.le]

/-- The prescribed Firey support is attained by a point of the exact body in
every vector direction. -/
theorem exists_mem_inner_eq_normalizedFireySupportVec {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ξ : Plane) :
    ∃ x ∈ normalizedLpSumTwo a b,
      inner ℝ x ξ = normalizedFireySupportVec a b ξ := by
  by_cases hy : 0 ≤ ξ 1
  · exact exists_supportingPoint_upperHalf ha hb ξ hy
  · obtain ⟨x, hx, hsupport⟩ :=
      exists_supportingPoint_upperHalf ha hb (-ξ) (by simpa using le_of_not_ge hy)
    refine ⟨-x, neg_mem_normalizedLpSumTwo hx, ?_⟩
    rw [inner_neg_left]
    rw [inner_neg_right, normalizedFireySupportVec_neg] at hsupport
    exact hsupport

/-- The literal subtype-supremum support of the exact halfspace body agrees
with its prescribed Firey support in every vector direction. -/
theorem setSupportFunction_normalizedLpSumTwo_allDirections {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ξ : Plane) :
    setSupportFunction (normalizedLpSumTwo a b) ξ =
      normalizedFireySupportVec a b ξ := by
  obtain ⟨x, hx, hattain⟩ :=
    exists_mem_inner_eq_normalizedFireySupportVec ha hb ξ
  have hgreatest : IsGreatest
      ((fun y : Plane ↦ inner ℝ y ξ) '' normalizedLpSumTwo a b)
      (normalizedFireySupportVec a b ξ) := by
    constructor
    · exact ⟨x, hx, hattain⟩
    · rintro _ ⟨y, hy, rfl⟩
      exact hy ξ
  exact hgreatest.isLUB.ciSup_set_eq ⟨x, hx⟩

/-! ## A supporting normal at every frontier point -/

/-- Every frontier point of the exact compact convex body lies in a literal
exposed face for some nonzero vector normal. -/
theorem exists_nonzero_normal_mem_exposedFace_of_mem_frontier
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) {x : Plane}
    (hx : x ∈ frontier (normalizedLpSumTwo a b)) :
    ∃ u : Plane, u ≠ 0 ∧ x ∈ normalizedExposedFace a b u := by
  have hx' : x ∈ normalizedLpSumTwo a b ∧
      x ∉ interior (normalizedLpSumTwo a b) := by
    have : x ∈ normalizedLpSumTwo a b \ interior (normalizedLpSumTwo a b) := by
      rw [← (isClosed_normalizedLpSumTwo a b).frontier_eq]
      exact hx
    exact this
  obtain ⟨f, hf, hmax⟩ := geometric_hahn_banach_of_nonempty_interior_point
    (convex_normalizedLpSumTwo a b) hx'.2
    (interior_normalizedLpSumTwo_nonempty a b)
  let u : Plane := (InnerProductSpace.toDual ℝ Plane).symm f
  have hu : u ≠ 0 := by
    intro hu0
    apply hf
    have hfu : f = (InnerProductSpace.toDual ℝ Plane) u := by
      exact ((InnerProductSpace.toDual ℝ Plane).apply_symm_apply f).symm
    rw [hu0] at hfu
    simpa using hfu
  have hriesz (z : Plane) : f z = inner ℝ z u := by
    calc
      f z = inner ℝ u z := InnerProductSpace.toDual_symm_apply.symm
      _ = inner ℝ z u := real_inner_comm z u
  obtain ⟨y, hy, hyattain⟩ :=
    exists_mem_inner_eq_normalizedFireySupportVec ha hb u
  have hyx : inner ℝ y u ≤ inner ℝ x u := by
    rw [← hriesz y, ← hriesz x]
    exact hmax y hy
  have hxupper : inner ℝ x u ≤ normalizedFireySupportVec a b u := hx'.1 u
  have hxeq : inner ℝ x u = normalizedFireySupportVec a b u := by
    linarith
  exact ⟨u, hu, hx'.1, hxeq⟩

#print axioms norm_sq_le_normalizedFireySupportVecSq
#print axioms isCompact_normalizedLpSumTwo
#print axioms exists_mem_inner_eq_normalizedFireySupportVec
#print axioms setSupportFunction_normalizedLpSumTwo_allDirections
#print axioms exists_nonzero_normal_mem_exposedFace_of_mem_frontier

end L2Hexagon
