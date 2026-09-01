# Audit note on the claimed coefficient-stopping induction

Laurore, *On the Link Between Stopping Time and Non-Trivial Cycles in the
Collatz Problem* (2025), DOI `10.4236/apm.2025.156018`, Theorem 4.7, claims to
propagate equality of ordinary and coefficient stopping times by strong
induction. The proof assumes a
counterexample `s` with coefficient stopping time `k` and writes

```text
s = 2^k m + s',  0 <= s' < 2^k.
```

The parity-cylinder identity correctly gives the same first `k` parity bits
and hence the same coefficient stopping time for `s'`. The next sentence,
however, invokes the induction hypothesis as if `sigma(s')=k` had also been
established. Only `kappa(s')=k` is known. The induction hypothesis in the
paper is restricted to starts whose **ordinary** stopping time equals a
smaller index, so it does not apply.

In fact the exact contracting-cylinder calculation points the other way. If
the shared word has `q` odd steps, `3^q<2^k`, and `s` has not descended at step
`k`, then

```text
T^k(s') + 3^q m >= s' + 2^k m
```

implies

```text
T^k(s') - s' >= (2^k-3^q)m >= 0.
```

All proper-prefix coefficients are at least one by the definition of the
coefficient stopping time, so `s'` has not descended earlier either. Thus the
deduction available from the stated premises is `sigma(s')>k`, not
`sigma(s')=k`. Theorem 4.7 therefore does not prove the coefficient
stopping-time conjecture. This diagnoses a proof gap; it is not a
counterexample to the conjecture itself.

The Lean file in this directory machine-checks the underlying base-forcing and
downward-closure statements.
