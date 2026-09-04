import Mathlib.Tactic

/-!
# Modular residue-slab composition of finite line partitions

This file represents a finite partition by a surjective coloring function.
Its fibers are the parts.  It formalizes the dimension-free composition step
used in the reviewed four-dimensional Hamming construction: complete blocks
of `s` in a new coordinate become new-coordinate parts, while each residual
layer receives a copy of the base partition.
-/

open Function

namespace ResidueSlabComposition

universe u v

/-- The colors used by the slab construction.  The left summand indexes an
old point and a complete `s`-block in the new coordinate.  The right summand
indexes a residual layer and an old color. -/
abbrev SlabColor (α : Type u) (β : Type v) (s p : ℕ) :=
  (α × Fin (p / s)) ⊕ (Fin (p % s) × β)

/-- A relation saying that two points of an appended product lie on one
coordinate line, assuming `baseLine` has that meaning in the old box. -/
def AppendedLine {α : Type u} {p : ℕ} (baseLine : α → α → Prop)
    (x y : α × Fin p) : Prop :=
  x.1 = y.1 ∨ (x.2 = y.2 ∧ baseLine x.1 y.1)

/-- Coloring realizing the slab construction. -/
def appendColor {α : Type u} {β : Type v}
    (s p : ℕ) (hs : 0 < s) (color : α → β) :
    α × Fin p → SlabColor α β s p := fun xz =>
  if h : xz.2.val < s * (p / s) then
    Sum.inl (xz.1, ⟨xz.2.val / s,
      (Nat.div_lt_iff_lt_mul hs).2 (by simpa [mul_comm] using h)⟩)
  else
    Sum.inr
      (⟨xz.2.val - s * (p / s), by
          have hp := Nat.mod_add_div p s
          omega⟩,
       color xz.1)

/-- A point in complete block `q`, at offset `r`. -/
def blockPoint {α : Type u} (s p : ℕ) (_hs : 0 < s)
    (x : α) (q : Fin (p / s)) (r : Fin s) : α × Fin p :=
  (x, ⟨s * q.val + r.val, by
    have hq : q.val + 1 ≤ p / s := q.isLt
    have hblock : s * q.val + r.val < s * (p / s) := calc
      s * q.val + r.val < s * q.val + s := Nat.add_lt_add_left r.isLt _
      _ = s * (q.val + 1) := by ring
      _ ≤ s * (p / s) := Nat.mul_le_mul_left s hq
    have hp := Nat.mod_add_div p s
    omega⟩)

/-- A point in residual layer `r`. -/
def residualPoint {α : Type u} (s p : ℕ)
    (x : α) (r : Fin (p % s)) : α × Fin p :=
  (x, ⟨s * (p / s) + r.val, by
    have hp := Nat.mod_add_div p s
    omega⟩)

@[simp]
theorem appendColor_blockPoint {α : Type u} {β : Type v}
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (x : α) (q : Fin (p / s)) (r : Fin s) :
    appendColor s p hs color (blockPoint s p hs x q r) =
      Sum.inl (x, q) := by
  have hr : s * q.val + r.val < s * (p / s) := by
    calc
      s * q.val + r.val < s * q.val + s := Nat.add_lt_add_left r.isLt _
      _ = s * (q.val + 1) := by ring
      _ ≤ s * (p / s) := Nat.mul_le_mul_left s q.isLt
  unfold appendColor
  split
  · apply congrArg Sum.inl
    apply Prod.ext
    · rfl
    · apply Fin.ext
      dsimp only [blockPoint]
      rw [Nat.add_comm, Nat.add_mul_div_left r.val q.val hs,
        Nat.div_eq_of_lt r.isLt, zero_add]
  · contradiction

@[simp]
theorem appendColor_residualPoint {α : Type u} {β : Type v}
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (x : α) (r : Fin (p % s)) :
    appendColor s p hs color (residualPoint s p x r) =
      Sum.inr (r, color x) := by
  have hnot : ¬s * (p / s) + r.val < s * (p / s) := by omega
  simp [appendColor, residualPoint, hnot]

/-- Every slab color is used when every base color is used. -/
theorem appendColor_surjective {α : Type u} {β : Type v}
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (hcolor : Surjective color) :
    Surjective (appendColor s p hs color) := by
  intro d
  cases d with
  | inl xq =>
      exact ⟨blockPoint s p hs xq.1 xq.2 ⟨0, hs⟩,
        appendColor_blockPoint s p hs color xq.1 xq.2 ⟨0, hs⟩⟩
  | inr rb =>
      obtain ⟨x, hx⟩ := hcolor rb.2
      refine ⟨residualPoint s p x rb.1, ?_⟩
      simp [hx]

/-- Offsets give an injection from `Fin s` into every complete-block fiber. -/
theorem completeBlock_fiber_card_ge {α : Type u} {β : Type v}
    [Fintype α] [DecidableEq α] [DecidableEq β]
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (x : α) (q : Fin (p / s)) :
    s ≤ Fintype.card
      {u : α × Fin p // appendColor s p hs color u = Sum.inl (x, q)} := by
  let f : Fin s →
      {u : α × Fin p // appendColor s p hs color u = Sum.inl (x, q)} :=
    fun r => ⟨blockPoint s p hs x q r,
      appendColor_blockPoint s p hs color x q r⟩
  have hf : Injective f := by
    intro r t hrt
    have hz : (blockPoint s p hs x q r).2 =
        (blockPoint s p hs x q t).2 :=
      congrArg (fun u => u.val.2) hrt
    apply Fin.ext
    have hzv := congrArg Fin.val hz
    simpa [blockPoint] using Nat.add_left_cancel hzv
  simpa using Fintype.card_le_of_injective f hf

/-- A residual-layer fiber contains an injective copy of its base fiber. -/
theorem residual_fiber_card_ge {α : Type u} {β : Type v}
    [Fintype α] [DecidableEq α] [DecidableEq β]
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (r : Fin (p % s)) (b : β)
    (hbase : s ≤ Fintype.card {x : α // color x = b}) :
    s ≤ Fintype.card
      {u : α × Fin p // appendColor s p hs color u = Sum.inr (r, b)} := by
  let f : {x : α // color x = b} →
      {u : α × Fin p // appendColor s p hs color u = Sum.inr (r, b)} :=
    fun x => ⟨residualPoint s p x.val r, by
      simp [x.property]⟩
  have hf : Injective f := by
    intro x y hxy
    apply Subtype.ext
    have hp : (residualPoint s p x.val r).1 =
        (residualPoint s p y.val r).1 :=
      congrArg (fun u => u.val.1) hxy
    simpa [residualPoint] using hp
  exact hbase.trans (Fintype.card_le_of_injective f hf)

/-- Every fiber in the appended coloring has size at least `s` if every base
fiber does. -/
theorem appendColor_fiber_card_ge {α : Type u} {β : Type v}
    [Fintype α] [DecidableEq α] [DecidableEq β]
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (hbase : ∀ b, s ≤ Fintype.card {x : α // color x = b})
    (d : SlabColor α β s p) :
    s ≤ Fintype.card {u : α × Fin p // appendColor s p hs color u = d} := by
  cases d with
  | inl xq => exact completeBlock_fiber_card_ge s p hs color xq.1 xq.2
  | inr rb => exact residual_fiber_card_ge s p hs color rb.1 rb.2 (hbase rb.2)

/-- Equality of appended colors preserves coordinate-line containment. -/
theorem appendColor_line {α : Type u} {β : Type v}
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (baseLine : α → α → Prop)
    (hbase : ∀ b x y, color x = b → color y = b → baseLine x y)
    {x y : α × Fin p}
    (hxy : appendColor s p hs color x = appendColor s p hs color y) :
    AppendedLine baseLine x y := by
  unfold appendColor at hxy
  split at hxy <;> split at hxy
  · left
    exact congrArg (fun z => z.1) (Sum.inl.inj hxy)
  · contradiction
  · contradiction
  · right
    have hp := Sum.inr.inj hxy
    have hr := congrArg (fun z => z.1) hp
    have hc := congrArg (fun z => z.2) hp
    constructor
    · apply Fin.ext
      have hxv := x.2.isLt
      have hyv := y.2.isLt
      have hxlower : s * (p / s) ≤ x.2.val := by omega
      have hylower : s * (p / s) ≤ y.2.val := by omega
      have hrv := congrArg Fin.val hr
      dsimp only at hrv
      omega
    · exact hbase (color x.1) x.1 y.1 rfl hc.symm

/-- Cardinality of the slab color type. -/
theorem card_slabColor {α : Type u} {β : Type v}
    [Fintype α] [Fintype β] (s p : ℕ) :
    Fintype.card (SlabColor α β s p) =
      Fintype.card α * (p / s) + (p % s) * Fintype.card β := by
  simp [SlabColor, mul_comm]

/-- The exact shortfall of the slab-plus-residual scheme is the quotient of
the product of the two remainders. -/
theorem modular_scheme_deficit {s M p : ℕ} (hs : 0 < s) :
    M * p / s =
      M * (p / s) + (p % s) * (M / s) +
        ((p % s) * (M % s)) / s := by
  have hdecomp :
      M * p =
        s * (M * (p / s) + (p % s) * (M / s)) +
          (p % s) * (M % s) := by
    have hM := Nat.mod_add_div M s
    have hp := Nat.mod_add_div p s
    calc
      M * p = M * (p % s + s * (p / s)) := by rw [hp]
      _ = (p % s) * M + s * (M * (p / s)) := by ring
      _ = (p % s) * (M % s + s * (M / s)) +
          s * (M * (p / s)) := by rw [hM]
      _ = s * (M * (p / s) + (p % s) * (M / s)) +
          (p % s) * (M % s) := by ring
  rw [hdecomp, Nat.mul_add_div hs]

/-- Exact arithmetic count when the product of remainders is below `s`. -/
theorem modular_part_count
    {s M p : ℕ} (hs : 0 < s)
    (hremainder : (p % s) * (M % s) < s) :
    M * (p / s) + (p % s) * (M / s) = M * p / s := by
  have h := modular_scheme_deficit (M := M) (p := p) hs
  rw [Nat.div_eq_of_lt hremainder, add_zero] at h
  exact h.symm

/-- The reviewed modular composition theorem, stated entirely through
standard finite types, coloring fibers, and an abstract coordinate-line
relation.  Surjectivity says the fibers form exactly the displayed number of
nonempty parts. -/
theorem modularComposition {α : Type u} {β : Type v}
    [Fintype α] [Fintype β] [DecidableEq α] [DecidableEq β]
    (s p : ℕ) (hs : 0 < s) (color : α → β)
    (baseLine : α → α → Prop)
    (hsurj : Surjective color)
    (hbaseSize : ∀ b, s ≤ Fintype.card {x : α // color x = b})
    (hbaseLine : ∀ b x y, color x = b → color y = b → baseLine x y)
    (hbaseCount : Fintype.card β = Fintype.card α / s)
    (hremainder : (p % s) * (Fintype.card α % s) < s) :
    Surjective (appendColor s p hs color) ∧
      (∀ d, s ≤ Fintype.card
        {u : α × Fin p // appendColor s p hs color u = d}) ∧
      (∀ d x y,
        appendColor s p hs color x = d →
        appendColor s p hs color y = d →
        AppendedLine baseLine x y) ∧
      Fintype.card (SlabColor α β s p) =
        Fintype.card (α × Fin p) / s := by
  refine ⟨appendColor_surjective s p hs color hsurj,
    appendColor_fiber_card_ge s p hs color hbaseSize, ?_, ?_⟩
  · intro d x y hx hy
    exact appendColor_line s p hs color baseLine hbaseLine (hx.trans hy.symm)
  · rw [card_slabColor, hbaseCount]
    simpa [Fintype.card_prod] using
      modular_part_count (M := Fintype.card α) (p := p) hs hremainder

#print axioms appendColor_surjective
#print axioms completeBlock_fiber_card_ge
#print axioms residual_fiber_card_ge
#print axioms appendColor_fiber_card_ge
#print axioms appendColor_line
#print axioms card_slabColor
#print axioms modular_scheme_deficit
#print axioms modular_part_count
#print axioms modularComposition

end ResidueSlabComposition
