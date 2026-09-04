# Exact diagonal responses on cyclomatic-three equality cores

For a graph `H`, put

```text
M(H) = Q(H) - 2I,
g_H(x) = (M(H)^(-1))_[x,x].
```

The preceding cyclomatic-three core classification proves that every
connected simple graph of minimum degree at least two with `c(H)=3` and
`s(L(H))=2` belongs to the equality family described below.  It also proves
that `M(H)` is nonsingular, so every diagonal response `g_H(x)` is defined.

## Theorem

Write an equality graph as `H(A,B;p,q;r,s)`, where:

- the two terminal-cycle lengths are `A` and `B`;
- the two arcs of the central cycle have lengths `p` and `q`;
- the two paths joining the central cycle to the terminal cycles have lengths
  `r` and `s`.

The equality conditions are

```text
A = B = 1 (mod 4),
{p,q} = {1,3} (mod 4),
r and s are odd.
```

Every diagonal response is positive and is determined exactly by the vertex
role:

```text
g_H(x) = 1/2   on either terminal cycle;
g_H(x) = 3/2   on the central cycle;
g_H(x) = 3/2   at even distance from the central endpoint of a connector;
g_H(x) = 1/2   at odd distance from that endpoint.
```

The endpoint descriptions agree because each connector has odd length.  In
particular,

```text
min_x g_H(x) = 1/2 > -1/2.
```

Consequently, adjoining one leaf at any vertex of an extremal
minimum-degree-two cyclomatic-three core lowers the line-graph signature
exactly from two to one.

The numbers of vertices with the two response values are also explicit:

```text
# {x : g_H(x)=1/2} = A+B+(r-1)/2+(s-1)/2,
# {x : g_H(x)=3/2} = p+q+(r-1)/2+(s-1)/2.
```

## Four-subdivision response transport

Replace an edge `uv` of `H` by

```text
u-a-b-c-d-v
```

and call the new graph `H'`.  The internal block of `M(H')` is

```text
P = [0 1 0 0]       P^(-1) = [ 0 1 0 -1]
    [1 0 1 0]                  [ 1 0 0  0]
    [0 1 0 1]                  [ 0 0 0  1]
    [0 0 1 0]                  [-1 0 1  0].
```

Order the old vertices first and write

```text
M(H') = [N C  ]
        [C^T P].
```

The old degrees are unchanged.  The removed `uv` entry gives

```text
N = M(H) - e_u e_v^T - e_v e_u^T,
C = e_u e_a^T + e_v e_d^T.
```

Direct multiplication gives

```text
C P^(-1) C^T = -e_u e_v^T - e_v e_u^T,
N - C P^(-1) C^T = M(H).
```

Thus the Schur complement is exactly `M(H)`.  The block-inverse formula says
that the old-old block of `M(H')^(-1)` is `M(H)^(-1)`.  Since the diagonal of
`P^(-1)` is zero and the four columns of `C P^(-1)` are

```text
-e_v, e_u, e_v, -e_u,
```

the new diagonal responses, in path order, are

```text
(g_H(v), g_H(u), g_H(v), g_H(u)).                 (1)
```

This proves both nonsingularity preservation and the response-transport rule.

## Reduced bases

Repeatedly reverse four-subdivisions.  Every equality graph reduces to one
with terminal cycles of length five, central arcs of lengths one and three,
and connector lengths `r_0,s_0` in `{1,3}`.  Interchanging the central arcs
only changes their labels.  There are therefore four labeled connector bases
and three bases up to reflection.

The following is the complete exact cofactor calculation.  Here `D=det M`,
and a response is its diagonal principal cofactor divided by `D`.

| `(r_0,s_0)` | `D` | vertices with `g=1/2` | their cofactor | vertices with `g=3/2` | their cofactor |
|---|---:|---:|---:|---:|---:|
| `(1,1)` | `-4` | 10 | `-2` | 4 | `-6` |
| `(1,3)` or `(3,1)` | `4` | 11 | `2` | 5 | `6` |
| `(3,3)` | `-4` | 12 | `-2` | 6 | `-6` |

Within every base, all vertices of the two terminal 5-cycles have response
`1/2`, all vertices of the central 4-cycle have response `3/2`, and the two
internal vertices of a length-three connector have responses `(1/2,3/2)`
when read from the central endpoint.  This is the asserted role formula on
the reduced bases.

Now apply (1).  A four-subdivision inside a terminal cycle inserts four
vertices of response `1/2`; one inside the central cycle inserts four of
response `3/2`.  Adjacent connector vertices have alternating responses, and
(1) extends that alternation by four positions.  Induction proves the exact
formula and the two counting identities for all parameters.

## One-leaf consequence

Let `G` be obtained by adding a new leaf at `x`.  Pivoting the leaf coordinate
of `M(G)` gives

```text
In(M(G)) = (0,0,1) + In(M(H) + 2 e_x e_x^T).
```

For nonsingular `M(H)`, the rank-one response trichotomy shows that the update
has the same inertia as `M(H)` whenever `1+2g_H(x)>0`.  Here that scalar is
two or four.  Therefore `sig M(G)=sig M(H)-1`.  The cyclomatic number is
unchanged, so the incidence identity

```text
s(L(X)) = sig(M(X)) - c(X) + 1
```

gives `s(L(G))=s(L(H))-1=1`.

## Reproduction

Python 3.11 or later is sufficient; no third-party packages are used.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_responses.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_response_cofactors.py
shasum -a 256 -c SHA256SUMS
```

The primary checker uses exact `Fraction` inversion and congruence.  It checks
all eight labeled bases, 128 vertex/leaf ports, and four-subdivision transport
on every one of the 144 labeled base edges.  It ends with

```text
RESULT_SHA256=47fd238a20fb011de41e12807f3bd0fc48c165867a0de0d29175a146fb4896be
```

The independent checker reconstructs the bases without importing the primary
checker and calculates all responses as exact Bareiss determinants and
principal cofactors.  The two programs agree entry by entry through

```text
record_sha256=3f35404094eee97889596aa8fa4387782aef8a329fb3ec58b5d6651deeae5651
```

and the independent run ends with

```text
RESULT_SHA256=b49da24c9733ab37ce854cf37d770d0d9371fdee04b948a3e019e77c9f28a88d
```

## Literature boundary and trust

Paone and Paone prove the `-1/2` one-leaf threshold and state stability of
extremal minimum-degree-two cores as an open conjecture.  Their exact tests
include 1,305 three-cycle chains but are explicitly reported as bounded
negative tests, not a theorem.  Paone classifies the modulo-four
three-cycle-chain signature family and proves the four-subdivision integral
congruence, but does not give this diagonal-response classification.  The
response-protection paper concerns pair responses for adding missing edges
and a generated odd-cyclomatic family; it does not prove the pendant-leaf
claim here.

Primary sources checked:

- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://doi.org/10.5281/zenodo.21706797>.
- Andrea Paone, *Unbounded signature of line graphs: counterexamples and
  transfer mechanisms*, version 2, <https://doi.org/10.5281/zenodo.21534809>.
- Andrea Paone and Marco Paone, *Response Protection for Line-Graph Equality
  Families*, version 1.0, <https://doi.org/10.5281/zenodo.21793638>.

The universal part of this result is the displayed block-inverse transport
and induction.  Exact computation supplies the four finite base inverses;
the cofactor replay has a distinct arithmetic path but shares the graph-family
definition.  The result depends on the preceding computer-assisted
cyclomatic-three equality classification.  It says nothing about multiple
leaves, deeper pendant trees, nonextremal cores, or cyclomatic number four.
