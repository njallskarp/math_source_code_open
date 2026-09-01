# Cyclic(43) red-to-blue perturbation search

This directory studies the first open question in Section 7 of Ge, Jayasooriya,
Qiu, Sun, and Yuan, *Study of Exoo's Lower Bound for Ramsey number R(5,5)*
(arXiv:2212.12630v3): among colorings obtained from their `Cyclic(43)` coloring
by changing any collection of red edges to blue, what is the minimum possible
number of monochromatic copies of `K5`?

`solve_cyclic43.py` makes one Boolean variable for each of the 473 initially red
edges. For every one of the `C(43,5) = 962598` vertex sets it adds a unit-weight
soft clause for the possible all-blue state; for each of the seed's 43 red
`K5`s it adds a second clause for the all-red state. Each clause is false exactly
when its monochromatic state occurs. Thus the exact weighted-MaxSAT optimum
equals the desired monochromatic-`K5` count.
The returned coloring is then checked independently by direct enumeration.

Run the exact optimization with:

```bash
uv run --with python-sat python solve_cyclic43.py --output certificate.json
```

An independent MaxSAT algorithm and SAT-backend rerun can use:

```bash
uv run --with python-sat python solve_cyclic43.py \
  --algorithm fm --solver m22 --output certificate-fm.json
```

Recount every `K5` in an existing certificate without invoking a SAT solver:

```bash
python solve_cyclic43.py --verify certificate.json
```

Compute exact unrestricted edge-toggle rigidity through radii two and three:

```bash
python local_rigidity.py certificate.json --output local-rigidity-primary.json
python local_rigidity_radius3.py certificate.json \
  --output local-rigidity-radius3-primary.json
```

The same commands with `certificate-fm.json` independently analyze the second,
structurally different optimum. Both optima remain at two monochromatic `K5`s
through Hamming radius three, even when edge changes in either direction are
allowed.

The bounded-distance C++ checker extends this result through radius six:

```bash
g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  local_rigidity_bounded.cpp -o local_rigidity_bounded
./local_rigidity_bounded certificate.json 6
./local_rigidity_bounded certificate-fm.json 6
```

The persisted runs used Homebrew GCC 16.2.0 on macOS 26.2 arm64. The primary
and Fu-Malik passes took 197.71 and 200.04 seconds of wall time, respectively.

Find and verify a constant-two path between the two optima:

```bash
python plateau_path.py certificate-fm.json --radius 15 \
  --target certificate.json --output plateau-bridge.json
```

The certificates have Hamming distance 15. The path uses every differing edge
exactly once, so it is geodesic, and every intermediate coloring has exactly
two monochromatic `K5`s. All 15 edges have cyclic length one. Thus the optima
belong to the same single-edge-connected component of the optimum-2 plateau.
The unit test independently recounts every intermediate coloring and checks the
endpoint against the primary certificate.

Continue the neutral defect transport until no unused edge preserves the count:

```bash
python plateau_path.py certificate.json --radius 43 --allow-partial
```

This reaches radius 37. If cyclic edge `i` means `{i,i+1}` modulo 43, the edge
positions obey `p[2k] = 42+17k` and `p[2k+1] = 37+17k` modulo 43. The first 37
positions are distinct and the next requested position is the already-used
edge 42. An exact scan of all 866 unused edges at the terminal coloring finds
no constant-two extension: the minimum next count is four, uniquely at edge
`(21,22)`. The compact result is `defect-orbit-primary.json`.

Continue the modular transport after it first reuses an edge and classify the
one-flip neutral component:

```bash
python defect_cycle.py certificate.json \
  --fu-malik certificate-fm.json \
  --bridge plateau-bridge.json \
  --all-edge-neighbors --direct-verify \
  --output defect-cycle.json
```

The transport closes after 86 steps and visits 86 distinct two-clique
colorings. At every state, exactly two of all 903 single-edge reversals preserve
the objective: the predecessor and successor length-one edges. Thus the complete
one-flip-connected optimum-2 component through the primary certificate is the
cycle `C86`. The Fu-Malik certificate occurs at state 71, and the existing
15-step bridge is exactly the closing segment. The direct-verification mode
recounts all 962,598 five-sets independently at every state.

The same exhaustive neighborhood scan determines the exact first-step escape
barrier. Every off-cycle neighbor has at least three monochromatic `K5`s, and
this bound is attained at every cycle state. If `S_n` is the set of cyclic
length-one positions attaining three from state `n`, then
`S_(2k) = {17j mod 43 : k-8 <= j <= k-1}` and
`S_(2k+1) = {17j mod 43 : k-8 <= j <= k}`. Thus even states have eight minimum
exits, odd states have nine, and the full 903-neighbor objective spectrum
depends only on state parity. The certificate records all aggregate and
parity-resolved counts.

Classify the complete connected objective-at-most-three component containing
that cycle:

```bash
python escape_component.py certificate.json \
  --cycle defect-cycle.json \
  --all-edge-neighbors --direct-verify \
  --output escape-component.json
```

The 731 objective-three boundary colorings are all distinct. Their induced
graph is the disjoint union of 43 paths `P17`, one for each cyclic length-one
edge position, and each boundary vertex has one edge back to a unique cycle
state. A full 903-edge scan of 17 rotational representatives, lifted by proven
rotation symmetry, finds no other objective-two or objective-three neighbor.
Therefore the entire connected sublevel-three component has 817 vertices and
1,505 edges: `C86`, the 43 paths, and 731 center-to-boundary spokes.

Close the next objective layer under every one-edge move:

```bash
python objective_four_frontier.py certificate.json \
  --cycle defect-cycle.json \
  --escape escape-component.json \
  --scan-frontier --direct-verify \
  --output objective-four-component.json
```

The first objective-four frontier has 3,311 vertices in 77 rotational orbits.
Orbit-wise breadth-first expansion adds exactly one more 43-vertex orbit and
then closes. The complete connected sublevel-four component therefore has
4,171 vertices and 10,621 edges. No objective-four vertex has an objective at
most three neighbor outside the earlier component, and every objective-four
neighbor stays in the closure. Thus the exact one-flip escape level from this
basin is five.

Close the objective-five layer and scan its full one-edge neighborhood:

```bash
python objective_five_frontier.py certificate.json \
  --cycle defect-cycle.json \
  --escape escape-component.json \
  --objective-four objective-four-component.json \
  --scan-frontier --direct-verify \
  --output objective-five-component.json
```

The 29,541 outgoing objective-five edges from the sublevel-four component
deduplicate to 13,158 colorings in 306 free rotational orbits. Scanning all
903 edge reversals at every orbit representative finds no new endpoint of
objective at most five: every lower endpoint is already in the certified
sublevel-four component and every objective-five endpoint stays in this
frontier. Hence the complete connected sublevel-five component has 17,329
vertices and 52,890 edges, and its exact one-flip escape level is six. All 306
representatives are independently recounted over all `C(43,5)` five-sets.

Classify the first objective-six frontier of that closed component:

```bash
python objective_six_frontier.py certificate.json \
  --cycle defect-cycle.json \
  --escape escape-component.json \
  --objective-four objective-four-component.json \
  --objective-five objective-five-component.json \
  --direct-verify-strata \
  --output objective-six-frontier.json
```

The 129,473 directed objective-six exits deduplicate to 49,192 colorings in
1,144 free rotational orbits. Their incidences with source objectives two
through five realize 21 signatures; one representative of every signature is
independently recounted over all `C(43,5)` five-sets. This classifies only the
first objective-six frontier. Its own one-edge neighborhood has not yet been
scanned, so the result does not claim sublevel-six closure.

Close the full objective-six layer with the bit-packed C++ kernel:

```bash
g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  objective_six_component.cpp -o objective_six_component
./objective_six_component certificate.json defect-cycle.json \
  --representatives objective-six-component-representatives.json \
  > objective-six-component-fast.json
```

The first frontier is not closed: breadth-first orbit expansion finds exactly
39 additional free rotation orbits. It then closes with 1,183 objective-six
orbits, or 50,869 colorings. The sixth layer has 55,126 induced edges. Hence the
complete connected sublevel-six component through the primary optimum has

```text
68,198 vertices and 237,489 edges,
```

and its exact one-flip escape level is seven. The complete scan evaluates
1,068,249 representative edge reversals, representing 45,934,707 full-state
checks. On the recorded Apple Silicon host, the optimized scan took 0.86
seconds; the original Python reference run was interrupted after 18 minutes
before reaching the sixth-layer closure. The speedup comes from keeping states
in fifteen 64-bit words and maintaining all 903 single-flip objective deltas
incrementally while an orbit DFS changes one edge and backtracks.

Independently verify every one of the 1,183 representatives with a fresh direct
five-set recount and fresh per-state single-flip deltas:

```bash
g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic -fopenmp \
  verify_objective_six_component.cpp -o verify_objective_six_component
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  > objective-six-component-independent.json
```

The independent checker took 1.79 seconds, found zero missing same-layer
neighbors, and reproduced the complete neighbor-objective histogram exactly.
It does not reuse the incremental search engine: every representative is
decoded from the compact certificate, all 962,598 five-sets are recounted, and
all 903 one-edge objective deltas are rebuilt from scratch. The two C++ programs
share only the mathematical encoding and standard-library JSON parsing, so
compiler, edge-ordering, and rotation implementations remain within the trust
boundary.

Extract the complete first objective-seven frontier of the closed sublevel-six
component:

```bash
g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic \
  objective_six_component.cpp -o objective_six_component
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-frontier objective-seven-frontier-fast.json \
  > /tmp/objective-six-regression.json
```

The exact frontier has 4,217 free rotation orbits, hence 181,331 colorings.
Its 525,202 directed incidences with the complete sublevel-six component split
by source objective as

```text
2:   2,193
3:  14,018
4:  72,111
5: 142,072
6: 294,808
```

There are 35 distinct per-target incidence signatures
`(d_2,d_3,d_4,d_5,d_6)`. The 495 KiB certificate stores every canonical target,
the parallel signature list, and all lower-layer representatives needed for an
independent membership check. This is only the first objective-seven frontier;
it does not assert that the objective-seven layer is closed.

Verify all targets and signatures using direct five-set recounts rather than
the incremental search engine:

```bash
g++-16 -std=c++20 -O3 -DNDEBUG -Wall -Wextra -Wpedantic -fopenmp \
  verify_objective_six_component.cpp -o verify_objective_six_component
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-seven-frontier objective-seven-frontier-fast.json \
  > objective-seven-frontier-independent.json
```

The recorded ten-thread run took 3.06 seconds. It directly recounted all
962,598 five-sets for each of 4,217 targets, established objective exactly
seven, rebuilt every single-flip delta, checked every lower-objective neighbor
against the certified component, and reproduced every target's five-coordinate
incidence signature with zero discrepancies.

Close the full threshold-seven component and simultaneously extract its first
objective-eight frontier:

```bash
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-component objective-seven-component-fast.json \
  --objective-eight-frontier objective-eight-frontier-fast.json \
  > /tmp/objective-six-regression.json
```

The first objective-seven frontier is already closed: it contains all 4,217
objective-seven rotation orbits, with no additional objective-seven orbit and
no newly connected orbit of objective at most six. The seventh layer has
219,988 induced edges. Therefore the complete connected sublevel-seven
component through the primary optimum has

```text
249,529 vertices and 982,679 edges,
```

and exact one-flip escape level eight. The exact closure examined 3,807,951
representative reversals, representing 163,741,893 full-state checks.

Verify all seventh-layer moves by a fresh direct recount:

```bash
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-seven-component objective-seven-component-fast.json \
  objective-seven-frontier-fast.json \
  > objective-seven-component-independent.json
```

The independent checker found no missing objective-at-most-seven neighbor and
reproduced the full boundary histogram, including 439,976 directed same-layer
incidences and 1,020,906 exits to objective eight.

The complete first objective-eight frontier has 13,702 free rotation orbits,
or 589,186 colorings. Its 1,929,754 directed incidences with the sublevel-seven
component split by source objective as

```text
2:     2,537
3:    16,813
4:    62,393
5:   285,649
6:   541,456
7: 1,020,906
```

Exactly 64 incidence signatures `(d_2,...,d_7)` occur. Independently verify all
13,702 targets and signatures with:

```bash
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-eight-frontier objective-eight-frontier-fast.json \
  objective-seven-component-fast.json objective-seven-frontier-fast.json \
  > objective-eight-frontier-independent.json
```

The ten-thread direct verifier took 12.77 seconds and found zero wrong
objectives, noncanonical representatives, missing sublevel-seven neighbors, or
signature discrepancies. The objective-eight result is a first-frontier
classification only; it does not claim closure at threshold eight.

Close threshold eight and collect its complete first objective-nine frontier in
the same exact pass:

```bash
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-component /tmp/objective-seven-regression.json \
  --objective-eight-component objective-eight-component-fast.json \
  --objective-nine-frontier objective-nine-frontier-fast.json \
  > /tmp/objective-six-regression.json
```

The eighth layer is not equal to its first frontier: exact closure adds 36
rotation orbits, giving 13,738 free rotation orbits and 590,734 colorings. It
has 764,153 induced one-flip edges. Consequently the connected component of
all states with objective at most eight that contains the primary optimum has

```text
840,263 vertices and 3,676,586 edges,
```

and exact escape level nine. The closure examined 12,405,414 representative
reversals, or 533,432,802 symmetry-lifted checks. Directly verify the entire
eighth layer with:

```bash
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-eight-component objective-eight-component-fast.json \
  objective-seven-component-fast.json objective-seven-frontier-fast.json \
  > objective-eight-component-independent.json
```

The independent checker directly recounts every five-set for all 13,738
representatives, finds no missing objective-at-most-eight neighbor, and matches
the optimized neighbor histogram entry-for-entry.

The complete first objective-nine frontier has 42,661 free rotation orbits,
1,834,423 colorings, 6,603,854 directed incidences with the certified
sublevel-eight component, and 113 signatures `(d_2,...,d_8)`. Verify it with:

```bash
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-nine-frontier objective-nine-frontier-fast.json \
  objective-eight-component-fast.json objective-seven-component-fast.json \
  objective-seven-frontier-fast.json \
  > objective-nine-frontier-independent.json
```

All frontier objectives and component-incidence signatures match. The fresh
recount also detects 64 representative incidences (2,752 after lifting the 43
rotations) from frontier states to exactly 20 objective-eight rotation orbits
outside the primary sublevel-eight component. This does not contradict the
component closure: those external states are reached only after passing through
objective nine. Their representatives are included in the independent JSON for
follow-up classification of the newly exposed low-objective islands.

Classify every threshold-eight component meeting those 20 exposed seeds with:

```bash
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-component /tmp/objective-seven-regression.json \
  --objective-eight-component /tmp/objective-eight-regression.json \
  --external-objective-eight-seeds objective-nine-frontier-independent.json \
  --external-objective-eight-components \
    external-objective-eight-components-fast.json \
  > /tmp/objective-six-regression.json
```

All 20 seeds lie in one complete connected component of the **rotation
quotient** of the external sublevel-eight graph. Exact closure adds one
rotation orbit, so the quotient island consists of 21 free rotation orbits,
or 903 labeled colorings in total, all with objective exactly eight. Across all
903 colorings there are 1,376 induced one-flip edges, the exact escape level is
nine, and the objective-nine boundary contains 115 rotation orbits reached by
5,633 directed labeled-state incidences. The optimized closure run took 100.39
seconds.

Independently verify the claim by direct five-set recount and a fresh rotation
canonicalizer:

```bash
python3 verify_external_objective_eight_components.py \
  external-objective-eight-components-fast.json \
  objective-nine-frontier-independent.json \
  > external-objective-eight-components-independent.json
```

The independent run took 9.00 seconds and found zero wrong objectives,
noncanonical or non-free representatives, or missing objective-at-most-eight
neighbors. It reproduced the vertex, edge, escape, and objective-nine-boundary
counts exactly. That original checker verified quotient closure but did not
test connectivity of the 43-fold labeled lift. A later explicit BFS over all
903 labeled states corrected the connectivity interpretation: the quotient
island lifts to **43 pairwise-disjoint, rotation-equivalent components**, each
with 21 vertices and 32 edges. Thus the aggregate counts above remain exact,
but the 903 labeled colorings do not form one connected component.

Close the primary component through objective nine with:

```bash
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-component /tmp/objective-seven-regression.json \
  --objective-eight-component /tmp/objective-eight-regression.json \
  --objective-nine-component objective-nine-component-fast.json \
  > /tmp/objective-six-regression.json
```

The first objective-nine frontier is not closed. Exact orbit expansion finds
120 further objective-nine orbits and also pulls in 34 lower-objective orbits
that were disconnected at threshold eight: one orbit at objective seven and
33 at objective eight. In total the new part of the closure has 42,815 free
rotation orbits, split as

```text
objective 7:      1 orbit
objective 8:     33 orbits
objective 9: 42,781 orbits
```

It has 2,514,167 internal edges and 6,603,854 edges back to the previously
certified primary sublevel-eight component. Consequently the complete
connected sublevel-nine component through the primary optimum has

```text
2,681,308 vertices and 12,794,607 edges,
```

and its exact one-flip escape level is ten. The optimized search checks every
one of 903 reversals at all 42,815 new orbit representatives, corresponding to
1,662,463,635 labeled-state checks after the free-orbit lift.

Independently verify the complete new part with fresh direct five-set recounts:

```bash
OMP_NUM_THREADS=10 ./verify_objective_six_component \
  certificate.json objective-six-component-representatives.json \
  --objective-nine-component objective-nine-component-fast.json \
  objective-nine-frontier-fast.json objective-eight-component-fast.json \
  objective-seven-component-fast.json objective-seven-frontier-fast.json \
  > objective-nine-component-independent.json
```

The reachability-enabled ten-thread checker took 32.79 seconds in a fresh run.
For all 42,815 representatives it
reconstructed the coloring, recounted all 962,598 five-sets, rebuilt all 903
single-flip deltas, checked canonicality and freeness, and tested every accepted
neighbor against the union of the old and new strata. It found zero objective,
canonicality, frontier-containment, or closure discrepancies and independently
reproduced every edge count, objective histogram, and escape level.

The checker now also materializes the independently reconstructed quotient
adjacency and performs an explicit BFS seeded by all 42,661 first-frontier
orbits. It reaches every one of the 42,815 new-part orbits, closing the
reachability caveat identified in the graph review. The exact quotient-distance
histogram from the first frontier is

```text
distance 0: 42,661 orbits
distance 1:     34 orbits
distance 2:     53 orbits
distance 3:     20 orbits
distance 4:     22 orbits
distance 5:     16 orbits
distance 6:      9 orbits
```

Thus the farthest added representatives are exactly six quotient edges beyond
the certified first frontier. This BFS is part of the direct-recount verifier;
it does not rely on the optimized generator's queue or discovery order.

Resolving the shells by objective gives a less naive attachment picture:

```text
objective \ distance      0      1    2    3    4    5    6
7                         0      0    0    0    0    1    0
8                         0     20    1    5    2    3    2
9                    42,661     14   52   15   20   12    7
```

The 20 previously exposed external objective-eight seeds account for the
objective-eight part of shell one, but 14 additional objective-nine orbits are
also directly adjacent to the first frontier. The second lower quotient island
is genuinely deeper: its unique objective-seven orbit occurs at distance five.
Thus the tempting hypothesis that every added objective-nine orbit requires an
initial downward move is false.

The 34 newly attached lower orbits have additional exact structure. Recount
and classify their quotient and labeled lifts with:

```bash
python3 verify_threshold_nine_lower_islands.py \
  objective-nine-component-fast.json \
  external-objective-eight-components-fast.json \
  objective-eight-component-fast.json objective-seven-component-fast.json \
  objective-seven-frontier-fast.json \
  > threshold-nine-lower-islands-independent.json
```

There are exactly two closed threshold-eight quotient components. The first is
the previously exposed 21-orbit objective-eight quotient island; an explicit
labeled-state BFS and an independent \(\mathbb Z/43\mathbb Z\) voltage check
both show that it lifts to 43 components of 21 vertices and 32 edges each. The
second is new: it contains one objective-seven orbit and 12 objective-eight
orbits, has a nonzero cycle voltage, and therefore lifts to one connected
component of 559 labeled colorings and 688 edges. Its exact escape level is
nine; its objective-nine boundary has 56 rotation orbits and 4,042 directed
labeled-state incidences. The direct Python classification took 14.61 seconds.

These are finite local classifications of the Cyclic(43) perturbation
landscape, not a determination of \(R(5,5)\) and not a global classification of
all low-objective colorings. Searches of the committed Discovery Net graph and
the cited primary R(5,5) sources found no prior threshold-nine closure or these
two lift classifications. That is a novelty assessment, not a priority claim;
unrelated disconnected sublevel-eight or sublevel-nine components remain out
of scope.

## Complete first objective-ten frontier of the primary threshold-nine component

Let \(M(x)\) be the number of monochromatic copies of \(K_5\) in the
two-coloring obtained by applying the perturbation state \(x\) to the fixed
Cyclic(43) seed. Let \(P_9\) be the complete connected one-flip component
through the primary optimum induced by states with \(M\leq 9\), as certified
above, and quotient states by cyclic rotation. Define its first objective-ten
frontier by

\[
F_{10}=\left\{[z]:M(z)=10,\ \exists [x]\in P_9\text{ with }
                  d_H(x,z)=1\right\}.
\]

### Exact frontier theorem

An exhaustive orbit-canonical scan of every one of the 903 edge reversals at
all 62,356 rotation representatives of \(P_9\) gives

\[
|F_{10}|=128{,}184\quad\text{rotation orbits},\qquad
43|F_{10}|=5{,}511{,}912\quad\text{labeled colorings}.
\]

Every source and target orbit is free. The complete directed labeled incidence
from source objective \(j\) into \(F_{10}\) is

\[
\begin{array}{c|rrrrrrrr}
j&2&3&4&5&6&7&8&9\\ \hline
I_j&4{,}945&36{,}077&115{,}369&300{,}441&884{,}639&
3{,}896{,}918&6{,}173{,}295&10{,}105{,}516.
\end{array}
\]

Thus \(\sum_{j=2}^{9}I_j=21{,}517{,}200\). For each target orbit \([z]\),
the certificate stores the exact incidence signature

\[
\sigma(z)=\bigl(i_2(z),i_3(z),\ldots,i_9(z)\bigr),
\qquad
i_j(z)=\#\{e:\,[z\triangle\{e\}]\in P_9\cap M^{-1}(j)\}.
\]

Exactly 196 signatures occur. The boundary degree
\(\deg_{P_9}(z)=\sum_{j=2}^{9}i_j(z)\) lies between one and nine, with exact
orbit distribution

\[
\begin{array}{c|rrrrrrrrr}
d&1&2&3&4&5&6&7&8&9\\ \hline
\#\{[z]:\deg_{P_9}(z)=d\}&
1{,}780&13{,}054&31{,}088&43{,}520&28{,}836&8{,}509&1{,}250&139&8.
\end{array}
\]

### Exact quotient-boundary structure and the level-ten shadow

Form the simple bipartite quotient boundary with the 62,356 source orbits of
\(P_9\) on one side and the 128,184 target orbits of \(F_{10}\) on the other,
joining two orbits when some representatives differ by one edge. An independent
bidirectional reconstruction gives exactly

\[
500{,}397
\]

simple quotient edges. The multiplicity-weighted quotient incidence count is
500,400. The excess consists of exactly three source--target orbit pairs of
multiplicity two; every other pair has multiplicity one. In the sorted
objective-ten certificate, the three exceptional target indices are
12,845, 26,794, and 128,182.

The source-side boundary degrees range from zero to 59. Exactly 65 source
orbits have degree zero, all have objective nine, and all 65 already belong to
the complete first objective-nine frontier of the sublevel-eight component.
Direct scans of all 903 reversals show that their minimum objective outside
\(P_9\) is 11. Every other source orbit has minimum external objective 10:

\[
\begin{array}{c|rr}
\text{minimum external objective}&10&11\\ \hline
\text{source rotation orbits}&62{,}291&65.
\end{array}
\]

Thus the level-ten frontier does not touch all of \(P_9\): it leaves an exact
65-orbit *level-ten shadow* whose one-flip exits jump over objective ten.

The objective-ten targets also admit an exact partition by the minimum
objective among their neighbors in \(P_9\):

\[
\begin{array}{c|rrrrrrrr}
\min M(x)&2&3&4&5&6&7&8&9\\ \hline
\#\text{ target orbits}&115&839&2{,}683&6{,}941&19{,}996&
67{,}747&26{,}564&3{,}299.
\end{array}
\]

The 128,184 targets realize 49 distinct supports across the eight source
objective layers; 6,784 meet one layer, 62,589 meet two, 58,347 meet three,
and 464 meet four. These are exact certificate corollaries, not evidence that
the objective-ten layer is closed.

### Exact first expansion of the objective-ten frontier

Let \(F_{10}\) denote the 128,184-orbit first objective-ten frontier above and
scan all \(128{,}184\binom{43}{2}=115{,}150{,}248\) representative one-edge
moves. The number \(m(x)\) of objective-ten moves from a target orbit has the
exact distribution

\[
\begin{array}{c|rrrrrrrrrrrr}
m&0&1&2&3&4&5&6&7&8&9&10&11\\ \hline
\#\{[x]\in F_{10}:m(x)=m\}&
4{,}366&22{,}497&39{,}071&21{,}565&16{,}775&12{,}958&
6{,}601&3{,}003&1{,}041&251&52&4.
\end{array}
\]

Of the resulting 369,002 quotient-level objective-ten moves, 367,744 remain
inside \(F_{10}\). They give 367,744 distinct directed quotient pairs, with no
self-orbit pair. The remaining 1,258 moves expose exactly 376 new rotation
orbits, all of objective ten. No new orbit of objective at most nine is
exposed. Thus \(F_{10}\) is not closed, but its complete first one-flip
expansion is finite and exactly classified.

The minimum objective strictly above ten among the 903 neighbors of a frontier
representative is 11 for 127,836 orbits and 12 for the remaining 348. This is
a local frontier profile; it is not itself the escape level of the eventual
closed component.

### Complete primary sublevel-ten component

Define \(P_{10}\) to be the one-edge-connected component of the sublevel set

\[
\{x:M(x)\leq 10\}
\]

that contains the primary Cyclic(43) optimum. Starting with the 376 newly
exposed orbits and continuing exact orbit-canonical breadth-first search to
closure adds exactly 527 objective-ten rotation orbits beyond \(F_{10}\), and
adds no orbit with objective at most nine. Consequently the complete
objective-ten layer of \(P_{10}\) contains 128,711 free rotation orbits, or
5,534,573 labeled colorings.

The complete component has the exact invariants

\[
\begin{aligned}
|V(P_{10})|&=8{,}215{,}881,\\
|E(P_{10})|&=42{,}320{,}815,\\
|E(P_{10}[M=10])|&=8{,}009{,}008,\\
|E(P_9,M=10)|&=21{,}517{,}200.
\end{aligned}
\]

Every one-edge neighbor of \(P_{10}\) with objective at most ten is already in
the certificate, while an objective-eleven exit exists. Hence the exact
one-flip escape level of this component is 11. This closes the primary
threshold-ten component; it does not exclude disconnected sublevel-ten
components elsewhere in the \(2^{903}\)-coloring space.

For a finer audit, the 527 added orbits contribute 22,661 labeled vertices,
54,094 edges back to the previously known portion, and 48,418 internal edges.
Their complete sorted representative list is reproduced independently in both
persisted component certificates.

### Quotient geometry of the 527-orbit addition

An exact quotient-neighbor scan gives considerably more structure than the
aggregate closure count.  The added orbits lie in four successive one-flip
shells beyond the original objective-ten frontier:

\[
\begin{array}{c|rrrr}
\text{distance from the original frontier}&1&2&3&4\\ \hline
\text{rotation orbits}&376&116&32&3.
\end{array}
\]

The induced cyclic quotient on these 527 orbits has 1,126 edges, with no
loops and no parallel multiplicity.  It has 21 connected components; the five
largest have 178, 131, 116, 50, and 15 vertices.  Its exact shell-edge counts
are

\[
e_{11}=540,\quad e_{12}=302,\quad e_{22}=146,\quad
e_{23}=96,\quad e_{33}=30,\quad e_{34}=12.
\]

The boundary back to the original frontier consists of 1,258 simple quotient
edges incident with 841 distinct original-frontier orbits; again there is no
parallel multiplicity.  Multiplying the internal and boundary quotient counts
by the free rotation-orbit size 43 reproduces 48,418 and 54,094 labeled edges.
The first shell agrees exactly with the independently persisted 376-orbit
first expansion.

Reflection preserves every shell and permutes the 21 components.  Exactly 37
rotation orbits are reflection-fixed, so the addition has 282 dihedral orbits.
All three depth-four orbits are reflection-fixed.  This decomposition supplies
small, symmetry-stable pieces for subsequent objective-eleven boundary scans.

### Complete first objective-eleven frontier

Let \(F_{11}\) be the set of cyclic rotation orbits of objective-eleven
colorings one edge from the complete primary component \(P_{10}\):

\[
F_{11}=\{[z]:M(z)=11,\ \exists [x]\in P_{10},\ d_H(x,z)=1\}.
\]

An exhaustive scan of all \(191{,}067\cdot903=172{,}233{,}501\)
source-representative moves gives

\[
\boxed{|F_{11}|=372{,}974\text{ free rotation orbits}}
\]

and hence exactly \(16{,}037{,}882\) labeled frontier colorings. There are 324
distinct incidence signatures across source objectives 2 through 10. The
directed labeled incidence vector is

\[
\begin{array}{c|rrrrrrrrr}
j&2&3&4&5&6&7&8&9&10\\ \hline
I_j&
5{,}246&41{,}366&174{,}666&460{,}143&1{,}153{,}776&
3{,}093{,}377&12{,}722{,}023&18{,}994{,}777&30{,}310{,}743.
\end{array}
\]

Thus \(\sum_{j=2}^{10}I_j=66{,}956{,}117\). The boundary-incidence degree
of an objective-eleven target ranges from one through ten, with exact
distribution

\[
\begin{array}{c|rrrrrrrrrr}
d&1&2&3&4&5&6&7&8&9&10\\ \hline
N_d&5{,}933&25{,}539&75{,}930&118{,}397&96{,}350&
40{,}281&9{,}302&1{,}014&212&16.
\end{array}
\]

Every source orbit of objectives 2 through 9 has an objective-eleven exit.
Among the 128,711 objective-ten source orbits, exactly 128,363 have minimum
outside-\(P_{10}\) objective 11, while exactly 348 have minimum 12. Therefore
the primary threshold-ten component has an exact 348-orbit
*level-eleven shadow*:

\[
\begin{array}{c|rr}
\min\{M(y):d_H(x,y)=1,\ M(y)>10\}&11&12\\ \hline
\#\text{ objective-ten source orbits}&128{,}363&348.
\end{array}
\]

The complete 372,974-representative array and its aligned signature array were
independently regenerated entry for entry. To avoid committing two large
derived JSON files, the repository retains a compact certificate containing
canonical SHA-256 digests of both arrays and of every aligned
representative/signature pair; both full files are deterministically
regenerable by the commands below.

### Exact first expansion of the objective-eleven frontier

Scan all (372{,}974\cdot903=336{,}895{,}522) one-edge moves from the
complete first frontier (F_{11}).  After cyclic canonicalization, the moves
of objective at most eleven split exactly as follows:

\[
\begin{array}{c|r}
\text{endpoint class}&\text{quotient incidences}\\ \hline
P_{10}&1{,}557{,}119\\
F_{11}&1{,}139{,}644\\
\text{new objective-eleven orbits}&772\\
\text{new orbits of objective at most ten}&0.
\end{array}
\]

The 772 outward incidences expose exactly 148 new free rotation orbits, or
6,364 labeled colorings.  Every source--target pair has multiplicity one.
Only 642 frontier orbits touch the addition: 526 have one new neighbor, 104
have two, ten have three, and two have four.  On the target side, the exact
numbers with source degrees (1,\ldots,9) are

\[
(2,3,18,25,24,48,24,2,2).
\]

In particular, this complete scan exposes no lower-objective island across
the first objective-eleven layer.  A direct OpenMP implementation independently
recounts all \(\binom{43}{5}=962{,}598\) five-sets for every frontier source
and agrees on the complete 148-representative target set and all thirteen
shared mathematical fields.

### Complete primary sublevel-eleven component

Starting from the 148-orbit first expansion and continuing exact breadth-first
closure under every move with (M\leq11) discovers one final shell of exactly
two objective-eleven orbits.  Those two expose no further sublevel-eleven
state.  Thus the objective-eleven layer of the connected primary component is

\[
372{,}974+148+2=373{,}124
\]

free rotation orbits, representing 16,044,332 labeled colorings.  Combining
this layer with the already closed (P_{10}) gives

\[
\boxed{|V(P_{11})|=24{,}260{,}213},\qquad
\boxed{|E(P_{11})|=133{,}822{,}192}.
\]

The 150-orbit addition has 772 quotient incidences back to (F_{11}), zero
to (P_{10}), and 226 induced quotient edges.  Every added orbit has an
external objective-twelve neighbor, and the complete frontier scan already
contains objective-twelve exits.  Therefore the exact one-flip escape level
of (P_{11}) is twelve.  A separately implemented direct five-set recount
reconstructs the final two-orbit shell, all 150 representatives, and the
complete reverse-incidence counts with zero omissions or mismatches.  This is
a component classification through the primary optimum; it does not exclude
disconnected sublevel-eleven components elsewhere in the (2^{903}) search
space.

Reproduce the expansion and closure with:

```bash
g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  scan_objective_eleven_first_expansion.cpp \
  -o scan_objective_eleven_first_expansion
./scan_objective_eleven_first_expansion \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json /tmp/objective-eleven-frontier-fast.json \
  objective-eleven-first-expansion-fast.json

g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  close_objective_eleven_component.cpp -o close_objective_eleven_component
./close_objective_eleven_component \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json /tmp/objective-eleven-frontier-fast.json \
  objective-eleven-first-expansion-fast.json \
  objective-eleven-component-fast.json
```

### The objective-twelve boundary of the objective-ten shadow

The objective-eleven exit census isolates a finite ``shadow''

\[
S_{10}=\{x\in P_{10}:M(x)=10,\;N(x)\cap M^{-1}(11)=\varnothing\}
\]

of 348 cyclic rotation orbits.  An exact scan of all 903 one-edge moves from
every member gives the complete objective-twelve boundary

\[
B_{12}=N(S_{10})\cap M^{-1}(12),\qquad |B_{12}/C_{43}|=2{,}823.
\]

There are 3,384 quotient incidences, hence 145,512 labeled incidences after
lifting the free cyclic action.  All 3,384 source--target pairs are distinct:
there is no parallel quotient-edge excess.  The exact source-degree spectrum
is

\[
\begin{array}{c|rrrrrrrrrrrrrr}
d&4&5&6&7&8&9&10&11&12&13&14&15&16&17\\\hline
\#&5&2&9&40&146&24&11&26&5&16&9&38&13&4,
\end{array}
\]

while 2,262 target orbits have one incident shadow source and 561 have two.
The resulting simple bipartite quotient graph has 30 connected components and
cycle rank 243.  Its largest component has 112 source orbits, 676 target
orbits, 896 edges, and cycle rank 109.

The target-side reverse scan supplies a useful closure check and a bridge to
the next layers.  Every objective-ten neighbor of every target in (B_{12})
belongs to the certified primary component (P_{10}): no external
objective-ten orbit appears.  Besides the 348 shadow sources, these targets
meet 718 distinct nonshadow objective-ten orbits.  They also meet 8,696
distinct objective-eleven orbits.  Their minimum one-flip objective has exact
histogram

\[
\begin{array}{c|rrrr}
\min_{y\sim x}M(y)&7&8&9&10\\\hline
\#\{x\in B_{12}/C_{43}\}&40&603&1{,}943&237.
\end{array}
\]

A second implementation directly recounts all 962,598 five-vertex sets at
each of the 348 sources and 2,823 targets.  It independently reconstructs the
same target set and bidirectional incidences, agrees on all ten shared
aggregate fields, and reports zero omissions, aligned-array errors, and
reverse-adjacency errors.  This theorem classifies only the one-edge
objective-twelve boundary of (S_{10}); it does not claim threshold-eleven or
threshold-twelve closure.

### Reproduction and independent verification

Build and regenerate the full lower closure and frontier with:

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  objective_six_component.cpp -o objective_six_component
./objective_six_component certificate.json defect-cycle.json \
  --objective-seven-component /tmp/objective-seven-regression.json \
  --objective-eight-component /tmp/objective-eight-regression.json \
  --objective-nine-component /tmp/objective-nine-regression.json \
  --objective-ten-frontier objective-ten-frontier-fast.json \
  --objective-ten-component objective-ten-component-fast.json \
  > /tmp/objective-six-regression.json
```

The regenerated threshold-nine output was byte-for-byte identical to
`objective-nine-component-fast.json` before the new scan began. A separately
implemented checker then proves the frontier in both directions: it directly
recounts all \(\binom{43}{5}=962{,}598\) five-sets at every listed objective-ten
target and reconstructs each stored incidence signature; independently, it
recounts every source in \(P_9\) and verifies that every objective-ten exit is
present in the listed frontier. Run it with:

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_ten_frontier.cpp -o verify_objective_ten_frontier
OMP_NUM_THREADS=10 ./verify_objective_ten_frontier \
  objective-seven-frontier-fast.json \
  objective-seven-component-fast.json \
  objective-eight-component-fast.json \
  objective-nine-component-fast.json \
  objective-ten-frontier-fast.json \
  > objective-ten-component-independent.json

python3 analyze_objective_ten_boundary.py \
  objective-nine-frontier-fast.json \
  objective-nine-component-fast.json \
  objective-ten-frontier-fast.json \
  objective-ten-frontier-independent.json \
  > objective-ten-boundary-structure.json

python3 analyze_objective_ten_component_structure.py \
  objective-ten-frontier-fast.json \
  objective-ten-component-fast.json \
  objective-ten-component-independent.json \
  > objective-ten-component-structure.json

OMP_NUM_THREADS=10 ./verify_objective_ten_frontier \
  objective-seven-frontier-fast.json objective-seven-component-fast.json \
  objective-eight-component-fast.json objective-nine-component-fast.json \
  objective-ten-frontier-fast.json objective-ten-component-fast.json \
  /tmp/objective-eleven-frontier-direct.json \
  > /tmp/objective-ten-component-regenerated.json

g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  scan_objective_eleven_frontier.cpp -o scan_objective_eleven_frontier
./scan_objective_eleven_frontier \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json \
  /tmp/objective-eleven-frontier-fast.json

python3 summarize_objective_eleven_frontier.py \
  /tmp/objective-eleven-frontier-direct.json \
  /tmp/objective-eleven-frontier-fast.json \
  > objective-eleven-frontier-certificate.json

g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  scan_objective_twelve_shadow.cpp -o scan_objective_twelve_shadow
./scan_objective_twelve_shadow \
  certificate.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json objective-twelve-shadow-fast.json

g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_twelve_shadow.cpp -o verify_objective_twelve_shadow
OMP_NUM_THREADS=10 ./verify_objective_twelve_shadow \
  objective-ten-frontier-fast.json objective-ten-component-fast.json \
  objective-twelve-shadow-fast.json objective-twelve-shadow-direct.json
```

The independent checker found zero omitted frontier neighbors, zero wrong
objectives, zero noncanonical or nonfree targets, and zero signature
mismatches. Its source-side and target-side incidence totals agree in every
objective layer, and it independently reproduces all 196 signatures and the
degree spectrum above. It then performs its own direct five-set-recount closure
from the 376 first-expansion orbits. Its sorted list of all 527 added orbits and
every component aggregate agrees exactly with the separately implemented
optimized generator. For objective eleven, the same direct five-set engine and
a separate incremental persisted-certificate scanner agree on every one of the
372,974 sorted representatives, every aligned incidence signature, all 324
signature classes, and the complete source exit-level profile. The compact
certificate binds the regenerated full arrays by SHA-256.

### Novelty assessment, scope, and trust boundary

The committed Discovery Net graph was searched through indexed height 644 for
objective-ten, objective-eleven, threshold-ten, Cyclic(43), and `R(5,5)`
frontier classifications; no overlapping objective-ten or objective-eleven
result was found. The authoritative McKay data
page records the known 42-vertex Ramsey(5,5) graphs, while the current primary
upper-bound paper proves \(R(5,5)\leq 46\); neither source classifies this finite
perturbation frontier
([McKay data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
[Angeltveit--McKay, 2024](https://arxiv.org/abs/2409.15709)). This supports a
novelty assessment within the searched graph and sources, not a claim of
priority over all unpublished computation.

These theorems are exact finite computational classifications conditional on
the programs and persisted certificates. They do **not** determine \(R(5,5)\),
do not exclude disconnected sublevel-ten components outside \(P_{10}\), and do
not improve the global numerical bounds on \(R(5,5)\). The objective-eleven
frontier is complete relative to \(P_{10}\), but no threshold-eleven closure is
claimed. The optimized generator and direct verifier use separate closure and
objective-evaluation implementations, but share C++, the Cyclic(43) seed
convention, and the same persisted lower certificates; these are the remaining
common-mode trust boundaries. Canonical array digests and reproducible full
outputs allow a future formal or alternative-language verifier to check more
than aggregate prose.

The results above were regenerated with Homebrew GCC 16.2.0 and Python
3.12.12. The complete regression suite passed 29/29 tests. The threshold-nine
optimized closure and aggregate recount took 408.60 seconds; its independent
ten-thread direct recount with explicit reachability BFS took 32.79 seconds,
and the lower-island direct
recount plus two independent lift-connectivity checks took 14.61 seconds.
The combined regenerated lower closures and objective-ten frontier scan took
1,505.77 seconds under concurrent load. A fresh ten-thread expanded
bidirectional boundary recount took 221.78 seconds; the deterministic
certificate-intersection analysis took 0.90 seconds. The expanded ten-thread
direct verifier and complete threshold-ten closure took 228.94 seconds; the
independent optimized regeneration and closure took 2,030.69 seconds under
concurrent load. The quotient-geometry scan took 4.90 seconds. The ten-thread
direct objective-eleven scan took 207.42 seconds; the independent single-thread
incremental scan took 207.61 seconds alone and 333.73 seconds when rerun
concurrently with the direct checker.

SHA-256:

```text
1afeeb35cffb8995b293833855d76aa9e2ea56e5c3d10feb531e1b1fe736063b  objective_six_component.cpp
d963ccaabefd5838bbdf96632dfc3f767a903ee401e0d98c5dd1c936093fc79a  verify_objective_six_component.cpp
0913516c58ad591f51ef90862b185ee05f308613077ee9335df880946d015c48  verify_objective_ten_frontier.cpp
216a3726bf3e842731cadee81181a762dbdb9f0ec4f9aba46b7e73d22c8e688c  verify_external_objective_eight_components.py
885d86d8fa5dac7864c322101bdccb5d28231cc6b431a4b59b9da4148d9944ea  verify_threshold_nine_lower_islands.py
0f7c3c647e62007bcdefc4ba6e3bec732ec63b2a0a7055945c78e331961d1bbc  test_cyclic43.py
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
b3f361462d07ff2d01d766515f81ebab3a6fa48a7b34af40089a13d24544dd11  objective-eight-component-independent.json
ed95024d463512eb0ade0af77725dd8031ffc712e258283499cff6c06144a693  objective-nine-frontier-fast.json
892e1990095bfb0d714e1ce1dabd9a51b37bda8c114559ed5e67d353c482a295  objective-nine-frontier-independent.json
dee76687683f480bb3eeb788608bf0420c8d61fe5378558adb961acc42f160ff  external-objective-eight-components-fast.json
319f92ea07c57edf4a94a1fc89c60ab177a3bd4d02f73f4127f29c2c7979db78  external-objective-eight-components-independent.json
e04e0f20b5e2f696658e8e4258f437c31d29e928f531b3e951d42caa3daeefaa  objective-nine-component-fast.json
25fb32b4cfaf67130bdc9644c2cfa5448f604adc603855df7e39eb8953f8c0cb  objective-nine-component-independent.json
fe3a66d5d937bc109920e45b2c105e5cfa2dbdebbb56a3b25adf8f0686650c88  threshold-nine-lower-islands-independent.json
9b5b3b4747fedfba8b0191f052c9e6d2847aa9c910465f6c29358c2336977df4  objective-ten-frontier-fast.json
977ddfaa5ab06d43e28a0f2a1d13606d571d12e1a7fca06751651a719cefae56  objective-ten-frontier-independent.json
2a8eb47b4204801169ecae8f0734643d091455124ee2ee09ccba9698e9236551  analyze_objective_ten_boundary.py
a6fc7029bd7ec7d79fd5d50ea629db88878ea7f3e0b14d4a89aff354fe72bb72  objective-ten-boundary-structure.json
0c29669eb32ac4bb64f8bcffa38813cfdd258faae9701e070dbfdbe65284d4e4  analyze_objective_ten_component_structure.py
6a26775e85ad7a09574074e9fd615ca39f56f3508f85e12625c6ac2b4a34e076  objective-ten-component-structure.json
389a31ddb2546fd62da112b138757ee4cbd54577520e54d7d8e8d3cc0991b996  objective-ten-component-fast.json
ea791e04c6928dbd083afd428652ba1d9dbc895647d5f5f4961c1d22a95d4a14  objective-ten-component-independent.json
52b23b9f1c9b4be757b5f8fa011286ceb93a819af9f4006ec893d026b0e5438d  scan_objective_eleven_frontier.cpp
920a18275c90564d19b96653899f17dd77ae452c11b9f6383d39fab336f31ba6  summarize_objective_eleven_frontier.py
09f3046c6ed743c9523e8c6fcc6b0edf696b4d641761bed4ad745bacd65c41f4  objective-eleven-frontier-certificate.json
```

Certify a radius-five tube around all 38 vertices of that defect orbit:

```bash
python defect_orbit_tube.py \
  --checker ./local_rigidity_bounded \
  --orbit defect-orbit-primary.json \
  --radius 5 --jobs 4 \
  --output defect-orbit-tube-radius5.json
```

Every closed ball has exact minimum two. Their union contains exactly
186,056,295,651,406 distinct colorings after overlaps are removed, so any
coloring with at most one monochromatic `K5` is at least six edge reversals
from every orbit center. The script counts overlap using a reflection-principle
formula for distance from a binary word to the prefix chain; it does not
enumerate all `2^37` path-coordinate patterns.

Check a radius-six tube around every vertex of the 15-edge bridge:

```bash
python bridge_tube.py \
  --checker ./local_rigidity_bounded \
  --bridge plateau-bridge.json \
  --radius 6 --jobs 4 \
  --output bridge-tube-radius6.json
```

All 16 centers have exact closed-ball minimum two. Accounting exactly for ball
overlaps, their union contains 11,711,422,789,686,316 distinct colorings—about
15.71 times one radius-six ball. Any coloring with at most one monochromatic
`K5` is therefore at least seven edge reversals from every bridge center.
Per-center search counts and the overlap calculation are stored in
`bridge-tube-radius6.json`.

At any partial perturbation with at least two monochromatic `K5`s, a final
coloring with at most one must change an edge in at least one of any two chosen
current witnesses. The checker branches on precisely that union of at most 20
edges and memoizes the resulting flip sets. Because the total radius is at most
six, changing all ten edges of a current witness and making it monochromatic in
the opposite color is impossible. This gives a complete search rather than a
heuristic local search. The persisted radius-six outputs are
`local-rigidity-radius6-primary.json` and `local-rigidity-radius6-fm.json`.

The MaxSAT solver establishes optimality within the stated red-to-blue family.
The direct verifier checks the upper-bound coloring, but is not an independently
checkable proof of the MaxSAT lower bound; that solver trust boundary should be
kept explicit when citing the result. The radius-one through radius-three
scripts use exact finite enumeration and directly recount minimizing
perturbations. The radius-six result relies on the C++ exhaustive search and its
forced-hitting-set completeness argument; it is not a SAT proof certificate.

Primary sources and data context:

- https://arxiv.org/abs/2212.12630
- https://doi.org/10.1002/jgt.70029
- https://users.cecs.anu.edu.au/~bdm/data/ramsey.html
