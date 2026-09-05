# Two-leaf Hall obstructions force a third-pair escape

This note sharpens the two-slot Hall obstruction in the corrected order-`2k`
conformal-diamond setup.  When the representative graph has exactly a
two-leaf star and both leaves compete for the same singleton slot, failure of
the standard subdivision routing forces an induced alternating rectangle in
the complement.  Vertex-criticality then forces every factor at the
unavailable endpoint to leave those two color pairs and involve a third pair.

The theorem is uniform in `k`.  It is a structural weakening of the desired
cross-diamond capacity statement; it does not eliminate an order-58 row.

## 1. Setup

Let `G` be a `k`-vertex-critical graph on `2k` vertices, let
`H=bar(G)` be connected, and let `d_G(v)=k-1`.  Use the corrected
Stehlik-coloring labels

```
B=N_G(v)={w,b_2,...,b_{k-1}},
A=N_H(v)={p,q,a_2,...,a_{k-1}},
C_0={w,p,q},             C_l={b_l,a_l} (2<=l<=k-1).
```

Thus

```
P_v={{v},{w,p,q}} union {M_l={a_l,b_l}:2<=l<=k-1}
```

is a minimum `k`-clique partition of `H`.  Put `J=H[B]`.  For every
`w b_l in E(H)`, the nonempty availability set is

```
S_l={s in {p,q}: w-a_l-s-b_l is a G-path}.
```

The height-2805 routing uses the branch set `{v} union B`.  It uses a direct
edge for an adjacent branch pair, the forced path
`b_r-a_s-a_r-b_s` for an edge `b_r b_s` of `J` not incident with `w`,
and an available path through `p` or `q` for an edge `w b_l` of `J`.

## 2. Alternating-rectangle and escape theorem

### Theorem

Assume that `G` contains no subdivision `TK_k`, that

```
d_J(b_l)<=1 for every l>=2,
N_J(w)={b_i,b_j},
S_i=S_j={p}
```

for distinct `i,j`.  Then all of the following hold.

1. The four pair vertices induce exactly an alternating rectangle in `H`:

   ```
   H[M_i union M_j]=K_{2,2}
   ```

   with bipartition `{a_i,a_j}` and `{b_i,b_j}`.  Equivalently, all four
   `a`--`b` edges are in `H`, while `a_i a_j` and `b_i b_j` are in `G`.

2. Put `Q_l=N_H(q) intersect M_l`.  Both `Q_i,Q_j` are nonempty, and either

   ```
   |Q_i|+|Q_j|>=3,
   ```

   or the two singleton blockers have the same orientation:

   ```
   Q_i={a_i}, Q_j={a_j};
   ```

   or

   ```
   Q_i={b_i}, Q_j={b_j}.
   ```

3. Let

   ```
   P_q={{q},T_q} union N_q
   ```

   be any endpoint clique partition supplied by criticality and Stehlik,
   where `T_q` is a triangle and `N_q` consists of `k-2` pairs.  In the
   block-incidence overlay `Gamma(P_v,P_q)`, the exceptional component has
   at least four blocks on each side and contains some base pair `M_l` with
   `l` outside `{i,j}`.

In particular, the endpoint factor at the unavailable slot cannot repair the
two-leaf obstruction inside the diamond and its two obstructing pairs: it
must escape through at least one third pair.  For `k=4`, no such two-leaf
obstruction can occur.

### Proof of the forced cross edges

Because `p` belongs to both availability sets, all of

```
w a_i, p a_i, p b_i, w a_j, p a_j, p b_j
```

are edges of `G`.  Suppose first that `a_i b_j` is also an edge of `G`.
Route the two missing center--leaf branch pairs by

```
w-a_i-b_j,             w-a_j-p-b_i.
```

Their internal vertices are disjoint.  Since `d_J(b_i),d_J(b_j)<=1` and
both leaves are already adjacent to `w` in `J`, neither `a_i` nor `a_j` is
used by any of the forced paths for other edges of `J`.  Together with the
standard height-2805 paths, the two displayed paths therefore give a
`TK_k`, a contradiction.  Hence `a_i b_j` lies in `H`.  Interchanging
`i,j` gives `a_j b_i in E(H)`.

The base matching already supplies `a_i b_i,a_j b_j in E(H)`.  Moreover,
`b_i b_j` is not in `H`, because each of `b_i,b_j` already has its unique
allowed `J`-neighbor `w`.

It remains to exclude `a_i a_j in E(H)`.  If that edge existed, then the
following would be a clique partition of `H` into only `k-1` blocks:

```
{v,p,q}, {a_i,a_j,b_i}, {w,b_j}, M_l (l notin {i,j}).
```

Indeed, the two displayed triples and the displayed pair are cliques of
`H`, and the remaining `M_l` are the base matching edges.  This contradicts
`chi(G)=k`.  Therefore `a_i a_j` lies in `G`, proving the induced-rectangle
claim.

### Proof of blocker coherence

Since `q` is absent from each availability set, it has an `H`-neighbor in
each of `M_i,M_j`; hence `Q_i,Q_j` are nonempty.  A second pair of disjoint
center paths would also exist if either

```
q a_i, q b_j in E(G),  or  q a_j, q b_i in E(G).
```

For example, in the first case use

```
w-a_i-q-b_j,           w-a_j-p-b_i.
```

The same noninterference argument completes the standard routing to a
`TK_k`.  Thus neither crossed pair of `q`-edges can occur.

If `q` has only two `H`-neighbors in `M_i union M_j`, it has exactly one in
each pair.  Opposite orientations would be one of the two forbidden crossed
`G`-edge patterns above.  The two blockers must therefore both be `a`-type
or both be `b`-type.  With three or four `H`-neighbors the first alternative
of conclusion 2 holds.

### Proof of third-pair escape

Recall the endpoint-overlay theorem: the exceptional component of
`Gamma(P_v,P_q)` contains the singleton and triangle blocks of both
partitions, has equally many blocks on its two sides, and is unicyclic.  Its
base side therefore consists of `{v}`, `{w,p,q}`, and some collection of
the pairs `M_l`.

The component cannot contain only one base pair.  Such a three-block-per-side
component partitions `{v,w,p,a_l,b_l}` into an endpoint triangle and pair
after the singleton `q` is removed.  In any such partition, `v` either lies
in the triangle `{v,p,a_l}` or is paired with `p` or `a_l`; checking the
remaining block in all three cases forces `w b_l in E(H)`.  Kempe
connectivity then forces `w a_l in E(G)`, excluding the case in which `v`
is paired with `p`.  The other two patterns put an `H`-neighbor of `p` in
`M_l`, so `p` is unavailable.  Nonemptiness of `S_l` gives `S_l={q}`.
Since the only neighbors of `w` in `J` are `b_i,b_j`, this forces `l` to be
`i` or `j`, contradicting `S_i=S_j={p}`.

Suppose next that every base pair in the exceptional component belongs to
`{M_i,M_j}`.  At least two are needed, so the component must use both.  Its
label set would then be

```
X={v,w,p,q,a_i,b_i,a_j,b_j}.
```

But `H[X-{q}]` is triangle-free.  The induced rectangle handles the four
pair vertices.  Inside the remaining seven vertices, `p` is adjacent in
`H` only to `v,w`; `v` is adjacent only to `p,a_i,a_j`; and `w` is adjacent
only to `p,b_i,b_j`.  The possible neighbor pairs in each of these three
sets are nonadjacent in `H`, so none lies in a triangle.

The endpoint triangle `T_q` belongs to the exceptional component and avoids
the singleton vertex `q`.  It would therefore be a triangle of
`H[X-{q}]`, a contradiction.  Thus the exceptional component uses at least
two base pairs and at least one lies outside `{M_i,M_j}`.  It has at least
four blocks per side.  When `k=4` there is no third pair, so the assumed
configuration is impossible.

## 3. Order-58 meaning and remaining obstruction

For `k=29`, conclusion 3 turns the smallest unresolved two-slot Hall failure
into a genuinely nonlocal factor exchange: every coloring after deleting the
unavailable endpoint must involve at least a third one of the 27 pair
classes.  Thus the height-2861 endpoint-factor existence theorem now has an
explicit cross-boundary consequence.

No row `(58,838..840)` is eliminated.  The other height-2805 obstructions --
a leaf of `J`-degree at least two or a center of degree at least three --
remain untouched.  Even in the two-leaf case, a two-pair or longer
exceptional component involving a third pair need not yet yield internally
disjoint branch paths.  The next exact input would have to turn that first
escaping block into a rerouting path, or construct a fully endpoint-critical
model in which every escape is trapped.

## 4. Trust boundary and literature

All new claims are elementary finite graph arguments: explicit path
replacement, clique-partition contradiction, a four-vertex incidence
classification, and the previously proved block-overlay invariant.  No
enumeration, solver, floating point, crossing table, or topology
classification is used.

The external input is M. Stehlik, *Critical graphs with connected
complements*, J. Combin. Theory Ser. B 89 (2003), 189--194,
DOI `10.1016/S0095-8956(03)00069-8`, which supplies the endpoint deletion
partitions.  Targeted searches of the primary critical-graph, coloring, and
immersion literature found no statement of this exact two-leaf alternating
rectangle or third-pair escape.  This is a scoped literature check, not a
priority claim.
