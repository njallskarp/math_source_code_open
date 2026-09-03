import Mathlib

open scoped BigOperators
open Finset

namespace AlbertsonIntegralSampling

/-- The number of fixed supports in `features` that are wholly visible in a
vertex sample `S`.  Edges have two-element supports; crossings in a good
drawing have four-element supports. -/
def supportedCount {α ι : Type*} [DecidableEq α] [DecidableEq ι]
    (features : Finset ι) (support : ι → Finset α) (S : Finset α) : ℕ :=
  #(features.filter fun x ↦ support x ⊆ S)

/-- A `k`-element support is visible in exactly
`choose (|U|-k) (s-k)` of the `s`-element samples of `U`.  Summing over a
finite family gives the reusable incidence identity used in induced-subgraph
sampling arguments. -/
theorem sum_supportedCount_powersetCard
    {α ι : Type*} [DecidableEq α] [DecidableEq ι]
    (U : Finset α) (features : Finset ι) (support : ι → Finset α) (k s : ℕ)
    (hsubset : ∀ x ∈ features, support x ⊆ U)
    (hcard : ∀ x ∈ features, #(support x) = k) (hks : k ≤ s) :
    (∑ S ∈ U.powersetCard s, supportedCount features support S) =
      #features * Nat.choose (#U - k) (s - k) := by
  calc
    (∑ S ∈ U.powersetCard s, supportedCount features support S) =
        ∑ S ∈ U.powersetCard s, ∑ x ∈ features, if support x ⊆ S then 1 else 0 := by
      apply Finset.sum_congr rfl
      intro S hS
      simp [supportedCount]
    _ = ∑ x ∈ features, ∑ S ∈ U.powersetCard s, if support x ⊆ S then 1 else 0 := by
      rw [Finset.sum_comm]
    _ = ∑ x ∈ features, Nat.choose (#U - k) (s - k) := by
      apply Finset.sum_congr rfl
      intro x hx
      rw [Finset.sum_boole]
      simpa [hcard x hx] using
        Finset.card_filter_powersetCard_subset (support x) U s (hsubset x hx)
          (by simpa [hcard x hx] using hks)
    _ = #features * Nat.choose (#U - k) (s - k) := by simp

/-- At sample order 24, the published rational local bound
`c ≥ 5m - (203/9)(24-2)` and integrality sharpen to
`5m ≤ c + 496`. -/
theorem local_integral_rounding_24
    {m c : ℕ}
    (h : (((5 * m : ℕ) : ℚ) - (203 : ℚ) / 9 * 22) ≤ (c : ℚ)) :
    5 * m ≤ c + 496 := by
  by_contra hnot
  have hgap : c + 497 ≤ 5 * m := by omega
  have hgapQ : (c : ℚ) + 497 ≤ ((5 * m : ℕ) : ℚ) := by exact_mod_cast hgap
  norm_num at h hgapQ
  linarith

/-- If every `s`-vertex sample satisfies the local inequality
`a * edges ≤ crossings + d`, double counting two- and four-vertex supports
gives the corresponding global integer inequality. -/
theorem fixed_support_sampling_bound
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (s a d : ℕ)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4s : 4 ≤ s)
    (hlocal : ∀ S ∈ U.powersetCard s,
      a * supportedCount edges edgeSupport S ≤
        supportedCount crossings crossingSupport S + d) :
    a * #edges * Nat.choose (#U - 2) (s - 2) ≤
      #crossings * Nat.choose (#U - 4) (s - 4) + d * Nat.choose #U s := by
  have hsum :
      (∑ S ∈ U.powersetCard s, a * supportedCount edges edgeSupport S) ≤
        ∑ S ∈ U.powersetCard s, (supportedCount crossings crossingSupport S + d) :=
    Finset.sum_le_sum fun S hS ↦ hlocal S hS
  have hedge_sum := sum_supportedCount_powersetCard U edges edgeSupport 2 s
    hedges_subset hedges_card (by omega)
  have hcrossing_sum := sum_supportedCount_powersetCard U crossings crossingSupport 4 s
    hcrossings_subset hcrossings_card h4s
  calc
    a * #edges * Nat.choose (#U - 2) (s - 2) =
        ∑ S ∈ U.powersetCard s, a * supportedCount edges edgeSupport S := by
      rw [Nat.mul_assoc, ← hedge_sum, Finset.mul_sum]
    _ ≤ ∑ S ∈ U.powersetCard s,
        (supportedCount crossings crossingSupport S + d) := hsum
    _ = #crossings * Nat.choose (#U - 4) (s - 4) +
        d * Nat.choose #U s := by
      rw [Finset.sum_add_distrib, hcrossing_sum]
      simp [Finset.card_powersetCard, Nat.mul_comm]

/-- The exact integer arithmetic at the order-54 Albertson frontier. -/
theorem order54_floor_of_averaged_inequality
    {crossings : ℕ}
    (h : 5 * 726 * Nat.choose 52 22 ≤
      crossings * Nat.choose 50 20 + 496 * Nat.choose 54 24) :
    6076 ≤ crossings := by
  norm_num [Nat.choose] at h ⊢
  omega

/-- The exact locally rounded average reported at the order-54 frontier. -/
theorem order54_integral_average_value :
    ((((5 * 726 * Nat.choose 52 22 : ℕ) : ℚ) -
      ((496 * Nat.choose 54 24 : ℕ) : ℚ)) /
        ((Nat.choose 50 20 : ℕ) : ℚ)) = (10759164 : ℚ) / 1771 := by
  norm_num [Nat.choose]

/-- The locally rounded 24-vertex inequality forces at least 6076 crossings
for 726 two-vertex supports on a 54-element universe. -/
theorem albertson_order54_integral_sampling
    {α ε χ : Type*} [Fintype α]
    [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (hcard : Fintype.card α = 54) (hedges : #edges = 726)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hlocal : ∀ S ∈ (Finset.univ : Finset α).powersetCard 24,
      5 * supportedCount edges edgeSupport S ≤
        supportedCount crossings crossingSupport S + 496) :
    6076 ≤ #crossings := by
  apply order54_floor_of_averaged_inequality
  simpa [hcard, hedges] using
    fixed_support_sampling_bound (Finset.univ : Finset α) edges crossings
      edgeSupport crossingSupport 24 5 496
      (fun _ _ ↦ Finset.subset_univ _)
      hedges_card
      (fun _ _ ↦ Finset.subset_univ _)
      hcrossings_card
      (by omega)
      hlocal

/-- The order-54 conclusion stated directly from the rational local crossing
bound of Büngener--Kaufmann, applied to every 24-vertex sample.  Distinct
crossings are allowed to have the same four-vertex support. -/
theorem albertson_order54_of_published_local_bound
    {α ε χ : Type*} [Fintype α]
    [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (hcard : Fintype.card α = 54) (hedges : #edges = 726)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hlocal : ∀ S ∈ (Finset.univ : Finset α).powersetCard 24,
      ((((5 * supportedCount edges edgeSupport S : ℕ) : ℚ) -
        (203 : ℚ) / 9 * 22) ≤
          (supportedCount crossings crossingSupport S : ℚ))) :
    6076 ≤ #crossings := by
  apply albertson_order54_integral_sampling edges crossings edgeSupport crossingSupport
    hcard hedges hedges_card hcrossings_card
  intro S hS
  exact local_integral_rounding_24 (hlocal S hS)

#print axioms sum_supportedCount_powersetCard
#print axioms local_integral_rounding_24
#print axioms fixed_support_sampling_bound
#print axioms order54_floor_of_averaged_inequality
#print axioms order54_integral_average_value
#print axioms albertson_order54_integral_sampling
#print axioms albertson_order54_of_published_local_bound

end AlbertsonIntegralSampling
