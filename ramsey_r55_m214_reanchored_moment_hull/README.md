# Reanchored moments cut the M214 survivor and admit an exact repair

A shared-coordinate moment identity strictly strengthens the complete
height-3341 \(M=214\) LP. Its guarded integer hull cuts off the **entire
previous rational survivor interval** \([3/14,6/13]\). Changing only the
triangle coordinates gives a new exact affine survivor family, feasible
precisely for

\[
\frac{3}{14}\leq\rho\leq\frac{10}{39}.
\]

The new family satisfies every old constraint, all 264,560 new guarded
moment-hull rows, and all 903 universal red-edge codegree bounds. Thus this
strengthened full LP is feasible and cannot have a valid LP/Farkas
infeasibility certificate. This is a rational pseudomodel, not a Ramsey graph
or a Boolean satisfying assignment. No Boolean root is excluded and no
Ramsey-number bound changes.

## Precisely which relaxation is covered

Let \(P_0\) be the LP relaxation of the [height-3323 full
formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_column_hull).
It has 98,758 variables in \([0,1]\), 2,983,003 rows including 87 equalities,
and the 511,537,255-byte generated OPB SHA-256

```text
9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609
```

Its rows include both five-set inequalities, triangle conjunctions and local
triangle totals, prescribed degrees, exceptional incidences, the complete
389-root selector interface, footprints, shared pair cells and scalar column
hulls. Let \(P_1\) add all 21,762 [height-3341 coupled-column
bounds](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_coupled_column_separator).
Let \(P_2\) add the 264,560 moment rows and 903 codegree rows defined below.
There are 3,270,228 total rows in \(P_2\), with no additional variables.

The complete base OPB is regenerated and checked literally. The extra rows
are defined by the displayed formulas and evaluated directly over every
physical root and core pair; no expanded \(P_2\) OPB or digest is claimed.
*Complete* means these specified formulations, not the convex hull of Ramsey
graphs or the conjunction of every network contribution. The separate
third-anchor quotient is not included as an additional LP suffix.

## The shared-coordinate identity

Suppose an order-43 graph in the intrinsic \(M=214\) branch selects a red
anchor edge \(uv\). Let \(H=N_R(u)\cap N_R(v)\), \(c=|H|\in\{9,\ldots,13\}\),
and \(X=V\setminus(\{u,v\}\cup H)\), with \(n=41-c\).
For distinct \(i,j\in H\), write \(d_i,d_j\in\{20,21\}\) for their
prescribed total red degrees and

\[
a_i=\sum_{h\in H\setminus\{i\}}x_{ih},\qquad
T_{ij}=\sum_{z\in X}z_{ijz},\qquad
Q_{ij}=\sum_{P\in\binom X2}q_{P,ij}.
\]

The existing Boolean coordinates have meanings

\[
z_{ijk}=x_{ij}x_{ik}x_{jk},\qquad
m_{\{z,z'\},i}=(1-x_{zi})(1-x_{z'i}),\qquad
q_{P,ij}=x_{ij}m_{P,i}m_{P,j}.
\]

When \(ij\) is red, inclusion-exclusion for its exterior red neighborhoods
gives its number of common blue exterior neighbors as the existing affine
expression

\[
S_{ij}=45-c-d_i-d_j+a_i+a_j+T_{ij}.
\]

Indeed, the two exterior red degrees are \(d_i-2-a_i\) and
\(d_j-2-a_j\), and their intersection has order \(T_{ij}\).
Counting pairs of common blue exterior neighbors now gives the exact bridge

\[
Q_{ij}=\binom{S_{ij}}2.
\]

The common red neighborhood of any red edge is a triangle-free graph with
independence number at most four, so has order at most 13. The elementary
proof of \(R(3,5)\leq14\), independent of catalogs, is given in the
height-3341 source. Both anchors are common red neighbors of \(i,j\), hence
\(T_{ij}\leq11\). Also \(H\) is triangle-free with independence number
at most four, giving \(a_i,a_j\leq4\). Consequently

\[
0\leq S_{ij}\leq K_{ij}:=64-c-d_i-d_j\in\{9,\ldots,15\}.
\]

The exact convex hull of \((s,\binom s2)\) for integer \(0\leq s\leq K\)
is

\[
Q\geq rS-\binom{r+1}{2}\quad(0\leq r<K),\qquad
2Q\leq(K-1)S.
\]

The lower edges join successive integer points and the upper edge joins
the two endpoints. The inequalities also imply \(0\leq S\leq K\).
These familiar binomial hull facets are not claimed as historically new.
The strengthening comes from substituting shared edge and triangle
coordinates for \(S\), instead of using only its coarse upper bound.

## Guards and complete finite scope

For a root selector \(y\), put \(x=x_{ij}\), \(C=45-c-d_i-d_j\),
\(p=\binom{41-c}{2}\), and \(K=64-c-d_i-d_j\). Add

\[
Q-rS+\binom{r+1}{2}+g_r(2-y-x)\geq0,
\qquad g_r=r(84-d_i-d_j)-\binom{r+1}{2},
\quad 0\leq r<K,
\]

and

\[
(K-1)S-2Q+g_U(2-y-x)\geq0,
\qquad g_U=-(K-1)C+2p.
\]

For \(y=x=1\) these are the active hull. Otherwise one of the Boolean
activation coordinates is zero. The variable box gives
\(C\leq S\leq C+c+39\) and \(0\leq Q\leq p\), since
\(a_i+a_j\) has coefficient sum \(2(c-1)\), including \(x_{ij}\)
twice, and \(T\) has \(41-c\) terms. The displayed nonnegative guards
therefore make every inactive inequality valid throughout that box.
This proves validity for every Boolean Ramsey graph covered by the old
encoding. It also makes every row with \(y=0\) harmless throughout the
fractional box, irrespective of \(x\).

Enumerating all 389 roots and all their core pairs gives 264,560 rows. In
addition, for every one of the 903 vertex pairs add the valid bound

\[
\sum_{k\notin\{i,j\}}z_{ijk}\leq13x_{ij}.
\]

For a red edge this is the common-red-neighborhood bound just proved. For
a blue edge its triangle coordinates vanish. This standard codegree bound
is included in the repaired full LP; it is not a novelty claim.

## Strict separation of the previous full-LP family

The height-3341 family selects zero-based root 48,
\((\mathtt{E8},13,0,\mathtt A)\), with anchors 0 and 1,
exceptional set \(E=\{2,\ldots,14\}\), and core \(H=\{15,\ldots,27\}\).
Its red core is cyclic with differences \(\{1,5,8,12\}\) modulo 13.
Each core vertex has internal red degree four and total red degree 21.
For each of its 26 red core edges the old triangle table gives

\[
T_{ij}=3,\qquad S_{ij}=-10+8+3=1,\qquad Q_{ij}=78\rho.
\]

Here \(K=9\), so the new upper chord requires \(156\rho\leq8\),
or \(\rho\leq2/39\). The entire old \(P_1\)-feasible interval
\([3/14,6/13]\) is therefore excluded. At its lower endpoint the 26
violated hull rows each have exact slack

\[
8-\frac{234}{7}=-\frac{178}{7}.
\]

The old point independently violates 182 of the new codegree rows.
The checker verifies that this baseline really satisfies every \(P_1\)
row, so the separator is against the complete previous relaxation.

## An exact repaired full-LP family

Keep all old edge coordinates, all missed-pair coordinates and the same
affine \(q\)-coordinate convention. For the active columns the missed
values are \(7/26\), \(14/65\), and \(1/7\), according as an exterior
pair contains two, one, or zero exceptional vertices. They sum to 78 in
every column. For an active red core edge use \(q_{P,ij}=\rho m_{P,i}\);
the 9,828 such coordinates are the only ones that vary with \(\rho\).
All remaining coordinates follow the pinned predecessor producer.

Replace only the triangle coordinates by the 171 exact class values in
`triangle_orbits.tsv`. Their SHA-256 is

```text
9b3fc0b002ee2963c51e0159900d8fb9ebb66d3c6c0ed45c6e300e08c1900deb
```

This table gives \(T_{ij}=7\), and hence \(S_{ij}=5\), at every active
red core edge. The new upper chord becomes \(78\rho\leq20\), forcing
\(\rho\leq10/39\). The old row for the blue exterior pair \(\{2,14\}\)
has missed cardinality \(7/2\) and induced-red-edge moment \(7\rho\),
so requires \(7\rho\geq7/2-2=3/2\), forcing \(\rho\geq3/14\).

The exact checker verifies every row of \(P_2\) at both these endpoints.
Every coordinate is affine in \(\rho\), so all intervening points are
feasible. The two necessary bounds prove that the interval is exact for
this specified family. This does not classify all feasible points of
\(P_2\) or assert feasibility of each of the other 388 roots separately.
No joint distribution of whole graphs is asserted.

## Reproduction and trust boundary

CPython 3.12.12 was used; Python 3.11 or newer with its standard library is
sufficient. From a checkout containing the predecessor directories:

```sh
python3 -B ramsey_r55_m214_reanchored_moment_hull/test_check.py
python3 -B ramsey_r55_m214_reanchored_moment_hull/reproduce.py \
  /tmp/m214-reanchored-moment-run
```

The work directory must be new and outside the repository. Allow 1.2 GB
of temporary disk space. The pinned predecessor reproducer regenerates
and verifies \(P_0\) and \(P_1\); then the new producer expands the compact
table to three full vectors and the checker verifies the complete base
stream and all added rows. The final output must equal `EXPECTED_RESULT.json`.
The common exact scaling denominator is 44,717,400. Formula streams,
expanded vectors, discovery LPs and solver outputs remain local generated
state and are not published.

For a previously generated base OPB, the equivalent direct check is:

```sh
python3 -B ramsey_r55_m214_reanchored_moment_hull/witness.py \
  --output /tmp/m214-reanchored-points.tsv
python3 -B ramsey_r55_m214_reanchored_moment_hull/check.py \
  --vector /tmp/m214-reanchored-points.tsv --opb /path/to/m214-3323.opb
```

`check.py` imports neither the witness producer nor a solver. It explicitly
reuses the SHA-pinned `physical_maps()` decoder from the height-3341 verifier;
it does not claim an independently rewritten physical decoder. Its own
generic OPB parser uses arbitrary-precision integer arithmetic, reads every
row through EOF, and verifies byte count, row and equality counts, and hash.
New inequalities are evaluated directly from decoded vertex sets. Small
controls cover 195 integer hull vertices, 180 inactive box corners, 5,461
common-neighbor identities, 125 comparisons with Fraction arithmetic, and
six malformed-row rejections. These controls support the checker; the
universal validity argument is the proof above.

The compact triangle repair was discovered with SoPlex 8.0.3, GMP 6.3.0,
using a 171-variable LP with 11 equalities and 903 codegree inequalities.
Reconstruction and full verification use exact rational arithmetic, and
verification has no solver dependency. Optional discovery reproduction is:

```sh
python3 -B ramsey_r55_m214_reanchored_moment_hull/derive.py --lp /tmp/repair.lp
soplex --readmode=1 --solvemode=2 --int:checkmode=2 \
  --int:ratfac_minstalls=0 --bool:ratfacjump=true \
  --real:feastol=1e-30 --real:opttol=1e-30 \
  --real:fpfeastol=1e-30 -s0 -g0 -v3 -t60 -X=/tmp/repair.sol /tmp/repair.lp
python3 -B ramsey_r55_m214_reanchored_moment_hull/derive.py \
  --solution /tmp/repair.sol --output /tmp/repaired-triangle-orbits.tsv
```

Different solver versions may select different feasible tables. Solver status
alone establishes none of the full-LP claims. The published table is the
certificate checked by the solver-free command.

## Graph context, review and limits

Selection began at indexedHeight 3358 from the supplied Ramsey problem,
traversing 549 nodes from 30 signers. The newest principal report recommended
full-LP coupling followed by different-anchor or two-color coupling. The
dense-core structural classification at heights 3349/3355 and the M215
partition at 3343 are separate lanes. No absence beyond the indexed cutoff
was inferred.

The source dependencies are local deficiency 2099, independently reviewed
at 2285; the M214 specialization 2127; complete roots 3148; selector formula
3160 and its semantic reproduction 3170; footprints 3228/3254; pair lift
3274; scalar column hull 3323; and the complete LP survivor at 3341.
The 3170 reproduction does not independently review its author's upstream
cover. At initial inspection, 3323 and 3341 had no committed external review.
This result is an author-checked exact certificate with an unformalized
validity proof, not external review or a proof-assistant theorem.

After graph-grounded target selection, the [Angeltveit--McKay primary
paper](https://arxiv.org/abs/2409.15709v2) was checked for literature context.
It proves \(R(5,5)\leq46\), using edge-based gluing, subgraph identities
and LP bounds. No priority claim is made for common-neighbor counting,
red-edge codegree bounds, or the scalar binomial hull.

Trust remains in the displayed mathematical reductions and proof, the pinned
physical coordinate conventions, exact Python arithmetic, SHA-256 and
ordinary hardware. Catalog completeness is inherited for interpretation of
the hard-branch reduction; the new counting identity and literal LP
feasibility check use no catalog enumeration.

Covered: every row of \(P_2\) over the complete 389-root selector union,
with the rational witness selecting root 48; strict exclusion of the entire
specified old \(P_1\) affine family. Uncovered: Boolean feasibility, other
M-slices, the deficiency-at-most-six branch, and the general order-43 problem.

The next falsifiable milestone is a strict full-LP separator or exact
survivor after adding joint triangle/footprint consistency or a further
global reanchoring identity. Repeating this hull or its scalar projections
cannot close this relaxation. After two consecutive passes with only
incremental rows and no strict separator, survivor or complete-family effect,
declare that mechanism exhausted and select the next principal-ranked target.
