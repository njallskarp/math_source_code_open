# A forced high-codegree anchor pair in the M=214 `E_left_8` cell

## Result

Assume a red/blue coloring of `K_43` has no monochromatic `K_5` and lies in
the complete M=214 `E_left_8` cell.  Thus `E={0,...,12}` is the red-degree-20
class, vertex 5 is the unique member with `a_5=8`, every other vertex has
`a_v=6`, and the fixed degree-21 anchor `u=13` has

```text
N_R(u) intersect E = {0,...,5},
N_R(u) intersect C = {14,...,28},
t_R(u) = 100,
```

where `C={13,...,42}`.  Then some `v` in `{14,...,28}` has at least nine
common red neighbours with `u`.

Consequently the whole labeled cell is equisatisfiable with a disjunction of
60 canonical pair-root types.  This is a structural quotient mechanism, not a
SAT result: none of the 60 roots is claimed satisfiable or unsatisfiable, and
no Ramsey bound follows yet.

## Proof of the codegree-nine bound

For a red edge `xy`, put `q_R(x,y)=|N_R(x) intersect N_R(y)|`.  Its common red
neighbourhood contains no red triangle, since such a triangle together with
`x,y` would be a red `K_5`; it contains no blue `K_5` by the global
hypothesis.  The classical exact value `R(3,5)=14` therefore gives
`q_R(x,y)<=13`.

Double-count the red edges in `G_R[N_R(u)]` by their endpoints:

```text
sum_{v in N_R(u)} q_R(u,v) = 2 t_R(u) = 200.
```

Only six red neighbours of `u` lie in `E`, so their total contribution is at
most `6*13=78`.  The other fifteen red neighbours lie in `C` and contribute
at least 122.  If all fifteen had codegree at most eight, the complete sum
would be at most `78+15*8=198`, a contradiction.  Hence one central red
neighbour has codegree `c` in `{9,10,11,12,13}`.

## Complete 60-type quotient

Use the residual `S_15` symmetry on `{14,...,28}` to name a qualifying
partner `v=14`.  Let

```text
s = 1 if v is red-adjacent to the exceptional vertex 5, otherwise 0;
k = |N_R(v) intersect {0,...,4}|;
p = s+k = |N_R(u) intersect N_R(v) intersect E|.
```

The residual `S_5 x S_7` action on `{0,...,4}` and `{6,...,12}` has exactly
the twelve orbits `(s,k)` with `s in {0,1}` and `k in {0,...,5}`.  This is
complete because `v` has exactly six red neighbours in `E`, leaving
`6-p` in `{6,...,12}`.  For fixed `c,p`, the four adjacency cells of the
remaining vertices have sizes

```text
                         both red   u only   v only   both blue
E (13 vertices)              p       6-p      6-p       1+p
C minus {u,v} (28)         c-p    14-c+p   14-c+p       c-p.
```

The residual `S_14 x S_14` action on the two central anchor cells is
transitive on choices with those sizes.  Thus each of the five possible `c`
values and twelve `(s,k)` values gives one canonical partner neighbourhood:
exactly 60 types.  The roots may overlap when a graph has multiple qualifying
partners; disjointness is neither needed nor claimed.

`PAIR_TYPES.tsv` contains the cell sizes, conditional orbit size after the
partner has been sent to 14, and SHA-256 of the 41 additional partner-edge
literals.  The anchor already fixes edge `13--14`, so it is not duplicated.
`generate_pair_types.py` can emit full unit suffixes internally but generated
CNF roots are intentionally omitted.

## Reproduction

Tested with CPython 3.12.12 and Apple clang 17.0.0.  From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 generate_pair_types.py \
  --output /tmp/PAIR_TYPES.tsv
cmp PAIR_TYPES.tsv /tmp/PAIR_TYPES.tsv
PYTHONDONTWRITEBYTECODE=1 python3 verify_pair_quotient.py PAIR_TYPES.tsv
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_pair_quotient.py PAIR_TYPES.tsv

xcrun clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  check_pair_quotient.cpp -o /tmp/check_pair_quotient
/tmp/check_pair_quotient PAIR_TYPES.tsv
PYTHONDONTWRITEBYTECODE=1 python3 test_pair_checker.py \
  --checker /tmp/check_pair_quotient --types PAIR_TYPES.tsv
```

On macOS installations requiring explicit SDK headers, add the `-isysroot`
and `-isystem` arguments recorded in the pass report.  Compare the concatenated
generator, normal verifier, C++ checker, and negative-control output with
`EXPECTED_OUTPUT.txt`; the optimized verifier repeats the four Python `PASS`
lines.

The Python verifier does not import the generator.  It definitionally checks
the local double count on 33,867 labeled graphs of orders one through six,
enumerates all 1,716 six-subsets of `E`, reconstructs every table row and unit
digest, and checks all cell totals.  The C++ implementation independently
parses and reconstructs the 60 rows, enumerates the same subset orbits, and
repeats the graph audit.  Normal, ASan, and UBSan builds pass.  Negative
controls remove a type, alter a cell, or duplicate one key; all are rejected.

## Scope and trust boundary

The mathematical content is the displayed double count, the exact
`R(3,5)=14` input, and the elementary orbit argument.  The code checks finite
bookkeeping, not the classical Ramsey value or the hand proof of
equisatisfiability under relabeling.  The cell itself inherits the complete
height-2505 graph-to-formula reduction and the height-2603 exact excess
partition, including their extremal-catalog trust boundary.  Trusted for the
audit are CPython exact integers, the C++ compiler/library, ordinary hardware,
and SHA-256 collision resistance.  There is no solver, generated CNF, witness,
UNSAT trace, core catalogue, or omitted search result in this contribution.

Primary context: Brendan D. McKay and Stanislaw P. Radziszowski,
“Subgraph counting identities and Ramsey numbers,” *J. Combin. Theory Ser. B*
69 (1997), 193–209; and Vigleik Angeltveit and Brendan D. McKay,
“`R(5,5) <= 46`,” arXiv:2409.15709 (2024).
