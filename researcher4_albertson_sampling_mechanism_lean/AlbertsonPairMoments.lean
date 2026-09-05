import Mathlib.Combinatorics.SimpleGraph.DeleteEdges
import Mathlib.Combinatorics.SimpleGraph.DegreeSum
import Mathlib.Data.Finset.Prod
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

open scoped BigOperators
open Finset

namespace AlbertsonPairMoments

/-- The `0`/`1` indicator of adjacency in a finite simple graph. -/
def adjBit {V : Type*} (G : SimpleGraph V) [DecidableRel G.Adj]
    (u v : V) : ℕ :=
  if G.Adj u v then 1 else 0

theorem neighborFinset_deleteIncidenceSet
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] {u v : V} (hvu : v ≠ u) :
    (G.deleteIncidenceSet u).neighborFinset v = G.neighborFinset v \ {u} := by
  ext w
  simp [SimpleGraph.mem_neighborFinset, SimpleGraph.deleteIncidenceSet_adj, hvu]

theorem degree_deleteIncidenceSet_add_adjBit
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] {u v : V} (hvu : v ≠ u) :
    (G.deleteIncidenceSet u).degree v + adjBit G u v = G.degree v := by
  change #((G.deleteIncidenceSet u).neighborFinset v) + adjBit G u v =
    #(G.neighborFinset v)
  rw [neighborFinset_deleteIncidenceSet G hvu,
    Finset.sdiff_singleton_eq_erase]
  by_cases huv : G.Adj u v
  · have hu : u ∈ G.neighborFinset v := by
      simpa [SimpleGraph.mem_neighborFinset] using G.adj_symm huv
    have hpos : 0 < G.degree v := by
      change 0 < #(G.neighborFinset v)
      exact Finset.card_pos.mpr ⟨u, hu⟩
    simp only [adjBit, huv, if_true, Finset.card_erase_of_mem hu]
    exact Nat.sub_add_cancel hpos
  · have hu : u ∉ G.neighborFinset v := by
      simpa [SimpleGraph.mem_neighborFinset, G.adj_comm] using huv
    simp [adjBit, huv, Finset.erase_eq_self.mpr hu]

/-- Deleting two distinct vertices removes the sum of their degrees, with
the common edge (when present) restored once.  The additive form avoids any
truncated-subtraction side condition. -/
theorem card_edges_delete_two_add_degrees
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] {u v : V} (huv : u ≠ v) :
    #((G.deleteIncidenceSet u).deleteIncidenceSet v).edgeFinset +
        G.degree u + G.degree v =
      #G.edgeFinset + adjBit G u v := by
  rw [SimpleGraph.card_edgeFinset_deleteIncidenceSet,
    SimpleGraph.card_edgeFinset_deleteIncidenceSet]
  have hdu : G.degree u ≤ #G.edgeFinset := G.degree_le_card_edgeFinset u
  have hdv : (G.deleteIncidenceSet u).degree v ≤
      #(G.deleteIncidenceSet u).edgeFinset :=
    (G.deleteIncidenceSet u).degree_le_card_edgeFinset v
  have hdegree := degree_deleteIncidenceSet_add_adjBit G huv.symm
  have hcard := SimpleGraph.card_edgeFinset_deleteIncidenceSet G u
  omega

section PairSums

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Removing the diagonal from a double sum, over the integers. -/
theorem sum_offDiag_eq_sum_product_sub_diag (f : V × V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, f uv) =
      (∑ u : V, ∑ v : V, f (u, v)) - ∑ u : V, f (u, u) := by
  have h := Finset.sum_union (f := f)
    (Finset.disjoint_diag_offDiag (Finset.univ : Finset V))
  rw [Finset.diag_union_offDiag, Finset.sum_diag, Finset.sum_product] at h
  linarith

theorem sum_offDiag_fst (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, x uv.1) =
      ((Fintype.card V : ℤ) - 1) * ∑ u : V, x u := by
  rw [sum_offDiag_eq_sum_product_sub_diag]
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  rw [← Finset.mul_sum]
  ring_nf

theorem sum_offDiag_snd (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, x uv.2) =
      ((Fintype.card V : ℤ) - 1) * ∑ u : V, x u := by
  rw [sum_offDiag_eq_sum_product_sub_diag]
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  ring_nf

theorem sum_offDiag_fst_mul_snd (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, x uv.1 * x uv.2) =
      (∑ u : V, x u) ^ 2 - ∑ u : V, (x u) ^ 2 := by
  rw [sum_offDiag_eq_sum_product_sub_diag]
  simp_rw [← Finset.mul_sum]
  rw [← Finset.sum_mul]
  ring_nf

theorem sum_offDiag_add_sq (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, (x uv.1 + x uv.2) ^ 2) =
      2 * ((Fintype.card V : ℤ) - 2) * (∑ u : V, (x u) ^ 2) +
        2 * (∑ u : V, x u) ^ 2 := by
  simp_rw [add_sq, Finset.sum_add_distrib]
  rw [sum_offDiag_fst (fun u ↦ (x u) ^ 2),
    sum_offDiag_snd (fun u ↦ (x u) ^ 2)]
  simp_rw [mul_assoc]
  rw [← Finset.mul_sum, sum_offDiag_fst_mul_snd]
  ring_nf

end PairSums

section GraphPairSums

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (H : SimpleGraph V) [DecidableRel H.Adj]

/-- Integer-valued complement-edge indicator on an ordered pair. -/
def adjBitInt (u v : V) : ℤ :=
  if H.Adj u v then 1 else 0

/-- Defect attached to an ordered distinct pair.  For the Albertson
application, `H` is the complement and `x v = degree_G(v) - (r-1)`. -/
def pairDefect (x : V → ℤ) (u v : V) : ℤ :=
  x u + x v + adjBitInt H u v

omit [Fintype V] [DecidableEq V] in theorem pairDefect_comm (x : V → ℤ) (u v : V) :
    pairDefect H x u v = pairDefect H x v u := by
  simp only [pairDefect, adjBitInt, H.adj_comm]
  ring_nf

omit [DecidableEq V] in theorem sum_offDiag_adjBitInt :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag, adjBitInt H uv.1 uv.2) =
      2 * (#H.edgeFinset : ℤ) := by
  simp only [adjBitInt]
  rw [Finset.sum_boole]
  have hfilter :
      (Finset.univ : Finset V).offDiag.filter (fun uv ↦ H.Adj uv.1 uv.2) =
        (Finset.univ : Finset (V × V)).filter (fun uv ↦ H.Adj uv.1 uv.2) := by
    ext uv
    simp only [Finset.mem_filter, Finset.mem_offDiag, Finset.mem_univ, true_and]
    constructor
    · exact fun h ↦ h.2
    · intro h
      exact ⟨H.ne_of_adj h, h⟩
  rw [hfilter]
  exact_mod_cast H.two_mul_card_edgeFinset.symm

omit [DecidableEq V] in theorem sum_adj_fst (x : V → ℤ) :
    (∑ u : V, ∑ v : V, if H.Adj u v then x u else 0) =
      ∑ u : V, (H.degree u : ℤ) * x u := by
  apply Finset.sum_congr rfl
  intro u _
  rw [← Finset.sum_filter]
  rw [← H.neighborFinset_eq_filter]
  simp [SimpleGraph.card_neighborFinset_eq_degree, mul_comm]

omit [DecidableEq V] in theorem sum_adj_snd (x : V → ℤ) :
    (∑ u : V, ∑ v : V, if H.Adj u v then x v else 0) =
      ∑ u : V, (H.degree u : ℤ) * x u := by
  rw [Finset.sum_comm]
  simpa only [H.adj_comm] using sum_adj_fst H x

theorem sum_offDiag_adj_endpoint (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag,
        if H.Adj uv.1 uv.2 then x uv.1 + x uv.2 else 0) =
      2 * ∑ u : V, (H.degree u : ℤ) * x u := by
  rw [sum_offDiag_eq_sum_product_sub_diag]
  have hdiag :
      (∑ u : V, if H.Adj u u then x u + x u else 0) = 0 := by simp
  rw [hdiag, sub_zero]
  have hsplit : ∀ u v : V,
      (if H.Adj u v then x u + x v else 0) =
        (if H.Adj u v then x u else 0) +
          (if H.Adj u v then x v else 0) := by
    intro u v
    by_cases h : H.Adj u v <;> simp [h]
  simp_rw [hsplit, Finset.sum_add_distrib]
  rw [sum_adj_fst H x, sum_adj_snd H x]
  ring_nf

omit [DecidableEq V] in theorem weighted_degree_sum_of_degree_add
    (x : V → ℤ) (d : ℤ)
    (hdegree : ∀ v, (H.degree v : ℤ) + x v = d) :
    (∑ v : V, (H.degree v : ℤ) * x v) =
      d * (∑ v : V, x v) - ∑ v : V, (x v) ^ 2 := by
  calc
    (∑ v : V, (H.degree v : ℤ) * x v) =
        ∑ v : V, (d - x v) * x v := by
      apply Finset.sum_congr rfl
      intro v _
      have hv := hdegree v
      rw [show (H.degree v : ℤ) = d - x v by linarith]
    _ = d * (∑ v : V, x v) - ∑ v : V, (x v) ^ 2 := by
      simp_rw [sub_mul, pow_two, Finset.sum_sub_distrib]
      rw [← Finset.mul_sum]

/-- The half of the ordered off-diagonal sum.  For a symmetric pair statistic
this is exactly its sum over unordered pairs. -/
def unorderedPairTotal (f : V → V → ℤ) : ℤ :=
  (∑ uv ∈ (Finset.univ : Finset V).offDiag, f uv.1 uv.2) / 2

theorem sum_offDiag_pairDefect (x : V → ℤ) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag,
        pairDefect H x uv.1 uv.2) =
      2 * ((Fintype.card V : ℤ) - 1) * (∑ v : V, x v) +
        2 * (#H.edgeFinset : ℤ) := by
  simp_rw [pairDefect, Finset.sum_add_distrib]
  rw [sum_offDiag_fst x, sum_offDiag_snd x, sum_offDiag_adjBitInt H]
  ring_nf

/-- Generic first moment of the complement defect over unordered pairs. -/
theorem unorderedPairTotal_pairDefect (x : V → ℤ) :
    unorderedPairTotal (pairDefect H x) =
      ((Fintype.card V : ℤ) - 1) * (∑ v : V, x v) +
        (#H.edgeFinset : ℤ) := by
  rw [unorderedPairTotal, sum_offDiag_pairDefect H x]
  have hfactor :
      2 * ((Fintype.card V : ℤ) - 1) * (∑ v : V, x v) +
          2 * (#H.edgeFinset : ℤ) =
        2 * (((Fintype.card V : ℤ) - 1) * (∑ v : V, x v) +
          (#H.edgeFinset : ℤ)) := by ring_nf
  rw [hfactor]
  norm_num

theorem sum_offDiag_pairDefect_sq
    (x : V → ℤ) (d : ℤ)
    (hdegree : ∀ v, (H.degree v : ℤ) + x v = d) :
    (∑ uv ∈ (Finset.univ : Finset V).offDiag,
        (pairDefect H x uv.1 uv.2) ^ 2) =
      2 * ((Fintype.card V : ℤ) - 4) * (∑ v : V, (x v) ^ 2) +
        2 * (∑ v : V, x v) ^ 2 +
        4 * d * (∑ v : V, x v) + 2 * (#H.edgeFinset : ℤ) := by
  have hsquare : ∀ u v : V,
      (pairDefect H x u v) ^ 2 =
        (x u + x v) ^ 2 +
          2 * (if H.Adj u v then x u + x v else 0) +
          adjBitInt H u v := by
    intro u v
    by_cases h : H.Adj u v
    · simp only [pairDefect, adjBitInt, h, if_true]
      ring_nf
    · simp [pairDefect, adjBitInt, h]
  simp_rw [hsquare, Finset.sum_add_distrib]
  simp_rw [← Finset.mul_sum]
  rw [sum_offDiag_add_sq x, sum_offDiag_adj_endpoint H x,
    sum_offDiag_adjBitInt H, weighted_degree_sum_of_degree_add H x d hdegree]
  ring_nf

/-- Generic second moment of the complement defect over unordered pairs. -/
theorem unorderedPairTotal_pairDefect_sq
    (x : V → ℤ) (d : ℤ)
    (hdegree : ∀ v, (H.degree v : ℤ) + x v = d) :
    unorderedPairTotal (fun u v ↦ (pairDefect H x u v) ^ 2) =
      ((Fintype.card V : ℤ) - 4) * (∑ v : V, (x v) ^ 2) +
        (∑ v : V, x v) ^ 2 +
        2 * d * (∑ v : V, x v) + (#H.edgeFinset : ℤ) := by
  rw [unorderedPairTotal, sum_offDiag_pairDefect_sq H x d hdegree]
  have hfactor :
      2 * ((Fintype.card V : ℤ) - 4) * (∑ v : V, (x v) ^ 2) +
          2 * (∑ v : V, x v) ^ 2 +
          4 * d * (∑ v : V, x v) + 2 * (#H.edgeFinset : ℤ) =
        2 * (((Fintype.card V : ℤ) - 4) * (∑ v : V, (x v) ^ 2) +
          (∑ v : V, x v) ^ 2 + 2 * d * (∑ v : V, x v) +
          (#H.edgeFinset : ℤ)) := by ring_nf
  rw [hfactor]
  norm_num

end GraphPairSums

section PairDeletionDefect

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G H : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel H.Adj]

/-- Exact graph-level two-vertex deletion formula in the complement-defect
coordinates.  `H` need only be complementary to `G` on the selected pair;
no criticality, colouring, matching, or drawing hypothesis is imported. -/
theorem card_edges_delete_two_eq_sub_pairDefect
    (x : V → ℤ) (q : ℤ) {u v : V} (huv : u ≠ v)
    (hcompl : H.Adj u v ↔ ¬ G.Adj u v)
    (hdegree_u : (G.degree u : ℤ) = q + x u)
    (hdegree_v : (G.degree v : ℤ) = q + x v) :
    (#((G.deleteIncidenceSet u).deleteIncidenceSet v).edgeFinset : ℤ) =
      (#G.edgeFinset : ℤ) - (2 * q - 1) - pairDefect H x u v := by
  have hdeleteNat := card_edges_delete_two_add_degrees G huv
  have hdelete :
      (#((G.deleteIncidenceSet u).deleteIncidenceSet v).edgeFinset : ℤ) +
          (G.degree u : ℤ) + (G.degree v : ℤ) =
        (#G.edgeFinset : ℤ) + (adjBit G u v : ℤ) := by
    exact_mod_cast hdeleteNat
  have hbits : (adjBit G u v : ℤ) + adjBitInt H u v = 1 := by
    by_cases hG : G.Adj u v
    · have hH : ¬ H.Adj u v := by
        intro h
        exact (hcompl.mp h) hG
      simp [adjBit, adjBitInt, hG, hH]
    · have hH : H.Adj u v := hcompl.mpr hG
      simp [adjBit, adjBitInt, hG, hH]
  rw [hdegree_u, hdegree_v] at hdelete
  unfold pairDefect
  linarith

end PairDeletionDefect

section R28Specializations

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (H : SimpleGraph V) [DecidableRel H.Adj]

/-- First complement-defect moment on the surviving `(55,768)` row. -/
theorem r28_m768_pairDefect_sum
    (x : V → ℤ) (hcard : Fintype.card V = 55)
    (hedges : #H.edgeFinset = 717) (hsum : (∑ v : V, x v) = 51) :
    unorderedPairTotal (pairDefect H x) = 3471 := by
  rw [unorderedPairTotal_pairDefect H x, hcard, hedges, hsum]
  norm_num

/-- Second complement-defect moment on the surviving `(55,768)` row. -/
theorem r28_m768_pairDefect_sq_sum
    (x : V → ℤ) (hcard : Fintype.card V = 55)
    (hedges : #H.edgeFinset = 717) (hsum : (∑ v : V, x v) = 51)
    (hdegree : ∀ v, (H.degree v : ℤ) + x v = 27) :
    unorderedPairTotal (fun u v ↦ (pairDefect H x u v) ^ 2) =
      51 * (∑ v : V, (x v) ^ 2) + 6072 := by
  rw [unorderedPairTotal_pairDefect_sq H x 27 hdegree,
    hcard, hedges, hsum]
  ring_nf

/-- First complement-defect moment on the surviving `(55,769)` row. -/
theorem r28_m769_pairDefect_sum
    (x : V → ℤ) (hcard : Fintype.card V = 55)
    (hedges : #H.edgeFinset = 716) (hsum : (∑ v : V, x v) = 53) :
    unorderedPairTotal (pairDefect H x) = 3578 := by
  rw [unorderedPairTotal_pairDefect H x, hcard, hedges, hsum]
  norm_num

/-- Second complement-defect moment on the surviving `(55,769)` row. -/
theorem r28_m769_pairDefect_sq_sum
    (x : V → ℤ) (hcard : Fintype.card V = 55)
    (hedges : #H.edgeFinset = 716) (hsum : (∑ v : V, x v) = 53)
    (hdegree : ∀ v, (H.degree v : ℤ) + x v = 27) :
    unorderedPairTotal (fun u v ↦ (pairDefect H x u v) ^ 2) =
      51 * (∑ v : V, (x v) ^ 2) + 6387 := by
  rw [unorderedPairTotal_pairDefect_sq H x 27 hdegree,
    hcard, hedges, hsum]
  ring_nf

end R28Specializations

#print axioms AlbertsonPairMoments.card_edges_delete_two_add_degrees
#print axioms AlbertsonPairMoments.card_edges_delete_two_eq_sub_pairDefect
#print axioms AlbertsonPairMoments.unorderedPairTotal_pairDefect
#print axioms AlbertsonPairMoments.unorderedPairTotal_pairDefect_sq
#print axioms AlbertsonPairMoments.r28_m768_pairDefect_sum
#print axioms AlbertsonPairMoments.r28_m768_pairDefect_sq_sum
#print axioms AlbertsonPairMoments.r28_m769_pairDefect_sum
#print axioms AlbertsonPairMoments.r28_m769_pairDefect_sq_sum

end AlbertsonPairMoments
