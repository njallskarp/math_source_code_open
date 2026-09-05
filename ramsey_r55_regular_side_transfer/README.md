# Exact limitation witnesses for the regular-side transfer

## Result

The accepted regular `(4,4;15)` obstruction does **not**, by itself, extend
through the exceptional-root core/signature relaxation across the remaining
double-degree-19 family.  For each `r=1,...,5`, this directory gives an exact integer witness
for the profile

```text
19^2 20^r 21^36 22^(5-r),       M=221-r.
```

These are all five double-degree-19 profiles among the 66 hard-branch
profiles remaining after Discovery Net height 2609.  Together they represent
25 anchored splits.  Each witness satisfies a stronger relaxation than the
degree-count system: it supplies a literal seven-vertex exceptional core,
integer central signature counts, every earlier common-neighborhood union
cut, and all the individual hard-branch weighted constraints.  Nevertheless,
every one-way side rooted at an ordered pair of exceptional vertices has at
most fourteen vertices.  The order-fifteen obstruction therefore never
activates.

This is a rigorous limitation result for the stated relaxation, not evidence
that any of the five profiles is realized by a Ramsey `(5,5;43)` graph.

## Exact relaxation

Let `E` be the seven vertices of degree different from 21 and let `C` be the
36 degree-21 vertices.  A witness consists of a red graph `F` on `E` and a
nonnegative integer `y_X` for every signature

```text
X = N_R(v) intersect E,       v in C.
```

Put `epsilon_i=d_i-21` and use

```text
b(19)=221, b(20)=220, b(22)=221.
```

The verifier checks all of the following directly.

1. `F` has neither a red nor a blue `K5`, and every exceptional vertex obeys

   ```text
   sum_(j in N_F(i)) epsilon_j <= M-b(d_i).
   ```

   It also checks the summed central weighted inequality

   ```text
   sum_i epsilon_i (d_i-deg_F(i)) <= 36(M-220).
   ```

2. A signature is admitted only when

   ```text
   sum_(i in X) epsilon_i <= M-220,
   omega(F[X]) <= 3,
   alpha(F[E\X]) <= 3.
   ```

   Its capacity is

   ```text
   c_X=min(36,U(5-omega(F[X]),5-alpha(F[E\X]))-1),
   ```

   where `U` is the elementary Ramsey recurrence with the even/even
   handshaking improvement.  The exact margins are

   ```text
   sum_X y_X=36,
   sum_(X containing i) y_X=d_i-deg_F(i),
   0<=y_X<=c_X.
   ```

3. For every disjoint red clique `A` and blue clique `B` of `F`, not both
   empty, the complete union cut is imposed:

   ```text
   sum_(X containing A, X disjoint B) y_X
     + |T_F(A,B)| <= U(5-|A|,5-|B|)-1.
   ```

   The five witnesses pass all 1,522 such inequalities.

4. For every ordered pair `i!=j` in `E`, form the full one-way set determined
   at this level,

   ```text
   S_ij={v outside {i,j}: iv is red and jv is blue}.
   ```

   Its size is exactly the number of fixed exceptional vertices with that
   color pattern plus

   ```text
   sum_(X: i in X, j not in X) y_X.
   ```

   There are `5*7*6=210` ordered sides.  Every recorded size is at most 14;
   the maximum is attained in each profile.

In an actual graph with no monochromatic `K5`, every `S_ij` is a `(4,4)`
graph: a red `K4` extends through `i`, and a blue `K4` extends through `j`.
Height 2609 excludes a particular regular order-15 case, while height 2647
proves a stronger 50--55 edge interval at order 15 and a 58--62 interval at
order 16.  The present witnesses avoid both orders entirely.  Thus no
argument using only the displayed core/signature constraints and those
order-specific results can exclude this five-profile family.  A successful
next transfer must add central-edge information or force a larger side by a
new invariant.

## Certificate summary

Masks use lexicographic unordered exceptional-vertex pairs, least significant
bit first.  Signature bit `i` means red adjacency to exceptional vertex `i`.

| `r` | `M` | core mask | eligible signatures | positive cells | union cuts | maximum side |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 220 | 740695 | 90 | 21 | 287 | 14 |
| 2 | 219 | 304595 | 90 | 21 | 306 | 14 |
| 3 | 218 | 435543 | 90 | 22 | 268 | 14 |
| 4 | 217 | 758013 | 82 | 20 | 327 | 14 |
| 5 | 216 | 18430 | 87 | 21 | 334 | 14 |

The sparse certificate [WITNESSES.json](WITNESSES.json) is under 8 KB.  It
contains no central-central edge variables, solver transcript, graph catalog,
or claimed target graph.

## Reproduction

The theorem-level check uses CPython 3.11 or newer and only the standard
library:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify_witnesses.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_witnesses.py | cmp - EXPECTED_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The verifier reconstructs clique numbers and union roots by literal subset
tests rather than importing the discovery code.  It rejects four altered
certificates.

Optional regeneration uses NumPy 2.2.6 and SciPy 1.15.3 only to discover an
integer witness.  Obtain a fresh checkout of
`https://github.com/helgithorskarp/math_results` at commit
`08af2b1a1be96995b1a1dadeea9421b3a3bef018`, then run

```bash
python3 -m venv /tmp/r55-transfer-venv
/tmp/r55-transfer-venv/bin/pip install -r requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  /tmp/r55-transfer-venv/bin/python explore_transfer.py /path/to/math_results \
  --two-degree19 --attempts 20 --output /tmp/WITNESSES.json
cmp WITNESSES.json /tmp/WITNESSES.json
```

The generator pins the four campaign input files by SHA-256, reconstructs the
66-row list, and selects its complete double-degree-19 subfamily.  The solver
status is not proof: only the committed sparse integers and the solver-free
checker authorize the limitation result.

## Provenance, literature, and trust boundary

The 66-profile accounting and the fact that these five rows are its complete
double-degree-19 subfamily are imported from the campaign chain ending at
heights 2609/2619.  The profile-specific regular-side result is accepted at
height 2619.  Height 2647 supplies the catalog-free density strengthening but
was not independently reviewed when this directory was prepared; the present
limitation does not need its correctness because it already avoids order 15.

The small order-15 edge range is also a classical consequence of Brendan
McKay's complete Ramsey-graph catalog; no novelty is claimed for it.  The
global context is Angeltveit--McKay, *R(5,5) <= 46*, arXiv:2409.15709 / JGT
(2026), DOI `10.1002/jgt.70029`.

Trusted for this result are the displayed finite relaxation, the literal
standard-library checker, exact integer/Boolean semantics, the pinned campaign
profile inputs, source provenance, SHA-256, and ordinary hardware.  Not
provided are edges inside or between central cells, individual central
neighborhood edge counts, a lift to a 43-vertex graph, a proof that any profile
survives stronger edge-aware relaxations, or a new bound on `R(5,5)`.
