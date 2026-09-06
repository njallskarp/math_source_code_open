# Audit map for the full planar equality proof

Audit date: 6 September 2026. Committed graph cutoff: height 3564.
Principal source: [MANUSCRIPT.md](MANUSCRIPT.md).

## Verdict and delivery scope

The reconstruction found no invalid inference in the slope-quantization
proof at height 1769. The manuscript makes its limiting and topological
steps explicit and incorporates the finite strictness calculations into
one proof. This is a completed proof-audit/source-delivery milestone.
It is not a new theorem, an independent review verdict, or evidence that
the full classification has been independently accepted.

At this cutoff, height 1769 has no incoming review, objection, or
reproduction relation. The independently accepted finite-polygon chain
ends at height 1757; its scope cannot be enlarged by editorial work.
The full manuscript is ready for adversarial mathematical review with
that status stated. It is not ready to describe as an independently
accepted resolution.

## Exact theorem

For each fixed real \(1<p<\infty\), put \(q=p/(p-1)\) and
\(c_q=2\Gamma(1+1/q)^2/\Gamma(1+2/q)\).
For a full-dimensional compact convex planar body with a center of symmetry
and containing zero, the proposed conclusion is
\[
|K+_p(-K)|=(2+c_q)|K|
\quad\Longleftrightarrow\quad
K\text{ is a parallelogram with a vertex at zero}.
\]
Central symmetry is about an arbitrary center. The origin is part of the
placement data. The manuscript makes no endpoint-\(p\), higher-dimensional,
arbitrary-body stability, or formal-verification claim.

## Composition map

| Obligation | Exact hypothesis and conclusion | Resolution in manuscript |
| --- | --- | --- |
| Global ceiling | Every centrally symmetric planar body containing zero satisfies the sharp upper bound | External input U, Section 1 |
| Linear normalization | Invertible linear maps preserve the ratio and origin placement | Support identity, Section 1 |
| Translation normalization | All translates in the interval contain zero; original placement is interior in the parameter | Compact translation lift and equality propagation, Sections 3 and 9 |
| Segment representation | Arbitrary central body containing zero has a finite positive oriented generating measure | Polygon representations, bounded measure mass, weak compactness, Section 4 |
| One-sided slopes | Zero is an exposed-face endpoint; downward mass vanishes; horizontal mass has one orientation | Section 4, equation (4.4), including the first-moment bound |
| Area formula | Finite measure with integrable slopes; horizontal mass \(h\geq0\) | Simple-function approximation, support continuity and (5.1), giving \(\lvert K\rvert=hM+D\) |
| Positive bins | At least \(k\) support points, \(k=2\) or \(3\) | Separated support neighborhoods and cuts outside the countable atom set, Section 6 |
| Exact quantization | \(D>0\); smooth monotone quantizers have positive area eventually | Rescale by \(D/d_n\), equation (6.3) |
| Negative parameter | Lipschitz constant belongs to the rescaled map | Equation (6.5) proves order preservation on a nonempty negative interval |
| Genuine shadow | Slopes may be unbounded but have finite first moment | Compact closure of the lifted selector set, with three explicit coordinate bounds, Section 7 |
| Constant area | Ordered differences keep their signs for every parameter | Equation (6.6); the horizontal contribution remains \(hM\) |
| Equality propagation | Same positive area and common ceiling; original equality is at an interior parameter | Convexity from horizontal sections and Firey coefficient lift, Section 3 |
| Limit | Quantizers converge in \(L^1(\nu)\) | Uniform support bound (7.6), Firey support bound (2.5), area continuity (2.4) |
| Six sides | Exactly three nonzero pairwise nonparallel generators in a pointed cone | Positive functional and side-count argument, Section 7 |
| Strict obstruction | All finite \(p>1\), all positive normalized hexagon parameters | Complete half-boundary formula and derivative sign change, Section 8.1 |
| Original origin placement | Shape first known to be a parallelogram | Exact edge deficit, then an interior chord avoiding four vertices, Sections 8.2 and 9 |

Two details prevent common false shortcuts. First, strictness of approximating
polygons never implies strictness of the limit. Here each approximation
endpoint is itself an equality body before the limit is taken. Second,
\(\varepsilon_n\) may tend to zero. The argument needs an interior parameter
for each individual shadow, not a common negative interval for all shadows.

The compact-lift proof also resolves a possible ambiguity in the phrase
“every indexed point moves affinely”: bounded generators are not assumed,
and different selectors representing one projected point may have different
speeds. Their integrated speeds are uniformly bounded for each shadow.
Closing the lifted selector set makes all required convex sets compact.
This is an explicit justification of the original argument, not a discovered
counterexample to it.

## Imported theorems and foundational trust

The only problem-specific external inequality left as an import is
Corollary 29 of
[Fradelizi--Manui--Meyer--Ndiaye, arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1#S4).
It supplies the upper bound and the origin-vertex parallelogram equality
examples. Its Conjecture 5 is the classification target, not a theorem used
in the proof. The live arXiv record checked on the audit date lists version 1.

The relevant classical shadow statements are Theorems 2.2 and 2.3 of
[Bianchini--Colesanti, arXiv:math/0702102v1](https://arxiv.org/pdf/math/0702102v1).
The manuscript proves the required planar compact-lift versions directly,
including Firey closure by nonnegative coefficient duality. Thus it does
not silently assume a theorem for finite index sets applies to arbitrary
selectors, or that the lift contains the origin.

The human proof still uses support separation, finite-dimensional
compactness, weak compactness of finite positive measures on the circle,
simple-function approximation in \(L^1\), dominated convergence, Fubini,
Green's formula, and the beta integral. Section 2 proves the precise
Hausdorff/area and Firey-continuity facts needed in the limits. No Lean
artifact, numerical experiment, or checksum verifies these human bridges.

The finite strictness and edge-placement arguments are independently
reviewed inputs from the graph, reproduced in Section 8 for a reader
without graph access. The polygon deletion induction itself is not needed
by the direct continuum-to-hexagon reduction.

## Committed evidence and immutable provenance

The following content-addressed graph artifacts identify the actual claims
and their reviews. All were reconstructed from committed GraphQL results,
not inferred from a source directory name.

| Height | Claim or review | Artifact reference |
| --- | --- | --- |
| 961 | Equality problem and distinction from the unrestricted inequality | bafkreicafoo54mtx6wfmjncrewegqdpo33tub57irza46bsq2cfpvfvbgy |
| 1731 | Strict all-\(p\) origin-vertex hexagon theorem | bafkreiheholqeo36ftoxx55wz6ofwuklfwehvkpymxdr2kebeh2bnpa7y4 |
| 1747 | Independent acceptance of 1731, with a refined finite stability bound | bafkreiafllskekl2fsoxh6amkmhhuty6va6myc5ia4gaxz7yymmhrzzw24 |
| 1749 | Finite-polygon equality classification | bafkreia5tvsipltq7nhjsz6j5m5jxbfk4cxibvunlaq3bvjygtpr3veraa |
| 1757 | Independent acceptance of 1749; nonuniform deletion-factor warning | bafkreiagat34zqdzk6mj6ja6cmxo3rvpn7qs5jkedf3yqfw3uoydygelfu |
| 1769 | Proposed arbitrary-measure equality classification | bafkreig74h4lfjxgwy5y472whjk24muf5eh7tlsy2ps6zlr74dmkgq56tu |

The proof artifacts 1731, 1749 and 1769 share an author signer. The review
artifacts 1747 and 1757 have a distinct reviewer signer. No review of 1769
was present at the cutoff. This audit is not submitted as a verification
relation.

Height 1769 pins public source commit
**84f1b71f73f63e42b433737371a0345a1aaaacee**. Its original proof and checker
match the fresh public clone byte for byte:

| File | SHA-256 |
| --- | --- |
| ZONOID_QUANTIZATION_FULL_EQUALITY.md | d75769cb129d632511bfed2eda2d08054b43aead99bb9640b8f5291a0664a3e2 |
| verify_zonoid_quantization.py | 2d255da73263eb229e09af41032a52570a3bfe48019e621fd47369141ae99402 |
| FIREY_HEXAGON_ALL_P.md | 2cb73cfc1d8c5283b32d7fb0e7663027373f0957f2673c1c434757f9b7897be2 |
| SYMMETRIC_POLYGON_EQUALITY.md | 28ea7cf3fbc91ed8fe59da0eed553dee9680dca4b1131e0299b2adc6f1f30986 |

Those four files remain unchanged. New exposition is confined to the
manuscript, this audit map, the README status, and their integrity manifest.
The new delivery commit is recorded by Git history; it is not substituted
for the immutable evidence cited by height 1769.

## Reproduction and remaining falsifiable obligation

In this directory, with CPython 3.12.12 and no third-party packages:

~~~sh
python3 verify_zonoid_quantization.py
shasum -a 256 -c SHA256SUMS
~~~

The first command ends with:

~~~text
result_sha256=e0a90164ffd457f60d55c805af0ca31d1a038310b1ffad96fae7f8ed6cfed398
VERIFIED
~~~

Every manifest entry must report OK. The checker corroborates two
uniform-measure examples only. The audit did not expand its scope or treat
its output as a proof of the continuum lemma.

The next falsifiable action is a genuinely independent review of the
height-1769 implication for arbitrary measures, using Sections 4--7 of the
manuscript and checking its composition with Section 8. A specific failing
measure, missing compactness hypothesis, invalid support limit, or incorrect
hexagon reduction would defeat the proof. No such defect was identified in
this audit. No graph contribution is added for this packaging milestone.
