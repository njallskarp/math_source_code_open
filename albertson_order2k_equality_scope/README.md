# The order-\(2k\) equality-scope obstruction

This note separates two different equality theories for sparse critical
graphs. The distinction is load-bearing for the order-\(58\),
\(r=29\) Albertson frontier.

The sharp order-\(2k\) excess result of Kostochka--Stiebitz gives
\(f_k(2k)=k^2-3\). By contrast, the later theorem saying that equality
graphs are exactly the \(k\)-Ore graphs concerns equality in the
Kostochka--Yancey potential bound. These are not the same equality class.

## Proposition 1: the Ore-order obstruction

Every \(k\)-Ore graph has

\[
|V(G)|=1+s(k-1)
\]

for some positive integer \(s\). More precisely,

\[
|E(G)|=s\left(\binom{k}{2}-1\right)+1.
\]

Consequently, no \(k\)-Ore graph has order \(2k\) when
\(k\geq 3\).

### Proof

The base graph \(K_k\) has order \(1+(k-1)\) and
\(\binom{k}{2}\) edges. An Ore composition of graphs with parameters
\((n_1,m_1)\) and \((n_2,m_2)\) has parameters

\[
n=n_1+n_2-1,\qquad m=m_1+m_2-1.
\]

Induction gives both displayed formulas, with the new value of \(s\)
equal to the sum of the two old values. If \(2k=1+s(k-1)\), then

\[
s=2+\frac{1}{k-1},
\]

which is not an integer for \(k\geq3\).

## Proposition 2: exact potential separation

Let \(G\) have order \(2k\) and

\[
|E(G)|=k^2-3+t.
\]

Write

\[
X(G)=2|E(G)|-(k-1)|V(G)|
\]

for degree excess, and use the Kostochka--Yancey potential

\[
\rho_{KY}(G)=(k-2)(k+1)|V(G)|-2(k-1)|E(G)|.
\]

Then

\[
X(G)=2k-6+2t,\qquad
\rho_{KY}(G)=2k-6-2(k-1)t.
\]

The potential deficit from the \(k\)-Ore equality value
\(k(k-3)\) is exactly

\[
\Delta_t
=k(k-3)-\rho_{KY}(G)
=(k-2)(k-3)+2(k-1)t.
\]

Equivalently, if \(B_{KY}(k,2k)\) denotes the unrounded
Kostochka--Yancey edge lower bound, then

\[
|E(G)|-B_{KY}(k,2k)=\frac{\Delta_t}{2(k-1)}.
\]

Thus equality at \(t=0\) is equality in the older
Kostochka--Stiebitz excess theorem, but it is separated from
Kostochka--Yancey equality by the positive potential gap
\((k-2)(k-3)\).

For \(k=29\), the rounded Kostochka--Yancey floor at order \(58\)
is \(826\). The three rows \(838,839,840\) therefore lie exactly
\(12,13,14\) edges above that floor. Their potentials are respectively
\(52,-4,-60\), while the \(29\)-Ore equality potential is
\(754\).

## Corollary: the exact classification gap

The standard structural theorems meet the order-\(2k\) frontier on
opposite sides:

- Gallai's join structure and its extremal classification cover the
  low-order range through \(2k-1\), but not order \(2k\).
- Kostochka--Yancey's equality classification identifies the
  \(k\)-Ore graphs, but Proposition 1 excludes every such graph at order
  \(2k\).
- Kostochka--Stiebitz determine the minimum excess at order \(2k\), but
  the audited theorem statement and survey specify the value and possible
  equality orders, not a graph-by-graph classification of the order-\(2k\)
  equality family.

Accordingly, the order-\(58\) Albertson continuation needs a structural
theorem at the Kostochka--Stiebitz excess scale. An Ore-equality theorem cannot
be substituted. The exact missing input is one of the following:

1. classify the \(29\)-critical graphs of order \(58\) and excess
   \(52\), then test the no-\(TK_{29}\) four-block footprint;
2. prove a two-step stability theorem covering excesses \(52,54,56\);
   or
3. use the local no-\(TK_{29}\) and cross-deletion hypotheses directly
   to exclude those three excess levels.

This is a dependency and prior-art obstruction. It eliminates no frontier
row.

## Primary-source audit

The following sources were checked on 2026-09-05:

- Alexandr Kostochka, [*Color-Critical Graphs and Hypergraphs with Few
  Edges: A Survey*](https://kostochk.web.illinois.edu/docs/2008/book06.pdf),
  especially Theorems 5 and 6. Theorem 5 states the sharp excess bound and
  the equality orders; Theorem 6 records Gallai's low-order classification.
- Alexandr Kostochka and Matthew Yancey, [*Ore's Conjecture on
  Color-Critical Graphs Is Almost
  True*](https://arxiv.org/abs/1209.1050), for the potential bound.
- Alexandr Kostochka and Matthew Yancey, [*A Brooks-Type Result for Sparse
  Critical Graphs*](https://doi.org/10.1007/s00493-017-3068-3),
  Combinatorica 38 (2018), 887--934, Theorem 6, for the \(k\)-Ore equality
  classification, as quoted in the next source.
- Ron Gould, Victor Larsen, and Luke Postle, [*Structure in Sparse
  \(k\)-Critical Graphs*](https://arxiv.org/abs/2107.00976),
  Theorems 1.2 and 1.3, which state the Kostochka--Yancey potential theorem
  and its \(k\)-Ore equality characterization separately.

The literature statement is deliberately limited: these audited sources do
not supply the needed order-\(2k\) equality classification. This is not a
claim that no such theorem exists anywhere.

## Reproduction

Requires CPython 3.10 or later and only the standard library.

```bash
cd albertson_order2k_equality_scope
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected output ends with
`certificate_sha256=abcb8ce93e7330c829e08788d0574c6c0dfbbaee6641770c9025236b89ef8179`.

## Trust boundary

The checker verifies the Ore-composition recurrences, order congruence,
potential identities, exact rational gaps, and the \(k=29\)
specialization. It does not verify criticality of Ore compositions, the cited
critical-graph theorems, their prose proofs, the primary-source scope audit,
or the existence of any subdivision. No solver, floating point, randomness,
downloaded data, or generated certificate is used.
