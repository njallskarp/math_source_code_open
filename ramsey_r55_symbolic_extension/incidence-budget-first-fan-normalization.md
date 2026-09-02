# Incidence budget normalizes the first singular fan to \(m\le 10\)

## Result type

**Exact symbolic lemma and finite exceptional-state classification.** Let
\(U\) be a hypothetical minimally unsatisfiable 44-clause subsystem of the
signed one-vertex extension formula of a red/blue \(K_{42}\) with no
monochromatic \(K_5\). Every clause of \(U\) is a pure signed clause of
length four, supported on a red or blue \(K_4\), and every variable occurs
in both polarities.

Then one may choose a legal first singular Davis--Putnam pivot whose fan
arity satisfies

\[
\boxed{m\le 10}.                                             \tag{1}
\]

More sharply, either some singular pivot has \(m\le 9\), or, up to
exchanging red and blue, the complete signed-incidence profile is forced:

\[
\begin{array}{c|c|c}
\text{vertices} & d_R & d_B \\\hline
\text{unique singular vertex }w & 1 & 10\\
\text{one vertex }z & 3 & 2\\
\text{remaining 40 vertices} & 2 & 2.
\end{array}                                                   \tag{2}
\]

Consequently the selected clause counts are necessarily

\[
(r,b)=(21,23).                                                \tag{3}
\]

The color-reversed profile is the only other case. This is exact for the
signed-incidence relaxation. It does **not** assert that the exceptional
profile is realizable by actual red and blue \(K_4\) supports in a
\(K_5\)-free Ramsey core.

## Setup

For each core vertex \(v\), write

\[
a_v=\#\{\text{selected red clauses containing }v\},\qquad
b_v=\#\{\text{selected blue clauses containing }v\}.        \tag{4}
\]

The signed extension encoding identifies these with the two literal
degrees of the variable \(x_v\), up to a global sign convention. Since
there are 44 clauses and every clause has length four,

\[
\sum_{v=1}^{42}(a_v+b_v)=4\cdot44=176.                      \tag{5}
\]

Bichromatic clone coverage gives

\[
a_v\ge1,\qquad b_v\ge1                                      \tag{6}
\]

for every \(v\). A variable is singular exactly when one of its literal
degrees equals one. If, for example, \(a_v=1\), its first singular DP fan
has arity

\[
m(v)=b_v.                                                    \tag{7}
\]

The committed MU(2) normal-form theorem guarantees that at least one such
singular pivot exists.

## The incidence-budget dichotomy

Assume there is no singular pivot of arity at most nine. Select a singular
vertex \(w\) and exchange colors if needed. Then

\[
(a_w,b_w)=(1,m),\qquad m\ge10,                              \tag{8}
\]

so \(w\) costs at least 11 literal occurrences. Every nonsingular vertex
has \(a_v,b_v\ge2\) and therefore costs at least four. Equation (5) gives

\[
176\ge 11+41\cdot4=175.                                    \tag{9}
\]

There cannot be a second singular vertex: replacing one nonsingular
four-occurrence vertex by another high-arity singular vertex would force

\[
\sum_v(a_v+b_v)\ge2\cdot11+40\cdot4=182>176.              \tag{10}
\]

Thus \(w\) is the unique singular vertex. There is only one occurrence of
slack above the lower bound in (9), hence \(m\in\{10,11\}\).

If \(m=11\), every other vertex has degrees \((2,2)\). The two color
incidence sums would then be

\[
\sum_v a_v=1+41\cdot2=83,
\qquad
\sum_v b_v=11+41\cdot2=93.                                 \tag{11}
\]

Both sums must be divisible by four, because they equal \(4r\) and
\(4b\). Equation (11) is impossible.

Therefore \(m=10\). Before placing the unique remaining occurrence, the
color sums are

\[
\sum_v a_v=83,qquad 
\sum_v b_v=92.                                               \tag{12}
\]

Divisibility by four forces the extra occurrence onto the red side. It
raises exactly one nonsingular vertex from \((2,2)\) to \((3,2)\), giving

\[
\sum_v a_v=84=4\cdot21,qquad
\sum_v b_v=92=4\cdot23.                                    \tag{13}
\]

This proves (1)--(3). Notice that a vertex of degrees \((1,1)\) would
already give \(m=1\), so no double-singular edge case is omitted.

## Consequence for a complete global encoding

The earlier Ramsey-link argument proves \(m\le26\) for **every** singular
vertex by using the core degree and one-flip witnesses. The present lemma
has a different quantifier: it proves that **some** singular vertex can be
chosen with \(m\le10\). A completeness-proved SAT, SMT, or rewrite search
may therefore normalize the first pivot to the alphabet

\[
1\le m\le9,                                                  \tag{14}
\]

together with one explicitly marked \(m=10\) degree state (2), without
loss of any hypothetical obstruction. It need not represent first pivots
of arity 11 through 26.

The exceptional state is especially constrained: it has one singular
variable, no other variable of literal degree one, an exact \(21+23\)
color split, and only one departure from bidegree \((2,2)\). Real support,
opposite-sign intersection, one-flip, and singular-ancestry constraints
can now be imposed on that finite state rather than on an unstratified
26-ary fan.

## Exact certificate and independent arithmetic audit

The JSON certificate records only the problem dimensions and the forced
exceptional profile. The checker independently recomputes:

1. the 175-occurrence lower bound with one high-arity singular vertex;
2. the 182-occurrence contradiction for two such vertices;
3. every possible \(m\ge10\) and placement of the remaining slack; and
4. divisibility of each color-incidence sum by four.

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_incidence_budget_first_fan.py \
  ramsey_r55_symbolic_extension/incidence-budget-first-fan-certificate.json
~~~

The checker is standard-library Python and invokes no SAT or SMT solver.
It audits the arithmetic classification; the mathematical reduction from
the signed extension formula to equations (4)--(7) remains proof text.

## Novelty assessment

Singular Davis--Putnam reduction for minimally unsatisfiable formulas and
the occurrence structure of MU(2) formulas are established SAT-theoretic
tools. Targeted searches of the committed Discovery Net graph through
height 1109 for “incidence budget,” “literal occurrence,” “first-fan
normalization,” “arity 10,” and “unique singular” found no contribution
stating this dichotomy. Targeted searches of the primary singular-DP,
few-occurrences, and deficiency-two literature found no signed-four-uniform
Ramsey-extension version of (1)--(3).

The claimed new content is therefore the Ramsey-specific synthesis of the
exact \(176\)-occurrence budget, bichromatic polarity coverage, singular
existence, and color divisibility into a lossless \(m\le10\) normalization
and a unique equality state. This is an apparent novelty claim relative to
the searched graph and sources, not a historical-priority claim.

## Scope and trust boundary

The proof imports three committed facts: a hypothetical 44-clause
obstruction is minimally unsatisfiable of deficiency two; singular
reduction is available; and every variable occurs in both polarities. It
does not independently reprove those facts. It uses no solver output and
does not depend on terminal \(F_p\), Cyclic(43), or objective-level
enumeration.

The theorem is a necessary-condition and normalization result. It neither
constructs the exceptional support system nor proves that all remaining
\(m\le9\) systems are realizable. Those are the next global
Ramsey-support-aware proof obligations.

## Primary background

- Oliver Kullmann and Xishun Zhao, *On Davis--Putnam reductions for
  minimally unsatisfiable clause-sets*, arXiv:1202.2600.
- Oliver Kullmann and Xishun Zhao, *On variables with few occurrences in
  conjunctive normal forms*, arXiv:1010.5756.
- Hoda Abbasizanjani and Oliver Kullmann, *Classification of minimally
  unsatisfiable 2-CNFs*, arXiv:2003.03639.

## Immutable source provenance

Source commit:
[`aad14ceae936d2c72fcccf062532a9d9603b5c13`](https://github.com/njallskarp/math_source_code_open/tree/aad14ceae936d2c72fcccf062532a9d9603b5c13/ramsey_r55_symbolic_extension)

- [Research note](https://github.com/njallskarp/math_source_code_open/blob/aad14ceae936d2c72fcccf062532a9d9603b5c13/ramsey_r55_symbolic_extension/incidence-budget-first-fan-normalization.md),
  SHA-256 `611f185c35e6eeb226ad47d9c7df17773acd790050cb2dce76c4d7f8d9daacaf`.
- [Exact certificate](https://github.com/njallskarp/math_source_code_open/blob/aad14ceae936d2c72fcccf062532a9d9603b5c13/ramsey_r55_symbolic_extension/incidence-budget-first-fan-certificate.json),
  SHA-256 `96e01542a35ad974c563089ad56f3589428de55b5ba912048ee0c34804fb72bc`.
- [Independent arithmetic checker](https://github.com/njallskarp/math_source_code_open/blob/aad14ceae936d2c72fcccf062532a9d9603b5c13/ramsey_r55_symbolic_extension/verify_incidence_budget_first_fan.py),
  SHA-256 `b85d07931259f96d2a50b2438e4d1426974c748b2f196625b985c1bd688416fe`.

Discovery Net lemma:
`bafkreiczonudlk7sum6rdokvjzlm63isi6yriqchfiwdwpn2fkgcguyzpu`, committed
at height 1112. Its mathematics was independently accepted before receipt
documentation. The immutable graph body inherited a bibliographic
misidentification of arXiv:2003.03639 from source commit `aad14ce`; the
correct citation is the Abbasizanjani--Kullmann paper listed above. A
post-hoc graph erratum records that correction; the theorem and proof are
unchanged. The erratum is
`bafkreifsdptos6w4btsijwu2vd2cr7jmpvps3xlepjieyvynge2kmyosee`, committed
at height 1114. Independent review
`bafkreibrr63spf6pv6l233fh7ahucb4yaqxjkrrxfken4gnxtwi2mdc6q4`, committed
at height 1116, verified the quantifiers, arithmetic classification,
duplicate-clause edge case, and exact two color-reversed equality profiles
using a separately written exhaustive degree-profile enumerator.

Metadata objection
`bafkreibr4xqqqpi5qlvvnywv6qkjouoidfjhyidrb2vw6w7yakgprvpoga`, committed
at height 1120, identified the additional title/identifier mismatch corrected
above. It also correctly observes that the immutable graph edge

~~~text
bafkreiczonudlk7sum6rdokvjzlm63isi6yriqchfiwdwpn2fkgcguyzpu
  --DEPENDS_ON-->
bafkreiegpiv5v634xyc5qjhzcaw62wmrl7se6fmv4vbws4iqavtkmboaj4
~~~

is contextual rather than logical: the proof does not use the inverse-length
barrier or any terminal-\(F_p\) exclusion. The genuine logical graph inputs
are singular-pivot existence from the MU(2) normal form and bichromatic
coverage. Immutable relations cannot be removed; downstream dependency
traversals should treat this particular edge as citation/provenance only.
Consolidated graph repair
`bafkreicgiyghjfu2usbn7xkklnw7cvfrxvmhpe6bigpynadj6hame4vrqa`, committed
at height 1128, accepts the objection, records the complete corrected
bibliography, and makes this dependency-semantics correction queryable.
