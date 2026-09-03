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

/-- A `k`-element support inside `U` survives deletion of exactly `|U|-k`
vertices.  This is the vertex-deletion analogue of
`sum_supportedCount_powersetCard`; feature identifiers keep the statement
multiplicity-safe when several features have the same support. -/
theorem sum_supportedCount_erase
    {α ι : Type*} [DecidableEq α] [DecidableEq ι]
    (U : Finset α) (features : Finset ι) (support : ι → Finset α) (k : ℕ)
    (hsubset : ∀ x ∈ features, support x ⊆ U)
    (hcard : ∀ x ∈ features, #(support x) = k) :
    (∑ v ∈ U, supportedCount features support (U.erase v)) =
      #features * (#U - k) := by
  calc
    (∑ v ∈ U, supportedCount features support (U.erase v)) =
        ∑ v ∈ U, ∑ x ∈ features,
          if support x ⊆ U.erase v then 1 else 0 := by
      apply Finset.sum_congr rfl
      intro v hv
      simp [supportedCount]
    _ = ∑ x ∈ features, ∑ v ∈ U,
          if support x ⊆ U.erase v then 1 else 0 := by
      rw [Finset.sum_comm]
    _ = ∑ x ∈ features, (#U - k) := by
      apply Finset.sum_congr rfl
      intro x hx
      have hfilter :
          U.filter (fun v ↦ support x ⊆ U.erase v) = U \ support x := by
        ext v
        simp [Finset.subset_erase, hsubset x hx]
      have hcount :
          #(U.filter (fun v ↦ support x ⊆ U.erase v)) = #U - k := by
        rw [hfilter, Finset.card_sdiff_of_subset (hsubset x hx), hcard x hx]
      simpa using hcount
    _ = #features * (#U - k) := by simp

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

/-- The improved order-54 arithmetic if every 24-vertex sample satisfies the
one-unit stronger local inequality with deficit 495. -/
theorem order54_floor_of_local495_averaged_inequality
    {crossings : ℕ}
    (h : 5 * 726 * Nat.choose 52 22 ≤
      crossings * Nat.choose 50 20 + 495 * Nat.choose 54 24) :
    6105 ≤ crossings := by
  norm_num [Nat.choose] at h ⊢
  omega

/-- The exact average associated with the proposed 24-vertex obstruction. -/
theorem order54_local495_average_value :
    ((((5 * 726 * Nat.choose 52 22 : ℕ) : ℚ) -
      ((495 * Nat.choose 54 24 : ℕ) : ℚ)) /
        ((Nat.choose 50 20 : ℕ) : ℚ)) = (1965795 : ℚ) / 322 := by
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

/-- The sampling consequence of a uniform deficit-495 theorem on all
24-vertex induced subdrawings.  In the graph result this uniform theorem is
reduced to the local obstruction `cr(24,132) ≥ 165`; that reduction remains
outside this finite-support interface. -/
theorem albertson_order54_of_local495
    {α ε χ : Type*} [Fintype α]
    [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (hcard : Fintype.card α = 54) (hedges : #edges = 726)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hlocal : ∀ S ∈ (Finset.univ : Finset α).powersetCard 24,
      5 * supportedCount edges edgeSupport S ≤
        supportedCount crossings crossingSupport S + 495) :
    6105 ≤ #crossings := by
  apply order54_floor_of_local495_averaged_inequality
  simpa [hcard, hedges] using
    fixed_support_sampling_bound (Finset.univ : Finset α) edges crossings
      edgeSupport crossingSupport 24 5 495
      (fun _ _ ↦ Finset.subset_univ _)
      hedges_card
      (fun _ _ ↦ Finset.subset_univ _)
      hcrossings_card
      (by omega)
      hlocal

/-- Summing the reviewed vertex-deletion inequalities over a 54-element
universe.  Here `excess v` represents `degree v - 26`; the handshake and
minimum-degree arguments enter only through the exact total `48`.

The pointwise hypothesis is the subtraction-free form of
`deleted v ≥ 5650 - 27 * excess v`. -/
theorem order54_deleted_sum_lower_bound
    {α : Type*} [Fintype α]
    (deleted excess : α → ℕ)
    (hcard : Fintype.card α = 54)
    (hexcess : ∑ v, excess v = 48)
    (hlocal : ∀ v, 5650 ≤ deleted v + 27 * excess v) :
    303804 ≤ ∑ v, deleted v := by
  have hsum : (∑ v : α, (5650 : ℕ)) ≤
      ∑ v : α, (deleted v + 27 * excess v) := by
    exact Finset.sum_le_sum fun v _ ↦ hlocal v
  simp [Finset.sum_add_distrib, ← Finset.mul_sum, hcard, hexcess] at hsum
  omega

/-- The finite handshake arithmetic behind the degree-excess total.  The
graph-theoretic facts `sum degree = 2 * 726` and `degree v ≥ 26` remain outside
this lemma; the latter is represented constructively by `degree v = 26 +
excess v`. -/
theorem order54_degree_excess_total
    {α : Type*} [Fintype α]
    (degree excess : α → ℕ)
    (hcard : Fintype.card α = 54)
    (hdegreeSum : ∑ v, degree v = 1452)
    (hdecomp : ∀ v, degree v = 26 + excess v) :
    ∑ v, excess v = 48 := by
  have hsumDecomp : (∑ v, degree v) = ∑ v, (26 + excess v) := by
    apply Finset.sum_congr rfl
    intro v hv
    exact hdecomp v
  simp [Finset.sum_add_distrib, hcard] at hsumDecomp
  omega

/-- The final exact ceiling step: `303804 / 50 = 6076.08`. -/
theorem order54_floor_of_two_stage_inequality
    {crossings : ℕ} (h : 303804 ≤ 50 * crossings) :
    6077 ≤ crossings := by
  omega

/-- The bounded two-stage implication underlying the independently reviewed
Albertson `r = 27`, order-54 refinement.  A feature is a crossing occurrence
of a fixed drawing and its support is its four distinct endpoints.  Deleting
a vertex retains exactly the features whose supports avoid it, so the generic
deletion identity gives the coefficient `54 - 4 = 50`.

No graph or drawing topology is modeled here.  The pointwise local inequality,
the four-endpoint property, and the degree-excess total are the explicit
interface to those external arguments. -/
theorem albertson_order54_two_stage_deletion
    {α χ : Type*} [Fintype α]
    [DecidableEq α] [DecidableEq χ]
    (crossings : Finset χ) (crossingSupport : χ → Finset α)
    (excess : α → ℕ)
    (hcard : Fintype.card α = 54)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hexcess : ∑ v, excess v = 48)
    (hlocal : ∀ v,
      5650 ≤ supportedCount crossings crossingSupport
        ((Finset.univ : Finset α).erase v) + 27 * excess v) :
    303804 ≤ 50 * #crossings ∧ 6077 ≤ #crossings := by
  have hsumLower :
      303804 ≤ ∑ v, supportedCount crossings crossingSupport
        ((Finset.univ : Finset α).erase v) :=
    order54_deleted_sum_lower_bound
      (fun v ↦ supportedCount crossings crossingSupport
        ((Finset.univ : Finset α).erase v))
      excess hcard hexcess hlocal
  have hsumExact :
      (∑ v, supportedCount crossings crossingSupport
        ((Finset.univ : Finset α).erase v)) = #crossings * 50 := by
    simpa [hcard] using
      sum_supportedCount_erase (Finset.univ : Finset α) crossings
        crossingSupport 4
        (fun _ _ ↦ Finset.subset_univ _)
        hcrossings_card
  rw [hsumExact] at hsumLower
  constructor
  · simpa [Nat.mul_comm] using hsumLower
  · apply order54_floor_of_two_stage_inequality
    simpa [Nat.mul_comm] using hsumLower

#print axioms sum_supportedCount_powersetCard
#print axioms sum_supportedCount_erase
#print axioms local_integral_rounding_24
#print axioms fixed_support_sampling_bound
#print axioms order54_floor_of_averaged_inequality
#print axioms order54_integral_average_value
#print axioms order54_floor_of_local495_averaged_inequality
#print axioms order54_local495_average_value
#print axioms albertson_order54_integral_sampling
#print axioms albertson_order54_of_published_local_bound
#print axioms albertson_order54_of_local495
#print axioms order54_deleted_sum_lower_bound
#print axioms order54_degree_excess_total
#print axioms order54_floor_of_two_stage_inequality
#print axioms albertson_order54_two_stage_deletion

end AlbertsonIntegralSampling
