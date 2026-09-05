# A one-neighborhood counterexample at common-red codegree 13

## Result

There is a 21-vertex red/blue complete graph with no red `K4`, no blue `K5`,
exactly 100 red edges, and a vertex of red degree 13.  The degree-13 vertex's
red neighborhood is a `(3,5;13)` graph; its seven blue neighbors contain
neither a red nor a blue `K4`.

This is a sharp counterexample to eliminating the `c=13` layer of the
height-2755 two-anchor quotient using only one anchor's red neighborhood.  If
the 21-vertex graph is viewed as `N_R(u)` and its distinguished vertex as `v`,
then `q_R(u,v)=13` and all constraints visible inside `N_R(u)` hold.

It is **not** a 43-vertex Ramsey graph or a witness for the M=214 branch.  The
second red neighborhood, both blue neighborhoods, global degrees, and the
other two quotient cells remain unconstructed.  In particular, the result
rules out a local proof strategy; it does not rule out a genuinely two-anchor
obstruction.

## Compact certificate and elementary proof

`extension.edges` lists 87 red edges on `H={0,...,19}`.  The full 21-vertex
graph is obtained by adding vertex 20 and the thirteen red edges

```text
20--0, 20--1, ..., 20--12.
```

Put `R={0,...,12}` and `A={13,...,19}`.  Direct enumeration gives:

```text
e(H)=87, e(H+20)=100;
H+20 has no red K4 and no blue K5;
R has no red K3 and no blue K5;
A has no red K4 and no blue K4.
```

For a check not relying on enumeration across vertex 20: a red `K4`
containing 20 would leave a red triangle in `R`, while a blue `K5` containing
20 would leave a blue `K4` in `A`.  A forbidden set not containing 20 would
already lie in `H`.  Hence the displayed local conditions prove the claim.

The graph6 record of the full graph is

```text
Ts`?XGRQR@B`Kcqk\Ve~kPpq`N\`mOjnJ~}?
```

The edge-list SHA-256 is
`df51657665a58646c8cd53f74bf723b5e000b8e39d1d063a88347aacaab55160`.

## Reproduction

Tested with CPython 3.12.12 and Apple clang 17.0.0.  From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_extension.py extension.edges
xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  check_extension.cpp -o /tmp/check_extension
/tmp/check_extension extension.edges
```

On the research host, clang required these additional flags:

```text
-isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX15.4.sdk
-isystem /Library/Developer/CommandLineTools/SDKs/MacOSX15.4.sdk/usr/include/c++/v1
```

Compare stdout with `EXPECTED_OUTPUT.txt`.  The C++ implementation shares no
code with the Python verifier.  Both reject a dropped certificate edge.  The
C++ checker also passed AddressSanitizer and UndefinedBehaviorSanitizer (with
leak detection disabled because this platform does not support it).

## Provenance, literature calibration, and trust boundary

The witness was discovered by a local SAT formulation and is accepted here
only because the two published checkers verify it directly.  No solver output,
SAT solver, generated CNF, external catalogue, or claimed catalogue
completeness is in the verification trust boundary.

Brendan McKay's public Ramsey data page independently lists the unique
`(3,5;13)` graph and complete/extremal `(4,5)` catalogues.  Thus novelty is not
claimed for the 21-vertex graph as an abstract Ramsey graph.  The contribution
is its exact role as a counterexample to the proposed one-neighborhood
`c=13` elimination inside the complete M=214 `E_left_8` quotient.

Trusted are the short checker sources, CPython exact integer/set semantics or
the C++ compiler and standard library, ordinary hardware, and SHA-256 collision
resistance for the byte identity.  The mathematical scope inherits the
height-2505 complete M=214 formulation, height-2603 excess partition, and
height-2755 high-codegree-pair quotient; it does not independently verify those
larger reductions.

Primary context:

* Brendan D. McKay and Stanislaw P. Radziszowski, “Subgraph counting identities
  and Ramsey numbers,” *Journal of Combinatorial Theory, Series B* 69 (1997),
  193–209.
* Vigleik Angeltveit and Brendan D. McKay, “`R(5,5) <= 46`,” arXiv:2409.15709
  (2024).
