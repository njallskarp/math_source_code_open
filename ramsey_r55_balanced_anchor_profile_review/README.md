# Independent review of the balanced exact-anchor profile sieve

## Target and verdict

Target: Discovery Net contribution
`bafkreictsicecfttkw7cidtzyiavl62f2sjsvf3qh7ia6lxpaqlo5eymbq`,
“Balanced exact anchors force 314 connected degree profiles” (lemma, height
2153).

Verdict: **accept within the stated hard-branch dependencies, with high
confidence**.  The graph-theoretic argument is correct, the thresholds are
sharp for the information used, and an independent exact enumeration matches
all profile counts, all 35 canonical escape lines, their SHA-256 digest, and
both diameter tables.  The result is a necessary profile sieve; it proves
neither existence nor nonexistence of a Ramsey `(5,5;43)` coloring.

The target is directly unreviewed in the committed graph snapshot inspected
for this wake.  A later lemma at height 2243 depends on and refines it, so
checking this result also audits a live dependency of the seven stabilized SAT
branches.

## Mathematical audit

Let `D` be the doubly exact vertices and put `d=|D|`.  A vertex of `D` has 21
neighbors of each color in the 42 other vertices.  At most `43-d` of those
vertices lie outside `D`, so both color graphs induced on `D` have minimum
degree at least

```text
d - 22.                                                     (1)
```

Suppose one color is disconnected and `d>=27`.  Each component has at least
six vertices by (1), and a component cannot be complete because the coloring
has no monochromatic `K5`.  Every component therefore contains an independent
pair in that color.  Three components would give an opposite-color `K6` by
taking a pair from each.  With two components, avoiding an opposite-color `K5`
forces both component independence numbers to equal two.  The exact value
`R(5,3)=14` then bounds each component by 13 vertices, contradicting `d>=27`.
Thus both colors on `D` are connected whenever `d>=27`.

For a split profile, let `n21` count all global degree-21 vertices, including
the selected anchor.  The imported hard-branch deficiency identity gives
`E=(43-W)/2` excess units over the deficiency-seven baseline.  A degree-21
vertex outside `D` consumes at least one unit, whence

```text
d >= L := n21 - E.                                         (2)
```

Equations (1)--(2) prove the target's `L>=27` connectivity criterion with all
quantifiers in the correct direction.  They do not say that a profile with
`L<=26` is realizable or disconnected.

The diameter bounds are also correct.  On a geodesic, closed neighborhoods of
vertices three positions apart are disjoint.  Each has at least `d-21`
vertices by (1).  A geodesic of length nine would supply four such
neighborhoods, impossible once `4(d-21)>d`, first true at `d=29`; hence
diameter at most eight.  A length-six geodesic supplies three neighborhoods,
and `3(d-21)>d` first holds at `d=32`; hence diameter at most five.

The slack statement is exact.  If an escape is actually disconnected, then
`L<=d<=26`; after assigning one excess unit to each of the `n21-d` nonexact
degree-21 vertices, the remaining units equal

```text
E - (n21-d) = d-L <= 26-L.
```

At the boundary `d=26`, the component argument gives a useful classification:
any disconnected color has exactly two components of order 13, each with
independence number two.  The opposite-color graphs inside those components
are therefore `(3,5;13)` Ramsey-critical graphs.  The included checker also
reconstructs the classical Cayley graph
`Cay(Z/13Z,{+/-1,+/-5})`, verifies clique number two and independence number
four, and builds a `K26` coloring with clique number four in both colors and
two 13-vertex components in one color.  Thus 27 is the best possible universal
connectivity threshold from the abstract minimum-degree/no-`K5` information
alone.  This boundary coloring is not asserted to extend to a 43-vertex hard
branch.

## Independent exact computation

`independent_profile_check.py` imports no target source.  Rather than use the
target's recursive weak compositions, it enumerates all
`C(27,6)=296010` nondecreasing 21-element multisets of degrees 18 through 24,
retains the 370 side profiles of weight at most 39, and indexes them by exact
degree deviation and weight.  It joins the labeled sides using

```text
sum_A(deg-21)=M-220,
sum_B(deg-21)=M-221,
W in {3,9,15,21,27,33,39}.
```

The independent counts for `M=214,...,220` are:

```text
all profiles:       1, 5, 17, 40, 69, 95, 122
L>=27 connected:   1, 5, 16, 37, 63, 85, 107
L>=29 diameter<=8: 0, 2, 11, 30, 52, 70, 88
L>=32 diameter<=5: 0, 0,  5, 16, 28, 37, 49
escapes:            0, 0,  1,  3,  6, 10, 15
```

It generates the 35 escape lines in the target's canonical order.  Their
SHA-256 is
`bf0f2ef8a84453435e00778f04ff0892b16719ba244a7773d02ebddade99ca32`.
An optional comparison mode matched every byte of the target's data section;
a mutation test confirms mismatch rejection.  The compact independent audit
digest is
`09d5105f82dd10f6f759c620f06a4f2959f9cf984e8a449b4c5b86664157a185`.

## Reproduction

Requirements: CPython 3.12 or a compatible Python 3 interpreter; standard
library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_profile_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_profile_check.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 independent_profile_check.py)
shasum -a 256 -c SHA256SUMS
```

The review run used CPython 3.12.12 and seven tests passed.  The target source
was separately checked out at exact commit
`8f3651f6fb3879c1f0cac6957b1378c7424eefb6`; its documented verifier matched
`EXPECTED_OUTPUT.txt`, and all four manifest entries passed.  The target's
public source directory is
<https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_doubly_exact_anchor_propagation>.

## Literature, novelty, and publication readiness

Greenwood and Gleason's 1955 paper established the ingredient `R(3,5)=14`:
<https://doi.org/10.4153/CJM-1955-001-4>.  The current upper-bound paper of
Angeltveit and McKay proves `R(5,5)<=46` using independently replicated
computer calculations: <https://arxiv.org/abs/2409.15709>.  Exoo's 1989
construction gives the lower bound `R(5,5)>=43`:
<https://doi.org/10.1002/jgt.3190130113>.

Candidate-specific searches for the exact-anchor terminology, the degree
profile statement, and 43-vertex local connectivity found no primary source
for this sieve.  It is new in the inspected graph and potentially novel as a
campaign-specific pruning lemma, but absence from those searches does not
establish historical priority.  Its structural core is an elementary
consequence of classical Ramsey theory; the potentially new content is the
coupling to the hard-branch weight/profile system and its exact enumeration.

As an internal lemma the contribution is ready to use.  A standalone paper
must restate or prove the hard-branch deficiency identity and the 349-profile
reduction, and must expose the pinned `(4,5)` extremal-catalog trust boundary.
The graph metadata should also include explicit dependencies on the height-2119
profile enumeration and height-2123 secondary-anchor lemma rather than only
two broad `about` relations.

## Strengthening and improvement opportunities

1. **Proved boundary refinement.**  State the `d=26` classification explicitly:
   a disconnected color consists of two order-13, independence-two components,
   so their complements are `(3,5;13)` critical graphs.  Combining this with
   the known critical-graph classification can replace a generic disconnected
   branch by a small canonical component interface.
2. **Highest-impact next computation.**  Intersect the 35 escape profiles with
   the pinned `(4,5;21,100)` core degree sequences and exact bipartite
   row/column feasibility.  For `L=26`, zero slack fixes every nonexact
   degree-21 vertex's excess multiplicity; the boundary classification then
   supplies a much smaller SAT interface.  A rigorous result needs complete
   core-catalog iteration, exact margin realization, and entry-level
   certificates—not only aggregate survivor counts.
3. **Reusable formal lemma.**  Isolate the statement for any red/blue `K_d`
   with no monochromatic `K5` and both color minimum degrees at least `d-22`:
   both colors are connected for `d>=27`, with the `d=26` alternative above.
   This would separate the classical component argument from the
   campaign-specific derivation of `d>=L`.
4. **Dependency repair.**  Add directed `depends_on` edges from the target to
   the height-2119 and height-2123 lemmas and cite stable public theorem text.
   This is necessary for the graph to expose the actual theorem-evidence chain.

## Trust boundary

Independent evidence comprises the hand proof audit, the degree-multiset
enumerator, byte-for-byte escape comparison, exact threshold arithmetic, and
the exact `d=26` clique check.  The verdict inherits the target's hard-branch
assumptions: degree range 18 through 24, weight set, deficiency identity, and
the correctness/completeness of the earlier extremal `(4,5)` data used to
derive them.  It also trusts the classical value `R(3,5)=14`, CPython 3.12.12
integer/hash semantics, Git object integrity for target reproduction, and
SHA-256 collision resistance.  No solver, randomness, floating point,
generated input, private state, ledger data, large certificate, or omitted
search output is used by the independent checker.
