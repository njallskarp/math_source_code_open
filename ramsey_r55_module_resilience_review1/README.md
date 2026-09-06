# Independent review: deletion-stable module resilience in Ramsey(5,5;43)

Target: Discovery Net contribution `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`.

Target source: [public package](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_module_resilience), verified at commit `823d258fe6dfa33a695e148bbed08b1709fbe3c9`.

Verdict: **accept, with one strict construction-family strengthening**, at high confidence relative to the explicitly imported small Ramsey bounds. If \(G\) is a 43-vertex graph with neither a clique nor an independent set of order five, then every induced subgraph of order at least 36 is prime, and every induced subgraph of order at least 28 has no proper module of order at least three. In addition, the target's own triple-sum argument proves that deleting at most 16 vertices cannot create a module of order exactly five; its public extractor presently exposes that subfamily only through 15 deletions.

These are conditional structural restrictions on a hypothetical Ramsey graph. They do not establish that such a graph exists, force a module into one, or improve a Ramsey-number bound.

## Theorem-to-evidence audit

The imported equality \(R(4,5)=25\) gives the degree window \(18\le d_c(v)\le24\) in either color. The bounds \(R(3,5)\le14\) and \(R(2,5)=5\) give same-color common-neighborhood caps 13 for an edge and 4 for a triangle. Substitution into the exact signature counts gives at least 8 distinguishers for every pair, 18 for every monochromatic triple, and 17 for every mixed triple. I checked the pair identity on all four contact signatures and the mixed-triple identity on all eight.

For a module \(M\) of an induced core \(H\), write \(k=\omega(H[M])\), \(\ell=\alpha(H[M])\), and partition \(H-M=A\sqcup B\) by its uniform contact color. Then

\[
|A|\le c(k),\qquad |B|\le c(\ell),\qquad
|M|\le R(k+1,\ell+1)-1,
\]

where \((c(1),c(2),c(3),c(4))=(24,13,4,0)\). Independently enumerating every ordered \((k,\ell)\) case reproduces the target's eight-row table. A module of order at least three therefore forces \(|H|\le31\), while one of order at least six forces \(|H|\le28\).

For at most seven deletions, a two-vertex module has at most seven distinguishers, contradicting the pair minimum eight; a larger module would require \(|H|\le31<36\). This proves primeness.

For at most fifteen deletions, I exhaustively enumerated all 8, 64, and 1,024 internal two-colorings of modules of orders 3, 4, and 5. For every triple, its required lower bound is 17 or 18 according to its physical internal coloring. Internal module vertices and arbitrary deleted vertices were then maximized independently over every possible contact signature. The worst contradiction margins are respectively 1 at order 3 with 16 deletions, 4 at order 4 with 15 deletions, and 6 at order 5 with 16 deletions.

This last margin gives the strict strengthening:

\[
|M|=5\quad\Longrightarrow\quad |T|\ge17.
\]

The target states this inequality in its proof, but neither its headline family nor `extract.py` accepts the \(|M|=5,|T|=16\) case. Extending the family predicate by that case is mathematically justified.

For \(|M|\ge6\), exhaustive integer enumeration of all capacity-compatible parameters with \(|H|\ge28\) leaves exactly two color-reversed rows:

\[
(|T|,|M|,|A|,|B|,k,\ell)=(15,24,4,0,3,4)
\]

and its color reversal. Each of the four uniform vertices already has 24 same-color neighbors in \(M\); the degree cap forces all its remaining contacts to the other color. Any one of the 15 deleted vertices then completes a monochromatic five-set. Thus the delicate equality case is closed, rather than silently discarded by the capacity table.

## Independent computation

`independent_check.py` reads no target file. It checks the literal signature identities, reconstructs the complete capacity table from the imported Ramsey values, enumerates every small-module coloring and contact signature, and enumerates every large-module boundary tuple. The canonical JSON serialization of all audit facts has SHA-256

```text
41c24618f3f83a49c3a8a4d57900623935f32eb6302b5afa71db5ef4c2bd0fc4
```

With Python 3.10 or later and only the standard library:

```sh
cd ramsey_r55_module_resilience_review1
python3 -B independent_check.py | diff -u EXPECTED.txt -
python3 -O -B independent_check.py | diff -u EXPECTED.txt -
```

Both modes ran in about 0.1 seconds on the review machine.

I separately replayed all 14 target files at exact commit `823d258fe6dfa33a695e148bbed08b1709fbe3c9`. Normal and assertion-disabled full runs both returned `REPRODUCED_MODULE_RESILIENCE_PACKAGE`; all manifest hashes matched. The replay checked 130 deterministic physical family graphs, 10,240 small literal clique comparisons, and rejection of 10 bad family inputs and 6 bad certificates. I also confirmed directly that the current extractor rejects a valid-format \(|M|=5,|T|=16\) family input at its scope gate, consistent with the documented but underextended interface.

## Literature status and imported premises

The proof imports classical small Ramsey bounds. Greenwood and Gleason's primary paper is [*Combinatorial Relations and Chromatic Graphs*](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/combinatorial-relations-and-chromatic-graphs/BF0DEBC881488344266BCD77CBBCD86B), and McKay and Radziszowski prove [\(R(4,5)=25\)](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf). The current degree-window formulation also appears in Angeltveit and McKay, [\(R(5,5)\le46\)](https://arxiv.org/html/2409.15709v2).

A search-indexed `kenan.works` summary asserts the weaker statement that every \((5,5)\)-good graph of order at least 40 is prime, but its underlying proof was not retrievable. Neither the target nor this review claims priority for primeness or the module-capacity method. I found no primary source for the deletion-resilience refinements; this limited search is not a historical-priority proof.

## Exact trust boundary

Imported: the listed small Ramsey bounds, including the historical computer-assisted proof of \(R(4,5)=25\), and the target statement to audit. Checked independently: all contact identities, local arithmetic, table rows and color reversals, every small-module internal coloring and contact signature, all large-module capacity tuples, the 28-vertex saturation case, the order-five strengthening, and the target package's deterministic replay.

No target certificate, fixture, extractor, comparison graph, catalogue, solver, or private trace is an input to the independent checker. Remaining trust is in the short mathematical reductions, the compact unformalized Python program, exact Python semantics, SHA-256, the interpreter, the imported Ramsey bounds, and ordinary hardware.

## Defects and objections

No blocking defect was found. The theorem's hypotheses, quantifiers, deletion complements, color symmetry, proper-module convention, and equality case align with the proof. The only correction is positive: the proof excludes five-vertex modules through 16 deletions, one deletion beyond the public extractor's declared family.

## Strengthening and improvement opportunities

Add \(|M|=5,|T|\le16\) to the extractor's accepted family; the existing proof gives it without a new premise. At the next boundary, a four-vertex module after 16 deletions must have no monochromatic internal triangle, sharply restricting it to the two-colorings of \(K_4\) whose color classes are both triangle-free. Formalizing the signature and capacity argument would remove the remaining Python and prose-proof trust boundary.
