# Two-leaf stability on cyclomatic-three equality cores

Let `H` be a connected simple graph of minimum degree at least two with

```text
c(H)=3,                 s(L(H))=2,
```

and let `G=G(H;x,y)` be obtained by adjoining two distinct new leaves, one at
`x` and one at `y`.  The ports may coincide.  Put

```text
M = Q(H)-2I,            E = [e_x,e_y],
S_H(x,y) = (1/2)I_2 + E^T M^(-1) E.
```

The preceding equality-family response theorem proves that `M` is
nonsingular and that every diagonal entry of `M^(-1)` is either `1/2` or
`3/2`.

## Theorem

For every such `H,x,y`,

```text
s(L(G))-s(L(H)) = -sig(S_H(x,y)) <= 0.
```

Consequently,

```text
s(L(G)) <= 2.
```

Thus every cyclomatic-three equality core is stable under the simultaneous
addition of two leaves.  The conclusion allows two leaves at the same port,
but it does not assert stability for deeper pendant trees or for an arbitrary
number of simultaneous leaves.

## Rank-two inertia identity

Order the old vertices before the two new leaves.  Increasing the degrees at
the ports and adding the two incidence columns gives

```text
M(G) = [M+EE^T   E ] .
       [ E^T    -I_2]
```

Pivoting the lower-right block shows that this is congruent to

```text
(-I_2) direct-sum (M+2EE^T).                         (1)
```

Now consider the bordered matrix

```text
B = [M       E     ].
    [E^T  -(1/2)I_2]
```

Schur complementation in its two possible orders gives

```text
B congruent to M direct-sum (-S_H(x,y)),
B congruent to -(1/2)I_2 direct-sum (M+2EE^T).
```

Taking signatures and using (1) yields the exact update formula

```text
sig M(G) - sig M = -sig(S_H(x,y)).                   (2)
```

Adding leaves does not change cyclomatic number.  The incidence identity

```text
s(L(X)) = sig(Q(X)-2I) - c(X) + 1
```

therefore turns (2) into the displayed line-graph formula.

## Why the update cannot be positive

The diagonal-response classification gives

```text
S_H(x,y)_[1,1] = 1/2 + g_H(x) in {1,2},
S_H(x,y)_[2,2] = 1/2 + g_H(y) in {1,2}.
```

A real symmetric `2` by `2` matrix with both diagonal entries positive cannot
be negative definite.  Hence its possible signatures are `0`, `1`, and `2`,
all nonnegative.  Equation (2) proves the theorem.  Notice that no estimate
for the off-diagonal response `(M^(-1))_[x,y]` is needed.

## Exact reduced-base replay

The proof above is all-parameter once the diagonal-response theorem is known.
For an additional finite audit, the primary checker enumerates all eight
labeled reduced equality bases and every unordered pair of ports, with
repetition.  It forms `S_H(x,y)` by exact `Fraction` inversion, verifies (2)
against `M(G)`, and finds

```text
base assignments                         8
unordered port pairs                  1096
positive-definite response matrices   1088
indefinite response matrices             8
singular response matrices                0
```

The independent checker reconstructs the bases without importing the response
checker, builds each augmented line graph directly from edge intersections,
and obtains the same 1,096 outcome records through an exact
characteristic-polynomial inertia calculation.

Both checkers produce the common outcome-record digest

```text
23e4837cd42cd256addc6621fb0257bb623ae426264d144403c685691663e5e9
```

Their respective result hashes are

```text
c6dbf73ee8ec2f4f9b864c805e70a664734fcc202819008a93762f61f4d7e977
64257c5fe32e79f7eae92330b7bf4a562d21b4a69441c0c252a8756120fc7214
```

Run, with Python 3.11 or later and no third-party package,

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_two_leaves.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_two_leaves_direct.py
shasum -a 256 -c SHA256SUMS
```

The finite replay is corroboration, not an extrapolation: all-parameter
coverage comes from the rank-two identity and the already-proved
four-subdivision diagonal-response transport.

## Literature boundary and trust

Paone and Paone formulate the one-leaf conjecture and a stronger arbitrary
pendant-forest conjecture.  Their version 1.3 package reports bounded tests of
1,400 pairs of leaf attachments; those tests are not an all-parameter proof.
The generic rank-two identity above also appears in the independently authored
cyclomatic-two two-leaf analysis in Discovery Net.  The new content here is
its application to the exact all-parameter cyclomatic-three diagonal-response
classification.

Primary sources checked:

- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://doi.org/10.5281/zenodo.21706797>.
- Andrea Paone and Marco Paone, *Response Protection for Line-Graph Equality
  Families*, version 1.0, <https://doi.org/10.5281/zenodo.21793638>.

The rank-two congruence argument is human-checkable.  Its use here depends on
the computer-assisted cyclomatic-three equality classification and the exact
diagonal-response theorem in `C3_EQUALITY_RESPONSE.md`; the latter has two
same-author exact implementations but has not yet received independent
mathematical review.  The reduced-base pair census shares the family definition
with those results.  The direct line-graph checker has an independent graph
builder and spectral route, but it remains a finite audit of the reduced bases.
