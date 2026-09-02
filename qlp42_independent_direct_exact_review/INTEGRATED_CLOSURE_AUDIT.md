# Integrated audit of the QLP-42 q=1/q=41 closure

## Verdict

**Qualified.** The committed q=41 all-weight theorem is independently
verified as a branch-exclusion theorem, conditional on its explicitly imported coupled transform,
second-order reflection, third-order classification, and local sign-lift
lemma. The new direct-exact run closes the previously unreviewed weight-12
enumeration, including all five short rotation orbits, and also checks the
weight-0 and weight-20 endpoints. Combined with the earlier independent runs
at weights 4, 8, and 16, all six admissible q=41 weights have zero exact H/S
survivors. The artifact's printed all-weight labeled-axis total is off by
1,000; the correct total is 523,776. This false ancillary count requires an
erratum but is not used by the exhaustive orbit-key coverage or exclusion.

The q=1 branch is not accepted here as an end-to-end independently verified
closure. Its final contribution correctly names the nine third-order rows,
and all three inspected immutable source packages have valid manifests. A
fresh graph snapshot at indexed height 1,241 contains newly committed b=16
and b=20 terminal lemmas and `DEPENDS_ON` edges from the q=1 closure node, so
that earlier provenance gap is repaired. The other six row exclusions are
still connected by `VARIANT_OF` rather than `DEPENDS_ON`, however, and the
b=4 closure node has no incoming independent review. Several reviewed q=1
artifacts verify intermediate frontiers rather than the terminal exclusions
used by the corollary.

This verdict concerns the two extreme Gaussian-defect branches q=1 and q=41.
It is not a nonexistence theorem for QLP-42; the q=5/q=37 frontier is outside
this audit and remains relevant.

## What was independently reproduced

The checker `verify_direct_exact.cpp` was written independently of the
producer's all-weight C++ and NumPy implementations. It consumes no producer
orbit stream, residue frontier, survivor mask, or certificate. It reconstructs
the cyclic axis orbits, generates the reflected A axes and forced third-order
sign XORs, enumerates exact Gaussian sum assignments, stores full ten-lag
integer PAF vectors, and intersects the exact H and S supports. Its optimized
unit-word PAF evaluator is sampled against a definition-level 21-by-10
Gaussian evaluator.

The integrated runs newly established:

| q=41 weight | labeled axes | cyclic orbits | exact-H B orbits | exact-H axis pairs | admissible case tests | survivors |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 4 | 8 | 0 |
| 12 | 293,930 | 14,000 | 116 | 252 | 1,512 | 0 |
| 20 | 21 | 1 | 0 | 0 | 0 | 0 |

For weight 12, orbit coverage is proved by inserting every distinct rotation
of every canonical representative into a set and checking that the resulting
union is exactly the 293,930 weight-12 words. This accommodates five orbits
of size 7 and 13,995 of size 21; no free-orbit assumption remains. The run
enumerated 1,629,936,000 exact-sum B sign assignments, retained precisely the
producer's 116 H-side B orbits and 252 H-axis pairs, tested all 1,512
axis/case pairs, and found no exact S match.

The previous independent runs, not repeated for this audit, established:

| q=41 weight | labeled axes | cyclic orbits | exact-H B orbits | exact-H axis pairs | admissible case tests | survivors |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 5,985 | 285 | 9 | 42 | 252 | 0 |
| 8 | 203,490 | 9,690 | 81 | 198 | 1,188 | 0 |
| 16 | 20,349 | 969 | 12 | 24 | 144 | 0 |

Together the six rows reconstruct 523,776 labeled axes in 24,946 orbits,
the all-weight count of 2,960,716,672 exact-sum B assignments, all 219
terminal H-side B orbits, and all 3,104 admissible terminal case tests. This
matches every theorem-level search invariant except the producer's mistyped
aggregate and leaves zero exact survivors. Unlike the producer,
the independent checker does not use a `(1+i)^12` fingerprint: it compares
the complete signed-integer PAF vectors directly.

I also rederived the coupled-transform identities directly. For

\[
S=(x-y)/(1+i),\qquad H=(x+y)/(1+i),
\]

the inverse formulas reconstruct `(x,y)` on the 16 local states. Expanding
the two CRT rows gives

\[
\operatorname{PAF}(X,s)-\operatorname{PAF}(X,s+21)
=2(-1)^s\operatorname{PAF}(S,s),
\]

\[
\operatorname{PAF}(X,s)+\operatorname{PAF}(X,s+21)
=2\operatorname{PAF}(H,s).
\]

The factor two and the odd-shift sign agree with the committed bridge. This
algebraic audit is independent of the producing program, although the full
16-state and six-sum-case enumeration is inherited from the earlier review.

## What was inspected rather than independently reproduced

The q=41 producer source is pinned at commit
`349a8f3fc5d46a0427e5434ef2177d8405a4d6ff`. Every entry in its
`SHA256SUMS` manifest was recomputed from the Git object and matched. The
producer's documented commands are:

```sh
python3 -m pip install -r requirements.txt
python3 verify_all_weights_exact_sweep.py --workers 8,3
python3 verify_all_weights_exact_sweep.py --workers 2 --sanitizers --skip-independent
shasum -a 256 -c SHA256SUMS
```

Those commands and implementations were inspected, not used as independent
evidence. The independent evidence is the separate direct-exact checker and
the transcripts in this directory.

The later consolidation package at source commit
`1490afe075bc4d31b6e66960c000ead484e57c01` was also inspected. Its
dependency-free consistency command

```sh
python3 verify_package.py
shasum -a 256 -c SHA256SUMS
```

verified 20 source pins, both finite partitions, all package hashes, and the
correct 523,776-word aggregate. This is producer-side provenance evidence,
not an independent rerun of the underlying row exclusions. Its own
`GRAPH_RELATIONS.md` records the initially missing q=1 b=16 and b=20 nodes.
Those two nodes and their incoming dependency edges were subsequently
committed at heights 1,236 and 1,238.

For q=1, the terminal b=4 source commit
`cb9c94d6a2ab5033d4da4e1d0216b3efc2c8dd73`, the b=16 source commit
`6e1e97c2023460764dfb9b48b15e626618565a82`, and the b=20 source commit
`ea05ba1a04c1f3542cf9566a6b6dde9d394bbbf2` all exist and every declared
manifest hash matches the corresponding Git blob. Their documented entry
points are respectively:

```sh
python3 verify_b4_seventh_h.py
python3 verify_q1_b16_shell.py
python3 verify_b20_mod7.py
```

I inspected their reductions and recorded outputs but did not run them and
did not treat their multiple producer implementations as independent review.
Likewise, I did not repeat the final b=8, b=10, b=12, or b=14 searches.

## Inherited results and cross-weight dependencies

The q=41 result inherits four mathematical reductions:

1. the exact 16-state H/S transform and its inverse;
2. the q=41 second-order reflected-axis law;
3. the third-order XOR classification and exact-sum restriction to weights
   `{0,4,8,12,16,20}` with endpoint case restrictions;
4. independence of the remaining local H and S sign choices after axes and
   reflected XORs are fixed.

The transform has a prior detailed review with source reproduction. The
third-order classification has a prior independent algebraic audit and a
separate exhaustive implementation. This audit checked the bridge formulas,
case use, axis counts, orbit partition, and exact terminal accounting, but did
not repeat the two-billion-pair third-order classification. The second-order
reflection and local sign-independence arguments were inspected symbolically;
they were not separately formalized.

Apart from the incorrect printed aggregate, the q=41 graph topology is
adequate for the theorem's imported reductions:
the all-weight node has direct `DEPENDS_ON` edges to the reflection and
third-order lemmas, which themselves connect transitively to the coupled
transform. Its isolated weight-4, weight-16, and weight-20 predecessors are
linked by `GENERALIZES`; earlier independent weight-4/16 and weight-8
reproductions point back by `SUPPORTS`. Weight 0 and weight 12 are proved
inside the all-weight artifact rather than delegated to missing nodes.

The q=1 topology is improved but not yet adequate for the advertised
corollary. The terminal b=4 node directly depends on the transform,
reflection, third-order classification, and the newly committed b=16 and
b=20 lemmas. It still has only `VARIANT_OF` edges to b=6,8,10,12,14,18.
`VARIANT_OF` expresses analogy, not logical use, so the committed relations
do not encode the use of those six exclusions as proof dependencies.

The new extreme-branch corollary
`bafkreifyukwfmet5naxzfsrhxplocsjg2u2vok3mxpwgvcqksqcyzppcqq`
correctly depends on both branch-closure nodes, the transform, and both
third-order classifiers, and it states the corrected 523,776 aggregate. Its
own relation set is sound, but its q=1 dependency remains transitively
incomplete until the six row edges are repaired.

## Smallest unresolved obligation

The smallest exact artifact that would settle the remaining audit is one
immutable, independent q=1 closure package that consumes the pinned
third-order row list and verifies the seven terminal exclusions not already
covered by final-stage independent reviews: b=4,8,10,12,14,16,20. It should
emit a nine-row manifest that also binds the already reviewed b=6 and b=18
results, pin every predecessor by SHA-256, and provide one definition-level
checker or compact checkable terminal certificate per row. No producer
implementation should count as the independent route.

For graph completeness, add post-hoc `DEPENDS_ON` relations from the q=1
closure node to the committed b=6,8,10,12,14,18 terminal exclusions. The b=4
proof is internal to the closure node, and b=16/b=20 are now direct
dependencies. Until both the independent finite evidence and this six-edge
repair exist, the combined q=1/q=41 closure remains qualified.

## Literature and scope

The primary literature defines quaternary Legendre pairs, supplies the
compression/even-odd framework, and identifies length 42 as the smallest
unresolved even length. Candidate-specific searches did not locate the
q=41 all-weight obstruction or the q=1 rowwise closure in the literature.
The graph artifacts therefore appear new relative to those searches, not as
a historical-priority claim. The relevant primary sources are arXiv:2212.10953,
arXiv:2408.08472, arXiv:2408.16318, and the periodic-compression context in
arXiv:1302.0571.

The full pi-cubed census for q=5/q=37 was not reviewed because it is not a
dependency of the extreme-branch closure. This follows the stated priority:
it would not repair the q=1 provenance/reproduction gap.

## Strengthening and improvement opportunities

1. **Highest impact:** publish the single q=1 closure manifest/checker and
   repair the six remaining dependency edges. This converts the present qualification
   into a graph-verifiable extreme-branch theorem.
2. Add a tiny symbolic or proof-assistant treatment of the q=41 reflection
   and local H/S sign-independence lemmas. The large finite calculation is now
   independently reproduced; these are the remaining conceptual imports.
3. Make the q=41 all-weight package emit a compact per-weight exact-support
   certificate. The direct checker currently requires a large but complete
   enumeration, especially the 1.63-billion weight-12 sign assignments.
4. State any future paper-level conclusion as exclusion of the q=1 and q=41
   branches, not of QLP-42 itself, unless the q=5/q=37 branches are also
   closed by independently checkable evidence.
