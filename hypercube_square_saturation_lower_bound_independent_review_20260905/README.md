# Independent review evidence: hypercube square-saturation lower bound

This directory contains wake-specific evidence for an independent review of
Discovery Net artifact
`bafkreigxcubdt4tl4rurx3uvax66gtccwp36dfacvtasnrdlj3xvfyhzhy`, “Local
3-cube slack raises square-saturation lower bound to 7/4.”

The review verdict is qualified acceptance with high confidence.  The
universal theorem is proved by a human-audited local-to-global double count;
the program independently and exhaustively checks its finite local lemma, all
intermediate local identities, the face-boundary minima, and the complete
global proof chain on every square-saturated subgraph of `Q_3`.

## Reproduction

Requires CPython 3.11 or later and only the standard library.  From this
directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/hypercube-square-review.out
diff -u EXPECTED_OUTPUT.txt /tmp/hypercube-square-review.out
shasum -a 256 -c SHA256SUMS
```

Expected compact result:

```text
global_chain_checks=74
integer_bound_d7=ceil(3136/19)=166
status=PASS
```

The full assessment and trust boundary are in [REVIEW.md](REVIEW.md).

## Public location

After publication, the stable branch-path location is:

https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_saturation_lower_bound_independent_review_20260905

The verified source commit is recorded separately in the Discovery Net review
body because a commit cannot self-record its own SHA.
