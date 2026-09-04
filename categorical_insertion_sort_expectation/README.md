# Expected insertion-sort swaps on categorical arrays

This directory gives a complete solution of the Discovery Net problem
"Expected Insertion-Sort Swaps for Categorical Arrays" (height 144).  The
input alphabet is ordered, insertion sort uses the strict comparison `>`, and
equal entries are never swapped.

The two random-input models have different answers.  If
`n_1 + ... + n_m = n`, and `p_k = n_k/n` in the fixed-count model, then

```text
fixed-count shuffle:  E[S] = (1/2) sum_{a<b} n_a n_b
                            = n^2/4 (1 - sum_k p_k^2),

i.i.d. sampling:      E[S] = binom(n,2) sum_{a>b} p_a p_b
                            = n(n-1)/4 (1 - sum_k p_k^2).
```

The proof and its generating-function cross-check are in
[`EXPECTATION_THEOREM.md`](EXPECTATION_THEOREM.md).  The computation is an
audit, not a premise of the proof.

## Reproduce

Python 3.12 or later is sufficient; there are no third-party dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_expectation.py
sha256sum -c SHA256SUMS
```

The verifier uses only exact Python integers and `fractions.Fraction`.  It
checks the insertion-sort/inversion identity word by word, every positive
ordered count vector of total size at most 8, the fixed-count mean, the
palindromicity of each inversion distribution, and a grid of exact rational
i.i.d. laws by direct weighted enumeration.  It ends with

```text
summary={"arithmetic":"exact integers and fractions","fixed_count_vectors":255,"fixed_words":598444,"iid_probability_laws":56,"iid_weighted_words":208116,"palindromic_distributions":255,"python":"3.12+ standard library"}
result_sha256=fed436308f138d8116813de490655e854e7cd4efabe942d5c7092177052888fd
VERIFIED
```

## Trust boundary

The theorem is proved by finite pair counting and does not rely on code.  The
checker is a definition-level audit using the CPython standard library.  It
uses no floating point, randomness, external data, solver, or generated
certificate.
