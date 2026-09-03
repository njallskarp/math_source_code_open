# Safe-margin repair of eight dead BHR `{1,2,11}` orthants

## Precise result

Write `(a,b,c)` for the multiplicities of lengths `1,2,11`.  For every row
`(A,B,C)` below, every multiset

\[
  \{1^a,2^b,11^C\},\qquad a\geq A,\quad b\geq B,
  \quad b\equiv B\pmod 2,
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
`K_(a+b+C+1)`.

| residue case | `(A,B,C)` | modes lost after one old growth | new first interior seed | selected cuts |
|---|---:|---:|---:|---:|
| `(1,1,2)` | `(2,17,2)` | `1 -> 2` | `(3,19,2)` | `1@0, 2@1` |
| `(1,1,5)` | `(3,13,5)` | `1 -> 2`, `2 -> 1` | `(4,15,5)` | `1@0, 2@1` |
| `(1,1,7)` | `(3,11,7)` | `2 -> 1` | `(4,13,7)` | `1@6, 2@8` |
| `(1,2,2)` | `(1,18,2)` | `1 -> 2` | `(2,20,2)` | `1@0, 2@1` |
| `(1,2,3)` | `(2,16,3)` | `1 -> 2` | `(3,18,3)` | `1@5, 2@1` |
| `(1,2,4)` | `(1,16,4)` | `1 -> 2`, `2 -> 1` | `(2,18,4)` | `1@18, 2@19` |
| `(1,2,6)` | `(3,12,6)` | `1 -> 2` | `(4,14,6)` | `1@0, 2@1` |
| `(1,2,8)` | `(3,10,8)` | `1 -> 2`, `2 -> 1` | `(4,12,8)` | `1@5, 2@6` |

All sixteen paths (the eight old boundary seeds and eight new interior seeds)
are recorded explicitly in `dead_orthant_certificate.json`.  This result
strictly contains the previously proved `C=4` orthant repair.  It does not
repair the full finite certificate: records involving simultaneous growth by
`11`, or other transitions that relocate rather than disappear, remain to be
audited separately.

## What the transition audit establishes

The pinned source is commit
`8fcd1e624b3d668794e3179787d0965137365286` of
<https://github.com/helgithorskarp/math_results>, whose finite certificate has
SHA-256
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`.
Its checker validates every advertised growth mode separately, then treats the
modes as independent in its coordinatewise coverage predicate.

`audit_source_certificate.py` performs the missing ordered transition test.
Across 628 witnesses it checks

\[
  \sum_P |X(P)|^2=1093
\]

post-growth obligations.  The cut predicted by order-preserving relabelling
fails 18 times.  Seven of these retain the tested mode at another cut; 11 lose
it at every legal cut.  The 11 total losses occur in precisely the eight rows
of the table.  In each row, the first mixed target `(A+1,B+2,C)` was covered by
that failing source witness and by no other source witness under the old
abstract coverage predicate.  The canonical 18-record audit digest is
`0a604cbf19537c855faa04a8d31b4a5985603ec6f1464ddb6f9e60a357795b03`.

## Safe-margin gap-refinement lemma

For vertices `r,s` of `K_v`, let

\[
  \ell_v(r,s)=\min(|r-s|,v-|r-s|).
\]

Inserting a gap of width `x` after cut `m` fixes labels at most `m` and adds
`x` to larger labels.  An `x`-growable path has exactly one changed-edge
incidence at every vertex in `(m-x,m]`, with no other changed edge.  Splitting
those changed edges through the `x` new labels is denoted `G_(x,m)`.

**Lemma.**  Suppose every edge of a path `P` in `K_v` has length at most `D`.
Let `x` and `y` be distinct growth modes, and suppose `P` is `x`-growable at
`m_x` and `y`-growable at `m_y`.  If

\[
  2D+x+y\leq v,
\]

then `G_(x,m_x)(P)` remains `y`-growable at

\[
  m_y' = \begin{cases}
    m_y,&m_y\leq m_x,\\
    m_y+x,&m_y>m_x.
  \end{cases}
\]

The symmetric statement also holds, and the two twice-refined paths are
identical after these cut transports.  Every edge of either once-refined path
still has length at most `D` when `x,y <= D`.

**Proof.**  Give every old edge its unique shorter circular arc.  After gaps of
total width at most `x+y` are inserted, an old arc has length at most
`D+x+y`, while its complement has length at least `v-D`.  The displayed
inequality therefore prevents the shorter arc from switching to its
complement (equality can only tie after both insertions, and the two arc
lengths then give the same cyclic length).  Consequently a gap changes an
edge exactly when that fixed shorter arc crosses the gap.

The growth construction replaces every crossing edge by the two subarcs cut
at the corresponding new vertex.  For a second gap, exactly one descendant of
an old crossing edge crosses it, and no descendant of a noncrossing edge does.
Thus the second gap has exactly the old one-per-critical-vertex incidences,
with its interval transported by the order-preserving insertion.  If the two
critical intervals overlap, the new vertex supplied by the first split is the
transported critical vertex for the second split; this is the same local
subdivision viewed in the opposite order.  Subdividing an arc at two marked
points is order-independent, proving both cross-preservation and commutation.
Finally, the descendants have either the old edge length or the inserted-gap
length.  Hence their lengths are at most `D`.  ∎

The usual same-mode step is the one-gap part of the same subdivision argument:
`G_(x,m)(P)` is again `x`-growable at `m`.  Unlike the false unrestricted
cross-mode sentence in the original growth proof, the lemma above explicitly
rules out circular-short-arc flips.

## Application to the eight seeds

Every new interior seed has order `v=25`, maximum edge length `D=11`, and is
both 1- and 2-growable at its displayed cuts.  Therefore

\[
  2D+1+2=25=v.
\]

After either refinement the maximum edge length stays 11 and the order grows,
so the safe margin persists.  Induction and commutation give every interior
point `(A+1+p,B+2+2q,C)` for `p,q >= 0`.  Repeated same-mode growth from the
old boundary seed gives `(A+p,B,C)` and `(A,B+2q,C)`.  The two boundary rays
and the interior partition the claimed orthant.

## Reproduction

The certificate checker needs only CPython's standard library:

```bash
cd research/bhr_1_2_11_transition_repair
python3 verify_dead_orthants.py dead_orthant_certificate.json --grid 10
python3 -m unittest -v test_verify.py test_dead_orthants.py
python3 check_safe_margin.py --max-order 8
```

The reference run under CPython 3.12.12 checks all eight seeds, reproduces all
11 boundary losses, checks 1,152 interior paths and 968 commuting squares, and
reports certificate SHA-256
`33d53244922865533b379d8f40d91063e1758f5997362e940f5d1ea503e7686d`.
The small-order lemma regression fixes the first vertex at 0 and exhausts all
5,910 paths of orders 4 through 8; 456 safe-margin ordered cut obligations are
nonvacuous.

To reproduce the source audit, first check out the pinned repository commit,
then run:

```bash
python3 audit_source_certificate.py \
  /path/to/math_results/graph_theory/bhr_1_2_11/certificate.json
```

To regenerate a particular new seed, install the pinned solver dependency and
pass its counts, for example:

```bash
python3 -m venv /tmp/bhr-dead-orthants-venv
/tmp/bhr-dead-orthants-venv/bin/pip install -r requirements.txt
/tmp/bhr-dead-orthants-venv/bin/python find_seed.py \
  --counts 4 15 5 --seconds 120
```

The reference generator used CPython 3.12.12, OR-Tools 9.14.6206, one worker,
and random seed 1.  It reproduces all eight stored paths exactly.  For the
`(2,18,4)` path it reports the alternate valid 1-cut 21; the certificate uses
cut 18, which the definition-level checker independently validates.

## Trust boundary and novelty scope

The theorem rests on displayed finite paths, exact integer cyclic-length and
growth-incidence checks, the gap-refinement lemma, and induction.  CP-SAT is
only a witness generator; no optimality or infeasibility conclusion is used.
The grid and small-order enumerations are regression tests, not substitutes for
the written all-parameter proof.  The source audit trusts the pinned source
bytes only as the object being criticized; the new existence claims do not
trust its coverage conclusion.

The primary literature is Chand and Ollis, *The Buratti-Horak-Rosa conjecture
holds for some under-explored sets of lengths* (<https://arxiv.org/abs/2202.07733>)
and Ollis, Pasotti, Pellegrini, and Schmitt, *New methods to attack the
Buratti-Horak-Rosa conjecture* (<https://arxiv.org/abs/2105.00980>).  Live
searches on 2026-09-03 found no published safe-margin correction or these eight
explicit seeds.  This supports only novelty relative to the searched graph and
sources, not an unrestricted priority claim.
