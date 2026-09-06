# Sharp four-connectivity in degree-22 Ramsey neighborhoods

## Result and scope

Every graph \(H\) with 22 vertices, no red \(K_4\), no independent
five-set and at least 101 red edges satisfies

\[
\kappa(H)\geq4.
\]

In particular, this holds for every degree-22 deficiency-at-most-six
neighborhood in the order-43 Ramsey program, where the local edge condition
is \(e(H)\geq114-6=108\). The connectivity bound is **sharp on that
entire local family**: the exact graph below has 108 edges and connectivity
four. Thus neither five-connectivity nor six-connectivity follows from
these local hypotheses.

By the classical Chvátal–Erdős theorem, \(\kappa(H)\geq\alpha(H)\)
implies Hamiltonicity. Therefore every graph in the stated family has a
red Hamiltonian cycle. It may be labeled along one such cycle in a complete
search. This is a relabeling normalization, **not** a cyclic-automorphism
assumption. A prescribed common core or other anchored labels cannot be
retained arbitrarily under that relabeling.

This excludes the whole family of local separator profiles of size at most
three. It does not exclude the degree-22 deficiency-six branch, any complete
\(M\)-value, or a hypothetical Ramsey graph on 43 vertices. The sharpness
witness is a 22-vertex neighborhood graph, not a 43-vertex coloring. No new
Ramsey-number bound is claimed. Sharpness concerns connectivity at 108 edges;
the sufficient edge threshold 101 is not asserted optimal.

## Uniform separator proof

Suppose \(S\) is a vertex cut with \(s=|S|\leq3\). Independence numbers
of distinct components of \(H-S\) add, so their sum is at most four.
A component of independence number 1, 2 or 3 has at most 3, 8 or 17 vertices,
respectively, by \(R(4,2)=4\), \(R(4,3)=9\) and \(R(4,4)=18\).
There are at least 19 surviving vertices. Every partition of the independence
budget except \(1+3\) has total capacity at most 16. Consequently there
are exactly two components: a clique \(B\) of size \(b\leq3\), and a
\((4,4)\) graph \(A\) of size \(a\leq17\), with
\(a+b+s=22\).

Every vertex has at most eight red neighbors in \(A\). Indeed, its
neighborhood inside \(A\) is triangle-free (otherwise it completes a
red \(K_4\)) and has no independent four-set, so \(R(3,4)=9\) applies.
This holds both for vertices in \(A\) and for vertices of \(S\). Hence

\[
e(H[A])\leq4a,\qquad e_H(S,A)\leq8s.
\]

There are no \(A\)-to-\(B\) edges. Turán's bound on the
\(K_4\)-free graph induced by \(S\cup B\) gives

\[
e(H)\leq4a+8s+\left\lfloor\frac{(s+b)^2}{3}\right\rfloor.
\]

The complete remaining cases are small because they arose from the
independence budget, not from a graph census:

| \(s\) | \(a\) | \(b\) | Edge upper bound |
| ---: | ---: | ---: | ---: |
| 2 | 17 | 3 | 92 |
| 3 | 17 | 2 | 100 |
| 3 | 16 | 3 | 100 |

Thus \(e(H)\geq101\) contradicts every cut of size at most three.
This proof uses no catalogue completeness premise or solver output.

## Exact sharpness construction

On \(A=\{0,\ldots,16\}\), use the Paley graph: join distinct \(i,j\)
when \(i-j\) is a nonzero square modulo 17. On
\(S=\{17,18,19,20\}\), use the four-cycle in that order. Add vertex
21 adjacent to all of \(S\) and none of \(A\). The red neighborhoods
in \(A\) of vertices 17 through 20 are, respectively,

\[
\begin{aligned}
&\{0,1,3,4,6,10,11,15\},\\
&\{0,2,3,6,7,9,12,14\},\\
&\{1,2,5,7,8,12,13,15\},\\
&\{2,4,5,8,9,11,14,16\}.
\end{aligned}
\]

There are \(68+32+4+4=108\) red edges. Direct verification finds no
red four-clique and no independent five-set. Removing \(S\) leaves
components of orders 17 and 1. All 1,794 deletions of at most three vertices
leave a connected graph, establishing \(\kappa(H)=4\) by direct checking
as well as by the uniform theorem. The red degree profile is
\(4^1\,9^3\,10^{13}\,11^5\).

[WITNESS.json](WITNESS.json) contains both these signatures and an independent
graph6 serialization. Adding one universal red vertex gives a directly
checked 23-vertex Ramsey \((5,5)\) local cone. The other 20 vertices needed
for an order-43 completion are **not supplied or asserted to exist**.

## Reproduction and evidence

Use CPython 3.11 or newer; only the standard library is required. The observed
interpreter was CPython 3.12.12. No solver, floating-point arithmetic, optimization
certificate, randomness or external catalogue input is needed for replay.

```sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_VERIFY.json
python3 -B -O verify.py | cmp - EXPECTED_VERIFY.json
python3 -B audit.py | cmp - EXPECTED_AUDIT.json
python3 -B -O audit.py | cmp - EXPECTED_AUDIT.json
python3 -B test_verify.py | cmp - EXPECTED_TEST.json
python3 -B -O test_verify.py | cmp - EXPECTED_TEST.json
shasum -a 256 -c SHA256SUMS
```

Expected: empty comparisons; both graph verifiers check 108 edges, zero
forbidden cliques and the exact connectivity four. Five malformed inputs
are rejected. A deliberately inserted red \(K_4\) is detected; long-path
controls guard against radius-capped connectivity checks. The independent
clique routine matches 3,300 definition-level tests on all graphs through
order five. Each full verifier runs in well under one second on the observed
machine; no timeout or incomplete computation supports the result.

Canonical sorted red-edge list SHA-256 (compact JSON plus newline):
`7ad8fce8852efd386b3ec188841e114930c9ab8856d80c5e8339b8c73805032a`.

[verify.py](verify.py) reconstructs the modular construction and uses literal
subsets and set-based graph traversal. [audit.py](audit.py) imports no producer
code: it decodes the graph6 integer, uses bitset clique recursion, and computes
components by repeated bitset closure. Their exact edge hashes agree.
[test_verify.py](test_verify.py) supplies the rejection controls.

## Literature, graph context and trust boundary

The component-independence argument is standard; height 2405 already uses it
for different hard-branch exact-anchor graphs. Height 2775 supplies the
degree-22 deficiency-six context. Neither its sharp pair-root examples nor
any author-only audit is a premise of this separator theorem.

Primary literature checked on 2026-09-06:

- [Angeltveit–McKay, Section 3.4](https://arxiv.org/html/2409.15709v2)
  gives the local extremum 114 and the near-extremal gluing context.
- [Xu–Shao–Radziszowski, Section 5](https://www.cs.umd.edu/~gasarch/TOPICS/const_ramsey/xsr.pdf)
  proves connectivity and Hamiltonicity results for Ramsey-critical graphs,
  including order 24 in the \((4,5)\) case. Its critical-order hypothesis
  does not directly cover the present order-22 edge-threshold statement.
- [Chvátal–Erdős, *A note on Hamiltonian circuits*](https://doi.org/10.1016/0012-365X(72)90079-9)
  supplies the classical Hamiltonicity implication; it is also explicitly
  stated and applied in the preceding primary paper.
- [McKay's primary catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  records the small Ramsey values and the Paley order-17 context. No catalogue
  files or catalogue-completeness assumptions are needed to check this example.

No priority claim is made. The contribution is the density-sensitive separator
bound and the concrete sharpness certificate at the assigned local threshold,
not the classical connectivity method, Paley graph or Hamiltonicity theorem.
The uniform proof trusts the cited small Ramsey bounds, Turán and
Chvátal–Erdős, plus the displayed unformalized argument. The finite certificate
trusts ordinary CPython integer, JSON and file semantics, SHA-256 and hardware.
Different author-written verification algorithms are not independent peer
review or proof-assistant formalization.
