# A circulant barrier to pair-deletion at the Albertson r=28 frontier

This directory gives an explicit structural obstruction to one proposed next
step after the exact `r=28` frontier reduction.  It does **not** construct an
Albertson counterexample.  Rather, it proves that degree data,
factor-criticality, the degree-27 Hall matchings, and the first two pair moments
do not by themselves strengthen the existing one- or two-vertex deletion
bounds.

## Barrier proposition

Let `C` be the graph on `Z/55Z` joining two vertices when their circular
distance is at most 13.  Thus `C` is 26-regular, has 715 edges, and contains the
spanning cycle of step one.  Define

    H_769 = C + {0,27},
    H_768 = C + {0,27} + {1,28},

and let `G_m` be the complement of `H_m`.  Then:

1. `G_m` has `m` edges.  For `m=769`, its excess vector
   `x_v=d_G(v)-27` is `0^2,1^53`; for `m=768` it is `0^4,1^51`.
2. Each `H_m` is connected and factor-critical.
3. For every vertex with `x_v=0`, `H_m-v` has a perfect matching entirely
   across `(N_H(v),N_G(v))`.  Thus all degree-27 Hall constraints recorded in
   the frontier theorem hold.
4. Let `F_s(q)` be the exact integer table obtained from the four published
   affine crossing inequalities and the reviewed convex induced-subgraph
   recurrence.  The deletion functionals are

       row 768: sum_v F_54(768-27-x_v) = 360044, ceiling /51 = 7060;
       row 769: sum_v F_54(769-27-x_v) = 361685, ceiling /51 = 7092.

   For pairs, put `h_uv=1[uv in E(H)]` and
   `D_uv=x_u+x_v+h_uv`.  The exact distributions and functionals are

       row 768: #D=(0:2,1:108,2:762,3:613),
                sum D=3471, sum D^2=8673,
                sum F_53(715-D)=9000908, ceiling /1275 = 7060;

       row 769: #D=(1:55,2:767,3:663),
                sum D=3578, sum D^2=9090,
                sum F_53(716-D)=9040923, ceiling /1275 = 7091.

Consequently the exact pair-deficit moments, even when realised by connected
factor-critical graphs satisfying every minimum-degree-root Hall constraint,
do not improve 7060 on row 768 or 7092 on row 769.  In particular they cannot
provide the requested ten-crossing gain or eliminate row 769.

## Proof of the structural assertions

The step-one edges form a Hamilton cycle in both graphs.  After deleting any
vertex `v`, list the remaining cycle vertices as

    v+1,v+2,...,v+54  (mod 55)

and pair consecutive entries.  These 27 cycle edges give a perfect matching,
so both graphs are factor-critical.

The degree-27 roots of `H_769` are `0,27`; those of `H_768` are
`0,1,27,28`.  For root 0, an explicit cross matching is

    {i,i+13} (1<=i<=13), {27,28}, {i,i-13} (42<=i<=54).

For root 27, use

    {0,54}, {i,i-13} (14<=i<=26), {i,i+13} (28<=i<=40).

For roots 1 and 28 in `H_768`, translate these two matchings by one.  Each
displayed pair is an edge of the appropriate circulant-plus-chords graph, the
pairs cover all vertices except the root, and exactly one endpoint of every
pair is a neighbour of the root.  This proves the Hall claims constructively.

For row 769, let `A={0,27}`.  Its unique internal pair is an `H`-edge.  Counting
pairs inside `A`, across `(A,V-A)`, and inside `V-A` gives the displayed
distribution of `D`.  For row 768, the four roots span exactly four `H`-edges:
the two cycle edges `01,27-28` and the two added chords.  The same three-class
count gives `(2,108,762,613)`.  Substitution into the reconstructed exact
tables gives the deletion sums above.

## The missing criticality invariant

Both pseudomodels deliberately expose why they are not complements of
28-chromatic graphs.  The vertices `{0,1,2}` form a triangle in `H_m`, and
`H_m-{0,1,2}` has the 26-edge perfect matching

    {3,4},{5,6},...,{53,54}.

Thus this is a *conformal triangle*.  In the complement, it becomes one
independent triple and the matching edges become 26 independent pairs, giving
a 27-colouring.  An actual 28-critical complement therefore has no conformal
triangle.  This exclusion, which is stronger than factor-criticality and the
root Hall matchings, is an explicit missing invariant that any further
structural pass must use.

The conclusion is deliberately limited: it does not say that conformal-
triangle exclusion is sufficient to close either row, nor that no stronger
argument can exploit the full critical graph.  It says exactly that the
previously recorded factor-critical/Hall and pair-moment data cannot do so.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_pair_deletion_barrier
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

The verifier reconstructs the rounded convex tables through order 54, builds
both graphs from their definitions, checks every vertex-deletion matching and
every displayed root matching, computes every pair deficit directly, and
checks the conformal triangle.  Runtime is about nine seconds.

## Trust boundary

The executable uses Python arbitrary-precision integers, `fractions.Fraction`,
finite sets, and deterministic loops.  It uses no solver, graph library,
floating point, randomness, downloaded data, or imported campaign code.  The
script verifies the finite construction and arithmetic, not the cited
crossing inequalities, the topology-to-deletion recurrence, or the prose
interpretation that an independent triple plus 26 independent pairs is a
27-colouring.

## Status and relation to prior work

The exact two-row frontier and its factor-critical, Hall, and pair-moment
consequences are at Discovery Net height 2523.  Height 2521 independently
formalizes the relevant deletion recurrence values.  This contribution adds
the explicit circulant realisations showing that those particular structural
statistics are insufficient; it neither objects to nor duplicates either
result.

Stehlik's [critical-complement colouring
theorem](https://doi.org/10.1016/S0095-8956(03)00069-8) supplies the matching
normal form for genuine critical graphs.  The elementary conformal-triangle
exclusion used here is also recorded in the earlier Discovery Net complement
analysis at height 1777.  Targeted committed-graph and matching-literature
searches through 2026-09-05 found no prior statement of these two exact
circulant barrier instances.  This is a search-relative novelty statement, not
a claim of historical priority.

## Conditional claims

There are none.  No `r=27` terminal theorem and no local crossing conjecture is
used.  The objects above are explicitly labelled pseudomodels, not
28-chromatic graphs.
