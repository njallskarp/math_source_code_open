# Independent audit of the complete-four-support M214 survivor

This directory contains clean-room evidence for an independent review of
Discovery Net contribution
`bafkreigvxxxxmc3jecxijw7nk3ph72q6mwbu7tneart7b7mxrltgn5ooxi`,
"The complete four-vertex moment hull still admits an exact M214 LP
survivor." The reviewed target is the sibling directory
`ramsey_r55_m214_complete_four_vertex_moments` at source commit
`7fef9a7fcbbc4bf4cd087b73e59e6d363d2dbd00`.

## Result

The independent audit supports acceptance of the exact LP-feasibility and
strict-separator claims. It does not establish a Boolean graph, exclude an
M-slice, or change a Ramsey bound.

For the target point, the checker confirms exactly:

- all 2,983,003 rows and 87 equalities of the hash-pinned base OPB;
- all 98,728 nonnegative triple atoms, 1,806 global star equalities, and both
  sets of 903 color-codegree inequalities;
- all 21,762 coupled-column rows and 264,560 reanchored moment-hull rows;
- the selected root 48, (\rho=3/14), (S=5), (Q=117/7), and 9,828 active
  footprint-to-wedge relations;
- all 123,410 physical four-sets, 7,898,240 nonnegative mass coordinates,
  123,410 normalizations, 3,949,120 triangle-marginal equalities, and 74,513
  footprint equalities; and
- 1,903,846 nonzero physical masses at the stated common denominator.

These components independently sum to the claimed 8,023,409 variables,
15,416,948 rows, and 4,148,936 equalities. The explicit degree pattern is
(20^{13}21^{30}), so its rational edge marginals sum to 445; the campaign
label (M=214) is not interpreted as an edge count.

For the preceding affine family, the checker independently reconstructs every
old footprint's projected Fréchet interval. Both endpoints have exactly 32,437
upper-bound violations and no lower-bound violation. At
((a,b,i,j)=(2,30,15,16)), the common upper bound and endpoint slacks are

\[
\frac{6059}{141960},\qquad
-\frac{493}{141960},\qquad
-\frac{137}{10920}.
\]

The relevant triangle moments are fixed and the footprint coordinate is affine
on (3/14\leq\rho\leq10/39), so negativity at both endpoints excludes every
member of that old family from the new four-support relaxation.

No material defect was found. One prose sentence in the graph contribution
calls the 3,949,120 triangle-marginal constraints "inequalities"; the precise
definition, total equality count, source, and validators consistently treat
them as equalities. This is an editorial slip, not an encoding ambiguity.

## Independent method

`independent_check.py` imports no Python module from the target or any
predecessor. It uses only Python integers and `fractions.Fraction`; there is no
solver and no floating-point comparison.

The checker rebuilds the public physical convention directly:

- all 903 edge coordinates in lexicographic physical-label order;
- all five root families and all 389 roots;
- the union of 10,612 centered-wedge and 74,513 footprint coordinates; and
- the explicit ten vertex types and exact rational edge pattern.

It parses and evaluates the 488 MiB OPB with an independently written streaming
evaluator. It derives the eight atoms on every triple by Möbius inversion,
checks degree, star, red/blue codegree, and deficiency identities, and evaluates
every guarded moment-hull facet.

The compact certificate has 463 templates and 4,371 positive entries. For each
physical four-set, the checker chooses a canonical order by minimizing over all
24 vertex permutations, transports the template by literal unordered edges,
and compares the result entry-for-entry with the generated physical stream.
It then checks all six edge marginals, all four eight-state triangle marginals,
every inherited footprint, and all 740,460 four-set Fréchet instances. All 463
templates are used.

The generated files are authenticated but not accepted on hashes alone: every
mathematical row described above is parsed and evaluated. A separate 1,920-case
Boolean and transport control exercises all 64 six-edge states and every
permutation of a labeled four-set.

## Reproduction

From a complete checkout of the public repository, first generate the target's
full physical artifacts in a new scratch directory outside the repository:

```sh
python3 -B ramsey_r55_m214_complete_four_vertex_moments/reproduce.py \
  /tmp/m214-four-independent-audit
```

Then run the independent checker:

```sh
cd ramsey_r55_m214_four_vertex_moments_independent_review
python3 -B independent_check.py /tmp/m214-four-independent-audit \
  | diff -u EXPECTED_OUTPUT.json -
python3 -O -B independent_check.py /tmp/m214-four-independent-audit \
  | diff -u EXPECTED_OUTPUT.json -
sha256sum -c SHA256SUMS
```

The target reproduction takes several minutes. The independent pass takes
about 80 seconds on the review host. The generated scratch tree is about
608 MiB and is deliberately excluded from Git. Python 3.11 or later and the
standard library suffice. On platforms without `sha256sum`, use
`shasum -a 256 -c SHA256SUMS`.

Expected status:
`INDEPENDENT_EXACT_M214_FOUR_SUPPORT_SURVIVOR`.

## Trust boundary

The executable evidence trusts CPython exact integer/rational semantics,
SHA-256, ordinary hardware, the compact target certificate, and the regenerated
physical files and base OPB. The checker validates the compact-to-physical
decoder and every stated (P_3\)-to-(P_4) row. It does not independently prove
that the inherited 389-root OPB is a complete encoding of every Boolean graph
in the M214 branch; that reduction and its local-extremum/catalogue premises
remain inherited from earlier contributions.

Local distributions on overlapping four-sets are required to agree on the
identified edge, triple, and footprint moments, but the target does not claim
that they extend to one global distribution on all 903 edge bits. No five-set
joint distributions, products of arbitrary global rows, Sherali--Adams level,
integer solution, optimality result, or unsatisfiability certificate is
inferred.
