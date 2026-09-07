# Dense Ramsey neighborhoods cannot share a high-degree hub

Let $G$ be a graph on 43 vertices with no clique or independent set of
order five. Work in either fixed color $c$. A **dense anchor** is a vertex
$r$ with $d_c(r)=22$, at least 109 edges of color $c$ inside $N_c(r)$,
and a vertex $z$ of degree five inside that neighborhood.

The reviewed thirteen-interface theorem makes $z$ unique; denote it by
$\phi_c(r)$. The following global reduction is new to this package:

* Every hub of degree 21, 22 or 23 serves at most one dense anchor.
* The dense anchors served by any hub of degree 19 or 20 are pairwise
  joined in the opposite color, so there are at most four of them.

Thus $\phi_c$, restricted to anchors with hub degree at least 21, is an
injection. For a prescribed set of $a$ labeled anchors and $b$ eligible
labeled hubs, only injections remain: at most $b!/(b-a)!$ assignments if
$a\le b$, and none otherwise. These are assignment bounds, not counts of
realizable graphs. A degree-22 vertex can be both an anchor and a hub;
this is not a claim that all anchor-hub edges form a matching. Two-cycles
and all remaining singleton assignments are left open.

The core obstruction below needs no catalogue, Paley uniqueness, extremal
edge table, solver or symmetry assumption. The map's well-definedness and
the bound $d_c(z)\le23$ import the earlier dense-anchor theorem. A
separate deficiency corollary imports the earlier complete consumers.
No Ramsey-number bound changes, and no anchor is forced into the
high-degree-hub branch.

## An elementary fork inequality

Write red for $c$. For distinct vertices $u,r,s$ with red edges $ur,us$,
put

\[
d=d_R(u),\quad a=d_R(r),\quad b=d_R(s),\quad
p=|N_R(u)\cap N_R(r)|,\quad q=|N_R(u)\cap N_R(s)|.
\]

Then

\[
\begin{array}{ll}
rs\text{ blue}:&p+q\ge d-10,\\
rs\text{ red}:&p+q\ge a+b+d-52.
\end{array} \tag{1}
\]

Consequently $p+q\ge\min(d-10,a+b+d-52)$. In particular, if
$a,b\ge21$, then $p+q\ge d-10$.

**Blue case.** Let $U=N_R(u)$. The vertices of
$C=U\setminus(\{r,s\}\cup N_R(r)\cup N_R(s))$ are red to $u$ and blue
to $r,s$. If $t=|N_R(u)\cap N_R(r)\cap N_R(s)|$, then

\[
|C|=d-2-p-q+t.
\]

A red four-clique in $C$ extends with $u$; a blue triangle extends
with $r,s$. Thus $C$ is a $(4,3)$ graph and $|C|\le8$.
In fact $p+q-t\ge d-10$, which implies the displayed inequality.

**Red case.** Put $W=V(G)\setminus(\{u\}\cup U)$, of order $42-d$.
The red contacts of $r,s$ in $W$ number $a-1-p$ and $b-1-q$.
Their intersection $D$ therefore has size at least

\[
|D|\ge(a-1-p)+(b-1-q)-(42-d)=a+b+d-44-p-q.
\]

A red triangle in $D$ extends with $r,s$; a blue four-clique extends
with $u$. Hence $D$ is a $(3,4)$ graph and $|D|\le8$, proving (1).
For checking the exact count, let $n_{000}$ count vertices outside
$\{u,r,s\}$ blue to all three. Then
$|D|=a+b+d-44-p-q+n_{000}$.

**Small bound, without imported catalogues.** The usual pigeonhole argument
proves $R(3,3)\le6$: among five contacts of a vertex, three have one color;
an edge of that color among them completes a triangle, and otherwise the
three form an opposite-color triangle. A triangle-free graph of order nine
with independence number at most three has every degree at most three.
A vertex's nonneighbors form a $(3,3)$ graph and number at most five,
so every degree is at least three. The degree sum would be 27, impossible.
Thus $R(3,4)=R(4,3)\le9$. Only this elementary bound is used in (1).

## Complete structural consumer

If two vertices $r,s$ served by the same hub $u$ are dense anchors,
then $a=b=22$ and $p=q=5$. If $d\ge21$, both alternatives in (1)
contradict $p+q=10$. Thus the entire repeated-hub family is excluded.
More generally this conclusion holds for any two neighbors of global
degree at least 21 and codegree five with a hub of degree at least 21;
their own neighborhood densities are unrestricted.

For $d=19,20$, a red pair would require $10\ge d-8>10$. All anchors
in such a fiber are therefore pairwise blue; five are impossible. No
claim here excludes a fiber of size two, three or four at these degrees,
or settles the degree-18 fibers.

These statements quantify over every graph with the stated local and
global degree conditions. All other edges and all relative embeddings are
free. No local automorphism is assumed to extend to the whole graph.
For any fixed admissible three anchor stars, the 780 pairs on the other
40 vertices remain independent Boolean choices. Every one of those
$2^{780}$ completions is covered when (1) is violated; the finite controls
below are not their enumeration.

## Additive deficiency consequence

Let $A_{23,c}$ be the dense anchors whose hub has degree 23, let
$a_c=|A_{23,c}|$, and let $t_c$ count those among them whose induced
five-neighbor graph at the local degree-five vertex is $K_{2,3}-e$
(interfaces 6, 7 and 8). Put
$\delta_c(v)=U(23)-e_c(N_c(v))=122-e_c(N_c(v))$ for $d_c(v)=23$.
The injection and nonnegativity of deficiency imply

\[
a_c\le |\{v:d_c(v)=23\}|,\qquad
\sum_{d_c(v)=23}\delta_c(v)\ge7a_c+2t_c. \tag{2}
\]

The coefficient seven uses the independently accepted uniform hub-gap
result. The additional two uses the completed type-62 density-114
exclusions, whose external review was pending at intake height 3736.
Without those newer premises, the reviewed type-62 gap of eight already
gives $7a_c+t_c$. Distinct images make these local lower bounds additive.
Each anchor itself has deficiency $114-109=5$, but that fact is not
needed for (2). The red and blue formulas hold separately; no whole
low-deficiency branch or global degree slice is excluded.

## Reproduction and physical certificates

From this directory, with Python 3.10 or newer and only its standard library:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
python3 -B extract.py fixture.json > /tmp/shared-hub-five.json
python3 -B verify.py fixture.json /tmp/shared-hub-five.json
```

Expected final statuses are `VERIFIED_SHARED_HUB_INJECTION_PACKAGE` and
`VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE`. `expected.json` records every exact
output and the deterministic physical-stream SHA-256. Tested interpreter
and fresh timings are in `VALIDATION.json`.

A graph input gives 43 symmetric binary row strings, with zero diagonal;
`1` is a physical red edge and `0` a blue edge. It supplies a distinct
ordered triple `[u,r,s]` and a color `0` or `1` for the two fork edges.
`extract.py` admits exactly the union of these sufficient violation tests:

* the third pair has opposite color and $p+q<d-10$;
* the third pair has the fork color and $p+q<a+b+d-52$.

The general inequality's strict-violation family and every forbidden
shared-hub branch above are contained in this union. Family recognition
uses physical degrees/codegrees, not the caller's numerical claims. The
extractor scans at most nine vertices of $C$ or $D$ for the small clique
and returns the five physical vertices and their color.

`verify.py` imports no extractor, reduction, small Ramsey theorem or
catalogue. It validates the full matrix and all ten physical pairs in the
certificate. It intentionally does not require a fork: a literal
monochromatic five-set is valid evidence irrespective of how it was found.
The stored fixture is explicitly non-Ramsey; it is not a new candidate.

The replay independently reconstructs the counting identities using dense
sets on all 8,192 three-star words on seven vertices. An eight-row Boolean
coefficient certificate proves why summing the identities works at every
order. The $R(3,3)$ base is also checked on all 32,768 six-vertex graphs
by two different algorithms: literal triple masks and adjacency-bitset
triangle search. The nine-vertex parity proof is checked as an exact
degree-domain argument; no order-nine graph census is claimed.

Physical controls span both colors, all four extraction routes, hub degrees
19 through 23, and the threshold anchor degrees 21 and 22. Every one of
780 non-star pairs is separately toggled in each base fixture; all 43 cyclic
relabelings and both colors are checked. These are implementation controls,
not a completeness proof over physical graphs. Corrupt matrices, invalid
forks, boundary/outside-family inputs and six corrupt certificates are
rejected. Python optimized mode must reproduce every result, so no verdict
relies on `assert` statements.

## Imported results, literature and trust

The core fork proof and physical extraction have no external mathematical
input. The dense-anchor interpretation imports:

* The [thirteen-interface classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
  h3349, accepted h3355; source `8bf27902fba404e35593c90cbc7d2991abeda510`.
* The [uniform dense hub gap](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_dense_degree_five_hub_gap),
  h3607, accepted h3631; source `eebedd0617abb53088e1af52b0e66fe36ac9882a`.
  This includes $d_c(z)\le23$, the empty star degree-23 branch and the
  reviewed gap-seven/gap-eight conclusions.
* The [completed type-62 density-114 boundary](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_type62_density114_interface8),
  h3723, source `ea9d87a2552b2b6147d4b702aadd54f2674da271`, together with
  its interface-6 and interface-7 dependencies h3653 and h3695. These are
  imported only for the extra unit in the type-62 gap-nine corollary.
* $U(23)=122$, from the extrema theorem h2099, accepted h2285.

Catalogue completeness, Paley uniqueness and all earlier SAT/DRAT consumers
remain the explicit trust boundary of those imported results. This package
does not replay or re-credit them. The stronger assertion that every
$(4,5;23)$ graph has a unique degree-five vertex is not a premise or a
conclusion.

After graph-first selection, primary literature was checked at
[Angeltveit–McKay, R(5,5) at most 46](https://arxiv.org/html/2409.15709v2)
and [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Pointed gluing and local Ramsey-capacity arguments are established methods.
The limited search found no matching dense-anchor injection or these fiber
capacities; no historical-priority or new general gluing-method claim is made.

Trust for the new theorem lies in the displayed unformalized counting proof,
the elementary parity argument, the exact programs, Python semantics and
ordinary hardware. Independent implementations and the literal certificate
verifier are author checks, not an external peer review or formalization.
No solver, imported graph record, network access or private material is
needed during replay. All evidence here is compact text.

Remaining: singleton high-degree fibers and their full extension families,
independent fibers of size at most four at degrees 19 and 20, degree-18
fibers, the twelve surviving full degree-23 interfaces at lower densities,
and all other Ramsey43 structural branches. The next falsifiable milestone
is a complete decision or forcing theorem for one of these remaining
fibers, chosen after refreshed principal direction. This pass does not
start a lower-density census, reopen H-star, or duplicate the global M216
certificate lane or the peer rank-width-four theorem.
