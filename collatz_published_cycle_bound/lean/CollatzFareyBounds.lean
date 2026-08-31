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

/-! ## Current published phase -/

theorem current_denominator_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    137528045312 ≤ k := by
  omega

theorem current_shortcut_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    217976794617 ≤ n := by
  omega

theorem current_classical_bound (n k : Nat)
    (h_lower : 103768467013 * k < 65470613321 * n)
    (h_upper : 72057431991 * n < 114208327604 * k) :
    355504839929 ≤ n + k := by
  omega

/-! ## Next phase after excluding the current upper convergent -/

theorem next_denominator_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    890638885193 ≤ k := by
  omega

theorem next_shortcut_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    1411629234715 ≤ n := by
  omega

theorem next_classical_bound (n k : Nat)
    (h_lower : 1193652440098 * k < 753110839881 * n)
    (h_upper : 137528045312 * n < 217976794617 * k) :
    2302268119908 ≤ n + k := by
  omega

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

end CollatzFareyBounds
