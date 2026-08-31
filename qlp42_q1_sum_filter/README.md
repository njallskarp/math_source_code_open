# Exact Gaussian-sum filter for the QLP-42 `q=1` reflection branch

## Theorem

Assume the coupled norm-32 QLP-42 shell has total quarter-turn count `q=1`.
By the oriented parity and second-order reflection lemmas, family `B` has the
unique quarter cell, which may be rotated to position zero, and its remaining
opposite/equal types occur in ten reflected pairs.

Let `o` be the number of opposite non-quarter cells in family `B`.  The four
type counts are forced by the center energies:

```text
family A: opposite = 21-o,  equal = o,
family B: opposite = o,     equal = 20-o.                (1)
```

The four possible oriented exceptional states realize all independent sign
choices

```text
S_B(0)=sigma*i,       H_B(0)=tau,       sigma,tau in {+1,-1}.
```

Imposing all four exact Gaussian sum equations gives the following complete
classification:

| case | representative `(p,q,x,y)` | possible `o` | reflected count patterns |
|---:|---|---|---:|
| 0 | `(1,0,5,0)` | `4,6,8,10,12,14,16,18,20` | 123 |
| 1 | `(3,0,4,1)` | `4,6,8,10,12,14,16,18` | 120 |
| 2 | `(3,0,3,-2)` | `4,6,8,10,12,14,16,18` | 120 |
| 3 | `(3,2,3,2)` | `4,6,8,10,12,14,16` | 113 |
| 4 | `(3,2,2,3)` | `4,6,8,10,12,14,16` | 113 |
| 5 | `(4,1,2,-1)` | `2,4,6,8,10,12,14,16` | 116 |

Thus every case excludes at least five of the 128 reflected residue-count
patterns before any nonzero-shift autocorrelation equation is used.  The
boundary sign restrictions are also exact:

```text
case 0, o=4:  sigma=-1;        case 0, o=20: tau=+1;
case 2, o=4:  sigma=-1;        case 5, o=2:  sigma=-1.
```

All other displayed case/count pairs allow all four `(sigma,tau)` choices.
The full machine-readable summary is `case_filter.tsv`.

## Proof

Every nonzero non-quarter entry of either transformed word lies in

```text
(1+i)*mu_4 = {(1,1),(1,-1),(-1,1),(-1,-1)}.
```

Consequently a sum of exactly `n` such entries realizes a Gaussian integer
`r+si` if and only if

```text
|r| <= n,  |s| <= n,  r = n (mod 2),  s = n (mod 2).     (2)
```

The two coordinates can be chosen independently, so (2) is both necessary
and sufficient.  Substitute the counts in (1) and the canonical targets

```text
sum(S_A)=(p+q)+(q-p)i,       sum(H_A)=0,
sum(S_B)=(x+y-1)+(y-x)i,     sum(H_B)=1,
```

then test (2) for `S_B-sigma*i` and `H_B-tau`.  This gives precisely the
case/count/sign table above.

If `(k_0,k_1,k_2,k_3,k_3,k_2,k_1)` is the reflected mod-7 opposite-count
vector, then

```text
o = 2*(k_0+k_1+k_2+k_3),
k_0 in {0,2},  k_1,k_2,k_3 in {0,1,2,3}.
```

Enumerating these 128 vectors against the allowed `o` sets gives the final
column.

## Exact certificate and trust boundary

Run:

```bash
python3 verify_q1_sum_filter.py
```

The standard-library verifier reconstructs the 16 coupled states, checks the
four exceptional sign pairs, proves (2) by exhaustive dynamic programming for
every `0 <= n <= 21`, derives every allowed count/sign combination, verifies
the TSV, and enumerates all 128 reflected count vectors.  All arithmetic is
exact.  No SAT result, floating point, or heuristic search enters the theorem.

The filter is necessary at the type/count level.  It does not assert that any
surviving pattern admits compatible phases at all positions or satisfies the
nonzero autocorrelation equations.

This refines the committed second-order `q=1` reflection lemma and ultimately
the coupled QLP-42 reformulation.  The argument is elementary once those
identities are fixed; novelty is relative to the current Discovery Net graph,
not a historical-priority claim.
