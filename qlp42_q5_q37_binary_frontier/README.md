# Full binary-shadow frontier for QLP-42 `q=5` and `q=37`

## Exact intermediary theorem

Let `(S_A,H_A,S_B,H_B)` be the established coupled length-21 transform of a
candidate in the canonical norm-32 QLP-42 shell.  Let `u_A,u_B` be the
binary indicators of quarter-turn local cells.  The local 16-state table and
reduction modulo `pi=1+i` force

```text
c_uA(s) + c_uB(s) = 0 in F_2,  1 <= s <= 10,
```

where `c_u(s)=sum_j u_j u_(j+s)`.  At shift zero the corresponding equation
is automatic because `q=wt(u_A)+wt(u_B)` is odd.

For `q=5`, exactly 10,248 of the `C(42,5)=850,668` labeled support pairs
satisfy all ten equations.  Under independent cyclic rotation of `u_A` and
`u_B`, these form exactly 36 orbits.  Their complete canonical manifest is
[`frontier_orbits.tsv`](frontier_orbits.tsv).

Simultaneous bit-complement is an equivariant bijection from this frontier
to the `q=37` frontier.  Consequently `q=37` also has exactly 10,248 labeled
pairs and 36 independent-rotation orbits.

The distribution by family weights is:

| `(q_A,q_B)` | all labeled supports | compatible labeled supports | rotation orbits |
|---:|---:|---:|---:|
| `(0,5)` | 20,349 | 126 | 6 |
| `(1,4)` | 125,685 | 882 | 2 |
| `(2,3)` | 279,300 | 4,116 | 10 |
| `(3,2)` | 279,300 | 4,116 | 10 |
| `(4,1)` | 125,685 | 882 | 2 |
| `(5,0)` | 20,349 | 126 | 6 |

All 12 mod-7 quotient orbits allowed by the predecessor compression theorem
occur.  Their lift distribution is nevertheless sharply nonuniform: the
12 quotient fibers contain respectively `7,7,1,1,3,3,3,3,3,3,1,1` of the
36 full-length rotation orbits in the lexicographic quotient order printed
by the Python verifier.  Thus the full length-21 equations refine the
mod-7 result without excluding a quotient orbit.

## Complement proof

For a binary length-21 word `u` and a nonzero shift `s`, expansion in
`F_2` gives

```text
c_(1-u)(s)
 = sum_j (1+u_j)(1+u_(j+s))
 = 21 + 2 wt(u) + c_u(s)
 = 1 + c_u(s).
```

Complementing both words therefore adds `1+1=0` to every combined
autocorrelation.  It sends total weight `5` to `42-5=37`, is an involution,
and commutes with both cyclic rotation actions.  It is consequently a
bijection both on labeled frontiers and on independent-rotation orbits.

## Complete finite census

The Python verifier enumerates masks of weights zero through five, groups
them by exact weight and the ten-bit autocorrelation signature, and obtains
the counts by exact signature intersection.  It then performs a separate
definition-level pass through all 850,668 support pairs, directly checks
the ten equations, canonicalizes both rotations, reconstructs the 36-row
manifest, and checks every mod-7 quotient fiber.  It also exhaustively
verifies the complement identity on all `2^21` binary words.

The independently written C++20 verifier uses a different enumeration: it
generates every five-subset of a single 42-bit universe with Gosper's rule,
splits each subset into the two families, evaluates overlaps directly, and
canonicalizes each compatible pair.  It reproduces all theorem-level
counts and the complete manifest.  The 42-bit representation fits in
`uint64_t`; every enumerated counter is below one million, so the fixed-width
arithmetic is far below its bounds.

## Reproduction

On the recorded Apple-arm64 host, Python 3.12.12 took about 15.1 seconds and
16 MB maximum RSS.  The GCC 16.2.0 release verifier took about 0.4 seconds
and 9 MB.  A full AddressSanitizer/UndefinedBehaviorSanitizer run passed.

Run all hashes, both exact verifiers, output comparisons, and sanitizers:

```bash
CXX=/opt/homebrew/bin/g++-16 ./verify_all.sh
```

On another system, set `CXX` to a C++20 compiler supporting AddressSanitizer
and UndefinedBehaviorSanitizer.

## Scope, sources, and next step

This is an exact theorem about the full binary-shadow consequence of the
coupled QLP-42 equations.  It does **not** show that any of the 36 support
orbits lifts through the next Gaussian residue layer, the four exact global
sums, the 16-state coupling, or the integer autocorrelation equations.  It
therefore does not exclude either `q=5` or `q=37` and does not settle
QLP-42.  The trust boundary is the established coupled transform and local
binary reduction, the elementary complement argument, source inspection,
the two exact implementations, compiler/interpreter, operating system, and
hardware.  No floating point, randomness, solver status, heuristic cutoff,
concurrency, or time limit enters the result.

Primary context is Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*,
<https://arxiv.org/abs/1302.0571>; Kotsireas--Winterhof, *Quaternary
Legendre Pairs*, <https://arxiv.org/abs/2212.10953>; Jedwab--Pender, *Two
constructions of quaternary Legendre pairs of even length*,
<https://arxiv.org/abs/2408.08472>; and Kotsireas--Koutschan--Winterhof,
*Quaternary Legendre pairs II*, <https://arxiv.org/abs/2408.16318>.  A
targeted primary-source and committed-graph search found no matching
full-length `q=5/q=37` binary-shadow census.  Apparent novelty is relative
to those searches, not a historical-priority claim.

The strongest next step is to impose the next `pi`-adic local-state layer
and the exact four Gaussian sums directly on the 36 certified support
orbits, retaining the complement map as an audit of which conclusions do
and do not survive beyond the binary shadow.
