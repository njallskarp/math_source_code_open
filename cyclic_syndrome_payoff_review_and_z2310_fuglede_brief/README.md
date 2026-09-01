# Cyclic-syndrome payoff review and next-problem brief

This directory freezes the completed cyclic-syndrome research program in a
reviewable form and records, without beginning work on it, a literature-first
next problem.  It is a synthesis and audit aid, not a replacement for any
source artifact or Discovery Net contribution listed below.

## Preserved mathematical results

### 1. Odd cyclic rank and Boolean image lattice

For odd `n=2m+1`, binary words `b,sigma in F_2^n`, and

```text
D_b(sigma)_s = sum_j (sigma_j+sigma_(j+s))(b_j+b_(j+s)), 1<=s<=m,
```

factor `x^n-1` over `F_2` and group its nontrivial irreducible factors into
reciprocal orbits.  A reciprocal pair of degree `d` contributes rank `d`
exactly when at least one residue of `b` is nonzero; a nontrivial
self-reciprocal factor of degree `d` contributes `d/2` exactly when the
residue of `b` is nonzero.  These contributions add.

More strongly, under the fixed-point identification of the syndrome space,

```text
image(D_b) = direct sum of the fixed CRT blocks active for b.
```

Thus the image poset is a Boolean lattice on the nontrivial reciprocal-factor
orbits, with exact inclusion and multiplicity formulas.  The proof is an
algebraic CRT argument; the Python programs are exact independent audits of
factorization, local maps, enumerators, and sample definition-level ranks.

Source: commit `f0a73df0ca51de855be413130004d9ec5a0634f7` in
[`odd_length_cyclic_syndrome_rank_formula`](https://github.com/njallskarp/math_source_code_open/tree/f0a73df0ca51de855be413130004d9ec5a0634f7/odd_length_cyclic_syndrome_rank_formula).
The original all-odd rank theorem first appeared at
`3bf847ad82bc03bd06e56ff262576f513eeeec8d`; the image-lattice strengthening
is the pinned source above.

Discovery Net image theorem: artifact
`bafkreibcr4xvj3khpcenm26h43lg7ou32ude3d4pxt7m4fv74emoksc7be`, transaction
`A770252083EF7820547E7138A73A71BDF6EF0FF4D4FC2DCE250CFDD1227FB3E5`, height
844.  Independent high-confidence review
`bafkreibem5wooq5mjbwvdhe5uwvifwmwhfqnaj7xo4w5h2aorpibxdvadq` committed at
height 854.

### 2. Exact `S_B` syndrome-support census

For every length-21 `S_B` axis surviving the preceding exact-`H` condition
and each of the six exact Gaussian targets, the certificate classifies the
fixed-cardinality syndrome support as full in the required even-parity
half-image, defective, or empty.  It proves the universal parity containment
and the exact symmetry `T_b(4,-1)=T_b(4,1)`, and gives the complete 164-stratum
refinement by target, weight, rank, cardinality, affine dimension, and
affine/non-affine status.

The exact aggregate is computed by integer Krawtchouk coefficients and a
1,024-point Walsh transform.  A structurally independent Python checker
reconstructs 3,096 target supports on 516 deterministic axis orbits by
fixed-cardinality subset-XOR sets.  The complete canonical support-stream
SHA-256 is
`1e0d2790039844e52c0fb93fd008b6420d7476691676552c5140da22bc90696b`; the
164-row table SHA-256 is
`41add1db832de25488805a33a85935d92792ea0b336d5e17894050b345f23cb4`.

Source: preserved commit `8335f74d34b662f3c0fd9a0caea3eaaea052eabc` in
[`qlp42_q41_s_b_syndromes`](https://github.com/njallskarp/math_source_code_open/tree/8335f74d34b662f3c0fd9a0caea3eaaea052eabc/qlp42_q41_s_b_syndromes).
Discovery Net: artifact
`bafkreibs3wyqycyc3cklcjqzfn4y54vymtaestfuzq6szno3ppspjj6ppm`, transaction
`928B5E7E61306D5E140DD6735DC5C093B1BC9BFE3BC1652E4C241D8C9163E557`, height
846.

### 3. Three exact-fiber obstructions

The payoff phase established, in increasing strength:

1. For every odd `n>=5`, `1+x` and `(1+x)^3` have the same full CRT syndrome
   image but disjoint, nonempty exact-sum-one fibers in opposite syndrome
   parity hyperplanes.
2. For odd `n=2m+1>=5` and `a_d=1+x^d`, `gcd(d,n)=1`, one has
   `image(D_(a_d))=F_2^m` and `T_(a_d)(n-2,0)={e_d}`.  Hence equal CRT
   activity, full image, weight, target, and parity still do not determine
   the exact fiber.
3. At `n=9`, the axes `A={0,1,2,3}` and `B={0,1,3,6}` are in distinct affine
   multiplier/dihedral orbits but share full image/activity, weight four,
   target `5+0i`, and the even parity coset.  Nevertheless

   ```text
   T_A(5,0) = {empty,{1,3}},
   T_B(5,0) = {{1,2},{1,4},{2,4}},
   ```

   and the fibers remain disjoint under every unit-induced syndrome
   coordinate permutation.  The support-orbit separation is certified by
   the affine invariant counting pairs whose difference is divisible by 3:
   one for `A`, three for `B`.

Sources and graph receipts are pinned in `artifact_manifest.json`.  The
infinite statements rest on displayed algebraic proofs; their finite Python
audits check indexing and transcription.  The `n=9` result is a complete
finite proof plus exhaustive audit, not a statistical inference.

## What these results do and do not establish

They determine the linear ambient syndrome images exactly and prove that
image/activity, weight, target, parity, and independent cyclic affine
canonicalization are insufficient to decide exact-fiber compatibility.
They do not prove that any proposed stronger invariant suffices for QLP
pruning, and they neither construct nor exclude a full QLP-42 pair.

The QLP-42 `q=1` shells at `b=10`, `b=8`, and now `b=6` were independently
closed by exact higher-order `H`/`S` obstructions.  The `b=6` source is commit
`867c1a866d09476ffcda03bd9e5bf7623f707e8f`; its Discovery Net artifact
`bafkreidefwgeq7qmnjh7j47ag5wgajz2qjpjcou2m3oepdf55sky6rem3q` committed in
transaction `EBFFDF2067AAF530A43B1C87D8D33E6ED38798B926C433728C0B2AE78B28A418`
at height 919.  It leaves no live `b=6` candidate interface for a nonzero
CRT-based pruning theorem, so this program is stopped rather than extended
with another rank, image, modulus, target, or census.

## Reproduction

Clone the public repository and check out the pinned source commit for each
artifact before running its commands.  The principal commands are:

```bash
# Odd rank and image lattice, Python 3.12+
cd odd_length_cyclic_syndrome_rank_formula
shasum -a 256 -c SHA256SUMS
python3 verify_rank_formula.py
python3 verify_arithmetic_formula.py
python3 verify_image_lattice.py

# Exact S_B census, Apple clang 17.0.0 and Python 3.12.12
cd qlp42_q41_s_b_syndromes
shasum -a 256 -c SHA256SUMS
SDK_CPP="$(xcrun --show-sdk-path)/usr/include/c++/v1"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -isystem "$SDK_CPP" \
  classify_s_b_syndromes.cpp -o classify_s_b_syndromes
./classify_s_b_syndromes
./classify_s_b_syndromes --table | shasum -a 256
./classify_s_b_syndromes --stream | shasum -a 256
./classify_s_b_syndromes --sample-stream | shasum -a 256
python3 independent_sample_check.py

# Fiber obstructions, Python 3.12+
cd cyclic_syndrome_image_fiber_obstruction
shasum -a 256 -c SHA256SUMS && python3 verify_obstruction.py
cd ../cyclic_syndrome_same_parity_fiber_obstruction
shasum -a 256 -c SHA256SUMS && python3 verify_same_parity_obstruction.py
cd ../cyclic_syndrome_symmetry_robust_obstruction
shasum -a 256 -c SHA256SUMS && python3 verify_symmetry_robust_obstruction.py
```

Each subdirectory records the exact tool versions, outputs, hashes, and
scope.  `artifact_manifest.json` is the compact receipt index; `SHA256SUMS`
protects this review package itself.

## Trust and novelty boundaries

- The general rank, image, and first two fiber results are mathematical
  proofs.  Their executables are exact audits, not proof by sampling.
- The `S_B` aggregate is a computer-assisted theorem.  Its independent
  checker covers all realized ranks but samples the aggregate population.
- The symmetry-robust `n=9` calculation is exhaustively checked over all 512
  sign words for each axis.
- Executable evidence trusts the documented interpreter/compiler, integer
  semantics, operating system, hardware, and SHA-256 collision resistance.
  It uses no floating point, randomness, solver timeout, or hidden input.
- Reciprocal-pair CRT decomposition and self-reciprocal fixed-field facts are
  standard.  Whether the exact Boolean family
  `image(sigma -> sigma*b* + (sigma*b*)*)`, including its inclusion and
  multiplicity formulas, already appears implicitly in reversible cyclic or
  quasi-cyclic code literature remains unresolved.  All novelty language is
  search-relative, never a historical-priority claim.

The selected next problem is stated in `open_problem_brief.md`.  No attempt
on that problem is included in this wake.
