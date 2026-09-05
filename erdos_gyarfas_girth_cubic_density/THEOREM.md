# Girth-sensitive cubic-density theorem

All graphs below are finite, simple, and undirected.  A *dyadic cycle* is a
cycle of length `2^k` for an integer `k >= 2`.

Choose a graph `G` lexicographically minimally by `(number of vertices,
number of edges)` among graphs of minimum degree at least three having no
dyadic cycle.  Such a `G` is called a minimal counterexample.  Let

* `A = {v : d(v)=3}` and `a=|A|`;
* `B = {v : d(v)>=4}` and `b=|B|`;
* `g` be the girth of `G`.

The minimum-degree condition makes `g` finite.  Since `G` has no 4-cycle,
`g != 4` (and, similarly, `g != 8`).

## The theorem

Every minimal counterexample satisfies the exact integer inequality

    4b <= a + 2 floor(a/(g-1)).                         (1)

In particular,

    a / |V(G)| >= (4g-4)/(5g-3).                       (2)

If equality holds in (2), then every component of `G[A]` is a path on
`g-1` vertices, every vertex of `B` has degree four, and every such path has a
unique vertex of `B` adjacent to both endpoints.  That vertex has degree four,
and the path together with its two incident edges is a `g`-cycle.

Consequences include:

* the unrestricted estimate `a/|V(G)| >= 2/3`;
* if `G` is triangle-free, then `g>=5` and
  `a/|V(G)| >= 8/11`;
* if `g>=6`, then `a/|V(G)| >= 20/27`.

The last two bounds are strict improvements over `2/3`.  The rational function
`4(g-1)/(5g-3)` is increasing in `g` and tends to `4/5`.

## Proof

### 1. Minimality facts

Every nonempty proper subgraph `F` of `G` has minimum degree at most two.
Indeed, if `F` had minimum degree at least three, then either it would have
fewer vertices than `G`, or the same vertices and fewer edges.  Minimality
would give a dyadic cycle in `F`, hence in `G`, a contradiction.

The set `B` is independent.  If two vertices of degree at least four were
joined by an edge, deleting that edge would leave minimum degree at least
three, contradicting the preceding fact.

Every vertex of `G` has a neighbor in `A`.  For a vertex `v`, the graph `G-v`
is nonempty and proper, so it has a vertex `x` of degree at most two.  Deleting
one vertex lowers any surviving degree by at most one.  Thus `x` was a
degree-three neighbor of `v` in `G`.

It follows in particular that the induced graph `H=G[A]` has minimum degree at
least one.  Also, `G` is connected: otherwise one of its components would be a
nonempty proper subgraph of minimum degree at least three.

### 2. A component-radius lemma

If `B` is empty, then `a=|V(G)|` and both (1) and (2) are immediate.  Assume
that `B` is nonempty, and let `C` be a component of `H`.

Delete every vertex of `C`.  The resulting graph is nonempty and proper, so
some surviving vertex has degree at most two.  No vertex in `A\C` loses an
edge: an edge from `A\C` to `C` would join two components of `H`.  Therefore
there is a vertex `z` in `B` such that

    |N_G(z) intersect C| >= d_G(z)-2 >= 2.              (3)

Choose two distinct neighbors `x,y` of `z` in `C`, and let `P` be a shortest
`x`--`y` path in `C`.  The path `P`, together with `zx` and `zy`, is a simple
cycle.  Its length is `length(P)+2`, and hence the definition of girth gives

    length(P) >= g-2.

Thus every component `C` of `H` has at least `g-1` vertices.

### 3. Counting

Let `q` be the number of components of `H` and `e(H)` its number of edges.
Every component is connected, so the component-radius lemma gives

    q <= floor(a/(g-1)),
    e(H) >= a-q.

Count the cut between `A` and `B`.  From the `A` side,

    e(A,B) = 3a - 2e(H)
           <= a + 2q
           <= a + 2 floor(a/(g-1)).                    (4)

From the `B` side, independence of `B` and the definition of `B` give

    e(A,B) = sum_{z in B} d_G(z) >= 4b.                (5)

Combining (4) and (5) proves (1).  Dropping the floor yields

    4b <= ((g+1)/(g-1))a.

Consequently

    |V(G)| = a+b <= ((5g-3)/(4g-4))a,

which is (2).

### 4. Equality

Suppose equality holds in (2).  Then equality holds at every relaxed counting
step.  In particular, every component of `H` has exactly `g-1` vertices and is
a tree, while every vertex of `B` has degree four.

For a component `C`, choose `z` as in (3).  Any two neighbors of `z` in `C`
have distance at least `g-2`, while a tree on `g-1` vertices has diameter at
most `g-2`.  Hence `C` has diameter `g-2` and is the path on `g-1` vertices;
`z` is adjacent to its two endpoints.  There cannot be a third neighbor of
`z` in `C`, since three vertices in this path cannot be pairwise at distance
at least `g-2`.  Equation (3) then forces `d_G(z)=4`.

Finally this endpoint-closing vertex is unique.  Two distinct vertices both
adjacent to both endpoints would form a 4-cycle, which `G` does not contain.
This proves the equality classification.

## Trust boundary

The proof is elementary once the minimal-counterexample definition is fixed.
It uses no computation and no unverified claim about the existence of a
counterexample.  `verify_density.py` checks only the exact arithmetic
optimization and displayed specializations; it does not certify the universal
component-radius lemma.
