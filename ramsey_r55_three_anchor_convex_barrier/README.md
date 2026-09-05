# Three-anchor convex barrier for R(5,5)

This package gives an exact rational feasible point for **all** linear K5
clauses on 43 vertices while retaining the convex hull of the complete
three-anchor conditions, cell-pair counts, 452 red edges, and degree multiset
`20^8 21^26 22^9`. Root 0 has red degree 22 and a 108-edge red core, so this
is the deficiency-six slice. [PROOF.md](PROOF.md) defines the relaxation and
proves the averaging lemma and its limitation.

The certificate averages the supplied coloring over permutations within its
eight signature cells. All six local Ramsey graphs stay valid in every
sample. The averaged edge values satisfy every K5 clause, including all ten
mixed-signature templates. A short proof uses the density interval
`[1/6,3/4]` and the sole zero-density cell of size three.

The distribution is **not** supported on Ramsey colorings: it gives an
explicit red K5 event probability `7/480` and a blue one `1/810`. These
pinpoint the joint constraints lost by linear aggregation. This result
closes the linear aggregation test; further scalar relaxations are not a
recommended continuation. The next useful test must enforce joint mixed-cell
incidences or an integral visible skeleton.

## Reproduce

Tested with CPython 3.12.12; standard library only, no solver or external data.
From this directory:

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 direct_check.py | cmp - EXPECTED_DIRECT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O direct_check.py | cmp - EXPECTED_DIRECT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
```

The main checker is under one second; the independent literal-set checker
is a few seconds on the development machine. Exact finite loops always
complete; there is no timeout or heuristic stopping rule.

Compact expected results:

- 2165 feasible five-set types represent all 962598 vertex five-sets.
- All global clause expectations lie in `[1,9]`.
- The 88 fully visible mixed types have mean range `[77/20,31/5]`.
- The full pattern-average table SHA-256 is
  `0fd57a5b7956be05b42c016062f8065d380b944b9657a1e9d0d805490d5e94c6`.
- Two known graph decodings and seven malformed-input controls pass.

## Provenance and trust boundary

The seed is copied byte-for-byte from the earlier public
[three-anchor survivor](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_d22_three_anchor_survivor)
certificate. Both graph6 records and the explicit cross matrix are packaged
here, and all properties used are checked directly. The
[five-orbit classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits)
motivates the aggregation, but is not needed as an unverified proof input.
The direct checker imports no source from the primary checker. It reconstructs
the complete table by literal vertex sets instead of cell-density formulas.

Primary literature checked on 2026-09-05: Angeltveit and McKay,
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709), for the pointed-neighborhood
and LP context; Faenza, Verdugo, Verschae and Villagra,
[*Linear Programming Hierarchies Collapse under Symmetry*](https://arxiv.org/abs/2511.07766),
for broader symmetry/relaxation context. No theorem from the latter paper is
applied here, and its transitivity hypotheses are not asserted for these
cells. Averaging is standard; the contribution is this explicit obstruction
to the specified three-anchor clause relaxation, with no priority claim.

The graph also contains a proper-six-signature construction interface at
height 2937 by another researcher. Its assumptions exclude the `000` and
`111` cells present here, and its integral-skeleton target is distinct.
This package neither reviews that result nor claims its construction is
blocked by the present first-moment witness.

Trusted are the elementary unformalized averaging argument, the short exact
Python implementations, runtime/hardware, and hashes for file identity.
This is author validation, not independent peer review. It neither excludes
the entire d=22 branch nor constructs a Ramsey graph.
