import AlbertsonColoringClique

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

#print axioms AlbertsonColoringClique.exists_compl_clique_of_coloring
#print axioms AlbertsonColoringClique.exists_clique_of_induced_compl_coloring
#print axioms AlbertsonColoringClique.exists_triangle_of_deletion_colorable
#print axioms AlbertsonColoringClique.exists_disjoint_compl_cliques_of_deletion_colorable

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

-- Neither a triangle nor residual-graph premises are assumed. One deletion
-- coloring suffices for the triangle; drawing topology remains external.
example {V : Type*} [Fintype V] [DecidableEq V] (H : SimpleGraph V)
    [DecidableRel H.Adj] (v : V) (horder : Fintype.card V = 58)
    (hc : (Hᶜ.induce (↑((Finset.univ : Finset V).erase v) : Set V)).Colorable 28)
    (hmeet : ∀ T U : Finset V, H.IsNClique 3 T → H.IsNClique 3 U → ¬ Disjoint T U)
    (hedges : 813 ≤ H.edgeFinset.card) (hdegree : H.maxDegree ≤ 29) :
    ∃ T X Y : Finset V, v ∉ T ∧ H.IsNClique 3 T ∧ X ⊆ Tᶜ ∧ Y ⊆ Tᶜ ∧
      Hᶜ.IsClique (X : Set V) ∧ Hᶜ.IsClique (Y : Set V) ∧ Disjoint X Y ∧
      X.card ≤ 29 ∧ Y.card ≤ 29 ∧ 54 ≤ X.card + Y.card := by
  obtain ⟨T, X, Y, hvT, hT, hX, hY, hcX, hcY, hXY, hx, hy, hsize⟩ :=
    AlbertsonColoringClique.exists_disjoint_compl_cliques_of_deletion_colorable H v 29
      (by decide) horder hc hmeet 729 (by decide) (by omega)
  refine ⟨T, X, Y, hvT, hT, hX, hY, hcX, hcY, hXY,
    hx.trans hdegree, hy.trans hdegree, ?_⟩
  rw [horder] at hsize
  omega

-- A concrete positive example: the canonical two-coloring of K3,3 supplies
-- a triangle in its complement, without a separately supplied triangle.
example : ∃ T : Finset (Σ _ : Fin 2, Fin 3),
    (SimpleGraph.completeMultipartiteGraph (fun _ : Fin 2 => Fin 3))ᶜ.IsNClique 3 T := by
  exact AlbertsonColoringClique.exists_compl_clique_of_coloring _
    (SimpleGraph.completeMultipartiteGraph.coloring _) 2 (by decide)

-- Equality cannot replace strict pigeonhole excess: K2,2 has two colors
-- and four vertices, but its complement is triangle-free.
example : (SimpleGraph.completeMultipartiteGraph (fun _ : Fin 2 => Fin 2)).Colorable 2 ∧
    Fintype.card (Σ _ : Fin 2, Fin 2) = 2 * 2 ∧
    (SimpleGraph.completeMultipartiteGraph (fun _ : Fin 2 => Fin 2))ᶜ.CliqueFree 3 := by
  refine ⟨⟨SimpleGraph.completeMultipartiteGraph.coloring _⟩, by decide, ?_⟩
  unfold SimpleGraph.CliqueFree
  simp only [SimpleGraph.isNClique_iff]
  decide
