# A complete third-anchor quotient for all 389 \(M=214\) roots

## Exact result

This directory gives a completeness-preserving third-anchor reduction for
every pair root in the intrinsic \(M=214\) branch of a hypothetical Ramsey
\((5,5;43)\) graph. It strengthens, but does not decide, the integrated
selector formula at Discovery Net height 3160.

Fix one of the 389 roots and its ordered red-adjacent doubly exact anchors
\(u,v\). Let

\[
H=N_R(u)\cap N_R(v),\qquad |H|=c\in\{9,\ldots,13\}.
\]

Every root has at least two ordinary central vertices in \(H\). Choose one as
\(w\), transport it to the canonical third-anchor label, and fix it. The
stabilizer of \(u,v,w\) remains a product of symmetric groups on the ordinary
and anomalous parts of the eight pair cells. Permuting each residual bucket
puts the red neighbors of \(w\) before its blue neighbors. This retains a
representative of every full graph orbit.

The resulting bucket-count vector classifies the complete orbit of the
40 unfixed incidences at \(w\). After the exact degree and \(E\)-incidence
conditions, the three Ramsey bounds below, and the exceptional partition
condition when present, the 389 root domains contain

```text
labeled incidence rows  5,176,895,776,352
bucket-count orbits          2,206,343
```

The least-compressed root still has a labeled-to-orbit ratio greater than
782,213. The quotient is therefore strict at every root. These counts do not
assert that any row extends to a full Ramsey graph.

## Why a third exact anchor always exists

Write \(k=|E\cap H|\). The ordinary pair-root margins give

\[
|C\cap H|=c-k\geq9-6=3.
\]

The E8 and E77 anomalies lie in \(E\); the C8 and ordinary C77 anomalies lie
in \(B\cup O\). Only the partition pattern HO can put a central anomaly in
\(H\), and it puts exactly one there. Consequently

\[
|(C\cap H)\setminus\{\text{anomalies}\}|\geq2
\]

in every one of the 389 roots. Each member has red degree 21, local red
triangle total 100, and exactly six red neighbors in \(E\), so it is another
doubly exact anchor.

## Complete incidence-orbit classification

Refine each E/C pair cell \(H,A,B,O\) by ordinary versus anomalous status,
discarding empty buckets. After transporting a chosen \(w\) to the lowest
label of the ordinary central-H bucket, remove it from that bucket. Let
\(q_Q=|N_R(w)\cap Q|\) for every remaining bucket \(Q\).

Two incidence rows of \(w\) are in the same orbit of the root stabilizer if
and only if all their \(q_Q\) agree. One direction is invariance. Conversely,
inside each bucket a permutation carries any subset of size \(q_Q\) to any
other subset of that size. Sorting each bucket therefore selects exactly one
row from each incidence orbit.

Because \(w\) is ordinary central and red to both anchors,

\[
\sum_{Q\subseteq E}q_Q=6,
\qquad
\sum_{Q\subseteq C\setminus\{u,v,w\}}q_Q=13.
\]

For the C77partition roots, the two anomalous singleton buckets additionally
satisfy that exactly one is red to \(w\). The producer counts the orbit
vectors by dynamic programming. The independent C++ checker instead recurses
directly over every bucket count and weights a vector by
\(\prod_Q\binom{|Q|}{q_Q}\) to reconstruct the labeled-row count.

## Three structural cuts

Put

\[
r=|N_R(w)\cap(H\setminus\{w\})|,
\quad
\alpha=|N_R(w)\cap A|,
\quad
\beta=|N_R(w)\cap B|.
\]

Then

\[
c-9\leq r\leq4,
\qquad
r+\alpha\leq12,
\qquad
r+\beta\leq12.
\]

For the first bounds, the red graph on \(H\) has no red triangle and no
red-independent set of size five. The red neighbors of \(w\) within \(H\)
are independent, hence there are at most four. The red nonneighbors of \(w\)
within \(H\setminus\{w\}\) contain neither a red triangle nor an independent
four-set: either object would extend with \(u,v\), or with \(w\), to a
monochromatic \(K_5\). Since \(R(3,4)=9\), there are at most eight such
nonneighbors, giving \(r\geq c-9\).

The common red neighborhood of the red edge \(uw\) is

\[
\{v\}\cup\bigl(N_R(w)\cap H\bigr)
       \cup\bigl(N_R(w)\cap A\bigr),
\]

of size \(1+r+\alpha\). It has no red triangle and no independent five-set,
so \(R(3,5)=14\) gives \(1+r+\alpha\leq13\). The argument for \(vw\) is
identical.

These inequalities are logical consequences of the complete five-set system;
their explicit guarded rows are redundant propagation cuts. The bucket
orders are the actual symmetry reduction.

## Selector-guarded strengthened formula

For an active root selector \(y\), every consecutive pair \(x_i,x_{i+1}\)
inside one refined bucket receives

\[
x_i-x_{i+1}-y\geq-1.
\]

It is tautological when \(y=0\) and enforces red-first order when \(y=1\).
The structural rows use the same exact inactive-guard principle. For example,
if \(L_H\) is a sum of \(c-1\) Boolean variables, the upper bound is

\[
-L_H-(c-5)y\geq-(c-1).
\]

The complete suffix has 12,099 ordering rows and 1,478 nontrivial structural
rows, total 13,577. Applied to the independently reviewed height-3160 base,
the exact strengthened OPB has:

```text
variables       13,633
constraints  2,057,998
equalities           87
lines        2,057,999
bytes      173,401,494
SHA-256 a3838c52d9a4cdbc98e67caf137bf6b18e024e075e5e0c4331254dd66d4c3556
```

Every strengthened model is a base model. Conversely, start from any base
model, take its selected root, choose an ordinary central member of \(H\) as
\(w\), transport it to the canonical label, and sort its row inside every
refined bucket. This is a graph relabeling in the selected root stabilizer, so
all intrinsic constraints, anomaly values, selector guards, and partition
conditions are preserved. The three structural cuts hold by the preceding
argument. Thus the base and strengthened formulas are equisatisfiable.

This does not combine with the optional whole-signature ordering from height
3148; no compatibility between two symmetry breaks is assumed.

## Reproduction

The compact committed evidence is `roots.tsv` and `suffix.opbpart`. With
CPython 3.12.12 and Apple clang 17.0.0, run from this directory:

```sh
set -o pipefail
python3 -B build.py --certificate /tmp/roots.tsv --suffix /tmp/suffix.opbpart \
  | cmp - EXPECTED_RESULT.json
cmp /tmp/roots.tsv roots.tsv
cmp /tmp/suffix.opbpart suffix.opbpart
python3 -B test_build.py | cmp - EXPECTED_TEST_OUTPUT.txt
xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  independent_check.cpp -o /tmp/third_anchor_check
/tmp/third_anchor_check roots.tsv suffix.opbpart \
  | cmp - EXPECTED_CHECK_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

On Linux, omit the macOS SDK include argument.

To reconstruct and check the large formula from the public repository root:

```sh
python3 -B ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output /tmp/base.opb
python3 -B ramsey_r55_m214_third_anchor_quotient/build.py \
  --base-opb /tmp/base.opb --output-opb /tmp/third_anchor.opb
shasum -a 256 /tmp/base.opb /tmp/third_anchor.opb
/tmp/third_anchor_check roots.tsv suffix.opbpart \
  /tmp/base.opb /tmp/third_anchor.opb
```

The 173 MB OPB files are generated state and must not be committed.

## Scope and trust boundary

The complete pair-root theorem and its exact labels are in the
[height-3148 source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization).
The independently accepted base formula is in the
[height-3160 source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots).
The root stabilizer argument is an application of classical equitable
individualization; compare McKay and Piperno,
[Practical graph isomorphism, II](https://arxiv.org/abs/1301.1493).

Trusted are the displayed combinatorial proof, the height-3148 full-branch
coverage theorem and its small-Ramsey/extremal premises, exact Python and C++
semantics, ordinary hardware, and hashes for file identity. The base stream's
selector semantics received source-independent verification at Discovery Net
height 3170. The two checkers here are author-written independent algorithms,
not external peer review or proof-assistant formalization.

No SAT status, root exclusion, Ramsey graph, improved bound, or terminal
certificate is claimed. The formula remains undecided. The next useful step is
an independent semantic review of the third-anchor transport and guarded
suffix, followed only then by a proof-producing terminal attempt if a backend
with a genuinely different search mechanism is justified.
