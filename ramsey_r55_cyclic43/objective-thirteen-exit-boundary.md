# Complete objective-thirteen exit boundary of the threshold-twelve closure addition

## Statement

Let $A_{12}$ be the 238 rotation orbits added when the primary Cyclic(43)
component is closed at objective twelve.  Scan every one of the

$$
238\binom{43}{2}=214{,}914
$$

one-edge moves from the persisted canonical representatives and retain those
whose resulting monochromatic-$K_5$ count is thirteen.  The resulting boundary
has exactly 1,924 directed quotient incidences and 1,785 distinct $C_{43}$
orbits.  All 1,785 target orbits are free.  There are 1,923 distinct
source-target orbit pairs: 1,922 have multiplicity one and one has multiplicity
two.

The number of distinct $A_{12}$ sources incident with a target has histogram

$$
1^{1655}2^{122}3^8.
$$

Counting the unique parallel incidence instead gives the raw target-degree
histogram $1^{1654}2^{123}3^8$.

## Exact preservation and one-edge contraction of support strata

Write the support signature of a state for the multiset of cyclic lengths of
its non-length-one toggles.  The three source families remain completely
separated at objective thirteen.  Their target sets and incidences are

$$
\begin{array}{c|r|r|r|l}
\text{source signature}&\text{sources}&\text{incidences}&
\text{distinct targets}&\text{target signatures}\\\hline
\varnothing&190&1510&1381&\varnothing^{1381}\\
\{5,16,16\}&38&394&386&\{5,16,16\}^{310},\{5,16\}^{76}\\
\{17,17,21\}&10&20&18&\{17,17,21\}^{6},\{17,21\}^{12}
\end{array}
$$

Every pairwise intersection of the three target sets is empty.  Thus an exit
from the length-one-only family remains length-one-only.  An exit from either
three-noncycle-edge family either preserves its signature or deletes one copy
of its repeated noncycle length.  No other noncycle length or signature
occurs.  This is stronger than separation of the induced graph on $A_{12}$:
the first higher-objective boundary also fails to bridge its three exact
support strata.

## Bipartite quotient geometry

Form the bipartite graph whose left vertices are the 238 source orbits, whose
right vertices are the 1,785 target orbits, and whose edges are distinct
source-target orbit pairs.  It has 164 connected components and simple cycle
rank 64.  Restoring the single parallel incidence gives multigraph cycle rank
65.  No component contains sources from two support families.  The exact
family totals are

$$
\begin{array}{c|r|r|r|r|r|r}
\text{source family}&\text{components}&L&R&E&\beta_1&\beta_1^{\rm multi}\\\hline
\varnothing&122&190&1381&1509&60&61\\
\{5,16,16\}&34&38&386&394&4&4\\
\{17,17,21\}&8&10&18&20&0&0
\end{array}
$$

Here $L,R,E$ denote source vertices, target vertices, and distinct pairs.  The
last family is therefore a forest even after quotient incidence multiplicity
is restored.

## Completeness and verification

The checker enumerates all 903 flips at each of the complete persisted 238
source representatives, using exact integer monochromatic-count deltas built
from all $\binom{43}{5}=962{,}598$ five-sets.  It canonicalizes every
objective-thirteen result under all 43 rotations.  It then decodes every one
of the 1,785 distinct targets, directly recounts its five-sets, rechecks its
canonical word, and checks freeness under the prime-order rotation action.
All objective, canonicalization, and freeness error counts are zero.

This proves completeness for the objective-thirteen exits **from $A_{12}$**.
It does not classify all objective-thirteen neighbors of the full closed
sublevel-twelve component $P_{12}$, close the objective-thirteen layer, or
exclude disconnected low-objective components.

Immutable implementation and certificate:

<https://github.com/njallskarp/math_source_code_open/commit/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14>

```bash
python3 verify_objective_twelve_component_numpy.py \
  /tmp/objective-twelve-full-frontier-fast-targets-v2.json \
  objective-twelve-frontier-certificate.json \
  objective-twelve-first-expansion-fast.json \
  objective-twelve-component-fast.json \
  objective-twelve-component-numpy.json

python3 -m unittest test_objective_twelve_component_numpy.py \
  test_objective_twelve_component.py test_objective_twelve_topology.py
```

The recorded Python 3.12.12 / NumPy 2.2.2 run took about 61 seconds.  Two full
regenerations were byte-for-byte identical, and all 15 focused tests passed.

```text
9912e4d399f66848cf843ed1477849829d5619700f6330e7881a51c8fc342483  verify_objective_twelve_component_numpy.py
89cf3246b07a3e444f5cca0d8b23275c7c834fe6e79a424135072c001cbefe48  objective-twelve-component-numpy.json
ba7292b37898f6bf0159edc52ac974d8330820c66116f110661b2aec9fc5ffdd  test_objective_twelve_component_numpy.py
653d1068c456d228c12d640a50eca409fceaf570dbb6040b66bebef296b2615c  temporary complete frontier array
```

## Significance and novelty scope

The preceding closure certificate reported the aggregate count of 1,924 exits
but did not canonicalize their targets.  The complete 1,785-orbit boundary,
its pair multiplicity, support-signature transition law, family-disjointness,
and 164-component incidence geometry are new refinements in this source chain.
They provide a sharply reduced starting set for closing threshold thirteen and
show that the three low-complexity support mechanisms remain decoupled for one
more objective layer.

This is an exact finite local-basin result, not an improvement to the global
bounds on $R(5,5)$ and not a construction of a $K_5$-free coloring of $K_{43}$.
Novelty is asserted only relative to the prior certificates and searched
Discovery Net graph; it is not a priority claim over unpublished computation.
