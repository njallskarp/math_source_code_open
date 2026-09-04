# Formal audit

Audit date: 2026-09-04.

## Pinned environment

- Lean: `v4.33.1`, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Mathlib: `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

The exact transitive dependency revisions are recorded in
`lake-manifest.json`.

## Clean build

After `lake update` and `lake exe cache get`:

```sh
lake clean stable_tournament_restriction
lake build StableTournamentRestriction
```

completed successfully with 124 jobs.

The `#print axioms` output for

- `isTournament_pullback`,
- `isTransitiveTournament_pullback`,
- `hasOneSummandWitness_pullback`,
- `isOneSummandStable_pullback`,
- `not_isOneSummandStable_of_pullback`,
- `isOneSummandStable_induced`, and
- `not_isOneSummandStable_of_induced`

reported that every theorem depends on no axioms.  The source was also
scanned for `sorry`, `admit`, `native_decide`, `unsafe`, and project `axiom`
declarations; none occur.  The audited source SHA-256 is

```text
e003f5989b84ce33fc015ef8b540e901e2009c8b4e3cf20db73962676f80f4da  StableTournamentRestriction.lean
```

## Logical coverage

The proof checks all of the following:

1. pullback along an injective vertex map preserves the tournament axioms;
2. the same pullback preserves the transitivity shortcut condition;
3. pulling back each of `T`, `X`, `Y`, and `Z` preserves the pointwise
   equality `T + X = Y + Z`;
4. one-summand stable transitivity is consequently induced-hereditary;
5. contrapositively, an induced obstruction remains an obstruction in every
   extension.

The statement is generic in the vertex types and uses no finiteness or
decidability instance.  The finite order-eight classification and its 96
isomorphism-class count are deliberately outside the formal trust boundary.
