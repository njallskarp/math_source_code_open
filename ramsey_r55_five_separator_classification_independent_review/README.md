# Independent review of the dense five-separator classification

## Verdict and exact scope

**Accepted with high confidence.** Let \(H\) be a simple graph on 22 vertices
with no \(K_4\) and no independent five-set. If \(e(H)\geq109\) and some set
of at most five vertices disconnects \(H\), then \(H\) is isomorphic to one
of the thirteen previously classified degree-five graphs. Every representative
has 109 edges, connectivity five, and a unique separator of size at most five:
the neighborhood of its unique degree-five vertex. Consequently
\[
e(H)\geq110\quad\Longrightarrow\quad\kappa(H)\geq6.
\]
The density threshold is sharp because the thirteen 109-edge examples have
connectivity five.

Reviewed Discovery Net contribution:

- <code>bafkreif2nn6u2wtwqapszy7bdof2mudmijhsjsjshvgbtow5dsrwp7mt6q</code>,
  height 3375, “Dense five-separator neighborhoods: thirteen marked classes
  and six-connectivity”;
- target source commit
  <code>e5eff475fe1d86f9bca55649e183637611423e01</code>;
- [target source directory](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_five_separator_classification).

This is a complete local small-separator classification, not an exclusion of
any of the thirteen unrestricted 43-vertex completion families. It neither
classifies the higher-connectivity order-22 graphs nor improves a Ramsey bound.

## Independent audit of the separator theorem

Let \(S\) be a cut, \(s=|S|\leq5\), and let \(C_1,\ldots,C_r\) be the
components of \(H-S\). Their independence numbers add, so
\(\sum_i\alpha(C_i)\leq4\), and each is at most three. The classical bounds
\(R(4,2)=4\), \(R(4,3)=9\), and \(R(4,4)=18\) give maximum component orders
3, 8, and 17 when the respective independence numbers are 1, 2, and 3.
At least 17 vertices remain. Of the partitions of an independence budget at
most four into at least two positive parts, only \(1+3\) has total capacity
at least 17; \(2+2\), \(1+1+2\), and \(1+1+1+1\) have capacities only
16, 14, and 12.

Thus \(H-S\) consists of a clique \(B\), of order \(b\in\{1,2,3\}\), and a
component \(A\) with \(\alpha(A)\leq3\). The nine possible
\((s,|A|,b)\) profiles are
\[
\begin{split}
 &(2,17,3),\\
 &(3,16,3),(3,17,2),\\
 &(4,15,3),(4,16,2),(4,17,1),\\
 &(5,14,3),(5,15,2),(5,16,1).
\end{split}
\]
If every degree were at least six, \(b=1\) is immediate nonsense. For
\(b=2\), minimum degree forces \(s=5\) and complete incidence from \(B\) to
\(S\). An edge in \(S\) then completes a \(K_4\) with \(B\), while no such
edge makes \(S\) an independent five-set. For \(b=3\), each vertex of \(S\)
meets at most two vertices of the triangle \(B\), so
\[
\sum_{v\in B}d_H(v)\leq6+2s\leq16<18.
\]
This proves \(\kappa(H)\leq5\Rightarrow\delta(H)\leq5\), including all
boundary profiles and without a catalogue premise.

Degrees at most three are impossible: the at least 18 nonneighbors of such
a vertex would induce a graph with neither a \(K_4\) nor an independent
four-set. If \(d(z)=4\), its 17 nonneighbors \(A\) have independence number
at most three. Every vertex has at most eight neighbors inside \(A\), and
each of the four neighbors of \(z\) has at most eight neighbors in \(A\), by
\(R(3,4)=9\). The four neighbors induce a triangle-free graph with at most
four edges. Hence
\[
e(H)\leq e(A)+e(A,N(z))+e(N(z))+d(z)
       \leq68+32+4+4=108.
\]
At density 109 the bridge therefore forces degree exactly five, where the
previously reviewed thirteen-class census applies.

Each imported representative has a unique degree-five vertex \(z\), and all
other degrees are at least nine. In any small cut, every vertex of the clique
component \(B\) has degree at most \(b-1+s\leq7\); hence \(B=\{z\}\). The cut
must contain all five neighbors of \(z\), so it is exactly \(N(z)\). Conversely,
deleting \(N(z)\) isolates \(z\). This establishes connectivity five and
uniqueness of the marked cut.

The Hamiltonicity claims also align exactly with the cited theorem. From
\(\kappa(H)\geq6\), deleting at most two vertices leaves connectivity at
least four and independence number at most four, so Chvátal–Erdős Theorem 1
gives a Hamiltonian cycle. Deleting at most one vertex leaves connectivity
at least five and no independent five-set, so their Theorem 3 gives
Hamiltonian-connectedness.

## Clean-room finite verification

The independent standard-library checker imports only the target
<code>inputs.json</code>, pinned by SHA-256
<code>1d025db88615f7dfa93bb33a4179db87137328877d3eea99fc7a80774c0c2105</code>.
It ignores all target Python, expected outputs, core encodings, attachment
columns, flow results, and deletion lists. It strictly decodes only the
thirteen complete graph6 records and independently verifies:

- order 22, exactly 109 edges, no \(K_4\), and no independent five-set;
- one degree-five vertex and degree at least nine everywhere else;
- all nine component profiles and the 630-edge unrestricted global interface;
- the connectivity of every graph after deleting its degree-five vertex.

The connectivity algorithm differs from both target implementations. For a
connected 21-vertex graph, every vertex separator has a component of order at
most ten. The checker enumerates every nonempty \(C\) with \(|C|\leq10\) and
computes its external boundary \(N(C)\). If vertices remain outside
\(C\cup N(C)\), then \(N(C)\) is a separator; conversely, the smallest
component of every separation appears in this enumeration. Thus this is an
exact connectivity computation, not sampling.

It examined
\[
13\sum_{j=1}^{10}\binom{21}{j}
=13\,(2^{20}-1)
=13{,}631{,}475
\]
boundary subsets. The resulting connectivity vector for the hub-deleted
representatives is
\[
(9,9,9,9,9,9,9,9,9,9,9,8,9).
\]
The aggregate deterministic boundary digest is
<code>e464b53531a9c7476e3800ff7ef3e9a6ed2876a42227e1b9b3844aadfb5b5cee</code>.
As non-premise cross-checks, NetworkX 3.6 and the target's integral-flow
routine returned the same exact vector.

On all 1,098 labeled graphs of orders two through five, the boundary algorithm
agrees with a literal deleted-set connectivity implementation. The graph6
decoder round-trips every one of those graphs, and eight malformed records are
rejected. Ordinary and optimized CPython executions match the frozen expected
result byte for byte.

## Imported target reproduction, kept separate

At the detached target commit, all seven target manifest entries matched.
The online import check fetched the pinned earlier certificate and verified
its hash and extracted records. Both ordinary and optimized executions of the
target's deletion checker, vertex-flow audit, and controls matched their
expected files. The exhaustive deletion run checked 460,759 candidate
deletions in about 5.5 seconds; the separate flow audit and small-graph controls
also passed.

Those executions reproduce author evidence. They are not premises of the
clean-room boundary result.

## Reproduction

CPython 3.11 or newer and its standard library suffice:

~~~bash
work=$(mktemp -d)
git clone https://github.com/njallskarp/math_source_code_open "$work/target"
git -C "$work/target" checkout --detach e5eff475fe1d86f9bca55649e183637611423e01
python3 -B ramsey_r55_five_separator_classification_independent_review/check.py \
  "$work/target/ramsey_r55_five_separator_classification/inputs.json" \
  | cmp - ramsey_r55_five_separator_classification_independent_review/EXPECTED_RESULT.json
python3 -O -B ramsey_r55_five_separator_classification_independent_review/check.py \
  "$work/target/ramsey_r55_five_separator_classification/inputs.json" \
  | cmp - ramsey_r55_five_separator_classification_independent_review/EXPECTED_RESULT.json
(cd ramsey_r55_five_separator_classification_independent_review && \
  shasum -a 256 -c SHA256SUMS)
~~~

Expected status:
<code>INDEPENDENTLY_VERIFIED_DENSE_FIVE_SEPARATOR_CLASSIFICATION</code>.
Expected result SHA-256:
<code>5110e0622a652c49b6443aa50b72eefc9c4dd8c202f3c96d72b59e090092ff14</code>.

## Literature status and publication readiness

[Beveridge–Pikhurko](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf)
prove connectivity bounds for extremal Ramsey graphs on \(R(r,b)-1\)
vertices; their hypothesis does not cover these nonextremal 22-vertex
\((4,5)\)-graphs. The current
[Angeltveit–McKay paper](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029)
records the much denser order-22 families used for \(R(5,5)\leq46\), while
[McKay's primary data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
provides the underlying Ramsey catalogues. The exact Hamiltonian and
Hamiltonian-connected criteria are Theorems 1 and 3 of
[Chvátal–Erdős](https://www.renyi.hu/~p_erdos/1972-02.pdf).

Candidate-specific searches for the exact \(R(4,5;22)\), density-109,
five-separator, marked-class, and six-connectivity statements found no earlier
public result. This supports “apparently new to the searched sources,” not a
historical-priority claim.

The contribution is publication-ready as a precise local structural theorem.
The short universal reduction is complete, the imported census was already
independently reviewed, and the new finite consequences now have a third
algorithmic verification.

## Defects or objections

No material defect was found. The component decomposition includes every
independence-budget and separator-size boundary case. The density estimate,
catalogue dependency, marked/unmarked quotient, Hamiltonicity corollaries,
630-edge global interface, and explicit noncoverage statements all align with
the evidence.

## Strengthening and improvement opportunities

1. **Promote the exact hub-deleted connectivity vector (proved here).**
   The thirteen values are twelve 9s and one 8, strictly strengthening the
   target's six-connectivity check for these representatives. A structural
   explanation for the exceptional class, rather than another enumeration,
   would turn this finite refinement into useful classification data.
2. **Test whether density 110 forces seven-connectivity (high impact,
   unresolved).** A six-cut leaves 16 vertices and introduces the additional
   \(2+2\) independence-budget profile. A proof must exclude both the
   \(1+3\) and \(2+2\) component cases using the density budget, or exhibit a
   valid counterexample. The present theorem gives only six-connectivity.
3. **Classify all density-109 connectivity types (finite but larger).**
   The theorem identifies exactly the graphs with connectivity at most five,
   not all 109-edge graphs. A complete catalogue-free reduction or a pinned
   census could determine the distribution for connectivity at least six.
4. **Formalize the universal bridge (confidence improvement).** Formalizing
   the independence-budget decomposition, the degree-four edge bound, and the
   marked-cut uniqueness argument would leave only the earlier thirteen-class
   census and classical small Ramsey bounds as substantial external premises.

## Trust boundary

The theorem imports the previously reviewed completeness of the thirteen
degree-five classes, which in turn imports completeness of McKay's two
\(R(4,4;16)\) records. The independent finite check imports the thirteen target
graph6 strings through one hash-pinned JSON file. It does not re-establish the
census's catalogue completeness.

Trust remains in the displayed combinatorial proof, the classical small Ramsey
bounds and Chvátal–Erdős theorems, the clean-room checker, CPython exact integer
and Boolean semantics, SHA-256, and ordinary hardware. No target code,
expected output, columns, core reconstruction, deletion list, flow verdict,
private workspace, solver, floating-point calculation, or omitted generated
artifact is imported into the independent verification. This is not a
proof-assistant formalization.
