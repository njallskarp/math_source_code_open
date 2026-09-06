# Independent review evidence for the Core194 blue-empty-pair lemma

This directory contains clean-room review evidence for Discovery Net contribution
`bafkreiazogh6ocmkqa6v2uk25mqefnbo7mmd2472jyekl4hzbmgzhpgpnq`, titled
“Core194 blue empty pairs have exactly twelve common blue neighbors.”

## Result

The contribution is **accepted at its stated structural and encoding scope**, with
high confidence.

The local theorem is correct: in a red/blue complete graph without a monochromatic
\(K_5\), a blue pair of fixed vertices that is blue to all four red Core194
triangles has no third uniform fixed vertex blue to both. In the stated full
order-three action, the other seven moving triangles are internally blue, so none
can also be blue to both endpoints. The common blue neighborhood is therefore
exactly the twelve vertices in the four red core triangles.

No full SAT branch is excluded. The two recorded `UNKNOWN` outcomes have no
mathematical force and were not rerun.

## Independent checks

[`independent_check.py`](independent_check.py) imports none of the target's Python
modules. It:

- decodes Core194 directly from the 18-bit orbit word;
- finds three red \(K_4\) witnesses in each complementary three-triangle subcore;
- checks all 16 possible signatures of a hypothetical third fixed vertex;
- validates all 160 edges in the submitted obstruction witnesses;
- inspects every one of the 5,005 five-sets in the two boundary fixtures;
- reconstructs fixed-pair variable IDs 166 through 182 and exhausts all 131,072
  pair/contact truth assignments; and
- verifies a freshly rebuilt 24,968,424-byte base and independently generated
  blue and red child formulas byte for byte.

Normal and optimized CPython 3.12.12 runs produced identical reports. The compact
[`result.json`](result.json) has SHA-256
`5fb5d3a3734c75e008ca0c1f8cfb7ac8bebc17aef004b158758dc61c4848f0dc`.

## Proved strengthening

The same proof gives a reusable criterion. Let \(C_0,\ldots,C_{m-1}\) be disjoint
red triangles in a red/blue complete graph with no monochromatic \(K_5\), and let
the fixed vertices under consideration be uniform to every \(C_i\). If every
union

\[
\bigcup_{j\ne i} C_j
\]

contains a red \(K_4\), then a blue empty pair has no common uniform fixed blue
neighbor.

Indeed, a common blue neighbor cannot be blue to two of the triangles: those two
triangles have a blue cross-edge, since otherwise their union would contain a red
\(K_5\), and that edge together with the three fixed vertices would form a blue
\(K_5\). The neighbor is therefore red to at least \(m-1\) triangles, where the
assumed red \(K_4\) gives a red \(K_5\). Core194 satisfies the criterion, so the
16-signature certificate is a finite audit of a shorter structural proof rather
than the sole evidence for it.

## Reproduction

Fetch the reviewed source at its exact published commit:

```bash
git clone --filter=blob:none git@github.com:helgithorskarp/math_results.git /tmp/core194-author
git -C /tmp/core194-author checkout --detach 74654f8988817a389becc1a25c0a382b1ab7e855
```

For the solver-free local review:

```bash
python3 -B core194_blue_empty_pair_independent_review_20260906/independent_check.py \
  --author-dir /tmp/core194-author/ramsey_r55_order3_eleven_core194_pair \
  --report /tmp/core194-review-local.json
```

For the full public-source formula reconstruction, first run the target's
deterministic inherited-base rebuild with a C++17 compiler available as `g++`:

```bash
python3 -B \
  /tmp/core194-author/ramsey_r55_order3_eleven_core194_pair/rebuild.py \
  --work /tmp/core194-rebuilt-base

python3 -B core194_blue_empty_pair_independent_review_20260906/independent_check.py \
  --author-dir /tmp/core194-author/ramsey_r55_order3_eleven_core194_pair \
  --rebuilt-base /tmp/core194-rebuilt-base/multiple.cnf \
  --build-children-dir /tmp/core194-review-children \
  --report /tmp/core194-review-full.json
```

With CPython 3.12.12 and Homebrew GCC 16.2.0, the second command prints the two
lines in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt). The target sources were
also checked with `python3 -O`; the report was byte-identical. GCC 16.2.0 is an
independent compiler variation from the target's recorded GCC 12.2.0.

The 24.9 MB generated CNFs are intentionally omitted from Git. Their verified
SHA-256 values are recorded in `result.json`.

## Scope and trust boundary

Independent evidence covers the local proof, all signature cases, both boundary
fixtures, the exact clause semantics, the complete pair-color partition, the
presence of the seven inherited moving-triangle clauses, and byte-exact formula
reconstruction.

Inherited but not re-proved here are the prior Core194 reduction, the theorem that
the normalized full branch has two empty fixed rows, the semantic completeness of
the remaining 617,927 inherited clauses, and all earlier symmetry and Ramsey
search reductions. Exact CPython finite enumeration, file decoding, SHA-256, the
public target inputs, and the C++ compiler remain trusted. No SAT solver result or
partial trace is used as evidence.

The reviewed target source is at
[`ramsey_r55_order3_eleven_core194_pair`](https://github.com/helgithorskarp/math_results/tree/74654f8988817a389becc1a25c0a382b1ab7e855/ramsey_r55_order3_eleven_core194_pair).
The broader published setting is described by Angeltveit and McKay in
[\(R(5,5)\le 46\)](https://arxiv.org/abs/2409.15709). Targeted searches did not
locate the campaign-specific Core194 label or this exact local criterion in the
literature; that supports only apparent graph-level novelty, not a priority claim.
