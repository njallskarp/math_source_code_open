import Lean.Elab.Tactic.Omega

/-!
# Machine-checked Diophantine bridges for Collatz cycle-length bounds

`n` denotes the shortcut-map cycle length and `k` the number of odd entries.
The hypotheses are cross-multiplied rational interval bounds.  This file does
not formalize the external analytic proof that a Collatz cycle lies in either
interval; it formalizes the exact discrete consequences once those strict
inequalities are available.
-/

namespace CollatzFareyBounds

/-! ## Generic Farey-neighbor certificate

If `a/b < n/k < c/d` and `b*c - a*d = 1`, the two positive
cross-product gaps give the exact identities

`k = b * (c*k - d*n) + d * (b*n - a*k)` and
`n = a * (c*k - d*n) + c * (b*n - a*k)`.

Consequently `k ≥ b+d` and `n ≥ a+c`.  This is the reusable theorem behind
both numerical phases below.
-/

theorem fareyNeighborBounds (a b c d n k : Nat)
    (h_lower : a * k < b * n)
    (h_upper : d * n < c * k)
    (h_det : b * c = a * d + 1) :
    b + d ≤ k ∧ a + c ≤ n := by
  let u := b * n - a * k
  let v := c * k - d * n
  have hu : 1 ≤ u := by simp [u]; omega
  have hv : 1 ≤ v := by simp [v]; omega
  have hu_eq : a * k + u = b * n := by simp [u]; omega
  have hv_eq : d * n + v = c * k := by simp [v]; omega
  have h_bv : b * d * n + b * v = b * c * k := by
    calc
      b * d * n + b * v = b * (d * n + v) := by
        simp [Nat.mul_add, Nat.mul_assoc]
      _ = b * (c * k) := by rw [hv_eq]
      _ = b * c * k := by simp [Nat.mul_assoc]
  have h_du : a * d * k + d * u = b * d * n := by
    calc
      a * d * k + d * u = d * (a * k + u) := by
        simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]
      _ = d * (b * n) := by rw [hu_eq]
      _ = b * d * n := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
  have h_det_k : b * c * k = a * d * k + k := by
    calc
      b * c * k = (a * d + 1) * k := by rw [h_det]
      _ = a * d * k + k := by simp [Nat.add_mul, Nat.mul_assoc]
  have h_k : b * v + d * u = k := by
    omega
  have h_av : a * d * n + a * v = a * c * k := by
    calc
      a * d * n + a * v = a * (d * n + v) := by
        simp [Nat.mul_add, Nat.mul_assoc]
      _ = a * (c * k) := by rw [hv_eq]
      _ = a * c * k := by simp [Nat.mul_assoc]
  have h_cu : a * c * k + c * u = b * c * n := by
    calc
      a * c * k + c * u = c * (a * k + u) := by
        simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]
      _ = c * (b * n) := by rw [hu_eq]
      _ = b * c * n := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
  have h_det_n : b * c * n = a * d * n + n := by
    calc
      b * c * n = (a * d + 1) * n := by rw [h_det]
      _ = a * d * n + n := by simp [Nat.add_mul, Nat.mul_assoc]
  have h_n : a * v + c * u = n := by
    omega
  have hb : b ≤ b * v := by
    simpa using Nat.mul_le_mul_left b hv
  have hd : d ≤ d * u := by
    simpa using Nat.mul_le_mul_left d hu
  have ha : a ≤ a * v := by
    simpa using Nat.mul_le_mul_left a hv
  have hc : c ≤ c * u := by
    simpa using Nat.mul_le_mul_left c hu
  constructor <;> omega

/-! ## Current published phase -/

private theorem current_phase_bounds (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    137528045312 ≤ k ∧ 217976794617 ≤ n := by
  have h := fareyNeighborBounds
    103768467013 65470613321 114208327604 72057431991 n k
    h_lower h_upper (by decide)
  omega

theorem current_denominator_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    137528045312 ≤ k := by
  exact (current_phase_bounds n k h_lower h_upper).1

theorem current_shortcut_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    217976794617 ≤ n := by
  exact (current_phase_bounds n k h_lower h_upper).2

theorem current_classical_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    355504839929 ≤ n + k := by
  have h := current_phase_bounds n k h_lower h_upper
  omega

/-! ## Next phase after excluding the current upper convergent -/

private theorem next_phase_bounds (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    890638885193 ≤ k ∧ 1411629234715 ≤ n := by
  have h := fareyNeighborBounds
    1193652440098 753110839881 217976794617 137528045312 n k
    h_lower h_upper (by decide)
  omega

theorem next_denominator_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    890638885193 ≤ k := by
  exact (next_phase_bounds n k h_lower h_upper).1

theorem next_shortcut_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    1411629234715 ≤ n := by
  exact (next_phase_bounds n k h_lower h_upper).2

theorem next_classical_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    2302268119908 ≤ n + k := by
  have h := next_phase_bounds n k h_lower h_upper
  omega

/-! ## Shortcut-to-classical parity-word bridge

An even shortcut step expands to one classical step.  An odd shortcut step
`(3x+1)/2` expands to the two classical steps `3x+1` and division by two.
The following combinatorial encoding makes the resulting length identity
explicit.  It does not prove that an arbitrary word is realized by a cycle.
-/

inductive ShortcutStepKind where
  | even
  | odd
  deriving DecidableEq

def oddCount : List ShortcutStepKind → Nat
  | [] => 0
  | ShortcutStepKind.even :: steps => oddCount steps
  | ShortcutStepKind.odd :: steps => oddCount steps + 1

def classicalExpansion : List ShortcutStepKind → List ShortcutStepKind
  | [] => []
  | ShortcutStepKind.even :: steps =>
      ShortcutStepKind.even :: classicalExpansion steps
  | ShortcutStepKind.odd :: steps =>
      ShortcutStepKind.odd :: ShortcutStepKind.even :: classicalExpansion steps

theorem classicalExpansion_length (steps : List ShortcutStepKind) :
    (classicalExpansion steps).length = steps.length + oddCount steps := by
  induction steps with
  | nil => rfl
  | cons step steps ih =>
      cases step <;> simp [classicalExpansion, oddCount, ih, Nat.add_assoc,
        Nat.add_comm, Nat.add_left_comm]

theorem classicalCycleLengthBridge (steps : List ShortcutStepKind) (n k : Nat)
    (h_length : steps.length = n)
    (h_odd : oddCount steps = k) :
    (classicalExpansion steps).length = n + k := by
  rw [classicalExpansion_length, h_length, h_odd]

theorem current_expanded_cycle_bound (steps : List ShortcutStepKind) (n k : Nat)
    (h_length : steps.length = n)
    (h_odd : oddCount steps = k)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    355504839929 ≤ (classicalExpansion steps).length := by
  rw [classicalCycleLengthBridge steps n k h_length h_odd]
  exact current_classical_bound n k h_lower h_upper

theorem next_expanded_cycle_bound (steps : List ShortcutStepKind) (n k : Nat)
    (h_length : steps.length = n)
    (h_odd : oddCount steps = k)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    2302268119908 ≤ (classicalExpansion steps).length := by
  rw [classicalCycleLengthBridge steps n k h_length h_odd]
  exact next_classical_bound n k h_lower h_upper

/-! ## Closed arithmetic witnesses and determinant-one certificates -/

theorem current_witness_lower :
    103768467013 * 137528045312 < 65470613321 * 217976794617 := by
  decide

theorem current_witness_upper :
    72057431991 * 217976794617 < 114208327604 * 137528045312 := by
  decide

theorem next_witness_lower :
    1193652440098 * 890638885193 < 753110839881 * 1411629234715 := by
  decide

theorem next_witness_upper :
    137528045312 * 1411629234715 < 217976794617 * 890638885193 := by
  decide

theorem current_left_det :
    217976794617 * 65470613321 = 103768467013 * 137528045312 + 1 := by
  decide

theorem current_right_det :
    114208327604 * 137528045312 = 217976794617 * 72057431991 + 1 := by
  decide

theorem next_left_det :
    1411629234715 * 753110839881 = 1193652440098 * 890638885193 + 1 := by
  decide

#print axioms current_denominator_bound
#print axioms current_shortcut_bound
#print axioms current_classical_bound
#print axioms next_denominator_bound
#print axioms next_shortcut_bound
#print axioms next_classical_bound
#print axioms fareyNeighborBounds
#print axioms classicalExpansion_length
#print axioms classicalCycleLengthBridge
#print axioms current_expanded_cycle_bound
#print axioms next_expanded_cycle_bound

end CollatzFareyBounds
