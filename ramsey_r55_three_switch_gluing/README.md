# A minimal three-block gluing obstruction for the R(5,5) interface

This package proves an exact block-relation completion theorem and realizes
its missing consistency condition in a **vertex-minimal 15-vertex
proper-three-anchor skeleton**.

The skeleton passes all six full root-neighborhood tests and both
mixed-stratum tests. Each of its three complementary \(2\times2\) blocks
has two degree realizations. Every two-block subsystem has two solutions,
and every individual state has support in each other block. Nevertheless,
no joint degree-constrained Ramsey completion exists.

Six literal blue-\(K_5\) clauses force

\[
x_0\ne x_1,\qquad x_1\ne x_2,\qquad x_0\ne x_2.
\]

The missing invariant is consistency around the triangle of block
realizations. This is stronger than checking nonempty pair relations
or iterating arc consistency.

The exact theorem and hand proof are in [PROOF.md](PROOF.md); the full
partial matrix, individual degrees and six selected five-sets are in
[fixture.json](fixture.json).

## What is established

- For any proper-three-anchor visible skeleton, the individual-degree
  and complete \(K_5\) completion problem is exactly the triangle join
  of three block domains and their two-block relations.
- For binary domains with full pairwise projections, the only
  inconsistent networks are the four odd-parity triples of bijections.
  All \(343\) labeled networks are checked.
- The displayed literal Ramsey skeleton realizes the all-disequality
  case. All \(4096\) assignments of its twelve unknown pairs are
  checked directly. Exactly eight meet the prescribed degrees;
  none is Ramsey.
- Fifteen vertices are minimal **within this proper-three-anchor,
  fixed-individual-degree, arc-consistent block-relation framework**.
  Each of three nontrivial bipartite degree fibers needs at least
  four vertices, in addition to the three anchors.
- The six selected clique rows have six deletion witnesses when
  interpreted on the degree fibers. This is selected-certificate
  minimality, not minimum proof size or deletion-minimality of the
  full ten active rows.

Without the degree requirements, the partial matrix has 648 Ramsey
completions, including the all-red assignment of the unknown pairs.
Thus the degree/clique composition is essential.

This is an exact separation and conditional obstruction template, **not**
a 43-vertex coloring, an exclusion of any current 43-vertex profile,
or an improvement of a Ramsey bound. No instance of this binary face
is claimed inside the current H20 or \(c=13\) survivors.

## Reproduce

CPython 3.12.12, standard library only. From this directory:

~~~sh
set -o pipefail
python3 -B verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B test_verify.py | cmp - EXPECTED_CONTROLS.txt
python3 -B -O verify.py | cmp - EXPECTED_OUTPUT.json
python3 -B -O direct_check.py | cmp - EXPECTED_DIRECT.json
python3 -B -O test_verify.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
~~~

The primary checker compiles literal colored five-set clauses and
restricts them to complete bipartite margin fibers. The separate
checker imports no primary code: it constructs all 4096 full graphs,
finds their cliques recursively, and reconstructs the relation table
from the actual eight degree-valid graphs. It also checks the abstract
network table by matrix multiplication instead of assignment filtering.
Thirteen damaged-certificate controls pass.

The complete ten-row active-event table is present in both expected
outputs, not just its counts. Its SHA-256 is
29dbb7b877312c433e93df753cf09be4ffd46c63a23ab4bf9d82b4fb2bbed4a2.
The complete 343-row abstract table has SHA-256
7c4c88da209e2b0d25a59d198c75f6e7882945a394d475d7774426290300f12d.
Canonical hashes use compact JSON followed by one newline, with the
list order specified by the checkers. A relation entry \((a,b)\)
occupies bit \(a+2b\); masks \(9\) and \(6\) are equality and
disequality, respectively.

Fixture SHA-256:
3f1ef5ecc44668734fafd88bd79b27ecda41594c1aa3425fbf3dd2eb6552d5d8.

## Dependencies and scope of the integration

The mathematical interfaces composed are:

- [Helgi's proper-six-signature completion kernel](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_two_stratum_kernel),
  height 2937,
  bafkreidjm5bizbpa2reqlkvmp6aq2lus5mddc7abu2hto6rzurdvk7el3a,
  source commit 5367ce6ad2d32942da123b6c4f2c065742d15f60.
  Its complete visible preflight, complementary blocks and individual
  margin interface are preserved.
- [R2's complete mixed-cube interface](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits),
  height 2931,
  bafkreieffob5vhnmz5n4omjv7rrmqhfdbjrdhn3lz4tz3db3jijqyn5u7u,
  source commit 8d576378618dc348cf6cc53d0d226f7a70254d7f.
  Its visible gap is closed in this skeleton, so the obstruction lies
  in the remaining degree-constrained block gluing.

The kernel already states that degrees factor but Ramsey clauses do not.
We do not claim that warning, the signature support classification,
ordinary switching, or relation composition as new. The contribution is
the exact relation-level criterion, its minimum-size Ramsey realization,
and a compact six-clause odd-cycle certificate.

The previous [repair LP barrier](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_cube_creation_lp_barrier)
at height 2995 is separate and remains valid. The present result is
integral and uses complete degree fibers, not another fractional
objective or a larger clause prefix.

R1's \(c=13\) incidence/triple search, R2's fixed-core profile widening,
and Helgi's H20 footprint selection and fixed-seed integer search are
not repeated. Their current specific survivor families are not excluded.

## Trust, prior literature and next test

Arc and path consistency are classical:
Mackworth, [*Consistency in Networks of Relations*](https://www.cs.ubc.ca/~mack/Publications/AI77.pdf),
especially Sections 3–4. No historical-priority claim is made for the
abstract odd-cycle obstruction or a new general CSP algorithm.
Primary Ramsey context remains Angeltveit and McKay,
[*R(5,5) ≤ 46*](https://arxiv.org/abs/2409.15709).

A small PySAT 1.9.dev15 / Glucose 4.2.1 synthesis found the fixture.
Its verdict, encoding and search history are not proof premises:
the supplied matrix is exhaustively checked directly without a solver.
There is no UNSAT-trace claim and no omitted proof artifact.

The proof remains unformalized. Trusted are its graph-to-relation and
minimality arguments, the exact Python implementations, runtime/hardware
and hashes for file identity. Both checkers are author-written
cross-validation, not independent peer review or a second-language check.

Stop after this obstruction template. The next falsifiable step,
after ownership review, is to identify an actual three-block binary
face in a current proper-signature 43-vertex interface and compute its
three exact pair relations. Odd composition yields a reusable face
exclusion; even composition supplies joint switch states. More small
fixtures without that transfer are not further progress.
