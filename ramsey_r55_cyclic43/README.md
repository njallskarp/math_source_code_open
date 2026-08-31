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
