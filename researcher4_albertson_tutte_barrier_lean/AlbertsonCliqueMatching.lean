import AlbertsonTutteBarrier
import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex

/-!
# A clique plus a matching gives a coloring of the complement

This closes the nonconformality input to the tight Tutte-witness theorem.
The graph, matching, and proper coloring are native Mathlib objects.
-/

open Set SimpleGraph

namespace AlbertsonTutteBarrier

variable {V : Type*} {G : SimpleGraph V}

/-- Distinct complement-adjacent vertices cannot belong to the same matching edge. -/
theorem matching_toEdge_ne_of_compl_adj {M : G.Subgraph} (hM : M.IsMatching)
    {u v : M.verts} (huv : Gᶜ.Adj u.val v.val) : hM.toEdge u ≠ hM.toEdge v := by
  intro heq
  have hu := hM.mem_coe_toEdge u.property
  have hv := hM.mem_coe_toEdge v.property
  rw [← heq] at hv
  have hedge := (Sym2.mem_and_mem_iff huv.1).mp ⟨hu, hv⟩
  have hmem := (hM.toEdge u).property
  rw [hedge] at hmem
  exact huv.2 hmem.adj_sub

/-- Use one color for `T` and one for each matching edge outside `T`. -/
noncomputable def cliqueMatchingColoring (T : Set V) (hT : G.IsClique T)
    (M : G.Subgraph) (hverts : M.verts = Tᶜ) (hM : M.IsMatching) :
    Gᶜ.Coloring (Option M.edgeSet) := by
  classical
  refine Coloring.mk (fun v => if hv : v ∈ T then none
    else some (hM.toEdge ⟨v, by rw [hverts]; exact hv⟩)) ?_
  intro v w hvw heq
  by_cases hv : v ∈ T <;> by_cases hw : w ∈ T
  · exact hvw.2 (hT hv hw hvw.1)
  · simp [hv, hw] at heq
  · simp [hv, hw] at heq
  · exact matching_toEdge_ne_of_compl_adj hM
      (u := ⟨v, by rw [hverts]; exact hv⟩)
      (v := ⟨w, by rw [hverts]; exact hw⟩) hvw
      (Option.some.inj (by simpa [hv, hw] using heq))

/-- Every native matching edge has exactly two vertices in its assignment fiber. -/
theorem matching_edge_fiber_ncard {M : G.Subgraph} (hM : M.IsMatching)
    (e : M.edgeSet) : (hM.toEdge ⁻¹' {e}).ncard = 2 := by
  rcases e with ⟨⟨u, v⟩, huv⟩
  rw [hM.toEdge_preimage_singleton huv]
  apply Set.ncard_pair
  intro heq
  exact huv.ne (congrArg Subtype.val heq)

/-- Exact matching cardinality, derived from the actual two-element edge fibers. -/
theorem matching_verts_ncard [Finite V] {M : G.Subgraph} (hM : M.IsMatching) :
    M.verts.ncard = 2 * M.edgeSet.ncard := by
  classical
  let := Fintype.ofFinite M.verts
  let := Fintype.ofFinite M.edgeSet
  have hfiber (e : M.edgeSet) :
      (Finset.univ.filter (fun v : M.verts => hM.toEdge v = e)).card = 2 := by
    have heq : (↑(Finset.univ.filter (fun v : M.verts => hM.toEdge v = e)) :
        Set M.verts) = hM.toEdge ⁻¹' {e} := by ext v; simp
    rw [← Set.ncard_coe_finset, heq]
    exact matching_edge_fiber_ncard hM e
  have hcount := Finset.card_eq_sum_card_fiberwise
    (f := hM.toEdge) (s := Finset.univ) (t := Finset.univ)
    (by intro v _; simp)
  simp_rw [hfiber] at hcount
  simpa [← Nat.card_eq_fintype_card, Nat.card_coe_set_eq, Nat.mul_comm] using hcount

/-- The general complement-coloring bound. The quotient is exact because the
matching pairs all vertices outside `T`. Empty `T` is allowed (one unused color). -/
theorem colorable_compl_of_clique_matching [Finite V] (T : Set V)
    (hT : G.IsClique T) (hm : HasMatchingOff G T) :
    Gᶜ.Colorable (1 + (Nat.card V - T.ncard) / 2) := by
  classical
  obtain ⟨M, hverts, hM⟩ := hm
  let := Fintype.ofFinite M.edgeSet
  have hcol : Gᶜ.Colorable (M.edgeSet.ncard + 1) := by
    simpa [← Nat.card_eq_fintype_card, Nat.card_coe_set_eq] using
      (cliqueMatchingColoring T hT M hverts hM).colorable
  have hcount := matching_verts_ncard hM
  have htotal := Set.ncard_add_ncard_compl T
  rw [← hverts] at htotal
  have hnum : M.edgeSet.ncard + 1 = 1 + (Nat.card V - T.ncard) / 2 := by omega
  rwa [← hnum]

/-- On order `2*k+1`, a triangle with a complementary perfect matching would
make the complement `k`-colorable. No criticality or topology is assumed. -/
theorem no_matchingOff_triangle_of_not_colorable [Finite V] {k : ℕ}
    (horder : Nat.card V = 2 * k + 1) (hnot : ¬ Gᶜ.Colorable k)
    (T : Set V) (hclique : G.IsClique T) (hT : T.ncard = 3) :
    ¬ HasMatchingOff G T := by
  intro hm
  have hcol := colorable_compl_of_clique_matching T hclique hm
  have hle := Set.ncard_le_card T
  have hnum : 1 + (Nat.card V - T.ncard) / 2 = k := by omega
  exact hnot (hnum ▸ hcol)

/-- The complete finite triangle-to-summary interface: the formerly external
nonconformality hypothesis is now derived from a native coloring obstruction. -/
theorem exists_tight_witness_of_triangle [Finite V] {k : ℕ}
    (hfc : FactorCritical G) (horder : Nat.card V = 2 * k + 1)
    (hnot : ¬ Gᶜ.Colorable k) (T : Set V) (hclique : G.IsClique T)
    (hT : T.ncard = 3) :
    ∃ B : Set V, T ⊆ B ∧ oddCount G B + 1 = B.ncard := by
  exact exists_tight_witness_of_three_deleted G hfc T hT
    (no_matchingOff_triangle_of_not_colorable horder hnot T hclique hT)

/-- The same interface stated with Mathlib's chromatic number. -/
theorem exists_tight_witness_of_chromaticNumber [Finite V] {k : ℕ}
    (hfc : FactorCritical G) (horder : Nat.card V = 2 * k + 1)
    (hchrom : (k : ℕ∞) < Gᶜ.chromaticNumber) (T : Set V)
    (hclique : G.IsClique T) (hT : T.ncard = 3) :
    ∃ B : Set V, T ⊆ B ∧ oddCount G B + 1 = B.ncard := by
  exact exists_tight_witness_of_triangle hfc horder
    (fun hc => (not_le_of_gt hchrom) hc.chromaticNumber_le) T hclique hT

end AlbertsonTutteBarrier
