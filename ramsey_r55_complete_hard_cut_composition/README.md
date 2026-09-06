# Complete edge-cut composition from hard triangle caps

Let \(G\) be a simple red graph on 43 vertices, with blue its complement.
Assume red degrees are 18 through 24 and that, at every vertex in both
colors, the literal triangle count is at most \(C(d)\) at color degree \(d\):
\[
(C(18),\ldots,C(24))=(78,85,93,100,107,115,125).
\]
Then for every nonempty proper subset \(A\), with
\(a=\min(|A|,43-|A|)\),
\[
q(a)\le e_R(A,V\setminus A)\le a(43-a)-q(a),
\qquad q(a)=18a-2\left\lfloor\frac{3a^2}{8}\right\rfloor.
\]

**No monochromatic-five prohibition is needed.** Thus the complete
size-dependent edge-cut schema of h3391, independently accepted at h3407,
is redundant in the literal degree-and-hard-cap subsystem, before its
five-clique constraints. This covers all subsets, both colors, and all
seven \(M=214,\ldots,220\) slices. In particular it covers every one of
the fifteen complete M216 formulas at h3481/h3487 with all their non-core
edges free.

H3509 previously proved only the uniform 34/48 cut implication and stronger
uniform 35/51 gaps. Its numerical envelope left the full schema unresolved
at side sizes 13,14,15,16. Here those four sizes are closed, with required
cut bounds \(108,106,102,96\), respectively. The stronger old uniform
35/51 theorem is retained. No profile or whole M-slice is excluded.

## Physical reduction

Write \(d_v=d_R(v)\), \(m=e_R(G)\), and
\[
W=21(n_{18}+n_{24})+12(n_{19}+n_{23})+3(n_{20}+n_{22}).
\]
Mixed-wedge counting gives
\[
\sum_v(t_R(v)+t_B(v))
=3\binom{43}{3}-\frac32\sum_v d_v(42-d_v).
\]
The total cap deficit is therefore
\[
S=\sum_v\bigl(C(d_v)+C(42-d_v)-t_R(v)-t_B(v)\bigr)
=\frac{43-W}{2}\ge0.
\]
Handshaking makes \(W/3\) odd, so \(W\le39\). Since the weights dominate
three times the absolute degree deviation,
\(\sum_v|21-d_v|\le13\). Orient red so that \(m\le451\); then
\(445\le m\le451\), and \(M=m-231\) ranges over all seven slices.

Fix a color and a smaller cut side \(A\), with \(a=|A|\le21\),
\(B=V\setminus A\), \(b=43-a\). Let
\[
D_A=\sum_{v\in A}d_v,\quad C_A=\sum_{v\in A}C(d_v),\quad
q=e(A,B),\quad e=e(A),\quad h=\binom a2-e.
\]
Then \(D_A=2e+q\). The following three necessary inequalities all concern
the same physical graph. None uses K5-freeness.

### 1. Internal triangles

For every red edge \(uv\) of \(G[A]\), its common-neighbor count in \(A\)
is at least \(d_A(u)+d_A(v)-a\). Hence
\[
3T(G[A])\ge\sum_{v\in A}d_A(v)^2-ae.
\]
If \(2e=ak+r\), \(0\le r<a\), the minimum square sum over integer
degrees is \(Q_a(2e)=(a-r)k^2+r(k+1)^2\). This follows by transferring
one unit between two entries differing by at least two. Consequently
\[
Q_a(2e)-ae\le C_A. \tag{I}
\]

### 2. Triangles crossing the cut

Every missing edge in \(A\) destroys at most \(a-2\) internal triangles,
so \(T(G[A])\ge\binom a3-h(a-2)\).
Let \(c_v=d(v,A)\) for \(v\in B\); their sum is \(q\). The number of
triangles with two vertices in \(A\) and one in \(B\) is at least
\[
\sum_{v\in B}\binom{c_v}{2}-bh.
\]
For \(q=bk+r\), \(0\le r<b\), convexity gives the minimum
\(F_b(q)=b\binom{k}{2}+rk\).
Internal triangles contribute three incidences at \(A\); triangles with
two vertices in \(A\) contribute two. Dropping the nonnegative contribution
of triangles with only one vertex in \(A\) yields
\[
3\binom a3+2F_b(q)-(a+80)h\le C_A. \tag{X}
\]
The coefficient is \(3(a-2)+2b=a+80\). Negative lower bounds are harmless.

### 3. Exceptional-degree weight on missing edges

Put \(w_v=21-d_v\), and
\[
H(d)=21d+\binom{42-d}{2}-m-C(d)-C(42-d).
\]
The literal local identity
\[
t_R(v)+t_B(v)=\binom{42-d_v}{2}-m+
                 \sum_{u\in N_R(v)}d_u
\]
shows that the nonnegative cap slack at \(v\) is
\[
s_v=\sum_{u\in N_R(v)}w_u-H(d_v).
\]
In particular \(\sum_{v\in A}s_v\le S\).
Write \(W_A=\sum_{v\in A}w_v\), \(H_A=\sum_{v\in A}H(d_v)\), and
\(W_B^-=\sum_{v\in B}\min(0,w_v)\).
The internal weighted neighbor sum equals
\[
(a-1)W_A-
\sum_{\substack{\{u,v\}\subset A\\uv\notin E}}(w_u+w_v).
\]
The outside contribution is at least \(aW_B^-\): each negative-weight
outside vertex has at most \(a\) incidences, and nonnegative contributions
can be dropped. Thus
\[
(a-1)W_A+aW_B^- -H_A-S
\le
\sum_{\substack{\{u,v\}\subset A\\uv\notin E}}(w_u+w_v)
\le P_A(h), \tag{W}
\]
where \(P_A(h)\) is the sum of the \(h\) largest entries of the multiset
\(\{w_u+w_v:\{u,v\}\subset A\}\). Negative entries and multiplicities
are retained. This last bound is a uniform upper bound for every placement
of the missing edges, not a choice of their locations.

## Complete finite arithmetic bridge

The coarse degree envelope has exactly 104 tuples
\((n_{18},\ldots,n_{24})\), characterized by:

- nonnegative counts summing to 43;
- \(W\le39\);
- even degree sum at most 902.

Their counts for \(M=214,\ldots,220\) are \(1,3,7,14,21,27,31\).
This deliberately larger envelope precedes the stronger sieves that leave
the campaign's 66 profiles / 271 anchored splits. It does not reinstate
any excluded profile or depend on those later sieves.

For each profile and color, retain every degree-class count vector
\(a_d\in[0,n_d]\) with \(1\le\sum a_d\le21\). For each, test every
integer cut value
\[
\max(0,D_A-a(a-1))\le q<q(a),\qquad q\equiv D_A\pmod2.
\]
These are exactly the possible counterexample parameters after only
the cut identity and simple-graph edge box. Other impossible parameters
may remain, which only weakens this necessary layer.

There are 81,996 oriented side placements and 187,929 candidate cut
violations. Every one violates at least one of (I), (X), (W):

| \(M\) | Internal (I) | Crossing (X) | Weighted (W) |
|---:|---:|---:|---:|
| 214 | 1172 | 35 | 25 |
| 215 | 4811 | 125 | 44 |
| 216 | 12513 | 239 | 28 |
| 217 | 24846 | 296 | 8 |
| 218 | 37846 | 244 | 1 |
| 219 | 49156 | 153 | 0 |
| 220 | 56293 | 94 | 0 |
| Total | 186637 | 1186 | 106 |

The order of tests is I, then X, then W; counts mean first rejecting
inequality, not disjoint mathematical obstruction types. Minimum positive
integer gaps are 2,1,29, respectively. No candidate survives.

An arbitrary violating physical graph maps to its degree profile, color,
side counts and literal cut value in this list, and must satisfy all three
inequalities. Exhaustion therefore proves the complete cut implication.
No symmetry of the whole graph is assumed: only statistics invariant under
relabeling are used. No core, exceptional incidence, or outside edge is fixed.

## Two load-bearing M216 examples

Take the full profile \(19^2 20^5 21^{36}\), where \(m=447\), \(S=2\).
At a vertex of degree 19, \(H(d)=5\); at degree 20 or 21, it is four.

If \(A\) consists of both degree-19 vertices, all five degree-20 vertices
and seven degree-21 vertices, then \(a=14\), \(D_A=285\), \(C_A=1335\).
A cut of size 105 has \(e=90,h=1\). Inequalities I and X give lower
bounds 1056 and 1280, so neither contradicts the cap. But
\[
(a-1)W_A+aW_B^- -H_A-S=13\cdot9-58-2=57,
\qquad P_A(1)=4.
\]
The weighted inequality fails by 53. This example exposes why retaining
the cap identity on the exceptional incidences matters.

If \(A\) instead consists of both degree-19 vertices and thirteen
degree-21 vertices, then \(a=15,D_A=311,C_A=1470\).
The cut value 101 forces \(h=0\). Inequality I gives only 1365 and
the weighted lower bound is negative. Inequality X gives
\[
1365+2F_{28}(101)=1365+270=1635>1470.
\]
These are witnesses to the need for the new arithmetic rows in this proof,
not claimed physical cap-feasible graphs.

## Reproduction and independence

With Python 3.10+ and standard library only, from the repository root:

~~~sh
python3 -B ramsey_r55_complete_hard_cut_composition/reproduce.py
~~~

Expected status: VERIFIED_COMPLETE_HARD_CAP_CUT_REDUNDANCY.
Certificate SHA-256:
fec26f418e8d9464923e099d3a2ec3d6fc9f13fe986f2114425e9a8b9bd4e64e.
Complete candidate stream SHA-256:
8a2b4eb1b2be51a57642929b0a33d37d30f4b8eba604c13d65057adf1267bb06.

The producer uses bounded multiplicities, balanced-degree formulas and
sorted missing-edge weights. The checker imports no producer: it uses
weighted-budget recursion, degree-class convolution, minimum-cost dynamic
programs for squares and crossing wedges, and bounded knapsack on
degree-class pair multiplicities for missing-edge weight.

The reproducer compares every complete candidate record byte for byte in
temporary scratch space, then removes those streams. It also checks the
compact certificate and normal/assertion-disabled output agreement.
It fails on timeout, any surviving case, changed certificate, or stream
disagreement. No solver or external catalog is used in reproduction.

Definition-level controls cover all 33,867 labeled graphs on one through
six vertices, 31,668 physical cut instances at orders at most five, and
fourteen explicit knapsack cases including negative pair weights. The
local and global identities are checked on actual graph counts; synthetic
nonnegative cap slack tests the weighted inequality without requiring a
small graph to satisfy the special order-43 cap table. Six modified
certificates are rejected.

The finite reduction and inequalities are unformalized mathematics.
Exact complete arithmetic and independent author implementations provide
validation, not external review or proof-assistant verification. Trust
remains in that reduction, source, Python semantics, hashes for identity
and ordinary hardware. No raw graph dump, private input, binary, database,
floating solver verdict, or omitted large certificate is a premise.

## Composition ledger and remaining scope

The explicit literal theorem needs no Ramsey catalog. Interpreting its
caps as the campaign's hard deficiency imports h2099's extrema table;
the usual degree window imports \(R(4,5)=25\).

It completes the h3509 edge-cut composition gap and shows that h3391's
entire size-dependent schema adds no Boolean graph restriction to any
complete degree-and-cap subsystem, including all fifteen h3481 formulas.
This statement does not concern a fractional moment relaxation whose
triangle coordinates need not be literal graph triangles.

Open: vertex-connectivity and binary-rank composition, all full M-slices,
all fifteen retained M216 formulas, the low-deficiency branch and the
shared-cap realization gate. The two unsuccessful M216 cap passes remain
recorded; no repair search was extended here. R1's strengthened M214
moment system and r2's local-family/gluing work remain separate.

Next falsifiable bridge: a complete implication or explicit admissible
counterexample for the 18-vertex-connectivity condition on a named literal
degree-and-cap layer, or a strict rank-family separator on a complete
remaining relaxation. Do not keep adding edge-cut thresholds after the
declared full-family implication is complete.

## Provenance and primary context

Graph targets:

- h3509: bafkreia5ddojekboppxrieutu26y3b5bkoigvok25hwez22dwztpc6i24m.
- h3391: bafkreibldpy2ryp62lcj42ryosot6cddteumpvgh7e3nxxjgxxsk4oelva;
  independent acceptance h3407:
  bafkreiacpo4shcyfksp4mh5ci7shjs5y4sciwag2q4kkroy3xram7yeud4.
- h2099: bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba.
- h3481: bafkreicmohnam44363c6b777mfzgmcgsyprfrmuhy5f4p3qhthvcufzslm;
  independent acceptance h3487:
  bafkreie4qp7hir2cghzie7423pwcdf77old4ma4c4g5rbzcnvfwpvppdcy.

Targeted primary checks after gap selection:
[McKay--Radziszowski, Subgraph Counting Identities and Ramsey Numbers](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
and [Angeltveit--McKay, R(5,5) at most 46](https://arxiv.org/html/2409.15709v2).
The local identities, convexity, edge counting and finite necessary-layer
method are classical. No historical-priority, numerical-sharpness or new
general-method claim is made. No Ramsey-number bound changes.
