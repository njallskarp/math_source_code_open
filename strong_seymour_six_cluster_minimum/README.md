# Exact minimum for six-cluster transitive Strong Seymour blow-ups

## Result

Let `Q` be an arbitrary tournament on six vertices.  Replace vertex `i` of
`Q` by a nonempty transitive tournament of order `s_i`, and orient every edge
between two clusters in the direction of the corresponding edge of `Q`.
Among all tournaments obtained this way, the minimum order of a tournament
with no strong Seymour vertex is exactly

```text
36.
```

Here the exact second out-neighborhood of `x` is

```text
N++(x) = {z : x -> y -> z for some y} \ (N+(x) union {x}),
```

and `x` is a strong Seymour vertex when the arcs from `N+(x)` to `N++(x)`
contain a matching whose tails cover all of `N+(x)`.

The order-36 upper bound is the construction of Dzitsoev recorded in
Bai--Li--Park, Remark 3.1.  Its quotient out-neighborhoods and transitive
cluster sizes are

```text
0 -> 1,4,5       sizes (7,3,11,3,9,3)
1 -> 3,4,5
2 -> 0,1,3
3 -> 0,4
4 -> 2,5
5 -> 2,3.
```

The checker reconstructs this tournament and confirms directly that it has no
strong vertex.  The new lower result is an exhaustive exact exclusion of every
six-cluster transitive blow-up of order at most 35.  This is a minimum only in
the stated six-cluster class; it does not determine the unrestricted minimum
order of a tournament with no strong Seymour vertex.

## Why the enumeration is complete

A tournament on six labeled vertices is encoded by its 15 edge directions.
The program applies every permutation in `S_6` and obtains exactly 56
unlabeled quotient representatives.  For each total `n=6,...,35`, it visits
every ordered positive composition

```text
s_0 + s_1 + s_2 + s_3 + s_4 + s_5 = n.
```

Every labeled quotient can be relabeled to one of the 56 representatives;
applying the same relabeling to its cluster-size vector gives one of the
ordered compositions checked with that representative.  Hence this covers
every tournament in the class.  The exact number of configurations checked is

```text
sum(n=6..35) 56 * binomial(n-1,5) = 90,896,960.
```

This is an exhaustive covering count, not a count of nonisomorphic blow-ups:
automorphisms of a quotient can make two checked configurations isomorphic.

For every vertex, the checker constructs its exact first and second
out-neighborhoods and runs an exact augmenting-path bipartite matching test.
It stops with a witness if any checked tournament has no strong vertex.  The
completed direct run finds none.  The optional `--all` mode uses the theorem
that a counterexample has minimum out-degree at least six as a filter;
`--all-direct`, used for the stated certificate, does not use that filter.

## Reproduction

The main result requires a C++20 compiler.  It was reproduced with Homebrew
GCC 16.2.0 on arm64 macOS:

```sh
/opt/homebrew/bin/g++-16 -std=c++20 -O3 \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  verify.cpp -o /tmp/strong-seymour-six-cluster
/usr/bin/time -l /tmp/strong-seymour-six-cluster --all-direct \
  | tee /tmp/strong-seymour-six-cluster.stdout
shasum -a 256 /tmp/strong-seymour-six-cluster.stdout
```

The direct run takes about 55 seconds on the reference machine.  Its final
line is

```text
VERIFIED SIX-CLUSTER OBSTRUCTION; quotient_classes=56 total_configurations=90896960 matching_tested=90896960 degree_filter=off quotient_fnv64=9337430478797765613 checksum_fnv64=15769541166478794547
```

The complete stdout has SHA-256

```text
67a2ffa33e2706ef6eea80187064871bf0178e912a30fa3997dcceea4fc5c082.
```

An AddressSanitizer/UndefinedBehaviorSanitizer build completed the same full
domain without a diagnostic and produced the same final marker.  The
warning-clean optimized build above is the compact reproduction command.

The independent Python program shares no C++ code.  It partitions the 32,768
labeled quotients into orbits by set action rather than canonical scanning,
uses Hopcroft--Karp rather than the C++ augmenting-path routine, validates the
published order-36 witness, and checks all labeled quotients for that size
vector and each of its six one-cluster decrements:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
shasum -a 256 -c SHA256SUMS
```

Its principal output is

```json
{"all_six_cluster_configurations_through_35": 90896960, "published_order": 36, "published_strong_vertices": [], "quotient_classes": 56, "quotient_representatives_sha256": "3bc4e5954003d8e06c168920532f0cfa40aafba6f69c4a7e56d6895707fa3d08", "shell_no_strong_counts": [6, 0, 0, 0, 0, 0, 0], "status": "INDEPENDENT VERIFIED"}
```

All four unit tests pass.  The independent program does not replay all
90,896,960 configurations; it independently checks the quotient orbit count,
the count formula, the construction, matching semantics, and the nearest
order-35 boundary.  The C++ direct run is the exhaustive exclusion.

## Literature boundary and relation to prior work

Bai, Li, and Park, *Towards a strengthening of the second neighborhood
conjecture* (<https://arxiv.org/abs/2607.18047>), introduce the strong matching
condition, prove that minimum out-degree at most five guarantees a strong
Seymour vertex, and record the order-36 six-cluster construction in Remark
3.1.  The existing exact Discovery Net result proves that every tournament of
order at most 14 has a strong vertex and separately minimizes the six strict
inequalities displayed in Remark 3.1.  A later Lean development formalizes
that integer-inequality minimum.

The result here is different: it discards those six sufficient inequalities
and checks the strong-vertex property itself for every choice of a six-vertex
quotient and every positive transitive cluster vector below order 36.  Thus it
closes the entire six-cluster transitive blow-up class, not only Dzitsoev's
fixed quotient or its displayed inequality chamber.

Austin Gibbons's public SSNC source
(<https://github.com/AustinBGibbons/ssnc>) studies regular tournaments and
strong-vertex counts, not no-strong six-cluster classification.  Targeted
searches of that source, the Bai--Li--Park paper, the web, and committed
Discovery Net knowledge through height 2038 found no prior statement of this
class minimum.  Novelty is search-relative, not a historical-priority claim.

## Trust boundary

The mathematical claim relies on the written orbit/composition completeness
argument and inspection of the compact C++ construction and matching code.
The exhaustive execution additionally trusts GCC's C++20 implementation,
64-bit integer and bit-operation semantics, the operating system, and
hardware.  Sanitizers test but do not prove implementation correctness.  The
separate Python implementation reduces correlated risk for quotient orbits,
the published witness, and matching semantics; it is not a second exhaustive
run.  The order-36 existence side trusts the transcribed primary-source
quotient and is checked directly by both programs.

There is no SAT/SMT/MILP solver, floating point, randomness, external dataset,
generated input, private state, database, or omitted certificate.  The
published directory contains all source needed to reproduce the result.
