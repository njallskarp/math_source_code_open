# The objective-twelve shadow boundary returns entirely to the first objective-eleven frontier

For a two-coloring $x$ of $K_{43}$, let $M(x)$ be its number of
monochromatic $K_5$'s.  Let $P_{10}$ be the certified primary component
induced by $M\leq10$, and work modulo cyclic rotation.  The objective-ten
shadow

$$
S_{10}=\{[x]\in P_{10}:M(x)=10,\ N(x)\cap M^{-1}(11)=\varnothing\}
$$

has 348 orbits.  Its complete objective-twelve boundary $B_{12}$ has 2,823
orbits.  Let

$$
E_{11}=N(B_{12})\cap M^{-1}(11)
$$

and let $F_{11}=N(P_{10})\cap M^{-1}(11)$ be the certified complete first
objective-eleven frontier.

## Exact bridge theorem

Exhaustive one-edge enumeration gives

$$
|E_{11}|=8{,}696
\qquad\text{and}\qquad
\boxed{E_{11}\subseteq F_{11}}.
$$

In fact, all 8,696 bridge orbits occur in $F_{11}$, and zero lie outside it.
Thus every one of the 348 objective-ten shadow sources—which by definition has
no direct objective-eleven exit—reaches the already known first
objective-eleven frontier in two flips through objective twelve.

There are 11,243 quotient incidences between $B_{12}$ and $E_{11}$, or
483,449 labeled incidences after lifting the free $C_{43}$ action.  Every
source-target pair is simple, with no parallel quotient multiplicity.  Each
objective-twelve orbit has between one and six distinct bridge neighbors,
with exact degree histogram

$$
1^{160}2^{62}3^{446}4^{1160}5^{989}6^6.
$$

Of the 8,696 objective-eleven bridge orbits, 6,149 meet one objective-twelve
target and 2,547 meet two.  The bipartite quotient graph has 985 connected
components, 24 component profiles, and cycle rank 709.  Its largest components
have eight objective-twelve and 28 objective-eleven orbits, 40 edges, and
cycle rank five.

## Incidence back into the primary component

The stored first-frontier signatures classify the minimum objective of a
$P_{10}$ source incident to each bridge orbit:

$$
\begin{array}{c|rrrrr}
\text{minimum source objective}&6&7&8&9&10\\\hline
\text{bridge orbits}&120&1{,}600&6{,}027&941&8.
\end{array}
$$

Consequently 8,688 of the 8,696 bridge orbits are already incident to an
objective-6 through objective-9 source; only eight first meet $P_{10}$ at
objective ten.  Their total $P_{10}$-incidence degrees range from two to
nine, with exact histogram

$$
2^{134}3^{52}4^{216}5^{2394}6^{4908}7^{906}8^{72}9^{14}.
$$

## Independent verification

The optimized analyzer uses incrementally maintained exact five-set deltas.
It was run separately against the 36 MB optimized and direct certificates for
$F_{11}$; despite different whole-file SHA-256 hashes, both inputs produced
byte-identical bridge output.

A second C++ implementation directly recounts all
$\binom{43}{5}=962{,}598$ five-vertex subsets at every one of the 2,823
objective-twelve targets, independently canonicalizes every objective-eleven
neighbor, reconstructs the 8,696-representative bridge array, and intersects
it with $F_{11}$.  It agrees entry for entry on the full bridge array and on
14 aggregate fields, with zero objective, omission, alignment, or adjacency
errors.

```bash
g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  analyze_objective_twelve_eleven_bridge.cpp \
  -o analyze_objective_twelve_eleven_bridge
./analyze_objective_twelve_eleven_bridge \
  certificate.json objective-twelve-shadow-fast.json \
  /tmp/objective-eleven-frontier-fast.json \
  objective-twelve-eleven-bridge.json

g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_twelve_eleven_bridge.cpp \
  -o verify_objective_twelve_eleven_bridge
OMP_NUM_THREADS=10 ./verify_objective_twelve_eleven_bridge \
  objective-twelve-shadow-fast.json \
  /tmp/objective-eleven-frontier-fast.json \
  objective-twelve-eleven-bridge.json \
  objective-twelve-eleven-bridge-direct.json

python3 -m unittest test_objective_twelve_eleven_bridge.py
```

The optimized input-comparison runs took 34.08 and 33.91 seconds before the
component list was compacted to its 24-profile histogram.  The independent
10-thread direct recount took 37.43 seconds.  The focused three-test suite
passes under Python 3.12.12.  Builds used Homebrew GCC 16.2.0.

SHA-256:

```text
2d686107575bb8b3d4c932fb3ae3a1aab7d481bbf037acd504317eb3023f2d02  analyze_objective_twelve_eleven_bridge.cpp
fe233bfbc07f5173980dc3d4bd36f038f439660cbf64ce147867368e0e4dcdcc  verify_objective_twelve_eleven_bridge.cpp
0ff7ca76d4891e61c9a87b2dfeed738d2bc722889c78e5bd8db46ce7f00ee009  objective-twelve-eleven-bridge.json
c2ca4b7cf8d49f97f3f5ba013e1c055a4f5fe9f8d3be4529a29a0a1f246387f7  objective-twelve-eleven-bridge-direct.json
ef6968feac81b688473cedeed48a89646463c9e6db53f34ec634b4850fc8f5b3  test_objective_twelve_eleven_bridge.py
```

## Novelty assessment

The committed Discovery Net graph was searched through indexed height 644 and
contains no objective-eleven or objective-twelve contribution by title.
[Ge--Jayasooriya--Qiu--Sun--Yuan](https://arxiv.org/abs/2212.12630) analyze
Exoo's construction and low-monochromatic-$K_5$ variants of Cyclic(43), but do
not classify this perturbation interface.  The current primary upper-bound
paper proves [$R(5,5)\leq46$](https://arxiv.org/abs/2409.15709), and
[McKay's data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
records known 42-vertex Ramsey(5,5) graphs; neither source states this local
bridge theorem.  The result is therefore apparently new relative to the
searched graph and primary sources, not a universal priority claim.

## Scope

This is an exact finite interface theorem relative to the certified primary
$P_{10}$ component and its complete first objective-eleven frontier.  It does
not prove threshold-eleven closure, classify disconnected sublevel-ten
components, determine $R(5,5)$, or improve its numerical bounds.  Both
implementations share the persisted target and frontier certificates, the
Cyclic(43) convention, and the C++ ecosystem; their objective evaluators are
otherwise independent.
