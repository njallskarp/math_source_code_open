import L2Hexagon.ExposedFaces

/-!
# The middle exposed transition face

Put `n=(-b,a)`, `v=(a,b)`, and `R=a²+b²`.  The generator `(a,b)` has zero
pairing with `n`, so the middle sign change occurs at this normal.  The exact
claim proved below is

`{x ∈ normalizedLpSumTwo a b | inner x n = sqrt R}
  = sectorTwoThreeJump a b`.

The reverse inclusion is algebraic.  If `T=inner x v`, perturb the normal by
`n+t v` and `n-t v`.  In the two adjacent sign chambers the squared supports
are exactly

`(sqrt R + a sqrt R t)² + t² R (1+b)²`,
`(sqrt R + b sqrt R t)² + t² R (1+a)²`.

Choosing `t` explicitly small compared with an alleged excess proves
`-b sqrt R ≤ T ≤ a sqrt R`.  No directional limit or unformalized support
derivative is used.
-/

open Real Set

namespace L2Hexagon

noncomputable def middleRadiusSq (a b : ℝ) : ℝ := a ^ 2 + b ^ 2

noncomputable def middleRadius (a b : ℝ) : ℝ := √(middleRadiusSq a b)

noncomputable def middleNormal (a b : ℝ) : Plane := planeVector (-b) a

noncomputable def middleTangent (a b : ℝ) : Plane := planeVector a b

noncomputable def middlePlusDirection (a b t : ℝ) : Plane :=
  planeVector (-b + a * t) (a + b * t)

noncomputable def middleMinusDirection (a b t : ℝ) : Plane :=
  planeVector (-b - a * t) (a - b * t)

theorem middleRadiusSq_pos {a b : ℝ} (ha : 0 < a) :
    0 < middleRadiusSq a b := by
  unfold middleRadiusSq
  nlinarith [sq_pos_of_pos ha]

theorem middleRadius_pos {a b : ℝ} (ha : 0 < a) :
    0 < middleRadius a b := Real.sqrt_pos.2 (middleRadiusSq_pos ha)

theorem middleRadius_sq {a b : ℝ} :
    middleRadius a b ^ 2 = middleRadiusSq a b := by
  exact Real.sq_sqrt (by unfold middleRadiusSq; positivity)

/-- Exact value of the source support at the unnormalized middle normal. -/
theorem normalizedFireySupportVec_middleNormal {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    normalizedFireySupportVec a b (middleNormal a b) = middleRadius a b := by
  have hsq : normalizedFireySupportVecSq a b (middleNormal a b) =
      middleRadiusSq a b := by
    rw [normalizedFireySupportVecSq_eq_positiveParts]
    simp only [middleNormal, inner_planeVector]
    have hmid : a * -b + b * a = 0 := by ring
    rw [hmid]
    unfold positivePart middleRadiusSq
    norm_num
    rw [max_eq_right (neg_nonpos.mpr hb.le), max_eq_left ha.le,
      max_eq_left hb.le, max_eq_right (neg_nonpos.mpr ha.le)]
    ring
  rw [normalizedFireySupportVec, hsq]
  rfl

theorem inner_middlePlusDirection (a b t : ℝ) (x : Plane) :
    inner ℝ x (middlePlusDirection a b t) =
      inner ℝ x (middleNormal a b) + t * inner ℝ x (middleTangent a b) := by
  rw [PiLp.inner_apply, PiLp.inner_apply, PiLp.inner_apply, Fin.sum_univ_two,
    Fin.sum_univ_two, Fin.sum_univ_two]
  simp [middlePlusDirection, middleNormal, middleTangent, planeVector]
  ring

theorem inner_middleMinusDirection (a b t : ℝ) (x : Plane) :
    inner ℝ x (middleMinusDirection a b t) =
      inner ℝ x (middleNormal a b) - t * inner ℝ x (middleTangent a b) := by
  rw [PiLp.inner_apply, PiLp.inner_apply, PiLp.inner_apply, Fin.sum_univ_two,
    Fin.sum_univ_two, Fin.sum_univ_two]
  simp [middleMinusDirection, middleNormal, middleTangent, planeVector]
  ring

/-- Exact squared support in the Sector II chamber adjacent to the middle normal. -/
theorem normalizedFireySupportVecSq_middlePlus {a b t : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ht : 0 ≤ t) (hat : a * t ≤ b) :
    normalizedFireySupportVecSq a b (middlePlusDirection a b t) =
      (-b + a * t) ^ 2 +
        (a + t * (middleRadiusSq a b + b)) ^ 2 := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  simp only [middlePlusDirection, inner_planeVector]
  have hx : -b + a * t ≤ 0 := by linarith
  have hmid : 0 ≤ t * middleRadiusSq a b :=
    mul_nonneg ht (le_of_lt (middleRadiusSq_pos ha))
  have hz : 0 ≤ a + b * t := by positivity
  have hmidEq : a * (-b + a * t) + b * (a + b * t) =
      t * middleRadiusSq a b := by unfold middleRadiusSq; ring
  rw [hmidEq]
  unfold positivePart
  norm_num
  rw [max_eq_right hx, max_eq_left hmid, max_eq_left hz]
  have hnegx : 0 ≤ -(a * t) + b := by linarith
  have hnegmid : -(t * middleRadiusSq a b) ≤ 0 := neg_nonpos.mpr hmid
  have hnegz : -(b * t) + -a ≤ 0 := by
    nlinarith [mul_nonneg hb.le ht]
  rw [max_eq_left hnegx, max_eq_right hnegmid, max_eq_right hnegz]
  unfold middleRadiusSq
  ring

/-- Exact squared support in the Sector III chamber adjacent to the middle normal. -/
theorem normalizedFireySupportVecSq_middleMinus {a b t : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ht : 0 ≤ t) (hbt : b * t ≤ a) :
    normalizedFireySupportVecSq a b (middleMinusDirection a b t) =
      (a - b * t) ^ 2 +
        (b + t * (middleRadiusSq a b + a)) ^ 2 := by
  rw [normalizedFireySupportVecSq_eq_positiveParts]
  simp only [middleMinusDirection, inner_planeVector]
  have hx : -b - a * t ≤ 0 := by
    nlinarith [mul_nonneg ha.le ht]
  have hmid : a * (-b - a * t) + b * (a - b * t) =
      -(t * middleRadiusSq a b) := by unfold middleRadiusSq; ring
  have hmidNonpos : -(t * middleRadiusSq a b) ≤ 0 := by
    exact neg_nonpos.mpr (mul_nonneg ht (le_of_lt (middleRadiusSq_pos ha)))
  have hz : 0 ≤ a - b * t := by linarith
  rw [hmid]
  unfold positivePart
  norm_num
  rw [max_eq_right hx, max_eq_right hmidNonpos, max_eq_left hz]
  have hnegx : 0 ≤ a * t + b := by positivity
  have hnegmid : 0 ≤ t * middleRadiusSq a b :=
    mul_nonneg ht (le_of_lt (middleRadiusSq_pos ha))
  have hnegz : b * t - a ≤ 0 := by linarith
  rw [max_eq_left hnegx, max_eq_left hnegmid, max_eq_right hnegz]
  unfold middleRadiusSq
  ring

/-- The plus-chamber quadratic is its tangent linearization plus an exact
nonnegative second-order surplus. -/
theorem normalizedFireySupportVecSq_middlePlus_expansion {a b t : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ht : 0 ≤ t) (hat : a * t ≤ b) :
    normalizedFireySupportVecSq a b (middlePlusDirection a b t) =
      (middleRadius a b + a * middleRadius a b * t) ^ 2 +
        t ^ 2 * middleRadiusSq a b * (1 + b) ^ 2 := by
  rw [normalizedFireySupportVecSq_middlePlus ha hb ht hat]
  have hs := middleRadius_sq (a := a) (b := b)
  unfold middleRadiusSq at hs ⊢
  linear_combination -(1 + a * t) ^ 2 * hs

/-- The minus-chamber quadratic has the analogous exact surplus. -/
theorem normalizedFireySupportVecSq_middleMinus_expansion {a b t : ℝ}
    (ha : 0 < a) (hb : 0 < b) (ht : 0 ≤ t) (hbt : b * t ≤ a) :
    normalizedFireySupportVecSq a b (middleMinusDirection a b t) =
      (middleRadius a b + b * middleRadius a b * t) ^ 2 +
        t ^ 2 * middleRadiusSq a b * (1 + a) ^ 2 := by
  rw [normalizedFireySupportVecSq_middleMinus ha hb ht hbt]
  have hs := middleRadius_sq (a := a) (b := b)
  unfold middleRadiusSq at hs ⊢
  linear_combination -(1 + b * t) ^ 2 * hs

/-- Abstract square contradiction used for both tangent-coordinate bounds. -/
theorem not_le_sqrt_tangent_excess {s q C t δ : ℝ}
    (hs : 0 < s) (hq : 0 ≤ q) (hC : 0 ≤ C) (ht : 0 < t) (hδ : 0 < δ)
    (htC : t * C < s * δ) :
    ¬ (s + q * s * t + t * δ ≤
        √((s + q * s * t) ^ 2 + t ^ 2 * C)) := by
  intro hle
  have hP : s ≤ s + q * s * t := by
    nlinarith [mul_nonneg hq (mul_nonneg hs.le ht.le)]
  have hleft : 0 < s + q * s * t + t * δ := by positivity
  have hrad : 0 ≤ (s + q * s * t) ^ 2 + t ^ 2 * C := by positivity
  have hsquare := (sq_le_sq₀ hleft.le (Real.sqrt_nonneg _)).2 hle
  rw [Real.sq_sqrt hrad] at hsquare
  have hsδ : s * δ ≤ (s + q * s * t) * δ :=
    mul_le_mul_of_nonneg_right hP hδ.le
  have hfactor : t * C <
      2 * (s + q * s * t) * δ + t * δ ^ 2 := by
    nlinarith [mul_nonneg ht.le (sq_nonneg δ)]
  have hmul := mul_lt_mul_of_pos_left hfactor ht
  nlinarith

/-- The middle supporting line bounds the tangent coordinate above by the
Sector II one-sided endpoint value. -/
theorem inner_middleTangent_le_of_middle_support {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) {x : Plane}
    (hx : x ∈ normalizedLpSumTwo a b)
    (hnormal : inner ℝ x (middleNormal a b) = middleRadius a b) :
    inner ℝ x (middleTangent a b) ≤ a * middleRadius a b := by
  by_contra hnot
  let δ := inner ℝ x (middleTangent a b) - a * middleRadius a b
  have hδ : 0 < δ := sub_pos.2 (lt_of_not_ge hnot)
  let C := middleRadiusSq a b * (1 + b) ^ 2
  have hC : 0 ≤ C := by unfold C middleRadiusSq; positivity
  let t := min (b / (2 * a))
    (middleRadius a b * δ / (C + 1))
  have hs : 0 < middleRadius a b := middleRadius_pos ha
  have hsign : 0 < b / (2 * a) := div_pos hb (by positivity)
  have hden : 0 < C + 1 := by positivity
  have hscale : 0 < middleRadius a b * δ / (C + 1) :=
    div_pos (mul_pos hs hδ) hden
  have ht : 0 < t := lt_min hsign hscale
  have ht_sign : t ≤ b / (2 * a) := min_le_left _ _
  have ht_scale : t ≤ middleRadius a b * δ / (C + 1) := min_le_right _ _
  have hat_half : a * t ≤ b / 2 := by
    have hmul := mul_le_mul_of_nonneg_left ht_sign ha.le
    field_simp [ha.ne'] at hmul ⊢
    nlinarith
  have hat : a * t ≤ b := by linarith
  have htden : t * (C + 1) ≤ middleRadius a b * δ :=
    (le_div_iff₀ hden).mp ht_scale
  have htC : t * C < middleRadius a b * δ := by nlinarith
  have hhalf := hx (middlePlusDirection a b t)
  rw [normalizedFireySupportVec,
    normalizedFireySupportVecSq_middlePlus_expansion ha hb ht.le hat] at hhalf
  have htangent : inner ℝ x (middleTangent a b) =
      a * middleRadius a b + δ := by unfold δ; ring
  have hhalf' :
      middleRadius a b + a * middleRadius a b * t + t * δ ≤
        √((middleRadius a b + a * middleRadius a b * t) ^ 2 +
          t ^ 2 * C) := by
    calc
      middleRadius a b + a * middleRadius a b * t + t * δ =
          inner ℝ x (middlePlusDirection a b t) := by
            rw [inner_middlePlusDirection, hnormal, htangent]
            ring
      _ ≤ √((middleRadius a b + a * middleRadius a b * t) ^ 2 +
          t ^ 2 * C) := by
            convert hhalf using 1 <;> simp only [C] <;> ring
  have hcontra := not_le_sqrt_tangent_excess hs ha.le hC ht hδ htC
  exact hcontra hhalf'

/-- The corresponding lower tangent-coordinate bound comes from the Sector
III chamber. -/
theorem neg_b_mul_middleRadius_le_inner_middleTangent_of_middle_support
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) {x : Plane}
    (hx : x ∈ normalizedLpSumTwo a b)
    (hnormal : inner ℝ x (middleNormal a b) = middleRadius a b) :
    -(b * middleRadius a b) ≤ inner ℝ x (middleTangent a b) := by
  by_contra hnot
  let δ := -(b * middleRadius a b) - inner ℝ x (middleTangent a b)
  have hδ : 0 < δ := sub_pos.2 (lt_of_not_ge hnot)
  let C := middleRadiusSq a b * (1 + a) ^ 2
  have hC : 0 ≤ C := by unfold C middleRadiusSq; positivity
  let t := min (a / (2 * b))
    (middleRadius a b * δ / (C + 1))
  have hs : 0 < middleRadius a b := middleRadius_pos ha
  have hsign : 0 < a / (2 * b) := div_pos ha (by positivity)
  have hden : 0 < C + 1 := by positivity
  have hscale : 0 < middleRadius a b * δ / (C + 1) :=
    div_pos (mul_pos hs hδ) hden
  have ht : 0 < t := lt_min hsign hscale
  have ht_sign : t ≤ a / (2 * b) := min_le_left _ _
  have ht_scale : t ≤ middleRadius a b * δ / (C + 1) := min_le_right _ _
  have hbt_half : b * t ≤ a / 2 := by
    have hmul := mul_le_mul_of_nonneg_left ht_sign hb.le
    field_simp [hb.ne'] at hmul ⊢
    nlinarith
  have hbt : b * t ≤ a := by linarith
  have htden : t * (C + 1) ≤ middleRadius a b * δ :=
    (le_div_iff₀ hden).mp ht_scale
  have htC : t * C < middleRadius a b * δ := by nlinarith
  have hhalf := hx (middleMinusDirection a b t)
  rw [normalizedFireySupportVec,
    normalizedFireySupportVecSq_middleMinus_expansion ha hb ht.le hbt] at hhalf
  have htangent : inner ℝ x (middleTangent a b) =
      -(b * middleRadius a b) - δ := by unfold δ; ring
  have hhalf' :
      middleRadius a b + b * middleRadius a b * t + t * δ ≤
        √((middleRadius a b + b * middleRadius a b * t) ^ 2 +
          t ^ 2 * C) := by
    calc
      middleRadius a b + b * middleRadius a b * t + t * δ =
          inner ℝ x (middleMinusDirection a b t) := by
            rw [inner_middleMinusDirection, hnormal, htangent]
            ring
      _ ≤ √((middleRadius a b + b * middleRadius a b * t) ^ 2 +
          t ^ 2 * C) := by
            convert hhalf using 1 <;> simp only [C] <;> ring
  have hcontra := not_le_sqrt_tangent_excess hs hb.le hC ht hδ htC
  exact hcontra hhalf'

/-! ## Canonical endpoint pairings -/

noncomputable def middleSectorTwoEndpoint (a b : ℝ) : Plane :=
  let φ := arctan (b / a)
  planeVector (sectorTwoBoundaryX a b (π / 2 + φ))
    (sectorTwoBoundaryY a b (π / 2 + φ))

noncomputable def middleSectorThreeEndpoint (a b : ℝ) : Plane :=
  let φ := arctan (b / a)
  planeVector (sectorThreeBoundaryX a b (π / 2 + φ))
    (sectorThreeBoundaryY a b (π / 2 + φ))

theorem sqrt_one_add_div_sq_eq_middleRadius_div {a b : ℝ} (ha : 0 < a) :
    √(1 + (b / a) ^ 2) = middleRadius a b / a := by
  apply (sq_eq_sq₀ (Real.sqrt_nonneg _)
    (div_nonneg (middleRadius_pos ha).le ha.le)).mp
  rw [Real.sq_sqrt (by positivity)]
  have hs := middleRadius_sq (a := a) (b := b)
  unfold middleRadiusSq at hs
  field_simp [ha.ne']
  nlinarith

theorem middleRadius_mul_cos_generatorAngle {a b : ℝ} (ha : 0 < a) :
    middleRadius a b * cos (arctan (b / a)) = a := by
  rw [Real.cos_arctan, sqrt_one_add_div_sq_eq_middleRadius_div ha]
  field_simp [(middleRadius_pos ha).ne', ha.ne']

theorem middleRadius_mul_sin_generatorAngle {a b : ℝ} (ha : 0 < a) :
    middleRadius a b * sin (arctan (b / a)) = b := by
  rw [Real.sin_arctan, sqrt_one_add_div_sq_eq_middleRadius_div ha]
  field_simp [(middleRadius_pos ha).ne', ha.ne']

theorem middleRadius_mul_cos_middleAngle {a b : ℝ} (ha : 0 < a) :
    middleRadius a b * cos (π / 2 + arctan (b / a)) = -b := by
  rw [show π / 2 + arctan (b / a) = arctan (b / a) + π / 2 by ring,
    Real.cos_add_pi_div_two]
  calc
    middleRadius a b * -sin (arctan (b / a)) =
        -(middleRadius a b * sin (arctan (b / a))) := by ring
    _ = -b := by rw [middleRadius_mul_sin_generatorAngle ha]

theorem middleRadius_mul_sin_middleAngle {a b : ℝ} (ha : 0 < a) :
    middleRadius a b * sin (π / 2 + arctan (b / a)) = a := by
  rw [show π / 2 + arctan (b / a) = arctan (b / a) + π / 2 by ring,
    Real.sin_add_pi_div_two]
  exact middleRadius_mul_cos_generatorAngle ha

theorem middleSectorTwoEndpoint_normal_pairing {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    inner ℝ (middleSectorTwoEndpoint a b) (middleNormal a b) =
      middleRadius a b := by
  let θ := π / 2 + arctan (b / a)
  have hpair := supportBoundary_normal_pairing
    (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ
  change sectorTwoBoundaryX a b θ * cos θ +
    sectorTwoBoundaryY a b θ * sin θ = sectorTwoSupport a b θ at hpair
  have hsupport : sectorTwoSupport a b θ = 1 := by
    simpa [θ] using sectorTwoSupport_generator_boundary (b := b) ha
  rw [hsupport] at hpair
  have hcos : middleRadius a b * cos θ = -b := by
    simpa [θ] using middleRadius_mul_cos_middleAngle (b := b) ha
  have hsin : middleRadius a b * sin θ = a := by
    simpa [θ] using middleRadius_mul_sin_middleAngle (b := b) ha
  simp only [middleSectorTwoEndpoint, middleNormal, inner_planeVector]
  change sectorTwoBoundaryX a b θ * -b +
      sectorTwoBoundaryY a b θ * a = middleRadius a b
  calc
    sectorTwoBoundaryX a b θ * -b + sectorTwoBoundaryY a b θ * a =
        middleRadius a b *
          (sectorTwoBoundaryX a b θ * cos θ +
            sectorTwoBoundaryY a b θ * sin θ) := by
              linear_combination
                -sectorTwoBoundaryX a b θ * hcos -
                  sectorTwoBoundaryY a b θ * hsin
    _ = middleRadius a b := by rw [hpair]; ring

theorem middleSectorThreeEndpoint_normal_pairing {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    inner ℝ (middleSectorThreeEndpoint a b) (middleNormal a b) =
      middleRadius a b := by
  let θ := π / 2 + arctan (b / a)
  have hpair := supportBoundary_normal_pairing
    (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ
  change sectorThreeBoundaryX a b θ * cos θ +
    sectorThreeBoundaryY a b θ * sin θ = sectorThreeSupport a b θ at hpair
  have hsupport : sectorThreeSupport a b θ = 1 := by
    simpa [θ] using sectorThreeSupport_generator_boundary ha hb
  rw [hsupport] at hpair
  have hcos : middleRadius a b * cos θ = -b := by
    simpa [θ] using middleRadius_mul_cos_middleAngle (b := b) ha
  have hsin : middleRadius a b * sin θ = a := by
    simpa [θ] using middleRadius_mul_sin_middleAngle (b := b) ha
  simp only [middleSectorThreeEndpoint, middleNormal, inner_planeVector]
  change sectorThreeBoundaryX a b θ * -b +
      sectorThreeBoundaryY a b θ * a = middleRadius a b
  calc
    sectorThreeBoundaryX a b θ * -b + sectorThreeBoundaryY a b θ * a =
        middleRadius a b *
          (sectorThreeBoundaryX a b θ * cos θ +
            sectorThreeBoundaryY a b θ * sin θ) := by
              linear_combination
                -sectorThreeBoundaryX a b θ * hcos -
                  sectorThreeBoundaryY a b θ * hsin
    _ = middleRadius a b := by rw [hpair]; ring

theorem middleSectorTwoEndpoint_tangent_pairing {a b : ℝ}
    (ha : 0 < a) :
    inner ℝ (middleSectorTwoEndpoint a b) (middleTangent a b) =
      a * middleRadius a b := by
  let θ := π / 2 + arctan (b / a)
  have hpair := supportBoundary_tangent_pairing
    (sectorTwoSupport a b) (sectorTwoSupportDerivative a b) θ
  change -sectorTwoBoundaryX a b θ * sin θ +
    sectorTwoBoundaryY a b θ * cos θ =
      sectorTwoSupportDerivative a b θ at hpair
  have hderiv : sectorTwoSupportDerivative a b θ = -a := by
    simpa [θ] using sectorTwoSupportDerivative_generator_boundary (b := b) ha
  rw [hderiv] at hpair
  have hcos : middleRadius a b * cos θ = -b := by
    simpa [θ] using middleRadius_mul_cos_middleAngle (b := b) ha
  have hsin : middleRadius a b * sin θ = a := by
    simpa [θ] using middleRadius_mul_sin_middleAngle (b := b) ha
  simp only [middleSectorTwoEndpoint, middleTangent, inner_planeVector]
  change sectorTwoBoundaryX a b θ * a +
      sectorTwoBoundaryY a b θ * b = a * middleRadius a b
  calc
    sectorTwoBoundaryX a b θ * a + sectorTwoBoundaryY a b θ * b =
        -middleRadius a b *
          (-sectorTwoBoundaryX a b θ * sin θ +
            sectorTwoBoundaryY a b θ * cos θ) := by
              linear_combination
                -sectorTwoBoundaryX a b θ * hsin +
                  sectorTwoBoundaryY a b θ * hcos
    _ = a * middleRadius a b := by rw [hpair]; ring

theorem middleSectorThreeEndpoint_tangent_pairing {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    inner ℝ (middleSectorThreeEndpoint a b) (middleTangent a b) =
      -(b * middleRadius a b) := by
  let θ := π / 2 + arctan (b / a)
  have hpair := supportBoundary_tangent_pairing
    (sectorThreeSupport a b) (sectorThreeSupportDerivative a b) θ
  change -sectorThreeBoundaryX a b θ * sin θ +
    sectorThreeBoundaryY a b θ * cos θ =
      sectorThreeSupportDerivative a b θ at hpair
  have hderiv : sectorThreeSupportDerivative a b θ = b := by
    simpa [θ] using sectorThreeSupportDerivative_generator_boundary ha hb
  rw [hderiv] at hpair
  have hcos : middleRadius a b * cos θ = -b := by
    simpa [θ] using middleRadius_mul_cos_middleAngle (b := b) ha
  have hsin : middleRadius a b * sin θ = a := by
    simpa [θ] using middleRadius_mul_sin_middleAngle (b := b) ha
  simp only [middleSectorThreeEndpoint, middleTangent, inner_planeVector]
  change sectorThreeBoundaryX a b θ * a +
      sectorThreeBoundaryY a b θ * b = -(b * middleRadius a b)
  calc
    sectorThreeBoundaryX a b θ * a + sectorThreeBoundaryY a b θ * b =
        -middleRadius a b *
          (-sectorThreeBoundaryX a b θ * sin θ +
            sectorThreeBoundaryY a b θ * cos θ) := by
              linear_combination
                -sectorThreeBoundaryX a b θ * hsin +
                  sectorThreeBoundaryY a b θ * hcos
    _ = -(b * middleRadius a b) := by rw [hpair]; ring

theorem eq_of_middle_pairings {a b : ℝ} (ha : 0 < a) {x y : Plane}
    (hnormal : inner ℝ x (middleNormal a b) =
      inner ℝ y (middleNormal a b))
    (htangent : inner ℝ x (middleTangent a b) =
      inner ℝ y (middleTangent a b)) :
    x = y := by
  have hnormal' := hnormal
  have htangent' := htangent
  rw [PiLp.inner_apply, PiLp.inner_apply, Fin.sum_univ_two, Fin.sum_univ_two] at hnormal'
  rw [PiLp.inner_apply, PiLp.inner_apply, Fin.sum_univ_two, Fin.sum_univ_two] at htangent'
  simp [middleNormal, middleTangent, planeVector] at hnormal' htangent'
  have hxscaled : middleRadiusSq a b * (x 0 - y 0) = 0 := by
    unfold middleRadiusSq
    linear_combination -b * hnormal' + a * htangent'
  have hyscaled : middleRadiusSq a b * (x 1 - y 1) = 0 := by
    unfold middleRadiusSq
    linear_combination a * hnormal' + b * htangent'
  have hR : 0 < middleRadiusSq a b := middleRadiusSq_pos ha
  have hx0 : x 0 = y 0 := by nlinarith
  have hx1 : x 1 = y 1 := by nlinarith
  ext i
  fin_cases i
  · exact hx0
  · exact hx1

theorem sectorTwoThreeJump_eq_middleEndpoints (a b : ℝ) :
    sectorTwoThreeJump a b =
      segment ℝ (middleSectorTwoEndpoint a b) (middleSectorThreeEndpoint a b) := by
  rfl

/-! ## Exact middle exposed face -/

/-- At the middle generator sign change, the derivative jump segment is the
complete exposed face of the exact halfspace-defined `p=2` body. -/
theorem exposedFace_middleNormal_eq_sectorTwoThreeJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    {x | x ∈ normalizedLpSumTwo a b ∧
        inner ℝ x (middleNormal a b) =
          normalizedFireySupportVec a b (middleNormal a b)} =
      sectorTwoThreeJump a b := by
  rw [sectorTwoThreeJump_eq_middleEndpoints]
  ext x
  constructor
  · rintro ⟨hxbody, hsupport⟩
    rw [normalizedFireySupportVec_middleNormal ha hb] at hsupport
    have htangentUpper := inner_middleTangent_le_of_middle_support ha hb hxbody hsupport
    have htangentLower :=
      neg_b_mul_middleRadius_le_inner_middleTangent_of_middle_support ha hb hxbody hsupport
    let T := inner ℝ x (middleTangent a b)
    let s := middleRadius a b
    let den := (a + b) * s
    let r := (T + b * s) / den
    let q := (a * s - T) / den
    have hs : 0 < s := by simpa [s] using middleRadius_pos (b := b) ha
    have hab : 0 < a + b := add_pos ha hb
    have hden : 0 < den := by exact mul_pos hab hs
    have hr : 0 ≤ r := by
      apply div_nonneg
      · dsimp [T, s]
        linarith
      · exact hden.le
    have hq : 0 ≤ q := by
      apply div_nonneg
      · simpa [T, s] using sub_nonneg.2 htangentUpper
      · exact hden.le
    have hrq : r + q = 1 := by
      unfold r q den
      field_simp [hab.ne', hs.ne']
      ring
    refine ⟨r, q, hr, hq, hrq, ?_⟩
    apply eq_of_middle_pairings ha
    · rw [inner_add_left, real_inner_smul_left, real_inner_smul_left,
        middleSectorTwoEndpoint_normal_pairing ha hb,
        middleSectorThreeEndpoint_normal_pairing ha hb, hsupport]
      nlinarith
    · rw [inner_add_left, real_inner_smul_left, real_inner_smul_left,
        middleSectorTwoEndpoint_tangent_pairing (b := b) ha,
        middleSectorThreeEndpoint_tangent_pairing ha hb]
      unfold r q den T s
      field_simp [(add_pos ha hb).ne', (middleRadius_pos (b := b) ha).ne']
      ring
  · intro hxsegment
    have hxbody : x ∈ normalizedLpSumTwo a b := by
      apply sectorTwoThreeJump_subset_normalizedLpSumTwo ha hb
      rwa [sectorTwoThreeJump_eq_middleEndpoints]
    refine ⟨hxbody, ?_⟩
    rw [normalizedFireySupportVec_middleNormal ha hb]
    rcases hxsegment with ⟨r, q, hr, hq, hrq, rfl⟩
    rw [inner_add_left, real_inner_smul_left, real_inner_smul_left,
      middleSectorTwoEndpoint_normal_pairing ha hb,
      middleSectorThreeEndpoint_normal_pairing ha hb]
    calc
      r * middleRadius a b + q * middleRadius a b =
          (r + q) * middleRadius a b := by ring
      _ = middleRadius a b := by rw [hrq, one_mul]

#print axioms normalizedFireySupportVecSq_middlePlus_expansion
#print axioms normalizedFireySupportVecSq_middleMinus_expansion
#print axioms inner_middleTangent_le_of_middle_support
#print axioms neg_b_mul_middleRadius_le_inner_middleTangent_of_middle_support
#print axioms exposedFace_middleNormal_eq_sectorTwoThreeJump

end L2Hexagon
