import Mathlib.Combinatorics.SimpleGraph.DegreeSum
import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.ByContra

/-!
The finite graph-to-clique bridge in the triangle-free branch at Discovery Net
height 3014. The classical degree-square argument uses native darts and degrees.
No critical-graph, crossing-number, drawing or enumeration premise is imported.
-/

open Finset

namespace AlbertsonTriangleFreeCliques

variable {V : Type*} [Fintype V] (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Weighted counting over the first endpoint of each oriented edge. -/
theorem sum_dart_fst_degree :
    ∑ d : G.Dart, G.degree d.fst = ∑ v : V, G.degree v ^ 2 := by
  classical
  have h := Finset.sum_fiberwise' (univ : Finset G.Dart)
    (fun d : G.Dart => d.fst) (fun v : V => G.degree v)
  simpa [G.dart_fst_fiber_card_eq_degree, pow_two] using h.symm

/-- Reversing darts gives the same degree-square sum at their second endpoints. -/
theorem sum_dart_snd_degree :
    ∑ d : G.Dart, G.degree d.snd = ∑ v : V, G.degree v ^ 2 := by
  let e : G.Dart ≃ G.Dart :=
    ⟨SimpleGraph.Dart.symm, SimpleGraph.Dart.symm,
      SimpleGraph.Dart.symm_symm, SimpleGraph.Dart.symm_symm⟩
  have h := e.sum_comp (fun d : G.Dart => G.degree d.fst)
  change (∑ d : G.Dart, G.degree d.snd) = ∑ d : G.Dart, G.degree d.fst at h
  exact h.trans (sum_dart_fst_degree G)

/-- Every graph with an edge has an edge whose endpoint-degree sum is at least
twice the average degree. The natural-number form retains exact rounding. -/
theorem exists_adj_degree_sum (hm : 0 < G.edgeFinset.card) :
    ∃ u v, G.Adj u v ∧
      4 * G.edgeFinset.card ≤ Fintype.card V * (G.degree u + G.degree v) := by
  classical
  by_contra! h
  have hd : Nonempty G.Dart := Fintype.card_pos_iff.mp (by
    rw [G.dart_card_eq_twice_card_edges]
    omega)
  obtain ⟨d⟩ := hd
  have hpoint (d : G.Dart) :
      Fintype.card V * (G.degree d.fst + G.degree d.snd) < 4 * G.edgeFinset.card :=
    h d.fst d.snd d.adj
  have ht : (∑ d : G.Dart, Fintype.card V * (G.degree d.fst + G.degree d.snd)) <
      ∑ _ : G.Dart, 4 * G.edgeFinset.card := by
    apply Finset.sum_lt_sum
    · intro d _
      exact (hpoint d).le
    · exact ⟨d, mem_univ d, hpoint d⟩
  rw [← Finset.mul_sum, Finset.sum_add_distrib,
    sum_dart_fst_degree, sum_dart_snd_degree] at ht
  simp only [Finset.sum_const,
    Finset.card_univ, nsmul_eq_mul, G.dart_card_eq_twice_card_edges] at ht
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq (univ : Finset V)
    (fun v : V => G.degree v) (fun _ => (1 : ℕ))
  simp only [mul_one, one_pow, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, mul_one, G.sum_degrees_eq_twice_card_edges] at hcs
  nlinarith

omit [Fintype V] [DecidableRel G.Adj] in
/-- Adjacent vertices of a triangle-free graph have disjoint neighborhoods. -/
theorem disjoint_neighborSet_of_triangleFree (htri : G.CliqueFree 3)
    {u v : V} (huv : G.Adj u v) : Disjoint (G.neighborSet u) (G.neighborSet v) := by
  rw [Set.disjoint_left]
  intro w huw hvw
  exact (G.isIndepSet_neighborSet_of_triangleFree htri w)
    huw.symm hvw.symm huv.ne huv

/-- Actual disjoint cliques in the complement, with the degree-square size bound. -/
theorem exists_disjoint_compl_cliques (htri : G.CliqueFree 3)
    (hm : 0 < G.edgeFinset.card) :
    ∃ A B : Finset V, Gᶜ.IsClique (A : Set V) ∧ Gᶜ.IsClique (B : Set V) ∧
      Disjoint A B ∧ A.card ≤ G.maxDegree ∧ B.card ≤ G.maxDegree ∧
      4 * G.edgeFinset.card ≤ Fintype.card V * (A.card + B.card) := by
  classical
  obtain ⟨u, v, huv, hsize⟩ := exists_adj_degree_sum G hm
  refine ⟨G.neighborFinset u, G.neighborFinset v, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simpa using G.isIndepSet_neighborSet_of_triangleFree htri u
  · simpa using G.isIndepSet_neighborSet_of_triangleFree htri v
  · apply Finset.disjoint_coe.mp
    simpa using disjoint_neighborSet_of_triangleFree G htri huv
  · simpa using G.degree_le_maxDegree u
  · simpa using G.degree_le_maxDegree v
  · simpa using hsize

/-- Apply the bridge inside an induced subgraph and return cliques in the ambient
complement, contained in the specified vertex set. -/
theorem exists_disjoint_compl_cliques_in_induce [DecidableEq V] (S : Finset V)
    (htri : (G.induce (S : Set V)).CliqueFree 3)
    (hm : 0 < (G.induce (S : Set V)).edgeFinset.card) :
    ∃ A B : Finset V, A ⊆ S ∧ B ⊆ S ∧
      Gᶜ.IsClique (A : Set V) ∧ Gᶜ.IsClique (B : Set V) ∧ Disjoint A B ∧
      A.card ≤ G.maxDegree ∧ B.card ≤ G.maxDegree ∧
      4 * (G.induce (S : Set V)).edgeFinset.card ≤ S.card * (A.card + B.card) := by
  classical
  let F := G.induce (S : Set V)
  let f : ↑(S : Set V) ↪ V := Function.Embedding.subtype _
  let e : Fᶜ ↪g Gᶜ := SimpleGraph.Embedding.complEquiv (SimpleGraph.Embedding.induce _)
  have hmap {C : Finset ↑(S : Set V)} (hc : Fᶜ.IsClique (C : Set ↑(S : Set V))) :
      Gᶜ.IsClique (C.map f : Set V) := by
    intro a ha b hb hab
    obtain ⟨a, haC, rfl⟩ := Finset.mem_map.mp ha
    obtain ⟨b, hbC, rfl⟩ := Finset.mem_map.mp hb
    exact e.map_adj_iff.mpr (hc haC hbC (ne_of_apply_ne f hab))
  have hsub (C : Finset ↑(S : Set V)) : C.map f ⊆ S := by
    intro x hx
    obtain ⟨v, _, rfl⟩ := Finset.mem_map.mp hx
    exact v.property
  have hmax : F.maxDegree ≤ G.maxDegree := by
    apply F.maxDegree_le_of_forall_degree_le
    intro v
    have hv : F.degree v ≤ G.degree v.val := by
      rw [← F.card_neighborSet_eq_degree, ← G.card_neighborSet_eq_degree]
      exact Fintype.card_le_of_injective
        ((SimpleGraph.Embedding.induce (S : Set V)).mapNeighborSet v)
        ((SimpleGraph.Embedding.induce (S : Set V)).mapNeighborSet v).injective
    exact hv.trans (G.degree_le_maxDegree v.val)
  obtain ⟨A, B, hA, hB, hAB, ha, hb, hsize⟩ := exists_disjoint_compl_cliques F htri hm
  refine ⟨A.map f, B.map f, hsub A, hsub B, hmap hA, hmap hB,
    (Finset.disjoint_map f).mpr hAB, ?_, ?_, ?_⟩
  · simpa using ha.trans hmax
  · simpa using hb.trans hmax
  · simpa using hsize

end AlbertsonTriangleFreeCliques
