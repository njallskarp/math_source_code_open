import DeletionTableSpecification

/-!
Bounded soundness of upper-budget deletion tables on actual induced subgraphs.
Unlike exact-count table lookup, upper-budget induction needs no antitonicity.
Seeds and survival remain explicit hypotheses. No numerical source is imported.
-/

open Finset AlbertsonMissingEdgeDeletion AlbertsonDeletionTableSpecification

namespace AlbertsonDeletionTableSoundness

variable {V : Type*} [DecidableEq V] (H : SimpleGraph V) [DecidableRel H.Adj]

/-- Native identification of deletion inside an induced graph with finite erasure. -/
def induceEraseIso (S : Finset V) (v : S) :
    ((H.induce (S : Set V)).induce ({v}ᶜ : Set S)) ≃g
      H.induce (S.erase (v : V) : Set V) where
  toFun x := ⟨x.1.1, Finset.mem_erase.mpr ⟨fun h => x.2 (Subtype.ext h), x.1.2⟩⟩
  invFun x := ⟨⟨x.1, (Finset.mem_erase.mp x.2).2⟩,
    fun h => (Finset.mem_erase.mp x.2).1 (congrArg Subtype.val h)⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_rel_iff' := by intros; rfl

theorem card_induce_erase (S : Finset V) (v : S) :
    ((H.induce (S : Set V)).induce ({v}ᶜ : Set S)).edgeFinset.card =
      missingCount H (S.erase (v : V)) := by
  classical
  exact (induceEraseIso H S v).card_edgeFinset_eq

theorem missingCount_erase_le (S : Finset V) (v : S) :
    missingCount H (S.erase (v : V)) ≤ missingCount H S := by
  classical
  rw [← card_induce_erase, card_vertex_deletion]
  exact Nat.sub_le _ _

/-- Upper-budget statements on smaller vertex sets supply both local levels
directly, without any numerical monotonicity premise. -/
theorem subset_deletion_step (S : Finset V) (f t : ℕ)
    (hbudget : missingCount H S ≤ f) (ht : t ≤ S.card)
    (hgap : (t - 1).choose 2 < f) (horder : 4 < S.card)
    (a b : ℕ) (count : Finset V → ℕ)
    (hbase : ∀ v ∈ S, a ≤ count (S.erase v))
    (hbetter : ∀ v ∈ S, missingCount H (S.erase v) ≤ f - 1 → b ≤ count (S.erase v))
    (hsurvive : (∑ v ∈ S, count (S.erase v)) ≤ (S.card - 4) * count S) :
    ((S.card - t) * a + t * b) ⌈/⌉ (S.card - 4) ≤ count S := by
  classical
  obtain ⟨T, hTcard, hT⟩ := exists_improved_deletions (H.induce (S : Set V)) f t
    hbudget (by simpa using ht) hgap
  have hsum := two_level_sum_bound T a b (fun v : S => count (S.erase (v : V)))
    (fun v => hbase v v.2) (fun v hv => hbetter v v.2 (by
      rw [← card_induce_erase]
      exact hT v hv))
  have hconvert : (∑ v : S, count (S.erase (v : V))) = ∑ v ∈ S, count (S.erase v) := by
    exact (Finset.sum_subtype S (fun _ => Iff.rfl) (fun v => count (S.erase v))).symm
  rw [ceilDiv_le_iff_le_mul (show 0 < S.card - 4 by omega)]
  have h := hsum.trans (hconvert.le.trans hsurvive)
  simpa [hTcard] using h

/-- Every checked entry is sound for every actual induced subset and upper
budget in the rectangle. Only seed or strictly lower-order deletion steps occur.
There is deliberately no row-antitonicity hypothesis. -/
theorem checked_entries_sound (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) (count : Finset V → ℕ)
    (hentries : ∀ n ≤ maxOrder, ∀ f ≤ maxBudget,
      EntryValid value seed (step n f) n f)
    (hseed : SeedsValid H maxOrder maxBudget seed count)
    (hsurvive : DeletionSurvival maxOrder count) :
    ∀ S : Finset V, S.card ≤ maxOrder →
      ∀ f ≤ maxBudget, missingCount H S ≤ f → value S.card f ≤ count S := by
  intro S
  induction hn : S.card using Nat.strong_induction_on generalizing S with
  | h n ih =>
    intro hN f hf hbudget
    have hv := hentries n (by omega) f hf
    cases hs : step n f with
    | seed =>
      have he : value n f ≤ seed n f := by simpa [hs, EntryValid] using hv
      simpa [hn] using he.trans (by simpa [hn] using hseed S (by omega) f hf hbudget)
    | delete t =>
      have he : 4 < n ∧ t ≤ n ∧ (t - 1).choose 2 < f ∧
          value n f ≤ ((n - t) * value (n - 1) f + t * value (n - 1) (f - 1))
            ⌈/⌉ (n - 4) := by simpa [hs, EntryValid] using hv
      have hlocal (v : V) (hvS : v ∈ S) (g : ℕ) (hg : g ≤ maxBudget)
          (hbg : missingCount H (S.erase v) ≤ g) :
          value (n - 1) g ≤ count (S.erase v) := by
        have hc : (S.erase v).card = n - 1 := by rw [Finset.card_erase_of_mem hvS, hn]
        exact ih (n - 1) (by omega) (S.erase v) hc (by omega) g hg hbg
      have hout := subset_deletion_step H S f t hbudget (by omega) he.2.2.1
        (by omega) (value (n - 1) f) (value (n - 1) (f - 1)) count
        (fun v hvS => hlocal v hvS f hf
          ((missingCount_erase_le H S ⟨v, hvS⟩).trans hbudget))
        (fun v hvS hb => hlocal v hvS (f - 1) (by omega) hb)
        (hsurvive S (by omega) (by omega))
      simpa [hn] using he.2.2.2.trans (by simpa [hn] using hout)

/-- The previously frozen specification is a consequence of the stronger
theorem above. Its separate row-antitonicity clause is unused. -/
theorem soundnessTarget (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) (count : Finset V → ℕ) :
    SoundnessTarget H maxOrder maxBudget value seed step count := by
  intro hvalid hseed hsurvive
  exact checked_entries_sound H maxOrder maxBudget value seed step count
    (fun n hn f hf => hvalid.2 n (mem_range.mpr (by omega)) f (mem_range.mpr (by omega)))
    hseed hsurvive

/-- A finite, executable check of seed/deletion entries. It deliberately does
not check seed interpretation or crossing survival, which remain mathematical
hypotheses. No parser, table generator or external numerical data is trusted. -/
def tableCheck (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) : Bool :=
  (List.range (maxOrder + 1)).all fun n => (List.range (maxBudget + 1)).all fun f =>
    match step n f with
    | .seed => decide (value n f ≤ seed n f)
    | .delete t => decide (4 < n ∧ t ≤ n ∧ (t - 1).choose 2 < f ∧
        value n f ≤ ((n - t) * value (n - 1) f + t * value (n - 1) (f - 1))
          ⌈/⌉ (n - 4))

theorem tableCheck_eq_true_iff (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) :
    tableCheck maxOrder maxBudget value seed step = true ↔
      ∀ n ≤ maxOrder, ∀ f ≤ maxBudget, EntryValid value seed (step n f) n f := by
  simp only [tableCheck, List.all_eq_true, List.mem_range, Nat.lt_succ_iff]
  refine forall_congr' fun n => forall_congr' fun _ =>
    forall_congr' fun f => forall_congr' fun _ => ?_
  cases step n f <;> simp [EntryValid]

/-- Passing the finite checker implies validity on every actual induced subset
and checked upper budget, conditional only on seed interpretation and survival. -/
theorem tableCheck_sound (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) (count : Finset V → ℕ)
    (hcheck : tableCheck maxOrder maxBudget value seed step = true)
    (hseed : SeedsValid H maxOrder maxBudget seed count)
    (hsurvive : DeletionSurvival maxOrder count) :
    ∀ S : Finset V, S.card ≤ maxOrder →
      ∀ f ≤ maxBudget, missingCount H S ≤ f → value S.card f ≤ count S :=
  checked_entries_sound H maxOrder maxBudget value seed step count
    ((tableCheck_eq_true_iff maxOrder maxBudget value seed step).mp hcheck) hseed hsurvive

#print axioms induceEraseIso
#print axioms card_induce_erase
#print axioms missingCount_erase_le
#print axioms subset_deletion_step
#print axioms checked_entries_sound
#print axioms soundnessTarget
#print axioms tableCheck
#print axioms tableCheck_eq_true_iff
#print axioms tableCheck_sound

end AlbertsonDeletionTableSoundness
