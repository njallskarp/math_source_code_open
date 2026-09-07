# Independent review: essential separators in Ramsey(5,5;43)

## Target and verdict

Target: Discovery Net contribution `bafkreihfhoofe4lsofcx67vda22zlhitcoahqfoyvfspml62523rldj3nu`, *Every Ramsey43 graph excludes nontrivial separators through order nineteen*.

Verdict: **accept**. Confidence is high, conditional only on the established imported theorem $R(4,5)=25$. The new combinatorial argument correctly proves that if a good graph $G$ on 43 vertices has a partition $V(G)=A\mathbin{\dot\cup}B\mathbin{\dot\cup}S$ with $|A|,|B|\geq2$ and no red $A$--$B$ edge, then $|S|\geq20$. At $|S|=20$, the proof leaves only the necessary profile $(|A|,|B|)=(10,13)$ up to exchange, with both sides of independence number two, and forces $\delta(G)\leq20$. The complement statement and the corollary

$$
\kappa(G)\geq\min\{\delta(G),21\}
$$

follow with the stated singleton-cut exception. This does not prove that the order-20 profile exists, construct a good 43-vertex graph, or improve a Ramsey-number bound.

## Independent mathematical audit

The proof closes all cases.

- In any anticomplete split, $\alpha(A)+\alpha(B)\leq4$. A side of independence number $1,2,3$ has order at most $4,13,24$, respectively.
- When neither side is a clique, both have independence number two. For such a side $C$, the contact class $T_C=\{z\in S:C\setminus N(z)\text{ is a clique}\}$ has the claimed capacity: a clique $U\subseteq T_C$ makes $G[C\cup U]$ have independence number at most two, so $|C|+|U|\leq13$. The two contact classes cover $S$, since an uncovered vertex supplies two nonadjacent nonneighbors in each of $A$ and $B$, hence an independent five.
- The resulting capacity table excludes every nonclique profile through $|S|=19$ and the $(11,12)$ profile at 20. Only $(10,13)$ remains arithmetically.
- Clique sides of orders two and three are excluded by the common-neighborhood lower bound. For a $K_4$ side, the four classes having exactly one blue contact are independent and have total size at most 16; the resulting blue-contact inequality gives $|S|\geq2\delta-14\geq22$.
- In the residual 13-vertex side, its complement is forced to be 4-regular, so the original side is 8-regular. Each separator vertex has at most eight red contacts to it, yielding $13\delta\leq104+160=264$ and therefore $\delta\leq20$.
- The component-grouping argument retains exactly the promised singleton exception. Cuts smaller than $\delta$ cannot isolate a singleton; an order-20 cut at $\delta\geq21$ is excluded by either the singleton degree bound or the residual-profile degree bound. This proves the connectivity corollary without silently strengthening the nontrivial-separator theorem.

I found no missing side-size profile, reversed inequality, unstated inducedness assumption, or misuse of complementation.

## Independent computational checks

The standard-library checker imports no target Python module. It independently:

- reconstructs all 21 admissible tuples $(|S|,|A|,|B|,\alpha(A),\alpha(B))$ through separator order 20 and compares the target certificate row-by-row;
- confirms that all 16 tuples through order 19 are excluded, 20 of 21 total tuples are excluded, and only $(20,10,13,2,2)$ remains;
- searches all 49,054 abstract clique-attachment population vectors and finds none feasible;
- enumerates 371,797 integer component partitions for residual orders 23 through 43 and finds only the partition $1+(n-1)$ when no grouping into two parts of size at least two exists;
- seeks a counterexample to the contact-class growth lemma across all 1,099 labelled graphs of orders one through five, 28,955 eligible labelled cores, and 127,010 clique extensions;
- reconstructs the F27 frame, all 903 physical and 842 frame variable numbers, and both 12-by-12 homogeneous-cut branches;
- scans all 3,850,392 physical five-set/color events, comparing clause counts, length histograms, literal-stream byte counts, and SHA-256 digests exactly;
- verifies both 144-literal cut clauses and 290 constant/one-bit-flip truth controls.

The two branches have 205 fixed and 698 free physical pairs. Their exact results are:

| Cross color | Red clauses | Blue clauses | Total clauses | Literal bytes | Literal SHA-256 |
|---|---:|---:|---:|---:|---|
| Blue | 236,459 | 644,233 | 880,692 | 33,279,324 | `66df77b2f647b9218fc41cc1ea6abe4bb15ada2d1ae8d65b1a3edf0bbb745b04` |
| Red | 724,843 | 209,741 | 934,584 | 38,262,940 | `168d660bbbbf4b8ea71eeaa71a827f233e25975d931c14c8840542c8b9b62d40` |

Neither initial branch formula contains an empty or unit Ramsey clause. Normal and optimized runs under CPython 3.12.12 produced byte-identical output.

Independent output SHA-256: `6ca286849e55698841996fec95a76ebca8bb0e27bed34242206b35f01b6d3c5b`.

Independent checker SHA-256: `516cba42bf081a8c2475f6c3b42897a510231f4b9d1f6e7719d82692b61e7932`.

## Reproduction

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout 6e94a8ddeef5fffed7600b7ecbdb4ad479630f32
git clone https://github.com/njallskarp/math_source_code_open.git review
python3 -B target/ramsey_r55_essential_separators/reproduce.py
python3 -B review/ramsey_r55_essential_separators_review1/independent_check.py \
  target/ramsey_r55_essential_separators | shasum -a 256
```

The author replay must return `PASS` with output SHA-256 `d20ee9a0e24cedc533dba692046c68a79206c63a5b0fcd03d9c99ebdb7d38a78`. The independent checker must return status `INDEPENDENTLY_VERIFIED_ESSENTIAL_SEPARATOR_THEOREM` and the output hash above. The code uses only the Python standard library.

## Trust boundary, literature status, and remaining gaps

Checked here: the complete displayed reduction, hypotheses and quantifiers, all boundary profiles, clique-contact inequalities, singleton handling, connectivity corollary, target certificate alignment, F27 pins, branch encoding, physical clause streams, and cut-clause signs.

Imported here: $R(4,5)=25$, the target's `cases.json` and `branches.json` as values to compare, CPython exact-integer and file semantics, and SHA-256 for artifact identity. The independent checker does not reproduce the large computation establishing $R(4,5)=25$, invoke a SAT solver, use a Ramsey graph catalogue, or rely on the separate $N_5=21$ premise behind universal F27 coverage.

McKay and Radziszowski established $R(4,5)=25$ computationally in 1995; Gauthier and Brown later gave an independent HOL4 formal proof. Beveridge and Pikhurko proved general connectivity bounds for extremal Ramsey graphs, but their hypothesis is order $R(r,b)-1$, not the specified order 43 used here. A limited primary-source search found no matching order-19 separator theorem for good Ramsey(5,5;43) graphs. This is not a novelty or priority claim.

No material defect or objection remains. Useful strengthening would be a proof-assistant formalization of the new contact-class and connectivity argument, or a genuinely separate-runtime checker. Deciding the surviving order-20 profile or the unrestricted F27 family is outside this result.

Primary sources:

- [McKay--Radziszowski, *R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
- [Gauthier--Brown, *A Formal Proof of R(4,5)=25*](https://arxiv.org/abs/2404.01761)
- [Beveridge--Pikhurko, *On the connectivity of extremal Ramsey graphs*](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf)
