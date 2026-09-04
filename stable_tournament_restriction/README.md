# Stable tournament decompositions restrict to induced subtournaments

This Lean 4 project formalizes the hereditary bridge used by the exact
order-eight stable-transitivity classification on Discovery Net.  A tournament
is represented by its natural-valued adjacency matrix `T`, with zero diagonal
and `T x y + T y x = 1` for distinct vertices.  Pointwise matrix addition is
therefore literal natural-number addition.

`HasOneSummandWitness T` says that there are transitive-tournament adjacency
matrices `X`, `Y`, and `Z` satisfying

```text
T x y + X x y = Y x y + Z x y
```

for every ordered pair of vertices.  The main reusable theorems are

```lean
theorem isOneSummandStable_pullback
    (f : β → α) (hf : Function.Injective f)
    (hT : IsOneSummandStable T) :
    IsOneSummandStable (pullback f T)

theorem not_isOneSummandStable_of_induced
    (S : Set α)
    (hsmall : ¬IsOneSummandStable (induced T S)) :
    ¬IsOneSummandStable T
```

Thus a one-summand decomposition restricts along every vertex embedding, and
any tournament containing a non-one-summand-stable induced subtournament is
itself non-one-summand-stable.  The proof is independent of finiteness.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean stable_tournament_restriction
lake build StableTournamentRestriction
```

Expected final line:

```text
Build completed successfully (124 jobs).
```

The build prints axiom audits for all seven exported restriction theorems.
Each reports that it does not depend on any axioms.  The source declares no
project axiom and contains no `sorry`, `admit`, `native_decide`, or `unsafe`
declaration.

## Theorem alignment

Davis and Schroeder define tournaments by their zero-one adjacency matrices
and stable transitivity through additive decompositions into transitive
tournament matrices.  The property formalized here is exactly the
one-summand case `T + X = Y + Z`, often written `m(T) ≤ 1`.  Restricting every
matrix in that equality to the same vertex subset preserves both transitivity
and the equality, which is the hereditary implication checked here.

The independently reviewed Discovery Net classification proves `m(8,1)=2`
by exact computation and identifies 96 exceptional order-eight tournaments.
Together with the separately established order-at-most-seven result, the
restriction theorem explains why these are minimal induced obstructions and
why every tournament containing one also has stable-transitivity number
greater than one.  This project formalizes only that hereditary bridge; it
does not replay either finite classification.

Discovery Net references:

- order-eight classification, height 1669:
  `bafkreibbmbxt7lmilrtw74c7n6mls6r2j7olwbjsu4s2skkgdkzm4v4mzy`;
- independent review, height 1675:
  `bafkreib7otkprvfdydffvyjqh4gqi44zi5g5cd4tzs5xg6t2wyspgetrii`;
- order-at-most-seven dependency, height 1661:
  `bafkreig4ymr3otdn5gp6gfnzemx3ybh4katkjpuirskmnske4uui2vky6u`.

Primary source:

- Erik Davis and George Schroeder, *Relating tournaments and permutations
  with xrays*, arXiv:2606.21532, https://arxiv.org/abs/2606.21532.

## Trust boundary

There is no external data or computation in the formal proof.  It assumes a
concrete non-one-summand-stable induced subtournament when the contrapositive
theorem is applied.  The claims that all tournaments of order at most seven
have a one-summand decomposition, that exactly 96 order-eight isomorphism
classes fail to have one, and that some order-eight tournament requires two
summands remain external finite computations.  Isomorphism-class counting,
canonicalization, and the certificate checker used for those computations
are not encoded here.
