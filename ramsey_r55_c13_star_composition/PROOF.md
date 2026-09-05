# A mixed cube-star cut excludes the published c=13 footprint selection

## Domain and result

Use two red-adjacent anchors `u,v`, common-red core `H=Z/13Z`, and
outside vertices `D0,...,D27`. Core adjacency is

```text
ij is red iff i-j mod 13 belongs to {1,5,8,12}.
```

The outside cells are `A=D0..D6`, `B=D7..D13`, `O=D14..D27`.
Vertices of A are red only to u, vertices of B red only to v, and vertices
of O blue to both. A hexadecimal mask `S_x` records the red neighbors of
Dx in H; bit i refers to the core vertex i. All outside edges are variable.
Core indices and outside indices are different labels.

Fix **only these nine footprints**:

| x | 0 | 7 | 8 | 9 | 10 | 11 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|
| S_x | 1123 | 1439 | 0389 | 0e0e | 0f17 | 1895 | 1fbf | 11a1 | 1b85 |

Theorem. If the 18 colored five-set prohibitions below hold, then the
number `m_B` of red edges within B is at most 12. The other nineteen
footprints, all remaining outside edges, all individual degrees and all
exceptional-set incidences are unrestricted by this implication.

Consequently, in the aggregate family `m_B=61-I_B`, where
`I_B=sum_{x=7}^{13} |S_x|`, the nine fixed footprints imply `I_B>=49`.
The six fixed B footprints have total size 43, so the remaining B footprint
`S_12` must have size at least six. The published height-2943 selection has
`S_12=08e2`, of size five, and `I_B=48, m_B=13`. **No coloring of its 378
outside edges can extend it to a Ramsey(5,5;43) graph.** This excludes all
completions of those rows, not just the author's deterministic edge lift.

The theorem also excludes every relabeling of this fixed partial instance.
It does not exclude a different unpinned c=13 selection, the whole M=214
profile, or any Ramsey-number value. The height-2943 counterexample to the
pairwise-aggregate relaxation remains valid exactly as stated.

## Seventeen pairwise clauses

Write `x_ij` for the red indicator of `Di Dj`.

For each row of the next table, the listed core triple is blue, and both
outside endpoints are blue to all three core vertices. Avoiding a blue K5
on these five vertices forces `x_ij=1`.

| Outside pair | Blue core triple |
|---|---|
| 0,8 | 2,4,6 |
| 0,11 | 3,6,9 |
| 0,14 | 2,4,6 |
| 0,15 | 3,6,10 |
| 8,14 | 1,4,10 |
| 8,15 | 1,4,10 |
| 11,14 | 1,3,10 |
| 11,15 | 1,3,5 |
| 14,15 | 1,3,10 |

Call these nine pairs T. They are exactly all edges of
`Q={D0,D8,D11,D14,D15}` except `p={D8,D11}`.

For every pair in the following table, its endpoints lie in B, and both
are red to both endpoints of the listed red core edge. Together with v
they would form a red K5 if their own pair were red. Thus each of the
eight listed pairs must be blue. Call this pair set F.

| B pair | Red core edge |
|---|---|
| 7,11 | 0,12 |
| 7,13 | 0,5 |
| 8,10 | 0,8 |
| 8,13 | 0,8 |
| 9,10 | 1,2 |
| 9,13 | 1,2 |
| 10,13 | 0,1 |
| 11,13 | 0,12 |

All seventeen clauses have exactly two outside vertices, so they belong
to R1's pairwise interface. None uses `S_12`.

## Translation into R2's three-anchor cube interface

Choose the three *core* anchors `h=1,3,4`, rather than retaining u and v.
For x in Q, the red-incidence coordinate vectors in that order are

```text
D0    D8    D11   D14   D15
100   010   001   000   000.
```

This is precisely the `star_center` orbit from height 2931: a doubled
cube-star center with all three leaves. Each coordinate is mixed, so Q
is not contained in any one of these anchors' six color neighborhoods.
No two signatures are complementary, so each edge of Q is visible in
at least one such neighborhood. This uses no assumption that the new
three anchors form a monochromatic triangle; the cube-interface theorem
does not require one.

The red side of the mixed cut is

```text
x_8,11 + sum_{e in T} x_e <= 9.
```

The nine pairwise clauses force the sum on T to be 9, hence `x_8,11=0`.
This ninth blue pair inside B is disjoint from F. Of B's 21 edges, at
most 12 can therefore be red. This proves the theorem.

## Exact compact certificate

Let `P=choose(B,2) \ (F union {p})`, so `|P|=12`. Add the following
inequalities, each with multiplier one:

```text
x_f <= 0                     for the eight f in F,
-x_t <= -1                   for the nine t in T,
x_p + sum_{t in T} x_t <= 9   (the mixed star cut),
x_e <= 1                     for the twelve e in P,
-sum_{e in choose(B,2)} x_e <= -13  (the selected quota).
```

Every coefficient cancels on all 30 variables and the right sides sum to
`-9+9+12-13=-1`. This is a 31-term, all-unit Farkas certificate of
`0<=-1`. It actually refutes the corresponding box-bounded real relaxation
of this *fixed-footprint* branch. No optimizer, rounding, integrality
assumption or UNSAT solver verdict is needed for that identity.

Among Boolean variables, the eighteen K5 rows and the quota row are
deletion-minimal when box constraints are retained. Start with all pairs
in `choose(B,2)\F` and T red, and all pairs in F blue. This fails just
the star row. The following modifications give all other deletion models:

- Delete the quota: make p blue, giving `m_B=12`.
- Delete a T unit: make that one T pair blue; retain `m_B=13`.
- Delete an F unit: make that F pair red and p blue; retain `m_B=13`.

Every assignment satisfies all other rows. Minimality is for this
specified small certificate, not for the entire inherited constraint
system, and is not a minimum possible proof-size claim.

## Evidence and boundary

`verify.py` checks the fixed input identity, mask implications, cube
translation, every coefficient of the Farkas identity and all nineteen
explicit deletion witnesses. `direct_check.py` imports no other checker:
it builds the literal partial 43-vertex graph, reduces each displayed
five-set by its actual edge colors, propagates B's sharp cardinality,
checks 1,058 literal truth-table cases, and separately finds all nineteen
deletion models by a ten-edge Boolean enumeration and cardinality fill.
`test_verify.py` rejects eleven corrupted inputs/claims.

These are two separately structured implementations by the same author,
not independent peer review or formal verification. The proof is the
displayed elementary implication and exact identity, not an extrapolation
from the small enumeration. Trusted are the unformalized graph-to-row
reasoning, the short Python programs, CPython/runtime/hardware, and SHA-256
for input identity. No catalog uniqueness theorem is required for the
claim about this explicit cyclic core. Applying it to an independently
normalized general c=13 branch inherits that normalization's scope.

The generic clique clauses, saturation and Farkas summation are standard.
The substantive contribution is their exact composition on the surviving
height-2943 selection, including the nine-footprint conditional cut.
