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
lake clean av123_fixed_point_location
lake build Av123FixedPointLocation
```

completed successfully with 769 jobs.

The `#print axioms` output for

- `maps_before_first_above`,
- `maps_after_second_below`,
- `first_fixed_cardinality_bound`,
- `second_fixed_cardinality_bound`,
- `distance_two_fixed_point_bounds`,
- `even_distance_two_fixed_point_locations`, and
- `odd_distance_two_fixed_point_locations`

listed only subsets of `propext`, `Classical.choice`, and `Quot.sound`.
The source was scanned for `sorry`, `admit`, `native_decide`, `unsafe`, and
project `axiom` declarations; none occur.  The audited source SHA-256 is

```text
2ff767a7e5b28f7bff99d85be420cff65846415990b5025597bc14e5a4677251  Av123FixedPointLocation.lean
```

## Logical coverage

The proof checks all of the following:

1. a value below the first fixed value at an earlier position would form a
   `123` with the two fixed points;
2. dually, a value above the second fixed value at a later position would
   form a `123`;
3. permutation injectivity excludes the two fixed values from those image
   bands;
4. the cardinalities of `Finset.Iio` and `Finset.Ioi`, after erasing the
   other fixed point, yield the two location inequalities;
5. for distance two, Presburger arithmetic turns those inequalities into
   the exact even and odd location lists.

The finite permutation, order intervals, image cardinalities, and
injectivity are Mathlib definitions and lemmas.  Only the classical-pattern
avoidance predicate is defined locally, directly from its three-index
meaning.
