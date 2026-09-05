# A mod-17 gap for square saturation in Q6

## Result

For every integer `d >= 6`,

```text
sat(Q_d,Q_2) >= 5183640 d 2^d / (2874791 d + 7492489).   (1)
```

Consequently,

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 5183640/2874791.
```

This improves the preceding `39270/21779` asymptotic constant by exactly
`1452990/62610073189`.  The finite bound is also strictly stronger for every
`d >= 6`.

## Dependency and strengthened local statement

The [preceding Q6 live-facet lift][q6] proves

```text
102 S_L - 60 E_L >= E_L/11
```

for every square-free edge set in `L=Q6`.  Its proof sums, over the twelve
`Q5` facets `K`, the nonnegative integer deficits

```text
delta_K = 34 S_K - 12 E_K,
```

which are positive on every live facet.  This note retains the discarded
congruence information and proves the stronger additive gap

```text
W_L := 1122 S_L - 661 E_L >= 37                 (2)
```

for every nonempty square-free edge set in `Q6`.

## Facet arithmetic

Put `e_K=E_K`, `x_K=2S_K`, `D=sum_K delta_K`, and let `k` be the number of
live facets.  Then

```text
delta_K = 17x_K - 12e_K > 0,
delta_K == 5e_K (mod 17),
sum_K e_K = 5E_L,
D = 102S_L - 60E_L,
W_L = 11D-E_L.                                  (3)
```

The exact support capacities from the preceding lift show that for
`k=5,...,10`, respectively,

```text
E_L <= 1, 6, 11, 20, 36, 64.
```

Since `D>=k`, these cases give `W_L>=46`.  Fewer than five live facets cannot
support an edge.

If `k=11`, one `Q5` facet is empty.  At most 32 selected edges cross it, and
all remaining selected edges lie in the opposite square-free `Q5`, which has
at most 56 edges.  Thus `E_L<=88`.  If `W_L<=40`, then `D=11` and `E_L>=81`:
already `D>=12` would give `W_L>=132-88=44`.  Summing the congruences in
(3) gives `D == 8E_L (mod 17)`, hence `E_L == 12 (mod 17)`, impossible for
`81<=E_L<=88`.  Therefore this case actually has `W_L>=41`.

It remains to take `k=12`, where the exact cap `E_L<=132` applies.  If
`W_L<=36`, then `12<=D<=15`.  For a live facet with `1<=e_K<=56`, the largest
edge counts compatible with `delta_K=1,2,3,4` are, respectively,

```text
41, 48, 55, 45.                                  (4)
```

These follow immediately from `delta_K == 5e_K (mod 17)`.  Now:

- If `D=12`, every deficit is one, so `e_K<=41` and `E_L<=98`.
  The aggregate congruence gives `E_L==10 (mod 17)`, hence actually
  `E_L<=95`, and `W_L>=132-95=37`.
- If `D=13`, (4) gives `sum e_K<=48+11*41=499`, so `E_L<=99` and
  `W_L>=44`.
- If `D=14`, its two positive-deficit partitions give
  `sum e_K<=506`, so `E_L<=101` and `W_L>=53`.
- If `D=15`, its three partitions give `sum e_K<=513`, so `E_L<=102`
  and `W_L>=63`.

This proves (2).  Equality in the arithmetic argument is possible only when

```text
(E_L,D,k)=(95,12,12),
{e_K : K a Q5 facet}={24,41,41,...,41}.           (5)
```

Indeed, all twelve deficits must equal one, so every facet count lies in
`{7,24,41}`; summing to `5E_L=475` forces one 24 and eleven 41s.  The six
direction counts would then be `(30,13,13,13,13,13)`, up to symmetry.  This
note classifies the equality candidate but does not assert that it is
geometrically realizable.

## Improved global bound

The exact value `ex(Q6,C4)=132` and (2) give, also for the empty pattern,

```text
S_L >= 87289 E_L/148104.                         (6)
```

Every `Q3` in `Q_d` lies in `C(d-3,3)` six-subcubes and every edge lies in
`C(d-1,5)`, whose ratio is `(d-1)(d-2)/20`.  Thus

```text
S >= 87289 E(d-1)(d-2)/2962080.                  (7)
```

Using the inherited square-saturation identities

```text
B+3A=(d-1)E-3M,
B+3A>=M/2+S/(d-2),
M=d 2^(d-1)-E,
```

equation (7) yields

```text
2874791(d-1)E >= 10367280M,
(2874791d+7492489)E >= 10367280 d 2^(d-1),
```

which is (1).  Cross-multiplication against the preceding finite bound leaves
the positive numerator `1452990(d-1)`.

## Reproduction

CPython 3.11 or later is sufficient; there are no third-party dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The checker performs an exact dynamic program over the facet arithmetic in
(3), reproduces the minimum gap for every live count, verifies the unique
arithmetic equality profile, and checks every rational simplification.  It
does not enumerate square-free Q6 subgraphs.

## Primary-source and overlap status

The external finite inputs remain `ex(Q5,C4)=56`, due to
Dejter--Emamy-K--Guan, and `ex(Q6,C4)=132`, due to Harborth--Nienborg.  An
[author-uploaded primary record for the Q6 result][hn] is available online.
Searches before publication found no prior mod-17 gap (2), equality
classification (5), or constant `5183640/2874791`.  The committed graph had
no matching contribution or incoming review on the Q6 dependency.  Concurrent
standing work on `R(5,5)` and Albertson's conjecture is disjoint.

## Trust boundary

The mod-17 proof and global double count are human arguments.  `verify.py`
checks their finite arithmetic relaxation using only CPython integers and
`fractions.Fraction`.  It does not reprove the two explicit extremal inputs,
the preceding Q5/Q6 lemmas, or realizability of the equality profile (5).  No
solver result, floating-point computation, generated database, or hidden
artifact is used.

[q6]: https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_saturation_q6_lift
[hn]: https://www.researchgate.net/publication/244468901_Maximum_number_of_edges_in_a_six-cube_without_four-cycles
