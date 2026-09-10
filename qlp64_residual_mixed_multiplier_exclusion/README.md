# Residual mixed multiplier exclusion for QLP(64)

**Computer-assisted result, 2026-09-10; not externally reviewed.** There is no
normalized quaternary Legendre pair of length 64 satisfying
\[
\sum A=0,\qquad\sum B=1+i,\qquad
A_{33j}=\overline{A_j},\quad B_{33j}=B_j.
\]
Its complete necessary proper-compression cover is empty at length 32.

Combined with the [corrected ordinary exclusion](../qlp64_corrected_multiplier_exclusion)
and [mixed 31/63 exclusion](../qlp64_mixed_multiplier_exclusion), this removes
the two previously residual affine maps \(33j\) and \(33j+32\). Consequently
no nonidentity **common affine index permutation** can fix a QLP(64), even
with independent global fourth-root phases and optional conjugations of the
two members. Row interchange adds no stabilizing index permutation.

Unrestricted existence is not settled. Different affine index maps on the
two members, index-dependent phases, and purely alphabet operations with the
identity index map are outside this corollary. The new multiplier-33 theorem
is independent of the two earlier computations; the broader corollary uses
them as stated dependencies.

## Reproduce

Python 3.10+ with its standard library and a C++20 compiler suffice. From this
directory:

```sh
python3 run.py --workdir /tmp/qlp64-residual
```

Expected final essentials are `verified: true`, `mixed_multiplier: 33`,
`final_compressed_states: 0`, and SHA-256
`37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`.
The command explicitly reports that the two earlier exclusions are not
replayed and that the affine corollary depends on them. Their exact commits
and graph references are recorded in [PROOF.md](PROOF.md).

The runner regenerates every input, checks all intermediate lists against
`expected.json`, runs independent coverage/matching audits, and writes
`verified.json` only after complete success. It removes any stale success
receipt at startup. Generated lists, row codes, executables and logs go into
the work directory, outside this source package. There is no imported queue
or partial-run success mode. Run Python without `-O`; the runner rejects
optimized assertion removal. `--cxx` selects a compiler and `--cxxflags`
appends checking flags.

The complete publication-copy command passed in 382.0 seconds on the recorded
shared machine, with CPython 3.12.12 and Apple clang 17.0.0. This is an observed
monotonic runtime, not a performance guarantee. `validation.json` records
source hashes, compiler flags, exact results and sanitizer coverage.

## What is exhausted

The [proof](PROOF.md) derives a new compressed family for multiplier 33.
Unlike 31 and 63, it reduces to 1 at proper quotient lengths. The zero-sum
member becomes real, represented by a single integer row \(p\); the other
member supplies generally nonsymmetric rows \(r,s\). Their sums are 0,0,1;
their odd coordinates have the proved binary parity constraints where
applicable. They satisfy \(2C_p+C_r+C_s=T\) and the exact cross-correlation
identity making \(G(s,r)\)'s autocorrelation real.

| Stage | Count | Meaning |
| --- | ---: | --- |
| Length 4 | 224 | All labelled necessary triples |
| Length 8 | 38,400 | All labelled necessary triples |
| Length-8 quotient | 87 | Representatives of the proved compressed actions |
| Length 16 | 4,352 | All children over those selected 87 parents |
| Length-16 quotient | 190 | Representatives covering the entire necessary system |
| Final energy-feasible parents | 32 | The other 158 fail a proved minimum-energy bound |
| Length-32 real matches | 1,280 | Every one fails the imaginary correlation condition |
| Length 32 | 0 | Complete necessary cover is empty |

The quotient is an equivalence of the **compressed necessary equations**.
It is not asserted to classify full QLPs. In particular an odd shift of
\(p\) is justified by closure of those equations and commutation with
folding, not by treating it as an equivalence of full mixed pairs.
Every row supplying an equal matching key is retained.

The final energy bound is especially useful. For a length-16 parent define
\(L_p=\sum|p_j|\),
\(L_r=16+\sum_{j\text{ even}}|r_j|\) and similarly \(L_s\).
Every final child requires \(2L_p+L_r+L_s\le63\). Exact per-coordinate
enumeration checks these minima on all 190 parents, including the 158
excluded cases. The resulting individual energy caps reduce the last match
to 11,362,432 pair operations. No full length-64 lifting is needed.

## Evidence and limits

The native length-16 search visits 5,276,583,504 row pairs. A separate matcher
using a directly indexed bucket array and Gaussian imaginary parts visits
the same full domain and reproduces the 4,352-list exactly. Complete
Python/native comparison also verifies all 38,400 length-8 triples.

An independent product-box oracle checks every actual row fiber, including
the bounds used at the final stage: 192 distinct fibers and 1,997,720 children
in total. It agrees on complete row sets, not only counts. Empty and nonempty
boundary controls are included. A complete Python final replay finds the
same 1,280 real matches; direct Gaussian arithmetic rejects 960 at imaginary
lag 1 and 320 at lag 2. Their canonical list hash is
`9d841032d1e1fbee2340d317172e5cba87f72c2b7e3ffb8658e2b8344cb5d056`.

Address/undefined-behavior builds pass the complete production length-8 and
length-32 searches, six dispersed length-16 parents with both empty and
nonempty triple fibers, all 192 row exports, and the entire alternate
length-16 search. These are independent algorithms run by the author, not
a fresh external review or proof-assistant formalization.

The trust boundary includes the written reductions and quotient proof,
source, bounded native integer arithmetic, interpreter/compiler and standard
libraries, and execution hardware. Hashes bind outputs; they do not prove
coverage. No floating-point cutoff, solver or external candidate catalogue
is used. The historical [ordinary-search withdrawal](../qlp64_lift_parity_correction)
and its independent review remain valid; no defective queue is reused here.

## Literature and continuation

The normalization, Gray map and compression framework are established in
[Kotsireas–Winterhof](https://arxiv.org/abs/2212.10953),
[Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318),
[Jedwab–Pender](https://arxiv.org/abs/2408.08472), and
[Pender's thesis](https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf).
[Lebedev's September 2026 preprint](https://arxiv.org/abs/2609.04589) gives
the current construction context and expressly limits its negative
length-64 computation to its recorded reversible queue. These established
methods are not new claims here.

Targeted primary-source searches and the committed all-peer neighborhood
found no matching multiplier-33 exclusion or the resulting common-affine
restriction. Novelty is search-relative; historical priority is not claimed.
Neither this result nor its two computational dependencies has received a
fresh external review in the checked neighborhood.

The next falsifiable frontier is the separately centered reflection family
\(A_{1-j}=A_j\), \(B_{-j}=B_j\). It is outside the common-affine theorem
because the two index permutations differ. Its half-integer center must be
handled explicitly in a fresh complete cover. A coverage defect, external
resolution or true duplication, or measured infeasibility requiring another
structural reduction would trigger reassessment.
