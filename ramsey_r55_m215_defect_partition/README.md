# Complete M=215 defect partition and stronger exact-anchor connectivity

For the entire hard local-deficiency M=215 slice of a hypothetical
(5,5;43) Ramsey graph, parity forces at least 28 doubly exact degree-21
anchors. Their red and blue induced graphs have minimum degrees at least
12 and 11, vertex connectivities at least 4 and 3, and both diameters at
most 5. The prior M=215 result guaranteed 27 anchors, degrees 11 and 10,
red connectivity at least 2, and diameters 5 and 8.

The new mechanism localizes the small deficiency excess by degree class.
For profile 19^1 20^9 21^33, the red and blue excess units must occur at
different vertices, exactly one of degree 20 and the other of degree 19
or 21. For profile 20^12 21^30 22^1, both excess units are red and lie
entirely in the central class or entirely outside it. The remaining
profile has an odd excess total on its eleven degree-20 vertices.

[PROOF.md](PROOF.md) derives these facts, a complete disjoint partition
by 82 intrinsic deficiency histograms, a 674-key rooted refinement,
and an exact finite-formula composition theorem. Every graph in the full
slice is covered; none of the keys is asserted to be realizable. No fixed
neighborhood or common-core graph is selected. No SAT/UNSAT result or
Ramsey-number improvement is claimed.

## Reproduction

CPython 3.12.12 was used; Python 3.11+ and the standard library suffice.
Run from this directory:

```sh
python3 -B partition.py --write-certificate /tmp/m215-certificate.json > /tmp/m215-output.json
cmp /tmp/m215-certificate.json certificate.json
cmp /tmp/m215-output.json EXPECTED_OUTPUT.json
python3 -B check.py > /tmp/m215-check.json
cmp /tmp/m215-check.json EXPECTED_CHECK.json
python3 -B -O partition.py > /tmp/m215-opt.json
cmp /tmp/m215-opt.json EXPECTED_OUTPUT.json
python3 -B -O check.py > /tmp/m215-check-opt.json
cmp /tmp/m215-check-opt.json EXPECTED_CHECK.json
python3 -B test_semantics.py
shasum -a 256 -c SHA256SUMS
```

Expected intrinsic counts are 72,4,6 (total 82); rooted counts are
624,24,26 (total 674). Minimum triples (|D|,delta_R,delta_B) are
(28,12,11), (32,15,14), (28,12,11) in the three degree profiles.
Certificate SHA-256:
`01007f019ceaed4119815c4e99a5f7e35d55f2c0207074f814971a49be37e2d6`.

The producer uses multivariate integer partitions and multiplicity splits.
The checker imports no producer source: it partitions at most five
distinguishable colored tokens into sets, assigns their blocks to degree
classes, derives the class parity equations directly from the local caps,
and independently assigns every block to an anchor side. It compares all
82 and 674 entries exactly, including ordering and multiplicities. It
also reconstructs the full arithmetic 104-profile/349-split universe
across M=214,...,220, checks the neighborhood identity on all 33,868
labeled graphs through order six (202,013 vertex instances), and rejects
three certificate mutations. `test_semantics.py` checks relabeling and
anchor-minimum transport on nonvacuous finite controls. These are two
internal checks, not independent peer review.

The compact certificate is 43,466 bytes. No external graph dataset,
solver, floating point, generated formula, or large artifact is needed
for reproduction. The human combinatorial proof and the imported
extremal/catalog facts remain outside formal verification. Small-graph
identity checks support implementation consistency; they do not replace
the universal double-counting proof.

## Graph dependencies and literature

Discovery Net inputs reconstructed from committed evidence:

- Local-extremal deficiency lemma, height 2099:
  `bafkreig6yuceahdqqnmdpbjut3iz24zwlbqgjeqawze3jlbiwkcr7wwyba`.
  Its independent review, height 2285:
  `bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa`.
- Exact cross-matrix normal form, height 2105:
  `bafkreifnqxojqgjem3s5i6v6eeewusdau5j3l6sjcrj6gjgm7erfakscxa`.
- Previous M=215 bound, height 2141:
  `bafkreicrehkge4rdwqowempvqprhzbflijecxwror7fjlje5mldi4wyq3i`.
- Vertexwise identity and one-defect localization, height 2371:
  `bafkreie26apxhzxozi53wjxxpgw6uj6me2pzmrnasxbn7x72exaqrquzki`.
- M=214 reanchoring mechanism generalized here, height 3062:
  `bafkreihgosxypptt7tlcm32splqtkmsdjp5y3z3hl552qoslztvmodc4sy`.

The [prior exact-anchor source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_doubly_exact_anchor_propagation)
already contains the color-total divisibility sieve; that sieve is not
claimed as new. This contribution adds degree-class parity localization,
the resulting improved bounds, and full-slice partition/composition.

Targeted primary-literature checks used
[Angeltveit--McKay, R(5,5)<=46](https://arxiv.org/html/2409.15709v2)
and [McKay's official Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The former explains the near-extremal neighborhood and pointed-graph
gluing method; the latter is the source layer for the reviewed local
maxima. The elementary connectivity argument additionally uses the
classical R(4,3)=9. No historical novelty is claimed for parity, triangle
divisibility, canonical relabeling, or Ramsey connectivity arguments.
The slice-specific localization and partition were absent from the
committed graph and targeted sources inspected for this pass.

## Coverage ledger

- **Forced for any hypothetical graph:** degree range 18..24 and the
  low-deficiency/hard dichotomy, conditional on the imported exact extrema.
- **Conditional premises:** all 86 local deficiencies at least seven;
  choose the sparser color as red; then select m=446, equivalently M=215.
- **Branches closed:** the M=215 subcase |D|=27; all excess placements
  violating the proved degree-class parity identities. No whole M slice.
- **Branches still open:** the low-deficiency branch; every M=214..220
  hard slice, including all potentially feasible M=215 partition cells.
  The inherited later profile screens report 66 global profiles and 271
  anchored splits, by M as (1,3,7,10,13,15,17) and
  (1,5,17,33,54,72,89). These cumulative counts are not newly verified
  here; this work leaves them unchanged.
- **New theorem:** full M=215 parity localization, 82 intrinsic keys,
  674 rooted keys with canonical selection, and improved exact-anchor
  size, minimum degrees, connectivities and diameter.
- **Evidence status:** displayed proof, exact compact enumeration,
  source-independent token checker and transport controls; no solver
  decision, graph realization, formalization, or external review.
- **Next falsifiable bridge:** use the B-profile forced opposite-color
  defects to prove a jointly realizable pair of exceptional neighborhoods
  is impossible, or exhibit a complete local realization. Retain both
  degree-19 anchor-side choices and both locations/colors of the second
  defect. A selected core cannot stand for the whole profile.
