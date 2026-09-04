import ResidueSlabComposition
import Mathlib.Combinatorics.SimpleGraph.Prod

/-!
# The concrete Hamming lift of a finite-fiber line coloring

This file connects the finite-fiber interface in `ResidueSlabComposition` to
Mathlib's Cartesian (`boxProd`) graph product.  A coloring of a minor graph is
lifted constantly through a complete first coordinate.  Its same-color
neighborhood is the disjoint union of the other first-coordinate vertices and
the same-color neighborhood in the minor graph.
-/

open Function

namespace HammingLift

open SimpleGraph
open ResidueSlabComposition

universe u v

/-- Cartesian-product adjacency is decidable when both factor adjacencies and
both coordinate equalities are decidable. -/
instance instDecidableRelBoxProd
    {A B : Type*} [DecidableEq A] [DecidableEq B]
    (G : SimpleGraph A) (H : SimpleGraph B)
    [DecidableRel G.Adj] [DecidableRel H.Adj] :
    DecidableRel (G □ H).Adj := by
  intro x y
  change Decidable
    ((G.Adj x.1 y.1 ∧ x.2 = y.2) ∨ (H.Adj x.2 y.2 ∧ x.1 = y.1))
  infer_instance

/-- The neighbors of `x` receiving the same color as `x`. -/
def sameColorNeighborFinset {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq C] (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (x : V) : Finset V :=
  (G.neighborFinset x).filter fun y => color y = color x

@[simp]
theorem mem_sameColorNeighborFinset {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq C] (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (x y : V) :
    y ∈ sameColorNeighborFinset G color x ↔
      G.Adj x y ∧ color y = color x := by
  simp [sameColorNeighborFinset]

/-- The fiber of a color, as a finite set. -/
def fiberFinset {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq C] (color : V → C) (c : C) : Finset V :=
  Finset.univ.filter fun x => color x = c

@[simp]
theorem mem_fiberFinset {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq C] (color : V → C) (c : C) (x : V) :
    x ∈ fiberFinset color c ↔ color x = c := by
  simp [fiberFinset]

/-- Lift a coloring constantly through a new first coordinate. -/
def liftColor {I : Type*} {V : Type u} {C : Type v}
    (color : V → C) : I × V → C := fun x => color x.2

@[simp]
theorem liftColor_apply {I : Type*} {V : Type u} {C : Type v}
    (color : V → C) (i : I) (x : V) :
    liftColor color (i, x) = color x := rfl

/-- Exact decomposition of the same-color neighborhood in the Hamming lift. -/
theorem sameColorNeighborFinset_lift {I : Type*} {V : Type u} {C : Type v}
    [Fintype I] [DecidableEq I] [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (i : I) (x : V) :
    sameColorNeighborFinset (completeGraph I □ G) (liftColor color) (i, x) =
      ((Finset.univ.erase i).product ({x} : Finset V)) ∪
        (({i} : Finset I).product (sameColorNeighborFinset G color x)) := by
  ext y
  rcases y with ⟨j, y⟩
  simp only [mem_sameColorNeighborFinset, SimpleGraph.boxProd_adj,
    liftColor_apply, top_adj, Finset.mem_union]
  aesop

/-- Same-color degrees add under the concrete first-coordinate Hamming lift. -/
theorem card_sameColorNeighborFinset_lift
    {I : Type*} {V : Type u} {C : Type v}
    [Fintype I] [DecidableEq I] [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (i : I) (x : V) :
    (sameColorNeighborFinset (completeGraph I □ G)
        (liftColor color) (i, x)).card =
      (Fintype.card I - 1) + (sameColorNeighborFinset G color x).card := by
  rw [sameColorNeighborFinset_lift]
  rw [Finset.card_union_of_disjoint]
  · simp
  · rw [Finset.disjoint_left]
    intro y hyLeft hyRight
    rcases y with ⟨j, y⟩
    have hji : j ≠ i := (Finset.mem_erase.mp (Finset.mem_product.mp hyLeft).1).1
    have hji' : j = i := Finset.mem_singleton.mp (Finset.mem_product.mp hyRight).1
    exact hji hji'

/-- In a color fiber which is a clique, all other fiber points are same-color
neighbors. -/
theorem fiber_erase_subset_sameColorNeighbors
    {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (x : V)
    (hclique : ∀ y, color y = color x → y ≠ x → G.Adj x y) :
    (fiberFinset color (color x)).erase x ⊆
      sameColorNeighborFinset G color x := by
  intro y hy
  simp only [Finset.mem_erase, mem_fiberFinset] at hy
  exact mem_sameColorNeighborFinset G color x y |>.2
    ⟨hclique y hy.2 hy.1, hy.2⟩

/-- A fiber of size at least `s` which is a clique gives at least `s-1`
same-color neighbors in the minor graph. -/
theorem card_sameColorNeighbors_ge_fiber_sub_one
    {V : Type u} {C : Type v}
    [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (x : V)
    (hclique : ∀ y, color y = color x → y ≠ x → G.Adj x y) :
    (fiberFinset color (color x)).card - 1 ≤
      (sameColorNeighborFinset G color x).card := by
  have hmem : x ∈ fiberFinset color (color x) := by simp
  rw [← Finset.card_erase_of_mem hmem]
  exact Finset.card_le_card
    (fiber_erase_subset_sameColorNeighbors G color x hclique)

/-- The concrete Hamming lift bound: lifting a clique-fiber coloring through
the complete graph on `I` gives every lifted vertex at least
`|I|-1 + (s-1)` same-color neighbors. -/
theorem hammingLift_sameColorNeighbors_ge
    {I : Type*} {V : Type u} {C : Type v}
    [Fintype I] [DecidableEq I] [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (color : V → C) (s : ℕ)
    (hsize : ∀ c, s ≤ (fiberFinset color c).card)
    (hclique : ∀ c x y, color x = c → color y = c → x ≠ y → G.Adj x y)
    (i : I) (x : V) :
    (Fintype.card I - 1) + (s - 1) ≤
      (sameColorNeighborFinset (completeGraph I □ G)
        (liftColor color) (i, x)).card := by
  rw [card_sameColorNeighborFinset_lift]
  apply Nat.add_le_add_left _
  exact (Nat.sub_le_sub_right (hsize (color x)) 1).trans
    (card_sameColorNeighbors_ge_fiber_sub_one G color x
      (fun y hy hne => hclique (color x) x y rfl hy hne.symm))

/-- Distinct points are adjacent when they lie on one of the appended
coordinate lines.  When `baseLine` is the line relation of a Hamming box,
this is exactly its graph after appending one coordinate. -/
def appendedLineGraph {V : Type u} {p : ℕ}
    (baseLine : V → V → Prop) (hbaseSymm : Std.Symm baseLine) :
    SimpleGraph (V × Fin p) where
  Adj x y := x ≠ y ∧ AppendedLine baseLine x y
  symm.symm x y hxy := by
    refine ⟨hxy.1.symm, ?_⟩
    rcases hxy.2 with hfirst | hrest
    · exact Or.inl hfirst.symm
    · exact Or.inr ⟨hrest.1.symm, hbaseSymm.symm _ _ hrest.2⟩
  loopless.irrefl x hxx := by
    exact hxx.1 rfl

instance instDecidableRelAppendedLineGraph
    {V : Type u} {p : ℕ} [DecidableEq V]
    (baseLine : V → V → Prop) [DecidableRel baseLine]
    (hbaseSymm : Std.Symm baseLine) :
    DecidableRel (appendedLineGraph (p := p) baseLine hbaseSymm).Adj := by
  intro x y
  change Decidable
    (x ≠ y ∧ (x.1 = y.1 ∨ (x.2 = y.2 ∧ baseLine x.1 y.1)))
  infer_instance

/-- Reflexive closure of graph adjacency, i.e. containment in one complete
factor line when the graph is itself a Hamming product. -/
def sameOrAdjacent {V : Type u} (G : SimpleGraph V) (x y : V) : Prop :=
  x = y ∨ G.Adj x y

instance instDecidableRelSameOrAdjacent
    {V : Type u} [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] : DecidableRel (sameOrAdjacent G) := by
  intro x y
  change Decidable (x = y ∨ G.Adj x y)
  infer_instance

theorem sameOrAdjacent_symm {V : Type u} (G : SimpleGraph V) :
    Std.Symm (sameOrAdjacent G) where
  symm x y hxy := by
    rcases hxy with h | h
    · exact Or.inl h.symm
    · exact Or.inr h.symm

/-- Appending a coordinate-line graph is exactly Mathlib's Cartesian product
with a complete graph. -/
theorem appendedLineGraph_sameOrAdjacent_eq_boxProd
    {V : Type u} {p : ℕ} (G : SimpleGraph V) :
    appendedLineGraph (p := p) (sameOrAdjacent G)
      (sameOrAdjacent_symm G) = G □ completeGraph (Fin p) := by
  ext x y
  rcases x with ⟨x, i⟩
  rcases y with ⟨y, j⟩
  simp only [appendedLineGraph, AppendedLine, sameOrAdjacent,
    SimpleGraph.boxProd_adj, top_adj]
  aesop

/-- The existing residue-slab finite-fiber construction, followed by the
concrete Hamming lift.  Every lifted vertex has at least
`|I|-1 + (s-1)` same-color neighbors. -/
theorem residueSlab_hammingLift_sameColorNeighbors_ge
    {I : Type*} {V : Type u} {C : Type v}
    [Fintype I] [DecidableEq I]
    [Fintype V] [DecidableEq V] [DecidableEq C]
    (s p : ℕ) (hs : 0 < s) (color : V → C)
    (baseLine : V → V → Prop) [DecidableRel baseLine]
    (hbaseSymm : Std.Symm baseLine)
    (hbaseSize : ∀ c, s ≤ Fintype.card {x : V // color x = c})
    (hbaseLine : ∀ c x y,
      color x = c → color y = c → baseLine x y)
    (i : I) (x : V × Fin p) :
    (Fintype.card I - 1) + (s - 1) ≤
      (sameColorNeighborFinset
        (completeGraph I □ appendedLineGraph baseLine hbaseSymm)
        (liftColor (appendColor s p hs color)) (i, x)).card := by
  apply hammingLift_sameColorNeighbors_ge
  · intro d
    simpa [fiberFinset, ← Fintype.card_subtype] using
      appendColor_fiber_card_ge s p hs color hbaseSize d
  · intro d x y hx hy hne
    exact ⟨hne, appendColor_line s p hs color baseLine hbaseLine
      (hx.trans hy.symm)⟩

/-- Fully graph-native form of the construction.  Starting from clique fibers
in `G`, the residue-slab coloring of `G □ K_p`, lifted through `K_I`, has the
required same-color-neighbor bound in `K_I □ (G □ K_p)`. -/
theorem residueSlab_iteratedBoxProd_sameColorNeighbors_ge
    {I : Type*} {V : Type u} {C : Type v}
    [Fintype I] [DecidableEq I]
    [Fintype V] [DecidableEq V] [DecidableEq C]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (s p : ℕ) (hs : 0 < s) (color : V → C)
    (hbaseSize : ∀ c, s ≤ Fintype.card {x : V // color x = c})
    (hbaseClique : ∀ c x y,
      color x = c → color y = c → sameOrAdjacent G x y)
    (i : I) (x : V × Fin p) :
    (Fintype.card I - 1) + (s - 1) ≤
      (sameColorNeighborFinset
        (completeGraph I □ (G □ completeGraph (Fin p)))
        (liftColor (appendColor s p hs color)) (i, x)).card := by
  simpa only [appendedLineGraph_sameOrAdjacent_eq_boxProd] using
    (residueSlab_hammingLift_sameColorNeighbors_ge
      s p hs color (sameOrAdjacent G) (sameOrAdjacent_symm G)
      hbaseSize hbaseClique i x)

#print axioms sameColorNeighborFinset_lift
#print axioms card_sameColorNeighborFinset_lift
#print axioms fiber_erase_subset_sameColorNeighbors
#print axioms card_sameColorNeighbors_ge_fiber_sub_one
#print axioms hammingLift_sameColorNeighbors_ge
#print axioms appendedLineGraph
#print axioms appendedLineGraph_sameOrAdjacent_eq_boxProd
#print axioms residueSlab_hammingLift_sameColorNeighbors_ge
#print axioms residueSlab_iteratedBoxProd_sameColorNeighbors_ge

end HammingLift
