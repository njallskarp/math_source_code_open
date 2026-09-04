import Mathlib.Data.Finset.Card

namespace RamseyOneFlip

/-- A support is violated when every variable on it receives its forbidden value. -/
def Violated {V : Type*} (value : Bool) (x : V → Bool) (support : Finset V) : Prop :=
  ∀ v ∈ support, x v = value

/-- Unsatisfiability of selected pure-positive and pure-negative supports. -/
def SelectedUnsatisfiable {V : Type*}
    (reds blues : Finset (Finset V)) : Prop :=
  ∀ x : V → Bool,
    (∃ R ∈ reds, Violated true x R) ∨
    (∃ B ∈ blues, Violated false x B)

/-- Every pair of distinct vertices in `S` has the prescribed color. -/
def Monochromatic {V : Type*}
    (color : V → V → Bool) (value : Bool) (S : Finset V) : Prop :=
  ∀ ⦃u⦄, u ∈ S → ∀ ⦃v⦄, v ∈ S → u ≠ v → color u v = value

/-- Clone the colors at `w`, flip only coordinate `z`, and set the pivot value. -/
def oneFlip {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (w z : V) (pivot : Bool) (v : V) : Bool :=
  if v = w then pivot else if v = z then !(color w z) else color w v

@[simp] theorem oneFlip_pivot {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (w z : V) (pivot : Bool) :
    oneFlip color w z pivot w = pivot := by
  simp [oneFlip]

@[simp] theorem oneFlip_flipped {V : Type*} [DecidableEq V]
    (color : V → V → Bool) {w z : V} (pivot : Bool) (hwz : w ≠ z) :
    oneFlip color w z pivot z = !(color w z) := by
  simp [oneFlip, hwz.symm]

theorem oneFlip_other {V : Type*} [DecidableEq V]
    (color : V → V → Bool) {w z v : V} (pivot : Bool)
    (hvw : v ≠ w) (hvz : v ≠ z) :
    oneFlip color w z pivot v = color w v := by
  simp [oneFlip, hvw, hvz]

/-- A selected blue support witnessing a single red edge from `w`, at `z`. -/
def IsBlueWitness {V : Type*}
    (color : V → V → Bool) (w z : V) (B : Finset V) : Prop :=
  z ∈ B ∧ w ∉ B ∧ color w z = true ∧
    ∀ v ∈ B, v ≠ z → color w v = false

/-- Selected blue supports having exactly one red incident edge from `w`. -/
def blueDefectClauses {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (w : V) (blues : Finset (Finset V)) :
    Finset (Finset V) :=
  blues.filter fun B => w ∉ B ∧
    ∃ z ∈ B, color w z = true ∧
      ∀ v ∈ B, v ≠ z → color w v = false

/-- A common red-link vertex forces a selected blue one-edge-defect witness. -/
theorem exists_blue_witness_of_common_red_link
    {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (reds blues : Finset (Finset V))
    (w z : V) (hwz : w ≠ z)
    (hunsat : SelectedUnsatisfiable reds blues)
    (hredMono : ∀ R ∈ reds, Monochromatic color true R)
    (hredAtW : ∃ R ∈ reds, w ∈ R)
    (hcommon : ∀ R ∈ reds, w ∈ R → z ∈ R)
    (hredNoExtend : ∀ R ∈ reds, w ∉ R → ∃ v ∈ R, color w v = false)
    (hblueNoExtend : ∀ B ∈ blues, w ∉ B → ∃ v ∈ B, color w v = true) :
    ∃ B ∈ blues, IsBlueWitness color w z B := by
  obtain ⟨R0, hR0, hwR0⟩ := hredAtW
  have hzR0 : z ∈ R0 := hcommon R0 hR0 hwR0
  have hwzRed : color w z = true := hredMono R0 hR0 hwR0 hzR0 hwz
  let f := oneFlip color w z true
  have hnoRed : ¬ ∃ R ∈ reds, Violated true f R := by
    rintro ⟨R, hR, hviol⟩
    by_cases hwR : w ∈ R
    · have hzR : z ∈ R := hcommon R hR hwR
      have hfz := hviol z hzR
      simp [f, oneFlip, hwz.symm, hwzRed] at hfz
    · by_cases hzR : z ∈ R
      · have hfz := hviol z hzR
        simp [f, oneFlip, hwz.symm, hwzRed] at hfz
      · obtain ⟨v, hvR, hvBlue⟩ := hredNoExtend R hR hwR
        have hvw : v ≠ w := by
          intro hvw
          subst v
          exact hwR hvR
        have hvz : v ≠ z := by
          intro hvz
          subst v
          exact hzR hvR
        have hfv := hviol v hvR
        simp [f, oneFlip, hvw, hvz, hvBlue] at hfv
  rcases hunsat f with hredViolated | hblueViolated
  · exact (hnoRed hredViolated).elim
  · obtain ⟨B, hB, hviol⟩ := hblueViolated
    have hwB : w ∉ B := by
      intro hwB
      have hfw := hviol w hwB
      simp [f] at hfw
    have hzB : z ∈ B := by
      by_contra hzB
      obtain ⟨v, hvB, hvRed⟩ := hblueNoExtend B hB hwB
      have hvw : v ≠ w := by
        intro hvw
        subst v
        exact hwB hvB
      have hvz : v ≠ z := by
        intro hvz
        subst v
        exact hzB hvB
      have hfv := hviol v hvB
      simp [f, oneFlip, hvw, hvz, hvRed] at hfv
    refine ⟨B, hB, hzB, hwB, hwzRed, ?_⟩
    intro v hvB hvz
    have hvw : v ≠ w := by
      intro hvw
      subst v
      exact hwB hvB
    have hfv := hviol v hvB
    simpa [f, oneFlip, hvw, hvz] using hfv

/-- Any blue witness belongs to the finite family of blue defect clauses. -/
theorem mem_blueDefectClauses_of_isBlueWitness
    {V : Type*} [DecidableEq V]
    {color : V → V → Bool} {w z : V} {blues : Finset (Finset V)} {B : Finset V}
    (hB : B ∈ blues) (h : IsBlueWitness color w z B) :
    B ∈ blueDefectClauses color w blues := by
  rcases h with ⟨hzB, hwB, hwz, hrest⟩
  simp only [blueDefectClauses, Finset.mem_filter, hB, true_and]
  exact ⟨hwB, z, hzB, hwz, hrest⟩

/-- One defect clause cannot witness two distinct common-link vertices. -/
theorem blue_witness_injective_on_common_link
    {V : Type*} [DecidableEq V]
    {color : V → V → Bool} {w z z' : V} {B : Finset V}
    (hredZ' : color w z' = true)
    (hz : IsBlueWitness color w z B)
    (hz' : IsBlueWitness color w z' B) :
    z = z' := by
  by_contra hne
  have hz'B : z' ∈ B := hz'.1
  have hblue : color w z' = false := hz.2.2.2 z' hz'B (fun h => hne h.symm)
  simp [hredZ'] at hblue

/-- Common red-link vertices inject into the selected blue defect clauses. -/
theorem card_common_red_link_le_blueDefectClauses
    {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (reds blues : Finset (Finset V))
    (w : V) (I : Finset V)
    (hneq : ∀ z ∈ I, w ≠ z)
    (hunsat : SelectedUnsatisfiable reds blues)
    (hredMono : ∀ R ∈ reds, Monochromatic color true R)
    (hredAtW : ∃ R ∈ reds, w ∈ R)
    (hcommon : ∀ z ∈ I, ∀ R ∈ reds, w ∈ R → z ∈ R)
    (hredNoExtend : ∀ R ∈ reds, w ∉ R → ∃ v ∈ R, color w v = false)
    (hblueNoExtend : ∀ B ∈ blues, w ∉ B → ∃ v ∈ B, color w v = true) :
    I.card ≤ (blueDefectClauses color w blues).card := by
  classical
  have hexists (z : V) (hz : z ∈ I) :
      ∃ B ∈ blues, IsBlueWitness color w z B :=
    exists_blue_witness_of_common_red_link color reds blues w z (hneq z hz)
      hunsat hredMono hredAtW (hcommon z hz) hredNoExtend hblueNoExtend
  let chosen : V → Finset V := fun z =>
    if hz : z ∈ I then Classical.choose (hexists z hz) else ∅
  have hchosen (z : V) (hz : z ∈ I) :
      chosen z ∈ blues ∧ IsBlueWitness color w z (chosen z) := by
    simp only [chosen, dif_pos hz]
    exact Classical.choose_spec (hexists z hz)
  have hredOnI (z : V) (hz : z ∈ I) : color w z = true := by
    obtain ⟨R0, hR0, hwR0⟩ := hredAtW
    exact hredMono R0 hR0 hwR0 (hcommon z hz R0 hR0 hwR0) (hneq z hz)
  apply Finset.card_le_card_of_injOn chosen
  · intro z hz
    exact mem_blueDefectClauses_of_isBlueWitness (hchosen z hz).1 (hchosen z hz).2
  · intro z hz z' hz' heq
    have hzWitness := (hchosen z hz).2
    have hz'Witness := (hchosen z' hz').2
    rw [← heq] at hz'Witness
    exact blue_witness_injective_on_common_link (hredOnI z' hz') hzWitness hz'Witness

/-- A unique selected red four-set through `w` forces three blue defect clauses. -/
theorem unique_red_four_clause_forces_three_blue_defects
    {V : Type*} [DecidableEq V]
    (color : V → V → Bool) (reds blues : Finset (Finset V))
    (w : V) (R0 : Finset V)
    (hR0 : R0 ∈ reds) (hwR0 : w ∈ R0) (hR0card : R0.card = 4)
    (hunique : ∀ R ∈ reds, w ∈ R → R = R0)
    (hunsat : SelectedUnsatisfiable reds blues)
    (hredMono : ∀ R ∈ reds, Monochromatic color true R)
    (hredNoExtend : ∀ R ∈ reds, w ∉ R → ∃ v ∈ R, color w v = false)
    (hblueNoExtend : ∀ B ∈ blues, w ∉ B → ∃ v ∈ B, color w v = true) :
    3 ≤ (blueDefectClauses color w blues).card := by
  let I := R0.erase w
  have hIcard : I.card = 3 := by
    simp [I, Finset.card_erase_of_mem hwR0, hR0card]
  have hcard := card_common_red_link_le_blueDefectClauses color reds blues w I
    (fun z hz => by
      have hzw : z ≠ w := (Finset.mem_erase.mp hz).1
      exact fun hwz => hzw hwz.symm)
    hunsat hredMono ⟨R0, hR0, hwR0⟩
    (fun z hz R hR hwR => by
      rw [hunique R hR hwR]
      exact (Finset.mem_erase.mp hz).2)
    hredNoExtend hblueNoExtend
  omega

#print axioms exists_blue_witness_of_common_red_link
#print axioms blue_witness_injective_on_common_link
#print axioms card_common_red_link_le_blueDefectClauses
#print axioms unique_red_four_clause_forces_three_blue_defects

end RamseyOneFlip
