# Exact ten-cell excess partition for the complete R(5,5;43) M=214 OPB

## Result and scope

This directory extends the certified selection-ordered M=214 formula from
Discovery Net height 2563 by 97 deterministic variables and 638 constraints.
The output is one integrated OPB with ten case selectors `y_0,...,y_9` and the
proof-checked equality

```text
y_0+...+y_9=1.
```

Official VeriPB 3.0.2 checks the transformation as `EQUISATISFIABLE FILE`.
Thus the ten cases cover the complete labeled M=214 branch after the already
certified within-cell ordering; they are not selected core-pair instances.

This is a complete finite decomposition, not a decision of the branch.  The
proof deliberately concludes `NONE`: it supplies neither a Ramsey graph nor an
UNSAT certificate and establishes no new Ramsey bound.  Generated 168 MB OPB
files, proof files, binaries, and negative fixtures are not committed.

## Arithmetic dichotomy

Let `E={0,...,12}` be the degree-20 class, let anchor `13` be normalized as at
height 2505, and put

```text
a_v = |N_R(v) intersect E|.
```

The thirteen degree-20 equalities give

```text
sum_v a_v = 13*20 = 260.
```

Every base row has `a_v>=6`, so there are exactly two excess units and
`6<=a_v<=8`.  The normalized anchor has `a_13=6`.  Also

```text
sum_{v in E} a_v = 2e(E).
```

Writing `x_E=sum_{v in E}(a_v-6)`, parity and `0<=x_E<=2` force

```text
x_E=0, e(E)=39,  or  x_E=2, e(E)=40.
```

In the first case both excess units are central; in the second both are in
`E`.  No third class is possible.

## Ten ordered patterns

The height-2563 cells are

```text
P0=0..5, P1=6..12, P2=14..28, P3=29..42.
```

The proof first derives the adjacent inequalities `a_i<=a_j` in each cell
from the certified mixed-radix key comparisons.  It weakens at most 58
lower-signature variables per comparison, removes at most 3072 units of
positive normalized surplus, and applies Boolean division by 4096.  Define

```text
u_v = [a_v>=7],   w_v = [a_v>=8].
```

The transformation proves `a_v=6+u_v+w_v`, the exact global equality
`sum_v(u_v+w_v)=2`, the exceptional incidence equality

```text
2e(E)-sum_{v in E}(u_v+w_v)=78,
```

and monotonicity of `u,w` inside every cell.  A class bit `q` is defined as
`u_5 OR u_12`; the dichotomy shows that, on every valid model, `q=[e(E)=40]`.

For either active pair of cells, two excess units have exactly five ordered
forms:

1. one `a=8` at the left-cell tail;
2. one `a=8` at the right-cell tail;
3. two `a=7` values at the left-cell tail;
4. one tail `a=7` in each cell;
5. two `a=7` values at the right-cell tail.

This gives five `q=1` exceptional patterns and five `q=0` central patterns.
The selector extension uses a priority chain so totality and at-most-one also
hold syntactically outside the M=214 arithmetic domain.  On valid models the
ten mathematical conditions are mutually exclusive, so the priority selectors
coincide with those ten conditions.  The independent C++ audit enumerates all
946 placements of two indistinguishable excess units; after anchor, parity, and
cell-order filters, exactly ten states remain, one per selector.

## Reproduction

The input must be the ordered OPB of the sibling
`ramsey_r55_m214_certified_selection_ordering` directory, SHA-256

```text
d621bf525bd6e3525ef5f9ccc741dc01c66a07f39b3db4c5e63741190d75eebc.
```

Tested with CPython 3.12.12, Apple clang 17.0.0, Rust 1.92.0, and official
VeriPB tag 3.0.2 at commit
`c648bac06be995b82bd218e248f005140fc8ce11`.  In a clone containing the three
sibling directories, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ../ramsey_r55_m214_complete_formulation/generate_opb.py \
  --output /tmp/r55_m214_complete.opb

PYTHONDONTWRITEBYTECODE=1 python3 \
  ../ramsey_r55_m214_certified_selection_ordering/generate_certificate.py \
  --input /tmp/r55_m214_complete.opb \
  --output /tmp/r55_m214_selection_ordered.opb \
  --proof /tmp/r55_m214_selection_ordering.pbp

PYTHONDONTWRITEBYTECODE=1 python3 generate_partition.py \
  --input /tmp/r55_m214_selection_ordered.opb \
  --output /tmp/r55_m214_excess_partition.opb \
  --proof /tmp/r55_m214_excess_partition.pbp

xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  -isystem /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1 \
  check_partition.cpp -o /tmp/r55_check_excess_partition

/tmp/r55_check_excess_partition \
  /tmp/r55_m214_selection_ordered.opb \
  /tmp/r55_m214_excess_partition.opb \
  /tmp/r55_m214_excess_partition.pbp

/path/to/veripb-3.0.2 \
  /tmp/r55_m214_selection_ordered.opb \
  /tmp/r55_m214_excess_partition.pbp \
  /tmp/r55_m214_excess_partition.opb

shasum -a 256 \
  /tmp/r55_m214_excess_partition.opb \
  /tmp/r55_m214_excess_partition.pbp
```

Compare with `EXPECTED_OUTPUT.txt`.  The independent checker imports no Python
code: it byte-compares all 1,974,963 inherited rows, reconstructs all 638
appended rows from the mathematical definitions, audits the proof-command
census, and runs the 946-placement exact-cover check.

For deterministic rejection fixtures:

```bash
fixture_dir=$(mktemp -d /tmp/r55-excess-negative.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 make_negative_fixtures.py \
  --formula /tmp/r55_m214_excess_partition.opb \
  --proof /tmp/r55_m214_excess_partition.pbp \
  --output-directory "$fixture_dir"
```

The C++ checker rejects `corrupt_formula.opb` (the final one-hot right side is
changed from 1 to 2), and VeriPB rejects `corrupt_proof.pbp` (the first
threshold witness is changed from 0 to 1).

## Trust boundary

Trusted are the height-2505 graph-to-base-OPB equivalence and its inherited
extremal inputs; the independently accepted height-2563 selection ordering;
the displayed parity and ordered-excess argument; VeriPB 3.0.2 and its proof
rules; CPython exact integers; the C++ and Rust compilers/libraries; ordinary
hardware; and SHA-256 collision resistance.  The C++ reconstruction reduces
correlated generator risk but does not implement VeriPB or re-formalize the
height-2505 graph reduction.  No solver decision, generated artifact absent
from the stated hashes, or future subinstance result is trusted.

