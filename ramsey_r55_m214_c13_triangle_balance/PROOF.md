# All-marking outside-triangle balance in the \(M=214,c=13\) branch

## Hypotheses and notation

Color every edge of \(K_{43}\) red or blue. Let \(G\) be the red graph and let
\(E\) be the thirteen vertices of red degree 20; the other thirty vertices
have red degree 21. Assume that every vertex has six red neighbors in \(E\),
except for one marked pivot \(p\in E\), which has eight. The required red
local-triangle count is 93 at a vertex of \(E\) and 100 elsewhere.

Normalize a red edge \(uv\) between two degree-21 vertices whose common red
neighborhood \(H\) has order 13. In the \(c=13\) branch, \(H\) is the cyclic
graph on \(\mathbb Z/13\mathbb Z\) whose red differences are
\(\{1,5,8,12\}\). In particular, \(H\) has 26 red edges, 52 blue pairs, no
red triangle, and 78 blue triangles.

The remaining 28 vertices form \(W=A\mathbin{\dot\cup}B\mathbin{\dot\cup}O\),
where \(A\) consists of the seven vertices red only to \(u\), \(B\) consists
of the seven vertices red only to \(v\), and the fourteen vertices in \(O\)
are blue to both anchors. For \(x\in W\), put

\[
S_x=N_R(x)\cap H.
\]

Define

\[
\begin{aligned}
k&=|E\cap H|, &
\delta&=\mathbf 1_{\{p\in H\}},\\
X&=\sum_{x\in A\cup B}|S_x|, &
P&=\sum_{x\in W}e_H(S_x),\\
Q&=\sum_{x\in W}e_{\overline H}(H\setminus S_x).
\end{aligned}
\]

Thus \(P\) counts pairs consisting of an outside vertex and a red core edge
contained in its footprint. Similarly, \(Q\) counts pairs consisting of an
outside vertex and a blue core pair missed by its footprint. Write
\(T_R(W)\) and \(T_B(W)\) for the red and blue triangle counts induced by
\(W\).

## Balance theorem

Every coloring satisfying the hypotheses obeys

\[
\boxed{T_R(W)=33+7k+X+P}
\]

and

\[
\boxed{T_B(W)=119-7k+2\delta+Q}.
\]

These are simultaneous identities for every choice of the thirteen marks and
the exceptional pivot; no \(E\)-marking is pinned.

## Red proof

Summing the prescribed red local-triangle counts and dividing by three gives

\[
T_R(K_{43})=\frac{13\cdot93+30\cdot100}{3}=1403.
\]

Each anchor lies in 100 red triangles. Exactly the thirteen triangles \(uvh\),
with \(h\in H\), are counted at both anchors. Hence 187 red triangles meet an
anchor and 1216 do not.

Let

\[
I=\sum_{\substack{xy\in E_R(W)}}|S_x\cap S_y|.
\]

Because \(H\) has no red triangle, the no-anchor red triangles split into
types \(HHW\), \(HWW\), and \(WWW\), giving

\[
P+I+T_R(W)=1216. \tag{1}
\]

Now sum the red local-triangle counts over the thirteen core vertices. The
sum is \(1300-7k\). Counting the same incidences by triangle type gives:

- 13 incidences from the triangles \(uvh\);
- \(2\cdot2\cdot26=104\) incidences from one anchor and one red edge of
  \(H\);
- \(X\) incidences from one anchor, one core vertex, and one vertex of
  \(A\cup B\);
- \(2P\) incidences from type \(HHW\); and
- \(I\) incidences from type \(HWW\).

Consequently,

\[
X+2P+I=1183-7k. \tag{2}
\]

Eliminating \(I\) between (1) and (2) proves the red identity.

## Blue proof

The red graph has

\[
\frac{13\cdot20+30\cdot21}{2}=445
\]

edges. For a vertex \(z\), let \(d=d_R(z)\), let \(e\) be its number of red
neighbors in \(E\), and let \(t_R(z)\) be its red local-triangle count.
Partitioning the 445 red edges relative to \(N_R(z)\) gives

\[
t_B(z)=\binom{42-d}{2}-445-t_R(z)+21d-e. \tag{3}
\]

Equation (3) yields blue local-triangle count 100 at every unmarked vertex,
107 at each of the twelve ordinary marked vertices, and 105 at the pivot.
Thus

\[
T_B(K_{43})=\frac{30\cdot100+12\cdot107+105}{3}=1463.
\]

The blue triangle sets meeting \(u\) and \(v\) are disjoint because \(uv\) is
red, so 1263 blue triangles avoid both anchors. Of these, 78 lie entirely in
\(H\). Put

\[
J=\sum_{\substack{xy\in E_B(W)}}|H\setminus(S_x\cup S_y)|.
\]

The remaining no-anchor blue triangles split by the number of core vertices:

\[
Q+J+T_B(W)=1185. \tag{4}
\]

The sum of blue local-triangle counts over \(H\) is

\[
100(13-k)+107(k-\delta)+105\delta=1300+7k-2\delta.
\]

The 78 blue core triangles contribute 234 core incidences, type \(HHW\)
contributes \(2Q\), and type \(HWW\) contributes \(J\). Therefore

\[
2Q+J=1066+7k-2\delta. \tag{5}
\]

Eliminating \(J\) between (4) and (5) proves the blue identity.

## Ramsey-capacity corollaries

Now also assume that the coloring has no monochromatic \(K_5\).

For a red core edge \(e\), let

\[
W_e=\{x\in W:e\subseteq S_x\}.
\]

The red graph induced by \(W_e\) is triangle-free: a red triangle together
with the two ends of \(e\) would be a red \(K_5\). It also contains no blue
\(K_5\). Since \(R(3,5)=14\), one has \(|W_e|\leq13\). Summing over the 26 red
core edges gives

\[
P\leq338. \tag{6}
\]

For a blue core pair \(q\), let

\[
Y_q=\{x\in W:q\subseteq H\setminus S_x\}.
\]

The blue graph induced by \(Y_q\) is triangle-free, and it contains no red
\(K_5\). Again \(R(3,5)=14\) gives \(|Y_q|\leq13\), whence

\[
Q\leq676. \tag{7}
\]

Two sharper local capacities are also immediate. For each red core edge
\(e\), every pair in \(W_e\cap A\) must be blue, because a red pair together
with \(u\) and the ends of \(e\) would be a red \(K_5\). Therefore

\[
|W_e\cap A|\leq4,
\qquad
|W_e\cap B|\leq4. \tag{8}
\]

Finally, if \(q\) is a blue core triangle, then every pair of vertices whose
footprints miss all of \(q\) must be red; otherwise that pair and \(q\) form a
blue \(K_5\). The no-red-\(K_5\) condition gives

\[
|\{x\in W:q\cap S_x=\varnothing\}|\leq4. \tag{9}
\]

## Compact obstruction

The included certificate is the earlier exact pairwise-interface witness,
re-encoded in 399 bytes. It satisfies the degree sequence, every
\(E\)-incidence, both local-triangle counts at both anchors, and every
monochromatic-\(K_5\) test involving at most two vertices of \(W\). Its data
give

\[
k=\delta=0,\qquad X=96,\qquad P=231,\qquad Q=294.
\]

The theorem consequently requires

\[
(T_R(W),T_B(W))=(360,413).
\]

Direct enumeration instead gives \((318,455)\). Thus the witness has the
exact color discrepancy \((-42,+42)\) and cannot satisfy the complete
deficiency-seven layer. This is an obstruction to that explicit relaxation
witness, not an exclusion of the complete \(c=13\) branch.
