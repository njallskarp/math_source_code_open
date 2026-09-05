# Exact excess saturation at the order-`2k` frontier

This note records the sharp degree-excess boundary that any continuation of
the order-`2k` diamond argument must cross.  It is a dependency correction,
not an elimination of an `r=29` row.

## Proposition 1 (three-level saturation)

Let `G` be a `k`-critical graph on `2k` vertices, in the standard sense that
every proper subgraph is `(k-1)`-colourable, and put

```text
X(G)=sum_z (d_G(z)-(k-1))=2e(G)-2k(k-1).
```

Then

```text
X(G) >= 2(k-3).
```

Consequently, if `e(G)<=k^2-1`, there is a unique `t in {0,1,2}` such that

```text
e(G)=k^2-3+t,              X(G)=2(k-3)+2t.                 (1)
```

If `ell` is the number of vertices of degree `k-1`, then

```text
ell >= 2k-X(G)=6-2t.                                      (2)
```

### Proof

Kostochka--Stiebitz proved that a `k`-critical graph which is neither `K_k`
nor a member of their exceptional family `F_k` has excess at least
`2(k-3)`.  The two excluded families have orders `k` and `2k-1`, whereas
`G` has order `2k`, so the bound applies.

The integer `X(G)` is even.  The upper bound `e(G)<=k^2-1` is equivalent to
`X(G)<=2k-2`; hence the only possible even values between the two bounds are
`2k-6,2k-4,2k-2`, giving (1).  Finally every non-low vertex contributes at
least one to `X(G)`, so `2k-ell<=X(G)`, proving (2).

For `k=29`, (1)--(2) are exactly

```text
(m,X,ell_lower_bound)=(838,52,6),(839,54,4),(840,56,2).
```

Thus the three order-58 rows are not merely close to a convenient degree
threshold: they exhaust the first three parity levels above the sharp
critical-graph floor.

## Proposition 2 (the six-unit obstruction is genuine)

The proposed generic strengthening

```text
X(G) >= 2k                                                   (3)
```

is false for `k`-critical graphs of order `2k`: for every `k>=4` there is
such a graph with `e(G)=k^2-3`, hence `X(G)=2k-6`.  This is the exact value
`f_k(2k)=k^2-3` in the Kostochka--Stiebitz theorem, restated explicitly by
Kostochka--Yancey.

This does **not** refute (3) after adding the local four-block escape and
no-`TK_k` hypotheses of `STANDARD_BRANCH_SEPARATION.md`.  It proves that any
such strengthening must consume those extra hypotheses, rather than follow
from order, criticality, or a generic degree count alone.

## Alignment with the separation family

The family in `STANDARD_BRANCH_SEPARATION.md` has

```text
e(H_k)=7k-16,
e(G_k)=2k^2-8k+16,
X(G_k)=2k^2-14k+32.
```

At `k=29` this is `e(G_29)=1466` and `X(G_29)=1308`.  Moreover that family
is proved `k`-**vertex**-critical, not `k`-critical with respect to every
proper subgraph.  It therefore separates canonical routing, but it is not a
near-extremal witness against a strengthened excess statement for an actual
minimal Albertson counterexample.

Conversely, the proofs of the endpoint overlay, two-leaf escape, and
four-block footprint use vertex-critical deletion colourings and local
no-`TK_k` routing.  They do not use edge-criticality or the structure behind
the Kostochka--Stiebitz excess theorem.  This is the exact interface gap.

## Minimal resumption theorem

Scalar recurrence and profile enumeration remain frozen.  A structural
continuation at order 58 must exclude, under the no-`TK_k` and four-block
escape hypotheses, the three edge-critical classes

```text
C_t={G: |V(G)|=2k, G k-critical,
          X(G)=2(k-3)+2t},             t=0,1,2.             (4)
```

It is enough to prove that no member of any `C_t` supports the height-2945
rectangle/external-edge footprint.  For `t=0`, the class is nonempty without
the local hypotheses, so an argument must distinguish its extremal members
using the topological or cross-deletion data.  For `t=1,2`, an appropriate
stability form of the excess theorem would also suffice.

This three-class statement is strictly more precise than asking for another
local factor identity: it names the only excess levels relevant to the
frontier and the missing hypothesis--edge-critical near-extremal structure--
that no present diamond lemma uses.

## Primary sources and trust boundary

The external theorem is A. Kostochka and M. Stiebitz, *Excess in
colour-critical graphs*, Bolyai Society Mathematical Studies 7 (1999),
87--99.  Its statement and the equality orders are reproduced in A.
Kostochka, [*Color-Critical Graphs and Hypergraphs with Few Edges: A
Survey*](https://kostochk.web.illinois.edu/docs/2008/book06.pdf), Theorem 5.
The identity `f_k(2k)=k^2-3` is also stated in A. Kostochka and M. Yancey,
[*Ore's Conjecture on Color-Critical Graphs Is Almost
True*](https://arxiv.org/abs/1209.1050), introduction and Section 5.

The checker uses only exact Python integers to verify the algebra, parity
levels, `r=29` rows, and the separation-family formulas.  It does not verify
the cited critical-graph theorem, construct its equality examples, prove the
local diamond theorems, or decide whether an extremal graph contains a
`TK_k`.

## Reproduction

Requires CPython 3.10 or later and only the standard library.

```sh
cd albertson_order2k_diamond_capacity
PYTHONDONTWRITEBYTECODE=1 python3 verify_excess_saturation.py \
  | diff -u EXPECTED_EXCESS_SATURATION.txt -
shasum -a 256 -c SHA256SUMS
```
