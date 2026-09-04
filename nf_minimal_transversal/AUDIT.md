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
lake clean nf_minimal_transversal
lake build NFMinimalTransversal
```

completed successfully with 434 jobs.

The `#print axioms` output for

- `avoids_iff_complement_transversal`,
- `diff_diff_of_subset`,
- `maximalAvoider_iff_minimalTransversal_complement`, and
- `nfFacets_eq_complements_minimalTransversals`

listed only `propext`, `Classical.choice`, and `Quot.sound`.

The source was also scanned for `sorry`, `admit`, `native_decide`, `unsafe`,
and project `axiom` declarations; none occur.  The audited source SHA-256 is

```text
69cf5949d4b749b9f790b32dfbaa7d451826e123cc9c07d886c212ceb410d8c0  NFMinimalTransversal.lean
```

## Logical coverage

The proof checks all of the following:

1. avoiding a family is equivalent to its relative complement meeting every
   family member;
2. relative complementation is involutive on subsets of the universe;
3. complement exchanges inclusion-maximal avoiders and inclusion-minimal
   transversals;
4. the resulting equality holds for the entire two families of subsets.

No finiteness or existence assumption is hidden: if either family is empty,
the equality remains literal.  The only semantic bridge left external is the
identification of an NF complex with the avoiding complex of its facet
family, plus any application-specific minimal-transversal classification.
