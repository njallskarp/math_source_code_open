import Lean.Elab.Tactic.Omega

/-!
# Downward closure in a contracting Collatz cylinder

The arithmetic core is independent of Collatz. If `B < A`, the affine lift
endpoint `z + B*t` grows more slowly than the lift start `n + A*t`.
Consequently non-descent at one lift forces non-descent at the base and at
every smaller lift.
-/

namespace CollatzCSTCylinder

/-- A non-descending lift of a contracting affine cylinder forces its base
endpoint to be non-descending. -/
theorem contractingLiftForcesBase (n z A B t : Nat)
    (hcontract : B < A)
    (hlift : n + A * t ≤ z + B * t) :
    n ≤ z := by
  have hBt : B * t ≤ A * t :=
    Nat.mul_le_mul_right t (Nat.le_of_lt hcontract)
  omega

/-- A positive non-descending lift forces strict growth at the base. -/
theorem positiveContractingLiftForcesStrictBase (n z A B t : Nat)
    (hcontract : B < A) (ht : 0 < t)
    (hlift : n + A * t ≤ z + B * t) :
    n < z := by
  have hgap : 0 < (A - B) * t := by
    exact Nat.mul_pos (Nat.sub_pos_of_lt hcontract) ht
  have hB : B ≤ A := Nat.le_of_lt hcontract
  have hsplit : A * t = (A - B) * t + B * t := by
    calc
      A * t = ((A - B) + B) * t := by rw [Nat.sub_add_cancel hB]
      _ = (A - B) * t + B * t := by rw [Nat.add_mul]
  omega

/-- The non-descending lift parameters of a contracting cylinder are
downward-closed. -/
theorem contractingLiftDownwardClosed (n z A B t u : Nat)
    (hcontract : B < A) (hu : u ≤ t)
    (hlift : n + A * t ≤ z + B * t) :
    n + A * u ≤ z + B * u := by
  have hbase : n ≤ z := contractingLiftForcesBase n z A B t hcontract hlift
  have hB : B ≤ A := Nat.le_of_lt hcontract
  have hsplitT : A * t = (A - B) * t + B * t := by
    calc
      A * t = ((A - B) + B) * t := by rw [Nat.sub_add_cancel hB]
      _ = (A - B) * t + B * t := by rw [Nat.add_mul]
  have hboundT : (A - B) * t ≤ z - n := by
    have hz : z = n + (z - n) := by omega
    omega
  have hboundU : (A - B) * u ≤ z - n := by
    exact Nat.le_trans (Nat.mul_le_mul_left (A - B) hu) hboundT
  have hsplitU : A * u = (A - B) * u + B * u := by
    calc
      A * u = ((A - B) + B) * u := by rw [Nat.sub_add_cancel hB]
      _ = (A - B) * u + B * u := by rw [Nat.add_mul]
  have hz : z = n + (z - n) := by omega
  omega

/-- Shortcut-Collatz specialization with `A=2^k` and `B=3^q`. -/
theorem collatzCylinderDownwardClosed (n z k q t u : Nat)
    (hcontract : 3 ^ q < 2 ^ k) (hu : u ≤ t)
    (hlift : n + 2 ^ k * t ≤ z + 3 ^ q * t) :
    n + 2 ^ k * u ≤ z + 3 ^ q * u := by
  exact contractingLiftDownwardClosed n z (2 ^ k) (3 ^ q) t u
    hcontract hu hlift

#print axioms contractingLiftForcesBase
#print axioms positiveContractingLiftForcesStrictBase
#print axioms contractingLiftDownwardClosed
#print axioms collatzCylinderDownwardClosed

end CollatzCSTCylinder
