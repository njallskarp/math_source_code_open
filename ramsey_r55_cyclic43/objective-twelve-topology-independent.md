# Independent topology reconstruction of the Cyclic(43) objective-twelve boundary

## Result

Let $P_{11}$ and $F_{12}$ be the primary sublevel-eleven component and its
complete objective-twelve one-flip boundary defined in
`objective-twelve-frontier.md`.  A new edge-streaming pass emitted every one
of the $4{,}656{,}506$ source-boundary incidences as an explicit pair of
integer endpoint IDs.  A separate Python implementation then reconstructed
the bipartite connected components with its own union-find; it does not reuse
the C++ disjoint-set implementation that produced the original certificate.

The independent component profiles are exactly

$$
\begin{aligned}
&(282{,}383,521{,}734,2{,}336{,}601,1{,}532{,}485),\\
&(281{,}398,520{,}126,2{,}319{,}878,1{,}518{,}355),\\
&(1,15,15,0),\\
&(1,12,12,0),
\end{aligned}
$$

where each tuple is (source vertices, target vertices, edges, cycle rank).
All $1{,}041{,}887$ target orbits occur, $563{,}783$ of the $564{,}191$
source orbits are incident, and the total cycle rank is $3{,}050{,}840$.
The objective-eleven-only subgraph independently has 33,358 components,
cycle rank 759,978, and 372,716 incident sources.  Its largest component is
$(9{,}258,19{,}399,54{,}902,26{,}246)$.

## Exceptional stars

The reconstruction also identifies the previously anonymous centers of the
two exceptional tree components.  Both are objective-eight source orbits,
and both perturb the Exoo seed only on the length-one cycle edges.  In the
deterministic concatenated source ordering their IDs and cycle-edge positions
are

$$
\begin{array}{c|c|l}
\text{source ID}&\text{star degree}&\text{positions }i\text{ for }\{i,i+1\}\\\hline
8207&15&5,6,13,14,15,16,22,23,25,29,31,32,38,39,40,41\\
11778&12&5,6,7,8,14,15,16,22,23,24,30,31,32,38,39,40,41.
\end{array}
$$

The two canonical source states have Hamming distance seven.  Their complete
target-ID lists, state edge IDs, and vertex pairs are stored in
`objective-twelve-topology-independent.json`.  This makes the finite anomaly
directly addressable in subsequent structural work instead of leaving it as
an aggregate component count.

## Independent method

`stream_objective_twelve_incidence.cpp` rescans all $564{,}191\cdot903$
source-edge pairs, checks each persisted source objective, canonicalizes every
objective-twelve endpoint under $C_{43}$, and looks it up in the sorted target
array.  It writes a simple little-endian stream of
`(uint32 source_id, uint32 target_id)` records plus source states and source
objectives.  It found no missing target, source-objective error, or nonfree
target encounter.

`verify_objective_twelve_topology.py` memory-maps that stream and performs
union-by-rank and path compression in Python, with only the final bulk parent
compression and counting delegated to NumPy.  It reconstructs the full and
objective-eleven-only graphs separately, compares their invariants with the
published frontier certificate, and recovers the exceptional sources from
their component roots.  Thus endpoint enumeration still shares the certified
C++ clique/canonicalization machinery, but the topology calculation and star
identification are independent of its original C++ disjoint-set logic.

## Reproduction

The run used Homebrew GCC 16.2.0, Python 3.12.12, NumPy 2.2.2, and ten OpenMP
threads.  Generate the temporary streams with

```bash
g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  -Wall -Wextra -Wpedantic stream_objective_twelve_incidence.cpp \
  -o /tmp/stream_objective_twelve_incidence

OMP_NUM_THREADS=10 /tmp/stream_objective_twelve_incidence \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json \
  /tmp/node-njall-2-objective-eleven-frontier-fast-v2.json \
  objective-eleven-component-fast.json \
  /tmp/objective-twelve-full-frontier-fast-targets-v2.json \
  /tmp/objective-twelve-incidence.bin \
  /tmp/objective-twelve-source-states.bin \
  /tmp/objective-twelve-source-objectives.bin \
  /tmp/objective-twelve-incidence-metadata.json
```

The complete scan took 235 seconds wall time.  Reconstruct and test with

```bash
python3 verify_objective_twelve_topology.py \
  /tmp/objective-twelve-incidence.bin \
  /tmp/objective-twelve-source-states.bin \
  /tmp/objective-twelve-source-objectives.bin \
  /tmp/objective-twelve-incidence-metadata.json \
  objective-twelve-frontier-certificate.json \
  objective-twelve-topology-independent.json

python3 -m unittest test_objective_twelve_topology.py \
  test_objective_twelve_frontier.py
```

The seven focused tests pass.  SHA-256 values are

```text
5751813a0f55aa342f78d98fef290716272534e8e8ae32b29bcdd5dbe6416443  temporary incidence stream
9363321bea9fa4a9fa4910e17065f5a7b6990648c4d558a35245463599691d1c  temporary source-state stream
825ad243414175291c83631c710c3bb535d79f6b0524d9c6727bd0660a0d907c  temporary source-objective stream
8d69afec18d29230af5c49268cf9bc24a933952557fc32d768af031600611bbc  temporary stream metadata
07542336fbb39f8926a7f3bd61545629a8fbeaa0ee7b5ba95645393ad7e5bae9  stream_objective_twelve_incidence.cpp
5707c290879b8d80ef32d118924f0e6ca2d921a3e4d7379e61d6e123e47a7158  verify_objective_twelve_topology.py
4388b3dc811a13d5f94f05e0fce2e27b17fb4e6c58821e005849be69d9c971e6  objective-twelve-topology-independent.json
3335bd1eb721f2669a513176c4ea7066b3ee3681bb385f4d99f3448bce9692d8  test_objective_twelve_topology.py
```

The large binary streams are temporary reproducibility intermediates and are
not committed.

## Scope

This closes the independent-topology objection to the complete persisted
$P_{11}$--$F_{12}$ incidence graph and adds exact identities for its two star
centers.  It does not independently reimplement endpoint enumeration, prove
threshold-twelve closure, classify disconnected sublevel-eleven states, or
determine $R(5,5)$.
