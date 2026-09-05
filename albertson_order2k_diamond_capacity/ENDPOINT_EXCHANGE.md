# Endpoint-factor overlays and singleton-availability exchanges

This note continues the corrected order-`2k` conformal-diamond setup. It
proves a structural overlap theorem for the factors obtained after deleting
the two special diamond endpoints, and then identifies the smallest overlay
component exactly with singleton Hall availability.

The result is uniform in `k`. It does not prove the full cross-diamond
capacity statement and does not eliminate an `r=29` frontier row.

## 1. Corrected setup

Let `G` be a `k`-vertex-critical graph on `2k` vertices, let `H=bar(G)` be
connected, and let `d_G(v)=k-1`. Use the corrected labels

```
B=N_G(v)={w,b_2,...,b_{k-1}},
A=N_H(v)={p,q,a_2,...,a_{k-1}},
C_0={w,p,q},             C_i={b_i,a_i} (2<=i<=k-1).
```

Put `M_i={a_i,b_i}` and `M={M_i:2<=i<=k-1}`. In `H`, the set
`{v,w,p,q}` is the diamond missing `vw`; the cover

```
P_v={{v},{w,p,q}} union M
```

is a minimum `k`-clique partition of `H`.

Stehlik's theorem applied at `p` gives another minimum `k`-clique partition

```
P_p={{p},T_p} union N_p,
```

where `T_p` is a triangle and `N_p` consists of `k-2` pairs. Define `P_q`
symmetrically.

For a complement edge `w b_i` (equivalently, an edge from the center in
`J=H[B]`), write its nonempty availability set as

```
S_i={s in {p,q}: w-a_i-s-b_i is a path in G}.
```

## 2. The block-incidence overlay theorem

### Definition

For two clique partitions `P,Q` of the same vertex set, their overlay
`Gamma(P,Q)` is the bipartite multigraph whose left nodes are the blocks of
`P`, whose right nodes are the blocks of `Q`, and which has one edge labelled
`x` between the two blocks containing `x`, for each graph vertex `x`.
Parallel edges are retained.

### Theorem

In `Gamma(P_v,P_p)`:

1. every connected component contains the same number of `P_v`-blocks and
   `P_p`-blocks;
2. the component containing the edge labelled `p` contains all four
   exceptional blocks: the singleton and triangle of both partitions;
3. that exceptional component is unicyclic and has at least three blocks on
   each side; and
4. every other component is an alternating cycle consisting entirely of
   pair blocks.

After deleting the leaf node `{p}` and its incident edge, the endpoint
triangle node `T_p` lies on the unique cycle of the exceptional component.
The symmetric statements hold for `Gamma(P_v,P_q)`.

### Proof

Let `K` be a connected component of the overlay and let `X_K` be the set of
labels on its edges. The set `X_K` is a union of whole blocks of each
partition. If the restriction of either partition to `X_K` were not a
minimum clique partition of `H[X_K]`, replacing it inside `X_K` would give a
clique partition of `H` with fewer than `k` blocks. Therefore both
restrictions are minimum, and the two sides of `K` have the same number,
say `r`, of block nodes.

For a side of the overlay, the sum of its block sizes is

```
2r + (number of triangle blocks) - (number of singleton blocks).
```

Both degree sums count the same labelled edges. Consequently, in every
component,

```
#(left triangles)-#(left singletons)
 = #(right triangles)-#(right singletons).                 (1)
```

The edge labelled `p` joins the left triangle `{w,p,q}` to the right
singleton `{p}`. In its component, (1) reads

```
1 - [left singleton present] = [right triangle present] - 1.
```

Both indicators must therefore equal one. This proves that the same
component also contains `{v}` and `T_p`, and hence all four exceptional
blocks.

All other components contain only pair blocks. They are connected
2-regular bipartite multigraphs, hence alternating cycles. In the exceptional
component the equal side sizes and the block sizes `1,3,2,...,2` give `2r`
nodes and `2r` labelled edges. It is connected, so it is unicyclic.

If `r=2`, the right triangle would have to be `{v,w,q}`, but `vw` is not an
edge of `H`. Thus `r>=3`. Finally, remove the right singleton `{p}` and its
leaf edge. The graph remains connected and unicyclic; the left triangle now
has degree two, the left singleton has degree one, the right triangle has
degree three, and every other node has degree two. The unique degree-three
node must lie on the unique cycle, proving the last assertion.

## 3. Exact six-vertex exchange criterion

Call `P_p` a **one-pair endpoint exchange at i** if its exceptional overlay
component has three blocks on each side, equivalently if its labelled vertex
set is exactly

```
{v,w,p,q,a_i,b_i}.
```

### Theorem

For every `i` with `w b_i in E(H)`, the following are equivalent:

1. `S_i={p}`;
2. there exists a one-pair endpoint exchange at `i` in `P_p`.

When these conditions hold, one of the following two explicit local
partitions, together with all `M_j` for `j!=i`, is a valid `P_p`:

```
{p}, {v,q,a_i}, {w,b_i};                                 (A)
{p}, {w,q,b_i}, {v,a_i}.                                 (B)
```

The symmetric equivalence holds with `p,q` interchanged.

### Proof

For `w b_i in E(H)`, bichromatic connectivity in the height-2805 argument
forces `w a_i notin E(H)`. Hence `s` belongs to `S_i` exactly when neither
edge from `s` to `M_i={a_i,b_i}` belongs to `H`.

Suppose first that `S_i={p}`. Then `p` has no neighbour in `M_i`, while `q`
has at least one. If `q a_i` is an edge of `H`, the three blocks in (A) are
cliques of `H`; if `q b_i` is an edge, the blocks in (B) are cliques. Adding
the unchanged pairs `M_j`, `j!=i`, gives a minimum `k`-clique partition with
singleton `p`. Its only nonshared component uses the displayed six vertices,
so it is a one-pair endpoint exchange.

Conversely, suppose a one-pair endpoint exchange exists. After the singleton
`p` is removed, its triangle and pair partition

```
{v,w,q,a_i,b_i}.
```

Within this set, `v` is adjacent in `H` only to `q` and `a_i`. If `v` lies
in the triangle, that triangle must be `{v,q,a_i}` and the remaining pair is
`{w,b_i}`, giving (A). If `v` lies in the pair, it is paired with `q` or
`a_i`. Pairing it with `q` would leave the triangle `{w,a_i,b_i}`, which is
impossible because `w b_i in E(H)` forces `w a_i notin E(H)`. Thus `v` is
paired with `a_i` and the triangle is `{w,q,b_i}`, giving (B).

In either case `q` has a neighbour in `M_i`, so `q` is unavailable. The
general Kempe argument makes `S_i` nonempty, hence `S_i={p}`.

## 4. Sharp degree-excess bound

Let

```
R=N_J(w),
R_p={i in R:S_i={p}},
R_q={i in R:S_i={q}},
R_pq={i in R:S_i={p,q}}.
```

Put `x_y=d_G(y)-(k-1)=k-d_H(y)`. The singleton-exchange counts satisfy

```
|R_p| <= k-3-x_q,
|R_q| <= k-3-x_p,
|R_pq| >= |R|-2k+6+x_p+x_q.                              (2)
```

Indeed, each `i in R_p` contributes at least one distinct neighbour of `q`
inside the disjoint pair `M_i`, while `q` already has the three neighbours
`v,w,p`. Thus `d_H(q)>=3+|R_p|`; substitute `d_H(q)=k-x_q`.
The second inequality is symmetric, and the third follows by subtracting
the first two bounds from `|R|`.

For a full center star, `|R|=k-2`, (2) becomes

```
|R_pq| >= x_p+x_q-(k-4).
```

This bound is sharp under the local hypotheses: the separation family at
height 2841 has `x_p=x_q=k-3`, a full `(k-2)`-star, and every availability
set equals `{p,q}`.

At `k=29`, every singleton availability is therefore exactly a six-vertex
endpoint exchange, and a same-singleton two-edge Hall obstruction produces
two distinct shortest endpoint factors. This is genuine cross-deletion
information, but it does not by itself make their corresponding branch
paths internally disjoint.

## 5. Scope and next obstruction

The overlay theorem replaces arbitrary endpoint factors by one exceptional
unicyclic exchange component plus alternating cycles. The six-vertex theorem
identifies the shortest possible exceptional component exactly. It does not
control longer exceptional components and does not exclude a center with
three or more incident availability sets.

Thus no order-58 row is eliminated. The next bounded question is whether two
same-singleton six-vertex exchanges, or one longer unicyclic exchange, force
an alternative internally disjoint routing. Failure would require a model
that is fully vertex-critical at both special endpoints, unlike the height-
2841 separation family.

## Trust boundary and literature

All claims above are elementary finite clique-partition, incidence-graph,
degree-counting, and Kempe-path arguments. No enumeration, solver, floating
point, crossing table, or topology classification is used.

The only external input is the existence of the large-class deletion covers,
from M. Stehlik, *Critical graphs with connected complements*, J. Combin.
Theory Ser. B 89 (2003), 189--194,
DOI `10.1016/S0095-8956(03)00069-8`. The block-restriction argument is
reproved here; it is the elementary closed-cover minimality principle also
used in Stehlik's proof.
