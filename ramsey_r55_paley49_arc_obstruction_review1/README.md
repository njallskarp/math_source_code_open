# Independent review: Paley(49) switching-family obstruction

Targets:

- imported classification node `bafkreicxhkf2dmw6olzioypy4qubctodu4u4aoyluxe5p6kq6fhpftvnoe`;
- switching consequence `bafkreigbtza7cclrgw7ylpkxy2bbgdgmy64fbas66uhni6o34tx4la3keq`.

Verdict: **accept the switching consequence relative to the explicitly imported Hill–Love classification**, with high confidence. The classification node accurately records a published theorem; this review does not reproduce its MAGMA completeness computation.

The result proves that every induced 43-vertex subgraph of Paley(49), after any Seidel switch, contains a clique or independent set of order five. It excludes this complete construction family but neither improves \(R(5,5)\) nor claims that the order-42 bound is sharp.

## Theorem-to-evidence audit

Hill and Love state that there are exactly three projective-equivalence classes of \((22,4)_7\)-arcs in \(PG(2,7)\). Their no-two-secant case is handled geometrically and the remaining two classes use exhaustive MAGMA computation. The article is [On the (22,4)-arcs in PG(2,7) and related codes](https://www.sciencedirect.com/science/article/pii/S0012365X02008129), *Discrete Mathematics* 266 (2003), 253–261, DOI [10.1016/S0012-365X(02)00812-9](https://doi.org/10.1016/S0012-365X(02)00812-9).

The downstream reduction is sound:

1. Every affine \(\mathbf F_7\)-line is monochromatic in Paley(49), because every nonzero scalar in \(\mathbf F_7\) is a square in \(\mathbf F_{49}\). Hence a monochromatic-\(K_5\)-free 22-point set is a projective four-arc whose line at infinity is empty.
2. The three literal representatives have distinct line-intersection profiles and respectively 7, 6, and 4 empty lines. The published three-class theorem therefore makes this a complete representative list.
3. For a fixed empty line, every projective embedding into the affine chart differs from a canonical chart by an affine map. Translation preserves differences; the linear part ranges over all \(2{,}016\) matrices in \(GL(2,7)\).
4. Every one of the resulting \(17\cdot2{,}016=34{,}272\) linear images contains a monochromatic five-set.
5. A switch partitions any 43 selected vertices into two switch-bit classes, one of size at least 22. Edges inside that class are unchanged, so the 22-point obstruction survives the switch.

Boundary cases are stated correctly: a \(21+21\) split at order 42 is not excluded, arbitrary vertex labels and global color reversal preserve the property, and no degree profile, automorphism, neighborhood, or catalogue completeness is assumed.

## Independent computation

I replayed the cited public package at source commit `3699fda9b6c67adb2b0f1266c735271033201e79`. Normal and assertion-disabled CPython 3.12.12 both returned:

```text
VERIFIED_PALEY49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE
```

The target replay checked all 714 normalized cases and 7,140 witness pairs.

The separate `verify_review.py` imports none of the target modules and ignores all 714 target witnesses. It:

- reconstructs \(PG(2,7)\), the three literal arcs, all 57 lines, and their three secant profiles;
- chooses affine chart coordinates through an independent rank test;
- enumerates every matrix in \(GL(2,7)\), avoiding the target's quotient to 42 normalized maps;
- checks translation invariance on all \(49^3=117{,}649\) translated ordered field-pair instances;
- constructs all 34,272 images and searches each one directly for a red or blue \(K_5\).

The independent run completed in 14.62 seconds. It found 480 blue-first and 33,792 red-first witnesses. Its deterministic witness-stream SHA-256 is `6cff1310892dcea121505536e0fb9d947ea2f82a8e0178c18fbf1725999455d2`. The input certificate SHA-256 is `ffa55fc61f4fb2733dbb492b32d7acf3f4aaa4a7da6392c72eb7a9811b33f594`.

## Reproduction

With Python 3.11 or later, use a checkout of `helgithorskarp/math_results` containing the cited certificate:

```sh
python3 -B ramsey_r55_paley49_arc_obstruction_review1/verify_review.py /path/to/math_results
```

Compare the complete output with `EXPECTED.json`.

## Imported premises and trust boundary

Imported: completeness of the Hill–Love three-class theorem, including its MAGMA component. Checked directly: the literal representatives, all incidence profiles and empty lines, every affine linear embedding after removing translations, every physical Paley color used by the independent witnesses, and the switching implication.

The remaining trust is in the published classification, the short public Python implementations, CPython integer semantics, and ordinary hardware. The independent computation uses exact arithmetic and no solver, package, network access, randomness, or omitted generated artifact.

## Defects and objections

No blocking defect was found. The classification contribution must continue to be described as an imported published premise rather than as an independently reproduced enumeration; both target reports do so accurately.

## Strengthening and improvement opportunities

Reproducing or formally verifying the Hill–Love MAGMA classification would remove the dominant inherited trust boundary. A structural proof that avoids the 22-point arc classification would be stronger still.
