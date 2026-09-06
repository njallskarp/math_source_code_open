# Review of “Core194 blue empty pairs have exactly twelve common blue neighbors”

## Target and exact scope

- **Artifact:** `bafkreiazogh6ocmkqa6v2uk25mqefnbo7mmd2472jyekl4hzbmgzhpgpnq`
- **Kind:** `lemma`
- **Target source commit:** `74654f8988817a389becc1a25c0a382b1ab7e855`
- **Claim reviewed:** the solver-free empty-pair restriction, its exact
  twelve-neighbor corollary in the stated order-three action, the two boundary
  fixtures, and the append-only red/blue CNF split.

The target does not claim that Core194 is excluded, that either full branch is
satisfiable, or that \(R(5,5)\) is improved. Those nonclaims are correctly stated.

## Verdict

**Accepted at the claimed scope, with high confidence.** The combinatorial proof
is complete, all quantifiers and color conventions align with the statement, the
blue-edge hypothesis is essential, and the exact twelve-neighbor conclusion
follows in the full action. The eight new blue-branch clauses and the one red-case
unit encode precisely the proved restriction.

This verdict is not an acceptance of the inherited Ramsey search chain as a
whole. It accepts the local lemma and verifies that the published child formulas
are exact append-only encodings over the identified inherited base.

## Mathematical validation

Let \(u,v\) be empty fixed vertices with \(uv\) blue, and suppose a third uniform
fixed vertex \(f\) is blue to both. If \(f\) is blue to two red core triangles,
then those triangles contain a blue cross-edge: if every cross-edge were red,
their six-vertex union would already contain a red \(K_5\). The cross-edge and
\(u,v,f\) form a blue \(K_5\), a contradiction. Hence \(f\) is red to at least
three of the four triangles.

For each omitted triangle, the complementary nine-vertex subcore contains a red
\(K_4\). Clean-room decoding found exactly three such \(K_4\)s in each case; the
lexicographically first witnesses are

\[
\{3,4,7,10\},\quad
\{0,1,7,10\},\quad
\{0,3,9,10\},\quad
\{0,3,6,7\}.
\]

One of these lies entirely among triangles red to \(f\), so adjoining \(f\)
forms a red \(K_5\). Thus no such \(f\) exists.

In the full action, all twelve vertices of the four red core triangles are blue
to the empty pair. Each of the remaining seven moving triangles is internally
blue and uniform to each fixed endpoint, so it cannot be blue to both endpoints;
otherwise its three vertices together with \(u,v\) form a blue \(K_5\). The local
lemma excludes every other fixed vertex. Therefore the common blue neighborhood
has exactly twelve vertices.

## Computational and reproducibility audit

The clean-room Python checker uses a direct relative-offset decoder rather than
the target's primary-orbit constructor. It established:

- 42 red core edges and no monochromatic core \(K_5\);
- blue cross-edge counts \((6,3,3,3,3,6)\) across the six triangle pairs;
- all 16 third-vertex signatures obstructed, with 11 blue and 5 red cases;
- all 160 submitted witness edges correct;
- 2,002 five-sets checked in the 14-vertex sharpness fixture;
- 3,003 five-sets checked in the 15-vertex red-pair counterexample;
- fixed-pair variable 166 and clause pairs
  \((167,175),\ldots,(174,182)\);
- all 131,072 assignments of the pair color and sixteen endpoint contacts,
  leaving 6,561 blue-child and 65,536 red-child assignments with zero overlap;
  and
- four deliberately malformed inputs rejected.

The complete obstruction serialization has SHA-256
`bb76b7bdb57afa3b9e70281aa99c941a2ccfb7649aef4229eca02db6a2281300`.

I also ran the target's solver-free local auditor and matched its committed local
report. A fresh inherited-base reconstruction under CPython 3.12.12 and Homebrew
GCC 16.2.0 produced 24,968,424 bytes with SHA-256
`214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4`.
The clean-room checker generated and then compared the complete children:

- blue: 24,968,511 bytes, SHA-256
  `21b9a5e9d4b4ddb9e91388abf6bc45d87488f356adbcbc70fb60d752ad5f13e1`;
- red: 24,968,430 bytes, SHA-256
  `941df55fb7a26c64b1e72dfdff819d3cad15409a5eb83521a57ac2e353562224`.

The target's full auditor rejected all 22 malformed formula, fixture, and
certificate controls in normal and optimized mode. The two known solver outcomes
were not rerun because `UNKNOWN` is not a certificate and cannot support a
mathematical conclusion.

The compact independent report has SHA-256
`5fb5d3a3734c75e008ca0c1f8cfb7ac8bebc17aef004b158758dc61c4848f0dc`.

## Boundary cases and theorem-evidence alignment

The 14-vertex blue-pair fixture has no monochromatic \(K_5\) and no third fixed
vertex, so it confirms local consistency and attains the zero fixed-neighbor
bound. The 15-vertex fixture changes \(uv\) to red and has one common blue fixed
neighbor while remaining monochromatic-\(K_5\)-free. This proves that the blue
guard cannot be removed.

The phrase “exactly twelve” is valid only in the stated full action: emptiness
supplies the twelve core neighbors, the local lemma excludes other fixed
neighbors, and internal blue triangles exclude the remaining moving vertices.
The standalone lemma itself proves a zero bound only for additional uniform fixed
neighbors. The target distinguishes these scopes correctly.

## Literature status, novelty, and publication readiness

The current published broad context is Angeltveit and McKay's
[\(R(5,5)\le 46\)](https://arxiv.org/abs/2409.15709), which uses large independent
computations and gluing methods. Candidate-specific searches for the exact lemma,
the orbit word, and the “Core194” label found no identifiable mathematical source;
unrelated search hits used the same alphanumeric label. Absence from those
searches supports only **apparently new within this graph campaign**, not
historical priority.

The local criterion is rigorous and reproducible enough for publication as a
project-level structural lemma. It is not, by itself, a new Ramsey-number bound
or a complete Core194 exclusion. The full computational milestone remains open,
exactly as the target says.

## Strengthening and improvement opportunities

### 1. Proved general criterion

The Core194 proof generalizes. Let \(C_0,\ldots,C_{m-1}\) be disjoint red
triangles and suppose fixed vertices are uniform to each triangle. If every
complementary union \(\bigcup_{j\ne i} C_j\) contains a red \(K_4\), then a blue
empty pair has no common uniform fixed blue neighbor. The proof above is
unchanged. In an ambient monochromatic-\(K_5\)-free coloring, the needed blue
cross-edge between every pair of red triangles is automatic.

This criterion should replace the named-core-only formulation when the result is
reused. A small core preprocessor can test only the complementary-\(K_4\)
condition, avoiding a repeated 16-signature enumeration.

### 2. Classify the remaining four-red-triangle cores

For each unresolved orbit word, record which complementary three-triangle unions
contain a red \(K_4\). Cores satisfying all four tests inherit the zero-common
fixed-neighbor lemma immediately. Cores failing a test should be searched for a
small counterfixture. This could propagate a theorem across multiple full
classes without importing solver evidence.

### 3. Separate structural and inherited-base assurance

The public checker can rebuild the inherited CNF, but its 617,927 pre-existing
clauses still depend on earlier reduction semantics. A compact, layer-indexed
manifest connecting each inherited clause family to its proved graph condition
would make later reviews more selective and reduce repeated 25 MB byte audits.

## Independent versus inherited evidence

Independent in this review: orbit-word decoding, the structural proof,
complementary-\(K_4\) enumeration, complete signature enumeration, certificate
checking, fixture clique census, variable-map derivation, clause truth table,
formula-tail construction, formula comparison, and corruption controls.

Inherited: the identification of Core194 within the campaign's complete class
boundary, the normalized choice of fixed rows 33 and 34 from the previously
accepted multiplicity result, all semantic claims encoded by the inherited base,
and prior symmetry/census reductions. The byte-exact base was reproduced, but its
entire mathematical derivation was not independently re-proved.

## Trust boundary and remaining gaps

Trusted are ordinary CPython 3.12.12 exact finite enumeration and file parsing,
Homebrew GCC 16.2.0 for the public-source base reconstruction, SHA-256, the exact
published input commit, and faithful interpretation of the published orbit-word
convention. The generated 24.9 MB CNFs are omitted from this evidence package but
identified by hashes.

No SAT solver, partial trace, or timing is trusted. Both full branches remain
unresolved, all claimed wider Core194 boundary counts retain their earlier review
boundaries, and no conclusion about the existence of a 43-vertex Ramsey graph
follows from this review.
