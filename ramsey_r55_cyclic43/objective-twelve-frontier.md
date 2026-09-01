# Complete objective-twelve boundary of the primary Cyclic(43) sublevel-eleven component

## Setting

Let $M(x)$ be the number of monochromatic copies of $K_5$ in the red-blue
coloring of $K_{43}$ encoded by $x$.  Let $P_{11}$ be the previously certified
connected component containing the Cyclic(43) optimum in the graph induced by
$M\leq 11$.  That component has $24{,}260{,}213$ labeled vertices and its
objective-eleven layer has $373{,}124$ free $C_{43}$-rotation orbits.

Define its complete one-flip objective-twelve boundary by

$$
F_{12}=\{y:M(y)=12,\ \exists x\in P_{11}\text{ with }d(x,y)=1\}.
$$

The computation below scans all 903 edge flips at every one of the $564{,}191$
rotation-orbit representatives in $P_{11}$, including every source objective
from 2 through 11.

## Exact computational theorem

The complete boundary has

$$
\boxed{|F_{12}/C_{43}|=1{,}041{,}887}
$$

free rotation orbits, representing exactly $44{,}801{,}141$ labeled
colorings.  The source-boundary incidence graph has $4{,}656{,}506$ quotient
incidences, hence $200{,}229{,}758$ labeled incidences.  There are
$4{,}656{,}503$ distinct source-target orbit pairs, so only three incidences
are quotient-parallel excess.

The boundary does **not** collapse to the neighbors of the top layer.  Its
target decomposition is

$$
\begin{array}{c|r}
\text{target class}&\text{rotation orbits}\\\hline
\text{adjacent to some source of objective at most 10}&1{,}024{,}348\\
\text{adjacent to some objective-eleven source}&931{,}507\\
\text{adjacent to both classes}&913{,}968\\
\text{lower-only}&110{,}380\\
\text{objective-eleven-only}&17{,}539
\end{array}
$$

Thus a natural compression heuristic suggested by the earlier two-flip shadow
bridge is false: $110{,}380$ objective-twelve boundary orbits have no neighbor
in the complete objective-eleven layer.  Their minimum incident source
objective has exact histogram

$$
\begin{array}{c|rrrrrrrrr}
\min M(x)&2&3&4&5&6&7&8&9&10\\\hline
\#&86&42&777&2{,}196&6{,}118&12{,}263&29{,}546&51{,}454&7{,}898.
\end{array}
$$

This is a structural counterexample to that reduction heuristic, not a
counterexample to any published Ramsey conjecture.

## Effect of the final threshold-eleven closure

The final 150 objective-eleven orbits added beyond the first frontier touch
exactly 1,022 objective-twelve targets.  Of these, 654 are not touched by the
original $372{,}974$-orbit first frontier, while 368 are touched by both.  The
previously certified $2{,}823$-orbit objective-twelve boundary of the
348-orbit objective-ten shadow is contained in $F_{12}$ in full.

## Quotient geometry

The complete bipartite quotient graph between incident sources in $P_{11}$
and targets in $F_{12}$ has only four connected components.  Their exact
profiles $(\#\text{sources},\#\text{targets},\#\text{edges},\text{cycle rank})$
are

$$
\begin{aligned}
&(282{,}383,521{,}734,2{,}336{,}601,1{,}532{,}485),\\
&(281{,}398,520{,}126,2{,}319{,}878,1{,}518{,}355),\\
&(1,15,15,0),\\
&(1,12,12,0).
\end{aligned}
$$

The two exceptional components are stars, while the two giant components
carry all remaining incidence.  The objective-eleven-only source-boundary
subgraph is much more fragmented: it has 33,358 components and total cycle
rank 759,978.  Adding the lower-layer incidences therefore performs a dramatic
component merger.

## Independent verification

The optimized engine maintains exact single-edge objective deltas while it
walks the certified representatives.  A separate verifier instead reconstructs
every coloring and directly enumerates all
$\binom{43}{5}=962{,}598$ five-vertex sets at each of the $564{,}191$ sources,
for $543{,}089{,}128{,}218$ five-set evaluations.  It independently rebuilds
all 903 deltas, canonicalizes every objective-twelve neighbor under $C_{43}$,
and partitions targets into lower-derived and objective-eleven-derived sets.

The direct verifier reported:

- zero omitted targets and zero unexpected targets against the complete sorted
  $1{,}041{,}887$-representative array;
- zero source-objective errors;
- zero nonfree target encounters;
- exact agreement on total incidences, distinct pairs, the three parallel
  excess incidences, every per-objective incidence count, every per-objective
  source-degree histogram, and all lower/top target intersections.

The optimized and direct q=11 frontier inputs were independently generated and
have distinct full-file hashes.  The temporary 75 MB full objective-twelve
representative array is deliberately not committed; its SHA-256 digest is
preserved in the compact certificate, and the committed programs regenerate
it.

## Reproduction

Compiler and runtime used:

```text
g++-16 (Homebrew GCC 16.2.0) 16.2.0
Python 3.12.12
OMP_NUM_THREADS=10
```

Optimized enumeration:

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  -Wall -Wextra -Wpedantic analyze_objective_twelve_frontier.cpp \
  -o /tmp/analyze_objective_twelve_frontier

OMP_NUM_THREADS=10 /tmp/analyze_objective_twelve_frontier \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json \
  /tmp/node-njall-2-objective-eleven-frontier-fast-v2.json \
  objective-eleven-component-fast.json objective-twelve-shadow-fast.json \
  /tmp/objective-twelve-full-frontier-fast-summary.json \
  /tmp/objective-twelve-full-frontier-fast-targets.json
```

Independent direct recount:

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  -Wall -Wextra -Wpedantic verify_objective_twelve_frontier.cpp \
  -o /tmp/verify_objective_twelve_frontier

OMP_NUM_THREADS=10 /tmp/verify_objective_twelve_frontier \
  objective-seven-frontier-fast.json objective-seven-component-fast.json \
  objective-eight-component-fast.json objective-nine-component-fast.json \
  objective-ten-frontier-fast.json objective-ten-component-fast.json \
  /tmp/node-njall-2-objective-eleven-frontier-direct-v2.json \
  objective-eleven-component-fast.json \
  /tmp/objective-twelve-full-frontier-fast-targets.json \
  /tmp/objective-twelve-full-frontier-direct-summary.json
```

Compact certificate:

```bash
python3 summarize_objective_twelve_frontier.py \
  /tmp/objective-twelve-full-frontier-fast-summary.json \
  /tmp/objective-twelve-full-frontier-direct-summary.json \
  /tmp/objective-twelve-full-frontier-fast-targets.json \
  /tmp/node-njall-2-objective-eleven-frontier-fast-v2.json \
  /tmp/node-njall-2-objective-eleven-frontier-direct-v2.json \
  > objective-twelve-frontier-certificate.json

python3 -m unittest test_objective_twelve_frontier.py
```

SHA-256 values:

```text
analyze_objective_twelve_frontier.cpp
  f335174238d42491b85a23cf9dc4f6bd5597812324d7ae9682b84aa6331784d2
verify_objective_twelve_frontier.cpp
  c1d10099223ccedc94ba7f30cfb6896ad1dcbdd0be3dfc8422568088797d3c41
summarize_objective_twelve_frontier.py
  9d7eab32feb7edf52aae0e18958e665918290c0936bff7583433117bb93433e1
objective-twelve-frontier-certificate.json
  e4390990fad91c8f9d7e584a7a4dbbc35d02d86b5971139376bee3895c51b5f1
test_objective_twelve_frontier.py
  af29e525ceb4e2d1dfdd41d7f7776e02cde0efaf0c2da3572b881a2df74cda73
temporary full objective-twelve representative file
  653d1068c456d228c12d640a50eca409fceaf570dbb6040b66bebef296b2615c
optimized q=11 frontier input
  9678d90da7d53da6efee8f659563bb65f0f08a6a90a27e601f5bd4d62bbe20cd
direct q=11 frontier input
  0fc958dbc17ada20115679851c4c1406e24fa630a92f0eb2f44e797ead1bbd86
```

## Literature and novelty assessment

The broader Cyclic(43) program is motivated by the low-monochromatic-$K_5$
construction of Exoo and its exact computational verification in Ge et al.,
*New lower bounds for Ramsey numbers $R(5,5)$ and $R(4,5)$*
(<https://arxiv.org/abs/2212.12630>), and is contextualized by the current
$R(5,5)\leq46$ upper-bound computation of Angeltveit and McKay
(<https://arxiv.org/abs/2409.15709>) and McKay's authoritative Ramsey graph
data (<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>).

No matching published classification of the complete Cyclic(43)
objective-twelve perturbation boundary was found in those sources or their
associated data.  The result is therefore apparently new to the searched
sources, but no priority claim is made without a broader literature and author
search.

## Scope and trust boundary

This theorem is complete for the one-edge objective-twelve boundary of the
already certified connected primary component $P_{11}$.  It does not classify
disconnected colorings with $M\leq11$, close the threshold-twelve component,
or determine $R(5,5)$.  The certificate depends on the completeness of the
committed lower-layer and objective-eleven source certificates, the two C++
implementations, the compiler/runtime, and the SHA-256 bridge to the temporary
full target list.  The independent direct pass materially reduces, but does
not eliminate, that computational trust boundary.
