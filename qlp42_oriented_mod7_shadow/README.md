# Oriented mod-7 binary shadows for the norm-32 QLP-42 shell

## Parity-orientation lemma

Let `q_A` and `q_B` be the numbers of quarter-turn cells in the two coupled
length-21 words.  Every canonical norm-32 candidate satisfies

```text
q_A = 0 (mod 2),       q_B = 1 (mod 2).                 (1)
```

Indeed, on each of the 16 local states the quarter-turn indicator equals

```text
Re(H_X(j)) + Im(H_X(j))  (mod 2).
```

The fixed coupled sums are `sum(H_A)=0` and `sum(H_B)=1`, so summing the local
identity proves (1).  The `S` sums independently give the same parity:

```text
sum(S_A) = (p+q)+(q-p)i,
sum(S_B) = (x+y-1)+(y-x)i.
```

Their coordinate sums are `2q` and `2y-1`, respectively.

## Refinement of the mod-7 classification

Let `v_A,v_B` be the length-7 binary shadows obtained by parity-compressing
the quarter-turn indicators in blocks of three.  Block compression preserves
total weight modulo two, hence

```text
wt(v_A) is even,       wt(v_B) is odd.                  (2)
```

The preceding mod-7 result classified 1,008 ordered solutions of

```text
v_A v_A* + v_B v_B* = 1 in F_2[x]/(x^7-1)
```

into 24 independent-rotation orbits.  Condition (2) selects exactly 504
ordered pairs and 12 orbits.  In the finite-field proof of the predecessor,
this fixes the formerly free augmentation pair to
`(epsilon_A,epsilon_B)=(0,1)`, so the ordered count becomes

```text
(8^2-1)*8 = 504.
```

Burnside's lemma gives the orbit count directly.  The identity fixes all 504
pairs, each of the twelve one-sided nonidentity rotations fixes seven
oriented pairs, and the 36 rotations nontrivial on both words fix none:

```text
(504 + 12*7)/49 = 12.
```

The solver-ready representatives are in `oriented_orbit_table.tsv`.  Combining
them with the predecessor's exact lift spectrum gives the following numbers
of surviving oriented orbits:

```text
q:          1  5  9 13 17 21 25 29 33 37 41
orbits:     1  6 11 12 12 12 12 12 11  6  1.
```

In particular, the extreme branch `q=1` forces `(v_A,v_B)` to be an empty
word and a singleton, while `q=41` forces a weight-six word and the all-one
word.  Up to independent rotations, each extreme branch now has one quotient
orbit rather than two.

## Exact verification

Run:

```bash
python3 verify_oriented_mod7_shadow.py
```

The standard-library verifier checks the local parity identity on all 16
phase pairs and both sum derivations in all six canonical cases.  It then
enumerates all `2^14=16,384` length-7 binary pairs, confirms the 504 oriented
solutions, performs the full Burnside fixed-point check, verifies the 12-row
table, and derives every displayed survivor count.

The lift spectra used for the survivor counts are a direct specialization of
the exact length-21 classification in `qlp42_mod7_binary_shadow`; this lemma
does not independently repeat that predecessor's `2^21`-word join.  No SAT
status, floating-point computation, or heuristic output enters the result.

## Scope and context

This is a necessary binary-shadow constraint, not a Gaussian lift or a
solution of QLP-42.  Its practical value is an oriented branch table and
redundant parity clauses for the full exact solver.

Primary context is Djokovic--Kotsireas, *Compression of Periodic
Complementary Sequences and Applications*, arXiv:1302.0571, and
Kotsireas--Koutschan--Winterhof, *Quaternary Legendre pairs II*,
arXiv:2408.16318.  The refinement is elementary once the coupled sums and
the predecessor's 24-orbit classification are combined; novelty is claimed
only relative to the committed Discovery Net graph.
