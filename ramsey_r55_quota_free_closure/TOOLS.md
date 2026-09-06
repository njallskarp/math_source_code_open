# Toolchain and bounded evidence

- CPython 3.12.12; `python-sat==1.9.dev15`, using Glucose 4.2.1.
- Solver-free checks also passed under optimized Python.
- DRAT-trim source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Existing pinned checker binary SHA-256:
  `2f8f8baa88cb30a5c857a6d1f03076c72c9d470a33f989cf5cbbbf8a64d3d691`.
- Checker build: Apple clang 17.0.0, `arm64-apple-darwin25.2.0`, with
  `gcc drat-trim.c -std=c99 -O2 -o drat-trim`. This pass reused that previously
  built checker after checking its binary hash; it did not claim a new build.

Build the pinned checker in a separate directory:

```sh
git clone https://github.com/marijnheule/drat-trim.git /tmp/new-r55-checker
git -C /tmp/new-r55-checker checkout --detach 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/new-r55-checker drat-trim
```

Fresh successful end-to-end regeneration took 144.06 seconds on the production
host. The twenty local solves and replays took 100.06 seconds of that run;
concurrent unrelated verification work affected the observed timing. No peak
resident-memory measurement was taken. Timings are observations, not guarantees.
The commands fail if any bounded solve or replay remains unresolved.

All 43 generated formula/proof files were byte-identical between the discovery
work directory and fresh regeneration. The 21 proof files total 44,690,094
bytes; the largest is 7,257,777 bytes. None is included in the public source.
The compact complete manifest `verification.json` has SHA-256
`bca9a8debd3198d4b20b4654136dd29424a7a93eb4b46e843e0a7295a69e9d15`.

The successful evidence consists only of RUP-only replays. No general RAT
verdict, flattened-trace timeout, or direct-solver timeout is used as proof.
The gate and local-interface audits justify composition of the 21 refutations.
