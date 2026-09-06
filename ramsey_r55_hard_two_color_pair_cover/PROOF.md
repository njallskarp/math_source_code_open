# A two-color exact-pair cover for the whole hard branch

## The balanced-degree lemma

Let $G$ be any simple graph on an odd number $n$ of vertices. Call a
vertex balanced if its red degree is $(n-1)/2$, where red denotes an edge
of $G$, and blue denotes a nonedge between distinct vertices. For two
balanced vertices $u,v$, let $q_{uv}$ count their common neighbors in
the color of the pair $uv$. If $A$ is a set of $k$ balanced vertices,
then

$$
 Q(A):=\sum_{\{u,v\}\subset A}q_{uv}
 \ \geq\ L(n,k):=
 \left\lceil\frac{(n-4)k^2-(2n-5)k+p(n,k)}8\right\rceil,
 \qquad
 p(n,k)=\begin{cases}k&k\text{ even},\\n-k&k\text{ odd}.\end{cases}
$$

**Proof.** Define the signed row $s_u\in\{-1,0,1\}^n$ by putting zero
at $u$, $+1$ at red neighbors, and $-1$ at blue neighbors. Its squared
norm is $n-1$. Put $t=|N_R(u)\cap N_R(v)|$. If $uv$ is red, the
common blue degree is $t+1$; if $uv$ is blue, it is $t-1$. Counting
the agreements and disagreements in the other $n-2$ coordinates gives

$$
 \langle s_u,s_v\rangle=4q_{uv}-(n-4)
$$

in both cases. Therefore

$$
 8Q(A)=(n-4)k^2-(2n-5)k+
 \left\|\sum_{u\in A}s_u\right\|^2. \tag{1}
$$

The coordinate sum has parity $k-1$ on $A$ and parity $k$ outside
$A$. Each odd coordinate has squared value at least one. This proves
the lower bound on the norm, and integrality proves the ceiling. ∎

For $n=43,k=15$, the bound is $Q(A)\geq949>9\binom{15}{2}=945$.
Consequently **every set of 15 degree-21 vertices contains a pair with
$q_{uv}\geq10$**. The pair's color is part of the conclusion; it is
not prescribed. Equivalently, on the balanced vertices, the graph joining
pairs with $q_{uv}\geq10$ has independence number at most 14. This is a
degree-only theorem, with no Ramsey, local-extremum, or catalog premise.

One can see the contradiction directly: if all 105 pair codegrees were
at most nine, their signed inner products would be at most $-3$, so
the squared norm of the sum of the 15 rows would be at most
$15\cdot42-6\cdot105=0$. But its 28 outside coordinates are odd.

## Independent degree-moment form

For $w\in V(G)$, let $a_w=|N_R(w)\cap A|$, and let $e=e_R(A)$.
The sum of common red degrees over pairs in $A$ is
$\sum_w\binom{a_w}{2}$. For each blue pair its same-color common
degree is one less than its common red degree, while a red pair needs
no correction. Thus

$$
 Q(A)=\sum_w\binom{a_w}{2}-\binom{k}{2}+e,\qquad
 \sum_{w\in A}a_w=2e,\quad
 \sum_{w\notin A}a_w=k(n-1)/2-2e. \tag{2}
$$

For fixed integer sum, a list minimizes the sum of its binomial
coefficients when its entries differ by at most one: moving one unit
from $b\geq a+2$ to $a$ decreases the objective by $b-a-1>0$.
The checker minimizes this relaxation for every feasible internal edge
count $0\leq e\leq\binom{k}{2}$, subject to the crossing count lying
between zero and $k(n-k)$. At $n=43$, it agrees with equation (1) for every
$15\leq k\leq42$. This is a lower-bound relaxation, not an assertion
that its degree lists or minima are graphically realizable.

## From an arbitrary hypothetical Ramsey coloring to the hard branch

Assume now that neither color contains a $K_5$. Import the reviewed
local extrema and degree bound:

$$
18\leq d(v)\leq24,\qquad
U(18),\ldots,U(24)=(85,92,100,107,114,122,132).
$$

Here $U(j)$ is the maximum number of edges of a $(4,5;j)$ graph.
Let $t_R(v)$ count red triangles through $v$, equivalently red edges
in its red neighborhood, and define $t_B(v)$ in blue. The two local
deficiencies are $U(d(v))-t_R(v)$ and $U(42-d(v))-t_B(v)$.

Their sum over all vertices is $\Delta$. If $n_j$ counts degree $j$
vertices, the mixed-wedge double count gives

$$
2\Delta=1247-W,\qquad
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}). \tag{3}
$$

For completeness, the monochromatic triangle count is
$\binom{43}{3}-\frac12\sum_v d(v)(42-d(v))$, and the sum of all
$t_R(v)+t_B(v)$ is three times that count. Substitution gives equation (3).
The seven resulting per-vertex coefficients in $2\Delta$ are
$(8,17,26,29,26,17,8)$.

The **global case split** is: some local deficiency is at most six,
or all 86 local deficiencies are at least seven. The latter is the
**hard branch**. Only that branch is covered by the new pair theorem
below. In it, equation (3) gives $W\leq43$. Since $W$ is a multiple of three
and $1247-W$ is even, $W\equiv3\pmod6$, so
$W\in\{3,9,15,21,27,33,39\}$.

Let $D$ consist of balanced vertices whose two deficiencies both equal
seven; call them doubly exact. The excess above the baseline $86\cdot7$
is $E=(43-W)/2$. At most $W/3$ vertices are nonbalanced, and at most
$E$ balanced vertices fail to be doubly exact. Consequently

$$
 |D|\geq43-W/3-E=(129+W)/6\geq22. \tag{4}
$$

Choose the sparser color as red, once and for all, and write $m=e_R(G)$.
Since $3|d-21|$ is at most the degree's weight in $W$,

$$
 |2m-903|\leq\sum_v|d(v)-21|\leq W/3\leq13.
$$

It follows that $445\leq m\leq451$. At any $u\in D$, its red and
blue neighborhoods both have order 21 and exactly 100 edges in their
respective colors. Its red cross total is therefore

$$
 M=m-\bigl(21+100+(\binom{21}{2}-100)\bigr)=m-231
 \in\{214,\ldots,220\}. \tag{5}
$$

Changing the anchor preserves this $M$. Equations (3)--(5) reproduce
the inherited hard-branch anchor bridge; their upstream trust boundary
is the local-extremum catalog completeness and $R(4,5)=25$.

## New whole-hard-branch pair theorem

Apply the balanced-degree lemma to any 15 vertices of $D$. There exist
$u,v\in D$, a color $\sigma\in\{R,B\}$ equal to the color of $uv$,
and $c=q_{uv}\geq10$. Their common $\sigma$-neighborhood is a
$(3,5;c)$ graph in color $\sigma$: a triangle extends with $u,v$
to a monochromatic five-set, and an independent five-set is also forbidden.
Thus $c\leq13$.

The last bound needs no catalog: $R(3,5)\leq14$ follows elementarily
from $R(3,4)\leq9$. A triangle-free 14-vertex graph with independence
number at most four has maximum degree at most four, but each
nonneighborhood has order at most eight, forcing minimum degree at least
five. To establish $R(3,4)\leq9$, a triangle-free 9-vertex graph with
independence number at most three has maximum degree at most three;
$R(3,3)\leq6$ forces minimum degree at least three, contradicting
handshaking on nine vertices. The elementary six-vertex pigeonhole proof
establishes $R(3,3)\leq6$.

Moreover, for any $k$ vertices of $D$, every pair has codegree at most
13. If $h$ pairs have codegree at least ten, then

$$
 L(43,k)\leq Q(A)\leq9\binom{k}{2}+4h,
 \qquad h\geq\left\lceil\frac{L(43,k)-9\binom{k}{2}}4\right\rceil. \tag{6}
$$

At $k=22$, $L(43,22)=2140$, the margin is 61, and $h\geq16$.
Every hard graph therefore contains **at least 16 qualifying exact pairs**.
The previous $M=215$ localization gives $|D|\geq28$ there, hence at
least 35 pairs. Its profile B has $|D|\geq32$, hence at least 52 pairs.
These multiplicity consequences depend on the corresponding prior
anchor counts. No optimality or realizability of these lower bounds is claimed.

## Complete pair cover and finite-formula composition

There are $7\cdot2\cdot4=56$ scalar families indexed by
$(M,\sigma,c)\in\{214,\ldots,220\}\times\{R,B\}\times\{10,\ldots,13\}$.
For a chosen ordered qualifying pair $u,v$, partition the other 41
vertices by adjacency in color $\sigma$ to the two endpoints:

| Cell | Common | $u$-only | $v$-only | Neither |
|---|---:|---:|---:|---:|
| Size | $c$ | $20-c$ | $20-c$ | $c+1$ |

Relabel $u,v$ as 0,1 and put the four cells consecutively after them.
This is a relabeling of vertices. When $\sigma=B$, interpret blue
adjacency as a zero of the original red-edge bit. **Do not complement
the whole graph:** its red total remains $231+M$, not $903-(231+M)$.

Here is an exact finite-formula specification for each family. Use one
Boolean $x_{ij}$ for each of the 903 unordered vertex pairs, always
indicating red. Require:

1. Every five-set has at least one red and at least one blue pair.
2. Every degree is in $18..24$, and $\sum_{i<j}x_{ij}=231+M$.
3. For every vertex $v$, require
   $t_R(v)\leq U(d(v))-7$ and $t_B(v)\leq U(42-d(v))-7$.
4. At both endpoints, require degree 21 and $t_R=t_B=100$.
5. Pin the two endpoint stars according to the displayed cell sizes
   and pair color. If a common-core type is selected, pin its internal
   edge bits using color $\sigma$.

The triangle counts in this specification are literal integer sums of
products of three edge bits, or their complements. In a Boolean encoding,
each auxiliary triple bit must be equivalent to the conjunction of all
three relevant literals, in both directions. Degree-dependent $U$
values are defined by a finite case split on the integer degree.

With no common core pinned, every physical edge among the remaining 41
vertices is free before these constraints: 820 bits. If a common core
of order $c$ is pinned, the 83 endpoint-incident pairs and its
$\binom c2$ internal pairs are fixed. All

$$
 903-83-\binom c2=820-\binom c2
 \in\{775,765,754,742\}
$$

other physical edge bits remain. These include every edge between cells
and every unpinned within-cell edge, including the neither cell. Local
triangle totals, degree sums, or neighborhood compatibility cannot
replace these shared edge bits or the mixed five-set constraints.

**Composition theorem.** A hard-branch $(5,5;43)$ coloring exists if
and only if at least one of these 56 complete formulas is satisfiable.
For the forward implication, orient the sparser color red, select the
pair supplied by the theorem, and relabel by its four cells. All five
conditions hold on the transported physical edge assignment. For the
reverse implication, read the edge bits of a satisfying assignment:
condition 1 gives the Ramsey property, condition 3 gives the hard
branch, and the other conditions specify its slice and exact pair. ∎

The families can overlap: one graph may have many qualifying pairs.
If a canonical scalar partition is desired, for each graph choose the
lexicographically least triple $(M,\sigma,c)$ attained by a qualifying
pair, ordering red before blue. A canonical labeled representative can
be obtained by minimizing the 903-bit adjacency string over all ordered
pairs attaining that triple and all permutations within the four cells.
This is a finite minimization over relabelings, not an automorphism
assumption. The 56 unrestricted formulas already form a complete cover;
no such costly minimization is needed for a complete exclusion search.

Optionally use the complete historical $(3,5;c)$ catalogs, whose
isomorphism counts for $c=10,11,12,13$ are $313,105,12,1$. This refines
the cover to $7\cdot2(313+105+12+1)=6034$ **unmarked core templates**.
This count imports catalog completeness and nonisomorphism; it is not a
count of graphs, admissible marked profiles, or feasible completions.
The 56-family theorem can instead leave the entire common core variable,
so its completeness does not require those catalogs.

## Composition boundaries with earlier work

The earlier $M=214$ codegree-nine theorem guarantees a **red** exact
pair. The present result guarantees codegree at least ten in **one of
the two colors**. It does not show that the red pair can always have
codegree ten. In particular, one cannot remove the $c=9$ cases from
the existing red-only 389-formula cover on the strength of this theorem.
A backend using the new restriction must implement both pair colors.

For $M=215$, the 82 intrinsic defect keys remain valid. After choosing
an endpoint of a qualifying pair as anchor, its raw rooted key is among
the existing 674 complete rooted keys. However, the earlier optional
rule choosing a minimum incidence-vector **single anchor** cannot simply
be conjoined with the new pair restriction. There is no proof that such
a minimum anchor is incident to a qualifying pair. Use the raw cover,
or choose a qualifying pair first and canonicalize within that domain.
Both exceptional-vertex color choices and all five profile/color splits
must remain represented.

No entire $M$ slice is excluded. The low-deficiency branch is separate;
its previously published 189 scalar roots / 18,767 optional core
templates are unaffected. The inherited later arithmetic screens across
the seven hard slices still give 66 global profiles and 271 anchored
splits. The new universal pair restriction does not change those counts.

## Provenance and trust

The hard-branch imports are Discovery Net artifacts
`bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba`
(height 2099), reviewed at
`bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa`
(height 2285). The exact-anchor cross normal form is
`bafkreifnqxojqgjem3s5i6v6eeewusdau5j3l6sjcrj6gjgm7erfakscxa`
(height 2105), and the general propagated counts are
`bafkreieqidxlesjy5jq2hwfx2plxw7t25lcyghvuggoi7olmadrgfngi6q`
(height 2123). The stronger $M=215$ counts and rooted keys are
`bafkreigpzuhmpfexudfk4eipfy3a26pdmvi2ywzxz6vqf56fzlwipjuvsi`
(height 3343), source commit `9feb85f0cc94b6961911b6bace882c3b4dc09483`.
The red-nine comparison is
`bafkreieexa3krkpvl72pfxvqs46nivcgaqedmvy7uy2ljduc3ub7joyqfu`
(height 3130), and the low-deficiency pair cover is
`bafkreiericmyeapmnstbygbr3syoxa3akf7kcd5q3pnm27ypp27oe3p2by`
(height 2775).

The selected primary-literature check was
[Angeltveit--McKay, *R(5,5) ≤ 46*, §2 and §5](https://arxiv.org/html/2409.15709v2),
whose complete pointed-graph gluing framework requires coverage of the
selected pair family and all retained gluing choices. The optional core
counts come from [McKay's primary Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The signed-row and second-moment mechanisms are classical. No historical
priority is claimed; the contribution is the displayed degree-43 lemma
and its exact composition with the inspected hard-branch reductions.

This is an unformalized hand proof with exact author-written checks,
not independent peer review, a solver verdict, or an UNSAT certificate.
No Boolean backend is generated or solved. The core-count fields of the
certificate copy the cited catalog counts; replay does not certify their
historical completeness. The balanced-degree theorem and the 56-family
transport require no external computational input. The Ramsey hard-branch
application inherits the reviewed $U$ table and $R(4,5)=25$.
