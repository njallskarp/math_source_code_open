# Independent all-order branched-broom audit

This directory independently checks the finite component and exact arithmetic
of Discovery Net contribution
bafkreignyano56e7pvwihgprbljwwnsv2z4lcwc7f3ryvqfjcvhsh5vy5y.

The checker constructs every branched-broom witness from its edges and
computes its leaf potentials from the recursive directed-deficit definition.
For symmetric double brooms it propagates that same directed-deficit
recurrence along the path, with direct full-graph cross-checks on boundary
and sampled parameters. It does not call or import the producer's programs
and does not use their closed-form potentials, core-distance evaluator,
weak-composition implementation, or canonical record encoding.

Run with CPython 3.11 or later:

    PYTHONDONTWRITEBYTECODE=1 python3 check_all_orders.py

The script checks all 554 orders from 23 through 576, every symmetric
double-broom parameter at each order, the unique winning leaf class in each
declared branched-broom witness, and the exact rational inequalities used at
the start of the uniform infinite tail.

The universal sibling-leaf classification is an imported mathematical
theorem. This checker independently validates its application to the
constructed trees but does not re-prove the pebbling transfer theorem.
