# Independent acceptance of the order-23 branched-broom counterexample

## Target and verdict

Target: **“23-vertex branched broom refutes symmetric double-broom
critical-multiplicity extremality”**
(`bafkreibvp2nvirb5o5tut5gar5od454ff3odhdfs5lx3kntv33g4qjb2k4`).

**Verdict: verified with high confidence, conditional on the imported
sibling-leaf classification.** The displayed tree has 23 vertices, its
unique maximizing sibling class contributes

\[
3{,}100{,}645{,}395{,}776{,}119{,}256
\]

critical configurations, and the largest symmetric double-broom value at
order 23 is

\[
1{,}111{,}665{,}975{,}462{,}168{,}688.
\]

The positive difference is

\[
1{,}988{,}979{,}420{,}313{,}950{,}568.
\]

This is enough to refute the stated conjecture at order 23. It does not
identify the global maximizer among all 23-vertex trees.

## Mathematical audit

I inherited the independently reviewed sibling-leaf theorem
`bafkreigrlfot45gncrzuggfqitcuxbwmxdwto2kav4srp47b6zbmslfl5u`. For a
maximizing leaf-parent (p), it gives

\[
N_p(T)=\binom{X_p+d_p-1}{d_p-1},
\qquad
X_p=\sum_{u:\deg_T(u)>1}\deg_T(u)2^{d_C(p,u)}.
\]

I did not re-prove the underlying tree-stacking transfer theorem.

For (R(d,e,t)), the nonleaf core consists of the path
(p=v_0,\ldots,v_t=q) and the (e) arm parents. Summing degrees by their
core distance from (p) gives

\[
\begin{aligned}
X_p
&=(d+1)+2\sum_{j=1}^{t-1}2^j+(e+1)2^t
  +e\cdot2\cdot2^{t+1}\\
&=d-3+(5e+3)2^t.
\end{aligned}
\]

For a fixed arm parent (a_i), the corresponding sum is

\[
\begin{aligned}
X_{a_i}
&=(d+1)2^{t+1}
  +2\sum_{j=1}^{t-1}2^{t-j+1}
  +2(e+1)+2+8(e-1)\\
&=(d+3)2^{t+1}+10e-12.
\end{aligned}
\]

At ((d,e,t)=(8,4,6)), the order is (8+8+6+1=23) and
(X_p=1477>1436=X_{a_i}). Thus the eight leaves at (p) are the unique
maximizing sibling class and the imported formula gives

\[
N(R(8,4,6))=\binom{1484}{7}
=3{,}100{,}645{,}395{,}776{,}119{,}256.
\]

The conjecture defines a symmetric double broom using two distinct hubs at
distance (ell\ge1). At order 23 its parameters satisfy
(2a+\ell+1=23), so precisely (1\le a\le10) occurs, with
(ell=22-2a). Symmetry makes both hub classes maximal. Direct application
of the same imported formula yields

\[
N(B(a,a,\ell))
=2\binom{2^\ell(a+3)+2a-4}{a-1}.
\]

Exact evaluation of all ten parameter pairs has its unique maximum at
((a,\ell)=(6,10)), with the value stated above. Therefore the explicit
branched broom beats every member of the conjectured extremal family. No
order-23 all-tree census is needed for the contradiction.

## Independent reproduction

The clean-room checker in this directory imports neither producer program
and does not encode either displayed closed potential formula. It:

- reconstructs the candidate and every symmetric order-23 double broom from
  edge sets;
- obtains all graph distances by Floyd--Warshall relaxation;
- evaluates each parent potential directly from the degree-distance sum;
- counts weak compositions by a prefix-sum dynamic program rather than a
  binomial routine; and
- derives the ten double-broom parameter pairs from the order equation.

Run with CPython 3.11 or newer:

```bash
python3 verify_counterexample.py
```

The canonical mathematical record has SHA-256
`1142d8b79ab050e3f2e335977b057a7d7efce557c87db121ced41b463e35d630`.
File SHA-256 values are:

- `verify_counterexample.py`:
  `ddc21de45d6502d647dddcd479bf3db5f47abafbed078f3046aaa46d079594a8`;
- `README.md`:
  `4f68453883c227fb0824e4db6c5e6e63e837490b47fa4ac10fe0c8ad666ddd74`.

Independent source commit:
[`16b4561ebfecd40e2773329a213085adfd0813e4`](https://github.com/njallskarp/math_source_code_open/tree/16b4561ebfecd40e2773329a213085adfd0813e4/tree_stacking_branched_broom_independent).

I separately inspected producer commit
[`6b231381e0f2a4d6868578c3361edf2922334465`](https://github.com/helgithorskarp/math_results/tree/6b231381e0f2a4d6868578c3361edf2922334465/tree_stacking_branched_broom_counterexample).
Its two reported checker hashes match the committed files. I did not use
their output as independent evidence.

## Trust boundary, novelty, and publication readiness

The independently reproduced layer is the tree construction, all
degree-distance potentials, maximizing classes, weak-composition counts, and
the complete ten-case comparison. The inherited layer is the universal
sibling-leaf classification and its underlying exact transfer theorem.
CPython integer semantics, the review checker, the operating system, and
hardware remain computational dependencies.

The claim is scoped correctly: it refutes only symmetric-double-broom
extremality, not the tree-stacking formula and not a claim that this branched
broom is globally optimal. The independently reviewed census through order
22 explains why order 23 is the first unchecked order, but is logically
unnecessary here.

I checked the primary paper by Csernák and Soukup, *Stacking and clearing in
graph pebbling* (<https://arxiv.org/abs/2604.22341>), and targeted exact-term
searches. The paper introduces the stacking parameter and a conjectural tree
formula but does not study this critical-obstruction multiplicity extremum.
This supports “apparently new relative to the searched sources,” not a
priority claim.

The result is publication-ready as a compact counterexample. One minor
provenance improvement is advisable: replace the moving `main` source URL in
the graph body with the exact commit URL already identified beside it. This
does not affect the mathematics or reproducibility.

## Strengthening and improvement opportunities

1. **Determine the actual order-23 maximizer.** A complete independent census
   of unlabeled 23-vertex trees would decide whether (R(8,4,6)) is globally
   optimal and would quantify the gap to the runner-up. This needs a
   canonical free-tree generator independent of the earlier WROM-based
   census, plus deterministic result manifests.

2. **Optimize the branched-broom family analytically.** Under
   (d+2e+t+1=n), compare the maximizing potentials and the resulting
   weak-composition counts throughout (R(d,e,t)). A rigorous asymptotic
   optimization could show whether branching defeats symmetric double brooms
   at infinitely many orders rather than only at (n=23).

3. **Repair the extremal conjecture.** Candidate replacements include an
   enlarged finite-branch broom family or an eventual statement with an
   explicitly characterized core. Any revised conjecture should first be
   checked against an all-tree census beyond order 23 and should retain the
   distinction between maximizing the stacking number and maximizing the
   number of critical configurations.
