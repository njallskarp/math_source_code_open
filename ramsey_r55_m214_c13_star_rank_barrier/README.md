# Exact rank barrier for the \(M=214,c=13\) outside-star layer

## Result and scope

This directory proves two all-marking facts about the normalized
\(M=214,c=13\) branch.

1. Under the forced degree sequence and \(E\)-incidences, each blue
   local-triangle equation is algebraically equivalent to the corresponding
   red equation.
2. The 28 remaining red outside-star equations cannot be replaced by a small
   exact linear aggregate. Their pure outside-triangle coefficient matrix has
   rational rank 28. After the already-derived global outside-triangle balance
   equation, 27 independent star directions remain.

The second statement is a precise obstruction to the proposed low-dimensional
cell/orbit Hall or Farkas compression. Any successful compression must either
retain those 27 directions or use genuinely new inequalities from the
monochromatic-\(K_5\) layer. It is not an exclusion of \(c=13\), a Ramsey
graph, or a Ramsey-number bound.

## Blue equations are redundant

Let \(G\) be the red graph, let \(E\) be its thirteen degree-20 vertices, and
write

\[
m_v=\mathbf 1_{\{v\in E\}},\qquad
p_v=\mathbf 1_{\{v\text{ is the unique pivot}\}}.
\]

The branch equations give

\[
d_R(v)=21-m_v,qquad |N_R(v)\cap E|=6+2p_v.
\]

Put \(R=N_R(v)\), \(B=N_B(v)\), and let \(t_R(v)\) and \(t_B(v)\) be the
red and blue local-triangle counts. Since the total red degree is 890,

\[
\sum_{x\in R}d_R(x)=21d_R(v)-(6+2p_v).
\]

Counting the red cut between \(R\) and \(B\), and then the red edges inside
\(B\), gives

\[
t_B(v)=200-2p_v-t_R(v).
\]

Consequently

\[
t_R(v)=100-7m_v
\quad\Longleftrightarrow\quad
t_B(v)=100+7m_v-2p_v.
\]

This holds simultaneously for every vertex and every permitted \(E\)-marking.

## Exact outside-star equation

Let \(W=A\mathbin{\dot\cup}B\mathbin{\dot\cup}O\) be the 28 vertices outside
the anchors and cyclic core \(H\). For \(x\in W\), let

\[
S_x=N_R(x)\cap V(H),\qquad R_x=N_R(x)\cap W,
\]

and set \(a_x=1\) for \(x\in A\cup B\), and \(a_x=0\) for \(x\in O\).
When \(a_x=1\), let \(C_x\) be the same seven-vertex anchor cell as \(x\).
Directly partitioning the red triangles through \(x\) yields

\[
e_G(R_x)+
\sum_{y\in R_x}
\left(|S_x\cap S_y|+a_x\mathbf 1_{\{y\in C_x\}}\right)
=100-7m_x-e_H(S_x)-a_x|S_x|.
\]

The term \(e_G(R_x)\) is exactly

\[
\sum_{\substack{T\in\binom W3\\x\in T}}z_T,
\]

where \(z_T\) is the indicator that the three outside edges on \(T\) are red.

## Rank certificate

Let \(A\) be the \(28\times\binom{28}{3}\) vertex-triple incidence matrix.
If coefficients \(\lambda_x\) cancel all pure outside-triangle terms, then

\[
\lambda_i+\lambda_j+\lambda_k=0
\]

for every triple. Comparing triples differing in one vertex makes all
\(\lambda_x\) equal, and then \(3\lambda_x=0\). Thus \(A\) has row rank 28
over \(\mathbb Q\).

There is also a compact determinant certificate. Select the 28 cyclic triples

\[
T_i=\{i,i+1,i+2\}\pmod {28}.
\]

Their incidence matrix is \(I+P+P^2\), where \(P\) is a cyclic shift, and has
determinant 3. The Python checker computes this determinant by exact
fraction-free elimination. The independent C++ checker computes determinant
3 modulo \(1{,}000{,}000{,}007\); Hadamard's bound

\[
|\det(I+P+P^2)|\leq(\sqrt 3)^{28}=3^{14}=4{,}782{,}969
\]

makes that residue an exact integer certificate.

The global equation \(\sum_Tz_T=360\) supplies exactly the all-ones row
combination, because summing all star rows gives \(3\sum_Tz_T\). More
generally, if \(\lambda_i+\lambda_j+\lambda_k\) is merely constant on all
triples, comparison again makes every \(\lambda_x\) equal. Therefore the
global total removes exactly one direction and leaves 27.

## Reproduction

The recorded environment uses CPython 3.12.12 and GNU g++ 16.2.0. No external
package or solver is needed.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_rank.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_rank.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 test_rank.py | cmp - EXPECTED_TEST_OUTPUT.txt
g++-16 -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror independent_check.cpp -o /tmp/r55_c13_star_rank_check
/tmp/r55_c13_star_rank_check | cmp - EXPECTED_INDEPENDENT.txt
shasum -a 256 -c SHA256SUMS
```

For sanitizer replay:

```bash
g++-16 -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  -Werror -fsanitize=address,undefined -fno-omit-frame-pointer \
  independent_check.cpp -o /tmp/r55_c13_star_rank_check_san
/tmp/r55_c13_star_rank_check_san
```

## Trust boundary and stopping condition

The proof trusts the accepted degree/\(E\)-incidence branch equations, exact
integer and rational arithmetic in either small checker, the language
toolchain, and ordinary hardware. It does not trust a solver, search,
generated formula, catalogue payload, private graph state, database, binary,
log, or credential.

This rank barrier closes the low-dimensional outside-star aggregation route.
It does not rule out a Farkas argument that essentially retains 27 star
directions and uses the \(K_5\) inequalities, but that is the complete
individual layer in different notation rather than the proposed compression.
Further \(c=13\) work should stop unless an independently motivated nonlinear
mechanism appears.
