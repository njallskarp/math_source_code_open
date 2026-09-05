import AlbertsonOverlayBalance

/-!
# Component balance in the actual block-intersection graph

Vertices are nonempty color classes, tagged by the coloring. Adjacency records
nonempty class intersection. Edge multiplicity and cycle rank are not modeled.
-/

open Set SimpleGraph

namespace AlbertsonOverlayBalance

variable {V A B : Type*} {G : SimpleGraph V}

/-- The underlying simple block-incidence graph, with unused colors excluded. -/
def incidenceGraph (C : G.Coloring A) (D : G.Coloring B) :
    SimpleGraph ((Set.range C) ⊕ (Set.range D)) where
  Adj
    | Sum.inl a, Sum.inr b => ∃ v, C v = a.val ∧ D v = b.val
    | Sum.inr b, Sum.inl a => ∃ v, C v = a.val ∧ D v = b.val
    | _, _ => False
  symm := ⟨by intro x y h; cases x <;> cases y <;> exact h⟩
  loopless := ⟨by intro x; cases x <;> exact id⟩

/-- Each original vertex supplies an incidence between its two actual blocks. -/
theorem incidence_adj (C : G.Coloring A) (D : G.Coloring B) (v : V) :
    (incidenceGraph C D).Adj
      (Sum.inl ⟨C v, Set.mem_range_self v⟩)
      (Sum.inr ⟨D v, Set.mem_range_self v⟩) := ⟨v, rfl, rfl⟩

/-- Labels belonging to an actual incidence component, defined from its left side. -/
def incidenceLabels (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) : Set V :=
  {v | Sum.inl ⟨C v, Set.mem_range_self v⟩ ∈ K.supp}

/-- The right-side definition selects exactly the same original labels. -/
theorem incidenceLabels_mem_right (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) (v : V) :
    v ∈ incidenceLabels C D K ↔ Sum.inr ⟨D v, Set.mem_range_self v⟩ ∈ K.supp :=
  K.mem_supp_congr_adj (incidence_adj C D v)

theorem incidenceLabels_saturated_left (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) :
    Saturated C (incidenceLabels C D K) := by
  intro v w heq
  have hsub : (⟨C v, Set.mem_range_self v⟩ : Set.range C) =
      ⟨C w, Set.mem_range_self w⟩ := Subtype.ext heq
  change (Sum.inl ⟨C v, Set.mem_range_self v⟩ ∈ K.supp) ↔
    Sum.inl ⟨C w, Set.mem_range_self w⟩ ∈ K.supp
  rw [hsub]

theorem incidenceLabels_saturated_right (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) :
    Saturated D (incidenceLabels C D K) := by
  intro v w heq
  rw [incidenceLabels_mem_right, incidenceLabels_mem_right]
  have hsub : (⟨D v, Set.mem_range_self v⟩ : Set.range D) =
      ⟨D w, Set.mem_range_self w⟩ := Subtype.ext heq
  rw [hsub]

/-- Left block vertices project bijectively to the colors used on the component labels. -/
theorem incidence_left_image (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) :
    Subtype.val '' (Sum.inl ⁻¹' K.supp) = C '' incidenceLabels C D K := by
  ext a
  constructor
  · rintro ⟨a, ha, rfl⟩
    change Sum.inl a ∈ K.supp at ha
    obtain ⟨v, hv⟩ := a.property
    have hsub : (⟨C v, Set.mem_range_self v⟩ : Set.range C) = a := Subtype.ext hv
    refine ⟨v, ?_, hv⟩
    change Sum.inl ⟨C v, Set.mem_range_self v⟩ ∈ K.supp
    simpa only [hsub] using ha
  · rintro ⟨v, hv, rfl⟩
    exact ⟨⟨C v, Set.mem_range_self v⟩, hv, rfl⟩

theorem incidence_right_image (C : G.Coloring A) (D : G.Coloring B)
    (K : (incidenceGraph C D).ConnectedComponent) :
    Subtype.val '' (Sum.inr ⁻¹' K.supp) = D '' incidenceLabels C D K := by
  ext b
  constructor
  · rintro ⟨b, hb, rfl⟩
    change Sum.inr b ∈ K.supp at hb
    obtain ⟨v, hv⟩ := b.property
    have hsub : (⟨D v, Set.mem_range_self v⟩ : Set.range D) = b := Subtype.ext hv
    refine ⟨v, (incidenceLabels_mem_right C D K v).mpr ?_, hv⟩
    simpa only [hsub] using hb
  · rintro ⟨v, hv, rfl⟩
    exact ⟨⟨D v, Set.mem_range_self v⟩,
      (incidenceLabels_mem_right C D K v).mp hv, rfl⟩

/-- The actual left and right block counts agree in every component of the
block-intersection graph of two optimal finite-palette colorings. -/
theorem incidence_component_balance [Finite A] [Finite B]
    (C : G.Coloring A) (D : G.Coloring B)
    (hC : G.chromaticNumber = ((Set.range C).ncard : ℕ∞))
    (hD : G.chromaticNumber = ((Set.range D).ncard : ℕ∞))
    (K : (incidenceGraph C D).ConnectedComponent) :
    (Sum.inl ⁻¹' K.supp).ncard = (Sum.inr ⁻¹' K.supp).ncard := by
  have hleft := Set.ncard_image_of_injective (Sum.inl ⁻¹' K.supp)
    (@Subtype.val_injective A (· ∈ Set.range C))
  have hright := Set.ncard_image_of_injective (Sum.inr ⁻¹' K.supp)
    (@Subtype.val_injective B (· ∈ Set.range D))
  rw [incidence_left_image] at hleft
  rw [incidence_right_image] at hright
  rw [← hleft, ← hright]
  exact used_colors_eq_of_optimal C D (incidenceLabels C D K) hC hD
    (incidenceLabels_saturated_left C D K) (incidenceLabels_saturated_right C D K)

end AlbertsonOverlayBalance
