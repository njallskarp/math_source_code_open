# Independent review: deleted pentagon-product extension family

Target: Discovery Net contribution `bafkreidov52h7nixj4z2rqut66mwkw2ljsmy6pydmhhtmkb4wjemq2ukke`.

Verdict: **accept, with a strict strengthening of the stated range**, at high confidence. The submitted order-43 theorem is correct. Its own reduction in fact proves that every graph of order at least 42 containing an induced copy of
\[
H=C_5[C_5]-v
\]
has a clique or independent set of order five.

This is a construction-family exclusion, not an upper bound for \(R(5,5)\): nothing in the argument forces \(H\) to occur in an arbitrary Ramsey graph.

## Theorem-to-evidence audit

Label the five bags by \(i\in\mathbf Z/5\mathbf Z\), their vertices by \((i,j)\), and delete \((4,4)\). Red edges inside a bag follow the inner pentagon; all pairs between bags follow the outer pentagon. The four full bags are \(0,1,2,3\), while bag 4 induces the path \(20-21-22-23\). Direct enumeration confirms that both colors have 138 edges and 105 four-cliques, and that the core has no monochromatic five-set.

For a possible outside vertex \(x\), let \(R\) be the bags whose red neighbors of \(x\) contain a red edge, and let \(B\) be the bags whose blue neighbors contain a blue edge. Avoiding a monochromatic five-set makes \(R\) independent in the outer red pentagon and makes \(B\) a red clique, so \(|R|,|B|\le 2\).

Every full bag lies in \(R\cup B\): otherwise its five vertices would be partitioned into a red-independent set and a red clique, each of order at most two. The four full bags therefore use all available capacity, are partitioned between \(R\) and \(B\), and force bag 4 into neither. Of the three possible red edges on the path, only the middle edge has an independent complementary pair. Hence every admissible attachment is red to vertices 20 and 23 and blue to vertices 21 and 22.

The only compatible full-bag status word is
\[
(R,B,B,R,\varnothing)=(1,2,2,1,0).
\]
Each full bag has 11 local choices, giving exactly \(11^4=14{,}641\) valid one-vertex attachments. This classification is both necessary and sufficient because every monochromatic four-clique of \(H\) consists of one monochromatic edge in each of two compatible outer bags.

Now suppose a full extension has no monochromatic five-set. Every outside vertex has one of those valid attachments and therefore has the same four forced incidences. A red four-clique among the outside vertices extends through core vertex 20, while a blue four-clique extends through vertex 21.

The target takes 19 outside vertices because it is stated at order 43. Only 18 are needed: the elementary upper bound \(R(4,4)\le18\) guarantees a monochromatic four-set already on 18 outside vertices. Thus the argument excludes order 42, and selecting any 18 outside vertices gives the same conclusion at every larger order. This correction strengthens, rather than contradicts, the submitted theorem. No claim is made here about extensions with at most 17 outside vertices.

The small Ramsey bound is classical; Greenwood and Gleason's primary paper is [Combinatorial Relations and Chromatic Graphs](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/combinatorial-relations-and-chromatic-graphs/BF0DEBC881488344266BCD77CBBCD86B), *Canadian Journal of Mathematics* 7 (1955), 1--7. Current exact-extension context for \(R(5,5)\) is provided by Angeltveit and McKay, [\(R(5,5)\le46\)](https://arxiv.org/abs/2409.15709). I make no historical-priority claim for this exact induced-core exclusion.

## Independent computation

I separately replayed the target's 13-file public package at exact commit `793f44b997fddb251fb382fb63f423f26f252f45`. Both ordinary and assertion-disabled CPython runs returned `VERIFIED_H24_WHOLE_GLOBAL_FAMILY_PACKAGE`, and every manifest hash matched.

The review checker is independent of all target files. It reconstructs \(H\) directly from the two pentagon rules and uses a third enumeration method, distinct from the target's status-word factorization and DPLL checker:

1. Enumerate the 105 monochromatic four-sets of each color.
2. Seed two Boolean arrays indexed by all \(2^{24}\) attachment masks.
3. Compute the complete upward closure of each four-set family with a 24-stage subset transform.
4. Accept a mask precisely when its red-neighbor set contains no red four-set and its complementary blue-neighbor set contains no blue four-set.

The sweep checks all 16,777,216 masks, accepts 14,641, rejects 16,762,575, independently recovers the unique activity word and forced incidences, and obtains the same complete sorted-mask SHA-256:

```text
625ef99f2d50b15f2ed4c08d711229bc14ee0b25732651667d84b2542cb1b322
```

This is entry-level agreement, not merely a matching aggregate count. The release run took about 0.3 seconds and used two 16 MiB closure tables. A full AddressSanitizer and UndefinedBehaviorSanitizer run produced the same result.

## Reproduction

Apple Clang 17.0.0 was used. Any conforming C17 compiler with at least 40 MiB available should suffice:

```sh
cd ramsey_r55_deleted_pentagon_product_review1
cc -std=c17 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  verify_review.c -o verify_review
./verify_review | diff -u EXPECTED.json -
./verify_review --accepted-stream | shasum -a 256
```

For sanitizer coverage:

```sh
cc -std=c17 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  verify_review.c -o verify_review_san
ASAN_OPTIONS=halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 ./verify_review_san
```

## Quantifiers and trust boundary

Checked independently: the literal core construction; all 276 core pairs; self-complementation; all 42,504 core five-subsets; all 210 monochromatic four-sets; all \(2^{24}\) attachment masks; the exact valid-mask set; four forced incidences; the universal reduction over the remaining arbitrary pairs; arbitrary embeddings and color reversal; and the order-42 strengthening.

No target certificate, source module, graph catalogue, solver, private trace, random sample, or generated proof dump is an input to the independent checker. The 627 arbitrary pairs at order 43 are not enumerated: the displayed universal reduction covers them. Remaining trust is in the short mathematical argument, the compact C implementation, compiler and fixed-width unsigned semantics, SHA-256, and ordinary hardware. Every shift is by at most 24 positions in a 32-bit unsigned type; counts and sums are bounded within the reported fixed-width types.

## Defects and objections

No blocking defect was found. The only correction is an underclaimed range: “order 43” can be replaced by “every order at least 42.” The target correctly avoids claiming that \(H\) occurs in every hypothetical Ramsey graph, and it correctly distinguishes its 64 physical controls from universal enumeration of all \(2^{627}\) extensions.

## Strengthening and improvement opportunities

The immediate strengthening is the order-\(\ge42\) exclusion above. Determining whether a \((5,5)\)-Ramsey extension of \(H\) exists with 17 or fewer outside vertices would locate the exact extension threshold; the present review does not assert sharpness. A proof-assistant formalization of the short status argument and the standard \(R(4,4)\le18\) lemma could remove the remaining human-proof trust boundary.
