# A mod-4 defect-count restriction in the norm-32 half-difference projection

Let `R_A,R_B` be the length-21 half-difference words for the canonical
norm-32 QLP-42 residual.  Across their 42 coordinates, let `q,o,z` count
quarter-turn, opposite, and equal antipodal pairs, respectively.  Then

```text
(q,o,z) = (1+4t, 21-2t, 20-2t),  0 <= t <= 10.
```

In particular, `q` is 1 modulo 4, `o` is odd, and `z` is even.  This removes
the other ten a priori energy-compatible count triples.

## Proof

Every half-difference is divisible by the Gaussian prime `pi=1+i`.  Put
`S_X=R_X/pi`.  Reducing `S_X` modulo `pi` gives a binary word `u_X`: a
coordinate is one precisely when its antipodal pair is a quarter-turn, and
zero when the pair is equal or opposite.

The divided combined autocorrelation target is 43 at shift zero, `-2` at
shifts 4 and 17, `2` at shifts 10 and 11, and zero elsewhere.  Reduction
modulo `pi` therefore gives

```text
sum_j u_A(j) u_A(j+s) + sum_j u_B(j) u_B(j+s)
  = 1  if s=0,
  = 0  otherwise                         (in F_2).
```

Write `w_A,w_B` for the two binary weights and `N_s` for the corresponding
combined integer overlap at shift `s`.  Thus `q=w_A+w_B` is odd and every
`N_s` with `s` nonzero is even.  Periodic overlap symmetry gives
`N_s=N_(21-s)`, while counting every ordered pair once gives

```text
w_A^2+w_B^2 = sum_(s=0)^20 N_s
            = q + 2 sum_(s=1)^10 N_s
            = q (mod 4).
```

Exactly one of `w_A,w_B` is odd, so the left side is 1 modulo 4.  Hence
`q=1 (mod 4)`.  The shift-zero target is

```text
2q+4o=86,  so q+2o=43,
```

and there are 42 coordinates, so `q+o+z=42`.  It follows that `o` is odd and
`z=o-1` is even, giving exactly the eleven displayed triples.

## Exact verification and scope

`verify_half_difference_parity.py` independently enumerates all `2^21`
binary words and their eleven independent periodic-autocorrelation parities.
It groups them into 2,048 signatures and verifies the mod-4 weight conclusion
for every compatible signature pair (representing 1,585,059,840 ordered word
pairs), then reproduces the eleven triples.  It uses only standard-library
integer arithmetic.

`solve_norm32_half_difference_sat.py` is a separate exact Boolean model.  It
uses one-hot alphabet variables and finite-state integer-sum automata for all
correlation equations, and adds the proved mod-4 restriction as a redundant
propagation constraint.  Initial bounded runs are exploratory only; an
`UNKNOWN` status is not evidence of either feasibility or infeasibility.

This result narrows the norm-32 projection but does not decide any of its six
canonical compression branches, lift a projected word to length 42, or settle
the QLP-42 existence problem.

## Primary-source context

- I. S. Kotsireas, C. Koutschan, and A. Winterhof, *Quaternary Legendre
  pairs II*, <https://arxiv.org/abs/2408.16318>.
- C. Bright, I. Kotsireas, A. Heinle, and V. Ganesh, *Complex Golay Pairs up
  to Length 28: A Search via Computer Algebra and Programmatic SAT*,
  <https://arxiv.org/abs/1907.11981>.
- T. Lumsden, I. Kotsireas, and C. Bright, *New Results on Periodic Golay
  Pairs*, <https://arxiv.org/abs/2408.15611>.

The first source provides the QLP-42 compression and PSD context.  The latter
two provide primary methodological context for exhaustive complementary-
sequence search, multi-level compression, and SAT+CAS.  A targeted search did
not locate this binary-shadow congruence; apparent novelty is relative to that
search and is not a claim of priority.
