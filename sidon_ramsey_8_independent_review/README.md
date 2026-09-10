# Independent end-to-end verification of SR(8) <= 85

This directory contains a referee's independent implementation of the complete
finite exclusion in Discovery Net contribution
`bafkreigvcq46gfxb2k7mp4eun5nw4njlza7jtiullxwboyekp7lgv5sk4a`
(height 4247), **Exact weighted enumeration proves SR(8) <= 85**.
See [REVIEW.md](REVIEW.md) for the verdict, scope, provenance and limitations.

The only imported mathematical input is the author's 85-entry integer weight
vector. All sets and packings are generated afresh by this implementation;
no producer code, catalogue, solver result or precomputed residual is loaded.
`weights.txt` is copied verbatim from the public source at commit
`12e0e0b0050e23d44f173091bb9e780e5eef7e98`:
[author source](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8).
The weight vector is a numerical certificate, not an assumption of its validity.
The verifier checks its bounds on every relevant Sidon set.

## Reproduce

Requires Python 3.11+ with its standard library and GCC with C++20 and
`__uint128_t` support. Tested on macOS arm64 with CPython 3.12.12 and
Homebrew GCC 16.2.0. Use an actual GCC executable; the macOS system `g++`
may be a Clang alias. All work paths must be fresh and outside this directory.

From this directory:

```sh
python3 reproduce.py --work /tmp/sidon-sr8-independent-review --cxx g++ --jobs 6
```

On the review machine the compiler argument was `/opt/homebrew/bin/g++-16`.
Expected final output includes:

```json
{"verified": true, "bound": "SR(8) <= 85", "residual_totals": {"tested": 130780, "ten_sets": 1487970, "eleven_sets": 26, "completable": 0}}
```

The final object also includes counts, hashes, the refinement audit and elapsed
time. The driver refuses to reuse an existing work directory, checks every
subprocess exit status, checks each batch length, and uses explicit exceptions
rather than Python assertions. Generated sets, tuples, binaries and detailed
run output remain in the work directory; none is published here.

A compact record of the completed author replay and independent runs is in
[results.json](results.json). SHA-256 checksums for this package are in
[SHA256SUMS](SHA256SUMS).

## Mathematical theorem interface

An integer set is Sidon when its unordered pair sums, including pairs with
repeated entries, are distinct. This is equivalent to distinct positive
pairwise differences: a repeated difference rearranges to a nontrivial sum
equality, and conversely. Three-term arithmetic progressions are therefore
forbidden. Translating `[85]` to `{0,...,84}` preserves this property.

The regenerated counts are 49,479,804 ten-sets, 56,110 eleven-sets, and zero
twelve-sets. Heredity excludes every larger set. Thus any eight-class partition
of 85 points must contain at least five eleven-sets, since four elevens and
four classes of size at most ten contain at most 84 points.

The nonnegative point weights sum to 7,899,969 and are at most 111,111.
Classes of size at most nine therefore weigh at most 999,999. Exhaustive
integer evaluation gives maxima 999,996 and 999,995 for tens and elevens.
Every class consequently weighs at most 1,000,000. In a hypothetical
partition, **any** chosen five eleven-classes must be pairwise disjoint and
weigh at least 7,899,969 - 3,000,000 = 4,899,969. The verifier enumerates every
such unordered choice, including equality, obtaining 130,780 choices and
130,780 distinct 30-point complements.

Three classes of size at most eleven summing to thirty have precisely the
sorted profiles (10,10,10), (9,10,11), (8,11,11). Every such partition has two
classes each of size ten or eleven. The residual verifier enumerates every
ten and eleven in the complement, tries every disjoint pair of the appropriate
sizes, and tests the remaining ten, nine or eight directly by all unordered
pair sums. All choices fail. This establishes the upper bound, without a
balance hypothesis, reflection quotient or unproved computation-to-theorem
bridge. Empty classes cannot produce another profile.

## Independent enumeration invariant

`Generator` enumerates increasing lists directly in the labelled domain. It
neither normalizes the minimum to zero nor fixes both endpoints. At a prefix
`A`, let `D` be its positive differences and let `C` contain precisely the
larger domain points whose individual addition preserves the Sidon property.
Initially `A` and `D` are empty and `C` is the domain.

Choose `x` from `C`. Its fresh differences are `x-a` for `a` in `A`, so the
updated difference set is `D' = D union {x-a : a in A}`. For a surviving
candidate `y>x`, a new conflict on adding both `x` and `y` occurs exactly when
`y-x` belongs to `D'`:

- This condition directly repeats the difference `y-x`.
- Conversely, a collision involving `y-a` and a fresh difference `x-b`
  rearranges to `y-x=a-b`; since `y>x`, this is an old positive difference.
  All other collisions were already excluded by membership in `C`, or are
  among distinct differences sharing the new endpoint and cannot occur.

Thus the new candidate mask is exactly the old larger-candidate mask with
`x+D'` removed. This is the single shifted mask in the implementation. The
only numerical pruning says that a suffix of `r` points must span at least
`r(r-1)/2`, because those positive differences are distinct. Insufficient
candidate count is also a necessary obstruction. All pruning is therefore
complete. Every set is generated once in increasing order.

The implementation's generation counts agree against brute-force pair-sum
checking for all 50 interval cases with `1<=n<=12`, `1<=k<=min(n,5)`, and 300
cases on deterministic ten-point subsets of `{0,...,84}` with `k=3,4,5`.
The latter exercise gaps, bit 64, and pair sums above 127. Separate controls
reject `{0,1,2}` and accept `{0,1,3}`. Three 30-point positive controls formed
from known disjoint Sidon sets exercise all residual size profiles.
These controls calibrate the code; the universal completeness argument above
is not inferred from finite testing.

## Packing and finite-object correspondence

Eleven-sets are sorted by decreasing integer weight, with the exact subset
mask breaking ties. The packing search maintains increasing catalogue indices
and intersects candidate lists with disjointness from each chosen set. Its
only weight bounds replace unchosen sets by heavier available candidates.
It omits the producer's extra individual-candidate pruning and does not build
the alternative producer's adjacency-bitset graph. This implementation visits
2,059,358 packing nodes, versus 2,029,824 in the producer's vector search.
The resulting sorted catalogue and tuple file agree byte for byte:

| File | SHA-256 |
| --- | --- |
| `weights.txt` | `fd37c58558d7af2066661eccb4f97d271b771c6f0277b06398c7343357cbc703` |
| `ordered_sets.txt` | `29f50fe15a092b6b1a8270dcbe7c6f4714b6e21cd3d9ea3fe71831af8d96f907` |
| `packings.txt` | `3ac309d39a65e7853042b50a8d11d4203821ed19ba13a952a107befc369d7122` |

There are no quotient multiplicities to import. The generator proves completeness;
the hashes establish exact correspondence with the producer's encoded objects.
The residual stage validates eleven-set syntax and Sidon status, strictly
increasing tuple indices, disjointness, cardinalities, full file reads and batch
coverage. Its direct leftover pair-sum test replaces the producer's hash lookup
and least-point normalization. It also enumerates elevens unconditionally.

The six independent residual batches reproduce the producer and its alternate
pair-sum checker separately: ten-set counts 246609, 248655, 248318, 248992,
248316, 247080 and eleven-set counts 5, 2, 6, 5, 5, 3.

## Trust boundary

This is exact computer-assisted mathematics, not a proof-assistant derivation.
The boundary is the written reduction and enumeration proofs, the reviewed C++
and Python sources, GCC/runtime and hardware. The data path uses exact integers;
floating point is used only for timing. Point and difference indices are at most
84; shifts are below 128, and discarded high bits are outside the domain.
Direct pair sums index a 169-entry array. Counts use 64 bits; weights and their
sums are far below signed 64-bit limits. The deterministic control seed uses
intentional unsigned wraparound. Checks remain active in optimized builds.

LP weight discovery, optimal Golomb-ruler tables, external catalogues, and the
published lower bound are not premises of this upper-bound verification.
No claim of determining SR(8), proving absolute literature priority, or formal
verification is made. The author replay and referee computation use the same
local compiler and hardware and therefore are not independent of those layers.
