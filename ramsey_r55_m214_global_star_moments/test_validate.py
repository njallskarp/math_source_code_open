#!/usr/bin/env python3
"""Definition-level controls for atom inversion and degree multiplication."""

import itertools as it
import tempfile
from fractions import Fraction as F
from pathlib import Path

from validate import MOMENT_HEADER, atom_values, read_moments, require


def compositions(total, count):
    if count == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, count-1):
                yield (first,) + rest


def reject(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("malformed input accepted")


def main():
    distributions = 0
    incident = ((0, 1), (0, 2), (1, 2))
    for masses in compositions(4, 8):
        x = tuple(sum(p for mask, p in enumerate(masses) if mask >> i & 1) for i in range(3))
        m = tuple(sum(p for mask, p in enumerate(masses)
                      if all(not (mask >> i & 1) for i in bits)) for bits in incident)
        require(atom_values(x, m, masses[7], 4) == masses, "definition-level atom inversion")
        distributions += 1
    graphs = stars = triangle_projections = 0
    for n in range(1, 6):
        pairs = list(it.combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adjacency = [[0]*n for _ in range(n)]
            for i, (a, b) in enumerate(pairs):
                adjacency[a][b] = adjacency[b][a] = mask >> i & 1
            degrees = [sum(row) for row in adjacency]
            for h in range(n):
                for a in range(n):
                    if h == a:
                        continue
                    red = sum(adjacency[h][a]*adjacency[h][b] for b in range(n) if b not in (a, h))
                    blue = sum((1-adjacency[h][a])*(1-adjacency[h][b])
                               for b in range(n) if b not in (a, h))
                    require(red == (degrees[h]-1)*adjacency[h][a], "red star identity")
                    require(blue == (n-2-degrees[h])*(1-adjacency[h][a]), "blue star identity")
                    stars += 1
            for a, b, h in it.combinations(range(n), 3):
                aa, bb, cc = adjacency[h][a], adjacency[h][b], adjacency[a][b]
                m, z = (1-aa)*(1-bb), aa*bb*cc
                wedge = m+aa+bb-1
                require(wedge-z >= 0 and z-wedge-cc+1 >= 0, "projected triangle constraints")
                triangle_projections += 1
            graphs += 1
    require(F(0)-F(5, 26)-F(5, 6)+1 == -F(1, 39), "old-family strict separator")
    require(7*F(3, 14) == F(3, 2) and 78*F(10, 39) == 20, "sharp parameter interval")
    # The first physical triple suffices to reject these malformed streams.
    broken = ["wrong header\n", MOMENT_HEADER,
              MOMENT_HEADER+"0\t1\t3\t0\t0\t0\n",
              MOMENT_HEADER+"0\t1\t2\t0\t0\n",
              MOMENT_HEADER+"0\t1\t2\t-1\t0\t0\n",
              MOMENT_HEADER+"0\t1\t2\t2\t0\t0\n"]
    with tempfile.TemporaryDirectory(prefix="m214-star-controls-") as directory:
        path = Path(directory) / "moments.tsv"
        for text in broken:
            path.write_text(text)
            reject(lambda: read_moments(path))
    print(f"PASS atom_distributions={distributions} graphs={graphs} star_identities={stars} "
          f"triangle_projections={triangle_projections} malformed_streams={len(broken)}")


if __name__ == "__main__":
    main()
