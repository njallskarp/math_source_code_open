# An explicit transition-closed BHR `{1,2,11}` residual slab

## Result

For every `p,q >= 0`, the multiset

\[
  \{1^{2+p},2^{21+2q},11\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
on `25+p+2q` vertices.  This supplies the first slab below the 22 complete cap
orthants that was not already covered by the transition-aware certificate
audit.

## Explicit four-block family

For `p,q >= 0`, let `P[p,q]` be the concatenation of

```text
(p+1, p+3, ..., p+13+2q),
(p+14+2q, p+16+2q, ..., p+24+2q),
(0,1,...,p, p+2,p+4,...,p+12+2q),
(p+23+2q, p+21+2q, ..., p+15+2q).
```

The seed is therefore

```text
P[0,0] =
(1,3,5,7,9,11,13,14,16,18,20,22,24,0,2,4,6,8,10,12,
 23,21,19,17,15).
```

The four blocks partition `0,...,24+p+2q`: the first and the tail of the
third partition the two parities from `p+1` through `p+13+2q`; the second and
fourth do the same from `p+14+2q` through `p+24+2q`; and the consecutive
prefix of the third block is `0,...,p`.

Inside the consecutive prefix are `p` edges of length 1.  Two more length-1
edges join the first two blocks and join the last vertex `24+p+2q` to 0 in
the cyclic metric.  Every other within-block edge has length 2, with counts

\[
  (6+q)+5+(6+q)+4=21+2q.
\]

The sole remaining join is from `p+12+2q` to `p+23+2q`, of length 11.  Thus
`P[p,q]` realizes exactly the claimed multiset.

Direct gap-insertion calculation also gives

\[
  G_{1,0}(P[p,q])=P[p+1,q],\qquad
  G_{2,p+1}(P[p,q])=P[p,q+1].
\]

Consequently every member is 1-growable at cut 0 and 2-growable at cut
`p+1`, and the two transitions commute.  The displayed formula and edge
count prove the family for all parameters; no finite grid or solver
completeness claim is used for the universal quantifiers.

## Discovery and exact reproduction

The pinned deterministic generator command was

```bash
python3 find_seed.py --counts 2 21 1 --seconds 300
```

using CPython 3.12.12, OR-Tools 9.14.6206, one worker, and random seed 1.  It
returned the displayed seed with selected cuts 0 and 1 after 27.70 seconds.
The solver is only a discovery mechanism.

The standard-library checker is the proof-computation entry point:

```bash
python3 verify_residual_slab.py residual_slab_certificate.json --grid 24
python3 -m unittest -v test_residual_slab.py
```

It reconstructs every path from the formula, verifies its permutation and
cyclic edge-length multiset, checks both growth definitions and recurrences,
and checks commuting squares.  `expected_residual_slab.txt` records the exact
reference output.  Certificate SHA-256 is
`8031d3eda5e24ee5609effe05cd1da7998d944a60f64c677e4251909c4c28d8b`,
and the grid-24 transition-record SHA-256 is
`742283d6593b95da86c4ab22dd18010516e18788969a19d52b8b48648d19fede`.
A large-parameter test independently verifies the order-3025 path at
`(p,q)=(1000,1000)`, and a negative test rejects seed tampering.

## Coverage and trust boundary

Before this result, proved transition-closed regions covered 8,052 of the
pinned source certificate's 9,544 admissible symbolic patterns.  This slab
covers 19 previously residual patterns, including the high sentinels on both
the `a` and `b` coordinates, reducing the conservative residual from 1,492 to
1,473.  This finite count measures coverage of proved regions; it is not a
claim that the remaining patterns are unrealizable.

The theorem trusts exact integer arithmetic, the displayed formula and block
proof, the compact certificate, and CPython executing the definition-level
checker.  It does not trust CP-SAT, solver optimality, the source certificate's
old coordinatewise coverage inference, or the bounded parameter grid as an
induction proof.

Chand and Ollis leave `{1,2,11}` as the possible exception in their
size-three classification (<https://arxiv.org/abs/2202.07733>).  The later
grid-based theorem (<https://arxiv.org/abs/2402.08736>) explicitly excludes
the broad large-order case with `a in {1,2}` and odd third length, so it does
not supply this frontier.  Live support-specific and exact-parameter searches
on 2026-09-03 found no prior formula for this slab.  This is search-relative
novelty, not a priority claim.
