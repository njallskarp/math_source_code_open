# Cyclomatic-two line-graph core stability

This directory proves a bounded case of the open fixed-cyclomatic line-graph
signature program: an extremal minimum-degree-two core with cyclomatic number
two cannot gain line-graph signature from one attached leaf.

`TWO_LEAF_STABILITY.md` strengthens this to any two simultaneous leaves,
including two leaves at the same support.  Its rank-two response identity and
a zero-response kernel-difference lemma cover every singular case.  It does
not claim stability for arbitrary deeper pendant trees.

`THREE_LEAF_STABILITY.md` proves stability for any three simultaneous leaves,
again allowing repeated supports.  It combines a marked modulo-four reduction
with seven nonsingular and ten singular all-range response types.

`FOUR_LEAF_STABILITY.md` strengthens this to any four simultaneous leaves.  A
new four-dimensional local-to-global inertia lemma imports the three-port
classification.  The only new singular branch reduces to seven exact mixed
response types on a complete four-mark subdivision quotient.

`FIVE_LEAF_STABILITY.md` proves stability for five simultaneous leaves.  Its
response-alphabet inequality classifies every locally admissible five-port
matrix using only the three-port types, independently of graph order or
subdivision length.  It also gives an explicit five-distinct-support equality
case.  No claim is made for six leaves.

The main argument is in `CYCLOMATIC_TWO_CORE_STABILITY.md`.  It combines an
exact leaf rank-one criterion with a four-subdivision congruence that
preserves inertia and every defined/undefined vertex response.  A modulo-four
reduction then leaves four extremal dumbbell bases.

## Reproduce

The standard-library proof checkers require CPython 3.11 or later and no
third-party packages.  The optional independent characteristic-polynomial
audits require SymPy 1.14.x.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c2_core.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_two_leaf_charpoly.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_leaf.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_leaf_charpoly.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_four_leaf.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_four_leaf_charpoly.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_five_leaf.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_five_leaf_charpoly.py
```

Expected final lines:

```text
result_sha256=92b3ea8ffb472f39aaf452b83549404246772fe0b4cb67ea70979dffb35c70e8
VERIFIED
result_sha256=c80a82442617de3292cef4a807c76d1f6bc6ce5d399c3c62d08955592b16767c
VERIFIED
result_sha256=010f70c2a3f809ac8058173550f86f7baeecec02bcaebe9135c6128948f6cfc1
VERIFIED
result_sha256=15c98ee6dbf61da872c7caa997362f27e4808c74648d13cf9d083ccc28f0a4a6
VERIFIED
result_sha256=4fc568578691a39bfa29412cb21652b8224c7046c812293bfb2606b4e7ac22c0
VERIFIED
result_sha256=4ca9b47cf0280c8b5cdc3ace780c0df2005772f83701fcec2d6370f7a10c4495
VERIFIED
result_sha256=4bd8dc171f6c8010104a44a12096b3769099f3c0fbe1f0e67a03f888bfbacf0d
VERIFIED
result_sha256=b37bc71bff79ccf0c5d3a2bfd83d4ed162157aa24cbf1c2f3bf57036e08e176b
VERIFIED
result_sha256=f59cbfc4684bc947ab89d4ca4be85d165e832df14a6b11984bd6f4013873e8d1
VERIFIED
```

On the publication machine (CPython 3.12.12), the exhaustive three-leaf
checker took 193 seconds and its independent SymPy audit took 17 seconds. The
four-leaf checker took about 214 seconds and its independent audit took 41
seconds. The five-leaf checker took about 82 seconds and its independent audit
took about 149 seconds. These wall times are informative and are not included
in the result hashes.

The output records 16 reduced rose cases, 64 reduced theta cases, both exact
dumbbell signature tables, 46 four-subdivision checks, 714 leaf checks, and
the nonextremal response `-3/4` sharpness witness.  The three-leaf checker
additionally covers 631,680 marked-representative triples, all 17 response
types, and 30,513 direct full-matrix regressions. The four-leaf checker covers
2,185,340 cases in the only new singular branch, all seven resulting types,
3,048 locally admissible four-dimensional response matrices, and 15,948
direct full-matrix regressions. Its independent audit constructs and checks
all 3,576 four-leaf placements on the minimal bases.

The five-leaf checker exhausts 1,678 nonsingular and 2,160 singular all-range
switching-normalized response matrices, plus 344 locally admissible singular
compressions and 22,253 direct regressions. Its independent audit reimplements
both response searches through characteristic polynomials and directly checks
all 10,660 minimal-base five-leaf placements plus the equality witness.

## Trust boundary

The proof is symbolic and human-readable.  The checker uses exact
`fractions.Fraction` arithmetic and a direct symmetric-congruence inertia
algorithm.  Its finite calculations corroborate the displayed residue and
response tables.  It does not replace the graph-topology classification or
the general block-congruence proof, and it makes no claim about multiple or
iterated pendant attachments beyond the separately proved two-, three-, and
four-, and five-leaf theorems.
