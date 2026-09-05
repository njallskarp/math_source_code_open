import AlbertsonTriangleFreeCliques

#print axioms AlbertsonTriangleFreeCliques.sum_dart_fst_degree
#print axioms AlbertsonTriangleFreeCliques.sum_dart_snd_degree
#print axioms AlbertsonTriangleFreeCliques.exists_adj_degree_sum
#print axioms AlbertsonTriangleFreeCliques.disjoint_neighborSet_of_triangleFree
#print axioms AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques
#print axioms AlbertsonTriangleFreeCliques.exists_disjoint_compl_cliques_in_induce

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
