import AlbertsonTriangleDeletion

#print axioms AlbertsonTriangleFreeCliques.sum_dart_fst_degree
#print axioms AlbertsonTriangleFreeCliques.sum_dart_snd_degree
#print axioms AlbertsonTriangleFreeCliques.exists_adj_degree_sum
#print axioms AlbertsonTriangleFreeCliques.disjoint_neighborSet_of_triangleFree
#print axioms AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques
#print axioms AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques_in_induce

#print axioms AlbertsonTriangleDeletion.degree_induce_eq_card_inter
#print axioms AlbertsonTriangleDeletion.sum_card_neighbor_inter
#print axioms AlbertsonTriangleDeletion.sum_card_neighbor_inter_comm
#print axioms AlbertsonTriangleDeletion.card_induce_compl_add_sum_degrees
#print axioms AlbertsonTriangleDeletion.card_induce_triangle
#print axioms AlbertsonTriangleDeletion.card_delete_triangle_add_sum_degrees
#print axioms AlbertsonTriangleDeletion.card_delete_triangle_bound
#print axioms AlbertsonTriangleDeletion.cliqueFree_induce_compl
#print axioms AlbertsonTriangleDeletion.exists_disjoint_compl_cliques_of_triangle

-- The graph-theoretic input used in height 3014, not a graph construction or
-- a crossing-number theorem. All induced-graph and ambient hypotheses remain.
example {V : Type*} [Fintype V] [DecidableEq V] (H : SimpleGraph V)
    [DecidableRel H.Adj] (S : Finset V) (horder : S.card = 55)
    (hedges : 729 ≤ (H.induce (S : Set V)).edgeFinset.card)
    (htri : (H.induce (S : Set V)).CliqueFree 3) (hdegree : H.maxDegree ≤ 29) :
    ∃ A B : Finset V, A ⊆ S ∧ B ⊆ S ∧ Hᶜ.IsClique (A : Set V) ∧
      Hᶜ.IsClique (B : Set V) ∧ Disjoint A B ∧
      A.card ≤ 29 ∧ B.card ≤ 29 ∧ 54 ≤ A.card + B.card := by
  obtain ⟨A, B, hAS, hBS, hA, hB, hAB, ha, hb, hsize⟩ :=
    AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques_in_induce H S htri (by omega)
  refine ⟨A, B, hAS, hBS, hA, hB, hAB, ha.trans hdegree, hb.trans hdegree, ?_⟩
  rw [horder] at hsize
  omega

-- Nonempty edges cannot be omitted from the edge-witness theorem.
example : ¬ ∃ u v : Fin 3, (⊥ : SimpleGraph (Fin 3)).Adj u v := by simp

-- The full finite-graph input for the height-3014 triangle branch. Neither
-- the residual order, residual edge count nor residual triangle-freeness
-- is assumed. No crossing-number fact or critical-graph theorem is imported.
example {V : Type*} [Fintype V] [DecidableEq V] (H : SimpleGraph V)
    [DecidableRel H.Adj] (T : Finset V) (hT : H.IsNClique 3 T)
    (hmeet : ∀ U : Finset V, H.IsNClique 3 U → ¬ Disjoint T U)
    (horder : Fintype.card V = 58) (hedges : 813 ≤ H.edgeFinset.card)
    (hdegree : H.maxDegree ≤ 29) :
    ∃ A B : Finset V, A ⊆ Tᶜ ∧ B ⊆ Tᶜ ∧ Hᶜ.IsClique (A : Set V) ∧
      Hᶜ.IsClique (B : Set V) ∧ Disjoint A B ∧
      A.card ≤ 29 ∧ B.card ≤ 29 ∧ 54 ≤ A.card + B.card := by
  obtain ⟨A, B, hAT, hBT, hA, hB, hAB, ha, hb, hsize⟩ :=
    AlbertsonTriangleDeletion.exists_disjoint_compl_cliques_of_triangle H hT hmeet
      729 (by decide) (by omega)
  refine ⟨A, B, hAT, hBT, hA, hB, hAB, ha.trans hdegree, hb.trans hdegree, ?_⟩
  rw [horder] at hsize
  omega

-- Deleting the whole triangle leaves no residual edge. This boundary does
-- not satisfy the endpoint's positive residual-budget premise.
example : ((⊤ : SimpleGraph (Fin 3)).induce
    (↑((Finset.univ : Finset (Fin 3))ᶜ) : Set (Fin 3))).edgeFinset.card = 0 := by
  decide

-- The reusable deletion identity also accepts the empty deletion set.
example {V : Type*} [Fintype V] [DecidableEq V] (H : SimpleGraph V)
    [DecidableRel H.Adj] :
    (H.induce (↑((∅ : Finset V)ᶜ) : Set V)).edgeFinset.card = H.edgeFinset.card := by
  let : IsEmpty ↑(↑(∅ : Finset V) : Set V) :=
    ⟨fun v => Finset.notMem_empty v.val v.property⟩
  have h0 : (H.induce (↑(∅ : Finset V) : Set V)).edgeFinset.card = 0 := by
    have h := (H.induce (↑(∅ : Finset V) : Set V)).card_edgeFinset_le_card_choose_two
    simpa using h
  simpa only [Finset.sum_empty, h0, Nat.add_zero] using
    AlbertsonTriangleDeletion.card_induce_compl_add_sum_degrees H ∅
