# Correction and exact matching-interface separation

This addendum repairs the indexing in the source supporting Discovery Net
height 2805 and proves a sharp obstruction to combining that local
conformal-diamond lemma with the Tutte interfaces formalized at heights 2815
and 2831.

The repair does not change the height-2805 proof mechanism. The separation
theorem below does not eliminate any `r=29` frontier row and is not an
Albertson counterexample.

## 1. Indexing repair at height 2805

The height-2805 body accidentally used `a_1` both in the triple and in the
first pair. It also displayed only `k-1` vertices in `N_H(v)`, although
`d_G(v)=k-1` in a graph of order `2k` gives `d_H(v)=k`.

The corrected labels are

```
B=N_G(v)={b_0,b_2,...,b_{k-1}},
A=N_H(v)={a_0,a_1,a_2,...,a_{k-1}},
C_0={b_0,a_0,a_1},       C_i={b_i,a_i}  (2 <= i <= k-1).
```

Thus `|B|=k-1`, `|A|=k`, and the matching outside the diamond is

```
M={a_i b_i : 2 <= i <= k-1}.
```

With this repair, every count and every path in the proof is well typed. In
particular the pair auxiliaries are `a_i` for `2<=i<=k-1`, while the two
special triple slots are the distinct vertices `a_0,a_1`.

## 2. A two-vertex-criticality separation family

### Theorem

For every integer `k>=5` there is a graph `G_k` of order `2k`, with connected
complement `H_k`, having the following properties.

1. `chi(G_k)=k`.
2. Exactly two vertices, denoted `v,b_0`, have degree `k-1` in `G_k`.
3. `chi(G_k-x)=k-1` for every vertex except `a_0,a_1`, whereas
   `chi(G_k-a_0)=chi(G_k-a_1)=k`.
4. At each of `v,b_0`, the corrected reciprocal `K_3+(k-2)K_2` factor is the
   unique optimal deletion factor, up to permuting its cliques.
5. At both low vertices, every leaf representative has auxiliary degree one,
   both special slots are available on every center--leaf path, and the
   height-2805 Hall-capacity test fails solely because the center has degree
   `k-2>=3`.

Consequently, connectedness, `k`-chromaticity, two low vertices, exact
chromatic equality after deleting either low vertex, and even uniqueness of
the reciprocal factors do not force cross-diamond capacity. Within this
family, the only missing vertex-criticality tests are deletion of the two
shared diamond endpoints `a_0,a_1`.

### Construction

Take

```
V(H_k)={v,b_0,a_0,a_1} union
       {a_i,b_i : 2 <= i <= k-1}.
```

The edge set of `H_k` consists exactly of

```
v a_0, v a_1, a_0 a_1, b_0 a_0, b_0 a_1,
v a_i, a_i b_i, b_0 b_i              (2 <= i <= k-1).
```

Let `G_k` be the complement of `H_k`.

### Proof

The graph `H_k` is connected. Its only triangles are

```
{v,a_0,a_1} and {b_0,a_0,a_1};
```

they share the edge `a_0a_1`, and `H_k` has no clique of order four. Hence a
partition of its `2k` vertices into `k-1` cliques is impossible: at most one
part can have order three, and all remaining parts have order at most two,
covering at most `3+2(k-2)=2k-1` vertices. On the other hand,

```
{v,a_0,a_1}, {b_0}, {a_i,b_i} (2<=i<=k-1)
```

is a partition into `k` cliques. Since clique covers of `H_k` are colorings
of its complement, `chi(G_k)=k`.

Deleting `v` leaves the unique triangle `{b_0,a_0,a_1}`; deleting `b_0`
leaves the unique triangle `{v,a_0,a_1}`. In either case the remaining
vertices have the unique perfect matching

```
M={a_i b_i : 2<=i<=k-1}.
```

An odd graph on `2k-1` vertices cannot be covered by `k-1` cliques of order
at most two, so the triangle is forced in every optimal deletion cover and
then `M` is forced. Thus both deletion chromatic numbers equal `k-1` and the
displayed factors are unique.

For `2<=i<=k-1`, deletion of `a_i` has the `(k-1)`-clique cover

```
{v,a_0,a_1}, {b_0,b_i}, {a_j,b_j} (j != i),
```

and deletion of `b_i` has the cover

```
{b_0,a_0,a_1}, {v,a_i}, {a_j,b_j} (j != i).
```

The lower bound `theta(H_k-x)>=theta(H_k)-1=k-1` makes these exact. By
contrast, `H_k-a_0` and `H_k-a_1` are triangle-free graphs of odd order
`2k-1`, so each needs at least `k` cliques. Restricting the displayed
`k`-clique cover of `H_k` shows equality. This proves the deletion claims.

Both `v` and `b_0` have degree `k` in `H_k`, hence degree `k-1` in `G_k`.
Every other vertex has degree strictly larger than `k-1` in `G_k` when
`k>=5`, so these are the only low vertices.

At `v`, the representative graph induced by

```
N_G(v)={b_0,b_2,...,b_{k-1}}
```

is the star with center `b_0` and all `k-2` leaves. For every leaf `b_i`,
both paths

```
b_0-a_i-a_0-b_i,       b_0-a_i-a_1-b_i
```

lie in `G_k`. Thus every availability set is `{0,1}` and Hall fails only
because there are `k-2>=3` sets. Interchanging `v` and `b_0`, and
interchanging `a_i` with `b_i` in every pair, gives the identical conclusion
at `b_0`. This proves the theorem.

## 3. Exact obstruction to the heights 2815/2831 bridge

The formal interface at height 2815 starts with an **odd factor-critical**
graph and a triangle `T` for which deleting `T` leaves **no** perfect
matching. The height-2831 composition obtains that nonconformality from the
strict chromatic hypothesis

```
chi(complement F) > (|V(F)|-1)/2.
```

The order-`2k` Albertson complement has even order and therefore is not
factor-critical. More decisively, each height-2805 odd deletion graph is on
`2k-1` vertices at exact equality

```
chi(G-v)=chi(G-b_0)=k-1,
```

and its distinguished triangle is conformal: deleting that triangle leaves
the displayed perfect matching `M`. Thus both triggers of the Tutte
extraction fail in the exact opposite direction. The family above shows
that this is not a cosmetic mismatch: all data visible in the two low-vertex
deletions can coexist with maximal center overload.

For a genuinely vertex-critical order-`2k` graph, Stehlik also supplies
conformal `K_3+(k-2)K_2` factors after deleting `a_0` and `a_1`. A viable
cross-diamond theorem must compare those two endpoint-deletion factors with
the shared matching `M`. Heights 2815 and 2831 neither produce those factors
nor constrain their overlap, because they concern nonconformal triangles
above the chromatic threshold. This is the exact hypothesis-alignment
obstruction.

## 4. Consequence for the order-58 frontier

At `k=29`, the construction has order 58, exactly two degree-28 vertices,
unique reciprocal factors, and a 27-leaf capacity obstruction at each low
vertex. It is **not** 29-critical: deletion of `a_0` or `a_1` leaves
chromatic number 29. It has 1567 edges, not one of the frontier edge counts
838--840, and makes no crossing-number or frontier-row claim.
Indeed `e(H_k)=3k-1`, so
`e(G_k)=binom(2k,2)-(3k-1)=2k^2-4k+1`.

Therefore no order-58 row is eliminated. The smallest credible route to
resume is an endpoint-deletion exchange theorem using the full
vertex-critical hypotheses

```
chi(G-a_0)=chi(G-a_1)=k-1
```

to couple the two new conformal factors to `M` and force either a capacity
factor or a `(k-1)`-clique cover of `H`. Further Tutte-summary manipulation,
without such cross-factor data, cannot distinguish the separation family
from the desired local conclusion.

## Trust boundary

The correction and separation theorem are elementary prose proofs. No
enumeration, solver, floating point, crossing table, topology classification,
or private data is used. The only external theorem needed for the final
Albertson interpretation is Stehlik's connected-complement coloring theorem;
the constructed family and all clique-cover calculations are self-contained.

Primary source for that external theorem: M. Stehlik, *Critical graphs with
connected complements*, Journal of Combinatorial Theory, Series B 89 (2003),
189--194, DOI `10.1016/S0095-8956(03)00069-8`.
