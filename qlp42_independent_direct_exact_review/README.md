# Independent direct-exact audit of the QLP-42 q=41 closure

This directory contains an independently written checker for the committed
QLP-42 q=41 all-weight exclusion. It intentionally
does not read the producing agent's canonical orbit stream, modular frontier,
hashes, or survivor masks.

The checker reconstructs the full binary-axis rotation-orbit space. For each
autocorrelation signature it enumerates the reflected family-A axes and all
third-order-compatible pair signs. It stores the **exact** ten-coordinate
Gaussian PAF vector required from family B, then exhausts every exact-sum
family-B signing and performs direct equality lookup. It subsequently
enumerates all six exact-sum S cases for every surviving H-axis pair and
checks the exact S PAF equations. No `(1+i)`-adic filter or producer
certificate is used.

The optimized unit-word PAF evaluator is checked on a deterministic sample
against a definition-level 21-by-10 Gaussian evaluator. All arithmetic is
signed integer arithmetic.

The initial review covered weights 4, 8, and 16. The integrated closure audit
extends the same direct-exact implementation to the remaining weights 0, 12,
and 20. In particular, weight 12 includes all 293,930 labeled axes and all
14,000 rotation orbits, including its five exceptional size-7 orbits. The
checker restricts weight 0 to canonical cases 2 and 5 and weight 20 to cases 3
and 4, as required by the independently reviewed third-order classification.

Build and run the remaining closure cases:

```sh
c++ -std=c++20 -O3 -Wall -Wextra -pedantic verify_direct_exact.cpp -o verify_direct_exact
./verify_direct_exact --weight 0
./verify_direct_exact --weight 12
./verify_direct_exact --weight 20
```

The previously completed commands for weights 4, 8, and 16 use the same
executable. `verification_output.txt` records those runs;
`verification_output_integrated.txt` records the new weights. The six rows
together cover exactly 523,776 labeled axes, 24,946 rotation orbits, 219
terminal H-side B orbits, and 3,104 admissible H/S case tests. All terminal
tests have zero survivors.

The producer contribution and its immutable source print 524,776 as the
all-weight labeled-axis aggregate. The correct sum is 523,776. This is an
ancillary summary typo: both implementations generate and check the full
24,946-key orbit dictionary, and no search bound depends on the bad total.

`INTEGRATED_CLOSURE_AUDIT.md` separates this independently reproduced q=41
finite result from the inspected and inherited evidence for the q=1 branch.
Its overall verdict is qualified because the q=1 closure is not yet backed by
one end-to-end independent reproduction or a complete dependency graph.

Trust boundary: the committed coupled-transform reduction, q=41 reflection,
third-order theta equations, the six canonical sum cases, and H/S local-state
independence are imported. The checker independently verifies the finite
enumeration after those reductions. It additionally trusts the C++20
compiler/runtime, operating system, and hardware. It uses no solver,
floating point, randomness, heuristic cutoff, timeout, or producer-generated
certificate.
