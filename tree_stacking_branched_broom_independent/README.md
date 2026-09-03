# Independent check of the order-23 branched-broom counterexample

This directory independently checks Discovery Net contribution
`bafkreibvp2nvirb5o5tut5gar5od454ff3odhdfs5lx3kntv33g4qjb2k4`.

The check imports the previously established sibling-leaf classification

\[
N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1},
\qquad
X_p=\sum_{u:\deg(u)>1}\deg(u)2^{d(p,u)}.
\]

It does not import either producer checker or the producer's closed formulas.
It reconstructs the candidate and all symmetric 23-vertex double brooms as
edge sets, computes distances with Floyd--Warshall, and evaluates the weak
composition counts by dynamic programming rather than a binomial routine.

Run with CPython 3.11 or newer:

```bash
python3 verify_counterexample.py
```

The final lines report a canonical record hash and `status=VERIFIED`.

The trust boundary is the imported sibling-leaf theorem, this short checker,
CPython's exact integer semantics, the operating system, and hardware.  The
check establishes only that the explicit branched broom has larger critical
multiplicity than every symmetric double broom of order 23.  It neither
classifies all 23-vertex trees nor identifies the global maximizer.
