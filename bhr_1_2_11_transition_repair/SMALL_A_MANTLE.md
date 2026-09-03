# A transition-closed eleven-residue small-`a` BHR mantle

## Result

Let the row indexed by `s` in the following table define `(B_s,C_s)`.

| `s` | source counts | source cuts `(2,11)` | safe seed `(1,B_s,C_s)` | seed cuts `(2,11)` |
|---:|---:|---:|---:|---:|
| 1 | `(1,9,12)` | `(1,11)` | `(1,11,23)` | `(1,13)` |
| 2 | `(1,9,13)` | `(1,10)` | `(1,11,24)` | `(1,12)` |
| 3 | `(1,7,14)` | `(2,11)` | `(1,9,25)` | `(2,13)` |
| 4 | `(1,7,15)` | `(2,11)` | `(1,9,26)` | `(2,13)` |
| 5 | `(1,7,16)` | `(19,10)` | `(1,9,27)` | `(30,10)` |
| 6 | `(1,7,17)` | `(5,14)` | `(1,9,28)` | `(5,16)` |
| 7 | `(1,7,18)` | `(5,14)` | `(1,9,29)` | `(5,16)` |
| 8 | `(1,7,19)` | `(6,15)` | `(1,9,30)` | `(6,17)` |
| 9 | `(1,13,9)` | `(21,11)` | `(1,15,20)` | `(32,11)` |
| 10 | `(1,11,10)` | `(1,11)` | `(1,13,21)` | `(1,13)` |
| 11 | `(1,11,11)` | `(1,10)` | `(1,13,22)` | `(1,12)` |

For every `s in {1,...,11}` and every `q,r>=0`, there is a BHR realization
of

\[
  \{1,2^{B_s+2q},11^{C_s+11r}\}.
\]

Here `C_s` is congruent to `s` modulo 11, with residue 11 represented by
11.  In particular, because the thresholds `C_s` are the consecutive
integers 20 through 30 and `max_s B_s=15`, every multiset

\[
  \{1,2^b,11^c\},\qquad b\geq15\text{ odd},\quad c\geq20,
\]

has a Hamiltonian-path realization.  This is the full odd-`b`, large-`c`
mantle of the `a=1` frontier, not a collection of isolated bounded examples.

## Explicit finite certificate

Each source row is a selected path from the pinned Chand--Ollis finite
certificate.  The new certificate embeds all eleven paths, so provenance is
not a mathematical trust dependency.  On each source path, the checker first
recomputes its cyclic edge-length multiset and verifies the displayed
2-growability and 11-growability incidences.

Every source order is below the uniform safe threshold, so no unproved
cross-mode preservation is used there.  Instead, for each row the checker
performs both orders directly:

\[
  G_{11,\widehat m_{11}}G_{2,m_2}(g_s)
  =G_{2,\widehat m_2}G_{11,m_{11}}(g_s)=p_s,
\]

where hats denote order-preserving transport of the other cut.  Every
intermediate operation is definition-level valid, and the two labelled paths
and cut pairs agree exactly.  This is 44 checked derivation steps: eleven
sources, two orders, and two operations per order.  The endpoint `p_s` is the
safe seed in the table and has counts equal to its source plus `(0,2,11)`.

The compact certificate is
[`small_a_mantle_certificate.json`](small_a_mantle_certificate.json), with
SHA-256
`7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192`.
The canonical collection of its eleven endpoint paths has SHA-256
`cd3cd69b37cbb53c9d6ffc50e1b1429f57601dd8707387d103d20fc80b0addd0`.

## Transition closure

Every endpoint edge has cyclic length at most `D=11`, and the endpoint orders
range from 36 to 41.  Therefore every row satisfies

\[
  2D+2+11=35\leq |V(p_s)|.
\]

The finite-mode safe-margin theorem proved in
[`TRIMODAL_SAFE_CORES.md`](TRIMODAL_SAFE_CORES.md) says that under precisely
this inequality the transported 2- and 11-cuts persist and the two refinements
commute.  The maximum edge length stays at most 11 and the order only grows,
so induction applies forever.  Repeating 2-growth `q` times and 11-growth `r`
times proves every row of the table and hence the uniform corollary.

This use of the safe-margin theorem is logically separate from the bounded
grid below.  The grid is a regression test, not the source of the universal
quantifiers.

## Conservative coverage effect

Relative to the transition-aware 9,544-pattern audit after the earlier
`c=3 mod 11` slab, the eleven-row mantle covers 60 additional residual
representatives in eight previously untreated `a=1` residue classes:

```text
c residue       2   4   5   6   7   8   9  11
newly covered  12  12  10  10   8   4   2   2
```

The `s=3` row reproduces the earlier slab; rows `s=1` and `s=10` overlap
earlier constructions in this finite audit.  Cumulative coverage rises from
8,151 to 8,211 of 9,544, leaving 1,333 symbolic representatives.  The new
residual-record SHA-256 is
`00ed42e9e22d87d0a202e6b0e55ddc284cf8a7fff3479cff98df18e7def54b27`.
These are construction-coverage facts, not claims of unrealizability for the
remaining records.

## Reproduction

Only CPython's standard library is needed.  From this directory, run:

```bash
python3 verify_small_a_mantle.py small_a_mantle_certificate.json --grid 6
python3 independent_small_a_mantle_check.py small_a_mantle_certificate.json --grid 6
python3 -m unittest -v test_small_a_mantle.py
```

Both checkers report 11 residue classes, 44 source-derivation steps, minimum
seed order 36, 704 family paths, 1,078 coordinate transitions, 539 commuting
squares, transition-record SHA-256
`9dbdc10aa3bd26922507777712b06f311302b7bfa17b2454c8176c18bbb5959d`,
and `VERIFIED`.  To reproduce the coverage count as well, set
`BHR_SOURCE_CERTIFICATE` to the pinned external certificate and run the test;
the source SHA-256 must be
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`.
The derivation artifact itself can be regenerated with:

```bash
python3 build_small_a_mantle_certificate.py "$BHR_SOURCE_CERTIFICATE" /tmp/mantle.json
cmp /tmp/mantle.json small_a_mantle_certificate.json
```

## Trust and novelty boundaries

The infinite-family result trusts the eleven displayed finite paths in the
certificate, exact integer cyclic-length and incidence calculations, the
written finite-mode safe-margin proof, ordinary induction, CPython, and either
checker implementation.  It does not trust a solver, floating point, network
data, the source certificate's coverage predicate, or a finite grid as an
infinite proof.  Only the optional coverage count additionally trusts the
external pinned finite certificate.

Primary-source calibration used Chand--Ollis, *The Buratti--Horak--Rosa
Conjecture Holds for Some Underlying Sets of Size Three*
(<https://arxiv.org/abs/2202.07733>), which leaves `{1,2,11}` as the possible
exception in its range, and Ağırseven--Ollis, *Grid-based graphs, linear
realizations and the Buratti--Horak--Rosa conjecture*
(<https://arxiv.org/abs/2402.08736>), whose large-order theorem for
`{1^a,2^b,x^c}` explicitly retains `a in {1,2}` when `x` is odd as its possible
exception.  Live exact-parameter and committed-graph searches through height
1784 on 2026-09-03 found no prior publication of this eleven-residue mantle or
its uniform `a=1`, odd-`b>=15`, `c>=20` corollary.  This supports only “new to
the searched sources,” not a priority claim.
