import IntegerMixture
import Mathlib.Tactic.IntervalCases
import Mathlib.Data.Int.Interval

/-!
The literal order-seven table is checked here, not imported from Python.
Its agreement with the height-2713 program is an external exact replay.
The population need not arise as all induced subgraphs of one graph.
-/

open Finset IntegerMixture

namespace SamplingFixture

/-- The 22 entries, on `0..21`: sixteen zeroes, then `1,2,3,4,6,7`. -/
def row7 (x : ℤ) : ℤ :=
  if x ≤ 19 then max 0 (x - 15) else if x = 20 then 6 else 7

theorem row7_minorant (x : ℤ) (hx : x ∈ Icc (0 : ℤ) 21) :
    (3 / 2 : ℚ) * x - 49 / 2 ≤ (row7 x : ℚ) := by
  simp only [mem_Icc] at hx
  obtain ⟨h0, h21⟩ := hx
  interval_cases x <;> norm_num [row7]

theorem row7_contacts (x : ℤ) (hx : x ∈ Icc (0 : ℤ) 21) :
    (row7 x : ℚ) = (3 / 2 : ℚ) * x - 49 / 2 ↔ x = 19 ∨ x = 21 := by
  simp only [mem_Icc] at hx
  obtain ⟨h0, h21⟩ := hx
  interval_cases x <;> norm_num [row7]

/-- The actual parameter fixture fails the formal divisibility criterion. -/
theorem no_relaxed_attainment :
    ¬ ∃ q : Fin 36 → ℤ, (∀ i, q i ∈ Icc (0 : ℤ) 21) ∧
      (∑ i, q i) = 693 ∧ (∑ i, (row7 (q i) : ℚ)) = 315 / 2 := by
  have h := exists_affine_attainment_iff 36 693 19 21 (by norm_num)
    (Icc (0 : ℤ) 21) (by decide) (by decide) (fun x => (row7 x : ℚ))
    (3 / 2) (-(49 / 2))
    (by intro x hx; simpa only [sub_eq_add_neg] using row7_minorant x hx)
    (by intro x hx; simpa only [sub_eq_add_neg] using row7_contacts x hx)
  norm_num at h ⊢
  exact h

/-- The integer minimum is at least 158, from the still-valid affine bound. -/
theorem population_cost_ge (q : Fin 36 → ℤ)
    (hD : ∀ i, q i ∈ Icc (0 : ℤ) 21) (hT : ∑ i, q i = 693) :
    158 ≤ ∑ i, row7 (q i) := by
  have h := affine_sum_le q (fun x => (row7 x : ℚ)) (3 / 2) (-(49 / 2))
    (fun i => by simpa only [sub_eq_add_neg] using row7_minorant (q i) (hD i))
  rw [hT] at h
  have hq : (315 : ℚ) ≤ 2 * ((∑ i, row7 (q i) : ℤ) : ℚ) := by
    push_cast
    linarith
  have hz : (315 : ℤ) ≤ 2 * ∑ i, row7 (q i) := by exact_mod_cast hq
  omega

/-- Four entries of 21, one of 20, and thirty-one of 19. -/
def witness (i : Fin 36) : ℤ :=
  if i.val < 4 then 21 else if i.val = 4 then 20 else 19

theorem witness_correct :
    (∀ i, witness i ∈ Icc (0 : ℤ) 21) ∧
      (∑ i, witness i) = 693 ∧ (∑ i, row7 (witness i)) = 158 := by
  decide

/-- Exact minimum over all domain-valid populations of this size and total. -/
theorem minimum_cost : IsLeast
    {c : ℤ | ∃ q : Fin 36 → ℤ, (∀ i, q i ∈ Icc (0 : ℤ) 21) ∧
      (∑ i, q i) = 693 ∧ (∑ i, row7 (q i)) = c} 158 := by
  refine ⟨⟨witness, witness_correct⟩, ?_⟩
  rintro c ⟨q, hD, hT, hc⟩
  rw [← hc]
  exact population_cost_ge q hD hT

end SamplingFixture
