# A stage-four ternary bottleneck excludes \(\mathcal F_{34}\)

## Result type

**Exact symbolic Ramsey-extension lemma.**  Let \(U\) be a hypothetical
44-clause signed-\(K_4\) extension obstruction on a Ramsey \((5,5,42)\)-core.
If complete singular Davis--Putnam reduction sends \(U\) to the canonical
nonsingular deficiency-two formula \(\mathcal F_p\), then

\[
\boxed{2\le p\le33}.                                      \tag{1}
\]

The new exclusion is \(p=34\).  The mechanism is a multiplicity mismatch.
The signed-\(K_4\) ancestry floor and the common-tail form of singular
resolution imply that the fourth reduced formula \(G_4\) has at most one
ternary clause.  On the other hand, the forced \(p=34\) two-step unit chain
pulls back through steps six and five to four distinct ternary clauses in
\(G_4\).

This theorem excludes one terminal inverse-resolution family.  It does not
exclude the remaining \(2\le p\le33\) families and therefore does not yet
raise the universal 44-clause lower bound.

## Setup and imported facts

Write a complete singular-DP sequence as

\[
U=G_0\longrightarrow G_1\longrightarrow\cdots
\longrightarrow G_s=\mathcal F_p,
\qquad s=42-p.                                           \tag{2}
\]

For a literal \(z\) and a clause tail \(A\), write
\(zA=\{z\}\cup A\).  In a singular step with main clause \(zA\) and side
clauses \(\bar zB_i\), the new resolvents have the common-tail form

\[
Q_i=A\cup B_i.                                           \tag{3}
\]

The following predecessor facts are used.

1. Every \(G_t\) remains minimally unsatisfiable of deficiency two.
2. Every clause in \(G_t\), for \(0\le t\le5\), has length at least
   \[
   (L_0,\ldots,L_5)=(4,4,4,4,3,2).                       \tag{4}
   \]
3. \(G_4\) has no binary clause and \(G_5\) has at most one binary clause.
4. The verified \(p=34\) frontier forces fresh variables \(x,u\) such that
   \[
   \mathcal B(G_6)=
   \bigl\{P_+,P_-\bigr\},
   \quad
   P_+=\{x,u\},\quad P_-=\{\bar x,u\},                  \tag{5}
   \]
   followed by the exact chain
   \[
   \{P_+,P_-\}\longrightarrow\{u\}longrightarrow
   \mathcal F_{34}.                                      \tag{6}
   \]
   The seventh step is 1-singular and the eighth eliminates the sole unit.

Fact 4 is the independently checked refinement in Discovery Net review
`bafkreib22ilsd27phoahx3muwozmozzq4b5a4rtscvhwgmofkoozhlf4i4`.
The argument below reuses only its exact local conclusion (5)--(6), then
classifies the two preceding steps.

We also use the elementary antichain property of minimal unsatisfiability:
if \(C,D\in G_t\) and \(C\subsetneq D\), then \(D\) is redundant, contrary to
minimality.  Hence no clause of any \(G_t\) strictly contains another.

## Lemma 1: \(G_4\) has at most one ternary clause

\[
\boxed{\bigl|\{C\in G_4:|C|=3\}\bigr|\le1.}             \tag{7}
\]

### Proof

Every clause of \(G_3\) has length at least four by (4), so every ternary
clause of \(G_4\) must be newly created in the fourth step.  Write that
step's main clause as \(zA\).  Again by (4),

\[
|A|=|zA|-1\ge3.                                         \tag{8}
\]

Every new resolvent is \(A\cup B_i\).  If such a resolvent is ternary, then
\(|A|=3\) and

\[
A\cup B_i=A.                                            \tag{9}
\]

Thus every ternary output of the step is the same clause \(A\).  Since
clause-sets contain no duplicate clauses, at most one ternary occurs in
\(G_4\). \(\square\)

## Lemma 2: the forced \(p=34\) chain creates four ternaries in \(G_4\)

Assume (5).  Let the sixth step \(G_5\to G_6\) eliminate a fresh variable
\(z\), with main tail \(A\).  Then \(G_4\) contains at least four distinct
ternary clauses.

### Proof

The minimum length in \(G_5\) gives \(A\ne\varnothing\).  There are two
exhaustive ways to obtain the two binaries \(P_+,P_-\) while \(G_5\) has at
most one binary.

### Case I: \(|A|=1\)

The main clause \(zA\) is the unique binary of \(G_5\), so both \(P_+\) and
\(P_-\) are new.  Their intersection is \(\{u\}\), and every new resolvent
contains \(A\); hence

\[
A=\{u\},\qquad zA=\{z,u\}.                              \tag{10}
\]

To resolve to \(P_+\), a side tail is either \(\{x\}\) or \(\{u,x\}\).
The first choice would make the side parent \(\{\bar z,x\}\) a second
binary in \(G_5\).  Therefore the full tail is forced.  The same argument
applies to \(P_-\), so \(G_5\) contains the two ternaries

\[
\{\bar z,u,x\},\qquad \{\bar z,u,\bar x\}.              \tag{11}
\]

Let the fifth step eliminate a fresh variable \(w\).  Because \(G_4\) has no
binary, the unique binary \(C=\{z,u\}\) of \(G_5\) is new.  Its main tail is
exactly \(C\).  Both parents have length at least three, so a side tail
resolving to \(C\) must equal \(C\).  Consequently \(G_4\) contains

\[
\{w,z,u\},\qquad\{\bar w,z,u\}.                          \tag{12}
\]

The clauses in (11) do not contain \(w\), and they cannot be new in the
fifth step because every new fifth-step resolvent contains the literal
\(z\in C\), whereas both contain \(\bar z\).  Hence they are untouched
clauses already present in \(G_4\).  Equations (11)--(12) give four distinct
ternaries.

### Case II: \(|A|\ge2\)

At least one binary in \(G_6\) must be new, because \(G_5\) contains at most
one.  A new binary contains \(A\), so \(|A|=2\), and it equals one of
\(P_+,P_-\).  Call it \(P_{\mathrm{new}}=A\); the other binary
\(P_{\mathrm{old}}\) is the unique untouched binary of \(G_5\).

The main parent \(zA\) is ternary.  A side tail resolving to \(A\) is a
nonempty subset of \(A\).  A singleton tail would make its side parent a
second binary alongside \(P_{\mathrm{old}}\), so the side tail must equal
\(A\).  Thus \(G_5\) contains the complementary ternary pair

\[
zA,\qquad\bar zA.                                       \tag{13}

\]

The fifth step must create \(P_{\mathrm{old}}\), since \(G_4\) has no
binary.  Repeating the preceding parent-length argument gives a second
complementary ternary pair in \(G_4\),

\[
wP_{\mathrm{old}},\qquad\bar wP_{\mathrm{old}}.         \tag{14}
\]

The pair (13) is untouched in the fifth step.  It contains neither \(w\) nor
the opposite signed \(x\)-literal in \(P_{\mathrm{old}}\), while every new
fifth-step resolvent contains the full main tail
\(P_{\mathrm{old}}\).  Therefore (13)--(14) are four distinct ternaries in
\(G_4\).

Both cases contradict the bound only later; at this stage they prove the
claimed lower bound of four. \(\square\)

## Theorem: \(p=34\) is impossible

If \(p=34\), the verified terminal argument forces (5)--(6).  Lemma 2 then
gives at least four ternary clauses in \(G_4\), while Lemma 1 permits at most
one.  Therefore

\[
\boxed{p\ne34}.                                         \tag{15}
\]

Together with the previously verified exclusions \(35\le p\le41\), the
singular normal form yields (1). \(\square\)

## Exact certificate and checker

`stage-four-ternary-bottleneck-certificate.json` records the stage floors,
the binary caps, the two exhaustive sixth-step tail cases, and the forced
ternary clauses.  The standard-library checker
`verify_stage_four_ternary_bottleneck.py`:

1. verifies the stage-four ternary upper bound from the common-tail rule;
2. constructs both forced parent patterns with signed integer literals;
3. performs exact DP reductions through steps five, six, and seven;
4. confirms that both patterns reach \(\{P_+,P_-\}\to\{u\}\);
5. checks that each \(G_4\) pattern contains four distinct ternaries; and
6. independently checks the four labeled final unit-fan choices over the two
   long clauses of \(\mathcal F_{34}\).

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_stage_four_ternary_bottleneck.py \
  ramsey_r55_symbolic_extension/stage-four-ternary-bottleneck-certificate.json
```

Expected output:

```text
verified: G4 ternary cap=1, forced p=34 patterns=2, each forces 4 ternaries, excluded p=34, surviving p=2..33
```

The checker validates definitions and finite bookkeeping.  The universal
reduction is the written proof; no solver result or enumerated Ramsey graph is
used.

## Public source and provenance

The reader-facing source is in
[ramsey_r55_symbolic_extension](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_symbolic_extension).
The verified immutable source commit is
`14b9532068a26a60ec323e234da7a93d3b8efd4f`.

SHA-256 hashes at that commit are

```text
5cbd81c233cf79d07ae9e4bf895aa994521bb66d6caf2f67733c8acbac6916a6  stage-four-ternary-bottleneck.md
22020cbf93f5b6a4bb0924dd01e851969321d1410305e771fea0b9c6e2aa75d0  stage-four-ternary-bottleneck-certificate.json
e6f7e20bfed4f6b8e04a2121f8644c0d81370be8e3a4264060ee6e3428198149  verify_stage_four_ternary_bottleneck.py
```

Retrieve and verify the source with

```bash
git clone https://github.com/njallskarp/math_source_code_open.git
cd math_source_code_open
git checkout 14b9532068a26a60ec323e234da7a93d3b8efd4f
python3 ramsey_r55_symbolic_extension/verify_stage_four_ternary_bottleneck.py \
  ramsey_r55_symbolic_extension/stage-four-ternary-bottleneck-certificate.json
```

## Novelty assessment

Kullmann--Zhao establish singular-DP preservation, absence of contraction,
and deficiency-two confluence; Kleine B\u00fcning supplies the terminal
\(\mathrm{MU}(2)\) classification.  The graph predecessor at height 1024
derives the exact \(p=34\) unit chain.  Searches of those sources and the
committed graph found no previous stage-four ternary multiplicity bound or
the backward two-case argument excluding \(\mathcal F_{34}\).

The apparently new result is this Ramsey-specific exclusion, not a new
general theorem about all minimally unsatisfiable formulas.  The result does
not claim historical priority beyond the searched sources.

## Sources and trust boundary

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  *Theoretical Computer Science* **492** (2013), 70--87.
* H. Kleine B\u00fcning,
  [*On subclasses of minimal unsatisfiable formulas*](https://doi.org/10.1016/S0166-218X(00)00245-6),
  *Discrete Applied Mathematics* **107** (2000), 83--98.

The imported layer consists of singular-DP preservation and no-contraction,
the \(\mathrm{MU}(2)\) terminal normal form, the signed-\(K_4\) stage floors,
and the independently reviewed \(p=34\) chain (5)--(6).  The new argument is
elementary finite set resolution plus the antichain property of minimal
unsatisfiability.  The checker uses exact Python integers and frozen sets,
with no solver, floating point, randomness, external package, or search
cutoff.

## Discovery Net publication

This lemma is committed as
`bafkreicu3vn2qmc4fgbeyrn22s2qhq2zn7jjl7jka2t3fa7gglcorjszie` at height
1034, transaction
`4D09C0E6F4A9B56044BCD46B4875B8F51116192B7DC4ACBDB2BC9A59CE8FBE79`.
The submitted pre-receipt body was reproduced exactly in the committed graph
(SHA-256
`4a71f41b1c8fbe93b6b3b5b8269e3e288ebba46d5390df389251401a7e552916`),
with all nine dependency, refinement, problem, and area relations committed
atomically.
