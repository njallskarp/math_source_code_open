# A deficiency-six `d=22` anchor survives every one-anchor constraint

## Exact limitation result

There is a red/blue coloring `X` of `K_43` with a vertex `u` such that:

1. every red and blue degree is in `18..24`;
2. `d_R(u)=22`, and the red graph on `A=N_R(u)` is a `(4,5;22)` graph
   with 108 edges, hence deficiency `114-108=6` from the exact extremum;
3. the blue graph on `B=N_B(u)` is a `(4,5;20)` graph with 100 edges;
4. no monochromatic `K_5` contains `u`;
5. the 18 vertices of red `A`-degree 10 induce 73 red edges.  For every
   such edge `vw`, the red triangle `uvw` has triple common-neighborhood
   size `k` at most four; the distribution is `k=2:4, k=3:34, k=4:35`.

The coloring is **not** an `R(5,5;43)` graph: it has 206 red and 1,536 blue
five-cliques, all avoiding `u`.  It is an exact feasibility witness for the
whole relaxation that enforces the degree box, both exact induced color
neighborhoods of one anchor, and every consequence of excluding a
monochromatic five-clique through that anchor.  Consequently, even coupling
all high-codegree partners inside the anchor cannot exclude the `d=22`,
deficiency-six branch.  Any successful next constraint must couple the anchor
to a forbidden five-clique avoiding it (for example by reanchoring a partner
and constraining its full outside neighborhood).

## Construction

Number the vertices as

```text
u=0,  A={1,...,22},  B={23,...,42}.
```

`ANCHOR_DATA.json` stores two graph6 records.  On `A`, start with the listed
114-edge extremal `(4,5;22)` graph and delete the six listed edges, producing
the 108-edge red graph `H`.  On `B`, the stored 100-edge `(4,5;20)` graph `J`
is the **blue** graph.  Join `u` red to `A` and blue to `B`.  Finally, color
the cross edge `A_i B_j` red precisely when

```text
(j-i) mod 20 in {0,1,...,9}.
```

The red degree sequence is

```text
19^7, 20^10, 21^25, 22,
```

and the blue sequence is its complement

```text
20, 21^25, 22^10, 23^7.
```

No red five-clique through `u` exists because `H` has no red `K_4`; no blue
five-clique through `u` exists because `J` has no blue `K_4`.

## Joint-partner identity

The deficiency argument forces at least five partners of red `A`-degree at
least 10.  Since `H` has independence number below five, two are adjacent;
write them `v,w`.  Put

```text
a = |N_R(u) intersect N_R(v)|,
b = |N_R(u) intersect N_R(w)|,
p = d_R(v),  r = d_R(w),
q = |N_R(v) intersect N_R(w)|,
k = |N_R(u) intersect N_R(v) intersect N_R(w)|.
```

In a hypothetical `R(5,5;43)` graph, the triple common neighborhood is red
independent (otherwise it completes `uvw` to a red `K_5`) and has size at
most four (otherwise it is a blue `K_5`).  On the 40 vertices other than
`u,v,w`, the eight red-adjacency signatures to `(u,v,w)` therefore have exact
sizes, in binary order `111,110,101,011,100,010,001,000`,

```text
k,
a-1-k,
b-1-k,
q-1-k,
22-a-b+k,
p-a-q+k,
r-b-q+k,
43-22-p-r+a+b+q-k.
```

`verify.py` checks this identity entry by entry for all 73 eligible triangles,
not just in aggregate.  Thus the witness closes the proposed joint-partner
step as an insufficiency result rather than extending a finite census.

## Reproduction

With CPython 3.11 or newer:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_verify.py | cmp - EXPECTED_TEST_OUTPUT.txt
python3 -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 independent_networkx_check.py \
  | cmp - EXPECTED_NETWORKX_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

## Trust boundary

The main checker uses exact CPython integers, an explicit graph6 decoder, and
exhaustive subset tests.  The NetworkX 3.6 checker independently decodes the
records and uses its clique implementation for the two local cores; it also
reconstructs the 43-vertex coloring and directly recounts every five-subset.
The compact graph6 inputs ultimately come from Brendan McKay's published
edge-extremal `(4,5)` catalogs; their catalog completeness and the value
`U(22)=114` remain external inputs.  The asserted properties of these two
specific records are checked directly and do not rely on completeness.  The
result makes no claim that the displayed coloring is Ramsey.

## Primary sources

- V. Angeltveit and B. D. McKay, *R(5,5) <= 46*,
  [arXiv:2409.15709v2](https://arxiv.org/abs/2409.15709), for the local-graph
  and gluing framework and the current `(4,5)` census.
- B. D. McKay's
  [Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
  for the edge-extremal `(4,5)` graph6 data.
