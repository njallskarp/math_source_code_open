# Degree-57 Moore graph: global saturation of the sharp deficit-two star

This directory returns to the frozen 398-coclique frontier only because a new
global incidence invariant is available.  It classifies the equality case of
the maximum-five positive-defect obstruction from Discovery Net height 2491.
The result is structural: it uses the entire Moore radius-two partition, not a
larger table of arbitrary defect profiles.

It does **not** prove that a degree-57 Moore graph exists or does not exist,
and it does not prove that every 398-coclique extends.  It says exactly what
the sharp 96-energy obstruction would have to look like globally.

## Setup

Let `G` be strongly regular with parameters

```
(v,k,lambda,mu)=(3250,57,0,1),
```

and let `S` be an independent set of size 398.  Put `H=G-S` and, for
`u in H`, set

```
a_u=|N_G(u) intersect S|,       z_u=a_u-8.
```

Write `P={u:z_u>0}`, `W={u:z_u<0}`, and `w_u=-z_u` on `W`.  The standard
edge and common-neighbour counts give

```
sum_H z=-130,       sum_H z^2=244,
sum_H z(z+1)=114,  A_H z=7z-2*1.                 (1)
```

For each `s in S` there is also the pointwise design identity

```
sum_{u in N_G(s)} z_u=-2.                         (2)
```

Indeed, the 57 blocks `N_G(u) intersect S` through `s` contain `s` once
for each neighbour `u` and partition the other 397 points of `S`; hence
their sizes sum to `57+397=454`, and `454-8*57=-2`.

## Theorem

Assume

```
max_{u in P} z_u=5,
E_P=sum_{u in P} z_u(z_u+1)=96.                  (3)
```

Then the following conclusions hold.

1. **The positive support is forced.**  `G[P]` is the star `K_{1,33}`.
   Its centre `x` has weight `z_x=5`; its 33 leaves have weight one; and
   there are no edges from `P` to `W`.

2. **Twenty-four global Moore branches carry all negative weight.**  Root
   the Moore radius-two tree at `x`.  Put

   ```
   C=N_G(x) intersect S,
   T=N_G(x) intersect P,
   Q=N_G(x) setminus (S union P).
   ```

   Then `|C|=13`, `|T|=33`, and `|Q|=11`; every vertex of `Q` has defect
   zero.  For each `y in T`, the branch `N_G(y)-{x}` contains nine vertices
   of `S` and 47 zero-defect vertices.  All of `W` lies in the 24 branches
   rooted at `C union Q`, and each such branch has total negative weight
   exactly seven.

3. **Only four negative multiplicity profiles remain.**  Every negative
   weight is at most three.  If `n_j=|{u in W:w_u=j}|`, then for one
   `t in {0,1,2,3}`,

   ```
   (n_1,n_2,n_3)=(150+3t, 9-3t, t).
   ```

   Thus `|W|=159+t`; these are four exact possibilities, not a claim that
   any is realizable.

4. **Weight three forces branchwise Moore saturation.**  A weight-three
   vertex has exactly 23 neighbours in `W`, all of weight one, with exactly
   one in every other weight-bearing branch.  Its five neighbours in `S`
   meet five distinct positive blocks: if its branch is rooted at a point of
   `C`, these are that point of `C` and four distinct nine-point leaf blocks;
   if its branch is rooted in `Q`, they are five distinct leaf blocks.

## Proof

Choose `x in P` with `z_x=5` and put

```
c=sum_{u in N_H(x) intersect W} w_u.
```

The equation at `x` in (1) says that the positive weights on its positive
neighbours sum to `33+c`.  Since `r(r+1)>=2r` for every positive integer
`r`,

```
E_P >= 5*6 + 2(33+c) = 96+2c.
```

Equality in (3) forces `c=0`, makes all 33 positive neighbours have weight
one, and leaves no energy for any further positive vertex.  Thus `P` is the
displayed star.  At a leaf, the centre already contributes five to the
required neighbour sum `7*1-2=5`; (1) then excludes every additional
positive neighbour and every negative neighbour.  Hence there are no
`P`--`W` edges.

The centre has `a_x=13`, so it has 13 neighbours in `S` and 44 in `H`.
The latter are the 33 leaves and 11 zero-defect vertices.  Because `G` has
girth five and attains the diameter-two Moore bound, the 57 sets

```
B_y=N_G(y)-{x},       y in N_G(x),
```

are disjoint 56-vertex branches and cover every vertex outside the closed
neighbourhood of `x`.

For `y in T`, the leaf has nine neighbours in `S`; all its other 47 branch
vertices have defect zero by the first part.  For `s in C`, identity (2)
contains the centre's contribution five and gives
`sum_{B_s} z=-7`.  For `q in Q`, the equation in (1) similarly gives
`sum_{B_q intersect H} z=-7`, again after subtracting the centre's
contribution five.  No branch contains another positive vertex.  Therefore
the 24 branches rooted at `C union Q` contain all of `W`, each with total
`w`-weight seven; the leaf branches contain none.

The moments in (1) and the forced positive star give

```
sum_W w=168,       sum_W w^2=186,
sum_W w(w-1)=18.                                 (4)
```

In particular `w<=4`.  Since there are no `P`--`W` edges, (1) restricted
to `W` becomes

```
A_{G[W]} w=7w+2*1.                               (5)
```

Vertices in the same Moore branch are nonadjacent and have no common
neighbour in `W`: they already share their branch root.  A vertex has at most
one neighbour in each other branch, since two would share both it and that
other branch root.  Thus every vertex of `W` has at most 23 neighbours in
`W`.

Suppose `w_u=4`, and write `d=d_{G[W]}(u)`.  Equation (5) gives neighbour
weight 30 and

```
(A_{G[W]}^2 w)_u=7*30+2d=210+2d.
```

The returning two-walks contribute `4d`.  All nonreturning endpoints are
distinct by girth five, avoid the weight-seven branch of `u`, and avoid its
neighbours of total weight 30.  Their total available weight is at most
`168-7-30=131`.  Consequently

```
210+2d <= 4d+131,
```

so `d>=40`, contradicting `d<=23`.  Therefore `w<=3`.  Equations (4) now
give `n_2+3n_3=9` and `n_1=150+3n_3`, proving conclusion 3.

If `w_u=3`, (5) gives neighbour weight 23.  Again put
`d=d_{G[W]}(u)`.  The same two-walk argument now gives

```
161+2d=(A_{G[W]}^2w)_u <= 3d+(168-7-23)=3d+138.
```

Hence `d>=23`.  The branch constraint gives `d<=23`, so equality holds.
All 23 neighbours have weight one and occupy the 23 other branches one each.

It remains to locate the five `S`-neighbours of such a vertex.  The centre
block `C=N_G(x) intersect S` and the 33 nine-point blocks
`N_G(y) intersect S`, `y in T`, are pairwise disjoint: their corresponding
vertices are neighbours of `x`.  Identity (2) says that their negative
weighted demands are respectively 7 and 3 per point, while every point
outside those blocks has demand 2.  A weight-three block cannot meet the
last region, and it meets each positive block at most once because its vertex
is nonadjacent to every positive vertex.  A vertex in a branch rooted at
`s in C` contains `s`; a vertex in a branch rooted at `q in Q` cannot meet
`C`, since it and `x` already have the unique common neighbour `q`.
The two asserted five-point patterns follow.

## What this closes, and what it does not

Height 2491 exhibited a weighted `K_{1,33}` consuming 96 of the 114 defect
energy units as a local barrier.  The theorem above proves that equality
forces that star globally and then compresses its negative side to four
profiles with an exact 24-branch design.  It also eliminates weight four and
turns every weight-three vertex into a fully saturated branch transversal.

This does not eliminate the sharp star itself.  The next legitimate target is
now precise: exclude or construct one of the four weighted 24-branch systems,
starting with the `t=0` all-weight-one/two case, using the perfect matchings
between Moore branches.  If that step becomes only labelled configuration
enumeration, freeze the lane again.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd moore57_star_saturation
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

The verifier uses only Python arbitrary-precision integers.  It checks the
global moments, equality forcing, all branch totals, the weight-four
contradiction, the weight-three equality, and the four residual profiles.

## Literature and trust boundary

Primary sources checked on 2026-09-05:

- M. A. Fiol and E. Garriga, [*On outindependent subgraphs of strongly
  regular graphs*](https://doi.org/10.1080/03081080500143902).
- C. Dalfo, [*A survey on the missing Moore
  graph*](https://doi.org/10.1016/j.laa.2018.12.035).
- V. Faber and J. Keegan, [*Existence of a Moore graph of degree 57 is still
  open*](https://arxiv.org/abs/2210.09577).
- Y. Ishida, [*No involutions in the missing Moore
  graph*](https://arxiv.org/abs/2606.29183).

The first two sources cover the Hoffman bound, outindependent spectra, and the
400-coclique equality case.  The latter two confirm the degree-57 existence
problem remains open and record current conditional restrictions.  Targeted
searches found no treatment of 398-cocliques, the sharp weighted star, or the
24-branch saturation above.  This is a scoped novelty audit, not an exhaustive
historical-priority claim.

The theorem trusts only the stated strongly regular parameters, exact finite
counting, Rayleigh-free two-walk inequalities, and elementary integer
arithmetic.  The script audits those arithmetic consequences but does not
prove the prose graph argument.  No floating point, randomness, solver,
external dataset, catalogue, large certificate, or private state is used.
