import AlbertsonDeletionThreshold

/-!
# Exact recurrence gate for the order-57, `r = 29` Albertson frontier

This file instantiates the parameterized one-vertex-deletion recurrence at
order 57.  Three sparse affine supports of the exact order-56 table cover the
edge window 824--829.  Lean checks all recurrence values and proves that every
one of the three supports has the same exact `Z(29)` threshold, namely 829.

The final theorem is deliberately conditional: applicability of the selected
support and the order-56 local crossing bounds remain explicit hypotheses.
No separator-profile classification, critical-graph structure, drawing
topology, or claim about the five rows 824--828 is imported.
-/

namespace AlbertsonSamplingMechanism

/-- Order-56 table support active at the order-57 mean for edge count 824. -/
def r29Order56Support824 : SparseAffineSupport where
  slope := 129
  intercept := 72328
  scale := 4
  left := 792
  right := 796

/-- Order-56 table support active at the order-57 means for edge counts
825--827. -/
def r29Order56Support825to827 : SparseAffineSupport where
  slope := 65
  intercept := 36562
  scale := 2
  left := 796
  right := 798

/-- Order-56 table support active at the order-57 means for edge counts
828--829. -/
def r29Order56Support828to829 : SparseAffineSupport where
  slope := 33
  intercept := 18680
  scale := 1
  left := 798
  right := 804

/-- The finite set of supports needed for the order-57 threshold window. -/
def IsR29Order56WindowSupport (cert : SparseAffineSupport) : Prop :=
  cert = r29Order56Support824 ∨
    cert = r29Order56Support825to827 ∨
      cert = r29Order56Support828to829

theorem r29_zarankiewicz_value : zarankiewiczNumber 29 = 8281 := by
  norm_num [zarankiewiczNumber]

/-- The external subdivision-free critical-edge inequality rounds to 824 at
`(r,n)=(29,57)`.  Only the rounding is checked here. -/
theorem r29_order57_edge_floor :
    subdivisionFreeCriticalEdgeBound 29 57 = 824 := by
  norm_num [subdivisionFreeCriticalEdgeBound, Nat.ceilDiv_eq_add_pred_div]

/-! The rational deletion means lie in the declared active intervals. -/

theorem r29_m824_support_window :
    r29Order56Support824.left * 57 ≤ 824 * (57 - 2) ∧
      824 * (57 - 2) ≤ r29Order56Support824.right * 57 := by
  norm_num [r29Order56Support824]

theorem r29_m825_to_m827_support_window (edgeCount : ℕ)
    (hlo : 825 ≤ edgeCount) (hhi : edgeCount ≤ 827) :
    r29Order56Support825to827.left * 57 ≤ edgeCount * (57 - 2) ∧
      edgeCount * (57 - 2) ≤ r29Order56Support825to827.right * 57 := by
  simp only [r29Order56Support825to827]
  omega

theorem r29_m828_to_m829_support_window (edgeCount : ℕ)
    (hlo : 828 ≤ edgeCount) (hhi : edgeCount ≤ 829) :
    r29Order56Support828to829.left * 57 ≤ edgeCount * (57 - 2) ∧
      edgeCount * (57 - 2) ≤ r29Order56Support828to829.right * 57 := by
  simp only [r29Order56Support828to829]
  omega

/-! Exact rational-ceiling values for the complete numerical window. -/

theorem r29_order57_m824_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support824.slope
      r29Order56Support824.intercept r29Order56Support824.scale 824 = 8131 := by
  norm_num [deletionRecurrenceBound, r29Order56Support824,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_m825_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support825to827.slope
      r29Order56Support825to827.intercept
      r29Order56Support825to827.scale 825 = 8164 := by
  norm_num [deletionRecurrenceBound, r29Order56Support825to827,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_m826_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support825to827.slope
      r29Order56Support825to827.intercept
      r29Order56Support825to827.scale 826 = 8198 := by
  norm_num [deletionRecurrenceBound, r29Order56Support825to827,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_m827_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support825to827.slope
      r29Order56Support825to827.intercept
      r29Order56Support825to827.scale 827 = 8232 := by
  norm_num [deletionRecurrenceBound, r29Order56Support825to827,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_m828_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support828to829.slope
      r29Order56Support828to829.intercept
      r29Order56Support828to829.scale 828 = 8266 := by
  norm_num [deletionRecurrenceBound, r29Order56Support828to829,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_m829_recursive_value :
    deletionRecurrenceBound 57 r29Order56Support828to829.slope
      r29Order56Support828to829.intercept
      r29Order56Support828to829.scale 829 = 8300 := by
  norm_num [deletionRecurrenceBound, r29Order56Support828to829,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order57_open_row_gaps :
    zarankiewiczNumber 29 - 8131 = 150 ∧
      zarankiewiczNumber 29 - 8164 = 117 ∧
      zarankiewiczNumber 29 - 8198 = 83 ∧
      zarankiewiczNumber 29 - 8232 = 49 ∧
      zarankiewiczNumber 29 - 8266 = 15 := by
  norm_num [zarankiewiczNumber]

theorem r29_order57_m829_surplus :
    8300 - zarankiewiczNumber 29 = 19 := by
  norm_num [zarankiewiczNumber]

/-- All three active supports independently invert to the same exact edge
threshold. -/
theorem r29_order57_selected_support_threshold
    (cert : SparseAffineSupport) (hcert : IsR29Order56WindowSupport cert) :
    deletionEdgeThreshold 57 cert.slope cert.intercept cert.scale
      (zarankiewiczNumber 29) = 829 := by
  rcases hcert with rfl | rfl | rfl <;>
    norm_num [deletionEdgeThreshold, zarankiewiczNumber,
      r29Order56Support824, r29Order56Support825to827,
      r29Order56Support828to829, Nat.ceilDiv_eq_add_pred_div]

/-- For any support used in the order-57 window, the affine deletion recurrence
reaches `Z(29)` exactly from edge count 829 onward. -/
theorem r29_order57_reaches_zarankiewicz_iff
    (cert : SparseAffineSupport) (hcert : IsR29Order56WindowSupport cert)
    (edgeCount : ℕ) :
    829 ≤ edgeCount ↔
      zarankiewiczNumber 29 ≤
        deletionRecurrenceBound 57 cert.slope cert.intercept cert.scale
          edgeCount := by
  rw [← r29_order57_selected_support_threshold cert hcert]
  rcases hcert with rfl | rfl | rfl <;>
    exact deletionEdgeThreshold_le_iff (by norm_num)
      (by norm_num [r29Order56Support824, r29Order56Support825to827,
        r29Order56Support828to829])
      (by norm_num [r29Order56Support824, r29Order56Support825to827,
        r29Order56Support828to829])
      (by norm_num [zarankiewiczNumber])

/-- The theorem-aligned order-57 closure.  Once an applicable checked support
and the local order-56 lower bounds are supplied, 829 edges force at least
`Z(29)` abstract crossing occurrences. -/
theorem r29_order57_closed_from_829
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ) (cert : SparseAffineSupport)
    (hUcard : U.card = 57) (hedgeCount : 829 ≤ edges.card)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, (edgeSupport e).card = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, (crossingSupport x).card = 4)
    (hselected : IsR29Order56WindowSupport cert)
    (hcert : cert.IsActiveAtRatio F 1540 (edges.card * (57 - 2)) 57)
    (hedgeRange : ∀ v ∈ U,
      supportedCount edges edgeSupport (U.erase v) ≤ 1540)
    (hlocal : ∀ v ∈ U,
      F (supportedCount edges edgeSupport (U.erase v)) ≤
        supportedCount crossings crossingSupport (U.erase v)) :
    zarankiewiczNumber 29 ≤ crossings.card := by
  have hrecurrence := deletion_recurrence_of_active_support U edges crossings
    edgeSupport crossingSupport F cert 1540 57 hUcard hedges_subset hedges_card
    hcrossings_subset hcrossings_card (by norm_num) hcert hedgeRange hlocal
  exact ((r29_order57_reaches_zarankiewicz_iff cert hselected edges.card).1
    hedgeCount).trans hrecurrence

end AlbertsonSamplingMechanism

#print axioms AlbertsonSamplingMechanism.r29_m824_support_window
#print axioms AlbertsonSamplingMechanism.r29_order57_m824_recursive_value
#print axioms AlbertsonSamplingMechanism.r29_order57_open_row_gaps
#print axioms AlbertsonSamplingMechanism.r29_order57_selected_support_threshold
#print axioms AlbertsonSamplingMechanism.r29_order57_reaches_zarankiewicz_iff
#print axioms AlbertsonSamplingMechanism.r29_order57_closed_from_829
