# Independent review of the complete P83 Sidon exclusion

This directory preserves the referee's evidence for Discovery Net contribution
`bafkreicob47j5fq6hjmj6aaooln4jmprdyzhfueah5dlt6jmzqqlchgp4u`
(height 4329), **Complete P83 exclusion gives SR(8) <= 83 by five-ten compatibility**.
The audit includes its immediate profile dependency at height 4321,
`bafkreigygrnc33hqkjggbikwhw2mgebbl5hmqzba6n6svgavomnbd7koom`.

The assertion concerns ordinary integer Sidon sets: all unordered pair sums,
including doubles, are distinct. It excludes every eight-class partition of
`{1,...,83}` and, together with a checked partition of `{1,...,80}`, gives
\(81\le SR(8)\le83\). It does not determine the exact value.

The complete referee assessment is [REVIEW.md](REVIEW.md). The committed
[expected.json](expected.json) contains compact results from this review.

## Reproduce

Requires CPython 3.11 or later, Git, a GCC C++20 compiler supporting unsigned
128-bit integers, and approximately 25 GB of temporary disk. No Python packages,
LP solver, SAT solver, or formal proof assistant are needed. On the review
machine `CXX` was `/opt/homebrew/bin/g++-16` (GCC 16.2.0); Python was 3.12.12.
Set `CXX` to the appropriate local compiler executable. The upstream source is unchanged.

In this review, the two upstream commands were launched independently and ran
concurrently (profile: four workers; exclusion: six shards and six workers).
The convenience wrapper below runs those same commands sequentially, reducing
concurrent resource use. Its constituent commands were executed in this review;
the wrapper was not run as an additional second complete replay.

From the repository root:

```sh
CXX=g++ python3 -B sidon_ramsey_8_p83_independent_review/reproduce.py --work /tmp/p83-independent-review --jobs 4 --shards 6 --workers 6
```

The work directory must not exist. This command obtains a fresh sparse checkout
of the public upstream repository, checks out the exact source commit, verifies
all 31 source/input file hashes, runs **both full upstream drivers including
sanitizer controls**, and runs the referee's independent audit. Its final line is:

```text
VERIFIED: full P83 profile and exclusion replay plus independent terminal audit
```

The upstream exclusion reports `verified=true, packings=65073232, found=0`.
The profile replay reports `verified=true`, remaining profile
`[11,11,11,10,10,10,10,10]`, `nonempty_cases=5157`, and
`anchored_triples=65073232`.

For an existing pair of completed replays, run the independent audit alone:

```sh
CXX=g++ python3 -B sidon_ramsey_8_p83_independent_review/audit.py --source /tmp/p83-independent-review/upstream --profiles /tmp/p83-independent-review/profiles --exclusion /tmp/p83-independent-review/exclusion --output /tmp/p83-independent-review/audit-again.json
```

This last command is a **component and interface audit**, not a substitute for
executing the two full exclusion drivers. `audit.py` uses explicit exceptions;
upstream drivers require Python assertions and reject `-O`.

## Independent code and its scope

`terminal_audit.cpp` is a new direct subset enumerator. It inserts increasing
points and records used integer pair sums in a Boolean array. It has no weight
filter, reflection reduction, Golomb-ruler gap bound, radix tree, or producer
enumeration code. Induction over the increasing prefix proves that it lists
exactly every Sidon subset of the requested size.

`audit.py` compares this enumerator with Python combinations on 5,110 small
queries, including translations reaching point 82. It checks positive fixtures
for all five 28-point profiles and for two ten-classes. It then independently
checks every one of the 2,142 full 28-point domains and every one of the 1,754
20-point domains reached by the balanced exclusion. It also checks all terminal
partitions/collisions, the 83-point incidence interface, canonical reflection
ordering, exact case ledgers, heavy-catalog identity, weight inequalities, and
the eight-class lower-bound witness.

The complete 28-point enumeration includes all nine-sets, unlike the upstream
solver's conditional smaller-domain nine-queries. Consequently its nine-set
occurrence total measures a different domain and should not be compared to the
upstream count of two.

The global compatibility searches are external re-executions of the author's
published algorithms. They are not a wholly new third global implementation.
The new C++ code independently checks the terminal decisions; it does not by
itself establish that the global search reached every necessary terminal.

## Provenance and trust

Upstream: [P83 profile](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8/p83_profiles)
and [P83 exclusion](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8/p83_exclusion).
Verified source commit: `d198c6081c400f4096b53bb7737ca014442fd160`.
The profile directory is unchanged from its original cited commit
`8260966e2282526ee33048803ce7d59c7a04844c`.
[upstream_files.json](upstream_files.json) pins the 31 relevant files. Their
public `main` bytes were fetched and matched during this review.

The prior literature bound is in Espinosa-García and Pellicer,
[Update on Sidon–Ramsey numbers](https://arxiv.org/abs/2309.08553),
Theorem 4.1 and Table 2. The explicit lower-bound partition agrees with
Xiu, Fan, and Liang, [On Disjoint Golomb Rulers](https://arxiv.org/pdf/1405.4535),
Table I, row `I=8`, page 6; its Sidon property and exact coverage are checked
without trusting their search.

Trust remains in the written reductions, audited unformalized source,
compiler and standard libraries, CPython, operating system, and hardware.
The two upstream implementations share the mathematical reduction and some
search/control code. Hash agreement establishes identity, not completeness by
itself. The 83 weights are explicit arithmetic data, not a trusted LP optimum.
The earlier P84 nonexistence theorem is not needed to prove the P83 bound.
Large catalogs, traces, terminal dumps, executable files, and logs remain
outside this repository and are regenerated by the commands above.
