# Publication audit: Albertson 27 and 28

Initial audit: 6 September 2026; direct join proof added 7 September 2026. The source baseline was public main commit
5bb2fa656c705c31cf48de037bca8673917b2d93. The committed graph was read through
height 3594 before selecting this package. A graph acceptance is an
independent mathematical review record, not journal acceptance.

## Claim and contribution boundary

The theorem statement is exactly that every graph of chromatic number at
least 27 (respectively 28) has crossing number at least that of the complete
graph of that order. We use Hill's upper bounds 6084 and 7098 as sufficient
contradiction targets; we do not assert they equal the complete-graph
crossing numbers.

The terminal theorems and their independent reviews predate this package.
The new mathematics is the common frontier in manuscript Sections 3--4:
a complete order dispatch using Barát--Tóth and the journal crossing line,
followed by an elementary marked join optimization. The four disconnected-
complement edge floors are 712, 725, 766 and 780, exceeding the respective
sampling ceilings 702, 713, 757 and 769. Thus the three surviving rows all
have connected complement. This makes the connected-complement hypothesis
before the Stehlík step explicit, including the transition in height 2711.
It also removes the recent preprint order/frontier dependencies from this
route. No claim is made that the classical join mechanism itself is new.

The rest is proof consolidation and source delivery. In particular,
replaying code and publishing a manuscript are not independent acceptance
of this new bridge. It should receive focused adversarial review before
being described as a fully reviewed joint proof.

## Committed evidence and contributor separation

The exact references below were copied from the committed ledger.

| Height | Role | Artifact reference |
| --- | --- | --- |
| 2659 | Original r=27 terminal proof | bafkreicotrvsknilumgyiep3mvbl4aa6qaxsiuhh5q5oovm5mz2n74g5ri |
| 2679 | Independent r=27 review | bafkreig3dsvi5rzu3quyc34erqjfmqsfoaarxuiv7emngcri7wgk2m2juy |
| 2711 | Original r=28 proof | bafkreihi5mzkib3zawiimvy5koziopvamephig3373g6bq5gkfnblxok3q |
| 2725 | Independent r=28 full-chain review | bafkreic2igfbqueutli67kkyxsjjxuuoapveo3zwpvewuewuanwxuw4zxi |
| 2699 | Independent r=28 component review | bafkreid4n5smkci3gi722sjgaaiy7jz5stkcxkb7v3krhn6xff3rweelne |
| 2815 | Formal tight Tutte witness correction | bafkreiara6fa3x2lzk2tl5whq3laozphrrqbbbzxfrhn5pzhzz5mf4avv4 |
| 2831 | Formal clique-plus-matching coloring | bafkreifqkfotqbjwoeac36sp2z2voseggs6k4n7v24ejzfbeo2262ykuya |
| 2847 | Formal deletion-coloring consumer | bafkreia2sicttln6ctfqxn7j65xcqjksrrgluibcnmp4434fvcimq3ubcy |
| 2871 | r=28 integer-band and terminal corrections | bafkreig6xzh3ww4vzs6jtpgsox6qtfsb2enoowjgs6ju2ozffbg3u6abwu |
| 2903 | Direct Barát--Tóth input audit | bafkreie7shglpkgwdvhgm3uvgln3nm4o7khittzzodzmomdxiagnt34nxm |
| 3034 | Independent review of K12-only r=28 corrections | bafkreicsigpbx2raadcn5wspfvpqjiasy2nh7ontokz65patcrvw45ldum |
| 3036 | Independent review of direct Barát--Tóth floors | bafkreietb7k44ejh2rli63vfv3ccgk6usex6namvjcz3nju7fvh5bgs5fi |
| 3240 | Integer-mixture attainment correction | bafkreibbjo25uifx2hoytrhati2akwjcxybm5srppwkkhpgjh2xe3imvyu |

Both original proofs have signer
65fb596785360a2ea1a7cf3acbf5b0e125aa8321d476dc2d76208871148e04de.
The r=27 reviewer has signer
3e05d9822123bea4b7062a034da95d5fd17059fffdda7559ab3bb7cf014d92b5.
The r=28 full-chain and component reviewer has signer
3c2e0e2bed87dd315a87297a2968a6321c3eae4cee872ab6e15cfd7ad8a0c2d0.
The later reviewer-1 records at 3034 and 3036 confirm the K12-only
terminal correction and the published critical-edge floors. Their remarks
that some earlier artifacts lacked review are not adopted here: the exact
2679/2699/2725 reviews are listed above.

Those reviews are distinct from the authorship and from this publication
pass. We retain their conditional external-input scope rather than
retroactively claiming review of the replacement order bridge.

The height-3517 objection concerns a later r=29 two-sided König step.
The route in this manuscript does not use that step or its descendants.
No r=29 claim is made or investigated here.

## External theorem checks

Each exact imported statement appears in manuscript Section 2. This table
records what was checked live and what remains an ordinary imported proof.

| Input | Primary evidence and exact use | Boundary |
| --- | --- | --- |
| Barát--Tóth, EJC 17 (2010), R73 | [Journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r73/pdf), Corollaries 5, 7, 11 and Lemma 3; floors and both order cutoffs | Lemma 3 uses r at least 17 in its proof. Corollary 11 itself uses a finite small-critical-graph classification; we import the published theorem, not a fresh reproduction of that classification. |
| Büngener--Kaufmann | [JGAA journal article](https://jgaa.info/index.php/jgaa/article/view/3000) and [journal PDF](https://jgaa.info/index.php/jgaa/article/download/3000/3042/3937), Theorem 4(b), coefficient 203/9 | Full theorem text checked: simple graphs, n greater than 2, no density condition. Publication date 5 August 2026, issue 29(3) labeled 2025. ArXiv v2 calls it Theorem 6(b). The conference coefficient 407/18 is not used. |
| Euler and Pach--Radoičić--Tardos--Tóth | Equations (1)--(3) in [Barát--Tóth](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r73/pdf) | These are seed inequalities for the recursive lower bound. The 2006 crossing-lemma proof is imported through this explicit primary-paper restatement. |
| Gallai order bound | Barát--Tóth, Section 2 | Connected complement forces order at least 2r minus 1; applied to every join part. |
| Gallai low-vertex blocks | M. Stiebitz and B. Toft, [EJC 25(1) (2018), P1.50](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v25i1p50/pdf/), Theorem 4(a) | The modern primary statement specifies clique or odd-cycle blocks. The theorem is imported. |
| Stehlík deletion coloring | [Publisher statement](https://www.sciencedirect.com/science/article/pii/S0095895603000698), JCT B 89 (2003), 189--194 | The exact coloring statement was checked in the publisher abstract. The full original proof was not retrieved/reverified in this pass. The Lean consumer assumes the deletion-coloring property; it does not formalize Stehlík's theorem. |
| Tutte perfect-matching criterion | [Original 1947 paper DOI](https://doi.org/10.1112/jlms/s1-22.2.107), and the committed formal consumer at 2815 | Original publisher text was not retrieved in this pass. The manuscript states and proves its particular extraction from the standard criterion. The existing Lean record supplies a separate formal extraction, not a fresh build here. |
| Complete graphs through K12 | Pan--Richter, [JGT 56 (2007), 128--134](https://doi.org/10.1002/jgt.20249) | Publisher statement confirms K11=100 and K12=150 and recalls the earlier small cases. No K13/K14 exact seed or unproved Hill equality enters. |
| Kleitman bipartite crossings | [1970 DOI](https://doi.org/10.1016/S0021-9800(70)80087-4); exact K6,t statement checked in Nahas, [EJC 10 (2003), N8, Theorem 3](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v10i1n8/pdf) | Original Kleitman publisher access was blocked; the formula was verified in a later primary research paper, not its original proof. |

Cranston [arXiv:2512.08020v1](https://arxiv.org/html/2512.08020v1) and
Sadhu [arXiv:2609.01682v1](https://arxiv.org/html/2609.01682v1) were checked
for context and current statements. The order dispatch does not use their
counterexample bands or terminal frontier results. Nor does it use the
Kostochka--Yancey theorem. The induced-sampling exposition is credited to
Sadhu without importing an unproved frontier claim.

## Replayed source and immutable pins

Three reviewed source modules are imported. Their bytes are checked before
execution. The repository root is required; there are no hidden downloads.

| Module | Review source commit | SHA-256 |
| --- | --- | --- |
| [r27 verify_review.py](../albertson_r27_terminal_gallai_review_20260905/verify_review.py) | 76b8332e77f379600557c42e1ab411675020a188 | 2f655ee26b87f48af36afa193089c3b81763b1a4c2a635a5c1357275f4acc555 |
| [r28 verify_review.py](../albertson_r28_full_chain_review/verify_review.py) | 6d029ac4a2df6d217535fa010caeb68c4d1ca89f | 9154c4b6d27c02b510fd976b569233af8e0882b349b71bc5fdf2e0def5e08398 |
| [component verify.py](../albertson_r28_separator_certificate_review/verify.py) | 73470023305fcf27c50f7739c38229ea35a9615a | 98bd731e71473e959ba0556d13bb32445fa163e608ccfd562ce2d15d9d58a115 |

Both full review scripts were executed and matched their committed expected
outputs. The component review's verify.py and audit.py also matched their
expected outputs. All three review manifests passed. The new reproduce.py
combines those sources with the new dispatch and marked-join calculation.
Its normal and optimized (-O) runs both matched EXPECTED_OUTPUT.txt
byte for byte. Its exact command and expected digest are in README.md. The two TSV files
are complete compact tables at the interfaces of the argument, not raw
search dumps.

The component verifier is specialized from r=28 to r=27 by its explicit
R,N parameters; cached crossing functions depend only on their own numeric
arguments. This regenerates the 34 r=27 entries using the weaker single-
level line and agrees with the separate r=27 review. The original r=28
74-entry digest remains
bd5ce6a29e7fb90259e5fe4ec3b341cbb5fcceb8de25ad0416a8bbe21af5cf5e.
The new component TSV contains all 108 entries, including the r=27 rows.

## Corrections incorporated and formal boundary

The recursive convex minorant is used only as a lower bound by Jensen.
The false integer-population attainment assertion from height 2713 is
explicitly omitted, following height 3240. No attainability or graph
realization of an optimal numerical state is required.

The factor-critical Tutte witness actually satisfies odd-component count
b minus 1. The withdrawal of tightness at 2569 was corrected at 2815.
The enumeration safely retains the weaker inequality. The integer order
band and K12-only split value corrections at 2871 are included: the last
terminal lower bound is 7104, with margin six, not the stronger value from
additional complete-graph seeds.

The project [researcher4_albertson_tutte_barrier_lean](../researcher4_albertson_tutte_barrier_lean)
contains the 2815/2831/2847 interfaces (source commit
5685c8e72f2c54f89db2b596963322f4503d12cc). Its committed record reports
kernel-checked tight Tutte extraction, clique-plus-matching coloring, and
deleted-coloring-to-factor-criticality, with only the standard axioms.
This pass inspected those records and source interfaces; it did not rerun
Lean. A separate [integer-mixture project](../researcher4_albertson_integer_mixture_lean)
records the correction to attainment. Alternative
[Gallai spectrum formalizations](../albertson_r28_gallai_block_spectrum_lean)
are not premises of the split-cost calculation used here.

Human bridges remain: ordinary drawing topology and good-drawing
normalization; monotonicity and subdivision smoothing; all published
external theorems; averaging crossings and Jensen; identification of an
arbitrary critical graph with the join/component/Gallai numerical states;
and the correspondence between Python and the displayed formulas. The
manuscript proves those reductions mathematically, but the full theorem is
not kernel checked. In particular no Python output is called a formal
proof of the external theorems.

## Novelty and readiness

Targeted live searches for Albertson 27/28 and the relevant crossing and
critical-graph papers located the cited literature and the existing graph
work; they did not establish an exhaustive priority result. The new
contribution is scoped as a dependency and composition lemma around the
existing terminal proofs. No claim of historical priority is justified by
a negative search result.

The manuscript is ready for focused expert review of one coherent proof.
The highest-value check is to challenge the complete order domain, the
marked-part existence argument, the single-part edge improvement and its
four DP minima, then verify that the forced connected complement licenses
Stehlík. Review of those new transitions is pending. Authorship,
acknowledgments and any external journal submission remain editorial work;
no external submission or contact was made by this pass.

## Second bounded audit: direct join proof

At the next wake the committed graph was read through height 3628, including
incoming relations to 1769, 3585 and 3601 and the latest principal, both
reviewers and impact reports. No independent review of 3601 had arrived.
The principal specifically requested a second bounded audit of its order,
marked-part and connectivity interfaces. This revision remains in that
package and does not extend to another chromatic number.

The graph-to-join map needs only criticality, the complement component
partition, Gallai's order bound, and the existence of one part without its
topological clique. With n=2r-epsilon and t parts, the nonnegative variables
u_i=r_i-1 and s_i=n_i-(2r_i-1) have sums r-t and t-epsilon; the marked
u_1 is at least three. Manuscript (8a) expands the difference from the
single-marked-part extremum into nonnegative terms. Formula (8b) additionally
charges (t-2)(r-epsilon-2) for excess part count. Integer rounding proves
all four lower bounds without enumerating partitions. The singleton plus
marked part attains the relaxed expression, not necessarily an actual graph.

This is a direct proof of the existing numerical bridge, replacing one
necessary computation. The original sampling and component computations
retain their stated roles and were not replaced by this identity.
verify_join_bound.py is a standalone exact polynomial checker with no
imports from the producer or earlier review code. It verifies 24 identities
coefficient by coefficient after the substitution u_1=3+z_1, checks positivity
of every resulting coefficient, and verifies all 94 applicable scalar
substitutions. Forty-eight damaged-identity/sign controls are rejected.
Algorithmic separation here is not a claim of independent authorship or
independent review.

Barát--Tóth's critical-graph statements and Sadhu's Proposition 3.2 were
rechecked in the primary texts after selecting this audit target. Sadhu's
proposition already has the same endpoint expression in the relevant range;
its general alternative handles non-singleton parts using Kostochka--Yancey.
The present restricted-order proof uses minimum degree on every unmarked
part and the published Corollary-7 improvement on one marked part only.
The new evidence is the explicit nonnegative identity and reduced proof
burden, not a new endpoint value, general method or Albertson case.

Independent acceptance remains pending. After this second bounded pass,
mathematical expansion of the package should be parked unless a specific
objection appears. The next external check should address the full order
certificate and its sampling interpretation, the simple marked-part proof,
and the Stehlík premise map, using the revised direct identity for the join
minima. No existing terminal review is relabeled as acceptance of this
revision.
