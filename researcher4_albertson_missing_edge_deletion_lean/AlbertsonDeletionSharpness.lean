import AlbertsonMissingEdgeDeletion
import Mathlib.Data.Fin.Embedding
import Mathlib.Data.Set.Card

/-!
Uniform sharpness of the missing-edge deletion threshold. All constructions use
native edge sets, support, graph maps and induced graphs. The exact-budget
improvement characterization is adapted from the reviewer-authored refinement
at Discovery Net height 3150; it is not claimed as a new result here.
Reviewer source:
https://github.com/njallskarp/math_source_code_open/blob/main/albertson_missing_edge_deletion_lean_independent_review_20260905/ReviewAudit.lean
-/

open Finset

namespace AlbertsonDeletionSharpness

variable {V : Type*} [Fintype V]

/-- Select exactly the requested number of edges from any finite graph. -/
theorem exists_subgraph_ncard_edges (G : SimpleGraph V) (f : ℕ)
    (hf : f ≤ G.edgeSet.ncard) :
    ∃ H : SimpleGraph V, H ≤ G ∧ H.edgeSet.ncard = f := by
  classical
  have hcard : f ≤ G.edgeFinset.card := by
    simpa [SimpleGraph.edgeFinset, Set.ncard_eq_toFinset_card'] using hf
  obtain ⟨E, hEG, hEcard⟩ := Finset.exists_subset_card_eq hcard
  have hset : (E : Set (Sym2 V)) ⊆ G.edgeSet := by
    intro e he
    exact G.mem_edgeFinset.mp (hEG he)
  have hdiag : Disjoint (E : Set (Sym2 V)) Sym2.diagSet := by
    rw [Set.disjoint_left]
    intro e he hd
    exact G.not_isDiag_of_mem_edgeSet (hset he) hd
  have hedge : (SimpleGraph.fromEdgeSet (E : Set (Sym2 V))).edgeSet = E := by
    rw [SimpleGraph.edgeSet_fromEdgeSet, sdiff_eq_left.mpr hdiag]
  refine ⟨SimpleGraph.fromEdgeSet (E : Set (Sym2 V)), ?_, ?_⟩
  · rw [← SimpleGraph.edgeSet_subset_edgeSet, hedge]
    exact hset
  · simpa [hedge] using hEcard

/-- Every feasible edge count is realized on a prescribed finite order. -/
theorem exists_graph_ncard_edges (s f : ℕ) (hf : f ≤ s.choose 2) :
    ∃ H : SimpleGraph (Fin s), H.edgeSet.ncard = f := by
  have htop : f ≤ (⊤ : SimpleGraph (Fin s)).edgeSet.ncard := by
    classical
    have he : (⊤ : SimpleGraph (Fin s)).edgeSet.ncard = s.choose 2 := by
      simpa only [SimpleGraph.edgeFinset_card, Set.fintypeCard_eq_ncard,
        Fintype.card_fin] using
        (SimpleGraph.card_edgeFinset_top_eq_card_choose_two (V := Fin s))
    exact hf.trans_eq he.symm
  obtain ⟨H, _, hH⟩ := exists_subgraph_ncard_edges (⊤ : SimpleGraph (Fin s)) f htop
  exact ⟨H, hH⟩

/-- Realize a positive budget on its least possible support, with arbitrary
additional isolated vertices supplied by a native graph embedding. -/
theorem exists_exact_support_graph (n s f : ℕ) (hsn : s ≤ n)
    (hgap : (s - 1).choose 2 < f) (hcap : f ≤ s.choose 2) :
    ∃ H : SimpleGraph (Fin n), H.edgeSet.ncard = f ∧ H.support.ncard = s := by
  classical
  obtain ⟨G, hG⟩ := exists_graph_ncard_edges s f hcap
  have hsupp : G.support.ncard = s := by
    have hupper : G.support.ncard ≤ s := by
      simpa using Set.ncard_le_ncard (Set.subset_univ G.support)
    have hedge := AlbertsonMissingEdgeDeletion.card_edges_le_choose_support G
    have hedge' : f ≤ G.support.ncard.choose 2 := by
      simpa only [SimpleGraph.edgeFinset_card, Set.fintypeCard_eq_ncard, hG] using hedge
    by_contra hne
    have hsmall : G.support.ncard ≤ s - 1 := by omega
    have hc := Nat.choose_le_choose 2 hsmall
    omega
  let e : Fin s ↪ Fin n := Fin.castLEEmb hsn
  refine ⟨G.map e, ?_, ?_⟩
  · have he := SimpleGraph.card_edgeFinset_map e G
    simpa only [SimpleGraph.edgeFinset_card, Set.fintypeCard_eq_ncard, hG] using he
  · rw [SimpleGraph.support_map, Set.ncard_image_of_injective _ e.injective, hsupp]

/-- Exact-budget specialization of the height-3150 reviewer characterization,
expressed as equality of native vertex sets. Positivity is essential. -/
theorem improved_vertices_eq_support (H : SimpleGraph V) (f : ℕ) (hf : 0 < f)
    (hexact : H.edgeSet.ncard = f) :
    {v : V | (H.induce ({v}ᶜ : Set V)).edgeSet.ncard ≤ f - 1} = H.support := by
  classical
  ext v
  have he : H.edgeFinset.card = f := by
    simpa [SimpleGraph.edgeFinset, Set.ncard_eq_toFinset_card'] using hexact
  have hd := AlbertsonMissingEdgeDeletion.card_vertex_deletion H v
  have hp := H.degree_pos_iff_mem_support v
  change (H.induce ({v}ᶜ : Set V)).edgeSet.ncard ≤ f - 1 ↔ v ∈ H.support
  have hn : (H.induce ({v}ᶜ : Set V)).edgeSet.ncard =
      (H.induce ({v}ᶜ : Set V)).edgeFinset.card := by
    simp [SimpleGraph.edgeFinset, Set.ncard_eq_toFinset_card']
  rw [hn]
  rw [hd, he, ← hp]
  omega

/-- An actual graph attains the lower bound on the number of improved deletions. -/
theorem exists_exactly_s_improvements (n s f : ℕ) (hsn : s ≤ n)
    (hgap : (s - 1).choose 2 < f) (hcap : f ≤ s.choose 2) :
    ∃ H : SimpleGraph (Fin n), H.edgeSet.ncard = f ∧
      {v : Fin n | (H.induce ({v}ᶜ : Set (Fin n))).edgeSet.ncard ≤ f - 1}.ncard = s := by
  obtain ⟨H, he, hs⟩ := exists_exact_support_graph n s f hsn hgap hcap
  refine ⟨H, he, ?_⟩
  rw [improved_vertices_eq_support H f (lt_of_le_of_lt (Nat.zero_le _) hgap) he, hs]

/-- Complete parameterized characterization: the sharp support threshold is
exactly the number of improved deletions guaranteed by an upper budget alone. -/
theorem uniform_improvement_iff_le (n s f t : ℕ) (hsn : s ≤ n)
    (hgap : (s - 1).choose 2 < f) (hcap : f ≤ s.choose 2) :
    (∀ H : SimpleGraph (Fin n), H.edgeSet.ncard ≤ f →
      t ≤ {v : Fin n | (H.induce ({v}ᶜ : Set (Fin n))).edgeSet.ncard ≤ f - 1}.ncard) ↔
      t ≤ s := by
  classical
  constructor
  · intro hall
    obtain ⟨H, he, himproved⟩ := exists_exactly_s_improvements n s f hsn hgap hcap
    simpa [himproved] using hall H (le_of_eq he)
  · intro hts H hbudget
    have hbudget' : H.edgeFinset.card ≤ f := by
      simpa [SimpleGraph.edgeFinset, Set.ncard_eq_toFinset_card'] using hbudget
    have htgap : (t - 1).choose 2 < f :=
      (Nat.choose_le_choose 2 (Nat.sub_le_sub_right hts 1)).trans_lt hgap
    obtain ⟨S, hcard, hS⟩ := AlbertsonMissingEdgeDeletion.exists_improved_deletions
      H f t hbudget' (by simpa using hts.trans hsn) htgap
    have hsub : (S : Set (Fin n)) ⊆
        {v : Fin n | (H.induce ({v}ᶜ : Set (Fin n))).edgeSet.ncard ≤ f - 1} := by
      intro v hv
      simpa [SimpleGraph.edgeFinset, Set.ncard_eq_toFinset_card'] using hS v hv
    simpa [hcard] using Set.ncard_le_ncard hsub

end AlbertsonDeletionSharpness
