import Mathlib.Algebra.Order.Floor.Div
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Sum
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/-!
# Parameterized induced sampling and sparse affine supports

This file isolates the finite combinatorial kernel behind integer-aware and
convex-minorant sampling arguments for crossing-number lower bounds.  It does
not define graph drawings or crossing number.  Edges and crossing occurrences
are abstract identifiers with two- and four-vertex supports.
-/

open scoped BigOperators
open Finset

namespace AlbertsonSamplingMechanism

/-- Number of feature identifiers whose complete support is visible in `S`.
Identifiers are separate from supports, so coincident supports retain their
multiplicity. -/
def supportedCount {α ι : Type*} [DecidableEq α] [DecidableEq ι]
    (features : Finset ι) (support : ι → Finset α) (S : Finset α) : ℕ :=
  #(features.filter fun x ↦ support x ⊆ S)

/-- A family of `k`-supported features is seen in exactly
`choose (|U|-k) (s-k)` samples per feature. -/
theorem sum_supportedCount_powersetCard
    {α ι : Type*} [DecidableEq α] [DecidableEq ι]
    (U : Finset α) (features : Finset ι) (support : ι → Finset α) (k s : ℕ)
    (hsubset : ∀ x ∈ features, support x ⊆ U)
    (hcard : ∀ x ∈ features, #(support x) = k) (hks : k ≤ s) :
    (∑ S ∈ U.powersetCard s, supportedCount features support S) =
      #features * Nat.choose (#U - k) (s - k) := by
  calc
    (∑ S ∈ U.powersetCard s, supportedCount features support S) =
        ∑ S ∈ U.powersetCard s,
          ∑ x ∈ features, if support x ⊆ S then 1 else 0 := by
      apply Finset.sum_congr rfl
      intro S hS
      simp [supportedCount]
    _ = ∑ x ∈ features,
        ∑ S ∈ U.powersetCard s, if support x ⊆ S then 1 else 0 := by
      rw [Finset.sum_comm]
    _ = ∑ x ∈ features, Nat.choose (#U - k) (s - k) := by
      apply Finset.sum_congr rfl
      intro x hx
      rw [Finset.sum_boole]
      simpa [hcard x hx] using
        Finset.card_filter_powersetCard_subset (support x) U s (hsubset x hx)
          (by simpa [hcard x hx] using hks)
    _ = #features * Nat.choose (#U - k) (s - k) := by simp

/-- A `k`-supported feature survives exactly `|U|-k` single-vertex
deletions. -/
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

/-- Summed fixed-support consequence of the local scaled affine inequality
`slope * e_S ≤ scale * c_S + intercept`. -/
theorem affine_sampling_inequality
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (n s slope intercept scale : ℕ)
    (hUcard : #U = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4s : 4 ≤ s)
    (hlocal : ∀ S ∈ U.powersetCard s,
      slope * supportedCount edges edgeSupport S ≤
        scale * supportedCount crossings crossingSupport S + intercept) :
    slope * #edges * Nat.choose (n - 2) (s - 2) ≤
      scale * #crossings * Nat.choose (n - 4) (s - 4) +
        intercept * Nat.choose n s := by
  have hsum :
      (∑ S ∈ U.powersetCard s,
          slope * supportedCount edges edgeSupport S) ≤
        ∑ S ∈ U.powersetCard s,
          (scale * supportedCount crossings crossingSupport S + intercept) :=
    Finset.sum_le_sum fun S hS ↦ hlocal S hS
  have hedge_sum := sum_supportedCount_powersetCard U edges edgeSupport 2 s
    hedges_subset hedges_card (by omega)
  have hcrossing_sum := sum_supportedCount_powersetCard U crossings
    crossingSupport 4 s hcrossings_subset hcrossings_card h4s
  calc
    slope * #edges * Nat.choose (n - 2) (s - 2) =
        ∑ S ∈ U.powersetCard s,
          slope * supportedCount edges edgeSupport S := by
      rw [Nat.mul_assoc, ← hUcard, ← hedge_sum, Finset.mul_sum]
    _ ≤ ∑ S ∈ U.powersetCard s,
        (scale * supportedCount crossings crossingSupport S + intercept) := hsum
    _ = scale * #crossings * Nat.choose (n - 4) (s - 4) +
        intercept * Nat.choose n s := by
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, hcrossing_sum]
      simp [Finset.card_powersetCard, hUcard, Nat.mul_assoc, Nat.mul_comm]

/-- Exact natural-number ceiling of a sampled affine lower bound. -/
def sampledCeilBound
    (n s slope intercept scale edgeCount : ℕ) : ℕ :=
  (slope * edgeCount * Nat.choose (n - 2) (s - 2) -
      intercept * Nat.choose n s) ⌈/⌉
    (scale * Nat.choose (n - 4) (s - 4))

theorem sampledCeilBound_le_of_inequality
    {n s slope intercept scale edgeCount crossingCount : ℕ}
    (hscale : 0 < scale)
    (hchoose : 0 < Nat.choose (n - 4) (s - 4))
    (h : slope * edgeCount * Nat.choose (n - 2) (s - 2) ≤
      scale * crossingCount * Nat.choose (n - 4) (s - 4) +
        intercept * Nat.choose n s) :
    sampledCeilBound n s slope intercept scale edgeCount ≤ crossingCount := by
  rw [sampledCeilBound, ceilDiv_le_iff_le_mul (Nat.mul_pos hscale hchoose)]
  apply (Nat.sub_le_iff_le_add).2
  simpa [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using h

/-- Parameterized exact-ceiling sampling theorem for an arbitrary scaled
affine local inequality. -/
theorem affine_sampling_ceiling
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (n s slope intercept scale : ℕ)
    (hUcard : #U = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4s : 4 ≤ s) (hsn : s ≤ n) (hscale : 0 < scale)
    (hlocal : ∀ S ∈ U.powersetCard s,
      slope * supportedCount edges edgeSupport S ≤
        scale * supportedCount crossings crossingSupport S + intercept) :
    sampledCeilBound n s slope intercept scale #edges ≤ #crossings := by
  apply sampledCeilBound_le_of_inequality hscale
    (Nat.choose_pos (by omega))
  exact affine_sampling_inequality U edges crossings edgeSupport crossingSupport
    n s slope intercept scale hUcard hedges_subset hedges_card
    hcrossings_subset hcrossings_card h4s hlocal

/-- Clearing a positive denominator and using Euclidean division turns a
rational intercept into its exact natural-number floor. -/
theorem le_add_div_of_mul_le_add
    {x y numerator denominator : ℕ} (hden : 0 < denominator)
    (h : denominator * x ≤ denominator * y + numerator) :
    x ≤ y + numerator / denominator := by
  by_cases hxy : x ≤ y
  · exact hxy.trans (Nat.le_add_right y _)
  · have hyx : y ≤ x := by omega
    have hmul : denominator * (x - y) ≤ numerator := by
      have hdecomp :
          denominator * x = denominator * (x - y) + denominator * y := by
        rw [Nat.mul_sub_left_distrib, Nat.sub_add_cancel]
        exact Nat.mul_le_mul_left denominator hyx
      omega
    have hdiv : x - y ≤ numerator / denominator :=
      (Nat.le_div_iff_mul_le hden).2 (by simpa [Nat.mul_comm] using hmul)
    exact (Nat.sub_le_iff_le_add').1 hdiv

/-- Local integer rounding for the cleared-denominator inequality
`denominator * slope * e ≤ denominator * c + numerator * (s-2)`. -/
theorem local_floor_of_scaled_affine
    {s slope numerator denominator edgeCount crossingCount : ℕ}
    (hden : 0 < denominator)
    (h : denominator * (slope * edgeCount) ≤
      denominator * crossingCount + numerator * (s - 2)) :
    slope * edgeCount ≤
      crossingCount + (numerator * (s - 2)) / denominator :=
  le_add_div_of_mul_le_add hden h

/-- Arbitrary-`(n,s)` integer-aware induced sampling from a local rational
affine line after exact denominator clearing.  The inner `/` is the local
floor and `sampledCeilBound` is the final global ceiling. -/
theorem integer_aware_affine_sampling
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (n s slope numerator denominator : ℕ)
    (hUcard : #U = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4s : 4 ≤ s) (hsn : s ≤ n) (hden : 0 < denominator)
    (hlocal : ∀ S ∈ U.powersetCard s,
      denominator * (slope * supportedCount edges edgeSupport S) ≤
        denominator * supportedCount crossings crossingSupport S +
          numerator * (s - 2)) :
    sampledCeilBound n s slope ((numerator * (s - 2)) / denominator) 1
      #edges ≤ #crossings := by
  apply affine_sampling_ceiling U edges crossings edgeSupport crossingSupport
    n s slope ((numerator * (s - 2)) / denominator) 1 hUcard
    hedges_subset hedges_card hcrossings_subset hcrossings_card h4s hsn
    (by omega)
  intro S hS
  simpa using local_floor_of_scaled_affine hden (hlocal S hS)

/-- A sparse rational affine support `slope*x/scale-intercept/scale`, together
with the integer interval on which it is active. -/
structure SparseAffineSupport where
  slope : ℕ
  intercept : ℕ
  scale : ℕ
  left : ℕ
  right : ℕ
  deriving DecidableEq, Repr

namespace SparseAffineSupport

/-- The scaled affine line lies below the integer table on its whole declared
domain. -/
def IsMinorant (cert : SparseAffineSupport) (F : ℕ → ℕ) (maxEdges : ℕ) : Prop :=
  0 < cert.scale ∧
    ∀ q, q ≤ maxEdges → cert.slope * q ≤ cert.scale * F q + cert.intercept

/-- Besides minorant validity, the line meets the table at both endpoints and
the queried rational mean lies in their interval. -/
def IsActiveAtRatio (cert : SparseAffineSupport) (F : ℕ → ℕ)
    (maxEdges numerator denominator : ℕ) : Prop :=
  cert.IsMinorant F maxEdges ∧
    cert.left ≤ cert.right ∧ cert.right ≤ maxEdges ∧
    cert.slope * cert.left = cert.scale * F cert.left + cert.intercept ∧
    cert.slope * cert.right = cert.scale * F cert.right + cert.intercept ∧
    cert.left * denominator ≤ numerator ∧ numerator ≤ cert.right * denominator

end SparseAffineSupport

/-- Numerator of the mean number of edges in an `s`-vertex induced sample. -/
def meanEdgeNumerator (s edgeCount : ℕ) : ℕ :=
  edgeCount * s * (s - 1)

/-- Denominator of the mean number of edges in an induced sample. -/
def meanEdgeDenominator (n : ℕ) : ℕ := n * (n - 1)

/-- A sparse active affine support for any integer lower-bound table supplies
the full convex-minorant sampling step.  Convex-hull construction is not
trusted here: validity of the selected support is an explicit hypothesis. -/
theorem sampling_recurrence_of_active_support
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ) (cert : SparseAffineSupport) (maxEdges n s : ℕ)
    (hUcard : #U = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4s : 4 ≤ s) (hsn : s ≤ n)
    (hcert : cert.IsActiveAtRatio F maxEdges
      (meanEdgeNumerator s #edges) (meanEdgeDenominator n))
    (hedgeRange : ∀ S ∈ U.powersetCard s,
      supportedCount edges edgeSupport S ≤ maxEdges)
    (hlocal : ∀ S ∈ U.powersetCard s,
      F (supportedCount edges edgeSupport S) ≤
        supportedCount crossings crossingSupport S) :
    sampledCeilBound n s cert.slope cert.intercept cert.scale #edges ≤
      #crossings := by
  apply affine_sampling_ceiling U edges crossings edgeSupport crossingSupport
    n s cert.slope cert.intercept cert.scale hUcard hedges_subset hedges_card
    hcrossings_subset hcrossings_card h4s hsn hcert.1.1
  intro S hS
  exact (hcert.1.2 _ (hedgeRange S hS)).trans
    (Nat.add_le_add_right (Nat.mul_le_mul_left cert.scale (hlocal S hS)) _)

/-- Exact ceiling produced by one vertex-deletion recurrence. -/
def deletionRecurrenceBound
    (n slope intercept scale edgeCount : ℕ) : ℕ :=
  (slope * edgeCount * (n - 2) - intercept * n) ⌈/⌉
    (scale * (n - 4))

/-- Abstract convex-minorant deletion recurrence.  Two-supported edges survive
`n-2` deletions and four-supported crossing occurrences survive exactly
`n-4` deletions. -/
theorem deletion_recurrence_of_active_support
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ) (cert : SparseAffineSupport) (maxEdges n : ℕ)
    (hUcard : #U = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (h4n : 4 < n)
    (hcert : cert.IsActiveAtRatio F maxEdges (#edges * (n - 2)) n)
    (hedgeRange : ∀ v ∈ U,
      supportedCount edges edgeSupport (U.erase v) ≤ maxEdges)
    (hlocal : ∀ v ∈ U,
      F (supportedCount edges edgeSupport (U.erase v)) ≤
        supportedCount crossings crossingSupport (U.erase v)) :
    deletionRecurrenceBound n cert.slope cert.intercept cert.scale #edges ≤
      #crossings := by
  have hpoint : ∀ v ∈ U,
      cert.slope * supportedCount edges edgeSupport (U.erase v) ≤
        cert.scale * supportedCount crossings crossingSupport (U.erase v) +
          cert.intercept := by
    intro v hv
    exact (hcert.1.2 _ (hedgeRange v hv)).trans
      (Nat.add_le_add_right (Nat.mul_le_mul_left cert.scale (hlocal v hv)) _)
  have hsum :
      (∑ v ∈ U,
          cert.slope * supportedCount edges edgeSupport (U.erase v)) ≤
        ∑ v ∈ U,
          (cert.scale * supportedCount crossings crossingSupport (U.erase v) +
            cert.intercept) :=
    Finset.sum_le_sum fun v hv ↦ hpoint v hv
  have hedge_sum := sum_supportedCount_erase U edges edgeSupport 2
    hedges_subset hedges_card
  have hcrossing_sum := sum_supportedCount_erase U crossings crossingSupport 4
    hcrossings_subset hcrossings_card
  have hglobal :
      cert.slope * #edges * (n - 2) ≤
        cert.scale * #crossings * (n - 4) + cert.intercept * n := by
    calc
      cert.slope * #edges * (n - 2) =
          ∑ v ∈ U,
            cert.slope * supportedCount edges edgeSupport (U.erase v) := by
        rw [Nat.mul_assoc, ← hUcard, ← hedge_sum, Finset.mul_sum]
      _ ≤ ∑ v ∈ U,
          (cert.scale * supportedCount crossings crossingSupport (U.erase v) +
            cert.intercept) := hsum
      _ = cert.scale * #crossings * (n - 4) + cert.intercept * n := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, hcrossing_sum]
        simp [hUcard, Nat.mul_assoc, Nat.mul_comm]
  rw [deletionRecurrenceBound,
    ceilDiv_le_iff_le_mul (Nat.mul_pos hcert.1.1 (by omega))]
  apply (Nat.sub_le_iff_le_add).2
  simpa [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using hglobal

/-! Exact diagnostic specializations. -/

/-- Active order-54 affine support selected by the exact recurrence checker. -/
def r28Order54Support : SparseAffineSupport where
  slope := 91
  intercept := 47708
  scale := 3
  left := 740
  right := 743

/-- Active order-55 affine support selected by the exact recurrence checker. -/
def r28Order55Support : SparseAffineSupport where
  slope := 59
  intercept := 31220
  scale := 2
  left := 752
  right := 754

/-- The exact order-55 recurrence value once the order-54 support is supplied. -/
theorem r28_order55_recursive_value :
    deletionRecurrenceBound 55 r28Order54Support.slope
      r28Order54Support.intercept r28Order54Support.scale 768 = 7060 := by
  norm_num [deletionRecurrenceBound, r28Order54Support,
    Nat.ceilDiv_eq_add_pred_div]

/-- The exact order-56 recurrence value once the order-55 support is supplied. -/
theorem r28_order56_recursive_value :
    deletionRecurrenceBound 56 r28Order55Support.slope
      r28Order55Support.intercept r28Order55Support.scale 781 = 7115 := by
  norm_num [deletionRecurrenceBound, r28Order55Support,
    Nat.ceilDiv_eq_add_pred_div]

/-- Concrete order-55 instance of the abstract deletion recurrence.  Validity
of the checker-selected order-54 support remains an explicit hypothesis. -/
theorem r28_order55_recursive_bound
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ)
    (hUcard : #U = 55) (hedgeCount : #edges = 768)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hcert : r28Order54Support.IsActiveAtRatio F 1431
      (#edges * (55 - 2)) 55)
    (hedgeRange : ∀ v ∈ U,
      supportedCount edges edgeSupport (U.erase v) ≤ 1431)
    (hlocal : ∀ v ∈ U,
      F (supportedCount edges edgeSupport (U.erase v)) ≤
        supportedCount crossings crossingSupport (U.erase v)) :
    7060 ≤ #crossings := by
  have hglobal := deletion_recurrence_of_active_support U edges crossings
    edgeSupport crossingSupport F r28Order54Support 1431 55 hUcard
    hedges_subset hedges_card hcrossings_subset hcrossings_card (by norm_num)
    hcert hedgeRange hlocal
  simpa [hedgeCount, r28Order54Support, deletionRecurrenceBound,
    Nat.ceilDiv_eq_add_pred_div] using hglobal

/-- Concrete order-56 instance of the abstract deletion recurrence.  Validity
of the checker-selected order-55 support remains an explicit hypothesis. -/
theorem r28_order56_recursive_bound
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ)
    (hUcard : #U = 56) (hedgeCount : #edges = 781)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, #(edgeSupport e) = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, #(crossingSupport x) = 4)
    (hcert : r28Order55Support.IsActiveAtRatio F 1485
      (#edges * (56 - 2)) 56)
    (hedgeRange : ∀ v ∈ U,
      supportedCount edges edgeSupport (U.erase v) ≤ 1485)
    (hlocal : ∀ v ∈ U,
      F (supportedCount edges edgeSupport (U.erase v)) ≤
        supportedCount crossings crossingSupport (U.erase v)) :
    7115 ≤ #crossings := by
  have hglobal := deletion_recurrence_of_active_support U edges crossings
    edgeSupport crossingSupport F r28Order55Support 1485 56 hUcard
    hedges_subset hedges_card hcrossings_subset hcrossings_card (by norm_num)
    hcert hedgeRange hlocal
  simpa [hedgeCount, r28Order55Support, deletionRecurrenceBound,
    Nat.ceilDiv_eq_add_pred_div] using hglobal

/-- The standard four-factor drawing value used as the Albertson comparison
threshold.  Its relevance to complete-graph crossing number is external. -/
def zarankiewiczNumber (r : ℕ) : ℕ :=
  (r / 2) * ((r - 1) / 2) * ((r - 2) / 2) * ((r - 3) / 2) / 4

theorem r28_zarankiewicz_value : zarankiewiczNumber 28 = 7098 := by
  norm_num [zarankiewiczNumber]

theorem r28_order56_recursive_exceeds_zarankiewicz :
    zarankiewiczNumber 28 <
      deletionRecurrenceBound 56 r28Order55Support.slope
        r28Order55Support.intercept r28Order55Support.scale 781 := by
  norm_num [zarankiewiczNumber, deletionRecurrenceBound, r28Order55Support,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order55_m768_recursive_gap :
    zarankiewiczNumber 28 -
      deletionRecurrenceBound 55 r28Order54Support.slope
        r28Order54Support.intercept r28Order54Support.scale 768 = 38 := by
  norm_num [zarankiewiczNumber, deletionRecurrenceBound, r28Order54Support,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order55_m769_recursive_value :
    deletionRecurrenceBound 55 r28Order54Support.slope
      r28Order54Support.intercept r28Order54Support.scale 769 = 7092 := by
  norm_num [deletionRecurrenceBound, r28Order54Support,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order55_m770_recursive_value :
    deletionRecurrenceBound 55 r28Order54Support.slope
      r28Order54Support.intercept r28Order54Support.scale 770 = 7123 := by
  norm_num [deletionRecurrenceBound, r28Order54Support,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order55_m770_exceeds_zarankiewicz :
    zarankiewiczNumber 28 <
      deletionRecurrenceBound 55 r28Order54Support.slope
        r28Order54Support.intercept r28Order54Support.scale 770 := by
  norm_num [zarankiewiczNumber, deletionRecurrenceBound, r28Order54Support,
    Nat.ceilDiv_eq_add_pred_div]

theorem r28_order56_m781_recursive_surplus :
    deletionRecurrenceBound 56 r28Order55Support.slope
        r28Order55Support.intercept r28Order55Support.scale 781 -
      zarankiewiczNumber 28 = 17 := by
  norm_num [zarankiewiczNumber, deletionRecurrenceBound, r28Order55Support,
    Nat.ceilDiv_eq_add_pred_div]

/-- Integer edge threshold supplied by the external critical-graph inequality
`2m ≥ (r-1)n + (2r-6)`.  This definition only rounds the stated arithmetic
bound; the graph-theoretic inequality itself is outside this file. -/
def subdivisionFreeCriticalEdgeBound (r n : ℕ) : ℕ :=
  ((r - 1) * n + (2 * r - 6)) ⌈/⌉ 2

theorem r28_order55_edge_input :
    subdivisionFreeCriticalEdgeBound 28 55 = 768 := by
  norm_num [subdivisionFreeCriticalEdgeBound, Nat.ceilDiv_eq_add_pred_div]

theorem r28_order56_edge_input :
    subdivisionFreeCriticalEdgeBound 28 56 = 781 := by
  norm_num [subdivisionFreeCriticalEdgeBound, Nat.ceilDiv_eq_add_pred_div]

theorem historical_order54_direct :
    sampledCeilBound 54 24 5 496 1 726 = 6076 := by
  norm_num [sampledCeilBound, Nat.choose, Nat.ceilDiv_eq_add_pred_div]

theorem historical_order53_714_from_50_line :
    sampledCeilBound 53 50 26 11706 1 714 = 6100 := by
  norm_num [sampledCeilBound, Nat.choose, Nat.ceilDiv_eq_add_pred_div]

theorem historical_order53_715_from_50_line :
    sampledCeilBound 53 50 26 11706 1 715 = 6129 := by
  norm_num [sampledCeilBound, Nat.choose, Nat.ceilDiv_eq_add_pred_div]

/-- Direct published-line diagnostic at the natural `(55,768)` `r=28` input. -/
theorem r28_order55_direct :
    sampledCeilBound 55 24 5 496 1 768 = 6988 := by
  norm_num [sampledCeilBound, Nat.choose, Nat.ceilDiv_eq_add_pred_div]

/-- Direct published-line diagnostic at the natural `(56,781)` `r=28` input. -/
theorem r28_order56_direct :
    sampledCeilBound 56 25 5 518 1 781 = 7048 := by
  norm_num [sampledCeilBound, Nat.choose, Nat.ceilDiv_eq_add_pred_div]

#print axioms sum_supportedCount_powersetCard
#print axioms sum_supportedCount_erase
#print axioms affine_sampling_inequality
#print axioms sampledCeilBound_le_of_inequality
#print axioms affine_sampling_ceiling
#print axioms le_add_div_of_mul_le_add
#print axioms local_floor_of_scaled_affine
#print axioms integer_aware_affine_sampling
#print axioms sampling_recurrence_of_active_support
#print axioms deletion_recurrence_of_active_support
#print axioms r28_order55_recursive_value
#print axioms r28_order56_recursive_value
#print axioms r28_order55_recursive_bound
#print axioms r28_order56_recursive_bound
#print axioms r28_zarankiewicz_value
#print axioms r28_order56_recursive_exceeds_zarankiewicz
#print axioms r28_order55_m768_recursive_gap
#print axioms r28_order55_m769_recursive_value
#print axioms r28_order55_m770_recursive_value
#print axioms r28_order55_m770_exceeds_zarankiewicz
#print axioms r28_order56_m781_recursive_surplus
#print axioms r28_order55_edge_input
#print axioms r28_order56_edge_input
#print axioms historical_order54_direct
#print axioms historical_order53_714_from_50_line
#print axioms historical_order53_715_from_50_line
#print axioms r28_order55_direct
#print axioms r28_order56_direct

end AlbertsonSamplingMechanism
