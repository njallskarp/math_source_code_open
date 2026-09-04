import Lean.Elab.Tactic.Omega

namespace StrongSeymourCluster

/-- The six strict cluster-size inequalities from Bai--Li--Park, Remark 3.1. -/
def ClusterFeasible (a b c d e f : Nat) : Prop :=
  0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d ∧ 0 < e ∧ 0 < f ∧
  c + d < b + e + f ∧
  c < e + f ∧
  e + f < a + b + d ∧
  b + f < a ∧
  a + b + d < c + f ∧
  a + b < c

/-- Some sharp componentwise consequences of the cluster inequalities. -/
theorem cluster_component_lower_bounds
    {a b c d e f : Nat} (h : ClusterFeasible a b c d e f) :
    3 ≤ b ∧ 3 ≤ d ∧ 3 ≤ f ∧ 7 ≤ a ∧ 11 ≤ c ∧ 12 ≤ e + f := by
  unfold ClusterFeasible at h
  omega

/-- Every positive integral solution of the cluster inequalities has total at least 36. -/
theorem cluster_total_ge_36
    {a b c d e f : Nat} (h : ClusterFeasible a b c d e f) :
    36 ≤ a + b + c + d + e + f := by
  unfold ClusterFeasible at h
  omega

/-- Equality in the total-size bound forces the displayed six cluster sizes. -/
theorem cluster_total_eq_36_unique
    {a b c d e f : Nat} (h : ClusterFeasible a b c d e f)
    (htotal : a + b + c + d + e + f = 36) :
    a = 7 ∧ b = 3 ∧ c = 11 ∧ d = 3 ∧ e = 9 ∧ f = 3 := by
  unfold ClusterFeasible at h
  omega

/-- The six cluster sizes displayed by Bai--Li--Park satisfy their inequalities. -/
theorem published_cluster_tuple_feasible :
    ClusterFeasible 7 3 11 3 9 3 := by
  unfold ClusterFeasible
  omega

/-- Complete classification of feasible cluster tuples of total size 36. -/
theorem cluster_total_eq_36_iff
    {a b c d e f : Nat} :
    ClusterFeasible a b c d e f ∧ a + b + c + d + e + f = 36 ↔
      a = 7 ∧ b = 3 ∧ c = 11 ∧ d = 3 ∧ e = 9 ∧ f = 3 := by
  constructor
  · rintro ⟨h, htotal⟩
    exact cluster_total_eq_36_unique h htotal
  · rintro ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩
    exact ⟨published_cluster_tuple_feasible, rfl⟩

#print axioms cluster_component_lower_bounds
#print axioms cluster_total_ge_36
#print axioms cluster_total_eq_36_unique
#print axioms published_cluster_tuple_feasible
#print axioms cluster_total_eq_36_iff

end StrongSeymourCluster
