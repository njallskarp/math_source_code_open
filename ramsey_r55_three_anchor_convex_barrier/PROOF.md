# A convex barrier for the three-anchor K5 clause relaxation

## Precise relaxation

Use red indicators `X_uv` on the complete graph on vertices `0,...,42`.
Fix the red anchor triangle `A={0,3,9}` and the incidences of every other
vertex to it. Write `C_s` for the three-bit signature cells, in binary order.
Their sizes are

```text
(6,4,4,6,5,6,6,3).
```

Let `F` be the set of Boolean colorings with these fixed incidences, 452 red
edges, degree multiset `20^8 21^26 22^9`, both partners of root 0 having red
degree ten in its red core, and the following six full local conditions and
same-color edge counts:

```text
root,color,order,edges =
(0,R,22,108), (0,B,20,100),
(3,R,21, 99), (3,B,21, 96),
(9,R,21, 97), (9,B,21, 97).
```

In each neighborhood the root color has no K4 and the opposite color has no
K5. The root-0 red core therefore has deficiency six from 114. One may
additionally fix every cell-pair red edge count to the table below in `F`.

Consider the relaxation

```text
P = conv(F) intersect {x : 1 <= sum_{uv in choose(S,2)} x_uv <= 9
                          for every five-set S}.
```

Theorem: `P` is nonempty. The result remains true if `conv(F)` is replaced
by the convex hull of just the cell permutations of the supplied seed.
Consequently no rational Farkas combination of these constraints, including
arbitrary linear inequalities valid on `F` and all global K5 clauses, can
exclude this whole profile. The claim concerns this explicitly defined
relaxation; it does not assert that every earlier global Ramsey condition is
included, nor that a Ramsey coloring exists.

## Exact primal point and preservation of local information

The compact `SEED.json` reconstructs the height-2907 coloring `H`. Its
properties above are checked directly; no graph catalog or prior review is
assumed. Let

```text
Gamma = product_{s in {0,1}^3} Sym(C_s),
x = (1/|Gamma|) sum_{g in Gamma} 1_{E_red(gH)}.
```

The anchors are fixed. Every `gH` has the same signatures, edge count, degree
multiset, cell-pair edge counts, and local counts. Each of the six entire
neighborhoods is an isomorphic copy of the corresponding neighborhood in
`H`. Thus `gH` belongs to `F`, and `x` belongs to `conv(F)`. This also supplies
exact distributions on the six whole local graphs. They agree on all common
marginals, since all are restrictions of the single finite law `gH`.
The order of `Gamma` is `111451255603200000`; the uniform orbit description
is a compact exact certificate, not a demand to enumerate this group.

For `s<t`, let `e_st` count red edges between cells, and let `e_ss` count red
edges within a cell. Transitivity on cross pairs and on unordered within-cell
pairs gives

```text
x_uv = e_st/(n_s*n_t)       (u in C_s, v in C_t, s<t),
x_uv = e_ss/choose(n_s,2)   (distinct u,v in C_s).
```

Anchor incidences remain zero or one. The complete upper-triangular table
`e_st`, with row and column order `000,...,111`, is

```text
 4 13 15 20 19 23 20  8
    2  8 10 12 16 10  5
       1 10 13  9 14  9
          7 12 16 18  8
             5 14 15 10
                6 18  8
                   7  6
                      0
```

## Uniform proof of every global linear clause

All positive central edge densities in the table lie in `[1/6,3/4]`.
The only zero-density block is inside `C_111`, which has three vertices.
Any five-set outside `A` has at most `choose(3,2)=3` zero-density edges.
Therefore, uniformly over every such five-set,

```text
7/6 = (10-3)/6 <= sum x_uv <= 10*(3/4) = 15/2.
```

These bounds imply both K5 clauses. For a five-set meeting an anchor, every
`gH` is nonmonochromatic on that set: a monochromatic K5 containing the
anchor would give a same-color K4 in its neighborhood. Averaging its
integer edge count in `[1,9]` proves the two clauses there as well.
This proves `x in P` without a numerical solver or a large five-set census.

More generally, the same argument applies to any locally valid anchored
seed whose cell average has positive densities at least `a` and at most
`b`, and whose zero-density edges occupy at most `z` edges in each unanchored
five-set, whenever `(10-z)*a >= 1` and `10*b <= 9`.

## Why summing the orbit cuts cannot help

For multiplicities `m_s` summing to five, put

```text
N(m) = product_s choose(n_s,m_s),
L(m) = sum_s choose(m_s,2)*e_ss/choose(n_s,2)
       + sum_{s<t} m_s*m_t*e_st/(n_s*n_t).
```

Double counting edges over all five-sets with this signature multiset gives
exactly `N(m)*L(m)`. The sum of their K5 clauses is therefore
`1 <= L(m) <= 9` after dividing by positive `N(m)`.
Every one of the 88 mixed, complement-free patterns from height 2931
satisfies this inequality. Their exact mean range is `[77/20,31/5]`.
Thus all five orbit families, all their cell realizations, all nonnegative
weighted sums, and even the linear clauses for every other five-set survive
simultaneously. This closes the proposed linear aggregation test.

## The omitted joint events

Satisfying an expected clause does not make a distribution supported on
Ramsey colorings. Every `gH` still has 269 red and 200 blue K5s. For a fixed
five-set with signature multiset `(001,010,100,100,111)`, this law gives

```text
E[number of red edges] = 6,
P[all ten edges red] = 7/480.
```

For `(011,101,101,110,111)` the corresponding values are

```text
E[number of red edges] = 401/90,
P[all ten edges blue] = 1/810.
```

Cell permutations act transitively on the five-sets with a fixed signature
multiset, and the uniform group element gives a uniform image on this orbit.
These probabilities are therefore obtained by literally counting all 480
and 1620 five-sets of the respective types in `H`. They identify missing joint
ten-edge constraints. For example, for the first type the required Ramsey
identity `E[product_{e in choose(S,2)} X_e]=0` fails by exactly `7/480`.
Equivalently, multiplying the red clause slack by any nine of its red
indicators gives, on Boolean points,

```text
(product_{i=1}^9 X_i)*(9-sum_{i=1}^{10} X_i)
    = -product_{i=1}^{10} X_i.
```

Its expectation is negative for the displayed law. This is a concrete
omitted interface, not a claim of minimal hierarchy level. A different
global law with the same first moments is not ruled out by this example.

## Validation and scope

`verify.py` constructs the rational point, checks the six local Ramsey
conditions and the short density bound, and evaluates all 2165 realizable
five-set types. They represent all 962598 five-sets. `direct_check.py`
independently decodes the graph, visits all those literal vertex sets, and
adds their integer red-edge counts. The two complete tables agree through
the canonical digest in the expected outputs. The direct checker also
counts the two displayed forbidden joint events.

The proof uses elementary finite averaging and exact double counting. All
arithmetic is integer or rational. No SAT verdict, LP optimizer, floating
point, external catalog completeness, or independent peer-review verdict is
assumed. The checkers are two implementations by the same author; they are
not independent mathematical review. No bound on R(5,5) follows.
