import AlbertsonTriangleDeletion
import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Combinatorics.Pigeonhole

/-!
A finite coloring supplies actual complement cliques by pigeonhole. Applied to
one vertex deletion, this supplies the triangle needed by the deletion endpoint
without a special clique-and-matching cover or any drawing hypothesis.
-/

open Finset

namespace AlbertsonColoringClique

variable {V A : Type*} [Fintype V] [Fintype A] (G : SimpleGraph V)

/-- A proper coloring on more than `d` times as many vertices as colors gives
an actual `(d+1)`-clique in the complement. -/
theorem exists_compl_clique_of_coloring (C : G.Coloring A) (d : ℕ)
    (hsize : Fintype.card A * d < Fintype.card V) :
    ∃ T : Finset V, Gᶜ.IsNClique (d + 1) T := by
  classical
  obtain ⟨c, hc⟩ := Fintype.exists_lt_card_fiber_of_mul_lt_card (fun v => C v) hsize
  obtain ⟨T, hT, hcard⟩ := Finset.exists_subset_card_eq (Nat.succ_le_of_lt hc)
  refine ⟨T, ?_, hcard⟩
  intro u hu v hv huv
  refine ⟨huv, ?_⟩
  exact C.not_adj_of_mem_colorClass (Finset.mem_filter.mp (hT hu)).2
    (Finset.mem_filter.mp (hT hv)).2

omit [Fintype V] in
/-- A coloring of an induced ambient complement supplies a clique in the
ambient graph, with its actual vertices contained in the selected subset. -/
theorem exists_clique_of_induced_compl_coloring [DecidableEq V] (S : Finset V)
    (C : (Gᶜ.induce (S : Set V)).Coloring A) (d : ℕ)
    (hsize : Fintype.card A * d < S.card) :
    ∃ T : Finset V, T ⊆ S ∧ G.IsNClique (d + 1) T := by
  classical
  obtain ⟨T, hT⟩ := exists_compl_clique_of_coloring (Gᶜ.induce (S : Set V)) C d
    (by simpa using hsize)
  let f : ↑(S : Set V) ↪ V := Function.Embedding.subtype _
  refine ⟨T.map f, ?_, ?_, by simpa using hT.card_eq⟩
  · intro v hv
    obtain ⟨w, _, rfl⟩ := Finset.mem_map.mp hv
    exact w.property
  · intro u hu v hv huv
    obtain ⟨u, huT, rfl⟩ := Finset.mem_map.mp hu
    obtain ⟨v, hvT, rfl⟩ := Finset.mem_map.mp hv
    have h := hT.isClique huT hvT (ne_of_apply_ne f huv)
    by_contra hn
    exact h.2 ⟨huv, hn⟩

omit [Fintype A] in
/-- At order `2*r`, one `(r-1)`-colorable vertex deletion of `Gᶜ` supplies
a triangle of `G` avoiding that vertex. No optimality or special cover is used. -/
theorem exists_triangle_of_deletion_colorable [DecidableEq V] (v : V) (r : ℕ)
    (hr : 0 < r) (horder : Fintype.card V = 2 * r)
    (hc : (Gᶜ.induce (↑((univ : Finset V).erase v) : Set V)).Colorable (r - 1)) :
    ∃ T : Finset V, v ∉ T ∧ G.IsNClique 3 T := by
  obtain ⟨C⟩ := hc
  obtain ⟨T, hT, htri⟩ := exists_clique_of_induced_compl_coloring G (univ.erase v) C 2
    (by simp only [Fintype.card_fin, card_erase_of_mem (mem_univ v), card_univ, horder]
        omega)
  refine ⟨T, ?_, htri⟩
  intro hv
  exact (Finset.mem_erase.mp (hT hv)).1 rfl

omit [Fintype A] in
/-- One deletion coloring and the global triangle-intersection condition feed
the full ambient complement-clique endpoint, with the triangle also returned. -/
theorem exists_disjoint_compl_cliques_of_deletion_colorable [DecidableEq V]
    [DecidableRel G.Adj] (v : V) (r : ℕ) (hr : 0 < r)
    (horder : Fintype.card V = 2 * r)
    (hc : (Gᶜ.induce (↑((univ : Finset V).erase v) : Set V)).Colorable (r - 1))
    (hmeet : ∀ T U : Finset V, G.IsNClique 3 T → G.IsNClique 3 U → ¬ Disjoint T U)
    (q : ℕ) (hq : 0 < q) (hbudget : q + 3 * G.maxDegree ≤ G.edgeFinset.card + 3) :
    ∃ T X Y : Finset V, v ∉ T ∧ G.IsNClique 3 T ∧ X ⊆ Tᶜ ∧ Y ⊆ Tᶜ ∧
      Gᶜ.IsClique (X : Set V) ∧ Gᶜ.IsClique (Y : Set V) ∧ Disjoint X Y ∧
      X.card ≤ G.maxDegree ∧ Y.card ≤ G.maxDegree ∧
      4 * q ≤ (Fintype.card V - 3) * (X.card + Y.card) := by
  obtain ⟨T, hvT, hT⟩ := exists_triangle_of_deletion_colorable G v r hr horder hc
  obtain ⟨X, Y, hX, hY, hcX, hcY, hXY, hx, hy, hsize⟩ :=
    AlbertsonTriangleDeletion.exists_disjoint_compl_cliques_of_triangle G hT
      (fun U hU => hmeet T U hT hU) q hq hbudget
  exact ⟨T, X, Y, hvT, hT, hX, hY, hcX, hcY, hXY, hx, hy, hsize⟩

end AlbertsonColoringClique
