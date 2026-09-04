# Independent width-five recurrence for the dumbbell NF-number

## Result

Let `B_(5,m)` be obtained from disjoint cliques `K_5` and `K_m` by adding one
edge between distinguished vertices.  With first return taken up to
isomorphism,

```text
NF(B_(5,m)) = m + 7                         (m >= 2).
```

This is an independently derived fixed-width proof.  A pre-publication refresh
then found the stronger all-width theorem at Discovery Net height 1877, so this
package was not submitted as a separate lemma.  Instead it supplies clean-room
specialization evidence for the independent audit in `AUDIT.md`.

## Lossless symmetry quotient

Write

```text
X={x_0,x_1,x_2,x_3,x_4},  Y={y_0,y_1,...,y_q},  q=m-1,
```

and take `x_0y_0` as the bridge.  The group `S_4 x S_q` permuting the
ordinary vertices in the two cliques preserves the whole orbit.  Every subset
orbit has a type

```text
(a,i,b,j) in {0,1} x {0,1,2,3,4} x {0,1} x {0,...,q}.    (1)
```

Possible containment of representatives is exactly coordinatewise
comparison.  Thus the quotient is a lossless 20-fibre encoding, not a sample.

For a facet antichain `E` and base `z=(a,i,b)`, put

```text
h_E(z)=min({j-1 : (v,j) in E and v<=z} union {q}).        (2)
```

Discard negative fibre heights and retain the coordinatewise maximal tops.
The result is exactly `D(E)=delta_NF(E)`: an allowed subset contains no old
facet, and (2) is its largest possible height in that fibre.

For a displayed set of types, `C_q` discards terms with last coordinate
outside `[0,q]` and restores maximality.  Write `aib:r` for `(a,i,b,r)`.

## Ten prefix states

The following affine lists define `F_0,...,F_9` after applying `C_q`:

```text
F_0={000:2,001:1,020:0,101:0,110:0}
F_1={010:1,011:0,100:1}
F_2={001:q,101:0,140:0}
F_3={040:q,041:q-1,130:q}
F_4={031:q,121:q,131:q-1,140:q-1,141:q-2}
F_5={021:q,040:q,041:q-1,111:q,121:q-1,130:q,
     131:q-2,140:q-2,141:q-3}
F_6={011:q,030:q,031:q-1,040:q-1,041:q-2,101:q,
     111:q-1,120:q,121:q-2,130:q-1,131:q-3,
     140:q-3,141:q-4}
F_7={001:q,020:q,021:q-1,030:q-1,031:q-2,040:q-2,
     041:q-3,101:q-1,110:q,111:q-2,120:q-1,121:q-3,
     130:q-2,131:q-4,140:q-4,141:q-5}
F_8={010:q,011:q-1,020:q-1,021:q-2,030:q-2,031:q-3,
     040:q-3,041:q-4,100:q,101:q-2,110:q-1,111:q-3,
     120:q-2,121:q-4,130:q-3,131:q-5,140:q-5,141:q-6}
F_9={001:q,010:q-1,011:q-2,020:q-2,021:q-3,030:q-3,
     031:q-4,040:q-4,041:q-5,100:q-1,101:q-3,110:q-2,
     111:q-4,120:q-3,121:q-5,130:q-4,131:q-6,
     140:q-6,141:q-7}.                                      (3)
```

Direct application of (2) gives `D(F_r)=F_(r+1)` whenever both states occur
in the orbit described below.

## Translating wave

For bases in lexicographic order, the weights are

| `z` | 000 | 001 | 010 | 011 | 020 | 021 | 030 | 031 | 040 | 041 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `w(z)` | 4 | 3 | 2 | 1 | 1 | 0 | 0 | -1 | -1 | -2 |

| `z` | 100 | 101 | 110 | 111 | 120 | 121 | 130 | 131 | 140 | 141 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `w(z)` | 2 | 0 | 1 | -1 | 0 | -2 | -1 | -3 | -3 | -4 |

The weights strictly decrease on every proper comparability.  Define

```text
A_s={(z,s+w(z)) : 0<=s+w(z)<=q}.                          (4)
```

For `4<=s<=q-4`, all input fibres are in range.  Among the predecessors of
`z`, strict weight decrease makes `w(z)` the unique minimum.  Formula (2)
therefore gives the top `(z,s-1+w(z))`; at `s=4` the sole negative output is
discarded.  Thus

```text
D(A_s)=A_(s-1)                         (4<=s<=q-4).        (5)
```

The remaining boundary calculation gives `D(A_3)=A_2`.

## Three wrap states and small boundaries

Set

```text
U={000:5,001:4,010:3,011:2,020:2,021:1,030:1,031:0,
   100:3,101:1,110:2,111:0,120:1,140:0}
V={000:4,001:3,010:2,011:1,020:1,021:0,040:0,
   100:2,101:0,110:1,130:0}
T={000:3,001:2,010:1,011:0,030:0,100:1,120:0}.            (6)
```

After `C_q`, the ordinary wrap is

```text
D(A_2)=U,  D(U)=V,  D(V)=T,  D(T)=F_0.                   (7)
```

Only `q=1,2` need exceptional antichains:

```text
U_1={011:1,030:1,031:0,101:1,111:0,120:1,140:0}
V_1={001:1,020:1,021:0,040:0,101:0,110:1,130:0}
U_2={001:2,020:2,021:1,030:1,031:0,101:1,110:2,
     111:0,120:1,140:0}.                                  (8)
```

The complete labelled orbit is

```text
q=1: F_0,...,F_5,U_1,V_1,T,F_0
q=2: F_0,...,F_6,U_2,V,T,F_0
q=3: F_0,...,F_7,U,V,T,F_0
q=4: F_0,...,F_8,U,V,T,F_0
q=5: F_0,...,F_9,U,V,T,F_0
q>=6: F_0,...,F_9,A_(q-4),A_(q-5),...,A_2,U,V,T,F_0.      (9)
```

There are `q+8=m+7` states before return in every case.

No earlier state is isomorphic to `F_0`.  The initial graph contains `K_5`,
while `F_1` is bipartite.  Every later displayed state has a facet of size at
least three: this is immediate in the finite prefix and wrap lists, and each
wave has its `000` facet of size `s+4>=6`.  Dimension and bipartiteness are
isomorphism invariants.  This proves the theorem.

## Exact certificate and reproduction

The checkers require CPython 3.10 or later and no third-party packages.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-m 500 --direct-max-m 8
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-m 8
PYTHONDONTWRITEBYTECODE=1 python3 compare_target_specialization.py --max-m 200
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

Expected compact output:

```text
SYMBOLIC CERTIFICATE q>=15; affine_transitions=15; wave_order_checks=250; exact_boundary_q=1..14
VERIFIED B_(5,m), m=2..500; type_states=128742; type_transitions=128742; definition_states=84; expanded_facets=16375; NF(B_(5,m))=m+7
RESULT_SHA256=1eab43a679ca325bb213df376344b79e705129a71316027cbe9474db472b61d4
INDEPENDENT VERIFIED B_(5,m), m=2..8; full_boolean_states=84; facets_seen_with_multiplicity=16375; labelled_period=m+7; no earlier isomorphic return
ORBIT_SHA256=ecd499dd2366d2f17a67662de9090e8f290dfa902692274a19497ecfe4300f34
EXACT SPECIALIZATION MATCH B_(5,m), m=5..200; cases=196; states=21462
MATCH_SHA256=8775286d7f59c74cadc633bcd1c3b585cbcd8500b107b79146a2e9f571b6424a
```

The universal conclusion does not rest on the `m<=500` regression.  The
symbolic checker represents every height in (3), (6), and the wave entrance as
an exact affine expression `a*q+b`.  It computes a point beyond every possible
ordering crossing (`q=15`), applies both the minimum in (2) and maximality in
affine arithmetic, and proves exact coefficient equality for all 15 prefix,
wave-boundary, and wrap transitions for every `q>=15`.  It also checks every
clipping/order chamber `1<=q<15` exactly.  The generic wave proof reduces to
the 20-base strict-weight and predecessor-minimum identities; 250 exact order
comparisons are checked.

The main checker additionally expands every type orbit into actual subsets and
applies the defining Boolean-lattice operation through `m=8`.  The independent
checker imports no types or formulas: it constructs `B_(5,m)` from its edges
and directly iterates the Boolean lattice through `m=8`.  Computation assumes
ordinary CPython integer, set, tuple, and SHA-256 semantics.  There is no
solver, randomness, floating point, generated input, or external certificate.

## Literature boundary

Rather, *The NF-operator and the NF-Numbers of Simplicial Complexes*,
[arXiv:2605.30781](https://arxiv.org/abs/2605.30781), Conjecture 3.7, proposes
`NF(B_(n,m))=n+m+2`, gives the first two iterates, and reports computation only
for `2<=n,m<=5`.  Its conclusion says a complete proof needs a full
parameterization of the orbit.  Hibi and Mahmood,
[*The NF-number of a simplicial complex*](https://arxiv.org/abs/2005.01247),
prove the analogous formula for the disjoint union `K_n` and `K_m`, not for a
bridge dumbbell.  The committed graph contained independently reviewed
all-parameter proofs for widths two, three, and four through indexed height
1868.  During the pre-publication duplicate check, indexed height 1880 exposed
the stronger height-1877 complete classification.  This package is therefore
evidence for review of that result, not a priority or standalone novelty claim.
