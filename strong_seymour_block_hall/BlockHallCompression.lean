import Mathlib.Combinatorics.Hall.Basic

/-!
# Hall compression for complete-or-empty block relations

This file proves that, for a finite bipartite relation which is constant on
pairs of quotient blocks, Hall's condition need only be checked on unions of
whole source blocks. It also proves the dual quotient-cut formulation and
connects both compressed conditions to an actual injective matching through
Mathlib's finite Hall theorem.
-/

namespace BlockHallCompression

open Function

set_option linter.unusedSectionVars false

universe uA uB uI uJ

variable {A : Type uA} {B : Type uB} {I : Type uI} {J : Type uJ}
variable [Fintype A] [Fintype B] [Fintype I] [Fintype J]
variable [DecidableEq A] [DecidableEq B] [DecidableEq I] [DecidableEq J]

/-- The union of the source blocks indexed by U. -/
def blockPreimage (block : A → I) (U : Finset I) : Finset A :=
  Finset.univ.filter fun a => block a ∈ U

/-- Quotient target blocks adjacent from at least one block in U. -/
def blockNeighbors (Q : I → J → Prop) [DecidableRel Q]
    (U : Finset I) : Finset J :=
  Finset.univ.filter fun j => ∃ i ∈ U, Q i j

/-- Vertex targets adjacent from at least one vertex in S, for the relation
obtained by expanding every quotient pair to a complete or empty block. -/
def vertexNeighbors (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] (S : Finset A) : Finset B :=
  Finset.univ.filter fun b => ∃ a ∈ S, Q (leftBlock a) (rightBlock b)

/-- Ordinary vertex-level Hall condition for the expanded block relation. -/
def VertexHall (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] : Prop :=
  ∀ S : Finset A,
    S.card ≤ (vertexNeighbors leftBlock rightBlock Q S).card

/-- Hall inequalities compressed to unions of whole source blocks. -/
def BlockHall (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] : Prop :=
  ∀ U : Finset I,
    (blockPreimage leftBlock U).card ≤
      (blockPreimage rightBlock (blockNeighbors Q U)).card

/-- Source blocks all of whose quotient neighbors lie in the target-block cut
V. -/
def cutSources (Q : I → J → Prop) [DecidableRel Q]
    (V : Finset J) : Finset I :=
  Finset.univ.filter fun i => ∀ j, Q i j → j ∈ V

/-- The target-cut form of the compressed Hall inequalities. -/
def CutHall (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] : Prop :=
  ∀ V : Finset J,
    (blockPreimage leftBlock (cutSources Q V)).card ≤
      (blockPreimage rightBlock V).card

@[simp] theorem mem_blockPreimage (block : A → I) (U : Finset I) (a : A) :
    a ∈ blockPreimage block U ↔ block a ∈ U := by
  simp [blockPreimage]

@[simp] theorem mem_blockNeighbors (Q : I → J → Prop) [DecidableRel Q]
    (U : Finset I) (j : J) :
    j ∈ blockNeighbors Q U ↔ ∃ i ∈ U, Q i j := by
  simp [blockNeighbors]

@[simp] theorem mem_vertexNeighbors (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] (S : Finset A) (b : B) :
    b ∈ vertexNeighbors leftBlock rightBlock Q S ↔
      ∃ a ∈ S, Q (leftBlock a) (rightBlock b) := by
  simp [vertexNeighbors]

@[simp] theorem mem_cutSources (Q : I → J → Prop) [DecidableRel Q]
    (V : Finset J) (i : I) :
    i ∈ cutSources Q V ↔ ∀ j, Q i j → j ∈ V := by
  simp [cutSources]

/-- The vertex neighbors of S are exactly the full target blocks adjacent
from the quotient blocks met by S. -/
theorem vertexNeighbors_eq_blockPreimage_image
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] (S : Finset A) :
    vertexNeighbors leftBlock rightBlock Q S =
      blockPreimage rightBlock (blockNeighbors Q (S.image leftBlock)) := by
  ext b
  simp

/-- A set of source vertices is contained in the union of the blocks it meets. -/
theorem subset_blockPreimage_image (leftBlock : A → I) (S : Finset A) :
    S ⊆ blockPreimage leftBlock (S.image leftBlock) := by
  intro a ha
  exact (mem_blockPreimage leftBlock _ a).2
    (Finset.mem_image.2 ⟨a, ha, rfl⟩)

/-- Neighbors of a union of source blocks lie in the corresponding union of
target blocks. This inclusion does not require quotient blocks to be nonempty. -/
theorem vertexNeighbors_blockPreimage_subset
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] (U : Finset I) :
    vertexNeighbors leftBlock rightBlock Q (blockPreimage leftBlock U) ⊆
      blockPreimage rightBlock (blockNeighbors Q U) := by
  intro b hb
  obtain ⟨a, ha, hab⟩ := (mem_vertexNeighbors _ _ _ _ _).1 hb
  exact (mem_blockPreimage _ _ _).2
    ((mem_blockNeighbors Q U _).2
      ⟨leftBlock a, (mem_blockPreimage _ _ _).1 ha, hab⟩)

/-- If every quotient source block is nonempty, the neighbors of a union of
whole source blocks are exactly the corresponding union of target blocks. -/
theorem vertexNeighbors_blockPreimage
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q]
    (hleft : Surjective leftBlock) (U : Finset I) :
    vertexNeighbors leftBlock rightBlock Q (blockPreimage leftBlock U) =
      blockPreimage rightBlock (blockNeighbors Q U) := by
  ext b
  simp only [mem_vertexNeighbors, mem_blockPreimage, mem_blockNeighbors]
  constructor
  · rintro ⟨a, ha, hab⟩
    exact ⟨leftBlock a, ha, hab⟩
  · rintro ⟨i, hi, hib⟩
    obtain ⟨a, rfl⟩ := hleft i
    exact ⟨a, hi, hib⟩

/-- Ordinary Hall inequalities are equivalent to the quotient inequalities
checked only on unions of whole blocks. Empty source blocks merely make some
quotient inequalities redundant, so no nonemptiness hypothesis is needed. -/
theorem vertexHall_iff_blockHall
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] :
    VertexHall leftBlock rightBlock Q ↔
      BlockHall leftBlock rightBlock Q := by
  constructor
  · intro hVertex U
    calc
      (blockPreimage leftBlock U).card
          ≤ (vertexNeighbors leftBlock rightBlock Q
              (blockPreimage leftBlock U)).card := hVertex _
      _ ≤ (blockPreimage rightBlock (blockNeighbors Q U)).card :=
        Finset.card_le_card
          (vertexNeighbors_blockPreimage_subset leftBlock rightBlock Q U)
  · intro hBlock S
    calc
      S.card ≤ (blockPreimage leftBlock (S.image leftBlock)).card :=
        Finset.card_le_card (subset_blockPreimage_image leftBlock S)
      _ ≤ (blockPreimage rightBlock
          (blockNeighbors Q (S.image leftBlock))).card := hBlock _
      _ = (vertexNeighbors leftBlock rightBlock Q S).card := by
        rw [vertexNeighbors_eq_blockPreimage_image]

/-- A quotient set is contained in the cut closure of its neighborhood. -/
theorem subset_cutSources_blockNeighbors
    (Q : I → J → Prop) [DecidableRel Q] (U : Finset I) :
    U ⊆ cutSources Q (blockNeighbors Q U) := by
  intro i hi
  simp only [mem_cutSources]
  intro j hij
  exact (mem_blockNeighbors Q U j).2 ⟨i, hi, hij⟩

/-- The quotient neighborhood of the cut closure of U is its original
quotient neighborhood. -/
theorem blockNeighbors_cutSources_blockNeighbors
    (Q : I → J → Prop) [DecidableRel Q] (U : Finset I) :
    blockNeighbors Q (cutSources Q (blockNeighbors Q U)) =
      blockNeighbors Q U := by
  apply Finset.Subset.antisymm
  · intro j hj
    obtain ⟨i, hi, hij⟩ := (mem_blockNeighbors Q _ j).1 hj
    exact (mem_cutSources Q _ i).1 hi j hij
  · intro j hj
    obtain ⟨i, hi, hij⟩ := (mem_blockNeighbors Q U j).1 hj
    exact (mem_blockNeighbors Q _ j).2
      ⟨i, subset_cutSources_blockNeighbors Q U hi, hij⟩

/-- Quotient Hall inequalities have an equivalent two-sided target-cut form. -/
theorem blockHall_iff_cutHall
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] :
    BlockHall leftBlock rightBlock Q ↔
      CutHall leftBlock rightBlock Q := by
  constructor
  · intro hBlock V
    calc
      (blockPreimage leftBlock (cutSources Q V)).card
          ≤ (blockPreimage rightBlock
              (blockNeighbors Q (cutSources Q V))).card := hBlock _
      _ ≤ (blockPreimage rightBlock V).card := by
        apply Finset.card_le_card
        intro b hb
        simp only [mem_blockPreimage] at hb ⊢
        obtain ⟨i, hi, hib⟩ := (mem_blockNeighbors Q _ _).1 hb
        exact (mem_cutSources Q V i).1 hi (rightBlock b) hib
  · intro hCut U
    calc
      (blockPreimage leftBlock U).card
          ≤ (blockPreimage leftBlock
              (cutSources Q (blockNeighbors Q U))).card := by
        exact Finset.card_le_card (fun a ha =>
          (mem_blockPreimage _ _ _).2
            (subset_cutSources_blockNeighbors Q U
              ((mem_blockPreimage _ _ _).1 ha)))
      _ ≤ (blockPreimage rightBlock (blockNeighbors Q U)).card := hCut _

/-- The quotient block inequalities are equivalent to the existence of an
injective matching in the expanded complete-or-empty block relation. -/
theorem blockHall_iff_exists_injective
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] :
    BlockHall leftBlock rightBlock Q ↔
      ∃ f : A → B, Injective f ∧
        ∀ a, Q (leftBlock a) (rightBlock (f a)) := by
  rw [← vertexHall_iff_blockHall leftBlock rightBlock Q]
  exact Fintype.all_card_le_filter_rel_iff_exists_injective
    (fun a b => Q (leftBlock a) (rightBlock b))

/-- The quotient target-cut inequalities are likewise equivalent to an actual
injective matching. -/
theorem cutHall_iff_exists_injective
    (leftBlock : A → I) (rightBlock : B → J)
    (Q : I → J → Prop) [DecidableRel Q] :
    CutHall leftBlock rightBlock Q ↔
      ∃ f : A → B, Injective f ∧
        ∀ a, Q (leftBlock a) (rightBlock (f a)) := by
  rw [← blockHall_iff_cutHall leftBlock rightBlock Q]
  exact blockHall_iff_exists_injective leftBlock rightBlock Q

#print axioms vertexNeighbors_eq_blockPreimage_image
#print axioms vertexNeighbors_blockPreimage_subset
#print axioms vertexNeighbors_blockPreimage
#print axioms vertexHall_iff_blockHall
#print axioms subset_cutSources_blockNeighbors
#print axioms blockNeighbors_cutSources_blockNeighbors
#print axioms blockHall_iff_cutHall
#print axioms blockHall_iff_exists_injective
#print axioms cutHall_iff_exists_injective

end BlockHallCompression
