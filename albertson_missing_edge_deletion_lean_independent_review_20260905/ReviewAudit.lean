import AlbertsonMissingEdgeDeletion

open Finset

namespace IndependentReview

variable {V : Type*} [Fintype V] [DecidableEq V]
  (H : SimpleGraph V) [DecidableRel H.Adj]

/-- Exact characterization of the vertices that improve a positive upper
edge budget.  This is a reviewer-authored strengthening of the selection
lemma: in the slack case every vertex works, while at an exact budget the
working vertices are precisely the nonisolated support. -/
theorem residual_improved_iff (f : ℕ) (hf : 0 < f)
    (hbudget : H.edgeFinset.card ≤ f) (v : V) :
    (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ f - 1 ↔
      H.edgeFinset.card < f ∨ v ∈ H.support := by
  rw [H.card_edgeFinset_induce_compl_singleton, H.card_edgeFinset_deleteIncidenceSet]
  constructor
  · intro himproved
    by_cases hslack : H.edgeFinset.card < f
    · exact Or.inl hslack
    · right
      apply (H.degree_pos_iff_mem_support v).mp
      omega
  · rintro (hslack | hsupport)
    · omega
    · have hdegree := (H.degree_pos_iff_mem_support v).mpr hsupport
      omega

/-- Under a strict upper budget, all vertex deletions meet the improved
budget; no support threshold is needed. -/
theorem all_deletions_improve_of_slack (f : ℕ)
    (hslack : H.edgeFinset.card < f) (v : V) :
    (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ f - 1 := by
  have hf : 0 < f := lt_of_le_of_lt (Nat.zero_le _) hslack
  exact (residual_improved_iff H f hf (Nat.le_of_lt hslack) v).2 (Or.inl hslack)

/-- At an exact positive budget, improvement is equivalent to belonging to
the support. -/
theorem exact_budget_improves_iff_support (f : ℕ) (hf : 0 < f)
    (hexact : H.edgeFinset.card = f) (v : V) :
    (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ f - 1 ↔ v ∈ H.support := by
  rw [residual_improved_iff H f hf (le_of_eq hexact) v, hexact]
  simp

#print axioms IndependentReview.residual_improved_iff
#print axioms IndependentReview.all_deletions_improve_of_slack
#print axioms IndependentReview.exact_budget_improves_iff_support

end IndependentReview
