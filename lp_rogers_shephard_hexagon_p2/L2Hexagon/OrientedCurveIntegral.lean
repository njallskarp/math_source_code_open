import L2Hexagon.CyclicPathSimplicity
import Mathlib.MeasureTheory.Integral.CurveIntegral.Basic

/-!
# The genuine oriented curve integral of the normalized boundary path

For a planar point `x` and velocity `v`, let

`orientedAreaForm x v = x₀ v₁ - x₁ v₀`.

This is the standard one-form `x dy - y dx`.  The goal of this file is to
evaluate Mathlib's literal `curveIntegral` of this one-form along the already
constructed cyclic boundary path.  In particular, the integral is not defined
to be the previously assembled scalar support-density formula.

The Green/Jordan theorem identifying one half of this curve integral with
planar Lebesgue area remains a separate downstream theorem.
-/

open Real Set MeasureTheory
open scoped Interval unitInterval

namespace L2Hexagon

noncomputable section

/-- Cartesian determinant of two plane vectors. -/
def planeDet (x v : Plane) : ℝ := x 0 * v 1 - x 1 * v 0

/-- The standard oriented-area one-form `x dy - y dx`. -/
noncomputable def orientedAreaForm (x : Plane) : Plane →L[ℝ] ℝ :=
  LinearMap.toContinuousLinearMap
    { toFun := fun v => planeDet x v
      map_add' := by
        intro u v
        simp [planeDet]
        ring
      map_smul' := by
        intro c v
        simp [planeDet]
        ring }

@[simp] theorem orientedAreaForm_apply (x v : Plane) :
    orientedAreaForm x v = planeDet x v := rfl

theorem planeDet_lineMap_sub (x y : Plane) (t : ℝ) :
    planeDet (AffineMap.lineMap x y t) (y - x) = planeDet x y := by
  simp only [planeDet, AffineMap.lineMap_apply_module, PiLp.add_apply,
    PiLp.smul_apply, PiLp.sub_apply]
  ring

/-- Every straight segment is integrable for the oriented-area one-form. -/
theorem curveIntegrable_orientedAreaForm_segment (x y : Plane) :
    CurveIntegrable orientedAreaForm (Path.segment x y) := by
  rw [curveIntegrable_segment]
  simpa only [orientedAreaForm_apply, planeDet_lineMap_sub] using
    (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => planeDet x y) volume 0 1)

/-- The oriented curve integral of a straight segment is its endpoint determinant. -/
theorem curveIntegral_orientedAreaForm_segment (x y : Plane) :
    (∫ᶜ z in Path.segment x y, orientedAreaForm z) = planeDet x y := by
  rw [curveIntegral_segment]
  simp only [orientedAreaForm_apply, planeDet_lineMap_sub]
  simp

/-! ## Affine reparametrization of a smooth plane curve -/

/-- Pointwise curve-integral density for a smooth plane curve pulled back along
the affine segment from `c` to `d`. -/
theorem curveIntegralFun_orientedAreaForm_map_segment
    {c d : ℝ} {f f' : ℝ → Plane} (hf : Continuous f)
    (hderiv : ∀ θ, HasDerivAt f (f' θ) θ) {t : ℝ} (ht : t ∈ I) :
    curveIntegralFun orientedAreaForm ((Path.segment c d).map hf) t =
      (d - c) * planeDet (f (AffineMap.lineMap c d t))
        (f' (AffineMap.lineMap c d t)) := by
  rw [curveIntegralFun_def]
  let γ := (Path.segment c d).map hf
  have heq : Set.EqOn γ.extend (fun s => f (AffineMap.lineMap c d s)) I := by
    intro s hs
    rw [Path.extend_apply γ hs]
    simp [γ, Path.map_coe, Path.segment_apply]
  rw [heq ht, derivWithin_congr heq (heq ht)]
  have hcomp : HasDerivAt (fun s => f (AffineMap.lineMap c d s))
      ((d - c) • f' (AffineMap.lineMap c d t)) t :=
    (hderiv (AffineMap.lineMap c d t)).scomp t
      (AffineMap.hasDerivAt_lineMap (a := c) (b := d) (x := t))
  rw [hcomp.hasDerivWithinAt.derivWithin (uniqueDiffOn_Icc_zero_one t ht)]
  simp only [orientedAreaForm_apply, planeDet, PiLp.smul_apply]
  ring

/-- A continuously differentiable plane curve, affinely parametrized on the
unit interval, is integrable for the oriented-area one-form. -/
theorem curveIntegrable_orientedAreaForm_map_segment
    {c d : ℝ} {f f' : ℝ → Plane} (hf : Continuous f)
    (hderiv : ∀ θ, HasDerivAt f (f' θ) θ)
    (hdensity : Continuous (fun θ => planeDet (f θ) (f' θ))) :
    CurveIntegrable orientedAreaForm ((Path.segment c d).map hf) := by
  rw [CurveIntegrable]
  have hcont : Continuous (fun t =>
      (d - c) * planeDet (f ((AffineMap.lineMap c d : ℝ →ᵃ[ℝ] ℝ) t))
        (f' ((AffineMap.lineMap c d : ℝ →ᵃ[ℝ] ℝ) t))) := by
    exact continuous_const.mul (hdensity.comp AffineMap.lineMap_continuous)
  refine (hcont.intervalIntegrable 0 1).congr ?_
  intro t ht
  rw [uIoc_of_le zero_le_one] at ht
  exact (curveIntegralFun_orientedAreaForm_map_segment hf hderiv
    (Ioc_subset_Icc_self ht)).symm

/-- Affine reparametrization of a smooth curve preserves its oriented curve
integral.  The right side uses the original parameter interval `[c,d]`. -/
theorem curveIntegral_orientedAreaForm_map_segment
    {c d : ℝ} {f f' : ℝ → Plane} (hf : Continuous f)
    (hderiv : ∀ θ, HasDerivAt f (f' θ) θ) :
    (∫ᶜ z in (Path.segment c d).map hf, orientedAreaForm z) =
      ∫ θ in c..d, planeDet (f θ) (f' θ) := by
  rw [curveIntegral_def]
  calc
    (∫ t in (0 : ℝ)..1,
        curveIntegralFun orientedAreaForm ((Path.segment c d).map hf) t) =
        ∫ t in (0 : ℝ)..1,
          (d - c) * planeDet (f (AffineMap.lineMap c d t))
            (f' (AffineMap.lineMap c d t)) := by
      apply intervalIntegral.integral_congr
      intro t ht
      rw [uIcc_of_le zero_le_one] at ht
      exact curveIntegralFun_orientedAreaForm_map_segment hf hderiv ht
    _ = ∫ θ in c..d, planeDet (f θ) (f' θ) := by
      simpa [AffineMap.lineMap_apply_ring', smul_eq_mul, mul_comm] using
        (intervalIntegral.smul_integral_comp_mul_add
          (f := fun θ => planeDet (f θ) (f' θ))
          (a := (0 : ℝ)) (b := 1) (d - c) c)

/-! ## The two canonical curved pieces -/

theorem planeVector_eq_smul_basis (x y : ℝ) :
    planeVector x y = x • planeE1 + y • planeE2 := by
  ext i
  fin_cases i <;> simp [planeVector, planeE1, planeE2]

/-- Velocity of the Sector II canonical boundary point. -/
noncomputable def sectorTwoBoundaryVelocity (a b θ : ℝ) : Plane :=
  planeVector (sectorTwoBoundaryDX a b θ) (sectorTwoBoundaryDY a b θ)

/-- Velocity of the Sector III canonical boundary point. -/
noncomputable def sectorThreeBoundaryVelocity (a b θ : ℝ) : Plane :=
  planeVector (sectorThreeBoundaryDX a b θ) (sectorThreeBoundaryDY a b θ)

theorem hasDerivAt_sectorTwoBoundaryPoint {a b : ℝ} (hb : 0 < b) (θ : ℝ) :
    HasDerivAt (sectorTwoBoundaryPoint a b) (sectorTwoBoundaryVelocity a b θ) θ := by
  rw [show sectorTwoBoundaryPoint a b = fun t =>
      sectorTwoBoundaryX a b t • planeE1 + sectorTwoBoundaryY a b t • planeE2 by
    funext t
    exact planeVector_eq_smul_basis _ _]
  rw [sectorTwoBoundaryVelocity, planeVector_eq_smul_basis]
  exact ((hasDerivAt_sectorTwoBoundaryX hb θ).smul_const planeE1).add
    ((hasDerivAt_sectorTwoBoundaryY hb θ).smul_const planeE2)

theorem hasDerivAt_sectorThreeBoundaryPoint {a b : ℝ} (ha : 0 < a) (θ : ℝ) :
    HasDerivAt (sectorThreeBoundaryPoint a b)
      (sectorThreeBoundaryVelocity a b θ) θ := by
  rw [show sectorThreeBoundaryPoint a b = fun t =>
      sectorThreeBoundaryX a b t • planeE1 + sectorThreeBoundaryY a b t • planeE2 by
    funext t
    exact planeVector_eq_smul_basis _ _]
  rw [sectorThreeBoundaryVelocity, planeVector_eq_smul_basis]
  exact ((hasDerivAt_sectorThreeBoundaryX ha θ).smul_const planeE1).add
    ((hasDerivAt_sectorThreeBoundaryY ha θ).smul_const planeE2)

theorem planeDet_sectorTwoBoundaryPoint_velocity (a b θ : ℝ) :
    planeDet (sectorTwoBoundaryPoint a b θ) (sectorTwoBoundaryVelocity a b θ) =
      sectorTwoBoundaryOrientedDensity a b θ := by
  simp [planeDet, sectorTwoBoundaryPoint, sectorTwoBoundaryVelocity,
    sectorTwoBoundaryOrientedDensity, planeVector]

theorem planeDet_sectorThreeBoundaryPoint_velocity (a b θ : ℝ) :
    planeDet (sectorThreeBoundaryPoint a b θ) (sectorThreeBoundaryVelocity a b θ) =
      sectorThreeBoundaryOrientedDensity a b θ := by
  simp [planeDet, sectorThreeBoundaryPoint, sectorThreeBoundaryVelocity,
    sectorThreeBoundaryOrientedDensity, planeVector]

theorem continuous_sectorTwoCurvature {a b : ℝ} (hb : 0 < b) :
    Continuous (sectorTwoCurvature a b) := by
  unfold sectorTwoCurvature
  apply Continuous.div continuous_const
  · unfold sectorTwoSq sectorTwoU
    fun_prop
  · intro θ
    exact (sectorTwoSq_pos (a := a) hb θ).ne'

theorem continuous_sectorThreeCurvature {a b : ℝ} (ha : 0 < a) :
    Continuous (sectorThreeCurvature a b) := by
  unfold sectorThreeCurvature
  apply Continuous.div continuous_const
  · unfold sectorThreeSq sectorThreeW
    fun_prop
  · intro θ
    exact (sectorThreeSq_pos (b := b) ha θ).ne'

theorem continuous_sectorTwoBoundaryOrientedDensity {a b : ℝ} (hb : 0 < b) :
    Continuous (sectorTwoBoundaryOrientedDensity a b) := by
  exact (continuous_congr (fun θ =>
    sectorTwoBoundaryOrientedDensity_eq_curvature (a := a) (b := b) hb θ)).2
      (continuous_sectorTwoCurvature (a := a) (b := b) hb)

theorem continuous_sectorThreeBoundaryOrientedDensity {a b : ℝ} (ha : 0 < a) :
    Continuous (sectorThreeBoundaryOrientedDensity a b) := by
  exact (continuous_congr (fun θ =>
    sectorThreeBoundaryOrientedDensity_eq_curvature (a := a) (b := b) ha θ)).2
      (continuous_sectorThreeCurvature (a := a) (b := b) ha)

/-- The literal Sector II arc path is curve-integrable for `x dy - y dx`. -/
theorem curveIntegrable_orientedAreaForm_sectorTwoArc {a b : ℝ}
    (hb : 0 < b) : CurveIntegrable orientedAreaForm (sectorTwoArcPath a b hb) := by
  apply curveIntegrable_orientedAreaForm_map_segment
    (continuous_sectorTwoBoundaryPoint hb)
    (hasDerivAt_sectorTwoBoundaryPoint hb)
  simpa only [planeDet_sectorTwoBoundaryPoint_velocity] using
    continuous_sectorTwoBoundaryOrientedDensity hb

/-- The literal Sector III arc path is curve-integrable for `x dy - y dx`. -/
theorem curveIntegrable_orientedAreaForm_sectorThreeArc {a b : ℝ}
    (ha : 0 < a) : CurveIntegrable orientedAreaForm (sectorThreeArcPath a b ha) := by
  apply curveIntegrable_orientedAreaForm_map_segment
    (continuous_sectorThreeBoundaryPoint ha)
    (hasDerivAt_sectorThreeBoundaryPoint ha)
  simpa only [planeDet_sectorThreeBoundaryPoint_velocity] using
    continuous_sectorThreeBoundaryOrientedDensity ha

/-- Exact Mathlib curve integral of the literal Sector II arc. -/
theorem curveIntegral_orientedAreaForm_sectorTwoArc {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in sectorTwoArcPath a b hb, orientedAreaForm z) =
      (1 + b) * arctan (b / a) := by
  rw [sectorTwoArcPath,
    curveIntegral_orientedAreaForm_map_segment
      (continuous_sectorTwoBoundaryPoint hb)
      (hasDerivAt_sectorTwoBoundaryPoint hb)]
  simpa only [planeDet_sectorTwoBoundaryPoint_velocity] using
    integral_sectorTwoBoundaryOrientedDensity ha hb

/-- Exact Mathlib curve integral of the literal Sector III arc. -/
theorem curveIntegral_orientedAreaForm_sectorThreeArc {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in sectorThreeArcPath a b ha, orientedAreaForm z) =
      (1 + a) * (π / 2 - arctan (b / a)) := by
  rw [sectorThreeArcPath,
    curveIntegral_orientedAreaForm_map_segment
      (continuous_sectorThreeBoundaryPoint ha)
      (hasDerivAt_sectorThreeBoundaryPoint ha)]
  simpa only [planeDet_sectorThreeBoundaryPoint_velocity] using
    integral_sectorThreeBoundaryOrientedDensity ha hb

/-! ## The three literal jump segments -/

theorem planeDet_sectorOneVertex_sectorTwoBoundaryPoint_pi_div_two
    {a b : ℝ} (hb : 0 < b) :
    planeDet (sectorOneVertex a b) (sectorTwoBoundaryPoint a b (π / 2)) = 1 + b := by
  rw [sectorTwoBoundaryPoint_pi_div_two' hb]
  simp [planeDet, sectorOneVertex, planeVector]
  ring

theorem planeDet_middleBoundaryPoints {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    planeDet
      (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
      (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))) = a + b := by
  unfold planeDet sectorTwoBoundaryPoint sectorThreeBoundaryPoint
  change
    sectorTwoBoundaryX a b (π / 2 + arctan (b / a)) *
        sectorThreeBoundaryY a b (π / 2 + arctan (b / a)) -
      sectorTwoBoundaryY a b (π / 2 + arctan (b / a)) *
        sectorThreeBoundaryX a b (π / 2 + arctan (b / a)) = a + b
  simpa [sectorTwoBoundaryX, sectorTwoBoundaryY, sectorThreeBoundaryX,
    sectorThreeBoundaryY, supportBoundaryTransitionDet] using
      sectorTwoThree_transitionDet ha hb

theorem planeDet_sectorThreeBoundaryPoint_pi_neg_sectorOneVertex
    {a b : ℝ} (ha : 0 < a) :
    planeDet (sectorThreeBoundaryPoint a b π) (-sectorOneVertex a b) = 1 + a := by
  unfold sectorThreeBoundaryPoint
  rw [sectorThreeBoundaryPoint_pi ha]
  simp [planeDet, sectorOneVertex, planeVector]
  ring

/-- The first literal jump segment contributes `1+b`. -/
theorem curveIntegral_orientedAreaForm_firstJump {a b : ℝ} (hb : 0 < b) :
    (∫ᶜ z in Path.segment (sectorOneVertex a b)
      (sectorTwoBoundaryPoint a b (π / 2)), orientedAreaForm z) = 1 + b := by
  rw [curveIntegral_orientedAreaForm_segment,
    planeDet_sectorOneVertex_sectorTwoBoundaryPoint_pi_div_two hb]

/-- The middle literal jump segment contributes `a+b`. -/
theorem curveIntegral_orientedAreaForm_middleJump {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in Path.segment
      (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
      (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a))),
      orientedAreaForm z) = a + b := by
  rw [curveIntegral_orientedAreaForm_segment, planeDet_middleBoundaryPoints ha hb]

/-- The closing literal upper jump segment contributes `1+a`. -/
theorem curveIntegral_orientedAreaForm_closingJump {a b : ℝ} (ha : 0 < a) :
    (∫ᶜ z in Path.segment (sectorThreeBoundaryPoint a b π)
      (-sectorOneVertex a b), orientedAreaForm z) = 1 + a := by
  rw [curveIntegral_orientedAreaForm_segment,
    planeDet_sectorThreeBoundaryPoint_pi_neg_sectorOneVertex ha]

/-! ## The literal five-piece upper path -/

/-- Every piece of the actual five-piece upper boundary path is curve-integrable. -/
theorem curveIntegrable_orientedAreaForm_normalizedUpperBoundaryPath
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    CurveIntegrable orientedAreaForm (normalizedUpperBoundaryPath a b ha hb) := by
  unfold normalizedUpperBoundaryPath
  exact (((curveIntegrable_orientedAreaForm_segment _ _).trans
      (curveIntegrable_orientedAreaForm_sectorTwoArc hb)).trans
    (curveIntegrable_orientedAreaForm_segment _ _)).trans
      (curveIntegrable_orientedAreaForm_sectorThreeArc ha) |>.trans
        (curveIntegrable_orientedAreaForm_segment _ _)

/-- The genuine Mathlib curve integral of the five-piece upper path agrees
with the independently assembled arcs-plus-jumps total. -/
theorem curveIntegral_orientedAreaForm_normalizedUpperBoundaryPath_eq_total
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in normalizedUpperBoundaryPath a b ha hb, orientedAreaForm z) =
      normalizedUpperBoundaryOrientedTotal a b := by
  have h1 := curveIntegrable_orientedAreaForm_segment
    (sectorOneVertex a b) (sectorTwoBoundaryPoint a b (π / 2))
  have h2 := curveIntegrable_orientedAreaForm_sectorTwoArc (a := a) hb
  have h3 := curveIntegrable_orientedAreaForm_segment
    (sectorTwoBoundaryPoint a b (π / 2 + arctan (b / a)))
    (sectorThreeBoundaryPoint a b (π / 2 + arctan (b / a)))
  have h4 := curveIntegrable_orientedAreaForm_sectorThreeArc (b := b) ha
  have h5 := curveIntegrable_orientedAreaForm_segment
    (sectorThreeBoundaryPoint a b π) (-sectorOneVertex a b)
  rw [normalizedUpperBoundaryPath,
    curveIntegral_trans (((h1.trans h2).trans h3).trans h4) h5,
    curveIntegral_trans ((h1.trans h2).trans h3) h4,
    curveIntegral_trans (h1.trans h2) h3,
    curveIntegral_trans h1 h2,
    curveIntegral_orientedAreaForm_firstJump hb,
    curveIntegral_orientedAreaForm_sectorTwoArc ha hb,
    curveIntegral_orientedAreaForm_middleJump ha hb,
    curveIntegral_orientedAreaForm_sectorThreeArc ha hb,
    curveIntegral_orientedAreaForm_closingJump ha,
    normalizedUpperBoundaryOrientedTotal_eq ha hb]
  ring

/-- Closed formula for the genuine oriented integral of the upper path. -/
theorem curveIntegral_orientedAreaForm_normalizedUpperBoundaryPath
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in normalizedUpperBoundaryPath a b ha hb, orientedAreaForm z) =
      2 * (1 + a + b) + (1 + b) * arctan (b / a) +
        (1 + a) * (π / 2 - arctan (b / a)) := by
  rw [curveIntegral_orientedAreaForm_normalizedUpperBoundaryPath_eq_total ha hb,
    normalizedUpperBoundaryOrientedTotal_eq ha hb]

/-! ## Invariance under pointwise negation -/

theorem Path.extend_map_neg {x y : Plane} (γ : Path x y) (t : ℝ) :
    (γ.map (f := fun z : Plane => -z) continuous_neg).extend t = -γ.extend t := by
  rcases le_total t 0 with ht | ht
  · rw [Path.extend_of_le_zero _ ht, Path.extend_of_le_zero _ ht]
  rcases le_total 1 t with ht1 | ht1
  · rw [Path.extend_of_one_le _ ht1, Path.extend_of_one_le _ ht1]
  · have htI : t ∈ (Icc (0 : ℝ) 1) := ⟨ht, ht1⟩
    rw [Path.extend_apply _ htI, Path.extend_apply _ htI]
    rfl

theorem curveIntegralFun_orientedAreaForm_map_neg {x y : Plane}
    (γ : Path x y) (t : ℝ) :
    curveIntegralFun orientedAreaForm
        (γ.map (f := fun z : Plane => -z) continuous_neg) t =
      curveIntegralFun orientedAreaForm γ t := by
  rw [curveIntegralFun_def, curveIntegralFun_def]
  have hext :
      (γ.map (f := fun z : Plane => -z) continuous_neg).extend =
        fun s => -γ.extend s := by
    funext s
    exact Path.extend_map_neg γ s
  rw [hext]
  change planeDet (-γ.extend t)
      (derivWithin (fun s => -γ.extend s) I t) =
    planeDet (γ.extend t) (derivWithin γ.extend I t)
  have hderiv : derivWithin (fun s => -γ.extend s) I t =
      -derivWithin γ.extend I t := by
    change derivWithin (-γ.extend) I t = -derivWithin γ.extend I t
    exact derivWithin.neg
  rw [hderiv]
  simp [planeDet]

/-- The oriented-area one-form is invariant under simultaneously negating
the path point and its velocity. -/
theorem curveIntegral_orientedAreaForm_map_neg {x y : Plane} (γ : Path x y) :
    (∫ᶜ z in γ.map (f := fun z : Plane => -z) continuous_neg, orientedAreaForm z) =
      ∫ᶜ z in γ, orientedAreaForm z := by
  rw [curveIntegral_def, curveIntegral_def]
  apply intervalIntegral.integral_congr
  intro t _
  exact curveIntegralFun_orientedAreaForm_map_neg γ t

/-- Curve-integrability for the oriented-area one-form is preserved by
pointwise negation. -/
theorem curveIntegrable_orientedAreaForm_map_neg_iff {x y : Plane} (γ : Path x y) :
    CurveIntegrable orientedAreaForm
        (γ.map (f := fun z : Plane => -z) continuous_neg) ↔
      CurveIntegrable orientedAreaForm γ := by
  rw [CurveIntegrable, CurveIntegrable]
  apply intervalIntegrable_congr
  intro t _
  exact curveIntegralFun_orientedAreaForm_map_neg γ t

/-! ## The genuine full-cycle curve integral -/

/-- The actual continuous cyclic boundary path is curve-integrable for
`x dy - y dx`. -/
theorem curveIntegrable_orientedAreaForm_normalizedCyclicBoundaryPath
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    CurveIntegrable orientedAreaForm (normalizedCyclicBoundaryPath a b ha hb) := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  let lower : Path (-sectorOneVertex a b) (sectorOneVertex a b) :=
    (upper.map (f := fun z : Plane => -z) continuous_neg).cast rfl (neg_neg _).symm
  have hu : CurveIntegrable orientedAreaForm upper :=
    curveIntegrable_orientedAreaForm_normalizedUpperBoundaryPath ha hb
  have hm : CurveIntegrable orientedAreaForm
      (upper.map (f := fun z : Plane => -z) continuous_neg) :=
    (curveIntegrable_orientedAreaForm_map_neg_iff upper).2 hu
  have hl : CurveIntegrable orientedAreaForm lower := by
    exact hm.cast rfl (neg_neg _).symm
  change CurveIntegrable orientedAreaForm (upper.trans lower)
  exact hu.trans hl

/-- The literal curve integral of the pointwise-negative return half equals
the upper-half integral. -/
theorem curveIntegral_orientedAreaForm_negativeUpperHalf
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    let upper := normalizedUpperBoundaryPath a b ha hb
    (∫ᶜ z in (upper.map (f := fun z : Plane => -z) continuous_neg).cast rfl
      (neg_neg _).symm, orientedAreaForm z) =
      ∫ᶜ z in upper, orientedAreaForm z := by
  dsimp only
  rw [curveIntegral_cast, curveIntegral_orientedAreaForm_map_neg]

/-- Exact full-cycle identity for the genuine Mathlib curve integral of
`x dy - y dx` along the already checked simple cyclic frontier path. -/
theorem curveIntegral_orientedAreaForm_normalizedCyclicBoundaryPath
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ᶜ z in normalizedCyclicBoundaryPath a b ha hb, orientedAreaForm z) =
      2 * (2 * (1 + a + b) + (1 + b) * arctan (b / a) +
        (1 + a) * (π / 2 - arctan (b / a))) := by
  let upper := normalizedUpperBoundaryPath a b ha hb
  let lower : Path (-sectorOneVertex a b) (sectorOneVertex a b) :=
    (upper.map (f := fun z : Plane => -z) continuous_neg).cast rfl (neg_neg _).symm
  have hu : CurveIntegrable orientedAreaForm upper :=
    curveIntegrable_orientedAreaForm_normalizedUpperBoundaryPath ha hb
  have hm : CurveIntegrable orientedAreaForm
      (upper.map (f := fun z : Plane => -z) continuous_neg) :=
    (curveIntegrable_orientedAreaForm_map_neg_iff upper).2 hu
  have hl : CurveIntegrable orientedAreaForm lower := by
    exact hm.cast rfl (neg_neg _).symm
  change (∫ᶜ z in upper.trans lower, orientedAreaForm z) = _
  rw [curveIntegral_trans hu hl]
  have hlint : (∫ᶜ z in lower, orientedAreaForm z) =
      ∫ᶜ z in upper, orientedAreaForm z := by
    simpa only [lower] using
      curveIntegral_orientedAreaForm_negativeUpperHalf ha hb
  rw [hlint, curveIntegral_orientedAreaForm_normalizedUpperBoundaryPath ha hb]
  ring

/-- The full-cycle oriented integral is strictly positive.  This is the
algebraic orientation certificate; identifying its half with Lebesgue area
still requires a Green/Jordan theorem. -/
theorem curveIntegral_orientedAreaForm_normalizedCyclicBoundaryPath_pos
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    0 < ∫ᶜ z in normalizedCyclicBoundaryPath a b ha hb, orientedAreaForm z := by
  rw [curveIntegral_orientedAreaForm_normalizedCyclicBoundaryPath ha hb]
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφ0 : 0 < arctan (b / a) := by
    simpa only [generatorAngle] using hφ.1
  have hφπ : 0 < π / 2 - arctan (b / a) := by
    have := hφ.2
    simp only [generatorAngle] at this
    linarith
  have hmain : 0 < 2 * (1 + a + b) := by positivity
  have htwo : 0 < (1 + b) * arctan (b / a) := by positivity
  have hthree : 0 < (1 + a) * (π / 2 - arctan (b / a)) := by positivity
  positivity

#print axioms curveIntegrable_orientedAreaForm_segment
#print axioms curveIntegral_orientedAreaForm_segment
#print axioms curveIntegral_orientedAreaForm_normalizedUpperBoundaryPath
#print axioms curveIntegrable_orientedAreaForm_normalizedCyclicBoundaryPath
#print axioms curveIntegral_orientedAreaForm_normalizedCyclicBoundaryPath
#print axioms curveIntegral_orientedAreaForm_normalizedCyclicBoundaryPath_pos

end

end L2Hexagon
