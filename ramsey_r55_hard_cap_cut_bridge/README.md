# Hard triangle caps force global 35/51 cut gaps

Every simple graph on 43 vertices satisfying the following **literal**
conditions has at least 35 edges of each color across every partition
with both parts of size at least two, and at least 51 of each color when
both parts have size at least three:

- Red degrees are between 18 and 24, and blue is the ordinary complement.
- At a vertex of degree \(d\) in either color, the number of triangles
  of that color through it is at most \(C(d)\), where
  \[
  (C(18),\ldots,C(24))=(78,85,93,100,107,115,125).
  \]

No five-clique prohibition, fixed exceptional core, signature distribution,
local catalog, or assumed global symmetry is needed for this literal theorem.
For the campaign's hard branch these caps follow from all 86 deficiencies
being at least seven, using the explicit h2099 extrema import.

Consequently the two uniform 34/48 cut families of h3391, accepted at h3407,
are already redundant in the full physical degree-and-cap layer across
every \(M=214,\ldots,220\). This is a complete implication for all subsets
and both colors, rather than checking cuts of one saved graph.
It also excludes the additional hard-branch cut sizes 34 (two vertices
on each side) and 48, 49, 50 (three on each side).

The **whole size-dependent** h3391 schema is a different family. We do not
claim it is redundant: the numerical envelope below does not dominate its
bound at smaller-side orders 13, 14, 15, 16. Nor is this a claim about
fractional triangle variables, vertex connectivity, or binary rank.

## Short universal proof

Let \(n_d\) count red degrees \(d\), and put
\[
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}).
\]
For any graph, not only a Ramsey graph, counting mixed wedges gives
\[
\sum_v(t_R(v)+t_B(v))
=3\binom{43}{3}-\frac32\sum_vd_v(42-d_v).
\]
Subtracting this from the sum of the displayed caps gives exactly
\((43-W)/2\). Thus \(W\le43\). Handshaking implies an odd number
of even-degree vertices, so \(W/3\) is odd. Hence \(W\le39\).
Also
\[
\sum_v|d_v-21|\le W/3\le13.
\]
Both facts are invariant under complementation.

Work in either color and take the smaller part \(A\) of a partition,
of order \(a\le21\). Set \(D=\sum_{v\in A}d(v)\), \(e=e(G[A])\),
and \(q=|\partial A|=D-2e\).
For two vertices their degree sum is at least 37: two degree-18 vertices
would already cost 42 in \(W\). Thus \(q\ge35\) if \(a=2\).
Any three degrees sum to at least 57. A smaller sum would require either
two degree-18 vertices or degrees \(18,19,19\), with costs at least 42
or 45. Therefore \(q\ge51\) if \(a=3\).

For \(4\le a\le18\), the deviation bound gives
\[
q\ge21a-13-a(a-1)=a(22-a)-13\ge59.
\]
It remains to exclude \(q\le50\) for \(a=19,20,21\).
That assumption forces
\[
e\ge e_0=\left\lceil(21a-63)/2\right\rceil.
\]
For any graph \(H\) of order \(a\) with \(e\) edges and \(T\) triangles,
summing common-neighbor lower bounds over its edges gives
\[
3T\ge\sum_{v\in H}d_H(v)^2-ae\ge4e^2/a-ae.
\]
Here \(3T\le\sum_{v\in A}t_G(v)\le125a\).
We would need \(4e^2-a^2e-125a^2\le0\), but:

| \(a\) | \(e_0\) | \(4e_0^2-a^2e_0-125a^2\) |
|---:|---:|---:|
| 19 | 168 | 7123 |
| 20 | 179 | 6564 |
| 21 | 189 | 4410 |

All are positive, and the quadratic is increasing for \(e\ge e_0\).
This proves the 35/51 conclusion for every subset and both colors.
The proof uses the local caps before any Ramsey prohibition is imposed.

## Exact envelope by slice and cut size

The public certificate additionally provides a stronger, integer envelope.
For \(2e=ak+r\), \(0\le r<a\), the minimum sum of squared integer
degrees is
\[
Q_a(2e)=(a-r)k^2+r(k+1)^2.
\]
Indeed, moving one unit from a degree at least two larger than another
strictly decreases the square sum. Therefore, writing
\(C_A=\sum_{v\in A}C(d(v))\), every physical graph satisfies
\[
Q_a(2e)-ae\le C_A.
\]
Take the largest integer \(e\in[0,\binom a2]\) satisfying this condition,
and subtract twice it from \(D\). This is a valid cut lower bound.
No assertion that a minimizing degree sequence or cut is realizable is made.

Orient red to have at most 451 edges. The deviation bound forces
\(445\le m\le451\), hence \(M=m-231\in\{214,\ldots,220\}\).
The complete **coarse arithmetic envelope** consists of 104 degree profiles,
with slice counts \(1,3,7,14,21,27,31\). These are all nonnegative
seven-tuples summing to 43, with \(W\le39\), even degree sum, and
degree sum at most 902.

This envelope deliberately precedes the stronger graph reductions that
leave the campaign's 66 profiles / 271 anchored splits.
The numbers 104 and 66 describe different layers; no previously excluded
profile is reinstated and no stronger catalog-completeness claim is made.
Using the larger envelope makes the implication independent of those
later reductions.

For each profile, all degree-class placements of a smaller side are kept.
There are 40,998 such placements. Relabeling within a degree class changes
neither \(D\) nor \(C_A\); thus this numerical reduction covers every actual
subset, without assuming a full-graph automorphism.
The certificate records all 104 profiles, the complete placement-stream
hash, both 21-entry bounds for every slice, and their minima:

| \(M\) | Red, sides \(\ge2\) | Blue, sides \(\ge2\) | Red, sides \(\ge3\) | Blue, sides \(\ge3\) |
|---:|---:|---:|---:|---:|
| 214 | 38 | 40 | 54 | 57 |
| 215 | 37 | 39 | 53 | 56 |
| 216 | 36 | 38 | 52 | 55 |
| 217 | 35 | 38 | 51 | 54 |
| 218 | 35 | 37 | 51 | 54 |
| 219 | 35 | 37 | 52 | 53 |
| 220 | 36 | 36 | 52 | 53 |

Across slices and colors the bounds for \(a=1,\ldots,21\) are
\[
(18,35,51,65,78,88,96,103,107,109,110,108,104,99,92,92,92,91,90,89,86).
\]
They are certified lower bounds, not claimed sharp cut minima.

## Composition and scope

In every one of h3481's fifteen full M216 formulas, the physical degree
equations and two-color triangle equations imply the hypotheses above.
Thus adding the uniform 34/48 cuts cannot exclude any further **Boolean
graph** from that degree-and-cap subsystem. This conclusion holds with
every exceptional incidence and every central edge free.

More generally, the implication covers all seven hard \(M\)-slices,
independently of anchor selection, core normalization, cells, profiles
retained by later sieves, or formula marking. No full M-slice, retained
M216 formula, or low-deficiency branch is closed by it.
The exact generalized statement replaces the K5-free premise in the
uniform cut corollary by the hard cap hypotheses and improves its gaps.

The named h2731 graph fails central caps, so it is not a survivor of this
layer. This result does not turn it or the author's private nearpoints
into admissible witnesses. It does not meet the separate central-cap
realization gate. Both central-cap repair passes remain unsuccessful.

## Reproduction and trust

From the repository root, with Python 3.10+ and no third-party packages:

~~~sh
python3 -B ramsey_r55_hard_cap_cut_bridge/reproduce.py
~~~

Expected status: VERIFIED_HARD_CAP_35_51_CUT_BRIDGE.
The reproducer runs normal and assertion-disabled producer/checker modes,
compares exact bytes, and verifies all manifest entries.

The producer enumerates bounded multiplicities and uses the balanced-degree
formula. The checker imports no producer code: it independently recurses
over the weighted degree budget, composes every side placement by degree
class, and uses a minimum-square dynamic program over all integer degree
values. Complete profile lists and placement streams agree entry for entry,
as do all 294 slice/color/size bounds. Six mutated certificates are rejected.
Definition-level controls check all 33,867 labeled graphs of orders one
through six and 32,767 literal cut identities for orders at most five.
The three large-side contradiction rows are also checked separately.

The short universal argument is the theorem's proof; finite arithmetic
checks and small-graph controls validate its implementation and the sharper
envelope. This is author validation, not external peer review or a formal
proof. The literal theorem imports no Ramsey catalog or solver.
Its application to hard deficiency imports h2099's explicit local-extremum
table and the usual degree window from \(R(4,5)=25\).
Other trust comprises the displayed argument, exact Python semantics,
hash identity and ordinary hardware. No private graph dump, database,
solver status, floating-point bound or omitted large certificate is used.

## Primary context and graph provenance

The mixed-wedge and degree-square methods are classical; no historical
priority or new general extremal method is claimed. After selecting the
graph gap, the following primary sources were checked:

- [McKay--Radziszowski, Subgraph Counting Identities and Ramsey Numbers](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf).
- [Angeltveit--McKay, R(5,5) at most 46](https://arxiv.org/html/2409.15709v2),
  especially the separation between forced coverage and pointed gluing.
- [Goodman, Triangles in a complete chromatic graph](https://www.cambridge.org/core/journals/journal-of-the-australian-mathematical-society/article/triangles-in-a-complete-chromatic-graph/845889AE182D7A30D01E7CDC3697CAB9).

Graph inputs:
h2099 bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba;
h3391 bafkreibldpy2ryp62lcj42ryosot6cddteumpvgh7e3nxxjgxxsk4oelva;
h3407 bafkreiacpo4shcyfksp4mh5ci7shjs5y4sciwag2q4kkroy3xram7yeud4;
h3481 bafkreicmohnam44363c6b777mfzgmcgsyprfrmuhy5f4p3qhthvcufzslm;
h3487 bafkreie4qp7hir2cghzie7423pwcdf77old4ma4c4g5rbzcnvfwpvppdcy.

The next falsifiable bridge is whether the remaining size-dependent cuts,
vertex-connectivity cuts, or binary-rank constraints strictly separate a
fully specified remaining relaxation, rather than re-adding the now
redundant uniform cuts.
