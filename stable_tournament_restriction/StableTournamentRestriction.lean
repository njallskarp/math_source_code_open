import Mathlib.Data.Nat.Basic
import Mathlib.Data.Set.Defs

/-!
# One-summand stable transitivity is hereditary

This file formalizes the induced-subtournament bridge used by the exact
order-eight stable-transitivity classification.  Tournaments and transitive
tournaments are represented by their natural-valued adjacency weights, so
the identity `T + X = Y + Z` is literal pointwise addition.
-/

namespace StableTournamentRestriction

universe u v

variable {α : Type u} {β : Type v}

/-- A natural-valued adjacency matrix is an ordinary tournament when its
diagonal is zero and the two directed weights on every distinct pair sum to
one. -/
def IsTournament (T : α → α → ℕ) : Prop :=
  (∀ x, T x x = 0) ∧ ∀ ⦃x y⦄, x ≠ y → T x y + T y x = 1

/-- A transitive tournament.  The second conjunct says that two consecutive
weight-one edges force the shortcut edge. -/
def IsTransitiveTournament (T : α → α → ℕ) : Prop :=
  IsTournament T ∧
    ∀ ⦃x y z⦄, T x y = 1 → T y z = 1 → T x z = 1

/-- Pull an adjacency weight back along an embedding.  For a subtype
embedding this is the ordinary induced-subtournament adjacency matrix. -/
def pullback (f : β → α) (T : α → α → ℕ) : β → β → ℕ :=
  fun x y => T (f x) (f y)

/-- The adjacency weights of the subtournament induced on a vertex subset. -/
def induced (T : α → α → ℕ) (S : Set α) : Subtype S → Subtype S → ℕ :=
  pullback (fun x : Subtype S => x.1) T

/-- A one-summand witness for stable transitivity: adding the transitive
tournament `X` to `T` gives the sum of the transitive tournaments `Y,Z`. -/
def HasOneSummandWitness (T : α → α → ℕ) : Prop :=
  ∃ X Y Z : α → α → ℕ,
    IsTransitiveTournament X ∧
    IsTransitiveTournament Y ∧
    IsTransitiveTournament Z ∧
    ∀ x y, T x y + X x y = Y x y + Z x y

/-- The property `m(T) ≤ 1` for an ordinary tournament `T`. -/
def IsOneSummandStable (T : α → α → ℕ) : Prop :=
  IsTournament T ∧ HasOneSummandWitness T

/-- Induced restrictions of tournaments are tournaments. -/
theorem isTournament_pullback (f : β → α) (hf : Function.Injective f)
    {T : α → α → ℕ} (hT : IsTournament T) :
    IsTournament (pullback f T) := by
  refine ⟨?_, ?_⟩
  · intro x
    exact hT.1 (f x)
  · intro x y hxy
    exact hT.2 (hf.ne hxy)

/-- Induced restrictions of transitive tournaments are transitive. -/
theorem isTransitiveTournament_pullback (f : β → α)
    (hf : Function.Injective f)
    {T : α → α → ℕ} (hT : IsTransitiveTournament T) :
    IsTransitiveTournament (pullback f T) := by
  refine ⟨isTournament_pullback f hf hT.1, ?_⟩
  intro x y z hxy hyz
  exact hT.2 hxy hyz

/-- Restricting each of `T,X,Y,Z` preserves a one-summand pointwise
decomposition. -/
theorem hasOneSummandWitness_pullback (f : β → α)
    (hf : Function.Injective f)
    {T : α → α → ℕ} (hT : HasOneSummandWitness T) :
    HasOneSummandWitness (pullback f T) := by
  obtain ⟨X, Y, Z, hX, hY, hZ, hEq⟩ := hT
  refine ⟨pullback f X, pullback f Y, pullback f Z,
    isTransitiveTournament_pullback f hf hX,
    isTransitiveTournament_pullback f hf hY,
    isTransitiveTournament_pullback f hf hZ, ?_⟩
  intro x y
  exact hEq (f x) (f y)

/-- One-summand stable transitivity is hereditary under induced
subtournaments. -/
theorem isOneSummandStable_pullback (f : β → α)
    (hf : Function.Injective f)
    {T : α → α → ℕ} (hT : IsOneSummandStable T) :
    IsOneSummandStable (pullback f T) :=
  ⟨isTournament_pullback f hf hT.1,
    hasOneSummandWitness_pullback f hf hT.2⟩

/-- Contrapositive extension principle: a tournament containing an induced
subtournament with no one-summand witness cannot itself have one. -/
theorem not_isOneSummandStable_of_pullback
    (f : β → α) (hf : Function.Injective f) {T : α → α → ℕ}
    (hsmall : ¬IsOneSummandStable (pullback f T)) :
    ¬IsOneSummandStable T := by
  intro hlarge
  exact hsmall (isOneSummandStable_pullback f hf hlarge)

/-- The restriction theorem in the ordinary induced-subtournament form. -/
theorem isOneSummandStable_induced (S : Set α)
    {T : α → α → ℕ} (hT : IsOneSummandStable T) :
    IsOneSummandStable (induced T S) :=
  isOneSummandStable_pullback (fun x : Subtype S => x.1)
    (by intro x y h; exact Subtype.ext h) hT

/-- Any tournament containing a non-one-summand-stable induced subtournament
is itself non-one-summand-stable. -/
theorem not_isOneSummandStable_of_induced (S : Set α)
    {T : α → α → ℕ}
    (hsmall : ¬IsOneSummandStable (induced T S)) :
    ¬IsOneSummandStable T :=
  not_isOneSummandStable_of_pullback
    (fun x : Subtype S => x.1) (by intro x y h; exact Subtype.ext h) hsmall

#print axioms isTournament_pullback
#print axioms isTransitiveTournament_pullback
#print axioms hasOneSummandWitness_pullback
#print axioms isOneSummandStable_pullback
#print axioms not_isOneSummandStable_of_pullback
#print axioms isOneSummandStable_induced
#print axioms not_isOneSummandStable_of_induced

end StableTournamentRestriction
