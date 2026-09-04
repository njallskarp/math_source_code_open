import Mathlib.Combinatorics.SimpleGraph.AdjMatrix
import Mathlib.Combinatorics.SimpleGraph.IncMatrix
import Mathlib.Combinatorics.SimpleGraph.LineGraph
import Mathlib.Algebra.Polynomial.RingDivision
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff

open Matrix

namespace LineGraphIncidence

open SimpleGraph

variable {V : Type*} [DecidableEq V]

/-- The usual vertex-by-edge unsigned incidence matrix, obtained by restricting
Mathlib's all-unordered-pairs incidence matrix to the actual edge subtype. -/
def edgeIncMatrix (R : Type*) [Zero R] [One R]
    (G : SimpleGraph V) [DecidableRel G.Adj] : Matrix V G.edgeSet R :=
  (G.incMatrix R).submatrix id (fun e => e.1)

/-- An entry of the incidence Gram matrix counts common endpoints. -/
theorem edgeIncMatrix_transpose_mul_apply_eq_card_inter
    {R : Type*} [Semiring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (e f : G.edgeSet) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G) e f =
      ((e.1.toFinset ∩ f.1.toFinset).card : R) := by
  classical
  simp [edgeIncMatrix, Matrix.mul_apply, SimpleGraph.incMatrix_apply',
    SimpleGraph.edge_mem_incidenceSet_iff, ← Sym2.mem_toFinset, Finset.inter_comm]

/-- Actual edges are determined by their two-element endpoint finsets. -/
theorem edge_toFinset_injective (G : SimpleGraph V) :
    Function.Injective (fun e : G.edgeSet => e.1.toFinset) := by
  intro e f hef
  apply Subtype.ext
  apply Sym2.ext
  intro x
  simpa only [Sym2.mem_toFinset] using Finset.ext_iff.mp hef x

/-- Two distinct two-element finsets with a common member intersect in one element. -/
theorem card_inter_eq_one_of_card_two
    {s t : Finset V} (hs : s.card = 2) (ht : t.card = 2)
    (hne : s ≠ t) (hnonempty : (s ∩ t).Nonempty) :
    (s ∩ t).card = 1 := by
  have hpos : 0 < (s ∩ t).card := Finset.card_pos.mpr hnonempty
  have hle : (s ∩ t).card ≤ 2 := by
    calc
      (s ∩ t).card ≤ s.card := Finset.card_le_card Finset.inter_subset_left
      _ = 2 := hs
  have hneTwo : (s ∩ t).card ≠ 2 := by
    intro htwo
    have his : s ∩ t = s :=
      Finset.eq_of_subset_of_card_le Finset.inter_subset_left (by omega)
    have hit : s ∩ t = t :=
      Finset.eq_of_subset_of_card_le Finset.inter_subset_right (by omega)
    exact hne (his.symm.trans hit)
  omega

/-- Every edge of a simple graph has exactly two distinct endpoints. -/
theorem edge_toFinset_card (G : SimpleGraph V) (e : G.edgeSet) :
    e.1.toFinset.card = 2 :=
  Sym2.card_toFinset_of_not_isDiag e.1 (G.not_isDiag_of_mem_edgeSet e.2)

/-- Adjacent line-graph vertices, being distinct graph edges, share exactly one endpoint. -/
theorem edge_inter_card_of_lineGraph_adj
    (G : SimpleGraph V) (e f : G.edgeSet) (h : G.lineGraph.Adj e f) :
    (e.1.toFinset ∩ f.1.toFinset).card = 1 := by
  rw [SimpleGraph.lineGraph_adj_iff_exists] at h
  obtain ⟨hef, v, hve, hvf⟩ := h
  apply card_inter_eq_one_of_card_two (edge_toFinset_card G e) (edge_toFinset_card G f)
  · exact fun hfin => hef (edge_toFinset_injective G hfin)
  · exact ⟨v, Finset.mem_inter.mpr
      ⟨Sym2.mem_toFinset.mpr hve, Sym2.mem_toFinset.mpr hvf⟩⟩

/-- Distinct nonadjacent line-graph vertices have disjoint endpoint finsets. -/
theorem edge_inter_card_of_not_lineGraph_adj
    (G : SimpleGraph V) (e f : G.edgeSet) (hef : e ≠ f)
    (h : ¬G.lineGraph.Adj e f) :
    (e.1.toFinset ∩ f.1.toFinset).card = 0 := by
  rw [Finset.card_eq_zero]
  rw [Finset.eq_empty_iff_forall_notMem]
  intro v hv
  have hve : v ∈ (e : Sym2 V) := Sym2.mem_toFinset.mp (Finset.mem_inter.mp hv).1
  have hvf : v ∈ (f : Sym2 V) := Sym2.mem_toFinset.mp (Finset.mem_inter.mp hv).2
  exact h (SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hef, v, hve, hvf⟩)

theorem edgeIncMatrix_transpose_mul_apply_of_adj
    {R : Type*} [Semiring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (e f : G.edgeSet)
    (h : G.lineGraph.Adj e f) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G) e f = 1 := by
  rw [edgeIncMatrix_transpose_mul_apply_eq_card_inter, edge_inter_card_of_lineGraph_adj G e f h]
  norm_num

theorem edgeIncMatrix_transpose_mul_apply_of_not_adj
    {R : Type*} [Semiring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (e f : G.edgeSet)
    (hef : e ≠ f) (h : ¬G.lineGraph.Adj e f) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G) e f = 0 := by
  rw [edgeIncMatrix_transpose_mul_apply_eq_card_inter,
    edge_inter_card_of_not_lineGraph_adj G e f hef h]
  norm_num

theorem edgeIncMatrix_transpose_mul_apply_diag
    {R : Type*} [Semiring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (e : G.edgeSet) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G) e e = 2 := by
  rw [edgeIncMatrix_transpose_mul_apply_eq_card_inter, Finset.inter_self,
    edge_toFinset_card G e]
  norm_num

/-- Over every semiring, the edge-incidence Gram matrix is the adjacency
matrix of the Mathlib line graph plus twice the identity. -/
theorem edgeIncMatrix_transpose_mul
    {R : Type*} [Semiring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel G.lineGraph.Adj] :
    (edgeIncMatrix R G)ᵀ * edgeIncMatrix R G =
      G.lineGraph.adjMatrix R + (2 : R) • (1 : Matrix G.edgeSet G.edgeSet R) := by
  ext e f
  by_cases hef : e = f
  · subst f
    simp [edgeIncMatrix_transpose_mul_apply_diag]
  · by_cases hAdj : G.lineGraph.Adj e f
    · simp [hAdj, edgeIncMatrix_transpose_mul_apply_of_adj G e f hAdj, hef]
    · simp [hAdj, edgeIncMatrix_transpose_mul_apply_of_not_adj G e f hef hAdj, hef]

/-- Ring-valued form used in spectral line-graph arguments:
`A(L(G)) = Bᵀ B - 2I`. -/
theorem lineGraph_adjMatrix_eq_transpose_mul_sub
    {R : Type*} [Ring R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj] [DecidableRel G.lineGraph.Adj] :
    G.lineGraph.adjMatrix R =
      (edgeIncMatrix R G)ᵀ * edgeIncMatrix R G -
        (2 : R) • (1 : Matrix G.edgeSet G.edgeSet R) := by
  rw [edgeIncMatrix_transpose_mul]
  exact (add_sub_cancel_right _ _).symm

/-- If the graph has at least as many edges as vertices, the characteristic
polynomial of the edge Gram matrix is the characteristic polynomial of the
vertex co-Gram matrix with exactly the dimension-difference power of `X`.

This is the rectangular `AB`/`BA` characteristic-polynomial identity applied
to the unsigned incidence matrix. -/
theorem edgeGram_charpoly_eq_X_pow_mul_coGram
    {R : Type*} [CommRing R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hcard : Fintype.card V ≤ Fintype.card G.edgeSet) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G).charpoly =
      Polynomial.X ^ (Fintype.card G.edgeSet - Fintype.card V) *
        (edgeIncMatrix R G * (edgeIncMatrix R G)ᵀ).charpoly :=
  Matrix.charpoly_mul_comm_of_le (edgeIncMatrix R G)ᵀ (edgeIncMatrix R G) hcard

/-- In the cyclomatic-three cardinality regime `|E| = |V| + 2`, the edge
Gram characteristic polynomial has exactly the explicit surplus factor `X²`. -/
theorem edgeGram_charpoly_eq_X_sq_mul_coGram
    {R : Type*} [CommRing R] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hcard : Fintype.card G.edgeSet = Fintype.card V + 2) :
    ((edgeIncMatrix R G)ᵀ * edgeIncMatrix R G).charpoly =
      Polynomial.X ^ 2 * (edgeIncMatrix R G * (edgeIncMatrix R G)ᵀ).charpoly := by
  rw [edgeGram_charpoly_eq_X_pow_mul_coGram G (by omega),
    show Fintype.card G.edgeSet - Fintype.card V = 2 by omega]

/-- Away from zero, the edge Gram and vertex co-Gram matrices have identical
algebraic root multiplicities. -/
theorem edgeGram_rootMultiplicity_eq_coGram_of_ne_zero
    {K : Type*} [Field K] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hcard : Fintype.card V ≤ Fintype.card G.edgeSet)
    {μ : K} (hμ : μ ≠ 0) :
    ((edgeIncMatrix K G)ᵀ * edgeIncMatrix K G).charpoly.rootMultiplicity μ =
      (edgeIncMatrix K G * (edgeIncMatrix K G)ᵀ).charpoly.rootMultiplicity μ := by
  rw [edgeGram_charpoly_eq_X_pow_mul_coGram G hcard,
    Polynomial.rootMultiplicity_mul]
  · simp [Polynomial.rootMultiplicity_eq_zero, Polynomial.IsRoot, hμ]
  · exact mul_ne_zero (pow_ne_zero _ Polynomial.X_ne_zero)
      (Matrix.charpoly_monic _).ne_zero

/-- The zero-root algebraic multiplicity of the edge Gram matrix is the
zero-root multiplicity of the vertex co-Gram matrix plus the index-cardinality
difference. -/
theorem edgeGram_rootMultiplicity_zero_eq_card_sub_add_coGram
    {K : Type*} [Field K] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hcard : Fintype.card V ≤ Fintype.card G.edgeSet) :
    ((edgeIncMatrix K G)ᵀ * edgeIncMatrix K G).charpoly.rootMultiplicity 0 =
      (Fintype.card G.edgeSet - Fintype.card V) +
        (edgeIncMatrix K G * (edgeIncMatrix K G)ᵀ).charpoly.rootMultiplicity 0 := by
  rw [edgeGram_charpoly_eq_X_pow_mul_coGram G hcard,
    Polynomial.rootMultiplicity_mul]
  · rw [show (Polynomial.X : Polynomial K) ^
          (Fintype.card G.edgeSet - Fintype.card V) =
        (Polynomial.X - Polynomial.C 0) ^
          (Fintype.card G.edgeSet - Fintype.card V) by simp,
      Polynomial.rootMultiplicity_X_sub_C_pow]
  · exact mul_ne_zero (pow_ne_zero _ Polynomial.X_ne_zero)
      (Matrix.charpoly_monic _).ne_zero

/-- In the cyclomatic-three cardinality regime, the edge Gram matrix has two
more zero roots (with algebraic multiplicity) than the vertex co-Gram matrix. -/
theorem edgeGram_rootMultiplicity_zero_eq_two_add_coGram
    {K : Type*} [Field K] [Fintype V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hcard : Fintype.card G.edgeSet = Fintype.card V + 2) :
    ((edgeIncMatrix K G)ᵀ * edgeIncMatrix K G).charpoly.rootMultiplicity 0 =
      2 + (edgeIncMatrix K G * (edgeIncMatrix K G)ᵀ).charpoly.rootMultiplicity 0 := by
  rw [edgeGram_rootMultiplicity_zero_eq_card_sub_add_coGram G (by omega),
    show Fintype.card G.edgeSet - Fintype.card V = 2 by omega]

#print axioms edgeIncMatrix_transpose_mul_apply_eq_card_inter
#print axioms edge_toFinset_injective
#print axioms card_inter_eq_one_of_card_two
#print axioms edge_toFinset_card
#print axioms edge_inter_card_of_lineGraph_adj
#print axioms edge_inter_card_of_not_lineGraph_adj
#print axioms edgeIncMatrix_transpose_mul
#print axioms lineGraph_adjMatrix_eq_transpose_mul_sub
#print axioms edgeGram_charpoly_eq_X_pow_mul_coGram
#print axioms edgeGram_charpoly_eq_X_sq_mul_coGram
#print axioms edgeGram_rootMultiplicity_eq_coGram_of_ne_zero
#print axioms edgeGram_rootMultiplicity_zero_eq_card_sub_add_coGram
#print axioms edgeGram_rootMultiplicity_zero_eq_two_add_coGram

end LineGraphIncidence
