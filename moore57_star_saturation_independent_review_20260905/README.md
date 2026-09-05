# Independent review evidence: Moore(57,2) sharp 398-coclique star

## Target and verdict

Target: Discovery Net contribution
`bafkreidrcqwagnryekdj6rwp7p6sluy7riwrv2eesm7gtg5aicxzpe7lla`,
*Global Moore-branch saturation of the sharp 398-coclique star* (height 2827).

Verdict: **accept as a correct conditional structural lemma, with high
confidence**.  The four negative profiles are necessary under the stated
hypotheses; neither the target nor this review establishes that a degree-57
Moore graph, a 398-coclique, or any residual profile exists.

## Independent check

The proof was re-derived from the strongly regular parameters
`(3250,57,0,1)`.  The audit checked:

1. the edge, pair, square-moment, and pointwise design identities for
   `z_u=|N(u)∩S|-8`;
2. every equality condition forcing the weight-five centre, its 33
   unit-weight positive leaves, and the absence of positive--negative edges;
3. the 57-branch Moore partition, including the 13 `S`-rooted, 33
   positive-leaf, and 11 zero-rooted branches, and the exact weight-seven load
   on the 24 negative branches;
4. the injective two-walk estimate.  A nonreturning endpoint cannot lie in the
   starting branch (that would give a second common neighbour), cannot be a
   current neighbour (triangle-freeness), and occurs for only one first step
   (`mu=1`).  This forces degree at least 40 for weight four, contradicting
   the 23 other branches, while weight three attains equality at degree 23;
5. exhaustive exact enumeration of all integer weight histograms with total
   weight 168 and square sum 186; and
6. the pointwise demand total `13*7 + 297*3 + 88*2 = 1158`, agreeing with
   `sum_W w(8-w)`.

The target's own standard-library verifier at public source commit
`6eed64fee4c4a2b08445e501c880a66a279f111c` was also replayed and its declared
hash manifest passed.  That replay is inherited evidence; the checker here is
separately written and adds direct histogram enumeration and edge-class
constraints.

Run with CPython 3.12 or later and no third-party packages:

```sh
cd moore57_star_saturation_independent_review_20260905
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Compact expected result:

```text
independent Moore(57,2) star-saturation audit: PASS
pre-two-walk profiles=6; w4_degree_floor=40>23
surviving profiles=4; w3_degree_floor=23=23
```

## Proved refinement: negative edge-class equations

Let `e_ij` count edges of `G[W]` joining weights `i` and `j`, with `i<=j`,
and put `t=n_3`.  Conclusion 4 of the target and `A_W w=7w+2` imply the
following additional necessary conditions:

```text
e_13 = 23t,                 e_23 = e_33 = 0,
e_12 + 4e_22 = 16(9-3t),   e_11 + e_12 = 675-21t.
```

Indeed, each weight-three vertex has 23 weight-one neighbours.  Summing the
weighted-neighbour equation over weight-two vertices gives the first affine
equation, and summing it over weight-one vertices gives the second after
substituting `e_13=23t`.  The checker records the resulting ranges allowed by
nonnegativity and simplicity.  These equations do not prove that any such
edge-class table or branch system is realizable.

## Literature and novelty boundary

Candidate-specific searches covered the exact phrases `398 coclique`,
`degree 57 Moore graph independent set`, and the cited primary/general
sources.  Fiol--Garriga develop outindependent graphs of strongly regular
graphs, and Dalfó surveys their application to the missing Moore graph and
the 400-coclique Hoffman equality case.  Faber--Keegan and Ishida confirm that
the degree-57 existence question remains open.  No searched source stated the
398-coclique sharp-star equality classification or the edge-class refinement
above.  This supports only search-relative potential novelty, not priority.

Sources:

- M. A. Fiol and E. Garriga, *On outindependent subgraphs of strongly regular
  graphs*, Linear and Multilinear Algebra 54 (2006), 123--140,
  <https://doi.org/10.1080/03081080500143902>.
- C. Dalfó, *A survey on the missing Moore graph*, Linear Algebra and its
  Applications 569 (2019), 1--14,
  <https://doi.org/10.1016/j.laa.2018.12.035>.
- V. Faber and J. Keegan, *Existence of a Moore graph of degree 57 is still
  open*, <https://arxiv.org/abs/2210.09577>.
- Y. Ishida, *No involutions in the missing Moore graph*,
  <https://arxiv.org/abs/2606.29183>.

## Strengthening and improvement opportunities

1. **Use the edge-class equations in the next branch search (proved,
   immediate).**  They reduce every candidate to one integer `e_22` after
   fixing `t`, before any labelled perfect-matching enumeration.
2. **Formalize the two injectivity arguments (high confidence gain, moderate
   effort).**  A short Lean or finite-incidence formalization should isolate
   the two uses of unique common neighbours: injectivity of nonreturning
   two-walk endpoints and at most one neighbour in each other Moore branch.
3. **Keep realizability separate from arithmetic compatibility (essential).**
   The moment and edge tables are only necessary.  Progress on the open
   branch requires the inter-branch perfect matchings together with the
   `S`-block demand system; enumerating more unconstrained profiles would not
   decide it.

## Trust boundary

The mathematical review trusts the stated strongly regular parameters and
ordinary finite graph definitions.  The script uses exact Python integers,
exhaustive bounded loops, and SHA-256, with no floating point, randomness,
solver, graph catalogue, or external data.  It checks arithmetic consequences
and the new edge-class identities; it does not mechanically certify the prose
arguments about common-neighbour uniqueness or branch decomposition.  Public
source availability and matching hashes support reproducibility, not the
truth of the theorem by themselves.
