# Seventh-order `H` obstruction for the QLP-42 `q=41`, weight-20 stratum

## Theorem

In the canonical coupled length-21 transform of the norm-32 QLP-42 shell,
assume the `q=41` branch and let `b` be the binary Gaussian-axis word of
`H_B`.  There is no lift with

```text
wt(b)=20,   sum(H_A)=0,   sum(H_B)=1,
PAF(H_A,s)+PAF(H_B,s)=-2  for 1 <= s <= 10.
```

In fact the obstruction already appears modulo `(1+i)^7`.  The earlier
third-order and global-sum classification shows that weight 20 occurs only
in canonical sum cases 3 and 4.  Therefore this theorem removes the complete
weight-20 stratum from both cases in the surviving `q=41` branch.

This is a finite computer-assisted theorem, not a complete resolution of
QLP-42.  We write `pi=1+i`.

## Complete finite reduction

Up to cyclic rotation, a length-21 binary word of weight 20 has one orbit.
The verifier puts its unique real-axis position at zero.  The exact equation
`sum(H_B)=1` then fixes that entry to `+1` and requires exactly ten negative
signs among the twenty imaginary entries.  Thus every possible `H_B` is one
of exactly

```text
C(20,10) = 184,756
```

words.

The `q=41` reflection theorem gives 1,024 possible half-axis words for
`H_A`.  For each one, the third-order equations uniquely fix the ten sign
XORs in the reflected pairs.  Exhausting all 1,024 pair-sign masks and
retaining `sum(H_A)=0` visits exactly 127,704 assignments over all axes.
The local sign variables used here are complete: at every quarter-turn cell,
the `S` and `H` signs are independent, and the exceptional `A` cell has
`H_A(0)=0`.

For a Gaussian integer `z`, the programs compute its canonical `pi`-adic
digits by repeatedly subtracting `(Re(z)+Im(z)) mod 2` and dividing exactly
by `pi`.  Concatenating the ten PAF residues gives an exact fingerprint in
`(Z[i]/(pi^k))^10`.  Matching `H_A` to the complement `-2-H_A` gives:

| imposed `H` level | compatible `A` sign assignments | surviving `A` axes |
|---:|---:|---:|
| modulo `pi^4` | 127,704 | 512 |
| modulo `pi^5` | 16,272 | 418 |
| modulo `pi^6` | 720 | 4 |
| modulo `pi^7` | 0 | 0 |

The four sixth-order half-axis masks are

```text
0x000, 0x164, 0x29b, 0x3ff.
```

The `H_B` side has respectively 512, 72,688, 92,128, and 92,854 distinct
fingerprints at orders four through seven.  It has 92,854 distinct exact PAF
vectors, and the direct exact-vector intersection is empty as well.

As a predecessor regression, the programs independently impose the case-3
`S_A=5-i` and `S_B=4-i` sums modulo `pi^4`.  They reproduce the known 388
all-sums fourth-order `A` axes for the single weight-20 `B` orbit; 317 of
those survive fifth-order `H`, and none survive seventh-order `H`.  Case 4
has the same axis set by the established `S_B(4,-1)=S_B(4,1)` symmetry.

## Independent implementations

`verify_weight20_seventh_h.cpp` is a scalar C++20 verifier.  It generates
fixed-cardinality sign words with Gosper's combination recurrence, evaluates
every Gaussian PAF coefficient directly, and stores sorted exact residue and
PAF records.

`independent_numpy.py` is separately written.  It constructs combinations
from Python's lexicographic iterator, evaluates all ten correlations in
vectorized signed-integer arrays, and represents each residue row as its ten
explicit `pi`-adic digits.  It agrees entry-level on the complete quotient
ladder, the four sixth-order axes, the exact-sum counts, and the all-sums
regression.  The two programs share the mathematical finite reduction and
direct PAF definition; they do not share enumeration or residue code.

Run both implementations and compare their outputs:

```sh
python3 -m pip install -r requirements.txt
python3 verify_weight20_seventh_h.py
python3 verify_weight20_seventh_h.py --sanitizers
shasum -a 256 -c SHA256SUMS
```

The driver uses `CXX` when set, otherwise `clang++` or `g++`.  It was tested
with Apple clang 17.0.0, Python 3.12.12, and NumPy 2.2.2 on arm64 macOS.  A
normal dual run takes about seven seconds and stays below 0.5 GB on the
recorded machine.  AddressSanitizer and UndefinedBehaviorSanitizer pass.

## Scope, provenance, and trust boundary

The proof trusts the previously established `q=41` transform, reflection and
third-order sign-XOR reduction, source inspection, C++ and NumPy signed-
integer semantics, the compiler/interpreter, operating system, and hardware.
All mathematical arithmetic is integral; there is no floating point,
randomness, solver status, heuristic cutoff, concurrency, or time limit.  It
is not a proof-assistant formalization.

Primary context:

- Kotsireas--Winterhof, *Quaternary Legendre Pairs*,
  <https://arxiv.org/abs/2212.10953>;
- Jedwab--Pender, *Two constructions of quaternary Legendre pairs of even
  length*, <https://arxiv.org/abs/2408.08472>;
- Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
  <https://arxiv.org/abs/2408.16318>.

The last source identifies length 42 as the smallest unresolved case.  A
targeted search of these primary sources and the committed Discovery Net
graph found no matching weight-20 seventh-order obstruction.  Apparent
novelty is relative to those searches, not a historical-priority claim.

Public source directory:
<https://github.com/njallskarp/math_source_code_open/tree/main/qlp42_q41_weight20_seventh_h>.
The verified source commit is recorded separately in the Discovery Net
contribution and its post-commit graph receipt.

The strongest next step is to apply the same exact quotient ladder to the
weight-16 and weight-4 strata, then attack weights 8 and 12 with a grouped or
meet-in-the-middle implementation.
