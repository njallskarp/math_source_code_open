# Independent NumPy verification and quotient geometry of the Cyclic(43) threshold-twelve closure

## Verified closure theorem

Let $P_{11}$ be the certified primary Cyclic(43) component in the one-edge
graph induced by $M\leq11$, let $F_{12}$ be its complete objective-twelve
boundary, and let $A_{12}$ be the 238 objective-twelve rotation orbits added
when closing the component at threshold twelve.  A third implementation,
written in Python and NumPy, independently checks every one of the

$$
238\cdot\binom{43}{2}=214{,}914
$$

directed one-edge moves from $A_{12}$.  It directly rebuilds all
$\binom{43}{5}=962{,}598$ five-sets, evaluates exact monochromatic-$K_5$
deltas, constructs the $C_{43}$ edge action and canonical word ordering from
scratch, and streams the hash-pinned 1,041,887-representative array for
frontier membership.

The independent census is

$$
214{,}914=1{,}307+464+213{,}143,
$$

where the terms are respectively moves from $A_{12}$ to $F_{12}$, moves
inside $A_{12}$, and moves to objective above twelve.  There are no moves to
objective at most eleven and no omitted objective-twelve target.  Every one
of the 238 sources has objective twelve, minimum neighbor objective twelve,
and minimum external-neighbor objective thirteen.  The independently rebuilt
adjacency graph reaches all 238 representatives from the 229 first-expansion
seeds and discovers exactly the final nine states.  This reproduces the exact
escape level thirteen without reusing either C++ objective evaluator.

The full directed-neighbor objective histogram, from objective 12 through
56, is preserved in `objective-twelve-component-numpy.json`.  In particular,
there are exactly 1,924 objective-thirteen exits.  Their per-source degree
histogram is

$$
1^2 2^6 3^2 4^3 5^6 6^{35} 7^{32} 8^{50}
9^{37} 10^{36} 11^{21} 12^2 13^4 14^2.
$$

## New quotient geometry of the 238-orbit addition

The induced quotient multigraph on $A_{12}$ has 238 vertices, 232 edges
counting multiplicity, 230 distinct unordered orbit pairs, no self-orbit
move, and exactly two parallel-edge excess.  It has 61 connected components
and total cycle rank

$$
232-238+61=55.
$$

The largest component has 36 vertices, 58 edges, and cycle rank 23.  The
final nine-orbit shell is exactly the set of nine addition vertices with no
direct incidence back to $F_{12}$.  It meets only three components:

- seven final-shell vertices join three seeds in a 10-vertex, 18-edge
  component of cycle rank nine;
- each remaining final-shell vertex lies with four seeds in a distinct
  five-vertex tree.

The seven vertices in the first group have addition degree four and exactly
eight objective-thirteen exits each.  The other two have addition degree two
and exactly three objective-thirteen exits each.

The interface back to $F_{12}$ meets only 1,196 distinct frontier orbits.
Their addition-source degree histogram is

$$
1^{1095}2^{93}3^6 4^2,
$$

which accounts for all 1,307 directed interface incidences.  Thus the
closure addition is not only tiny relative to the million-orbit boundary;
its attachment to that boundary is itself highly sparse.

## Independent method

For each persisted addition representative, the checker constructs the seed
coloring and toggles its perturbation edges.  NumPy evaluates the red-edge
count on every five-set.  A flip destroys a monochromatic five-set when its
red count is zero or ten, and creates one exactly when the count is one and
the unique red edge is flipped, or nine and the unique blue edge is flipped.
Exact `bincount` accumulation therefore produces all 903 objective deltas.

Only moves of resulting objective at most twelve require canonicalization.
The checker independently builds the 43 rotation permutations on the 903
edges and minimizes the resulting fifteen-word state encoding.  Every such
canonical target is found either in the persisted 238-orbit addition or in
the complete sorted frontier array; the frontier file is streamed rather
than loaded as Python objects, and strict ordering and uniqueness are checked
simultaneously.

## Reproduction

Immutable source, deterministic compact certificate, and tests:

<https://github.com/njallskarp/math_source_code_open/commit/36bb566edcaef1679349c61f2ae4d760de146c1a>

The recorded run used Python 3.12.12 and NumPy 2.2.2 and completed in about
17.8 seconds.

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

The deterministic output was regenerated twice with the same SHA-256, and
all 13 focused tests pass.

```text
af617fdd2d0d5f9cb90d0efd68a0fbadb26af82135707347f729d3bda2f338ae  verify_objective_twelve_component_numpy.py
f5e05f2ddaecdabe8648fdb865cb475e22738b09c630b8d876dd23012e4146b6  objective-twelve-component-numpy.json
b51c0f582a65768143a57d4fd938d812487dba0a89297c1567324a4375c957cf  test_objective_twelve_component_numpy.py
653d1068c456d228c12d640a50eca409fceaf570dbb6040b66bebef296b2615c  temporary complete frontier array
4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3  optimized closure certificate
```

## Novelty and scope

The closure theorem itself is reproduced, not claimed anew.  The exact
61-component addition geometry, two parallel excess edges, complete
neighbor-objective histogram, sparse 1,196-orbit frontier interface, and
three-component placement of the final shell were absent from the preceding
closure certificates and are computational refinements new to this source
chain.

This verification relies on the persisted 238 representatives, the 229 seeds,
and the hash-pinned complete frontier array.  It independently checks every
move from the claimed closure set and proves reachability of that set from the
seeds, but it does not independently reconstruct the million-orbit frontier
or enumerate disconnected colorings with $M\leq12$.  It neither constructs a
$K_5$-free coloring of $K_{43}$ nor changes the known global bounds on
$R(5,5)$.
