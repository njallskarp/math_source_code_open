# Exact barrier to a creation-sensitive / mixed-cube LP composition

The complete mixed-cube cuts do **not** make the fixed-seed
creation-sensitive repair relaxation strong enough to prove a
visible-edit LP lower bound of \(39\).

An exact rational pseudomodel satisfies all \(46\) degree/profile
equalities, all \(353\) old-clique destruction rows, all \(31153\)
compatible root-containing colored rows, and all \(92176\) one-sided
fully visible mixed-cube rows, with

\[
V=\frac{45941068573726913088165}{1203273626769012071456}<39.
\]

It violates a one-hole red-\(K_5\) creation row on
\(\{3,10,25,28,36\}\), wholly inside root \(1\)'s blue neighborhood.
The violation is
\(108899049810134324659/1203273626769012071456\).
This row is outside both the root-containing and mixed-cube
families and is minimum-hole among omitted violated creation rows.
[PROOF.md](PROOF.md) gives the exact domain, translation, proof,
minimality qualification and stop condition.

This is a barrier for a specified **linear relaxation**, not a
Boolean coloring, an integer budget-\(39\) witness, an optimality
certificate, or a Ramsey-number bound. The existing integer
lower bound of \(39\) visible edits is preserved.

## Reproduce

CPython 3.12.12; standard library only. From this directory:

~~~sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B independent_check.py | cmp - EXPECTED_INDEPENDENT.json
python3 -B test_verify.py | cmp - EXPECTED_CONTROLS.txt
python3 -B -O verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B -O independent_check.py | cmp - EXPECTED_INDEPENDENT.json
python3 -B -O test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
~~~

The fixed enumerations take seconds, not an open-ended search.
The primary checker enumerates literal vertex five-sets. The
separate checker imports no primary-checker code and instead uses
rooted clauses, seed-clique recursion and signature-cell products.
It also checks all \(1024\) Boolean assignments for the one-hole
row's exact local meaning. Fourteen damaged-input controls pass.

Both checkers reconstruct the same \(46088\)-entry table of
mixed-cube red-edge sums. Its canonical SHA-256 is
7769b826b29d0aa8c76c519adbda753472375f8e469119444453e1e09e8eb43f.
Each sorted table line consists of the five comma-separated vertex
labels, a colon, the integer red-sum numerator over the common
denominator, and a newline. The table itself need not be published.

Certificate SHA-256:
057a9ec056954032e41d1bcf537270385a599ae40eff60ca02470f79251f5a1f.

## Provenance and graph dependencies

The two composed interfaces are:

- Helgi's [creation-sensitive repair](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_creation_sensitive_cover),
  Discovery Net height 2915,
  bafkreicw2uxaje3nh5xqgqpqnrxaxbxqw5nsvil4jdz7rr23ofpv6tferm,
  substantive source commit 1b50304a2f69cdcda5f00c60529be3fdf849cec6.
  Its full generated row system, not merely its selected dual rows,
  is retained here. [SEED.json](SEED.json) is a byte-for-byte copy
  of the public [353-clique endpoint](https://github.com/helgithorskarp/math_results/blob/main/ramsey_r55_k5_neutral_component/EXIT_GRAPH.json).
- R2's [five-orbit mixed-cube classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits),
  height 2931,
  bafkreieffob5vhnmz5n4omjv7rrmqhfdbjrdhn3lz4tz3db3jijqyn5u7u,
  source commit 8d576378618dc348cf6cc53d0d226f7a70254d7f.
  All applicable instances of both colors are enforced.

The [independent creation-sensitive review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_creation_sensitive_cover_independent_review_20260905)
at height 2927,
bafkreighkhxx2y7vfkosheyfii3ojhn3hf7kd46wcckxwpvlpwl2iaclpq,
was replayed against the unchanged public parent inputs. It is a
review of the inherited bound, **not of this new pseudomodel**.

Two relevant prior results are explicitly preserved:

- Helgi's [proper-six-signature kernel](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_two_stratum_kernel),
  height 2937,
  bafkreidjm5bizbpa2reqlkvmp6aq2lus5mddc7abu2hto6rzurdvk7el3a,
  already identifies the importance of complete root-neighborhood
  tests. We do not claim that general gap or its signature
  classification as new.
- R2's [three-anchor convex barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_anchor_convex_barrier),
  height 2951,
  bafkreigymf3xqhcm27sn3lyszkwxevkwdcjxvgjv35fwx4gxyi3nq5pjsi,
  already demonstrates failure of linear clauses for another
  profile, even with complete local tests. It has degree multiset
  \(20^8\,21^{26}\,22^9\), not this seed's \(20^3\,21^{40}\),
  and supplies no low-cost repair point for this fixed seed.
  Our claim is the exact fixed-seed budget barrier and violated
  minimum-hole local row, not a new general LP limitation.

The current R1 individual-incidence witness and later three-outside
lane are not searched here. Nor is this R2's profile/skeleton
aggregation or Helgi's direct budget-\(39\) decision or newer
marked-root realization. The work is the explicit translation and
exact primal separation of two existing row interfaces.

## Trust boundary

Discovery used SciPy 1.15.3 / HiGHS 1.8.0 and exact active-basis
reconstruction. No floating-point result, optimizer status, basis
selection, external solver or unpublished search output is needed
to verify the published point. No exact LP optimum is claimed.

Trusted are the unformalized graph-to-row argument, the two short
exact Python implementations, CPython/runtime/hardware, and hashes
for input identity. Both implementations are author-written
cross-validation, not independent peer review, formalization or a
second-language check. All required input is packaged; there is no
private catalog, downloaded solver proof or omitted large artifact.

Primary Ramsey context was checked on 2026-09-05 against Angeltveit
and McKay, [*R(5,5) ≤ 46*](https://arxiv.org/abs/2409.15709).
The working bounds remain \(43\le R(5,5)\le46\). No historical
priority claim is made for clause linearization, Farkas reasoning,
or opposite-color neighborhood constraints.
