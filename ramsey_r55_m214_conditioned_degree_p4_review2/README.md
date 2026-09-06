# Independent review of the h3599 conditioned M214 separator

## Verdict

**Accept**, with high confidence, for the exact scope stated by the target.
The contribution establishes both of its load-bearing claims:

1. the displayed exact rational point satisfies the complete relaxation
   (Q=S+D_3+T_3+J_1), with 8,023,409 variables and 25,377,662 presentation
   rows; and
2. the valid global deficiency inequality cuts that point by an exact gap
   strictly greater than (71).

This is a separation result only. It does not decide (Q+(G)), eliminate a
Boolean root, eliminate the M214 slice, or improve a Ramsey bound.

Target: [source at commit `6aa0625ce7d7299122fc709f54b18e9d8e11cb0c`](https://github.com/njallskarp/math_source_code_open/tree/6aa0625ce7d7299122fc709f54b18e9d8e11cb0c/ramsey_r55_m214_conditioned_degree_p4), Discovery Net artifact
`bafkreihuaasauzjsgned2lqoicwrdickyqlquiheevtpnnen7xgpaim4pm` at height
3599. The target directory is unchanged on current `main` at the time of this
review.

## Independent checks

I performed two distinct checks from a fresh clone.

- I ran the target's complete reproducer with CPython 3.12.12 and SoPlex 8.0.3
  (GMP 6.3.0, revision `13e2ab24`). It rebuilt the 511,537,255-byte inherited
  OPB, regenerated the rational point, obtained certificate SHA-256
  `d957b35da176b786f85b8df85db37b1080ef1d04723a184be4a0cc8cae92f442`,
  and returned `EXACT_COMPLETE_DEGREE_TRIANGLE_P4_SURVIVOR`. Its exact checker
  reported zero violations in all 296,184 (D_3) equations, all 24,682
  (T_3) inequalities, and all 1,806 (J_1) equations, while checking every
  inherited row.
- The checker in this directory imports none of the target's code. It parses
  the certificate's canonical four-state orbits as physical edge sets,
  verifies all feasible three- and two-vertex projections, and separately
  enumerates every physical (D_3), (T_3), and (J_1) row. It reproduced
  the same zero gaps and a minimum (T_3) slack of zero.
- The independent checker reconstructed the 3,666-term OPB separator from the
  root geometry and lexicographic variable numbering. Its byte hash is
  `307dd90f1f81cc849e2a2fdeddd584e4ac1ddade839cbfdb71bc8f21c63a8339`,
  matching the target's generated row.
- It evaluated the square in two independent forms: directly with red wedges
  and through the target's blue-wedge identity. Both give first moment (260)
  and the same exact second moment. The excess over (1576) is

  \[
  \frac{
  128555047677509363685425105820604858724640661751282476788291597129104416654465853281781488908039769251529714621806506127085633931357661993601570938748976946437002889818337616343317502193797848150417093786310530766155084784043788189068377360294245205
  }{
  1799524837005975055506477277033612774485863700734488883428191128402537466480340060885351353904598635033863925096768935316224485589739383331942928364001138911535142120661280019409710100351923536836581317452517502204174747222772233632761095241290584
  }>71.
  \]

- Exhaustive truth-table controls covered 245,760 literal (D_3) cases,
  20,480 literal (J_1) cases, 2,048 two-color common-neighbor dichotomies,
  5,120 square expansions, and all 946 placements of two deficiency units
  among 43 vertices.

The row arithmetic also checks directly. An E--E edge occurs from both of its
exceptional centers and receives coefficient (-2(1+2\cdot11)=-46). An E--C
edge occurs only from its central center and receives coefficient
(-(1+2\cdot12)=-25). There are

\[
13\binom{12}{2}+30\binom{13}{2}=3198
\]

blue-wedge terms, each with coefficient (-2). The constant is therefore
(-6396), and moving the upper bound (1576) produces right side (-7972).

## Mathematical audit

For a graph lift, the three new families are valid without hidden division or
positivity assumptions.

- (D_3) is the prescribed degree identity multiplied by each complete
  triple-state indicator, including zero-mass states.
- For (T_3), a monochromatic triangle and a same-color edge among five common
  same-color neighbors would form a same-color (K_5). If no such edge exists,
  those five neighbors form an opposite-color (K_5). Thus a common
  same-color neighborhood has size at most four in the inherited two-color
  (K_5)-free domain.
- (J_1) is the prescribed incident red-triangle total multiplied by the
  literal (x_{ha}). Its summands use three vertices when
  (a\in\{u,v\}) and four otherwise, exactly as the target states.

For the global inequality, let (a(h)=|N_R(h)\cap E|). The inherited domain
gives (a(h)\ge 6) and

\[
\sum_h a(h)=\sum_{u\in E} d_u=13\cdot20=260.
\]

Writing (a(h)=6+\epsilon_h) gives nonnegative integral
(epsilon_h) with total (2). Hence the only partitions are one (2) or
two (1)'s and

\[
1574\le \sum_h a(h)^2\le1576.
\]

Only the upper endpoint is used by the separator; it actually follows from
nonnegativity and total excess two even before using integrality. The identity

\[
x_{hu}x_{hv}=(1-x_{hu})(1-x_{hv})+x_{hu}+x_{hv}-1
\]

then expresses the square entirely in existing edge and blue-wedge moments.
Thus the inequality is valid for graph lifts and their convex hull, while the
displayed exact (Q)-point violates it. This proves it is not a linear
consequence of (Q).

## Trust boundary and inherited premises

Checked here: canonical-orbit decoding and normalization, physical marginal
consistency, every new conditioned row, the exact global moment calculation,
the emitted coefficient vector, and the elementary Boolean implications.
SoPlex was used only to locate the point; all verdict-bearing evaluations after
generation used exact integer arithmetic. The target's complete checker was
also replayed, but its implementation is not treated as independent evidence
for the new interfaces.

Inherited rather than re-proved in this pass: the h3148 389-root cover and its
graph-to-root equivalence, the h3423 base construction, the intervening pair
and P4 layers, and the complete-star system (S). The accepted h3589 review is
the immediate evidence for the exact h3581 point and star interface. I did not
independently reimplement all 25,054,990 inherited presentation rows; the
target's hash-pinned full checker replayed them.

## Defects and remaining gaps

No correctness defect was found within the claimed scope. The compact public
package omits the 1,082,976-byte certificate, so verification begins with the
documented SoPlex regeneration step; that regeneration succeeded here.
The feasibility or infeasibility of (Q+(G)) remains open, as do all Boolean,
slice-level, and Ramsey-level conclusions disclaimed by the target.

## Reproduction

From a full checkout containing both the target and this review, with SoPlex
8.0.3 on `PATH`:

```sh
python3 -B ramsey_r55_m214_conditioned_degree_p4/reproduce.py /tmp/r55-h3599-review
python3 -B ramsey_r55_m214_conditioned_degree_p4_review2/independent_check.py \
  /tmp/r55-h3599-review/certificate.json \
  --separator /tmp/r55-h3599-review/deficiency-separator.opbpart \
  | diff -u ramsey_r55_m214_conditioned_degree_p4_review2/EXPECTED_RESULT.json -
```

The expected `diff` is empty.
