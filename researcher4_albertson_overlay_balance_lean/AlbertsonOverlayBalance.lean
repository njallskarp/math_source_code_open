import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Data.Set.Card
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.SplitIfs

/-!
# Optimal-coloring balance on common unions of color classes

The finite-palette replacement argument underlying endpoint-factor overlays.
No criticality, deletion-factor existence, multigraph, or routing is assumed.
-/

open Set SimpleGraph

namespace AlbertsonOverlayBalance

variable {V A B : Type*} {G : SimpleGraph V}

/-- Membership in `S` is constant on every fiber of the coloring. -/
def Saturated (C : G.Coloring A) (S : Set V) : Prop :=
  ∀ ⦃v w⦄, C v = C w → (v ∈ S ↔ w ∈ S)

/-- Saturation says exactly that `S` is a union of whole color classes. -/
theorem saturated_iff_preimage_image (C : G.Coloring A) (S : Set V) :
    Saturated C S ↔ C ⁻¹' (C '' S) = S := by
  constructor
  · intro h
    ext v
    constructor
    · rintro ⟨w, hw, heq⟩
      exact (h heq).mp hw
    · intro hv
      exact ⟨v, hv, rfl⟩
  · intro h v w heq
    have hvw : v ∈ C ⁻¹' (C '' S) ↔ w ∈ C ⁻¹' (C '' S) := by
      simp only [Set.mem_preimage, heq]
    simpa only [h] using hvw

/-- Splice `D` inside `S` with `C` outside, using disjoint tagged palettes.
This is a proper coloring without any saturation hypothesis. -/
noncomputable def spliceColoring (C : G.Coloring A) (D : G.Coloring B) (S : Set V) :
    G.Coloring ((D '' S) ⊕ (C '' Sᶜ)) := by
  classical
  refine Coloring.mk
    (fun v => if h : v ∈ S then Sum.inl ⟨D v, v, h, rfl⟩
      else Sum.inr ⟨C v, v, h, rfl⟩) ?_
  intro v w hadj heq
  split_ifs at heq
  · exact D.valid hadj (congrArg Subtype.val (Sum.inl.inj heq))
  · exact C.valid hadj (congrArg Subtype.val (Sum.inr.inj heq))

theorem colorable_splice [Finite A] [Finite B]
    (C : G.Coloring A) (D : G.Coloring B) (S : Set V) :
    G.Colorable ((D '' S).ncard + (C '' Sᶜ).ncard) := by
  classical
  let := Fintype.ofFinite (D '' S)
  let := Fintype.ofFinite (C '' Sᶜ)
  simpa only [← Nat.card_eq_fintype_card, Nat.card_sum,
    Nat.card_coe_set_eq] using (spliceColoring C D S).colorable

/-- A saturated set splits the actual used colors into disjoint parts.
Unused palette entries are not counted. -/
theorem used_colors_split [Finite A] (C : G.Coloring A) (S : Set V)
    (hS : Saturated C S) :
    (C '' S).ncard + (C '' Sᶜ).ncard = (Set.range C).ncard := by
  have hd : Disjoint (C '' S) (C '' Sᶜ) := by
    rw [Set.disjoint_left]
    rintro a ⟨v, hv, rfl⟩ ⟨w, hw, heq⟩
    exact hw ((hS heq).mpr hv)
  rw [← Set.ncard_union_eq hd, ← Set.image_union, Set.union_compl_self,
    Set.image_univ]

/-- An optimal coloring cannot use more colors on a saturated set than any
competing proper coloring uses there. -/
theorem used_colors_le_of_optimal [Finite A] [Finite B]
    (C : G.Coloring A) (D : G.Coloring B) (S : Set V)
    (hC : G.chromaticNumber = ((Set.range C).ncard : ℕ∞))
    (hS : Saturated C S) :
    (C '' S).ncard ≤ (D '' S).ncard := by
  have hbound := (colorable_splice C D S).chromaticNumber_le
  rw [hC] at hbound
  have hnat : (Set.range C).ncard ≤ (D '' S).ncard + (C '' Sᶜ).ncard := by
    exact_mod_cast hbound
  have hsplit := used_colors_split C S hS
  omega

/-- Two optimal proper colorings use equally many colors on any common union
of whole color classes. The graph need not have finitely many vertices. -/
theorem used_colors_eq_of_optimal [Finite A] [Finite B]
    (C : G.Coloring A) (D : G.Coloring B) (S : Set V)
    (hC : G.chromaticNumber = ((Set.range C).ncard : ℕ∞))
    (hD : G.chromaticNumber = ((Set.range D).ncard : ℕ∞))
    (hSC : Saturated C S) (hSD : Saturated D S) :
    (C '' S).ncard = (D '' S).ncard := by
  exact Nat.le_antisymm (used_colors_le_of_optimal C D S hC hSC)
    (used_colors_le_of_optimal D C S hD hSD)

/-- Native label graph: distinct labels are adjacent when they share a class
in either coloring. No incidence-multigraph encoding is imported. -/
def labelGraph (C : G.Coloring A) (D : G.Coloring B) : SimpleGraph V where
  Adj v w := v ≠ w ∧ (C v = C w ∨ D v = D w)
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.elim (Or.inl ∘ Eq.symm) (Or.inr ∘ Eq.symm)⟩⟩
  loopless := ⟨fun _ h => h.1 rfl⟩

theorem component_saturated_left (C : G.Coloring A) (D : G.Coloring B)
    (K : (labelGraph C D).ConnectedComponent) : Saturated C K.supp := by
  intro v w heq
  by_cases hvw : v = w
  · subst w
    rfl
  · exact K.mem_supp_congr_adj ⟨hvw, Or.inl heq⟩

theorem component_saturated_right (C : G.Coloring A) (D : G.Coloring B)
    (K : (labelGraph C D).ConnectedComponent) : Saturated D K.supp := by
  intro v w heq
  by_cases hvw : v = w
  · subst w
    rfl
  · exact K.mem_supp_congr_adj ⟨hvw, Or.inr heq⟩

/-- Actual connected components of the shared-class label graph are balanced
between the two optimal colorings. -/
theorem component_used_colors_eq [Finite A] [Finite B]
    (C : G.Coloring A) (D : G.Coloring B)
    (hC : G.chromaticNumber = ((Set.range C).ncard : ℕ∞))
    (hD : G.chromaticNumber = ((Set.range D).ncard : ℕ∞))
    (K : (labelGraph C D).ConnectedComponent) :
    (C '' K.supp).ncard = (D '' K.supp).ncard := by
  exact used_colors_eq_of_optimal C D K.supp hC hD
    (component_saturated_left C D K) (component_saturated_right C D K)

end AlbertsonOverlayBalance
