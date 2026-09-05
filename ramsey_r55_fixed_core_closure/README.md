# Exact closure of the height-2951 fixed-core profile

Every completion of the explicitly specified fixed cores and anchor incidences,
with the degree intervals and cell counts below, contains a monochromatic
\(K_5\). This is a computer-assisted **conditional family exclusion**, not an
exclusion of all \(d=22\) cores, all deficiency-six graphs, or an entire
\(M\)-value. No Ramsey bound is improved.

## Exact family

Vertices are \(0,\ldots,42\). The anchors are \(0,3,9\). In
[PARTIAL.json](PARTIAL.json), `1` means red, `0` blue, `.` free, and `-` a
diagonal entry. All 503 specified pairs are fixed. Exactly 400 pairs remain
free: the cross-edges from \(\{1,\ldots,22\}\setminus\{3,9\}\) to
\(\{23,\ldots,42\}\).

Require red degree 22 at vertex 0, red degree 21 or 22 at vertices 1 through
22, and red degree 20 or 21 at vertices 23 through 42. For each nonanchor,
its three-bit signature records red adjacency to the anchors in that order.
The cell sizes are \((6,4,4,6,5,6,6,3)\). Require the 36 cell-pair red counts
in [PROFILE.json](PROFILE.json), including the eight within-cell counts.
These are explicit restrictions, not a universal Ramsey classification.

The counts imply 452 red edges and degree multiset \(20^8 21^{26}22^9\).
The two fixed cores have 108 red edges on 22 vertices and 100 blue edges on
20 vertices. The seed and profile come from heights 2907 and 2951.

## Proof and validation

[PROOF.md](PROOF.md) gives the graph-to-CNF reduction and explicit counter
extensions. The final formula has 400 primary variables, 13,600 total
variables and 88,433 clauses. It contains all 51,624 distinct undischarged
global \(K_5\) clauses and 112 cardinality blocks, totaling 26,320 counter
clauses. Other clauses are duplicates of valid global prohibitions.

The solver-free [auditor](audit.py) imports neither the producer nor PySAT.
It reconstructs possible monochromatic cliques by bitset intersections,
checks exact global-clause coverage, and independently reconstructs every
threshold-grid counter from the displayed input. Seven malformed formulas
are rejected; 2,304 canonical counter extensions pass exhaustive small tests.
Normal and optimized Python audits and controls agree.

Discovery used complete-column decision diagrams. They are **not premises
of the final proof**: the trimmed trace passes RUP-only replay against the
smaller final formula, without any decision-diagram clause or variable.
The original proof and a fresh source regeneration were each checked against
both the discovery formula and the final formula. This is author validation,
not independent mathematical review or formalization.

## Reproduction

Use CPython 3.12.12 and `python-sat==1.9.dev15` (Glucose 4.2.1). Build
[DRAT-trim](https://github.com/marijnheule/drat-trim) at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` in a separate tool directory.
Pass its executable path below. The supplied work directory must not exist
and must be outside this source directory.

```sh
uv run --no-project --with python-sat==1.9.dev15 python -B run.py \
  --work /tmp/new-r55-fixed-core-proof \
  --drat-trim /path/to/drat-trim
python3 -B audit.py /tmp/new-r55-fixed-core-proof/final.cnf
python3 -B controls.py /tmp/new-r55-fixed-core-proof/final.cnf
shasum -a 256 -c SHA256SUMS
```

Expected: `UNSAT`, two `s VERIFIED` results, `all_checks: true`, and the
counts in [EXPECTED_AUDIT.json](EXPECTED_AUDIT.json) and
[EXPECTED_CONTROLS.json](EXPECTED_CONTROLS.json). The final formula hash is
`9c809bbc4cee28279e25a961cfa7e8966682f234caab087f19390aad764157ac`.
[verification.json](verification.json) records compact evidence hashes.

The successful discovery took about 50 seconds including domain construction;
fresh reproduction took about 48 seconds before proof replay. The default
solve limit is 240 seconds. Timing is not evidence and varies by host. A
timeout does not establish infeasibility and does not invalidate a previously
checked trace. Reproduction succeeds only when both RUP replays pass.

Large generated CNFs and proof traces are deliberately omitted. The original
trace is about 19 MB and the trimmed trace about 16 MB; public source
regenerates them outside Git. Their hashes identify the checked files but do
not replace proof regeneration and replay.

## Scope, trust, and prior work

The final claim trusts the unformalized reduction, the short exact Python
auditor, RUP checking, the runtime and hardware, and input identity. It does
not require trust in the SAT solver's verdict, the decision diagrams, graph
catalogue completeness, or an imported Ramsey-number bound.

The height-2951 convex limitation remains valid: a fractional point satisfies
the aggregated linear constraints while this particular Boolean completion
family is excluded. The visible-only Boolean relaxation remains unresolved.
A 180-second test removing the profile and degree restrictions returned
`UNKNOWN`; no stronger fixed-core theorem is asserted.

Primary context is [Angeltveit and McKay's Ramsey paper](https://arxiv.org/abs/2409.15709).
The encoding mechanisms are standard; no historical-priority claim is made.
The final counter audit was checked against the
[PySAT threshold-grid source](https://github.com/pysathq/pysat/blob/master/cardenc/seqcounter.hh),
but does not import it. Relevant campaign sources are the
[height-2907 seed](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_d22_three_anchor_survivor)
and the [height-2951 convex barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_anchor_convex_barrier).

Keep this closed profile fixed pending independent review. A new family
claim must explicitly justify any removed assumption; do not infer it from
the present certificate or continue through cosmetic seed variants.
