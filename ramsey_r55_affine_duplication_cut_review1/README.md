# Independent review: zero-free affine-duplication cut family

This directory contains reviewer-written evidence for the claim that no
43-vertex red/blue coloring without a monochromatic $K_5$ has the following
fixed $20+23$ cut:

- each side contains all 15 nonzero vectors of $\mathbb F_2^4$;
- five distinct row types are doubled;
- the eight column types in one affine hyperplane are doubled; and
- each cross color is the binary dot product of its row and column types.

All 443 within-side edges remain arbitrary.  The result is a complete
exclusion of this declared finite family, not a decision of every rank-four
cut, a construction of a good graph on 43 vertices, or an improved Ramsey
bound.

The checker imports no module from the reviewed package.  It enumerates all
$2^{16}$ binary $4\times4$ matrices to recover
$|\operatorname{GL}(4,2)|=20{,}160$ and the 1,344-element hyperplane
stabilizer.  It independently checks the 16 orbits of the 3,003 doubled-row
sets, every transported dot-product contact, all 96,096 doubled-pair color
assignments, every cut-rank profile, and the exact physical-family count.

It then reads a fresh public replay.  For each of the 32 branches it rebuilds
the physical 23-side projection from the mathematical definitions, checks the
entire physical clause set, truth-tables every auxiliary threshold gate,
checks the two degree units for every vertex, and matches the newly generated
CNF and proof bytes to the published identities.  The public replay itself
executes pinned `drat-trim` on every newly generated DRAT proof; saved UNSAT
statuses are not accepted.

## Reproduction

Fetch the target at its reviewed commit:

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout a960dc16a0377c12e93d1ed5afd6da92fe10b833
```

From `target/ramsey_r55_affine_duplication_cut`, run the target's documented
public replay on Debian amd64 with CPython 3.11:

```sh
python3 -B bootstrap.py /tmp/r55-affine-tools
python3 -B reproduce.py /tmp/r55-affine-replay \
  --cadical /tmp/r55-affine-tools/cadical/usr/bin/cadical \
  --drat-trim /tmp/r55-affine-tools/drat-trim/usr/bin/drat-trim
```

Clone the public reviewer repository beside `target`, then run the independent
checker from their common parent (CPython 3.12 or later):

```sh
git clone https://github.com/njallskarp/math_source_code_open.git review
python3 -B review/ramsey_r55_affine_duplication_cut_review1/independent_check.py \
  target/ramsey_r55_affine_duplication_cut \
  /tmp/r55-affine-replay
python3 -O -B review/ramsey_r55_affine_duplication_cut_review1/independent_check.py \
  target/ramsey_r55_affine_duplication_cut \
  /tmp/r55-affine-replay
```

Both reviewer runs report
`INDEPENDENT_AFFINE_DUPLICATION_CUT_REVIEW_ACCEPTED` and deterministic
evidence SHA-256

```text
5444d81f6f7984414101944973075c4b08f068b9847f097e24f04089a0285c56
```

The checker SHA-256 is

```text
9d3dc6b589ee4c884ede3a37c9a1e6f0eaaeb3ee53045fadd5aa76af9914eba2
```

The review replay used the `python:3.11-bookworm` linux/amd64 image with image
digest `sha256:35d3a4a3d5e42e02ab916d44513a050689f12c0533d45598d229672503fe77ca`.
It regenerated 111,618,212 CNF bytes and 188,371,117 proof bytes in 273.463
seconds; all 32 proofs checked.  The reviewer audit covered 3,149,477 clauses,
161,328 gates, and 2,370,368 gate truth assignments.  Those bulky generated
files are deliberately not published.

## Scope and trust boundary

Checked independently: family normalization, stabilizer and dual actions,
orbit coverage, pair-color completeness, red/complement cut ranks, absence of
zero types, physical-family count, all 32 projected formulas, all threshold
semantics, source and replay identities, and branch/proof coverage.  The
definition-level searches actively fail on any surviving unclassified color
assignment, orbit overlap, missing physical clause, malformed gate, or stale
proof identity.

Imported rather than re-established here: McKay and Radziszowski's theorem
$R(4,5)=25$, standard DRAT soundness, the reviewed source bytes at the pinned
commit, CPython and pinned C-checker semantics, Docker's amd64 emulation,
SHA-256, and ordinary hardware.  The author-hosted primary source explicitly
states and proves $R(4,5)=25$:
https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf.

The remaining gap is the rest of the zero-free rank-four cut family: different
duplication patterns, higher-rank cuts, and unrestricted good43 existence are
not decided.
