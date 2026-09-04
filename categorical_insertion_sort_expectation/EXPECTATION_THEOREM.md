# Exact expected swap counts for categorical insertion sort

Let the ordered alphabet be `1 < ... < m`.  For a word
`A=(A_1,...,A_n)`, run insertion sort using the strict comparison `>` and let
`S(A)` count adjacent swaps (equivalently, one-position right shifts of an
earlier entry).

## Theorem

1. If `A` is a uniformly random rearrangement of a multiset with `n_k`
   copies of category `k`, where `sum_k n_k=n`, then

   ```text
   E[S(A)] = (1/2) sum_{a<b} n_a n_b
           = (1/4)(n^2-sum_k n_k^2).
   ```

   Writing the empirical probabilities as `p_k=n_k/n`, this is

   ```text
   E[S(A)] = n^2/4 (1-sum_k p_k^2).
   ```

2. If `A_1,...,A_n` are independent with `P(A_i=k)=p_k`, then

   ```text
   E[S(A)] = binom(n,2) sum_{a>b} p_a p_b
           = n(n-1)/4 (1-sum_k p_k^2).
   ```

Both formulas include `n=0` or `n=1` and zero-probability/zero-count
categories after the evident harmless conventions.

## Proof

Define the strict inversion number

```text
I(A) = #{(i,j): 1 <= i < j <= n and A_i > A_j}.
```

An adjacent swap made by insertion sort exchanges a strictly inverted adjacent
pair.  Such a swap changes the order of exactly that pair and therefore lowers
`I` by exactly one.  The algorithm stops at a weakly increasing word, whose
strict inversion number is zero.  Consequently

```text
S(A)=I(A)                                                   (1)
```

for every deterministic input, including inputs with ties.

For the fixed-count model, distinguish the occurrences temporarily.  There
are

```text
e_2(n_1,...,n_m)=sum_{a<b}n_a n_b
```

unordered pairs of occurrences having different categories.  In a uniform
shuffle, either occurrence in any fixed pair is first with probability `1/2`.
Exactly one of these two relative orders is an inversion.  Linearity of
expectation and (1) give `E[S]=e_2/2`.  Finally,

```text
2 e_2 = (sum_k n_k)^2-sum_k n_k^2,
```

which gives the remaining fixed-count forms.

For the i.i.d. model, for each fixed pair `i<j`, independence gives

```text
P(A_i>A_j) = sum_{a>b} p_a p_b
           = (1/2)((sum_k p_k)^2-sum_k p_k^2)
           = (1/2)(1-sum_k p_k^2).
```

Summing this probability over the `binom(n,2)` position pairs proves the
i.i.d. formula.

## Generating-function cross-check

For fixed counts, classical Mahonian theory gives the inversion enumerator

```text
sum_A q^I(A) = [n]_q! / product_k [n_k]_q!,                (2)
```

where the sum is over distinct multiset words.  Reversing a word complements
its inversion number within the `e_2(n_1,...,n_m)` unequal-category pairs.
Thus (2) is palindromic of degree `e_2`, and its normalized distribution has
mean `e_2/2`, independently confirming the first formula.

For i.i.d. sampling, conditioning on the multinomial count vector gives the
probability generating function

```text
E[q^S] = sum_{n_1+...+n_m=n}
         (product_k p_k^{n_k}) [n]_q!/product_k[n_k]_q!.    (3)
```

Differentiating (3) at `q=1` and inserting the fixed-count mean gives

```text
E[S] = (1/4)(n^2-sum_k E[N_k^2])
     = n(n-1)/4 (1-sum_k p_k^2),
```

because `E[N_k^2]=n p_k(1-p_k)+n^2p_k^2`.

## Exact finite-population correction

When the same empirical vector `p_k=n_k/n` is used in both models and `n>1`,

```text
E_fixed[S] / E_iid[S] = n/(n-1)
```

unless all mass lies in one category (when both expectations are zero), and

```text
E_fixed[S]-E_iid[S] = n/4 (1-sum_k p_k^2).
```

The difference is caused by the random multinomial counts in the i.i.d.
model, not by any change in the sorting rule.

## Literature status

Canfield, Janson, and Zeilberger, *The Mahonian probability distribution on
words is asymptotically normal*, Advances in Applied Mathematics 46 (2011),
109--124, gives the normalized `q`-multinomial probability generating function
and explicitly records the fixed-count mean `e_2/2`:
https://arxiv.org/abs/0908.2089 .  Thus the fixed-count formula is classical;
no novelty claim is made for it.  The contribution here closes the graph
problem by proving the requested insertion-sort identity, stating both random
models side by side, deriving the i.i.d. formula, and isolating their exact
finite-population correction.
