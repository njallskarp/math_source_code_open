# The NF-number of width-four dumbbell graphs

## Result

Let `B_(4,m)` be the dumbbell graph formed from disjoint cliques `K_4` and
`K_m` by adding one bridge edge.  With the NF-number defined up to
isomorphism, the first open width beyond the known width-two and width-three
families satisfies the conjectured formula.

**Theorem.** For every `m >= 2`,

```text
NF(B_(4,m)) = m + 6.
```

Consequently `NF(B_(n,m))=n+m+2` whenever `min(n,m) <= 4`, apart from
`B_(2,2)=P_4`, whose up-to-isomorphism NF-number is `1`.

## Exact type reduction

Write

```text
X={x_0,x_1,x_2,x_3},  Y={y_0,y_1,...,y_q},  q=m-1,
```

and use `x_0y_0` as the bridge.  The group `S_3 x S_q`, independently
permuting the ordinary vertices in each clique, preserves the entire NF
orbit.  A subset has type

```text
(a,i,b,j) in {0,1} x {0,1,2,3} x {0,1} x {0,...,q},       (1)
```

where `a,b` record the bridge endpoints and `i,j` count ordinary vertices.
Possible containment is exactly coordinatewise comparison.  Thus the
16-fibre type poset computes every facet orbit without loss.

For an invariant facet antichain `E` and base `z=(a,i,b)`, put

```text
h_E(z)=min({j-1:(v,j) in E and v<=z} union {q}).          (2)
```

Discard negative fibre heights and take the coordinatewise maximal remaining
tops `(z,h_E(z))`.  The resulting antichain is exactly
`D(E)=delta_NF(E)`: a subset is in the new complex precisely when it contains
no old facet, and (2) finds the largest admissible element in every fibre.

For a displayed finite set of types, let `C_q` discard terms whose final
coordinate is outside `[0,q]` and then take its coordinatewise maximal
elements.  Abbreviate `(a,i,b,j)` as `aibj`.

## Seven prefix states

Define

```text
F_0 = C_q{0002,0011,0200,1010,1100},
F_1 =     {0101,0110,1001},
F_2 =     {001q,1010,1300},
F_3 = C_q{030q,031(q-1),120q},
F_4 = C_q{021q,111q,121(q-1),130(q-1),131(q-2)},
F_5 = C_q{011q,030q,031(q-1),101q,111(q-1),120q,
          121(q-2),130(q-2),131(q-3)},
F_6 = C_q{001q,020q,021(q-1),030(q-1),031(q-2),101(q-1),
          110q,111(q-2),120(q-1),121(q-3),130(q-3),131(q-4)}.   (3)
```

For the sole case `q=1`, the upper-bound collisions replace the last line by

```text
F_6'={0011,0201,0210,1010,1101,1300}.                    (4)
```

Direct substitution in the sixteen instances of (2) gives

```text
D(F_r)=F_(r+1)                    for 0<=r<6,
D(F_6')=T                         when q=1,
D(F_6)=U                          when q=2,
D(F_6)=A_(q-2)                    when q>=3.              (5)
```

In the first line, `F_6` means the exceptional state (4) at `q=1`.  All
expressions in (3) are constants or `q-r` with `0<=r<=4`; hence the direct
fibre calculation has one stable regime `q>=4`, while `q=1,2,3` are the three
explicit clipping rows checked separately.

## Translating wave and wrap states

For bases in lexicographic order, use the weights

| `z` | 000 | 001 | 010 | 011 | 020 | 021 | 030 | 031 | 100 | 101 | 110 | 111 | 120 | 121 | 130 | 131 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `w(z)` | 4 | 3 | 2 | 1 | 1 | 0 | 0 | -1 | 2 | 0 | 1 | -1 | 0 | -2 | -2 | -3 |

The weights strictly decrease whenever distinct bases are comparable.  For
`1<=s<=q-2`, set

```text
A_s={(z,s+w(z)):0<=s+w(z)<=q}.                            (6)
```

The monotonicity makes this an antichain.  Formula (2) gives

```text
D(A_s)=A_(s-1)                       for 2<=s<=q-2.        (7)
```

Indeed, when the facet over `z` is in range, its threshold is the least among
all predecessor thresholds, giving height `(s-1)+w(z)`.  At the lower end,
the bases of weight `-2` at height zero force the weight `-3` fibre negative,
exactly deleting it.  At the upper end `s=q-2`, the temporary top `000q` is
dominated by `001q`; every other clipping agrees directly with (7).

Define two terminal antichains

```text
U=C_q{0004,0013,0102,0111,0201,0210,1002,1010,1101,1300},
T=C_q{0003,0012,0101,0110,0300,1001,1200}.                (8)
```

For `q>=4`, the fibre heights in the three wrap calculations are shown below;
an asterisk marks a maximal surviving top and a dash a negative height.
The three smaller values are exactly the `C_q` truncations already covered in
(4)-(5).

| input | 000 | 001 | 010 | 011 | 020 | 021 | 030 | 031 | 100 | 101 | 110 | 111 | 120 | 121 | 130 | 131 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `A_1` | 4* | 3* | 2* | 1* | 1* | 0* | 0 | - | 2* | 0* | 1* | - | 0 | - | 0* | - |
| `U` | 3* | 2* | 1* | 0* | 0 | - | 0* | - | 1* | - | 0 | - | 0* | - | - | - |
| `T` | 2* | 1* | 0 | - | 0* | - | - | - | 0 | 0* | 0* | - | - | - | - | - |

Thus

```text
D(A_1)=U,   D(U)=T,   D(T)=F_0.                           (9)
```

## Period and first return up to isomorphism

For `q>=2`, the complete labelled orbit is

```text
F_0,F_1,...,F_6,A_(q-2),A_(q-3),...,A_1,U,T,F_0,         (10)
```

where the wave is empty when `q=2`.  For `q=1`, it is

```text
F_0,F_1,...,F_5,F_6',T,F_0.                              (11)
```

The number of states before return is respectively
`7+(q-2)+2=q+7=m+6` and `8=m+6`.

There is no earlier return up to isomorphism.  `F_0=B_(4,m)` contains `K_4`,
whereas `F_1=K_(4,m)` minus the bridge pair is bipartite.  Every state from
`F_2` through `T` has a facet of size at least three, as is immediate from
(3)-(4), (6), and (8), so none is a graph.  Dimension and bipartiteness are
isomorphism invariants.  This proves the theorem.

## Reproduction

The checkers require CPython 3.10 or later and no third-party packages.

```sh
python3 verify.py --max-m 300 --direct-max-m 9
python3 independent_check.py --max-m 9
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected summary lines are:

```text
VERIFIED B_(4,m), m=2..300; type_states=46943; type_transitions=46943; definition_states=92; expanded_facets=16436; NF(B_(4,m))=m+6
INDEPENDENT VERIFIED B_(4,m), m=2..9; full_boolean_states=92; facets_seen_with_multiplicity=16436; labelled_period=m+6; no earlier isomorphic return
```

`verify.py` checks every displayed type transition through `m=300`, the
strict weight inequalities, all small clipping cases, and an independent
expansion of the type formulas into actual facets through `m=9` before
applying the defining Boolean-lattice NF operation.  `independent_check.py`
does not import the formulas or use orbit types: it constructs each dumbbell
from its edge list and directly iterates all subsets through `m=9`.  The tests
exercise the exceptional `m=2` boundary, wave translation and wraps,
definition-level expansion, and the no-early-isomorphism dimension witness.

The universal theorem rests on the finite symbolic 16-fibre calculation
above; bounded computation is corroborative and protects against transcription
and boundary errors.  There is no solver, floating point, randomness, raw
search dump, or external certificate.

## Literature and novelty boundary

- B. A. Rather, *The NF-operator and the NF-Numbers of Simplicial
  Complexes*, Conjecture 3.7, [arXiv:2605.30781](https://arxiv.org/abs/2605.30781).
  It states the general dumbbell formula, proves only the first orbit
  descriptions, and reports finite values for `2<=n,m<=5`.
- T. Hibi and H. Mahmood, *The NF-number of a simplicial complex*,
  [arXiv:2005.01247](https://arxiv.org/abs/2005.01247); *Algebra
  Colloquium* 29 (2022), 643-650.  It proves the analogous formula for the
  disjoint union of two cliques.

Targeted exact-title, formula, notation, and citation searches through
2026-09-04 found no proof of the width-four infinite family.  This is an
apparently-new-to-the-searched-sources statement, not a historical-priority
claim.
