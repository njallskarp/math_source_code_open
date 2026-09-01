# Objective-eleven growth caused by closing the Cyclic(43) threshold-ten component

## Exact statement

Let \(P_9\) be the certified primary sublevel-nine component, let \(F_{10}\)
be its 128,184-orbit first objective-ten frontier, and let \(A_{10}\) be the
527 additional objective-ten rotation orbits needed to close the primary
sublevel-ten component \(P_{10}\).  For a source set \(S\), write

\[
B_{11}(S)=\{[y]: M(y)=11,\ d_H(x,y)=1\text{ for some }[x]\in S\}.
\]

Two independent global enumerators agree, representative for representative
and incidence signature for incidence signature, that

\[
|B_{11}(P_{10})|=372{,}974
\]

rotation orbits.  The exact quotient incidence from \(P_{10}\) to this
frontier is 1,557,119.

The pre-closure source set \(P_9\cup F_{10}\) sees exactly 370,581 of these
target orbits through 1,552,780 quotient incidences.  Scanning every one-edge
move from \(A_{10}\) gives

\[
|B_{11}(A_{10})|=3{,}393,
\qquad I(A_{10},B_{11})=4{,}339.
\]

Exactly 1,000 of those targets were already incident to \(P_9\cup F_{10}\),
whereas

\[
\boxed{2{,}393}
\]

are exposed for the first time by completing the threshold-ten closure.  The
new target set therefore contains 102,899 labeled colorings.  There is no
parallel source-target incidence among the 4,339 quotient moves.

## Degree and component structure

Every one of the 527 added sources has between four and thirteen distinct
objective-eleven exits.  On the target side, 2,593 orbits meet one added
source, 654 meet two, and 146 meet three.

Deleting the old frontier leaves 21 connected components in \(A_{10}\).  At
level eleven, 738 target orbits meet sources in more than one such component:
730 meet two components and eight meet three.  The resulting component
intersection graph has 21 vertices and 29 edges.  It consists of one
13-component connected block and eight isolated vertices, and has cycle rank

\[
29-21+9=17.
\]

Thus the first objective-eleven layer already couples most of the formerly
separate threshold-ten addition, while eight small components remain isolated
at this one-step interface.

## Reflection symmetry

Reflection preserves both the 3,393 touched targets and the 2,393 newly
exposed targets.  Exactly five rotation orbits are reflection-fixed, and all
five are newly exposed.  Consequently the touched and newly exposed target
sets contain respectively

\[
\frac{3393+5}{2}=1{,}699,
\qquad
\frac{2393+5}{2}=1{,}199
\]

dihedral orbits.

## Reproduction

Generate the complete frontier independently by the optimized incremental
scanner and direct five-set recount:

~~~bash
g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  scan_objective_eleven_frontier.cpp -o /tmp/objective-eleven-fast
/tmp/objective-eleven-fast \
  certificate.json objective-seven-frontier-fast.json \
  objective-seven-component-fast.json objective-eight-component-fast.json \
  objective-nine-component-fast.json objective-ten-frontier-fast.json \
  objective-ten-component-fast.json /tmp/objective-eleven-fast.json

g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_ten_frontier.cpp -o /tmp/objective-eleven-direct
OMP_NUM_THREADS=10 /tmp/objective-eleven-direct \
  objective-seven-frontier-fast.json objective-seven-component-fast.json \
  objective-eight-component-fast.json objective-nine-component-fast.json \
  objective-ten-frontier-fast.json objective-ten-component-fast.json \
  /tmp/objective-eleven-direct.json

python3 analyze_objective_eleven_addition.py \
  /tmp/objective-eleven-fast.json \
  objective-ten-frontier-fast.json objective-ten-component-fast.json \
  objective-ten-component-independent.json \
  objective-ten-component-structure.json \
  --independent-objective-eleven-frontier \
  /tmp/objective-eleven-direct.json \
  > objective-eleven-addition-structure.json

python3 -m unittest test_objective_eleven_addition.py
~~~

The compact analysis takes under 25 seconds, including loading and comparing
both global certificates.  The persisted result regenerates byte-for-byte and
the five focused tests pass.  The runs used Homebrew GCC 16.2.0 and Python
3.12.12.

SHA-256:

~~~text
a9b69971d2ee14188868b93df87b05304905f3c8f54357bd5ce8b177340cf3d4  analyze_objective_eleven_addition.py
74b9c4e0be3b20ed4a6e0a329a19de4bbe963751818adeb8df708a4ccd774265  objective-eleven-addition-structure.json
55e2e1eb428b50b45feabd6f5ed755a3454ff0c33c79b0ac8b220e60becc10b0  test_objective_eleven_addition.py
~~~

## Novelty and scope

The committed Discovery Net graph was searched through indexed height 644 and
contained no objective-ten or objective-eleven Cyclic(43) classification.  The
authoritative McKay data page and the current upper-bound paper do not classify
this finite perturbation frontier
([McKay data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
[Angeltveit--McKay, 2024](https://arxiv.org/abs/2409.15709)).  This supports
apparent novelty relative to the searched graph and sources, not universal
priority.

This is an exact finite computational classification conditional on the two
frontier programs and persisted certificates.  It does not close the
threshold-eleven component, exclude disconnected sublevel-ten components,
determine \(R(5,5)\), or improve its global numerical bounds.  The two global
enumerators evaluate objectives independently, but share C++, the cyclic seed
convention, and the lower certificate files.  The compact analyzer does not
recount monochromatic five-sets; it consumes their agreed target and incidence
certificates and independently reconstructs the 527-source quotient geometry.
