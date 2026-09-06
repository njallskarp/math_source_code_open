import AlbertsonMissingEdgeDeletion

/-!
Bounded proof-carrying table schema, originally isolated as a local specification.
`DeletionTableSoundness.lean` now proves its soundness, in fact without the
row-antitonicity clause. This schema alone does not prove soundness, certify the
published Python table, extract a certificate, or formalize any drawing.

The missing-edge graph is native. Counts are indexed by actual ambient vertex
subsets, so the soundness theorem cannot ignore induced graphs.
All rows and budgets needed by recursive deletion lie in the checked rectangle.
-/

open Finset

namespace AlbertsonDeletionTableSpecification

abbrev Table := ℕ → ℕ → ℕ

/-- A zero or independently justified seed can terminate a dependency branch.
A deletion step must record an admissible threshold, not just a hash. -/
inductive ActiveStep where
  | seed
  | delete (threshold : ℕ)

def EntryValid (value seed : Table) (step : ActiveStep) (n f : ℕ) : Prop :=
  match step with
  | .seed => value n f ≤ seed n f
  | .delete t =>
      4 < n ∧ t ≤ n ∧ (t - 1).choose 2 < f ∧
        value n f ≤
          ((n - t) * value (n - 1) f + t * value (n - 1) (f - 1)) ⌈/⌉ (n - 4)

/-- Original stronger interface on a finite checking domain. Both recursive
budgets remain in the rectangle, and deletion strictly lowers the order.
The companion's Boolean checker omits this unnecessary row-monotonicity clause.
No automatic certificate serialization is provided. -/
def TableValid (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) : Prop :=
  (∀ n ∈ range (maxOrder + 1),
    AntitoneOn (value n) (Set.Iic maxBudget)) ∧
  ∀ n ∈ range (maxOrder + 1), ∀ f ∈ range (maxBudget + 1),
    EntryValid value seed (step n f) n f

variable {V : Type*} [DecidableEq V]
    (H : SimpleGraph V) [DecidableRel H.Adj]

/-- The actual missing-edge count in an induced vertex set. -/
def missingCount (S : Finset V) : ℕ :=
  (H.induce (S : Set V)).edgeFinset.card

/-- External mathematical interpretation: local seed bounds must hold on each
actual induced subgraph, for every checked upper missing-edge budget. -/
def SeedsValid (maxOrder maxBudget : ℕ) (seed : Table) (count : Finset V → ℕ) : Prop :=
  ∀ S : Finset V, S.card ≤ maxOrder →
    ∀ f ≤ maxBudget, missingCount H S ≤ f → seed S.card f ≤ count S

/-- External drawing interface, expressed solely on actual finite subsets.
Existence and interpretation of such a count family are not assumed silently. -/
def DeletionSurvival (maxOrder : ℕ) (count : Finset V → ℕ) : Prop :=
  ∀ S : Finset V, S.card ≤ maxOrder → 4 < S.card →
    (∑ v ∈ S, count (S.erase v)) ≤ (S.card - 4) * count S

/-- Original soundness interface, proved by `soundnessTarget` in the companion
module. This is itself a proposition-valued definition, not an axiom. It
quantifies over every ambient subset and upper budget, with premises exposed. -/
def SoundnessTarget (maxOrder maxBudget : ℕ) (value seed : Table)
    (step : ℕ → ℕ → ActiveStep) (count : Finset V → ℕ) : Prop :=
  TableValid maxOrder maxBudget value seed step →
  SeedsValid H maxOrder maxBudget seed count →
  DeletionSurvival maxOrder count →
  ∀ S : Finset V, S.card ≤ maxOrder →
    ∀ f ≤ maxBudget, missingCount H S ≤ f → value S.card f ≤ count S

#check @SoundnessTarget
#print axioms EntryValid
#print axioms TableValid
#print axioms missingCount
#print axioms SeedsValid
#print axioms DeletionSurvival
#print axioms SoundnessTarget

-- A published large-budget diagnostic recursively visits (37, 685).
-- Its source threshold is 38: the previous pair capacity is 666, then 703.
example : (37 : ℕ).choose 2 < 685 ∧ 685 ≤ (38 : ℕ).choose 2 := by decide

-- A 38-vertex deletion witness cannot be used on a 37-vertex state.
example (value seed : Table) : ¬ EntryValid value seed (.delete 38) 37 685 := by
  intro h
  have ht : 38 ≤ 37 := h.2.1
  omega

-- Rejecting that active branch does not reject a separately justified zero seed.
example : EntryValid (fun _ _ => 0) (fun _ _ => 0) .seed 37 685 := by
  exact Nat.le_refl 0

end AlbertsonDeletionTableSpecification
