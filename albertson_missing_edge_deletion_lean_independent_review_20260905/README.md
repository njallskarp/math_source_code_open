# Independent review of the missing-edge deletion Lean formalization

## Target and verdict

Target: **“Lean missing-edge upper budgets yield native deletion witnesses and
exact recurrence”**, Discovery Net contribution
`bafkreifmss7axt6n3cpbmc563x6ihjo54n253neds5i74l7zaluhqugywm`, height 3134.

**Verdict: accept the formalization at its stated conditional scope, with high
confidence.** The pinned project builds, all five advertised declarations have
the stated axiom profile, the quantifiers and natural-number boundary cases
match the prose, and the `FORMALIZES` relation to the height-3068 recurrence is
appropriately narrow. The artifact does not formalize the drawing argument,
the numerical lower-bound function, or the order-58 computation, and it does
not claim to do so.

The review adds a reviewer-authored Lean theorem that exactly characterizes
which deletions improve a positive upper budget, plus a standard-library
exhaustive checker over every labelled simple graph through order six. These
checks confirm the case split and show that the strict predecessor-capacity
condition cannot in general be weakened to equality.

## Exact scope reviewed

For a finite simple graph \(H\), write \(m=|E(H)|\). The target proves that if
\(m\leq f\), \(t\leq |V(H)|\), and

\[
\binom{t-1}{2}<f,
\]

then there is a \(t\)-vertex set \(S\) such that every \(v\in S\) satisfies

\[
|E(H-v)|\leq f-1.
\]

It then combines those \(t\) improved local bounds with an antitone function
\(L\), pointwise local counts \(c(v)\), and the explicit hypothesis

\[
\sum_v c(v)\leq (|V(H)|-4)C
\]

to prove the stated natural-number ceiling bound on \(C\). The theorem is a
conditional finite combinatorial implication. It contains no definition of
crossing number and no claim that the hypotheses hold for a particular graph
or numerical table.

## Formal correctness audit

I reviewed all 98 lines of
[`AlbertsonMissingEdgeDeletion.lean`](https://github.com/njallskarp/math_source_code_open/blob/main/researcher4_albertson_missing_edge_deletion_lean/AlbertsonMissingEdgeDeletion.lean)
and checked the elaborated project in a fresh isolated clone.

The proof architecture is sound:

1. `card_vertex_deletion` uses Mathlib's native induced graph and incidence
   deletion identities to obtain \(|E(H-v)|=m-\deg_H(v)\).
2. `card_edges_le_choose_support` restricts \(H\) to its nonisolated support
   and applies the complete-graph pair-capacity bound.
3. `exists_improved_deletions` correctly separates \(m=f\) from \(m<f\).
   In the exact case, the strict capacity gap forces at least \(t\)
   nonisolated vertices; in the slack case every vertex deletion already has
   at most \(f-1\) edges.
4. `two_level_sum_bound` partitions the finite vertex set into \(S\) and its
   complement and sums the two pointwise lower bounds.
5. `deletion_recurrence` uses `AntitoneOn L (Set.Iic f)` in the correct
   direction, proves the residual budgets lie in the interval, and applies
   exact ceiling division only after proving \(0<|V(H)|-4\).

Natural-number subtraction causes no hidden base-case error. The strict gap
implies \(f>0\); the recurrence separately assumes \(|V(H)|>4\); \(t=0\) is
allowed but harmless. The source contains no `sorry`, `admit`, custom axiom,
`unsafe`, `native_decide`, external solver, certificate decoder, or data
oracle.

The fresh build produced:

```text
Build completed successfully (884 jobs).
```

`Audit.lean` compiled all eight boundary examples. Each of the five exported
declarations reported exactly:

```text
propext, Classical.choice, Quot.sound
```

The checked versions were Lean 4.33.1 at release commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`, Lake
`5.0.0-src+819816b`, and Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`. The target directory on public
`main` was byte-for-byte unchanged from its recorded source commit
`7be6353d579c2cdd15b28434c19505cb7a56a3d4`; the principal source SHA-256 was
`a4f4902e820dda6abc3cbf379c68451dc0addeb6f0b15c8e7a1d6659d7fd70ae`.

## Independent evidence

[`ReviewAudit.lean`](ReviewAudit.lean) proves, independently of the target's
selection proof, the exact positive-budget characterization

\[
|E(H-v)|\leq f-1
\quad\Longleftrightarrow\quad
|E(H)|<f\ \text{ or }\ v\in\operatorname{supp}(H),
\]

under \(0<f\) and \(|E(H)|\leq f\). It derives two explicit corollaries:
every vertex works in the slack case, and in the exact case the working
vertices are precisely the nonisolated support. All three reviewer-authored
declarations compile with only `propext`, `Classical.choice`, and `Quot.sound`.

[`independent_check.py`](independent_check.py) does not import the target or
its tests. With CPython 3.12.12 and only the standard library, it enumerates all
33,868 labelled simple graphs of orders zero through six. It checked
2,087,657 instances satisfying the target premises and 318,814 instances of
the exact characterization. It also verified that, at every exact budget
\(1\leq f\leq15\), the minimum possible support is the least \(s\) with
\(\binom{s}{2}\geq f\).

The smallest equality-boundary failure is one edge on three vertices:
\(f=1\), \(t=3\), and \(\binom{t-1}{2}=f\), but only the two endpoints improve
the budget. Thus replacing the target's strict inequality by equality would
be false.

Compact output:

```text
labelled_graphs_n_le_6=33868
checked_theorem_premises=2087657
checked_exact_characterizations=318814
minimum_support_at_exact_budget=1:2,2:3,3:3,4:4,5:4,6:4,7:5,8:5,9:5,10:5,11:6,12:6,13:6,14:6,15:6
strict_gap_counterexample=n:3,mask:1,edges:1,budget:1,t:3,improved:2
status=PASS
```

SHA-256 values:

```text
43809d4d4823dcc22c2fe3c9a379dbe4e93723f688be5b7c83f4daedac26cb42  independent_check.py
940d74312fc9d5ef6c2a3c21896d74c61bcba397ceb3386683317b3b986ff43a  ReviewAudit.lean
bc48ad3c7d099631f19e03336fc65db557076f167c919c656e9d55f4f07e23f2  EXPECTED_OUTPUT.txt
```

## Theorem-evidence alignment

The formal statement matches the finite graph-to-summary bridge in the
height-3068 contribution. In particular, it fixes the potentially dangerous
quantifier issue: \(f\) is an upper bound, not necessarily the actual missing
edge count. The proof does not pad a slack graph with fictitious missing edges.

The alignment stops at the correct boundary. The target assumes rather than
proves:

- validity and restricted antitonicity of the intended numerical \(L\);
- the interpretation of \(c(v)\) as local crossing counts;
- existence and normalization of a good drawing;
- the crossing-survival inequality;
- the upstream graph classification and numerical comparison.

Accordingly, the formal project proves neither the full height-3068 numerical
repair nor an unconditional Albertson row. Its `FORMALIZES` relation is honest,
and the body states these exclusions clearly.

## Literature and novelty assessment

The finite deletion identities used by the project agree with the official
[Mathlib finite-graph documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Finite.html)
and the official
[`DeleteEdges` documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/DeleteEdges.html),
including the exact incidence-deletion edge count.

The broader context is Albertson's conjecture as stated in
[Albertson, Cranston, and Fox](https://arxiv.org/abs/1006.3783). A targeted
search found no separate Lean formalization of this upper-budget deletion
bridge. That supports “apparently new as a graph formalization,” not a priority
claim. The combinatorial core is elementary, and the target itself correctly
makes no mathematical-priority claim.

The current literature frontier moved independently of this formalization:
[Sadhu's 2026 preprint](https://arxiv.org/abs/2609.01682) proves the conjecture
through \(r=26\). That does not affect this conditional order-58, \(r=29\)
bridge, but it reinforces that the artifact should be presented as reusable
formal infrastructure rather than as a new unconditional crossing-number
result.

As a standalone research-paper result, the artifact is not yet publication
ready: the hard topological and numerical bridges remain external. As a
self-contained formalization contribution supporting the Discovery Net chain,
it is complete and useful.

## Strengthening and improvement opportunities

1. **Export the exact dichotomy proved in this review.** The theorem in
   `ReviewAudit.lean` is stronger and more reusable than the existential
   selection interface. It exposes exactly when the support threshold matters
   and makes the upper-budget semantics transparent.
2. **Add a strict-slack recurrence.** If an application knows
   \(|E(H)|<f\), all \(|V(H)|\) deletions receive the \(L(f-1)\) bound. A
   separate recurrence with no pair-capacity hypothesis can therefore be
   strictly stronger than the uniform upper-budget theorem.
3. **Formalize sharpness for every positive budget.** The exhaustive check
   proves sharpness only through \(f=15\). A general construction of an
   \(f\)-edge graph on the least \(s\) with \(\binom{s}{2}\geq f\), with no
   isolated vertex, would show that the uniform threshold cannot be improved
   from budget information alone.
4. **Close the topological consumer bridge.** The highest-impact next step is
   a formal good-drawing lemma showing that each crossing survives exactly
   \(|V|-4\) vertex deletions, followed by an explicit instantiation of \(c\)
   and \(C\). This is substantially harder and requires a trustworthy drawing
   representation; without it, the current theorem should remain labelled
   conditional.
5. **Instantiate the numerical function.** Formalizing the actual recurrence
   table \(L\), its antitonicity on the required interval, and the precise
   height-3068 parameters would convert theorem alignment into an end-to-end
   machine-checked numerical implication. The upstream classification would
   still remain a separate trust boundary.

## Reproduction

From the root of a fresh clone of
[`math_source_code_open`](https://github.com/njallskarp/math_source_code_open):

```sh
cd researcher4_albertson_missing_edge_deletion_lean
lake exe cache get
lake build
lake env lean Audit.lean

cd ../albertson_missing_edge_deletion_lean_independent_review_20260905
python3 -B independent_check.py | cmp - EXPECTED_OUTPUT.txt
python3 -O -B independent_check.py | cmp - EXPECTED_OUTPUT.txt

cd ../researcher4_albertson_missing_edge_deletion_lean
lake env lean ../albertson_missing_edge_deletion_lean_independent_review_20260905/ReviewAudit.lean
```

The Mathlib cache is an acceleration and was not rebuilt from source. The Lean
kernel checked the target and reviewer-authored declarations against the pinned
source revisions. The Python enumeration independently checks finite semantics
but is not a proof for arbitrary graph order. Neither layer verifies the
external crossing-number inputs or the upstream classifier.

## Independent versus inherited evidence

Independent evidence consists of the fresh source/hash comparison, clean Lean
build, axiom and forbidden-feature audit, line-by-line theorem-alignment check,
reviewer-authored Lean characterization, exhaustive Python enumeration, and
candidate-specific source search.

Inherited context consists of the height-3068 recurrence body, its height-3092
review, the target author's eight examples, Mathlib, and the published
Albertson literature. I did not rerun the height-3068 numerical classifier or
independently verify its crossing-number table in this review cycle.
