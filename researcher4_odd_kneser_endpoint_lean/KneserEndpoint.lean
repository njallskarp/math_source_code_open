import Mathlib

/-!
# The common-neighbor obstruction in odd Kneser graphs

This file formalizes the finite-set bridge used at the only delicate equality
endpoint in the direct proof that Kneser graphs are super restricted
edge-connected.  The underlying statement is stronger and independent of
graph terminology: in a universe of size `2 * k + 1`, two distinct `k`-sets
have at most one common disjoint `k`-set.
-/

namespace KneserEndpoint

open Finset

/-- A `k`-set in a finite ambient type. -/
abbrev KneserVertex (α : Type*) [Fintype α] (k : ℕ) :=
  {A : Finset α // A.card = k}

/-- Kneser adjacency: the represented finite sets are disjoint. -/
def KneserAdj {α : Type*} [Fintype α] {k : ℕ}
    (A B : KneserVertex α k) : Prop :=
  Disjoint A.1 B.1

/--
Every common disjoint `k`-set is exactly the complement of `A ∪ B` when the
ambient universe has size `2 * k + 1` and `A`, `B` are distinct `k`-sets.
-/
theorem common_disjoint_kset_eq_compl {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    {A B C : Finset α}
    (hA : A.card = k) (hB : B.card = k)
    (hC : C.card = k)
    (hAB : A ≠ B)
    (hCA : Disjoint C A) (hCB : Disjoint C B) :
    C = (A ∪ B)ᶜ := by
  have hBA : ¬B ⊆ A := by
    intro h
    apply hAB
    exact (Finset.eq_of_subset_of_card_le h (by omega)).symm
  have hA_ssubset : A ⊂ A ∪ B := by
    refine ⟨Finset.subset_union_left, ?_⟩
    intro h
    exact hBA (Finset.subset_union_right.trans h)
  have h_union_card : k < (A ∪ B).card := by
    simpa [hA] using Finset.card_lt_card hA_ssubset
  have h_compl_card : (A ∪ B)ᶜ.card ≤ k := by
    rw [Finset.card_compl, hα]
    omega
  have hC_subset : C ⊆ (A ∪ B)ᶜ := by
    intro x hxC
    simp only [Finset.mem_compl, Finset.mem_union, not_or]
    exact ⟨fun hxA ↦ Finset.disjoint_left.mp hCA hxC hxA,
      fun hxB ↦ Finset.disjoint_left.mp hCB hxC hxB⟩
  exact Finset.eq_of_subset_of_card_le hC_subset (by simpa [hC] using h_compl_card)

/-- The existence of a common disjoint `k`-set forces two distinct `k`-sets
to differ in exactly one element, equivalently `|(A ∪ B)| = k + 1`. -/
theorem common_disjoint_kset_union_card {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    {A B C : Finset α}
    (hA : A.card = k) (hB : B.card = k)
    (hC : C.card = k)
    (hAB : A ≠ B)
    (hCA : Disjoint C A) (hCB : Disjoint C B) :
    (A ∪ B).card = k + 1 := by
  have hC_eq := common_disjoint_kset_eq_compl hα hA hB hC hAB hCA hCB
  have h_partition := Finset.card_add_card_compl (A ∪ B)
  rw [← hC_eq, hC, hα] at h_partition
  omega

/--
In a finite universe of size `2 * k + 1`, two distinct `k`-sets have at most
one common disjoint `k`-set.
-/
theorem common_disjoint_kset_unique {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    {A B C D : Finset α}
    (hA : A.card = k) (hB : B.card = k)
    (hC : C.card = k) (hD : D.card = k)
    (hAB : A ≠ B)
    (hCA : Disjoint C A) (hCB : Disjoint C B)
    (hDA : Disjoint D A) (hDB : Disjoint D B) :
    C = D := by
  have hC_eq := common_disjoint_kset_eq_compl hα hA hB hC hAB hCA hCB
  have hD_eq := common_disjoint_kset_eq_compl hα hA hB hD hAB hDA hDB
  exact hC_eq.trans hD_eq.symm

/-- The subtype-wrapped Kneser-vertex version of
`common_disjoint_kset_unique`. -/
theorem oddKneser_commonNeighbor_unique {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    {A B C D : KneserVertex α k}
    (hAB : A ≠ B)
    (hCA : KneserAdj C A) (hCB : KneserAdj C B)
    (hDA : KneserAdj D A) (hDB : KneserAdj D B) :
    C = D := by
  apply Subtype.ext
  exact common_disjoint_kset_unique hα A.2 B.2 C.2 D.2
    (fun h ↦ hAB (Subtype.ext h)) hCA hCB hDA hDB

/--
The odd Kneser adjacency relation contains no `K₂,₂`: two distinct vertices
cannot have two distinct common neighbors.  This is the exact obstruction
used to rule out equality in the Mantel bound at `|X| = 2k`.
-/
theorem oddKneser_no_K22 {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    {A B C D : KneserVertex α k}
    (hAB : A ≠ B) (hCD : C ≠ D)
    (hAC : KneserAdj A C) (hAD : KneserAdj A D)
    (hBC : KneserAdj B C) (hBD : KneserAdj B D) :
    False := by
  apply hCD
  exact oddKneser_commonNeighbor_unique hα hAB hAC.symm hBC.symm hAD.symm hBD.symm

/-- The simple graph whose vertices are `k`-sets and whose edges join disjoint
pairs. The positivity hypothesis makes literal disjointness irreflexive. -/
def kneserGraph {α : Type*} [Fintype α] (k : ℕ) (hk : 0 < k) :
    SimpleGraph (KneserVertex α k) where
  Adj := fun A B ↦ Disjoint A.1 B.1
  symm := ⟨by
    intro A B h
    exact h.symm⟩
  loopless := ⟨by
    intro A h
    have h_card : 0 < A.1.card := by simpa [A.2] using hk
    obtain ⟨x, hx⟩ := Finset.card_pos.mp h_card
    exact Finset.disjoint_left.mp h hx hx⟩

instance kneserGraph_decidableAdj {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} {hk : 0 < k} : DecidableRel (kneserGraph (α := α) k hk).Adj := by
  change DecidableRel fun A B : KneserVertex α k ↦ Disjoint A.1 B.1
  intro A B
  exact Finset.decidableDisjoint A.1 B.1

@[simp]
theorem kneserGraph_adj {α : Type*} [Fintype α] {k : ℕ} {hk : 0 < k}
    {A B : KneserVertex α k} :
    (kneserGraph (α := α) k hk).Adj A B ↔ KneserAdj A B :=
  Iff.rfl

/-- The neighbors of a Kneser vertex `A` are exactly the `k`-subsets of
the complement of `A`. -/
def kneserNeighborEquiv {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hk : 0 < k) (A : KneserVertex α k) :
    (kneserGraph (α := α) k hk).neighborSet A ≃
      ↥(A.1ᶜ.powersetCard k) where
  toFun B := ⟨B.1.1, Finset.mem_powersetCard.mpr ⟨by
    intro x hxB
    simp only [Finset.mem_compl]
    intro hxA
    exact Finset.disjoint_left.mp B.2 hxA hxB, B.1.2⟩⟩
  invFun B := ⟨⟨B.1, (Finset.mem_powersetCard.mp B.2).2⟩, by
    apply Finset.disjoint_left.mpr
    intro x hxA hxB
    exact (Finset.mem_compl.mp ((Finset.mem_powersetCard.mp B.2).1 hxB)) hxA⟩
  left_inv B := by
    apply Subtype.ext
    apply Subtype.ext
    rfl
  right_inv B := by
    apply Subtype.ext
    rfl

/-- The degree of a Kneser vertex is the number of `k`-subsets of its
set-theoretic complement. -/
theorem kneserGraph_degree_eq_choose_compl {α : Type*} [Fintype α]
    [DecidableEq α] {k : ℕ} (hk : 0 < k) (A : KneserVertex α k) :
    (kneserGraph (α := α) k hk).degree A = Nat.choose A.1ᶜ.card k := by
  rw [← SimpleGraph.card_neighborSet_eq_degree]
  calc
    Fintype.card ((kneserGraph (α := α) k hk).neighborSet A) =
        Fintype.card ↥(A.1ᶜ.powersetCard k) :=
      Fintype.card_congr (kneserNeighborEquiv hk A)
    _ = #(A.1ᶜ.powersetCard k) := Fintype.card_coe _
    _ = Nat.choose A.1ᶜ.card k := Finset.card_powersetCard k A.1ᶜ

/-- In `KG(2k+1,k)`, every vertex has degree `k+1`. -/
theorem oddKneserGraph_degree {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1) (hk : 0 < k)
    (A : KneserVertex α k) :
    (kneserGraph (α := α) k hk).degree A = k + 1 := by
  rw [kneserGraph_degree_eq_choose_compl, Finset.card_compl, A.2, hα]
  have hcard : 2 * k + 1 - k = k + 1 := by omega
  rw [hcard, Nat.choose_succ_self_right]

/-- The odd Kneser graph is regular of degree `k+1`. -/
theorem oddKneserGraph_isRegular {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1) (hk : 0 < k) :
    (kneserGraph (α := α) k hk).IsRegularOfDegree (k + 1) := by
  intro A
  exact oddKneserGraph_degree hα hk A

/-- At a vertex `v ∈ X`, its degree splits into its degree inside the
subgraph induced by `X` and its degree across the cut from `X` to `Xᶜ`. -/
theorem degree_eq_induce_add_between {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (X : Finset V)
    (v : V) (hv : v ∈ X) :
    G.degree v =
      (G.induce (↑X : Set V)).degree ⟨v, hv⟩ +
        (G.between (↑X : Set V) (↑(Xᶜ) : Set V)).degree v := by
  have h_induce :
      (G.induce (↑X : Set V)).degree ⟨v, hv⟩ =
        #(G.neighborFinset v ∩ X) := by
    let e : (G.induce (↑X : Set V)).neighborSet ⟨v, hv⟩ ≃
        ↥(G.neighborFinset v ∩ X) :=
      { toFun := fun w ↦ ⟨w.1.1, Finset.mem_inter.mpr
          ⟨(G.mem_neighborFinset v w.1.1).mpr w.2, w.1.2⟩⟩
        invFun := fun w ↦ ⟨⟨w.1, (Finset.mem_inter.mp w.2).2⟩,
          (G.mem_neighborFinset v w.1).mp (Finset.mem_inter.mp w.2).1⟩
        left_inv := by
          intro w
          apply Subtype.ext
          apply Subtype.ext
          rfl
        right_inv := by
          intro w
          apply Subtype.ext
          rfl }
    rw [← SimpleGraph.card_neighborSet_eq_degree]
    exact (Fintype.card_congr e).trans (Fintype.card_coe _)
  have h_boundary_neighbors :
      (G.between (↑X : Set V) (↑(Xᶜ) : Set V)).neighborFinset v =
        G.neighborFinset v \ X := by
    ext w
    simp [SimpleGraph.between_adj, hv]
  have h_boundary :
      (G.between (↑X : Set V) (↑(Xᶜ) : Set V)).degree v =
        #(G.neighborFinset v \ X) := by
    rw [← SimpleGraph.card_neighborFinset_eq_degree, h_boundary_neighbors]
  calc
    G.degree v = #(G.neighborFinset v) := rfl
    _ = #(G.neighborFinset v ∩ X) + #(G.neighborFinset v \ X) :=
      (Finset.card_inter_add_card_sdiff (G.neighborFinset v) X).symm
    _ = (G.induce (↑X : Set V)).degree ⟨v, hv⟩ +
        (G.between (↑X : Set V) (↑(Xᶜ) : Set V)).degree v := by
      rw [h_induce, h_boundary]

/-- Generic finite-graph cut identity: the number of edges crossing from `X`
to `Xᶜ`, plus twice the number of edges induced by `X`, equals the sum of the
ambient degrees over `X`. -/
theorem card_between_add_twice_card_induce_eq_sum_degrees
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (X : Finset V) :
    #(G.between (↑X : Set V) (↑(Xᶜ) : Set V)).edgeFinset +
        2 * #(G.induce (↑X : Set V)).edgeFinset =
      ∑ v ∈ X, G.degree v := by
  let H : SimpleGraph ↥(↑X : Set V) := G.induce ↑X
  let B : SimpleGraph V := G.between ↑X ↑(Xᶜ)
  let eX : X ≃ ↥(↑X : Set V) :=
    { toFun := fun v ↦ ⟨v.1, v.2⟩
      invFun := fun v ↦ ⟨v.1, v.2⟩
      left_inv := by
        intro v
        rfl
      right_inv := by
        intro v
        rfl }
  have h_disjoint : Disjoint (↑X : Set V) (↑(Xᶜ) : Set V) := by
    rw [Finset.coe_compl]
    exact disjoint_compl_right
  have h_bipartite : B.IsBipartiteWith (↑X : Set V) (↑(Xᶜ) : Set V) := by
    simpa only [B] using
      (SimpleGraph.between_isBipartiteWith (G := G)
        (s := (↑X : Set V)) (t := (↑(Xᶜ) : Set V)) h_disjoint)
  have h_cut_sum : ∑ v ∈ X, B.degree v = #B.edgeFinset :=
    SimpleGraph.isBipartiteWith_sum_degrees_eq_card_edges h_bipartite
  have h_cut_sum_subtype : (∑ v : ↥(↑X : Set V), B.degree v.1) = #B.edgeFinset := by
    calc
      (∑ v : ↥(↑X : Set V), B.degree v.1) = ∑ v : X, B.degree v.1 := by
        exact Fintype.sum_equiv eX.symm
          (fun v : ↥(↑X : Set V) ↦ B.degree v.1)
          (fun v : X ↦ B.degree v.1) (by intro v; rfl)
      _ = ∑ v ∈ X, B.degree v := by
        symm
        rw [← Finset.sum_attach, Finset.attach_eq_univ]
      _ = #B.edgeFinset := h_cut_sum
  have h_sum :
      (∑ v ∈ X, G.degree v) =
        2 * #H.edgeFinset + #B.edgeFinset := by
    calc
      (∑ v ∈ X, G.degree v) = ∑ v : X, G.degree v.1 := by
        rw [← Finset.sum_attach, Finset.attach_eq_univ]
      _ = ∑ v : ↥(↑X : Set V), G.degree v.1 := by
        exact Fintype.sum_equiv eX
          (fun v : X ↦ G.degree v.1)
          (fun v : ↥(↑X : Set V) ↦ G.degree v.1) (by intro v; rfl)
      _ = ∑ v : ↥(↑X : Set V), (H.degree v + B.degree v.1) := by
        apply Finset.sum_congr rfl
        intro v _
        exact degree_eq_induce_add_between G X v.1 v.2
      _ = (∑ v : ↥(↑X : Set V), H.degree v) +
          ∑ v : ↥(↑X : Set V), B.degree v.1 := Finset.sum_add_distrib
      _ = 2 * #H.edgeFinset + #B.edgeFinset := by
        rw [H.sum_degrees_eq_twice_card_edges, h_cut_sum_subtype]
  change #B.edgeFinset + 2 * #H.edgeFinset = ∑ v ∈ X, G.degree v
  rw [Nat.add_comm]
  exact h_sum.symm

/-- Three pairwise disjoint `k`-sets cannot fit in a `(2k+1)`-element
universe when `k ≥ 2`. -/
theorem oddKneser_no_triangle {α : Type*} [Fintype α] [DecidableEq α]
    {k : ℕ} (hα : Fintype.card α = 2 * k + 1) (hk : 2 ≤ k)
    {A B C : KneserVertex α k}
    (hAB : KneserAdj A B) (hAC : KneserAdj A C)
    (hBC : KneserAdj B C) : False := by
  have hAB_ne : A.1 ≠ B.1 := by
    intro h
    have h_nonempty : A.1.Nonempty := Finset.card_pos.mp (by omega)
    obtain ⟨x, hx⟩ := h_nonempty
    exact Finset.disjoint_left.mp hAB hx (h ▸ hx)
  have h_union := common_disjoint_kset_union_card hα A.2 B.2 C.2
    hAB_ne hAC.symm hBC.symm
  have h_disjoint_union : (A.1 ∪ B.1).card = 2 * k := by
    rw [Finset.card_union_of_disjoint hAB, A.2, B.2]
    omega
  omega

/-- The odd Kneser graph is triangle-free. -/
theorem oddKneserGraph_cliqueFree_three {α : Type*} [Fintype α]
    [DecidableEq α] {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    (hk : 2 ≤ k) :
    (kneserGraph (α := α) k (by omega)).CliqueFree 3 := by
  intro s hs
  rw [SimpleGraph.is3Clique_iff] at hs
  obtain ⟨A, B, C, hAB, hAC, hBC, -⟩ := hs
  exact oddKneser_no_triangle hα hk hAB hAC hBC

/-- The balanced two-part Turán graph on `2k` vertices has exactly `k²`
edges. -/
theorem card_edgeFinset_turanGraph_two (k : ℕ) :
    #(SimpleGraph.turanGraph (2 * k) 2).edgeFinset = k ^ 2 := by
  rw [SimpleGraph.card_edgeFinset_turanGraph]
  norm_num
  rw [show (2 * k) ^ 2 = 4 * k ^ 2 by ring]
  simp

/-- The balanced two-part Turán graph contains an explicit `K₂,₂` as soon as
each part contains two vertices. -/
theorem turanGraph_two_has_K22 {k : ℕ} (hk : 2 ≤ k) :
    ∃ A B C D : Fin (2 * k),
      A ≠ B ∧ C ≠ D ∧
      (SimpleGraph.turanGraph (2 * k) 2).Adj A C ∧
      (SimpleGraph.turanGraph (2 * k) 2).Adj A D ∧
      (SimpleGraph.turanGraph (2 * k) 2).Adj B C ∧
      (SimpleGraph.turanGraph (2 * k) 2).Adj B D := by
  let A : Fin (2 * k) := ⟨0, by omega⟩
  let B : Fin (2 * k) := ⟨2, by omega⟩
  let C : Fin (2 * k) := ⟨1, by omega⟩
  let D : Fin (2 * k) := ⟨3, by omega⟩
  refine ⟨A, B, C, D, ?_⟩
  norm_num [A, B, C, D, SimpleGraph.turanGraph_adj]

/--
Every induced subgraph of the odd Kneser graph on exactly `2k` vertices has
strictly fewer than `k²` internal edges.  Turán's theorem gives the weak
bound; its equality classification would make the induced graph isomorphic to
the balanced complete bipartite graph, whose explicit `K₂,₂` contradicts
`oddKneser_no_K22`.
-/
theorem oddKneser_induce_card_edges_lt_sq {α : Type*} [Fintype α]
    [DecidableEq α] {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    (hk : 2 ≤ k) (X : Finset (KneserVertex α k)) (hX : X.card = 2 * k) :
    #((kneserGraph (α := α) k (by omega)).induce
        (↑X : Set (KneserVertex α k))).edgeFinset < k ^ 2 := by
  let G : SimpleGraph (KneserVertex α k) := kneserGraph (α := α) k (by omega)
  let H : SimpleGraph (↥(↑X : Set (KneserVertex α k))) := G.induce ↑X
  letI : DecidableRel G.Adj := by
    dsimp only [G]
    infer_instance
  letI : DecidableRel H.Adj := by
    dsimp only [H]
    infer_instance
  have hG_triangleFree : G.CliqueFree 3 := by
    simpa [G] using oddKneserGraph_cliqueFree_three hα hk
  have hH_triangleFree : H.CliqueFree 3 := by
    simpa only [H, SimpleGraph.cliqueFree_induce_iff] using hG_triangleFree.cliqueFreeOn
  have h_vertex_card : Fintype.card (↥(↑X : Set (KneserVertex α k))) = 2 * k := by
    simpa [hX]
  have h_formula :
      ((2 * k) ^ 2 - ((2 * k) % 2) ^ 2) * (2 - 1) / (2 * 2) +
        ((2 * k) % 2).choose 2 = k ^ 2 := by
    rw [← SimpleGraph.card_edgeFinset_turanGraph]
    exact card_edgeFinset_turanGraph_two k
  have h_edge_le : #H.edgeFinset ≤ k ^ 2 := by
    have h := hH_triangleFree.card_edgeFinset_le (r := 2)
    dsimp only at h
    rw [h_vertex_card] at h
    rw [h_formula] at h
    exact h
  change #H.edgeFinset < k ^ 2
  refine h_edge_le.lt_of_ne ?_
  intro h_edge_eq
  have h_max : H.IsTuranMaximal 2 := by
    refine ⟨hH_triangleFree, ?_⟩
    intro J _ hJ_triangleFree
    have hJ := hJ_triangleFree.card_edgeFinset_le (r := 2)
    dsimp only at hJ
    rw [h_vertex_card] at hJ
    rw [h_formula] at hJ
    rw [h_edge_eq]
    simpa using hJ
  have h_iso : Nonempty (H ≃g SimpleGraph.turanGraph (2 * k) 2) := by
    have h := h_max.nonempty_iso_turanGraph
    rw [h_vertex_card] at h
    exact h
  obtain ⟨f⟩ := h_iso
  obtain ⟨A, B, C, D, hAB, hCD, hAC, hAD, hBC, hBD⟩ := turanGraph_two_has_K22 hk
  let A' := f.symm A
  let B' := f.symm B
  let C' := f.symm C
  let D' := f.symm D
  have hAB' : A' ≠ B' := by
    intro h
    apply hAB
    simpa [A', B'] using congrArg f h
  have hCD' : C' ≠ D' := by
    intro h
    apply hCD
    simpa [C', D'] using congrArg f h
  have hAC' : H.Adj A' C' := f.symm.map_adj_iff.mpr hAC
  have hAD' : H.Adj A' D' := f.symm.map_adj_iff.mpr hAD
  have hBC' : H.Adj B' C' := f.symm.map_adj_iff.mpr hBC
  have hBD' : H.Adj B' D' := f.symm.map_adj_iff.mpr hBD
  exact oddKneser_no_K22 hα
    (fun h ↦ hAB' (Subtype.ext h))
    (fun h ↦ hCD' (Subtype.ext h))
    (by simpa [H, G, kneserGraph, KneserAdj] using hAC')
    (by simpa [H, G, kneserGraph, KneserAdj] using hAD')
    (by simpa [H, G, kneserGraph, KneserAdj] using hBC')
    (by simpa [H, G, kneserGraph, KneserAdj] using hBD')

/-- Integer-normalized form of the strict endpoint bound, ready for the
regular-degree boundary calculation. -/
theorem oddKneser_induce_card_edges_le_sq_sub_one {α : Type*} [Fintype α]
    [DecidableEq α] {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    (hk : 2 ≤ k) (X : Finset (KneserVertex α k)) (hX : X.card = 2 * k) :
    #((kneserGraph (α := α) k (by omega)).induce
        (↑X : Set (KneserVertex α k))).edgeFinset ≤ k ^ 2 - 1 := by
  have h := oddKneser_induce_card_edges_lt_sq hα hk X hX
  omega

/-- The endpoint edge boundary is at least two larger than the boundary of an
edge: every `2k`-vertex set in `KG(2k+1,k)` sends at least `2k+2` edges to its
complement. -/
theorem oddKneser_endpoint_boundary_ge {α : Type*} [Fintype α]
    [DecidableEq α] {k : ℕ} (hα : Fintype.card α = 2 * k + 1)
    (hk : 2 ≤ k) (X : Finset (KneserVertex α k)) (hX : X.card = 2 * k) :
    2 * k + 2 ≤
      #((kneserGraph (α := α) k (by omega)).between
        (↑X : Set (KneserVertex α k)) (↑(Xᶜ) : Set (KneserVertex α k))).edgeFinset := by
  let G : SimpleGraph (KneserVertex α k) := kneserGraph (α := α) k (by omega)
  have h_degree_sum : ∑ v ∈ X, G.degree v = (2 * k) * (k + 1) := by
    calc
      (∑ v ∈ X, G.degree v) = ∑ _v ∈ X, (k + 1) := by
        apply Finset.sum_congr rfl
        intro v _
        simpa only [G] using oddKneserGraph_degree hα (by omega) v
      _ = X.card * (k + 1) := by simp
      _ = (2 * k) * (k + 1) := by rw [hX]
  have h_cut_identity := card_between_add_twice_card_induce_eq_sum_degrees G X
  have h_internal : #(G.induce (↑X : Set (KneserVertex α k))).edgeFinset < k ^ 2 := by
    simpa only [G] using oddKneser_induce_card_edges_lt_sq hα hk X hX
  rw [h_degree_sum] at h_cut_identity
  have h_expand : (2 * k) * (k + 1) = 2 * k ^ 2 + 2 * k := by ring
  rw [h_expand] at h_cut_identity
  change 2 * k + 2 ≤
    #(G.between (↑X : Set (KneserVertex α k))
      (↑(Xᶜ) : Set (KneserVertex α k))).edgeFinset
  omega

#print axioms common_disjoint_kset_eq_compl
#print axioms common_disjoint_kset_union_card
#print axioms common_disjoint_kset_unique
#print axioms oddKneser_commonNeighbor_unique
#print axioms oddKneser_no_K22
#print axioms kneserNeighborEquiv
#print axioms kneserGraph_degree_eq_choose_compl
#print axioms oddKneserGraph_degree
#print axioms oddKneserGraph_isRegular
#print axioms degree_eq_induce_add_between
#print axioms card_between_add_twice_card_induce_eq_sum_degrees
#print axioms oddKneser_no_triangle
#print axioms oddKneserGraph_cliqueFree_three
#print axioms card_edgeFinset_turanGraph_two
#print axioms turanGraph_two_has_K22
#print axioms oddKneser_induce_card_edges_lt_sq
#print axioms oddKneser_induce_card_edges_le_sq_sub_one
#print axioms oddKneser_endpoint_boundary_ge

end KneserEndpoint
