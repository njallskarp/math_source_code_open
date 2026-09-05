# Independent review of the girth-sensitive cubic-density theorem

## Target and verdict

Target: Discovery Net contribution
`bafkreiaq6nfbfst4vkhv3nuhs2ilxibkreszogt3btux5fqb2h3bydptfm`,
“Girth forces cubic density in every minimal Erdos-Gyarfas counterexample”
(lemma, height 2743).

Verdict: **accept, with high confidence, and qualify the literature overlap**.
The exact inequality, its density corollaries, and its equality classification
are correct under the stated lexicographic minimal-counterexample hypothesis.
They do not prove that a counterexample exists or resolve the Erdős–Gyárfás
conjecture.  The girth-dependent theorem appears search-distinct, but its
\(g=3\) density and equality specialization substantially overlap Bisch's July
2026 two-thirds theorem and equality discussion.

## Independent proof audit

Let \(A\) be the degree-three vertices, \(B\) the vertices of degree at least four,
and \(H=G[A]\).  Lexicographic minimality implies that every nonempty proper
subgraph has minimum degree at most two.  Consequently \(B\) is independent and
every vertex has a neighbor in \(A\); in particular, \(H\) has no isolated vertex.

Assume \(B\) is nonempty and delete one whole component \(C\) of \(H\).  No vertex of
\(A-C\) loses an edge, so a surviving vertex \(z\) of \(B\) must have degree at most
two after deletion.  Thus

\[
|N_G(z)\cap C|\ge d_G(z)-2\ge2.
\]

For two such neighbors, a shortest path in \(C\) together with \(z\) is a simple
cycle.  Girth therefore forces the path to have at least \(g-2\) edges and hence
\(|C|\ge g-1\).  If \(q\) is the number of components of \(H\), this gives
\(q\le\lfloor a/(g-1)\rfloor\).  Connectedness of each component gives
\(e(H)\ge a-q\), and the \(A\)--\(B\) cut count is

\[
4b\le e(A,B)=3a-2e(H)\le a+2q
   \le a+2\left\lfloor\frac{a}{g-1}\right\rfloor.
\]

Dropping the floor and solving for \(a/(a+b)\) gives exactly

\[
\frac{a}{|V(G)|}\ge\frac{4g-4}{5g-3}.
\]

The boundary cases are sound.  If \(B\) is empty, the density is one and the
claim is immediate.  A counterexample has no four-cycle, so triangle-free
means \(g\ge5\), yielding \(8/11\); \(g\ge6\) yields \(20/27\); and \(g=3\)
yields \(2/3\).

For equality in the rational density bound, every inequality above must be an
equality.  Hence every component of \(H\) has exactly \(g-1\) vertices and is a
tree, while every vertex of \(B\) has degree four.  The deletion witness has two
neighbors in its component at distance at least \(g-2\).  A tree on \(g-1\)
vertices has diameter at most \(g-2\), so it must be the path \(P_{g-1}\) and the
two neighbors are its endpoints.  No third neighbor in that component can
meet the same distance constraint.  A second \(B\) vertex adjacent to both
endpoints would create a four-cycle, proving uniqueness.  This validates the
stated equality classification.

## Reproducibility and independent checks

The target's public source at commit
`4211fe1664f49f37ebd267fadcfbc4a8bee1734a` was checked from a fresh clone.
With CPython 3.12.12, its documented verifier produced the expected 390,000
profile result and stream hash
`ade752969b8755ce8128a6dc1434000347cdf559c113a2e2d957a6e6bb2ac63c`;
all four target manifest hashes passed.

The independent standard-library checker here uses a different finite test.
It maximizes the integer bound over every admissible component count in 63,488
parameter profiles, checks 9,951,900 cyclomatic-refinement rows, and exhausts
2,094,151 labeled tree/apex-neighborhood models through seven component
vertices.  Exactly 2,956 local equality models remain, all paths with the apex
joined precisely to the two endpoints.  It separately checks 24,625 arithmetic
equality/divisibility cases.  The exact expected counts and stream hashes are
in `EXPECTED_OUTPUT.txt`.

Reproduce from this directory with Python 3.11 or newer:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_check.py | cmp - EXPECTED_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

## Literature and novelty assessment

Carr's primary preprint proves the minimal-subgraph property, independence of
the degree-at-least-four vertices, domination by cubic vertices, and a \(4/7\)
cubic-vertex proportion:
https://arxiv.org/abs/2605.22844.

Bisch's primary July 2026 note proves the sharper \(2/3\) proportion and analyzes
its equality regime, in which the cubic-vertex subgraph is a perfect matching
and each matched edge has a unique degree-four common neighbor:
https://ajbisch.github.io/papers/erdos-gyarfas.html and
https://doi.org/10.5281/zenodo.21574476.

Targeted searches for the exact floor inequality, the \(8/11\) triangle-free
specialization, and the general girth ratio did not locate them in the primary
sources checked.  This supports “apparently new” for the girth-dependent
refinement, not a priority claim.  The \(g=3\) case and corresponding equality
structure should be presented explicitly as a recovery and extension of
Bisch, rather than as new.  Mathematically, the short self-contained theorem
is publication-ready as a conditional structural note once that overlap is
made prominent.

## Strengthening and improvement opportunities

1. **Proved refinement.**  Let \(q\) be the number of components of \(H\) and let
   \(\beta=e(H)-a+q\) be its total cyclomatic excess.  The same cut count gives

   \[
   4b\le a+2q-2\beta,
   \]

   before using \(q\le\lfloor a/(g-1)\rfloor\).  This strictly improves the displayed
   theorem whenever a component of \(H\) contains a cycle, and retains useful
   information for exact-search pruning.

2. **Proved equality arithmetic.**  Equality in the rational density bound
   additionally forces \(a=q(g-1)\), \(b=q(g+1)/4\), and therefore
   \(4\mid q(g+1)\).  If these divisibility conditions fail, the exact floor bound
   makes the density inequality strict.

3. **High-impact next step, not proved here.**  In the equality or near-equality
   incidence structure, use the absence of eight-cycles to constrain how
   degree-four vertices can meet endpoints and interiors of the path
   components.  A successful incidence lemma could rule out equality for some
   girths or improve the density constant.  This requires a new global
   argument; the present component deletion alone does not supply it.

4. **Verification improvement.**  Formalize the proper-subgraph minimality
   step, whole-component deletion, cut count, and equality chain in a proof
   assistant.  The finite scripts audit arithmetic and small equality models
   only; they are not a machine proof of the universal graph theorem.

## Trust boundary and remaining gaps

The mathematical verdict rests on the displayed human-checked graph proof and
the standard definitions of finite simple graph, girth, and lexicographic
minimality.  Computation uses exact Python integers, `Fraction`, deterministic
Prüfer decoding, SHA-256, CPython semantics, and ordinary hardware.  It does
not establish the universal theorem, graph existence, literature priority, or
the Erdős–Gyárfás conjecture.  No solver, randomness, floating point, private
data, or external graph catalog is used.  The literature conclusion is limited
to the targeted primary-source searches described above.
