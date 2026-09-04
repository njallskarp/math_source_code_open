import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Order.Interval.Finset.Fin
import Lean.Elab.Tactic.Omega

/-!
# Location bounds for two fixed points in a 123-avoiding permutation

This file formalizes the finite-order reduction at the start of the proof of
the distance-two fixed-point slice for `Av(123)`.  Positions and values are
zero-based elements of `Fin n`.
-/

namespace Av123FixedPointLocation

/-- A permutation avoids the classical pattern `123`. -/
def Avoids123 {n : ℕ} (π : Equiv.Perm (Fin n)) : Prop :=
  ∀ ⦃i j k : Fin n⦄, i < j → j < k →
    ¬(π i < π j ∧ π j < π k)

/-- Before two fixed points, every value lies above the first fixed value. -/
theorem maps_before_first_above {n : ℕ} {π : Equiv.Perm (Fin n)}
    {a b : Fin n} (havoid : Avoids123 π) (hab : a < b)
    (hfixa : π a = a) (hfixb : π b = b) :
    ∀ ⦃i : Fin n⦄, i < a → a < π i := by
  intro i hia
  have hnot : ¬π i < a := by
    intro hil
    exact havoid hia hab ⟨by simpa [hfixa] using hil,
      by simpa [hfixa, hfixb] using hab⟩
  have hle : a ≤ π i := le_of_not_gt hnot
  have hne : π i ≠ a := by
    intro h
    have hi_eq : i = a := π.injective (by simpa [hfixa] using h)
    exact (ne_of_lt hia) hi_eq
  exact lt_of_le_of_ne hle hne.symm

/-- After two fixed points, every value lies below the second fixed value. -/
theorem maps_after_second_below {n : ℕ} {π : Equiv.Perm (Fin n)}
    {a b : Fin n} (havoid : Avoids123 π) (hab : a < b)
    (hfixa : π a = a) (hfixb : π b = b) :
    ∀ ⦃i : Fin n⦄, b < i → π i < b := by
  intro i hbi
  have hnot : ¬b < π i := by
    intro hhigh
    exact havoid hab hbi ⟨by simpa [hfixa, hfixb] using hab,
      by simpa [hfixb] using hhigh⟩
  have hle : π i ≤ b := le_of_not_gt hnot
  have hne : π i ≠ b := by
    intro h
    have hi_eq : i = b := π.injective (by simpa [hfixb] using h)
    exact (ne_of_gt hbi) hi_eq
  exact lt_of_le_of_ne hle hne

/-- There must be enough values strictly above `a`, other than the second
fixed value `b`, to receive all positions before `a`. -/
theorem first_fixed_cardinality_bound {n : ℕ} {π : Equiv.Perm (Fin n)}
    {a b : Fin n} (havoid : Avoids123 π) (hab : a < b)
    (hfixa : π a = a) (hfixb : π b = b) :
    a.val ≤ n - 1 - a.val - 1 := by
  classical
  have hsubset : (Finset.Iio a).image π ⊆ (Finset.Ioi a).erase b := by
    intro x hx
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hx
    have hia : i < a := Finset.mem_Iio.mp hi
    refine Finset.mem_erase.mpr ⟨?_, Finset.mem_Ioi.mpr
      (maps_before_first_above havoid hab hfixa hfixb hia)⟩
    intro h
    have hi_eq : i = b := π.injective (by simpa [hfixb] using h)
    exact (ne_of_lt (lt_trans hia hab)) hi_eq
  have hcard := Finset.card_le_card hsubset
  rw [Finset.card_image_of_injective _ π.injective] at hcard
  simpa [Finset.card_erase_of_mem (Finset.mem_Ioi.mpr hab)] using hcard

/-- There must be enough values strictly below `b`, other than the first
fixed value `a`, to receive all positions after `b`. -/
theorem second_fixed_cardinality_bound {n : ℕ} {π : Equiv.Perm (Fin n)}
    {a b : Fin n} (havoid : Avoids123 π) (hab : a < b)
    (hfixa : π a = a) (hfixb : π b = b) :
    n - 1 - b.val ≤ b.val - 1 := by
  classical
  have hsubset : (Finset.Ioi b).image π ⊆ (Finset.Iio b).erase a := by
    intro x hx
    obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hx
    have hbi : b < i := Finset.mem_Ioi.mp hi
    refine Finset.mem_erase.mpr ⟨?_, Finset.mem_Iio.mpr
      (maps_after_second_below havoid hab hfixa hfixb hbi)⟩
    intro h
    have hi_eq : i = a := π.injective (by simpa [hfixa] using h)
    exact (ne_of_gt (lt_trans hab hbi)) hi_eq
  have hcard := Finset.card_le_card hsubset
  rw [Finset.card_image_of_injective _ π.injective] at hcard
  simpa [Finset.card_erase_of_mem (Finset.mem_Iio.mpr hab)] using hcard

/-- The two structural bounds, specialized to fixed points at distance two. -/
theorem distance_two_fixed_point_bounds {n : ℕ} {π : Equiv.Perm (Fin n)}
    {a b : Fin n} (havoid : Avoids123 π) (hgap : a.val + 2 = b.val)
    (hfixa : π a = a) (hfixb : π b = b) :
    a.val ≤ n - 1 - a.val - 1 ∧ n - 1 - b.val ≤ b.val - 1 := by
  have hab : a < b := by
    change a.val < b.val
    omega
  exact ⟨first_fixed_cardinality_bound havoid hab hfixa hfixb,
    second_fixed_cardinality_bound havoid hab hfixa hfixb⟩

/-- In even size `2m`, the first zero-based fixed-point location is `m-2` or
`m-1`; the second is two positions later.  In one-based notation these are
the pairs `(m-1,m+1)` and `(m,m+2)`. -/
theorem even_distance_two_fixed_point_locations {m : ℕ} (hm : 2 ≤ m)
    {π : Equiv.Perm (Fin (2 * m))} {a b : Fin (2 * m)}
    (havoid : Avoids123 π) (hgap : a.val + 2 = b.val)
    (hfixa : π a = a) (hfixb : π b = b) :
    (a.val = m - 2 ∧ b.val = m) ∨
      (a.val = m - 1 ∧ b.val = m + 1) := by
  have hbounds := distance_two_fixed_point_bounds havoid hgap hfixa hfixb
  have ha_lt : a.val < 2 * m := a.isLt
  have hb_lt : b.val < 2 * m := b.isLt
  omega

/-- In odd size `2m+1`, the unique zero-based fixed-point pair at distance
two is `(m-1,m+1)`, or `(m,m+2)` in one-based notation. -/
theorem odd_distance_two_fixed_point_locations {m : ℕ} (hm : 2 ≤ m)
    {π : Equiv.Perm (Fin (2 * m + 1))} {a b : Fin (2 * m + 1)}
    (havoid : Avoids123 π) (hgap : a.val + 2 = b.val)
    (hfixa : π a = a) (hfixb : π b = b) :
    a.val = m - 1 ∧ b.val = m + 1 := by
  have hbounds := distance_two_fixed_point_bounds havoid hgap hfixa hfixb
  have ha_lt : a.val < 2 * m + 1 := a.isLt
  have hb_lt : b.val < 2 * m + 1 := b.isLt
  omega

#print axioms maps_before_first_above
#print axioms maps_after_second_below
#print axioms first_fixed_cardinality_bound
#print axioms second_fixed_cardinality_bound
#print axioms distance_two_fixed_point_bounds
#print axioms even_distance_two_fixed_point_locations
#print axioms odd_distance_two_fixed_point_locations

end Av123FixedPointLocation
