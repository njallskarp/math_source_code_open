# Independent review of the Firey equality classification for symmetric polygons

## Target and verdict

Target: `bafkreia5tvsipltq7nhjsz6j5m5jxbfk4cxibvunlaq3bvjygtpr3veraa`,
**Firey equality cases among centrally symmetric polygons are exactly
origin-vertex parallelograms**.

**Verdict: correct in its stated polygonal scope, with high confidence.**  For
every \(1<p<\infty\), the argument correctly proves that a full-dimensional
centrally symmetric planar polygon \(K\) containing the origin satisfies

\[
 |K+_p(-K)|=(2+c_q)|K|,
 \qquad
 c_q=\frac{2\Gamma(1+1/q)^2}{\Gamma(1+2/q)},
 \qquad q=\frac p{p-1},
\]

if and only if \(K\) is a parallelogram and the origin is one of its vertices.
The proof does not settle the equality classification for nonpolygonal
centrally symmetric bodies.

The new generator-deletion induction, the equality-propagation argument, the
translated-parallelogram calculation, and the reduction of all origin
placements were checked independently.  The strict three-generator base case
is inherited from the target's dependency
`bafkreiheholqeo36ftoxx55wz6ofwuklfwehvkpymxdr2kebeh2bnpa7y4`; I checked its
use and parameter matching but did not repeat the prior complete
support-boundary derivation.

## Mathematical audit

### Origin-vertex normal form and deletion shadow

If an origin-vertex centrally symmetric polygon has \(2m\) sides, its first
half-boundary edge vectors give the minimal zonotope representation

\[
 K=\sum_{i=1}^m[0,v_i].
\]

After an invertible linear normalization, one may take
\(v_1=e_1\), \(v_i=(x_i,y_i)\) with \(x_i,y_i>0\) for \(2\le i<m\), and
\(v_m=(0,y_m)\).  The distinct directions are in increasing slope order, so
all pair determinants are positive where required.  With

\[
 Y=\sum_{i=2}^m y_i,
 \qquad
 Q=\sum_{2\le i<j\le m}\det(v_i,v_j),
 \qquad
 \lambda=Q/Y>0,
\]

define, for \(-1/\lambda\le s\le1\),

\[
 w_1(s)=(1+\lambda s)e_1,
 \qquad
 w_i(s)=((1-s)x_i,y_i),
 \qquad
 K_s=\sum_i[0,w_i(s)].
\]

Every subset-sum vertex moves affinely parallel to \(e_1\), so \(K_s\) is a
shadow system.  Direct determinant expansion gives

\[
 |K_s|=(1+\lambda s)Y+(1-s)Q=Y+Q.
\]

At \(s=-1/\lambda\), exactly the first generator vanishes.  The common
positive rescaling of the other horizontal coordinates preserves all their
distinct slopes, hence the endpoint is full dimensional and has exactly
\(2(m-1)\) sides.  At \(s=1\), the remaining generators are parallel to
\(e_2\), so that endpoint is a parallelogram.  This verifies the degeneracy,
orientation, and side-count claims, including the boundary case \(m=3\).

### Equality propagation

The cited primary source proves that the Firey sum of two shadow systems is a
shadow system and that its volume is convex in the parameter.  Since
\(-K_s\) is also a shadow system along \(e_1\),

\[
 F(s)=|K_s+_p(-K_s)|
\]

is convex.  Every \(K_s\) remains full dimensional, centrally symmetric, and
contains the origin, so the sharp global inequality applies throughout the
closed interval and gives the common upper bound
\(F(s)\le(2+c_q)(Y+Q)\).

The parameter \(s=0\) is interior.  If equality holds there, convexity forces
equality everywhere: for any point on either side of zero, pair it with a
point on the other side and apply the convexity inequality at zero; both
endpoint values are already bounded above by the same constant.  In
particular, equality propagates to the deletion endpoint.  Iteration reaches
a genuine three-generator hexagon, contradicting the strict all-\(p\)
hexagon theorem.  Thus an origin-vertex equality polygon has exactly two
generator directions.  Conversely, the cited primary paper computes equality
for every origin-vertex parallelogram.

### Other origin placements

For a parallelogram with the origin in the relative interior of an edge,
affine invariance reduces to

\[
 P_a=[-a,1-a]\times[0,1],\qquad 0<a<1.
\]

Writing \(A=1-a\), \(L=(A^p+a^p)^{1/p}\),
\(\alpha=(A/L)^{p-1}\), \(\beta=(a/L)^{p-1}\), and letting \(S\) be the
first-quadrant \(\ell_q\)-arc integral from \((1,0)\) to
\((\alpha,\beta)\), direct exposure of the two upper mixed sectors gives

\[
 |P_a+_p(-P_a)|=1+L(\alpha+\beta)+aS+A(c_q-S).
\]

The three intervening face determinants are respectively \(1\),
\(L(\alpha+\beta)\), and the two arc coefficients \(a,A\); orientations and
the exchange \((\alpha,\beta)\leftrightarrow(\beta,\alpha)\) give exactly the
displayed signs.  Consequently the deficit is

\[
 1-L(\alpha+\beta)+AS+a(c_q-S)=\Delta_p(A,a)>0,
\]

which is precisely the verified strict hexagon deficit with both parameters
positive.

If the origin is in an edge interior of an arbitrary polygon, translation
along the edge gives a constant-area shadow with origin-vertex endpoints.
Equality at the interior parameter would propagate to those endpoints, so
the origin-vertex classification would force the shape to be a
parallelogram; the preceding formula rules that out.  If the origin is in the
interior of \(K\), choose a line avoiding the finitely many vertex directions.
The maximal translation interval has edge-interior boundary placements, and
the same propagation gives a contradiction.  These cases exhaust
\(0\in K\).

## A quantitative refinement

The same deformation proves more than qualitative equality propagation.  Put

\[
 \delta_s=(2+c_q)(Y+Q)-F(s).
\]

The right endpoint \(K_1\) is an origin-vertex parallelogram, so
\(\delta_1=0\).  Since

\[
 0=\frac{\lambda}{1+\lambda}\left(-\frac1\lambda\right)
   +\frac1{1+\lambda}\cdot1,
\]

convexity yields the proved refinement

\[
 \boxed{\displaystyle
 \delta_0\ge\frac{\lambda}{1+\lambda}\,
 \delta_{-1/\lambda}.}
\]

Iterating gives a product-weighted lower bound by the final hexagon deficit.
This is not yet a uniform stability theorem because the successive
\(\lambda\)-factors can degenerate.

## Reproducibility

The standard-library checker `independent_check.py` has two independent
layers:

1. exact `fractions.Fraction` enumeration of every zonotope subset sum for a
   hexagon and an irregular octagon, confirming the determinant area formula,
   five constant-area probes, and the exact endpoint side counts; and
2. a definition-level floating-point reconstruction of Firey bodies as
   polars of convex hulls of \(n/h(n)\), using 32,768 support directions per
   body.  It compares the translated-parallelogram formula at nine
   \((p,a)\)-pairs and checks sampled deletion-shadow convexity and the strict
   bound away from equality endpoints.

Run under CPython 3.12.12 with no third-party packages:

```sh
shasum -a 256 -c SHA256SUMS && python3 independent_check.py --normals 32768
```

The two manifest entries print `OK`, and the compact output ends with

```text
worst_edge_relative_error=3.655692804152e-08
result_sha256=864ac801014b7d8910097a368efa54abc1914cf2efde939cd70484478d47a7d8
VERIFIED
```

The exact layer reports constant areas `5/2` and `49/10` and side-count
transitions `6 -> 4` and `8 -> 6` at the deletion endpoint.

## Literature, novelty, and publication readiness

Fradelizi, Manui, Meyer, and Ndiaye,
[*L_p-Rogers--Shephard type inequalities for L_p-zonoids and symmetric
bodies*](https://arxiv.org/abs/2607.03582), arXiv:2607.03582v1, prove the
sharp planar inequality in Corollary 29, establish equality for
origin-vertex parallelograms, and state uniqueness as Conjecture 5.  Their
Section 4 explicitly supplies the Firey shadow-closure and convex-volume facts
used here.  Candidate-specific searches for the exact equality
classification, polygonal induction, and origin-placement formula found no
primary-source solution beyond that conjecture.  This supports graph-level
novelty and “apparently new to the searched sources,” not a priority claim.

The finite-polygon theorem is ready for conventional expert circulation after
copy-editing.  It is a human convex-geometric proof, not a formal theorem, and
should not be advertised as resolving the nonpolygonal case.

## Strengthening and improvement opportunities

1. **Proved here; immediate:** include the quantitative deletion inequality
   \(\delta_0\ge\lambda(1+\lambda)^{-1}\delta_-\).  It isolates exactly what
   must be controlled for polygonal stability.
2. **Highest impact; open:** extend equality uniqueness from polygons to all
   centrally symmetric planar convex bodies.  Polygonal approximation alone
   loses strictness.  A viable bridge would be a uniform lower bound on the
   product-weighted hexagon deficit in terms of a compactness-normalized
   distance from the origin-vertex parallelogram class.
3. **High value; feasible:** derive a quantitative stability theorem for
   polygons under a nondegeneracy hypothesis bounding the deletion factors
   \(\lambda_j\) away from zero.  Iterating the boxed inequality and the sharp
   hexagon stability bound would then give an explicit deficit.
4. **Moderate value:** formalize the planar zonotope normal form, exact
   determinant deformation, the elementary convex maximum lemma, and the
   translated-parallelogram boundary calculation.  The remaining imported
   theorem would be the established Firey shadow-closure/volume-convexity
   result.

## Trust boundary

The acceptance rests on a human audit of the zonotope normal form, the exact
determinant identities, the primary-source shadow theorems, the elementary
convexity argument, and the previously reviewed strict hexagon base case.
The Python exact layer checks only two rational examples, and the
support-halfplane layer uses IEEE-754 arithmetic and is falsification evidence,
not a proof.  No solver, random input, external dataset, private workspace,
generated certificate, or omitted large artifact is used.
