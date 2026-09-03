# Finite-radius stability of complete-bipartite cut extremizers

## Purpose

The asymptotic classification in `ASYMPTOTIC_EXTREMIZERS.md` says that a
sequence attaining the sharp local `K_(s,t)` forcing constant must lose its
degree mode and approach a balanced signed rank-one regular core.  This note
makes that conclusion quantitative at a fixed local radius.  It converts two
observable errors,

- the relative forcing-ratio deficit `tau`, and
- the `L^infinity` locality radius `r`,

into explicit bounds on degree energy, regular-cycle energy, and distance in
operator norm from the extremal two-block family.

The decisive point is a quadratic inequality for the square root of the
degree-energy share.  Keeping that quadratic, rather than discarding the
negative linear loss in the fourth root, improves the natural error scale
from the preliminary `tau+sqrt(r)` to `tau+r`.

## Constants

Fix integers `s,t>=2` and `0<p<1`, and put

\[
 e=st,\qquad
 A=s\binom t2+t\binom s2,\qquad
 N=\binom s2\binom t2,\qquad
 L=N^{-1/4}p^{-(e-4)/4}.                                \tag{1}
\]

For `0<=x<=1`, define the error polynomials from the unrestricted local
expansion:

\[
 E_v(x)=6^e x+e2^{e-1}x^2,
 \qquad
 E_4(x)=(2^e+e2^{e-1})x^2.                              \tag{2}
\]

Given `0<r<=1/3`, let

\[
 \rho=\max\left\{\frac{E_v(3r)}A,\frac{E_4(3r)}N\right\}.
                                                                    \tag{3}
\]

When `rho<1`, put

\[
 m_-=(1+\rho)^{-1},\qquad m_+=(1-\rho)^{-1},            \tag{4}
\]

and define

\[
 \Gamma=\frac{4\,2^{e/4}N^{1/4}}{\sqrt A}\sqrt r.      \tag{5}
\]

For a forcing-ratio deficit `0<=tau<1`, set

\[
 H=\tau+m_+^{1/4}-1,                                   \tag{6}
\]

\[
 Y=2m_+^{3/4}
 \left(\Gamma+\sqrt{\Gamma^2+H/m_+^{3/4}}\right).       \tag{7}
\]

Finally, provided `Y^2<m_-`, define

\[
 \varepsilon_*
 =1-\frac{1-\tau-\Gamma Y}{m_+^{1/4}},                 \tag{8}
\]

\[
 \Theta=\max\left\{
 m_+^{1/4}-1,
 1-(m_--Y^2)^{1/4}
 \right\},                                             \tag{9}
\]

and

\[
 \Omega=\frac{2^{e/4}}{\sqrt A}\,
 p^{\,1-e/4}\sqrt r\,Y.                               \tag{10}
\]

All these quantities are explicit functions only of `s,t,p,r,tau`.

## The finite-radius theorem

### Theorem 1

Let `W:[0,1]^2->[0,1]` be a nonconstant symmetric graphon of edge density
`p` satisfying

\[
 \|W-p\|_\infty\leq rp.                                \tag{11}
\]

Write `F=W-p` and make the canonical decomposition

\[
 a=T_F1,\qquad v=\|a\|_2^2,\qquad
 D=a\otimes1+1\otimes a,\qquad U=F-D,\qquad
 z=t(C_4,U).                                            \tag{12}
\]

Let

\[
 \delta=t(K_{s,t},W)-p^e>0.                            \tag{13}
\]

Suppose the perturbation has forcing ratio within relative deficit `tau` of
the sharp limiting constant:

\[
 \frac{\|F\|_\square}{\delta^{1/4}}
 \geq(1-\tau)\frac L4.                                 \tag{14}
\]

Assume `rho<1`, `Y^2<m_-`, and

\[
 0\leq\varepsilon_*\leq\frac1{128}.                    \tag{15}
\]

Then the degree-energy share and regular-cycle share obey

\[
\boxed{
 \frac v\delta\leq\frac{Y^2}{Ap^{e-2}},
 \qquad
 \left|\frac{Np^{e-4}z}{\delta}-1\right|
 \leq Y^2+\frac{\rho}{1-\rho}.}                       \tag{16}
\]

The degree kernel is quantitatively negligible:

\[
\boxed{
 \frac{\|T_D\|_{2\to2}}{\delta^{1/4}}
 \leq\Omega.}                                         \tag{17}
\]

The same bound holds with the operator norm replaced by the cut norm.
Moreover, `z>0`, and there are a balanced sign
`b=2 1_B-1`, `lambda(B)=1/2`, and `kappa in {-1,1}` such that

\[
\boxed{
 \left\|T_{U/z^{1/4}}-\kappa b\otimes b\right\|_{2\to2}
 \leq10\varepsilon_*^{1/4}.}                          \tag{18}
\]

For the full perturbation,

\[
\boxed{
 \left\|T_{F/\delta^{1/4}}-\kappa Lb\otimes b\right\|_{2\to2}
 \leq
 \Omega+10Lm_+^{1/4}\varepsilon_*^{1/4}+L\Theta.}     \tag{19}
\]

The bounds in (18)--(19) also hold in cut norm.

### Proof

Put

\[
 P=Ap^{e-2}v,\qquad Q=Np^{e-4}z,\qquad
 \alpha=P/\delta,\qquad\beta=Q/\delta.                \tag{20}
\]

Both `P` and `Q` are nonnegative.  Indeed,
`z=||T_U||_(S_4)^4`.  Since (11) gives

\[
 \max\{\|U\|_\infty,\|a\|_\infty\}/p\leq3r,          \tag{21}
\]

the uniform two-component expansion and monotonicity of the polynomials in
(2) imply

\[
 |\delta-P-Q|\leq\rho(P+Q).                            \tag{22}
\]

Consequently,

\[
 m_-\leq\alpha+\beta\leq m_+.                          \tag{23}
\]

The ordinary spanning expansion has no linear term because `integral F=0`.
As `r<=1`, it gives the coarse but uniform upper bound

\[
 0<\delta\leq2^ep^er^2.                                \tag{24}
\]

The centered cut--Schatten bound and the degree-kernel estimate give

\[
 \|F\|_\square\leq z^{1/4}/4+\sqrt v.                 \tag{25}
\]

Divide (25) by `L delta^(1/4)/4`.  Equations (20), (24), and the definitions
of `L`, `P`, and `Gamma` give exactly

\[
 1-\tau\leq\beta^{1/4}+\Gamma\sqrt\alpha.              \tag{26}
\]

By (23), `beta<=m_+-alpha`.  Concavity of the fourth root yields the tangent
bound

\[
 (m_+-\alpha)^{1/4}
 \leq m_+^{1/4}-\frac{\alpha}{4m_+^{3/4}}.             \tag{27}
\]

Combining (26)--(27) and writing `y=sqrt(alpha)` gives

\[
 \frac{y^2}{4m_+^{3/4}}-\Gamma y-H\leq0.              \tag{28}
\]

The positive root of the left side is exactly `Y` from (7), so

\[
 \alpha\leq Y^2.                                       \tag{29}
\]

The first claim in (16) follows from `alpha=Ap^(e-2)v/delta`.  Equations
(23) and (29) also give

\[
 m_--Y^2\leq\beta\leq m_+,
 \qquad
 |\beta-1|\leq Y^2+m_+-1
 =Y^2+\frac\rho{1-\rho},                               \tag{30}
\]

which proves the second claim in (16) and, by the assumed strict lower bound,
shows `z>0`.

If `v=0`, then `D=0`.  Otherwise, the nonzero part of `T_D` on the
orthonormal basis `1,a/sqrt(v)` has matrix
`[[0,sqrt(v)],[sqrt(v),0]]`; the operator vanishes on the orthogonal
complement.  Thus in either case `||T_D||_(2->2)=sqrt(v)`.  Therefore (24)
and (29) give

\[
 \frac{\|T_D\|_{2\to2}}{\delta^{1/4}}
 \leq
 \frac{2^{e/4}}{\sqrt A}\,
 p^{1-e/4}\sqrt r\,Y=\Omega,                           \tag{31}
\]

and cut norm is bounded by operator norm.

It remains to quantify near equality for the regular core.  From (14) and
`||D||_square<=sqrt(v)`,

\[
 \frac{4\|U\|_\square}{z^{1/4}}
 \geq\frac{1-\tau-\Gamma\sqrt\alpha}{\beta^{1/4}}
 \geq\frac{1-\tau-\Gamma Y}{m_+^{1/4}}
 =1-\varepsilon_*.                                    \tag{32}
\]

The second inequality uses (15), which makes the numerator positive, along
with (23) and (29).  The quantitative centered rigidity theorem, including
its exact equality case when `epsilon_*=0`, now proves (18).

Finally,

\[
 \frac{z^{1/4}}{\delta^{1/4}}=L\beta^{1/4}.            \tag{33}
\]

The interval for `beta` in (30) implies

\[
 |\beta^{1/4}-1|\leq\Theta.                            \tag{34}
\]

Decompose `F=D+U`, use (17)--(18), `beta^(1/4)<=m_+^(1/4)`, and (33)--(34).
This gives (19).  Every rectangle integral is bounded by the corresponding
operator norm, completing the proof.

## Clean asymptotic form

### Corollary 2

For fixed `s,t,p`, there are constants `c,C>0` such that whenever
`0<=r,tau<=c` and (11)--(14) hold,

\[
 \frac v\delta\leq C(\tau+r),
 \qquad
 \left|\frac{Np^{e-4}z}{\delta}-1\right|
 \leq C(\tau+r),                                      \tag{35}
\]

\[
 \frac{\|T_D\|_{2\to2}}{\delta^{1/4}}
 \leq C\sqrt{r(\tau+r)},                              \tag{36}
\]

and

\[
 \inf_{\kappa,b}
 \left\|T_{F/\delta^{1/4}}-\kappa Lb\otimes b\right\|_{2\to2}
 \leq C(\tau+r)^{1/4},                                \tag{37}
\]

where the infimum is over signs `kappa` and balanced signs `b`.  The operator
norm in (36)--(37) may again be replaced by cut norm.

To verify the scale, note from (2)--(7) that

\[
 \rho=O(r),\quad \Gamma=O(\sqrt r),\quad
 H=O(\tau+r),\quad Y=O(\sqrt{\tau+r}).                 \tag{38}
\]

Hence `epsilon_*=O(tau+r)`, `Theta=O(tau+r)`, and
`Omega=O(sqrt(r(tau+r)))`.  All side conditions of Theorem 1 hold once
`tau+r` is sufficiently small, and (35)--(37) follow.

## Optimality of the fourth-root modulus

The exponent `1/4` in (37) cannot be increased.  Let `b,c` be orthogonal
balanced signs and set

\[
 K_\theta=b\otimes b+\theta c\otimes c,
 \qquad0<\theta<1.                                    \tag{39}
\]

Choose a positive amplitude `eta_theta=O(theta^5)` small enough that
`W_theta=p+eta_theta K_theta` is a graphon.  This is a regular perturbation,
and the regular expansion gives

\[
 \delta_\theta
 =Np^{e-4}\eta_\theta^4(1+\theta^4)
  +O(\eta_\theta^6).                                  \tag{40}
\]

Its cut norm is `eta_theta/4`.  Thus the smallest admissible relative deficit
in (14) satisfies

\[
 \tau_\theta\sim\theta^4/4,
 \qquad r_\theta=O(\theta^5).                          \tag{41}
\]

The second singular value of the normalized perturbation is asymptotic to
`L theta`, so its operator distance from every rank-one model is bounded below
by a positive constant times `theta`.  An estimate with an exponent strictly
larger than `1/4` on `tau+r` would contradict (41).

## Validation and trust boundary

The theorem is an analytic consequence of the already validated uniform
two-component expansion and centered rigidity theorem.
`verify_finite_radius_extremizers.py` supplies a definition-level finite-step
audit.  It uses `Fraction` arithmetic for graphon densities, cut norms, degree
decompositions, and every polynomial coefficient.  Every square and fourth
root is enclosed between decimal rationals at 70 digits; the endpoint powers
are checked by exact integer arithmetic, so no floating-point assumption is
present.

The checker verifies six profiles with a small critical degree component and
six with an orthogonal spectral tail.  For each profile it certifies the side
conditions, the quadratic `Y` envelope, both claims in (16), the exact
degree-operator estimate, and the full operator-distance bound (19) against a
direct `K_(s,t)` density.  CPython 3.12.12 returns

```text
python=3.12.12
arithmetic=fractions.Fraction
root_digits=70
degree_profiles=6
spectral_profiles=6
record_sha256=29dd73a1a31c287a33bc393c9c8cd3be2fab0f622b3a961aa24360ab15e4fc08
status=PASS
```

These finite profiles audit constants, normalization, and sharp mechanisms;
they do not replace the universal proof above.

## Literature boundary

The signed-density expansion and local Sidorenko framework are prior tools
from L. Lovasz, *Subgraph densities in signed graphons and the local
Sidorenko conjecture* (2010), <https://arxiv.org/abs/1004.3026>.  The
even-cycle/Schatten-norm setting is treated by H. Hatami, *Graph norms and
Sidorenko's conjecture* (2008), <https://arxiv.org/abs/0806.0047>, and the
cut-norm convention is standard in S. Janson, *Graphons, cut norm and
distance, couplings and rearrangements* (2011),
<https://arxiv.org/abs/1009.2376>.

Y. Zhao's *Tensor Amplification and Spectral Transfer for Sidorenko-Type
Inequalities* (2026), <https://arxiv.org/abs/2607.02260>, proves broad
quantitative near-equality regularization, but does not give a cut-ratio
deficit, balanced rank-one operator conclusion, or fixed-radius extremizer
modulus.  Targeted arXiv searches through 2026-09-03 found no theorem matching
(16)--(19) or the `O((tau+r)^(1/4))` corollary.  The result is therefore
described only as apparently new relative to the searched sources, without a
historical-priority claim.
