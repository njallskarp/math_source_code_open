# QLP-42 q=41 exact-sum hyperplane equation

This directory gives a closed equation and reproducible certificate for the
exact-sum-one syndrome hyperplanes in the length-21 compressed `H_B` branch of
the QLP-42 search.

## Theorem

Let `b` and `sigma` be elements of `F_2^21`, with indices modulo 21, and define

```text
D_b(sigma)_s = sum_j (sigma_j + sigma_{j+s})(b_j + b_{j+s}) in F_2,
1 <= s <= 10.
```

Write

```text
T_b = {D_b(sigma) : sum_j (-1)^sigma_j i^b_j = 1}.
```

For every even-weight `b`,

```text
T_b = {t in im(D_b) : t_1 + ... + t_10 = wt(b)/2 (mod 2)}.       (1)
```

Thus the normal is universal: in ten-bit syndrome notation it is `0x3ff`.
For nonzero even `b`, this functional is nonzero on `im(D_b)`, so (1) is a
codimension-one affine hyperplane. For `b=0`, both sides are the singleton
`{0}`.

## Short proof of the equation

The coefficient of `sigma_k` in the sum of all ten syndrome coordinates is

```text
sum_{s=1}^{10} (b_{k+s} + b_{k-s})
  = sum_{ell != k} b_ell
  = b_k,
```

where the last equality uses the even weight of `b`. Hence

```text
sum_s D_b(sigma)_s = b dot sigma.                                (2)
```

The exact Gaussian sum condition says that precisely `wt(b)/2` imaginary-axis
positions have negative sign. Therefore `b dot sigma = wt(b)/2 (mod 2)`, and
(2) proves that `T_b` is contained in the right side of (1).

Equivalently, the XOR of the ten rows of `D_b` is `b`, or
`D_b^T(1,...,1)=b`. Consequently the displayed functional is nonzero on the
image whenever `b` is nonzero. The preceding exhaustive syndrome theorem
establishes that `T_b` already has half the size of `im(D_b)` for positive
rank, so the containment is equality. The C++ verifier here independently
recomputes all exact syndrome fibers and checks equality directly.

## Certificate

`verify_hyperplane_equation.cpp` visits one canonical (least integer) member of
every rotation orbit. For all 49,940 even-axis orbits it:

- checks that the XOR of the ten matrix rows equals `b`;
- computes `im(D_b)` exactly;
- recomputes every exact-sum-one fiber using integer Krawtchouk coefficients
  and a 1,024-point Walsh transform;
- checks fiber support against equation (1) syndrome by syndrome; and
- emits, on `--stream`, a canonical record consisting of the axis word, orbit
  size, rank, least syndrome origin, universal normal, and right-hand side.

The independent Python program does not use Krawtchouk coefficients or Walsh
inversion. It reconstructs the complete canonical stream from the matrix image,
matches its SHA-256 digest, and uses fixed-cardinality subset-XOR dynamic
programming to reconstruct the exact supports for 256 deterministic axis words
covering all eight ranks.

The canonical stream has SHA-256

```text
03494099cbe4c7baff54bb27ebb1808af123badc133cf24d6b544bb441d9b2e7
```

Its header and record format are:

```text
axis_word<TAB>orbit_size<TAB>rank<TAB>origin<TAB>normal<TAB>rhs
```

Hexadecimal fields use lowercase fixed widths of six, three, and three digits.
The stream contains 49,940 data records and is generated rather than stored.

## Reproduction

On macOS with the Command Line Tools libc++ headers:

```sh
SDK_CPP="$(xcrun --show-sdk-path)/usr/include/c++/v1"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  -isystem "$SDK_CPP" verify_hyperplane_equation.cpp \
  -o verify_hyperplane_equation
./verify_hyperplane_equation
./verify_hyperplane_equation --stream | shasum -a 256
python3 independent_digest_check.py
sha256sum -c SHA256SUMS
```

Tested with Apple clang 17.0.0 and Python 3.12.12 on arm64 macOS 26.2.

## Scope and trust boundary

The equation has an elementary proof once the earlier cardinality theorem is
available. The direct exhaustive equality check additionally trusts the C++20
compiler, integer semantics, Walsh implementation, operating system, and
hardware. The Python digest reconstruction is implementation-independent for
the matrix image and canonical data, while its direct support audit is sampled
rather than exhaustive. This result identifies the exact finite q=41
hyperplane interface; it does not establish a general-length equality or settle
existence of a quaternary Legendre pair of length 42. No historical-priority
claim is made.
