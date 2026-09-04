import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.DegreeSum
import Mathlib.Combinatorics.SimpleGraph.Prod

namespace HypercubeSquareLift

open SimpleGraph

variable {V : Type*}

/-- A three-edge path which closes to a genuine four-vertex square after
adding the edge `x -- y`.  Adjacency supplies the three consecutive
distinctness conditions; the two stated inequalities exclude the remaining
vertex collisions. -/
def SquareWitness (G : SimpleGraph V) (x y : V) : Prop :=
  ∃ a b, x ≠ b ∧ a ≠ y ∧
    G.Adj x a ∧ G.Adj a b ∧ G.Adj b y

/-- Reversing the closing path reverses a square witness. -/
theorem SquareWitness.symm {G : SimpleGraph V} {x y : V}
    (h : SquareWitness G x y) : SquareWitness G y x := by
  obtain ⟨a, b, hxb, hay, hxa, hab, hby⟩ := h
  exact ⟨b, a, hay.symm, hxb.symm, by simpa [adj_comm] using hby,
    by simpa [adj_comm] using hab, by simpa [adj_comm] using hxa⟩

/-- A graph contains no four-cycle. -/
def SquareFree (G : SimpleGraph V) : Prop :=
  ∀ ⦃x y⦄, G.Adj x y → ¬SquareWitness G x y

/-- `G` is square-saturated inside the host `H`: it is a spanning subgraph,
is square-free, and every omitted host edge closes a square. -/
structure SquareSaturatedIn (G H : SimpleGraph V) : Prop where
  le_host : G ≤ H
  squareFree : SquareFree G
  closes_omitted : ∀ ⦃x y⦄, H.Adj x y → ¬G.Adj x y → SquareWitness G x y

/-- A set dominates a graph when every vertex outside it has a neighbor in
the set.  This is the open-neighborhood convention needed by the lift. -/
def Dominates (K : SimpleGraph V) (D : Set V) : Prop :=
  ∀ ⦃v⦄, v ∉ D → ∃ u ∈ D, K.Adj u v

/-- Two horizontal graph layers, with a vertical edge precisely over each
vertex of `D`.  `Sum.inl` and `Sum.inr` name the two layers. -/
def twoLayerLift (G₀ G₁ : SimpleGraph V) (D : Set V) : SimpleGraph (Sum V V) where
  Adj x y :=
    match x, y with
    | .inl a, .inl b => G₀.Adj a b
    | .inr a, .inr b => G₁.Adj a b
    | .inl a, .inr b => a = b ∧ a ∈ D
    | .inr a, .inl b => a = b ∧ b ∈ D
  symm.symm x y := by
    cases x <;> cases y <;> simp [adj_comm, eq_comm]
  loopless.irrefl x := by
    cases x <;> simp

@[simp] theorem twoLayerLift_adj_inl_inl
    (G₀ G₁ : SimpleGraph V) (D : Set V) (x y : V) :
    (twoLayerLift G₀ G₁ D).Adj (.inl x) (.inl y) ↔ G₀.Adj x y :=
  Iff.rfl

@[simp] theorem twoLayerLift_adj_inr_inr
    (G₀ G₁ : SimpleGraph V) (D : Set V) (x y : V) :
    (twoLayerLift G₀ G₁ D).Adj (.inr x) (.inr y) ↔ G₁.Adj x y :=
  Iff.rfl

@[simp] theorem twoLayerLift_adj_inl_inr
    (G₀ G₁ : SimpleGraph V) (D : Set V) (x y : V) :
    (twoLayerLift G₀ G₁ D).Adj (.inl x) (.inr y) ↔ x = y ∧ x ∈ D :=
  Iff.rfl

@[simp] theorem twoLayerLift_adj_inr_inl
    (G₀ G₁ : SimpleGraph V) (D : Set V) (x y : V) :
    (twoLayerLift G₀ G₁ D).Adj (.inr x) (.inl y) ↔ x = y ∧ y ∈ D :=
  Iff.rfl

instance instDecidableRelTwoLayerLift [DecidableEq V]
    {G₀ G₁ : SimpleGraph V} [DecidableRel G₀.Adj] [DecidableRel G₁.Adj]
    {D : Set V} [DecidablePred (· ∈ D)] :
    DecidableRel (twoLayerLift G₀ G₁ D).Adj := by
  intro x y
  cases x <;> cases y <;> simp <;> infer_instance

/-- Lifting preserves a square-closing witness in the left layer. -/
theorem SquareWitness.inl {G₀ G₁ : SimpleGraph V} {D : Set V} {x y : V}
    (h : SquareWitness G₀ x y) :
    SquareWitness (twoLayerLift G₀ G₁ D) (.inl x) (.inl y) := by
  obtain ⟨a, b, hxb, hay, hxa, hab, hby⟩ := h
  exact ⟨.inl a, .inl b, by simpa, by simpa,
    by simpa, by simpa, by simpa⟩

/-- Lifting preserves a square-closing witness in the right layer. -/
theorem SquareWitness.inr {G₀ G₁ : SimpleGraph V} {D : Set V} {x y : V}
    (h : SquareWitness G₁ x y) :
    SquareWitness (twoLayerLift G₀ G₁ D) (.inr x) (.inr y) := by
  obtain ⟨a, b, hxb, hay, hxa, hab, hby⟩ := h
  exact ⟨.inr a, .inr b, by simpa, by simpa,
    by simpa, by simpa, by simpa⟩

/-- A common neighbor across the two layers supplies the mixed square which
closes an omitted vertical edge. -/
theorem vertical_squareWitness {G₀ G₁ : SimpleGraph V} {D : Set V} {u v : V}
    (huD : u ∈ D) (h₀ : G₀.Adj u v) (h₁ : G₁.Adj u v) :
    SquareWitness (twoLayerLift G₀ G₁ D) (.inl v) (.inr v) := by
  refine ⟨.inl u, .inr u, ?_, ?_, ?_, ?_, ?_⟩
  · simp
  · simp
  · simpa [adj_comm] using h₀
  · simpa using huD
  · simpa using h₁

/-- The lift is square-free when each horizontal layer is square-free and
`D` is independent in the intersection graph. -/
theorem squareFree_twoLayerLift {G₀ G₁ : SimpleGraph V} {D : Set V}
    (hfree₀ : SquareFree G₀) (hfree₁ : SquareFree G₁)
    (hind : (G₀ ⊓ G₁).IsIndepSet D) :
    SquareFree (twoLayerLift G₀ G₁ D) := by
  rw [SimpleGraph.isIndepSet_iff] at hind
  unfold SquareFree at hfree₀ hfree₁ ⊢
  intro x y hxy hsq
  obtain ⟨a, b, hxb, hay, hxa, hab, hby⟩ := hsq
  cases x <;> cases y <;> cases a <;> cases b
  all_goals try simp_all
  all_goals first
    | exact hfree₀ hxy ⟨_, _, hxb, hay, hxa, hab, hby⟩
    | exact hfree₁ hxy ⟨_, _, hxb, hay, hxa, hab, hby⟩
    | exact (hind (by simpa [hxa.1] using hxa.2) hby.2
        (G₀.ne_of_adj hxy) hxy) hab
    | exact (hind (by simpa [hxy.1] using hxy.2)
        (by simpa [hab.1] using hab.2) (G₀.ne_of_adj hxa) hxa)
        (by simpa [adj_comm] using hby)
    | exact (hind hxy.2 hab.2 (G₁.ne_of_adj hxa)
        (by simpa [adj_comm] using hby)) hxa
    | exact (hind hxa.2 (by simpa [hby.1] using hby.2)
        (G₀.ne_of_adj hab) hab) hxy

/-- The two-layer lift lies inside the corresponding two-layer host whenever
both horizontal graphs lie inside the base host. -/
theorem twoLayerLift_le_host {G₀ G₁ H : SimpleGraph V} {D : Set V}
    (h₀ : G₀ ≤ H) (h₁ : G₁ ≤ H) :
    twoLayerLift G₀ G₁ D ≤ twoLayerLift H H Set.univ := by
  intro x y hxy
  cases x <;> cases y <;> simp_all
  all_goals first | exact h₀ hxy | exact h₁ hxy

/-- Reviewed two-layer product-lift theorem.  If two square-saturated graphs
share an independent dominating set in their intersection graph, placing them
in two layers and adding the corresponding vertical matching produces a
square-saturated graph in the two-layer host. -/
theorem twoLayer_productLift_squareSaturated
    {G₀ G₁ H : SimpleGraph V} {D : Set V}
    (hsat₀ : SquareSaturatedIn G₀ H)
    (hsat₁ : SquareSaturatedIn G₁ H)
    (hind : (G₀ ⊓ G₁).IsIndepSet D)
    (hdom : Dominates (G₀ ⊓ G₁) D) :
    SquareSaturatedIn (twoLayerLift G₀ G₁ D)
      (twoLayerLift H H Set.univ) := by
  refine ⟨twoLayerLift_le_host hsat₀.le_host hsat₁.le_host,
    squareFree_twoLayerLift hsat₀.squareFree hsat₁.squareFree hind, ?_⟩
  intro x y hhost hmissing
  cases x with
  | inl x =>
      cases y with
      | inl y =>
          exact (hsat₀.closes_omitted (by simpa using hhost)
            (by simpa using hmissing)).inl
      | inr y =>
          have hhost' : x = y ∧ x ∈ (Set.univ : Set V) := by
            simpa using hhost
          have hxy : x = y := hhost'.1
          subst y
          have hxD : x ∉ D := by
            intro hx
            exact hmissing (by simp [hx])
          obtain ⟨u, huD, hu⟩ := hdom hxD
          exact vertical_squareWitness huD hu.1 hu.2
  | inr x =>
      cases y with
      | inl y =>
          have hhost' : x = y ∧ y ∈ (Set.univ : Set V) := by
            simpa using hhost
          have hxy : x = y := hhost'.1
          subst y
          have hxD : x ∉ D := by
            intro hx
            exact hmissing (by simp [hx])
          obtain ⟨u, huD, hu⟩ := hdom hxD
          exact (vertical_squareWitness huD hu.1 hu.2).symm
      | inr y =>
          exact (hsat₁.closes_omitted (by simpa using hhost)
            (by simpa using hmissing)).inr

/-- Original one-base-graph form of the product lift. -/
theorem productLift_squareSaturated
    {G H : SimpleGraph V} {D : Set V}
    (hsat : SquareSaturatedIn G H)
    (hind : G.IsIndepSet D) (hdom : Dominates G D) :
    SquareSaturatedIn (twoLayerLift G G D)
      (twoLayerLift H H Set.univ) := by
  apply twoLayer_productLift_squareSaturated hsat hsat
  · simpa using hind
  · simpa using hdom

/-- The sum presentation used for the two layers is canonically equivalent to
the usual product with a Boolean coordinate. -/
def sumEquivProdBool : Sum V V ≃ V × Bool where
  toFun
    | .inl v => (v, false)
    | .inr v => (v, true)
  invFun
    | (v, false) => .inl v
    | (v, true) => .inr v
  left_inv x := by cases x <;> rfl
  right_inv x := by obtain ⟨v, b⟩ := x; cases b <;> rfl

/-- The two-layer host is exactly Mathlib's Cartesian/box product of the base
host with the two-vertex complete graph. -/
def twoLayerHostIso (H : SimpleGraph V) :
    twoLayerLift H H Set.univ ≃g H □ (⊤ : SimpleGraph Bool) where
  toEquiv := sumEquivProdBool
  map_rel_iff' := by
    rintro (x | x) (y | y) <;> simp [sumEquivProdBool]

/-- The degree in the left layer is the horizontal degree plus the indicator
of membership in the vertical matching set. -/
theorem degree_twoLayerLift_inl [Fintype V] [DecidableEq V]
    (G₀ G₁ : SimpleGraph V) [DecidableRel G₀.Adj] [DecidableRel G₁.Adj]
    (D : Set V) [DecidablePred (· ∈ D)] (v : V) :
    (twoLayerLift G₀ G₁ D).degree (.inl v) =
      G₀.degree v + if v ∈ D then 1 else 0 := by
  classical
  unfold SimpleGraph.degree
  rw [SimpleGraph.neighborFinset_eq_filter,
    SimpleGraph.neighborFinset_eq_filter]
  rw [Finset.card_filter, Finset.card_filter]
  simp [Fintype.sum_sum_type, twoLayerLift]
  have hcard : (∑ x : V, if G₀.Adj v x then 1 else 0) =
      (Finset.univ.filter fun x : V => G₀.Adj v x).card := by
    exact (Finset.card_filter (fun x : V => G₀.Adj v x) Finset.univ).symm
  have hcross : (∑ x : V, if v = x ∧ v ∈ D then 1 else 0) =
      if v ∈ D then 1 else 0 := by
    calc
      _ = ∑ x : V, if v = x then (if v ∈ D then 1 else 0) else 0 := by
        apply Finset.sum_congr rfl
        intro x _
        by_cases h : v = x <;> simp [h]
      _ = _ := Fintype.sum_ite_eq v _
  exact congrArg₂ Nat.add hcard hcross

/-- Right-layer analogue of `degree_twoLayerLift_inl`. -/
theorem degree_twoLayerLift_inr [Fintype V] [DecidableEq V]
    (G₀ G₁ : SimpleGraph V) [DecidableRel G₀.Adj] [DecidableRel G₁.Adj]
    (D : Set V) [DecidablePred (· ∈ D)] (v : V) :
    (twoLayerLift G₀ G₁ D).degree (.inr v) =
      G₁.degree v + if v ∈ D then 1 else 0 := by
  classical
  unfold SimpleGraph.degree
  rw [SimpleGraph.neighborFinset_eq_filter,
    SimpleGraph.neighborFinset_eq_filter]
  rw [Finset.card_filter, Finset.card_filter]
  simp [Fintype.sum_sum_type, twoLayerLift]
  have hcard : (∑ x : V, if G₁.Adj v x then 1 else 0) =
      (Finset.univ.filter fun x : V => G₁.Adj v x).card := by
    exact (Finset.card_filter (fun x : V => G₁.Adj v x) Finset.univ).symm
  have hcross : (∑ x : V, if v = x ∧ x ∈ D then 1 else 0) =
      if v ∈ D then 1 else 0 := by
    calc
      _ = ∑ x : V, if v = x then (if x ∈ D then 1 else 0) else 0 := by
        apply Finset.sum_congr rfl
        intro x _
        by_cases h : v = x <;> simp [h]
      _ = _ := Fintype.sum_ite_eq v _
  exact (congrArg₂ Nat.add hcross hcard).trans (Nat.add_comm _ _)

/-- Exact edge budget of the generalized two-layer lift.  This is the
reviewed formula `|E(G₀)| + |E(G₁)| + |D|`, derived from Mathlib's
handshaking lemma rather than from a custom edge representation. -/
theorem card_edgeFinset_twoLayerLift [Fintype V] [DecidableEq V]
    (G₀ G₁ : SimpleGraph V) [DecidableRel G₀.Adj] [DecidableRel G₁.Adj]
    (D : Set V) [DecidablePred (· ∈ D)] :
    (twoLayerLift G₀ G₁ D).edgeFinset.card =
      G₀.edgeFinset.card + G₁.edgeFinset.card + D.toFinset.card := by
  classical
  have hindicator : (∑ v : V, if v ∈ D then 1 else 0) =
      D.toFinset.card := by
    have hDfin : D.toFinset = Finset.univ.filter fun v : V => v ∈ D := by
      ext v
      simp
    rw [hDfin, Finset.card_filter]
  have hdegrees : ∑ x : Sum V V, (twoLayerLift G₀ G₁ D).degree x =
      2 * (G₀.edgeFinset.card + G₁.edgeFinset.card + D.toFinset.card) := by
    rw [Fintype.sum_sum_type]
    simp_rw [degree_twoLayerLift_inl, degree_twoLayerLift_inr]
    simp only [Finset.sum_add_distrib]
    rw [G₀.sum_degrees_eq_twice_card_edges,
      G₁.sum_degrees_eq_twice_card_edges, hindicator]
    omega
  rw [(twoLayerLift G₀ G₁ D).sum_degrees_eq_twice_card_edges] at hdegrees
  omega

/-- Edge budget in the original one-base-graph product lift. -/
theorem card_edgeFinset_productLift [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (D : Set V) [DecidablePred (· ∈ D)] :
    (twoLayerLift G G D).edgeFinset.card =
      2 * G.edgeFinset.card + D.toFinset.card := by
  rw [card_edgeFinset_twoLayerLift]
  omega

/-- The arithmetic specialization used in the reviewed 432-edge `Q₈`
construction.  The concrete 208-edge base graph and its 16-vertex independent
dominating set remain external data. -/
theorem edge_budget_208_16 [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (D : Set V) [DecidablePred (· ∈ D)]
    (hG : G.edgeFinset.card = 208) (hD : D.toFinset.card = 16) :
    (twoLayerLift G G D).edgeFinset.card = 432 := by
  rw [card_edgeFinset_productLift, hG, hD]

#print axioms SquareWitness.symm
#print axioms squareFree_twoLayerLift
#print axioms twoLayerLift_le_host
#print axioms twoLayer_productLift_squareSaturated
#print axioms productLift_squareSaturated
#print axioms twoLayerHostIso
#print axioms degree_twoLayerLift_inl
#print axioms degree_twoLayerLift_inr
#print axioms card_edgeFinset_twoLayerLift
#print axioms card_edgeFinset_productLift
#print axioms edge_budget_208_16

end HypercubeSquareLift
