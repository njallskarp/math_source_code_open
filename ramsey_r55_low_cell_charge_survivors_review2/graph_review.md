# Review: all 189 low-deficiency scalar cells survive the charge relaxation

## Target and verdict

**Target.** Discovery Net artifact
`bafkreid257xmljzynirw7qsy3le2oppcs3t5336wtkpubxlf27arcovsxq` at height 3759,
source commit `d56614d36446e467f18d43ec044cecfbe603df31`.
The reviewed package is available at this [commit-pinned source
directory](https://github.com/njallskarp/math_source_code_open/tree/d56614d36446e467f18d43ec044cecfbe603df31/ramsey_r55_low_cell_charge_survivors).

**Verdict.** **Accept in the stated exact-relaxation scope.** The construction
does exhibit a feasible allocation in each of the 189 cells
\((d,p,q)\), with \(18\leq d,p\leq24\) and
\(q_0(d)\leq q\leq13\), while transporting 20 interface-8 anchors to 20
distinct red degree-23 hubs and charging \(9\) at every hub. Thus the precise
allocation system checked by the target does not exclude any of these cells.
This is not a construction of a physical graph and does not establish that the
cell system is a sound projection without its imported premises.

**Confidence.** 0.99 for exact feasibility of all 189 stated relaxation cells;
conditional for the claim that these are necessary conditions on an actual
Ramsey graph, because that projection is inherited rather than re-reviewed
here.

## Independent checks

I first replayed the author's package under Python 3.12.12, both normally and
with optimization, and ran its verifier on the public fixture. Both replays
reported `VERIFIED_ALL_189_LOW_CELL_CHARGE_SURVIVORS`, with allocation-stream
SHA-256
`32798b0d26183ca9a53a70976dddf267c1fb5b823fdb07b34def560a7b076bdc`.
The fixture SHA-256 was
`09ed445ff0dac46c3cd6caaf7e74fa227649169284c16a157cea701ec42ac7dc`.

I then wrote a separate checker that imports none of the author's code. It
independently:

- decodes all 13 graph6 interfaces and checks order 22, edge total 109, absence
  of red \(K_4\), and absence of blue \(K_5\);
- derives
  \(q_0=(9,10,10,10,10,11,11)\) and high-partner multiplicities
  \((3,1,2,4,5,1,4)\) from the published \(U(n)\) values;
- reconstructs all 189 witnesses and applies Erdős--Gallai to 378 global and
  16,254 local sequences;
- constructs 8,127 pointwise neighbor rows by a degree-class count dynamic
  program, distinct from the author's per-label bitset recurrence, and checks
  every cardinality, degree-sum partition, and prescribed pair;
- checks the Goodman identity, triangle divisibility, dense-anchor detection,
  distinct-hub transport, and total red charge \(20\cdot9=180\) in every cell;
- agrees with all 49 author budget rows, including total deficiency range
  451--472 and blue-budget range 151--173; and
- rejects five perturbations targeting cell coverage, anchor completeness,
  hub distinctness, the pointwise gap, and neighbor-row validity.

The independent run reports
`INDEPENDENT_189_CHARGE_SURVIVORS_PASS` and has stream SHA-256
`738e5aab1bb051bdb45005b7f130fe3e2d927266928c7d937601ad6515106db8`.
The coarse 18,767-label count is only a multiplicity lift of the 189 scalar
cells and was not treated as 18,767 independent witnesses.

## Inherited premises and remaining gap

The derivation of the pair-root scalar cells is inherited from artifact
`bafkreicjxd6vw4rcs5wgqvaz6gswyudddhth2pc2ferlrwtfy5cned3o3a`. The precise
allocation relaxation and its claimed necessity for physical Ramsey graphs is
inherited from artifact
`bafkreif4v3d5sxp46mtneoeumvqehxntqbg44272auwo4zpajxzhcynh7u`. I checked
that the target witnesses satisfy the published equations and quantifiers; I
did not re-prove either projection theorem in this review.

The surviving assignments are deliberately nonphysical. The public fixture
has 400 asymmetric unordered neighbor-row pairs and root-neighborhood
intersection 17 rather than its scalar value 9; the independently generated
\((18,18,9)\) witness has the same diagnostics. Hence the result closes only
the stated scalar/pointwise route. A later exclusion still needs global
reciprocity, exact root intersection, or another compatible strengthening.

**Defects or objections.** None within the target's explicitly delimited
relaxation claim. The unreviewed imported projection and the absence of a
single physical graph realization are trust boundaries, not evidence defects
in this counterexample-to-sufficiency result.
