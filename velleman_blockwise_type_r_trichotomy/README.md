# Blockwise-Type-R lambda-permutations: the trichotomy survives

## Scope and status

This note studies the first relaxation proposed in Section 4 of
Polymath Jr. 2020 Collaboration and Yunus Zeytuncu,
*Type R lambda-Permutation Approach to Velleman's Open Problem*,
arXiv:2507.20062v2 (2025).  The relaxation preserves the order of the
positive blocks and the order of the nonpositive blocks, but permits an
arbitrary order inside each individual block.

The result below is a self-contained proof, not a computational inference.
The definitions and the substantial-property terminology follow
arXiv:2507.20062v2.  Velleman's block-number characterization is treated as
prior art.  The novelty claim is deliberately search-relative: targeted
searches on 2026-09-02 found the relaxation proposed in the 2025 paper, but
no proof of the result below.

## Definitions

Let `S=sum_(n>=0) a_n` be a conditionally divergent real series in Velleman's
sense: the series diverges, but some permutation makes it converge.  Put

```text
P = {n : a_n > 0},       N = {n : a_n <= 0}.
```

Write the maximal consecutive components, in their original order, as

```text
P_1, P_2, ...            and            N_1, N_2, ... .
```

As in the Type R paper, an initial zero may be adjoined so that the blocks
alternate as `N_1,P_1,N_2,P_2,...`.  This changes neither attainable sums nor
any eventual statement below.  Write

```text
p_i = sum_{n in P_i} a_n >= 0,
n_i = sum_{n in N_i} a_n <= 0.
```

For a permutation `sigma` of the indices, let

```text
E_t(sigma) = {sigma(0),...,sigma(t)}
```

and let `b_t(sigma)` be the number of maximal intervals of consecutive
integers whose disjoint union is `E_t(sigma)`.  Its block number is
`sup_t b_t(sigma)`.  By Velleman's theorem, bounded block number is equivalent
to convergence preservation.  If such a permutation fixes the present
divergent series, it is a lambda-permutation: its inverse cannot also preserve
convergence, since applying that inverse to the convergent rearrangement would
make the original series converge.

A permutation `sigma` is **blockwise Type R for S** if, for each sign and all
block indices `i<j`, every element of the earlier block occurs before every
element of the later block:

```text
u in P_i, v in P_j  =>  sigma^(-1)(u) < sigma^(-1)(v),
u in N_i, v in N_j  =>  sigma^(-1)(u) < sigma^(-1)(v).
```

There is no restriction on the order of elements within one `P_i` or one
`N_i`, nor on the interlacing of the active positive and nonpositive blocks.
A **blockwise-Type-R lambda-permutation** is a blockwise-Type-R permutation
with bounded block number whose rearranged series converges to a finite real
value.  Let `Z_BR(S)` be the set of all such values.

For integers `r<=s`, use

```text
P[r,s] = p_r + ... + p_s,       N[r,s] = n_r + ... + n_s.
```

The positive substantial property `ST_P` means that some `k`, `epsilon>0`,
and `i_0` satisfy `P[i,i+k] >= epsilon` for all `i>i_0`.  The negative property
`ST_N` is defined symmetrically by `N[i,i+k] <= -epsilon`.

## Completion-time sandwich

**Lemma.**  Let `sigma` be blockwise Type R with block number at most `C`.
Let

```text
T_i^- = max { sigma^(-1)(n) : n in N_i },
R_i(sigma) = sum_{t=0}^{T_i^-} a_{sigma(t)}.
```

With empty out-of-range block sums understood as zero,

```text
N[1,i] + P[1,i-C]  <=  R_i(sigma)
                         <=  N[1,i] + P[1,i+C-1].       (1)
```

**Proof.**  At time `T_i^-`, block order says that all of `N_1,...,N_i` and
no later nonpositive block have been selected.

If `P_(i-C)` were not complete, then no later positive block could have
started.  The unselected part of `P_(i-C)` and the unselected positive blocks
after it would separate the selected initial portion from each of
`N_(i-C+1),...,N_i`.  Thus `E_(T_i^-)(sigma)` would have at least `C+1`
components, a contradiction.  Hence every positive block through `P_(i-C)`
is complete.

If any element of `P_(i+C)` had been selected, every earlier positive block
would be complete.  Since no block `N_(i+1),N_(i+2),...` has started, those
unselected nonpositive blocks would separate the selected initial portion and
the selected pieces `P_(i+1),...,P_(i+C)`, again producing at least `C+1`
components.  Hence `P_(i+C)` has not started.  The selected positive mass is
therefore between `P[1,i-C]` and `P[1,i+C-1]`; the selected nonpositive mass
is exactly `N[1,i]`.  This proves (1).  Notice that internal order has vanished
because the stopping time exhausts `N_i`.  QED.

### What fails at the old labeled endpoint

The distinction between an original endpoint and a completion time is
essential.  In a two-term nonpositive block with terms `(-1,-1)`, the internal
swap can output the last original index first.  At that instant only `-1`, not
the full block mass `-2`, has appeared.  Thus the original Type R notation
"the partial sum when the last index of `N_i` is selected" cannot be reused.
The error at an arbitrary time is bounded only by the total masses of the two
currently active blocks:

```text
|partial_sum(sigma) - partial_sum(straightened sign schedule)|
    <= p_(active positive block) + |n_(active nonpositive block)|.   (2)
```

This need not tend to zero.  Formula (1), rather than an unjustified `o(1)`
claim in (2), is the correct generalized block-boundary inequality.

## Main theorem

**Theorem (blockwise-Type-R trichotomy).**  For every conditionally divergent
real series `S`,

```text
Z_BR(S) is empty, a singleton, or all of R.
```

More precisely, if `Z_BR(S)` is nonempty, then

```text
ST_P and ST_N both hold       =>  Z_BR(S) = R;
at least one of them fails    =>  |Z_BR(S)| = 1.            (3)
```

**Proof.**  Empty is tautological.  Suppose first that `ST_P` and `ST_N`
hold and that `sigma_0` is one blockwise-Type-R lambda-permutation, with block
number `C_0` and finite limit `r_0`.  Applying (1) to `sigma_0` gives exactly
the boundary estimate used in the Type R proof:

```text
S_(q_(i-C_0)) + N[i-C_0+1,i] <= R_i(sigma_0)
                                  <= S_(m_i) + P[i,i+C_0-1]. (4)
```

Here `q_j` and `m_j` are the original final indices of `P_j` and `N_j`.
Because `R_i(sigma_0)->r_0`, (4) and the two substantial properties give the
same uniform finite bound on the lag of the two sign streams as in the greedy
Riemann construction: for any target `r`, repeatedly take the first unused
positive term while the running sum is at most `r`, and the first unused
negative term while it is greater than `r`.  The usual term-to-zero argument
gives convergence to `r`.  The lag bound derived from (4) gives a bounded
block number (the proof of Theorem 3.1(1) of arXiv:2507.20062v2 uses no other
property of `sigma_0`).  This greedy permutation is ordinary Type R, hence is
also blockwise Type R.  Therefore every real `r` lies in `Z_BR(S)`.

For completeness, the lag step is quantitative.  From the left side of (4)
and convergence, there is a constant `B` with

```text
S_(q_i) + N[i+1,i+C_0] < B                              (5)
```

eventually.  If `ST_N` is witnessed by `(k,epsilon)`, choose `M` with
`B-M*epsilon<r`.  Summing `M` consecutive substantial groups in (5) shows
that the greedy rule cannot reach `N_(i+C)` before starting `P_(i+1)`, where
`C=C_0+M(k+1)+1`.  The symmetric estimate from `ST_P` bounds lag in the other
direction.  A bounded lag between the two in-order sign streams gives bounded
block number.

Now suppose, for example, that `ST_P` fails.  If two blockwise-Type-R
lambda-permutations `sigma_1,sigma_2` had distinct limits `r_1>r_2`, let `C`
bound both block numbers.  Apply (1) at their respective completion times and
use convergence.  For all sufficiently large `i`, with
`epsilon=(r_1-r_2)/4`,

```text
r_1-epsilon < N[1,i] + P[1,i+C-1],
N[1,i] + P[1,i-C] < r_2+epsilon.
```

Subtracting yields

```text
P[i-C+1,i+C-1] > (r_1-r_2)/2                           (6)
```

for every sufficiently large `i`.  This is precisely `ST_P`, a contradiction.
If `ST_N` fails, use the upper estimate for `sigma_1` at `i` and the lower
estimate for `sigma_2` at `j=i+2C-1`; cancellation of the positive prefixes
gives

```text
N[i+1,i+2C-1] < -(r_1-r_2)/2,
```

which is `ST_N`, again a contradiction.  Hence a nonempty `Z_BR(S)` has at
most one element whenever either substantial property fails.  This proves
(3) and the trichotomy.  QED.

## Sharpness and next bounded relaxation

No assumption that individual block masses tend to zero is needed.  In fact,
(2) shows why such an assumption would be an artificial route: internal-order
error can remain macroscopic at ordinary times, yet the exact completion-time
sandwich still controls attainable limits.

Because this first relaxation inherits the Type R argument, the next and only
planned relaxation is **K-local block order**: for each sign, the order in
which whole same-sign blocks are exhausted is a permutation of their natural
order with displacement at most `K`; internal order remains arbitrary.  The
falsifiable next target is:

> Determine whether a completion-time sandwich with a fixed `O(C+K)` window
> suffices to prove the same trichotomy, or exhibit a series for which the
> finitely many out-of-order active block masses create two but not all finite
> attainable values.

This is one bounded step beyond blockwise Type R, not an open-ended hierarchy.
The likely obstruction is explicit: unlike internal disorder, an unexhausted
or prematurely exhausted neighboring block contributes its **whole mass** at
the natural completion boundary, and substantiality of only one sign may not
control that error.

## Reproduction and trust boundary

No software is required for the proof.  Reproduce the source audit and file
hashes from the repository root with:

```bash
curl -fsSL https://arxiv.org/e-print/2507.20062v2 -o /tmp/type-r-v2.tar
mkdir -p /tmp/type-r-v2 && tar -xf /tmp/type-r-v2.tar -C /tmp/type-r-v2
rg -n 'Positive/Negative block|Type R|bounded block|substantial|Future works' \
  /tmp/type-r-v2/*.tex
shasum -a 256 velleman_blockwise_type_r_trichotomy/README.md \
  velleman_blockwise_type_r_trichotomy/claim_manifest.json
```

Trust boundaries:

- Velleman's equivalence between convergence preservation and bounded block
  number is external prior art.
- The 2025 Type R theorem, terminology, and its greedy lag argument are
  external prior art; the completion-time replacement and its use for the
  relaxed class are proved here.
- No floating point, solver, exhaustive subset enumeration, or empirical
  inference enters the theorem.
- Literature novelty is search-relative, not a claim of exhaustive novelty.

## Primary references

1. Polymath Jr. 2020 Collaboration and Yunus Zeytuncu, *Type R
   lambda-Permutation Approach to Velleman's Open Problem*,
   [arXiv:2507.20062v2](https://arxiv.org/abs/2507.20062v2), 2025.
2. Daniel J. Velleman, *A Note on lambda-Permutations*, American Mathematical
   Monthly 113 (2006), 173--178,
   [DOI 10.1080/00029890.2006.11920294](https://doi.org/10.1080/00029890.2006.11920294).
3. Steven G. Krantz and Jeffery D. McNeal, *Creating More Convergent Series*,
   American Mathematical Monthly 111 (2004), 32--38.
