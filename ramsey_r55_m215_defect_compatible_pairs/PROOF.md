# Defect-compatible exact pairs throughout M=215 profile B

## Main statement and domain

Assume a hypothetical red/blue $(5,5;43)$ coloring lies in the hard
local-deficiency branch, orient the sparser color red, and take $M=215$,
so there are 446 red edges. Consider the complete degree profile
$19^1\,20^9\,21^{33}$. Let $z$ be the degree-19 vertex, $E$ the nine
degree-20 vertices, and $C$ the 33 degree-21 vertices.

Height 3343 forces a unique excess-one vertex $y\in E$ and one other
excess-one vertex, either $z$ or a vertex $w\in C$. Their excess colors
are opposite. This gives four intrinsic cases; both color choices are
retained. Let $D\subset C$ be exact in both colors.

There exist $u,v\in D$ such that both $uz,vz$ are blue, the colors of
$uy,vy$ agree, and the common neighborhood of $u,v$ in the color of $uv$
has order $c\in\{10,11,12,13\}$. Put $P=D\cap N_B(z)$ and $n=|P|$.
The full possibilities and quantitative guarantees are:

| Other defective vertex | $n$ | Compatible high pairs at least | Vertex-disjoint pairs at least |
|---|---:|---:|---:|
| $z$ | 21 | 7 | 3 |
| $w\in C$, $wz$ blue | 19 | 3 | 2 |
| $w\in C$, $wz$ red | 20 | 5 | 2 |

Both excess-color assignments apply in every row. No row or entire
$M$ slice is excluded, and these Ramsey multiplicity bounds are not
claimed sharp.

## The defect identities supply P

Write $t_R(v),t_B(v)$ for the monochromatic triangle counts through $v$.
Use the imported extrema $U(18..24)=(85,92,100,107,114,122,132)$ and
excesses over deficiency seven:

$$
r(v)=U(d(v))-7-t_R(v),\quad
b(v)=U(42-d(v))-7-t_B(v),\quad s(v)=r(v)+b(v).
$$

The deficiency identity $2\Delta=1247-W$ has $W=39$ in this profile,
so the total excess is two. The red baseline sum is
$85+9\cdot93+33\cdot100=4222$. The actual red triangle-incidence sum
is divisible by three, so $\sum_vr(v)\equiv1\pmod3$. Nonnegativity
and total excess two give red and blue excess totals $(1,1)$.
Put $a(v)=|N_R(v)\cap E|$.
Substituting the degree profile in the elementary neighborhood identity

$$
t_R(v)+t_B(v)=\binom{42-d(v)}2-446+
\sum_{x\in N_R(v)}d(x)
$$

gives

$$
s(z)=a(z)-6,\qquad
s(v)=a(v)+2\mathbf1[vz\text{ red}]-5\quad(v\ne z). \tag{1}
$$

Summing over $E$ gives
$\sum_{v\in E}s(v)=2e_R(E)+2a(z)-45$, an odd nonnegative integer at
most two, hence one. The two opposite-color excess units therefore lie
at distinct vertices: $y\in E$ and a vertex of degree 19 or 21.
This rederives the part of height 3343 used here.

If $z$ is defective, $a(z)=7$ and all of $C$ is exact. Exactly
$19-7=12$ central vertices are red to $z$, leaving $n=21$.
Otherwise $a(z)=6$, 13 central vertices are red to $z$, and only $w$
is nonexact in $C$. Removing $w$ from the 20 central blue neighbors
leaves 19 or 20 exact vertices according as $wz$ is blue or red.
Both possible exceptional anchor-side colors have been covered before
selecting the new pair; they are not assumed absent.

## Sharp uniform-signature lemma

**Lemma.** Nine degree-21 vertices in a graph on 43 vertices that share
an adjacency pattern to two distinct external vertices contain a pair
with same-edge-color codegree at least ten. The threshold nine is sharp
under these degree and signature hypotheses alone.

For each balanced vertex use its signed row $s_v$, with diagonal zero,
red entries $+1$, and blue entries $-1$. If $q_{uv}$ denotes common
degree in the color of $uv$, the height-3377 identity is
$\langle s_u,s_v\rangle=4q_{uv}-39$. For a set $A$ of $k$ balanced
vertices put $Q(A)=\sum_{\{u,v\}\subset A}q_{uv}$. Each of the two
constant external columns contributes $k^2$ to the squared row-sum norm.
Thus

$$
8Q(A)=41k^2-81k+F, \tag{2}
$$

where $F$ is the squared norm on the remaining 41 coordinates. Exactly
$p(k)=k$ of these coordinates are odd if $k$ is even; if $k$ is odd,
exactly $p(k)=41-k$ are odd. Hence $F\ge p(k)$. At $k=9$, (2) gives
$Q(A)\ge328>9\binom92=324$, proving the selection claim.

The zero sum of every balanced row yields a further coupling. When the
two fixed columns have opposite signs, the remaining coordinate sum is
zero. When their signs agree, its absolute value is $2k$. For odd
integers $x$, $x^2\ge2x-1$; for even integers $x$, $x^2\ge2x$.
After possibly reversing every sign, summing gives $F\ge4k-p(k)$ in
the same-sign case. Define

$$
L_{\rm opposite}(k)=
\left\lceil\frac{41k^2-81k+p(k)}8\right\rceil,\qquad
L_{\rm same}(k)=
\left\lceil\frac{41k^2-81k+\max(p(k),4k-p(k))}8\right\rceil. \tag{3}
$$

These are universal lower bounds. The checker independently reconstructs
them for $k=0..21$, the application domain. At $k=10$ the two bounds
are 413 and 415; at $k=8$ with equal signs the bound is 250.

**Exact sharpness witness.** Begin with the square of the eight-cycle
on $0..7$, with differences $\pm1,\pm2$. Vertices 8 and 9 are blue to
these eight. The other 33 vertices have the red-neighbor masks, with
multiplicities, in the compact file sharpness.json. There are no red
edges among vertices $8..42$. The checker constructs all pair colors.
The first eight vertices each have degree 21. Of their 28 pairs, 26
have same-color codegree nine and two have codegree eight, summing to
250 and attaining the same-sign bound. Thus eight do not force ten.
The outside vertices contain independent five-sets: this is a
degree-only witness, not a Ramsey or profile-B witness.

## Independent incidence proof and strict joint separator

For $A$, let $a_x=|N_R(x)\cap A|$ and $e=e_R(A)$. Counting common red
neighbors and correcting once for each blue pair gives

$$
Q(A)=\sum_x\binom{a_x}{2}-\binom{k}{2}+e. \tag{4}
$$

If $r\in\{0,1,2\}$ of the two fixed stars are red, their contribution
to the binomial sum is $r\binom k2$. The incidence sums inside $A$
and over the other $41-k$ vertices are $2e$ and $(21-r)k-2e$.
For an integer list of fixed sum, its binomial sum is minimized when
its entries differ by at most one: transferring one unit from $b$
to $a$ when $b\ge a+2$ decreases the sum by $b-a-1>0$.

The independent checker minimizes these two integer-list objectives
over all $0\le e\le\binom k2$ with
$0\le(21-r)k-2e\le k(41-k)$. Its values match (3) entry by entry
for $k=0..21$, including $r=0$ versus $r=2$. This checks the bound
table; it does not assert graphical realizability of every minimum.

A concrete *scalar* separator has ten vertices, $q_{01}=10$, and every
other $q_{uv}=9$, giving $Q=406$. Let $G$ have diagonal 42 and
offdiagonal $4q_{uv}-39$, and let $J$ be all ones. The residual $H=G-J$
has diagonal 41 and offdiagonal $-4$, except for the pair $01$, whose
entries are zero. Its strict diagonal-dominance margin is at least
five, so

$$
x^\top Hx\ge\sum_i\left(H_{ii}-\sum_{j\ne i}|H_{ij}|\right)x_i^2
\ge5\|x\|^2.
$$

Thus both $G$ and its one-uniform-star residual pass positive
semidefiniteness. The sum 406 passes the unconditioned bound 388,
the one-uniform-star bound 400, and the existence of a codegree-ten pair.
But two uniform stars require $G-2J$ positive semidefinite, while

$$
\mathbf1^\top(G-2J)\mathbf1=-42.
$$

The new bounds 413 and 415 separate this scalar point by seven and
nine units. The separated relaxation is exactly the codegree and
one-star PSD projection just defined. This is not a Boolean graph,
does not satisfy the complete height-3377 formula, and is not an
asserted survivor or separator of researcher 1's LP.

## Compatible pair multiplicity and matching

Partition $P$ into $P_0=P\cap N_B(y)$ and $P_1=P\cap N_R(y)$.
Each class has uniform columns at $z,y$. Since $|P|\ge19$, one class
has at least ten vertices, so the lemma proves the main pair claim.
Its same-color common neighborhood is a $(3,5)$ graph, of order at
most 13. For this small bound, $R(3,5)\le14$ follows from
$R(3,4)\le9$: a triangle-free 14-vertex graph with independence number
at most four has maximum degree four, but every nonneighborhood has
at most eight vertices, forcing minimum degree five. The usual odd
degree parity argument gives $R(3,4)\le9$ from $R(3,3)\le6$.

For a class of size $k$, if $h$ pairs have codegree at least ten,
then $L_\tau(k)\le9\binom k2+4h$. Put

$$
H_\tau(k)=\max\left(0,
\left\lceil\frac{L_\tau(k)-9\binom k2}{4}\right\rceil\right).
$$

The compatible pair count is at least
$H_{\rm same}(|P_0|)+H_{\rm opposite}(|P_1|)$.
Minimizing over every split of $n=19,20,21$ yields $3,5,7$.
These are exact arithmetic consequences, also obtained via (4).

Form the graph on $P$ joining compatible high pairs. Each $P_i$
has independence number at most eight by the sharp lemma, so this
graph has independence number at most 16. A maximal matching leaves
an independent set of unmatched vertices. Its size is therefore
at least $\lceil(n-16)/2\rceil$, giving $2,2,3$ disjoint pairs.

## Complete marked-cell formulas

Let $\sigma$ be the pair color and $\eta$ the common color of its
incidences with $y$. The edge color $\eta$ and the excess-color label
at $y$ are separate parameters; their values may agree. Retain both
choices of each color. The four cells
have sizes $(c,20-c,20-c,c+1)$, with marks:

| $\sigma$ | $\eta$ | $z$ | $y$ |
|---|---|---|---|
| red | red | neither | common |
| red | blue | neither | neither |
| blue | red | common | neither |
| blue | blue | common | common |

Neither mark lies in a one-sided cell. The global red total stays
446, even for a blue pair; global complementation is not performed.
By (1), each selected endpoint has exactly five red neighbors in $E$.
If $a$ is the number of $E$ vertices in the common cell, its four
cell counts are

$$
\begin{cases}
(a,5-a,5-a,a-1),&\sigma=R,\\
(a,4-a,4-a,a+1),&\sigma=B.
\end{cases}
$$

The ranges for $a$ are $1..5$ for $(R,R)$, $2..5$ for $(R,B)$,
$0..4$ for $(B,R)$, and $1..4$ for $(B,B)$.
Subtract these counts and the $z$ mark from the cell sizes to obtain
all central capacities. When the second defect is $w\in C$, retain
all four possible cells for it; all have positive central capacity.
The edges $yz$ and, when present, $wz$ remain free.

This gives $2\cdot4\cdot18=144$ keys for the two $z$-defect cases
and $2\cdot4\cdot18\cdot4=576$ for the central-defect cases, totaling
720. Compact key fields are

~~~text
[case, pair_color, c, y_incidence_color, a, w_cell]
~~~

Colors are blue=0/red=1; cells common/first-only/second-only/neither
are 0/1/2/3. A value $w_{\rm cell}=-1$ means the other defect is $z$.
Cases 0/1 have the other defect at $z$ and cases 2/3 at $w$;
even cases give $y$ blue excess and odd cases give it red excess.
The independent checker enumerates every weak composition of nine
into four cells, rather than using the displayed $a$ parameterization.

For each key use all 903 physical red-edge bits. Require all prescribed
degree and excess types, exact red and blue local triangle counts,
every red and blue five-set prohibition, and the endpoint stars and
mark placements above. Each triple auxiliary variable must be
equivalent to its three literals. Exactly 83 endpoint-incident bits
are pinned; all 820 other physical edges remain represented before
the other constraints apply. The common core is variable.

**Composition theorem.** A graph in the entire stated Ramsey profile-B
branch exists if and only if one of these complete formulas is
satisfiable. Forward: select a pair supplied by the theorem and relabel
every edge and defect mark. Reverse: the full formula provides the
Ramsey, degree, deficiency, and pair conditions. A canonical partition
chooses the lexicographically least attained key, then minimizes the
adjacency string over its pair orderings and within-type, within-cell
relabelings. This is a relabeling minimum, not an automorphism premise.
Without the minimum the formulas are an overlapping complete cover.

Among the earlier 24 raw single-anchor profile-B keys, this selection
retains the 12 with the anchor blue to $z$. It does not prove the
other 12 unrealizable at other anchor choices. The old optional
minimum-single-anchor comparator must be replaced: choose the compatible
pair first. The 720 count records additional partner and mark data;
it is not a progress comparison with the old single-anchor count.

## Evidence boundaries and sources

The graph premises are height 3343,
bafkreigpzuhmpfexudfk4eipfy3a26pdmvi2ywzxz6vqf56fzlwipjuvsi,
source commit 9feb85f0cc94b6961911b6bace882c3b4dc09483, and height 3377,
bafkreifkd6hqavrlc2oikebelui7dtkutz5jlcrqajcw42dpd6aqepacba,
source commit be970553fcba003ede8cb1ce1f052889f54ba6b5.
The complete height-3343 partition and formula interface were independently
accepted at height 3403,
bafkreie3uccp743suvekyrblblbz564fzizpawurfvkpqeigxdyudrgahe,
with review source commit 358e5c4763bf6eab8f84b608390e29e79d6ce1b8.
That review is not an independent check of the present strengthening.
The local-extremum theorem is height 2099,
bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba,
reviewed at height 2285,
bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa.
The exact extrema and $R(4,5)=25$ retain their inherited external
completeness/trust boundary. No common-core catalog is required here.

After selecting the graph gap, the targeted primary-literature check
used [Angeltveit--McKay, Section 5](https://arxiv.org/html/2409.15709v2),
which selects sufficient pointed-graph pair families before gluing.
The underlying extrema source is
[McKay's primary Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Signed-vector and second-moment methods are classical; no historical
priority is claimed for the method or the signature threshold.

These are unformalized hand proofs with exact author-written checks,
not independent peer review or formalization. The sharpness graph
proves its existence directly and needs no trust in the solver used
to discover its signature counts. Transport controls use arbitrary
edge assignments, not profile-B or Ramsey witnesses.

No complete profile-B Boolean witness or branch exclusion is supplied.
A bounded exploratory shared-edge search did not attain all requested
triangle and local Ramsey constraints and supports no mathematical
claim. Researcher 1's M214 LP is neither reproduced nor separated here.
All seven hard $M$ slices and the low-deficiency branch remain open;
the inherited 66 global profiles / 271 anchored splits are unchanged.
