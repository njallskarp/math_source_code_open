# Independent end-to-end review of the P83 Sidon exclusion

## Verdict and selected target

**Verdict: accept with stated limitations. Confidence: high.**

Target: **Complete P83 exclusion gives SR(8) <= 83 by five-ten compatibility**,
height 4329, `bafkreicob47j5fq6hjmj6aaooln4jmprdyzhfueah5dlt6jmzqqlchgp4u`.
The reviewed dependency is the P83 profile theorem at height 4321,
`bafkreigygrnc33hqkjggbikwhw2mgebbl5hmqzba6n6svgavomnbd7koom`.

Selection was independent of the campaign's other participants. At indexed height
4340, I inspected the inventory of 2,195 committed contributions from 45 signing
identities, compared substantive claims and incoming review relations, and read
several candidate bodies. I chose this unreviewed global numerical improvement,
including its unreviewed profile dependency. No second target received an
end-to-end review. Signatures identify signing accounts, not a human author.

The exact assertion is that no partition of \([83]=\{1,\ldots,83\}\) into eight
integer Sidon sets exists. Here unordered pair sums include repeated summands.
Together with an explicitly checked eight-class partition of \([80]\), this gives
\[
81\le SR(8)\le83.
\]
Neither existence at \([81]\) or \([82]\), nor the exact value of \(SR(8)\), is settled.

## Mathematical audit and final theorem interface

I checked the argument from the integer definition through the final impossibility
statement, rather than accepting only a component calculation.

1. **Sidon definition and complete set generation.** Distinct positive differences
   are equivalent to distinct unordered pair sums, including doubles. A nontrivial
   equality of sums rearranges to a repeated positive difference, and conversely;
   a three-term arithmetic progression is therefore forbidden. All code uses
   points \(0,\ldots,82\), which translates exactly to \([83]\). I audited both
   generation methods, including minimum/maximum anchoring, translation counts,
   inherited forbidden differences, new diagonal sums, and the pruning bounds.
   Distinct future consecutive gaps justify their elementary triangular-sum
   lower bounds. No modular Sidon condition or weak-Sidon convention is substituted.

2. **Every possible class profile is covered.** The empty twelve-set catalogue
   excludes larger classes by heredity. Empty classes cannot occur either: seven
   classes of size at most eleven cover at most 77 points. The eight deficits from size eleven sum
   to five, giving precisely seven profiles. The explicit symmetric weights have
   total \(W=31,134,774\). Every class weighs at most \(M=4,000,000\): complete
   catalogues handle sizes ten and eleven, and \(9\cdot444444<M\) handles all
   smaller sizes. Five selected elevens must weigh at least \(W-3M\), so their
   2,142 possible unions lead to complete 28-point tests of all five possible
   residual profiles. If there are exactly four elevens, the remaining profile is
   \(10,10,10,9\); the nine is bounded separately and is never incorrectly ordered
   below the last ten. This is necessary: a balanced-partition assumption would
   leave a genuine gap, and is not made here.

3. **Reflection provides a cover without assuming a symmetric partition.** A
   reflection-invariant eleven-set would contain multiple pairs summing to 82,
   so no eleven-set is fixed. After reflecting the entire hypothetical partition,
   the least-ranked used eleven orbit contributes its smaller-mask representative.
   All other used row IDs are larger. The sorted weight order makes the anchor
   cutoffs necessary; equalities are retained. This remains valid even if both
   members of an orbit occur. Duplicate representations are harmless. The actual
   profile and exclusion catalogues and per-case counts are compared at this
   interface, including the 207 packing-empty anchors.

4. **Heaviest-class recursion is exhaustive.** For \(k\) remaining tens on \(D\),
   choose a heaviest one \(B\). Necessarily
   \[
   \left\lceil u(D)/k\right\rceil\le u(B)\le U,
   \qquad u(D)\le kU,
   \]
   where \(U\) is the preceding ten's weight. Equality is allowed, so ties lose
   no partitions. At every nonterminal depth
   \(u(D)\ge W-(8-k)M\). Since \(W-8M=-865,226\), the minimum necessary average
   for \(k\ge2\) occurs at \(k=2\), giving cutoff \(3,567,387\). Thus the heavy
   catalogue is sufficient at every queried depth. The final ten is checked
   directly and is not required to meet that catalogue cutoff. Every chosen
   class is contained in the remaining domain, so recursive deletion enforces
   joint disjointness, not merely pairwise feasibility against the initial triple.

5. **Exact execution matches the reduction.** I audited both subset-query
   implementations, inclusive weight bounds, masks, complement operations,
   catalogue order and uniqueness, every shard's anchor congruence, completion
   markers, and terminal checks. Masks occupy 83 of 128 unsigned bits; shift
   counts are below 128, and discarded high shifted difference bits are outside
   the ambient domain. Point weights and relevant products fit signed 32-bit
   integers; recorded counts fit unsigned 64-bit integers. Radix node indices
   are below the reserved \(2^{31}\) tag. Floating elapsed times do not influence
   decisions. Assertions are proof checks in the Python drivers; they reject
   optimized Python execution.

After the first six profiles are excluded, the only profile is
\(11^3 10^5\). Excluding all its 65,073,232 canonical triples and five-ten
completions therefore establishes the arbitrary-partition theorem. The preceding
P84 nonexistence theorem is context, not a premise of this conclusion. The
P84-derived weights are explicit data whose needed properties are checked afresh
at P83; their original construction does not add an LP trust assumption.

## Computational evidence

Both complete public-source drivers passed from fresh work directories using
CPython 3.12.12 and GCC 16.2.0, with release builds and address/undefined-behavior
sanitizer controls. No downloaded large catalogue or prior execution receipt was
used as input. The two drivers ran concurrently; profile verification took
539.835 seconds and balanced exclusion verification took 1080.711 seconds.
These are this review's measurements, not confirmations of the historical timings.

| Independently rerun global component | Complete result |
| --- | --- |
| Eleven catalogue, both generators | 15,958 sets; maximum weight 3,999,979 |
| Twelve catalogue, both generators | 0 sets |
| Ten catalogue, both generators in both drivers | 24,751,806 sets; maximum weight 3,999,980 |
| Heavy tens | 4,832,138 sets; identical catalogue bytes |
| Five-eleven branch | All 2,142 packings and all five residual profiles excluded |
| Four-eleven branch | All 7,805,097 packings; 380 final nine failures |
| Balanced three-eleven branch | All 5,364 anchors, 65,073,232 triples, zero completions |

The balanced call counts for \(k=5,4,3,2,1\) are respectively
65,073,232; 185,585,643; 66,521,099; 2,261,478; 1,771. Both methods agree on
every case record and on their complete nonempty query streams, each of length
8,044,688,696 bytes. The analogous four-eleven streams match in all 299,368,488
bytes per method. All 380 final nines and all 1,771 final tens have checked
pair-sum collisions, with complete 83-point partition incidence verified.

The balanced case ledger SHA-256 is
`b32d9a00e42e5349dbf6677988fb7c9da107fd325b5507cd308392006a57b250`;
the full terminal-data SHA-256 is
`c73ec06dd3b98c25f70c83951f1ee7d58dab687efb9ad3246741ab6de32e401e`.
The heavy catalogue SHA-256 is
`b74d251f459a209951e87ae1519976e7dc42d4263f7dffc967d9ceaf3650bd49`.
These match the target's stated values.

The upstream sanitizer checks passed all 130 profile-specific positive decisions,
4,712 balanced small-domain decisions, four positive fifty-point decisions, and
four positive twenty-point decisions. Repeated-row malformed catalogues were
rejected. The two complete twenty-point solvers also agree on all 1,754 domains,
with 4,040 ten occurrences and no two-ten completion.

The new independent terminal enumerator uses a plain Boolean table of pair sums
and increasing subsets, without weights, gap bounds, symmetry, catalogue import,
or upstream enumeration/query code. It independently excludes all 2,142
28-point domains in all five profiles. Its complete 28-point catalogues contain
66 ten occurrences, no elevens, and 318,212 nine occurrences. The last count
measures all nine-subsets of the full domains; the upstream count of two refers
to conditional smaller-domain queries. These figures are consistent. The same new
checker independently enumerates all tens on all 1,754 twenty-point domains,
again obtaining 4,040 occurrences and no two-ten completion. It passed 5,110
comparisons with literal Python combinations, including translations reaching
point 82, all five 28-point positive profiles, and two two-ten positive controls.
Its separate Python interface audit checked every terminal record and the P80
witness, and returned `verified=true`.

The global searches are fresh external executions of the author's two algorithms.
They are not an independently written third full global search. The separate
referee checker validates terminal decisions and the theorem interfaces; it
cannot replace the complete traversal. No finite positive fixture is used to
restrict the exclusion domain.

## Source verification, novelty, and trust

The upstream [profile package](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8/p83_profiles)
and [exclusion package](https://github.com/helgithorskarp/math_results/tree/main/sidon_ramsey_8/p83_exclusion)
were checked at source commit `d198c6081c400f4096b53bb7737ca014442fd160`.
The profile directory is unchanged from its cited commit
`8260966e2282526ee33048803ce7d59c7a04844c`. I verified both source manifests and
fetched all 31 relevant source/input files from public main, matching every byte.

I verified the definition and the published upper bound 86 in Espinosa-García and
Pellicer, [Update on Sidon–Ramsey numbers](https://arxiv.org/abs/2309.08553),
Theorem 4.1 and Table 2; the journal version is
[Discrete Applied Mathematics 378 (2026), 120–124](https://doi.org/10.1016/j.dam.2025.07.002).
The explicit lower-bound witness matches Xiu, Fan, and Liang,
[On Disjoint Golomb Rulers](https://arxiv.org/pdf/1405.4535), Table I, row \(I=8\),
page 6. Its coverage and pair sums are also checked directly, so the lower bound
does not depend on trusting their search.

Candidate-specific searches for Sidon–Ramsey bounds, the number 83, and the
five-ten compatibility method located no independent published bound at 83 or
stronger. This supports a potentially new published-literature improvement,
not a priority guarantee. In the committed graph, it improves the earlier bound
84. Historical priority and journal acceptance are not established by this review.

Residual trust is in the written proofs, audited unformalized exact code, GCC and
its standard libraries, CPython, the operating system, and hardware. The upstream
methods share the mathematical reduction, canonical convention, and portions of
search/control logic; agreement does not eliminate all possible common errors.
Hashes establish source/input/output identity, not completeness by themselves.
There is no formal proof-assistant certificate, independently rebuilt third
whole search, or independent verification of the authors' historical runtimes.
No solver timeout, floating tolerance, LP optimum, or externally supplied large
catalogue is a mathematical premise.

## Material objections and minimal closure conditions

No mathematical defect was found in the written proof
or the audited computation-to-theorem interfaces. The trust limitations above
must remain explicit whenever this is described as an exact computer-assisted
theorem. The small public terminal-example files alone are not a full certificate;
the complete regenerated search is essential. No correction to the mathematical
claim is presently indicated. A conventional paper should consolidate the profile
and completion arguments and preserve the pinned source and reproduction path.
Formal certification would reduce the trust boundary but is not required to make
this an honest computer-assisted result.

## Strengthening and improvement opportunities

1. **Proved small refinement.** The checked maxima already permit
   \(M'=3,999,996\), since this is the crude nine-point cap and exceeds both
   catalogue maxima. Thus the three-eleven union cutoff can rise from
   11,134,774 to 11,134,794, and the universal heavy-ten cutoff from 3,567,387
   to 3,567,399. These arithmetic implications are proved; no new case counts,
   runtime improvement, or stronger bound on \(SR(8)\) is claimed.
2. **Highest mathematical value: the P82 decision.** The proven absence of
   twelve-sets applies to its subinterval, but the eight deficits now sum to six,
   yielding eleven possible profiles before further restrictions. A P82 phase
   needs its own complete weight/profile reduction and compatibility search.
   Neither the P83 profile nor the failure of extensions of the published P80
   witness can replace that global obligation. This is a research direction,
   not a result of this review.
3. **Reduce the certification burden.** Formalize the generic weighted
   heaviest-class cover lemma, including the exceptional smaller final class,
   then certify catalogue generation and subset-query completeness against it.
   This would isolate the shared trust in the two implementations. The generic
   ordering argument itself is elementary; no independent novelty is claimed
   for that abstraction.

## Public review evidence and reproduction

[Review, independent checker, reproduction driver, and compact expected results](https://github.com/njallskarp/math_source_code_open/tree/main/sidon_ramsey_8_p83_independent_review).
The verified evidence commit is recorded in the signed graph review.

From the evidence repository root, with `CXX` selecting GCC with C++20 support:

```sh
CXX=g++ python3 -B sidon_ramsey_8_p83_independent_review/reproduce.py --work /tmp/p83-independent-review --jobs 4 --shards 6 --workers 6
```

The work directory must be new. This regenerates all inputs from the pinned
upstream commit, executes both full drivers including sanitizer controls, and
runs the independent checker. Expected final line:

```text
VERIFIED: full P83 profile and exclusion replay plus independent terminal audit
```

The two underlying public drivers and the separate referee audit were actually
executed in this review. The convenience wrapper was added afterward and was
not run as a second complete replay; it runs the same commands sequentially,
whereas the reviewed executions overlapped. The validated constituents and exact
source versions are recorded in the public package. Allow about 25 GB of
temporary disk. Large traces, catalogues, terminal dumps, logs and binaries are
regenerated outside Git; they were not published. This publication contains only
compact source, documentation, hashes and expected numerical evidence.
