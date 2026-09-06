import AlbertsonMissingEdgeDeletion

#print axioms AlbertsonMissingEdgeDeletion.card_vertex_deletion
#print axioms AlbertsonMissingEdgeDeletion.card_edges_le_choose_support
#print axioms AlbertsonMissingEdgeDeletion.exists_improved_deletions
#print axioms AlbertsonMissingEdgeDeletion.two_level_sum_bound
#print axioms AlbertsonMissingEdgeDeletion.deletion_recurrence

open Finset AlbertsonMissingEdgeDeletion

-- A slack budget has no support-size lower bound. Nonetheless it supplies
-- actual improved deletions, which is the conclusion the recurrence needs.
example : Fintype.card (⊥ : SimpleGraph (Fin 5)).support = 0 ∧
    ∃ S : Finset (Fin 5), S.card = 2 ∧
      ∀ v ∈ S, ((⊥ : SimpleGraph (Fin 5)).induce ({v}ᶜ : Set (Fin 5))).edgeFinset.card
        ≤ 1 - 1 := by
  refine ⟨by decide, ?_⟩
  exact exists_improved_deletions ⊥ 1 2 (by decide) (by decide) (by decide)

-- Two disjoint missing edges. No vertex deletion removes both of them.
private def twoDisjointEdges : SimpleGraph (Fin 4) :=
  SimpleGraph.fromEdgeSet {s(0, 1), s(2, 3)}

private instance : DecidableRel twoDisjointEdges.Adj :=
  inferInstanceAs (DecidableRel (SimpleGraph.fromEdgeSet
    ({s(0, 1), s(2, 3)} : Set (Sym2 (Fin 4)))).Adj)

example : twoDisjointEdges.edgeFinset.card = 2 ∧
    ∀ v, (twoDisjointEdges.induce ({v}ᶜ : Set (Fin 4))).edgeFinset.card = 1 := by
  decide

example : ∃ S : Finset (Fin 4), S.card = 3 ∧
    ∀ v ∈ S, (twoDisjointEdges.induce ({v}ᶜ : Set (Fin 4))).edgeFinset.card ≤ 1 := by
  exact exists_improved_deletions twoDisjointEdges 2 3
    (by decide) (by decide) (by decide)

-- A complete graph at its edge capacity: every
-- deletion has the smaller budget. This checks the threshold at full order.
example : ∃ S : Finset (Fin 5), S.card = 5 ∧
    ∀ v ∈ S, ((⊤ : SimpleGraph (Fin 5)).induce ({v}ᶜ : Set (Fin 5))).edgeFinset.card
      ≤ 10 - 1 := by
  exact exists_improved_deletions ⊤ 10 5 (by decide) (by decide) (by decide)

-- The boundary `f=0` is excluded by the threshold gap, not silently rounded.
example (t : ℕ) : ¬ (t - 1).choose 2 < 0 := Nat.not_lt_zero _

-- Equality in the threshold gap is insufficient: one edge on three
-- vertices has only two deletions that remove that edge.
private def oneEdge : SimpleGraph (Fin 3) :=
  SimpleGraph.fromEdgeSet {s(0, 1)}

private instance : DecidableRel oneEdge.Adj :=
  inferInstanceAs (DecidableRel (SimpleGraph.fromEdgeSet
    ({s(0, 1)} : Set (Sym2 (Fin 3)))).Adj)

example : ¬ ∃ S : Finset (Fin 3), S.card = 3 ∧
    ∀ v ∈ S, (oneEdge.induce ({v}ᶜ : Set (Fin 3))).edgeFinset.card ≤ 0 := by
  rintro ⟨S, hcard, hS⟩
  have hu : S = univ := S.eq_univ_of_card hcard
  have h := hS 2 (by simp [hu])
  have hn : (oneEdge.induce ({(2 : Fin 3)}ᶜ : Set (Fin 3))).edgeFinset.card = 1 := by
    decide
  omega

-- Synthetic local counts test the full recurrence and its nonintegral
-- quotient. These numbers are not claimed to be drawing crossing counts.
private def sixVertexDefect : SimpleGraph (Fin 6) :=
  SimpleGraph.fromEdgeSet {s(0, 1), s(2, 3)}

private instance : DecidableRel sixVertexDefect.Adj :=
  inferInstanceAs (DecidableRel (SimpleGraph.fromEdgeSet
    ({s(0, 1), s(2, 3)} : Set (Sym2 (Fin 6)))).Adj)

example : ((6 - 3) * (6 - 2) + 3 * (6 - (2 - 1))) ⌈/⌉ (6 - 4) ≤ (14 : ℕ) := by
  apply deletion_recurrence sixVertexDefect 2 3 (by decide) (by decide) (by decide)
    (fun k => 6 - k) ?_
    (fun v => 6 - (sixVertexDefect.induce ({v}ᶜ : Set (Fin 6))).edgeFinset.card) 14
    (fun _ => le_rfl) (by decide) (by decide)
  intro a ha b hb hab
  exact Nat.sub_le_sub_left hab 6

example : ((6 - 3) * (6 - 2) + 3 * (6 - (2 - 1))) ⌈/⌉ (6 - 4) = (14 : ℕ) := by
  decide
