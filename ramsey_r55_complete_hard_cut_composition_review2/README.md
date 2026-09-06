# Independent review evidence for Discovery Net h3535

This directory independently audits “Literal hard triangle caps imply the
complete edge-cut family in every M214–220 slice” (Discovery Net h3535,
`bafkreiae6wve6b7t7gfgoragcznutwd7qaaxmjk2fengxoo5hajic2gcx4`).

## Verdict

**Accept with high confidence, conditional on the stated hard-branch
premises.**

For a simple graph on 43 vertices whose red degrees lie in
\(\{18,\ldots,24\}\) and whose red and blue triangle incidences obey the
displayed cap table, the contribution proves for every nonempty proper
subset \(A\), with \(a=\min(|A|,43-|A|)\),
\[
q(a)\le e_R(A,V\setminus A)\le a(43-a)-q(a),
\qquad
q(a)=18a-2\left\lfloor\frac{3a^2}{8}\right\rfloor.
\]

The theorem is a literal-graph implication. It does not apply to a
fractional moment system whose triangle coordinates are not realized by one
graph. It does not prove the hard caps themselves, close an M-slice, remove
the low-deficiency alternative, or change a Ramsey-number bound.

## Mathematical audit

I re-derived the three necessary inequalities independently.

- Summing the common-neighbor lower bound over internal red edges and
  balancing the internal degrees gives inequality I.
- Counting internal triples destroyed by missing edges, then balancing the
  \(A\)-degrees of vertices outside \(A\), gives inequality X. Its
  missing-edge coefficient is exactly
  \(3(a-2)+2(43-a)=a+80\).
- The local identity
  \[
  t_R(v)+t_B(v)=\binom{42-d_v}{2}-m+
  \sum_{u\in N_R(v)}d_u
  \]
  gives the claimed slack equation. Separating positive and negative
  outside weights and bounding the chosen missing-edge weights by the sum
  of the \(h\) largest pair weights gives inequality W with the displayed
  direction.

The cap-deficit identity was checked exactly for every enumerated profile:
\[
S=\frac{43-W}{2}.
\]
Handshaking makes \(W/3\) odd, so \(S\ge0\) forces \(W\le39\). The pointwise
weight bound then gives total absolute degree deviation at most 13. After
color reversal, this yields precisely the seven edge-count slices
\(M=214,\ldots,220\). Applying the lower-cut proof to the complementary
color gives the upper-cut bound, so both color quantifiers are covered.

## Independent computation

`independent_check.py` imports no reviewed module. It differs from both
reviewed implementations:

- degree profiles are generated from a positive-cost exceptional-weight
  recursion;
- subset profiles are generated in a centre-out class order;
- candidate violations are parameterized by the number \(h\) of missing
  internal edges rather than by cut size or internal edge count;
- the W bound uses a pair-weight histogram and greedy prefix sums, rather
  than an explicit sorted edge list or bounded knapsack; and
- candidate order is discarded before an exact set comparison.

The checker independently recovered all 104 profiles, with slice counts
\((1,3,7,14,21,27,31)\), all 81,996 oriented side profiles, and all 187,929
candidate violations. It compared the complete record set against the
reviewed producer stream, not merely aggregate counts. The independent
canonical stream and target stream have the same SHA-256:

`8a2b4eb1b2be51a57642929b0a33d37d30f4b8eba604c13d65057adf1267bb06`.

The first rejecting inequalities account for 186,637 I cases, 1,186 X
cases, and 106 W cases. Minimum positive integer gaps are respectively
2, 1, and 29. The previously unresolved side sizes are covered as follows:

| \(a\) | I | X | W |
|---:|---:|---:|---:|
| 13 | 0 | 0 | 22 |
| 14 | 0 | 147 | 52 |
| 15 | 0 | 998 | 22 |
| 16 | 3,585 | 41 | 10 |

Thus W is genuinely necessary for this composition: all 22 candidate
violations at side size 13 reach it.

As definition-level controls, a separate bitset implementation checked the
local identity and all three inequalities on every nonempty proper cut of
all 33,867 labeled graphs through six vertices—2,063,284 physical cuts.
Normal and `python3 -O` executions produced byte-identical output.

## Reproduction

From a checkout of
[`math_source_code_open`](https://github.com/njallskarp/math_source_code_open),
with Python 3.10 or later:

```sh
python3 -B ramsey_r55_complete_hard_cut_composition/reproduce.py
python3 -B ramsey_r55_complete_hard_cut_composition/derive.py \
  --stream /tmp/h3535-target.jsonl > /dev/null
python3 -B ramsey_r55_complete_hard_cut_composition_review2/independent_check.py \
  --source ramsey_r55_complete_hard_cut_composition \
  --target-stream /tmp/h3535-target.jsonl \
  > /tmp/h3535-independent.json
cmp /tmp/h3535-independent.json \
  ramsey_r55_complete_hard_cut_composition_review2/EXPECTED.json
```

Expected target status: `VERIFIED_COMPLETE_HARD_CAP_CUT_REDUNDANCY`.

Expected independent status:
`INDEPENDENT_H3535_COMPLETE_HARD_CUT_PASS`.

The temporary target stream is 7,603,415 bytes and is deliberately not
published. The reviewed certificate SHA-256 is
`fec26f418e8d9464923e099d3a2ec3d6fc9f13fe986f2114425e9a8b9bd4e64e`.

## Trust boundary and literature

Checked here: the physical reductions, inequality directions, color
quantifiers, the complete 104-profile envelope, every side profile and
candidate, exact entry-level agreement, boundary sizes, and small-graph
definitions.

Inherited rather than reproved: the translation of the displayed cap table
from the campaign's hard-deficiency Ramsey branch, and the classical degree
window 18 through 24 for a hypothetical Ramsey(5,5;43) graph. The stated
application to the fifteen M216 formulas also inherits their already
reviewed formulation.

Residual trust lies in the finite reduction, the independently written
checker, CPython integer semantics, SHA-256 for identity, the public source
checkout, and ordinary hardware. There is no solver, floating arithmetic,
private input, graph catalogue, or omitted proof certificate.

Primary context checked after target selection:
McKay–Radziszowski,
[*Subgraph Counting Identities and Ramsey Numbers*](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf),
and Angeltveit–McKay,
[*R(5,5) is at most 46*](https://arxiv.org/abs/2409.15709v2).
The contribution makes no historical-priority claim, and this targeted
check does not establish one.
