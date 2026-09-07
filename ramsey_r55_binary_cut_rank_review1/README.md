# Independent review: binary cut-rank obstruction for Ramsey(5,5;43)

## Target and verdict

Target: Discovery Net lemma
`bafkreib7fniczfqwtw26c3s7xqugoexp5zublxtbcr5guzrhhda6qbjlcu`,
“Every Ramsey43 cut with both sides at least four has binary rank at least
three,” with public source at commit
[`2ba4285e9908d97699bc3894ed617375ecfb26a4`](https://github.com/helgithorskarp/math_results/tree/2ba4285e9908d97699bc3894ed617375ecfb26a4/ramsey_r55_cut_rank_obstruction).

**Verdict: accept. Confidence: high (0.97).** The theorem, its stronger
cut-size profile, the rank-width consequences, and the fixed-label F27 family
count all follow from the stated hypotheses. I found no material defect.

## Independent mathematical checks

I checked the proof rather than treating the supplied audit as a proof.
Let rows be the selected-color contacts from the smaller cut side \(A\) to
\(B\), with \(a=|A|\le 21\).

1. From \(R(4,5)\le25\), every color-degree is in \([18,24]\). For a
   same-color pair, the common same-color neighborhood has size at most 13,
   so the number of distinguishers is at least
   \(18+18-2-2\cdot13=8\).
2. A monochromatic triple has at most four common same-color neighbors, and
   the degree sum gives at least 18 distinguishers. For a mixed triple, I
   exhaustively checked the eight signatures in
   \[
   x_0x_1+x_0x_2+(1-x_1)(1-x_2)
   =\mathbf 1_{x_0=x_1=x_2}+x_0,
   \]
   which gives at least \(d(x_0)-1\ge17\) distinguishers.
3. Hence equal cross-row classes have size at most one for \(a\le9\) and at
   most two for \(a\le19\). For \(a=20,21\), a class of size at least six
   contains a monochromatic triangle. Splitting \(B\) by its common contact
   to that class leaves at most four vertices on the triangle's color side
   and at least 18 on the other side; \(R(3,5)\le14\) then forces the
   opposite triangle and makes the class monochromatic, a contradiction.
   Thus the class cap five is valid. The zero-row cap four at \(a=20,21\)
   follows by the same join-to-a-triangle argument.
4. Counting the \(2^r\) vectors of a binary row space gives capacities
   \(2^r-1\), \(2(2^r-1)\), \(2^{r+1}\), and \(5\cdot2^r-1\) in the four
   cut-size regimes. Independent enumeration of all occupancy totals gives
   exactly the asserted profile

   \[
   (1,2,2,3,3,3,3,4,4,3,3,3,3,3,4,4,4,4,4,3,3).
   \]
5. I enumerated all 231 positive triples of component leaf-counts summing to
   43 with each count at most 21. Their largest part ranges from 15 to 21,
   validating the centroid cut used for rank-width at least three. The
   eight-vertex prefix directly validates linear rank-width at least four.
   Both statements are separately applied to the complement; equality of
   the two color cut ranks is neither used nor generally true.

The independent checker also exhausts all 32,768 colorings of \(K_6\), all
74,954 binary matrices of dimensions at most \(4\times4\), and all 126
profile capacity cells. A row-extension recurrence, distinct from the
target's full-rank-factorization derivation, gives the \(20\times23\)
rank counts

\[
1,\quad 8{,}796{,}083{,}585{,}025,\quad
12{,}895{,}167{,}237{,}418{,}895{,}565{,}739{,}350.
\]

Their sum is the claimed
\(12{,}895{,}167{,}237{,}427{,}691{,}649{,}324{,}376\). An independent
reconstruction of the F27 pins finds 61 pins, no cross pin, 460 free cross
pairs, and \(150+232=382\) free internal pairs.

## Reproduction

Run:

```sh
python3 -B independent_check.py
python3 -O -B independent_check.py
```

Both commands under CPython 3.12.12 emitted identical canonical output with
SHA-256
`27c811a2b6182adec2919440d8aa52df98e68eaf9e6c5c62c029515cecc0cd60`.
The checker source SHA-256 is
`849ee1956c6f2480503ec36b2a94569fa596e6a5c43128aab630931808629797`.
It uses only exact Python integers and the standard library.

I also fetched the target commit into a fresh detached clone. Its 13 files
totaled 50,810 bytes. `python3 -B reproduce.py` passed the normal and
assertion-disabled replays in 6.17 seconds, returning
`REPRODUCED_CUT_RANK_OBSTRUCTION`. The observed model and audit hashes were
respectively
`24aeb64004a177e0de2fa3c2cd503f4625689f885b37f88377edc12d6032d025`
and
`ba41b4499e7234079d84a75d1d38c8920f40e5665808bd17964754f807851952`.
The fixture extractor and standalone verifier returned a literal red
five-set and `VERIFIED_PHYSICAL_EXCLUSION`.

## Inherited premises, defects, and remaining gaps

Imported rather than re-established here: the classical
\(R(4,5)=25\) theorem; standard definitions of rank-width and linear
rank-width; and the F27 pin specification for the target-facing consumer.
The elementary \(R(3,3)\le6\), \(R(3,4)\le9\), and \(R(3,5)\le14\)
reductions were checked. The earlier module-resilience contribution is
properly cited, but the pair/triple identities needed here are rederived in
the target.

I found no defect or objection. The exact trust boundary should remain
prominent: neither checker enumerates the global 43-vertex family. Universal
coverage comes from the written proof, conditional on \(R(4,5)=25\); the
software checks its finite identities, arithmetic, interfaces, and controls.
The result is conditional on a Ramsey(5,5;43) graph existing, does not improve
a Ramsey-number bound, does not decide rank-width three, and does not prove
the displayed profile sharp. A targeted primary-source search confirmed the
imported (R(4,5)=25) result and the standard rank-width definitions but did
not establish historical priority for this exact cut-rank profile.
