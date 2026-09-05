# Unique extension of a 399-coclique

## Theorem

Let `G` be a strongly regular graph with parameters

```text
(v,k,lambda,mu) = (3250,57,0,1).
```

Every independent set `S` of size `399` is contained in a unique independent
set of size `400`.  More precisely, among the `2851` vertices outside `S`, the
numbers of neighbours in `S` have multiset

```text
{0^1, 7^57, 8^2793}.
```

Hence a degree-57 diameter-two Moore graph cannot have independence number
`399`; its independence number is either at most `398` or exactly `400`.

## Proof

Write `H=G[V(G)\S]`.  For `x in V(H)` put

```text
a_x = |N_G(x) intersect S|,        z_x = a_x - 8.
```

### 1. Exact defect moments

Counting the edges from `S` to its complement gives

```text
sum_x a_x = 57*399.
```

Every pair of vertices of `S` is nonadjacent, hence has exactly one common
neighbour.  That common neighbour lies outside `S`.  Counting a pair by its
common neighbour gives

```text
sum_x binom(a_x,2) = binom(399,2).
```

Therefore

```text
sum_x a_x^2 = 399*(399+56) = 399*455.
```

There are `3250-399=2851` vertices in `H`.  Expanding `z_x=a_x-8` now yields

```text
sum_x z_x   = -65,
sum_x z_x^2 = 121,
sum_x z_x(z_x+1) = 56.                 (1)
```

Because `z_x` is an integer, every summand in the last expression is
nonnegative.

There is also a pointwise identity.  Fix `x in V(H)`.  If `s in S` is adjacent
to `x`, triangle-freeness says that no neighbour of `x` in `H` is adjacent to
`s`.  If `s` is not adjacent to `x`, the unique common neighbour of `s` and
`x` lies in `H`.  Thus

```text
sum_{y adjacent_H x} a_y = 399-a_x.
```

Since `deg_H(x)=57-a_x`, subtraction of eight times the degree gives

```text
A_H z = 7z - 1.                         (2)
```

### 2. Spectral Moore bound

We use the following elementary bound twice.

**Lemma.** If a finite simple graph `F` has girth at least five, then

```text
rho(F)^2 <= |V(F)|-1.
```

Indeed, for a vertex `u`, triangle- and four-cycle-freeness make the vertices
reached by the non-returning length-two walks from `u` all distinct and
outside `N_F(u) union {u}`.  Hence every row sum of `A_F^2` is at most
`|V(F)|-1`.  The spectral radius of the nonnegative matrix `A_F^2` is at most
its maximum row sum, and it equals `rho(F)^2`.

### 3. Positive defects are impossible

Let `P={x:z_x>0}` and suppose `P` is nonempty.  From (1), each vertex of `P`
uses at least `2` units of defect energy, so

```text
|P| <= 28.                               (3)
```

For `x in P`, discard the nonpositive terms from the neighbour sum (2):

```text
(A_{G[P]} z|_P)_x >= 7z_x-1 >= 6z_x.
```

Multiplying componentwise by the positive vector `z|_P` and summing shows by
the Rayleigh quotient that `rho(G[P])>=6`.  The induced graph `G[P]` has girth
at least five, so the lemma gives

```text
36 <= rho(G[P])^2 <= |P|-1 <= 27,
```

a contradiction.  Thus `z_x<=0` for every `x`.

### 4. The nonpositive profile is forced

Put `w=-z>=0`, and let `W={x:w_x>0}` with `m=|W|`.  Equations (1)--(2) become

```text
sum_x w_x   = 65,
sum_x w_x^2 = 121,
A_H w       = 7w + 1.
```

Restricting the last identity to `W` is legitimate because `w` vanishes off
`W`.  Therefore

```text
w^T A_{G[W]} w = 7*121+65 = 912.
```

The Rayleigh quotient and the spectral Moore bound give

```text
rho(G[W]) >= 912/121,
m-1 >= rho(G[W])^2 > 56,
```

where the strict final inequality is the exact integer comparison

```text
912^2 - 56*121^2 = 11848 > 0.
```

Thus `m>=58`.

For `x in W`, set `t_x=w_x-1`.  These are nonnegative integers.  With
`E=65-m`, the two moments give

```text
sum_{x in W} t_x   = E,
sum_{x in W} t_x^2 = m-9 = 56-E.        (4)
```

Since `m>=58`, we have `0<=E<=7`.  But nonnegative numbers of sum `E` have
sum of squares at most `E^2`.  If `E<=6`, (4) would give

```text
50 <= 56-E = sum t_x^2 <= E^2 <= 36,
```

which is impossible.  Hence `E=7`.  Equality now holds in
`sum t_x^2<=E^2`, so exactly one `t_x` equals `7` and all the others vanish.
Consequently `m=58`, one `w_x` equals `8`, fifty-seven equal `1`, and the
remaining `2793` equal `0`.  Since `a_x=8-w_x`, this is precisely

```text
{a_x:x outside S} = {0^1,7^57,8^2793}.
```

The unique vertex with `a_x=0` has no neighbour in `S`, so adjoining it gives
an independent set of size `400`.  No other vertex can be adjoined, proving
uniqueness.  Finally, if the independence number were `399`, a maximum
399-set would have the extension just constructed, a contradiction.  This
proves the theorem.

## Corollary

The map

```text
(C,c), where C is a 400-coclique and c in C,
    -> C \ {c}
```

is a bijection onto the 399-cocliques.  In particular, if `N_400` and `N_399`
denote their respective numbers, then `N_399=400*N_400`.
