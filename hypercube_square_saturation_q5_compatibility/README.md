# Q5 facet compatibility for square saturation

## Result

Let `G` be a square-saturated spanning subgraph of the `d`-cube, and let
`sat(Q_d,Q_2)` denote the minimum possible number of selected edges.  For every
`d >= 5`,

```text
sat(Q_d,Q_2) >= 39984 d 2^d / (22175 d + 57793).
```

Consequently,

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 39984/22175.
```

The new asymptotic constant exceeds the preceding `119/66` bound by exactly
`119/1463550`.

## Local compatibility lemma

For a square-free edge set `F` in a copy `K` of `Q5`, let `E_K=|F|`.  Sum the
inherited `Q3` slack `sigma` over the 40 three-dimensional subcubes of `K`, and
call the result `S_K`.  Then every nonempty `F` satisfies

```text
34 S_K - 12 E_K >= 1.                         (1)
```

The [preceding reproducible note][q4] defines `sigma`, proves its
nonnegativity, and proves the sharp `Q4` inequality used below.  Thus this note
has one explicit mathematical dependency rather than silently reintroducing
that machinery.

Here is a proof that uses the sharp `Q4` lemma

```text
17 S_H - 3 E_H >= 0                           (2)
```

on each of the ten `Q4` facets `H` of `K`.  Each `Q3` lies in two facets and
each edge lies in four, so summing (2) gives the left side of (1).  It remains
to rule out equality.

The equality arithmetic in a nonempty facet is rigid: because `E_H <= 24` and
`17 S_H = 3 E_H`, it forces `(E_H,S_H)=(17,3)`.  If `k` of the ten facets are
nonempty, double-counting edge-facet incidences gives

```text
17 k = 4 E_K.
```

Thus `k` is either 4 or 8.  Every edge of `F` must have all four of its
containing facets among those `k` live facets.

- Four live facets can support at most one edge: an allowed edge's four facets
  would have to be exactly the live set, and their coordinate/bit labels
  determine that edge uniquely.
- Eight live facets leave two empty.  If they are the two opposite facets of
  one coordinate, exactly the 16 edges in that direction avoid both.  If they
  have distinct coordinates, the two corresponding directions contribute 8
  edges each and the other three directions contribute 4 each, for 28 total.

These capacities contradict the required `E_K=17` and `E_K=34`, respectively.
The summed deficit is an integer, so it is at least one, proving (1).

## Using the exact Q5 extremal value

The published value `ex(Q5,C4)=56` is equivalent to saying that 24 edges are
necessary to meet all 80 squares of `Q5`.  It is the one external finite input
to this note.  It was proved in I. J. Dejter, M. R. Emamy-K, and P. Guan,
*On the fault tolerance in a 5-cube*, Congressus Numerantium 80 (1991),
171--176.  An [author-uploaded copy and bibliographic record][fault] and the
[original conference abstract][program] are available online.

Combining `E_K <= 56` with (1) yields

```text
S_K >= (12 E_K + 1)/34 >= 673 E_K / 1904.     (3)
```

The last inequality is valid also for `E_K=0`.

## Global count

Let `E` be the number of selected edges, `M=d*2^(d-1)-E` the number of missing
edges, and `S` the total inherited `Q3` slack.  Summing (3) over all `Q5`
subcubes and using

```text
C(d-1,4)/C(d-3,2) = (d-1)(d-2)/12
```

gives

```text
S >= 673 E (d-1)(d-2) / 22848.                (4)
```

The established global identities for square saturation give

```text
B + 3A = (d-1)E - 3M
B + 3A >= M/2 + S/(d-2).
```

Substituting (4) and simplifying produces

```text
22175(d-1)E >= 79968M.
```

Since `M=d*2^(d-1)-E`, this is exactly the stated theorem.

## Reproduction

Python 3.11 or later is sufficient; the program uses only the standard
library.

```bash
python3 verify.py
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

`EXPECTED_OUTPUT.txt` is the complete expected first command output.  The
checker independently constructs all 80 edges, 80 squares, and ten `Q4`
facets of `Q5`; confirms both relevant live-facet capacity distributions; and
checks every rational simplification in the bound.

## Primary-source and overlap status

The saturation framework is due to [Johnson and Pinto][jp] and the general
fixed-subcube order of magnitude was settled by [Morrison, Noel, and Scott][mns].
This note extends the committed sharp `Q4` weighted-slack result.  A graph and
literature search before publication found no prior `Q5` compatibility lemma
of the form (1), nor the constant `39984/22175`.  Concurrent standing lanes on
`R(5,5)` and Albertson's conjecture are disjoint from this work.

## Trust boundary

The proof of the compatibility lemma and the all-dimensional double count are
human mathematical arguments.  `verify.py` corroborates the finite incidence,
support-capacity, integrality, and rational-arithmetic claims using CPython
integer arithmetic.  It does **not** prove the external theorem
`ex(Q5,C4)=56`; readers should verify that input from the cited 1991 primary
source.  No solver, floating-point arithmetic, generated database, or hidden
artifact is used.

[fault]: https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube
[program]: https://www.math.fau.edu/combinatorics/previous-years/21st-cgtc-entire-program-booklet.pdf
[jp]: https://arxiv.org/abs/1406.1766
[mns]: https://arxiv.org/abs/1408.5488
[q4]: https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_saturation_q4_slack
