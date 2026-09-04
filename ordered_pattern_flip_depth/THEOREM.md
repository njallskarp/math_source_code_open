# Flip-depth exactness for ordered pattern-clique extremal numbers

## 1. Statement

An `r`-partite `r`-pattern `P` consists of two disjoint `r`-edges whose
vertices occur in `r` consecutive two-vertex blocks.  Label the edge containing
the first vertex `A` and the other edge `B`.  Its normalized orientation word
is

    epsilon=(epsilon_1,...,epsilon_r),
    epsilon_1=+1,

where `epsilon_i=+1` if block `i` is `AB` and `epsilon_i=-1` if it is `BA`.
Let

    f(P)=#{i in {1,...,r-1}: epsilon_i != epsilon_(i+1)}

be the number of flips.  Let `P^(m)` denote the unique ordered `P`-clique of
`m` edges.

This flip count is intrinsic to the ordered pattern: exchanging the two
unlabeled edges changes every sign and the normalization changes them all
back, while reversing the ground-set order reverses the word and possibly all
signs, neither of which changes its number of sign changes.

**Theorem (flip-depth exactness).**  Let `m>=2` and `0<=s<=f(P)`, and put
`N=rm+s`.  Then

    ex_<(N,P^(m)) = binom(N,r)-binom(r+s,r).               (1)

Equivalently, every family of deleted `r`-edges meeting all copies of
`P^(m)` on `[N]` has at least `binom(r+s,r)` members, and this is sharp.

In particular, if `P` has at least two flips, then the Anastos--Jin--Kwan--
Sudakov conjecture holds at the first previously open boundary `N=rm+2`:

    ex_<(rm+2,P^(m)) = binom(rm+2,r)-binom(r+2,2).         (2)

The cases `m=1` and `s=0` are immediate.  The theorem is nontrivial for
`m>=2` and `s>=1`.

## 2. Canonical cliques indexed by weak multisets

For `1<=j<=m`, put

    p_i(j) = j             if epsilon_i=+1,
             m+1-j         if epsilon_i=-1,
    b_i(j) = (i-1)m+p_i(j).

The canonical copy of `P^(m)` on `[rm]` has edges

    B_j={b_i(j):1<=i<=r}.                                  (3)

For every weakly increasing `s`-tuple

    Q=(q_1,...,q_s),  0<=q_1<=...<=q_s<=r,

delete from `[N]` the positions

    X_Q={q_t m+t:1<=t<=s}.                                 (4)

They are strictly increasing and lie in `[N]`.  Define the cumulative count

    c_Q(i)=#{t:q_t<i}.                                     (5)

The order-preserving embedding of `[rm]` into `[N]\X_Q` sends every position
in block `i` to that position plus `c_Q(i)`.  Indeed, the deleted positions
with `q_t<i` are exactly those preceding the image of block `i`: sortedness
gives `t<=c_Q(i)` in the first case and `t>c_Q(i)` in the second, which places
`q_t m+t` on the required side of every shifted block position.  Therefore the
canonical clique `C_Q` on `[N]\X_Q` has edges

    E_(j,Q)={b_i(j)+c_Q(i):1<=i<=r},  1<=j<=m.             (6)

There are exactly

    #{Q}=binom(r+s,s)=binom(r+s,r)                         (7)

such canonical cliques.

## 3. Total-variation collision inequality

**Lemma.**  If `0<=s<=f(P)`, the edge sets of the cliques `C_Q` in (6) are
pairwise disjoint.

**Proof.**  Suppose an edge `E_(j,Q)` equals `E_(k,R)`.  The entries in (6)
are increasing, so equality holds coordinatewise.  With `d=j-k`, this gives

    c_R(i)-c_Q(i)=epsilon_i d,  1<=i<=r.                  (8)

If `d=0`, the cumulative counts agree.  Their first value gives the
multiplicity of `0`, their successive differences give the multiplicities of
`1,...,r-1`, and `s-c_Q(r)` gives the multiplicity of `r`.  Hence `Q=R`.

Suppose instead that `d` is nonzero.  For `0<=t<=r`, let

    Delta_t = multiplicity_R(t)-multiplicity_Q(t).

Writing `h_i=c_R(i)-c_Q(i)`, cumulative differences give

    Delta_0=h_1,
    Delta_i=h_(i+1)-h_i  for 1<=i<r,
    Delta_r=-h_r.                                         (9)

Since `h_i=d epsilon_i`, its discrete total variation is

    sum_(t=0)^r |Delta_t|
      = |h_1|+sum_(i=1)^(r-1)|h_(i+1)-h_i|+|h_r|
      = 2|d|(f(P)+1).                                     (10)

On the other hand, `Delta` is the difference of the multiplicity vectors of
two `s`-element multisets, so

    sum_(t=0)^r |Delta_t| <= 2s.                          (11)

Equations (10)--(11) imply `|d|(f(P)+1)<=s`, impossible because
`|d|>=1` and `s<=f(P)`.  Thus `d=0` and `Q=R`; distinct selected cliques
share no edge. `square`

The threshold for this particular packing is exact.  At `s=f(P)+1`, define
the signed multiplicities

    Delta_0=epsilon_1,
    Delta_i=epsilon_(i+1)-epsilon_i  (1<=i<r),
    Delta_r=-epsilon_r.                                   (12)

The positive and negative parts both have mass `f(P)+1`.  Let `R` and `Q`
be the corresponding multisets.  Then `c_R(i)-c_Q(i)=epsilon_i`, and for
`m>=2`, equation (8) produces the collision

    E_(2,Q)=E_(1,R).                                      (13)

This does not disprove the extremal conjecture beyond flip depth; it shows
only that the present edge-disjoint packing cannot cross that boundary.

## 4. Extremal upper bound

Let `G` be a `P^(m)`-free ordered `r`-graph on `[N]`, and let `D` be its set
of missing edges.  Each canonical clique `C_Q` must contain an edge of `D`.
The cliques are pairwise edge-disjoint by the lemma, so these missing edges
are distinct.  From (7),

    |D|>=binom(r+s,r),

and hence

    |E(G)|<=binom(N,r)-binom(r+s,r).                       (14)

## 5. Matching construction

For completeness, here is the matching lower bound from the primary source.
For `1<=i<r`, let `a_i` be the number of vertices of the second pattern edge
strictly between the `i`th and `(i+1)`st vertices of the first edge, and let
`a_r` be the number after its last vertex.  Then `a_i>=0` and

    a_1+...+a_r=r.                                        (15)

Delete precisely the `r`-sets `e={e_1<...<e_r}` satisfying

    e_(i+1)-e_i > a_i(m-1)  for 1<=i<r,
    e_r <= N-a_r(m-1).                                    (16)

The remaining ordered `r`-graph is `P^(m)`-free.  Otherwise, order a
hypothetical clique's edges by their first vertices.  Between consecutive
vertices of its first edge, each of the other `m-1` edges contributes the
prescribed `a_i` vertices, and after its last vertex they contribute `a_r`
vertices.  Thus its first edge satisfies (16) and was deleted.

The shift

    y_i=e_i-(m-1) sum_(h<i) a_h                           (17)

is a bijection from the deleted edges to the `r`-subsets of
`[N-r(m-1)]=[r+s]`.  Consequently exactly `binom(r+s,r)` edges are deleted,
matching (14) and proving (1). `square`

## 6. Scope, prior art, and trust boundary

Anastos, Jin, Kwan, and Sudakov prove the construction in Section 5 and
conjecture its optimality for all `r,n,m` and all `r`-partite patterns.  They
prove every `m=2` case and every `n` for the alternating pattern.  The reviewed
Discovery Net theorem at height 1509 proves every pattern through `n=rm+1`.
The present theorem reaches `n=rm+s` uniformly through the sign-change depth
and, in particular, proves the review's proposed `rm+2` frontier for every
pattern with at least two flips.

Primary source: Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny Sudakov,
*Extremal, enumerative and probabilistic results on ordered hypergraph
matchings*, Forum of Mathematics, Sigma 13 (2025), e55,
https://doi.org/10.1017/fms.2024.144; open manuscript
https://arxiv.org/abs/2308.12268.

The upper bound and collision inequality are self-contained symbolic proofs.
The lower bound is reproduced above rather than treated as a black box.  The
companion exact checker validates the embedding formula, disjointness, sharp
collision at depth `f+1`, and the lower construction over a finite parameter
box.  Computation is corroborative and does not establish the universal
theorem.
