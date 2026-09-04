# The NF-number of all remaining dumbbell graphs

## Result

Let `B_(n,m)` be the graph obtained from disjoint cliques `K_n` and `K_m`
by adding one bridge edge. The NF operator sends a simplicial complex to
the Stanley--Reisner complex of its facet ideal, and the NF-number is the
first positive return up to simplicial-complex isomorphism.

**Theorem.** For every `n,m >= 3`,

```text
NF(B_(n,m)) = n + m + 2.
```

Together with the previously proved width-two result

```text
NF(B_(2,m)) = m+4  for m>=3,
NF(B_(2,2)) = 1    up to isomorphism,
```

this resolves the dumbbell conjecture under its stated up-to-isomorphism
convention:

```text
NF(B_(n,m)) = n+m+2
```

for all `n,m>=2` except `B_(2,2)=P_4`, whose value is `1`.

The proof below gives one orbit construction parameterized simultaneously by
both clique sizes. Computation is used only to check the formulas and guard
their collision boundaries.

## Lossless type quotient

By `B_(n,m) ~= B_(m,n)`, assume

```text
3 <= k=n <= m,    q=m-1.
```

Write

```text
X={x_0,x_1,...,x_(k-1)},   Y={y_0,y_1,...,y_q},
```

and use `x_0y_0` as the bridge. The group
`S_(k-1) x S_q`, independently permuting the ordinary vertices in the two
cliques, preserves the entire NF orbit. A subset has type

```text
(a,i,b,j) in {0,1} x {0,...,k-1} x {0,1} x {0,...,q},    (1)
```

where `a,b` record the distinguished vertices and `i,j` count ordinary
vertices. Possible containment of two subset orbits is exactly
coordinatewise comparison of their types. The quotient therefore loses no
incidence information.

For an invariant facet antichain `E` and a base `z=(a,i,b)`, put

```text
h_E(z)=min({j-1 : (v,j) in E and v<=z} union {q}).        (2)
```

The new complex consists of the subsets which contain no old facet. Thus
`h_E(z)` is exactly the largest allowed `j` in the fibre over `z`; after
discarding negative heights, the coordinatewise maximal fibre tops are the
facets of `D(E)=delta_NF(E)`.

Write `C` for the operation which discards a displayed type outside the box
(1) and then takes coordinatewise maximal elements. Every range below is an
integer range; an empty range contributes no terms.

## Prefix construction

The first four antichains are

```text
P_0 = {(0,0,0,2),(0,0,1,1),(0,2,0,0),(1,0,1,0),(1,1,0,0)},
P_1 = {(0,1,0,1),(0,1,1,0),(1,0,0,1)},
P_2 = {(0,0,1,q),(1,0,1,0),(1,k-1,0,0)},
P_3 = {(0,k-1,0,q),(0,k-1,1,q-1),(1,k-2,0,q)}.          (3)
```

For `4<=t<=k+2`, let `u=k-t+4` and define `P_t=C` of the following six
families:

```text
(0,i,0,q-(i-u))       for u<=i<=k-1,
(0,u-2,1,q),
(0,i,1,q-(i-u+1))     for u<=i<=k-1,
(1,i,0,q-(i-u+1))     for u-1<=i<=k-2,
(1,k-1,0,q-(t-3)),
(1,i,1,q-(i-u+3))     for u-3<=i<=k-1.                  (4)
```

These are formulas, not orbit data extracted separately for each width.

To verify the generic prefix transition, suppose `4<=t<=k+1`. Before
maximalization, direct substitution of (4) into (2) gives the following four
fibre-height rows:

| base | range of `i` | `h_(P_t)(a,i,b)` |
|---|---|---:|
| `00` | `i<u` | `q` |
| `00` | `i>=u` | `q+u-i-1` |
| `01` | `i<u-2` | `q` |
| `01` | `u-2<=i<u` | `q-1` |
| `01` | `i>=u` | `q+u-i-2` |
| `10` | `i<u-1` | `q` |
| `10` | `u-1<=i<=k-2` | `q+u-i-2` |
| `10` | `i=k-1` | `q-k+u-2` |
| `11` | `i<u-3` | `q` |
| `11` | `i>=u-3` | `q+u-i-4` |

Taking maximal tops gives exactly (4) with `u` replaced by `u-1`. Hence

```text
D(P_t)=P_(t+1)  for 4<=t<=k+1.                           (5)
```

The four initial substitutions and the exit from the prefix are

```text
P_0 -> P_1 -> P_2 -> P_3 -> P_4,
P_(k+2) -> A_(q-k+2).                                    (6)
```

For the exit calculation, the raw heights over bases `00,01,10,11` are,
respectively,

```text
00: q (i<2), then q+1-i;
01: q-1 (i=0,1), then q-i;
10: q (i=0), q-i (1<=i<=k-2), then q-k;
11: q-i-2.
```

Their maximal elements are the wave state defined next. These formulas
remain valid when `m=k`: the operation `C` performs exactly the coincident
upper/lower clipping.

## Diagonal wave

For a base `z=(a,i,b)`, define

```text
w_k(0,i,0) = k                  if i=0, else k-i-1,
w_k(0,i,1) = k-1                if i=0, else k-i-2,
w_k(1,i,0) = -2                 if i=k-1, else k-i-2,
w_k(1,i,1) = k-i-4.                                      (7)
```

For `1<=s<=q-k+2`, set

```text
A_s=C{(a,i,b,s+w_k(a,i,b)) : all bases (a,i,b)}.          (8)
```

The weights strictly decrease on every proper comparability of bases. If a
facet over `z` is in the box, it is therefore the least predecessor
threshold at `z`, and (2) lowers its height by one. Only four endpoint
events require attention:

- At the upper end, only bases `000` and `001` can exceed `q`.
- A temporary top over `000` is dominated by the top over `001`.
- At the lower end, only weights `-2` and `-3` can leave the box.
- The height-zero weight-`-2` facets make the weight-`-3` fibre negative.

Consequently

```text
D(A_s)=A_(s-1)  for 2<=s<=q-k+2.                         (9)
```

The upper index is nonempty because `q>=k-1`.

## Lower-bound tail

For `1<=r<=k-2`, define `R_r=C` of

```text
(0,0,0,r+2),        (0,r+2,0,0),
(0,i,0,r+1-i)       for 1<=i<=r,
(0,0,1,r+1),
(0,i,1,r-i)         for 1<=i<=r,
(1,i,0,r-i)         for 0<=i<=r-1,
(1,r+1,0,0),
(1,i,1,r-2-i)       for 0<=i<=r-2.                      (10)
```

Substitution in (2) gives

```text
D(A_1)=R_(k-2).                                           (11)
```

For `2<=r<=k-2`, the raw fibre heights of `R_r` are

| base | raw heights as `i` increases |
|---|---|
| `00` | `r+1` at `i=0`; `r-i` for `1<=i<=r`; `0` at `i=r+1`; then negative |
| `01` | `r` at `i=0`; `r-i-1` for `1<=i<=r-1`; then negative |
| `10` | `r-i-1` for `0<=i<=r-1`; `0` at `i=r`; then negative |
| `11` | `r-i-3` for `0<=i<=r-3`; then negative |

Maximalization removes the duplicated zero endpoints and gives

```text
D(R_r)=R_(r-1).                                           (12)
```

Finally, direct use of (2) in the seven-term state `R_1` gives

```text
D(R_1)=P_0.                                               (13)
```

At the transition (11), the only possible upper collisions are
`q=k-1`, `q=k`, and `q>=k+1`; applying `C` in these three cases yields the
same formula (10). This includes the square boundary `n=m`.

## Complete orbit and first isomorphic return

Equations (5)--(13) give the complete labelled orbit

```text
P_0,P_1,...,P_(k+2),
A_(q-k+2),A_(q-k+1),...,A_1,
R_(k-2),R_(k-3),...,R_1,P_0.                              (14)
```

The number of states before return is

```text
(k+3) + (q-k+2) + (k-2) = q+k+3 = k+m+2.                 (15)
```

There is no earlier return up to isomorphism. `P_0=B_(k,m)` contains a
triangle, whereas `P_1=K_(k,m)` minus the distinguished cross edge is
bipartite. Every state from `P_2` through `R_1` has a facet of size at least
three:

- `P_2` contains `(1,k-1,0,0)`.
- `P_3` contains `(1,k-2,0,q)`, and every `P_t` in (4) contains
  `(1,k-1,0,q-(t-3))`, whose size is at least `q+1=m>=3`.
- Every `A_s` contains `(0,1,0,s+k-2)`.
- `R_r` contains `(0,0,1,r+1)`.

Dimension and bipartiteness are isomorphism invariants, so (15) is the
NF-number.

## Reproduction

The checkers use CPython 3.10 or later and no third-party packages.

```sh
python3 verify.py --max-k 24 --extra-m 24
python3 independent_check.py --max-vertices 11
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected summaries are

```text
VERIFIED universal dumbbell orbit templates; 3<=k<=24; k<=m<=k+24; cases=550; states=22550; transitions=22550; NF(B_(k,m))=k+m+2
INDEPENDENT VERIFIED full Boolean-lattice dumbbell orbits; 3<=k<=m; k+m<=11; cases=12; states=134; facets_seen_with_multiplicity=11100; orbit_sha256=3abece6954a978ef0c73d219573cf4f9a883b5275afb27ae2cc5a127cc5148a8
```

`verify.py` implements the displayed parameterized templates and the exact
fibre update (2). It checks 22,550 individual transitions, including every
square collision boundary through `k=24`. `independent_check.py` imports no
templates or type quotient: it builds each small dumbbell from its labelled
edges and applies the defining Boolean-lattice operation to every subset.
The five unit tests separately exercise the square boundary, the required
width-five specialization, wave and tail recurrences, early-return invariant, and the
optimized maximal-element routine against its definition.

The universal conclusion rests on equations (2)--(14), not on the finite
regression ranges. There is no solver, floating point, randomness, generated
dataset, omitted search dump, or external certificate.

Exploratory exact type orbits at widths five through seven helped reveal the
templates (4), (7), and (10). They are discovery data, not proof: the
parameterized transition calculations above and the independent
Boolean-lattice implementation are the stated evidence.

## Width-two dependency and literature boundary

The width-two lemma and its independently checkable source are recorded in
Discovery Net as
`bafkreig2nb3pyrl3dbluvxp5olbmla25pnsznszu5dnfyqrsl3yjdisncm`.
The present construction independently covers all `n,m>=3`; only the final
all-width corollary depends on that earlier lemma.

- B. A. Rather, *The NF-operator and the NF-Numbers of Simplicial
  Complexes*, Conjecture 3.7,
  [arXiv:2605.30781](https://arxiv.org/abs/2605.30781), states the formula,
  derives the first two iterates, and reports finite checks only for
  `2<=n,m<=5`.
- T. Hibi and H. Mahmood, *The NF-number of a simplicial complex*,
  [arXiv:2005.01247](https://arxiv.org/abs/2005.01247), proves the analogous
  formula for the disjoint union of two cliques.

Targeted exact-formula, title, notation, and citation searches through
2026-09-04 found no proof of the full dumbbell conjecture. This is an
apparently-new-to-the-searched-sources statement, not a historical-priority
claim.
