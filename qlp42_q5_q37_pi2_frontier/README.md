# The `(1+i)^2` frontier obstruction at QLP-42 `q=5,37`

## Exact intermediary theorem

Start with the 36 independent-rotation binary-shadow orbits certified in
[`../qlp42_q5_q37_binary_frontier/frontier_orbits.tsv`](../qlp42_q5_q37_binary_frontier/frontier_orbits.tsv).
The exact Gaussian sum parities retain 18 orbits in the `q=5` branch and,
after simultaneous complement, 18 in the `q=37` branch.

For each retained support, encode a quarter-cell axis by `beta_j in F_2` and
an opposite/equal nonquarter cell by `t_j in F_2`.  Reducing the twenty
nonzero-shift autocorrelation equations after division by `pi=1+i` gives an
affine system over `F_2`.  On every one of these 36 supports:

1. the ten `S` equations and ten `H` equations are identical;
2. the resulting ten-equation system has rank exactly 10;
3. every support orbit has a solution in every one of the six canonical
   exact-sum cases; hence this entire residue layer excludes no support orbit.

This is a useful obstruction: any further frontier reduction must use at least
one bit of information absent modulo `pi^2`, such as the next Gaussian residue
layer or the full integer autocorrelation equations.

## Why the twenty equations collapse

Let `u_j` be the quarter indicator and take `t_j=0` on quarter cells.  For a
fixed family and nonzero shift `s`, the post-division `S` coefficient is

```text
F_S(s) = sum_j u_j u_(j+s)(beta_j + beta_(j+s))
       + sum_j (u_j t_(j+s) + t_j u_(j+s))                 in F_2.
```

For `H`, the quarter axis is `beta+u` and the nonquarter coefficient is
`1+u+t`.  The axis correction is zero termwise, while the cross-term
correction is

```text
sum_j (u_j + u_(j+s)) = 2 wt(u) = 0 in F_2.
```

Thus `F_H(s)=F_S(s)`.  The target autocorrelations are `0` or `+/-2`; their
post-division residues also vanish modulo `pi`, so they do not break the
identity.  The independent programs additionally derive the affine maps from
exact Gaussian arithmetic and exhaust all `C(42,2)=861` second differences on
each support, certifying that no quadratic bit interaction was discarded.

## Exact sums and census

The canonical `(p,q,x,y)` cases are

```text
(1,0,5,0), (3,0,4,1), (3,0,3,-2),
(3,2,3,2), (3,2,2,3), (4,1,2,-1).
```

A diagonal local term contributes independently signed real and imaginary
units; a quarter term contributes a signed unit on its chosen axis.  Therefore
`d` diagonal terms and `r` quarter terms can realize an integer coordinate
`T` exactly iff `abs(T) <= d+r` and `T = d+r (mod 2)`.  Applying this elementary
criterion to all four transformed sums gives the following counts of unsigned
axis/type assignments.  These are feasibility counts, not counts of sign
realizations.

| branch | residue solutions | case 1 | case 2 | case 3 | case 4 | case 5 | case 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=5` | 9,998,086,928 | 4,998,889,150 | 4,999,037,012 | 4,998,893,762 | 4,998,982,000 | 4,998,982,000 | 4,998,988,120 |
| `q=37` | 22,280,142,848 | 11,127,703,552 | 11,137,966,104 | 11,129,476,680 | 11,127,112,942 | 11,127,112,942 | 11,128,782,484 |

Every one of the 18 support orbits in each branch contributes positively to
every displayed case count.

## Independent verification

[`analyze_pi2_frontier.py`](analyze_pi2_frontier.py) derives the affine maps
using exact pairs of integers, uses exhaustive subset enumeration and
meet-in-the-middle matching, and prints every orbit-level count.

[`verify_pi2_frontier.cpp`](verify_pi2_frontier.cpp) is independently written.
It again derives the residues from exact Gaussian arithmetic, but counts with
familywise dynamic programming over `(weight,syndrome)` states.  It checks the
aggregate constants in [`expected_summary.txt`](expected_summary.txt), asserts
rank 10 and positive counts for every orbit/case, and is also run under
AddressSanitizer and UndefinedBehaviorSanitizer.

Reproduce everything with:

```bash
CXX=/opt/homebrew/bin/g++-16 ./verify_all.sh
```

The recorded Python exhaustive run took 76.6 seconds and about 157 MB maximum
RSS.  The C++ release verifier took 2.2 seconds and about 9 MB maximum RSS on
the same Apple-arm64 host.  No floating point, randomness, heuristic cutoff,
solver status, concurrency, or time limit enters either computation.

## Scope and sources

This does not construct or exclude a quaternary Legendre pair of length 42.
It proves that the complete `pi^2` consequence, even combined with energy and
exact-sum feasibility, leaves every parity-compatible binary-shadow orbit
alive.  The trust boundary is the established coupled transform and local
16-state table, the input frontier manifest and its checked SHA-256
`f1dff75420fb37a2454767a7177367045e100ab07a07a11addd5e5551407d89e`,
the elementary sign-sum lemma, the two implementations, toolchains, operating
system, and hardware.

Primary context is Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, <https://arxiv.org/abs/1302.0571>;
Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
<https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two constructions of
quaternary Legendre pairs of even length*, <https://arxiv.org/abs/2408.08472>;
and Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
<https://arxiv.org/abs/2408.16318>.  A targeted primary-source and committed-
graph search found no matching `q=5,37` `pi^2` frontier census.  Apparent
novelty is relative to those searches, not a historical-priority claim.

The strongest next step is the `pi^3` layer on these same 36 support orbits,
with the four exact sums imposed during enumeration rather than afterward.
