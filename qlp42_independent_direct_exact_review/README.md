# Independent direct-exact review of the QLP-42 q=41 weight strata

This directory contains an independently written checker for the committed
QLP-42 q=41 weight-4 and weight-16 exclusions. It intentionally does not read
the producing agent's canonical orbit stream, modular frontier, hashes, or
survivor masks.

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

Build and run:

```sh
c++ -std=c++20 -O3 -Wall -Wextra -pedantic verify_direct_exact.cpp -o verify_direct_exact
./verify_direct_exact --weight 4
./verify_direct_exact --weight 16
```

Trust boundary: the committed coupled-transform reduction, q=41 reflection,
third-order theta equations, the six canonical sum cases, and H/S local-state
independence are imported. The checker independently verifies the finite
enumeration after those reductions. It additionally trusts the C++20
compiler/runtime, operating system, and hardware. It uses no solver,
floating point, randomness, heuristic cutoff, timeout, or producer-generated
certificate.
