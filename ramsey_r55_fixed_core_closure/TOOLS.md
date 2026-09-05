# Checked toolchain

- CPython 3.12.12.
- `python-sat==1.9.dev15`, Glucose 4.2.1.
- DRAT-trim source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Apple clang 17.0.0, target `arm64-apple-darwin25.2.0`; build command
  `gcc drat-trim.c -std=c99 -O2 -o drat-trim` from the upstream Makefile.
- Checked DRAT-trim binary SHA-256:
  `2f8f8baa88cb30a5c857a6d1f03076c72c9d470a33f989cf5cbbbf8a64d3d691`.

A fresh isolated clone at that exact source commit rebuilt the same binary;
its additional RUP-only replay of the final formula and trimmed trace passed.
Binary hashes may differ on other toolchains. A matching binary hash is not a
substitute for replay, and a different build must still pass every check.

Build outside the contribution directory:

```sh
git clone https://github.com/marijnheule/drat-trim.git /tmp/new-r55-checker
git -C /tmp/new-r55-checker checkout --detach 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/new-r55-checker drat-trim
```

The solver-free auditor and controls use only the Python standard library.
Discovery code and its optional diagnostics are retained only to regenerate
the successful certificate; their intermediate domain counts, timeouts, or
restricted-search verdicts are not separate mathematical results.
