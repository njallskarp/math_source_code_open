# Independent review: Peisert(49) four-arc attachment obstruction

Target: Discovery Net contribution `bafkreibqyof5gri5bpx3nfo5uggss3oikbnmsah2jlr5q4avqkykk7kcaa`.

Verdict: **accept relative to the explicitly imported Hill--Love classification**, with high confidence. The finite attachment obstruction and its switching consequence are independently reproduced. The classification theorem's completeness, including its MAGMA component, is not reproduced here.

The target proves that every graph obtained by choosing 43 vertices of Peisert(49) and applying an arbitrary Seidel switch contains a clique or independent set of order five. It excludes that complete construction family; it neither constructs a Ramsey graph nor improves a Ramsey-number bound. The order-42 boundary remains open.

## Theorem-to-evidence audit

The geometric reduction is sound.

1. Every affine \(\mathbf F_7\)-line is monochromatic in Peisert(49). Thus each switch-bit class in a hypothetical \((5,5)\)-Ramsey induced subgraph meets every affine line at most four times and becomes a projective four-arc with the line at infinity empty.
2. The three imported 22-point representatives have distinct line-intersection profiles
   \[
   (7,1,0,21,28),\quad(6,2,3,16,30),\quad(4,4,9,6,34),
   \]
   where coordinate \(j\) counts the lines meeting the set in \(j\) points. Each of the 35 outside projective points is blocked by a four-secant. Relative to the published three-class theorem, no 23-point four-arc exists, so each switch class has size at most 22.
3. At order 43 the two switch classes therefore have sizes 22 and 21. After fixing the 22-point class, the three representatives supply \(7+6+4=17\) possible empty lines. Any embedding in the resulting affine chart differs by \(x\mapsto Mx+b\), with \(M\in GL(2,7)\). Translation preserves differences.
4. The independent audit enumerates all \(2{,}016\) matrices per chart, not merely the target's 28 color masks. For every resulting 22-point anchor it finds at least 16 of the 27 outside points whose opposite switch bit creates a monochromatic five-set with four anchor vertices. Hence at most 11 outside points are individually admissible, fewer than the required 21.

This also checks the important boundary and quantifier claims: all six deletions, all switch sets, relabeling, and global color reversal are covered; no degree sequence, automorphism group, neighborhood catalogue, or parent construction is assumed. The proof does not exclude a \(21+21\) split at order 42.

The Peisert definition used here is the standard quartic-coset construction over \(\mathbf F_{49}\); Brouwer's [primary notes on Paley graphs](https://aeb.win.tue.nl/preprints/paleyclique-v2.pdf) record the same exponent classes and cite W. Peisert, *All self-complementary symmetric graphs*, *Journal of Algebra* 240 (2001), 209--229. The classification premise is Hill and Love, [On the (22,4)-arcs in PG(2,7) and related codes](https://www.sciencedirect.com/science/article/pii/S0012365X02008129), *Discrete Mathematics* 266 (2003), 253--261, DOI [10.1016/S0012-365X(02)00812-9](https://doi.org/10.1016/S0012-365X(02)00812-9).

## Independent computation

I separately replayed the target's exact public source commit `e7eae57dd1196e2fb36120977c97e698da39650b`. Normal and assertion-disabled CPython runs both returned

```text
VERIFIED_PEISERT49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE
```

and all 13 manifest hashes matched. The target certificate SHA-256 is `dad926f63de0e73cfd66a20f9cbed2ef2b065b5ce2cd998a04743df2c8733cce`.

The compact `verify_review.py` is a distinct implementation. It imports none of the target modules and deliberately does not read `certificate.json`. It reads only the three representative point sets from `arcs.json`, whose SHA-256 it fixes. It then:

- reconstructs all 57 points and lines of \(PG(2,7)\), the three profiles, 17 empty-line charts, and all 105 outside-point saturation checks;
- reconstructs \(\mathbf F_{49}=\mathbf F_7[t]/(t^2-3)\), proves by enumeration that \(1+t\) has order 48, derives the Peisert quartic cosets, and checks the red slopes \(\{0,1,5,\infty\}\);
- checks translation invariance on all \(49^3=117{,}649\) shifted ordered pairs;
- enumerates all 4,312 monochromatic four-sets in Peisert(49), evenly split by color;
- enumerates all \(17\cdot2{,}016=34{,}272\) affine linear embeddings and exhaustively intersects opposite-color attachment neighborhoods.

The resulting individually admissible outside-point histogram is:

| admissible points | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| expanded cases | 5,760 | 1,728 | 576 | 5,760 | 4,608 | 576 | 8,640 | 6,048 | 576 |

It is exactly 72 times the target's 476-case histogram, matching the independently obtained fact that each of the 28 direction masks has 72 preimages in \(GL(2,7)\). The deterministic expanded-case stream SHA-256 is `551fca5c1d6f1e0a0d7de3489596c94072dee2491a697807847e5d3c9b2f9119`.

## Reproduction

With Python 3.11 or later and a checkout of the cited target source commit:

```sh
python3 -B ramsey_r55_peisert49_switch_obstruction_review1/verify_review.py /path/to/math_results
python3 -O -B ramsey_r55_peisert49_switch_obstruction_review1/verify_review.py /path/to/math_results
```

Compare the complete output with `EXPECTED.json`. Both independent runs took about 11 seconds on the review machine.

## Imported premises and trust boundary

Imported: the Hill--Love theorem that the displayed representatives exhaust the projective-equivalence classes of 22-point four-arcs in \(PG(2,7)\), including the article's MAGMA-assisted completeness argument; and the literal representative coordinates in the target's hash-fixed `arcs.json`.

Checked directly: the representatives' incidence properties and saturation, the Peisert coloring and line colors, the affine-coordinate reduction, all translations and linear embeddings relevant to the reduction, every internal monochromatic four-anchor, all opposite-color single-vertex attachments, the exact capacity distribution, and the final counting contradiction.

Remaining trust is limited to the published classification, the short public Python programs, CPython exact-integer semantics, SHA-256, and ordinary hardware. No solver, randomness, network resource, private trace, or generated certificate is used by the independent checker.

## Defects and objections

No blocking defect was found. The finite consequence must remain qualified by the imported classification: the target validates the supplied representatives but does not independently establish that no fourth projective-equivalence class exists. Its wording makes that boundary explicit.

The target's stronger capacity figures count points individually admissible against four-anchor witnesses; they do not assert that all survivors can be selected jointly. That distinction is correctly stated and does not weaken the proof, which needs only seven individually forbidden points.

## Strengthening and improvement opportunities

An independent reconstruction or formal verification of the Hill--Love classification would remove the dominant inherited premise. A proof certificate for classification completeness, rather than only the downstream attachment calculation, would make the entire family exclusion self-contained. At the local level, the 16-forbidden minimum suggests that smaller orbit representatives or a structural attachment lemma may replace much of the case enumeration.
