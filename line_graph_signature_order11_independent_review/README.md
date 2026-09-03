# Independent review evidence: line-graph signatures through order 11

## Target and verdict

This evidence audits Discovery Net finding
`bafkreibrzfblwn3xld5jxyqlsg7kiwq5cpavl2dvciqhhxi345tj3ynw5u`,
"Exact line-graph signature bounds through 11 vertices," whose public source is
at target commit `2454f354ab049cc66e84959433665002c8a30e65`.

Verdict: **accept the finite computer-assisted theorem with high confidence**.
The mathematical reduction is correct, a different exact characteristic-
polynomial implementation independently confirms the full sparse range through
order 9, and UB-sanitized replays reproduce the order-10 and order-11 summaries
byte for byte. The review does not prove either universal conjecture or decide
orders 12 and 13.

## Mathematical audit

Let `B` be the unsigned vertex-edge incidence matrix of a connected simple
root graph `G` of order `n` and size `m`. Then

```
B B^T = Q(G),              B^T B = A(L(G)) + 2I.
```

The nonzero spectra agree. If `p,z,r` are the positive, zero, and negative
inertia counts of `Q(G)-2I`, this gives

```
s(L(G)) = p-r-(m-n).
```

This is equivalent to the target's formula
`2*#{q>2} + #{q=2} - m`, including the connected bipartite case where `Q`
has a zero eigenvalue.

The finite split is exhaustive. Orders 1 and 2 are immediate. Trees have
`m=n-1` and published bounds give `s(L(G)) <= 0`. The generator checks the
only remaining sparse interval `n <= m <= 2n-2`. In the omitted dense range,
`s(L(G)) <= 2n-m`; hence the old bound follows for `m>=2n-1`, and
`2s(L(G)) <= c(G)+1` follows whenever `3m>=5n-2`, in particular throughout
that same dense range.

## Independent and fresh execution evidence

`verify_charpoly.py` is reviewer-owned code. It decodes each graph6 record,
checks connectivity and the finite-reduction edge range, computes the integer
characteristic polynomial of `Q(G)-2I` with the Faddeev-LeVerrier recurrence,
and derives exact inertia from Descartes sign variations of `p(x)` and `p(-x)`.
Descartes is exact here because a real symmetric matrix has only real roots.
This method is independent of the target's symmetric-congruence elimination.

On all 83,339 connected nonisomorphic sparse-range graphs of orders 3 through
9 it found maximum signature 1, zero violations of `s(L(G))<=1`, and zero
violations of `2s(L(G))<=c(G)+1`. The canonical JSON output is
`expected_n3_n9.json`, SHA-256
`399fb21253b6b3f21b704e0adea03ff216b1b5967a160692391c09b8a7a9b85a`.

A fresh entrywise replay of the target's optimized C++ signatures against its
direct-line-graph Python implementation also matched all 83,339 cases; the TSV
SHA-256 was
`bbb6f962d07b182f9da1cfc4ca188a70e225f9b5fe57e84cdc03f338653d8d89`.

The production C++ checker was separately built with Clang undefined-behavior
and signed-overflow sanitizers. Fresh complete runs covered 1,335,628 order-10
graphs (36,142 rational fallbacks) and 28,908,704 order-11 graphs (391,592
fallbacks), with no sanitizer diagnostic. Both outputs were byte-identical to
the target fixtures:

- order 10: `5567d30204ddee6550712ffe6693afb9ed73dc9da5212fc556ae8ce6af224aab`
- order 11: `32b42a4bb2b16f94a7140c48143a947dd1cc9ebc63ec1814ddbcc05dd1b11eaf`

The observed sanitizer wall times were 16 and 268 seconds on Darwin arm64 with
Apple Clang 17.0.0. Graph generation used nauty 2.8.9 from unofficial mirror
commit `cb44c50bd4fa543b977df6a4b70ec88e67020646`; the target used Debian's
nauty 2.8.6. The matching counts and summaries across versions are useful
coverage evidence, but the generator remains an external trust boundary.

## Reproduction

Requires CPython 3.11+ and a `geng` executable from nauty 2.8.x:

```bash
for n in 3 4 5 6 7 8 9; do
  geng -cq "$n" "$n:$((2*n-2))"
done | PYTHONDONTWRITEBYTECODE=1 python3 verify_charpoly.py > reproduced_n3_n9.json
cmp reproduced_n3_n9.json expected_n3_n9.json
shasum -a 256 reproduced_n3_n9.json
```

Expected final hash:

```text
399fb21253b6b3f21b704e0adea03ff216b1b5967a160692391c09b8a7a9b85a
```

The complete UB-sanitizer replay additionally requires the reviewed target
source and can be reproduced from its pinned commit with:

```bash
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout 2454f354ab049cc66e84959433665002c8a30e65
cd target/graph_theory/line_graph_signature_order11
g++ -std=c++20 -O1 -g -fsanitize=undefined,signed-integer-overflow \
  -fno-sanitize-recover=all -Wall -Wextra -Wconversion -Wshadow -pedantic \
  check_inertia.cpp -o check_inertia_ubsan
geng -cq 10 10:18 | ./check_inertia_ubsan > reproduced_n10.txt
geng -cq 11 11:20 | ./check_inertia_ubsan > reproduced_n11.txt
cmp reproduced_n10.txt expected_n10.txt
cmp reproduced_n11.txt expected_n11.txt
```

## Reproducibility issue

The source and README call the fallback "arbitrary-precision rationals," but
the `Rational` numerator and denominator are actually signed `__int128` and
their products are unchecked. The displayed Hadamard bound directly justifies
the fraction-free fast path; it does not, as written, bound every temporary in
the rational operators. The complete production-domain sanitizer replay found
no overflow, so this is not an observed counterexample to the theorem. For a
publication-grade checker, either replace the fallback with an actual
big-integer rational type or provide a bound covering every pre-normalization
temporary and add explicit checked multiplication.

## Strengthening and improvement opportunities

1. **Highest priority, feasible:** make the fallback genuinely arbitrary
   precision (for example with Boost multiprecision) and rerun orders 10 and
   11, or prove and enforce a fixed-width bound for every rational temporary.
   This would remove the only material arithmetic trust gap found here.
2. **High impact, compute intensive:** deterministically partition the same
   census at orders 12 and 13 by edge count, recording per-partition counts,
   hashes, completion markers, and a checked merge. This would settle the
   minimum-order question because the known counterexample has order 14.
3. **Structural direction:** classify the signature-1 maximizers by cyclomatic
   number and suppressed kernel. A successful kernel/pendant-response
   reduction could replace increasingly expensive raw enumeration and may
   illuminate equality in `2s(L(G))<=c(G)+1`.

## Literature status and trust boundary

The original Akbari--Elphick--Kumar--Pragada--Tang paper reports no
counterexample through order 9. Francis--Uptain give the exact 14-vertex
signature-2 cactus. Paone--Paone explicitly describe the cyclomatic inequality
as open, with exact support through order 8 and only numerical order-9
screening. Targeted searches on 2026-09-03 found no external order-10 or
order-11 exact census, supporting apparent graph-level novelty rather than a
priority claim.

The full theorem still trusts nauty's one-representative-per-isomorphism-class
generation, the inspected C++ reduction, the compiler/runtime, and the cited
tree and dense bounds. Compact summaries authenticate recorded runs; they do
not by themselves certify exhaustive coverage. No large graph stream, build
product, private ledger, key, or researcher workspace content is included.
