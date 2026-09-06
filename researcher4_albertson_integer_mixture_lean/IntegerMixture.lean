import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Lean.Elab.Tactic.Omega

/-!
# Finite integer mixtures and affine-bound attainment

The population is an actual function on `Fin N`. No graph, drawing, external
table or convex-hull implementation is assumed. The intended characterization
includes both the interval condition and the divisibility of `T - N*a` by
`b-a`; arbitrary real mixing weights do not supply integer multiplicities.
-/

open Finset

namespace IntegerMixture

/-- The sum of a two-valued population is determined by its upper count. -/
theorem sum_two_values {N : ℕ} (q : Fin N → ℤ) (a b : ℤ)
    (hq : ∀ i, q i = a ∨ q i = b) :
    ∑ i, q i = (N : ℤ) * a +
      ((univ.filter fun i => q i = b).card : ℤ) * (b - a) := by
  have hpoint : ∀ i, q i = a + (if q i = b then b - a else 0) := by
    intro i
    by_cases hb : q i = b
    · simp [hb]
    · have ha := (hq i).resolve_right hb
      simp only [if_neg hb]
      omega
  calc
    ∑ i, q i = ∑ i, (a + if q i = b then b - a else 0) :=
      sum_congr rfl (fun i _ => hpoint i)
    _ = _ := by
      rw [sum_add_distrib, ← sum_filter]
      simp only [sum_const, card_univ, Fintype.card_fin, nsmul_eq_mul]

/-- Any integer upper count between zero and `N` has an actual population. -/
theorem exists_two_values_of_count (N k : ℕ) (a b : ℤ) (hk : k ≤ N) :
    ∃ q : Fin N → ℤ, (∀ i, q i = a ∨ q i = b) ∧
      ∑ i, q i = (N : ℤ) * a + (k : ℤ) * (b - a) := by
  obtain ⟨S, _, hS⟩ := exists_subset_card_eq
    (show k ≤ (univ : Finset (Fin N)).card by simpa using hk)
  refine ⟨fun i => a + if i ∈ S then b - a else 0, ?_, ?_⟩
  · intro i
    by_cases hi : i ∈ S <;> simp [hi]
  · simp only [sum_add_distrib, sum_const, card_univ, Fintype.card_fin, nsmul_eq_mul]
    congr 1
    rw [← sum_filter]
    simp only [filter_mem_eq_inter, univ_inter, sum_const, hS, nsmul_eq_mul]

/-- Two-endpoint realization is equivalent to an integer count equation. -/
theorem exists_two_values_iff_count (N : ℕ) (T a b : ℤ) :
    (∃ q : Fin N → ℤ, (∀ i, q i = a ∨ q i = b) ∧ ∑ i, q i = T) ↔
      ∃ k : ℕ, k ≤ N ∧ T = (N : ℤ) * a + (k : ℤ) * (b - a) := by
  constructor
  · rintro ⟨q, hq, hsum⟩
    refine ⟨(univ.filter fun i => q i = b).card, ?_, ?_⟩
    · simpa using card_filter_le (s := (univ : Finset (Fin N))) (p := fun i => q i = b)
    · rw [← hsum]
      exact sum_two_values q a b hq
  · rintro ⟨k, hk, hT⟩
    obtain ⟨q, hq, hs⟩ := exists_two_values_of_count N k a b hk
    exact ⟨q, hq, hs.trans hT.symm⟩

/-- The exact interval and divisibility criterion; the empty population is
included. The strict endpoint order is essential. -/
theorem exists_two_values_iff_dvd (N : ℕ) (T a b : ℤ) (hab : a < b) :
    (∃ q : Fin N → ℤ, (∀ i, q i = a ∨ q i = b) ∧ ∑ i, q i = T) ↔
      (N : ℤ) * a ≤ T ∧ T ≤ (N : ℤ) * b ∧ b - a ∣ T - (N : ℤ) * a := by
  rw [exists_two_values_iff_count]
  constructor
  · rintro ⟨k, hk, hT⟩
    have hk0 : (0 : ℤ) ≤ k := Int.natCast_nonneg k
    have hkN : (k : ℤ) ≤ N := by exact_mod_cast hk
    refine ⟨?_, ?_, ⟨(k : ℤ), ?_⟩⟩ <;> nlinarith
  · rintro ⟨hlo, hhi, k, hk⟩
    have hk0 : 0 ≤ k := by nlinarith
    have hkN : k ≤ (N : ℤ) := by nlinarith
    refine ⟨k.toNat, ?_, ?_⟩
    · exact_mod_cast (show (k.toNat : ℤ) ≤ N by simpa [Int.toNat_of_nonneg hk0] using hkN)
    · rw [Int.toNat_of_nonneg hk0]
      nlinarith

/-- Summing an affine function only uses the population size and total. -/
theorem sum_affine {N : ℕ} (q : Fin N → ℤ) (m c : ℚ) :
    (∑ i, (m * (q i : ℚ) + c)) = m * (∑ i, q i : ℤ) + (N : ℚ) * c := by
  simp [sum_add_distrib, ← mul_sum]

/-- A pointwise affine minorant gives a bound, with no attainment premise. -/
theorem affine_sum_le {N : ℕ} (q : Fin N → ℤ) (F : ℤ → ℚ) (m c : ℚ)
    (h : ∀ i, m * (q i : ℚ) + c ≤ F (q i)) :
    m * (∑ i, q i : ℤ) + (N : ℚ) * c ≤ ∑ i, F (q i) := by
  rw [← sum_affine]
  exact sum_le_sum fun i _ => h i

/-- Equality in the summed minorant holds exactly when every entry is a
contact. The premise lists all contacts on the actual population. -/
theorem affine_sum_eq_iff {N : ℕ} (q : Fin N → ℤ) (F : ℤ → ℚ) (m c : ℚ)
    (a b : ℤ) (h : ∀ i, m * (q i : ℚ) + c ≤ F (q i))
    (hc : ∀ i, F (q i) = m * (q i : ℚ) + c ↔ q i = a ∨ q i = b) :
    (∑ i, F (q i)) = m * (∑ i, q i : ℤ) + (N : ℚ) * c ↔
      ∀ i, q i = a ∨ q i = b := by
  rw [← sum_affine, ← sub_eq_zero, ← sum_sub_distrib]
  rw [sum_eq_zero_iff_of_nonneg (fun i _ => sub_nonneg.mpr (h i))]
  simp only [mem_univ, true_implies, sub_eq_zero, hc]

/-- Corrected finite-population attainment theorem. The domain and all
contacts of the affine minorant are explicit; no hull algorithm is trusted. -/
theorem exists_affine_attainment_iff (N : ℕ) (T a b : ℤ) (hab : a < b)
    (D : Finset ℤ) (ha : a ∈ D) (hb : b ∈ D) (F : ℤ → ℚ) (m c : ℚ)
    (hminor : ∀ x ∈ D, m * (x : ℚ) + c ≤ F x)
    (hcontact : ∀ x ∈ D, F x = m * (x : ℚ) + c ↔ x = a ∨ x = b) :
    (∃ q : Fin N → ℤ, (∀ i, q i ∈ D) ∧ (∑ i, q i) = T ∧
      (∑ i, F (q i)) = m * (T : ℚ) + (N : ℚ) * c) ↔
      (N : ℤ) * a ≤ T ∧ T ≤ (N : ℤ) * b ∧ b - a ∣ T - (N : ℤ) * a := by
  rw [← exists_two_values_iff_dvd N T a b hab]
  constructor
  · rintro ⟨q, hD, hT, hsum⟩
    refine ⟨q, ?_, hT⟩
    apply (affine_sum_eq_iff q F m c a b
      (fun i => hminor _ (hD i)) (fun i => hcontact _ (hD i))).mp
    simpa [hT] using hsum
  · rintro ⟨q, hq, hT⟩
    have hD : ∀ i, q i ∈ D := by
      intro i
      rcases hq i with h | h <;> simp [h, ha, hb]
    refine ⟨q, hD, hT, ?_⟩
    have he := (affine_sum_eq_iff q F m c a b
      (fun i => hminor _ (hD i)) (fun i => hcontact _ (hD i))).mpr hq
    simpa [hT] using he

end IntegerMixture
