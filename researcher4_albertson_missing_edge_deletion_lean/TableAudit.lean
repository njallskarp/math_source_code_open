import DeletionTableSoundness

open Finset AlbertsonDeletionTableSpecification AlbertsonDeletionTableSoundness

-- A genuinely nonmonotone upper-budget table: weaker budgets can be assigned
-- better valid seeds. The soundness checker need not reject this inefficiency.
private def auditSeed (n f : ℕ) : ℕ := if n = 5 ∧ f = 1 then 5 else 0

private def auditValue (n f : ℕ) : ℕ :=
  if n = 6 ∧ f = 1 then 10 else auditSeed n f

private def auditStep (n f : ℕ) : ActiveStep :=
  if n = 6 ∧ f = 1 then .delete 2 else .seed

example : tableCheck 6 1 auditValue auditSeed auditStep = true := by decide

example : ¬ AntitoneOn (auditValue 5) (Set.Iic 1) := by
  intro h
  have hbad : auditValue 5 1 ≤ auditValue 5 0 := h (by decide) (by decide) (by decide)
  have hvalues : auditValue 5 1 = 5 ∧ auditValue 5 0 = 0 := by decide
  omega

-- Complete semantic test, not just scalar checker evaluation. Counts are
-- the numbers of four-element vertex subsets, not drawing crossing counts.
-- The seed and survival hypotheses are proved on every induced vertex subset.
private theorem auditSeedsValid : SeedsValid (⊥ : SimpleGraph (Fin 6)) 6 1
    auditSeed (fun S => S.card.choose 4) := by
  intro S hS f hf hbudget
  by_cases h : S.card = 5 ∧ f = 1
  · simp only [auditSeed, h.1, h.2, and_self, ↓reduceIte]
    decide
  · simp only [auditSeed, if_neg h]
    exact Nat.zero_le _

private theorem auditSurvival : DeletionSurvival 6
    (fun S : Finset (Fin 6) => S.card.choose 4) := by
  intro S hS hfour
  have heq : (∑ v ∈ S, (S.erase v).card.choose 4) =
      S.card * (S.card - 1).choose 4 := by
    calc
      _ = ∑ v ∈ S, (S.card - 1).choose 4 := by
        apply Finset.sum_congr rfl
        intro v hv
        rw [Finset.card_erase_of_mem hv]
      _ = _ := by simp
  rw [heq]
  change S.card * (S.card - 1).choose 4 ≤ (S.card - 4) * S.card.choose 4
  rcases (show S.card = 5 ∨ S.card = 6 by omega) with h | h
  · rw [h]; decide
  · rw [h]; decide

#print axioms auditSeedsValid
#print axioms auditSurvival

example : ∀ S : Finset (Fin 6), S.card ≤ 6 → ∀ f ≤ 1,
    missingCount (⊥ : SimpleGraph (Fin 6)) S ≤ f →
      auditValue S.card f ≤ S.card.choose 4 :=
  tableCheck_sound ⊥ 6 1 auditValue auditSeed auditStep (fun S => S.card.choose 4)
    (by decide) auditSeedsValid auditSurvival

-- The active deletion branch is used at the full six-vertex set.
example : (10 : ℕ) ≤ (15 : ℕ) := by
  have h := tableCheck_sound (⊥ : SimpleGraph (Fin 6)) 6 1 auditValue auditSeed auditStep
    (fun S => S.card.choose 4) (by decide) auditSeedsValid auditSurvival
    univ (by decide) 1 (by decide) (by decide)
  have hv : auditValue (univ : Finset (Fin 6)).card 1 = 10 := by decide
  have hc : (univ : Finset (Fin 6)).card.choose 4 = 15 := by decide
  rwa [hv, hc] at h

-- Empty order and zero budget are accepted through valid seeds.
example : tableCheck 0 0 (fun _ _ => 0) (fun _ _ => 0) (fun _ _ => .seed) = true := by
  decide

-- A claimed seed larger than its justification is rejected.
example : tableCheck 0 0 (fun _ _ => 1) (fun _ _ => 0) (fun _ _ => .seed) = false := by
  decide

-- Even a zero-valued deletion step is rejected at order four.
example : tableCheck 4 1 (fun _ _ => 0) (fun _ _ => 0)
    (fun n f => if n = 4 ∧ f = 1 then .delete 2 else .seed) = false := by decide

-- Thresholds cannot exceed the actual vertex order.
example : tableCheck 5 20 (fun _ _ => 0) (fun _ _ => 0)
    (fun n f => if n = 5 ∧ f = 20 then .delete 6 else .seed) = false := by decide

-- A positive-capacity gap is required; zero-budget deletion is not a valid step.
example : tableCheck 5 0 (fun _ _ => 0) (fun _ _ => 0)
    (fun n _ => if n = 5 then .delete 1 else .seed) = false := by decide

-- One above the exact ceiling is rejected, with all other entry data unchanged.
example : tableCheck 6 1
    (fun n f => if n = 6 ∧ f = 1 then 11 else auditSeed n f)
    auditSeed auditStep = false := by decide

-- A nonintegral quotient must round upward, not down.
example : ((7 - 2) * 5 + 2 * 0) ⌈/⌉ (7 - 4) = (9 : ℕ) := by decide
