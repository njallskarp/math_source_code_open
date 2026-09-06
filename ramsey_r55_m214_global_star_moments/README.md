# Complete triangle moments and global star identities still admit M214

The complete height-3367 \(M=214\) LP has an exact rational survivor even
after imposing all eight probability inequalities on every physical
triangle, every degree equation multiplied by an incident edge, and
codegree bounds in both colors. The repaired affine family is feasible
precisely for

\[
\frac{3}{14}\leq\rho\leq\frac{10}{39}.
\]

The preceding height-3367 family has no lift to this system: its fixed
coordinates violate 2,713 projected triangle consistency inequalities.
Thus the new system strictly strengthens the complete preceding LP, while
remaining feasible itself. There can be no valid LP/Farkas infeasibility
certificate for this stated strengthened relaxation.

These are rational pseudomodels. No Boolean root, whole M-slice or Ramsey
graph family is excluded, and no Ramsey-number bound changes.

## Complete stated formulation

Start with the [height-3367 reanchored moment
formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_reanchored_moment_hull).
Call it \(P_2\). It retains the complete height-3323 OPB and all subsequent
height-3341/3367 rows, totaling 98,758 variables and 3,270,228 constraints,
including 87 equalities. Every old variable is in \([0,1]\).
The base OPB has 2,983,003 rows and 511,537,255 bytes, with SHA-256

```text
9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609
```

In particular, all five-set constraints, triangle conjunctions and local
triangle totals, prescribed degrees, exceptional incidences, the complete
389-root selector interface, pair cells, scalar column hulls and reanchored
moment hulls remain present. This is the named cumulative formulation,
not the conjunction of every graph contribution.

For all 12,341 physical vertex triples, supply all three missed-pair moments
defined below. Of the 37,023 moments, 10,612 already occur in \(P_2\) and
are identified with its exact existing coordinates. The other 26,411 are
new variables. Add 98,728 triangle probability inequalities, 1,806 global
star equalities and 903 blue codegree inequalities. The new LP \(P_*\)
has **125,169 variables and 3,371,665 rows**, including **1,893 equalities**.
All variables have the usual \([0,1]\) box; the new moment boxes also
follow from the probability inequalities.

The pinned base OPB is regenerated and evaluated literally through EOF.
All suffix rows are evaluated from their exact physical definitions.
No expanded \(P_*\) OPB or digest of such a stream is claimed.

## One joint distribution for each physical triangle

For a triple \(a<b<c\), let its three red edge bits, in this order, be

\[
A=x_{ab},\qquad B=x_{ac},\qquad C=x_{bc}.
\]

Let \(z=z_{abc}=ABC\) be the existing red triangle variable, and define
the missed-pair moments at the three centers by

\[
m_a=(1-A)(1-B),\quad
m_b=(1-A)(1-C),\quad
m_c=(1-B)(1-C).
\]

In the linearized system write

\[
u=m_a+A+B-1,\quad v=m_b+A+C-1,\quad w=m_c+B+C-1.
\]

They represent \(AB,AC,BC\). The complete eight-state probability table,
where the bit mask uses bit 0 for \(A\), bit 1 for \(B\), and bit 2 for
\(C\), is

| Mask | Probability |
| ---: | --- |
| 0 | \(1-A-B-C+u+v+w-z\) |
| 1 | \(A-u-v+z\) |
| 2 | \(B-u-w+z\) |
| 3 | \(u-z\) |
| 4 | \(C-v-w+z\) |
| 5 | \(v-z\) |
| 6 | \(w-z\) |
| 7 | \(z\) |

Require all eight expressions to be nonnegative. They sum identically to
one and recover the stated edge, pair and triple moments by summing the
appropriate masks. Conversely any joint distribution on the eight edge
colorings gives these expressions by inclusion-exclusion. Therefore these
inequalities are exactly the convex hull of the Boolean moment vectors for
this triple. They require no root guard and are valid for every Boolean
graph. The old and new moments on every overlapping support share one
coordinate.

The local distribution statement concerns the three edges of a physical
vertex triangle. It does not assert joint consistency on every arbitrary
triple of edges or a joint distribution of entire graphs. The full
Sherali--Adams hierarchy is not imposed here.

## Global degree-weighted identities

For distinct vertices \(h,a\), multiply the existing prescribed degree
equation \(\sum_{b\ne h}x_{hb}=d_h\) by \(x_{ha}\), using Boolean
idempotence. After linearization this gives the global star identity

\[
\sum_{b\notin\{h,a\}}
\bigl(m_{\{a,b\},h}+x_{ha}+x_{hb}-1\bigr)
=(d_h-1)x_{ha}.
\]

There is one equality for each of the \(43\cdot42=1,806\) ordered pairs.
Here \(d_h=20\) for \(h\in\{2,\ldots,14\}\), and \(d_h=21\)
otherwise, exactly as in the old formula. These are necessary for every
Boolean graph with those degrees and use shared moments across entire
42-edge stars. No new symmetry or root-selection condition is introduced.

The complementary identity follows from the same equality and the old
degree equation:

\[
\sum_{b\notin\{h,a\}}m_{\{a,b\},h}
=(41-d_h)(1-x_{ha}).
\]

The checker verifies all 1,806 complementary identities as well, but they
are derived checks and are not counted again as additional LP rows.

Let \(b_{ijk}\) be the mask-zero probability above, the linearized blue
triangle indicator. Add, for every vertex pair,

\[
\sum_{k\notin\{i,j\}}b_{ijk}\leq13(1-x_{ij}).
\]

The 903 red counterparts \(\sum_k z_{ijk}\leq13x_{ij}\) are already in
\(P_2\). In a Boolean Ramsey graph the common neighborhood of a pair in
its edge color has no same-color triangle and no opposite-color five-set,
so has order at most 13 by \(R(3,5)\leq14\). If the pair has the other
color, every relevant triangle indicator is zero. The preceding package
includes the elementary proof of that small Ramsey upper bound; no core
catalog is required for these inequalities.

## Exact separation of the previous complete-LP family

On any triple with existing \(m_{\{a,b\},h}\), the joint triangle hull
implies, with \(W=m_{\{a,b\},h}+x_{ah}+x_{bh}-1\),

\[
z_{abh}\leq W,\qquad z_{abh}\geq W+x_{ab}-1.
\]

The first is nonnegativity of the state with both incident edges red and
the other edge blue. The second follows by summing the nonnegative states
with \(x_{ab}=0\) and at least one incident edge blue.

In the complete height-3367 survivor, the triple \((a,b,h)=(2,3,15)\)
has

\[
x_{2,15}=x_{3,15}=\frac6{13},\quad
m_{\{2,3\},15}=\frac7{26},\quad
x_{2,3}=\frac56,\quad z_{2,3,15}=0.
\]

Thus \(W=5/26\), and the lower inequality has exact slack

\[
0-\frac5{26}-\frac56+1=-\frac1{39}.
\]

All these coordinates are constant throughout the preceding affine
interval \([3/14,10/39]\). The entire family therefore lacks a feasible
joint triangle lift. Direct evaluation of both projected inequalities on
all 10,612 old missed coordinates finds **351 lower violations and 2,362
upper violations**. These are checks on a previously verified full-LP
survivor, not an isolated local point.

## The repaired survivor and global deficiency totals

Keep every old edge coordinate and the selector for root 48,
\((\mathtt{E8},13,0,\mathtt A)\). Its anchors are 0 and 1, its core is
\(H=\{15,\ldots,27\}\), and \(X=\{2,\ldots,42\}\setminus H\).
The fixed edge values are the 20 exact parameters from the pinned
predecessor source, together with its fixed stars and cyclic 13-core.

The compact `moment_atoms.json` specifies eight rational state masses for
171 deterministic weighted-triple templates. `witness.py` expands each
physical triple using its vertex types and ordered edge values. Ties are
resolved by the first permutation of the increasing triple. This is a
deterministic compression of one candidate, not a completeness or orbit
enumeration theorem. The checker does not use this compression.

The expanded masses supply the new triangle coordinates and all three
missed-pair moments. On the active core columns the missed-pair values
remain \(7/26,14/65,1/7\), according as the exterior pair has two, one,
or zero exceptional vertices. For active core/exterior pairs set

\[
q_{P,ij}=\rho x_{ij}m_{P,i}.
\]

For all other old \(q\) coordinates use
\(\min(m_{P,i},m_{P,j},x_{ij})\). This specifies all 125,169 coordinates.
The triangle and wedge moments are fixed throughout the family, and only
the 9,828 active red-core \(q\) coordinates vary with \(\rho\).

The exact checker verifies every \(P_*\) row at both endpoints. All
coordinates are affine in \(\rho\), so the interval between them is
feasible. The old pair-cell row for the blue pair \(\{2,14\}\) still
requires \(7\rho\geq3/2\), forcing the lower endpoint. For each active
red core edge the repaired moments give \(T=7\), \(S=5\), and
\(Q=78\rho\). The retained reanchored upper chord requires
\(78\rho\leq20\), forcing the upper endpoint. The interval is therefore
exact for this specified family.

The local red triangle totals are still 93 at the 13 degree-20 vertices
and 100 at the other 30. The new blue triangle probabilities give local
totals 105 at vertex 2, 107 at vertices 3 through 14, and 100 at every
other vertex. Using the inherited neighborhood extrema, all red
deficiencies equal seven, all blue deficiencies equal seven except nine
at vertex 2, and their sums are exactly 301 and 303. Thus the two global
deficiency totals and all 86 local caps coexist with the new moment and
star constraints. This is an expectation-level realization, not actual
neighborhood graphs.

## Reproduction and evidence

Use Python 3.11 or newer with its standard library, in a checkout containing
the pinned predecessor directories. CPython 3.12.12 was used.

```sh
python3 -B ramsey_r55_m214_global_star_moments/test_validate.py
python3 -B ramsey_r55_m214_global_star_moments/reproduce.py \
  /tmp/m214-global-star-run
```

The work directory must be new and outside the public repository. Allow
1.2 GB of temporary disk space. The reproducer first regenerates and
fully checks the preceding LP and its original survivor, then generates
the new vectors and checks every retained row and every new constraint.
The final output must equal `EXPECTED_RESULT.json`. The full common
denominator used by the exact check is 1,788,696,000. Generated formulas,
expanded vectors, solver files and logs stay outside version control.

`validate.py` imports no new producer, discovery LP, solver or compact
template table. It explicitly reuses the SHA-pinned predecessor OPB
parser, physical decoder and suffix checker. These reused components are
not claimed as independently rewritten. It checks new moments by physical
vertex keys, inverts them to all eight triangle masses, evaluates every
global star, and sums blue triangle probabilities directly. The original
separating point is pinned by its exact vector hash and is fully checked
by the predecessor stage of the end-to-end command.

The small controls use direct definitions to check 330 rational atom
distributions, 1,099 complete small graphs, 21,300 ordered star identities,
10,504 triangle projections and six malformed-stream rejections. Normal
and optimized controls agree. The original 20 edge parameters are not
trusted as feasible merely because they came from an older source; the
complete literal OPB evaluation checks their feasibility again.

Optional discovery uses SoPlex 8.0.3, GMP 6.3.0. The 1,368-variable
reduced system has 4,389 rows. Its reconstruction checks every row and
box exactly; solver status alone is not evidence for the full LP.

```sh
python3 -B ramsey_r55_m214_global_star_moments/derive.py --lp /tmp/star.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 \
  --int:ratfac_minstalls=0 --bool:ratfacjump=true \
  --real:feastol=1e-30 --real:opttol=1e-30 \
  --real:fpfeastol=1e-30 -s0 -g0 -v3 -t60 -X=/tmp/star.sol /tmp/star.lp
python3 -B ramsey_r55_m214_global_star_moments/derive.py \
  --solution /tmp/star.sol --output /tmp/moment_atoms.json
```

A different solver version can select another feasible table. The compact
published table, rather than a particular discovery trajectory, is the
certificate for the solver-free reproduction command.

## Context, scope and next falsifiable test

Graph selection began at indexedHeight 3382 from the supplied Ramsey
problem, with 556 nodes from 30 signers in its three-step neighborhood.
The newest principal report recommended global shared-variable coupling.
R2's dense five-separator classification and H* extensions, r3's two-color
pair coverage/composition, and the peer's global connectivity theorem are
separate work. In particular, the new two-color cover is not silently
conjoined with the old red-only selector normalization.

Dependencies include the local deficiency identity and its review at
2099/2285; M214 specialization 2127; root cover 3148; selector formula
3160 and semantic reproduction 3170; footprints 3228/3254; pair lift
3274; scalar hull 3323; coupled-column bound 3341; and the repaired
reanchored hull 3367. The 3170 reproduction does not independently review
its author's upstream coverage proof. At the initial cutoff, 3274, 3323,
3341 and 3367 still had no committed incoming external review. This new
certificate is also author-checked, not externally reviewed or formalized.

The network's earlier one-vertex Sherali--Adams visibility result at 783
concerns a different fixed 42-core extension system. Generic probability
atom hulls and degree multiplication are standard methods, as in
[Sherali, Adams and Driscoll](https://pubsonline.informs.org/doi/10.1287/opre.46.3.396).
The [Angeltveit--McKay primary paper](https://arxiv.org/abs/2409.15709v2)
provides Ramsey LP and complete edge-gluing context. These primary sources
were checked after graph-grounded target selection. No historical-priority
claim is made for the method or its elementary identities.

Trust remains in the written reductions and moment proof, the disclosed
reused coordinate/checking code, exact Python arithmetic, hashing and
hardware. Catalog completeness is inherited when interpreting the
hard-branch reduction, not for the literal feasibility check or new
Boolean identities. No solver, discarded exploratory state or omitted
large certificate is needed for verification.

Covered: every row of \(P_*\) over the complete 389-root selector union,
with the witness selecting root 48; strict exclusion of the entire stated
old rational family. Uncovered: Boolean feasibility of any root, other
M-slices, low deficiency, the separate third-anchor suffix, arbitrary
higher edge moments, and the general order-43 problem.

The next falsifiable target is joint consistency between the old
\(q_{P,ij}\) coordinates and the triangle atoms on their four-vertex
supports, retaining the complete current LP. Require an exact separator,
survivor or complete-family certificate. Repeating triangle facets or
degree-star rows is exhausted by this survivor. After two consecutive
passes with only incremental rows and no stated milestone, pivot to the
next principal-ranked exact target.
