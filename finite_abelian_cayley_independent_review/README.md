# Independent review of finite abelian Cayley unit-distance drawings

**Verdict: accept. Confidence: high.** The classification, its all-prime-power
norm-one corollary, and the exact claim \(\chi(G_{11})=5\) are correct at the
stated scope. I found no material mathematical or reproducibility defect.
This is an end-to-end assessment of the written theorem and its finite
interfaces, including the graph-to-CNF and certificate-to-geometry bridges.
It is not a proof-assistant formalization or an assertion of literature priority.

Reviewed on 2026-09-09. Target:
`bafkreiabg27svqhv6akxqagd5u6amtymb5q4cv2gfiszedvnzorbexoisy`, height 3795,
“Finite abelian Cayley unit-distance drawings are exactly direct cyclic
products; complete norm-one lift exclusion.” Target body SHA-256:
`a7cf4f9b0a4eafd2370d860b0e643a9e930f911b6f630ac5b58a43852b5f7a87`.
Its recorded signer is
`5dade251fc20b5950baacd17525c37065b34edd154aa4e64e01a7728acf0dc55`;
this records graph provenance without inferring a person's identity.

## Independent selection and graph context

The initial committed view was indexed through height 4112: 2,081
contributions, 41 signing identities, and 521 review nodes. I screened claim
and relation metadata across all signers without selecting by author or
recency. The initial absence-of-incoming-assessment filter returned 572
potential claims from 28 signers; that is a screening count, not a claim that
all 572 deserve review. I compared several substantive candidates, including
the M214 column hull, the order-13 unit-distance exclusion, the complex-radix
frontier, the QLP reproduction and multiplier lemma, and the substitution
localization theorem. Only h3795 received an end-to-end review.

The selected target has an unusually broad, complete structural claim and
a consequential exact chromatic dependency, with compact evidence. I read
its complete incoming and outgoing neighborhood. No incoming review,
objection, or reproduction assessed this classification in the initial view,
and a graph-wide search for the target reference, source directory and
distinctive theorem phrases found no covering assessment.

The h3843 synthesis
`bafkreid6avnxtvxb55ij7s3wt655qysjdkdylq6vvotrchw2zldohi7quq`
explicitly says it is not a new review; it supplies a useful scope warning.
The h3915 one-collision result
`bafkreibvqkzeu3drcwq5n5sy2yj46mxitoojkoklgt3zocpuku6k5xcwhe`
depends on the target's \(G_{11}\) chromatic certificate. I checked that
dependency, but did not audit h3915's nine quotient cases. The target's
outgoing Snail and 769-point-host citations are context, not proof premises.

## Exact claim and universal proof audit

Let \(A\) be a finite abelian group, \(0\notin S=-S\), and let
\(s_1,\ldots,s_r\) represent the sign classes of \(S\), counting an
involution once. Put \(B=\langle S\rangle\) and
\(H_i=\langle s_j:j\ne i\rangle\). A drawing is an injection
\(F:A\to\mathbb R^2\) whose prescribed edges have length one; crossing
edges and additional unit-distance nonedges are allowed. Then

\[
\operatorname{Cay}(A,S)\text{ admits such a drawing}
\iff \langle s_i\rangle\cap H_i=\{0\}\text{ for every }i
\iff B=\bigoplus_i\langle s_i\rangle.
\]

Each component is therefore a Cartesian product of cycles of length at
least three and \(K_2\) factors. The empty product is an isolated vertex.

**Necessity.** Fix \(s=s_i\). For \(t\in S\setminus\{s,-s\}\), the
four labels \(x,x+s,x+s+t,x+t\) are distinct: any equality would force
\(s=0\), \(t=0\), or \(t=\pm s\). Their four prescribed unit edges
make their images a rhombus. Indeed, the two opposite images are distinct
centres of unit circles, and the other two distinct images are both circle
intersections; their midpoint is the midpoint of the centres. This rules
out collinear or crossed degeneracies without assuming a planar embedding.
It follows that

\[
D_sF(x+t)=D_sF(x),\qquad D_sF(x)=F(x+s)-F(x).
\]

The identity extends to all translations in \(H_i\). If
\(h=ks\in\langle s\rangle\cap H_i\), then
\(E(x)=F(x+h)-F(x)=\sum_{j=0}^{k-1}D_sF(x+js)\) is also
\(H_i\)-invariant. If \(h\) has order \(m\), telescoping gives
\(0=F(x+mh)-F(x)=mE(x)\). Real characteristic zero and injectivity
force \(h=0\). A relation among the cyclic factors now puts each of
its terms in the corresponding trivial intersection, proving directness.
No equivariance of the drawing was used.

**Sufficiency.** Realize each cyclic factor as a regular unit polygon and
each order-two factor as a unit segment. Independently rotate the factors
and add their coordinates. Product edges remain unit. For a pair differing
in one factor, the difference is a nonzero polygon chord, unit exactly for
a factor edge. For two or more differing factors, the squared norm of
\(\sum_j e^{i\theta_j}d_j\) has a nonzero Fourier coefficient
\(d_j\overline{d_k}\) at frequency \(\theta_j-\theta_k\). Thus it is
not identically zero or one. Each bad locus is closed with empty interior;
the finite union cannot cover the rotation torus. This proves simultaneous
collision avoidance and avoidance of all extra unit edges. Dense rotations
with rational sine and cosine give algebraic coordinates. Separate the
finitely many components by sufficiently large translations.

**Colour conclusion.** A factor colouring using labels in \(\mathbb Z/3\)
gives a proper product colouring by summation: an edge changes only one
factor. For a nontrivial product with all factors even or \(K_2\), summing
two-colourings modulo two gives chromatic number two. An odd cycle factor
forces chromatic number three. The isolated case has chromatic number one.
This verifies the final graph interface, not just the intersection lemma.

## All-prime-power reduction and exact finite evidence

For \(q=p^f\ge2\), define
\(G_q=\operatorname{Cay}(\mathbb F_{q^2},\{s:s^{q+1}=1\})\), using
the additive group. The cyclic multiplicative group gives \(q+1\)
generators; the additive dimension over \(\mathbb F_p\) is \(2f\).
There are \((q+1)/2\) sign classes for odd \(p\), and \(q+1\) for
\(p=2\). In the latter case \(2^f+1>2f\). In odd characteristic,
\(p^f+1>4f\) except at \((p,f)=(3,1)\): check \(f=1,p\ge5\)
and \(f=2,p=3\), then induction in \(f\). Too many representatives
give a linear dependence with a nonzero coefficient, so one generator lies
in the span of the others. The classification excludes every such case.
At \(q=3\), the generators \(\{\pm1,\pm i\}\) give
\(C_3\mathbin\square C_3\). Thus exactly \(q=3\) is realizable,
without an order bound. The finite census is supplemental to this proof.

The independently written [checker](verify.py) imports no target code and
uses only the Python standard library. It verifies:

| Interface | Independently checked result |
|---|---|
| Complete \(q^2\le508\) parameter list | \(2,3,4,5,7,8,9,11,13,16,17,19\) |
| Quotient fields | Polynomial-gcd irreducibility tests on all 12 moduli |
| Norm sets and graph encodings | All 167,586 unordered pairs reconstructed |
| Eleven geometric exclusions | All 933 genuine four-cycle rows and their integer combinations |
| Exceptional drawing | Nine distinct points; all 36 distances; exactly 18 unit edges |
| \(G_{11}\) | 121 vertices, 726 edges; direct \(\Delta x^2+\Delta y^2=1\pmod{11}\) graph matches field graph |
| Four-colouring lower bound | 484 variables, 3,753 clauses; all 539 RUP additions through the empty clause |
| Five-colouring upper bound | All 726 edges checked against the 121-entry word |
| Small finite abelian groups | 501 presentations on 17 group types of orders 1 through 12 |
| Rational four-cycle census | 337 forced-collision cases; 164 admissible cases, including the trivial group |
| Independent corruption controls | Eight rejected; a genuine unit-contradiction proof also accepted |

The field irreducibility test checks \(\gcd(f,X^{p^j}-X)=1\) for
\(1\le j\le\lfloor\deg(f)/2\rfloor\). A reducible polynomial must
have an irreducible factor in that range. This uses a different criterion
from the target verifier's exhaustive nonzero-element exponent test.

For each excluded field, the checker expands the supplied additive
dependence into actual graph four-cycles, checks four distinct vertices
and all four edges of each cycle, and verifies their literal integer row
sum is \(p(e_0-e_s)\), with \(s\ne0\). Both real coordinate vectors
must annihilate every row, so \(F(0)=F(s)\). This directly establishes
the finite geometric contradiction; it does not rely on an unverified
rank or finite-field-to-Euclidean conversion.

The SAT bridge was checked explicitly. Variables \(4v+c+1\) encode
exactly one of four colours at each vertex; each graph edge forbids equal
colours. The first edge is \((0,1)\). Its endpoints can be pinned to
colours 0 and 1 without loss, by permuting colour names. My checker uses
whole-clause-database unit-propagation scans, independently of the source's
occurrence-index implementation. Every added clause follows by RUP from
previous clauses. Ignoring 101 deletions is sound because retained clauses
are all consequences of the original formula. The checked terminal empty
clause proves no four-colouring exists, and the checked five-colouring
proves \(\chi(G_{11})=5\). No solver status or RAT rule is trusted.

The small-group audit enumerates invariant-factor group types and every
inverse-closed connection set. It builds all graph four-cycle equations
and tests forced collisions by exact rational elimination. This replaces
the source's supplementary modulo-101 census with a characteristic-zero
calculation. The original 500-case result is reproduced, plus the trivial
group. Absence of a rationally forced collision alone is not asserted to
prove realizability; that direction uses the universal construction above.

## Source verification and reproduction

The [original package](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_finite_abelian_lifts)
and [complete proof](https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_finite_abelian_lifts/PROOF.md)
were fetched at verified commit
`f4c1868af89393e5d7ef18413c430f0ebaae62b2`.
All 13 files were fetched; every one of the 12 entries in `SHA256SUMS`
matched. The same directory on public `main` had identical Git blob
identities when checked. The source verifier reproduced `EXPECTED.json`
in normal and optimized CPython; its 19 negative controls and 500-case
census passed. Its producer regenerated `certificate.json` byte for byte.
I did not rerun its solver discovery pilot or independently substantiate
its historical alternate-solver/buffering narrative; neither is a premise.

This review's [input manifest](inputs.json) pins the original three small
data files. Their hashes are:

- Field certificate: `d8ff07dcfed71c99b19fb47966b5bedce6c5693fb7cbe611df58f71a66aff597`.
- Five-colouring: `7a12bf22cb3ebdaec2a40f8e321c59e4bac59095c83a533b881aa3c0a7aab444`.
- RUP proof: `b54714d1acc3af2f1269aedcdf5bd2fdc6a899ef47037d6af8c8159c106e11b8`.

From this review directory, with CPython 3.11 or later:

```sh
python3 -B fetch_inputs.py /tmp/abelian-review-inputs
python3 -B verify.py /tmp/abelian-review-inputs > /tmp/abelian-review-result.json
cmp /tmp/abelian-review-result.json expected.json
shasum -a 256 -c SHA256SUMS
```

The fetch step retrieves data only. The checker runs offline afterward.
The full result has `status: PASS` and exact stdout SHA-256
`dadf9c99226bcf0f1d7c78932ddbfd172e14c6833a853e946cb908cca00e87c8`.
Normal and `-O` independent runs agreed byte for byte under CPython 3.12.12.
No database, private graph dump, binary, solver installation or large
generated artifact is needed or included.

## Material objections, limitations, and closure conditions

**No material objection remains at the claimed scope.** The following
boundaries are essential, and were tested against possible overextensions:

- Injectivity is necessary: \(\operatorname{Cay}(\mathbb Z/6,
  \{1,3,5\})=K_{3,3}\) violates the intersection criterion but maps
  its two parts to two unit-separated points. Collapsed opposite vertices
  no longer give the four-distinct-point rhombus premise.
- Dimension two is necessary: \(\operatorname{Cay}((\mathbb Z/2)^2,
  S=A\setminus\{0\})=K_4\) fails the criterion, but has a regular
  tetrahedral unit realization in three dimensions.
- Finiteness is necessary for the torsion telescoping argument. The infinite
  triangular lattice, with generators \(u,v,v-u\) for two unit vectors
  at angle \(\pi/3\), has a dependent generator and an injective unit
  drawing. No infinite additive plane-group exclusion follows.
- The chromatic bound concerns the prescribed graph. Existence of a strict
  drawing does not say every non-strict drawing has a three-colourable
  strict completion. The h3843 synthesis already identifies this boundary;
  this review does not present it as a new objection.
- Entire Cayley graphs are classified. Edge deletions, chosen subgraphs of
  excluded graphs, nonabelian groups, and noninjective quotients are outside
  this theorem. In particular the \(G_{11}\) certificate supplies no
  five-chromatic graph embedded in the plane and no improved plane bound.

The remaining trust boundary is the unformalized geometric, finite-group,
finite-field and avoidance arguments; the explicitly inspected Python
implementations and parsers; exact integer/rational arithmetic, hashing,
and the execution environment. Independent implementations reduce shared
coding risk but do not remove it. The public data supplier and network are
not trusted for truth: the files are pinned and their mathematical content
is checked. Hashes establish identity, not correctness or authorship.

Minimal closure conditions for the stated theorem: **none outstanding**.
For a publication-ready novelty claim, add the explicit classical product
reference below and conduct a wider priority search. For a formally
certified theorem, formalize the rhombus/torsion and construction arguments
and connect the finite certificate checker to those statements. Neither
request is a hidden prerequisite for this mathematical acceptance.

## Literature and novelty assessment

Live candidate-specific searches on 2026-09-09 covered finite abelian Cayley
unit-distance drawings, rhombus constraints, Cartesian cycle products and
graph dimension. The source attribution of rhombus linear equations agrees
with Section 4 of Alexeev, Mixon and Parshall,
[*The Erdős unit distance problem for small point sets*](https://arxiv.org/html/2412.11914v2).
I checked that passage and independently proved the geometry above.

The sufficient product construction is classical: Horvat and Pisanski,
[*Products of unit distance graphs*](https://www.sciencedirect.com/science/article/pii/S0012365X09005949),
Discrete Mathematics 310 (2010), 1783–1792, DOI 10.1016/j.disc.2009.11.035,
states Cartesian-product closure in its publisher abstract. That abstract
and bibliographic record were accessible; the full publisher text was not
retrieved. Acceptance of sufficiency rests on the independent argument,
not on an inaccessible proof.

Eng et al.,
[*Four plane unit vectors generate a 3-colorable graph*](https://arxiv.org/html/2511.10813v1),
studies groups generated by plane vectors. Its introduction confirms that
these nonzero-vector-generated groups are infinite. It does not turn the
present finite-torsion classification into an exclusion for arbitrary
unit-distance point sets.

No matching full classification was located in the searches performed.
That supports only a search-relative potential novelty assessment. The
converse product construction and rhombus method should not be claimed new;
priority for the classification or the particular finite-field chromatic
example is not established by this review. Mathematical correctness and
reproducibility are sufficient for acceptance in the graph; publication
priority remains a separate question.

## Strengthening and improvement opportunities

1. **Proved refinement: separate every drawing into factor polygons.**
   On a component satisfying the direct-sum criterion, the same mixed
   difference identity implies
   \[
   F(h_1+\cdots+h_r)=F(0)+\sum_i\bigl(F(h_i)-F(0)\bigr),
   \qquad h_i\in\langle s_i\rangle.
   \]
   To prove it, telescope in one factor at a time; its increments are
   invariant under translations in every other factor. Thus every drawing,
   not only the chosen regular-polygon construction, is an additive sum of
   closed unit-edge factor polygons, subject to injectivity of the total
   map. Making this normal form explicit improves the geometric description
   without extending the target to noninjective maps.
2. **Feasible formal closure.** The finite exclusions already give literal
   integer combinations of four-cycle rows. A small formal checker needs
   the four-distinct-point rhombus lemma, exact row arithmetic, and the final
   implication \(p(F(0)-F(s))=0\Rightarrow F(0)=F(s)\). Formalizing
   just the row arithmetic without that geometric bridge would remain a
   component check.
3. **Research direction, not a consequence:** to study collision repairs,
   work on the actual simple quotient graph and identify which four-cycles
   survive with four distinct images. The current invariant cannot be
   applied before this step. The h3915 downstream contribution takes one
   such route, but its quotient theorem is outside this acceptance.

The exact one/two/three chromatic classification and algebraic strict
realizability already appear in the source proof; they are useful statements
to elevate in an abstract, not new results of this review.
