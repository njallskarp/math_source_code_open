import AlbertsonTriangleFreeCliques

/-!
Exact vertex-deletion accounting and the finite input interface for the
triangle-free branch. All graph premises are native and explicitly quantified.
-/

open Finset

namespace AlbertsonTriangleDeletion

variable {V : Type*} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Count induced degrees by ambient neighbors in the chosen vertex set. -/
theorem degree_induce_eq_card_inter (S : Finset V) (v : (S : Set V)) :
    (G.induce (S : Set V)).degree v = (G.neighborFinset v.val ∩ S).card := by
  have h := congrArg Finset.card (G.map_neighborFinset_induce (s := (S : Set V)) v)
  simp only [Finset.card_map, SimpleGraph.card_neighborFinset_eq_degree,
    Finset.toFinset_coe] at h
  convert h using 1
  congr 1
  exact Subsingleton.elim _ _

/-- Handshaking on an actual induced graph, expressed by ambient neighbor sets. -/
theorem sum_card_neighbor_inter (S : Finset V) :
    ∑ v ∈ S, (G.neighborFinset v ∩ S).card =
      2 * (G.induce (S : Set V)).edgeFinset.card := by
  have h := (G.induce (S : Set V)).sum_degrees_eq_twice_card_edges
  simp_rw [degree_induce_eq_card_inter G S] at h
  convert h using 1
  exact (Finset.sum_coe_sort S (fun v : V => (G.neighborFinset v ∩ S).card)).symm

/-- The two orientations of a finite cut have the same cardinality. -/
theorem sum_card_neighbor_inter_comm (S T : Finset V) :
    ∑ v ∈ S, (G.neighborFinset v ∩ T).card =
      ∑ v ∈ T, (G.neighborFinset v ∩ S).card := by
  have h (v : V) (U : Finset V) :
      (G.neighborFinset v ∩ U).card = ∑ w ∈ U, if G.Adj v w then 1 else 0 := by
    rw [← Finset.card_filter]
    congr 1
    ext w
    simp [and_comm]
  simp_rw [h]
  rw [Finset.sum_comm]
  simp_rw [G.adj_comm]

/-- Exact deletion identity, with no truncated subtraction. Internal deleted
edges are counted twice in the degree sum but removed only once. -/
theorem card_induce_compl_add_sum_degrees (S : Finset V) :
    (G.induce (↑(Sᶜ) : Set V)).edgeFinset.card + (∑ v ∈ S, G.degree v) =
      G.edgeFinset.card + (G.induce (S : Set V)).edgeFinset.card := by
  have split (v : V) : G.degree v =
      (G.neighborFinset v ∩ S).card + (G.neighborFinset v ∩ Sᶜ).card := by
    simpa only [Finset.sdiff_eq_inter_compl, SimpleGraph.card_neighborFinset_eq_degree] using
      (Finset.card_inter_add_card_sdiff (G.neighborFinset v) S).symm
  have hs := Finset.sum_congr (s₁ := S) rfl (fun v _ => split v)
  have ht := Finset.sum_congr (s₁ := Sᶜ) rfl (fun v _ => split v)
  rw [Finset.sum_add_distrib, sum_card_neighbor_inter] at hs
  rw [Finset.sum_add_distrib, sum_card_neighbor_inter] at ht
  have hc := sum_card_neighbor_inter_comm G S Sᶜ
  have ha := Finset.sum_add_sum_compl S (fun v : V => G.degree v)
  rw [G.sum_degrees_eq_twice_card_edges] at ha
  omega

omit [Fintype V] in
/-- A triangle contributes exactly three edges to its induced graph. -/
theorem card_induce_triangle {T : Finset V} (hT : G.IsNClique 3 T) :
    (G.induce (T : Set V)).edgeFinset.card = 3 := by
  classical
  have h := congrArg (fun K : SimpleGraph ↑(T : Set V) => Nat.card K.edgeSet)
    (G.induce_eq_top.mpr hT.isClique)
  simp only [Nat.card_eq_fintype_card, SimpleGraph.card_edgeSet,
    SimpleGraph.card_edgeFinset_top_eq_card_choose_two] at h
  have ht : Fintype.card ↑(T : Set V) = 3 := by
    calc
      _ = Fintype.card T := Fintype.card_congr (Equiv.refl _)
      _ = 3 := by simpa using hT.card_eq
  rw [ht] at h
  norm_num at h
  convert h using 1

/-- The exact edge loss when a triangle is deleted. -/
theorem card_delete_triangle_add_sum_degrees {T : Finset V} (hT : G.IsNClique 3 T) :
    (G.induce (↑(Tᶜ) : Set V)).edgeFinset.card + (∑ v ∈ T, G.degree v) =
      G.edgeFinset.card + 3 := by
  rw [card_induce_compl_add_sum_degrees, card_induce_triangle G hT]

/-- Bounding the three deleted degrees gives the uniform edge-loss estimate. -/
theorem card_delete_triangle_bound {T : Finset V} (hT : G.IsNClique 3 T) :
    G.edgeFinset.card + 3 ≤
      (G.induce (↑(Tᶜ) : Set V)).edgeFinset.card + 3 * G.maxDegree := by
  have hsum : (∑ v ∈ T, G.degree v) ≤ 3 * G.maxDegree := by
    calc
      _ ≤ ∑ _ ∈ T, G.maxDegree := Finset.sum_le_sum (fun v _ => G.degree_le_maxDegree v)
      _ = _ := by simp [hT.card_eq]
  rw [← card_delete_triangle_add_sum_degrees G hT]
  exact Nat.add_le_add_left hsum _

omit [DecidableRel G.Adj] in
/-- If the chosen set meets every triangle, its deletion is triangle-free.
The chosen set need not itself be a triangle for this implication. -/
theorem cliqueFree_induce_compl (T : Finset V)
    (hmeet : ∀ U : Finset V, G.IsNClique 3 U → ¬ Disjoint T U) :
    (G.induce (↑(Tᶜ) : Set V)).CliqueFree 3 := by
  intro U hU
  have hc := (G.isNClique_induce_iff (↑(Tᶜ) : Set V) U 3).mp hU
  apply hmeet _ hc
  rw [Finset.disjoint_left]
  intro v hv hvU
  obtain ⟨w, _, rfl⟩ := Finset.mem_map.mp hvU
  exact (Finset.mem_compl.mp w.property) hv

/-- Complete finite input interface: an intersecting triangle family and an
ambient degree/edge budget yield actual disjoint ambient complement cliques. -/
theorem exists_disjoint_compl_cliques_of_triangle {T : Finset V}
    (hT : G.IsNClique 3 T)
    (hmeet : ∀ U : Finset V, G.IsNClique 3 U → ¬ Disjoint T U)
    (q : ℕ) (hq : 0 < q) (hbudget : q + 3 * G.maxDegree ≤ G.edgeFinset.card + 3) :
    ∃ A B : Finset V, A ⊆ Tᶜ ∧ B ⊆ Tᶜ ∧
      Gᶜ.IsClique (A : Set V) ∧ Gᶜ.IsClique (B : Set V) ∧ Disjoint A B ∧
      A.card ≤ G.maxDegree ∧ B.card ≤ G.maxDegree ∧
      4 * q ≤ (Fintype.card V - 3) * (A.card + B.card) := by
  have hbound := card_delete_triangle_bound G hT
  have hedges : q ≤ (G.induce (↑(Tᶜ) : Set V)).edgeFinset.card := by omega
  obtain ⟨A, B, hAT, hBT, hA, hB, hAB, ha, hb, hsize⟩ :=
    AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques_in_induce G Tᶜ
      (cliqueFree_induce_compl G T hmeet) (hq.trans_le hedges)
  refine ⟨A, B, hAT, hBT, hA, hB, hAB, ha, hb, ?_⟩
  simp only [Finset.card_compl, hT.card_eq] at hsize
  exact (Nat.mul_le_mul_left 4 hedges).trans hsize

end AlbertsonTriangleDeletion
