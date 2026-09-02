import L2Hexagon.BoundaryAssembly
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# The exact halfspace body and its ellipsoidal support points

For the normalized three-segment zonotope, the `p = 2` Firey body is the
literal intersection of all halfspaces

`{x | inner x ξ ≤ sqrt (h_K(ξ)^2 + h_K(-ξ)^2)}`.

This is the specialization of the source Formal Conjectures definition; the
first theorem below records the exact real-power/square-root alignment.

The substantive geometric result in this file is global rather than
sector-local.  The full Firey support dominates each of the two quadratic
supports that occur on Sectors II and III.  Cauchy--Schwarz then shows that
the corresponding ellipsoidal canonical support point belongs to every
halfspace, not merely the halfspace at its displayed normal.  On its own
sector that point attains the defining support value.

This still does not identify the entire boundary or prove a planar
Lebesgue-area formula.
-/

open Real Set

namespace L2Hexagon

/-! ## Scalar domination identities -/

/-- The three-positive-parts square dominates the Sector II quadratic form. -/
theorem three_positive_parts_sq_ge_first_tail (x y z : ℝ) :
    x ^ 2 + (y + z) ^ 2 ≤
      (positivePart x + positivePart y + positivePart z) ^ 2 +
        (positivePart (-x) + positivePart (-y) + positivePart (-z)) ^ 2 := by
  rw [three_positive_parts_sq_identity]
  have habs : |x - (y + z)| ≤ |x| + |y| + |z| := by
    calc
      |x - (y + z)| ≤ |x| + |y + z| := abs_sub x (y + z)
      _ ≤ |x| + (|y| + |z|) := by linarith [abs_add_le y z]
      _ = |x| + |y| + |z| := by ring
  have hsquareAbs : |x - (y + z)| ^ 2 ≤ (|x| + |y| + |z|) ^ 2 :=
    (sq_le_sq₀ (abs_nonneg _) (by positivity)).2 habs
  have hsquare : (x - (y + z)) ^ 2 ≤ (|x| + |y| + |z|) ^ 2 := by
    simpa only [sq_abs] using hsquareAbs
  nlinarith

/-- The same support square dominates the Sector III quadratic form. -/
theorem three_positive_parts_sq_ge_last_head (x y z : ℝ) :
    z ^ 2 + (x + y) ^ 2 ≤
      (positivePart x + positivePart y + positivePart z) ^ 2 +
        (positivePart (-x) + positivePart (-y) + positivePart (-z)) ^ 2 := by
  simpa only [add_comm, add_left_comm, add_assoc] using
    three_positive_parts_sq_ge_first_tail z x y

/-- The three-positive-parts square dominates the square of the total signed sum. -/
theorem three_positive_parts_sq_ge_sum (x y z : ℝ) :
    (x + y + z) ^ 2 ≤
      (positivePart x + positivePart y + positivePart z) ^ 2 +
        (positivePart (-x) + positivePart (-y) + positivePart (-z)) ^ 2 := by
  rw [three_positive_parts_sq_identity]
  have habs : |x + y + z| ≤ |x| + |y| + |z| := by
    calc
      |x + y + z| ≤ |x + y| + |z| := abs_add_le (x + y) z
      _ ≤ (|x| + |y|) + |z| := by linarith [abs_add_le x y]
      _ = |x| + |y| + |z| := by ring
  have hsquareAbs : |x + y + z| ^ 2 ≤ (|x| + |y| + |z|) ^ 2 :=
    (sq_le_sq₀ (abs_nonneg _) (by positivity)).2 habs
  have hsquare : (x + y + z) ^ 2 ≤ (|x| + |y| + |z|) ^ 2 := by
    simpa only [sq_abs] using hsquareAbs
  nlinarith

/-! ## Exact vector support and halfspace definition -/

/-- The literal squared `p=2` Firey support, for an arbitrary vector direction. -/
noncomputable def normalizedFireySupportVecSq (a b : ℝ) (ξ : Plane) : ℝ :=
  setSupportFunction (normalizedZonotope a b) ξ ^ 2 +
    setSupportFunction (normalizedZonotope a b) (-ξ) ^ 2

/-- The nonnegative square-root support used by the exact `p=2` halfspaces. -/
noncomputable def normalizedFireySupportVec (a b : ℝ) (ξ : Plane) : ℝ :=
  √(normalizedFireySupportVecSq a b ξ)

/-- The exact normalized `p=2` Firey body as an intersection of all halfspaces. -/
noncomputable def normalizedLpSumTwo (a b : ℝ) : Set Plane :=
  {x | ∀ ξ : Plane, inner ℝ x ξ ≤ normalizedFireySupportVec a b ξ}

/-- Coordinate formula for pairing a displayed plane vector with an arbitrary vector. -/
theorem inner_planeVector_apply (x y : ℝ) (ξ : Plane) :
    inner ℝ (planeVector x y) ξ = x * ξ 0 + y * ξ 1 := by
  rw [PiLp.inner_apply, Fin.sum_univ_two]
  simp [planeVector]
  ring

/-- The real-power convention at `p=2` is exactly the square root. -/
theorem normalizedFireySupportVec_rpow_half (a b : ℝ) (ξ : Plane) :
    normalizedFireySupportVecSq a b ξ ^ (1 / (2 : ℝ)) =
      normalizedFireySupportVec a b ξ := by
  exact (Real.sqrt_eq_rpow _).symm

/-- The vector and angular squared-support definitions agree exactly. -/
theorem normalizedFireySupportVecSq_planeDirection (a b θ : ℝ) :
    normalizedFireySupportVecSq a b (planeDirection θ) =
      normalizedFireySupportSq a b θ := rfl

/-- Expansion into the three signed generator pairings for any vector direction. -/
theorem normalizedFireySupportVecSq_eq_positiveParts (a b : ℝ) (ξ : Plane) :
    normalizedFireySupportVecSq a b ξ =
      (positivePart (inner ℝ (planeVector 1 0) ξ) +
          positivePart (inner ℝ (planeVector a b) ξ) +
          positivePart (inner ℝ (planeVector 0 1) ξ)) ^ 2 +
        (positivePart (-inner ℝ (planeVector 1 0) ξ) +
          positivePart (-inner ℝ (planeVector a b) ξ) +
          positivePart (-inner ℝ (planeVector 0 1) ξ)) ^ 2 := by
  rw [normalizedFireySupportVecSq, normalizedZonotope,
    setSupportFunction_threeSegmentZonotope,
    setSupportFunction_threeSegmentZonotope]
  simp only [threeSegmentSupport, inner_neg_right]

/-! ## A reusable two-generator ellipsoidal boundary point -/

/-- Squared support of the ellipsoid generated by two vectors. -/
noncomputable def twoGeneratorSupportSq (p q ξ : Plane) : ℝ :=
  inner ℝ p ξ ^ 2 + inner ℝ q ξ ^ 2

/-- The canonical support point of the two-generator ellipsoid at direction `n`. -/
noncomputable def twoGeneratorBoundaryPoint (p q n : Plane) : Plane :=
  (inner ℝ p n / √(twoGeneratorSupportSq p q n)) • p +
    (inner ℝ q n / √(twoGeneratorSupportSq p q n)) • q

/-- Cauchy--Schwarz in the two generator coordinates gives the global support bound. -/
theorem inner_twoGeneratorBoundaryPoint_le {p q n ξ : Plane}
    (hn : 0 < twoGeneratorSupportSq p q n) :
    inner ℝ (twoGeneratorBoundaryPoint p q n) ξ ≤
      √(twoGeneratorSupportSq p q ξ) := by
  let A := inner ℝ p n
  let B := inner ℝ q n
  let C := inner ℝ p ξ
  let D := inner ℝ q ξ
  have hroot : 0 < √(twoGeneratorSupportSq p q n) := Real.sqrt_pos.2 hn
  have hnroot : (√(twoGeneratorSupportSq p q n)) ^ 2 =
      twoGeneratorSupportSq p q n := Real.sq_sqrt hn.le
  have hξnonneg : 0 ≤ twoGeneratorSupportSq p q ξ := by
    unfold twoGeneratorSupportSq
    positivity
  have hξroot : (√(twoGeneratorSupportSq p q ξ)) ^ 2 =
      twoGeneratorSupportSq p q ξ := Real.sq_sqrt hξnonneg
  have hcauchy : (A * C + B * D) ^ 2 ≤
      (A ^ 2 + B ^ 2) * (C ^ 2 + D ^ 2) := by
    nlinarith [sq_nonneg (A * D - B * C)]
  have hdot : A * C + B * D ≤
      √(twoGeneratorSupportSq p q n) * √(twoGeneratorSupportSq p q ξ) := by
    by_cases hAC : A * C + B * D ≤ 0
    · exact hAC.trans (mul_nonneg hroot.le (Real.sqrt_nonneg _))
    · have hACpos : 0 < A * C + B * D := lt_of_not_ge hAC
      have hprod : 0 ≤
          √(twoGeneratorSupportSq p q n) * √(twoGeneratorSupportSq p q ξ) :=
        mul_nonneg hroot.le (Real.sqrt_nonneg _)
      have hprodSq :
          (√(twoGeneratorSupportSq p q n) *
              √(twoGeneratorSupportSq p q ξ)) ^ 2 =
            (A ^ 2 + B ^ 2) * (C ^ 2 + D ^ 2) := by
        rw [mul_pow, hnroot, hξroot]
        rfl
      exact (sq_le_sq₀ hACpos.le hprod).mp (by simpa [hprodSq] using hcauchy)
  rw [twoGeneratorBoundaryPoint, inner_add_left,
    real_inner_smul_left, real_inner_smul_left]
  rw [div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div]
  apply (div_le_iff₀ hroot).2
  simpa [A, B, C, D, mul_comm] using hdot

/-- At its defining normal, the ellipsoidal point attains the support value. -/
theorem inner_twoGeneratorBoundaryPoint_self {p q n : Plane}
    (hn : 0 < twoGeneratorSupportSq p q n) :
    inner ℝ (twoGeneratorBoundaryPoint p q n) n =
      √(twoGeneratorSupportSq p q n) := by
  have hroot : 0 < √(twoGeneratorSupportSq p q n) := Real.sqrt_pos.2 hn
  have hsquare : (√(twoGeneratorSupportSq p q n)) ^ 2 =
      twoGeneratorSupportSq p q n := Real.sq_sqrt hn.le
  rw [twoGeneratorBoundaryPoint, inner_add_left,
    real_inner_smul_left, real_inner_smul_left]
  rw [div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div]
  apply (div_eq_iff hroot.ne').2
  calc
    inner ℝ p n * inner ℝ p n + inner ℝ q n * inner ℝ q n =
        twoGeneratorSupportSq p q n := by
      unfold twoGeneratorSupportSq
      ring
    _ = (√(twoGeneratorSupportSq p q n)) ^ 2 := hsquare.symm
    _ = √(twoGeneratorSupportSq p q n) *
        √(twoGeneratorSupportSq p q n) := by ring

/-! ## Global domination by the full Firey support -/

/-- The full support dominates the Sector II ellipsoidal support in every direction. -/
theorem twoGeneratorSupportSq_sectorTwo_le_firey (a b : ℝ) (ξ : Plane) :
    twoGeneratorSupportSq (planeVector 1 0)
        (planeVector a b + planeVector 0 1) ξ ≤
      normalizedFireySupportVecSq a b ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  have h := three_positive_parts_sq_ge_first_tail
    (inner ℝ (planeVector 1 0) ξ)
    (inner ℝ (planeVector a b) ξ)
    (inner ℝ (planeVector 0 1) ξ)
  simpa only [twoGeneratorSupportSq, inner_add_left] using h

/-- The full support dominates the Sector III ellipsoidal support in every direction. -/
theorem twoGeneratorSupportSq_sectorThree_le_firey (a b : ℝ) (ξ : Plane) :
    twoGeneratorSupportSq (planeVector 0 1)
        (planeVector 1 0 + planeVector a b) ξ ≤
      normalizedFireySupportVecSq a b ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  have h := three_positive_parts_sq_ge_last_head
    (inner ℝ (planeVector 1 0) ξ)
    (inner ℝ (planeVector a b) ξ)
    (inner ℝ (planeVector 0 1) ξ)
  simpa only [twoGeneratorSupportSq, inner_add_left, add_comm] using h

/-- The fixed Sector I vertex. -/
noncomputable def sectorOneVertex (a b : ℝ) : Plane := planeVector (1 + a) (1 + b)

/-- The full Firey square dominates the fixed Sector I vertex pairing globally. -/
theorem sectorOneVertex_pairing_sq_le_firey (a b : ℝ) (ξ : Plane) :
    inner ℝ (sectorOneVertex a b) ξ ^ 2 ≤ normalizedFireySupportVecSq a b ξ := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  have h := three_positive_parts_sq_ge_sum
    (inner ℝ (planeVector 1 0) ξ)
    (inner ℝ (planeVector a b) ξ)
    (inner ℝ (planeVector 0 1) ξ)
  unfold sectorOneVertex
  simp only [inner_planeVector_apply, one_mul, zero_mul, zero_add, add_zero] at h ⊢
  nlinarith [h]

/-- A real number whose square is bounded by a nonnegative radicand is at most its root. -/
theorem le_sqrt_of_sq_le {x y : ℝ} (hy : 0 ≤ y) (hxy : x ^ 2 ≤ y) : x ≤ √y := by
  by_cases hx : x ≤ 0
  · exact hx.trans (Real.sqrt_nonneg y)
  · have hxpos : 0 < x := lt_of_not_ge hx
    have hsqrt : (√y) ^ 2 = y := Real.sq_sqrt hy
    exact (sq_le_sq₀ hxpos.le (Real.sqrt_nonneg y)).mp (by simpa [hsqrt] using hxy)

/-- The fixed Sector I vertex belongs to the exact halfspace body. -/
theorem sectorOneVertex_mem_normalizedLpSumTwo (a b : ℝ) :
    sectorOneVertex a b ∈ normalizedLpSumTwo a b := by
  intro ξ
  unfold normalizedFireySupportVec
  apply le_sqrt_of_sq_le
  · unfold normalizedFireySupportVecSq
    positivity
  · exact sectorOneVertex_pairing_sq_le_firey a b ξ

/-- The opposite fixed vertex also belongs to the centrally symmetric halfspace body. -/
theorem neg_sectorOneVertex_mem_normalizedLpSumTwo (a b : ℝ) :
    -sectorOneVertex a b ∈ normalizedLpSumTwo a b := by
  intro ξ
  unfold normalizedFireySupportVec
  apply le_sqrt_of_sq_le
  · unfold normalizedFireySupportVecSq
    positivity
  · rw [inner_neg_left, neg_sq]
    exact sectorOneVertex_pairing_sq_le_firey a b ξ

/-- The exact halfspace intersection is convex. -/
theorem convex_normalizedLpSumTwo (a b : ℝ) : Convex ℝ (normalizedLpSumTwo a b) := by
  rw [convex_iff_segment_subset]
  intro x hx y hy z hz
  rcases hz with ⟨r, s, hr, hs, hrs, rfl⟩
  intro ξ
  rw [inner_add_left, real_inner_smul_left, real_inner_smul_left]
  have hxξ := hx ξ
  have hyξ := hy ξ
  calc
    r * inner ℝ x ξ + s * inner ℝ y ξ ≤
        r * normalizedFireySupportVec a b ξ +
          s * normalizedFireySupportVec a b ξ :=
      add_le_add (mul_le_mul_of_nonneg_left hxξ hr)
        (mul_le_mul_of_nonneg_left hyξ hs)
    _ = normalizedFireySupportVec a b ξ := by rw [← add_mul, hrs, one_mul]

/-! ## Actual halfspace membership and supporting equality -/

/-- The Sector II ellipsoidal support point, before identifying coordinates. -/
noncomputable def sectorTwoEllipsoidPoint (a b θ : ℝ) : Plane :=
  twoGeneratorBoundaryPoint (planeVector 1 0)
    (planeVector a b + planeVector 0 1) (planeDirection θ)

/-- The Sector III ellipsoidal support point, before identifying coordinates. -/
noncomputable def sectorThreeEllipsoidPoint (a b θ : ℝ) : Plane :=
  twoGeneratorBoundaryPoint (planeVector 0 1)
    (planeVector 1 0 + planeVector a b) (planeDirection θ)

theorem twoGeneratorSupportSq_sectorTwo_direction (a b θ : ℝ) :
    twoGeneratorSupportSq (planeVector 1 0)
        (planeVector a b + planeVector 0 1) (planeDirection θ) =
      sectorTwoSq a b θ := by
  simp only [twoGeneratorSupportSq, planeDirection, inner_planeVector, inner_add_left,
    sectorTwoSq, sectorTwoU]
  ring

theorem twoGeneratorSupportSq_sectorThree_direction (a b θ : ℝ) :
    twoGeneratorSupportSq (planeVector 0 1)
        (planeVector 1 0 + planeVector a b) (planeDirection θ) =
      sectorThreeSq a b θ := by
  simp only [twoGeneratorSupportSq, planeDirection, inner_planeVector, inner_add_left,
    sectorThreeSq, sectorThreeW]
  ring

/-- Cartesian formula for the first coordinate of the Sector II canonical point. -/
theorem sectorTwoBoundaryX_eq_ellipsoid {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    sectorTwoBoundaryX a b θ =
      (cos θ + a * sectorTwoU a b θ) / sectorTwoSupport a b θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  have hroot : 0 < sectorTwoSupport a b θ := by
    exact Real.sqrt_pos.2 hpos
  have hsquare : sectorTwoSupport a b θ ^ 2 = sectorTwoSq a b θ := by
    exact Real.sq_sqrt hpos.le
  unfold sectorTwoBoundaryX supportBoundaryX sectorTwoSupportDerivative
  rw [show √(sectorTwoSq a b θ) = sectorTwoSupport a b θ by rfl]
  field_simp [hroot.ne']
  rw [hsquare]
  unfold sectorTwoSq sectorTwoBoundary sectorTwoU sectorTwoV
  calc
    ((a * cos θ + (1 + b) * sin θ) ^ 2 + cos θ ^ 2) * cos θ -
        ((a * cos θ + (1 + b) * sin θ) *
          (-a * sin θ + (1 + b) * cos θ) - cos θ * sin θ) * sin θ =
      (cos θ + a * (a * cos θ + (1 + b) * sin θ)) *
        (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = cos θ + a * (a * cos θ + (1 + b) * sin θ) := by
      rw [Real.sin_sq_add_cos_sq]
      ring

/-- Cartesian formula for the second coordinate of the Sector II canonical point. -/
theorem sectorTwoBoundaryY_eq_ellipsoid {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    sectorTwoBoundaryY a b θ =
      ((1 + b) * sectorTwoU a b θ) / sectorTwoSupport a b θ := by
  have hpos := sectorTwoSq_pos (a := a) hb θ
  have hroot : 0 < sectorTwoSupport a b θ := Real.sqrt_pos.2 hpos
  have hsquare : sectorTwoSupport a b θ ^ 2 = sectorTwoSq a b θ :=
    Real.sq_sqrt hpos.le
  unfold sectorTwoBoundaryY supportBoundaryY sectorTwoSupportDerivative
  rw [show √(sectorTwoSq a b θ) = sectorTwoSupport a b θ by rfl]
  field_simp [hroot.ne']
  rw [hsquare]
  unfold sectorTwoSq sectorTwoBoundary sectorTwoU sectorTwoV
  calc
    ((a * cos θ + (1 + b) * sin θ) ^ 2 + cos θ ^ 2) * sin θ +
        ((a * cos θ + (1 + b) * sin θ) *
          (-a * sin θ + (1 + b) * cos θ) - cos θ * sin θ) * cos θ =
      (1 + b) * (a * cos θ + (1 + b) * sin θ) *
        (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = (1 + b) * (a * cos θ + (1 + b) * sin θ) := by
      rw [Real.sin_sq_add_cos_sq]
      ring

/-- Cartesian formula for the first coordinate of the Sector III canonical point. -/
theorem sectorThreeBoundaryX_eq_ellipsoid {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    sectorThreeBoundaryX a b θ =
      ((1 + a) * sectorThreeW a b θ) / sectorThreeSupport a b θ := by
  have hpos := sectorThreeSq_pos (b := b) ha θ
  have hroot : 0 < sectorThreeSupport a b θ := Real.sqrt_pos.2 hpos
  have hsquare : sectorThreeSupport a b θ ^ 2 = sectorThreeSq a b θ :=
    Real.sq_sqrt hpos.le
  unfold sectorThreeBoundaryX supportBoundaryX sectorThreeSupportDerivative
  rw [show √(sectorThreeSq a b θ) = sectorThreeSupport a b θ by rfl]
  field_simp [hroot.ne']
  rw [hsquare]
  unfold sectorThreeSq sectorThreeBoundary sectorThreeW sectorThreeZ
  calc
    (sin θ ^ 2 + ((1 + a) * cos θ + b * sin θ) ^ 2) * cos θ -
        (sin θ * cos θ + ((1 + a) * cos θ + b * sin θ) *
          (-(1 + a) * sin θ + b * cos θ)) * sin θ =
      (1 + a) * ((1 + a) * cos θ + b * sin θ) *
        (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = (1 + a) * ((1 + a) * cos θ + b * sin θ) := by
      rw [Real.sin_sq_add_cos_sq]
      ring

/-- Cartesian formula for the second coordinate of the Sector III canonical point. -/
theorem sectorThreeBoundaryY_eq_ellipsoid {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    sectorThreeBoundaryY a b θ =
      (sin θ + b * sectorThreeW a b θ) / sectorThreeSupport a b θ := by
  have hpos := sectorThreeSq_pos (b := b) ha θ
  have hroot : 0 < sectorThreeSupport a b θ := Real.sqrt_pos.2 hpos
  have hsquare : sectorThreeSupport a b θ ^ 2 = sectorThreeSq a b θ :=
    Real.sq_sqrt hpos.le
  unfold sectorThreeBoundaryY supportBoundaryY sectorThreeSupportDerivative
  rw [show √(sectorThreeSq a b θ) = sectorThreeSupport a b θ by rfl]
  field_simp [hroot.ne']
  rw [hsquare]
  unfold sectorThreeSq sectorThreeBoundary sectorThreeW sectorThreeZ
  calc
    (sin θ ^ 2 + ((1 + a) * cos θ + b * sin θ) ^ 2) * sin θ +
        (sin θ * cos θ + ((1 + a) * cos θ + b * sin θ) *
          (-(1 + a) * sin θ + b * cos θ)) * cos θ =
      (sin θ + b * ((1 + a) * cos θ + b * sin θ)) *
        (sin θ ^ 2 + cos θ ^ 2) := by ring
    _ = sin θ + b * ((1 + a) * cos θ + b * sin θ) := by
      rw [Real.sin_sq_add_cos_sq]
      ring

/-- The ellipsoidal Sector II point is exactly the previously defined canonical arc point. -/
theorem sectorTwoEllipsoidPoint_eq_boundaryPoint {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    sectorTwoEllipsoidPoint a b θ =
      planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ) := by
  apply ext_inner_right ℝ
  intro ξ
  rw [sectorTwoEllipsoidPoint, twoGeneratorBoundaryPoint, inner_add_left,
    real_inner_smul_left, real_inner_smul_left,
    twoGeneratorSupportSq_sectorTwo_direction,
    sectorTwoBoundaryX_eq_ellipsoid hb, sectorTwoBoundaryY_eq_ellipsoid hb]
  simp only [planeDirection, inner_planeVector, inner_add_left]
  rw [inner_planeVector_apply, inner_planeVector_apply,
    inner_planeVector_apply, inner_planeVector_apply]
  unfold sectorTwoSupport sectorTwoU
  ring

/-- The ellipsoidal Sector III point is exactly the previously defined canonical arc point. -/
theorem sectorThreeEllipsoidPoint_eq_boundaryPoint {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    sectorThreeEllipsoidPoint a b θ =
      planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ) := by
  apply ext_inner_right ℝ
  intro ξ
  rw [sectorThreeEllipsoidPoint, twoGeneratorBoundaryPoint, inner_add_left,
    real_inner_smul_left, real_inner_smul_left,
    twoGeneratorSupportSq_sectorThree_direction,
    sectorThreeBoundaryX_eq_ellipsoid ha, sectorThreeBoundaryY_eq_ellipsoid ha]
  simp only [planeDirection, inner_planeVector, inner_add_left]
  rw [inner_planeVector_apply, inner_planeVector_apply,
    inner_planeVector_apply, inner_planeVector_apply]
  unfold sectorThreeSupport sectorThreeW
  ring

/-- Every Sector II ellipsoidal point belongs to the exact halfspace body. -/
theorem sectorTwoEllipsoidPoint_mem_normalizedLpSumTwo {a b θ : ℝ} (hb : 0 < b) :
    sectorTwoEllipsoidPoint a b θ ∈ normalizedLpSumTwo a b := by
  intro ξ
  have hn : 0 < twoGeneratorSupportSq (planeVector 1 0)
      (planeVector a b + planeVector 0 1) (planeDirection θ) := by
    rw [twoGeneratorSupportSq_sectorTwo_direction]
    exact sectorTwoSq_pos hb θ
  calc
    inner ℝ (sectorTwoEllipsoidPoint a b θ) ξ ≤
        √(twoGeneratorSupportSq (planeVector 1 0)
          (planeVector a b + planeVector 0 1) ξ) :=
      inner_twoGeneratorBoundaryPoint_le hn
    _ ≤ √(normalizedFireySupportVecSq a b ξ) :=
      Real.sqrt_le_sqrt (twoGeneratorSupportSq_sectorTwo_le_firey a b ξ)
    _ = normalizedFireySupportVec a b ξ := rfl

/-- Every Sector III ellipsoidal point belongs to the exact halfspace body. -/
theorem sectorThreeEllipsoidPoint_mem_normalizedLpSumTwo {a b θ : ℝ} (ha : 0 < a) :
    sectorThreeEllipsoidPoint a b θ ∈ normalizedLpSumTwo a b := by
  intro ξ
  have hn : 0 < twoGeneratorSupportSq (planeVector 0 1)
      (planeVector 1 0 + planeVector a b) (planeDirection θ) := by
    rw [twoGeneratorSupportSq_sectorThree_direction]
    exact sectorThreeSq_pos ha θ
  calc
    inner ℝ (sectorThreeEllipsoidPoint a b θ) ξ ≤
        √(twoGeneratorSupportSq (planeVector 0 1)
          (planeVector 1 0 + planeVector a b) ξ) :=
      inner_twoGeneratorBoundaryPoint_le hn
    _ ≤ √(normalizedFireySupportVecSq a b ξ) :=
      Real.sqrt_le_sqrt (twoGeneratorSupportSq_sectorThree_le_firey a b ξ)
    _ = normalizedFireySupportVec a b ξ := rfl

/-- On Sector II, the member attains the exact full Firey support. -/
theorem sectorTwoEllipsoidPoint_supporting {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    inner ℝ (sectorTwoEllipsoidPoint a b θ) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  have hn : 0 < twoGeneratorSupportSq (planeVector 1 0)
      (planeVector a b + planeVector 0 1) (planeDirection θ) := by
    rw [twoGeneratorSupportSq_sectorTwo_direction]
    exact sectorTwoSq_pos hb θ
  rw [sectorTwoEllipsoidPoint, inner_twoGeneratorBoundaryPoint_self hn,
    twoGeneratorSupportSq_sectorTwo_direction, normalizedFireySupportVec,
    normalizedFireySupportVecSq_planeDirection,
    normalizedFireySupportSq_eq_sectorTwoSq_on_sector ha hb hθ]

/-- On Sector III, the member attains the exact full Firey support. -/
theorem sectorThreeEllipsoidPoint_supporting {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    inner ℝ (sectorThreeEllipsoidPoint a b θ) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  have hn : 0 < twoGeneratorSupportSq (planeVector 0 1)
      (planeVector 1 0 + planeVector a b) (planeDirection θ) := by
    rw [twoGeneratorSupportSq_sectorThree_direction]
    exact sectorThreeSq_pos ha θ
  rw [sectorThreeEllipsoidPoint, inner_twoGeneratorBoundaryPoint_self hn,
    twoGeneratorSupportSq_sectorThree_direction, normalizedFireySupportVec,
    normalizedFireySupportVecSq_planeDirection,
    normalizedFireySupportSq_eq_sectorThreeSq_on_sector ha hb hθ]

/-- The previously integrated Sector II canonical arc lies in the exact halfspace body. -/
theorem sectorTwoBoundaryPoint_mem_normalizedLpSumTwo {a b θ : ℝ} (hb : 0 < b) :
    planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ) ∈
      normalizedLpSumTwo a b := by
  rw [← sectorTwoEllipsoidPoint_eq_boundaryPoint hb]
  exact sectorTwoEllipsoidPoint_mem_normalizedLpSumTwo hb

/-- The previously integrated Sector III canonical arc lies in the exact halfspace body. -/
theorem sectorThreeBoundaryPoint_mem_normalizedLpSumTwo {a b θ : ℝ} (ha : 0 < a) :
    planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ) ∈
      normalizedLpSumTwo a b := by
  rw [← sectorThreeEllipsoidPoint_eq_boundaryPoint ha]
  exact sectorThreeEllipsoidPoint_mem_normalizedLpSumTwo ha

/-- On Sector II, the actual canonical arc point attains its defining halfspace. -/
theorem sectorTwoBoundaryPoint_supporting {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    inner ℝ (planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ))
        (planeDirection θ) = normalizedFireySupportVec a b (planeDirection θ) := by
  rw [← sectorTwoEllipsoidPoint_eq_boundaryPoint hb]
  exact sectorTwoEllipsoidPoint_supporting ha hb hθ

/-- On Sector III, the actual canonical arc point attains its defining halfspace. -/
theorem sectorThreeBoundaryPoint_supporting {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    inner ℝ (planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ))
        (planeDirection θ) = normalizedFireySupportVec a b (planeDirection θ) := by
  rw [← sectorThreeEllipsoidPoint_eq_boundaryPoint ha]
  exact sectorThreeEllipsoidPoint_supporting ha hb hθ

/-- The literal support function of the halfspace body equals the prescribed support on Sector II. -/
theorem setSupportFunction_normalizedLpSumTwo_sectorTwo {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2) (π / 2 + arctan (b / a))) :
    setSupportFunction (normalizedLpSumTwo a b) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  let x := planeVector (sectorTwoBoundaryX a b θ) (sectorTwoBoundaryY a b θ)
  have hx : x ∈ normalizedLpSumTwo a b :=
    sectorTwoBoundaryPoint_mem_normalizedLpSumTwo hb
  have hattain : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) :=
    sectorTwoBoundaryPoint_supporting ha hb hθ
  have hgreatest : IsGreatest
      ((fun y : Plane ↦ inner ℝ y (planeDirection θ)) '' normalizedLpSumTwo a b)
      (normalizedFireySupportVec a b (planeDirection θ)) := by
    constructor
    · exact ⟨x, hx, hattain⟩
    · rintro _ ⟨y, hy, rfl⟩
      exact hy (planeDirection θ)
  exact hgreatest.isLUB.ciSup_set_eq ⟨x, hx⟩

/-- The literal support function of the halfspace body equals the prescribed support on Sector III. -/
theorem setSupportFunction_normalizedLpSumTwo_sectorThree {a b θ : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Icc (π / 2 + arctan (b / a)) π) :
    setSupportFunction (normalizedLpSumTwo a b) (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) := by
  let x := planeVector (sectorThreeBoundaryX a b θ) (sectorThreeBoundaryY a b θ)
  have hx : x ∈ normalizedLpSumTwo a b :=
    sectorThreeBoundaryPoint_mem_normalizedLpSumTwo ha
  have hattain : inner ℝ x (planeDirection θ) =
      normalizedFireySupportVec a b (planeDirection θ) :=
    sectorThreeBoundaryPoint_supporting ha hb hθ
  have hgreatest : IsGreatest
      ((fun y : Plane ↦ inner ℝ y (planeDirection θ)) '' normalizedLpSumTwo a b)
      (normalizedFireySupportVec a b (planeDirection θ)) := by
    constructor
    · exact ⟨x, hx, hattain⟩
    · rintro _ ⟨y, hy, rfl⟩
      exact hy (planeDirection θ)
  exact hgreatest.isLUB.ciSup_set_eq ⟨x, hx⟩

/-! ## The three literal jump segments -/

/-- The jump from the fixed Sector I vertex to the Sector II arc. -/
noncomputable def sectorOneTwoJump (a b : ℝ) : Set Plane :=
  segment ℝ (sectorOneVertex a b)
    (planeVector (sectorTwoBoundaryX a b (π / 2))
      (sectorTwoBoundaryY a b (π / 2)))

/-- The jump between the two curved arcs at the middle generator sign change. -/
noncomputable def sectorTwoThreeJump (a b : ℝ) : Set Plane :=
  let φ := arctan (b / a)
  segment ℝ (planeVector (sectorTwoBoundaryX a b (π / 2 + φ))
      (sectorTwoBoundaryY a b (π / 2 + φ)))
    (planeVector (sectorThreeBoundaryX a b (π / 2 + φ))
      (sectorThreeBoundaryY a b (π / 2 + φ)))

/-- The closing upper-half jump from Sector III to the opposite fixed vertex. -/
noncomputable def sectorThreeOneJump (a b : ℝ) : Set Plane :=
  segment ℝ (planeVector (sectorThreeBoundaryX a b π) (sectorThreeBoundaryY a b π))
    (-sectorOneVertex a b)

/-- The first canonical jump segment lies in the exact halfspace body. -/
theorem sectorOneTwoJump_subset_normalizedLpSumTwo {a b : ℝ} (hb : 0 < b) :
    sectorOneTwoJump a b ⊆ normalizedLpSumTwo a b := by
  unfold sectorOneTwoJump
  apply (convex_normalizedLpSumTwo a b).segment_subset
  · exact sectorOneVertex_mem_normalizedLpSumTwo a b
  · exact sectorTwoBoundaryPoint_mem_normalizedLpSumTwo hb

/-- The middle canonical jump segment lies in the exact halfspace body. -/
theorem sectorTwoThreeJump_subset_normalizedLpSumTwo {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    sectorTwoThreeJump a b ⊆ normalizedLpSumTwo a b := by
  unfold sectorTwoThreeJump
  apply (convex_normalizedLpSumTwo a b).segment_subset
  · exact sectorTwoBoundaryPoint_mem_normalizedLpSumTwo hb
  · exact sectorThreeBoundaryPoint_mem_normalizedLpSumTwo ha

/-- The closing upper-half canonical jump lies in the exact halfspace body. -/
theorem sectorThreeOneJump_subset_normalizedLpSumTwo {a b : ℝ} (ha : 0 < a) :
    sectorThreeOneJump a b ⊆ normalizedLpSumTwo a b := by
  unfold sectorThreeOneJump
  apply (convex_normalizedLpSumTwo a b).segment_subset
  · exact sectorThreeBoundaryPoint_mem_normalizedLpSumTwo ha
  · exact neg_sectorOneVertex_mem_normalizedLpSumTwo a b

#print axioms three_positive_parts_sq_ge_first_tail
#print axioms three_positive_parts_sq_ge_last_head
#print axioms three_positive_parts_sq_ge_sum
#print axioms normalizedFireySupportVec_rpow_half
#print axioms normalizedFireySupportVecSq_eq_positiveParts
#print axioms inner_twoGeneratorBoundaryPoint_le
#print axioms inner_twoGeneratorBoundaryPoint_self
#print axioms twoGeneratorSupportSq_sectorTwo_le_firey
#print axioms twoGeneratorSupportSq_sectorThree_le_firey
#print axioms sectorOneVertex_mem_normalizedLpSumTwo
#print axioms convex_normalizedLpSumTwo
#print axioms sectorTwoEllipsoidPoint_eq_boundaryPoint
#print axioms sectorThreeEllipsoidPoint_eq_boundaryPoint
#print axioms sectorTwoEllipsoidPoint_mem_normalizedLpSumTwo
#print axioms sectorThreeEllipsoidPoint_mem_normalizedLpSumTwo
#print axioms sectorTwoEllipsoidPoint_supporting
#print axioms sectorThreeEllipsoidPoint_supporting
#print axioms sectorTwoBoundaryPoint_mem_normalizedLpSumTwo
#print axioms sectorThreeBoundaryPoint_mem_normalizedLpSumTwo
#print axioms sectorTwoBoundaryPoint_supporting
#print axioms sectorThreeBoundaryPoint_supporting
#print axioms setSupportFunction_normalizedLpSumTwo_sectorTwo
#print axioms setSupportFunction_normalizedLpSumTwo_sectorThree
#print axioms sectorOneTwoJump_subset_normalizedLpSumTwo
#print axioms sectorTwoThreeJump_subset_normalizedLpSumTwo
#print axioms sectorThreeOneJump_subset_normalizedLpSumTwo

end L2Hexagon
