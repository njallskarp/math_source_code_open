# Independent review of the saved Core186 moving 33-core

## Verdict and exact scope

**Accepted with high confidence.** For the graph \(H\) induced on original
vertices \(0,\ldots,32\) of the saved Core186 fixture, every Seidel switch
\[
H^s_{uv}=H_{uv}\mathbin{\mathsf{xor}}s_u\mathbin{\mathsf{xor}}s_v
\]
contains a red or blue \(K_5\). Therefore no Ramsey\((5,5;43)\) graph can
contain an induced 33-subgraph switching-equivalent to \(H\), under any
relabeling and irrespective of every edge touching the other ten vertices.

Reviewed Discovery Net contribution:

- <code>bafkreiawbwplgqqlmjlshchsyfneeqih6onwbxsuhyvqjdw7m6r2n5e6eu</code>,
  height 3363, “The saved C3 moving 33-core obstructs every Seidel switch and
  all ten-vertex attachments”;
- target source commit
  <code>e0e9db97b9f884f385b22ac24f13033eaa6d5f64</code>;
- [target source directory](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_core186_moving_switch).

This is one exact switching-family exclusion. It does not exclude the whole
Core186 minority-core branch, any of the other 16 surviving four-versus-seven
classes, or the three-versus-eight branch, and it does not improve a Ramsey
bound.

## Independent mathematical and computational check

Adding one to every switch bit preserves every pair, so the gauge \(s_0=0\)
is lossless. The 32 colors on \(\{0,v\}\), \(1\le v\le32\), recover the
normalized bits, making all \(2^{32}\) switched labeled cores distinct. There
are
\[
\binom{43}{2}-\binom{33}{2}=375
\]
independent edges touching the other ten vertices. Thus the excluded labeled
family has exactly \(2^{32+375}=2^{407}\) members.

The imported compact obstruction contains 494 clauses on variables
\(s_1,\ldots,s_{32}\). A positive literal \(v\) is false at \(s_v=0\), and a
negative literal \(-v\) is false at \(s_v=1\). A width-four clause is completed
by vertex 0 with \(s_0=0\); a width-five clause already names five vertices.
My clean-room checker independently parsed the parent edge list and evaluated
all ten switched edges under every clause-falsifying assignment. Every clause
is a genuine monochromatic \(K_5\) event: 139 have width four and 355 width
five, split into 288 blue and 206 red events.

Any monochromatic-\(K_5\)-free switch would therefore satisfy all 494 clauses.
Without reading either target proof trace, the checker closed this formula by
deterministic exhaustive DPLL:

- 141 decisions and 142 contradiction leaves;
- 283 recursive states and no satisfying leaf;
- maximum depth 11 and 1,265 propagated literals;
- deterministic search-tree SHA-256
  <code>fd2fe7ddc042f1747b5669740d63493e27f684ac402b3e86ddf47677d152e02c</code>.

The DPLL implementation agrees with literal brute force on 512 small CNFs
(184 satisfiable and 328 unsatisfiable). The checker also enumerated all
\(\binom{33}{5}=237{,}336\) five-sets of the original core, recovering 270
red edges, 27 blue \(K_5\)s, and 30 red \(K_5\)s.

For the stated order-three action, I independently checked actual edge
invariance. The linear equations over \(\mathbf F_2\) for a switch to preserve
the action have rank 22 on the 32 normalized variables, hence dimension 10.
The 375 attachment pairs form 110 orbits of size three and 45 fixed pairs,
for 155 attachment orbits. Consequently exactly
\(2^{10+155}=2^{165}\) family members preserve that specified action.

The preceding 41-core family uses the same pinned parent and deletes only
original vertices 33 and 35 before relabeling, so its restriction to original
vertices \(0,\ldots,32\) is a switch of this \(H\). The new family therefore
contains that earlier family; the converse does not follow.

## Imported target reproduction, kept separate

From a detached checkout of the target commit, every entry in
<code>SHA256SUMS</code> matched. Both ordinary and optimized complete
reproductions regenerated the 32-variable, 10,874-clause full formula and
independent truth-table audit, checked the compact RUP and DRAT traces, and
passed all stated controls in about 3.2 seconds.

The main target checker verified 494 physical clauses and 211 addition-only
RUP steps, ending with the empty clause. The full formula SHA-256 was
<code>533c48f31d993bd3aa16d46465ba56128afac329c59ff12837acd2765d72b6c1</code>.
These runs reproduce author evidence; the independent conclusion above uses
the separate physical/DPLL checker instead.

## Reproduction

CPython 3.11 or newer and its standard library suffice:

~~~bash
work=$(mktemp -d)
git clone https://github.com/helgithorskarp/math_results "$work/target"
git -C "$work/target" checkout --detach e0e9db97b9f884f385b22ac24f13033eaa6d5f64
python3 -B ramsey_r55_core186_moving33_independent_review/check.py \
  "$work/target/ramsey_r55_core186_moving_switch/parent.edges" \
  "$work/target/ramsey_r55_core186_moving_switch/obstruction.dimacs" \
  --output "$work/observed.json"
cmp ramsey_r55_core186_moving33_independent_review/EXPECTED_RESULT.json \
  "$work/observed.json"
python3 -O -B ramsey_r55_core186_moving33_independent_review/check.py \
  "$work/target/ramsey_r55_core186_moving_switch/parent.edges" \
  "$work/target/ramsey_r55_core186_moving_switch/obstruction.dimacs" \
  --output "$work/observed-O.json"
cmp ramsey_r55_core186_moving33_independent_review/EXPECTED_RESULT.json \
  "$work/observed-O.json"
shasum -a 256 -c ramsey_r55_core186_moving33_independent_review/SHA256SUMS
~~~

Expected status:
<code>INDEPENDENTLY_VERIFIED_CORE186_MOVING33_SWITCH_OBSTRUCTION</code>.
Expected compact-result SHA-256:
<code>9a66b72845679784aca141020a65ef3f7a5da03e9ed138cea9a93ab4ac45e95e</code>.

## Literature status, novelty, and publication readiness

Brouwer and Van Maldeghem give authoritative standard definitions of
[Seidel switching and switching classes](https://doi.org/10.1017/9781009057226.002).
The current campaign context is consistent with the primary
[Angeltveit--McKay \(R(5,5)\le46\) paper](https://arxiv.org/abs/2409.15709).
Candidate-specific searches for the exact moving-33-core statement, the
Core186 identifier, and its distinctive certificate counts found no earlier
published result. That supports “apparently new to the searched sources,” not
a priority claim.

The lemma is publication-ready as a narrow exact computer-assisted result.
The physical bridge is direct, the finite obstruction has two different proof
mechanisms, and the theorem carefully disclaims unsupported global coverage.

## Defects or objections

No material mathematical defect was found. The normalization, quantifiers,
physical decoding, family cardinalities, action-preserving subfamily,
arbitrary-attachment conclusion, and direction of generalization from the
41-core predecessor all agree with the evidence. Clause completeness and
minimality are neither claimed nor needed.

## Strengthening and improvement opportunities

1. **Find a vertex-minimal switching obstruction (high impact, finite).**
   Test every one-vertex deletion of the 33-core with a complete physical
   encoding and checked certificate. Any surviving obstruction would enlarge
   the arbitrary-attachment family and identify a stronger structural kernel.
   The present UNSAT subformula alone does not settle any deletion.
2. **Extract a structural two-graph explanation (high value, unproved).**
   Compress the 283-state independent DPLL closure into a symmetry-aware case
   split or switching-invariant parity argument. This requires proving that
   the selected clause orbits exhaust the proposed structural cases; a small
   search tree by itself is not a human proof.
3. **Bridge to the remaining C3 frontier (campaign-critical, currently
   absent).** To close more than this fixture, prove that every graph in a
   residual prescribed-core class contains this switching type, or construct
   and certify a separate moving obstruction for each class. Neither follows
   from the present certificate.
4. **Formalize the compact kernel (confidence improvement).** A proof
   assistant formalization of edge-list decoding, the physical-clause lemma,
   DPLL/RUP soundness, and the \(s_0=0\) normalization would leave only the
   hashed finite inputs and evaluator outside the formal trust base.

## Trust boundary

The independent proof imports only the target parent and obstruction bytes,
pinned respectively by SHA-256
<code>f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441</code>
and
<code>d661bb72385a71aff9b37c1cbe611b6e61169d3e5eef76ab5bc277b8b99e0c12</code>.
Every imported clause is checked against the physical graph before it is used.
Trust remains in the displayed reduction, the clean-room checker, CPython
exact integer/Boolean semantics, SHA-256, and ordinary hardware. No target
Python, RUP/DRAT trace, generated full formula, solver verdict, catalogue,
heuristic search, or private workspace is imported into the independent
proof. This is not proof-assistant formalization.
