# Local extremal-deletion cuts for exact R(5,5) search

## Structural lemma

Color every edge of a complete graph red or blue and assume there is no
monochromatic `K5`.  Fix a vertex `u` and a color `c`.  Let

```text
H = G_c[N_c(u)],   d=|V(H)|,   t=e_c(H).
```

The graph `H`, with color `c` regarded as its edge color, is a `(4,5;d)`
Ramsey graph: a `c`-colored `K4` extends through `u`, while an opposite-color
`K5` is already forbidden.  Write

```text
U(q) = max{e(F): F is a (4,5;q) Ramsey graph}.
```

For every set `S` of `k` vertices in `H`, deleting `S` gives the exact cut

```text
e_c(S) + e_c(S,V(H)-S) >= t-U(d-k).                 (1)
```

Indeed, the left side is exactly `t-e_c(H-S)`, and `H-S` remains a
`(4,5;d-k)` graph.  Equivalently, with

```text
q_c(u,v)=|N_c(u) intersect N_c(v)|,
```

equation (1) is

```text
sum_(v in S) q_c(u,v) - e_c(S) >= t-U(d-k).         (2)
```

This is an arity-independent hereditary cut family.  If the local deficiency
is `delta=U(d)-t`, its right side is

```text
U(d)-U(d-k)-delta.                                  (3)
```

The first two levels have especially direct search interpretations:

```text
q_c(u,v) >= U(d)-U(d-1)-delta,

q_c(u,v)+q_c(u,w)-1[vw has color c]
  >= U(d)-U(d-2)-delta.
```

These are necessary conditions for every color, root, and selected same-color
neighbor set.  They are redundant consequences of full Ramsey feasibility,
as valid search cuts should be; they are not assumptions about a particular
profile or catalog graph.

## Exact-deficiency-seven table

Using the independently reviewed local extrema

```text
U(18..24)=85,92,100,107,114,122,132,
```

the positive known-range instances of (3) are:

| `d` | `k` | `d-k` | minimum incident `c`-edges |
|---:|---:|---:|---:|
| 20 | 1 | 19 | 1 |
| 20 | 2 | 18 | 8 |
| 21 | 2 | 19 | 8 |
| 21 | 3 | 18 | 15 |
| 22 | 2 | 20 | 7 |
| 22 | 3 | 19 | 15 |
| 22 | 4 | 18 | 22 |
| 23 | 1 | 22 | 1 |
| 23 | 2 | 21 | 8 |
| 23 | 3 | 20 | 15 |
| 23 | 4 | 19 | 23 |
| 23 | 5 | 18 | 30 |
| 24 | 1 | 23 | 3 |
| 24 | 2 | 22 | 11 |
| 24 | 3 | 21 | 18 |
| 24 | 4 | 20 | 25 |
| 24 | 5 | 19 | 33 |
| 24 | 6 | 18 | 40 |

For example, at an exact degree-21 local side, any two selected neighbors
must together meet at least eight local same-color edges, and any three must
meet at least fifteen.  Five explicit simple graphs in the verifier meet the
scalar cap `t=U(d)-7` but violate one of these cuts.  Thus the family is
strictly stronger than retaining the scalar local-edge total alone.

## Guarded OPB rows for the complete M=214 search

The height-2505 normalized M=214 formulation has red-edge bits `x_uv`, red
triangle bits `z_uab`, and exact red local totals

```text
T_u=93 for u=0,...,12,    T_u=100 for u=13,...,42.
```

For every fixed potential removed set `S` of size `k`, the guarded form of
(1) is the pseudo-Boolean row

```text
sum_(a<b, {a,b} intersects S) z_uab
  - T_u sum_(s in S) x_us
  >= T_u-U(d_u-k)-T_u*k.                             (4)
```

If every `x_us=1`, the triangle sum is precisely the number of local red
edges incident with `S`, so (4) is (1).  If at least one guard is zero, all
triangles using that missing root edge are zero and the exact equality
`sum z_uab=T_u` makes (4) automatic.  Thus (4) can be inserted without a new
variable or a new trust assumption.

To control formula growth, the public emitter stops at `k=2`.  It produces
37,569 rows: 546 degree-20 singleton cuts, 11,193 degree-20 pair cuts, and
25,830 degree-21 pair cuts.  The 29,045,208-byte generated stream is not
committed.  Its SHA-256 is

```text
724ea8d7788010b31617523b7d04b293b668445ca98b89463307b8403353036c.
```

The stream uses exactly the height-2505 variable numbering.  It is a row
fragment, not a standalone OPB: an integrator must place the rows into the
canonical formula and increase its constraint header from 1,974,731 to
2,012,300.  The `k=3` degree-21 tier is mathematically valid but intentionally
not emitted; it would add 344,400 rows and should instead be separated lazily
or enabled only after measured benefit.

## Exact verification

With CPython 3.11 or newer and no third-party dependency:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify_deletion_cuts.py | cmp - EXPECTED_VERIFY_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_deletion_cuts.py | cmp - EXPECTED_VERIFY_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 generate_m214_opb_cuts.py \
  --output /tmp/r55_m214_local_deletion_cuts.opb | cmp - EXPECTED_GENERATOR_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 audit_m214_opb_cuts.py \
  /tmp/r55_m214_local_deletion_cuts.opb | cmp - EXPECTED_AUDIT_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O audit_m214_opb_cuts.py \
  /tmp/r55_m214_local_deletion_cuts.opb | cmp - EXPECTED_AUDIT_OUTPUT.txt
shasum -a 256 /tmp/r55_m214_local_deletion_cuts.opb
shasum -a 256 -c SHA256SUMS
```

The theorem audit checks the edge-partition identity on all 33,868 labeled
graphs through order six and all 2,131,019 graph/subset pairs.  The independent
stream auditor checks all 37,569 guarded rows and 3,095,841 coefficients.

For an honest boundary test, `HEIGHT2731_SURVIVOR.json` is the immutable
height-2731 input with its original SHA-256.  It satisfies all 247,094
positive known-range cuts instantiated on its red and blue local graphs;
the minimum slack is zero.  Among the 54 root-color sides already satisfying
the scalar deficiency-seven caps, all 197,142 cuts pass with minimum slack
four.  Therefore this cut family is transferable search infrastructure but
does not exclude that survivor, repair its 32 central hard-cap failures, or
turn it into a Ramsey graph.

## Literature and trust boundary

Angeltveit--McKay's exact `R(5,5)<=46` proof combines linear programming and
large independently implemented case checks:
https://arxiv.org/abs/2409.15709.  Their earlier paper completed the extremal
`R(4,5)` catalog: https://arxiv.org/abs/1703.08768.  McKay's primary data page
publishes the complete order-24 catalog and extreme-edge files for smaller
orders: https://users.cecs.anu.edu.au/~bdm/data/ramsey.html.

No historical novelty is claimed for the elementary deletion principle.
Graph searches through indexed height 2746 found the local-extremal values,
the degree-neighborhood identity, and a different mixed-root deletion bound,
but no contribution expressing this all-subset local-profile family or its
guarded height-2505 OPB rows.

The universal proof is the two-line hereditary argument above.  The audited
values `U(18..24)` retain the historical catalog-completeness trust boundary.
The source checker trusts CPython integer/Boolean semantics, SHA-256, and
ordinary hardware.  The generated row stream is independently parsed but is
not itself an UNSAT certificate, a solver result, a graph construction, a
whole-profile exclusion, or a new Ramsey-number bound.
