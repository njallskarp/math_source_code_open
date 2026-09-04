# A cyclic solution to HOP(32,6,4)

This directory gives a compact, independently checkable solution to the
Honeymoon Oberwolfach instance with 21 couples and table sizes 32, 6, and 4.
Equivalently, it supplies a semi-uniform one-factorization of `K_42` whose
union of the spouse factor with every other factor has cycle type `(32,6,4)`.

The result advances the exact finite frontier from the published theorem for
all instances through 20 couples. It is one new instance, not a solution of
the general Honeymoon Oberwolfach conjecture and not a classification of all
21-couple types.

## Certificate

Number the couples `0,...,20`; couple `20` is the fixed infinity vertex and
the others are acted on by addition modulo 20. Write `(v,b)` for spouse `b`
in couple `v`. The file `certificate.json` lists the 21 external adjacency
edges in starter matchings `F1` and `F3`.

The third starter required by the odd-order development theorem is determined
as follows. Rotate `F1` by 10, remove

```text
{(0,0),(10,0)} and {(0,1),(10,1)},
```

and insert

```text
{(0,0),(10,1)} and {(0,1),(10,0)}.
```

This is `F2`: the prescribed replacement of the pink/blue difference-10
2-cycle by its two oppositely directed black edges. Develop `F1` and `F2` by
shifts `0,...,9`, and develop `F3` by shifts `0,...,19`. These are the 40
meals.

At every meal the external edges form a perfect matching of the 42 people.
Adding the fixed 21 spouse edges produces cycles of lengths 32, 6, and 4. The
developed external matchings partition all

```text
4 * binomial(21,2) = 840
```

edges between people in distinct couples. Thus every participant sits beside
their spouse at all 40 meals and beside every non-spouse exactly once.

This is also a direct edge-level verification of Proposition 3.5 (the
three-starter construction) in Jerade and Sajna: the half-turn pairing and
the difference-10 replacement are built into `F2`, while exact developed
coverage implies its orbit conditions.

## Reproduction

Requirements: CPython 3.12 or later; only the standard library is used.

Verify the retained certificate directly from the seating definition:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py
diff -u expected_output.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py)
shasum -a 256 -c SHA256SUMS
```

The final two digest lines must be

```text
certificate_sha256=9bf1bce4304692f64ad6acd44d81cdfc4c7d618b340dc72cdaf1ec1f6b7b33a0
developed_schedule_sha256=0ebb07f5aa67030b23d1aa735807f1a7c211fa6a0a0c0972e2790e68f9f398f9
```

The deterministic exploratory search that found the certificate can also be
replayed. Its first output line is byte-for-byte `certificate.json`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 search_starters.py \
  --seed 2026090402 --trials 250 --nodes-per-f1 200000 --progress 0 \
  | sed -n '1p' | diff -u certificate.json -
```

On the reference run the first admissible `F1` occurred at trial 231 and the
complementary-orbit exact-cover search visited 2,754 nodes. This search count
is discovery provenance only; the direct verifier does not trust the search.

## Method and trust boundary

Contract each spouse edge. A valid alternating factor is precisely a perfect
matching of the two labelled endpoints at every contracted couple. An edge
joining endpoint bits `(a,b)` records one of the four parallel coloured/
oriented edges in the standard `4K_21` formulation. The search samples an
`F1` of contracted cycle type `[16,3,2]` with 19 distinct ordinary cyclic
edge orbits and the required pink/blue difference-10 2-cycle. It then solves
an exact-cover problem choosing one edge from each of the 21 complementary
orbits for `F3`.

The existence theorem depends only on the 63 stored edges and the transparent
development check. The trust boundary is JSON decoding, the standard-library
Python checker, exact integer/set operations, the published starter theorem
or the equivalent direct scheduling argument above, CPython, and ordinary
runtime/hardware behavior. There is no SAT/MILP solver, floating point,
randomness, external data, or omitted generated certificate in the proof.

## Literature and novelty scope

- D. Lepine and M. Sajna, *On the Honeymoon Oberwolfach Problem*, Journal of
  Combinatorial Designs 27 (2019), 420--447,
  <https://doi.org/10.1002/jcd.21656>.
- M. R. Jerade and M. Sajna, *The Honeymoon Oberwolfach Problem: small cases*,
  Journal of Combinatorial Mathematics and Combinatorial Computing 128
  (2026), 97--118; preprint <https://arxiv.org/abs/2407.00204>. Their theorem
  covers all instances with at most 20 couples and supplies the starter
  formalism used here.

G. Rinaldi's 2024 paper *The Oberwolfach problem with loving couples*
(<https://doi.org/10.1002/jcd.21946>) includes HOP constructions such as the
family with one arbitrary even table and all remaining tables of size 4; it
therefore covers HOP(34,4,4), but not the mixed table sizes `(32,6,4)`.
Targeted searches of these primary sources, later generalized-HOP preprints,
and the committed Discovery Net graph found no HOP(32,6,4) solution. The
novelty claim is search-relative and makes no historical-priority claim.
