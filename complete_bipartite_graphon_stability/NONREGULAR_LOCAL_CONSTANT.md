# The sharp unrestricted local constant for complete-bipartite forcing

## Statement

Fix integers `s,t>=2` and `0<p<1`, and put

\[
 e=st,\qquad
 A=s\binom t2+t\binom s2,\qquad
 N=\binom s2\binom t2.                                  \tag{1}
\]

For `0<=x<=1`, define

\[
 E_v(x)=6^e x+e2^{e-1}x^2,
 \qquad
 E_4(x)=(2^e+e2^{e-1})x^2.                              \tag{2}
\]

Let `W:[0,1]^2->[0,1]` be a symmetric graphon of edge density `p`.
Write `F=W-p`, let

\[
 a(x)=\int_0^1F(x,y)\,dy,\qquad
 v=\int_0^1a(x)^2\,dx,                                  \tag{3}
\]

and make the canonical degree--regular decomposition

\[
 D(x,y)=a(x)+a(y),\qquad U=F-D.                         \tag{4}
\]

Then `T_U1=0`.  Put

\[
 z=t(C_4,U),\qquad
 h=\max\{\lVert U\rVert_\infty,\lVert a\rVert_\infty\},
 \qquad x=h/p.                                           \tag{5}
\]

If `x<=1` and

\[
 \delta=t(K_{s,t},W)-p^e,
\]

then the following uniform two-component expansion holds:

\[
\boxed{
 \left|\delta-Ap^{e-2}v-Np^{e-4}z\right|
 \le E_v(x)p^{e-2}v+E_4(x)p^{e-4}z.}                    \tag{6}
\]

The constants in (2) are deliberately coarse but completely explicit.  The
point is their orders: the degree error is `O(x)` and the regular-four-cycle
error is `O(x^2)`, uniformly over all graphons in the neighborhood.

Moreover,

\[
 \lVert F\rVert_\square
 \leq \frac14z^{1/4}+\sqrt v.                            \tag{7}
\]

Consequently, whenever `E_v(x)<A` and `E_4(x)<N`,

\[
\boxed{
 \lVert W-p\rVert_\square
 \leq
 \frac{\delta^{1/4}}
 {4[N-E_4(x)]^{1/4}p^{(e-4)/4}}
 +
 \frac{\delta^{1/2}}
 {[A-E_v(x)]^{1/2}p^{(e-2)/2}}.}                        \tag{8}
\]

This determines the sharp local constant without a regularity assumption.
Let

\[
 \mathcal C^{\rm all}_{s,t,p}(r)=
 \sup_W
 \frac{\lVert W-p\rVert_\square}
 {[t(K_{s,t},W)-p^e]^{1/4}},                             \tag{9}
\]

where the supremum is over nonconstant symmetric graphons of edge density
`p` satisfying `||W-p||_infinity<=rp`.  Then

\[
\boxed{
 \lim_{r\downarrow0}\mathcal C^{\rm all}_{s,t,p}(r)
 =\frac1{4N^{1/4}p^{(e-4)/4}}.}                         \tag{10}
\]

In fact, if `0<r<=1/3`, `E_v(3r)<A`, and `E_4(3r)<N`, then

\[
 \mathcal C^{\rm all}_{s,t,p}(r)
 \leq \frac1{p^{(e-4)/4}}
 \left\{
 \frac1{4[N-E_4(3r)]^{1/4}}
 +\frac{2^{e/4}\sqrt r}{[A-E_v(3r)]^{1/2}}
 \right\}.                                              \tag{11}
\]

Balanced rank-one regular perturbations show that the right side of (10) is
a lower bound for (9) at every positive radius.  Thus allowing degree
irregularity does not change the limiting sharp constant: the degree mode has
a positive quadratic cost and is negligible at the fourth-root extremal
scale.

## The canonical decomposition

Since `W` has edge density `p`, one has `integral a=integral F=0`.  Therefore

\[
 \int_0^1U(x,y)\,dy
 =a(x)-a(x)-\int_0^1a(y)\,dy=0.                          \tag{12}
\]

If `eta=||F||_infinity`, then `||a||_infinity<=eta` and

\[
 \lVert U\rVert_\infty
 \leq\lVert F\rVert_\infty+2\lVert a\rVert_\infty
 \leq3\eta.                                             \tag{13}
\]

For measurable sets `S,T`, centered Cauchy--Schwarz gives

\[
 \left|\int_Sa\right|
 =|\langle1_S-|S|,a\rangle|
 \leq\sqrt{|S|(1-|S|)}\sqrt v\leq\frac12\sqrt v.
\]

It follows that

\[
 \lVert D\rVert_\square\leq\sqrt v.                    \tag{14}
\]

The sharp centered cut--Schatten inequality for the regular kernel `U` gives

\[
 \lVert U\rVert_\square\leq\frac14t(C_4,U)^{1/4}.
\]

The triangle inequality and (14) prove (7).

## Colored spanning-subgraph expansion

Expand every edge factor of `K_(s,t)` as `p+U+D`, and regard every edge as
colored `p`, `U`, or `D`.  The sub-sum having no `D`-edge is
`t(K_(s,t),p+U)`.  The regular local expansion applies algebraically to the
bounded symmetric kernel `U`; positivity of `p+U` is not used in its proof.
Since the fourth-order survivors are exactly the `N` four-cycles, there is no
fifth-order survivor, and all later leafless terms are dominated by `C_4`,

\[
 \left|t(K_{s,t},p+U)-p^e-Np^{e-4}z\right|
 \leq2^e x^2p^{e-4}z.                                  \tag{15}
\]

Here `||U||_infinity/p<=x<=1`.

We next estimate the colored terms containing `D`.  Suppose a coloring has
`d>=2` `D`-edges and `u` `U`-edges, and put `k=d+u`.  Expand each

\[
 D(x,y)=a(x)+a(y).
\]

This produces at most `2^d` terms.  Bound all `U`-factors by `h`.  From the
remaining `d` factors of `a`, retain any two.  If they use one integration
variable their absolute integral is at most `v`; if they use two variables,
it is at most `(integral |a|)^2<=v`.  Bound the other `a`-factors by `h`.
Thus every such colored density satisfies

\[
 |t(H;U,D)|\leq2^d h^{k-2}v.                            \tag{16}
\]

When `d=2,u=0`, two disjoint `D`-edges have density zero because
`integral D=0`, whereas two adjacent `D`-edges have density

\[
 t(P_3,D)=\int_0^1\left(\int_0^1D(x,y)\,dy\right)^2dx
 =\int_0^1a(x)^2dx=v.                                  \tag{17}
\]

There are exactly

\[
 s\binom t2+t\binom s2=A
\]

adjacent edge pairs in `K_(s,t)`.  They give the first leading term in (6).
Every other coloring with at least two `D`-edges has `k>=3`.  There are at
most `3^e` colorings, the factor `2^d` is at most `2^e`, and `x<=1`.
After restoring the `p`-edges, (16) therefore bounds their total absolute
contribution by

\[
 6^e x\,p^{e-2}v.                                       \tag{18}
\]

It remains to handle colorings with exactly one `D`-edge.  After expanding
that edge, a typical integral has one distinguished factor `a(q)` and `u`
factors of `U`.  Let `H` be the graph of the `U`-edges and let
`phi_H(q)` be its rooted density after all other variables are integrated.
If `H` has a nonroot leaf, then `phi_H=0` by (12).  If the root is not
incident with `H`, integrating `a(q)` gives zero.  In every remaining case,
`u>=4`.

Glue two copies of rooted `H` at their root.  A nonroot neighbor of the root
has degree at least two in each copy, so the two corresponding vertices are
nonadjacent and both have degree at least two.  Lovasz's absolute
signed-density domination, applied after normalizing `U` by `h`, gives

\[
 \lVert\phi_H\rVert_2^2
 \leq h^{2u-4}t(C_4,U)=h^{2u-4}z.                       \tag{19}
\]

Consequently Cauchy--Schwarz gives, for each of the two endpoint terms from
the unique `D`-edge,

\[
 \left|\int a(q)\phi_H(q)\,dq\right|
 \leq h^{u-2}\sqrt{vz}.                                \tag{20}
\]

There are at most `e2^(e-1)` one-`D` colorings.  Because `u>=4`, equations
(20) and `2sqrt(XY)<=X+Y` show that their total is at most

\[
 e2^{e-1}x^2
 \left(p^{e-2}v+p^{e-4}z\right).                       \tag{21}
\]

Adding (15), (17)--(18), and (21) is exactly (6).

## The forcing estimate and the sharp limit

The lower half of (6) says

\[
 \delta\geq
 [A-E_v(x)]p^{e-2}v+[N-E_4(x)]p^{e-4}z.                \tag{22}
\]

When both coefficients are positive, separately bounding `v` and `z` in
(7) proves (8).

If `||F||_infinity<=rp`, then (13) gives `x<=3r`.  Also, the ordinary
spanning-subgraph expansion, `integral F=0`, and `r<=1` give

\[
 0\leq\delta
 \leq p^e\sum_{k=2}^e\binom ekr^k
 \leq2^ep^er^2.                                        \tag{23}
\]

Use monotonicity of (2), replace `x` by `3r` in (8), divide by
`delta^(1/4)`, and invoke (23).  This proves (11), hence the upper limit in
(10).

For the reverse inequality, let `f` be `1` and `-1` on two sets of measure
one half and put

\[
 W_\varepsilon=p+\varepsilon f\otimes f.
\]

For every fixed `r>0`, arbitrarily small nonzero `epsilon` give admissible
regular graphons, and

\[
 \lVert W_\varepsilon-p\rVert_\square=|\varepsilon|/4,
 \qquad
 \delta=Np^{e-4}\varepsilon^4+O(\varepsilon^6).
\]

Their ratios tend to the right side of (10), proving the lower limit and
completing the theorem.

## The falsifiable two-scale checkpoint

Let `U` be any bounded symmetric kernel with `T_U1=0`, let `b` be bounded
with `integral b=0`, and set

\[
 F_\varepsilon
 =\varepsilon U+\varepsilon^2[b(x)+b(y)].               \tag{24}
\]

In this case `a_epsilon=epsilon^2 b`,
`v_epsilon=epsilon^4 integral b^2`, and
`t(C_4,epsilon U)=epsilon^4t(C_4,U)`.  Equation (6), or the termwise proof
above, gives

\[
\boxed{
 t(K_{s,t},p+F_\varepsilon)-p^e
 =\varepsilon^4\left[
 Ap^{e-2}\int b^2+Np^{e-4}t(C_4,U)
 \right]+O(\varepsilon^5).}                             \tag{25}
\]

All coefficients of degrees one, two, and three vanish.  In particular, the
potential fourth-order term with one degree edge and two regular edges is
zero: the two `U`-edges form a forest with an unrooted leaf.  The two
nonnegative terms displayed in (25) are therefore the complete quartic
coefficient.

## Literature boundary

The signed-density ordering, its absolute form, `C_4` domination, and the
spanning-subgraph expansion used above are prior methodology from:

- L. Lovasz, *Subgraph densities in signed graphons and the local Sidorenko
  conjecture*, 2010, <https://arxiv.org/abs/1004.3026>.

Qualitative complete-bipartite forcing is classical:

- J. Skokan and L. Thoma, *Bipartite subgraphs and quasi-randomness*, Graphs
  and Combinatorics 20 (2004), 255--262,
  <https://digitalcommons.uri.edu/math_facpubs/249/>.

Zhao's 2026 tensor-amplification framework proves general equality-case
regularization and quantitative degree stability.  In particular, its
Corollary 6.2 bounds the `L^2` degree fluctuation in terms of a normalized
Sidorenko ratio for graphs in the spectral range:

- Y. Zhao, *Tensor Amplification and Spectral Transfer for Sidorenko-Type
  Inequalities*, 2026, <https://arxiv.org/abs/2607.02260>.

That result supports the degree-regularization principle used here, but it
does not identify the fourth-order `K_(s,t)` expansion, control the rooted
mixed terms, or determine the sharp unrestricted cut-forcing constant.

The earlier notes in this research chain prove the global degree-variance
lower bound, the all-`K_(s,t)` fourth-root modulus, rank-one exponent
sharpness, and the sharp constant in the exactly regular slice.  The present
result uses the variance bound to show that degree irregularity has a
quadratic cost, while the rooted signed-density estimate (19) prevents mixed
terms from changing the fourth-order constant.

Targeted primary-source searches through 2026-09-03 did not locate (6), (8),
or the unrestricted limiting constant (10).  These are claimed only as an
apparently new quantitative refinement, without a historical-priority claim.

## Exact finite validation and trust boundary

`verify_nonregular_local_constant.py` mean-centers arbitrary finite symmetric
adjacency kernels, makes decomposition (4), and directly evaluates both sides
of (6).  It also checks the three exact cut-norm ingredients behind (7).
Separately, it performs truncated polynomial arithmetic for (24), verifies
that the coefficients through degree three vanish, and compares the fourth
coefficient with (25).  All arithmetic is standard-library `Fraction`
arithmetic; no numerical root approximation or external solver is used.

```text
python3 verify_nonregular_local_constant.py --max-atoms 4 --max-part 4
python3 -m unittest -v test_nonregular_local_constant.py
```

The recorded CPython 3.12.12 run returned

```text
p=2/5
radii=1/50,1/100
max_atoms=4
max_part=4
nonzero_mean_centered_kernels=71
degree_irregular_kernels=62
checked_general_instances=1278
checked_two_scale_coefficients=558
record_sha256=f83875da4a0266200659f917a250d93a69d50fcdaa60633f61b7602ca0c6c981
status=PASS
```

The finite checker audits the decomposition, powers, constants, and
two-scale cancellation.  The universal theorem rests on the analytic proof,
not on finite enumeration.
