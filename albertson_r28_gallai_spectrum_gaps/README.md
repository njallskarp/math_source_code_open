# Gallai spectrum gaps eliminate the Albertson r=28 row 769

This directory closes the last three degree profiles in the exact
`(n,m)=(55,769)` Albertson frontier, conditional only on the explicitly stated
separator/profile input from Discovery Net heights 2569 and 2583.  It uses no
crossing-number improvement and no labelled graph enumeration.

## Theorem

Let `G` be a 28-critical graph with 55 vertices and 769 edges.  Suppose its
complement `H` has the height-2583 separator structure: a set
`B=T union {s}`, where `T` is a triangle, such that

    H-B = C union {w1} union {w2},       |C|=49,

the three displayed sets are components, and the degree-excess profile of
`G` is one of

    0^50 1^3 25^2,
    0^50 1^2 2 24 25,
    0^49 1^4 24 25.

Then no such `G` exists.  Combined with the height-2637 elimination of row
768 and the earlier profiles of row 769, this eliminates both exact order-55
frontier rows under the same separator-classification dependency.

## Gallai block spectra

Put `x_v=d_G(v)-27` and let `L=G[{v:x_v=0}]`.  Gallai's low-vertex theorem
says every block of `L` is a clique or an odd cycle.

Every clique block has order at most 26.  A larger one contains a low vertex
of `C`, since `B` has only four vertices and the singleton vertices are high.
That vertex would have at least 26 block neighbours and both `w1,w2` as
additional `G`-neighbours, exceeding degree 27.

There is at most one `K_26` block.  Two cannot share a cut vertex, and each
contains at least 22 vertices of `C`.  Those core vertices are saturated by
their 25 block neighbours and `w1,w2`.  Any other high vertex would therefore
have at least 44 neighbours in `H`, whereas every non-singleton high vertex
has `H`-degree at most 26.

For a Gallai forest with `c` components, put `u_Q=|Q|-1` for every block.
The block identity and edge contributions are

    |V(L)| = c + sum_Q u_Q,
    e(K_{u+1}) = u(u+1)/2,
    e(C_{u+1}) = u+1                 (even u>=4).

The exact generating-function/dynamic-programming expansion in `verify.py`
allows every multiset satisfying these identities, regardless of whether its
blocks form a realizable block tree.  Thus it is a relaxation.  Subject only
to clique order at most 26 and at most one `K_26`, its edge spectrum has the
two gaps

    |V(L)|=50:  581, then 600; no value in 582,...,599,
    |V(L)|=49:  559, then 576; no value in 560,...,575.

For readability, `audit.py` verifies the same endpoints from the convex block
packing cases.  Odd-cycle blocks cannot improve a case maximum: replace their
increment by clique increments no larger than the case cap, preserving the
total increment and weakly increasing the edge contribution.

## The two 50-low profiles

For either 50-low profile the high set `R` has five vertices and

    sum_{v in R} d_G(v) = 5*27+53 = 188.

The singleton components have no `H`-edge between them, so `w1w2` lies in
`G[R]`.  Since `1 <= e(G[R]) <= 10`, the exact degree identity gives

    e(L) = 769-188+e(G[R]) in [582,591].

This interval lies in the 50-vertex block-spectrum gap.

## The 49-low profile

Here the singleton excesses are 24 and 25, so their `H`-degrees are 3 and 2.
The height-2583 separator lemma has a unique local orbit of this degree type.
After relabelling,

    N_H(w1)={s,t3},       N_H(w2)={s,t1,t2},

and `s` is `H`-nonadjacent to all of `T={t1,t2,t3}`.  Hence the forced local
`G`-edges consist of `w1w2`, the three edges from `W` to its complementary
triangle vertices, and the three edges from `s` to `T`.

Let `k` of the four excess-one vertices lie in `C`.  Because exactly 49
vertices are low, exactly `k` vertices of `B` are low as well.  Both singleton
vertices are joined in `G` to every vertex of `C`.  Minimizing the forced
edges inside the high set over the `binom(4,k)` choices of low vertices of
`B` gives, for `k=0,1,2,3,4`,

    e(G[R]) >= 7,6,7,7,9,

respectively.  In particular `6 <= e(G[R]) <= binom(6,2)=15`.  Now

    sum_{v in R} d_G(v) = 6*27+53 = 215,
    e(L) = 769-215+e(G[R]) in [560,569],

which lies in the 49-vertex block-spectrum gap.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_gallai_spectrum_gaps
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 audit.py | diff -u EXPECTED_AUDIT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs and every manifest entry reports `OK`.

## Provenance and trust boundary

Gallai's theorem is from Tibor Gallai, *Kritische Graphen, II* (1963),
pp. 373--395; the Academy repository hosts the primary scan at
<https://real.mtak.hu/201455/>.  A modern primary-source statement is Theorem
1.3 of Kostochka--Rabern--Stiebitz,
<https://kostochk.web.illinois.edu/docs/accepted/dm-rs.pdf>.

Targeted primary-source and Discovery Net searches through 2026-09-05 found
no prior `r=28` row-769 spectrum-gap elimination.  This is a search-relative
novelty statement, not a claim of historical priority.

The checkers use exact Python integers, deterministic finite block-spectrum
expansion, the 16 choices of low vertices in the four-vertex separator, and
SHA-256.  They relax block-tree and degree realizability; they do not assume
it.  They do not re-prove Gallai's theorem, factor-criticality, the published
crossing estimates, or the height-2569 finite separator/component
classification inherited by height 2583.

The theorem stated at the top is unconditional under its explicit structural
hypotheses.  Its application to every possible Albertson `r=28`
counterexample remains review-gated on the finite height-2569/2583 separator
classification.  No `r=27` terminal theorem, `cr(24,132)>=165`, local crossing
conjecture, solver, floating point, or drawing topology is used.
