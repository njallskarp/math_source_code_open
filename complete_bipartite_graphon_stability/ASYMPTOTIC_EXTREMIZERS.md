# Asymptotic extremizers for complete-bipartite cut forcing

## Overview

This note classifies every sequence attaining the sharp local constant from
`NONREGULAR_LOCAL_CONSTANT.md`.  The central input is a quantitative
near-equality theorem for the sharp centered cut--Schatten inequality.  It
shows that no diffuse or infinite-rank obstruction exists: near equality
forces operator-norm, hence cut-norm, proximity to a signed balanced rank-one
two-block kernel.  The quantitative constant and sequence hypothesis below
incorporate the independent refinement in Discovery Net review
`bafkreiaotmxiouuki4po6h3cqynlq3aolousftclx5ntvmigqd3vqddk4y`.

Throughout, kernels are real, bounded, symmetric kernels on the atomless
probability space `[0,1]`.  For a kernel `K`, write `T_K` for its self-adjoint
integral operator and

\[
 \|K\|_{S_4}=\|T_K\|_{S_4}=t(C_4,K)^{1/4}.
\]

A balanced sign is a function

\[
 b=2\mathbf 1_B-1,
 \qquad \lambda(B)=\frac12.                              \tag{1}
\]

The balanced signed rank-one family is

\[
 \mathcal B={\kappa b\otimes b:
   \kappa\in\{-1,1\},\ b\text{ satisfies (1)}\}.         \tag{2}
\]

Every member of this family has operator and fourth Schatten norms one and
cut norm `1/4`.  The cut-norm convention throughout is

\[
 \|K\|_\square
 =\sup_{S,T\subseteq[0,1]}
   \left|\int_{S\times T}K(x,y)\,dx\,dy\right|.
\]

## Quantitative centered cut--Schatten stability

### Theorem 1

Let `K` be a nonzero bounded symmetric kernel satisfying `T_K 1=0`, and put

\[
 q=t(C_4,K)^{1/4}>0.
\]

If `0<epsilon<=1/128` and

\[
 \|K\|_\square\geq\frac{1-\varepsilon}{4}q,             \tag{3}
\]

then there are `kappa in {-1,1}` and a balanced sign `b` such that

\[
\boxed{
 \left\|T_{K/q}-\kappa\,b\otimes b\right\|_{2\to2}
 \leq10\varepsilon^{1/4}.}                              \tag{4}
\]

Consequently,

\[
 \left\|K/q-\kappa b\otimes b\right\|_\square
 \leq10\varepsilon^{1/4}.                               \tag{5}
\]

Here `b tensor b` denotes both the rank-one kernel and its integral operator.
The numerical constant is not optimized; the exponent `1/4` records the
fourth-Schatten tail scale and is optimal.

Equality is completely rigid:

\[
 \|K\|_\square=\frac14t(C_4,K)^{1/4}                    \tag{6}
\]

if and only if

\[
 K/q=\kappa b\otimes b\quad\text{almost everywhere}     \tag{7}
\]

for a balanced sign `b` and `kappa in {-1,1}`.

### Proof

Normalize `K` by `q` and write

\[
 A=T_{K/q},\qquad \|A\|_{S_4}=1.
\]

Choose measurable sets `S,T` whose rectangle integral is within
`epsilon/4` of the cut-norm supremum.  With `s=lambda(S)`, `t=lambda(T)`,

\[
 f=\mathbf1_S-s1,\qquad g=\mathbf1_T-t1,
\]

regularity gives

\[
 |\langle f,Ag\rangle|
 \geq\frac{1-2\varepsilon}{4}.                          \tag{8}
\]

Put `u=2||f||_2` and `w=2||g||_2`.  Both lie in `[0,1]`.  If `sigma_1` is
the largest singular value of `A`, then

\[
 1-2\varepsilon
 \leq4|\langle f,Ag\rangle|
 \leq uw\sigma_1\leq1.                                 \tag{9}
\]

It follows that

\[
 \sigma_1,u,w\geq1-2\varepsilon.                        \tag{10}
\]

In particular,

\[
 |s-1/2|,|t-1/2|\leq\sqrt\varepsilon,                  \tag{11}
\]

because `u^2=4s(1-s)=1-(2s-1)^2`, and similarly for `t`.

Let `sigma_2` be the second singular value.  Fourth-Schatten normalization
and (10) give

\[
 \sigma_2
 \leq(1-\sigma_1^4)^{1/4}
 \leq[1-(1-2\varepsilon)^4]^{1/4}
 \leq(8\varepsilon)^{1/4}\leq\frac12.                  \tag{12}
\]

Thus the eigenvalue of absolute value `sigma_1` is simple.  Choose a unit
eigenfunction `phi` and `kappa in {-1,1}` such that

\[
 A=\kappa\sigma_1\,\phi\otimes\phi+R,
 \qquad R\phi=0,
 \qquad\|R\|_{2\to2}=\sigma_2.                          \tag{13}
\]

Set `f_0=f/||f||_2`, `g_0=g/||g||_2` and

\[
 \alpha=|\langle f_0,\phi\rangle|,
 \qquad \beta=|\langle g_0,\phi\rangle|,
 \qquad X=(1-\alpha^2)^{1/2},
 \qquad Y=(1-\beta^2)^{1/2}.
\]

Since `||f||_2||g||_2<=1/4`, equation (8) implies

\[
 |\langle f_0,Ag_0\rangle|\geq1-2\varepsilon.          \tag{14}
\]

On the other hand, (13) and orthogonality give the sharper estimate

\[
 |\langle f_0,Ag_0\rangle|
 \leq\alpha\beta+\sigma_2XY
 \leq1-\frac{1-\sigma_2}{2}(X^2+Y^2).                  \tag{15}
\]

The last inequality uses

\[
 \sqrt{(1-X^2)(1-Y^2)}
 \leq1-\frac{X^2+Y^2}{2},
 \qquad XY\leq\frac{X^2+Y^2}{2}.
\]

Equations (12), (14), and (15) yield

\[
 X^2+Y^2\leq8\varepsilon.                              \tag{16}
\]

After changing the sign of `phi` if necessary,

\[
 \|f_0-\phi\|_2^2=2(1-\alpha)
 \leq2(1-\alpha^2)=2X^2,
\]

and hence

\[
 \|f_0-\phi\|_2\leq4\sqrt\varepsilon.                 \tag{17}
\]

Let `b_S=2 1_S-1`.  From (10)--(11),

\[
 \|f_0-b_S\|_2^2
 =2-4\|f\|_2=2(1-u)\leq4\varepsilon,                 \tag{18}
\]

where the identity follows from
`<f_0,b_S>=2||f||_2=u`.

Because the underlying space is atomless, modify `S` on a set of measure
`|s-1/2|` to obtain `B` of measure exactly `1/2`.  For
`b=2 1_B-1`, equations (11), (17), and (18) give

\[
 \|\phi-b\|_2
 \leq6\sqrt\varepsilon+2\varepsilon^{1/4}
 \leq8\varepsilon^{1/4}.                               \tag{19}
\]

Finally,

\[
\begin{aligned}
 \|A-\kappa b\otimes b\|_{2\to2}
 &\leq \sigma_2+(1-\sigma_1)
       +\|\phi\otimes\phi-b\otimes b\|_{2\to2}\\
 &\leq(8\varepsilon)^{1/4}+2\varepsilon
       +2\|\phi-b\|_2\\
 &\leq(8\varepsilon)^{1/4}+2\varepsilon
       +12\sqrt\varepsilon+4\varepsilon^{1/4}\\
 &\leq10\varepsilon^{1/4}.
\end{aligned}                                           \tag{20}
\]

For the last inequality, put `x=epsilon^(1/4)`.  The hypothesis gives
`x<3/10`, while `8^(1/4)<17/10`, and therefore the coefficient of `x` is
strictly less than

\[
 \frac{17}{10}+\frac{27}{500}+\frac{18}{5}+4
 =\frac{4677}{500}<10.
\]

This proves (4).  Every rectangle integral of a kernel is bounded by the
operator norm of its integral operator, so (5) follows.

If equality holds in (6), apply the preceding proof with arbitrarily small
positive `epsilon`.  Equations (10), (12), and (13) force `sigma_1=1` and
`R=0`; equation (19) makes the fixed top eigenfunction an `L^2` limit of
balanced signs.  The balanced-sign class is closed in `L^2`, so the top
eigenfunction is itself a balanced sign.  This proves (7).  The converse is
an immediate calculation.

To see that the stability exponent cannot be improved, choose orthogonal
balanced signs `b,c` (constant on four equal intervals suffices) and put

\[
 K_\rho=b\otimes b+\rho c\otimes c,
 \qquad0<\rho<1.                                        \tag{21}
\]

The operator eigenvalues are `1,rho`, so

\[
 t(C_4,K_\rho)^{1/4}=(1+\rho^4)^{1/4}.
\]

The centered cut--operator bound gives `||K_rho||_square<=1/4`; equality is
attained on the positive half of `b`, because `c` has zero integral on that
half.  Thus the relative cut deficit is

\[
 \varepsilon_\rho=1-(1+\rho^4)^{-1/4}\sim\rho^4/4.
\]

On the other hand, the operator-norm distance from
`K_rho/(1+rho^4)^(1/4)` to every rank-one operator is at least its second
singular value

\[
 \frac{\rho}{(1+\rho^4)^{1/4}}.
\]

Since the family (2) consists of rank-one operators, a stability estimate
with exponent strictly larger than `1/4` is impossible.

## Classification for complete-bipartite forcing

### Theorem 2

Fix `s,t>=2` and `0<p<1`, and put

\[
 e=st,\qquad N=\binom{s}{2}\binom{t}{2},\qquad
 L=N^{-1/4}p^{-(e-4)/4}.                                \tag{22}
\]

Let `r_n` tend to zero and let `W_n` be nonconstant symmetric graphons
of edge density `p` satisfying

\[
 \|W_n-p\|_\infty\leq r_np.                             \tag{23}
\]

Write

\[
 F_n=W_n-p,\qquad
 \delta_n=t(K_{s,t},W_n)-p^e,
\]

and make the canonical decomposition

\[
 a_n=T_{F_n}1,\quad v_n=\|a_n\|_2^2,\quad
 D_n=a_n\otimes1+1\otimes a_n,\quad U_n=F_n-D_n,
 \quad z_n=t(C_4,U_n).                                  \tag{24}
\]

Assume the sequence is asymptotically extremizing:

\[
 \frac{\|F_n\|_\square}{\delta_n^{1/4}}
 \longrightarrow
 \frac1{4N^{1/4}p^{(e-4)/4}}=\frac L4.                 \tag{25}
\]

Then

\[
\boxed{
 \frac{v_n}{\delta_n}\longrightarrow0,
 \qquad
 \frac{Np^{e-4}z_n}{\delta_n}\longrightarrow1.}        \tag{26}
\]

In particular, the degree mode is negligible in both requested topologies:

\[
 \frac{\|D_n\|_\square}{\delta_n^{1/4}}\longrightarrow0,
 \qquad
 \frac{\|T_{D_n}\|_{2\to2}}{\delta_n^{1/4}}
 \longrightarrow0.                                    \tag{27}
\]

Moreover, `z_n>0` eventually, and there exist balanced signs `b_n` and signs
`kappa_n in {-1,1}` such that

\[
\boxed{
 \left\|T_{U_n/z_n^{1/4}}-\kappa_n b_n\otimes b_n
 \right\|_{2\to2}\longrightarrow0.}                   \tag{28}
\]

The same convergence holds in cut norm.  Equivalently, the complete
perturbations satisfy the stronger normalized classification

\[
\boxed{
 \left\|T_{F_n/\delta_n^{1/4}}
       -\kappa_nL b_n\otimes b_n\right\|_{2\to2}
 \longrightarrow0,}                                    \tag{29}
\]

again also in cut norm.  Thus the distance of every asymptotically
extremizing sequence from the two signed balanced two-block models tends to
zero.  After measure-preserving relabeling, `b_n` may be taken to be the
standard sign of the two half intervals; after passing to a subsequence,
`kappa_n` is constant.

### Proof

For all sufficiently large `n`, the elementary spanning expansion and (23)
give

\[
 0<\delta_n\leq2^ep^er_n^2,                              \tag{30}
\]

so `delta_n` tends to zero.  The two-component expansion from
`NONREGULAR_LOCAL_CONSTANT.md` has the form

\[
 \delta_n
 =A p^{e-2}v_n+Np^{e-4}z_n
 +o(v_n+z_n),                                           \tag{31}
\]

where `A=s binom(t,2)+t binom(s,2)` and the little-oh is uniform after the
fixed powers of `p` are included.  More explicitly, its two relative error
coefficients tend to zero because

\[
 \max\{\|U_n\|_\infty,\|a_n\|_\infty\}/p\leq3r_n.
\]

The lower half of that expansion first gives

\[
 v_n+z_n=O(\delta_n).                                   \tag{32}
\]

Put

\[
 \alpha_n=\frac{Ap^{e-2}v_n}{\delta_n},
 \qquad
 \beta_n=\frac{Np^{e-4}z_n}{\delta_n}.
\]

Equations (31)--(32) imply

\[
 \alpha_n+\beta_n\longrightarrow1.                    \tag{33}
\]

The degree kernel satisfies

\[
 \|D_n\|_\square\leq\sqrt{v_n},
 \qquad
 \|T_{D_n}\|_{2\to2}=\sqrt{v_n}.                     \tag{34}
\]

If `v_n=0`, then `D_n=0`.  Otherwise, on the span of `1` and
`a_n/sqrt(v_n)`, the nonzero part of `T_(D_n)` has matrix
`[[0,sqrt(v_n)],[sqrt(v_n),0]]`; it vanishes on the orthogonal complement.

By (30) and (32), both right sides in (34), divided by
`delta_n^(1/4)`, tend to zero.  Hence (25) also gives

\[
 \frac{\|U_n\|_\square}{\delta_n^{1/4}}
 \longrightarrow\frac L4.                              \tag{35}
\]

The sharp centered inequality for the regular core says

\[
 \frac{\|U_n\|_\square}{\delta_n^{1/4}}
 \leq\frac{z_n^{1/4}}{4\delta_n^{1/4}}
 =\frac L4\,\beta_n^{1/4}.                              \tag{36}
\]

Equations (33), (35), and (36), together with `alpha_n>=0`, force

\[
 \beta_n\longrightarrow1,
 \qquad\alpha_n\longrightarrow0.
\]

This proves (26), while (27) follows again from (34).  Equations (35)--(36)
also show

\[
 \frac{4\|U_n\|_\square}{z_n^{1/4}}\longrightarrow1.   \tag{37}
\]

Apply Theorem 1 with an error tending to zero.  This proves (28).  Finally,

\[
 \frac{z_n^{1/4}}{\delta_n^{1/4}}\longrightarrow L
\]

by (26).  Combine this fact, (27), and (28) to obtain (29).

## Literature boundary

The identity `t(C_4,K)^(1/4)=||T_K||_(S_4)` and the standard comparison
between the cut norm and the fourth Schatten norm are classical graphon
tools.  They appear, for example, in:

- L. Lovasz and B. Szegedy, *Limits of dense graph sequences*, 2006,
  <https://arxiv.org/abs/math/0408173>;
- L. Lovasz, *Subgraph densities in signed graphons and the local Sidorenko
  conjecture*, 2010, <https://arxiv.org/abs/1004.3026>.

The first source treats cut/Schatten comparison as a norm relation; the
second uses signed-density inequalities in local Sidorenko theory.  Zhao's
recent tensor-amplification theorem supplies broad quantitative control of
degree irregularity but not the centered cut--Schatten equality case or the
rank-one stability conclusion:

- Y. Zhao, *Tensor Amplification and Spectral Transfer for Sidorenko-Type
  Inequalities*, 2026, <https://arxiv.org/abs/2607.02260>.

Targeted searches through 2026-09-03 did not locate Theorem 1, its equality
classification, or Theorem 2.  They are therefore claimed only as apparently
new quantitative refinements of the cited norm comparison and the committed
complete-bipartite forcing chain, without a historical-priority claim.

## Validation and trust boundary

`verify_extremizer_profiles.py` performs exact finite-step checks on two
independent extremal mechanisms:

1. orthogonal balanced rank-one spectral tails, which approach equality at
   the fourth-Schatten tail scale;
2. degree perturbations at the critical and negligible scales, verifying that
   a critical degree energy strictly lowers the limiting forcing ratio while a
   smaller degree mode preserves it.

The checker uses direct finite-step homomorphism densities, exhaustive subset
cut norms, and exact `Fraction` arithmetic.  It audits normalizations and the
necessity of both conclusions in Theorem 2.  The universal classification is
the analytic consequence of Theorem 1 and the earlier uniform expansion;
finite profiles do not prove it.
