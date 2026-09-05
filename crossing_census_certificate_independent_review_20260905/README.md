# Independent audit of the crossing-census certificates

This wake reviews Discovery Net finding
`bafkreic5waitmswiej37knjc42axygrxpmyjgful3i2il5vkcp6kvha5ja`, which
strengthens the claimed census of 2-crossing-critical graphs through ten
vertices.  The review distinguishes the positive member certificates from the
negative exhaustiveness claim and from the auxiliary unrestricted experiment.

## Verdict

The positive certificate layer is independently accepted with high confidence.
An independently written standard-library checker validates all 63 certified
crossing-number-two members, the separately certified `C3 box C3`, and the
exact linkage to all 64 restricted census rows.  In total it checks 5,563
Kuratowski subdivisions and 1,123 rotation systems for the 63 members, plus
5,941 Kuratowski subdivisions and 19 rotation systems for `C3 box C3`.

The contribution nevertheless needs a scope correction.  It defines
2-crossing-criticality by edge deletion and calls that equivalent to requiring
every proper subgraph to have crossing number at most one.  The equivalence
fails in the presence of isolated vertices.  Exactly 51 of the 311 stored
"unrestricted 2-crossing-critical" survivors have an isolated vertex: one at
order 7, seven at order 8, and 43 at order 9.  They are isolated-vertex
extensions of earlier survivors, hence pass every edge-deletion test but are
not crossing-critical under the proper-subgraph definition used in the cited
literature.  The upstream `check_reduction.py` accepts them because its
`suppress(E)` receives no vertex count and silently omits isolated vertices.
Thus the standard-critical count in these four files is 260, not 311.

This defect does not overturn the restricted minimum-degree-at-least-three
census.  It does mean that the empirical reduction paragraph and the opening
definition are false as written.  If edge-criticality is intended instead,
`C3 box C3` plus an isolated vertex is an immediate extra crossing-number-three
exception at suppressed order ten.  If standard proper-subgraph criticality is
intended, the clean repair is to use that definition and explicitly prove that
there are no isolated vertices before suppression.

## Independent method

`independent_audit.py` does not import upstream code.  It:

- reconstructs every one- and two-crossing planarization in the certificate's
  specified edge order;
- verifies rotation systems as permutations of directed darts and checks
  Euler characteristic two separately on every nontrivial component;
- decodes every Kuratowski bitmask, consumes every witness edge along maximal
  branch paths, and checks that the suppressed core is exactly `K5` or
  `K3,3`;
- verifies simple-graph and minimum-degree hypotheses, deletion-witness
  coverage, configuration admissibility, member uniqueness, hashes, and exact
  equality with the `CRIT2` rows;
- brute-force checks that the unique `CRIT_GE3` restricted row is isomorphic to
  `C3 box C3`; and
- classifies the isolated-vertex mismatch in the unrestricted output.

The upstream standard-library checkers were also run successfully with Python
3.12.12.  A fresh build of `crit2.c` against official nauty 2.9.1 reproduced
the unrestricted output files byte-for-byte for orders 6 through 9, including
input totals 156, 1,044, 12,346, and 274,668.  This replay confirms what the
program computed; it does not cure the definition mismatch or remove the
shared nauty trust boundary.

## Reproduction

Upstream source inspected at commit
`7851163e64f86c63454115c857a2668ba313abed`:

```sh
git clone https://github.com/abuzar08/discovery-net-notes.git /tmp/discovery-net-notes-crossing-review
git -C /tmp/discovery-net-notes-crossing-review checkout 7851163e64f86c63454115c857a2668ba313abed
python3 independent_audit.py \
  /tmp/discovery-net-notes-crossing-review/topological-graph-theory/crossing-number-two-subgraph \
  | diff -u expected_output.json -
```

Expected: no diff and exit status zero.  The deterministic JSON output has
SHA-256 `e3177c33e629ad65671bb39f4308f27f59623610283a8e040977c73e7c22dcaf`.

The independently checked upstream input hashes are:

- `census_certificate.json`:
  `aef4486f0cb298201e6222405f96cfeeea28b031a7df54a36087ee103211ea66`
- `certificate.json`:
  `8f8ca3086722062e8e39a255846903c06c8fb1068ccb490c3bc17d647f44ee7f`

## Literature and novelty boundary

Bokal, Oporowski, Richter, and Salazar define a crossing-critical graph using
**every proper subgraph** and report Vitray's unpublished conference claim that
`C3 box C3` is the only 2-crossing-critical graph whose crossing number is not
two: <https://arxiv.org/abs/1312.3712>.  Ringeisen and Beineke had already
proved `cr(C3 box Cn) = n`:
<https://doi.org/10.1016/0095-8956(78)90014-X>.  Richter's cubic special case is
<https://doi.org/10.1002/jgt.3190120308>.  The official ninth edition of
Schaefer's survey still lists the subgraph question on page 50:
<https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS21/pdf>.

The exact certificate bundle and bounded census appear potentially novel at
graph level, but the mathematical exception and an attributed stronger
classification are prior.  No priority claim follows from the targeted search.

## Strengthening and improvement opportunities

1. **High priority, proved repair:** replace the edge-deletion definition by
   the proper-subgraph definition, or add "no isolated vertices" everywhere
   the equivalence is used.  Pass `n` into the suppression checker and make an
   isolated vertex a loud anomaly.  Then report 260 standard-critical
   survivors in the unrestricted files, while optionally listing the 51
   edge-only extensions separately.
2. **High priority, reproducibility:** give the unrestricted run's exact `geng`
   commands, nauty archive hash, compiler flags, stderr summaries, and hashes
   of `u6.txt` through `u9.txt`.  The present checker validates stored output
   but cannot establish by itself that those rows came from a complete run.
3. **Medium priority, independence:** certify the negative order-ten census
   with a second generator/planarity implementation or a compact completeness
   transcript.  The member-level positive claims are independent of nauty;
   the assertion that no member was missed is not.
4. **Research direction, conjectural:** compare the 64 small members against
   the structural families and finite exceptional classes in the 2016
   classification work.  A canonical crosswalk could turn a raw census into a
   structural classification and reveal which order-eleven cases are genuinely
   new rather than subdivisions or known constructions.

## Trust boundary

The independent checker trusts Python 3.12.12, JSON decoding, arbitrary-size
integer bit operations, and the classical good-drawing reduction from at most
two crossings to the enumerated planarizations.  Rotation systems and
Kuratowski subdivisions are checked directly.  The negative exhaustiveness
claim still trusts `geng` and nauty's Boyer-Myrvold implementation; rebuilding
and replaying the same C program is reproducibility evidence, not algorithmic
independence.  No large/generated artifact is included here.
