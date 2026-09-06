# The Charney--Davis inequality for flag homology 5-spheres on 17 vertices

*Consolidated manuscript, 6 September 2026.*

**Evidence status.** The mathematical theorem was independently accepted in
Discovery Net at height 1340. This manuscript consolidates that proof and
incorporates the finite-graph Lean bridges at heights 1817 and 1829. It also
corrects a reciprocal normalization factor in the frozen audit and the review:
the four-dimensional link formula has factor \(8\), not \(1/8\).
The correction does not change the nonnegativity implication or theorem.
See [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md) for provenance, the exact
correction, reproduction, and the remaining formal trust boundary.

## Abstract

We prove that a finite flag generalized homology 5-sphere over any field
with 17 vertices satisfies the Charney--Davis inequality. Established
polar-size results reduce a hypothetical negative example to complement
degrees between three and six. A vertex-link identity and an
inclusion--exclusion count then force the complement to be triangle-free
with degree sequence \(3^{16}4^1\). The link of its distinguished
degree-four vertex has 12 vertices and 52 edges, giving
\(\gamma_2=-2\), contrary to low-dimensional nonnegativity.
The proof uses no graph census. We distinguish its human topological
interfaces from the polynomial, integer, and finite-graph statements checked
by the accompanying Lean projects.

## 1. Statement and conventions

Let \(\mathbb K\) be a field. A finite generalized homology
\((d-1)\)-sphere over \(\mathbb K\) means a finite pure simplicial complex
\(\Delta\) of dimension \(d-1\) such that, for every face \(\sigma\),
including the empty face,
\[
\widetilde H_i(\operatorname{lk}_\Delta\sigma;\mathbb K)
\cong
\begin{cases}
\mathbb K,&i=d-1-|\sigma|,\\
0,&i\ne d-1-|\sigma|.
\end{cases}
\tag{1.1}
\]
We use the usual reduced convention for the complex consisting of the empty
face, of dimension \(-1\). A complex is flag when every clique in its
one-skeleton is a face.

Write \(f_{i-1}\) for the number of faces with \(i\) vertices, so
\(f_{-1}=1\), and set
\[
F_\Delta(x)=\sum_{\sigma\in\Delta}x^{|\sigma|},\qquad
h_\Delta(t)=\sum_{i=0}^d f_{i-1}t^i(1-t)^{d-i}
=(1-t)^dF_\Delta\!\left(\frac{t}{1-t}\right).
\tag{1.2}
\]
The all-links hypothesis makes \(\Delta\) Eulerian. We use the standard
Dehn--Sommerville theorem in the form
\(h_\Delta(t)=t^d h_\Delta(1/t)\). Consequently there is a unique expansion
\[
h_\Delta(t)=
\sum_{i=0}^{\lfloor d/2\rfloor}
\gamma_i(\Delta)t^i(1+t)^{d-2i}.
\tag{1.3}
\]
Its coefficients are integers, by successive coefficient extraction in this
triangular basis, and \(\gamma_0=1\).

**Theorem.** If \(\Delta\) is a flag generalized homology 5-sphere over a
field and has exactly 17 vertices, then
\[
\gamma_3(\Delta)\geq0.
\]
For \(d=6\), equation (1.3) gives \(h_\Delta(-1)=-\gamma_3(\Delta)\);
thus the statement is exactly the Charney--Davis inequality in this case.

Let \(G\) be the one-skeleton and \(H=G^c\) its simple complement on the
same vertex set. Put
\[
q_v=\deg_H(v),\qquad m=|E(H)|,\qquad
T=\#\{\text{unordered triangles of }H\},\qquad
\pi=\min_v q_v.
\tag{1.4}
\]
The antipode number in the polar-size literature is \(q_v\); no metric
antipodal relation is involved.

## 2. Coefficient fields and the low-dimensional input

**Field-change lemma.** A finite \(\mathbb K\)-homology sphere with the
all-links convention (1.1) is a rational generalized homology sphere.

For each face link of dimension \(s\geq0\), its integral simplicial homology
groups are finitely generated. The universal-coefficient sequence injects
their tensor products with \(\mathbb K\) into the corresponding homology
over \(\mathbb K\). Vanishing in every degree below \(s\) therefore forces
the free integral ranks in those degrees to vanish. All lower rational
reduced Betti numbers are zero. The reduced Euler characteristic is
coefficient-independent and equals \((-1)^s\). There is no homology above
dimension \(s\), so the top rational Betti number is one. The dimension
\(-1\) case is immediate. Apply this argument to every link separately.
This proves the lemma; it does not assert vanishing of all integral torsion.

**Published input D.** Davis--Okun, Theorem 11.2.1, proves for a flag
rational homology 3-sphere \(S\) that
\[
\kappa(S):=F_S(-1/2)=
\sum_{i=0}^4(-1/2)^i f_{i-1}(S)\geq0.
\tag{2.1}
\]
We use the rational generalized-homology-sphere setting and all link
hypotheses of that result. See
[Davis--Okun](https://arxiv.org/pdf/math/0102104), Section 11.2.
By (1.2)--(1.3),
\[
\gamma_2(S)=h_S(-1)=16\kappa(S)\geq0.
\tag{2.2}
\]

We derive the four-dimensional consequence with its exact normalization.
Double-counting pairs \((v,\sigma)\) with \(v\in\sigma\) gives
\[
F'_\Delta(x)=\sum_v F_{\operatorname{lk}_\Delta(v)}(x).
\]
Substitution in (1.2), or ordinary differentiation, yields for a pure
\((d-1)\)-complex
\[
\sum_v h_{\operatorname{lk}_\Delta(v)}(t)
=d h_\Delta(t)+(1-t)h'_\Delta(t).
\tag{2.3}
\]
For a four-dimensional generalized homology sphere \(Y\), its gamma
expansion has degree-five basis terms, so
\(h_Y(-1)=0\) and \(h'_Y(-1)=\gamma_2(Y)\).
Apply (2.3) with \(d=5\), then (2.2), to obtain
\[
2\gamma_2(Y)
=\sum_v\gamma_2(\operatorname{lk}_Y(v))
=16\sum_v\kappa(\operatorname{lk}_Y(v)),
\]
and therefore
\[
\boxed{\gamma_2(Y)=8\sum_v\kappa(\operatorname{lk}_Y(v))\geq0.}
\tag{2.4}
\]
Links of links satisfy
\(\operatorname{lk}_{\operatorname{lk}_Y(v)}(\sigma)
=\operatorname{lk}_Y(\sigma\cup\{v\})\), so (1.1), flagness, and the
field-change lemma verify every use of D.
This is the qualitative implication in Gal's Corollaries 2.2.2--2.2.3;
we have derived the scalar in our conventions directly. See
[Gal](https://arxiv.org/pdf/math/0501046), Section 2.2.

The factor \(1/8\) recorded in the earlier audit and its review is not an
equivalent convention under their stated definition of \(\kappa\).
For example \(Y=C_5*C_5*S^0\) has \(\gamma_2(Y)=1\) and the sum in (2.4)
is \(1/8\). The incorrect factor would give \(1/64\). Section 7 records a
definition-level exact reproduction. Only nonnegativity is used below,
so the reciprocal-factor error does not invalidate that implication.

## 3. Polar-size reduction

We import the following specialized consequences of Labbé--Nevo
([arXiv:1612.01169v2](https://arxiv.org/html/1612.01169v2),
Lemmas 3.2, 3.4 and Corollary 4.3), for a flag homology
\((d-1)\)-sphere on \(2d+\ell\) vertices:

- \(1\leq\pi\leq\ell+1\); \(\pi=1\) characterizes suspensions.
  For \(d\geq3\), \(\pi=\ell+1\) forces \(\ell=0\).
- If a vertex \(v\) has exactly two antipodes \(x,y\), then \(xy\) is an
  edge and the gamma polynomials satisfy
  \(\gamma_\Delta(z)=\gamma_{\operatorname{lk}(v)}(z)
  +z\gamma_{\operatorname{lk}(xy)}(z)\).
- If \(d\geq3\) and \(\pi\geq3\), then
  \(\gamma_j(\Delta)=0\) for \(j\geq\ell-\pi+2\).

The variable \(z\) here belongs to the gamma polynomial
\(\gamma_\Delta(z)=\sum_i\gamma_i z^i\), not the h-polynomial.
Suspension preserves this polynomial because joining with \(S^0\)
multiplies \(h\) by \(1+t\).

Suppose \(\gamma_3(\Delta)<0\). Here \(d=6\) and \(\ell=5\).
If \(\pi=1\), suspension reduces to a four-dimensional sphere, whose
gamma polynomial has degree at most two, a contradiction.
If \(\pi=2\), the displayed decomposition reduces \(\gamma_3(\Delta)\)
to \(\gamma_2\) of a three-dimensional edge link, nonnegative by (2.2).
Values \(\pi=4,5\) give vanishing by the third input, and \(\pi=6\) is
excluded by \(\ell=5\ne0\). Hence
\[
\pi=3.
\tag{3.1}
\]

We also need the elementary minimum-vertex bound: a flag homology
\((s-1)\)-sphere has at least \(2s\) vertices. Induct on \(s\).
A vertex link has at least \(2(s-1)\) vertices. A vertex cannot be adjacent
to all other vertices, since flagness would then make the complex a cone,
contradicting its nonzero top reduced homology. Include that vertex and
one nonneighbor to obtain \(2s\). The base \(s=1\) is a homology 0-sphere,
which consists of two vertices.

The link of \(v\) has dimension four and \(16-q_v\) vertices. This bound
gives \(16-q_v\geq10\); together with (3.1),
\[
3\leq q_v\leq6\quad\text{for every }v.
\tag{3.2}
\]
No edge-contraction theorem or separate 16-vertex theorem is needed by
this proof. Those routes in the historical package are supplementary.

## 4. Three exact counting identities

Coefficient extraction from (1.2)--(1.3) gives, for \(n\) vertices and
\(e\) edges in dimension \(d-1\), with \(d\geq4\),
\[
\gamma_1=n-2d,\qquad
\gamma_2=e-(2d-3)n+2d(d-2).
\tag{4.1}
\]
For instance \(h_1=n-d\) and
\(h_2=e-(d-1)n+\binom d2\); equate these with the first two
gamma-basis coefficients. Thus at \(d=6,n=17\),
\(e=105+\gamma_2\) and \(m=\binom{17}{2}-e=31-\gamma_2\).
The handshaking identity gives
\[
\sum_v q_v=62-2\gamma_2.
\tag{4.2}
\]

For dimension five, differentiate (2.3) and set \(t=-1\).
The degree-five link polynomials contribute their \(\gamma_2\)'s.
For the degree-six polynomial of \(\Delta\),
\[
h'_\Delta(-1)=3\gamma_3,\qquad
h''_\Delta(-1)=2\gamma_2-6\gamma_3.
\]
The derivative of the right side of (2.3) is
\(5h'_\Delta+(1-t)h''_\Delta\). Consequently
\[
\sum_v\gamma_2(\operatorname{lk}_\Delta(v))
=3\gamma_3+4\gamma_2.
\tag{4.3}
\]
Every summand is nonnegative by (2.4).

Finally, flagness identifies 2-faces of \(\Delta\) with independent
three-sets of \(H\). Inclusion--exclusion over the missing edges gives
\[
f_2(\Delta)=\binom{17}{3}-15m+\sum_v\binom{q_v}{2}-T.
\tag{4.4}
\]
Each missing edge lies in 15 triples. Two such edges in one triple share
one vertex and are counted by \(\binom{q_v}{2}\); three form exactly one
triangle, giving the final subtraction. Equivalently a triple with \(j\)
missing edges receives weight \(1-j+\binom j2-\binom j3\), equal to one
for \(j=0\) and zero for \(j=1,2,3\).

The coefficient of \(t^3\) in the two h-expansions yields
\[
\gamma_3=f_2-6e+22n-64.
\]
Insert \(n=17\), (4.4), \(e=136-m\), and \(2m=\sum q_v\):
\[
2\gamma_3=348+\sum_vq_v(q_v-10)-2T.
\tag{4.5}
\]
These are identities for every complex in the stated class; no sampled
graph or enumeration is a premise.

## 5. The unique negative profile

Continue to suppose \(\gamma_3<0\). Integrality gives \(\gamma_3\leq-1\).
From (4.3) and link nonnegativity, \(4\gamma_2\geq-3\gamma_3\geq3\),
so \(\gamma_2\geq1\). Equations (3.2) and (4.2) give
\(51\leq62-2\gamma_2\), hence \(\gamma_2\leq5\).
Now (4.3) implies
\[
\gamma_3\geq-6.
\tag{5.1}
\]
The degree sum in (4.2) is at least 52, so at least one degree is at least
four. For integers \(3\leq q\leq6\),
\[
q(q-10)\leq-21,
\quad\text{and if }q\geq4,\quad q(q-10)\leq-24.
\]
Since \(T\geq0\), (4.5) yields
\[
2\gamma_3\leq348-16\cdot21-24=-12.
\]
Together with (5.1), this forces \(\gamma_3=-6\).
Then (4.3), nonnegativity and \(\gamma_2\leq5\) give \(\gamma_2=5\).
Equation (4.2) gives the exact excess-degree identity
\[
\sum_v(q_v-3)=1.
\tag{5.2}
\]
All summands are nonnegative integers. Thus exactly one vertex has degree
four and every other vertex has degree three. Notice that (5.2) is needed:
the quadratic bound alone gives the same value \(-24\) at degrees four and six.
Substituting this degree sequence in (4.5) forces \(T=0\).
We have proved
\[
\gamma_2=5,\qquad\gamma_3=-6,\qquad
m=26,\qquad T=0,\qquad (q_v)=3^{16}4^1.
\tag{5.3}
\]
Equation (4.3) additionally gives total vertex-link \(\gamma_2\) equal to 2.
No realization of (5.3) is asserted or required; it is a necessary condition
on a hypothetical counterexample.

## 6. The degree-four link

Let \(r\) be the unique degree-four vertex of \(H\), put \(N=N_H(r)\), and
let \(B=V(H)\setminus(\{r\}\cup N)\). Then \(|N|=4\) and \(|B|=12\).
Triangle-freeness makes \(N\) independent. Each member of \(N\) has degree
three, since \(r\) is the only degree-four vertex. Apart from its edge to
\(r\), it therefore has exactly two edges to \(B\).

All edges of \(H\) lie in the disjoint classes \(rN\), \(NB\), and \(H[B]\).
The first two classes have 4 and 8 edges. Thus
\[
|E(H[B])|=26-4-8=14.
\tag{6.1}
\]
This is the specialization of the general identity, valid when \(N_H(r)\)
is independent,
\[
|E(H)|=\deg_H(r)+
\sum_{u\in N_H(r)}(\deg_H(u)-1)+|E(H[B])|.
\tag{6.2}
\]
It is an additive decomposition into actual edge classes, so no convention
for truncated subtraction enters the count.

The vertices of \(\operatorname{lk}_\Delta(r)\) are exactly the
\(G\)-neighbors of \(r\), namely \(B\). For every \(A\subseteq B\),
\[
A\in\operatorname{lk}_\Delta(r)
\ \Longleftrightarrow\
A\cup\{r\}\in\Delta
\ \Longleftrightarrow\
A\text{ is a clique in }G[B].
\tag{6.3}
\]
The last equivalence uses flagness and all adjacencies from \(r\) to \(B\).
Thus the entire link, including its edges, is the clique complex of
\(G[B]=(H[B])^c\). Here the complement is taken on vertex set \(B\).
The link has 12 vertices and
\[
\binom{12}{2}-14=52
\]
edges. It is a flag generalized homology 4-sphere by (1.1) and the
links-of-links identity. Formula (4.1) with \(d=5\) gives
\[
\gamma_2(\operatorname{lk}_\Delta(r))
=52-7\cdot12+30=-2.
\tag{6.4}
\]
This contradicts (2.4), completing the theorem.

## 7. Exact normalization witness

Let \(C_5\) denote the five-cycle as a one-dimensional flag complex, and
let \(S^0\) consist of two isolated vertices. Their join
\(Y=C_5*C_5*S^0\) is a flag triangulation of \(S^4\).
The standard join-of-spheres fact establishes its topology; face
enumeration suffices for the following coefficients:
\[
F_Y(x)=(1+5x+5x^2)^2(1+2x)
=1+12x+55x^2+120x^3+125x^4+50x^5,
\]
\[
h_Y(t)=(1+t)(1+3t+t^2)^2,\qquad
\gamma_Y(z)=(1+z)^2.
\]
Each of the two suspension vertices has link \(C_5*C_5\), with
\(\gamma_2=1\) and \(\kappa=1/16\).
Each of the ten cycle vertices has link \(S^0*C_5*S^0\), with
\(\gamma_2=0\) and \(\kappa=0\).
Hence \(\gamma_2(Y)=1\) and the sum of link \(\kappa\)'s is \(1/8\).
This refutes precisely the reciprocal factor in the frozen audit, not
low-dimensional nonnegativity.

The standard-library script
[normalization_check.py](normalization_check.py) independently enumerates
the clique complex on these 12 labeled vertices, then computes every link,
the face and h-polynomials, and the gamma coefficients by exact integer
and rational arithmetic. It checks the complete identity (2.3) coefficient
by coefficient as well as the scalar correction. No floating point or
homology oracle is used.

## 8. Formal interfaces and reproducibility

The original project, with Lean 4.33.1 and Mathlib v4.33.1, checks the
polynomial and integer steps from supplied hypotheses. In particular:

| Declaration in namespace CharneyDavis17 | Kernel-checked conclusion | Human input |
| --- | --- | --- |
| sum_vertexLink_gammaTwo_eq | (2.3) implies (4.3) | The face-sum polynomial identity for the actual complex |
| negative_forces_polarSize_three | The polar-size case split | The published polar-size consequences |
| negative_forces_rigid_complement_profile | (5.3) and the total link coefficient | (3.2), (4.2)--(4.5), link nonnegativity, and \(T\geq0\) |
| degreeFour_linkGammaTwo_eq_negTwo | The local coefficient is \(-2\) | Numerical edge partition, complement count, and low-coefficient relation |
| negative_counterexample_impossible_from_degreeFour_link | No negative profile | The global hypotheses and a degree-four local-count implication |

The separate project
[charney_davis_neighborhood_edges](../charney_davis_neighborhood_edges)
formalizes (6.2) and the complement edge count for arbitrary finite
Mathlib simple graphs. Its declarations
degree_four_far_profile_of_triangleFree and
degree_four_far_compl_edge_count derive the exact \(12,14,52\) counts
from the triangle-free \(17,26,4,3\) graph hypotheses.
These are the bridges delivered at heights 1817 and 1829.

The two projects do not form an end-to-end Lean theorem about a simplicial
complex. The identification of actual faces and graphs, transport of
vertices to the integer kernel's Fin 17 indexing, the external topological
theorems, the field-change lemma, and the face-count identities remain
human mathematics. Equation (6.3) remains external to both projects.
The corrected factor (2.4) is proved above, not certified by the existing
Lean declarations. A complete interface inventory is in
[PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md).

From this directory, reproduce the original kernel and arithmetic checks:

~~~sh
lake clean
lake exe cache get
lake build
python3 audit_check.py
python3 normalization_check.py
shasum -a 256 -c SHA256SUMS
~~~

Then, from the repository root:

~~~sh
cd charney_davis_neighborhood_edges
lake clean
lake exe cache get
lake build
lake env lean NeighborhoodEdgeDecomposition.lean
~~~

The original audit checker reports 33,867 simple graphs through six vertices,
258 deterministic 17-vertex samples, the unique integer profile, and the
local \((14,52,-2)\) arithmetic. These finite checks corroborate the human
identities; the theorem is not inferred from the samples.
The normalization checker ends with

~~~text
result_sha256=1ec9d9fb4543b9328aff9262c2c04923961d1f15b03b23df091d1612020c3367
VERIFIED
~~~

Every integrity-manifest entry should report OK. The two Lean builds have
the declared default targets; axiom reports use only the standard
propext, Classical.choice and Quot.sound, or subsets thereof.
No custom axiom, sorry, admit, unsafe declaration, native_decide,
external data, or generated certificate occurs in the original Lean source.

## 9. Publication scope

The statement exactly matches the accepted 17-vertex graph theorem, with
the coefficient-field and all-links hypotheses explicit. The manuscript
repairs a normalization error and supplies a unified account of the
previously accepted argument and later formal graph counts. It does not
claim a new 17-vertex proof, independent reacceptance of this revised
manuscript, historical priority, or any result at 18 vertices.
The appropriate next step is expert scrutiny of this complete note and
its named human bridges.
