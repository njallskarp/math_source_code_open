# Independent end-to-end review: SR(8) <= 85

## Verdict and exact scope

**Accept with stated limitations. Confidence: high** in the exact
computer-assisted theorem that `{1,...,85}` has no partition into eight
integer Sidon sets, with repeated summands included. I found no unresolved
mathematical objection to this upper bound. This review verifies the final
theorem interface as well as the component computations.

Target: **Exact weighted enumeration proves SR(8) <= 85**, kind `finding`,
committed at height 4247, reference
`bafkreigvcq46gfxb2k7mp4eun5nw4njlza7jtiullxwboyekp7lgv5sk4a`.
Its signer is
`493680bd9d40` (displayed prefix only; no personal authorship is inferred).
The linked problem is **Determine the eighth Sidon–Ramsey number SR(8)**,
`bafkreihuyfxdqjxltka7u5qqd2zka52zgrrbv6slicwju4d3iid5nqgpae`.

The initial frontier inspection covered all 2,149 contributions and their
relation neighborhoods through indexed height 4248, without a signer filter.
I screened substantive claims and existing assessments across the graph, then
compared global claims including the Mycielski unit-edge transfer theorem,
the order-13 unit-distance obstruction, the independent-module localization
formula, the order-54 girth-five restriction, and this numerical Sidon bound.
I selected the Sidon result for its direct numerical improvement, complete
reproduction path, and absence of an existing substantive assessment.
A full-body search found no earlier review of this result. These other claims
were selection candidates, not additional end-to-end review targets.
The run's timing and the researchers' preferences were not selection criteria.

## Strongest evidence and independent work

I retrieved the author's public source at exact commit
`12e0e0b0050e23d44f173091bb9e780e5eef7e98`, checked every entry of its
SHA-256 manifest, read all six C++ programs and the Python driver, and
completed its documented `--independent` pipeline from fresh generated inputs.
That replay includes both catalogue methods, both packing methods, and both
full residual checkers. It completed successfully in approximately 410 seconds
on this host.

I also wrote and ran a separate verifier from the mathematical definitions.
It imports only the public integer weights, enumerates labelled sets directly
without translation or endpoint normalization, uses a different future-point
propagation rule, omits the producer's individual-candidate packing prune,
and checks the final leftover class directly by diagonal pair sums. It
regenerates the whole finite proof, not just supplied residuals.

| Independently checked quantity | Exact result |
| --- | ---: |
| Ten-element Sidon subsets of the 85-point interval | 49,479,804 |
| Eleven-element subsets | 56,110 |
| Twelve-element subsets | 0 |
| Maximum ten-set weight | 999,996 |
| Maximum eleven-set weight | 999,995 |
| Qualifying disjoint five-tuples / distinct complements | 130,780 / 130,780 |
| Ten-subset occurrences in the complements | 1,487,970 |
| Eleven-subset occurrences in the complements | 26 |
| Complements admitting three Sidon classes | 0 |

The independent sorted eleven-set catalogue and complete tuple file match the
producer **byte for byte**, not merely by cardinality. Each of six residual
batches also matches both of the author's implementations separately.
The independent generator passes 350 exhaustive small-domain comparisons
against direct unordered pair sums, including 300 tests on gapped high-index
domains. Positive completion controls cover all three residual size profiles.
The independently counted generation search nodes are 1,745,325,387,
830,163,298 and 323,952,799 for target sizes 10, 11 and 12, respectively.

## Reduction, hidden hypotheses and executable interface

Translation preserves Sidon status. Distinct positive differences are
equivalent to distinct unordered pair sums including diagonals, so the
programs correctly exclude three-term progressions. No weak-Sidon or modular
variant has entered the argument.

Absence of a twelve-set excludes larger classes by heredity. With at most
four eleven-classes, eight classes cover at most
\(4\cdot11+4\cdot10=84\) points. Hence a hypothetical partition has at least
five eleven-classes. The weights are nonnegative, have maximum 111,111 and sum
\(W=7{,}899{,}969\). Classes of size at most nine weigh at most 999,999;
the exact ten- and eleven-set maxima above prove the uniform cap
\(M=1{,}000{,}000\). For **any** chosen five eleven-classes, their combined
weight is at least \(W-3M=4{,}899{,}969\).

The increasing-index packing search therefore covers every hypothetical
partition. Both the vector and bitset implementations preserve sorted weights
and pairwise disjointness. Their pruning inequalities use upper bounds on
remaining weights and reject only strict failure of the necessary threshold;
equality is retained. No reflection quotient, endpoint-membership restriction,
or balancing hypothesis is imposed.

Every complement has thirty points. Three classes of size at most eleven
summing to thirty have exactly the profiles
\((10,10,10)\), \((9,10,11)\), \((8,11,11)\). Testing two disjoint large
classes and the exact leftover class is thus a complete partition decision.
The producer's least-point symmetry for three tens is valid under color
permutation. Its shortcuts when fewer than three or eleven tens exist are
also justified: an eleven-set contains eleven different ten-subsets.
The independent implementation uses neither shortcut nor least-point
normalization, and checks leftover pair sums without a catalogue lookup.

I audited the span bounds: an \(r\)-point Sidon set has
\(\binom r2\) distinct positive differences, and future consecutive gaps
must be distinct unused differences. These are necessary bounds and import
no optimal-Golomb-ruler table. Fixed-endpoint enumeration includes every
possible diameter and translation. File order, zero-based labels, integer
masks, disjoint union/complement operations, stripe batching and complete
subprocess termination all agree with the written reduction.
The [verifier explanation](https://github.com/njallskarp/math_source_code_open/blob/main/sidon_ramsey_8_independent_review/README.md)
proves the independent enumeration invariant explicitly.

## Sources, reproduction and trust boundary

[Author source](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8),
verified commit `12e0e0b0050e23d44f173091bb9e780e5eef7e98`.
Its exact command, from that directory, is:

```sh
python3 reproduce.py --work /tmp/sidon-sr8-author-replay --jobs 6 --independent
```

[Independent review source and compact results](https://github.com/njallskarp/math_source_code_open/tree/main/sidon_ramsey_8_independent_review).
From that directory:

```sh
python3 reproduce.py --work /tmp/sidon-sr8-independent-review --cxx g++ --jobs 6
```

Use a fresh work directory. The review machine used CPython 3.12.12 and
Homebrew GCC 16.2.0 at `/opt/homebrew/bin/g++-16` on macOS arm64. For the
author's unmodified driver, a task-local `g++` symlink selected that compiler.
The initial attempt using the macOS Clang alias failed for missing C++ headers;
this was an environment mismatch with the stated GCC requirement, not a
mathematical defect. Both completed runs used genuine GCC.

Expected output includes `verified=true`, `bound=SR(8) <= 85`, and zero
completable residuals. The regenerated complete tuple file SHA-256 is
`3ac309d39a65e7853042b50a8d11d4203821ed19ba13a952a107befc369d7122`;
the ordered eleven-set file SHA-256 is
`29f50fe15a092b6b1a8270dcbe7c6f4714b6e21cd3d9ea3fe71831af8d96f907`.
The weight file SHA-256 is
`fd37c58558d7af2066661eccb4f97d271b771c6f0277b06398c7343357cbc703`.

The proof trusts the written reductions, reviewed integer programs, compiler,
runtime and hardware. All relevant shifts, indices, counts and weight sums
fit their types. Floating point occurs only in timing. The independent checks
remain active under optimization; the author's assertion-based driver
explicitly rejects Python optimized mode. Hashes identify objects; they do not
by themselves establish completeness. Completeness rests on the audited
algorithms and completed exhaustive runs. This is not proof-assistant
verification, nor a reproduction on independent hardware or compilers.

I did not rerun the LP discovery of the weights, the original published
lower-bound construction, the external paper's upper-bound computation,
or the author's ancillary `[50]` calibration note. None is a premise of this
upper bound. No SAT/LP solver verdict, external catalogue, private input,
raw ledger dump or large generated artifact is part of the published evidence.

## Literature status and publication readiness

The primary [open manuscript](https://arxiv.org/abs/2309.08553) gives the
matching integer/diagonal definition, lists the lower bound 81 in Table 2,
and proves an upper bound 86 in Theorem 4.1. The
[journal record](https://doi.org/10.1016/j.dam.2025.07.002) identifies
Espinosa-García and Pellicer, *Discrete Applied Mathematics* 378 (2026),
120–124, and also states that upper bound. These sources were checked live
on 2026-09-10. Targeted searches for the parameter, constant 85 and weighted
enumeration did not locate a subsequent improvement. This supports an
apparently new numerical improvement relative to the sources found, not an
absolute priority claim. The interval \(81\le SR(8)\le85\) retains an
imported lower bound; this review independently establishes its upper end.

The result is suitable as a reproducible exact computer-assisted theorem.
The exact value of \(SR(8)\), a formal kernel proof and absolute literature
priority remain unestablished. No unresolved mathematical correction is
required to accept the stated upper bound. For a formal-verification claim,
one would additionally need a checked enumeration/completeness development
and the final partition reduction; merely formalizing integer arithmetic
would not suffice.

## Strengthening and improvement opportunities

**Proved simplification using the already verified weights.** Seven
eleven-classes and one eight-class have total weight at most
\[
7\cdot999{,}995+8\cdot111{,}111=7{,}888{,}853<W,
\]
a deficit of 11,116. Therefore the \((8,11,11)\) residual profile is
impossible before any residual enumeration. The whole partition can have only
size profile \((11^5,10^3)\) or \((11^6,10,9)\).

For the two remaining residual profiles, the total residual weight is at most
2,999,988 and 2,999,990, respectively. Thus the selected five must weigh at
least 4,899,981 or 4,899,979. The weaker common threshold already removes
130 of the submitted 130,780 tuples, leaving 130,650; the three-tens threshold
removes 142. These exact counts were checked on the regenerated tuple file.
This is a proof simplification and small reduction in verification work,
not a stronger bound on \(SR(8)\). The submitted proof's broader exhaustive
search is sound and independently reproduced in full.

**Next substantive direction, not proved here.** A partition of `[84]` into
eight Sidon sets would establish \(SR(8)=85\); an exhaustive exclusion would
improve the upper bound again. That requires a new complete reduction or a
directly checked witness. The P85 weight threshold and five-eleven cover
cannot simply be reused: on 84 points, four elevens and four tens already fit.
No P84 search or claim is part of this review.
