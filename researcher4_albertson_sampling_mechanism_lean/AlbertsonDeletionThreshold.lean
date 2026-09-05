import AlbertsonSamplingMechanism

/-!
# Exact edge thresholds for affine deletion recurrences

This file inverts `deletionRecurrenceBound`.  For positive slope, scale, and
target, it gives the least edge count at which the natural-number ceiling of
the affine deletion bound reaches the target.  The theorem is parameterized in
all coefficients and orders; the Albertson `r = 28` values are diagnostics.
-/

namespace AlbertsonSamplingMechanism

/-- Least edge count at which the affine one-vertex-deletion recurrence can
reach `target`.  The positivity hypotheses needed for its specification are
kept on the theorem rather than baked into the data. -/
def deletionEdgeThreshold
    (n slope intercept scale target : ℕ) : ℕ :=
  (intercept * n + scale * (n - 4) * (target - 1) + 1) ⌈/⌉
    (slope * (n - 2))

/-- Exact threshold inversion for the affine deletion recurrence.

The right side uses a ceiling after truncated subtraction.  Positivity of the
target makes the characterization exact: reaching a positive target forces
the pre-subtraction numerator to exceed the intercept term, so no information
is lost by natural-number subtraction. -/
theorem deletionEdgeThreshold_le_iff
    {n slope intercept scale target edgeCount : ℕ}
    (hn : 4 < n) (hslope : 0 < slope) (hscale : 0 < scale)
    (htarget : 0 < target) :
    deletionEdgeThreshold n slope intercept scale target ≤ edgeCount ↔
      target ≤
        deletionRecurrenceBound n slope intercept scale edgeCount := by
  let A := slope * edgeCount * (n - 2)
  let B := intercept * n
  let Q := scale * (n - 4)
  let P := slope * (n - 2)
  have hQ : 0 < Q := by
    dsimp [Q]
    exact Nat.mul_pos hscale (by omega)
  have hP : 0 < P := by
    dsimp [P]
    exact Nat.mul_pos hslope (by omega)
  have hPA : P * edgeCount = A := by
    dsimp [P, A]
    ac_rfl
  rw [deletionEdgeThreshold, deletionRecurrenceBound]
  change (B + Q * (target - 1) + 1) ⌈/⌉ P ≤ edgeCount ↔
    target ≤ (A - B) ⌈/⌉ Q
  constructor
  · intro hthreshold
    have hN : B + Q * (target - 1) + 1 ≤ A := by
      have := (ceilDiv_le_iff_le_mul hP).1 hthreshold
      rwa [hPA] at this
    have hB : B ≤ A := by omega
    have hstrict : Q * (target - 1) < A - B := by omega
    by_contra hnot
    have hceil : (A - B) ⌈/⌉ Q ≤ target - 1 := by omega
    have hupper : A - B ≤ Q * (target - 1) :=
      (ceilDiv_le_iff_le_mul hQ).1 hceil
    omega
  · intro hreaches
    apply (ceilDiv_le_iff_le_mul hP).2
    rw [hPA]
    have hstrict : Q * (target - 1) < A - B := by
      by_contra hnot
      have hupper : A - B ≤ Q * (target - 1) := by omega
      have hceil : (A - B) ⌈/⌉ Q ≤ target - 1 :=
        (ceilDiv_le_iff_le_mul hQ).2 hupper
      omega
    omega

/-- The order-55 affine recurrence first reaches the Albertson comparison
value at 770 edges. -/
theorem r28_order55_edge_threshold :
    deletionEdgeThreshold 55 r28Order54Support.slope
      r28Order54Support.intercept r28Order54Support.scale
      (zarankiewiczNumber 28) = 770 := by
  norm_num [deletionEdgeThreshold, r28Order54Support, zarankiewiczNumber,
    Nat.ceilDiv_eq_add_pred_div]

/-- Parameterized threshold inversion specialized only after the generic
proof: at order 55, the recurrence reaches `Z(28)` exactly from edge 770 on. -/
theorem r28_order55_reaches_zarankiewicz_iff (edgeCount : ℕ) :
    770 ≤ edgeCount ↔
      zarankiewiczNumber 28 ≤
        deletionRecurrenceBound 55 r28Order54Support.slope
          r28Order54Support.intercept r28Order54Support.scale edgeCount := by
  rw [← r28_order55_edge_threshold]
  exact deletionEdgeThreshold_le_iff (by norm_num) (by norm_num [r28Order54Support])
    (by norm_num [r28Order54Support]) (by norm_num [zarankiewiczNumber])

/-- The order-56 affine recurrence first reaches the same comparison value at
781 edges. -/
theorem r28_order56_edge_threshold :
    deletionEdgeThreshold 56 r28Order55Support.slope
      r28Order55Support.intercept r28Order55Support.scale
      (zarankiewiczNumber 28) = 781 := by
  norm_num [deletionEdgeThreshold, r28Order55Support, zarankiewiczNumber,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order56_reaches_zarankiewicz_iff (edgeCount : ℕ) :
    781 ≤ edgeCount ↔
      zarankiewiczNumber 28 ≤
        deletionRecurrenceBound 56 r28Order55Support.slope
          r28Order55Support.intercept r28Order55Support.scale edgeCount := by
  rw [← r28_order56_edge_threshold]
  exact deletionEdgeThreshold_le_iff (by norm_num) (by norm_num [r28Order55Support])
    (by norm_num [r28Order55Support]) (by norm_num [zarankiewiczNumber])

end AlbertsonSamplingMechanism

#print axioms AlbertsonSamplingMechanism.deletionEdgeThreshold_le_iff
#print axioms AlbertsonSamplingMechanism.r28_order55_edge_threshold
#print axioms AlbertsonSamplingMechanism.r28_order55_reaches_zarankiewicz_iff
#print axioms AlbertsonSamplingMechanism.r28_order56_edge_threshold
#print axioms AlbertsonSamplingMechanism.r28_order56_reaches_zarankiewicz_iff
