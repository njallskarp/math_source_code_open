# One-sided rigidity and obstruction at coclique deficit two

## Theorem

Let `G` be a strongly regular graph with parameters `(3250,57,0,1)`, and let
`S` be an independent set of size `398`.  For `x` outside `S`, write

```text
a_x = |N_G(x) intersect S|,       z_x = a_x-8.
```

Then:

1. If `z_x<=0` for every `x`, then the neighbour-count multiset is exactly

   ```text
   {0^2, 6^1, 7^112, 8^2737},
   ```

   and `S` is contained in a unique 400-coclique.

2. If `S` is not contained in a 400-coclique, its positive support
   `P={x:z_x>0}` satisfies

   ```text
   27 <= |P| <= 57,
   rho(G[P]) >= 5,
   max_{x in P} z_x is one of 1, 2, 5.
   ```

Thus any nonextendible 398-coclique must cross the Hoffman level `a_x=8` on a
large, spectrally dense, tightly quantized support.

## Exact identities

Put `H=G[V(G)\S]`.  Edge counting and unique common-neighbour counting give

```text
sum_x a_x = 57*398,
sum_x binom(a_x,2) = binom(398,2).
```

There are `2852` vertices outside `S`, so after substituting `z_x=a_x-8`,

```text
sum_x z_x=-130,
sum_x z_x^2=244,
sum_x z_x(z_x+1)=114.                         (1)
```

As in the deficit-one theorem, for each outside vertex `x`, the closed
`H`-neighbourhood blocks `N_G(y) intersect S` partition `S`.  Equivalently,

```text
A_H z = 7z-2.                                 (2)
```

We repeatedly use the elementary spectral Moore bound

```text
rho(F)^2 <= |V(F)|-1                          (3)
```

for a graph `F` of girth at least five.  It follows because every row sum of
`A_F^2` is at most `|V(F)|-1`: triangle- and four-cycle-freeness make all
non-returning two-step endpoints distinct.

## Nonpositive defects force extension

Assume first that `z<=0`, and put `w=-z`.  If some `a_x=0`, then adjoining
`x` gives a 399-coclique.  The deficit-one theorem in [THEOREM.md](THEOREM.md)
says that this 399-coclique has a unique 400-extension.  It remains only to
show that such an `x` must exist.

Suppose otherwise that every `a_x>=1`.  Then `0<=w_x<=7`, and (1)--(2) give

```text
sum w_x=130,       sum w_x^2=244,       A_H w=7w+2.     (4)
```

Let `Z={x:w_x=0}`.  At each `x in Z`, (4) says that the sum of the weights on
its neighbours is exactly `2`.  Hence a vertex of weight at least `3` has no
neighbour in `Z`.  Such a vertex of weight `w` would have all of its
`49+w` neighbours in the positive support of `w`.  Since each of those
neighbours has weight at least one, (4) would imply

```text
49+w <= 7w+2,
```

so `w>=8`, contrary to `w<=7`.  Thus every nonzero weight is `1` or `2`.
The two moments in (4) now force

```text
|W_1|=16,       |W_2|=57,       |Z|=2779.              (5)
```

Let `e_11` be the number of edges inside `W_1`, and `e_12` the number between
`W_1` and `W_2`.  Summing the weighted neighbour equation `A_Hw=9` over
`W_1` gives

```text
e_11+e_12=72.                                  (6)
```

Every vertex in `Z` has either one neighbour in `W_2` or two neighbours in
`W_1`.  Let `B` count the latter type.  Counting the `W_1`--`Z` edges by
their `W_1` endpoints, whose full `H`-degree is `50`, and then using (6),
gives

```text
2B = 16*50-(2e_11+e_12) = 728-e_11.            (7)
```

On the other hand, each such `Z` vertex selects a nonadjacent pair in `W_1`.
Triangle-freeness excludes adjacent pairs, and four-cycle-freeness prevents
two `Z` vertices from selecting the same pair.  Therefore

```text
B <= binom(16,2)-e_11 = 120-e_11.               (8)
```

Equations (7)--(8) would imply `488+e_11<=0`, which is impossible.  Hence an
outside vertex with `a_x=0` exists and the deficit-one theorem supplies the
unique 400-extension.

If `C` is that 400-coclique, the two vertices of `C\S` are nonadjacent and
have one common neighbour.  The standard Moore counts then give two outside
vertices with `a=0`, their common neighbour with `a=6`, 112 other vertices
adjacent to exactly one deleted point with `a=7`, and 2737 with `a=8`.  This
is the profile in part 1 and also proves uniqueness.

## Structure forced on the positive support

Now suppose `P={x:z_x>0}` is nonempty, and put `w_x=-z_x` on the negative
support.  Restricting (2) to `P` gives

```text
A_{G[P]} z_P = 7z_P-2*1 + B w >= 5z_P,          (9)
```

where `B` is the `P`--negative-support incidence matrix.  The Rayleigh
quotient yields `rho(G[P])>=5`; (3) yields `|P|>=26`.  Also every positive
integer contributes at least two to the energy in (1), so `|P|<=57`.

The equality case `|P|=26` is impossible.  Indeed (3) and (9) would force
equality throughout, hence `z_P=1`, `Bw=0`, and `G[P]` would be 5-regular of
girth at least five on 26 vertices.  It would attain the Moore bound, so on
the 25-dimensional space perpendicular to the all-ones vector its adjacency
eigenvalues would be the roots of

```text
t^2+t-4.
```

This polynomial is irreducible over the rationals, so its conjugate roots
must have equal multiplicity in the integral characteristic polynomial.  An
odd total multiplicity 25 is impossible.  Therefore `|P|>=27`.

It remains to quantize the maximum positive defect.  Let `M=max_P z`, choose
`v` of weight `M`, and write `t=z_u` for a positive neighbour `u` of `v`.
Equation (9) gives

```text
sum_{u in N_P(v)} z_u >= 7M-2.                  (10)
```

For each such `u`, its other positive neighbours have total weight at least
`max(0,7t-2-M)`.  Girth at least five makes these distance-two sets disjoint
for distinct neighbours of `v`.  Since a positive weight `r` consumes energy
`r(r+1)>=2r`, (1) gives

```text
114 >= M(M+1) + sum_{u in N_P(v)}
       [t(t+1)+2 max(0,7t-2-M)].                (11)
```

For `1<=M<=4`, the bracket is at least `(12-2M)t`, because the difference is

```text
(t-1)(t+2M+4) >= 0.
```

Together with (10), the resulting lower energy for `M=1,2,3,4` is
respectively `52,102,126,124`; hence `M=3,4` are impossible.  For `M>=5`,
discarding the distance-two term in (11) and using `t(t+1)>=2t` gives

```text
114 >= M(M+1)+2(7M-2) = M^2+15M-4.
```

This excludes every `M>=6`, while `M=5` is not excluded.  Thus
`M in {1,2,5}`, proving part 2.

## Barrier and freeze condition

The last alternative is genuine for this method.  At the positive-support
level, a star with centre weight `5` and 33 leaves of weight `1` satisfies
the equality-side local equations in (9): the centre sees weight 33 and each
leaf sees weight 5.  It consumes only 96 of the 114 defect-energy units and
has no triangle or four-cycle.  This is not claimed to embed in a Moore graph,
but it proves that the moment, radius-two, and spectral-Moore inequalities
alone cannot eliminate the positive branch.

Further progress therefore needs a new global incidence/design constraint,
not a longer degree-profile enumeration.  The coclique lane should remain
frozen unless such a mechanism or a reviewer objection appears.
