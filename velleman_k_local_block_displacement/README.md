# K-local same-sign block displacement: sandwich and exact obstruction

## Result and scope

This is the second and final step in a bounded relaxation of Type R
lambda-permutations.  It starts from the blockwise-Type-R trichotomy proved in
`velleman_blockwise_type_r_trichotomy` and permits infinitely many adjacent
same-sign block inversions, but only with one fixed local-displacement bound.

The outcome is twofold:

1. an explicit completion-time sandwich survives with an `O(C+K)` window;
2. the comparison of two limits controls only a **joint positive/negative
   window mass**.  It no longer forces either one-sign substantial property.

This identifies the exact missing datum in the Type R proof.  Under a natural
joint-thinness hypothesis the singleton branch is restored; when both
substantial properties hold, the all-real branch is still restored.  The
remaining unrestricted case is not claimed solved.

The proof is analytic and combinatorial.  No finite permutation census,
solver, floating-point calculation, or experimental inference is used.

## Definitions

Let `S=sum_(n>=0) a_n` be conditionally divergent in Velleman's sense.  As in
arXiv:2507.20062v2, after adjoining an initial zero if needed, write its
alternating maximal sign blocks as

```text
N_1, P_1, N_2, P_2, ...,
```

where `a_n<=0` on `N_i` and `a_n>0` on `P_i`.  Put

```text
n_i = sum_{n in N_i} a_n <= 0,
p_i = sum_{n in P_i} a_n >= 0,
N[r,s] = n_r+...+n_s,
P[r,s] = p_r+...+p_s.
```

A permutation `sigma` is **K-local block-order preserving** if, separately
for each sign, there is a permutation `pi_epsilon` of the positive integers
which lists the order in which entire blocks are processed, such that:

- every element of block `B_(pi_epsilon(r))` occurs before every element of
  `B_(pi_epsilon(s))` whenever `r<s`;
- the order inside one block is arbitrary; and
- if `rho_epsilon=pi_epsilon^(-1)` is the position of a naturally labelled
  block, then

```text
|rho_epsilon(j)-j| <= K                           (D)
```

for every `j` and both signs.

Condition (D) is the promised bounded adjacent-inversion convention.  If
`j<i` is inverted, then

```text
rho(j)>rho(i),  rho(j)<=j+K,  rho(i)>=i-K,
```

so `i-j<2K`.  Thus a block has at most `2K-1` inverted earlier neighbors and
at most `2K-1` inverted later neighbors.  In a reduced adjacent-transposition
realization it participates in at most `4K-2` adjacent swaps.  The class
allows infinitely many inversions globally but only uniformly local ones.

Let `Z_K(S)` be the finite limits attained by such permutations which have
block number at most some finite `C`.  As the permutation fixes a divergent
series and is convergence-preserving by Velleman's bounded-block theorem, it
is a lambda-permutation.

For an out-of-range endpoint, prefix sums below use the empty-prefix
convention.

## K-local completion-time sandwich

**Theorem 1.**  Let `sigma` be K-local and have block number at most `C`.  Let

```text
T_i^- = max { sigma^(-1)(n) : n in N_i },
R_i(sigma) = sum_{t=0}^{T_i^-} a_(sigma(t)).
```

Then

```text
N[1,i+2K] + P[1,i-C-4K-1]
    <= R_i(sigma)
    <= N[1,i-2K] + P[1,i+C+4K].                 (1)
```

The `2K` whole-block error is unavoidable in kind: termwise convergence
`a_n->0` alone does not make it `o(1)`.

### Proof

Let `h=rho_-(i)`.  At `T_i^-`, every nonpositive block of negative-order rank
at most `h` is complete and every block of larger rank is untouched.  From
`|h-i|<=K` and (D):

```text
N_j is complete for j<=i-2K,
N_j is untouched for j>=i+2K+1.                  (2)
```

Since nonpositive masses have the reverse order under inclusion, their
selected total `Q_-` obeys

```text
N[1,i+2K] <= Q_- <= N[1,i-2K].                   (3)
```

For the positive stream, choose its frontier rank `q` so that all ranks below
`q` are complete, rank `q` is incomplete (possibly untouched), and all ranks
above `q` are untouched.  Again by (D),

```text
P_j is complete for j<=q-K-1,
P_j is untouched for j>=q+K+1.                   (4)
```

The global block-number bound couples `q` and `h`.  If
`q<h-C-2K`, then for every

```text
j=q+K+1,...,h-K
```

the block `N_j` is complete and `P_j` is untouched.  These selected
nonpositive blocks lie in more than `C` distinct components of the selected
original-index set, contradiction.  Therefore

```text
q >= h-C-2K.                                     (5)
```

If `q>h+C+2K`, then the completed positive blocks

```text
P_(h+K+1),...,P_(q-K-1)
```

are separated by untouched nonpositive blocks.  Together with the component
containing the already selected `N_i`, they again give more than `C`
components.  Hence

```text
q <= h+C+2K.                                     (6)
```

Combining (4)--(6) with `i-K<=h<=i+K`, the selected positive total `Q_+`
satisfies

```text
P[1,i-C-4K-1] <= Q_+ <= P[1,i+C+4K].             (7)
```

Adding (3) and (7) proves (1).  For `K=0`, keeping track of the uniquely
active natural block removes the one-index envelope loss and recovers the
sharper blockwise-Type-R sandwich.  QED.

## Consequences for attainable values

Recall the substantial properties of arXiv:2507.20062v2:

```text
ST_P: some k,epsilon>0 have P[i,i+k]>=epsilon eventually;
ST_N: some k,epsilon>0 have N[i,i+k]<=-epsilon eventually.
```

Call `S` **jointly thin** if for every fixed `L>=0`,

```text
liminf_(i->infinity) ( P[i-L,i+L] - N[i-L,i+L] ) = 0.   (JT)
```

The quantity is nonnegative.  In particular, `p_i->0` and `n_i->0` imply
(JT), but (JT) also permits sparse large blocks provided both signs have
simultaneously thin windows arbitrarily far out.

**Theorem 2 (proved branches and the obstruction).**  Suppose `Z_K(S)` is
nonempty.

1. If both `ST_P` and `ST_N` hold, then `Z_K(S)=R`.
2. If (JT) holds, then `Z_K(S)` is a singleton.
3. More sharply, if `r_1>r_2` both belong to `Z_K(S)`, and `C` bounds the two
   witnessing block numbers, then eventually

```text
P[i-C-4K,i+C+4K] - N[i-2K+1,i+2K]
    > (r_1-r_2)/2.                                (8)
```

Thus two distinct limits force joint substantiality of fixed windows.  This
is exactly what the original Type R comparison proves after local block
inversions; it does **not** force `ST_P` or `ST_N` separately.

### Proof

For the all-real branch, let one witnessing permutation have limit `r_0` and
block bound `C`.  The lower half of (1), after putting
`j=i-C-4K-1`, gives a fixed integer `L=C+6K+1` such that

```text
S_(q_j) + N[j+1,j+L] <= R_(j+C+4K+1)(sigma).      (9)
```

The upper half, after putting `j=i-2K`, gives

```text
R_(j+2K)(sigma) <= S_(m_j) + P[j,j+C+6K].         (10)
```

Here `q_j,m_j` are the final original indices of `P_j,N_j`.  Since the middle
terms tend to `r_0`, (9)--(10) are exactly the two fixed-window estimates used
in the greedy Type R lag argument.  `ST_N` bounds how far the greedy
permutation can advance in the negative stream before starting the next
positive block; `ST_P` gives the symmetric bound.  Therefore the ordinary
Type R greedy rearrangement to every prescribed real target has bounded block
number.  It belongs to the K-local class (with zero displacement), proving
`Z_K(S)=R`.

For the comparison statement, choose witnesses for `r_1,r_2`, enlarge `C` to
bound both, and put `epsilon=(r_1-r_2)/4`.  For every sufficiently large `i`,
convergence and (1) give

```text
r_1-epsilon
  < N[1,i-2K] + P[1,i+C+4K],

N[1,i+2K] + P[1,i-C-4K-1]
  < r_2+epsilon.
```

Subtracting is exactly (8).  Under (JT), take `L` larger than both displayed
window radii.  A subsequence on which the larger joint window tends to zero
contradicts (8).  Hence at most one finite value is attainable.  QED.

## Why term decay does not remove the new error

The whole-block obstruction already occurs for `K=1` in a conditionally
divergent series with terms tending to zero.  For each `m>=1`, make both
blocks `N_(2m-1),N_(2m)` consist of `m` copies of `-1/m`, and both
`P_(2m-1),P_(2m)` consist of `m` copies of `1/m`.  In natural order the
partial sums repeatedly traverse an interval of length one, so the series
diverges.

Order both sign streams by

```text
2,1,4,3,6,5,...
```

and, for each block label in that order, alternate its negative and positive
terms.  The resulting partial sums alternate between `-1/m` and zero, hence
converge to zero.  The selected original indices have a uniformly bounded
number of components (at most four), so this is a lambda-permutation with
`K=1`.

When `N_(2m)` is exhausted before `N_(2m-1)`, its selected nonpositive mass
differs from the natural prefix through `N_(2m)` by one full unit, although
every individual term has size `1/m`.  This proves that the `2K` mass window
in (1) cannot be replaced merely by a termwise `o(1)` error.  The example does
not refute the attainable-set trichotomy; it certifies the obstruction in the
proof mechanism.

## Exact remaining lemma and stop decision

The unrestricted K-local trichotomy is reduced to one precise question:

> Does joint substantiality (8), together with the existence of two
> convergent bounded-block witnesses, force both one-sign substantial
> properties, or can correlated positive/negative mass spikes support a
> proper non-singleton attainable set?

No further subclass or displacement hierarchy is introduced here.  Per the
two-wake stopping rule, this lane stops at this reduction unless an
independent review supplies the missing implication or a concrete correlated
spike construction.

## Reproduction and trust boundary

No software is required.  Verify the public files with:

```bash
shasum -a 256 velleman_k_local_block_displacement/README.md \
  velleman_k_local_block_displacement/claim_manifest.json
```

Trust boundaries:

- Velleman's equivalence between bounded block number and convergence
  preservation is external prior art.
- The Type R substantial-property theorem and greedy lag argument are taken
  from arXiv:2507.20062v2.
- The K-local definition, sandwich (1), obstruction (8), conditional branches,
  and explicit `K=1` stress test are proved here.
- Novelty is search-relative.  Searches through 2026-09-02 found the 2025
  paper's proposal to relax same-sign block order, but no treatment of this
  bounded-displacement class.

## Primary references

1. Polymath Jr. 2020 Collaboration and Yunus Zeytuncu, *Type R
   lambda-Permutation Approach to Velleman's Open Problem*,
   https://arxiv.org/abs/2507.20062v2 (2025).
2. Daniel J. Velleman, *A Note on lambda-Permutations*, American Mathematical
   Monthly 113 (2006), 173--178,
   https://doi.org/10.1080/00029890.2006.11920294.
