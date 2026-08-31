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
