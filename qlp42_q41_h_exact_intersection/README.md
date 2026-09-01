# Exact H-sum intersection in the QLP-42 q=41 fourth-order branch

This directory intersects the complete q=41 fourth-order axis classification
with the exact component sums

```text
sum(H_A) = 0,     sum(H_B) = 1.
```

It uses the universal exact-sum-one syndrome equation from the preceding
`qlp42_q41_hyperplane_equation` certificate.

## Theorem

Start with the 1,717,504,656 labeled axis pairs (81,785,936 pairs modulo
cyclic rotation of family B) that lift through the complete fourth-order
autocorrelation residue system in the q=41 branch.

The two exact H-sum equations first require `wt(b) = 0 mod 4`. Among the
fourth-order survivors satisfying that necessary condition there are

```text
428,622,432 labeled axis pairs,
 20,410,592 B-rotation axis orbits.
```

Intersecting their fourth-order sign systems with both exact H sums leaves
exactly

```text
218,347,920 labeled axis pairs,
 10,397,520 B-rotation axis orbits.
```

The rank-stratified result is:

| rank of `D_b` | fourth-order labeled pairs with `wt(b)=0 mod 4` | fourth-order orbits | exact-H labeled pairs | exact-H orbits |
|---:|---:|---:|---:|---:|
| 0  | 0 | 0 | 0 | 0 |
| 3  | 0 | 0 | 0 | 0 |
| 4  | 168 | 8 | 0 | 0 |
| 6  | 6,552 | 312 | 0 | 0 |
| 7  | 90,720 | 4,320 | 0 | 0 |
| 9  | 32,937,408 | 1,568,448 | 20,554,128 | 978,768 |
| 10 | 395,587,584 | 18,837,504 | 197,793,792 | 9,418,752 |

Thus the exact H sums eliminate every rank-4, rank-6, and rank-7 axis pair.
Only ranks 9 and 10 remain at this layer.

## Reduction to an A-side parity test

Let `r_H(a,b)` be the fourth-order affine residual and `U_H(a)` the image of
the ten free reflected-pair sign flips in family A. The preceding exact
multiplicity theorem establishes, on every fourth-order survivor,

```text
U_H(a) subset image(D_b),     r_H(a,b) in image(D_b).
```

For `wt(b)=0 mod 4`, the universal H_B sum-one equation is

```text
T_b = {t in image(D_b) : parity(t)=0}.
```

Direct fourth-order Gaussian arithmetic shows that every column of `U_H(a)`
has even coordinate parity. The exhaustive grouped certificate also checks
that every surviving residual `r_H(a,b)` has even parity. Therefore, for
every A-pair sign choice, the required B syndrome lies in `T_b`. Once the
axis pair survives fourth order and `wt(b)=0 mod 4`, H_B contributes no
further obstruction beyond the universal parity equation.

It remains only to decide whether the reflected A word can sum to zero. A
pair with third-order sign XOR one contributes zero. A pair with XOR zero
contributes either `+2` or `-2` on its prescribed real or imaginary axis.
Consequently `sum(H_A)=0` is attainable if and only if the number of active
XOR-zero pairs is even on each axis. When the counts are even, flipping
exactly half the active pairs on each axis constructs a witness.

The verifier applies this criterion to every grouped fourth-order survivor,
giving the exact counts above.

## Reproduction

The primary verifier pins the SHA-256 of the complete fourth-order rank
verifier, rebuilds its A systems, and re-enumerates every length-21 B-axis
rotation orbit rather than importing survivor counts.

```sh
python3 verify_q41_h_exact_intersection.py
python3 independent_sample_check.py
sha256sum -c SHA256SUMS
```

The canonical 585-group stream records rank, autocorrelation signature,
orthogonal image, B word/orbit multiplicities, the full fourth-order
A-survivor mask, and the exact-H A-survivor mask. Its SHA-256 is

```text
bf8861cb10501ad1daf0ff119d88e95ade9502fc43c44919e738779aade2bcee
```

The independent checker reimplements Gaussian arithmetic, PAFs, reflected
axes, third-order XORs, and pair flips without importing the predecessor. On
512 deterministic A/signature pairs it directly enumerates all 1,024 pair
flip masks to check the sum-zero criterion and directly recomputes 5,120
fourth-order pair-direction columns to check even parity.

Tested with Python 3.12.12 on arm64 macOS 26.2. The complete verifier takes
about two minutes on the recorded machine and uses only the standard library.

## Scope and trust boundary

This is an exact finite classification inside the complete fourth-order
autocorrelation relaxation plus the two H component sums. It does not yet
impose the exact S_A and S_B sums or the full integral nonzero-shift
autocorrelation equations, and it does not settle QLP-42. The aggregate
classification trusts the pinned predecessor, Python integer/set semantics,
the grouped enumeration, compiler/interpreter, operating system, and hardware.
The independent audit checks the new local criterion but is sampled rather
than a second aggregate implementation. No floating point, randomness in the
proof path, SAT status, or historical-priority claim is used.
