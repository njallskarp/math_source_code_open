import SamplingFixture

open Finset IntegerMixture SamplingFixture

#print axioms sum_two_values
#print axioms exists_two_values_of_count
#print axioms exists_two_values_iff_count
#print axioms exists_two_values_iff_dvd
#print axioms sum_affine
#print axioms affine_sum_le
#print axioms affine_sum_eq_iff
#print axioms exists_affine_attainment_iff
#print axioms row7_minorant
#print axioms row7_contacts
#print axioms no_relaxed_attainment
#print axioms population_cost_ge
#print axioms witness_correct
#print axioms minimum_cost
#print axioms row7
#print axioms witness

example : ∃ q : Fin 0 → ℤ, (∀ i, q i = -3 ∨ q i = 2) ∧ ∑ i, q i = 0 := by
  rw [exists_two_values_iff_dvd 0 0 (-3) 2 (by norm_num)]
  norm_num

example : ¬ ∃ q : Fin 0 → ℤ, (∀ i, q i = -3 ∨ q i = 2) ∧ ∑ i, q i = 1 := by
  rw [exists_two_values_iff_dvd 0 1 (-3) 2 (by norm_num)]
  norm_num

example : ∃ q : Fin 3 → ℤ, (∀ i, q i = -3 ∨ q i = 1) ∧ ∑ i, q i = -5 := by
  rw [exists_two_values_iff_dvd 3 (-5) (-3) 1 (by norm_num)]
  norm_num

example : ¬ ∃ q : Fin 1 → ℤ, (∀ i, q i = 0 ∨ q i = 2) ∧ ∑ i, q i = 1 := by
  rw [exists_two_values_iff_dvd 1 1 0 2 (by norm_num)]
  norm_num

example : ¬ ∃ q : Fin 2 → ℤ, (∀ i, q i = 0 ∨ q i = 2) ∧ ∑ i, q i = 6 := by
  rw [exists_two_values_iff_dvd 2 6 0 2 (by norm_num)]
  norm_num

example : ¬ ∃ q : Fin 2 → ℤ, (∀ i, q i = 0 ∨ q i = 2) ∧ ∑ i, q i = -2 := by
  rw [exists_two_values_iff_dvd 2 (-2) 0 2 (by norm_num)]
  norm_num

example : ∃ q : Fin 36 → ℤ, (∀ i, q i = 19 ∨ q i = 21) ∧ ∑ i, q i = 694 := by
  rw [exists_two_values_iff_dvd 36 694 19 21 (by norm_num)]
  norm_num

example : (9 : ℕ).choose 7 = 36 ∧ 33 * (7 : ℕ).choose 5 = 693 ∧
    (5 : ℕ).choose 3 = 10 := by decide

example : (315 / 2 : ℚ) < 158 := by norm_num

-- Coincident endpoints belong to the count theorem, not the strict-order one.
example : ∃ q : Fin 3 → ℤ, (∀ i, q i = 2 ∨ q i = 2) ∧ ∑ i, q i = 6 := by
  rw [exists_two_values_iff_count]
  exact ⟨0, by decide, by norm_num⟩

example : ∃ q : Fin 36 → ℤ, (∀ i, q i ∈ Icc (0 : ℤ) 21) ∧
    (∑ i, q i) = 694 ∧ (∑ i, (row7 (q i) : ℚ)) = 159 := by
  have h := exists_affine_attainment_iff 36 694 19 21 (by norm_num)
    (Icc (0 : ℤ) 21) (by decide) (by decide) (fun x => (row7 x : ℚ))
    (3 / 2) (-(49 / 2))
    (by intro x hx; simpa only [sub_eq_add_neg] using row7_minorant x hx)
    (by intro x hx; simpa only [sub_eq_add_neg] using row7_contacts x hx)
  norm_num at h
  simpa only [mem_Icc] using h

-- An additional contact can attain the affine value without endpoint mixing.
example : (∃ q : Fin 1 → ℤ, (∑ i, q i) = 1 ∧
    (∑ i, (q i : ℚ)) = 1) ∧ ¬ (2 : ℤ) ∣ 1 := by
  refine ⟨⟨fun _ => 1, ?_, ?_⟩, by decide⟩ <;> norm_num
