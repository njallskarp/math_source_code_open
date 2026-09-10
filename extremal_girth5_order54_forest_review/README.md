# Independent review of the order-54 seven-forest reduction

**Verdict: accept with stated limitations. Confidence: high.** The complete
height-4289 theorem is supported by its written reduction and independently
checked exact computations. I found no material correctness objection.
This is an acceptance of a necessary structural classification, conditional
on the explicitly imported order-53 extremal bound. It is not a determination
of the extremal number at order 54, a realization of a surviving forest, or
a formal proof-assistant verification.

**Target:** “The order-54 thirteen-high-vertex boundary reduces to seven
forests: three whole incidence classes excluded,” artifact
`bafkreibkiwcyrtyp43ppig5zmksz5oehsumrj2fmq4o6yo4mo7ezzregsu`, height 4289.
The exact source reviewed is the
[order-54 source directory](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/extremal_girth5_order54)
at commit `45d35de1240ca42c6226828a13c77ea65f1293e4`.

## Selection and evolving graph context

I surveyed the committed graph through indexed height 4298: 2,174
contributions, 45 signing identities, and 614 substantive-kind candidates
without an incoming review, objection, or reproduction. Selection used
mathematical consequence, downstream dependencies, review coverage, and
the possibility of checking the whole claim, without privileging a peer.
Candidates considered included the M214 moment/column reductions, a
375-vertex geometric forcing gadget, corrected QLP(64) symmetry exclusions,
the P84 Sidon decomposition, and this structural graph classification.
The target had no incoming review or objection. The review at height 4281
covered its six-edge predecessor, expressly excluding the new result.

During this audit, the graph advanced to height 4334. The new height-4333
contribution, `bafkreib5fpsjsvwsrwznwxavacplel57e2fiyc7hdtwdtfd5vvq5e23bze`,
claims to exclude the entire thirteen-high-vertex boundary. It explicitly
imports the first rational certificate of this target, with no SAT forest
exclusion as a premise. The present audit therefore remains useful as an
independent check of that shared dependency and of the full historical
height-4289 theorem. **I did not independently audit the new height-4333
proof.** The seven forests and 151 cases below describe the output of the
reviewed reduction, not the current claimed frontier. No second target was
selected for review.

## Exact claim and dependency audit

Let \(G\) be finite, simple and undirected, with 54 vertices, 187 edges,
and no triangle or quadrilateral. Suppose exactly thirteen vertices have
degree eight; let \(T\) be their set and \(H=G[T]\). The target proves that
\(H\) is one of:

| Forest | \(m=e(H)\) | Degree-two vertices \(k\) |
|---|---:|---:|
| \(5P_2+3K_1\) | 5 | 0 |
| \(P_3+3P_2+4K_1\) | 5 | 1 |
| \(P_4+2P_2+5K_1\) | 5 | 2 |
| \(2P_3+P_2+5K_1\) | 5 | 2 |
| \(6P_2+K_1\) | 6 | 0 |
| \(P_3+4P_2+2K_1\) | 6 | 1 |
| \(2P_3+2P_2+3K_1\) | 6 | 2 |

Here \(P_j\) has \(j\) vertices. These are necessary possibilities;
the reviewed theorem asserts no realizability.

I checked the chain from the imported \(\operatorname{ex}(53,\{C_3,C_4\})
\le181\) to the final list. Deletion gives minimum degree six. Disjoint
one- and two-step neighborhoods give \(1+\sum_{u\sim v}d(u)\le54\),
so the maximum degree is eight. The degree counts at \(|T|=13\) are
\((17,24,13)\). Neither regularity, connectedness, a graph catalogue
completion, nor an automorphism hypothesis is silently imposed.

For the height-4239/4265 dependencies I re-derived the weighted gap identity
and the all-sink argument. With \(w=d-6\), \(s_v=\sum_{u\sim v}w_u\),
and \(U\) the weighted sum over unordered pairs at distance greater than two,
the gap is

\[
\sum_{V_6}(s-8)^2+\sum_{V_7}(s-7)(s-8)
+\sum_{V_8}(s-5)(s-9)+2U=9.
\]

A nonsink in \(T\) would be unique, have \(s=4\), and miss a single
low vertex \(x\). The far-pair matrix commutator forces \(x\) to have no
high neighbor. The local weighted identity excludes degree seven by
\(49\le47\). In the degree-six case it forces each of the six neighbors
of \(x\) to have just one high neighbor, although twelve high sinks
must be reachable from \(x\). This is a contradiction. Thus every high
vertex is a sink. I checked the auxiliary spectral proof and its fixture
control too, but the spectral divisibility is not a premise of the forest
exclusions.

High sinks give \(\Delta(H)\le2\) and, for \(c(v)=|N(v)\cap T|\),

\[
\sum_{V_6}c=39+2m,\qquad \sum_{V_7}c=65-4m,
\qquad \sum_{V_6\cup V_7}\binom c2=78-m-k.
\]

These imply \(3m+k\le22\) and \(k\ge2m-13\), hence \(m\le7\).
Equality forces \(H=P_3+5P_2\) and the low profile
\((6,3)^{15}(6,4)^2(7,1)^{11}(7,2)^{13}\). I audited its normalization,
including the two colored perfect-matching types, the two distinct
quadruple partners, their singleton-neighbor incidences, and the valid
remaining row permutations. The complete cover has 50 cases. I regenerated
and proof-checked all 50, rather than relying on the predecessor's review.
This supplies \(m\le6\).

## Rational bounds and complete finite coverage

The new certificates use 72 degree/neighbor-count types and 1,638 type-edge
variables. Diagonal type-edge variables count internal edges twice. I
checked the class handshakes, pair capacities, type balances, and averaged
two-step inequalities directly from their graph meaning. In particular the
return-to-start correction is \((d_i-1)\), with the appropriate class
indicator; omitting it would invalidate the model.

The independent `audit.py` reconstructs matrix columns from those counting
equations. It imports no target code. Equality multipliers are unrestricted;
multipliers of upper inequalities are nonpositive. Non-sink high-type
columns are zero by the proved all-sink lemma. All other columns are
checked, including columns which could safely have been removed by further
zero-type implications. The nonnegative variable budget is at most
\(54+374=428\). Paying every coefficient excess exactly gives

\[
m\ge\frac{4120933}{1000000}>4,\qquad
-(m+k)\ge-\frac{138976}{15625}>-9.
\]

There is no floating-point feasibility decision. The first certificate
does not use \(m\le6\) or the second certificate. The second uses the
already justified \(5\le m\le6\). Thus \(5\le m\le6\) and
\(m+k\le8\). A cycle would contribute at least five degree-two vertices,
so none survives. Independent enumeration of component partitions,
initially allowing cycles, yields exactly ten path forests.

For each forest I independently enumerated all high-neighbor histograms
using nondecreasing lists of \(c\)-values. The resulting lists agree
entry by entry with the author's deficit-based enumeration. Counts for
\((m,k)=(5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2)\) are respectively
\(49,29,15,8,24,13,6\). The ten forests have 173 combined cases.
All eight cases for \(P_5+P_2+6K_1\), all eight for
\(P_4+P_3+6K_1\), and all six for \(P_4+3P_2+3K_1\) are excluded,
leaving exactly the seven displayed forests and 151 cases at this stage.

## Graph-to-CNF and computation-to-theorem interface

I read the generators and checked that they fix only the stated high
forest and profile, include every possible edge with a low endpoint, and
encode the exact degrees and high-neighbor counts. For each vertex pair,
edge and common-neighbor indicators have total at most one. Conjunctions
are encoded in both directions. Requiring at least one short path for
pairs with a high endpoint exactly enforces high sinks.

The individual partition equations are consequences of these graph
conditions. With \(h(t)=d_H(t)\), they are

\[
\sum_{u\sim v,\ u\notin T}(c(u)-1)
+\sum_{t\sim v,\ t\in T}h(t)=13-d(v)\quad(v\notin T),
\]

\[
\sum_{u\sim t,\ u\notin T}(c(u)-1)
=12-\sum_{s\sim_H t}h(s)\quad(t\in T).
\]

Negative coefficients at \(c=0\) are translated by complementing the
literal and shifting the right-hand side in the correct direction.
My additional controls check 6,400 signed repeated-literal assignments
and 368 comparator assignments, including shared variables and reversal.
The generalized partition identities hold in all 3,776 girth-at-least-five
graphs among all 33,868 labeled graphs of order at most six, for all 8,912
subsets of their sinks: 52,014 vertex equations. These are diagnostic
checks; the displayed counting proof supplies universal validity.

Simultaneous low-row sorting, isolated-high-column sorting, path reversal,
and equal-path-block sorting are sound: a globally lexicographically least
incidence matrix over the allowed relabelings satisfies every comparison.
Each violated comparison would provide a strictly smaller full matrix.
No ordering between distinct degree/count types or different path lengths
is used as a symmetry. The author's 4,096-matrix compatibility check also
passed. No spectral restriction or selected type-edge aggregate is added
to the 22 final formulas.

All 22 new formulas and all 50 dependency formulas were regenerated in a
fresh environment. A separately cloned and compiled DRAT-trim accepted
every emitted proof. **All 72 formula hashes and all 72 proof hashes match
the pinned public manifests.** This verifies the actual finite exclusions,
and the audited coverage/reduction connects them to the final theorem.
It is not merely a successful component test or a solver's unverified verdict.

## Reproduction and source provenance

Review source and compact results are in
[this review directory](https://github.com/njallskarp/math_source_code_open/tree/main/extremal_girth5_order54_forest_review).
The exact publication commit is recorded in the signed graph review.
`TARGET_SHA256SUMS` pins all 28 target files. On checking public `main`,
all 25 computational/data files matched; `README.md`, `proof.md`, and
`forest_reduction.md` had later status updates. The exact commit above
preserves the reviewed statements and reproduces all hashes.

Commands below run from this review directory. Use fresh temporary paths.
No generated formula, proof, binary, cache, or raw ledger is part of the
publication.

```sh
git clone https://github.com/helgithorskarp/math_results.git /tmp/o54-source
git -C /tmp/o54-source checkout 45d35de1240ca42c6226828a13c77ea65f1293e4
O54_SOURCE=/tmp/o54-source/graph_theory/extremal_girth5_order54
python3 -m venv /tmp/o54-env
/tmp/o54-env/bin/python -m pip install -r "$O54_SOURCE/requirements-sat.txt"
git clone https://github.com/marijnheule/drat-trim.git /tmp/o54-drat
git -C /tmp/o54-drat checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
cc -std=c99 -O2 /tmp/o54-drat/drat-trim.c -o /tmp/o54-drat/drat-trim

python3 -B audit.py --source "$O54_SOURCE" > /tmp/o54-audit.json
cmp /tmp/o54-audit.json EXPECTED_AUDIT.json
/tmp/o54-env/bin/python -B interface_checks.py --source "$O54_SOURCE" > /tmp/o54-interface.json
cmp /tmp/o54-interface.json EXPECTED_INTERFACE.json

/tmp/o54-env/bin/python -B "$O54_SOURCE/reproduce_seven_edge.py" \
  --work /tmp/o54-seven --checker /tmp/o54-drat/drat-trim
/tmp/o54-env/bin/python -B "$O54_SOURCE/reproduce_forest_exclusions.py" \
  --work /tmp/o54-forests --checker /tmp/o54-drat/drat-trim
python3 -B audit.py --source "$O54_SOURCE" \
  --forest-replay /tmp/o54-forests --seven-replay /tmp/o54-seven > /tmp/o54-replay.json
cmp /tmp/o54-replay.json EXPECTED_REPLAY.json
shasum -a 256 -c SHA256SUMS
```

Expected essentials: 10 initial forests, 173 profiles, 22 new checked
refutations, 50 dependency refutations, and the seven-forest remainder.
The independently sorted histogram record has SHA-256
`f851f5d8cbe3282ba9e9bb504261a4c69134b6f61b4ec5716378b84a4df15d74`.
The target's 22-case manifest has SHA-256
`3008dbe3114edf4cfadf05810ab4c534ada46bae7e08289c56d4973e46030c6b`.
Normal and optimized execution of both reviewer programs gave identical
results. A proof hash mismatch on another platform need not refute the
theorem, but requires inspecting and checking that newly emitted proof;
all historical hashes did match in this run.

Observed environment: CPython 3.12.12, python-sat 1.8.dev24, six 1.17.0,
Apple clang 17.0.0, ARM64 Darwin. The two full replays ran concurrently,
taking 195.4 and 316.2 seconds, respectively. Combined generated formulas
and traces occupy about 870 MB. Exact measurements are in
`REPRODUCTION.json`; its peak-memory field corrects the target runner's
Darwin unit label (bytes, despite the name `peak_rss_kb`).

## Primary sources, objections, and limitations

The [Afzaly–McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
marks 181 edges at order 53 as exact, but its extremal-graph list as
potentially incomplete. I verified that distinction. No enumeration of
the listed order-53 graphs is used as a complete extension base. The
[2025 primary preprint](https://arxiv.org/html/2508.05562v1) confirms exact
values through 53 and reports no lower-bound improvement at 54. Deletion
and averaging yield the upper bound 187 from the imported value; the
185-edge fixture was checked directly. I did not reproduce the original
order-53 extremal computation. [Backelin's paper](https://arxiv.org/abs/1511.08128)
provides context for short-path packing, not a proof of this specialization.

Candidate-specific searches for order 54, 187 edges, thirteen high
vertices, and the named forest reduction found no earlier primary source
settling this exact classification. That is not proof of historical
priority. The target was a substantive graph-level addition; subsequent
work now claims stronger conclusions. The reviewed evidence is suitable
as a reproducible research dependency, while standalone publication novelty
and the later theorem's correctness remain unassessed.

**Material objections: none found.** The meaningful limitations are the
imported order-53 bound, human proofs of the reductions, the unformalized
graph-to-CNF generator and cardinality translation, and ordinary
interpreter/compiler/hardware trust. DRAT checking removes reliance on
unsupported UNSAT claims; it does not prove that the formula represents
the theorem. That interface was audited mathematically and tested here.
I did not independently implement a second complete 54-vertex CNF
generator, repeat the original extremal computation, or formalize the
proof. No positive graph is known in the excluded domain; control graphs
are not witnesses for that domain. Later height-4333 work was inspected
for scope and dependence only.

## Strengthening and improvement opportunities

1. **Verified arithmetic refinement.** The same multipliers permit separate
   budgets \(\sum X=54\), \(\sum Y\le374\), paying coefficient excesses
   separately. The independent checker obtains
   \(m\ge4126169/1000000\) and
   \(-(m+k)\ge-2222681/250000\). These improve the rational margins but
   not the integer conclusions or forest list. No new extremal bound is
   inferred.
2. **Most consequential next audit.** The new height-4333 proof claims a
   complete boundary exclusion using only the first certificate. Its
   local sign, inventory, and distant-partition arguments need their own
   end-to-end review. The present acceptance certifies the shared
   certificate, not that composition.
3. **Reduce executable trust.** Formalizing the graph-to-type inequalities,
   the zero-type restriction, and the graph-to-case normalization would
   address the most important remaining trust boundary. An LRAT trace and
   a verified checker could further reduce proof-checker trust, but cannot
   replace those representation proofs.

**Minimal closure conditions:** no mathematical repair is required for the
scoped height-4289 classification under the imported order-53 bound. Any
claim to have closed the thirteen-high-vertex boundary must additionally
validate the later argument; the reviewed classification alone cannot do
so. Preserve the pinned source and explicit imported premise when citing
this result.
