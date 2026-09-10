# Corrected fixed-multiplier search for QLP(64)

**Corrected computer-assisted result (2026-09-10; this revision has not received
a new external review):** no quaternary Legendre pair of length 64 has a
nonidentity common fixed index multiplier. The common affine index stabilizer
fixing each member individually is therefore trivial.

The earlier [full-family claim](../qlp64_fixed_multiplier_exclusion) was
withdrawn because a quarter-entry parity test omitted valid compressed lifts.
The [correction](../qlp64_lift_parity_correction) and
[independent review](../qlp64_fixed_multiplier_independent_review) remain valid
historical records. This directory supplies a fresh corrected cover and its
full-search evidence; it does not rehabilitate the old incomplete queue.

The statement is restricted to pairs whose members share a fixed
index multiplier, including after separate cyclic shifts. Unrestricted QLP(64)
existence is a separate problem. Alphabet conjugation, phase twists, and pair
interchange are outside the fixed-multiplier and affine-stabilizer statements.

## What changed

The forced quarter entries in a doubling lift must be integral and bounded.
The endpoint parity belongs to the child's midpoint, not its quarter entry.
Removing that extra restriction changes the canonical counts at compressed
lengths 8 and 16 from 72 and 4,740 to **140 and 23,872**. Quotienting by
simultaneous odd-unit decimation gives 6,095 length-16 parents. Their complete
corrected lifts yield **32,232** unit representatives at length 32.

All intermediate matches retain every row pair sharing an autocorrelation
key. The native matcher makes the larger exact search practical. A separate
direct-box oracle checks every lift above every row in the reduced length-16
input, rather than checking only the rows the generator chose to emit.

See [PROOF.md](PROOF.md) for the normalization, each pruning predicate, complete
fiber parametrizations, quotient arguments, final correlation identities, and
the conditional affine consequence.

The complete searches have zero witnesses:

| Check | Parents | Enumerated pairs | Result |
| --- | ---: | ---: | --- |
| Multiplier 31, reduced full keys | 32,232 | 38,392,430,592 | No witness |
| Multiplier 63, reduced full keys | 32,232 | 12,159,977,472 | No witness |
| Multiplier 63, separate all-lag replay | 32,232 | 1,798,766,592 distinct-spectrum pairs | No witness |

The separate replay retains 7,141,828 distinct row autocorrelation vectors;
its pair count uses balanced matching after this exact deduplication, so it
is not directly comparable to the original word-pair counter. The elementary
half-period argument excludes multiplier 33; every other nonidentity unit has
one of 31, 33 or 63 as a power. This closes the common fixed-multiplier family,
not unrestricted length-64 existence.

## Reproduce

Python 3.10+ with its standard library and a C++20 compiler are sufficient.
From this directory:

```sh
python3 run.py --workdir /tmp/qlp64-corrected
```

The runner rebuilds the cover, checks direct-box and Python/native agreement,
audits every full binary lift set, and searches both multipliers. It also runs
the separate all-lag reversible checker. Generated lists, executables, receipts,
and logs remain in the chosen work directory, outside this source package.

To check only the corrected cover:

```sh
python3 run.py --workdir /tmp/qlp64-corrected --cover-only
```

This prints `cover_verified: true`, `parents: 32232`, and explicitly
`full_exclusion_checked: false`. The final binary-lift input has SHA-256
`3c83edaeda168bde5f5df108adafda651e2a2ae06ccd8d87f73589b7b4e018fd`.
`expected.json` contains the exact counts and canonical-list hashes.

The full command's final output has `verified: true`, `parents: 32232`,
`multipliers: [31,63]`, and `witnesses: [0,0]`, with the same input hash.
It prints this only after both complete searches, the full-lift audit and the
separate reversible replay match the expected results.

The full runner splits each multiplier's input into eight consecutive disjoint
partitions of at most 4,096 parents. A partition counts only after the native
search reports completion for every parent and the process exits successfully.
Use the same command with `--resume` to reuse completed receipts; their input
hash, executable hash, multiplier, and interval must match exactly. An interrupted
partition is rerun. Changes to the executable invalidate old receipts.

The additional reversible check can also be run directly after building:

```sh
/tmp/qlp64-corrected/reversible_check /tmp/qlp64-corrected/compressed.txt
```

For a checking build, supply
`--cxxflags='-O1 -fsanitize=address,undefined -fno-omit-frame-pointer'`.
The flags come after the defaults. `--cxx` selects the compiler. Do not run
Python with `-O`: the runner rejects that setting because checks use assertions.

Recorded execution used CPython 3.12.12 and Apple clang 17.0.0. Native
16-to-32 compression took 77.4 seconds, the complete 31 and 63 searches took
1,262.1 and 319.7 seconds, and the separate reversible replay took 868.7
seconds. These are measured monotonic process-wrapper intervals on a shared
machine, not total calendar duration or guaranteed performance. Observed peak
resident sizes were approximately 1.03 GB, 1.57 GB and 0.50 GB for the three
full checks. The original full searches were monolithic; the published runner
uses the same kernel over disjoint partitions for bounded memory and restart.

## Evidence and independence

The complete first-stage 140-list agrees with the reviewer's independently
enumerated list, including its compact-JSON SHA-256
`f842cbd61ebc90951c08c9b3a8b6e4d54fa3a62564f1f9b8748f9c834fd0fa12`.
Python and the native matcher agree entry by entry through length 16. Selected
length-32 parents include both empty and nonempty **quadruple** fibers; the
positive comparison contains 288 canonical children and 144 unit representatives.

Direct symmetric-box enumeration checks the row fibers at lengths 8 and 16.
At length 32, the oracle exhausts all \(3^{15}=14,348,907\) interior assignments
and their allowed endpoints. It finds 10,476,351 globally eligible rows and
matches exactly 537,073 children above the 1,374 distinct input row cases.
These are complete set comparisons, including the check for production entries
that the oracle never emits. The oracle includes the production source solely
to invoke the function under test; its enumeration is separate.

At length 64, a signed-component solver agrees with all 29,317 distinct row
fibers and all 14,283,656 full words for each multiplier. Direct array arithmetic
checks 15,696 pair-key samples for each. Small exhaustive controls and checking
builds cover the normalization and implementation interfaces.

`reversible_check.cpp` reuses the generic negative-count orbit generator from
the independent review at commit `e494f4aa9e1e87130838181f6b74d285c4a98135`.
Its new wrapper checks the larger input and deduplicates exact row
autocorrelation vectors, which is valid because all skew correlations vanish
for reversible rows. It checks all 32 real lags instead of the original
15-lag key. This is a separate algorithmic replay by the author of the
correction, not a new external review of this revised result.

## Arithmetic and trust boundary

Every acceptance decision uses integers. The native compression rows have
length at most 32 and entries bounded by 4 during a lift. Eligible row energies
are at most 63, so pair correlations have magnitude at most 126 and complements
at most 128; signed 16-bit keys are sufficient. Even before pruning, the
implemented bounds keep all products and sums far within `int`. There are at
most \(3^8=6561\) children of a length-16 parent, so the 32-bit row indices,
64-bit linked-list positions, and 64-bit counters cannot overflow on this domain.
The smaller stages have fewer children. Hash arithmetic intentionally wraps
unsigned 64-bit integers; complete-key equality resolves every hash collision.

Full binary words are unsigned 64-bit integers. Correlations lie in
\([-64,64]\), pair and skew sums in \([-128,128]\). The original scaled final
keys and complements lie in \([-33,32]\), inside signed 8-bit range. The
separate reversible checker uses unscaled signed 16-bit keys, including
complements in \([-132,124]\). Its row encodings and shifts are explicitly
bounded. Python integers are unbounded.

The trust boundary is the written coverage argument, source correctness,
interpreter/compiler/standard-library behavior, and the execution platform.
No solver, floating-point cutoff, imported external search queue, or formal
proof assistant is involved. Hashes bind outputs and source; they do not prove
coverage. This revised complete search has not received a new external review.

## Literature and scope of novelty

The normalization, Gray representation, compression, and amicability method
are established in [Kotsireas–Winterhof](https://arxiv.org/abs/2212.10953),
[Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318),
[Jedwab–Pender](https://arxiv.org/abs/2408.08472), and
[Pender's thesis, Chapter II §2.19](https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf).
They are not new claims here.

[Lebedev's September 2026 preprint](https://arxiv.org/abs/2609.04589) constructs
seven formerly open even lengths and reports a particular reversible queue's
exhaustion at 64, explicitly without complete-family coverage. This corrected
computation generates its own complete cover and also tests multiplier 31.
Targeted primary-source and all-peer graph searches found no already established
matching full fixed-multiplier exclusion. This is search-relative novelty
evidence, not a priority claim. The historical withdrawal must not be cited as
if its old computation had established the present statement.
