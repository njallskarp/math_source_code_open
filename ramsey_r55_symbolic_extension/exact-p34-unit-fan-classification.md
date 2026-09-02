# Exact classification of the \(p=34\) terminal unit fan

## Result type

**Exact symbolic classification.**  Assume the forced local chain for a
hypothetical \(p=34\) inverse singular-DP history,

\[
\mathcal B(G_6)=
\bigl\{\{x,u\},\{\neg x,u\}\bigr\}
\longrightarrow \{u\}\in G_7
\longrightarrow G_8=\mathcal F_{34}.                   \tag{1}
\]

Then the final unit-elimination fan is completely determined except for two
independent binary choices: all 34 terminal cycle clauses must be side tails,
while each of the two long terminal clauses may independently be a side tail
or an untouched clause.  Consequently there are

\[
\boxed{4\text{ labeled fans and }3\text{ isomorphism classes}.}           \tag{2}
\]

All four labeled fans are locally valid minimally unsatisfiable
deficiency-two singular extensions.  They are nevertheless globally
impossible as signed-\(K_4\) histories because the separately proved
stage-four ternary bottleneck excludes \(p=34\).

This note finishes the \(p=34\) unit-chain classification.  It does not
continue the terminal parameter descent and does not assert anything new
about \(p\le33\).

## Terminal formula and unit extensions

Write

\[
Z_p=\bigl\{C_i=\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\bigr\},
\tag{3}
\]

\[
L^+=\{y_1,\ldots,y_p\},\qquad
L^-=\{\neg y_1,\ldots,\neg y_p\},                       \tag{4}
\]

so that

\[
\mathcal F_p=Z_p\cup\{L^+,L^-\}.                        \tag{5}
\]

Let the final step eliminate the unit \(\{u\}\).  For a set
\(S\subseteq\mathcal F_p\), define

\[
E_S=
\{\{u\}\}
\cup\bigl\{\{\neg u\}\cup C:C\in S\bigr\}
\cup(\mathcal F_p\setminus S).                          \tag{6}
\]

If \(S\ne\varnothing\), then \(u\) is singular in \(E_S\) and

\[
\operatorname{DP}_u(E_S)=\mathcal F_p.                 \tag{7}
\]

Conversely, every collision-free inverse singular step with main unit
\(\{u\}\) and terminal formula \(\mathcal F_p\) has the unique form (6).
Indeed, a side clause \(\{\neg u\}\cup B\) resolves to exactly \(B\), so its
tail must be one terminal clause.  No-contraction makes the generated and
untouched terminal clauses disjoint, giving a unique selection set \(S\).

## Lemma 1: every nonempty selection is a valid MU(2) unit extension

For every nonempty \(S\subseteq\mathcal F_p\),

\[
E_S\in\mathrm{MU}(2).                                   \tag{8}
\]

### Proof

The unit \(u=1\) reduces (6) to \(\mathcal F_p\), so \(E_S\) is
unsatisfiable.  It has one more variable and one more clause than
\(\mathcal F_p\), hence preserves deficiency two.

Minimality is direct.  If the unit is removed, set \(u=0\); all side clauses
are then true, and the untouched proper subformula
\(\mathcal F_p\setminus S\) is satisfiable because \(S\ne\varnothing\) and
\(\mathcal F_p\) is minimally unsatisfiable.  If a side clause indexed by
\(C\in S\) is removed, set \(u=1\) and use a satisfying assignment of
\(\mathcal F_p\setminus\{C\}\).  The same assignment with \(u=1\) works
after removing an untouched clause \(C\notin S\). \(\square\)

Thus the reviewer's count \(2^{36}-1\) is correct for unrestricted labeled
inverse unit extensions of \(\mathcal F_{34}\).  The additional binary-family
condition in (1) is what collapses that set.

The preceding 1-singular split is locally valid as well.  Replacing
\(\{u\}\) in \(E_S\) by \(\{x,u\},\{\neg x,u\}\) preserves deficiency and
minimal unsatisfiability: the pair forces \(u=1\); deleting either member is
witnessed by \(u=0\) and a suitable value of \(x\); and deleting any other
clause is witnessed by \(u=1\) together with a deletion witness for the
corresponding clause of \(\mathcal F_p\).  Hence every nonempty \(S\) gives a
locally valid two-step \(\mathrm{MU}(2)\) chain, before the earlier
signed-\(K_4\) history is imposed.

## Lemma 2: compatibility forces all cycle clauses into the fan

Let

\[
P_+=\{x,u\},\qquad P_-=\{\neg x,u\}.                   \tag{9}
\]

The 1-singular inverse step preceding (6) replaces \(\{u\}\) by
\(P_+,P_-\), so

\[
G_6(S)=
\{P_+,P_-\}
\cup\bigl\{\{\neg u\}\cup C:C\in S\bigr\}
\cup(\mathcal F_{34}\setminus S).                      \tag{10}
\]

The binary clauses of this formula are exactly

\[
\mathcal B(G_6(S))=
\{P_+,P_-\}\cup(Z_{34}\setminus S).                    \tag{11}
\]

### Proof

The pair \(P_+,P_-\) is binary.  A selected cycle clause acquires the fresh
literal \(\neg u\) and becomes ternary; an unselected cycle clause remains
binary.  The two long clauses have length 34 when untouched and length 35
when selected, so they never contribute a binary.  These exhaust (10).
\(\square\)

The exact chain (1) requires
\(\mathcal B(G_6(S))=\{P_+,P_-\}\).  Equation (11) therefore gives the
equivalence

\[
\boxed{G_6(S)\text{ is compatible with (1)}
\iff Z_{34}\subseteq S.}                                \tag{12}
\]

## Theorem: four labeled fans, three symmetry classes

By (12), a compatible selection has the unique form

\[
S_T=Z_{34}\cup T,
\qquad T\subseteq\{L^+,L^-\}.                           \tag{13}
\]

There are therefore \(2^2=4\) labeled fans.

For the isomorphism quotient, define the signed permutation on terminal
variables, using indices in \(\mathbb Z/34\mathbb Z\), by

\[
\phi(y_i)=\neg y_{-i}.                                  \tag{14}
\]

It reverses the directed cycle, preserves \(Z_{34}\), and swaps
\(L^+\leftrightarrow L^-\).  Fixing \(u\) and \(x\), it identifies the two
fans with \(|T|=1\).

Fans with different \(|T|\) cannot be isomorphic because their clause-length
profiles contain respectively \(|T|\) clauses of length 35 and
\(2-|T|\) clauses of length 34.  Hence the three canonical classes are

\[
|T|=0,\qquad |T|=1,\qquad |T|=2.                        \tag{15}

\]

This proves (2). \(\square\)

## Exact checker

`exact-p34-unit-fan-certificate.json` records the selection theorem, labeled
count, orbit representatives, and clause-length profiles.  The
standard-library checker `verify_exact_p34_unit_fans.py`:

1. reconstructs \(\mathcal F_{34}\) and explicit deletion witnesses for its
   minimal unsatisfiability;
2. proves the binary-family identity (11) clause by clause;
3. derives the count \(2^{36-34}=4\), rather than assuming four examples;
4. constructs every compatible fan and checks
   \(G_6\to E_S\to\mathcal F_{34}\) by exact DP reduction;
5. checks explicit clause-deletion witnesses for every \(E_S\) and \(G_6(S)\);
6. verifies the complement-reversal isomorphism for the two \(|T|=1\) fans;
   and
7. verifies that the three orbit representatives have distinct length
   profiles.

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_exact_p34_unit_fans.py \
  ramsey_r55_symbolic_extension/exact-p34-unit-fan-certificate.json
```

Expected output:

```text
verified: unrestricted=2^36-1, compatible labeled fans=4, symmetry classes=3, long-selection sizes=[0, 1, 2]
```

The checker audits the finite classification and witnesses.  The universal
bridge from a final singular unit step to (6), and the use of the exact binary
family in (1), are the written proof obligations.

## Public source and provenance

The reader-facing source is in
[ramsey_r55_symbolic_extension](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_symbolic_extension).
Immutable source provenance and hashes are added after the scoped source
commit is published.

## Novelty assessment

Kullmann--Zhao develop singular extensions and the no-contraction property.
The committed height-1024 review proves the exact \(p=34\) unit chain, and the
height-1050 review correctly observes that a general inverse unit extension
has \(2^{36}-1\) labeled selections and that the predecessor checker had only
constructed four examples.  The new contribution proves why the exact
binary-family condition selects precisely those four and computes their
three isomorphism classes.

Searches of the primary singular-DP literature and the committed graph found
no previous version of this Ramsey-specific unit-fan classification.  This is
search-relative novelty, not a claim of historical priority.

## Scope and trust boundary

The result classifies the last two steps of the counterfactual \(p=34\)
history.  It does not undo the independent theorem that no full signed-\(K_4\)
history with \(p=34\) exists.  It also does not classify arbitrary inverse
unit extensions without condition (1).

The imported layer is the \(\mathrm{MU}(2)\) terminal form, singular-DP
no-contraction, and the independently reviewed exact pair/unit chain.  The
new proof uses only clause sets, minimal-unsatisfiability witnesses, and one
explicit signed permutation.  The checker uses exact Python integers and
frozen sets; it has no solver, floating point, randomness, external package,
or search cutoff.

## Sources

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  *Theoretical Computer Science* **492** (2013), 70--87.
* O. Kullmann and X. Zhao,
  [*Bounds for variables with few occurrences in conjunctive normal forms*](https://arxiv.org/abs/1408.0629),
  *Theoretical Computer Science* **556** (2014), 23--51; Section 5.2 treats
  singular DP extensions.
