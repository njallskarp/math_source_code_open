import AlbertsonDeletionSharpness

open AlbertsonDeletionSharpness

#print axioms exists_subgraph_ncard_edges
#print axioms exists_graph_ncard_edges
#print axioms exists_exact_support_graph
#print axioms improved_vertices_eq_support
#print axioms exists_exactly_s_improvements
#print axioms uniform_improvement_iff_le

-- The edge-selection constructor includes the empty order and zero count.
example : ∃ H : SimpleGraph (Fin 0), H.edgeSet.ncard = 0 :=
  exists_graph_ncard_edges 0 0 (by decide)

-- Symbolic padding: one edge always has exactly two supported vertices.
example (n : ℕ) (hn : 2 ≤ n) :
    ∃ H : SimpleGraph (Fin n), H.edgeSet.ncard = 1 ∧ H.support.ncard = 2 :=
  exists_exact_support_graph n 2 1 hn (by decide) (by decide)

-- Budget 16 exceeds the reviewer's finite sharpness range (at most 15).
-- Five additional isolated vertices must not become improving deletions.
example : ∃ H : SimpleGraph (Fin 12), H.edgeSet.ncard = 16 ∧
    {v : Fin 12 | (H.induce ({v}ᶜ : Set (Fin 12))).edgeSet.ncard ≤ 15}.ncard = 7 :=
  exists_exactly_s_improvements 12 7 16 (by decide) (by decide) (by decide)

-- A nontriangular edge count at an interior support threshold.
example : ∀ H : SimpleGraph (Fin 8), H.edgeSet.ncard ≤ 5 →
    4 ≤ {v : Fin 8 | (H.induce ({v}ᶜ : Set (Fin 8))).edgeSet.ncard ≤ 4}.ncard :=
  (uniform_improvement_iff_le 8 4 5 4 (by decide) (by decide) (by decide)).mpr (by decide)

-- The next deletion count is not uniformly guaranteed at that same budget.
example : ¬ (∀ H : SimpleGraph (Fin 8), H.edgeSet.ncard ≤ 5 →
    5 ≤ {v : Fin 8 | (H.induce ({v}ᶜ : Set (Fin 8))).edgeSet.ncard ≤ 4}.ncard) := by
  rw [uniform_improvement_iff_le 8 4 5 5 (by decide) (by decide) (by decide)]
  decide

-- Full ambient capacity: all vertices are uniformly available.
example : ∀ H : SimpleGraph (Fin 4), H.edgeSet.ncard ≤ 6 →
    4 ≤ {v : Fin 4 | (H.induce ({v}ᶜ : Set (Fin 4))).edgeSet.ncard ≤ 5}.ncard :=
  (uniform_improvement_iff_le 4 4 6 4 (by decide) (by decide) (by decide)).mpr (by decide)

-- Equality in the predecessor capacity would predict four rather than three.
example : ¬ (∀ H : SimpleGraph (Fin 8), H.edgeSet.ncard ≤ 3 →
    4 ≤ {v : Fin 8 | (H.induce ({v}ᶜ : Set (Fin 8))).edgeSet.ncard ≤ 2}.ncard) := by
  rw [uniform_improvement_iff_le 8 3 3 4 (by decide) (by decide) (by decide)]
  decide

-- A requested count larger than the ambient order is not silently truncated.
example : ¬ (∀ H : SimpleGraph (Fin 4), H.edgeSet.ncard ≤ 6 →
    5 ≤ {v : Fin 4 | (H.induce ({v}ᶜ : Set (Fin 4))).edgeSet.ncard ≤ 5}.ncard) := by
  rw [uniform_improvement_iff_le 4 4 6 5 (by decide) (by decide) (by decide)]
  decide

-- At zero budget natural subtraction makes every empty-graph deletion work,
-- so equality with nonisolated support would be false without positivity.
example : {v : Fin 1 |
    ((⊥ : SimpleGraph (Fin 1)).induce ({v}ᶜ : Set (Fin 1))).edgeSet.ncard ≤ 0 - 1} ≠
    (⊥ : SimpleGraph (Fin 1)).support := by
  simp

-- The pair-capacity hypothesis cannot be dropped from the construction.
example : ¬ ∃ H : SimpleGraph (Fin 4), H.edgeSet.ncard = 7 := by
  rintro ⟨H, hH⟩
  classical
  have hc := H.card_edgeFinset_le_card_choose_two
  simp only [SimpleGraph.edgeFinset_card, Set.fintypeCard_eq_ncard,
    hH, Fintype.card_fin] at hc
  have hn : (4 : ℕ).choose 2 = 6 := by decide
  omega
