# Primitive quotient kernel for quaternary Legendre pairs of length 42

## Result

Let `A,B` be length-42 sequences over `{1,i,-1,-i}` and put

```text
c_s = PAF(A,s) + PAF(B,s),
e_0 = c_0 - 84 = 0,
e_s = c_s + 2                 (1 <= s < 42).
```

For a divisor `d` of 42, define the quotient sequence

```text
Q_d(A)_r = sum_{j congruent to r (mod d)} A_j.
```

The quotient-correlation equations forced by a quaternary Legendre pair are
equivalent to the vanishing of every residue-class sum of `e` modulo `d`.
Imposing the three maximal proper divisors `d=6,14,21` therefore imposes every
proper-divisor quotient equation.

Write `E(x)=sum_s e_s x^s`.  The simultaneous proper-quotient equations hold
if and only if

```text
E(x) = P(x) H(x),
P(x) = (x^42-1)/Phi_42(x)
     = x^30-x^29+x^28+x^23-x^22+x^21
       -x^9+x^8-x^7-x^2+x-1,
deg H <= 11.
```

Equivalently, the residual Fourier transform is supported only at primitive
42nd-root characters.  The full rational kernel has dimension 12.

Autocorrelation gives `e_(42-s)=conj(e_s)` and `e_0=0`.  Moreover each `c_s`
is a sum of 84 fourth roots, so `Re(e_s)+Im(e_s)` is even; coefficientwise,
`1+i` divides `E`.  Since `P(0)=-1`, it also divides `H`.  Writing
`H=(1+i)G`, anti-reciprocity of `P` reduces the integral Hermitian kernel to

```text
G_(12-k) = i*conj(G_k)  (1 <= k <= 5),
G_6 = (1+i)t,
```

with five freely chosen Gaussian integers and one ordinary integer `t`.
Thus the actual correlation-residual lattice has rank 11 over the integers.

For the explicit basis used by the verifier, its Gram matrix is the matrix
printed by `verify_primitive_quotient_kernel.py`.  Exact rational LDL
decomposition proves `M-I` positive definite.  Consequently a vector with
quadratic norm below 32 must have Euclidean coordinate norm at most 31.
`verify_residual_lattice_minimum.cpp` enumerates all 163,655,889 nonzero
integer coordinate vectors in that ball, up to global sign, and obtains

```text
min sum_s |e_s|^2 = 32.
```

Therefore an actual length-42 sequence pair satisfying every proper quotient
equation is either a genuine quaternary Legendre pair or has exact full
correlation residual energy at least 32.  This does not decide existence at
length 42; it identifies and quantifies the primitive-frequency obstruction
that every proper compression necessarily misses.

## Exact verification

The theorem and the finite minimum use only integer and rational arithmetic.

```bash
python verify_primitive_quotient_kernel.py

c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  verify_residual_lattice_minimum.cpp \
  -o verify_residual_lattice_minimum
./verify_residual_lattice_minimum
```

The first program verifies the cyclotomic factorization, exact rank 30 of the
combined quotient pushforward, a 12-vector rational kernel basis, the
11-vector integral Hermitian basis, its Gram matrix, and exact positive
definiteness of `M-I`.  The second performs the complete bounded enumeration.

`search_all_proper_quotients.cpp` and
`solve_all_proper_quotients_pysat.py` record exploratory searches for an
actual sequence pair in the quotient-feasible set.  The heuristic reached
residual quotient score 200; the initial exact SAT run did not finish within
the research window.  Neither observation is part of the theorem.

## Primary-source context

- I. S. Kotsireas, C. Koutschan, and A. Winterhof, *Quaternary Legendre
  pairs II*, Discrete Mathematics 348 (2025), 114501,
  <https://arxiv.org/abs/2408.16318>.  This records 42 as the smallest
  unresolved even length and develops compression/PSD search restrictions.
- I. S. Kotsireas and A. Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>.  This gives the definition, balance
  normalization, compression, and PSD framework.
- J. Jedwab and T. Pender, *Two constructions of quaternary Legendre pairs of
  even length*, Combinatorial Theory 5 (2025), Paper 15,
  <https://arxiv.org/abs/2408.08472>.
- I. S. Kotsireas et al., *Legendre pairs of lengths congruent to 0 modulo 5*,
  <https://arxiv.org/abs/2111.02105>, for the broader use of compression as a
  search-space reduction.
- T. Pender, PhD thesis, Simon Fraser University (2026), Chapter II,
  <https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf>.

A targeted search of these primary sources and arXiv found compression and
PSD restrictions, but not the simultaneous-all-proper-quotient cyclotomic
kernel, its rank-11 integral Hermitian form, or the exact energy gap 32.  The
result is therefore apparently new relative to that search, not a claim of
literature priority.

## Trust boundary

The algebraic verifier is standard-library Python.  The finite minimization is
a direct C++ enumeration after the exact positive-definiteness certificate.
No floating-point calculation, SAT result, heuristic trajectory, or external
computer-algebra output is trusted for the theorem.
