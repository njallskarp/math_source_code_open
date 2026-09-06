"""Discovery-only complete columns and reduced decision diagrams.

The final proof derives every column-root assertion from the audited base.
Correctness of this discovery helper is therefore not a theorem premise.
"""
from hashlib import sha256
from functools import lru_cache
from itertools import combinations
import json


def truth_tables(n):
    byte_count = (1 << n) // 8
    tables = []
    for j in range(n):
        if j < 3:
            pattern = bytes((0xAA, 0xCC, 0xF0)[j:j+1])
        else:
            block = 1 << (j - 3)
            pattern = bytes(block) + bytes([255]) * block
        tables.append(int.from_bytes(pattern * (byte_count // len(pattern)), 'little'))
    return tables


def complete_domains(red, fixed, variables, clauses):
    rows = [a for a in range(1, 23) if a not in (3, 9)]
    cols = range(23, 43)
    inverse = {v: p for p, v in variables.items()}
    n = len(rows)
    all_bits = (1 << (1 << n)) - 1
    tables = truth_tables(n)
    degree_tables = {}
    for weight in range(n + 1):
        buf = bytearray((1 << n) // 8)
        for positions in combinations(range(n), weight):
            mask = sum(1 << j for j in positions)
            buf[mask >> 3] |= 1 << (mask & 7)
        degree_tables[weight] = int.from_bytes(buf, 'little')
    unary = {b: set() for b in cols}
    for clause in clauses:
        if clause and all(abs(lit) in inverse for lit in clause):
            endpoints = {inverse[abs(lit)][1] for lit in clause}
            if len(endpoints) == 1:
                b = next(iter(endpoints))
                index = {variables[a, b]: j + 1 for j, a in enumerate(rows)}
                unary[b].add(tuple(sorted(index[abs(lit)] * (1 if lit > 0 else -1)
                                         for lit in clause)))
    domains, cache = {}, {}
    for b in cols:
        known = sum(c for pair, c in fixed.items() if b in pair)
        low, high = 20 - known, 21 - known
        normalized = tuple(sorted(unary[b]))
        key = (normalized, low, high)
        if key not in cache:
            surviving = degree_tables[low] | degree_tables[high]
            for clause in normalized:
                truth = 0
                for lit in clause:
                    truth |= tables[abs(lit) - 1] if lit > 0 else all_bits ^ tables[-lit - 1]
                surviving &= truth
            raw = surviving.to_bytes((1 << n) // 8, 'little')
            models = [8 * i + j for i, byte in enumerate(raw) if byte
                      for j in range(8) if byte & (1 << j)]
            # A literal-by-literal check is independent of truth-table arithmetic.
            for mask in models:
                if not low <= mask.bit_count() <= high:
                    raise ValueError('column degree')
                if not all(any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0)
                               for lit in clause) for clause in normalized):
                    raise ValueError('column clause')
            cache[key] = models
        domains[b] = cache[key]
        print(json.dumps({'column': b, 'free_degree': [low, high],
                          'unary_clauses': len(normalized), 'domain': len(domains[b]),
                          'sha256': sha256(json.dumps(domains[b], separators=(',', ':')).encode()).hexdigest()}), flush=True)
    return rows, domains


def decision_diagram(masks, n):
    """Reduced ordered BDD, testing the highest remaining bit first."""
    buf = bytearray((1 << n) // 8)
    for mask in masks:
        buf[mask >> 3] |= 1 << (mask & 7)
    nodes = {}
    unique = {}

    @lru_cache(None)
    def visit(level, bits):
        if bits == 0:
            return 0
        if bits == (1 << (1 << level)) - 1:
            return 1
        half = 1 << (level - 1)
        lo = visit(level - 1, bits & ((1 << half) - 1))
        hi = visit(level - 1, bits >> half)
        if lo == hi:
            return lo
        key = (level - 1, lo, hi)
        if key not in unique:
            unique[key] = len(unique) + 2
            nodes[unique[key]] = key
        return unique[key]

    root = visit(n, int.from_bytes(buf, 'little'))
    return root, nodes
