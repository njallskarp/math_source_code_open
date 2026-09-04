# Proof of the lower bound

## Theorem

For every integer `d >= 3`,

```text
sat(Q_d,Q_2) >= 7 d 2^(d-1) / (2d+5).
```

Equivalently, because the left side is integral,

```text
sat(Q_d,Q_2) >= ceil(7 d 2^(d-1) / (2d+5)).
```

In particular,

```text
liminf_{d -> infinity} sat(Q_d,Q_2)/2^d >= 7/4.
```

## Terminology and global slack

Fix a square-saturated graph `G` in `Q_d`.  Write

```text
N = |E(Q_d)| = d 2^(d-1),
E = |E(G)|,
M = N-E.
```

Call a square face **active** if exactly three of its four edges lie in `G`.
Let `T` be the number of active faces.  Every omitted edge must be the unique
omitted edge of at least one active face, so, if `w(e)` is the number of active
faces whose missing edge is the omitted edge `e`, then

```text
w(e) >= 1,
T = sum_(e omitted) w(e).
```

Define two nonnegative slacks

```text
A = T-M = sum_(e omitted) (w(e)-1),
B = (d-1)E-3T.
```

Here `(d-1)E` counts incidences `(selected edge, square face containing it)`,
while the active faces account for `3T` of these incidences.  Thus `B` is
exactly the number of selected-edge incidences on inactive square faces.

The identity to be strengthened is

```text
B+3A = (d-1)E-3M.                                      (1)
```

The usual active-face count uses only `A,B >= 0`.  We prove the extra bound

```text
B+3A >= T/2 >= M/2.                                    (2)
```

## Local 3-cube slack lemma

Consider any square-free edge pattern in a 3-cube `C`.  Let

- `t` be the number of active square faces of `C`;
- `r` be the number of distinct missing edges of those active faces; and
- `b` be the number of selected-edge incidences on inactive square faces of
  `C`.

Then

```text
b + 2(t-r) >= t/2.                                     (3)
```

### Proof

The adjacency graph of the six square faces of a 3-cube, where two faces are
adjacent when they share an edge, is `K_{2,2,2}`: the three parts are the
three pairs of opposite faces.  Let `S` be the set of `t` active faces and let
`delta(S)` be its edge boundary in this face-adjacency graph.

Each active face has three selected boundary edges and one missing boundary
edge.  Put

```text
q = t-r.
```

An edge of a 3-cube lies in two square faces.  Hence `q` is precisely the
number of adjacent active-face pairs whose shared edge is missing in both
faces.  Such pairs use `2q` of the `t` active missing-edge incidences.  The
remaining `t-2q` missing incidences cross from `S` to its complement.

Let `a` count boundary adjacencies whose shared edge is selected.  Therefore

```text
delta(S) = a + t-2q,
a+2q = delta(S)-t+4q.                                  (4)
```

Every adjacency counted by `a` supplies a selected-edge incidence on an
inactive face, so `b >= a`.

It remains to show `delta(S)+4q >= 3t/2`.  For subsets of size `t=1,2,3,4`
in `K_{2,2,2}`, the elementary boundary minima are respectively

```text
4, 6, 6, 6,
```

and each is at least `3t/2`.  If `t=5`, the face opposite the unique inactive
face has all four neighbours active.  Its missing edge is consequently also
missing in an adjacent active face, so `q >= 1`; now
`delta(S)+4q >= 4+4 > 15/2`.  If `t=6`, the other face containing the missing
edge of every active face is active.  These missing incidences pair up, so
`q=3`, and `delta(S)+4q=12 >= 9`.  The case `t=0` is immediate.

Combining this with (4) and `b >= a` proves (3).  Notice that square-freeness
is essential: it ensures every face has at most three selected edges and that
an active face has a unique missing edge.

## Summation over all 3-subcubes

Apply (3) to every 3-dimensional subcube `C` of `Q_d`, writing its parameters
as `t_C,r_C,b_C`.  Every square face lies in exactly `d-2` 3-subcubes.  Hence

```text
sum_C t_C = (d-2)T,
sum_C b_C = (d-2)B.                                    (5)
```

For a fixed omitted edge `e`, two different active faces witnessing `e`
span a unique 3-subcube.  Conversely, every repetition counted by
`t_C-r_C` is such a pair.  Therefore

```text
sum_C (t_C-r_C) = sum_(e omitted) binom(w(e),2).         (6)
```

An edge of `Q_d` lies in `d-1` square faces, so `1 <= w(e) <= d-1`.  It follows
that

```text
binom(w(e),2) <= (d-1)(w(e)-1)/2.
```

Sum (3) and use (5), (6), and this last estimate:

```text
(d-2)B + (d-1)A >= (d-2)T/2.                           (7)
```

For `d >= 3`, `d-1 <= 3(d-2)`.  Thus the left side of (7) is at most
`(d-2)(B+3A)`, and division by `d-2` proves (2).

Finally combine (1) and (2):

```text
(d-1)E-3M >= M/2,
2(d-1)E >= 7M = 7(N-E),
(2d+5)E >= 7N = 7d 2^(d-1).
```

This is the claimed bound.

## Checks at small dimensions

For `d=3`, the theorem gives `E >= ceil(84/11)=8`.  Direct enumeration finds
66 square-saturated patterns with eight edges and eight with nine edges, so
the new lower bound is exact in `Q_3`.  For `d=2`, direct enumeration gives
`sat(Q_2,Q_2)=3`; the theorem is intentionally stated only for `d>=3`, where
3-subcube summation is available.
