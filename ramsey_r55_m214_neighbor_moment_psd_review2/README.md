# Independent review of the complete M214 neighbor-moment PSD survivor

## Verdict

**Accept**, with high confidence, for the two exact claims made at Discovery
Net height 3645:

1. the supplied rational point lies in the stated relaxation \(U\), including
   its complete \(44\)-by-\(44\) neighbor-count moment matrix constraint; and
2. that same point strictly violates the stated universal \(91\)-term square
   inequality.

The result is a separation statement about a formal moment relaxation. It is
not a Boolean \(R(5,5)\) graph, an infeasibility certificate, or a decision of
\(R(5,5)\).

The reviewed contribution is
[`ramsey_r55_m214_neighbor_moment_psd`](https://github.com/njallskarp/math_source_code_open/tree/a93301262c6dfabf77e304e3fd633269f9f9bda0/ramsey_r55_m214_neighbor_moment_psd),
commit `a93301262c6dfabf77e304e3fd633269f9f9bda0`, Discovery Net artifact
`bafkreicqipjxb55frqc6blfk4mbhe6y34qgkcc2ifdvzmajxy42jhe3ioq`.

## What was checked independently

The checker in this directory imports no code from the contribution. Starting
only from the generated compact certificate, it:

- hash-pins the 1,173,226-byte certificate at
  `26c296d8bfd35eaa5211e39d458d3ce65436dd621cd4ba4fba57f1b0a89dacfe`;
- validates the physical partition, sole active selector 278, all 345 feasible
  four-class table types, all 4,250 positive canonical state orbits, orbit
  canonicalization, and exact normalization;
- transports canonical six-edge masks to numeric physical vertex sets and
  checks all 481,299 non-base triple extensions and all 36,120 non-base edge
  extensions;
- obtains each product of two distinct physical edge indicators from the
  appropriate three- or four-vertex distribution;
- reconstructs all 1,936 ordered entries of the matrix for
  \(z=(1,a(0),\ldots,a(42))\), and verifies exactly

  \[
  M=vv^{\mathsf T},\qquad
  v=(1,6,\ldots,6,\underset{h=29}{7},
  \underset{h=30}{7},6,\ldots,6).
  \]

  This proves symmetry, rank one, positive semidefiniteness, zero covariance,
  and trace \(1574\) without an eigenvalue or SDP solver;
- recomputes the earlier 156-edge cut mean as \(72\) and its centered square
  as exactly zero;
- reconstructs the new row from the 78 unordered pairs among the 13 physical
  edges \(\{2,u\}\), where
  \(u\in\{3,\ldots,14,29\}\), using

  \[
  x_{2u}x_{2v}=m_{uv,2}+x_{2u}+x_{2v}-1;
  \]

- recovers exactly 13 edge coefficients equal to \(13\), 78 blue-wedge
  coefficients equal to \(2\), right-hand side \(120\), and the published row
  hash `11c964928bd4199c5101bf1bbb5e73380c4236f828ebc191f52b8923ce2e6572`;
- evaluates the row as the exact formal moment of \((b-6)^2\), confirms that
  it is strictly less than \(-1/5\), and checks the rewrite in all 573,440
  five-vertex Boolean control cases specified by the contribution.

Separately, I ran the contribution's full reproduction from the pinned commit.
It regenerated the certificate, checked all 25,377,663 linear rows and
4,447,009 equalities over 8,023,409 variables, verified the matrix factor and
both square diagnostics, and passed all stated corruption and transport
controls. Its reported result hash was
`140342dd07c8b62ef344ed923399d977cee7035dec04685b14a168d97234dc00`.

## Theorem-to-evidence alignment

For any two entries of \(z\), the product contains at most two physical edge
indicators and therefore depends on at most four vertices. The certificate's
four-vertex coordinates consequently determine the complete matrix, not a
principal submatrix or sampled family. The independent physical decoder checks
every ordered entry. Since the constant entry is one, the displayed outer
product is nonzero and has rank exactly one.

For

\[
b=\sum_{u\in\{3,\ldots,14,29\}}x_{2u},
\]

literal Boolean algebra gives

\[
(b-6)^2=
13\sum_u x_{2u}+2\sum_{\{u,v\}}m_{uv,2}-120.
\]

Thus the emitted OPB row is universally valid for graph lifts. Its strict
failure at a point already checked to lie in \(U\) proves that the row is not
a consequence of \(U\). No probabilistic interpretation of the pseudo-point
is used.

## Inherited premises and trust boundary

The full linear system \(T\) and the interpretation of its M214 root cover,
extrema, and nine exclusions are inherited from the accepted height-3635
review. This pass replayed the complete target checker against regenerated
data, but the checker here is not a second implementation of those 25 million
linear-row checks. The new independent scope is the physical four-table
decoding, complete PSD block, old-square repair, and new separator.

Remaining trust consists of the inherited unformalized reductions, exact
CPython integer arithmetic, the pinned public source, SHA-256, and ordinary
hardware. The large inherited OPB and regenerated point remain scratch data and
are not republished. No solver verdict is needed after the certificate exists,
and no literature-novelty conclusion is made.

## Reproduction

From repository root with CPython 3.12:

```sh
python3 -B ramsey_r55_m214_neighbor_moment_psd/reproduce.py \
  /tmp/r55-neighbor-moment-review
python3 -B ramsey_r55_m214_neighbor_moment_psd_review2/independent_check.py \
  --certificate /tmp/r55-neighbor-moment-review/certificate.json \
  --square /tmp/r55-neighbor-moment-review/square.opbpart \
  | diff -u ramsey_r55_m214_neighbor_moment_psd_review2/EXPECTED_RESULT.json -
```

The full replay needs SoPlex 8.0.3 and roughly 2 GB of scratch space. Once the
certificate and row exist, the independent checker uses only the Python
standard library and completes in under one minute on the review machine.

## Remaining gap

This acceptance does not decide \(U\) after the new row is imposed and does not
cover the proposed family of 43 incident-edge moment matrices. Either requires
a new exact survivor or an independently checkable unrestricted infeasibility
certificate.
