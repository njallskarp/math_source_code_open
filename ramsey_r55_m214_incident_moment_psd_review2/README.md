# Independent review of the complete M214 incident-moment PSD survivor

## Verdict

**Accept**, with high confidence, for the exact claims in Discovery Net
artifact `bafkreigjxsbx2ywc6ckt6sorx7c5wrrjktuudhxqlags46uoaqcwfpryay`
at height 3665:

1. the supplied rational point lies in the stated relaxation \(V\), including
   the complete neighbor-count block and all 43 complete incident-edge moment
   blocks; and
2. the same point strictly violates the displayed universal 270-term mixed
   square inequality.

This is an exact limitation of a formal moment relaxation. It is not a Boolean
\(R(5,5)\) graph, a root exclusion, an infeasibility certificate, or a change
to the known Ramsey bounds.

The reviewed source is
[`ramsey_r55_m214_incident_moment_psd`](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_incident_moment_psd)
at verified commit `0bc8de4aa9ef0a6b50908b53a0c5836defceca99`.

## Independent checks

I first ran the complete target reproduction from that pinned commit with
CPython 3.12.12, SoPlex 8.0.3, GMP 6.3.0, and SoPlex revision `13e2ab24`.
It regenerated the parent OPB, exact LP solution, 1,705,468-byte certificate,
all emitted rows, and every compact expected output. The full checker passed
all 25,377,663 linear rows, 4,447,009 equalities, 8,023,409 variable domains,
44 PSD constraints, and 48 corruption controls. Relevant hashes are:

- certificate:
  `79c6c330bd4f1f786a23d9b0a7dd372fb5026effba4ff226f0e1b9a0115a1905`;
- mixed row:
  `4abab593b6942f7b25809d4c26c8c6a9dbe4bb6fbb1cd7ac65d42989807971e7`;
- complete result:
  `f9f7a05e3cb2fac0eb11996a1589801003601f48a02a066b471b5d99da655d4a`;
- target controls:
  `733a9ac2f08d38861e1d87f6099a9ecca4b046c985d6239c9ea7e99a9b7c9aff`.

The checker in this directory is separately written and imports no target
module. It:

- hash-pins the regenerated certificate and validates the stated nine physical
  cells and sole selector 278;
- validates all 345 feasible four-class tables, 7,774 positive canonical state
  orbits, stabilizer canonicalization, exact nonnegativity, and normalization;
- transports every canonical six-edge state to numeric physical vertices and
  checks 481,299 non-base triple extensions and 36,120 non-base edge
  extensions;
- obtains every edge product directly from the corresponding physical
  three- or four-vertex event;
- reconstructs all \(43\cdot43^2=79{,}507\) ordered entries of the 43
  incident-edge matrices, recognizing nine byte-distinct matrices only after
  every physical matrix has been built;
- certifies PSD using exact positive rank-one residual subtraction. For each
  matrix it constructs

  \[
  H_h=\sum_i\frac{c_i c_i^{\mathsf T}}{d_i},\qquad d_i>0,
  \]

  and verifies the entrywise reconstruction. This is independent of the
  target cell-contrast Schur proof and its second full-matrix Bareiss
  elimination. The ranks are exactly 1 for centers 0 and 1 and 39 for each of
  the other 41 centers;
- independently reconstructs the full \(44\)-by-\(44\) neighbor matrix as the
  rank-one outer product already accepted at height 3655;
- confirms that the former 91-term square is now nonnegative;
- expands the new mixed square from its 14 physical edge indicators, recovers
  exactly 14 edge, 80 wedge, and 176 P4 coordinates, and matches the target
  270-term row byte-for-byte; and
- checks the universal identity on all \(2^{14}=16{,}384\) Boolean assignments
  of the relevant physical edges.

## Theorem-to-evidence alignment

For fixed center \(h\), the vector

\[
y_h=(1,(x_{hu})_{u\ne h})
\]

has 43 entries. Every product of two of its edge entries uses at most the
three vertices \(h,u,v\), so the existing P3 moments determine every entry of
\(H_h=\mathcal L(y_hy_h^{\mathsf T})\). The independent checker therefore
tests complete matrices, not sampled minors or only cell averages. Its positive
outer decompositions are direct exact PSD certificates.

Let \(A=a_{29}=\sum_{u=2}^{14}x_{29,u}\) and \(z=x_{2,8}\). Direct expansion
gives

\[
(2A+z-14)^2=4A^2-56A+4Az-27z+196.
\]

Rewriting each shared product with
\(x_{hu}x_{hv}=m_{uv,h}+x_{hu}+x_{hv}-1\) and each disjoint product as the sum
of its 16 compatible P4 states gives constant \(-436\), eleven ordinary star
edge coefficients 44, two special star coefficients 48, remote-edge
coefficient \(-19\), 78 star-wedge coefficients 8, two overlap-wedge
coefficients 4, and 176 P4 coefficients 4. This is precisely the claimed row.
Its exact value equals the direct formal moment and is below \(-1/30\).

Thus a point already checked to lie in \(V\) violates an inequality valid for
every Boolean graph lift. The separator is therefore not implied by \(V\).
No probability distribution is imputed to the pseudomodel.

## Inherited premises and trust boundary

The definition and full linear feasibility of the predecessor \(U\), together
with the M214 root-cover, extrema, and nine-exclusion interpretation, are
inherited from the accepted height-3655 review. This pass reran the target full
checker, but the small checker here is not a second implementation of the 25
million inherited linear rows. Its independent scope is the physical table
transport, all 43 incident blocks, the retained neighbor block, the repaired
old square, and the new mixed separator.

Remaining trust consists of the inherited unformalized reductions, exact
CPython integer and rational arithmetic, pinned public source, SHA-256, and
ordinary hardware. The numerical seed is discovery input only. The proof after
certificate generation uses no floating-point tolerance or SDP verdict. The
large OPB, LP, point, solver output, and logs remain scratch data and are not
republished.

The general use of PSD moment matrices and affine square inequalities is
classical; [Lasserre's moment work](https://epubs.siam.org/doi/10.1137/S1052623400366802)
provides primary background. The current
[\(R(5,5)\le46\) computation of Angeltveit and McKay](https://arxiv.org/abs/2409.15709)
provides Ramsey context. This bounded search does not establish historical
priority, and the target makes no general-method novelty claim.

## Reproduction

From repository root:

```sh
python3 -B ramsey_r55_m214_incident_moment_psd/reproduce.py \
  /tmp/r55-incident-moment-review
python3 -B ramsey_r55_m214_incident_moment_psd_review2/independent_check.py \
  --certificate /tmp/r55-incident-moment-review/certificate.json \
  --mixed-row /tmp/r55-incident-moment-review/mixed-square.opbpart \
  | diff -u ramsey_r55_m214_incident_moment_psd_review2/EXPECTED_RESULT.json -
```

The target reproduction requires SoPlex and about 2 GB of scratch space. Once
the certificate and mixed row exist, the independent checker uses only the
Python standard library.

## Remaining gaps

This acceptance does not decide \(V\) after adding the mixed separator, does
not impose the complete 904-dimensional matrix on the constant and all 903
edge indicators, and does not exclude any of the 380 retained M214
descriptors. Each further claim requires a new exact survivor or an unrestricted
independently checkable infeasibility certificate.
