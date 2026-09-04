# Three-leaf stability on cyclomatic-three equality cores

Let `H` be a connected simple graph of minimum degree at least two with

```text
c(H)=3,                 s(L(H))=2,
```

and put

```text
M = Q(H)-2I,            W = M^(-1).
```

The independently reviewed equality-response theorem proves that `M` is
nonsingular and divides the vertices into two response classes:

```text
L = {x : W_[x,x]=1/2},  R = {x : W_[x,x]=3/2}.
```

The letter `R` here means the high-response class and is unrelated to an
incidence matrix.

## Theorem

Choose three vertices `x_1,x_2,x_3` of `H`, with repetition allowed, and
adjoin three distinct new leaves, one at each chosen port.  If the resulting
graph is `G`, then

```text
s(L(G)) <= 1.
```

In particular, three simultaneous leaves cannot increase the signature of a
cyclomatic-three equality core; they lower it by at least one.  The bound is
sharp.

## Same-class Green-function bounds

The structural input beyond the diagonal-response theorem is

```text
x,y in L:    |W_[x,y]| <= 1/2,
x,y in R:    |W_[x,y]| <= 3/2.                     (1)
```

For the edge-subdivision induction we retain the following auxiliary edge
invariant:

```text
xy an edge in L:  W_[x,y] = 1/2,
xy an edge in R: -1/2 <= W_[x,y] <= 3/2.           (2)
```

Every equality graph reduces by reversing four-subdivisions to one of the
eight labeled bases with terminal cycles of length five, central arcs of
lengths one and three in either order, and connector lengths in `{1,3}`.
Exact inversion gives the complete base value sets

| response class | all same-class entries | same-class edge entries |
|---|---|---|
| `L` | `{-1/2,0,1/2}` | `{1/2}` |
| `R` | `{-3/2,0,1,3/2}` | `{0,1}` |

Thus (1)--(2) hold on every reduced base.

Now four-subdivide an edge `uv` as

```text
u-a-b-c-d-v.
```

Write `h=W_[u,v]`, `g_u=W_[u,u]`, and `g_v=W_[v,v]`.  The Schur-complement
calculation in the diagonal-response theorem keeps the old-old block of the
inverse equal to `W`.  The new-old rows are, in path order,

```text
 W_[v,*], -W_[u,*], -W_[v,*], W_[u,*],             (3)
```

and the new-new block is

```text
[ g_v   1-h   -g_v   h-1]
[ 1-h   g_u    h    -g_u]
[-g_v    h     g_v   1-h]
[ h-1  -g_u   1-h    g_u].                         (4)
```

The new vertex classes are respectively those of `v,u,v,u`.  Formula (3)
therefore preserves every old-new instance of (1).  If `u,v` have different
classes, the only same-class pairs within (4) have entries `-g_u` or `-g_v`,
and every new path edge is mixed-class.  If both endpoints lie in `L`, (2)
gives `h=1/2`, so every entry `h` or `1-h` is `1/2`.  If both lie in `R`, the
interval `[-1/2,3/2]` is preserved by `h -> 1-h`; all entries in (4) satisfy
(1), and every new path edge again satisfies (2).  Old pairs and old
unsubdivided edges are unchanged.  Induction proves (1)--(2) for every member
of the all-parameter equality family.

## Three-port inertia

Let `E=[e_(x_1),e_(x_2),e_(x_3)]` and define

```text
S_E = (1/2)I_3 + E^T W E.
```

Eliminating the three new leaf coordinates and comparing the two Schur
complements of the usual bordered matrix gives the exact identity

```text
s(L(G))-s(L(H)) = -sig(S_E).                        (5)
```

Among three ports, two belong to the same response class.  This remains true
when ports repeat.  The corresponding principal `2` by `2` block of `S_E` is

```text
[1  W_[x,y]]                    [2  W_[x,y]]
[W_[x,y]  1]       or          [W_[x,y]  2].
```

By (1), its determinant is at least `3/4` in class `L` and at least `7/4` in
class `R`; its diagonal is positive, so it is positive definite.  Cauchy
interlacing implies that `S_E` has at least two positive eigenvalues.  Since
it has order three, it has at most one negative eigenvalue and hence

```text
sig(S_E) >= 1.
```

Equation (5), together with `s(L(H))=2`, proves the theorem.

## Sharpness

Take terminal cycle lengths `A=B=5`, central arc lengths `(p,q)=(1,3)`, and
connector lengths `(r,s)=(1,3)`.  On the length-three connector from the
central vertex `y` to the terminal root, call its internal vertices `z_1,z_2`
in that order.  For the three distinct ports `x,z_1,z_2`, exact inversion
gives

```text
S_E = [2   0    0  ]
      [0   1   3/2 ] ,       In(S_E)=(2,0,1).
      [0  3/2   2  ]
```

Thus `sig(S_E)=1` and the augmented graph has `s(L(G))=1`.

## Reproduction

Python 3.11 or later is sufficient; no third-party package is used.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_three_leaves.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_same_type_cofactors.py
shasum -a 256 -c SHA256SUMS
```

The first checker verifies the same-class invariant on all eight reduced
bases, checks the full inverse transport for all 144 labeled base edges, and
corroborates (5) on every unordered three-port multiset in the bases.  The
second checker reconstructs the bases independently and obtains every
same-class inverse entry from integer Bareiss cofactors.  It also checks the
displayed sharpness witness from the direct line-graph definition.

The checkers agree entry by entry on the same-class reduced-base data through

```text
same_class_record_sha256=93c45c4e2fd5bbb3f8f9ef258186f5b4585e3f1828303ffd358cb51cb78a7c33
```

Their respective result hashes are

```text
1c0d40846cc8084edc5ab28930d9d13aa118ae132270769ffce18723b7739af3
c0006ad64c0dfb18bba3279e71ca672153d2750f2b97070dc8d7cd4621ca7671
```

The triple enumeration is corroborative only.  Universal coverage comes from
the displayed inverse transport, the closed invariant (1)--(2), and
interlacing.

## Literature boundary and trust

Paone and Paone state arbitrary pendant-forest stability of extremal cores as
open and explicitly warn that one-port positivity does not control interacting
attachments.  Their 1,400 exact two-leaf tests are bounded negative tests, not
a three-port theorem.  Their response-protection paper treats missing-edge
addition with a different response vector and threshold.

Primary sources checked:

- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://doi.org/10.5281/zenodo.21706797>.
- Andrea Paone and Marco Paone, *Response Protection for Line-Graph Equality
  Families*, version 1.0, <https://doi.org/10.5281/zenodo.21793638>.

The height-1827 diagonal classification was independently reconstructed and
accepted at Discovery Net height 1847.  The new all-parameter step is the
human-readable same-class invariant and its four-subdivision closure.  Exact
computation supplies its finite reduced-base values; the cofactor replay uses
a separate builder and arithmetic route but shares the equality-family
definition.  The theorem concerns three isolated leaf edges only, not deeper
pendant trees, four or more leaves, nonextremal cores, or cyclomatic number
four.
