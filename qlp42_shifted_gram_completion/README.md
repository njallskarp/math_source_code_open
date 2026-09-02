# Positive-definite shifted-Gram completions for the QLP-42 middle branches

## Theorem

Let the combined length-(21) autocorrelation targets be

\[
T_S(0)=43,
\qquad T_S(4)=T_S(17)=-2,
\qquad T_S(10)=T_S(11)=2,
\]

with (T_S(r)=0) at every other shift, and

\[
T_H(0)=41,
\qquad T_H(r)=-2\quad(r\ne0).
\]

For one of the six canonical exact-sum cases, write

\[
\beta_c\in\{4-5i,4-3i,-5i,4-i,4+i,-3i\}.
\]

For every odd integer (sigma) with (|\sigma|\le37), there is a sequence
(C\in\mathbb Z[i]^{21}) satisfying

\[
C_0=i\sigma,
\qquad
\sum_{r=0}^{20}C_r=\beta_c,
\]

for which the block-circulant Hermitian matrix

\[
\mathcal G(C)=
\begin{pmatrix}
G_S&X_C\\
X_C^\ast&G_H
\end{pmatrix},
\]

is positive definite, where

\[
(G_S)_{r,s}=T_S(s-r),
\qquad
(G_H)_{r,s}=T_H(s-r),
\qquad
(X_C)_{r,s}=C_{s-r},
\]

and all subscripts are taken modulo (21).

Consequently every one of the (228) distinct case/fiber pairs for the
(q=37) branch, and hence all (36) branch-labeled pairs for (q=5), has
an abstract positive-definite completion of the full shifted Gram matrix.
Thus positive semidefiniteness of all simultaneous shifts, using only the
known combined (S)- and (H)-autocorrelations together with
(C_0=i\sigma) and (sum C_r=\beta_c), cannot exclude any middle-branch
fiber point.

This is a negative theorem about an obstruction mechanism. It does not
assert that the completed (C) is realized by coupled words, and it does
not construct a quaternary Legendre pair.

## Explicit completion

For an integer (t=20a+r), with (0\le r<20), define the balanced binary
word

\[
b_r(j)=
\left\lfloor\frac{(j+1)r}{20}\right\rfloor-
\left\lfloor\frac{jr}{20}\right\rfloor,
\qquad 0\le j<20.
\]

Put (t_R=\operatorname{Re}\beta_c) and
(t_I=\operatorname{Im}\beta_c-\sigma), and write
(t_R=20a_R+r_R) and (t_I=20a_I+r_I). The default construction is

\[
C_0=i\sigma,
\qquad
C_{j+1}=a_R+b_{r_R}(j)+i\bigl(a_I+b_{r_I}(j)\bigr).
\]

Only five endpoint pairs use a rotation. Here a rotation (ho) replaces
(b_r(j)) by (b_r(j+\rho\bmod20)).

| case (c) | (sigma) | real rotation | imaginary rotation |
|---:|---:|---:|---:|
| (0) | (-37) | (0) | (1) |
| (0) | (37) | (0) | (3) |
| (1) | (-37) | (0) | (1) |
| (2) | (37) | (0) | (3) |
| (3) | (-37) | (2) | (0) |

The file `completion_certificate.json` records this construction in a
machine-readable form.

## Exact verification

Since

\[
G_H=43I-2J,
\qquad
G_H^{-1}=\frac{I+2J}{43},
\]

and every row sum of (X_C) is (eta_c), the Schur complement is positive
definite exactly when

\[
M(C)=43G_S-X_CX_C^\ast-2|\beta_c|^2J
\]

is positive definite. The verifier constructs this (21\times21) Gaussian-
integer Hermitian matrix for every branch-labeled fiber point and performs
an exact (LDL^\ast) decomposition over (mathbb Q(i)). Every pivot is
proved to be a positive rational number. No numerical eigenvalue or
floating-point tolerance enters the certificate.

Run with CPython (3.12) or later:

    ./verify.sh

Expected summary:

    distinct_case_sigma_pairs=228
    branch_labeled_fiber_points=264
    positive_definite_completions=264
    nondefault_rotation_pairs=5
    direct_block_checks=12
    arithmetic=exact_rational_gaussian
    shifted_gram_mechanism=exhausted
    certificate=verified

## Scope and trust boundary

The theorem imports the coupled-transform autocorrelation targets, the six
canonical exact sums, and the primitive cross-trace identity. It proves that
the entire autocorrelation-only shifted-Gram route is too weak; the missing
invariant is whether a proposed cross-correlation sequence is realizable by
the pointwise (16)-state coupling.

The verifier also constructs the original (42\times42) block matrix and
checks it directly for both endpoint fibers in every case, independently
checking the Schur-complement normalization. The finite positivity certificate
is exact but trusts the published CPython implementation, interpreter,
operating system, and hardware. It does not
enumerate support words, support orbits, residue cells, local-state words,
or SAT assignments. It uses no ((1+i))-adic layer, floating point,
randomness, solver status, or timeout. QLP-42 remains unresolved.
