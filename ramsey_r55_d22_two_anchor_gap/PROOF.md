# The binary interface missed by one-edge two-anchor cuts

Let the colors be encoded by red indicators.  Fix roots `0` and `3`.  An
edge between two other vertices is **diagonal** when the endpoints have
opposite red/blue incidence to both roots.  These, and only these, are the
edges that occur in none of the four monochromatic neighborhoods of the two
roots.  All other edges are called exposed.

For a diagonal edge `e`, a five-set with `e` as its only diagonal edge and
all nine exposed edges red forces `e` blue.  The analogous all-blue five-set
forces `e` red.  These are the width-one residual clauses.

The supplied incidence matrix has 210 diagonal edges.  Exhaustive direct
enumeration gives seven distinct red width-one clauses and thirteen distinct
blue width-one clauses.  Their edge sets are disjoint.  Consequently all
width-one clauses are simultaneously satisfiable: assign every edge in the
first set blue and every edge in the second set red.

Nevertheless, put

```text
e = {4,32},       f = {4,35}.
```

The following three five-sets use only exposed edges except for the displayed
holes:

```text
{4,8,9,11,32}:       nine exposed edges blue, hole e;
{4,8,9,11,35}:       nine exposed edges blue, hole f;
{4,23,32,35,38}:     eight exposed edges red, holes e,f.
```

Writing `x_e,x_f` for their red indicators, absence of a monochromatic
five-clique gives

```text
x_e >= 1,
x_f >= 1,
x_e + x_f <= 1.
```

This is impossible.  Thus the complete fixed-neighborhood instance has no
Ramsey completion, but its entire width-one residual subsystem is feasible.
The least clause width that detects this instance is exactly two.

The same matrix also satisfies the tight global degree/edge conditions and
the complete local constraints at both roots.  Its four neighborhood profiles
are

```text
(root,color,order,same-color edges,deficiency)
(0,R,22,108,6), (0,B,20,100,0),
(3,R,21,95,12), (3,B,21,101,6).
```

This is a limitation witness for a proposed family-wide transfer of the
height-2811 one-edge mechanism.  It is not a red/blue coloring without a
monochromatic `K5`: the stored arbitrary diagonal completion has 336 red and
223 blue five-cliques.  Nor does the three-clause proof exclude every
`d=22,t>=108` profile.  It pinpoints the next omitted interface as coupled
constraints on at least two diagonal edges.

