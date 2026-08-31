# Coupled half-sum/half-difference transform for the norm-32 QLP-42 shell

## Exact reformulation

Let `X` be a length-42 sequence over `{1,i,-1,-i}`.  In the Chinese-remainder
coordinates `Z_42 = Z_21 x Z_2`, put

```text
x_j = X_(22*j mod 42),
y_j = X_(22*j+21 mod 42),
S_X(j) = (x_j-y_j)/(1+i),
H_X(j) = (x_j+y_j)/(1+i).
```

Every coordinate `(S_X(j),H_X(j))` is one of exactly 16 states, in bijection
with the ordered pair `(x_j,y_j)`.  Both entries lie in the ternary Gaussian
grid `{-1,0,1}+i*{-1,0,1}`, and pointwise

```text
|S_X(j)|^2 + |H_X(j)|^2 = 2,
Re(S_X(j)*conj(H_X(j))) = 0.
```

For `0 <= s <= 20`, direct expansion gives

```text
PAF(X,s)-PAF(X,s+21) = 2*(-1)^s*PAF(S_X,s),
PAF(X,s)+PAF(X,s+21) = 2*PAF(H_X,s).             (1)
```

Consequently the representative norm-32 residual shell is realized by
normalized fourth-root words `A,B` if and only if four length-21 ternary
Gaussian words `(S_A,H_A,S_B,H_B)` satisfy the 16-state pointwise coupling,
one of six sum cases below, and the two combined autocorrelation targets

```text
PAF(S_A,s)+PAF(S_B,s) =
  43  at s=0,
  -2  at s in {4,17},
   2  at s in {10,11},
   0  otherwise;

PAF(H_A,s)+PAF(H_B,s) =
  41  at s=0,
  -2  at every nonzero s.                         (2)
```

This is a bijective reformulation, not merely a necessary projection.  The
half-difference equations alone discard the `H` constraints and can admit
states that do not lift to fourth-root words.  Equations (1) reconstruct the
two original lags from (2), while the 16-state table reconstructs every
ordered phase pair.

## Canonical sum cases

For a canonical order-two compression representative `(p,q,x,y)`,

```text
sum(S_A) = (p+q) + (q-p)i,    sum(H_A) = 0,
sum(S_B) = (x+y-1) + (y-x)i,  sum(H_B) = 1.
```

The six representatives are

```text
(1,0,5,0), (3,0,4,1), (3,0,3,-2),
(3,2,3,2), (3,2,2,3), (4,1,2,-1).
```

The transform exposes two complementary structures simultaneously: the
previous sparse half-difference target of total energy 43 and a paired
half-sum target of energy 41 whose every out-of-phase value is `-2`.  It also
retains the mod-4 quarter-turn restriction because the unit-support cells of
`S_X` and `H_X` are the same local states.

## Verification

Run

```bash
python3 verify_coupled_half_transform.py
```

The standard-library verifier uses Gaussian-integer pairs.  It checks the
16-state bijection and pointwise identities, exhausts all `4^6=4096`
fourth-root words of length six to verify both autocorrelation identities at
every independent shift, derives both norm-32 targets, and checks all six sum
cases.  No floating-point arithmetic, SAT result, or heuristic output enters
the theorem.

## Scope and source context

This reformulation does not decide whether the norm-32 shell is realizable
and does not settle QLP-42.  Its immediate use is to strengthen exact search:
any solver using only the half-difference word should add the coupled
half-sum word and the 16-state lift table.

Primary context for even/odd separation, compression, and the QLP-42 open
case is Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
arXiv:2408.16318.  The QLP definition and decompression framework appear in
Kotsireas--Winterhof, *Quaternary Legendre Pairs*, arXiv:2212.10953.  A
targeted search found even/odd separation but not this coupled 16-state
norm-32 formulation; apparent novelty is limited to that search and the
current Discovery Net graph, not a claim of literature priority.
