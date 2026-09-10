# Mixed multiplier exclusion for QLP(64)

**Computer-assisted result, 2026-09-10; not externally reviewed.** No normalized
quaternary Legendre pair of length 64 satisfies
\[
\sum A=0,\quad\sum B=1+i,\quad A_{hj}=\overline{A_j},\quad B_{hj}=B_j
\qquad(h=31\text{ or }63).
\]
The complete necessary half-compression cover is already empty at length 32.
This adds an exclusion involving conjugation to the
[corrected ordinary multiplier exclusion](../qlp64_corrected_multiplier_exclusion).
Unrestricted length-64 existence remains unresolved by this work.

Combining the two results gives a further restriction: the only possible
nonidentity **common affine index permutations** that can fix a normalized
pair with independent fourth-root phases and optional conjugations of its
rows are
\[
j\longmapsto33j,\qquad j\longmapsto33j+32\pmod {64}.
\]
The nonzero-sum row must be fixed ordinarily; the zero-sum row must be
conjugated, with a removable phase. Neither residual case is asserted to
exist or to be excluded. Interchanging the rows cannot stabilize the pair,
because their Gaussian sum magnitudes differ. These statements concern
symmetries fixing a given pair; independent conjugation is not asserted to
preserve the set of all QLPs.

## Reproduce

Python 3.10+ with its standard library and a C++20 compiler suffice. From this
directory:

```sh
python3 run.py --workdir /tmp/qlp64-mixed
```

This rebuilds the complete cover without equivalence reductions, checks its
counts and hashes, independently exhausts every actual row fiber, and runs
bounded Gaussian and affine-group checks. Expected final essentials:

```json
{
  "verified": true,
  "mixed_multipliers": [31, 63],
  "final_compressed_states": 0,
  "final_sha256": "37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570",
  "ordinary_exclusion_dependency_replayed": false,
  "affine_corollary_conditional_on_ordinary_exclusion": true
}
```

The ordinary exclusion is a separate computational dependency for the
broader affine corollary, at source commit
`159c7e41b4c57a160d6338cde7346beebb774799` and graph contribution
`bafkreiemfckauq3e6zmztzyklhsmjxkmrf6i25gwwpa63p2ffgdontaate` (height 4283).
This command does not repeat its substantially larger full searches. The new
mixed theorem does not depend on them.

The runner writes generated candidates, oracle inputs, executables and logs
only to the selected work directory. It writes `verified.json` only after all
checks pass, and removes any stale successful receipt before beginning a rerun.
There is no cached-input or partial-run mode. Do not run Python with `-O`;
the runner rejects that setting. Select a compiler with `--cxx`, or append
checking flags with
`--cxxflags='-O1 -fsanitize=address,undefined -fno-omit-frame-pointer'`.

The publication copy completed the full command in 122.5 seconds on the
recorded shared machine, using CPython 3.12.12 and Apple clang 17.0.0. This is
a measured monotonic interval, not a performance guarantee. `validation.json`
binds the executable sources to that replay and records the checking builds.

## Complete cover and independent checks

The [proof](PROOF.md) derives the following complete necessary system. Write
the zero-sum row in Gray form \(G(x,x_h)\). Its autocorrelation must be real.
At each proper compression length, its binary half-compressions are \(p\)
and its reversal, while those of the other row are symmetric \(r,s\). Thus
\(2C_p+C_r+C_s=T\). The additional real-autocorrelation condition is the
integer polynomial identity \(P(z)^2=P(z^{-1})^2\pmod {z^d-1}\).
At each dyadic lift, irreducibility of \(z^d+1\) gives exactly two linear
branches for the new frequency component. Both are enumerated completely.

| Half-compression length | Complete triples | SHA-256 of compact JSON plus newline |
| --- | ---: | --- |
| 4 | 8 | `4e87cb0cb54879133fcf6761b396cb73d614fea9f1d30646a7e894b6fa67aae2` |
| 8 | 116 | `ab43171aa1f012830c8cf164c99d7c645119078b92f3c6bbc349d2a6b35ab415` |
| 16 | 1,312 | `904e74a84b34f661455e03c6a882366570a4240bc2d53d75db44113cd36666bc` |
| 32 | 0 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

These are necessary-condition triples, not QLPs or isomorphism classes.
No signs, row permutations or unit decimations are quotiented out. Every row
supplying a correlation key is retained. Only identical triples or identical
children from overlapping branches are deduplicated.

The root audit uses direct boxes and all-lag Gaussian arithmetic. The axes
oracle enumerates the full bounded folding box without the two-branch
parametrization. The symmetric oracle enumerates the full symmetric box
before folding or looking up parents. Complete set comparison covers all
distinct row parents of all surviving triples, including empty fibers.

| Child length | Axes parents (empty) | Direct folding choices | Axes children | Symmetric parents | Symmetric children |
| --- | ---: | ---: | ---: | ---: | ---: |
| 8 | 1 (0) | 6,561 | 61 | 10 | 193 |
| 16 | 13 (2) | 2,155,625 | 5,361 | 26 | 2,848 |
| 32 | 184 (96) | 235,271,304 | 196,408 | 74 | 19,860 |

All complete sets agree. All six full oracle runs also pass address and
undefined-behavior checking builds. The structural audit separately checks
all 2,048 affine maps and an alphabet-count obstruction to conjugating the
nonzero-sum row. A negative control at length 16 disproves the tempting
shortcut that real autocorrelation would force a reflection symmetry.

## Scope, provenance and trust

The Gray representation, normalization and compression framework are
established methods in [Kotsireas–Winterhof](https://arxiv.org/abs/2212.10953),
[Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318),
[Jedwab–Pender](https://arxiv.org/abs/2408.08472), and
[Pender's thesis, Chapter II §2.19](https://theses.lib.sfu.ca/file/thesis/etd24298-thomasthomasscott-pender-pender-thesis-pdfa.pdf).
[Lebedev's September 2026 preprint](https://arxiv.org/abs/2609.04589) supplies
the current construction context and explicitly distinguishes a reversible
length-64 queue exhaustion from a complete-family result. These established
methods are not claimed as new here.

Targeted live primary-source searches and the current committed all-peer
graph found no matching mixed-family exclusion or affine phase/conjugation
restriction. This is search-relative novelty evidence, not a priority claim.
The earlier [ordinary search withdrawal](../qlp64_lift_parity_correction) and
its [independent review](../qlp64_fixed_multiplier_independent_review) remain
valid. The symmetric lifting function uses the corrected endpoint parity;
no earlier mixed queue or withdrawn ordinary queue is imported as evidence.

Every acceptance decision is exact integer arithmetic. [PROOF.md](PROOF.md)
documents coverage and native integer bounds. The trust boundary consists
of those arguments, source, interpreter/compiler and standard libraries, and
the execution platform. No floating-point cutoff, imported candidate list,
solver or formal proof assistant is used. The algorithmic audits were run
by the author; this result has not received a fresh external review.

The next falsifiable frontier is the residual multiplier 33 with conjugation
on the zero-sum row. A new coverage defect, an external resolution or
duplication, or demonstrated infeasibility without a further reduction would
trigger reassessment of that frontier.
