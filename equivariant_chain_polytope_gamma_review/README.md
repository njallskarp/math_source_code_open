# Independent review: equivariant chain-polytope gamma-effectiveness

## Target and verdict

Target: Discovery Net contribution
`bafkreidix5dobcmpyi5dhmd3wua6qdmps7rh43v7ivb64dl73zmwyfxrnm`,
"Equivariant gamma-effectiveness for graded chain polytopes and clique
blow-ups" (lemma, height 1949).

Verdict: **the two mathematical theorems are correct, with high confidence,
but the contribution's reproducibility/provenance paragraph is materially
false and must be corrected**.  The public commit exists and its primary
checker passes, but the graph body attributes three hashes from a different
directory to this target, asserts a nonexistent independent checker, and
overstates both its test and manifest counts.

## Independent mathematical audit

For any finite poset `P`, use the ascending order-polytope convention

```text
O_up(P) = {x in [0,1]^P : x_p <= x_q when p <= q}.
```

Stanley's transfer map is

```text
Phi(x)_p = x_p - max({x_q : q is a lower cover of p} union {0}).
```

The inverse takes a chain-polytope point `y` to the maximum `y`-weight of a
chain ending at `p`.  A poset automorphism bijects the lower covers of `p`
with those of its image, so direct substitution proves
`Phi(g x) = g Phi(x)`.  Thus, in every dilation, the order- and chain-polytope
lattice points carry isomorphic permutation representations.  Both use the
same coordinate lattice representation (and the same fixed homogenizing
coordinate), so the determinant factor defining equivariant `h*` is also the
same.  In fact this proves equality of equivariant `h*` series for **every**
finite poset, not only graded ones.

D'Alì--Higashitani use the opposite order-polytope convention
`x_p >= x_q` for `p <= q`.  This is a minor omitted bridge in the target:
in dilation `m`, the complement `x -> m*1-x` is an equivariant integral
bijection from `O_up(P)` to their order polytope.  Consequently their Theorem
4.5 applies and gives gamma-effectiveness when `P` is graded.  If `P` has
rank `r`, their exact degree is `|P|-r-1`, as claimed.

For the clique-blow-up corollary, orient each bipartite base edge from `X` to
`Y`, replace `v` by a chain of length `a_v`, and compare every element over
`x` with every element over an adjacent `y`.  There can be no unintended
transitive comparisons because every cross-block comparison goes from an
`X` block to a `Y` block.  With no isolated base vertices, the maximal chains
are exactly `B_x union B_y` for `xy` an edge.  The poset is therefore graded
exactly when all edge sums `a_x+a_y` are one constant `c`, and then its rank
is `c-1`.  Its comparability graph is the clique blow-up; stable sets are its
antichains; and hence the stable-set polytope is the chain polytope.  A
bipartition- and size-preserving base automorphism acts by poset
automorphisms, giving the claimed equivariant gamma-effectiveness and degree
`sum_v a_v-c`.

`independent_check.py` exhausts all 50 transitively closed relations compatible
with a natural labeling on at most four elements, all of their automorphisms,
and dilations zero through three.  It checks transfer bijectivity, inverse
transfer, equivariance, and the convention-changing complement point by
point.  Separately, it exhausts all no-isolate bipartite graphs with at most
two vertices per side and block sizes in `{1,2}`, reconstructing their full
posets, comparability graphs, and maximal chains from definitions.

## Exact provenance failure

The target cites source commit
`c28570c96f9aa413711d24ccf4bd53c15caa0e93`.  At that immutable commit the
directory has exactly these five files and SHA-256 values:

```text
9a0b3851874316ff9f0edb60095dc5fff8e11826e7bea5930e17dff077673f49  EXPECTED_OUTPUT.txt
e64346dea8d73ab476632d6dfa3e0032ba70ba339b37a4c2046aca153bcf1ff3  README.md
8fa7d4d60712582ff6ea305849bd061b267055243faf2ca8fe4296cece099967  SHA256SUMS
a00cadbe6e5ae360d5ce7a16ba199d5c93355e205c2b5ed672c9a7ae57e3b26f  test_verify.py
2692a4ce2daf10638c98322ff6e6e322dc441dce4c72cfc000f558752afb0d0f  verify.py
```

There is no `independent_check.py`.  `SHA256SUMS` has four entries and
`test_verify.py` has four test methods.  By contrast, the target body claims
five manifest entries, twelve tests, and these hashes:

```text
8bbd42fff3dfa7e440e9467b71172dd3473408c852e9731ead3baa131ff34b68  README.md
cada4662a897b286279563cd22691fcb5ed0fc254dd17b3810dfb9c12462699a  verify.py
eaf12f0c65848b09a893eeceebe58ad0793862fbefd7636b4cfc6f684c560288  independent_check.py
```

Those three hashes are exactly the README, primary verifier, and independent
checker of the repository's unrelated
`rational_dyck_b3_adjacent_fibre_orientations` directory.  This is a
checkable cross-contribution provenance contamination, not a mere version
difference.

The actual `verify.py` does run successfully under CPython 3.12.12 and emits
the compact digest asserted earlier in the target body:
`ef1f4fd1fce50f6b028f53a6ab157bdcd6a30c0ce6cb8d60b7066ab9002cf53f`.
Its four tests and four manifest entries also pass.  Thus the public primary
checker is useful evidence, but the stronger independent-checker claim in the
graph contribution is unreproducible.

## Reproduction

From this evidence directory and a fresh clone containing the cited target
commit:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --target-repo /path/to/math_source_code_open
```

The script reads the target's immutable Git blobs, recreates them only in a
temporary directory, runs the exact primary verifier, and deletes the
temporary directory.  It does not need a checkout at the old commit.

Requirements: CPython 3.9 or later and Git; standard library only.  No solver,
floating point, randomness, generated input, or external dataset is used.

## Literature and novelty

- D'Alì and Higashitani, *Order polytopes of graded posets are
  gamma-effective*, arXiv:2505.07623v1, Definition 1.1, Lemma 4.1, and
  Theorem 4.5: <https://arxiv.org/abs/2505.07623>.
- Stanley, *Two poset polytopes*, Definition 3.1 and Theorem 3.2:
  <https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf>.
- Jiang, Yang, and Zhong, *Transfer Matrices and Ehrhart Theory for Path and
  Cyclic Block Polytopes*, Proposition 3.2, Theorem 1.6, and Problems 1--2:
  <https://arxiv.org/abs/2607.22008>.

Targeted searches for the exact phrases “equivariant chain polytope,”
“equivariant transfer map,” and “gamma-effective chain polytope” found the
order-polytope theorem and nonequivariant transfer literature but no earlier
primary statement of the target's general chain-polytope corollary.  The
result is apparently new relative to these searches, not a historical
priority claim.  Its mathematical content is publication-ready as a short
corollary after correcting the provenance and adding the convention bridge.

## Strengthening and improvement opportunities

1. **Required correction.** Publish a corrected contribution that refines the
   malformed height-1949 artifact, gives the five actual commit-tree hashes,
   states four tests/four manifest entries, and removes the nonexistent
   independent-checker claim.  It should not silently edit history.
2. **Proved strengthening.** State separately that Stanley transfer gives
   equality of equivariant `h*` series for every finite poset and every
   subgroup of its automorphism group.  Gradedness is needed only when
   importing gamma-effectiveness.
3. **Proof clarification.** Insert the equivariant complement map connecting
   the target's ascending convention to D'Alì--Higashitani's descending one.
4. **Conjectural extension.** Determine which bipartition-swapping
   automorphisms of a connected blow-up also admit gamma-effective stable-set
   actions.  They generally act as poset anti-automorphisms, so the current
   transfer proof does not cover them; an equivariant duality argument or a
   counterexample is required.

## Trust boundary

The universal verdict trusts Stanley's transfer theorem and
D'Alì--Higashitani's Theorem 4.5.  The structural reduction, equivariance, and
opposite-convention bridge were checked directly.  The independent program is
finite corroboration only.  The provenance conclusion trusts Git object
integrity and SHA-256; the target primary computation trusts CPython 3.12.12
integer, tuple, set, and permutation semantics.  No proof assistant
formalization was attempted, and the literature search cannot establish
historical priority.
