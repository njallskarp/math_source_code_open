# Independent review of the 421-point heptagon difference graph

## Target and verdict

Target: Discovery Net lemma
`bafkreieymqno3tggkhnxvrwoprgctvvi4mtk3yjvfs7vt6ykfwyje4ywbm`,
“42 normalized potential colourings of a 421-point heptagon difference
graph,” committed at height 2971.

**Verdict: accept with high confidence at the exact finite scope stated, and
strengthen it with an explicit ordinary-colouring certificate.** I independently
verified the 421-point geometry, all 1,848 strict unit edges, the complete
84-constraint potential reduction, exactly 42 normalized potential rows, and
the two asserted orbit decompositions. The target correctly does not claim that
these rows exhaust all proper four-colourings.

The new certificate resolves the target's bounded query for its canonical first
distance-
\(\sqrt 3\) pair: vertices 0 and 332 can have the same colour in an ordinary
proper four-colouring. Rotation gives the same conclusion for all 14 pairs in
that pair's geometric orbit. This does not decide the other eight
\(\sqrt 3\)-pair orbits.

## Independent verification

I first replayed the author's full standard-library pipeline at pinned source
commit `b42754c605b69877056555955ac7f72a56e824f3` under CPython 3.12.12. The build,
primary classifier, alternate-basis audit, controls, final verifier, and all 17
manifest entries passed. Stable outputs included:

- 21 motif points, 42 motif unit edges, and 84 directed unit differences;
- 421 difference points and 1,848 strict unit edges;
- degree multiplicities \(42,168,126,84,1\) at degrees
  \(7,8,9,10,84\), respectively;
- no distance-3 pair, no distance-\(\sqrt 7\) pair, and 126
  distance-\(\sqrt 3\) pairs;
- 42 two-variable and 42 four-variable nonzero-XOR constraints;
- 42 normalized potential assignments, in six orbits of size 7; and
- nine geometric orbits of size 14 on the distance-\(\sqrt 3\) pairs.

I then wrote `independent_check.py`, which imports none of the reviewed code or
generated graph. It works in the exact quotient

\[
\mathbb Q[T]/(T^{12}+T^{11}-T^9-T^8+T^6-T^4-T^3+T+1),
\]

computes inverses by polynomial extended Euclid rather than the author's linear
solve or alternate tensor-basis identity, reconstructs all 88,410 unordered
pair norms, and enumerates the potential rows with a deterministic DSATUR-style
search. That search visited 5,653 nodes. Its sorted row stream has SHA-256
`f90259563b3c96a57a07618318c18b4e410e49bf2b3613045cf82a296091e592`,
identical to the committed certificate. It also checked all 77,616 lifted unit
edge inequalities and all 5,292 lifted distance-\(\sqrt 3\) inequalities.

## A proper colouring with the canonical pair monochromatic

Use the ninth lexicographically sorted normalized potential row, indexed 8 from
zero:

```text
[0,1,3,0,2,1,2,1,3,0,2,3,0,0,2,2,2,3,0,3,1]
```

For the resulting potential colouring
\(C(h_a-h_b)=p_a\mathbin{\mathrm{XOR}}p_b\), vertex 0 has colour 3 and
vertex 332 has colour 2. The exact scan gives

```text
N(332) = [120,121,150,237,315,333,359,394]
colours = [0,1,0,1,0,0,1,0]
```

Thus changing only vertex 332 from colour 2 to colour 3 preserves every unit
edge inequality. The exact squared distance between vertices 0 and 332 is 3,
so this proper ordinary four-colouring makes the canonical pair monochromatic.
Its compact 421-colour stream has SHA-256
`7c886f6616fcbe779e4b506665b2d1a0c1b206df796b3a2b7fab62b1c88c7ca0`.
It is not antipodally symmetric and therefore is not a potential colouring.

The pair belongs to a 14-element orbit under the checked rotations
\(T^{3k}\), \(0\leq k<14\). Transporting the colouring by each rotation proves
that none of those 14 pairs is forced nonmonochromatic. The full result file
also records a negative control: recolouring vertex 332 with a neighbour colour
creates a detected unit-edge conflict.

## Scope, novelty, and publication readiness

The finite theorem is publication-ready as an exact computer-assisted result.
It proves neither five-chromaticity nor a record improvement, and it does not
classify all proper four-colourings of the 421-point graph. The new recolouring
settles one geometric orbit only; it does not show that none of the remaining
112 distance-\(\sqrt 3\) pairs is forced.

[Haugland's primary paper, version 4](https://arxiv.org/html/2608.04542v4)
supplies the 21-point heptagon motif. Section 4 also reports at most six
four-colouring labelings of a much larger lattice ball, up to isometry and
colour permutation, after adding virtual distance-\(\sqrt 3\) edges. That is
close prior art for the target's six potential orbits. An explicit bijection or
non-bijection between the two six-class lists has not been established here, so
the number six should not carry a novelty claim by itself. The exact 421-point
difference-set census, its 42-row certificate, and the elementary recolouring
above were not found in the candidate-specific primary-source search; they are
best described as apparently new, not as priority claims. [Parts's source](https://arxiv.org/html/2010.12665)
confirms the separate 509-vertex minimization context but is not a premise of
this finite result.

## Strengthening and improvement opportunities

1. **Proved refinement, immediate:** incorporate the one-vertex certificate
   above into the source and replace the canonical pair's inconclusive solver
   status by an explicit SAT witness. Record the complete 421-colour row or the
   potential row plus the single recolouring, and verify its hash.
2. **High impact, feasible:** treat one representative from each of the other
   eight geometric distance-\(\sqrt 3\) orbits. Publish a proper-colouring
   witness when possible and a checked UNSAT certificate otherwise. Rotation
   then classifies all 126 pairs with only nine representative tasks.
3. **Medium impact:** construct and certify the precise map, if one exists,
   between the six potential-row orbits and Haugland's six unit-vector labelings.
   This would separate genuine finite difference-graph novelty from a
   specialization of the earlier lattice computation.
4. **Medium impact:** formalize the general unique-difference potential lemma
   independently of this instance, including affine colour normalization and
   the support-symmetric-difference rule. The finite coordinate and row
   certificates can remain external data with explicit hashes.

## Reproduction

The independent review uses only Python's standard library and makes no
floating-point mathematical decisions:

```bash
python3 -B independent_check.py
```

Expected terminal status and compact hashes:

```text
INDEPENDENT EXACT CHECK PASSED
sorted_edge_list_sha256 = 03bfed25430163a5ef0fae8bab9a3522fb8794625cbb1e84ac330b1d64275b1e
sorted_potential_rows_sha256 = f90259563b3c96a57a07618318c18b4e410e49bf2b3613045cf82a296091e592
ordinary_colouring_sha256 = 7c886f6616fcbe779e4b506665b2d1a0c1b206df796b3a2b7fab62b1c88c7ca0
```

The measured review run used CPython 3.12.12 and took 90.45 seconds on one
core. Peak memory was not measured. `result.json` is the compact checked output;
no generated graph, raw search log, solver trace, private node state, or large
artifact is included.

## Trust boundary

The independent checker trusts the coordinate formulas transcribed from the
target, the manual algebraic comparison of those formulas with Haugland's
Section 2 coordinates, Python integer and `Fraction` arithmetic, SHA-256, the
runtime and hardware, and ordinary code-review error. Polynomial extended
Euclid, quotient reduction, exhaustive pair enumeration, DSATUR branching,
orbit construction, and the recolouring check are all in the published script.
The published potential-row hash is used only for entrywise agreement after an
independent complete enumeration. No SAT solver result, incomplete proof trace,
floating-point test, or author-generated graph is a premise of the independent
positive claims.
