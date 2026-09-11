"""Exact smallest-layer reduction; standard library only."""

from itertools import combinations, product

WORDS3 = tuple(product(range(4), repeat=3))
WORDS4 = tuple(product(range(4), repeat=4))
ALL = (1 << 64) - 1


def distance(x, y):
    return sum(a != b for a, b in zip(x, y, strict=True))


BALLS = tuple(sum(1 << j for j, y in enumerate(WORDS3) if distance(x, y) <= 1) for x in WORDS3)


def bits(mask):
    if not isinstance(mask, int) or not 0 <= mask <= ALL:
        raise ValueError("invalid layer mask")
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def covered(mask):
    result = 0
    for i in bits(mask):
        result |= BALLS[i]
    return result


class CNF:
    def __init__(self):
        self.nvars = 0
        self.clauses = []
        self.gates = []
        self.occupied = {}

    def variable(self):
        self.nvars += 1
        return self.nvars

    def add(self, *literals):
        # Boolean constants are eliminated before DIMACS serialization.
        if any(x is True for x in literals):
            return
        row = list(dict.fromkeys(x for x in literals if x is not False))
        if any(-x in row for x in row):
            return
        self.clauses.append(row)

    @staticmethod
    def negate(literal):
        return not literal if isinstance(literal, bool) else -literal

    def cardinality(self, variables, lower, upper=None):
        """Exact unary recurrence: count[i,j] iff the first i sum to >=j."""
        n = len(variables)
        upper = n if upper is None else upper
        if not 0 <= lower <= upper <= n:
            self.add()
            return
        limit = max(lower, upper + 1 if upper < n else 0)
        if not limit:
            return
        previous = [True] + [False] * limit
        for i, variable in enumerate(variables, 1):
            current = [True] + [False] * limit
            for j in range(1, min(i, limit) + 1):
                out = self.variable()
                a, b = previous[j], previous[j - 1]
                self.gates.append((out, a, b, variable))
                # out <-> a OR (b AND variable).
                self.add(self.negate(a), out)
                self.add(self.negate(b), -variable, out)
                self.add(-out, a, b)
                self.add(-out, a, variable)
                current[j] = out
            previous = current
        self.add(previous[lower])
        if upper < n:
            self.add(self.negate(previous[upper + 1]))

    def dimacs(self):
        return f"p cnf {self.nvars} {len(self.clauses)}\n" + "".join(
            " ".join(map(str, row)) + " 0\n" for row in self.clauses
        )


def build(mask, size=29, minimum=None, break_color_symmetry=True):
    selected = set(bits(mask))
    k = len(selected)
    if any(distance(WORDS3[i], WORDS3[j]) < 2 for i, j in combinations(selected, 2)):
        raise ValueError("input layer is not independent")
    minimum = k if minimum is None else minimum
    holes_mask = ALL ^ covered(mask)
    holes = set(bits(holes_mask))
    optional = sorted(set(range(64)) - selected - holes)
    slack = size - k - len(holes)
    cnf = CNF()
    meta = {
        "slice_size": k,
        "holes": len(holes),
        "optional_positions": len(optional),
        "slack": slack,
    }
    if slack < 0 or slack > len(optional):
        cnf.variable()
        cnf.add(1)
        cnf.add(-1)
        return cnf, {}, meta
    color = {(i, c): cnf.variable() for i in range(64) if i not in selected for c in range(3)}
    occupied = {i: cnf.variable() for i in optional}
    cnf.occupied = occupied
    for i in range(64):
        if i in selected:
            continue
        row = [color[i, c] for c in range(3)]
        for a, b in combinations(row, 2):
            cnf.add(-a, -b)
        if i in holes:
            cnf.add(*row)
        else:
            y = occupied[i]
            cnf.add(-y, *row)
            for a in row:
                cnf.add(-a, y)
        for j in bits(BALLS[i] & ~(1 << i)):
            if j > i and j not in selected:
                for c in range(3):
                    cnf.add(-color[i, c], -color[j, c])
    # At an unoccupied position each other layer must have a neighbor.
    for i in optional:
        for c in range(3):
            cnf.add(
                occupied[i], *(color[j, c] for j in bits(BALLS[i] & ~(1 << i)) if j not in selected)
            )
    cnf.cardinality(list(occupied.values()), slack, slack)
    # The distinguished slice has globally minimum size among all 16 slices.
    for c in range(3):
        cnf.cardinality([color[i, c] for i in range(64) if i not in selected], minimum)
    for axis in range(3):
        for value in range(4):
            already = sum(WORDS3[i][axis] == value for i in selected)
            lower = max(0, minimum - already)
            if lower:
                cnf.cardinality(
                    [
                        color[i, c]
                        for i in range(64)
                        if i not in selected and WORDS3[i][axis] == value
                        for c in range(3)
                    ],
                    lower,
                )
    if break_color_symmetry and holes:
        a = min(holes)
        cnf.add(color[a, 0])
        near = BALLS[a] & ~(1 << a) & holes_mask
        if near:
            cnf.add(color[next(bits(near)), 1])
    return cnf, color, meta


def check_words(words, size):
    words = tuple(tuple(w) for w in words)
    if len(words) != size or len(set(words)) != size or any(w not in WORDS4 for w in words):
        raise ValueError("invalid code size or word")
    if any(distance(x, y) < 2 for x, y in combinations(words, 2)):
        raise ValueError("incompatible selected words")
    histogram = {}
    for x in WORDS4:
        count = sum(distance(x, y) <= 1 for y in words)
        if count == 0:
            raise ValueError("undominated word")
        histogram[count] = histogram.get(count, 0) + 1
    return dict(sorted(histogram.items()))
