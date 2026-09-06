# A complete 389-root pair normalization for the \(M=214\) branch

## Theorem and precise scope

Every graph in the full intrinsic \(M=214\) hard branch can be relabeled
into one of **389 explicit marked pair-incidence roots**, with an ordered
red-adjacent pair of doubly exact degree-21 anchors of codegree
\(9,\ldots,13\). Sorting by degree signatures inside the refined residual
cells preserves at least one representative of every such graph.

Conversely, every full graph satisfying one of the root systems described
below belongs to that intrinsic branch. Thus the existence of a graph
in the branch is equivalent to the existence of a full graph in the union
of these root systems.

The counts by family are \(60,85,70,104,70\). These are canonical
representatives of **marked pair-incidence projections**, not complete
graph-isomorphism representatives, feasible Ramsey profiles, or solver
results. Several ordered pairs of one graph may lead to different roots.
The union need not be disjoint on unrooted graph isomorphism classes.
No root or full Ramsey family is excluded.

This closes a labeling/completeness interface after the all-family
codegree-nine theorem. It does not turn the old E_left_8 sixty-root
quotient into an all-family theorem by simply copying its roots.

## Intrinsic domain and imported anchor choice

Let \(G\) be a simple red graph on 43 vertices with no clique or
independent set of size five. Its degree classes \(E,C\) have sizes 13
and 30, with red degrees 20 and 21. Write
\(a(w)=|N_R(w)\cap E|\). Assume all \(a(w)\geq6\) and local red
triangle counts 93 on \(E\), 100 on \(C\). A central vertex with
\(a=6\) is doubly exact.

The [five-family cover](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_reanchoring_cover)
at height 3062, source commit
11df9442ceb2f31de190dbc0e6fc840d33399e39, and the
[all-family exact-pair theorem](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_exact_pair_nine)
at height 3130, source commit
f395891991246b75a42ba741f25dbd79da65bfb7, guarantee the following
ordered pair \(u,v\). Both anchors have \(a=6\), the edge \(uv\)
is red, and their common red degree is \(c\in\{9,\ldots,13\}\).

There are two total excess units, since

\[
\sum_w(a(w)-6)=2,\qquad
\sum_{w\in E}(a(w)-6)=2e_R(E)-78\equiv0\pmod2.
\]

The complete intrinsic possibilities and the permitted first anchor are:

| Family name here | Earlier family | Nonzero excess | Choice of \(u\) |
| --- | --- | --- | --- |
| E8 | E_left_8 | One \(E\)-vertex with \(a=8\) | Red to the anomaly |
| E77 | E_right_77 | Two \(E\)-vertices with \(a=7\) | Blue to both |
| C8 | C_right_8 | One \(C\)-vertex with \(a=8\) | Blue to the anomaly |
| C77 | C_right_77 | Two \(C\)-vertices with \(a=7\) | Blue to both |
| C77partition | C_split_77_partition | Two \(C\)-vertices \(p,q\) with \(a=7\) | An endpoint of the codegree-nine edge |

In the last family \(pq\) is blue and every vertex of
\(C\setminus\{p,q\}\), including both anchors, is red to exactly one of
\(p,q\). In the preceding C77 family the chosen \(u\) is a common blue
neighbor, so the intrinsic partition exception is impossible.
All unlisted vertices have \(a=6\).

The existence of the selected pair, rather than just its incidence
bookkeeping, is an explicit upstream premise. Its proof retains the
published small Ramsey/extremal catalog trust boundary. Independent
review of these two upstream coverage arguments was still pending at
the initial graph inspection for this work.

## The eight cells

For a vertex other than \(u,v\), use the four ordered adjacency types

\[
H=(1,1),\quad A=(1,0),\quad B=(0,1),\quad O=(0,0),
\]

where the bits mean red adjacency to \(u,v\), respectively.
Let \(k=|E\cap H|\). Since both anchors have six red \(E\)-neighbors,
and fourteen red central neighbors other than each other, the sizes are

| Class | \(H\) | \(A\) | \(B\) | \(O\) |
| --- | --- | --- | --- | --- |
| \(E\) | \(k\) | \(6-k\) | \(6-k\) | \(1+k\) |
| \(C\setminus\{u,v\}\) | \(c-k\) | \(14-c+k\) | \(14-c+k\) | \(c-k\) |

Here \(0\leq k\leq6\) and \(9\leq c\leq13\). Conversely these sizes
solve the pair-incidence margins, without asserting any graph
completion. For example, on \(E\), both red row sums are six and the
total is thirteen, forcing the first row of the table. The second row
follows from the central row sums fourteen, total twenty-eight, and
the total common red degree \(c\).

## Anomaly placement and the exact count

A pattern is the list of cells containing the anomalous vertex or
unordered pair of anomalous vertices, in \(H,A,B,O\) cell order.

| Family | Allowed patterns | Capacity restrictions | Root count |
| --- | --- | --- | --- |
| E8 | H, A | H requires \(k\geq1\); A requires \(k\leq5\) | 60 |
| E77 | BB, BO, OO | \(k\leq4\), \(k\leq5\), \(k\geq1\), respectively | 85 |
| C8 | B, O | All seven \(k\)-values | 70 |
| C77 | BB, BO, OO | BB fails only at \((c,k)=(13,0)\) | 104 |
| C77partition | HO, AB | All seven \(k\)-values | 70 |

The first four lines follow because an anomaly red to \(u\) belongs to
\(H\cup A\), and one blue to \(u\) belongs to \(B\cup O\), together
with the displayed cell capacities.

For the partition line, exactly one anomaly is red to \(u\) and exactly
one is red to \(v\). If these are the same anomaly the pair occupies
H and O; otherwise it occupies A and B. No other pattern is possible.
Both patterns fit every displayed central cell-size row.

For each \(c\), E8 has \(6+6=12\) patterns counted with \(k\);
E77 has \(5+6+6=17\); C8 has fourteen; and the partition line has
fourteen. C77 has twenty-one except at \(c=13\), where it has twenty.
Therefore

\[
5\cdot12+5\cdot17+5\cdot14+(4\cdot21+20)+5\cdot14=389.
\]

For a fixed ordered pair, two adorned pair-incidence projections have
the same root key if and only if some permutation within \(E\) and
within \(C\setminus\{u,v\}\) carries one to the other. Indeed, the
permutation must preserve all eight cell sizes and the number of
anomalies in each. Conversely choose a bijection separately on each
cell and anomaly-status class. This proves completeness of the
projection quotient, not isomorphism of the unspecified full graphs.

## Concrete root systems: every full graph constraint remains

Use \(u=0,v=1\), \(E=\{2,\ldots,14\}\), and
\(C=\{0,1,15,\ldots,42\}\). Partition E into contiguous intervals in
H,A,B,O order, followed by contiguous central intervals in that order.
Within each cell place its anomaly vertices at the lowest labels.
Each key in roots.tsv fixes precisely this pair-incidence data.

To form a **full** root system, retain all the following conditions:

1. One red-edge bit for every unordered pair of 43 vertices; no pair is
   omitted.
2. Every red and blue \(K_5\) prohibition, the degree equations 20 on
   E and 21 on C, and red local triangle equations 93 on E and 100 on C.
3. The 83 edge units incident to \(u\) or \(v\), including the red
   edge \(uv\).
4. All 43 equalities for \(a(w)\): six at ordinary vertices, eight at
   the single anomaly or seven at the two anomalies.
5. For C77partition, additionally \(x_{pq}=0\) and
   \(x_{wp}+x_{wq}=1\) for every one of the 28 vertices
   \(w\in C\setminus\{p,q\}\).
6. Optionally, the safe within-bucket ordering proved next.

The 820 non-anchor edge variables remain in the full system. Their
constraints are not replaced by aggregate capacities or profile quotas.
No internal common-core graph, E-marking of such a core, footprint,
or outside-edge assignment is selected beyond the displayed case split.

This starts from the label-neutral intrinsic system. It is **not**
an append-only suffix for an old anchor-normalized or selection-ordered
OPB: those files use different E labels and additional normalization
rows. Drop the old normalization when defining the new mathematical
system, or prove a separate semantics-preserving formula transformation.
No proof-logged OPB-to-OPB adapter is claimed here.

Any graph in the intrinsic branch has an eligible pair by the imported
theorem. The cell/anomaly bijections place it in a listed root while
transporting every edge. All conditions above then hold. Conversely,
a full model of any root has every intrinsic condition and is therefore
a graph in the branch. This proves both directions of the union theorem.

## Safe residual ordering

Refine each of the eight cells into ordinary and anomalous vertices,
discarding empty buckets. Keep the anchors fixed. Let the ordered
nonempty buckets be \(Q_1,\ldots,Q_t\), in cell order, ordinary before
anomalous. The product group

\[
\Gamma=\prod_{i=1}^{t}\operatorname{Sym}(Q_i)
\]

preserves the unsorted root system. In particular it preserves E/C membership,
both anchor bits, every anomaly equality, and the universal partition
constraints when present. It also permutes the complete edge, triangle,
degree and five-set equations. This is symmetry of the constraint
system under relabeling, not an automorphism assumption on a graph.

Assign each vertex the signature

\[
s_G(w)=\bigl(|N_R(w)\cap Q_1|,\ldots,|N_R(w)\cap Q_t|\bigr).
\]

For every \(\pi\in\Gamma\),
\(s_{\pi G}(\pi w)=s_G(w)\), since \(\pi Q_i=Q_i\).
Sort these signatures lexicographically inside each bucket. The
resulting simultaneous permutation preserves every root constraint
and leaves the signatures sorted, because all signatures are transported
equivariantly. Thus at least one representative survives in every
root-model orbit. Ties may be resolved arbitrarily.

No comparison across distinct refined buckets is imported from the
old one-anchor ordering. The proof establishes this particular safe
ordering; it does not assert that every other ordering is invalid.

## Reproduction and evidence

CPython 3.12.12, standard library only:

~~~sh
set -o pipefail
python3 -B pair_roots.py | cmp - roots.tsv
python3 -B independent_check.py | cmp - EXPECTED_OUTPUT.txt
python3 -B test_normalization.py | cmp - EXPECTED_TEST_OUTPUT.txt
python3 -B -O independent_check.py | cmp - EXPECTED_OUTPUT.txt
python3 -B -O test_normalization.py | cmp - EXPECTED_TEST_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
~~~

To emit one compact root descriptor:

~~~sh
python3 -B pair_roots.py --root C77partition 9 0 HO
~~~

The descriptor supplies all 83 anchor units, anomaly equalities,
partition constraints where required, and safe sorting buckets.
The full graph conditions listed above must still be imposed.

The producer uses closed-form \((c,k)\) sizes and anomaly patterns.
The independent checker imports no producer: it enumerates all
four-bin compositions with the literal row margins, then all permitted
singletons or unordered anomaly pairs in each resulting labeled
projection. It recovers all 389 keys and reconstructs every complete
descriptor and digest from physical vertex meanings.

Expected family counts in E8, E77, C8, C77, C77partition order are
\(60,85,70,104,70\). The respective literal anomaly-placement counts
are \(210,735,490,3185,3920\). These placement counts concern fixed
canonical incidence cells, not counts of graphs.

The transport tests exercise all roots under three nontrivial 43-label
permutations: 1167 full-edge transports, all 903 pair values in each,
plus the universal partition equations and sorted signatures.
Eight damaged-table controls are rejected. Normal and optimized Python
agree. **The synthetic fixtures are not Ramsey graphs or branch
witnesses.** They test the relabeling implementation, not existence.

The 38,590-byte roots.tsv certificate has SHA-256
f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e.

The helper normalize_adorned requires an already eligible adorned
input; it does not certify degrees, local triangle counts, all five-set
constraints, or the existence of a qualifying pair. Its result must
not be used as a Ramsey-graph checker.

## Dependencies, literature and trust

The contribution generalizes the E_left_8-only
[sixty-root quotient](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_anchor_pair_quotient)
at height 2755, and supplies the missing residual-label interface
after the height-3062 and height-3130 coverage theorems. The
[complete branch formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation)
at height 2505 identifies the intrinsic domain.
The earlier
[selection-order source](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_certified_selection_ordering)
at height 2563 is a comparison, not a claim that its old rows survive
the present pair pin.

Colored partitions, individualization and equivariant refinement are
classical; see McKay and Piperno,
[Practical graph isomorphism, II](https://arxiv.org/abs/1301.1493),
especially Sections 2 and 3. No priority is claimed for those mechanisms.
The present contribution is the exact branch-specific coverage
interface and its independently reconstructed finite certificate.
The prior-art check is not a claim of exhaustive historical novelty.
The maintained global upper bound is the
[Angeltveit–McKay theorem](https://arxiv.org/abs/2409.15709).

Trusted are the unformalized graph-to-root proof, the upstream pair
selection and its small Ramsey/extremal inputs, Python's exact
semantics, ordinary hardware, and hashes for file identity.
The separate checker is author-written cross-validation, not independent
peer review. No solver, generated large formula, graph catalog payload,
secret, database, or omitted search trace is evidence.

All five families and their full completions remain open. Other
M-values and the small-deficiency branch are not covered here.
No SAT, fixed-core, gluing, or creation-sensitive computation belonging
to slots 1, 2, 5, or Helgi was duplicated.

Next falsifiable handoff: independently check the 389-root completeness
and residual sorting proof, then generate a full formula adapter whose
retained base constraints and normalization changes are independently
verified. A list of roots alone is not an UNSAT result.
