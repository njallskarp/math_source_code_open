# Twenty distinct hub charges survive every low-deficiency scalar cell

**This is an exact counterexample to an incidence relaxation's sufficiency,
not a Ramsey graph or a claim that any physical extension cell is feasible.**

Every one of the 189 scalar cells in the complete low-deficiency cover admits
the allocation defined below. Each allocation has **20 additional dense
order-22 anchors of interface type 8**, assigned to **20 distinct degree-23
hubs**, each paying deficiency nine. All 86 local deficiencies are integral;
the exact global Goodman identity, both triangle divisibilities, global
handshaking, individually graphical neighborhood-degree lists, exact pointwise
neighbor-degree sums, the selected root's high-codegree condition and all stated hub-incidence restrictions hold.

Thus these necessary conditions exclude **zero scalar cells**, even with
substantial positive demand. No new lower-density catalogue or solver run is
used. Twenty is the size of this construction, not an optimality claim.

## The exact relaxation

Fix a red root edge $uv$ and relabel $u=0,v=1$. Write $d=d_R(u)$,
$p=d_R(v)$ and $q=|N_R(u)\cap N_R(v)|$. The imported complete cover is

$$
18\le d,p\le24,\qquad q_0(d)\le q\le13,
$$

where, in degree order 18 through 24,

$$
U=(85,92,100,107,114,122,132),\qquad
q_0=(9,10,10,10,10,11,11).
$$

Here $U(k)$ is the maximum number of edges in a $(4,5;k)$ graph.
The root has red deficiency at most six. The four cells on the other
41 vertices have sizes

$$
(q,\ d-1-q,\ p-1-q,\ 43-d-p+q). \tag{1}
$$

An allocation consists of 43 red degrees $D_i$, 86 deficiencies
$\delta_{i,c}$, 86 **anonymous local degree lists** $L_{i,c}$, and two
maps recording dense anchors, their hub labels and interface indices, plus
43 separately selected red neighbor sets $S_i$.
The lists are multisets of degrees inside a neighborhood; their entries
are not identified with a common set of physical neighbor labels.
The checker imposes exactly the following requirements.

1. $18\le D_i\le24$, $D_0=d,D_1=p$, and $D$ is graphical. Blue degree
   is $42-D_i$. Equation (1) is exact and every cell size is nonnegative.
2. For each color-side of order $n$, the deficiency is an integer in
   $[0,U(n)]$. Its list has length $n$, entries between $\max(0,n-18)$
   and 13, sum $2(U(n)-\delta)$, and is graphical. At order 22,
   deficiency at most five forces minimum local degree at least five;
   deficiency at most four forces minimum at least six.
3. The root red deficiency is at most six. Both endpoint red lists contain
   $q$, expressing reciprocity for the selected pair. Every side with
   deficiency at most six has at least
   $(3,1,2,4,5,1,4)_n$ entries at least $q_0(n)$.
4. Put $E_c=\sum_i(U(d_c(i))-\delta_{i,c})$. Require
   $E_R\equiv E_B\equiv0\pmod3$ and

   $$
   2(E_R+E_B)=6\binom{43}{3}-3\sum_iD_i(42-D_i). \tag{2}
   $$

5. A dense anchor is detected exactly when its color degree is 22, its
   deficiency is at most five, and its local list contains five.
   It must have deficiency five and a unique occurrence of five.
   Every such anchor is marked, its list is the degree multiset of its
   declared member of the complete thirteen-interface list, and its hub
   is a different vertex of color degree at most 23. The hub's local
   list must also contain five, and the anchor-hub pair has that color.
6. Each hub of color degree at least 21 has at most one marked preimage.
   At degree 19 or 20 it has at most four; pairs in that fiber have the
   opposite color. All prescribed pair colors, including the root edge,
   must be consistent. No further capacity is imposed at degree 18.
7. For a degree-23 image, the pointwise gap by interface index is

   $$
   (7,7,7,7,7,\text{forbidden},9,9,9,7,7,7,7).
   $$

   The deficiency sum over all degree-23 vertices in each color must
   also dominate the sum of charges of the anchors mapped to them.
   Thus the explicit additive inequality $\sum_{d_c=23}\delta_c\ge7a_c+2t_c$
   holds, with $t_c$ counting type-62 anchors.

8. The set $S_i$ has $D_i$ distinct labels other than $i$. It includes
   every prescribed red neighbor and excludes every prescribed blue neighbor.
   With $m=\frac12\sum_iD_i$ and $e_{i,c}=U(d_c(i))-\delta_{i,c}$, impose

   $$
   \sum_{w\in S_i}D_w=m+e_{i,R}+e_{i,B}-\binom{42-D_i}{2}. \tag{4}
   $$

   The checker uses the unsimplified edge partition: define
   $X_i=\sum_{w\in S_i}D_w-2e_{i,R}-D_i$, require $X_i\ge0$, and check
   $m=e_{i,R}+X_i+\binom{42-D_i}{2}-e_{i,B}+D_i$.
   These are pointwise selections. Except for prescribed pairs, $j\in S_i$
   is not required to imply $i\in S_j$; $L_{i,R}$ is not matched to the
   labels in $S_i$. Their root-row intersection is not constrained to $q$.

The additive condition in item 7 is redundant given individual charges, distinct images
and nonnegative deficiencies; retaining it makes the intended composition
explicit. An anchor can also be a hub. The general checker permits the
inherited degree-22 two-cycle possibility and does not impose the special
matching-shaped map used by our witnesses.

**What is omitted.** Lists at different vertices need not share physical
adjacency bits. The neighbor sets in item 8 need not be reciprocal or realize
the declared root intersection. Unmarked local lists need not admit a $(4,5)$ realization;
graphicality alone is required. Their selected common-core isomorphism types,
all unrecorded codegree reciprocity, mixed five-set constraints and the
actual joint embedding of marked interface graphs are not imposed. These
are deliberate boundaries of this exact relaxation, not properties of
Ramsey graphs. No 903-edge coloring is present in an allocation.

## Why this covers every claimed scalar branch

Let an actual $(5,5)$-good graph on 43 vertices have a color-side with
$\delta\le6$. The reviewed pair-root theorem selects a neighbor with
$q\ge q_0(d)$; its degree lies in 18 through 24. Relabel this chosen color
red and the two vertices 0 and 1. Take its actual degrees, actual local
edge deficiencies and actual neighborhood-degree multisets. These are
individually graphical, have the stated Ramsey degree bounds, and satisfy
(1), (2), triangle divisibility and the high-partner multiplicity bound.

The reviewed dense-neighborhood theorem supplies a unique local degree-five
vertex and one of thirteen types whenever an anchor is detected. Record
that vertex's physical global label as its hub. The shared-hub theorem gives
the fiber restrictions; the earlier complete consumers give the gap rules.
Actual edges cannot give conflicting prescribed pair colors. Set
$S_i=N_R(i)$. Summing the global degrees of its vertices gives
$2e_{i,R}+X_i+D_i$, where $X_i$ counts edges from $S_i$ to the vertices
outside $S_i\cup\{i\}$. The global edge partition gives (4).
Hence every actual graph in each claimed cell maps to an allocation satisfying every
listed requirement. No canonical labeling or graph symmetry is assumed.

The construction imposes twenty extra demands to make a stronger test of
feasibility. Those demands are **not** claimed to be forced by an actual
graph. A witness satisfying the extra demands is, in particular, a witness
for the weaker projected system in that cell.

The 18,767 coarse root labels add the common $(3,5;q)$ isomorphism type.
Their imported counts are $(290,313,105,12,1)$ for $q=9,\ldots,13$.
Since this relaxation retains only the order $q$, each scalar allocation
can carry any corresponding coarse label. This is an unused-label lift,
not an embedding or proof that any of those physical coarse families
extends. The substantive claim concerns all 189 scalar cells.

## Uniform exact construction

For every scalar key $(d,p,q)$ put

$$
k=\begin{cases}20&d+p\text{ even},\\21&d+p\text{ odd},\end{cases}
\qquad D=(d,p,k,22^{20},23^{20}).
$$

The degree sum is even. Vertices 3 through 22 are the twenty anchors;
vertices 23 through 42 are their hubs. Map $i$ to $i+20$, with every
interface index equal to 8. The first three vertices remain outside
these twenty pairs.

Set the red deficiencies to

$$
\delta_R=(6,6,6+j,5^{20},9^{20}),\qquad
j=\left(\sum_iU(D_i)-298\right)\bmod3. \tag{3}
$$

Let $n_s$ count degree $s$ and put

$$
\Omega=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}),\qquad
\Delta=(1247-\Omega)/2.
$$

Over the complete 49 ordered pairs $(d,p)$, this is integral and
$451\le\Delta\le472$. The red deficiency sum is $298+j$, so the remaining
blue budget $B=\Delta-298-j$ lies in $[151,173]$.

Start every blue deficiency at three. Begin with the vertex order
$(3,4,\ldots,42,0,1,2)$ and move each of vertices 0 and 1 having red degree
18 to its front, in increasing label order. Add $B-129$ units successively
in this cyclic order. All blue deficiencies are
between three and five; when a second circuit is needed, only vertex 3
gets five, and its blue degree is 20. In particular no unintended blue
dense anchor is introduced. The 49 budget rows are in `expected.json`.

Equation (3) makes $E_R$ divisible by three. The exact Goodman formula and
even degree sum make $E_R+E_B$ divisible by three, so $E_B$ is too. The
independent checker evaluates the original identity (2), not the producer's
simplified $\Omega$ formula.

Each anchor receives the exact degree multiset of the compact interface-8
record in `parameters.json`. Each hub receives a list of order 23 with
one entry five, twenty-one entries ten and one entry eleven. Its sum is
226, giving 113 local edges and deficiency nine. This is a degree list,
not a claim of a Ramsey realization of that hub neighborhood.

The other lists are balanced around their required average. At the two
selected red endpoints, reserve one entry $q$ and balance the remaining
entries. For a list of length $n$ and sum $s$, with reserved entry $h$ if
needed, write $s-h=a(n-1)+b$ and use $b$ entries $a+1$ and the remaining
entries $a$; without a reserved entry use $s=an+b$. The constructor
produces a literal simple-graph realization of every list by degree removal
and checks the resulting degrees. A separate checker tests all
Erdős–Gallai inequalities. The global degree vector is checked both ways.
No realization produced in this step is asserted to be Ramsey-good or
compatible with any other realization.

For item 8, an exact cardinality subset-sum construction selects the
required number of other labels with the target degree sum in (4), after
including the prescribed partner. All 8,127 rows are saved in their
respective generated certificates and checked by literal sums and edge
partitions. The checker does not rerun the subset-sum algorithm.
Prioritizing degree-18 roots in the blue budget is needed: without it,
for $(d,p)=(18,18)$ the first root needs a sum of 392 from its 17 remaining
neighbors, whose degrees are at most 23, giving maximum 391. Increasing
that root's blue deficiency by one removes this obstruction. This repair
preserves both global deficiency totals and triangle divisibilities.

Every anchor has deficiency five, every marked hub has deficiency nine,
and the map has twenty distinct images. The red charge is therefore 180.
There are no blue marked anchors. For example, the key $(18,18,9)$ has
$k=20,j=0,\Delta=451$, red sum 298 and blue sum 153. `allocation.json`
is its complete compact certificate.

## Reproduction and independent checks

With Python 3.10 or newer and its standard library, from this directory:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
python3 -B verify.py allocation.json parameters.json
python3 -B construct.py 22 23 13 > /tmp/low-cell-allocation.json
python3 -B verify.py /tmp/low-cell-allocation.json parameters.json
```

Expected statuses are `VERIFIED_ALL_189_LOW_CELL_CHARGE_SURVIVORS` and
`VERIFIED_EXACT_INCIDENCE_ALLOCATION`. `expected.json` includes all 49
budget rows, the full ordered allocation-stream SHA-256, counts and scope.
`VALIDATION.json` records the tested interpreter and fresh replay timings.
No network, solver or private file is needed for reproduction.

`verify.py` imports no constructor or parameter definitions. It reads only
the certificate and the thirteen graph6 strings supplied as explicit input;
it reconstructs their degrees with a different decoder and directly checks
all their red four-sets and blue five-sets. It does not import the producer's
values of $U$, gap vector or threshold table. Those mathematical premises
are separately stated below.

Two enumerations of the complete scalar domain agree entry for entry:
the producer uses the threshold table; the verifier ranges over all
integer triples and checks $dq\ge2(U(d)-6)$. Every generated certificate
is checked individually. All 16,254 local degree lists and 189 global
degree lists have constructive realizations and independent inequality
checks. There are also 8,127 exact pointwise neighbor-row certificates.
A nonroot label reversal is checked in every scalar cell, without
assuming it is a graph automorphism. Degree removal and degree inequalities
also agree on all 2,353 sorted candidate degree words through order seven.

Twenty-one deliberate corruptions are rejected. They include a missing
cell, wrong partition, odd global sum, failed triangle congruence, altered
Goodman budget, a nongraphical local list preserving its sum and pinned
$q$, an omitted anchor, a hub collision, a forbidden star image, and a
pointwise gap violation preserving the total charge, invalid neighbor rows,
a changed neighbor sum, and a missing prescribed partner at unchanged sum.
Normal and optimized Python must match every output field. Hashes record identities; they do not
replace the fresh definition-level checks.

## Imports, novelty and the remaining condition

The projection into this relaxation imports:

* $U(18..24)$ and the global degree/deficiency identity from h2099,
  independently accepted h2285.
* The [complete pair-root cover](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_low_deficiency_pair_roots),
  h2775, source `e7b42f40dbdc36a7e13d21faf1fb720e7845b4bf`.
* The [thirteen dense interfaces](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
  h3349, accepted h3355. The compact graph6 inputs are copied from the
  [dense-hub package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree23_hub_classification),
  source `590bcae0fe01e88e0a8fcf8030fbb2524973e4cb`; their parent input
  hash is pinned in `parameters.json`.
* The [uniform gap theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree_five_hub_gap),
  h3607, accepted h3631, and the type-62 density-114 consumers
  h3653, h3695 and h3723. The [interface-8 consumer](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface8)
  at source `ea9d87a2552b2b6147d4b702aadd54f2674da271` was independently
  accepted at h3743 for its intrinsic interface-8 scope. The full vector
  also uses interface 7, independently accepted at h3753; the intrinsic
  interface-6 consumer h3653 remains externally unreviewed. All our witnesses
  use only interface 8; the feasibility calculation needs no assertion
  that their marked neighborhoods occur together in a graph.
* The [shared-hub injection and fiber theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_shared_hub_injection),
  h3741, source `68e8a5118e93d7f3e01491f6d42d2b8a84b88b12`, external
  review pending at intake 3754.

Completeness of upstream catalogues and earlier physical exclusions is
imported for the projection, not re-established by checking representatives.
Existence of these arithmetic allocations is a direct exact calculation;
it does not depend on those catalogue-completeness assertions being true.
The numerical constants define the tested system in either case.

Primary literature was checked after graph-first selection at
[Angeltveit–McKay](https://arxiv.org/html/2409.15709v2) and
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Neighborhood-density linear programming and pointed gluing are established.
The limited search found no matching all-cell twenty-charge construction;
no historical priority or new general relaxation method is claimed.

The new evidence is author work with an independent implementation, not an
external peer verdict or a formal proof-assistant build. Trust lies in the
explicit definitions and constructor, exact Python semantics, the displayed
projection, imported premises where stated, hashes and ordinary hardware.

**Conclusion for this mechanism.** Additive hub charges plus the listed
scalar and anonymous local-degree conditions cannot exclude any of the
189 scalar cells. This remains true after twenty positive gap-nine demands
are imposed. It does not show that every stronger incidence model fails.
The missing step is a constraint tying these local counts to shared physical
vertices and edges, or enforcing local Ramsey/common-core realizability.
This gap is explicit in the saved $(18,18,9)$ allocation: its individually
valid sets $S_i$ have 400 unordered pairs with asymmetric membership, and
$|S_0\cap S_1|=17$ although $q=9$. Thus these particular row certificates
cannot be neighborhoods of one graph. This does not rule out different,
compatible selections with the same scalar data; that is a separate
mathematical question.
Any proposed strengthening must be stated explicitly and tested against the
saved allocations; merely reordering this test cannot change the result.

No physical family, whole low-deficiency branch, hard $M$-slice or Ramsey
bound is closed. Freeze this exact scalar mechanism. The next milestone is
a new necessary condition violated by these allocations, with a proved
projection and complete-family consumer, selected against refreshed
principal direction. The frozen H-star computation, r1's Boolean root-377
fallback and peer cut-rank families are not reopened or duplicated.
