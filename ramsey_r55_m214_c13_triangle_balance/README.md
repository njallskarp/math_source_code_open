# An all-marking triangle-balance mechanism for the \(M=214,c=13\) branch

## Result

This directory proves two exact outside-triangle identities for the normalized
two-anchor \(c=13\) branch of a hypothetical 43-vertex \((5,5)\)-Ramsey graph.
They hold simultaneously for every placement of the thirteen degree-20 marks
and the unique incidence-eight pivot.

For an outside vertex \(x\), let \(S_x\) be its red footprint in the
13-vertex common-red core \(H\). Let \(k=|E\cap H|\), let
\(\delta=1\) when the pivot lies in \(H\), and put

\[
X=\sum_{x\in A\cup B}|S_x|,
\qquad
P=\sum_{x\in W}e_H(S_x),
\qquad
Q=\sum_{x\in W}e_{\overline H}(H\setminus S_x).
\]

Then every complete candidate must satisfy

\[
T_R(W)=33+7k+X+P,
\qquad
T_B(W)=119-7k+2\delta+Q.
\]

The proof in [PROOF.md](PROOF.md) is a double count, not a solver inference.
It also derives four reusable Ramsey-capacity bounds from \(R(3,5)=14\).

The compact certificate instantiates the earlier pairwise-interface witness.
Its footprint statistics require outside-triangle counts \((360,413)\), while
direct enumeration finds \((318,455)\). The exact discrepancy is therefore
\((-42,+42)\). This rejects that witness at a single aggregate layer that
couples all 28 outside vertices. It does **not** exclude the complete \(c=13\)
branch or prove \(R(5,5)\leq43\).

## Certificate format

The normalized vertices are \(u,v,H_0,\ldots,H_{12},W_0,\ldots,W_{27}\).
The core is cyclic, with \(H_iH_j\) red exactly when
\(i-j\pmod {13}\in\{1,5,8,12\}\). The outside ordering is
\(A_0,\ldots,A_6,B_0,\ldots,B_6,O_0,\ldots,O_{13}\).

In `certificate.json`:

- `core_e` and `outside_e` identify the degree-20 marks;
- each four-digit hexadecimal `footprints` entry is a 13-bit red-core mask;
- `outside_red_bits` encodes the 378 lexicographically ordered outside pairs,
  with pair rank zero at the least significant bit; and
- `pivot` identifies the unique marked vertex with eight red \(E\)-neighbors.

The Python verifier parses this external certificate. The C++20 checker instead
embeds the data and reconstructs every quantity with independent nested loops.

## Reproduction

The recorded environment used CPython 3.12.12 and GNU g++ 16.2.0. No external
package or solver is required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py certificate.json \
  | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_certificate.py \
  | cmp - EXPECTED_TEST_OUTPUT.txt
g++-16 -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror \
  independent_check.cpp -o /tmp/r55_c13_balance_check
/tmp/r55_c13_balance_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

For a sanitizer replay:

```bash
g++-16 -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror -fsanitize=address,undefined -fno-omit-frame-pointer \
  independent_check.cpp -o /tmp/r55_c13_balance_check_san
/tmp/r55_c13_balance_check_san
```

The verifier checks all 43 red degrees and \(E\)-incidences, both anchor
triangle colors, the core census, the balance and capacity data, and all
\(\binom{43}{5}=962{,}598\) five-sets. Five deterministic certificate
corruptions must be rejected.

## Expected compact result

```text
E_core=0, delta=0, X=96, P=231, Q=294
outside triangles: actual red=318, blue=455; required red=360, blue=413
balance discrepancy: red=-42, blue=+42
capacity maxima: 12, 8, 3, 3
status: VERIFIED C13 OUTSIDE-TRIANGLE BALANCE OBSTRUCTION
```

## Trust boundary

Trusted are the normalized \(c=13\) hypotheses stated in
[PROOF.md](PROOF.md), the displayed finite double count, the 399-byte
certificate, the short Python verifier, the source-independent C++20 checker,
language semantics, ordinary hardware, and SHA-256 collision resistance. The
cyclic-core normalization inherits the separately recorded catalogue-uniqueness
trust boundary.

No SAT, PB, MILP, or CP solver; generated formula; timeout; private database;
raw search state; binary; catalogue payload; or credential is trusted by this
claim. The certificate itself is not asserted to be a Ramsey graph.

## Primary context

- Brendan McKay's [Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  provides the primary catalogue context for small Ramsey graphs.
- Stanisław Radziszowski's current
  [Dynamic Survey of Small Ramsey Numbers](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1)
  supplies the literature context for \(R(5,5)\).
