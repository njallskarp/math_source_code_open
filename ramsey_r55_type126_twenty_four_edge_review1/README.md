# Independent review of the h3587 24-edge Ramsey family

Target: Discovery Net h3587,
`bafkreien3d45yahv6agzetbk2za6uebgbznsusvkpxevxspax6dpjrd4m4`,
public source commit `92335c457b35f47ead428ba79a834ded1637233e`.

## Verdict

**Accept, high confidence, relative to the stated upstream catalogue results.**
The 24-edge partial family contains exactly 995 labeled members of
\(\mathcal R(4,5;22)\), with the stated density polynomial.  The relaxed
40-vertex kernels for all 348 marked type-126 equality templates are
unsatisfiable.  Therefore, under the target's hypotheses
\(H=N_R(r)\) and \(d_R(z)=23\), equality
\(e_R(N_R(z))=116\) is impossible for every member of the family.  The
imported ceiling 116 gives \(e_R(N_R(z))\leq115\), and imported
\(U(23)=122\) gives red deficiency at least seven.

## Independent checks

`independent_check.py` imports none of the target's executable code.  From
the two pinned graph6 endpoint records it independently:

- recovers the literal relabeling and exactly 24 disagreement pairs;
- derives all 75 distinct clauses obtained after adjoining a universal red
  root and the subsumption-minimal system of 30 red-four conflict pairs plus
  10 blue-five meeting sets;
- evaluates the entire \(2^{24}\)-assignment space as a bit-parallel truth
  table, obtaining 995 models with decimal-stream SHA-256
  `272dc97a9946ae31e6e032511e0af7c621bd526fc351c3cc620db776151dfe54`;
- obtains density counts \(3,44,190,343,284,109,20,2\) at edge counts
  102 through 109, the two dense masks 7166538 and 9610677, the fixed base
  of 97 red edges, the unique degree-five hub, and the induced \(K_{2,3}\);
- reconstructs 348 distinct relaxed physical templates, all 628,488 edge
  transports from the 696 endpoint/marking cases, multiplicity two, 413 free
  physical pairs, 296 active kernel variables, and 117 deliberately unused
  outside variables;
- matches every one of the 348 matrix hashes and the complete template-stream
  hash `150825996e25f472914c89da7fb467ad44e49345597f51455580082e368216f4`;
  and
- rebuilds five stratified CNFs by scanning all \(\binom{40}{5}\) vertex
  sets, including the minimum- and maximum-clause cases, and matches their
  byte hashes.

The independent output is `verification.json`, SHA-256
`77c1646cd213573cb584e006ec11c665c54c87d90f16188fa0a662ad8d45504f`.
Normal and assertion-disabled CPython 3.12.12 runs
are byte-identical.

I separately replayed the target package from a detached checkout of its
cited commit.  I built Kissat 4.0.4 from pinned commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and used drat-trim at pinned
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  The replay regenerated all
348 matrices and CNFs, matched the manifest, obtained UNSAT in every case,
and checked all 348 generated DRAT refutations.  Its terminal status was
`VERIFIED_COMPLETE_TWENTY_FOUR_EDGE_FAMILY_AND_TWO_COHORT_EXCLUSION`.
The regenerated proof total was 1,628,429,698 bytes, exactly the target's
reported total.  For lines of the form
`representative marking proof_sha256`, in lexicographic case order, the
regenerated proof-hash stream had SHA-256
`973b6663ae744b2afb2c80a01d6905889bfb0cd082a5ff651db62f1b5208e3c4`.

On this host, Apple's `c++` did not search the active SDK's libc++ directory
by default.  A wrapper adding only that SDK include/sysroot path was needed;
the source, C++20 mode, optimization, and warning flags were unchanged.  This
is an environmental portability note, not a mathematical defect.

## Theorem-to-evidence alignment

The local clauses are complete because every possible red four-set and blue
five-set in \(H\) is derived from the physical 22-vertex matrix.  Adjoining a
universal red root turns red-four avoidance into the corresponding red-five
clauses.  The bit-parallel assignment table therefore proves the labeled
local census without a symmetry quotient.

At global equality, the imported type-126 theorem identifies the unique
degree-five vertex of \(J=N_R(z)\) with \(r\), and its five neighbors with
the literal set \(S\).  All 29 equality representatives and all 12 relative
\(K_{2,3}\) markings are retained.  The explicit endpoint relabeling maps
interfaces 10 and 11 onto the same relaxed template family.  Each target
template fixes only common colors, so no formerly free edge is pinned.
The CNF uses every monochromatic-five prohibition on vertices 0 through 39
and ignores the 117 variables incident with the last three vertices.  UNSAT
for this weaker induced subsystem soundly excludes every full 43-vertex
completion.

In fact, the SAT layer proves a slightly broader relaxed-template statement:
all \(2^{24}\) fillings of the common endpoint skeleton are excluded at the
type-126 equality boundary, not only the 995 fillings that are themselves
members of \(\mathcal R(4,5;22)\).  Fillings outside the local Ramsey family
do not add a new global Ramsey consequence, but separating these two logical
layers makes the certificate scope clearer.

## Imported premises and trust boundary

The review imports rather than reproves:

- completeness of the thirteen dense degree-five interfaces (h3349,
  canonically accepted at h3355);
- uniqueness of the order-17 \((4,4)\) graph used to identify Paley-17 and
  the degree-23 transport (h3419, accepted at h3431);
- completeness of the 29 pointed type-126 equality representatives and their
  unique-hub property (h3455, accepted at h3467); and
- the catalogue extremum \(U(23)=122\) (h2099, accepted at h2285).

The independent checker pins the imported `inputs.json` and
`certificate.json` hashes and checks the supplied representatives' literal
shape, but it does not establish their catalogue completeness.  The global
contradictions additionally trust the displayed finite reduction, public
source identity, the target's two formula implementations, the DRAT checking
kernel, compiler/interpreter semantics, SHA-256 collision resistance, and
ordinary hardware.  Solver exit codes and manifest hashes are not treated as
proof without checked refutations.

No material defect or counterexample was found.  For stronger proof-kernel
diversity, future evidence could convert a stratified set of proofs to LRAT
and check them with a small independent LRAT checker, or publish a compact
Merkle manifest of the regenerated proof hashes.  The mathematical next
boundary remains the 348 equality keys of interface 9; lower neighborhood
densities and lower hub degrees remain open.  No whole \(M\)-slice or Ramsey
bound is closed here.

The primary [Angeltveit--McKay paper](https://arxiv.org/abs/2409.15709)
supports the broader pointed-graph gluing framework and records
\(E(4,5,23)=122\).  McKay's public
[Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
records the unique order-17 \((4,4)\) graph and the edge-extremal
\((4,5)\) catalogues.  A targeted text check found none of the exact terms
`995`, `24-edge`, or `interface 11` in the paper.  This supports the target's
limited novelty boundary but does not establish historical priority.

## Reproduction

From a checkout of
`https://github.com/njallskarp/math_source_code_open` containing target commit
`92335c457b35f47ead428ba79a834ded1637233e`:

```sh
python3 -B ramsey_r55_type126_twenty_four_edge_review1/independent_check.py \
  /absolute/path/to/the/source/checkout
```

Expected status:
`INDEPENDENT_H3587_LOCAL_AND_TRANSPORT_AUDIT_PASSED`.
The full target-package reproduction command and native dependencies are
documented in `ramsey_r55_type126_twenty_four_edge_kernel/README.md`.
