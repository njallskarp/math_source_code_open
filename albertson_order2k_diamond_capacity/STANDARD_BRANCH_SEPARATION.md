# Four-block escape forces an external matching edge, but not the canonical routing

This note gives the bounded structural answer suggested by the minimal escape
countermodel.  First, a four-by-four endpoint component that avoids both
Hall-obstructing pairs must use an **isolated outside edge** of the
representative graph.  Second, even this forced edge, full vertex-criticality,
and three degree-`k-1` vertices do not make the canonical height-2805 branch
set routable: a uniform family separates that conclusion for every `k>=6`.

The family contains an explicit `TK_k` on a shifted branch set.  It therefore
does not contradict the no-`TK_k` hypothesis at height 2891 or Albertson's
conjecture.  At `k=29` it is also far outside the surviving edge rows.  Its
role is to prove that the next order-58 argument must use either branch-set
mobility or the frontier's small degree excess; another theorem about the
canonical branch set alone cannot close the lane.

## 1. A four-block escape forces an outside edge of `J`

Use the setup and hypotheses of the height-2891 two-leaf theorem.  Thus

```text
B={w,b_2,...,b_{k-1}},
P_v={v}/{w,p,q}/{a_2,b_2}/.../{a_{k-1},b_{k-1}},
N_J(w)={b_i,b_j}, S_i=S_j={p},
d_J(b_l)<=1 for every l>=2,
```

where `J=H[B]` and `H=bar(G)`.  Suppose a `q`-singleton endpoint factor has
a four-block-per-side exceptional overlay component and that this component
avoids `M_i={a_i,b_i}` and `M_j={a_j,b_j}`.

### Theorem 1 (external-edge footprint)

There are distinct `r,s` outside `{i,j}` such that the base side of the
exceptional component is

```text
{v}, {w,p,q}, M_r, M_s,
```

and

```text
b_r b_s in E(H).
```

Consequently `b_r b_s` is an isolated edge of `J`: neither endpoint has any
other `J`-neighbour.

### Proof

The exceptional component contains the base singleton and triangle.  Four
base blocks therefore leave exactly two base pair blocks, and avoidance of
`M_i,M_j` names them `M_r,M_s`.

After removing the right singleton `{q}`, the endpoint factor partitions the
seven vertices

```text
{v,w,p,a_r,b_r,a_s,b_s}
```

into one `H`-triangle and two `H`-pairs.  The four vertices

```text
v,w,b_r,b_s
```

must occupy these three non-singleton blocks.  Now `vw,vb_r,vb_s` are edges
of `G` by the base factor, and `wb_r,wb_s` are edges of `G` because the only
neighbours of `w` in `J` are `b_i,b_j`.  Hence no two of these four vertices
can share an endpoint block, except possibly `b_r,b_s`.  Pigeonhole forces
`b_r,b_s` into the same block, proving `b_r b_s in E(H)`.  The degree-one
hypothesis on pair representatives makes this edge isolated in `J`.

Up to interchanging `r,s`, the three non-singleton endpoint blocks have one
of the following five footprints (slashes separate blocks):

```text
{b_r,b_s}     / {w,a_r,a_s} / {v,p};
{b_r,b_s}     / {v,p,a_r}   / {w,a_s};
{b_r,b_s}     / {w,p,a_r}   / {v,a_s};
{a_r,b_r,b_s} / {w,a_s}     / {v,p};
{p,b_r,b_s}   / {v,a_r}     / {w,a_s}.
```

This list follows by considering whether the common block of `b_r,b_s` is a
pair or the triangle.  If it is a pair, the remaining triangle and pair
partition `{v,w,p,a_r,a_s}`; the incompatibility `vw in E(G)` and overlay
connectivity leave the first three displayed types.  If it is the triangle,
its third member cannot be `v` or `w`.  A third member `a_r` (or `a_s`)
forces the fourth type, while third member `p` gives the fifth type, up to
interchanging `r,s`.  It is a structural classification of the component,
not a parameter enumeration.

The rest of `J-{w,b_i,b_j}` is a matching.  Since it has `k-4` vertices, it
also leaves an isolated representative whenever `k` is odd.  If `b_t` is
such an isolated representative, its auxiliary `a_t` is unused by every
standard path for the other edges of `J`.  Therefore the no-`TK_k` hypothesis
implies the useful blocker dichotomy

```text
w a_t in E(H),
or both a_t b_i and a_t b_j belong to E(H).                 (1)
```

Indeed, if `w a_t` and `a_t b_i` were both `G`-edges, use
`w-a_t-b_i` for one center demand and `w-a_j-p-b_j` for the other; all
remaining standard paths are internally disjoint.  The argument with `i,j`
interchanged is identical.  Summing (1) over the isolated indices `I_0`
gives the exact incidence inequality

```text
|I_0| <= e_H(w,{a_t:t in I_0})
       + (e_H(b_i,{a_t:t in I_0})+e_H(b_j,{a_t:t in I_0}))/2.       (2)
```

For `k=29`, `|I_0|=25-2 mu`, where `mu` is the size of the matching on the
25 representatives outside `{b_i,b_j}`.  The four-block escape proves
`mu>=1`.  Inequality (2) is uniform, but by itself it does not contradict
the order-58 degree bounds.

## 2. A uniform critical separation family

### Theorem 2 (canonical-route separation)

For every `k>=6` there is a graph `G_k` on `2k` vertices, with connected
complement `H_k`, such that:

1. `G_k` is `k`-vertex-critical;
2. `v,w,q` all have degree `k-1` in `G_k` (and for `k>=7` these are exactly
   the degree-`k-1` vertices);
3. at `v`, the representative graph is exactly
   `J=K_{1,2} disjoint_union K_2` plus isolated vertices, with
   `S_2=S_3={p}`;
4. the displayed `q`-endpoint factor has a four-by-four exceptional component
   avoiding `M_2,M_3`;
5. no subdivision of `K_k` with the canonical branch set `{v} union B`
   exists; but
6. `G_k` contains a displayed `TK_k` on a shifted branch set.

### Construction

Let

```text
V(H_k)={v,w,p,q} union {a_l,b_l:2<=l<=k-1}.
```

The edges of `H_k` are precisely:

```text
diamond: vp,vq,pq,wp,wq;

base factor: v a_l, a_l b_l                    (2<=l<=k-1);

target rectangle/blockers:
  w b_2,w b_3,a_2 b_3,a_3 b_2,q a_2,q a_3;

four-block escape:
  p a_4,w a_5,b_4 b_5;

canonical-route blockers:
  a_2 a_4,a_3 a_4,w a_4,q b_4;

tail blockers for every 6<=l<=k-1:
  q b_l,w a_l,a_2 a_l,a_3 a_l,b_4 a_l.
```

There are no other complement edges, and `G_k=bar(H_k)`.

The base and endpoint factors are

```text
P_v={v}/{w,p,q}/{a_2,b_2}/{a_3,b_3}/{a_4,b_4}/{a_5,b_5}
    / {a_l,b_l} (6<=l<=k-1),

P_q={q}/{v,p,a_4}/{w,a_5}/{a_2,b_2}/{a_3,b_3}/{b_4,b_5}
    / {a_l,b_l} (6<=l<=k-1).
```

Thus their exceptional component is the same four-by-four component on
`{v,w,p,q,a_4,b_4,a_5,b_5}` for every `k`; all tail pairs are unchanged
two-edge components.

## 3. Proof that `G_k` is vertex-critical

The complement has

```text
e(H_k)=7k-16,
```

is connected, and has no clique of order four.  Its triangles are exactly

```text
{v,p,q}, {v,p,a_4}, {v,q,a_2}, {v,q,a_3},
{v,a_2,a_4}, {v,a_3,a_4},
{v,a_2,a_l}, {v,a_3,a_l}                       (6<=l<=k-1),
{w,p,q}, {w,p,a_4}.
```

All but the last two contain `v`, while the last two meet in `{w,p}`.  Hence
at most two triangles can be pairwise disjoint.

Any partition with fewer than `k-1` blocks can be refined by splitting blocks,
so suppose `H_k` had a partition into exactly `k-1` cliques.  With no `K_4`, let `t`
and `s` be the numbers of triangle and singleton blocks.  Comparing its
`2k` vertices with two vertices per block gives `t-s=2`.  Triangle packing
number at most two then forces `t=2,s=0`; deleting the two triangles must
leave a perfect matching.

This never happens.  Every disjoint triangle pair contains one of
`U_0={w,p,q}`, `U_1={w,p,a_4}` and one triangle through `v`.  The complete
list of residual obstructions is:

| non-`v` triangle | disjoint `v`-triangle | residual obstruction |
|---|---|---|
| `U_0` | `{v,a_2,a_4}` | `b_2,b_3` have sole neighbour `a_3` |
| `U_0` | `{v,a_3,a_4}` | `b_2,b_3` have sole neighbour `a_2` |
| `U_0` | `{v,a_2,a_l}` or `{v,a_3,a_l}` | `b_l` is isolated |
| `U_1` | `{v,q,a_2}` | `b_2,b_3` have sole neighbour `a_3` |
| `U_1` | `{v,q,a_3}` | `b_2,b_3` have sole neighbour `a_2` |
| `U_1` | `{v,a_2,a_l}` | `b_2,b_3` have sole neighbour `a_3` |
| `U_1` | `{v,a_3,a_l}` | `b_2,b_3` have sole neighbour `a_2` |

Here `6<=l<=k-1`.  Each row precludes a perfect matching.  The displayed
base factor consequently proves `theta(H_k)=k`.

For completeness, put `H_* = H_6`.  The following are five-clique covers of
all its vertex deletions:

| deleted | cover of `H_*-x` |
|---|---|
| `v` | `wpq / a2b2 / a3b3 / a4b4 / a5b5` |
| `w` | `vpq / a2b2 / a3b3 / a4b4 / a5b5` |
| `p` | `vqa2 / wb2 / a3b3 / a4b4 / a5b5` |
| `q` | `vpa4 / wa5 / a2b2 / a3b3 / b4b5` |
| `a2` | `vpq / wb2 / a3b3 / a4b4 / a5b5` |
| `b2` | `va2 / wpq / a3b3 / a4b4 / a5b5` |
| `a3` | `vpq / wb2 / a2b3 / a4b4 / a5b5` |
| `b3` | `va2 / wpq / b2a3 / a4b4 / a5b5` |
| `a4` | `va5 / wpq / a2b2 / a3b3 / b4b5` |
| `b4` | `va4 / wpq / a2b2 / a3b3 / a5b5` |
| `a5` | `va4 / wpq / a2b2 / a3b3 / b4b5` |
| `b5` | `va5 / wpq / a2b2 / a3b3 / a4b4` |

For a deleted core vertex, append every tail pair `{a_l,b_l}`.  If `a_l`
is deleted, use the five-block cover of `H_*-q`, add `{q,b_l}`, and append
all other tail pairs.  If `b_l` is deleted, use the cover of `H_*-v`, add
`{v,a_l}`, and append the other tail pairs.  These are `(k-1)`-clique covers
of every deletion.  Since deleting one vertex lowers clique-cover number by
at most one, every displayed upper bound is exact.  Hence `G_k` is
`k`-vertex-critical.

Finally `d_{H_k}(v)=d_{H_k}(w)=d_{H_k}(q)=k`.  All other complement degrees
are at most `k-1` when `k>=7`, proving the degree assertion.

## 4. Why the canonical branch set cannot work

At `v`, put

```text
B={w,b_2,...,b_{k-1}}, A={p,q,a_2,...,a_{k-1}}.
```

The only edges of `J=H_k[B]` are

```text
w b_2, w b_3, b_4 b_5.
```

All other branch pairs are direct `G_k`-edges.  Any canonical subdivision
would therefore need internally disjoint paths for those three pairs using
internal vertices in `A`.

But the only `G_k`-neighbours of `w` in `A` are `a_2,a_3`.  The two center
paths must start with these two distinct vertices.  Neither can finish at
`b_2` or `b_3` immediately, and after excluding the other occupied start,
the only possible next internal vertices are `p,a_5`.  Consequently the two
center paths consume both `p` and `a_5`.

After deleting those four occupied internal vertices
`a_2,a_3,p,a_5`, vertex `b_4` has no `G_k`-neighbour among the remaining
internal vertices: its complement neighbours there are `q,a_4` and every
tail `a_l`.  Since `b_4b_5` is also a complement edge, the third path cannot
start.  No `TK_k` on the canonical branch set exists.

## 5. The shifted subdivision

The obstruction is branch-set-specific, not global.  Use

```text
K={v,p,a_2,b_2,b_4,b_5} union {b_l:6<=l<=k-1}
```

as the `k` branch vertices.  All branch pairs are `G_k`-edges except

```text
vp, v a_2, a_2 b_2, b_4 b_5.
```

Route these by

```text
v-b_3-p,
v-w-a_2,
a_2-a_5-b_2,
b_4-a_3-b_5.
```

The four interiors are mutually disjoint and avoid `K`, so these paths and
the direct branch edges form a `TK_k`.

## 6. Exact order-58 scope

At `k=29`, the family has

```text
e(H_29)=187, e(G_29)=binom(58,2)-187=1466.
```

The surviving frontier rows have only 838--840 edges in `G`.  Equivalently,
their total degree excess over 28 is 52--56, whereas this family has excess
1308.  Thus the family does not approach, model, or eliminate a frontier
row.  It proves instead that the frontier density is a necessary hypothesis
for any theorem meant to force routing after the four-block escape.

The next justified input is a degree-excess-sensitive branch-shift or linkage
inequality.  Generic criticality, three low vertices, endpoint-factor
minimality, and the canonical branch set are now exhausted as standalone
mechanisms.  Scalar recurrence and profile enumeration remain frozen.

## Reproduction and trust boundary

Run the exact standard-library checker:

```sh
cd albertson_order2k_diamond_capacity
python3 verify_standard_branch_separation.py
```

Expected output:

```text
k=6 n=12 eH=26 eG=40 canonical=no shifted_TK=yes theta_check=exact-dp
k=7 n=14 eH=33 eG=58 canonical=no shifted_TK=yes theta_check=exact-dp
k=8 n=16 eH=40 eG=80 canonical=no shifted_TK=yes theta_check=exact-dp
k=29 n=58 eH=187 eG=1466 canonical=no shifted_TK=yes theta_check=structural-certificate
certificate_sha256=e7548003a56943dfee2cc9c5ec6ceb4dd595ae8ca58022fc40b263d4b33998bd
```

It checks the defining edge formulas and proof certificates at
`k=6,7,8,29`; it additionally recomputes all clique-cover numbers for the
small cases `k=6,7,8`.  No floating point, random sampling, solver, or
external data is used.  The universal proof is the argument above; the
finite checker validates its formulas and boundary cases rather than
replacing the induction.

## Primary-source scope

The only external theorem used to interpret the endpoint factors in the
Albertson program remains Matej Stehlik,
[*Critical Graphs with Connected Complements*](https://doi.org/10.1016/S0095-8956(03)00069-8),
JCTB 89 (2003), 189--194.  The construction and criticality proof
are self-contained.  Targeted searches also checked the general clique-
subdivision literature, including
[Fox--Lee--Sudakov (2011)](https://arxiv.org/abs/1107.1920), but found no
prescribed-branch result or this exact critical separation family.  This is
a scoped novelty check, not a priority claim.
