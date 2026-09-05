import AlbertsonDeletionThreshold

/-!
# Exact recurrence gate for the orders 56--59, `r = 29` Albertson frontier

This file instantiates the parameterized one-vertex-deletion recurrence at the
four boundary orders 56--59. Sparse affine supports of the preceding exact
tables cover every edge-threshold window and the three disconnected-complement
diagnostic rows. Lean checks all recurrence values and exact `Z(29)`
thresholds.

The final theorem is deliberately conditional: applicability of the selected
support and the order-56 local crossing bounds remain explicit hypotheses.
No separator-profile classification, critical-graph structure, drawing
topology, or claim about the five rows 824--828 is imported.
-/

namespace AlbertsonSamplingMechanism

/-- The composition of the abstract deletion recurrence with its exact
arithmetic threshold inverse. This is parameterized in the order, target,
support, table, and all finite support data. -/
theorem deletion_recurrence_closes_at_threshold
    {α ε χ : Type*} [DecidableEq α] [DecidableEq ε] [DecidableEq χ]
    (U : Finset α) (edges : Finset ε) (crossings : Finset χ)
    (edgeSupport : ε → Finset α) (crossingSupport : χ → Finset α)
    (F : ℕ → ℕ) (cert : SparseAffineSupport) (maxEdges n target : ℕ)
    (hUcard : U.card = n)
    (hedges_subset : ∀ e ∈ edges, edgeSupport e ⊆ U)
    (hedges_card : ∀ e ∈ edges, (edgeSupport e).card = 2)
    (hcrossings_subset : ∀ x ∈ crossings, crossingSupport x ⊆ U)
    (hcrossings_card : ∀ x ∈ crossings, (crossingSupport x).card = 4)
    (hn : 4 < n) (hslope : 0 < cert.slope) (hscale : 0 < cert.scale)
    (htarget : 0 < target)
    (hthreshold : deletionEdgeThreshold n cert.slope cert.intercept
      cert.scale target ≤ edges.card)
    (hcert : cert.IsActiveAtRatio F maxEdges (edges.card * (n - 2)) n)
    (hedgeRange : ∀ v ∈ U,
      supportedCount edges edgeSupport (U.erase v) ≤ maxEdges)
    (hlocal : ∀ v ∈ U,
      F (supportedCount edges edgeSupport (U.erase v)) ≤
        supportedCount crossings crossingSupport (U.erase v)) :
    target ≤ crossings.card := by
  have hrecurrence := deletion_recurrence_of_active_support U edges crossings
    edgeSupport crossingSupport F cert maxEdges n hUcard hedges_subset hedges_card
    hcrossings_subset hcrossings_card hn hcert hedgeRange hlocal
  exact ((deletionEdgeThreshold_le_iff hn hslope hscale htarget).1
    hthreshold).trans hrecurrence

/-- Arithmetic edge floor supplied by the external two-branch join estimate
for a critical graph with disconnected complement. The graph inequality is
not asserted by this definition. -/
def disconnectedComplementEdgeFloor (r n : ℕ) : ℕ :=
  Nat.min
    ((n - 1) + (((r - 2) * (n - 1)) ⌈/⌉ 2) + (r - 4))
    (r * r + 3 * r - 19)

theorem r29_candidate_order_edge_floors :
    subdivisionFreeCriticalEdgeBound 29 56 = 810 ∧
      subdivisionFreeCriticalEdgeBound 29 57 = 824 ∧
      subdivisionFreeCriticalEdgeBound 29 58 = 838 ∧
      subdivisionFreeCriticalEdgeBound 29 59 = 852 := by
  norm_num [subdivisionFreeCriticalEdgeBound, Nat.ceilDiv_eq_add_pred_div]

theorem r29_disconnected_complement_edge_floors :
    disconnectedComplementEdgeFloor 29 56 = 823 ∧
      disconnectedComplementEdgeFloor 29 57 = 837 ∧
      disconnectedComplementEdgeFloor 29 58 = 852 := by
  norm_num [disconnectedComplementEdgeFloor, Nat.ceilDiv_eq_add_pred_div]

/-! Order-56 threshold window, using supports of the order-55 table. -/

def r29Order55Support810to812 : SparseAffineSupport where
  slope := 97
  intercept := 53334
  scale := 3
  left := 780
  right := 783

def r29Order55Support813to814 : SparseAffineSupport where
  slope := 65
  intercept := 35817
  scale := 2
  left := 783
  right := 785

def r29Order55Support815to817 : SparseAffineSupport where
  slope := 33
  intercept := 18301
  scale := 1
  left := 785
  right := 791

def r29Order55SupportDisconnected823 : SparseAffineSupport where
  slope := 169
  intercept := 94672
  scale := 5
  left := 793
  right := 798

def IsR29Order55Support (cert : SparseAffineSupport) : Prop :=
  cert = r29Order55Support810to812 ∨
    cert = r29Order55Support813to814 ∨
      cert = r29Order55Support815to817 ∨
        cert = r29Order55SupportDisconnected823

theorem r29_order56_selected_support_threshold
    (cert : SparseAffineSupport) (hcert : IsR29Order55Support cert) :
    deletionEdgeThreshold 56 cert.slope cert.intercept cert.scale
      (zarankiewiczNumber 29) = 817 := by
  rcases hcert with rfl | rfl | rfl | rfl <;>
    norm_num [deletionEdgeThreshold, zarankiewiczNumber,
      r29Order55Support810to812, r29Order55Support813to814,
      r29Order55Support815to817, r29Order55SupportDisconnected823,
      Nat.ceilDiv_eq_add_pred_div]

theorem r29_order56_window_values :
    deletionRecurrenceBound 56 r29Order55Support810to812.slope
        r29Order55Support810to812.intercept r29Order55Support810to812.scale
        810 = 8052 ∧
    deletionRecurrenceBound 56 r29Order55Support810to812.slope
        r29Order55Support810to812.intercept r29Order55Support810to812.scale
        811 = 8086 ∧
    deletionRecurrenceBound 56 r29Order55Support810to812.slope
        r29Order55Support810to812.intercept r29Order55Support810to812.scale
        812 = 8119 ∧
    deletionRecurrenceBound 56 r29Order55Support813to814.slope
        r29Order55Support813to814.intercept r29Order55Support813to814.scale
        813 = 8153 ∧
    deletionRecurrenceBound 56 r29Order55Support813to814.slope
        r29Order55Support813to814.intercept r29Order55Support813to814.scale
        814 = 8187 ∧
    deletionRecurrenceBound 56 r29Order55Support815to817.slope
        r29Order55Support815to817.intercept r29Order55Support815to817.scale
        815 = 8221 ∧
    deletionRecurrenceBound 56 r29Order55Support815to817.slope
        r29Order55Support815to817.intercept r29Order55Support815to817.scale
        816 = 8255 ∧
    deletionRecurrenceBound 56 r29Order55Support815to817.slope
        r29Order55Support815to817.intercept r29Order55Support815to817.scale
        817 = 8290 := by
  norm_num [deletionRecurrenceBound, r29Order55Support810to812,
    r29Order55Support813to814, r29Order55Support815to817,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order56_disconnected_value :
    deletionRecurrenceBound 56 r29Order55SupportDisconnected823.slope
      r29Order55SupportDisconnected823.intercept
      r29Order55SupportDisconnected823.scale 823 = 8497 := by
  norm_num [deletionRecurrenceBound, r29Order55SupportDisconnected823,
    Nat.ceilDiv_eq_add_pred_div]

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

/-- Order-56 support active at the disconnected-complement diagnostic row
`(n,m)=(57,837)`. -/
def r29Order56SupportDisconnected837 : SparseAffineSupport where
  slope := 133
  intercept := 75524
  scale := 4
  left := 804
  right := 808

/-- The finite set of supports needed for the order-57 threshold window. -/
def IsR29Order56WindowSupport (cert : SparseAffineSupport) : Prop :=
  cert = r29Order56Support824 ∨
    cert = r29Order56Support825to827 ∨
      cert = r29Order56Support828to829 ∨
        cert = r29Order56SupportDisconnected837

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
  rcases hcert with rfl | rfl | rfl | rfl <;>
    norm_num [deletionEdgeThreshold, zarankiewiczNumber,
      r29Order56Support824, r29Order56Support825to827,
      r29Order56Support828to829, r29Order56SupportDisconnected837,
      Nat.ceilDiv_eq_add_pred_div]

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
  rcases hcert with rfl | rfl | rfl | rfl <;>
    exact deletionEdgeThreshold_le_iff (by norm_num)
      (by norm_num [r29Order56Support824, r29Order56Support825to827,
        r29Order56Support828to829, r29Order56SupportDisconnected837])
      (by norm_num [r29Order56Support824, r29Order56Support825to827,
        r29Order56Support828to829, r29Order56SupportDisconnected837])
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

theorem r29_order57_disconnected_value :
    deletionRecurrenceBound 57 r29Order56SupportDisconnected837.slope
      r29Order56SupportDisconnected837.intercept
      r29Order56SupportDisconnected837.scale 837 = 8575 := by
  norm_num [deletionRecurrenceBound, r29Order56SupportDisconnected837,
    Nat.ceilDiv_eq_add_pred_div]

/-! Order-58 threshold window, using supports of the order-57 table. -/

def r29Order57Support838to841 : SparseAffineSupport where
  slope := 32
  intercept := 18248
  scale := 1
  left := 808
  right := 813

def r29Order57SupportDisconnected852 : SparseAffineSupport where
  slope := 67
  intercept := 38947
  scale := 2
  left := 821
  right := 825

def IsR29Order57Support (cert : SparseAffineSupport) : Prop :=
  cert = r29Order57Support838to841 ∨
    cert = r29Order57SupportDisconnected852

theorem r29_order58_selected_support_threshold
    (cert : SparseAffineSupport) (hcert : IsR29Order57Support cert) :
    deletionEdgeThreshold 58 cert.slope cert.intercept cert.scale
      (zarankiewiczNumber 29) = 841 := by
  rcases hcert with rfl | rfl <;>
    norm_num [deletionEdgeThreshold, zarankiewiczNumber,
      r29Order57Support838to841, r29Order57SupportDisconnected852,
      Nat.ceilDiv_eq_add_pred_div]

theorem r29_order58_window_values :
    deletionRecurrenceBound 58 r29Order57Support838to841.slope
        r29Order57Support838to841.intercept
        r29Order57Support838to841.scale 838 = 8210 ∧
    deletionRecurrenceBound 58 r29Order57Support838to841.slope
        r29Order57Support838to841.intercept
        r29Order57Support838to841.scale 839 = 8243 ∧
    deletionRecurrenceBound 58 r29Order57Support838to841.slope
        r29Order57Support838to841.intercept
        r29Order57Support838to841.scale 840 = 8276 ∧
    deletionRecurrenceBound 58 r29Order57Support838to841.slope
        r29Order57Support838to841.intercept
        r29Order57Support838to841.scale 841 = 8310 := by
  norm_num [deletionRecurrenceBound, r29Order57Support838to841,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_order58_disconnected_value :
    deletionRecurrenceBound 58 r29Order57SupportDisconnected852.slope
      r29Order57SupportDisconnected852.intercept
      r29Order57SupportDisconnected852.scale 852 = 8684 := by
  norm_num [deletionRecurrenceBound, r29Order57SupportDisconnected852,
    Nat.ceilDiv_eq_add_pred_div]

/-! Order-59 floor, using one support of the order-58 table. -/

def r29Order58Support852 : SparseAffineSupport where
  slope := 94
  intercept := 54166
  scale := 3
  left := 823
  right := 829

theorem r29_order59_selected_support_threshold :
    deletionEdgeThreshold 59 r29Order58Support852.slope
      r29Order58Support852.intercept r29Order58Support852.scale
      (zarankiewiczNumber 29) = 852 := by
  norm_num [deletionEdgeThreshold, zarankiewiczNumber,
    r29Order58Support852, Nat.ceilDiv_eq_add_pred_div]

theorem r29_order59_floor_value :
    deletionRecurrenceBound 59 r29Order58Support852.slope
      r29Order58Support852.intercept r29Order58Support852.scale 852 = 8299 := by
  norm_num [deletionRecurrenceBound, r29Order58Support852,
    Nat.ceilDiv_eq_add_pred_div]

theorem r29_boundary_closure_surpluses :
    8290 - zarankiewiczNumber 29 = 9 ∧
      8310 - zarankiewiczNumber 29 = 29 ∧
      8299 - zarankiewiczNumber 29 = 18 ∧
      8497 - zarankiewiczNumber 29 = 216 ∧
      8575 - zarankiewiczNumber 29 = 294 ∧
      8684 - zarankiewiczNumber 29 = 403 := by
  norm_num [zarankiewiczNumber]

end AlbertsonSamplingMechanism

#print axioms AlbertsonSamplingMechanism.deletion_recurrence_closes_at_threshold
#print axioms AlbertsonSamplingMechanism.r29_candidate_order_edge_floors
#print axioms AlbertsonSamplingMechanism.r29_disconnected_complement_edge_floors
#print axioms AlbertsonSamplingMechanism.r29_order56_selected_support_threshold
#print axioms AlbertsonSamplingMechanism.r29_order56_window_values
#print axioms AlbertsonSamplingMechanism.r29_m824_support_window
#print axioms AlbertsonSamplingMechanism.r29_order57_m824_recursive_value
#print axioms AlbertsonSamplingMechanism.r29_order57_open_row_gaps
#print axioms AlbertsonSamplingMechanism.r29_order57_selected_support_threshold
#print axioms AlbertsonSamplingMechanism.r29_order57_reaches_zarankiewicz_iff
#print axioms AlbertsonSamplingMechanism.r29_order57_closed_from_829
#print axioms AlbertsonSamplingMechanism.r29_order58_selected_support_threshold
#print axioms AlbertsonSamplingMechanism.r29_order58_window_values
#print axioms AlbertsonSamplingMechanism.r29_order59_selected_support_threshold
#print axioms AlbertsonSamplingMechanism.r29_order59_floor_value
#print axioms AlbertsonSamplingMechanism.r29_boundary_closure_surpluses
