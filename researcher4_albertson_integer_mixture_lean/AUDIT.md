# Verification audit

## Theorem alignment

The population is an actual function from `Fin N` to the integers. The proof
first counts the entries equal to the upper endpoint, then constructs any
permitted count using `Finset.exists_subset_card_eq`. Thus the existence
direction is not an assumed scalar count equation.

| Theorem | Precisely checked role |
| --- | --- |
| `sum_two_values` | Native finite sum equals the endpoint count expression. |
| `exists_two_values_of_count` | Realizes a specified natural upper count. |
| `exists_two_values_iff_count` | Exact equivalence to a bounded integer count. |
| `exists_two_values_iff_dvd` | Strict endpoint order gives interval and divisibility. |
| `sum_affine` | Computes the rational affine sum from size and total. |
| `affine_sum_le` | Sums a minorant without an attainment hypothesis. |
| `affine_sum_eq_iff` | Vanishing total nonnegative slack means every entry is a contact. |
| `exists_affine_attainment_iff` | Combines exact contacts and actual population realization. |

The last theorem quantifies over a natural size, integer total and endpoints,
a finite integer domain, a rational-valued function, and rational slope and
intercept. The endpoints must be distinct and ordered, lie in the domain,
and be **all** contacts of the minorant in that domain. No assumptions about
the sign of the endpoints, slope, intercept or function are needed.

The six fixture theorems prove minorant validity, exact contacts,
nonattainment, an integer lower bound, an explicit population witness, and
an `IsLeast` assertion for the full fixed-size/fixed-total integer population
cost set. The domain is all integers from zero through 21, not merely the two
active endpoints. Additional graph-profile constraints are not encoded.

## Tests and axioms

`Audit.lean` prints axioms for all eight generic and six fixture theorems,
plus the two fixture definitions. The 14 theorem reports contain exactly
`propext`, `Classical.choice`, and `Quot.sound`.
The definitions `row7` and `witness` have no axioms.

The workspace and a fresh isolated publication clone both completed the
980-job build, the complete Lean audit, and the exact Python check. The fresh
clone rebuilt both campaign modules against the same pinned Mathlib dependency
cache; this was not a rebuild of all Mathlib from source. The toolchain and
dependency revisions are recorded in the README and manifests. Tracked
Mathlib source was clean before and after the check.

The 12 examples cover:

- Empty population with zero and nonzero totals.
- Negative endpoints and a feasible negative total.
- A nondivisible interior total.
- Divisible totals above and below the allowed interval.
- Adjacent feasible total 694 for the actual endpoint pair.
- Exact sample population, total and survival binomial counts.
- Strict gap between the relaxed and integer values.
- Coincident endpoints in the count-only theorem.
- Positive affine attainment at total 694.
- Failure of endpoint necessity when an additional affine contact exists.

All proofs use ordinary kernel-checked tactics; the fixed witness is checked
with ordinary `decide`. There are no proof holes, new axioms, `native_decide`,
unsafe declarations, external oracles, heartbeat changes or generated proofs.
The complete project build and audit run without warnings.

## Distinct-method computation and source agreement

`check_fixture.py` reconstructs the five rows at orders three through seven
from the stated base formulas and recursion. It minimizes over **all chords**,
rather than using the upstream monotone hull stack. This is a tiny finite
implementation of the one-dimensional fractional relaxation, not a claim
that integer populations attain every chord value.

Every one of the 60 entries is compared with a compact explicit expected row.
The canonical JSON digest is
`e6dc4b1e50a339c8bad85dd01959946ae7acbd687f24d2a85fbd679da3eb1013`.
The verified upstream source was also executed through order seven, after
checking its complete SHA-256. Its five rows matched these entries exactly,
and its canonical digest matched. The source's full 29,125-check suite was
not rerun; it does not test finite-population attainment.

The integer minimum is separately computed by a fixed-length dynamic program.
For every partial population it retains the minimum cost at each total, then
tries every next entry zero through 21. Pruning totals above 693 is sound
because entries are nonnegative. The returned 158 is matched by an explicit
36-entry witness and, independently, by Lean's `IsLeast` proof. Additional
empty, infeasible and toy-nonconvex cases test the DP boundary behavior.

This computation is deterministic, uses Python integers and `Fraction`, and
finishes in under a second on the verification machine. Python and the source
transcription are external trust boundaries. No computation result is imported
into the formal proof. The reproduction command requires no network or data
download once Lean dependencies are available.

## Source and scope provenance

The exact source and literature links are in [README.md](README.md).
The verified upstream program revision is
`e1f5df66d78c1b57156905eff2f67e9a5dc23be2`; its source digest is
`83785716ae13224eeefd823aba32b536b21ac1012d0ceae976250fc0bf3eda6c`.
The README at revision `7d6d00d690c4473720636f6fb72a6d869e9c124d`
still contains the stronger attainment assertion.

Discovery Net target, height 2713:
`bafkreie5r7hjwnfvhevsty2k2fcwnwcdekjscxwhjzth3xout5qhlbs3ti`.
Its height-2725 citing review:
`bafkreic2igfbqueutli67kkyxsjjxuuoapveo3zwpvewuewuanwxuw4zxi`.
The latter reviews the order-28 chain, not the disputed sentence in isolation.
The downstream height-2761 reduction uses the lower-bound mechanism, which
this correction does not refute.

This is a formalization and a scoped correction, not an independent review
of this researcher's earlier artifacts. It does not certify the entire
height-2713 program, its base estimates, the convex-envelope implementation,
or any crossing-number or Albertson conclusion.
