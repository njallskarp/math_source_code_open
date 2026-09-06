import Mathlib.Combinatorics.SimpleGraph.DeleteEdges
import Mathlib.Algebra.Order.Floor.Div
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Lean.Elab.Tactic.Omega

/-!
Native missing-edge graphs supply improved vertex deletions for the dense-graph
recurrence. Missing-edge budgets are upper bounds, not assumed exact counts.
The local lower bounds and crossing-survival inequality remain explicit inputs.
-/

open Finset

namespace AlbertsonMissingEdgeDeletion

variable {V : Type*} [Fintype V] [DecidableEq V]
  (H : SimpleGraph V) [DecidableRel H.Adj]

/-- Exact edge count after deleting a vertex, on the actual induced graph. -/
theorem card_vertex_deletion (v : V) :
    (H.induce ({v}ᶜ : Set V)).edgeFinset.card = H.edgeFinset.card - H.degree v := by
  rw [H.card_edgeFinset_induce_compl_singleton, H.card_edgeFinset_deleteIncidenceSet]

omit [DecidableEq V] in
/-- Only nonisolated vertices can support edges. -/
theorem card_edges_le_choose_support :
    H.edgeFinset.card ≤ (Fintype.card H.support).choose 2 := by
  rw [← H.card_edgeFinset_induce_support]
  exact (H.induce H.support).card_edgeFinset_le_card_choose_two

/-- An upper budget `f` guarantees `t` actual improved deletions. If fewer
than `f` edges are present, every deletion improves the budget; otherwise the
support bound supplies the witnesses. The threshold need not be maximal. -/
theorem exists_improved_deletions (f t : ℕ) (hbudget : H.edgeFinset.card ≤ f)
    (ht : t ≤ Fintype.card V) (hgap : (t - 1).choose 2 < f) :
    ∃ S : Finset V, S.card = t ∧
      ∀ v ∈ S, (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ f - 1 := by
  classical
  by_cases heq : H.edgeFinset.card = f
  · have hs : t ≤ H.support.toFinset.card := by
      have hedge := card_edges_le_choose_support H
      rw [heq] at hedge
      have hcard : Fintype.card H.support = H.support.toFinset.card := by simp
      rw [hcard] at hedge
      by_contra hn
      have hc := Nat.choose_le_choose 2 (show H.support.toFinset.card ≤ t - 1 by omega)
      omega
    obtain ⟨S, hS, hcard⟩ := Finset.exists_subset_card_eq hs
    refine ⟨S, hcard, ?_⟩
    intro v hv
    have hd := (H.degree_pos_iff_mem_support v).mpr (by simpa using hS hv)
    rw [card_vertex_deletion, heq]
    omega
  · obtain ⟨S, _, hcard⟩ := Finset.exists_subset_card_eq
      (show t ≤ (univ : Finset V).card by simpa using ht)
    refine ⟨S, hcard, ?_⟩
    intro v _
    rw [card_vertex_deletion]
    omega

omit [DecidableEq V] H [DecidableRel H.Adj] in
/-- A chosen set of improved local bounds gives an exact two-level sum bound. -/
theorem two_level_sum_bound (S : Finset V) (a b : ℕ) (c : V → ℕ)
    (hbase : ∀ v, a ≤ c v) (hbetter : ∀ v ∈ S, b ≤ c v) :
    (Fintype.card V - S.card) * a + S.card * b ≤ ∑ v, c v := by
  classical
  have hs : S.card * b ≤ ∑ v ∈ S, c v := by
    simpa using Finset.sum_le_sum (fun v hv => hbetter v hv)
  have hc : (Fintype.card V - S.card) * a ≤ ∑ v ∈ Sᶜ, c v := by
    simpa [Finset.card_compl] using Finset.sum_le_sum (s := Sᶜ) (fun v _ => hbase v)
  have hsum := Finset.sum_add_sum_compl S c
  omega

/-- Graph-native dense-defect deletion recurrence with exact ceiling. The
function `L` need only be antitone on budgets up to `f`; crossing survival is
an explicit inequality, not an encoded topological assertion. -/
theorem deletion_recurrence (f t : ℕ) (hbudget : H.edgeFinset.card ≤ f)
    (ht : t ≤ Fintype.card V) (hgap : (t - 1).choose 2 < f)
    (L : ℕ → ℕ) (hmono : AntitoneOn L (Set.Iic f))
    (c : V → ℕ) (C : ℕ)
    (hlocal : ∀ v, L (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ c v)
    (hsurvive : ∑ v, c v ≤ (Fintype.card V - 4) * C)
    (horder : 4 < Fintype.card V) :
    ((Fintype.card V - t) * L f + t * L (f - 1)) ⌈/⌉
      (Fintype.card V - 4) ≤ C := by
  obtain ⟨S, hcard, hS⟩ := exists_improved_deletions H f t hbudget ht hgap
  have hres (v : V) : (H.induce ({v}ᶜ : Set V)).edgeFinset.card ≤ f := by
    rw [card_vertex_deletion]
    omega
  have hbase (v : V) : L f ≤ c v :=
    (hmono (hres v) (Set.mem_Iic.mpr (le_refl f)) (hres v)).trans (hlocal v)
  have hbetter (v : V) (hv : v ∈ S) : L (f - 1) ≤ c v :=
    (hmono (hres v) (Nat.sub_le f 1) (hS v hv)).trans (hlocal v)
  rw [ceilDiv_le_iff_le_mul (show 0 < Fintype.card V - 4 by omega)]
  have h := (two_level_sum_bound S (L f) (L (f - 1)) c hbase hbetter).trans hsurvive
  simpa [hcard] using h

end AlbertsonMissingEdgeDeletion
