# A minimal endpoint escape need not revisit the obstructing pairs

This note tests the smallest case left open by the two-leaf escape theorem.
It gives a completely explicit complement `H` whose graph `G=bar(H)` is
6-vertex-critical and whose endpoint-factor overlay has the minimum four
blocks on each side, yet that exceptional component avoids both pair classes
causing the two-leaf Hall obstruction.

The construction is **not** a counterexample to the two-leaf escape theorem
or to Albertson's conjecture: `G` contains a displayed subdivision `TK_6`.
Its purpose is narrower and structural.  It proves that vertex-criticality,
even together with minimal overlay size, cannot by itself make an escaping
endpoint factor return to either obstructing pair.  Any such conclusion must
use the global exclusion of `TK_k` (or some genuinely equivalent input).

## Proposition

There is a 6-vertex-critical graph `G` on 12 vertices with the following
properties in its connected complement `H`.

1. A degree-five vertex `v` has a factor

   ```text
   {v}, {w,p,q}, {a2,b2}, {a3,b3}, {a4,b4}, {a5,b5}.
   ```

2. In `J=H[N_G(v)]`, the center `w` has the two leaves `b2,b3`, every
   pair representative has degree at most one, and the two availability
   sets are the same singleton:

   ```text
   S2=S3={p}.
   ```

3. The endpoint `q` is unavailable for both leaves.  Nevertheless `H` has
   the factor

   ```text
   {q}, {v,p,a4}, {w,a5}, {a2,b2}, {a3,b3}, {b4,b5},
   ```

   whose exceptional overlay component has exactly four blocks on each
   side and contains neither `{a2,b2}` nor `{a3,b3}`.

Thus the proposed strengthening

> criticality plus a minimum-size endpoint escape forces the escape to meet
> one of the two Hall-obstructing pair classes

is false.

## Construction

Let

```text
V(H)={v,w,p,q,a2,b2,a3,b3,a4,b4,a5,b5}.
```

The 22 edges of `H` are precisely the following, grouped by their role:

```text
diamond:       vp, vq, pq, wp, wq
base factor:   va2, a2b2, va3, a3b3, va4, a4b4, va5, a5b5
rectangle:     wb2, wb3, a2b3, a3b2, qa2, qa3
outside escape: pa4, wa5, b4b5.
```

There are no other edges of `H`; define `G=bar(H)`.

## Proof of criticality

The base factor in the proposition is a six-clique partition of `H`, so
`theta(H)<=6`.  Direct inspection gives exactly five triangles:

```text
{v,p,q}, {v,p,a4}, {v,q,a2}, {v,q,a3}, {w,p,q}.
```

There is no clique of order four, and these five triangles are pairwise
intersecting.  A partition of 12 vertices into five cliques of order at most
three would need two disjoint triangles: with at most one triangle it covers
at most `3+4*2=11` vertices.  Therefore `theta(H)>=6`, and hence
`chi(G)=theta(H)=6`.

For every vertex `x`, the following row is a five-clique partition of `H-x`.

| `x` | clique partition of `H-x` |
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

Since `theta(H)=6`, every `theta(H-x)` is at least five; the table proves it
is exactly five.  Equivalently, `G` is 6-vertex-critical.  Also `H` is
connected.  The vertex `v` has six neighbours in `H`, hence degree five in
`G`, and

```text
N_G(v)={w,b2,b3,b4,b5}.
```

## The obstruction and the escaping factor

On this neighbourhood, the only edges of `H` are

```text
wb2, wb3, b4b5.
```

Thus all pair representatives have degree one in `J`, while `w` has the two
leaves `b2,b3`.  In the notation of the two-slot Hall criterion, the paths

```text
w-a2-p-b2,   w-a3-p-b3
```

are present in `G`, whereas `qa2,qa3` are edges of `H`.  Consequently
`S2=S3={p}` and `q` is unavailable for both leaves.  The rectangle forced by
the two-leaf lemma is visible as the `H`-edges `a2b3,a3b2` together with the
two base-pair edges.

Compare the base factor

```text
L: {v}, {w,p,q}, {a2,b2}, {a3,b3}, {a4,b4}, {a5,b5}
```

with the endpoint factor

```text
R: {q}, {v,p,a4}, {w,a5}, {a2,b2}, {a3,b3}, {b4,b5}.
```

Their intersection overlay has two isolated double-edge components, one for
each unchanged block `{a2,b2}` and `{a3,b3}`.  The remaining component uses
the four left blocks

```text
{v}, {w,p,q}, {a4,b4}, {a5,b5}
```

and the four right blocks

```text
{q}, {v,p,a4}, {w,a5}, {b4,b5}.
```

It is connected, has eight incidence edges, and has degree sequence
`3,3,2,2,2,2,1,1`: a six-cycle with one leaf attached at each of its two
degree-three blocks.  It is therefore a minimum four-by-four exceptional
component, but it avoids both obstructing pair blocks.

## Why this does not evade the global hypothesis

The graph `G` contains a subdivision of `K_6`.  Take branch vertices

```text
{v,w,b2,b3,b4,b5}.
```

All branch pairs are adjacent except `wb2`, `wb3`, and `b4b5`.  Route those
three pairs by

```text
w-a4-b2,
w-a2-a5-b3,
b4-a3-b5.
```

The internal vertex sets `{a4}`, `{a2,a5}`, and `{a3}` are disjoint and do
not meet the branch set.  Hence these paths, together with the remaining
direct branch edges, form a `TK_6`.

This displayed subdivision is the exact reason the example does not
contradict the preceding no-`TK_k` theorem.  It also isolates the next valid
research interface: one must couple all escaping factors to the global
absence of a subdivision, rather than try to force target-pair reuse from
criticality or overlay minimality alone.

## Reproduction and trust boundary

The standard-library checker verifies the graph definition, connectivity,
exact clique-cover numbers, the displayed deletion covers, obstruction data,
overlay decomposition, and subdivision paths:

```sh
cd albertson_order2k_diamond_capacity
python3 verify_minimal_escape_countermodel.py
```

Expected compact output:

```text
vertices=12 edges_H=22 connected_H=yes theta_H=6
deletion_theta=all_5
availability=S2:{p};S3:{p}
overlay_components=2,2,8 exceptional_sides=4x4
TK6_subdivision=valid
certificate_sha256=6854cac9a08ed8cdd824607b83995840801f27edc5c5099f3ede2f2a17804815
```

It uses exhaustive exact integer/set computation on 12 labelled vertices;
there is no floating-point arithmetic or external solver.  The code verifies
the finite construction only.  The structural interpretation and the claim
that this blocks a particular proof interface remain human-audited prose.

## Prior-art scope

The construction was obtained clean-room after consulting Matej Stehlik's
published critical-complement theorem and standard critical-graph/immersion
background.  A bounded primary-source and Discovery Net search found no
statement of this exact minimal endpoint-overlay countermodel.  This is a
scoped novelty check, not an exhaustive priority claim.
