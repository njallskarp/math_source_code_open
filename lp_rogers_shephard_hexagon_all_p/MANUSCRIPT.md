# Equality in the planar symmetric Firey inequality

*Consolidated proof for independent review, 6 September 2026.*

**Status.** This manuscript reconstructs the proof proposed in Discovery Net
at height 1769. The strict hexagon and finite-polygon arguments have independent
accepted reviews at heights 1747 and 1757. That acceptance does not extend to
the arbitrary-measure argument. The present proof audit found no invalid
inference, but is a source-delivery audit, not independent acceptance of height
1769. The precise provenance and outstanding review obligation are recorded
in [AUDIT_MAP.md](AUDIT_MAP.md).

## Abstract

We present a proof of the equality classification in the planar symmetric
Firey inequality, relative to its known sharp upper bound. The essential
step replaces an arbitrary integrable slope measure by a measure with two
or three atoms. Every smooth approximation to this replacement is reached
by a constant-area shadow with the original body at an interior parameter.
Equality therefore propagates before taking the limit. A non-parallelogram
equality case would produce a genuine hexagon equality case, contradicting
the explicit hexagon deficit. We give the measure approximation, compact
shadow construction, continuity arguments, and origin-placement reductions
in detail, including atomic and unbounded-support measures.

## 1. Statement and imported input

A convex body is a compact convex subset of the plane with nonempty interior.
Central symmetry means symmetry about some point, which need not be the origin.
Fix a real number \(1<p<\infty\), and put
\[
q=\frac{p}{p-1},\qquad
c_q=\frac{2\Gamma(1+1/q)^2}{\Gamma(1+2/q)},\qquad C_p=2+c_q.
\]
For compact convex sets containing zero, the Firey sum is defined by
\[
h_{K+_pL}(u)=\bigl(h_K(u)^p+h_L(u)^p\bigr)^{1/p}.
\]
Write \(\Phi_p(K)=|K+_p(-K)|\) and
\(\delta_p(K)=C_p|K|-\Phi_p(K)\), where bars denote planar area.

**Theorem.** For every centrally symmetric planar convex body \(K\) with
\(0\in K\),
\[
\Phi_p(K)=C_p|K|
\quad\Longleftrightarrow\quad
K\text{ is a parallelogram with a vertex at }0.
\]

**External inequality U.** Corollary 29 of Fradelizi, Manui, Meyer and Ndiaye,
[arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1#S4),
establishes \(\delta_p(K)\geq0\) for precisely this class and gives equality
for origin-vertex parallelograms. Its Conjecture 5 asks for the converse.
We import U, including the stated equality examples.

The remaining ingredients are proved below. Sections 2 and 3 expand the
topological and shadow interfaces. Sections 4--7 expand the measure bridge.
Section 8 reconstructs the independently reviewed finite calculation, and
Section 9 completes the classification. The endpoint values \(p=1,\infty\),
degenerate bodies as equality cases, quantitative stability for arbitrary
bodies, and higher dimensions are outside the theorem.

We use the following standard foundational facts: separation by support
functions; finite-dimensional compactness and compactness of the convex hull
of a compact set; weak sequential compactness of positive measures of bounded
mass on a compact metric space; approximation of integrable functions by
simple functions; Fubini's theorem and dominated convergence; and Green's
area formula and the beta integral. Their specific uses are identified below.
No formal proof assistant or finite computation discharges these facts.

An invertible linear map \(B\) commutes with Firey addition since
\(h_{BK}(u)=h_K(B^{\mathsf T}u)\). It multiplies both areas by
\(|\det B|\). Thus linear changes of coordinates preserve equality. General
translations do not preserve \(\Phi_p\); every translation used below is
justified as a shadow.

## 2. Support functions, integrals, and continuity

For a finite positive measure \(\mu\) and an integrable vector function \(v\),
define its segment integral by
\[
Z(v,\mu)=
\overline{\left\{\int f(s)v(s)\,d\mu(s):
                f\text{ measurable},\ 0\leq f\leq1\right\}}.
\tag{2.1}
\]
The set before closure is bounded and convex. Its closure is compact and
convex, and contains zero. Choosing the indicator of
\(\{s:\langle u,v(s)\rangle>0\}\) shows
\[
h_{Z(v,\mu)}(u)=\int\langle u,v(s)\rangle_+\,d\mu(s).
\tag{2.2}
\]
It is centrally symmetric about \(\frac12\int v\,d\mu\): replace \(f\) by
\(1-f\). This construction does not require a nonatomic measure or bounded
pointwise generators.

If \(v_n\to v\) in \(L^1(\mu)\), the Lipschitz property of the positive part
gives
\[
\sup_{\|u\|_2=1}|h_{Z(v_n,\mu)}(u)-h_{Z(v,\mu)}(u)|
\leq\int\|v_n-v\|_2\,d\mu.
\tag{2.3}
\]
For nonempty compact convex sets, uniform convergence of supports on the
unit circle is Hausdorff convergence. Indeed a support error at most
\(\eta\) is equivalent, by separation, to the two inclusions into the other
set plus the Euclidean disk of radius \(\eta\).

Here is the area-continuity fact needed even for intermediate degenerate
approximants. Suppose \(L_n\to L\) in Hausdorff distance. If \(L\) has an
interior point \(z\) and \(z+\rho B_2\subset L\), an error \(\eta<\rho\)
in the supports gives, after subtracting \(z\),
\[
(1-\eta/\rho)(L-z)\subset L_n-z
 \subset(1+\eta/\rho)(L-z).
\tag{2.4}
\]
Both inclusions follow by comparing supports, using \(h_{L-z}\geq\rho\).
Area monotonicity and scaling imply \(|L_n|\to|L|\). If \(L\) is a segment
or a point, its \(\eta\)-neighborhood lies in a rectangle whose area tends
to zero, and the same conclusion follows.

For \(L_n,L\) containing zero and support error at most \(\eta\), the reverse
triangle inequality for the \(\ell_p\) norm gives
\[
\sup_{\|u\|_2=1}
 |h_{L_n+_p(-L_n)}(u)-h_{L+_p(-L)}(u)|
\leq 2^{1/p}\eta.
\tag{2.5}
\]
Consequently both \(|L|\) and \(\Phi_p(L)\) are continuous in every limit
used here. The parameter \(p\) remains fixed.

## 3. Compact shadows and propagation of equality

We give the required planar shadow facts directly. This also checks the
arbitrary-index and bounded-speed hypotheses in the usual formulation.
For a compact convex set \(D\subset\mathbb R^3\), define
\[
\pi_t(x,y,z)=(x+tz,y),\qquad L_t=\pi_tD.
\]
For each \(y\) in the fixed projection of \(D\) to its second coordinate,
the right and left endpoints of the horizontal section of \(L_t\) are
\[
b_t(y)=\max_{(x,y,z)\in D}(x+tz),\qquad
a_t(y)=\min_{(x,y,z)\in D}(x+tz).
\]
The first is convex in \(t\), the second concave. Fubini's theorem yields
\[
|L_t|=\int\bigl(b_t(y)-a_t(y)\bigr)\,dy,
\]
so the area is convex in \(t\). Compactness supplies bounded, measurable
sections and finite integrals on every bounded parameter interval.
The lift \(D\) need not have three-dimensional interior.

If \(0\in L_t\) throughout an interval, the Firey difference bodies are
also projections of one compact convex set. Put
\[
E=\operatorname{conv}\{\alpha d-\beta e:
 d,e\in D,\ \alpha,\beta\geq0,\ \alpha^q+\beta^q\leq1\}.
\tag{3.1}
\]
The set inside the convex hull is compact, and so is \(E\). At a planar
normal \(u\), its projected support is
\[
h_{\pi_tE}(u)=
\max_{\substack{\alpha,\beta\geq0\\\alpha^q+\beta^q\leq1}}
\bigl(\alpha h_{L_t}(u)+\beta h_{L_t}(-u)\bigr)
=h_{L_t+_p(-L_t)}(u).
\tag{3.2}
\]
The final equality is finite-dimensional Hölder duality, with both support
values nonnegative because \(0\in L_t\).
Thus \(\Phi_p(L_t)=|\pi_tE|\) is convex.

These are the planar instances of the classical shadow-volume theorem and
Firey closure; compare Bianchini and Colesanti,
[arXiv:math/0702102v1](https://arxiv.org/pdf/math/0702102v1),
Section 2, Theorems 2.2 and 2.3. Their linear-parameter definition allows
an arbitrary index set but requires bounded positions and speeds. The compact
lifts constructed here satisfy that requirement. A unique speed for each
projected point is not needed.

**Equality propagation.** Suppose that \(L_t=\pi_tD\) is centrally symmetric,
contains zero, and has the same positive area \(V\) for all \(t\in[a,b]\),
where \(a<0<b\). If \(\delta_p(L_0)=0\), then
\[
\Phi_p(L_t)=C_pV\quad\text{for every }t\in[a,b].
\tag{3.3}
\]
Indeed U bounds the convex function \(\Phi_p(L_t)\) above by \(C_pV\).
For any parameter on either side of zero, combine it with a parameter on
the other side so that zero is their strict convex combination. Equality
at zero forces both values to equal the upper bound. This also proves the
claim for endpoints. No strict convexity is used.

Translations fit this construction. For \(L_t=L+tw\), rotate \(w\) to the
horizontal direction and use the compact lift with constant third coordinate
equal to the translation speed. It is unnecessary for that lift to contain
the three-dimensional origin; equation (3.2) uses only \(0\in L_t\).

## 4. One-sided generators at an exposed-face endpoint

We first justify the planar segment representation without an unmentioned
assumption on the placement of zero.

Every centrally symmetric polygon is, up to translation, the Minkowski sum
of its consecutive edge segments along half of its boundary. Opposite
boundary edges have opposite vectors, so the polygon and that zonotope
have the same cyclic list of edge vectors and differ only by translation.
If the polygon contains zero, write it as
\(b+\sum_i[0,v_i]\), choose \(s_i\in[0,1]\) with
\(b+\sum_i s_iv_i=0\), and obtain
\[
\sum_i[-s_iv_i,(1-s_i)v_i]
=\sum_i\bigl([0,-s_iv_i]+[0,(1-s_i)v_i]\bigr).
\tag{4.1}
\]
Zero-length segments may be discarded. Thus its support has the form
\(\int_{S^1}\langle u,v\rangle_+\,d\mu(v)\) for a finite positive measure.

For an arbitrary centrally symmetric body with center \(c\), take finite
increasing dense subsets of \(K\), include their reflections about \(c\),
and include \(0,2c\). Their convex hulls are centrally symmetric polygons
containing zero, eventually full-dimensional, and converge to \(K\).
All lie in a disk of radius \(R\) about zero. For their measures \(\mu_n\),
integration over the unit circle with arc-length measure gives
\[
2\mu_n(S^1)=\int_{S^1}h_{P_n}(u)\,du\leq2\pi R,
\tag{4.2}
\]
since the integral of \(\langle u,v\rangle_+\) over \(u\in S^1\) is 2.
Weak compactness of bounded positive measures on \(S^1\) supplies a
subsequence with limit \(\mu\). The continuous integrands at each fixed
normal give
\[
h_K(u)=\int_{S^1}\langle u,v\rangle_+\,d\mu(v).
\tag{4.3}
\]
Here polygonal approximation establishes a representation only; it makes
no assertion about passage of strict inequalities.

Now suppose that zero is an endpoint of an exposed face of \(K\), allowing
a singleton face. Choose a supporting line through zero to be horizontal
with \(K\subset\{y\geq0\}\). In (4.3),
\[
0=h_K(-e_2)=\int_{S^1}(-v_2)_+\,d\mu(v)
\]
forces \(v_2\geq0\) almost everywhere. If both horizontal directions had
positive mass, their segments would put zero inside a nontrivial segment
of \(K\). This contradicts that a face endpoint is an extreme point.
Reflect the horizontal axis if necessary; the horizontal mass is therefore
one segment \([0,he_1]\), \(h\geq0\).

On \(v_2>0\), put \(r=v_1/v_2\) and define \(\nu\) as the pushforward of
the measure \(v_2\,d\mu(v)\). It follows that
\[
K=[0,he_1]+Z((r,1),\nu),\qquad
M:=\nu(\mathbb R)>0,\qquad
\int(1+|r|)\,d\nu(r)<\infty.
\tag{4.4}
\]
In fact \(M=\int_{v_2>0}v_2\,d\mu\) and
\(\int|r|\,d\nu=\int_{v_2>0}|v_1|\,d\mu\).
The strict inequality \(M>0\) follows from full dimension. Slopes can be
unbounded; no angular gap from the supporting line was assumed.

## 5. The exact area functional

For a positive measure \(\nu\) as in (4.4) and an integrable real function
\(R\), set
\[
\mathcal A_\nu(R)=\frac12\iint|R(r)-R(s)|\,d\nu(r)\,d\nu(s).
\]
This is finite, and the triangle inequality gives the useful bound
\[
|\mathcal A_\nu(R)-\mathcal A_\nu(S)|
\leq M\int|R-S|\,d\nu.
\tag{5.1}
\]
The determinant formula for a finite planar zonotope gives, for simple \(R\),
\[
\left|[0,he_1]+Z((R,1),\nu)\right|
=hM+\mathcal A_\nu(R).
\tag{5.2}
\]
One way to see the finite determinant formula is to add segments successively:
adding \([0,v]\) increases area by the length of \(v\) times the width of
the existing zonotope perpendicular to \(v\). Widths add, giving
\(\sum_{i<j}|\det(v_i,v_j)|\).

Approximate an arbitrary integrable \(R\) by simple functions in \(L^1(\nu)\).
Equation (2.3) gives support convergence, Section 2 gives area convergence,
and (5.1) gives convergence of the right side of (5.2). Thus (5.2) holds
for arbitrary \(R\). In particular, with \(\mathrm{id}(r)=r\),
\[
D:=\mathcal A_\nu(\mathrm{id}),\qquad |K|=D+hM.
\tag{5.3}
\]
The condition \(D=0\) means that \(\nu\) is concentrated at one point:
otherwise two separated neighborhoods of distinct support points have
positive mass and contribute positively to the double integral. Full
dimension then forces \(h>0\), and (4.4) is an origin-vertex parallelogram.
If \(h=0\) and the support consists of two points, (4.4) is again such a
parallelogram. Consequently any remaining shape in (4.4) has \(D>0\)
and at least three support points when \(h=0\), or at least two when \(h>0\).

## 6. Quantization for arbitrary finite measures

**Lemma.** Suppose \(D>0\) and \(\operatorname{supp}\nu\) contains at least
\(k\geq2\) points. There exist bounded nondecreasing Lipschitz functions
\(T_n:\mathbb R\to\mathbb R\) such that
\[
\mathcal A_\nu(T_n)=D,\qquad T_n\longrightarrow T
\quad\text{in }L^1(\nu),
\tag{6.1}
\]
where \(T\) has exactly \(k\) distinct, ordered levels, each on a set of
positive measure.

**Proof.** Choose \(k\) distinct support points in increasing order and
small disjoint neighborhoods of them. Each neighborhood has positive mass.
Choose one cut between each consecutive pair of neighborhoods, avoiding
the countable set of atoms of \(\nu\). The cuts define ordered intervals
\(I_1,\ldots,I_k\), all of positive masses \(m_j\).
Their endpoints have zero mass, so their assignment to adjacent intervals
does not matter.

Choose \(q_1<\cdots<q_k\), and let \(Q=q_j\) on \(I_j\). Then
\[
d:=\mathcal A_\nu(Q)
=\sum_{i<j}m_im_j(q_j-q_i)>0.
\tag{6.2}
\]
Replace each jump by a linear ramp on a shrinking neighborhood of its cut.
Take the neighborhoods disjoint. The resulting \(Q_n\) are bounded between
\(q_1\) and \(q_k\), nondecreasing and Lipschitz, and converge pointwise off
the cuts to \(Q\). Dominated convergence for the finite measure \(\nu\)
gives \(Q_n\to Q\) in \(L^1(\nu)\), including when \(\nu\) has atoms,
a singular continuous part, or unbounded support.

By (5.1), \(d_n:=\mathcal A_\nu(Q_n)\to d>0\).
Discard finitely many indices so that \(d_n>0\), and set
\[
\gamma_n=D/d_n,\qquad T_n=\gamma_nQ_n,\qquad
\gamma=D/d,\qquad T=\gamma Q.
\tag{6.3}
\]
Positive homogeneity of \(\mathcal A_\nu\) gives (6.1). Moreover
\[
\|T_n-T\|_{L^1(\nu)}
\leq|\gamma_n|\|Q_n-Q\|_{L^1(\nu)}
  +|\gamma_n-\gamma|\|Q\|_{L^1(\nu)}
\longrightarrow0.
\]
The limiting levels \(\gamma q_j\) remain distinct and retain masses \(m_j\).
This proves the lemma.

For each \(n\), let \(L_n\) be a Lipschitz constant of the **rescaled**
function \(T_n\). Put
\[
\varepsilon_n=\frac1{2(1+L_n)},\qquad
S_{n,t}(r)=(1-t)r+tT_n(r),\qquad -\varepsilon_n\leq t\leq1.
\tag{6.4}
\]
These maps preserve order. For \(r<s\) and negative \(t\),
\[
S_{n,t}(s)-S_{n,t}(r)
\geq (1-t+tL_n)(s-r)>0.
\tag{6.5}
\]
The coefficient is positive at both ends of the negative interval; at
\(-\varepsilon_n\) it is \((3+L_n)/(2(1+L_n))\).
For \(0\leq t\leq1\), monotonicity follows by convex combination.
For every ordered pair of slopes the absolute difference therefore has
the same sign throughout, and Fubini yields
\[
\mathcal A_\nu(S_{n,t})
=(1-t)\mathcal A_\nu(\mathrm{id})+t\mathcal A_\nu(T_n)
=D.
\tag{6.6}
\]
The first equality is valid also for negative \(t\), precisely because of
(6.5).

## 7. Compact realization and passage of equality

For a fixed \(n\), take the closure in \(\mathbb R^3\) of the set of points
\[
\left(
 ah+\int f(r)r\,d\nu,\quad
 \int f(r)\,d\nu,\quad
 \int f(r)(T_n(r)-r)\,d\nu
\right),
\quad 0\leq a\leq1,\quad0\leq f\leq1,
\tag{7.1}
\]
with \(f\) measurable, and call it \(D_n\).
It is convex and bounded, since the absolute values of its three coordinates
are bounded respectively by
\[
h+\int|r|\,d\nu,\qquad M,\qquad
\int|T_n-r|\,d\nu<\infty.
\tag{7.2}
\]
Thus \(D_n\) is compact. Projection and (2.2) identify
\[
K_{n,t}:=\pi_tD_n
=[0,he_1]+Z((S_{n,t},1),\nu).
\tag{7.3}
\]
For clarity, projection of the closure in (7.1) equals the closure of the
projected set: one inclusion is continuity, and the other follows by
extracting a convergent subsequence in the bounded lifted set. Hence no
unproved closedness of an infinite selector image is required.

Every \(K_{n,t}\) is centrally symmetric and contains zero by Section 2.
Equations (5.2) and (6.6) give
\[
|K_{n,t}|=hM+D=|K|>0,\qquad K_{n,0}=K.
\tag{7.4}
\]
Positive area ensures full dimension for every parameter, including both
endpoints. Thus all hypotheses of U and equality propagation hold.
If \(K\) is an equality case, then so is \(K_{n,1}\) for every \(n\).

Write \(t_j=\gamma q_j\), and define
\[
K_T=[0,he_1]+\sum_{j=1}^k[0,m_j(t_j,1)].
\tag{7.5}
\]
Equation (2.3) gives the explicit estimate
\[
\sup_{\|u\|_2=1}|h_{K_{n,1}}(u)-h_{K_T}(u)|
\leq\int|T_n-T|\,d\nu\longrightarrow0.
\tag{7.6}
\]
Equations (2.4)--(2.5) now pass equality to \(K_T\), and (5.1) ensures
that its area is still \(hM+D>0\).

The order of quantifiers matters. For each \(n\), the negative interval is
nonempty and equality propagates from zero to one. We then take the limit
of the equality endpoints. There is no requirement that
\(\inf_n\varepsilon_n>0\), no limit of the shadows at negative times,
and no passage of a positive deficit through polygonal approximation.

If \(h=0\), choose \(k=3\); if \(h>0\), choose \(k=2\). In either case (7.5)
has exactly three nonzero, pairwise nonparallel generators. Distinct finite
slopes give nonzero determinants, and a horizontal generator is independent
of each \((t_j,1)\).
When \(h=0\), the functional \(y\) is strictly positive on all generators.
When \(h>0\), choose \(c>-\min_j t_j\); the functional \(x+cy\) is strictly
positive on all generators. Thus zero is an exposed vertex in both cases.
The finite zonotope has precisely six sides: each of its three distinct
generator directions occurs as a pair of opposite edges. It is a genuine
origin-vertex centrally symmetric hexagon.

## 8. The finite strictness input

We reproduce the load-bearing part of the accepted finite chain here. The
full original calculations remain in
[FIREY_HEXAGON_ALL_P.md](FIREY_HEXAGON_ALL_P.md) and
[SYMMETRIC_POLYGON_EQUALITY.md](SYMMETRIC_POLYGON_EQUALITY.md).

### 8.1. Hexagons

Every origin-vertex centrally symmetric hexagon is a sum of three segments
whose generators lie in a pointed cone. Map the two extreme generators to
\(e_1,e_2\). The middle generator becomes \((a,b)\) with \(a,b>0\); hence
\[
H(a,b)=[0,e_1]+[0,(a,b)]+[0,e_2],\qquad |H(a,b)|=1+a+b.
\]
Set
\[
\ell=(a^p+b^p)^{1/p},\quad t=a/\ell,\quad u=b/\ell,\quad
\alpha=t^{p-1},\quad\beta=u^{p-1}.
\]
On the first-quadrant \(\ell_q\) unit arc, let \(S\) be the oriented integral
of \(x\,dy-y\,dx\) from \((1,0)\) to \((\alpha,\beta)\).
The full arc integral is \(c_q\), by Green's formula and the beta integral.

For completeness, put \(A=1+a\), \(B=1+b\), and
\[
V=(A,B),\quad X=(a,B),\quad Y=(-1,0),\quad
X'=(0,1),\quad Y'=(-A,-b),\quad
P=\alpha X+\beta Y,\quad Q=\alpha X'+\beta Y'.
\]
As the outer normal traverses the upper half-circle, the positively
oriented half-boundary of the Firey difference body consists of the
following pieces. The last column is the integral of \(\det(z,dz)\).

| Piece | Contribution |
| --- | --- |
| Segment \(V\) to \(X\) | \(B\) |
| Arc \(xX+yY\), coefficients \((1,0)\) to \((\alpha,\beta)\) | \(BS\) |
| Segment \(P\) to \(Q\) | \(\ell(\alpha+\beta)\) |
| Arc \(xX'+yY'\), coefficients \((\alpha,\beta)\) to \((0,1)\) | \(A(c_q-S)\) |
| Segment \(Y'\) to \(-V\) | \(A\) |

Here the three open normal sectors have exposed-point pairs
\((V,0)\), \((X,Y)\), and \((X',Y')\), with transitions at
\(\pi/2\) and \(\pi/2+\arctan(b/a)\). On a sector with positive supports,
differentiating the Firey support gives the point \(xX+yY\) with
\(x^q+y^q=1\). Its determinant integral is
\(\det(X,Y)\int(x\,dy-y\,dx)\). At the middle transition the exposed
faces of both summands are parallel; their positive weighted Minkowski
sum is exactly the segment \(P Q\). This accounts for the face as well
as the two arcs. Direct calculation gives
\[
\det(P,Q)=(\alpha+\beta)(a\alpha+b\beta)
=\ell(\alpha+\beta).
\]
The whole difference body is symmetric about zero, so the factor \(1/2\)
in Green's area formula cancels the two congruent halves. Thus
\[
\Phi_p(H)=A+B+\ell(\alpha+\beta)+BS+A(c_q-S),
\]
and its deficit is
\[
\Delta_p(a,b)
=a+b-\ell(\alpha+\beta)+aS+b(c_q-S).
\tag{8.1}
\]

To prove positivity for every \(p>1\), regard
\[
\alpha=(1-\beta^q)^{1/q},\quad
t=\alpha^{q-1},\quad u=\beta^{q-1},\quad
F(\beta)=\Delta_p(a,b)/\ell
=t+u-\alpha-\beta+tS+u(c_q-S).
\]
For \(0<\beta<1\), differentiation gives
\[
S'(\beta)=1/t,\qquad
F'(\beta)=(q-1)\beta^{q-2}
\left[(1+c_q-S)-\frac{\beta}{\alpha}(1+S)\right].
\tag{8.2}
\]
For example \(S'=\alpha-\beta\alpha'=1/t\), since
\(\alpha'=-u/t\) and \(t\alpha+u\beta=1\); substitution gives the second
identity. The ratio \(\beta/\alpha\) increases strictly from zero to infinity,
whereas \((1+c_q-S)/(1+S)\) decreases strictly from \(1+c_q\) to
\(1/(1+c_q)\). The derivative changes sign exactly once, from positive to
negative. Continuity gives \(F(0)=F(1)=0\), whence
\[
\Delta_p(a,b)>0\qquad(a,b>0).
\tag{8.3}
\]
All differentiations occur on the open interval; only continuous limits are
used at its endpoints, including when a derivative has an endpoint singularity.

### 8.2. Edge-interior parallelograms

An origin in the relative interior of an edge of a parallelogram can be
normalized by an invertible linear map to
\[
P_a=[-a,1-a]\times[0,1],\qquad 0<a<1.
\]
Put \(A=1-a\), and use \(\ell,\alpha,\beta,S\) as above for the pair \((A,a)\).
The two open upper normal quadrants have exposed-point pairs
\(((A,1),(a,0))\) and \(((-a,1),(-A,0))\).
Their arcs contribute respectively \(aS\) and \(A(c_q-S)\):
the first has determinant \(-a\) and the reversed coefficient arc.
The top face contributes 1. The closing face at horizontal coordinate
\(-\ell\) runs from height \(\beta\) to height \(-\alpha\), contributing
\(\ell(\alpha+\beta)\). The same half-boundary area formula therefore gives
\[
\Phi_p(P_a)=1+\ell(\alpha+\beta)+aS+A(c_q-S).
\]
Since \(|P_a|=1\), subtraction yields the exact identity
\[
\delta_p(P_a)=
1-\ell(\alpha+\beta)+AS+a(c_q-S)
=\Delta_p(A,a)>0.
\tag{8.4}
\]

## 9. Completion for every shape and origin placement

Suppose first that an equality body has zero at an exposed-face endpoint.
Section 4 gives (4.4). If \(D=0\), or if \(h=0\) and there are only two
support points, Section 5 already identifies an origin-vertex parallelogram.
All other cases admit the construction in Sections 6 and 7. It produces an
equality hexagon, contradicting (8.3). Thus the endpoint case is complete.

Now start with any equality body. If zero is interior, fix a nonzero vector
\(w\) and take the maximal closed interval of parameters for which
\(0\in K+tw\). It is bounded and contains zero in its interior, since
\(-tw\in K\). Its endpoints put zero on the boundary. These translates have
the same area and central symmetry, so (3.3) propagates equality to both
boundary placements.

At a boundary placement, choose a supporting line through zero. Its exposed
face is either a point or a segment. If zero is already an endpoint, use
the endpoint conclusion. Otherwise zero is in the relative interior of
that segment. Translate parallel to the face over its maximal interval
while retaining zero. Equality again propagates to both endpoints.
Thus a translate of the original body is an origin-vertex parallelogram,
and the original underlying shape is a parallelogram.

This last shape conclusion precedes any use of generic edge contacts.
An edge-interior placement of a parallelogram is excluded by (8.4).
If zero is interior to the parallelogram, choose a line through zero
avoiding its four vertices. The endpoints of its chord lie in edge interiors.
Translating along that line and applying (3.3) would give equality at these
already excluded placements. Hence zero must be a vertex.
The converse is the equality example in U. This proves the theorem.

## 10. Scope, review, and reproducibility

The constant-area property (6.6), compactness (7.1)--(7.2), propagation
(3.3), and support estimate (7.6) compose without any uniform deletion
factor or uniform negative time interval. In particular no nonpolygonal
body is declared strict merely because all its approximating polygons are
strict. The limit in Section 7 is a limit of exact equality bodies.

The accepted finite-polygon theorem can also be recovered by generator
deletion as in the original source. That induction is not required by the
present proof: the continuum construction reaches the same reviewed
hexagon obstruction directly. The only finite inputs used are (8.3) and
(8.4), whose calculations are included above.

The existing Python checker verifies two continuous uniform-measure models
using exact rational arithmetic. It supplies reproducible examples of the
identities, not verification of arbitrary measures, convex geometry,
Green integrals, the imported upper bound, or this theorem. Under
CPython 3.12.12, from this directory run:

~~~sh
python3 verify_zonoid_quantization.py
shasum -a 256 -c SHA256SUMS
~~~

Expected checker ending:

~~~text
result_sha256=e0a90164ffd457f60d55c805af0ca31d1a038310b1ffad96fae7f8ed6cfed398
VERIFIED
~~~

All entries in the integrity manifest should report OK. The original proof
and checker bytes pinned by height 1769 are retained unchanged. This
manuscript supplies an end-to-end proof audit and expanded exposition; it
does not create a new equality theorem beyond that artifact or confer an
independent review verdict.
