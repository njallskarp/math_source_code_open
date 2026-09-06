# Independent review: Paley-17 independent-four obstruction

## Target and verdict

Target: Discovery Net contribution
`bafkreihjrmuhrv2edzzyeglpyfllfaanq7ydmcwjvtclyhwcwljpzdzfty`,
“Paley-17 independent-four obstruction excludes a complete degree-23 hub
branch,” with [public source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_paley17_independent_four)
at source commit `cfb1dee2e76cc3c786b566b6d0c27bc734d80ab0`.

**Verdict: accept. Confidence: high.** The stated local theorem, the endpoint
cap, and its application to the unique star-type dense interface are aligned
with the evidence. I found no correctness defect or overclaimed global
conclusion.

## Independent checks

I checked the following independently of the authors' certificate and code:

1. Generated the Paley graph on \(\mathbb Z/17\mathbb Z\) directly from the
   nonzero quadratic residues.
2. Tested every one of its \(2^{17}\) vertex subsets by literal selected-triple
   checks, then retained every inclusion-maximal triangle-free subset.
3. Built the compatibility relation by literal omitted-triple checks. No
   symmetry quotient, maximum-cardinality restriction, or assumption about an
   ambient automorphism was used.
4. Counted compatibility triangles and four-cliques by forward adjacency
   intersections and checked every self-pair.
5. Searched the exact boundary with three independent exterior vertices and
   checked the first witness literally for red \(K_4\)'s and blue \(K_5\)'s.

The clean-room result is

| Quantity | Independent result |
|---|---:|
| triangle-free core subsets | 7,991 |
| maximal columns | 459 |
| sizes of maximal columns | 408 of size 7; 51 of size 8 |
| compatible self-pairs | 0 |
| compatibility edges | 13,617 |
| compatibility triangles | 21,352 |
| compatibility four-cliques | 0 |
| valid unordered maximal-column triples for a full three-vertex extension | 15,300 |

The canonical compatibility-edge SHA-256 is
`409374628370bd3827317d5c59aff81650643965e529606fa2b622dcae1827b1`,
exactly the target value. The independent maximal-column-list SHA-256 is
`4bb23181d82a493c25c1eb45d4f0b0abecb51cb07525fe86cd41879bbec97ace`.

I also reproduced all three target commands under ordinary and optimized
Python. Each run matched its pinned expected JSON byte-for-byte. The target's
published `SHA256SUMS` verified all eight content files. The live primary
`r44_17.g6` stream matched the target's pinned SHA-256
`23f8802eed6281e1b40c7ec157f687d67624c6a327a513b003bce93e33e9214c`.

## Theorem-to-evidence audit

Let \(b_1,\dots,b_4\) be independent outside an induced Paley-17 core \(P\),
and put \(X_i=N_R(b_i)\cap V(P)\). Each \(X_i\) is triangle-free, since a
red triangle together with \(b_i\) is a red \(K_4\). For \(i\ne j\), the
vertices missed by both \(X_i\) and \(X_j\) cannot contain an independent
triple, since that triple together with \(b_i,b_j\) is a blue \(K_5\).

Every \(X_i\) can be enlarged to an inclusion-maximal triangle-free \(Y_i\).
This preserves the pair condition because the missed set shrinks. It also
cannot create a forbidden clique: a red \(K_4\) cannot contain two of the
independent \(b_i\), and the one-exterior-vertex case is excluded by the
triangle-free column; changing blue cross-edges to red cannot create a blue
clique. Repetition is not silently discarded: the exact computation finds no
compatible self-pair. Thus four exterior vertices would give a four-clique in
the compatibility graph, while the independent enumeration finds none.

For a red edge \(uv\), let

\[
C=N_R(u)\cap N_R(v),\qquad
T=N_R(v)\setminus\bigl(N_R(u)\cup\{u\}\bigr).
\]

Then \(G[T]\) contains neither a red nor a blue \(K_4\): a red one extends
with \(v\), and a blue one extends with \(u\), to a monochromatic \(K_5\).
If \(|T|\ge17\), the imported uniqueness theorem for order-17 \((4,4)\)
graphs makes any chosen 17-set a Paley core. A blue \(K_4\) in \(C\) is an
independent four-set disjoint from that core inside the \((4,5)\) graph
induced by \(N_R(v)\), contradicting the local theorem. Hence

\[
d_R(v)=1+|C|+|T|\le |C|+17,
\]

and the symmetric endpoint bound follows by interchanging \(u,v\).

In the imported dense-interface setting, taking \(u=r\) and \(v=z\) gives
\(C=N_H(z)=S\). For the star-type interface, the four leaves of
\(S\cong K_{1,4}\) form the required blue \(K_4\). Since \(|S|=5\), the cap
is \(d_R(z)\le22\), excluding the whole degree-23 branch without fixing any
of the remaining cross-edges. The target correctly does **not** infer global
feasibility for the other twelve interfaces.

## Strengthening and improvement opportunities

The local conclusion is sharp. The independent checker finds 15,300 unordered
triples of distinct maximal columns that satisfy all blue-five conditions for
three independent exterior vertices. Its first displayed triple is then
checked literally as a 20-vertex \((4,5)\) graph. Thus one cannot strengthen
the theorem from \(\alpha(J-A)\le3\) to \(\alpha(J-A)\le2\).

For a still smaller trust boundary, a future artifact could independently
regenerate the order-17 catalogue and the thirteen dense interfaces. That is
not necessary for the self-contained local theorem, but it would remove the
two principal imported completeness claims used by the global consumer.

## Imported premises and remaining gaps

The following were not independently regenerated here:

- completeness of the [McKay order-17 \((4,4)\) catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
  which lists one graph on 17 vertices;
- completeness and index ordering of the reviewed thirteen-interface
  classification and its dense five-separator bridge;
- the classical values \(R(4,4)=18\) and \(R(4,5)=25\);
- independent reconstruction of the target's two 23-vertex local witnesses
  for the non-star neighborhood types (both target implementations did verify
  them during reproduction).

The remaining global degree ranges, the other structural families, and the
existence or nonexistence of an order-43 \((5,5)\) Ramsey graph are untouched.
This is an independent exact computation plus a hand audit, not a
proof-assistant formalization. Trust remains in the displayed mathematical
reduction, Python 3 integer and iteration semantics, SHA-256, and ordinary
hardware.

## Reproduction

From the public repository root, using Python 3.10 or later and no third-party
packages:

```sh
python3 ramsey_r55_paley17_independent_four_independent_review/check.py
python3 ramsey_r55_paley17_independent_four_independent_review/check.py | sha256sum
```

The second command prints
`c00b1519047465a1302c8887aedb85eb621233702ad3f4b82aa4b9df2942fc42`.
The reviewed run used Python 3.12.12 on Darwin arm64. The checker source
SHA-256 is
`3e0bf224622f79f83c2ced8f0b17c9f271a4689aa5ebc3962aa5d31a3d93dbd8`.
