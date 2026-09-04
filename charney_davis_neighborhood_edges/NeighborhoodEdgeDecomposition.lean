import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.DegreeSum

open Finset

namespace NeighborhoodEdgeDecomposition

open SimpleGraph

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Vertices other than `r` that are not adjacent to `r`. -/
def farVertices (r : V) : Finset V :=
  (insert r (G.neighborFinset r))ᶜ

lemma mem_farVertices_iff (r v : V) :
    v ∈ farVertices G r ↔ v ≠ r ∧ ¬ G.Adj r v := by
  simp [farVertices, SimpleGraph.mem_neighborFinset]

lemma vertex_trichotomy (r v : V) :
    v = r ∨ v ∈ G.neighborFinset r ∨ v ∈ farVertices G r := by
  by_cases hvr : v = r
  · exact Or.inl hvr
  by_cases hav : G.Adj r v
  · exact Or.inr (Or.inl ((G.mem_neighborFinset r v).2 hav))
  · exact Or.inr (Or.inr ((mem_farVertices_iff G r v).2 ⟨hvr, hav⟩))

theorem graph_eq_star_sup_cross_sup_far
    (r : V)
    (hN : G.IsIndepSet (G.neighborSet r)) :
    G =
      (G.between ({r} : Set V) (G.neighborSet r) ⊔
      G.between (G.neighborSet r) (↑(farVertices G r) : Set V)) ⊔
      G.between (↑(farVertices G r) : Set V) (↑(farVertices G r) : Set V) := by
  ext v w
  constructor
  · intro hvw
    rcases vertex_trichotomy G r v with (hvr | hvN | hvB)
    · subst v
      exact Or.inl (Or.inl ⟨hvw, Or.inl ⟨Set.mem_singleton r, hvw⟩⟩)
    rcases vertex_trichotomy G r w with (hwr | hwN | hwB)
    · subst w
      exact Or.inl (Or.inl ⟨hvw, Or.inr ⟨hvw.symm, Set.mem_singleton r⟩⟩)
    · exact False.elim
        (hN ((G.mem_neighborFinset r v).1 hvN)
          ((G.mem_neighborFinset r w).1 hwN) (G.ne_of_adj hvw) hvw)
    · exact Or.inl (Or.inr
        ⟨hvw, Or.inl ⟨(G.mem_neighborFinset r v).1 hvN, hwB⟩⟩)
    · rcases vertex_trichotomy G r w with (hwr | hwN | hwB)
      · subst w
        exact False.elim (((mem_farVertices_iff G r v).1 hvB).2 hvw.symm)
      · exact Or.inl (Or.inr
          ⟨hvw, Or.inr ⟨hvB, (G.mem_neighborFinset r w).1 hwN⟩⟩)
      · exact Or.inr ⟨hvw, Or.inl ⟨hvB, hwB⟩⟩
  · rintro ((hstar | hcross) | hfar)
    · exact hstar.1
    · exact hcross.1
    · exact hfar.1

lemma edgeFinset_between_self (S : Finset V) :
    (G.between (↑S : Set V) (↑S : Set V)).edgeFinset =
      G.edgeFinset.filter (fun e ↦ e.toFinset ⊆ S) := by
  ext e
  obtain ⟨v, w⟩ := e
  simp [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeSet,
    SimpleGraph.between_adj, Finset.subset_iff]

lemma card_edgeFinset_between_self (S : Finset V) :
    #(G.between (↑S : Set V) (↑S : Set V)).edgeFinset =
      #((G.induce (↑S : Set V)).edgeFinset) := by
  rw [edgeFinset_between_self]
  exact G.card_filter_edgeFinset_toFinset_subset S

lemma neighborFinset_cross_eq_erase
    (r u : V) (hN : G.IsIndepSet (G.neighborSet r))
    (hu : u ∈ G.neighborFinset r) :
    (G.between (G.neighborSet r) (↑(farVertices G r) : Set V)).neighborFinset u =
      (G.neighborFinset u).erase r := by
  ext v
  simp only [SimpleGraph.mem_neighborFinset, Finset.mem_erase,
    SimpleGraph.between_adj]
  constructor
  · rintro ⟨huv, hparts⟩
    rcases hparts with (⟨huN, hvB⟩ | ⟨huB, hvN⟩)
    · exact ⟨((mem_farVertices_iff G r v).1 hvB).1, huv⟩
    · exact False.elim
        (((mem_farVertices_iff G r u).1 huB).2
          ((G.mem_neighborFinset r u).1 hu))
  · rintro ⟨hvr, huv⟩
    have huN : u ∈ G.neighborSet r := (G.mem_neighborFinset r u).1 hu
    have hnotrv : ¬ G.Adj r v := by
      intro hrv
      exact hN huN hrv (G.ne_of_adj huv) huv
    have hvB : v ∈ farVertices G r :=
      (mem_farVertices_iff G r v).2 ⟨hvr, hnotrv⟩
    exact ⟨huv, Or.inl ⟨huN, hvB⟩⟩

lemma degree_cross_eq_sub_one
    (r u : V) (hN : G.IsIndepSet (G.neighborSet r))
    (hu : u ∈ G.neighborFinset r) :
    (G.between (G.neighborSet r) (↑(farVertices G r) : Set V)).degree u =
      G.degree u - 1 := by
  have hru : r ∈ G.neighborFinset u :=
    (G.mem_neighborFinset u r).2 ((G.mem_neighborFinset r u).1 hu).symm
  rw [SimpleGraph.degree, neighborFinset_cross_eq_erase G r u hN hu,
    Finset.card_erase_of_mem hru]
  rw [G.card_neighborFinset_eq_degree]

lemma neighborFinset_star_eq (r : V) :
    (G.between ({r} : Set V) (G.neighborSet r)).neighborFinset r =
      G.neighborFinset r := by
  ext v
  simp [SimpleGraph.mem_neighborFinset, SimpleGraph.between_adj]

lemma card_edgeFinset_star (r : V) :
    #(G.between ({r} : Set V) (G.neighborSet r)).edgeFinset = G.degree r := by
  have hdis : Disjoint ({r} : Finset V) (G.neighborFinset r) :=
    G.singleton_disjoint_neighborFinset r
  have hbip :
      (G.between ({r} : Set V) (G.neighborSet r)).IsBipartiteWith
        ({r} : Finset V) (G.neighborFinset r) := by
    simpa only [Finset.coe_singleton, SimpleGraph.coe_neighborFinset] using
      (SimpleGraph.between_isBipartiteWith
        (G := G) (s := (↑({r} : Finset V) : Set V))
        (t := (↑(G.neighborFinset r) : Set V)) (Finset.disjoint_coe.mpr hdis))
  have hsum := SimpleGraph.isBipartiteWith_sum_degrees_eq_card_edges hbip
  rw [Finset.sum_singleton] at hsum
  calc
    #(G.between ({r} : Set V) (G.neighborSet r)).edgeFinset =
        (G.between ({r} : Set V) (G.neighborSet r)).degree r := hsum.symm
    _ = G.degree r := by
      rw [SimpleGraph.degree, neighborFinset_star_eq G r,
        SimpleGraph.card_neighborFinset_eq_degree]

lemma card_edgeFinset_cross
    (r : V) (hN : G.IsIndepSet (G.neighborSet r)) :
    #(G.between (G.neighborSet r) (↑(farVertices G r) : Set V)).edgeFinset =
      ∑ u ∈ G.neighborFinset r, (G.degree u - 1) := by
  have hdis :
      Disjoint (G.neighborFinset r) (farVertices G r) := by
    rw [Finset.disjoint_iff_ne]
    intro u hu v hv huv
    subst v
    exact ((mem_farVertices_iff G r u).1 hv).2
      ((G.mem_neighborFinset r u).1 hu)
  have hbip :
      (G.between (G.neighborSet r) (↑(farVertices G r) : Set V)).IsBipartiteWith
        (G.neighborFinset r) (farVertices G r) := by
    simpa only [SimpleGraph.coe_neighborFinset] using
      (SimpleGraph.between_isBipartiteWith
        (G := G) (s := (↑(G.neighborFinset r) : Set V))
        (t := (↑(farVertices G r) : Set V)) (Finset.disjoint_coe.mpr hdis))
  have hsum := SimpleGraph.isBipartiteWith_sum_degrees_eq_card_edges hbip
  rw [show (∑ u ∈ G.neighborFinset r,
      (G.between (G.neighborSet r) (↑(farVertices G r) : Set V)).degree u) =
      ∑ u ∈ G.neighborFinset r, (G.degree u - 1) by
        apply Finset.sum_congr rfl
        intro u hu
        exact degree_cross_eq_sub_one G r u hN hu] at hsum
  exact hsum.symm

lemma disjoint_star_cross (r : V) :
    Disjoint
      (G.between ({r} : Set V) (G.neighborSet r))
      (G.between (G.neighborSet r) (↑(farVertices G r) : Set V)) := by
  rw [disjoint_iff_inf_le]
  intro v w h
  simp only [SimpleGraph.inf_adj, SimpleGraph.between_adj] at h
  simp only [SimpleGraph.bot_adj]
  simp [farVertices] at h
  grind [G.loopless, G.adj_comm]

lemma disjoint_star_far (r : V) :
    Disjoint
      (G.between ({r} : Set V) (G.neighborSet r))
      (G.between (↑(farVertices G r) : Set V) (↑(farVertices G r) : Set V)) := by
  rw [disjoint_iff_inf_le]
  intro v w h
  simp only [SimpleGraph.inf_adj, SimpleGraph.between_adj] at h
  simp only [SimpleGraph.bot_adj]
  simp [farVertices] at h
  grind [G.loopless, G.adj_comm]

lemma disjoint_cross_far (r : V) :
    Disjoint
      (G.between (G.neighborSet r) (↑(farVertices G r) : Set V))
      (G.between (↑(farVertices G r) : Set V) (↑(farVertices G r) : Set V)) := by
  rw [disjoint_iff_inf_le]
  intro v w h
  simp only [SimpleGraph.inf_adj, SimpleGraph.between_adj] at h
  simp only [SimpleGraph.bot_adj]
  simp [farVertices] at h
  grind [G.loopless, G.adj_comm]

/-- Every edge lies uniquely in the star at `r`, between the neighborhood and
the far vertices, or inside the far vertices. -/
theorem card_edgeFinset_neighborhood_decomposition
    (r : V) (hN : G.IsIndepSet (G.neighborSet r)) :
    #G.edgeFinset =
      G.degree r + (∑ u ∈ G.neighborFinset r, (G.degree u - 1)) +
        #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) := by
  let A := G.between ({r} : Set V) (G.neighborSet r)
  let C := G.between (G.neighborSet r) (↑(farVertices G r) : Set V)
  let D := G.between (↑(farVertices G r) : Set V) (↑(farVertices G r) : Set V)
  have hdecomp : G = (A ⊔ C) ⊔ D := by
    simpa [A, C, D] using graph_eq_star_sup_cross_sup_far G r hN
  have hAC : Disjoint A.edgeFinset C.edgeFinset := by
    rw [SimpleGraph.disjoint_edgeFinset]
    simpa [A, C] using disjoint_star_cross G r
  have hAD : Disjoint A.edgeFinset D.edgeFinset := by
    rw [SimpleGraph.disjoint_edgeFinset]
    simpa [A, D] using disjoint_star_far G r
  have hCD : Disjoint C.edgeFinset D.edgeFinset := by
    rw [SimpleGraph.disjoint_edgeFinset]
    simpa [C, D] using disjoint_cross_far G r
  have hACD : Disjoint (A.edgeFinset ∪ C.edgeFinset) D.edgeFinset :=
    Finset.disjoint_union_left.mpr ⟨hAD, hCD⟩
  have hedge : G.edgeFinset = ((A ⊔ C) ⊔ D).edgeFinset :=
    SimpleGraph.edgeFinset_inj.mpr hdecomp
  calc
    #G.edgeFinset = #((A ⊔ C) ⊔ D).edgeFinset := congrArg Finset.card hedge
    _ = #((A.edgeFinset ∪ C.edgeFinset) ∪ D.edgeFinset) := by
      rw [SimpleGraph.edgeFinset_sup, SimpleGraph.edgeFinset_sup]
    _ = (#A.edgeFinset + #C.edgeFinset) + #D.edgeFinset := by
      rw [Finset.card_union_of_disjoint hACD,
        Finset.card_union_of_disjoint hAC]
    _ = G.degree r + (∑ u ∈ G.neighborFinset r, (G.degree u - 1)) +
        #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) := by
      rw [show #A.edgeFinset = G.degree r by
          simpa [A] using card_edgeFinset_star G r,
        show #C.edgeFinset = ∑ u ∈ G.neighborFinset r, (G.degree u - 1) by
          simpa [C] using card_edgeFinset_cross G r hN,
        show #D.edgeFinset =
            #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) by
          simpa [D] using card_edgeFinset_between_self G (farVertices G r)]

/-- The subtraction form of the edge partition. It is safe over `Nat` because
the additive decomposition proves that both subtractions remove actual edge
classes. -/
theorem card_far_induced_eq_sub_degrees
    (r : V) (hN : G.IsIndepSet (G.neighborSet r)) :
    #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) =
      #G.edgeFinset - G.degree r -
        ∑ u ∈ G.neighborFinset r, (G.degree u - 1) := by
  have hcount := card_edgeFinset_neighborhood_decomposition G r hN
  omega

lemma card_farVertices (r : V) :
    #(farVertices G r) = Fintype.card V - (G.degree r + 1) := by
  rw [farVertices, Finset.card_compl]
  rw [Finset.card_insert_of_notMem (G.notMem_neighborFinset_self r)]
  rw [SimpleGraph.card_neighborFinset_eq_degree]

/-- A finite simple graph and its complement partition all unordered pairs of
distinct vertices. -/
theorem card_edgeFinset_add_card_edgeFinset_compl
    {W : Type*} [Fintype W] [DecidableEq W]
    (H : SimpleGraph W) [DecidableRel H.Adj] :
    #H.edgeFinset + #Hᶜ.edgeFinset = (Fintype.card W).choose 2 := by
  classical
  have hdis : Disjoint H.edgeFinset Hᶜ.edgeFinset := by
    rw [SimpleGraph.disjoint_edgeFinset]
    exact disjoint_compl_right
  have hunion :
      H.edgeFinset ∪ Hᶜ.edgeFinset = (⊤ : SimpleGraph W).edgeFinset := by
    ext e
    obtain ⟨u, v⟩ := e
    by_cases huv : H.Adj u v
    · simp [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeSet,
        SimpleGraph.compl_adj, huv, H.ne_of_adj huv]
    · simp [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeSet,
        SimpleGraph.compl_adj, huv]
  rw [← Finset.card_union_of_disjoint hdis, hunion,
    SimpleGraph.card_edgeFinset_top_eq_card_choose_two]

/-- Subtraction form of the finite complement-edge count. -/
theorem card_edgeFinset_compl_eq_choose_sub
    {W : Type*} [Fintype W] [DecidableEq W]
    (H : SimpleGraph W) [DecidableRel H.Adj] :
    #Hᶜ.edgeFinset = (Fintype.card W).choose 2 - #H.edgeFinset := by
  have htotal := card_edgeFinset_add_card_edgeFinset_compl H
  omega

/-- The exact local graph count used at the rigid Charney--Davis profile:
a degree-four vertex in a 26-edge graph, with independent degree-three
neighbors, leaves 14 edges on the other vertices. -/
theorem degree_four_far_edge_count
    (r : V)
    (hN : G.IsIndepSet (G.neighborSet r))
    (hEdges : #G.edgeFinset = 26)
    (hDegree : G.degree r = 4)
    (hNeighborDegree : ∀ u ∈ G.neighborFinset r, G.degree u = 3) :
    #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) = 14 := by
  have hsum : (∑ u ∈ G.neighborFinset r, (G.degree u - 1)) = 8 := by
    calc
      (∑ u ∈ G.neighborFinset r, (G.degree u - 1)) =
          ∑ u ∈ G.neighborFinset r, 2 := by
        apply Finset.sum_congr rfl
        intro u hu
        rw [hNeighborDegree u hu]
      _ = #(G.neighborFinset r) * 2 := by simp
      _ = 8 := by
        rw [SimpleGraph.card_neighborFinset_eq_degree, hDegree]
  have hcount := card_edgeFinset_neighborhood_decomposition G r hN
  rw [hEdges, hDegree, hsum] at hcount
  omega

/-- In the 17-vertex specialization, the far induced subgraph has exactly 12
vertices and 14 edges. -/
theorem degree_four_far_profile
    (r : V)
    (hVertices : Fintype.card V = 17)
    (hN : G.IsIndepSet (G.neighborSet r))
    (hEdges : #G.edgeFinset = 26)
    (hDegree : G.degree r = 4)
    (hNeighborDegree : ∀ u ∈ G.neighborFinset r, G.degree u = 3) :
    #(farVertices G r) = 12 ∧
      #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) = 14 := by
  constructor
  · rw [card_farVertices G r, hVertices, hDegree]
  · exact degree_four_far_edge_count G r hN hEdges hDegree hNeighborDegree

/-- Triangle-freeness supplies the independent-neighborhood hypothesis in the
specialized profile used by the Charney--Davis argument. -/
theorem degree_four_far_profile_of_triangleFree
    (r : V)
    (hVertices : Fintype.card V = 17)
    (hTriangleFree : G.CliqueFree 3)
    (hEdges : #G.edgeFinset = 26)
    (hDegree : G.degree r = 4)
    (hNeighborDegree : ∀ u ∈ G.neighborFinset r, G.degree u = 3) :
    #(farVertices G r) = 12 ∧
      #((G.induce (↑(farVertices G r) : Set V)).edgeFinset) = 14 :=
  degree_four_far_profile G r hVertices
    (G.isIndepSet_neighborSet_of_triangleFree hTriangleFree r)
    hEdges hDegree hNeighborDegree

/-- The complement of the far induced graph has exactly 52 edges in the rigid
17-vertex profile. This is the one-skeleton count used after the external
flag-link identification in the Charney--Davis argument. -/
theorem degree_four_far_compl_edge_count
    (r : V)
    (hVertices : Fintype.card V = 17)
    (hTriangleFree : G.CliqueFree 3)
    (hEdges : #G.edgeFinset = 26)
    (hDegree : G.degree r = 4)
    (hNeighborDegree : ∀ u ∈ G.neighborFinset r, G.degree u = 3) :
    #((G.induce (↑(farVertices G r) : Set V))ᶜ.edgeFinset) = 52 := by
  have hprofile := degree_four_far_profile_of_triangleFree G r hVertices
    hTriangleFree hEdges hDegree hNeighborDegree
  have hcardtype :
      Fintype.card (↑(farVertices G r) : Set V) = 12 := by
    simpa using hprofile.1
  rw [card_edgeFinset_compl_eq_choose_sub, hcardtype, hprofile.2]
  decide

#print axioms graph_eq_star_sup_cross_sup_far
#print axioms card_edgeFinset_neighborhood_decomposition
#print axioms card_far_induced_eq_sub_degrees
#print axioms card_farVertices
#print axioms card_edgeFinset_add_card_edgeFinset_compl
#print axioms card_edgeFinset_compl_eq_choose_sub
#print axioms degree_four_far_edge_count
#print axioms degree_four_far_profile
#print axioms degree_four_far_profile_of_triangleFree
#print axioms degree_four_far_compl_edge_count

end NeighborhoodEdgeDecomposition
