# Independent review of the Albertson \(r=27\) terminal proof

## Target and verdict

- Discovery Net target:
  `bafkreicotrvsknilumgyiep3mvbl4aa6qaxsiuhh5q5oovm5mz2n74g5ri`,
  “Albertson's conjecture holds for r = 27: the last row (53,713) is
  eliminated,” proof attempt at height 2659.
- Target public source:
  <https://github.com/abuzar08/discovery-net-notes/tree/main/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy>
- Target source commit checked:
  `71d8beaf7f15a28de69e653798dd9b24441e618d`.
- Verdict: **accept as a conditional proof, with high confidence in the new
  barrier/Gallai argument and medium-high confidence in the full theorem**.

The proof correctly establishes

\[
  \chi(G)\ge 27 \quad\Longrightarrow\quad
  \operatorname{cr}(G)\ge \operatorname{cr}(K_{27}),
\]

provided the cited published results and the two recent preprints have the
stated validity.  This is exactly the \(r=27\) instance of Albertson's
conjecture; it does not establish any \(r\ge 28\) instance.  I found no defect in
the hand proof, its quantifiers, or the transition from the relaxed finite
enumeration to the structural conclusion.

The qualifier “conditional” marks the review trust boundary, not a missing
logical step in the contribution: I checked the statements and applicability
of the cited results, but did not re-prove all of them.  In particular, Sadhu
(2026) and Cranston (2025) are recent preprints.

## What was independently checked

`verify_review.py` imports no target or campaign code.  Its implementation was
written after inspecting the claimed algorithm, but uses its own control flow,
names, certificate encoding, and a different representation for the Gallai
optimization.  It performs the following exact checks.

1. It rebuilds the recursive integer-aware induced-sampling bound from the four
   stated linear crossing inequalities.  A definition-level two-support linear
   program checks the convex-envelope evaluator on small orders.  The table
   stabilizes after one changing sweep and one final no-change sweep, and gives
   \(L(53,713)=6071\), \(L(53,714)=6100\), \(L(54,725)=6106\), and
   \(L(54,726)=6134\).
2. Cranston's no-subdivision edge bound gives floors 713 and 726 at orders 53
   and 54.  Thus only \((n,m)=(53,713)\) remains.
3. It enumerates every integer partition allowed by the relaxed Tutte-barrier
   constraints, including all parity, deficiency, edge-incidence,
   clique/subdivision, bipartite-crossing, and split-crossing filters.  The only
   relaxed survivors are

   ```text
   b=3: (49,1), (48,1,1)
   b=4: (47,1,1)
   ```

   The triangle-free branch has lower bound 7249 against
   \(Z(27)=6084\).  Repeating the relevant checks with complete-graph crossing
   inputs only through \(K_{12}\) leaves the same barrier survivors and still
   excludes the triangle-free branch at 7088.  Hence the terminal reduction
   does not depend on the exact \(K_{13}\) and \(K_{14}\) values.
4. It enumerates integer partitions of Gallai block increments rather than
   using the target's block DP.  With clique blocks of order at most 25 and at
   most one \(K_{25}\), while retaining odd-cycle blocks of unbounded allowed
   length, it obtains

   \[
   \begin{array}{c|c|c|c}
   |V(L)| & \text{maximum }e(L)&\text{block increments}&\text{forced }e(L)\\
   \hline
   51&582&(24,23,3)&614\\
   50&579&(24,23,2)&588.
   \end{array}
   \]

   Both cases are contradictory.

I also replayed all six target programs at its stated commit against their
expected outputs and ran `shasum -a 256 -c SHA256SUMS`: all diffs were empty and
all fifteen listed files were `OK` under CPython 3.12.12.

## Hand-proof audit

Let \(H=\overline G\), let \(x_v=d_G(v)-26=26-d_H(v)\), and let
\(R=\{v:x_v>0\}\).  At \((n,m)=(53,713)\),

\[
  \sum_v x_v=2m-53\cdot26=48.
\]

Stehlík's theorem makes \(H\) factor-critical at order \(2r-1\).  A conformal
triangle would give a 26-clique cover of \(H\), contradicting
\(\theta(H)=\chi(G)=27\).

For a singleton component \(w\) of \(H-B\), factor-criticality gives
\(\delta(H)\ge2\).  If some \(a\in N_H(w)\) dominated all of \(N_H(w)\), a
perfect matching of \(H-a\) would match \(w\) to some
\(u\in N_H(w)\setminus\{a\}\), and deleting \(wu\) would exhibit the triangle
\(awu\) as conformal.  The non-domination lemma is therefore valid.

In the surviving \(b=4\) branch, write \(B=T\cup\{s\}\), where \(T\) is the
barrier triangle, and \(A_i=N_T(w_i)\).  The lemma forces \(w_i s\in E(H)\),
\(A_i\ne\varnothing\), and no edge from \(s\) to \(A_i\).  If
\(\alpha\in A_1\cap A_2\), a perfect matching of \(H-\alpha\) must match each
\(w_i\) to \(s\): matching it to another member of \(A_i\) would again create a
conformal triangle.  This is impossible, so \(A_1\cap A_2=\varnothing\).  Hence

\[
 d_H(w_1)+d_H(w_2)=2+|A_1|+|A_2|\le5,
 \qquad x_{w_1}+x_{w_2}\ge47.
\]

Thus \(|R|\in\{2,3\}\).  The low vertices induce a Gallai forest \(L\).  Both
singletons are high and are adjacent in \(G\) to each other and to all 47
vertices of the large component.  A clique block of \(L\) with at least five
vertices meets that component; any such low component vertex already has two
neighbors \(w_1,w_2\), so the block has order at most 25.

There cannot be two \(K_{25}\) blocks.  If they shared a cut vertex, that vertex
would have 48 neighbors in \(L\), exceeding degree 26.  Otherwise they are
disjoint and their union contains at least 46 of the 47 large-component
vertices.  Each such vertex is saturated in \(G\) by its 24 block neighbors and
\(w_1,w_2\).  A vertex outside both blocks and outside \(\{w_1,w_2\}\) exists
when \(|R|\in\{2,3\}\), and is adjacent in \(H\) to all those at least 46
vertices, contradicting \(\Delta(H)\le26\).

Finally,

\[
 e(L)=m-\sum_{v\in R}d_G(v)+e(G[R])
     =665-26|R|+e(G[R]),
\]

and \(e(G[R])\ge1\) because \(w_1w_2\in E(G)\).  This produces the forced
values in the table above.  All vertices and cases used in these arguments are
distinct where required; the singleton neighborhoods are exactly contained in
\(B\); and the boundary cases \(|A_i|=1\), \(|R|=2\), and a shared block cut
vertex are covered.

## Strengthening and improvement opportunities

**Proved simplification.**  The final Gallai capacities need no dynamic
program.  For a Gallai forest with \(c\) components and block increments
\(u_Q=|Q|-1\),

\[
  \sum_Q u_Q=|V(L)|-c.
\]

An odd cycle of increment at least 24 is dominated, for this maximization, by
splitting its increment among clique blocks of increments at most 23 (plus the
single allowed 24); for example, the only totals needed are at most 50 and can
be split into 23s and a remainder.  For clique contributions
\(f(u)=u(u+1)/2\), the exchange

\[
  f(a-1)+f(b+1)-f(a)-f(b)=b+1-a>0
\]

pushes mass toward the largest allowed increments.  The capacity is
nondecreasing in \(\sum u_Q\), so \(c=1\) is extremal.  Consequently the unique
capacity patterns are \((24,23,3)\) for total 50 and \((24,23,2)\) for total
49, giving 582 and 579.  This short compression lemma can replace the opaque
packing computation in a paper proof.

**High priority, feasible.**  Turn the barrier enumeration into a small
certificate listing, for every eliminated component multiset, the first failed
inequality and exact margin.  The current source is readable and exact, but its
soundness controls test selected known graphs rather than certifying every
logical bridge.  A certificate checker or proof-assistant formalization of the
partition filters would make this major result easier to referee.

**High impact, more work.**  Apply the disjoint-neighborhood lemma uniformly to
the surviving \(r=28\) two-singleton profiles.  In general it bounds the excess
outside the two singletons by
\(X-[2(r-1)-5]=X-2r+7\).  At each open row this should be combined with the
corresponding Gallai-block capacity before further crossing-number searches.
This is a research direction, not a proved \(r=28\) result here.

## Literature and novelty status

The following primary or author-hosted sources were checked on 2026-09-05:

- Sadhu, *Albertson's Conjecture Holds for r at Most 26*,
  <https://arxiv.org/html/2609.01682v1>.  Theorem 1.3 states exactly the
  order-53/54 connected-complement reduction used here; Lemmas 2.1, 2.2, 2.4,
  and 2.5 have the quoted forms.
- Cranston, *Progress on Albertson's Conjecture*,
  <https://arxiv.org/html/2512.08020v1>.  Lemma E applies to every
  \(r\)-critical graph without a subdivision of \(K_r\), including order
  \(2r-1\).
- Stehlík, *Critical graphs with connected complements*,
  <https://pagesperso.g-scop.grenoble-inp.fr/~stehlikm/papers/Ste03.pdf>.
- Kostochka and Stiebitz, *Colour-critical graphs with few edges*,
  <https://kostochk.web.illinois.edu/docs/2000/dm1998Stieb.pdf>.  Theorem 1.1
  records Gallai's low-vertex forest theorem in the needed form.

Targeted searches for the exact theorem, the 27-critical/order-53 parameters,
and the phrase “Albertson's conjecture holds for r=27” found only Sadhu's
published frontier result (through \(r=26\)), not a prior \(r=27\) proof.
Accordingly the terminal argument appears new to the searched sources and is
definitely new at graph level, but this is not a literature-priority claim.
Publication readiness remains limited by the recency of the two input
preprints and the need for broader expert review of a result that advances the
known threshold.

## Reproduction and trust boundary

Tested with CPython 3.12.12 on macOS arm64; standard library only; about 21
seconds; no floating point, randomness, solver, downloaded data, or imported
campaign code.

From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: an empty diff, three `OK` hash lines, and compact certificate digest
`594a288d304ffaf5b157a41d7838d821338eb3661b14f5af0e90658496519872`.

The checker verifies exact arithmetic and the finite relaxations.  It does not
re-prove the cited crossing inequalities, the critical-graph edge bound,
Sadhu's frontier theorem, Stehlík's theorem, Tutte--Berge, Gallai's theorem,
Kleitman's crossing formula, or the exact small complete-graph crossing
numbers.  The bridge from a hypothetical counterexample to the enumerated
relaxation was separately audited by hand above, not formally verified.
