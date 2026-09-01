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

The ten-thread checker took 27.05 seconds. For all 42,815 representatives it
reconstructed the coloring, recounted all 962,598 five-sets, rebuilt all 903
single-flip deltas, checked canonicality and freeness, and tested every accepted
neighbor against the union of the old and new strata. It found zero objective,
canonicality, frontier-containment, or closure discrepancies and independently
reproduced every edge count, objective histogram, and escape level.

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

The results above were regenerated with Homebrew GCC 16.2.0 and Python
3.12.12. The complete regression suite passed 25/25 tests. The threshold-nine
optimized closure and aggregate recount took 408.60 seconds; its independent
ten-thread direct recount took 27.05 seconds, and the lower-island direct
recount plus two independent lift-connectivity checks took 14.61 seconds.

SHA-256:

```text
30cf95dc602ed8dc896f6fa0c3a5bec1e71b19cdfe4c87735a6240bed534f278  objective_six_component.cpp
653814991888928db6f189d351e59b9c60bef237afb911959109b88e4219909e  verify_objective_six_component.cpp
216a3726bf3e842731cadee81181a762dbdb9f0ec4f9aba46b7e73d22c8e688c  verify_external_objective_eight_components.py
885d86d8fa5dac7864c322101bdccb5d28231cc6b431a4b59b9da4148d9944ea  verify_threshold_nine_lower_islands.py
67dfb691d45e400bf79f3e6f067fc054eb0c7d357a0aad630835abee837f40a3  test_cyclic43.py
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
b3f361462d07ff2d01d766515f81ebab3a6fa48a7b34af40089a13d24544dd11  objective-eight-component-independent.json
ed95024d463512eb0ade0af77725dd8031ffc712e258283499cff6c06144a693  objective-nine-frontier-fast.json
892e1990095bfb0d714e1ce1dabd9a51b37bda8c114559ed5e67d353c482a295  objective-nine-frontier-independent.json
dee76687683f480bb3eeb788608bf0420c8d61fe5378558adb961acc42f160ff  external-objective-eight-components-fast.json
319f92ea07c57edf4a94a1fc89c60ab177a3bd4d02f73f4127f29c2c7979db78  external-objective-eight-components-independent.json
e04e0f20b5e2f696658e8e4258f437c31d29e928f531b3e951d42caa3daeefaa  objective-nine-component-fast.json
73407f74e324429f405b2b4cdaf4bbf4c6cb981b96f21a0ae794cf6fc8d24838  objective-nine-component-independent.json
fe3a66d5d937bc109920e45b2c105e5cfa2dbdebbb56a3b25adf8f0686650c88  threshold-nine-lower-islands-independent.json
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
