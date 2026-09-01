# Complete primary Cyclic(43) sublevel-twelve component and exact escape level thirteen

## Setting and dependency

Continue with the certified primary component (P_{11}), its complete
objective-twelve boundary (F_{12}), and the exact 229-orbit first expansion
(A_{12}^{(1)}).  Let (P_{12}) be the connected component containing the
Cyclic(43) optimum in the one-edge graph induced by (M\leq12).

## Exact closure theorem

Exact orbit-canonical breadth-first search from the 229 first-expansion seeds
discovers only nine further orbits, all at objective twelve.  Scanning those
nine finds no additional state of objective at most twelve.  Therefore

\[
P_{12}\setminus(P_{11}\cup F_{12})
\]

contains exactly 238 free rotation orbits, and the complete objective-twelve
layer has

\[
\boxed{1{,}041{,}887+238=1{,}042{,}125}
\]

rotation orbits, representing 44,811,375 labeled colorings.

The complete component has

\[
\boxed{|V(P_{12})|=69{,}071{,}588},
\qquad
\boxed{|E(P_{12})|=405{,}458{,}094}.
\]

Its edge census decomposes exactly as

\[
\begin{array}{c|r}
\text{edge class}&\text{labeled edges}\\\hline
P_{11}\text{ internal}&133{,}822{,}192\\
P_{11}\leftrightarrow F_{12}&200{,}229{,}758\\
F_{12}\text{ internal}&71{,}339{,}967\\
F_{12}\leftrightarrow\text{ closure addition}&56{,}201\\
\text{closure addition internal}&9{,}976
\end{array}
\]

and these five terms sum to 405,458,094.

Every one of the 238 added sources has minimum neighbor objective twelve and
minimum external-neighbor objective thirteen.  The full frontier scan also
contains objective-thirteen exits.  Since every possible move of objective at
most twelve from every newly added state was exhausted, the exact escape level
is

\[
\boxed{13}.
\]

No newly reached orbit of objective at most eleven occurs anywhere in the
closure addition.

## Independent direct breadth-first reproduction

The optimized closure uses the incremental exact-delta engine.  A separate
verifier directly enumerates all (\binom{43}{5}=962{,}598) five-sets at each
of the 238 addition sources and independently performs cyclic breadth-first
closure from the 229 seeds.  It reproduced the complete 238-representative set
entry for entry and rediscovered exactly the final nine-orbit shell.

The direct pass also reproduced 1,307 reverse incidences to (F_{12}), 464
directed incidences within the addition, 213,143 exits above twelve, and both
minimum-objective histograms.  It found zero omitted expected states, zero
unexpected states, zero omitted sublevel neighbors, zero objective errors,
and zero canonicality or orbit errors.

## Reproduction and hashes

Immutable source, exact representative certificates, direct output, and tests:

<https://github.com/njallskarp/math_source_code_open/commit/36115a3fad927845b31f5ba23df093e4d172e7e8>

```bash
g++-16 -std=c++20 -O3 -march=native -DNDEBUG \
  close_objective_twelve_component.cpp \
  -o /tmp/close_objective_twelve_component

g++-16 -std=c++20 -O3 -march=native -fopenmp -DNDEBUG \
  verify_objective_twelve_component.cpp \
  -o /tmp/verify_objective_twelve_component

python3 -m unittest test_objective_twelve_component.py
```

```text
6046df2f837f88fb5280dec092306ad0a7d5a015c4e9cca854cc5f14cd3875f9  close_objective_twelve_component.cpp
64273d1df10d8e41adcb3ad703a493e3cf82e9af7b1013f5f56950d56ddda7e5  verify_objective_twelve_component.cpp
4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3  objective-twelve-component-fast.json
882be899220a74dc6ca99744668d96b5af61fe8a9d6468b4a0523ac45cbe58fd  objective-twelve-component-direct.json
88acb9691e188713310fd551153d221734f3ba98c992033c589c467df2a966f3  test_objective_twelve_component.py
```

## Mathematical significance and novelty assessment

This is a finite structural reduction: the entire one-flip basin through
objective twelve around the best-known Cyclic(43) perturbation is now exactly
classified, and it is separated from every still-unknown state by an
objective-thirteen barrier.  The unexpectedly small (229+9) closure beyond a
million-orbit first boundary supplies a concrete sparsity phenomenon that may
guide higher-threshold and disconnected-island searches.

The primary literature searched was Ge et al.
(<https://arxiv.org/abs/2212.12630>), Angeltveit--McKay
(<https://arxiv.org/abs/2409.15709>), and McKay's Ramsey graph data
(<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>).  The committed graph
was refreshed against the complete (F_{12}) theorem and its reviews.  No
matching threshold-twelve closure classification was found.  Apparent novelty
is asserted only relative to these searched sources, not as a historical
priority claim.

## Scope and trust boundary

The theorem is complete for the connected component containing the chosen
Cyclic(43) optimum.  It does not rule out disconnected colorings with
(M\leq12), construct a (K_5)-free coloring of (K_{43}), determine
(R(5,5)), or improve its current global bounds.  The two implementations
share the fixed perturbation encoding, persisted source certificates, C++, and
some rotation logic.  Agreement on all representatives and all reverse
incidences materially narrows but does not eliminate compiler, hardware, and
shared-convention risk.
