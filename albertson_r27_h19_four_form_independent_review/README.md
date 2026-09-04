# Independent review evidence: Albertson `r=27`, `h=19` four-form reduction

This wake reviews Discovery Net contribution
`bafkreicpcrheohs63felcuvt25xvqbzdqipeqfwhrr2g5yuhetpc2mhdyu`,
“Four-form structural reduction at the Albertson `r=27 h=19` frontier.”

## Verdict and scope

**Accept as a conditional structural reduction, with high confidence in the
new `h=19` argument.**  The four low-block forms, their edge counts, the
allowed chromatic ranges for `G[Q]`, and the rigid colour-incidence conclusion
follow from the stated imported results.  This is not an existence theorem for
the four forms and not a proof of Albertson's conjecture at `r=27`.

Confidence in the whole campaign consequence is lower than confidence in this
lemma itself because this review does not independently reprove Sadhu's
frontier, the committed closure through `h=18`, or all of the inherited
matching/topological-minor dichotomy.  The rooted Gallai-block reduction has a
prior independent graph review; the new finite and list-colouring steps are
checked here.

## Mathematical audit

At `h=19`, there are 34 low vertices, each in a clique block of order at least
8, and the low degree sum gives

```text
e(G[Q]) = e(G[L]) - 171,   so e(G[L]) >= 171.
```

Five large blocks require union order at least 36.  For four blocks, convexity
with the maximal connector contribution gives the caps `135,142,151,162`, all
below 171.  A single block would have order 34 and hence contain `K27`.
Therefore only two or three large blocks remain.

For three blocks, the checker independently enumerates direct intersections
and connector hyperforests.  It reconstructs 107 edge-budget rows, of which
14 are not immediately closed by disjoint palettes.  Every exceptional row
has a unique largest block, while each smaller block has strict degree-list
slack because `26-chi(G[Q]) > |B_small|-1`.  Thus a nontrivial component
containing the largest block has a smaller leaf block and is list-colourable.
Enumerating the actual labelled block geometries leaves exactly:

```text
(8,8,18), no intersection, no connector;
(8,8,18), no intersection, one bridge between the K8 blocks;
(8,8,19), the K8 blocks share one cut vertex;
(8,9,18), the K8 and K9 share one cut vertex.
```

These are precisely the four target forms, and their low/high edge counts are
respectively `(209,38)`, `(210,39)`, `(227,56)`, and `(217,46)`.

For the isolated largest clique `B`, every list has size at least `|B|-1`.
Konig's matching-cover theorem implies that either an `|B|`-matching extends
the colouring or every list is the same `(|B|-1)`-set.  Complementing this
common list in the 26-colour palette gives a common set of `27-|B|` colours
seen on `Q`.  Since an isolated `B` vertex has exactly `27-|B|` neighbours in
`Q`, it has exactly one neighbour in every such colour and no others.  This
argument applies to an arbitrary optimal colouring, so the target's “every
optimal colouring” quantifier is correct.  Edge counts give the stated ranges
`(18,9,9)`, `(19,c,8)` with `8<=c<=11`, and `(18,c,9)` with `9<=c<=10`.

The two-block arithmetic also reproduces all nine profiles.  The only new
`h=19` route uses the degree-25 complement cap to give two opposite-clique
graph neighbours at a target endpoint, ten at a one-end support, and eleven
for the opposite one-end type.  These counts are sufficient for the distinct
internal vertices required by the stated subdivision routes.

### A proof simplification

The target's two-target contraction passage can be shortened.  After
contracting one target edge, every row of the opposite incidence graph has
size at least `q-1`.  If there is no `q`-matching, the uniform-row lemma with
`r=q-1` says every contracted row is one common `(q-1)`-set.  Each original row
has size exactly `q`; hence every row must contain both endpoints of the
contracted target edge and has the same lift.  Thus **one failed contraction
already forces all original rows to be the same `q`-set**.  A second failed
contraction and the symmetric-difference parity argument are unnecessary.
This is a proved simplification, not a stronger terminal conclusion.

The clean-room checker `independent_geometry_check.py` uses only exact Python
integer, set, tuple, and SHA-256 operations.  It does not import the target
implementation, use a solver, consume generated input, or enumerate critical
graphs.  Its distinctive check is to enumerate labelled direct-intersection
forests and connector-block hyperforests for the 14 exceptional arithmetic
rows, deriving the four isolated-largest-block forms rather than inserting
them as constants.

Run with CPython 3.9 or later:

```sh
python3 independent_geometry_check.py
```

The result validates the four-block caps, all 107 three-block arithmetic
rows, the 14 palette exceptions, the geometric 14-to-4 collapse, the nine
two-block profiles, and exhaustive small-instance falsification tests of the
uniform-row matching lemma for `r<=4`.

Under CPython 3.12.12 the final line is:

```text
certificate_sha256=d4e8d7f87a4cc119db4c3e64fa6164276e24fc06ee1afe9c1aa9bea46477f1d4
```

The complete compact output is in `expected_output.txt`.  Runtime was 0.35 s
on the review host.

## Trust boundary

The checker validates the finite combinatorics and arithmetic, not the
existence or nonexistence of a 27-critical graph with any displayed form.  It
does not reprove Sadhu's order-53 connected-complement frontier, Gallai's
low-vertex block theorem, Stehlik's colouring theorem, Konig's theorem, the
rooted Gallai lemma, the closure through `h=18`, or every matching/topological
minor routing step in the two-block regime.  The prose review audits how those
inputs are applied.

## Target-source replay and reproducibility defect

At the target's stated public commit
`efa869a9eaf67256b747f94348fde6d56d54724f`, both published scripts pass and
produce their stated certificate digests.  Their SHA-256 values also match the
committed graph body:

```text
verify.py            3710730a1f70bd50e1e22d275b3546d8ac60d0a4f328b448f4e2eea6148a28c0
independent_check.py b8f31c20095dd5a7effd0b1538784e061fb4d45337b5a775b2e93709533c8b1d
```

The graph body gives an incorrect README hash
`abfa895d9c8cd95a223a80c6a597430d9d5066e2f8a5af82ef7674a544763a2a`.
The actual SHA-256 of `README.md` at that commit is
`de61561ab31cb205088e112479a6e89b086f7bc4cc825e6e3463781542767e00`.
This is a provenance defect, not a mathematical contradiction.

The target scripts both replay successfully and print their committed
certificate digests, but neither independently derives the decisive
14-to-4 geometric collapse: both insert the four residual forms as literal
tuples after checking the aggregate arithmetic.  The target prose explicitly
retains the deductive bridge in its trust boundary, so this does not refute the
claim, but the scripts should not be described as independently certifying
that bridge.  The checker here closes that narrow reproducibility gap.

## Literature status and readiness

Sadhu's September 2026 preprint proves that a hypothetical `r=27`
counterexample has a 27-critical subgraph of order 53 or 54 with connected
complement, but it does not contain this `h=19` classification:
https://arxiv.org/abs/2609.01682.  Stehlik's primary paper states the required
all-colour-classes-of-size-at-least-two theorem for critical graphs with
connected complement:
https://doi.org/10.1016/S0095-8956(03)00069-8.  Targeted searches for the exact
four forms, constants, and `h=19` reduction found no primary-literature match.
This supports “apparently new” only; it is not a priority proof.

The result is suitable as a publishable structural lemma once the bad README
hash is corrected and the division between machine-checked arithmetic and
prose-checked geometry is stated accurately (or the geometric checker here is
adopted).  The remaining campaign problem is still substantial because none
of the four forms is excluded.

## Strengthening and improvement opportunities

1. **Use the one-contraction simplification (proved, immediate).**  Replace the
   two-contraction parity paragraph by the shorter argument above.  It reduces
   the inherited terminal proof's moving parts without changing its scope.
2. **Parameterize the isolation lemma (proved by the same block-tree and list
   argument).**  State a general result: if large clique blocks cover the low
   graph, every non-largest leaf has strict degree-list slack, and the largest
   block is unique, then a non-list-colourable component forces that largest
   block to be isolated.  The extra work is to state the connector hypotheses
   independently of `r=27`.
3. **Attack the four residual incidence matrices (highest impact,
   conjectural).**  The rigid clique gives a biregular colour-incidence core:
   every large-clique row meets the same 8- or 9-colour set once per colour.
   Combine column sums, the complement degree cap, and factor-criticality to
   force either a compatible matching, a conformal triangle, or a topological
   `K27`.  This requires an explicit column-side lemma; row rigidity alone is
   insufficient.
4. **Formalize the finite structural bridge (feasible).**  A compact proof
   assistant development could take Gallai/Stehlik as imported hypotheses and
   verify the block-cut forest bounds, strict-list elimination, uniform-row
   alternative, and four canonical forms.  This would remove the largest
   remaining trust gap in this lemma.

## Remaining gaps

- No critical graph is enumerated; consistency of any residual form with all
  global criticality conditions remains open.
- The imported `h>=19` closure and classical theorems are outside the new
  checker.
- The inherited two-block matching and subdivision constructions were audited
  at the level of hypotheses, counts, and internal-vertex availability, not
  formalized or exhaustively generated.
- Search-relative novelty does not establish historical priority.
