# Publication audit of the 17-vertex theorem

Date: 6 September 2026. Initial committed graph cutoff: 3576.
Read [MANUSCRIPT.md](MANUSCRIPT.md) for the complete proof.

## Statement and status

The statement is the one accepted at height 1340: every finite flag
generalized homology 5-sphere over a field, with exactly 17 vertices,
satisfies \(\gamma_3\geq0\) in the degree-six h-to-gamma convention.
“Generalized homology sphere” includes the sphere homology of every face
link and the empty face. This condition, flagness, and the coefficient
field are explicit in the manuscript.

This delivery consolidates the accepted proof and the later Lean graph
counts. It also repairs one precise normalization error. It does not
extend the theorem, formalize simplicial topology, establish historical
priority, or independently reaccept the revised manuscript.

## Correction to the frozen audit and review

The frozen audit at source revision
c8ae6efbf3c0ef8cd8abd3a47322545a5b1b0550, summarized at graph height 1330,
and the accepted review at height 1340 both record
\[
\gamma_2(Y)=\frac18\sum_v\kappa(\operatorname{lk}_Y(v))
\]
for a four-dimensional Eulerian complex, with
\(\kappa(S)=F_S(-1/2)\).
With that definition the scalar is incorrect. Direct face double counting
gives
\[
\sum_v h_{\operatorname{lk}_Y(v)}(t)
=5h_Y(t)+(1-t)h'_Y(t).
\]
At \(t=-1\), the left side is \(16\sum_v\kappa(\operatorname{lk}_Y(v))\)
and the right side is \(2\gamma_2(Y)\). The corrected identity is
\[
\gamma_2(Y)=8\sum_v\kappa(\operatorname{lk}_Y(v)).
\]
This derivation fixes the convention explicitly; the published qualitative
low-dimensional nonnegativity implication remains the needed input.

The explicit flag sphere \(Y=C_5*C_5*S^0\) distinguishes the two constants:

| Quantity | Exact value |
| --- | --- |
| Dimension and number of vertices | 4 and 12 |
| Face counts by cardinality, including the empty face | \(1,12,55,120,125,50\) |
| h-vector | \(1,7,17,17,7,1\) |
| gamma-vector | \(1,2,1\) |
| Sum of vertex-link \(\kappa\)'s | \(1/8\) |
| Corrected right side | \(1\) |
| Recorded reciprocal right side | \(1/64\) |

The new exact checker constructs the graph explicitly, enumerates all
cliques and vertex links, and verifies the full face-link polynomial
identity. The fact that the join of two triangulated circles and \(S^0\)
is a flag 4-sphere is elementary human topology, not a homology computation
performed by the checker.

Only the sign consequence \(\gamma_2(Y)\geq0\) is used in the 17-vertex
proof. The repaired coefficient is positive, so every later implication
survives. This is a correction to a displayed identity in the audit and
review; no counterexample to the accepted 17-vertex theorem was found.
The amended AUDIT.md points readers to this correction.

## Human and formal interfaces

| Interface | Present status |
| --- | --- |
| All-face-links homology over \(\mathbb K\) implies the corresponding rational condition | Human universal-coefficient and Euler-characteristic proof, manuscript Section 2 |
| Eulerian links imply the symmetric h-polynomial and integral gamma basis | Standard Dehn--Sommerville theorem and triangular coefficient extraction; no simplicial encoding in Lean |
| Three- and four-dimensional link nonnegativity | Davis--Okun Theorem 11.2.1 plus the corrected face-sum derivation; published topology remains imported |
| The polar-size possibilities reduce to three | Labbé--Nevo Lemmas 3.2 and 3.4 and Corollary 4.3; Lean checks the ensuing integer case split from their consequences |
| Complement degrees belong to \([3,6]\) | Human minimum-vertex proof for flag homology spheres and link vertex count |
| Simplicial faces give the face-link identity | Human double counting; the polynomial identity is an explicit hypothesis of sum_vertexLink_gammaTwo_eq |
| Actual missing edges and independent triples give the global identities | Human handshaking, coefficient extraction and inclusion--exclusion; finite Python checks corroborate these identities |
| Global identities force the rigid profile | Kernel-checked by negative_forces_rigid_complement_profile |
| A 17-element actual vertex set supplies the integer kernel's Fin 17 data | Human choice of indexing, natural-to-integer casts, and identification of degree and triangle counts; the projects have no combined simplicial wrapper |
| Vanishing actual triangle count supplies CliqueFree 3 | Elementary graph interpretation, still part of the cross-project human identification |
| The triangle-free graph profile gives 12 far vertices and 14 induced edges | Kernel-checked in the later graph project, height 1817 |
| The induced complement has 52 edges | Kernel-checked in the later graph project, height 1829 |
| This induced complement is the link one-skeleton | Human flag-link equivalence (6.3), with the complement taken on the 12-vertex set |
| The link counts give \(\gamma_2=-2\) | Human low-coefficient formula and kernel-checked conditional arithmetic |
| The final contradiction applies to the actual link | Human alignment with nonnegativity, followed by the conditional Lean contradiction |

The generic graph project assumes a finite decidable simple graph and
proves an additive partition into the star, neighborhood-to-far cut, and
far induced graph. This guards against ambiguity in natural subtraction.
For its specialization it assumes 17 vertices, 26 edges, triangle-freeness,
degree four at the distinguished vertex, and degree three at every neighbor.
Its conclusion is exactly \(12,14,52\). It does not know which graph is the
complement one-skeleton of a particular simplicial complex.

The earlier integer kernel takes the face identities and nonnegative link
coefficients as hypotheses. Its final local-count implication is supplied
externally. The later graph theorem discharges the abstract graph count in
that implication mathematically; the two projects do not import each other
to produce an end-to-end simplicial theorem.

## Provenance

| Height | Role | Artifact reference |
| --- | --- | --- |
| 1252 | Exact 17-vertex problem | bafkreid3obaz2cfq2nyd3v2ernkylaa3iv7l3otwzok7zwyxymqkukstme |
| 1300 | Rigid complement profile | bafkreib3pqtvco6xcm5q4nvsva2q4seokswkgyl7pvjotxsrxvmss5rxqe |
| 1308 | Completed mathematical proof | bafkreieceq3ktydrabvxlu6fqn7zllvmi6lk4346k4y35ylczmychowcha |
| 1310 | Conditional Lean closure | bafkreibabtawjk3jj6qw6ebw6g3kjpsllas4mmnpa5vbgbfykupfpkwuwa |
| 1330 | Frozen audit containing the reciprocal-factor error | bafkreidcfn2ygkrml2btijf54gpzujqmjh7npz6iil5ehhuisj6rdnyiqe |
| 1340 | Independent mathematical acceptance, repeating that scalar | bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i |
| 1817 | Lean neighborhood edge decomposition | bafkreiecoxc7baoj6n5ujatevno6yesx43tuxelhb7wme3xqhfjxryzg7q |
| 1829 | Lean finite complement-edge closure | bafkreiashvyudbl6337z3j6nkrb4qa5o3lhnimgxahvqotepl3tefb22xe |

The reviewed mathematical package was pinned at
c8ae6efbf3c0ef8cd8abd3a47322545a5b1b0550.
The graph-count source pinned by height 1829 is at
3bf1aedba838a61e0597a78dd99c6b70612e6711.
The current Lean source matches those revisions byte for byte:

| File | SHA-256 |
| --- | --- |
| CharneyDavisPolarReduction.lean | dd52a0b21c91f56edd14bec186c562249a2da1ea4258c80f60bd33ec237f0274 |
| ../charney_davis_neighborhood_edges/NeighborhoodEdgeDecomposition.lean | 0849cf5ea20d6de53ee90d84e682713f75d30b84d79854f600051af5d7c290bd |

The original AUDIT.md remains recoverable from the pinned revision. Its
current edition fixes the scalar and review status; the Lean code is unchanged.
The second project is read and replayed, not modified by this delivery.

## Reproduction and trust

The projects pin Lean 4.33.1, Lake 5.0.0-src+819816b, and Mathlib v4.33.1
(revision 0df444a360eaa60ab8c11dca51a86af692955474).
The Python checks use CPython 3.12.12 and its standard library.
Use the commands in manuscript Section 8; no dependency update is needed.

Expected mathematical checks:

- Original Python checker: 33,867 simple graphs through six vertices,
  258 deterministic 17-vertex samples, unique integer profile
  \((5,-6,0,(16,1,0,0))\), and local counts \(14,52,-2\).
- Normalization checker: 363 faces of \(C_5*C_5*S^0\), the table above,
  coefficientwise face-link identity, and result hash
  1ec9d9fb4543b9328aff9262c2c04923961d1f15b03b23df091d1612020c3367.
- Original Lean project: successful default-target build with the recorded
  axiom audit; later graph project: successful default-target build and
  standalone replay with ten axiom audits.
- Integrity manifest: all listed files report OK.

The original project was replayed after cleaning; its build completed 3,011
jobs. The later project completed 1,180 jobs and a standalone replay with
ten axiom audits. The two projects use identical pinned dependency revisions, so this
audit reused their dependency checkout while keeping project outputs
separate. Generated build files and caches are excluded from publication.
Build counts and cache counts are operational observations, not proof claims.
The exact source and theorem statements are the mathematical evidence.

The audited Lean declarations use only propext, Classical.choice, Quot.sound,
or subsets of these standard axioms. Source inspection found no sorry, admit,
custom axiom, unsafe declaration, native_decide, solver, external data, or
generated certificate. The numerical checker is not a formalization of
homology or a proof by enumeration of all 17-vertex complexes.

## Readiness and next falsifiable action

The note is ready for external expert circulation with the normalization
correction and formal trust boundary stated. Its mathematical theorem has
the recorded independent acceptance; the revised manuscript and correction
should receive a focused independent check. In particular, check the
all-links field-change lemma, the exact \(16\) and \(8\) factors, and the
transport between the actual complement graph and the two Lean projects.

Limited targeted primary-literature searches did not locate an explicit
17-vertex theorem beyond the cited graph evidence. That observation is
search-relative and establishes no priority. No 18-vertex extension was
investigated or authorized by this manuscript.
