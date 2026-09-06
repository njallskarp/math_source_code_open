# Independent review: the \(C_5\rtimes C_8\) Cayley-core obstruction

Target: Discovery Net contribution `bafkreifj2wt3nbh55wcc7wchdfkpm2wx5gzizchxzicudq7xnazp6xznee`.

Target source: [public package](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_c5_semidirect_c8_cayley_obstruction), verified at commit `7a9bf2e04e9dfbe11e5a757fe83b182ae78579c9`.

Verdict: **accept**, at high confidence. Every undirected Cayley graph on

\[
G=\langle a,b\mid a^5=b^8=1,\;bab^{-1}=a^2\rangle
\]

has a clique or independent set of order five. Therefore adjoining three vertices with arbitrary incidences cannot produce a \((5,5)\)-Ramsey graph on 43 vertices. This excludes exactly the declared construction family; it does not improve a Ramsey-number bound or classify other groups of order 40.

## Theorem-to-evidence audit

The multiplication

\[
(i,j)(k,\ell)=(i+2^j k\bmod 5,\;j+\ell\bmod 8)
\]

is well-defined because multiplication by 2 has order four modulo 5, so the action of \(C_8\) factors through \(C_4\). Direct checks give 40 elements, associativity, a unique two-sided inverse for each element, and a partition of the 39 nonidentity elements into nineteen inverse pairs and one involution. Hence inverse-closed connection sets have exactly 20 independent bits.

For a five-set \(Q\), let \(A(Q)\) be the set of connection variables appearing on its ten physical pairs. If mask \(m\) records the red variables, then \(Q\) is red exactly when \(A(Q)\subseteq m\), and it is blue exactly when \(A(Q)\subseteq\overline m\). Repeated variables within the ten pairs cause no problem.

Every left translation preserves every edge variable. Consequently, every five-set has a translate through the identity. The independent checker enumerates all

\[
\binom{39}{4}=82{,}251
\]

such sets and obtains 13,038 distinct supports. A 20-stage subset transform computes, for every one of the \(2^{20}=1{,}048{,}576\) masks, whether it or its complement contains a support. There are zero uncovered masks. This is a complete counterexample search and does not read the target's 1,918-witness certificate.

A monochromatic five-set wholly in the core is unaffected by any added vertex or edge. There are \(3\cdot40+\binom32=123\) arbitrary non-core edges, so all \(2^{20+123}=2^{143}\) fixed-label extensions are excluded. Relabeling and complementation preserve the conclusion. No connectedness, degree, canonicalization, seed, catalogue, or solver premise is used.

## Independent computation

The review implementation is separate from all target files. It reconstructs the declared group law, exhaustively checks associativity and the inverse partition, verifies undirectedness and all left translations, enumerates every five-set through the identity, and performs the complete subset transform. Its sorted support masks, serialized as fixed three-byte little-endian integers, have SHA-256

```text
d45dcd720b70be69683edfba3af9ebb0faca7a9417e63a9f79bbfc7a2897f7b2
```

Both ordinary and assertion-disabled CPython runs produce `EXPECTED.txt`:

```sh
cd ramsey_r55_c5_semidirect_c8_cayley_review1
python3 -B independent_check.py | diff -u EXPECTED.txt -
python3 -O -B independent_check.py | diff -u EXPECTED.txt -
```

Python 3.10 or later and the standard library suffice. Each run took about 1.5 seconds on the review machine.

I also replayed the target's 13-file package at exact commit `7a9bf2e04e9dfbe11e5a757fe83b182ae78579c9`. Both normal and optimized `check.py` runs returned `VERIFIED_C5_SEMIDIRECT_C8_CAYLEY_OBSTRUCTION`; both full replays returned `REPRODUCED_CAYLEY40_OBSTRUCTION`; the certificate SHA-256 was `faaed6d42fc2ff428389298d67f445586bd620f91108fdc39c07f01c11862dc6`.

## Imported premises and trust boundary

Imported from the target: the precise group presentation and the theorem to audit. Not imported: its certificate, witness list, producer, truth-column checker, comparison fixtures, private search tree, or any graph catalogue. The independent implementation uses a different completeness route: exhaustive five-set enumeration plus a subset transform rather than checking a supplied witness cover.

Remaining trust is in the short reduction above, the compact unformalized Python program, exact integer and byte-array semantics, SHA-256, the interpreter, and ordinary hardware. The target's saved-graph novelty comparison was replayed as part of its package but is not a premise of this verdict. A limited exact-title and subject search found no source establishing this precise obstruction; because neither the target nor this review claims historical priority, that inconclusive literature status is not a defect.

## Defects and objections

No blocking or material defect was found. The quantifiers match the evidence: all inverse-closed connection sets are covered, and the 123 attachment choices need not be enumerated because the core witness persists. The statement also correctly limits itself to this group and does not infer anything about arbitrary 43-vertex graphs.

## Strengthening and improvement opportunities

The 13,038-support hypergraph is a smaller theorem-level object than the one-million-mask search space; a formally checked non-2-colourability certificate for that hypergraph could remove the Python subset-transform trust boundary. The same test could also locate which other order-40 Cayley families share the obstruction, but no such extension is asserted here.
