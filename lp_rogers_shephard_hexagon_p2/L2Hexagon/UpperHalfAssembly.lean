import L2Hexagon.SectorOneIntegral

/-!
# Assembly of the three normalized upper-half-circle sectors

This file defines one piecewise scalar density on `[0,π]` from the exact
Sector I, II, and III formulas.  It proves interval integrability on every
piece, uses interval additivity at both sign-change angles, and derives the
complete upper-half-circle integral

`2(1+a+b)+(1+b)φ+(1+a)(π/2-φ)`.

The set-level support restrictions are proved separately in
`NormalizedSectorSupport.lean`.  The present theorem does not invoke or claim
the planar support-area/Lebesgue-area identity.
-/

open Real Set MeasureTheory
open scoped Interval

namespace L2Hexagon

/-- The three checked scalar densities assembled according to their sign sectors. -/
noncomputable def normalizedUpperDensity (a b θ : ℝ) : ℝ :=
  if θ ≤ π / 2 then sectorOneDensity a b θ
  else if θ ≤ π / 2 + arctan (b / a) then sectorTwoDensity a b θ
  else sectorThreeDensity a b θ

/-- The assembled density equals Sector I in the open first interval. -/
theorem normalizedUpperDensity_eq_sectorOne {a b θ : ℝ}
    (hθ : θ ∈ Ioo 0 (π / 2)) :
    normalizedUpperDensity a b θ = sectorOneDensity a b θ := by
  rw [normalizedUpperDensity, if_pos hθ.2.le]

/-- The assembled density equals Sector II in the open second interval. -/
theorem normalizedUpperDensity_eq_sectorTwo {a b θ : ℝ}
    (hθ : θ ∈ Ioo (π / 2) (π / 2 + arctan (b / a))) :
    normalizedUpperDensity a b θ = sectorTwoDensity a b θ := by
  rw [normalizedUpperDensity, if_neg (not_le.mpr hθ.1), if_pos hθ.2.le]

/-- The assembled density equals Sector III in the open third interval. -/
theorem normalizedUpperDensity_eq_sectorThree {a b θ : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hθ : θ ∈ Ioo (π / 2 + arctan (b / a)) π) :
    normalizedUpperDensity a b θ = sectorThreeDensity a b θ := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  rw [normalizedUpperDensity,
    if_neg (not_le.mpr (lt_trans (by linarith [hφpos]) hθ.1)),
    if_neg (not_le.mpr hθ.1)]

/-- Sector II density is continuous, hence interval integrable, when `b>0`. -/
theorem sectorTwoDensity_continuous {a b : ℝ} (hb : 0 < b) :
    Continuous (sectorTwoDensity a b) := by
  have hsq : Continuous (sectorTwoSq a b) := by
    unfold sectorTwoSq sectorTwoU
    fun_prop
  have hboundary : Continuous (sectorTwoBoundary a b) := by
    unfold sectorTwoBoundary sectorTwoU sectorTwoV
    fun_prop
  unfold sectorTwoDensity
  exact hsq.sub ((hboundary.pow 2).div hsq (fun θ => (sectorTwoSq_pos hb θ).ne'))

/-- Sector III density is continuous, hence interval integrable, when `a>0`. -/
theorem sectorThreeDensity_continuous {a b : ℝ} (ha : 0 < a) :
    Continuous (sectorThreeDensity a b) := by
  have hsq : Continuous (sectorThreeSq a b) := by
    unfold sectorThreeSq sectorThreeW
    fun_prop
  have hboundary : Continuous (sectorThreeBoundary a b) := by
    unfold sectorThreeBoundary sectorThreeW sectorThreeZ
    fun_prop
  have hpos : ∀ θ, sectorThreeSq a b θ ≠ 0 := by
    intro θ
    rw [sectorThreeSq_reflect]
    exact (sectorTwoSq_pos (a := b) ha (3 * π / 2 - θ)).ne'
  unfold sectorThreeDensity
  exact hsq.sub ((hboundary.pow 2).div hsq hpos)

/-- The assembled density is interval integrable on Sector I. -/
theorem normalizedUpperDensity_intervalIntegrable_sectorOne (a b : ℝ) :
    IntervalIntegrable (normalizedUpperDensity a b) volume 0 (π / 2) := by
  have hbase : IntervalIntegrable (sectorOneDensity a b) volume 0 (π / 2) := by
    apply Continuous.intervalIntegrable
    unfold sectorOneDensity sectorOneSupport sectorOneDerivative
    fun_prop
  apply hbase.congr_uIoo
  intro θ hθ
  rw [uIoo_of_le Real.pi_div_two_pos.le] at hθ
  exact (normalizedUpperDensity_eq_sectorOne hθ).symm

/-- The assembled density is interval integrable on Sector II. -/
theorem normalizedUpperDensity_intervalIntegrable_sectorTwo {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    IntervalIntegrable (normalizedUpperDensity a b) volume
      (π / 2) (π / 2 + arctan (b / a)) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  have hbase : IntervalIntegrable (sectorTwoDensity a b) volume
      (π / 2) (π / 2 + arctan (b / a)) :=
    (sectorTwoDensity_continuous (a := a) (b := b) hb).intervalIntegrable
      (π / 2) (π / 2 + arctan (b / a))
  apply hbase.congr_uIoo
  intro θ hθ
  rw [uIoo_of_le (by linarith [hφpos])] at hθ
  exact (normalizedUpperDensity_eq_sectorTwo hθ).symm

/-- The assembled density is interval integrable on Sector III. -/
theorem normalizedUpperDensity_intervalIntegrable_sectorThree {a b : ℝ}
    (ha : 0 < a) (hb : 0 < b) :
    IntervalIntegrable (normalizedUpperDensity a b) volume
      (π / 2 + arctan (b / a)) π := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφlt : arctan (b / a) < π / 2 := by
    simpa [generatorAngle] using hφ.2
  have hbase : IntervalIntegrable (sectorThreeDensity a b) volume
      (π / 2 + arctan (b / a)) π :=
    (sectorThreeDensity_continuous (a := a) (b := b) ha).intervalIntegrable
      (π / 2 + arctan (b / a)) π
  apply hbase.congr_uIoo
  intro θ hθ
  rw [uIoo_of_le (by linarith [hφlt])] at hθ
  exact (normalizedUpperDensity_eq_sectorThree ha hb hθ).symm

/-- The complete checked scalar density integral over the upper half-circle. -/
theorem integral_normalizedUpperDensity {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (∫ θ in (0 : ℝ)..π, normalizedUpperDensity a b θ) =
      2 * (1 + a + b) + (1 + b) * arctan (b / a) +
        (1 + a) * (π / 2 - arctan (b / a)) := by
  have hφ := generatorAngle_mem_Ioo ha hb
  have hφpos : 0 < arctan (b / a) := by
    simpa [generatorAngle] using hφ.1
  have h0pi2 : (0 : ℝ) ≤ π / 2 := Real.pi_div_two_pos.le
  have hpi2φ : π / 2 ≤ π / 2 + arctan (b / a) := by linarith
  have hφpi : π / 2 + arctan (b / a) ≤ π := by
    have hφlt : arctan (b / a) < π / 2 := by
      simpa [generatorAngle] using hφ.2
    linarith
  have hI1 := normalizedUpperDensity_intervalIntegrable_sectorOne a b
  have hI2 := normalizedUpperDensity_intervalIntegrable_sectorTwo ha hb
  have hI3 := normalizedUpperDensity_intervalIntegrable_sectorThree ha hb
  have hEq1 : (∫ θ in (0 : ℝ)..π / 2, normalizedUpperDensity a b θ) =
      ∫ θ in (0 : ℝ)..π / 2, sectorOneDensity a b θ := by
    apply intervalIntegral.integral_congr_Ioo_of_le h0pi2
    intro θ hθ
    exact normalizedUpperDensity_eq_sectorOne hθ
  have hEq2 : (∫ θ in π / 2..π / 2 + arctan (b / a), normalizedUpperDensity a b θ) =
      ∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoDensity a b θ := by
    apply intervalIntegral.integral_congr_Ioo_of_le hpi2φ
    intro θ hθ
    exact normalizedUpperDensity_eq_sectorTwo hθ
  have hEq3 : (∫ θ in π / 2 + arctan (b / a)..π, normalizedUpperDensity a b θ) =
      ∫ θ in π / 2 + arctan (b / a)..π, sectorThreeDensity a b θ := by
    apply intervalIntegral.integral_congr_Ioo_of_le hφpi
    intro θ hθ
    exact normalizedUpperDensity_eq_sectorThree ha hb hθ
  calc
    (∫ θ in (0 : ℝ)..π, normalizedUpperDensity a b θ) =
        (∫ θ in (0 : ℝ)..π / 2, normalizedUpperDensity a b θ) +
          ∫ θ in π / 2..π, normalizedUpperDensity a b θ := by
            rw [intervalIntegral.integral_add_adjacent_intervals hI1 (hI2.trans hI3)]
    _ = (∫ θ in (0 : ℝ)..π / 2, normalizedUpperDensity a b θ) +
        ((∫ θ in π / 2..π / 2 + arctan (b / a), normalizedUpperDensity a b θ) +
          ∫ θ in π / 2 + arctan (b / a)..π, normalizedUpperDensity a b θ) := by
            rw [intervalIntegral.integral_add_adjacent_intervals hI2 hI3]
    _ = (∫ θ in (0 : ℝ)..π / 2, sectorOneDensity a b θ) +
        ((∫ θ in π / 2..π / 2 + arctan (b / a), sectorTwoDensity a b θ) +
          ∫ θ in π / 2 + arctan (b / a)..π, sectorThreeDensity a b θ) := by
            rw [hEq1, hEq2, hEq3]
    _ = 2 * (1 + a + b) + (1 + b) * arctan (b / a) +
        (1 + a) * (π / 2 - arctan (b / a)) := by
          rw [integral_sectorOneDensity, integral_sectorTwoDensity ha hb,
            integral_sectorThreeDensity ha hb]
          ring

#print axioms normalizedUpperDensity_eq_sectorOne
#print axioms normalizedUpperDensity_eq_sectorTwo
#print axioms normalizedUpperDensity_eq_sectorThree
#print axioms sectorTwoDensity_continuous
#print axioms sectorThreeDensity_continuous
#print axioms integral_normalizedUpperDensity

end L2Hexagon
