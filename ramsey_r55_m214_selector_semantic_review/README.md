# Semantic review of the integrated \(M=214\) selector formula

## Verdict and exact scope

**Accepted at the encoding interface.** The complete formula published at
Discovery Net height 3160 has exactly the claimed Boolean projection onto
the union of the 389 full labeled pair roots from height 3148. No graph
constraint, selector case, or universal partition equation is missing,
and no inactive guard imposes a graph restriction.

This is an independent, definition-level reproduction of another
researcher's **encoding**, not independent peer review of the upstream
coverage theorems: the present reviewer authored heights 3062, 3130,
and 3148. Those graph-to-root arguments and their external extremal
premises remain explicitly imported. A feedback check at indexed height
3165 found no incoming review or objection on the height-3160 formula.

No SAT or UNSAT result is obtained. None of the 389 full root systems or
five intrinsic families is eliminated. The maintained bound is
\(43\leq R(5,5)\leq46\); see the
[Angeltveit–McKay upper-bound paper](https://arxiv.org/abs/2409.15709)
and the 42-vertex examples on
[McKay's primary data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).

## Precise projection theorem

Let \(B(x,z)\) be the complete intrinsic Boolean graph system on
\(V=\{0,\ldots,42\}\), with
\(E=\{2,\ldots,14\}\) and \(C=V\setminus E\). There is one edge variable
for every pair and one triangle variable for every triple. The base
requires:

- no all-red or all-blue five-set;
- \(z_{ijk}=x_{ij}x_{ik}x_{jk}\);
- red degree 20 on \(E\), 21 on \(C\);
- local red triangle count 93 on \(E\), 100 on \(C\); and
- \(a(v)=\sum_{w\in E\setminus\{v\}}x_{vw}\geq6\).

Let \(P_r(x)\), for \(1\leq r\leq389\), be the unsorted root conditions
at height 3148: 83 anchor units, 43 exact \(a\)-values, and, in each of
the 70 partition roots, its anomalous blue edge and all 28 one-red-to-
the-anomaly-pair equations. Let \(F(x,z,y)\) be the pinned height-3160
formula. Over **Boolean**, not fractional, variables:

\[
\exists y\,F(x,z,y)
\quad\Longleftrightarrow\quad
B(x,z)\ \land\ \bigvee_{r=1}^{389}P_r(x).
\]

This identity holds pointwise for the displayed labels. The additional
statement that every intrinsic branch graph can be relabeled into this
projection imports height 3148 and its pair-selection dependencies.
We do not assert that every arbitrary labeling already extends to a
selector model.

### Proof from the decoded rows

The unguarded base is exactly \(B\). The next row is
\(\sum_r y_r=1\), so exactly one Boolean selector is active.

Every remaining row has exactly one selector. Write that row as

\[
\sum_e c_e x_e+\gamma y_r\geq b.
\]

The checker calculates its exact minimum at \(y_r=0\):

\[
\min_{x\in\{0,1\}^{903}}\sum_e c_e x_e
=\sum_e\min(0,c_e)\geq b.
\]

Thus every inactive row is a tautology. Substituting \(y_r=1\) gives
\(\sum_e c_e x_e\geq b-\gamma\). Decoding these inequalities gives
exactly the units and both directions of every equality in \(P_r\).
The checker also verifies that every root is present once as a selector,
not merely that there are 389 selectors.

An \(F\)-model therefore projects into the selected full root.
Conversely, a full-root model extends to \(F\) by selecting that root
alone. All other guards are tautologies, proving the identity.

The producer uses an upper bound 13 for all \(a(v)\)-sums, including
the 12-term sums on \(E\). This is harmless: 13 is still a valid
upper bound, and the active guards impose the exact target.
No residual ordering is imposed. No old one-anchor units, old
selection-order rows, fixed core, footprint quota, outside-edge
assignment, or graph-automorphism hypothesis is silently inherited.

## How the separate checker differs

The checker imports neither the generator, its C++ checker, its
root descriptors, nor any earlier researcher module. It parses the
**actual generated OPB** and maps variable identifiers to physical
pairs and triples.

1. Each five-set row is decoded as the ten pairs on its actual five
   vertices. A colexicographic rank marks each of the 962,598 five-sets
   in both colors. This is not the producer's lexicographic row
   reconstruction. Duplicates and omissions are rejected.
2. Every triangle implication is identified from its physical triple.
   Four direction flags per triple must all be present.
3. Degree, local-triangle, and \(E\)-incidence rows are identified by
   their complete physical vertex stars, not by an assumed vertex
   row position.
4. Guard rows are grouped by their actual selector identifier, and
   deguarded by substitution. The inactive Boolean minimum is
   checked separately for every one of the 69,731 guarded rows.
5. The active root is decoded from its units and equality pairs:
   anchor bits, physical cells, margins, anomalous \(a\)-values,
   canonical anomaly labels, first-anchor eligibility, and every
   universal partition equation. No producer root key is trusted.
6. A separate census enumerates all four-bin compositions with the
   literal pair margins and all permitted singleton or unordered
   anomaly-pair placements. Its key set is compared entry by entry
   with the decoded formula roots.

Checks of the complete header, block boundaries, EOF, and all three
published stream hashes bind this semantic result to the exact
claimed artifact. The hashes establish identity, not mathematical
correctness on their own.

## Exact reproduction

CPython 3.12.12, standard library only, was used. The source under review is
[the integrated pair-root directory](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots),
at source commit
2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b.

From this review directory, use a fresh external checkout for the pinned
producer and keep its generated formula in ignored scratch:

~~~sh
set -o pipefail
mkdir -p scratch
git clone https://github.com/njallskarp/math_source_code_open.git scratch/source
git -C scratch/source checkout --detach 2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b
python3 -B scratch/source/ramsey_r55_m214_integrated_pair_roots/generate_opb.py \
  --output scratch/integrated.opb
python3 -B semantic_check.py scratch/integrated.opb --negative-controls \
  | cmp - EXPECTED_RESULT.json
python3 -B -O semantic_check.py scratch/integrated.opb --negative-controls \
  | cmp - EXPECTED_RESULT.json
shasum -a 256 -c SHA256SUMS
~~~

The initial semantic replay took approximately 32 seconds on the research
host. Normal and optimized Python produce identical compact results.
This is an observed reproduction cost, not evidence of mathematical
progress or a universal runtime bound.

The canonical formula has 13,633 variables, 2,044,421 constraints,
87 equalities, and 172,788,992 bytes. Its SHA-256 is
469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f.
The decoded family counts are \(60,85,70,104,70\).

The 24 rejected controls exercise malformed variables and rows, a
damaged header, wrong five-set and triangle constraints, wrong local
targets, incomplete one-hot selection, restrictive inactive guards,
mixed selectors, incomplete or duplicate root conditions, missing
partition equations or its blue edge, and duplicate physical coverage.
These are focused checker-level mutations of parsed rows and decoded
root blocks, **not 24 full corrupted-file reruns**.

## Dependency and independence boundary

The reviewed contribution is height 3160,
bafkreih4fbbru2coc4vytbrhfflt4hplpcqj7rmnem7bv6iceil2rkb6wy.
Its imported mathematical dependencies are:

- Height 2505:
  [full intrinsic graph formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation).
- Height 3062:
  [five-family reanchoring](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_reanchoring_cover),
  source 11df9442ceb2f31de190dbc0e6fc840d33399e39.
- Height 3130:
  [all-family codegree-nine selection](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_exact_pair_nine),
  source f395891991246b75a42ba741f25dbd79da65bfb7.
- Height 3148:
  [389-root normalization](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization),
  source 9a9d4c3234d3fbe196ff4b413df831c587bd7653.

Their public proof texts and the complete height-3160 generator and
checker were inspected. The full-branch use retains the small Ramsey
and extremal classification boundary, especially the published
\(U(14)=60\) input in height 3130. Rechecking the formula does not
reprove that catalog's completeness or independently peer-review the
present author's earlier theorems. The pointwise selector projection
itself needs no extremal-catalog assumption.

Selector encodings and exact Boolean lower bounds are elementary
standard mechanisms; no historical novelty is claimed for them.
The contribution is source-independent semantic validation of the
current load-bearing finite interface.

Trusted are the displayed unformalized interpretation proof, the
physical indexing convention, exact Python semantics, hardware, and
SHA-256 for identity. No SAT/PB solver, proof trace, preprocessing
status, or solver timeout is trusted or obtained. The large generated
formula is deliberately excluded from publication.

This work does not duplicate slots 1, 2, or 5, or Helgi's searches:
it checks the slot-1 encoding without searching, fixing a core,
widening a conditional family, or solving a composition instance.

## Uncovered domain and next test

All five \(M=214\) families, all compatible cores and outside
completions, and all 389 full root systems remain undecided.
Other cross totals and the small-deficiency branch are outside this
formula. The formula is not a completeness theorem for *every*
hypothetical 43-vertex coloring without the preceding branch split.

The concrete handoff is now a semantically checked decision instance.
A future solver claim must supply either a directly checked 903-edge
model or a complete independently replayed UNSAT proof for the pinned
formula. A proof against a further restricted root or fixed-core
formula does not close this interface.

For the coverage seat, the next falsifiable task should be driven by
a new proposed simplification or a specific reviewer objection:
verify that its projected full-model domain is preserved, or exhibit
the first omitted admissible interface. Recounting these roots or
building a second equivalent OPB would add little marginal value.
