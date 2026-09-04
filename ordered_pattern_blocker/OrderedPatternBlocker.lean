import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Powerset

/-!
# Finite blocker bounds for the `rm + 1` ordered-pattern boundary

This file isolates the two finite incidence arguments used in the independently
reviewed upper bound for ordered `r`-partite pattern cliques.  The formal layer
does not encode order types or pattern cliques: a family `copies : X → Finset E`
records the edge sets of the forbidden copies, and `D : Finset E` is a blocker.
-/

namespace OrderedPatternBlocker

variable {X E : Type*}

/-- `D` meets the edge set of every member of the indexed family `copies`. -/
def IsBlocker [DecidableEq E] (D : Finset E) (copies : X → Finset E) : Prop :=
  ∀ x, ∃ e ∈ D, e ∈ copies x

/-- The indices of copies which contain a fixed edge. -/
def copiesContaining [Fintype X] [DecidableEq E]
    (copies : X → Finset E) (e : E) : Finset X :=
  Finset.univ.filter fun x => e ∈ copies x

@[simp]
theorem mem_copiesContaining [Fintype X] [DecidableEq E]
    (copies : X → Finset E) (e : E) (x : X) :
    x ∈ copiesContaining copies e ↔ e ∈ copies x := by
  simp [copiesContaining]

/--
If every blocker edge occurs in at most `m` copies, counting copy--edge
incidences gives `|X| ≤ |D| * m`.
-/
theorem card_copies_le_card_blocker_mul [Fintype X] [DecidableEq E]
    (D : Finset E) (copies : X → Finset E) (m : ℕ)
    (hblocker : IsBlocker D copies)
    (hmultiplicity : ∀ e ∈ D, (copiesContaining copies e).card ≤ m) :
    Fintype.card X ≤ D.card * m := by
  classical
  have hcover : (Finset.univ : Finset X) ⊆
      D.biUnion (copiesContaining copies) := by
    intro x hx
    obtain ⟨e, heD, hecopy⟩ := hblocker x
    exact Finset.mem_biUnion.mpr ⟨e, heD, by simpa using hecopy⟩
  calc
    Fintype.card X = (Finset.univ : Finset X).card := by simp
    _ ≤ (D.biUnion (copiesContaining copies)).card :=
      Finset.card_le_card hcover
    _ ≤ D.card * m :=
      Finset.card_biUnion_le_card_mul D (copiesContaining copies) m hmultiplicity

/--
At the ordered-pattern boundary `|X| = r*m + 1`, multiplicity at most `m`
forces every blocker to have at least `r + 1` edges.
-/
theorem rm_add_one_le_card_blocker_of_bounded_multiplicity
    [Fintype X] [DecidableEq E]
    (D : Finset E) (copies : X → Finset E) (r m : ℕ)
    (hcard : Fintype.card X = r * m + 1)
    (hblocker : IsBlocker D copies)
    (hmultiplicity : ∀ e ∈ D, (copiesContaining copies e).card ≤ m) :
    r + 1 ≤ D.card := by
  have hincidence :=
    card_copies_le_card_blocker_mul D copies m hblocker hmultiplicity
  rw [hcard] at hincidence
  by_contra hnot
  have hsmall : D.card ≤ r := Nat.lt_succ_iff.mp (Nat.lt_of_not_ge hnot)
  have hmul : D.card * m ≤ r * m := Nat.mul_le_mul_right m hsmall
  exact Nat.not_succ_le_self (r * m) (hincidence.trans hmul)

/--
If the selected copy edge-sets are pairwise disjoint, choosing one blocker
edge from each copy embeds the copy-index type into `D`.
-/
theorem card_copies_le_card_blocker_of_pairwiseDisjoint
    [Fintype X] [DecidableEq E]
    (D : Finset E) (copies : X → Finset E)
    (hblocker : IsBlocker D copies)
    (hdisjoint : Pairwise fun x y => Disjoint (copies x) (copies y)) :
    Fintype.card X ≤ D.card := by
  classical
  choose edge hedgeD hedgeCopy using hblocker
  let selected : X → {e // e ∈ D} := fun x => ⟨edge x, hedgeD x⟩
  have hinjective : Function.Injective selected := by
    intro x y hxy
    by_contra hne
    have hedgeEq : edge x = edge y := congrArg Subtype.val hxy
    exact (Finset.disjoint_left.mp (hdisjoint hne)) (hedgeCopy x)
      (by simpa [hedgeEq] using hedgeCopy y)
  simpa [selected] using Fintype.card_le_of_injective selected hinjective

/-- The nonconstant-orientation endpoint for `r + 1` disjoint copies. -/
theorem rm_add_one_le_card_blocker_of_pairwiseDisjoint
    [DecidableEq E] (D : Finset E) (copies : Fin (r + 1) → Finset E)
    (hblocker : IsBlocker D copies)
    (hdisjoint : Pairwise fun x y => Disjoint (copies x) (copies y)) :
    r + 1 ≤ D.card := by
  simpa using
    card_copies_le_card_blocker_of_pairwiseDisjoint D copies hblocker hdisjoint

/-- All `r`-uniform edges on the ordered vertex set `Fin n`. -/
def uniformEdges (n r : ℕ) : Finset (Finset (Fin n)) :=
  (Finset.univ : Finset (Fin n)).powersetCard r

@[simp]
theorem card_uniformEdges (n r : ℕ) :
    (uniformEdges n r).card = Nat.choose n r := by
  simp [uniformEdges]

/-- Removing at least `r + 1` edges gives the desired extremal upper bound. -/
theorem card_present_le_choose_sub
    (present : Finset (Finset (Fin n))) (r : ℕ)
    (hpresent : present ⊆ uniformEdges n r)
    (hmissing : r + 1 ≤ (uniformEdges n r \ present).card) :
    present.card ≤ Nat.choose n r - (r + 1) := by
  have hpartition := Finset.card_sdiff_add_card_eq_card hpresent
  rw [card_uniformEdges] at hpartition
  apply Nat.le_sub_of_add_le
  calc
    present.card + (r + 1) ≤ present.card + (uniformEdges n r \ present).card :=
      Nat.add_le_add_left hmissing present.card
    _ = (uniformEdges n r \ present).card + present.card := Nat.add_comm _ _
    _ = Nat.choose n r := hpartition

/--
The all-forward upper-bound kernel: a blocker of all `r*m+1` canonical copies,
with occurrence multiplicity at most `m`, leaves at most
`choose (r*m+1) r - (r+1)` present edges.
-/
theorem boundary_upper_of_bounded_multiplicity
    [Fintype X]
    (present : Finset (Finset (Fin (r * m + 1))))
    (copies : X → Finset (Finset (Fin (r * m + 1))))
    (hpresent : present ⊆ uniformEdges (r * m + 1) r)
    (hcard : Fintype.card X = r * m + 1)
    (hblocker : IsBlocker (uniformEdges (r * m + 1) r \ present) copies)
    (hmultiplicity : ∀ e ∈ uniformEdges (r * m + 1) r \ present,
      (copiesContaining copies e).card ≤ m) :
    present.card ≤ Nat.choose (r * m + 1) r - (r + 1) := by
  apply card_present_le_choose_sub present r hpresent
  exact rm_add_one_le_card_blocker_of_bounded_multiplicity
    (uniformEdges (r * m + 1) r \ present) copies r m hcard hblocker hmultiplicity

/--
The nonconstant-orientation upper-bound kernel: `r+1` pairwise-disjoint
canonical copies force `r+1` missing edges.
-/
theorem boundary_upper_of_pairwiseDisjoint
    (present : Finset (Finset (Fin (r * m + 1))))
    (copies : Fin (r + 1) → Finset (Finset (Fin (r * m + 1))))
    (hpresent : present ⊆ uniformEdges (r * m + 1) r)
    (hblocker : IsBlocker (uniformEdges (r * m + 1) r \ present) copies)
    (hdisjoint : Pairwise fun x y => Disjoint (copies x) (copies y)) :
    present.card ≤ Nat.choose (r * m + 1) r - (r + 1) := by
  apply card_present_le_choose_sub present r hpresent
  exact rm_add_one_le_card_blocker_of_pairwiseDisjoint
    (uniformEdges (r * m + 1) r \ present) copies hblocker hdisjoint

#print axioms card_copies_le_card_blocker_mul
#print axioms rm_add_one_le_card_blocker_of_bounded_multiplicity
#print axioms card_copies_le_card_blocker_of_pairwiseDisjoint
#print axioms rm_add_one_le_card_blocker_of_pairwiseDisjoint
#print axioms card_uniformEdges
#print axioms card_present_le_choose_sub
#print axioms boundary_upper_of_bounded_multiplicity
#print axioms boundary_upper_of_pairwiseDisjoint

end OrderedPatternBlocker
