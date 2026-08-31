# Cyclic(43) red-to-blue perturbation search

This directory studies the first open question in Section 7 of Ge, Jayasooriya,
Qiu, Sun, and Yuan, *Study of Exoo's Lower Bound for Ramsey number R(5,5)*
(arXiv:2212.12630v3): among colorings obtained from their `Cyclic(43)` coloring
by changing any collection of red edges to blue, what is the minimum possible
number of monochromatic copies of `K5`?

`solve_cyclic43.py` makes one Boolean variable for each of the 473 initially red
edges. For every one of the `C(43,5) = 962598` vertex sets it adds a unit-weight
soft clause for the possible all-blue state; for each of the seed's 43 red
`K5`s it adds a second clause for the all-red state. Each clause is false exactly
when its monochromatic state occurs. Thus the exact weighted-MaxSAT optimum
equals the desired monochromatic-`K5` count.
The returned coloring is then checked independently by direct enumeration.

Run the exact optimization with:

```bash
uv run --with python-sat python solve_cyclic43.py --output certificate.json
```

An independent MaxSAT algorithm and SAT-backend rerun can use:

```bash
uv run --with python-sat python solve_cyclic43.py \
  --algorithm fm --solver m22 --output certificate-fm.json
```

Recount every `K5` in an existing certificate without invoking a SAT solver:

```bash
python solve_cyclic43.py --verify certificate.json
```

Compute exact unrestricted edge-toggle rigidity through radii two and three:

```bash
python local_rigidity.py certificate.json --output local-rigidity-primary.json
python local_rigidity_radius3.py certificate.json \
  --output local-rigidity-radius3-primary.json
```

The same commands with `certificate-fm.json` independently analyze the second,
structurally different optimum. Both optima remain at two monochromatic `K5`s
through Hamming radius three, even when edge changes in either direction are
allowed.

The MaxSAT solver establishes optimality within the stated red-to-blue family.
The direct verifier checks the upper-bound coloring, but is not an independently
checkable proof of the MaxSAT lower bound; that solver trust boundary should be
kept explicit when citing the result. The local-rigidity scripts use exact finite
enumeration and directly recount a minimizing perturbation as an internal check.

Primary sources and data context:

- https://arxiv.org/abs/2212.12630
- https://doi.org/10.1002/jgt.70029
- https://users.cecs.anu.edu.au/~bdm/data/ramsey.html
