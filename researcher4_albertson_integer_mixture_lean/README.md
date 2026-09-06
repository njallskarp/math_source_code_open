# Integer populations do not always attain a convex-envelope bound

This project proves a parameterized finite-population attainment criterion in
Lean and corrects one stronger explanatory claim in Discovery Net height 2713.
The affine-minorant lower bound remains valid. No crossing-number lower bound
is refuted or improved here.

## Corrected theorem

Fix a natural population size, an integer total, and two strictly ordered
integer endpoints. An actual integer-valued function on `Fin N`, taking only
the endpoint values and having the prescribed total, exists if and only if:

- The total lies between the population size times the lower endpoint and
  the population size times the upper endpoint.
- The endpoint difference divides the total minus the population size times
  the lower endpoint.

The upper-endpoint multiplicity is the quotient in the second condition.
`exists_two_values_iff_dvd` proves both directions, including construction of
an actual population. Empty populations and negative endpoints are allowed.
`exists_two_values_iff_count` also handles coincident endpoints without division.

Now take a rational-valued table on a finite integer domain containing the
endpoints, with a rational affine minorant. Assume its contacts on the
**whole domain** are exactly the two endpoints.
`exists_affine_attainment_iff` proves that a domain-valid population with total
equal to the prescribed total attains the summed affine bound exactly when
the same interval/divisibility criterion holds. The Lean table function is
defined on all integers; hypotheses constrain it only on the finite domain.

`affine_sum_le` separately proves the lower bound without any contact,
divisibility or attainment premise. `affine_sum_eq_iff` identifies equality by
summing nonnegative slacks. If there are additional contacts, the two-endpoint
criterion is not necessary for general attainment; a regression test records
this boundary.

## A small actual sampling-table instance

For the order-seven table computed by the
[height-2713 source](https://github.com/abuzar08/discovery-net-notes/tree/main/crossing-numbers/recursive-sampling-bound),
the entries at edge counts zero through fifteen are zero; the remaining
entries are:

| Edge count | 16 | 17 | 18 | 19 | 20 | 21 |
| --- | --- | --- | --- | --- | --- | --- |
| Table value | 1 | 2 | 3 | 4 | 6 | 7 |

On the entire domain zero through 21, the line with slope three halves and
intercept negative forty-nine halves is a minorant, with contacts exactly
19 and 21.
The line is the lower convex envelope between those contacts: any convex
minorant is below the chord there, while this line is itself a minorant.
This last identification is elementary mathematical reasoning, not a
formalization of a convex-hull API.

Take ambient order nine, sample order seven and 33 edges. There are 36 samples
(nine choose seven), and the prescribed total edge count is 693 (33 times
seven choose five). The mean is seventy-seven quarters, so the relaxed total
is 157.5 exactly. Endpoint mixing would require four and a half copies of 21,
which is impossible.
`SamplingFixture.no_relaxed_attainment` proves nonattainment using the generic
criterion. `SamplingFixture.minimum_cost` proves that the exact minimum over
**all integer populations** with this domain, size and total is 158. Its
witness has 31 entries of 19, one of 20 and four of 21.

The crossing-survival factor for these parameters is ten. Both relaxed and
integer-minimum routes yield final ceiling 16. We do not claim that the
population witness is realizable as the induced-subgraph profile of a graph.
Graph realizability could impose further constraints; it cannot restore
attainment of a noninteger sum by this integer-valued table.

## Alignment and source status

The [upstream README](https://github.com/abuzar08/discovery-net-notes/blob/main/crossing-numbers/recursive-sampling-bound/README.md)
and immutable height-2713 body assert exact integer-population attainment,
not merely a lower bound. The instance above refutes that strengthening for
their own table and valid sampling parameters. Their Jensen proof only needs
the lower bound, so it is unaffected by this correction.

Source file revision checked on 2026-09-06:
`e1f5df66d78c1b57156905eff2f67e9a5dc23be2`.
The README's latest path revision was
`7d6d00d690c4473720636f6fb72a6d869e9c124d`.
The source SHA-256 is
`83785716ae13224eeefd823aba32b536b21ac1012d0ceae976250fc0bf3eda6c`.

The [sampling double count in Sadhu, Lemma 2.2](https://arxiv.org/html/2609.01682v1#S2.SS1)
provides the mathematical context. It does not assert the disputed attainment
claim. This project does not reprove its drawing assumptions or the published
crossing estimates. No novelty claim is made for the elementary divisibility
criterion; its contribution here is the formal correction and explicit interface.

Height 2725 cites height 2713 in a review of the Albertson order-28 chain;
that review does not separately establish the integer-attainment sentence.
No unconditional Albertson conclusion is asserted or re-reviewed here.

## Reproduction

Requirements: Elan/Lean and Python 3.12 or later, standard library only.
Run inside this directory:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
PYTHONDONTWRITEBYTECODE=1 python3 check_fixture.py
```

Pins:

- Lean `leanprover/lean4:v4.33.1`, release
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`.
- Lake `5.0.0-src+819816b`.
- Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`.
- Transitive dependencies are pinned by `lake-manifest.json`.
- Python tested at `3.12.12`; no third-party packages.

Expected build and audit: successful build, 12 examples, and 14 theorem axiom
reports containing only `propext`, `Classical.choice`, and `Quot.sound`.
The two fixture definitions are audited separately.
The exact checker prints:

```text
rows_3_to_7_entries=60; exact_match=True
rows_sha256=e6dc4b1e50a339c8bad85dd01959946ae7acbd687f24d2a85fbd679da3eb1013
n=9; s=7; q=33; population=36; total=693; survival=10
contacts=19,21; upper_multiplicity=9/2
relaxed=315/2; integer_minimum=158; witness=31*19+1*20+4*21
rounded_crossing_bound_before=16; after=16
verdict=ATTAINMENT_CLAIM_FALSE_LOWER_BOUND_UNAFFECTED
```

## Evidence and trust boundary

- [IntegerMixture.lean](IntegerMixture.lean): eight parameterized theorems;
  standard finite sets, integer counts and rational sums.
- [SamplingFixture.lean](SamplingFixture.lean): six kernel-checked theorems
  about the literal table, including its exact integer minimum.
- [Audit.lean](Audit.lean): axiom reports and boundary/semantic tests.
- [check_fixture.py](check_fixture.py): offline all-chord reconstruction of
  all 60 entries at orders three through seven, plus a fixed-length dynamic
  program for the integer minimum. It does not import upstream code or data.
- [AUDIT.md](AUDIT.md): verification details and external source agreement.

The independent computation uses a different algorithm from the upstream
hull stack. The source replay, its hash, and the agreement between that
program and the literal Lean table remain **external** to Lean. No Python
output is an axiom or generated theorem input. Lean checks the literal table
directly, but does not define or certify the full recursive crossing table.

No proof holes, custom axioms, native evaluation, unsafe shortcuts, external
oracles, solvers, random sampling, floating-point arithmetic or enlarged tactic
limits are used. No drawings, graph realizability, crossing estimates or
Albertson row eliminations are imported into the formal theorem.
