import Mathlib.Combinatorics.SimpleGraph.Prod

/-!
# Finite locating-dominating codes and Cartesian products

This file gives a finite-graph definition of a locating-dominating code and
proves the reusable product lemma used to lift codes in binary Hamming cubes.
-/

open Finset

namespace SimpleGraph

variable {V W : Type*}

/-- Decidable adjacency for the Cartesian product of two decidable graphs. -/
instance instDecidableRelBoxProdAdj (G : SimpleGraph V) (H : SimpleGraph W)
    [DecidableEq V] [DecidableEq W] [DecidableRel G.Adj] [DecidableRel H.Adj] :
    DecidableRel (G □ H).Adj :=
  fun x y ↦ inferInstanceAs <|
    Decidable (G.Adj x.1 y.1 ∧ x.2 = y.2 ∨ H.Adj x.2 y.2 ∧ x.1 = y.1)

section Finite

variable [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]

/-- The closed neighborhood of a vertex, as a finite set. -/
def closedNeighborFinset (v : V) : Finset V :=
  insert v (G.neighborFinset v)

/-- The signature seen by the code `C` at `v`. -/
def locatingSignature (C : Finset V) (v : V) : Finset V :=
  G.closedNeighborFinset v ∩ C

/-- A finite code is locating-dominating when every vertex has a nonempty
closed-neighborhood signature and distinct non-codewords have distinct
signatures. -/
def IsLocatingDominating (C : Finset V) : Prop :=
  (∀ v, (G.locatingSignature C v).Nonempty) ∧
    ∀ ⦃u v⦄, u ∉ C → v ∉ C →
      G.locatingSignature C u = G.locatingSignature C v → u = v

/-- A locating-dominating code of minimum cardinality. -/
def IsMinimumLocatingDominating (C : Finset V) : Prop :=
  G.IsLocatingDominating C ∧
    ∀ D : Finset V, G.IsLocatingDominating D → C.card ≤ D.card

end Finite

section Product

variable [Fintype V] [DecidableEq V] [Fintype W] [DecidableEq W]
variable (G : SimpleGraph V) [DecidableRel G.Adj]
variable (H : SimpleGraph W) [DecidableRel H.Adj]

/-- Away from `C × univ`, the signature in a Cartesian graph product is
exactly the old signature in the first coordinate, at the fixed second
coordinate. -/
theorem locatingSignature_boxProd_product_univ (C : Finset V) (x : V × W)
    (hx : x.1 ∉ C) :
    (G □ H).locatingSignature (C ×ˢ (univ : Finset W)) x =
      G.locatingSignature C x.1 ×ˢ {x.2} := by
  ext y
  simp only [locatingSignature, closedNeighborFinset, mem_inter, mem_insert,
    mem_neighborFinset, Finset.mem_product, mem_univ, and_true, boxProd_adj,
    mem_singleton]
  constructor
  · rintro ⟨hclose, hyC⟩
    rcases hclose with hxy | hleft | hright
    · subst y
      exact (hx hyC).elim
    · exact ⟨⟨Or.inr hleft.1, hyC⟩, hleft.2.symm⟩
    · exact (hx (hright.2.symm ▸ hyC)).elim
  · rintro ⟨⟨hclose, hyC⟩, hyx⟩
    refine ⟨?_, hyC⟩
    rcases hclose with hself | hAdj
    · exact (hx (hself.symm ▸ hyC)).elim
    · exact Or.inr (Or.inl ⟨hAdj, hyx.symm⟩)

/-- Taking the Cartesian product of a locating-dominating code with the full
vertex set of any finite graph preserves the locating-dominating property. -/
theorem IsLocatingDominating.boxProd_univ {C : Finset V}
    (hC : G.IsLocatingDominating C) :
    (G □ H).IsLocatingDominating (C ×ˢ (univ : Finset W)) := by
  constructor
  · intro x
    by_cases hx : x.1 ∈ C
    · refine ⟨x, ?_⟩
      simp [locatingSignature, closedNeighborFinset, hx]
    · rw [locatingSignature_boxProd_product_univ G H C x hx]
      obtain ⟨c, hc⟩ := hC.1 x.1
      exact ⟨(c, x.2), by simpa using hc⟩
  · intro x y hx hy hsig
    have hxC : x.1 ∉ C := by simpa using hx
    have hyC : y.1 ∉ C := by simpa using hy
    have hsx := hC.1 x.1
    obtain ⟨c, hc⟩ := hsx
    have hxy2 : x.2 = y.2 := by
      have hm : (c, x.2) ∈ G.locatingSignature C y.1 ×ˢ {y.2} := by
        rw [← locatingSignature_boxProd_product_univ G H C y hyC, ← hsig,
          locatingSignature_boxProd_product_univ G H C x hxC]
        simpa using hc
      exact Finset.mem_singleton.mp (Finset.mem_product.mp hm).2
    have hbase : G.locatingSignature C x.1 = G.locatingSignature C y.1 := by
      ext z
      constructor
      · intro hz
        have hm : (z, x.2) ∈ G.locatingSignature C y.1 ×ˢ {y.2} := by
          rw [← locatingSignature_boxProd_product_univ G H C y hyC, ← hsig,
            locatingSignature_boxProd_product_univ G H C x hxC]
          simpa using hz
        exact (Finset.mem_product.mp hm).1
      · intro hz
        have hm : (z, y.2) ∈ G.locatingSignature C x.1 ×ˢ {x.2} := by
          rw [← locatingSignature_boxProd_product_univ G H C x hxC, hsig,
            locatingSignature_boxProd_product_univ G H C y hyC]
          simpa using hz
        exact (Finset.mem_product.mp hm).1
    have hxy1 : x.1 = y.1 := hC.2 hxC hyC hbase
    exact Prod.ext hxy1 hxy2

end Product

end SimpleGraph

#print axioms SimpleGraph.locatingSignature_boxProd_product_univ
#print axioms SimpleGraph.IsLocatingDominating.boxProd_univ
