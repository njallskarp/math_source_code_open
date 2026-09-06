# A core-exact survivor of the \(M=214,c=13\) aggregate interface

## Claim and scope

This directory gives an exact 43-vertex colored graph satisfying a stronger
relaxation of the normalized \(M=214,c=13\) two-anchor branch than the
height-2969 pairwise witness. It has:

```text
red degrees                         20^13 21^30
red E-incidences                    6^42 8^1
red/blue local triangles at u,v,H   exact at all 15 vertices
global red/blue triangles           1403,1463
outside red/blue triangles          360,413
pairwise forced colors              53 red,16 blue
monochromatic K5s with <=2 outside  0
```

Its footprints also satisfy all four capacity inequalities from the
all-marking triangle-balance lemma. Consequently, the entire aggregate
balance plus individual anchor/core triangle layer does not eliminate this
fixed \(k=0\) interface.

This is a counterexample to the sufficiency of that relaxation. It is
emphatically **not** a \((5,5)\)-Ramsey graph, not an exclusion of the complete
\(c=13\) branch, and not a Ramsey-number bound. Only three outside vertices
have their required local triangle counts. The complete \(K_5\) census finds
monochromatic sets using three, four, and five outside vertices.

The same footprints were already eliminated from the full problem by the
independent height-2993 triple obstruction. The point here is different and
narrow: even after adding every anchor and core triangle equation and both
global color totals, the aggregate/core-slice relaxation remains feasible.
This closes that relaxation mechanism and identifies the unresolved
individual outside-triangle vector as essential.

## Certificate

Normalize the red anchor edge as \(uv\). Its common-red core \(H\) is the
cyclic graph on \(\mathbb Z/13\mathbb Z\), with

\[
i\sim j
\quad\Longleftrightarrow\quad
i-j\in\{1,5,8,12\}\pmod {13}.
\]

The 28 outside vertices are ordered
\(A_0,\ldots,A_6,B_0,\ldots,B_6,O_0,\ldots,O_{13}\). In
`certificate.json`:

- `core_e` and `outside_e` identify the thirteen degree-20
  vertices;
- each `footprints` entry is a 13-bit red-core mask;
- `outside_red_bits` encodes the 378 lexicographically ordered
  outside pairs, with pair rank zero at the least significant bit; and
- `pivot` identifies the unique marked vertex with eight red
  \(E\)-neighbors.

The certificate is 399 bytes and has SHA-256
`4df751975287926a6b882d1a590ad60f4cef0bb0609be1f0ae39e6c789ae9c16`.

The 15 anchor/core vertices all have local red and blue count 100. The three
exact outside vertices are global labels 35, 36, and 40. The ordered list of
the other 25 outside red/blue deviations has SHA-256
`e866221e98359771d46a66d91bace27d4436d0087ecc9e4cd1d91dfd49b3514b`.
The deviations sum to zero in each color, which is why both global totals are
exact despite the individual failures.

The monochromatic-five-set census is:

```text
outside vertices     0   1   2    3    4    5
red K5               0   0   0  184  162   35
blue K5              0   0   0   43  173   67
```

## Construction mechanism

`search_switches.cpp` starts from the height-2969 outside graph.
Partition the outside vertices into the six groups determined by anchor cell
\(A,B,O\) and mark status \(E,\overline E\). A move chooses four vertices in
one group or two vertices in each of two groups, removes one red perfect
matching, and inserts the other.

Every such \(2\times2\) switch preserves:

- every outside red degree;
- every outside red \(E\)-incidence;
- every \(A/B/O\) block edge total and hence all anchor triangle equations;
- all footprints and core column equations.

The search discards any switch that removes a footprint-forced red pair or
inserts a footprint-forced blue pair. Its exact integer objective is zero
precisely when all thirteen core red local-triangle counts equal 100 and the
outside red triangle count equals 360. The fixed seed reaches the included
certificate at restart 8, step 1,906,249.

The stochastic search is construction machinery, not evidence. Both checkers
reconstruct the final graph directly without replaying or trusting the search.

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
g++-16 -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror independent_check.cpp -o /tmp/r55_c13_core_exact_check
/tmp/r55_c13_core_exact_check | cmp - EXPECTED_INDEPENDENT.txt
g++-16 -std=c++20 -O3 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror search_switches.cpp -o /tmp/r55_c13_core_exact_search
/tmp/r55_c13_core_exact_search | cmp - EXPECTED_SEARCH.txt
shasum -a 256 -c SHA256SUMS
```

For sanitizer replays:

```bash
g++-16 -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror -fsanitize=address,undefined -fno-omit-frame-pointer \
  independent_check.cpp -o /tmp/r55_c13_core_exact_check_san
/tmp/r55_c13_core_exact_check_san
g++-16 -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror -fsanitize=address,undefined -fno-omit-frame-pointer \
  search_switches.cpp -o /tmp/r55_c13_core_exact_search_san
/tmp/r55_c13_core_exact_search_san
```

The Python verifier parses the external certificate, reconstructs every
equation above, and enumerates all
\(\binom{43}{5}=962{,}598\) five-sets. Five deterministic certificate
corruptions are rejected. The C++20 checker embeds the footprint and outside
adjacency data, uses fixed-width masks and nested loops, and independently
reconstructs the complete census.

## Trust boundary and stopping condition

Trusted are the accepted normalized \(c=13\) quotient and branch equations,
the 399-byte certificate, either short checker and its language toolchain,
ordinary hardware, and SHA-256 collision resistance. The cyclic-core
isomorphism normalization inherits its separately recorded McKay
catalogue-uniqueness trust boundary.

No search trajectory, pseudorandom generator quality, solver, generated
formula, timeout, private database, catalogue payload, raw state, binary, log,
or credential is evidence. Reproducing the search explains the construction;
checking the final certificate proves the scoped counterexample.

This endpoint freezes the aggregate/core-slice mechanism. A further \(c=13\)
step must couple all 28 individual outside triangle equations or use a
genuinely different complete mechanism. Another aggregate statistic, fixed
marking, or search-only failure is not continuation.
