# Hard caps classify every separator of order eighteen

Let \(G\) be a simple graph on 43 vertices with neither a red nor a blue
\(K_5\), where blue is the ordinary complement. Assume the literal local
triangle counts in **both** colors obey the hard cap table
\[
(C(18),\ldots,C(24))=(78,85,93,100,107,115,125)
\]
at the corresponding color degree.

**Theorem.** In either color, every separating vertex set of order at most
18 has order exactly 18 and is the full neighborhood of a degree-18
vertex. Removing it leaves exactly two connected components, of orders
1 and 24. The degree-18 vertex, and hence this separator, is unique in
that color. There is at most one such separator across the two colors.

Consequently:

- If all red degrees lie in 19 through 23, both color graphs are
  **19-connected**.
- If a red degree-18 vertex exists, red connectivity is exactly 18,
  with the unique minimum separator its neighborhood; blue connectivity
  is at least 19. A red degree-24 vertex gives the reversed statement.
- For all disjoint sets \(A,B\) with \(|A|,|B|\ge2\) and
  \(|A|+|B|\ge25\), the cross edges include both colors.

The assertions about a degree-18 vertex are conditional statements, not
existence or sharpness examples. No hypothetical Ramsey43 graph is
constructed, and no whole profile or M-slice is excluded.

This closes the complete **nontrivial order-18 separator branch** under
hard caps. It strengthens the h3381/h3393 global 18-connectivity result
by composing its component argument with the local deficit identity.
Unlike the h3535 edge-cut redundancy theorem, the new proof uses
monochromatic-five avoidance essentially. It does **not** prove that
18-connectivity follows from literal degree and caps alone.

## Inputs and notation

The standard \(R(4,5)=25\) theorem gives \(18\le d_R(v)\le24\).
We use \(R(3,3)\le6\), \(R(3,4)\le9\), and \(R(3,5)\le14\).
These small upper bounds have elementary proofs: the usual three-neighbor
argument proves the first. A triangle-free graph on nine vertices with
independence number at most three would have all degrees three, since
degrees are at most three and nonneighbor sets have order at most five.
Handshaking excludes it. The Ramsey recurrence then gives
\(R(3,5)\le R(2,5)+R(3,4)\le14\). Also \(R(2,5)=5\) and \(R(1,5)=1\).

Write \(d_v=d_R(v)\), \(m=e_R(G)\), and \(n_d=|\{v:d_v=d\}|\). Put
\[
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}).
\]
Let \(t_R(v)\) and \(t_B(v)\) be the literal monochromatic triangle
counts through \(v\), and define nonnegative slack
\[
s_v=C(d_v)+C(42-d_v)-t_R(v)-t_B(v),\qquad S=\sum_v s_v.
\]
The mixed-wedge identity gives
\[
S=\frac{43-W}{2}.
\tag{1}
\]
For clarity, this follows by subtracting
\[
\sum_v(t_R(v)+t_B(v))
=3\binom{43}{3}-\frac32\sum_vd_v(42-d_v)
\]
from the total cap sum. Substitution of the seven entries gives (1).

Since the degree sum is even, \(W/3\) is odd: its parity equals
\(\sum_v(d_v-21)\), which is odd at order 43. Hence
\[
W\le39,\qquad \sum_v|21-d_v|\le13.
\tag{2}
\]
The latter sum is odd. The cost for a deviation of magnitude 2 exceeds
three times that deviation by 6, and for magnitude 3 the excess is 12.
In particular \(n_{18}+n_{24}\le1\). These statements are invariant
under color reversal.

We will also use the literal local identity
\[
t_R(v)+t_B(v)=\binom{42-d_v}{2}-m+
                 \sum_{u\in N_R(v)}d_u.
\]
With \(w_u=21-d_u\) it becomes
\[
s_v=\sum_{u\in N_R(v)}w_u-H(d_v),\qquad
H(d)=21d+\binom{42-d}{2}-m-C(d)-C(42-d).
\tag{3}
\]
These counting identities are classical; no novelty is claimed for them.

## 1. Complete component reduction

Suppose \(X\) disconnects red and \(k=|X|\le18\). Independence numbers
of the components of \(G-X\) add, with sum at most four.

First consider a clique component \(A\), of order \(a\le4\). If
\(a=2,3,4\), each vertex has at least \(19-a\) red neighbors in \(X\).
The common red neighborhood of \(A\) in \(X\) has size at least
\[
a(19-a)-(a-1)k.
\]
At the worst value \(k=18\), these lower bounds are \(16,12,6\).
Its upper bounds, from absence of a red \((5-a)\)-clique and blue
five-clique, are \(13,4,0\), respectively. Thus these cases are impossible.

A singleton component \(v\) has all its neighbors in \(X\). The minimum
degree bound forces \(k=d_R(v)=18\) and \(X=N_R(v)\). By (2) there
cannot be another degree-18 vertex, so no other singleton component.
Other clique components have just been excluded. Two other nonclique
components would contribute at least \(1+2+2=5\) to independence.
Thus precisely one other component remains, of order 24. Its independence
number is exactly three: it is at most three by the budget and cannot
be at most two by \(R(5,3)\le14\). This is the stated allowed exception.

If there is no clique component, every component has independence number
at least two. Hence there are exactly two, \(A,B\), each of independence
number two and order at most 13. Their orders sum to \(43-k\ge25\).
Up to exchanging the parts, the only possibilities are
\[
(k,|A|,|B|)=(17,13,13),\quad(18,12,13).
\tag{4}
\]
This is a complete reduction, not a selection of a convenient component.

## 2. Outside vertices force the saturated twelve-side

For \(z\in X\), its red neighbors in either component have no red \(K_4\)
and independence number at most two. Thus there are at most eight,
by \(R(4,3)\le9\).

In the first case of (4), the blue neighbors of \(z\) in each component
number at least five. Each contains a blue edge, since a red \(K_5\)
is forbidden. These two blue edges, all blue cross edges, and \(z\)
give a blue \(K_5\). This recovers the last case in the reviewed
18-connectivity proof.

Now consider \((18,12,13)\). The blue neighbors of any \(z\in X\)
in the 13-side \(B\) contain a blue edge. The blue neighbors in \(A\)
therefore contain **no** blue edge; otherwise the same blue-five
argument applies. They form a red clique. There are at least four
of them, and at most four because red \(K_5\) is forbidden. Consequently
\[
d_R(z,A)=8\quad\hbox{for every }z\in X,\qquad e_R(A,X)=144.
\tag{5}
\]
Every vertex in \(G[A]\) also has internal red degree at most eight:
its red neighbors in \(A\) form a \((4,3)\)-graph. Hence
\[
e_R(A)\le48,\qquad
D_A=\sum_{v\in A}d_R(v)=2e_R(A)+144\le240.
\tag{6}
\]
This even degree sum is the load-bearing bridge from the Ramsey component
argument into the hard-cap degree budget.

## 3. The degree budget forces two profiles, and both contradict slack

By (2), \(D_A\ge12\cdot21-13=239\). Its evenness in (6) therefore
forces \(D_A=240\), so the signed degree deficit on \(A\) is 12.
The total absolute deficit is odd, at least 12 and at most 13; it is 13.
If any degree differed from 21 by at least two, the cost \(W\) would
be at least \(3\cdot13+6=45\), contradicting (2).

All degrees therefore lie in \(\{20,21,22\}\). The twelve vertices
of \(A\), with signed deficit 12, all have degree 20. Exactly one outside
vertex has nonzero deficit. The full working-color profile must be one of
\[
20^{13}21^{30}\quad(m=445,\ M=214),\qquad
20^{12}21^{30}22^1\quad(m=446,\ M=215).
\tag{7}
\]
Both have \(W=39\) and total slack \(S=2\).
Equality in (6) also forces \(G[A]\) to be 8-regular.

In the first profile, every vertex of \(A\) has eight internal red
neighbors of weight \(w=1\), and all outside weights are nonnegative.
Equation (3) has \(H(20)=451-m=6\). Thus \(s_v\ge8-6=2\) for
every \(v\in A\).

In the second profile, there is just one outside negative-weight
vertex, of weight \(-1\). The same neighbor sum is at least seven,
while \(H(20)=5\); again \(s_v\ge2\). Therefore in either case
\[
S\ge\sum_{v\in A}s_v\ge24>2=S.
\]
The contradiction has a margin of 22 slack units. This eliminates
the entire \((18,12,13)\) branch without enumerating any component graph,
attachment, core, or free outside edge.

Only the singleton case remains. Color reversal completes the theorem.
Since \(n_{18}+n_{24}\le1\), the exceptional separator can occur in at
most one color. A degree-18 vertex always supplies a separator by deleting
its neighborhood; this proves the conditional “exactly 18” statements.
No assertion of an actually existing hard-cap graph follows.

## Complete formula consequence and M coverage

For every disjoint \(A,B\) of total size 25, each of size at least two,
both disjunctions
\[
\bigvee_{u\in A,v\in B}x_{uv},\qquad
\bigvee_{u\in A,v\in B}\neg x_{uv}
\]
are necessary Boolean constraints. Larger such pairs contain a pair of
total size 25 with both sides nontrivial. Singleton sides are permitted
in the red-presence clause if red has no degree-18 vertex, and in the
blue-presence clause if blue has no degree-18 vertex. These are exact
universal schemas; the exponentially many physical clauses are not
claimed to have been emitted.

Orient red sparsely, so \(m\le451\). Equations (1)–(2) give
\(445\le m\le451\) and \(M=m-231\in\{214,\ldots,220\}\).
The coarse 104-profile envelope has this classification:

| M | Both colors at least 19-connected | Red degree18 exception | Blue degree18 exception |
|---:|---:|---:|---:|
| 214 | 1 | 0 | 0 |
| 215 | 3 | 0 | 0 |
| 216 | 6 | 1 | 0 |
| 217 | 11 | 3 | 0 |
| 218 | 16 | 5 | 0 |
| 219 | 20 | 6 | 1 |
| 220 | 23 | 5 | 3 |
| Total | 80 | 20 | 4 |

These are necessary degree-profile categories, not graph counts or
assertions of realization. The 104-profile envelope deliberately
precedes the later 66-profile / 271-split sieves; nothing here reinstates
their eliminated cases. In particular, the full profile
\(19^2 20^5 21^{36}\) has both colors 19-connected, so all fifteen
complete M216 formulas at h3481/h3487 inherit this stronger condition
with every non-core edge free. No one of those formulas is decided.

## Exact source and controls

From the repository root, with Python 3.10+ and standard library only:

~~~sh
python3 -B ramsey_r55_hard_separator18/reproduce.py
~~~

Expected status: VERIFIED_HARD_SEPARATOR18_CLASSIFICATION.
Certificate SHA-256:
3140a84e1ea86b3b29878d5294926b32c00de01f7b229653ed4c791ff1cf8caa.

The producer enumerates the bounded seven-class degree multiplicities,
every twelve-vertex degree submultiset in both colors, and the component
arithmetic. The checker imports no producer or earlier campaign package.
It reconstructs profiles by weighted-budget recursion and twelve-subsets
by convolution, then tests the two saturation profiles by direct choices
of the exceptional outside incidence. All 4,586 twelve-subset records
are compared byte for byte during reproduction.

The written proof, rather than the computed table, proves the universal
claim. The finite arithmetic audit checks all 104 profiles, both
orientations, 57 clique-component cases, the two nonclique size cases,
both saturated degree cases, and the complete singleton exception.
Definition-level controls exhaust all 33,867 labeled graphs on orders one
through six, checking local and global identities, component independence
additivity, and clique common-neighbor bounds. Sixty-four attachments of
an outside vertex to two red three-vertex paths, giving seven vertices
in total, test the
crossing-blue-pair implication nonvacuously; four yield explicit blue
five-sets. Seven certificate corruptions must be rejected.
Normal and assertion-disabled output must agree.

No solver, floating arithmetic, catalog, private data or external input
is required for reproduction. All temporary streams are removed. Native
hardware and unformalized Python semantics remain operational trust
boundaries. The independent algorithms are author-written validation,
not independent-author review or proof-assistant formalization.

## Provenance, scope and next bridge

Source graph target: h3381,
bafkreicyapqnopj5rghq27dcisg2yebhrtcbrk7duewblhv2mlrotpxdl4,
independently accepted at h3393,
bafkreic4aycbbjtbopoj3ic2xkxwuhv3pjax6bsb3rvtzyt3c5ukvz7g3q.
The explicit degree/cap identities were used in h3509/h3535; the new
step is the forced twelve-vertex degree saturation and slack contradiction.
The full edge-cut family closed at h3535 remains closed.

The hard-cap interpretation imports the h2099 local extrema
\(U(18..24)=(85,92,100,107,114,122,132)\) and their catalog completeness:
“every local deficiency is at least seven” implies the displayed caps.
Those caps are a conditional specialization of the original Ramsey
problem. The low-deficiency branch is untouched. The degree window
imports \(R(4,5)=25\). All further small Ramsey bounds are proved above.

Targeted primary checks after graph selection:
[Beveridge–Pikhurko, On the connectivity of extremal Ramsey graphs](https://opikhurko.warwick.ac.uk/E/BeveridgePikhurko08ajc.pdf)
and [Angeltveit–McKay, R(5,5) at most 46](https://arxiv.org/html/2409.15709v2).
The former assumes order \(R(r,b)-1\); this proof does not assume that
43 is extremal. Component independence, common-neighbor counting and
the local deficit identity are established methods. No historical
priority, numerical sharpness or new general technique is claimed.

Open: cap-only 18-connectivity redundancy, separators of order 19,
binary-rank composition, all whole M-slices, the low-deficiency alternative
and the shared-cap realization gate. This result requires the Ramsey
five-set conditions and cannot be applied to r1's fractional moment
survivor as if those coordinates were a graph. R1's fully linked P4
and r2's remaining interface families retain their separate scopes.

The next falsifiable target should consume this strict separator
condition on a named complete layer, or test binary-rank composition.
Do not infer a blanket 19-connectivity theorem while discarding the
degree-18 exception, and do not reset the parked M215/M216 search counters.
