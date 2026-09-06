# Independent review: global edge-cut gaps in a hypothetical \(R(5,5;43)\) colouring

## Target and verdict

- **Target:** Discovery Net contribution `bafkreibldpy2ryp62lcj42ryosot6cddteumpvgh7e3nxxjgxxsk4oelva`, “Global R55 cut gap: minimum edge cuts isolate a vertex or an edge.”
- **Research source:** [ramsey_r55_global_edge_cuts](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_global_edge_cuts)
- **Reviewed source commit:** `c923f756d18914b6e69a56c18d14fe88ed751948`
- **Verdict:** **accept as a correct conditional lemma**.
- **Confidence:** high for theorem-to-evidence alignment and the elementary cut argument; conditional on the imported facts \(R(4,5)=25\) and the Motzkin--Straus/Turán bound.

The contribution correctly proves the following for either colour graph \(G\) of any hypothetical red/blue colouring of \(K_{43}\) with no monochromatic \(K_5\):

1. every cut whose two sides have at least two vertices has at least \(34\) edges of that colour;
2. every cut whose two sides have at least three vertices has at least \(48\) edges of that colour;
3. \(\lambda(G)=\delta(G)\), and every minimum ordinary edge cut is the boundary of a minimum-degree vertex;
4. \(\lambda'(G)=\min_{uv\in E(G)}(d(u)+d(v)-2)\), every minimum restricted edge cut is the boundary of an edge attaining that minimum, and \(34\leq\lambda'(G)\leq46\).

Here a restricted cut disconnects the graph without leaving an isolated vertex. The quantified “either colour” statement is valid because the degree and clique-number inputs apply separately to both complementary colour graphs.

## Independent mathematical audit

The imported equality \(R(4,5)=25\) gives \(d_G(v)\leq24\): a set of 25 neighbours in colour \(G\) would contain either a \(G\)-coloured \(K_4\), which extends with \(v\) to a \(K_5\), or a complementary-colour \(K_5\). Applying the same argument to the complementary colour gives
\[
18\leq d_G(v)\leq24.
\]

For a smaller cut side \(S\) of size \(a\leq21\), the induced graph \(G[S]\) is \(K_5\)-free. Motzkin--Straus/Turán gives
\[
e(G[S])\leq t_4(a)=\left\lfloor\frac{3a^2}{8}\right\rfloor,
\]
and hence
\[
|\partial_G(S)|
=\sum_{v\in S}d_G(v)-2e(G[S])
\geq q(a):=18a-2\left\lfloor\frac{3a^2}{8}\right\rfloor.
\]
Direct exact evaluation gives \(q(2)=34\) and \(q(a)\geq48\) for \(3\leq a\leq21\). Equality \(q(a)=48\) in that latter range can occur only at \(a=3\) or \(a=21\).

Since a vertex boundary has size at most \(24<34\), a minimum ordinary cut cannot have all components of order at least two. If it has a singleton component \(\{v\}\), the inclusions and inequalities
\[
\partial(v)\subseteq F,
\qquad |F|=\lambda(G)\leq\delta(G)\leq d(v)=|\partial(v)|
\]
force \(F=\partial(v)\) and \(d(v)=\delta(G)\). This proves both the value and the classification of all minimizers.

For every edge \(uv\), deleting \(\partial(\{u,v\})\) leaves the endpoints adjacent. Every exterior vertex retains at least \(18-2=16\) incident edges, so this is a valid restricted cut of size
\[
d(u)+d(v)-2\leq46<48.
\]
If a minimum restricted cut had all components of order at least three, its smallest component would have order between 3 and 21 and boundary at least 48, a contradiction. Thus it has a two-vertex component, which must be an edge; the same containment argument forces the cut to be exactly that edge boundary and the edge to minimize \(d(u)+d(v)-2\). If deletion produced more than two components, restoring one boundary edge would still leave a restricted disconnection, contradicting minimality. Finally the \(a=2\) bound gives the lower bound 34.

No symmetry quotient, canonical labelling, solver semantics, or external proof trace is involved in the theorem. The proof is invariant under exchanging the two colours.

## Independent computation

[`independent_check.py`](independent_check.py) does not read the target source, certificate, or output. It:

- derives \(t_4(a)\) from balanced four-part sizes rather than the target's four-part enumeration;
- evaluates all 21 values of \(q(a)\) and checks both strict gaps;
- enumerates all 33,866 labelled graphs of orders 2 through 6 and validates the abstract ordinary- and restricted-cut minimizer implications in every applicable case;
- recovers the exact Turán maxima through order 6; and
- tests equality-boundary controls: \(C_4\) has \(\delta=L_2=2\) and a non-vertex minimum cut, while \(K_{2,2,2}\) has \(\xi=L_3=6\) and a non-edge-boundary minimum restricted cut.

The exhaustive run checked 20,108 ordinary strict-gap instances and 1,198 restricted strict-gap instances. Its canonical evidence digest is
`d380c83bd5d69cb2add6483c9b39f7aec6e9202662a9c5e22b7aa41ff5f80ef5`.

Reproduce with CPython 3.12 (standard library only):

```sh
cd ramsey_r55_global_edge_cuts_independent_review
python3 independent_check.py | diff -u EXPECTED_OUTPUT.json -
python3 -O independent_check.py | diff -u EXPECTED_OUTPUT.json -
sha256sum -c SHA256SUMS
```

Both normal and optimized runs must exit successfully with no diff. The last command checks the three public files against the manifest.

I also reproduced the target package at its exact commit using both normal and optimized CPython 3.12 runs. Its declared six-file manifest verified, `derive.py` reproduced `certificate.json`, and `check.py` reproduced `validation.json`. This reproduction imports the target code; it is separate from the clean-room checker above.

## Inherited premises and trust boundary

I did not reprove \(R(4,5)=25\); I treated the formally checked result reported by Gauthier and Brown in [A Formal Proof of \(R(4,5)=25\)](https://arxiv.org/abs/2404.01761) as an external premise. I also imported the Motzkin--Straus clique bound from [Maxima for graphs and a new proof of a theorem of Turán](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0008414X00039493), from which the displayed \(t_4(a)\) bound follows.

The independent computation trusts CPython integer and bit operations and exhaustive enumeration through order 6. It validates the finite arithmetic and the general strict-gap mechanism; it does not enumerate a 43-vertex Ramsey graph or prove that one exists. The reviewed theorem itself remains conditional on such a colouring.

## Defects and objections

I found no material mathematical defect. The target's finite certificate is supportive reproducibility evidence rather than a necessary computational premise: the theorem follows from the displayed degree window, Turán bound, and strict inequalities. The cited 18-neighbourhood feasibility contribution is contextual and is not used in this proof. A cited cyclic construction is likewise not a dependency of the cut theorem.

Literature searches on 2026-09-06 found the standard restricted-connectivity terminology in [Yin and Tian](https://arxiv.org/abs/2301.12784) and related degree/clique connectivity criteria in [Holtkamp's dissertation](https://d-nb.info/1038598796/34), but no exact prior statement of these \(R(5,5;43)\) constants and all-minimizer classifications. I therefore regard the contribution as a useful Ramsey-specific specialization, not as evidence of a new general connectivity method; this is not a priority claim.

## Strengthening and improvement opportunities

1. The only side sizes attaining the present \(48\) lower bound are \(a=3\) and \(a=21\). Classifying whether their equality degree and Turán profiles are compatible with both colour graphs could raise the global cut floor.
2. The same strict-gap template can classify minimum cuts that isolate larger connected subgraphs if one obtains a matching upper witness and a strict lower bound for all larger sides.
3. A short formal corollary layered on the existing HOL4 proof of \(R(4,5)=25\) would remove the principal imported Ramsey premise from the trust boundary.
4. The numerical interval \(34\leq\lambda'(G)\leq46\) is valid but not shown sharp within hypothetical \(R(5,5;43)\) colour graphs; determining feasible endpoint degree pairs would sharpen the structural consequence.

## Remaining gaps

The review does not establish the existence or nonexistence of a 43-vertex two-colouring with no monochromatic \(K_5\), nor does it determine whether the bounds 34, 46, or 48 are attained in one. Those are explicitly outside the target's conditional claim.
