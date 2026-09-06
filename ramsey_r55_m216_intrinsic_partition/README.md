# An intrinsic M216 partition and a forced degree-19 edge

Let G be a red/blue coloring of K43 with no monochromatic K5. Suppose its
red degree profile is 19²20⁵21³⁶ and its local triangle counts obey

| Red degree | Red cap | Blue cap |
|---|---:|---:|
| 19 | 85 | 115 |
| 20 | 93 | 107 |
| 21 | 100 | 100 |

These explicit hypotheses describe one complete hard-branch profile at
M=216. Interpreting the caps as deficiencies at least seven imports the
campaign's local-extremum table. The theorem below can instead be read
directly under the displayed caps.

**The two degree-19 vertices are red-adjacent.** Moreover the whole stated
profile has a complete partition into thirteen degree-preserving exceptional
core types and fifteen core/central-defect keys. Every blue triangle cap is
an equality, and there are exactly two units of red triangle deficit.
The keys retain every remaining physical edge and all central-defect
placements. They are not a list of existing completions.

The forced edge excludes a complete intrinsic branch with all attachments
free. The finite partition covers the whole stated profile, not the other
six M216 profiles or the other M-slices. No surviving key is decided here.
In particular this does not solve the h2731 central-cap realization target.

## Defect accounting

Write Z={0,1} for the degree-19 vertices, E={2,...,6} for the degree-20
vertices, C={7,...,42}, and F=G[Z union E]. Let r_v and b_v be the
differences between the displayed caps and actual red/blue triangle counts,
and put s_v=r_v+b_v. These are nonnegative integers.

Handshaking gives 447 red edges. Counting mixed triangles gives

$$
\sum_v(t_R(v)+t_B(v))
=3\left[\binom{43}{3}-\frac12\sum_v d_v(42-d_v)\right]
=8598.
$$

The cap sums are 4235 and 4365, totaling 8600. Thus
sum(r_v+b_v)=2. Since each monochromatic triangle is counted three times,
sum r_v is congruent to 4235, hence to 2, modulo 3. Consequently

$$
\sum_v r_v=2,\qquad b_v=0\text{ for every }v,\qquad s_v=r_v.
$$

For a vertex v let a_Z(v) and a_E(v) count its red neighbors in Z and E.
The exact neighborhood identity

$$
t_R(v)+t_B(v)=\binom{42-d_v}{2}-447+
\sum_{u\in N_R(v)}d_u
$$

therefore gives

$$
2a_Z(v)+a_E(v)=
\begin{cases}
5+s_v,&v\in Z,\\
4+s_v,&v\in E\cup C.
\end{cases}
\tag{1}
$$

All seven exceptional deficits are determined by F; their sum is at most
two. Every central signature has weighted size 4, 5, or 6, with its excess
over four exactly its red deficit. These conclusions use the same physical
graph, not independently assigned local moments.

## A catalog-free fourteen-vertex obstruction

An (4,4;14) graph cannot have 56 red edges. Each red degree is at most eight:
nine red neighbors would contain a red triangle or blue four-clique by
R(3,4)<=9. Hence 56 edges would make every red degree eight and every blue
degree five.

At each vertex the red neighborhood is a triangle-free eight-vertex graph
with no independent four-set. Each of its degrees is at most three, so its
edge count t_R is at most 12. The blue neighborhood is triangle-free on five
vertices and has at most six edges. The regular neighborhood identity is
t_R+t_B=18, forcing t_R=12 and t_B=6 everywhere.

The only triangle-free five-vertex graph with six edges is K2,3. Indeed its
maximum degree cannot be four, since that would make it a star; a vertex of
degree three has three independent neighbors, and the remaining vertex
must connect to all three to attain six edges.

Thus every blue neighborhood would induce K2,3. This is impossible.
Choose any blue triangle. For a blue edge uv put
q(uv)=|N_B(u) intersect N_B(v)|. Each q is either two or three. At any
vertex of the triangle the other two vertices are adjacent in its K2,3
neighborhood and lie in opposite parts, so the two incident q-values are
different. The three edges of a triangle cannot receive two values with
different values at each vertex.

For completeness, R(3,3)<=6 follows from three same-color neighbors.
A triangle-free nine-vertex graph with no independent four-set has maximum
degree three. A vertex of degree at most two would have six nonneighbors,
containing an independent triple by R(3,3)<=6. All nine degrees would
therefore be three, contradicting handshaking. This proves R(3,4)<=9.
The non-sharp fourteen-vertex edge bound is an elementary auxiliary lemma;
no novelty is claimed for the small Ramsey bounds or counting method.

## Excluding the blue degree-19 pair

Suppose 01 is blue. Equation (1) forces both vertices of Z to be red to
all five vertices of E, with s_0=s_1=0. For e in E it gives
s_e=d_{G[E]}(e). Since E has no blue K5, it has at least one red edge.
The total deficit of two forces exactly one red E-edge, and all central
vertices have s_v=0.

No central vertex can be red to both vertices of Z: its weighted size four
would then make it blue to every E vertex, and E contains a blue K4.
Consequently the two red central neighborhoods A and B are disjoint,
each of size 19-5=14.

Every vertex of A is red to exactly two E vertices by (1). Since the red
triangle count at 0 equals 85,

$$
85=1+2\cdot14+e_R(A),\qquad e_R(A)=56.
$$

A is red to 0 and blue to 1, so it contains neither color of K4. The
fourteen-vertex obstruction gives a contradiction. This proves 01 red for
every graph under the full stated profile, with no fixed signature vector,
central core, global automorphism, or restricted edit family.

## Complete exceptional-core census

For clarity the census includes the just-excluded blue-pair branch.
Set eta=1[01 red], b=e_R(Z,E), and e=e_R(E). Summing (1) over Z and E gives

$$
\sum_{v\in Z\cup E}s_v=4\eta+3b+2e-30\le2.
$$

Individual Z inequalities give b>=10 when eta=0 and b>=6 when eta=1.
The E inequalities give b+e>=10. Before checking individual degrees and
five-cliques, these leave precisely the buckets

$$
(\eta,b,e)=(0,10,0),(0,10,1),(1,6,4),(1,6,5),(1,7,3),(1,8,2).
$$

The first has a blue K5 on E. The last cannot meet the individual E
inequalities. In that last case an E vertex with no Z neighbor would require
four E neighbors but there are only two E edges. Thus the Z-incidence
multiplicities are 2,2,2,1,1; the last two vertices each require two E
neighbors. All four edge ends would then belong to just those two vertices,
impossible in a simple graph.

The exact remaining census has 1,480 degree-labeled cores in fourteen
orbits under S2 on Z and S5 on E. The sole blue-pair orbit has ten labeled
cores, leaving 1,470 labeled cores in thirteen red-pair orbits:

| Canonical mask | Orbit size | Sum of central red deficit |
|---:|---:|---:|
| 40573 | 60 | 1 |
| 65209 | 60 | 0 |
| 111865 | 30 | 2 |
| 111989 | 60 | 2 |
| 113913 | 60 | 0 |
| 114037 | 120 | 0 |
| 128249 | 120 | 0 |
| 128373 | 240 | 0 |
| 380153 | 120 | 0 |
| 380277 | 240 | 0 |
| 451059 | 120 | 0 |
| 451061 | 120 | 0 |
| 451431 | 120 | 0 |

Pairs use lexicographic order on 0,...,6; the first pair is the least
significant bit. Canonical means the minimum mask over S2 times S5.
This is the complete census of the displayed necessary finite predicate,
not a feasibility assertion for any central attachment.

The ten cores with no central deficit give ten keys. The one with central
deficit one gives one key, normalized to s_7=1. Each of the two cores with
central deficit two gives two keys: s_7=2 or s_7=s_8=1. Thus there are
fifteen keys. All unspecified deficits are zero. Choosing the canonical
core and the central-deficit multiset gives a unique invariant branch key;
it does not give a unique labeling of the full graph.

## Exact composition into fifteen complete formulas

For each key use all 903 Boolean red-edge variables x_uv. Fix only the
21 exceptional-core bits and impose the degree profile. Define literal
triangle polynomials

$$
T_R(v)=\sum_{\{a,b\}\subset V\setminus\{v\}}x_{va}x_{vb}x_{ab},
\quad
T_B(v)=\sum_{\{a,b\}\subset V\setminus\{v\}}
(1-x_{va})(1-x_{vb})(1-x_{ab}).
$$

Impose T_R(v)=red_cap(v)-s_v and T_B(v)=blue_cap(v) at every vertex.
For every five-set S impose

$$
1\le\sum_{\{u,v\}\subset S}x_{uv}\le9.
$$

The remaining 882 edges are unrestricted except for these stated equations
and inequalities. Equation (1) may be included as a redundant constraint.
No exceptional signature count, central edge quota, anchor-minimum rule,
or core outside the seven exceptional vertices is fixed.

Every original graph maps into one of these formulas: canonically relabel
its exceptional core, then move its central deficit support to 7 or 7,8.
The two permutations have disjoint supports. Conversely a satisfying
assignment literally gives a graph in the stated hard profile. This proves
equivalence between the full profile and the disjunction of the fifteen
formulas. Relabeling a graph is not an assumption that the permutation is
its automorphism. No SAT encoding or backend decision is claimed here.

## Reproduction and checks

With Python 3.10+ and a C++20 compiler, from the repository root:

~~~sh
python3 -B ramsey_r55_m216_intrinsic_partition/reproduce.py /tmp/m216-partition-replay
~~~

Use --cxx /absolute/path/to/compiler if needed. The default prefers
g++-16 when available. Expected status:
VERIFIED_M216_INTRINSIC_PARTITION_AND_BLUE_PAIR_EXCLUSION.
Build products and the full labeled stream are generated in external scratch.

The Python producer enumerates the proved structural buckets and forms
complete degree-preserving orbits. The independent C++ census reads no
producer data and checks all 2^21 literal graphs directly against the seven
weighted inequalities, deficit sum, and all five-sets. The complete sorted
labeled sets agree entry for entry. A separate set-based transport decoder
checks every group element. All 1,378 labeled central-defect placements
are normalized with all 903 physical edges retained.

Definition-level controls exhaust all 32,768 six-vertex colorings for the
R(3,3) premise, all 1,024 five-vertex graphs for the K2,3 equality case, and
all eight triangle-codegree patterns. Four changed certificates are rejected.
Normal and assertion-disabled Python agree. Production used CPython 3.12
and Homebrew GCC 16.2.0 with the flags in reproduce.py; the complete
reproduction took about eleven seconds. The fourteen-vertex and
blue-pair exclusions are the hand proofs above; the finite controls do not
pretend to enumerate all graphs on fourteen or 43 vertices.

The complete native census also agreed under address and undefined-behavior
sanitizers, using GCC 16.2.0 with -O1 -g -fsanitize=address,undefined and
-fno-omit-frame-pointer. All integer masks use 21 bits, individual weighted
degrees are at most nine, and all sums are at most 63, well within the
declared integer types.

## Provenance and boundary

This result follows the unresolved M216 central-cap target at Discovery Net
h2731, artifact bafkreibl7go4zdqocjagizwdnake6rxnnyjqpbujwu6ddubnmekffcy4ey,
source commit ad677522efbe0aacb531edc7b3e52a1780cdfe53 in
[the signature-cut transfer package](https://github.com/njallskarp/math_source_code_open/tree/ad677522efbe0aacb531edc7b3e52a1780cdfe53/ramsey_r55_m216_signature_cut_transfer).
Its fixed core 901619 maps to canonical core 380277 by
(0,1,2,3,4,5,6) -> (1,0,6,5,3,4,2); this transport is checked.
Its old pointwise
witness still fails the central caps. The new forced edge does not separate
that witness and is not credited as satisfying the central-cap realization
gate.

The hard-cap interpretation imports the extrema at h2099,
bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba.
The auxiliary regular-graph contradiction is distinct from the earlier
order-fifteen regular-side exclusion h2609. It uses no catalog or prior
enumeration certificate.
[McKay--Radziszowski](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
develop neighborhood subgraph identities;
[Angeltveit--McKay](https://arxiv.org/html/2409.15709v2) give the current
pointed-gluing context. A limited targeted search located no exact version
of this intrinsic profile partition; no historical-priority claim is made.

This is author-checked mathematics, not external peer review or
proof-assistant formalization. Trust remains in the displayed reductions,
the exact Python and independently implemented C++ code, compiler/runtime
semantics, hashes for identity, and ordinary hardware. No numerical
feasibility verdict or solver status enters the theorem.

No whole M-slice or full degree profile is excluded. All fifteen complete
formulas remain undecided. The original 66 hard profiles and 271 anchored
splits remain the coverage boundary. A literal graph meeting all central
caps and the claimed exceptional-root conditions, or a complete
profile-layer exclusion, remains the next substantive central-cap target.
