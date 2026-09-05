"""Complete column domains for the bounded fixed-core Boolean search.

Discovery only: a returned model requires direct checking; UNKNOWN is not a
mathematical result. Domains are enumerated by exact integer truth tables.
"""
import argparse
from collections import Counter
from hashlib import sha256
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
from threading import Timer
from time import monotonic

from pysat.solvers import Solver

from parent import build, validate_candidate


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
        seed_mask = sum(1 << j for j, a in enumerate(rows) if (a, b) in red)
        print(json.dumps({'column': b, 'free_degree': [low, high],
                          'unary_clauses': len(normalized), 'domain': len(domains[b]),
                          'seed_admissible': seed_mask in domains[b],
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seconds', type=float, default=240)
    parser.add_argument('--domains-only', action='store_true')
    parser.add_argument('--no-mixed', action='store_true')
    parser.add_argument('--no-quotas', action='store_true')
    parser.add_argument('--radius', type=int, help='discovery-only Hamming restriction per seed column')
    parser.add_argument('--full', action='store_true', help='include every global five-set prohibition')
    parser.add_argument('--certificate-work', type=Path, help='write generated CNF and an UNSAT trace here')
    args = parser.parse_args()
    start = monotonic()
    _, red, fixed, variables, clauses, origins = build(False, not args.no_quotas, not args.no_mixed)
    if args.full:
        extra = set()
        for vertices in combinations(range(43), 5):
            pairs = list(combinations(vertices, 2))
            fixed_colors = {fixed[pair] for pair in pairs if pair in fixed}
            if len(fixed_colors) == 2:
                continue
            for color in fixed_colors or (True, False):
                extra.add(tuple(variables[pair] * (-1 if color else 1)
                                for pair in pairs if pair in variables))
        clauses.extend(sorted(extra))
        print(json.dumps({'global_clauses': len(extra)}), flush=True)
    rows, domains = complete_domains(red, fixed, variables, clauses)
    print(json.dumps({'domain_total': sum(map(len, domains.values())),
                      'domain_seconds': monotonic() - start}), flush=True)
    if args.domains_only:
        return
    if args.radius is not None:
        if not 0 <= args.radius <= len(rows):
            raise ValueError('invalid column radius')
        for b, masks in domains.items():
            seed_mask = sum(1 << j for j, a in enumerate(rows) if (a, b) in red)
            domains[b] = [mask for mask in masks if (mask ^ seed_mask).bit_count() <= args.radius]
        print(json.dumps({'radius': args.radius, 'restricted_domains': {b: len(m) for b, m in domains.items()}}), flush=True)
    top = max(abs(lit) for clause in clauses for lit in clause)
    domain_clauses = []
    diagrams = {}
    for b, masks in domains.items():
        key = tuple(masks)
        if key not in diagrams:
            diagrams[key] = decision_diagram(masks, len(rows))
        root, nodes = diagrams[key]
        node_vars = {node: top + i + 1 for i, node in enumerate(nodes)}
        top += len(nodes)

        def node_lit(node, positive=True):
            if node in (0, 1):
                return bool(node) == positive
            return node_vars[node] * (1 if positive else -1)

        def append(clause):
            if any(lit is True for lit in clause):
                return
            domain_clauses.append([lit for lit in clause if lit is not False])

        for node, (j, lo, hi) in nodes.items():
            z, x = node_vars[node], variables[rows[j], b]
            append([-z, -x, node_lit(hi)])
            append([-z, x, node_lit(lo)])
            append([z, -x, node_lit(hi, False)])
            append([z, x, node_lit(lo, False)])
        append([node_lit(root)])
    full = clauses + domain_clauses
    print(json.dumps({'primary': len(variables), 'all_variables': top,
                      'clauses': len(full), 'domain_clauses': len(domain_clauses)}), flush=True)
    if args.certificate_work:
        args.certificate_work.mkdir(parents=True, exist_ok=True)
        with (args.certificate_work / 'formula.cnf').open('w') as stream:
            stream.write(f'p cnf {top} {len(full)}\n')
            for clause in full:
                stream.write(' '.join(map(str, clause)) + ' 0\n')
    with Solver(name='glucose42', bootstrap_with=full, with_proof=bool(args.certificate_work)) as solver:
        solver.set_phases([v if pair in red else -v for pair, v in variables.items()])
        timer = Timer(args.seconds, solver.interrupt)
        timer.start()
        try:
            status = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        print(json.dumps({'status': 'SAT' if status else 'UNSAT' if status is False else 'UNKNOWN',
                          'stats': solver.accum_stats(), 'seconds': monotonic() - start}), flush=True)
        if status is False and args.certificate_work:
            proof = solver.get_proof()
            (args.certificate_work / 'proof.drat').write_text('\n'.join(proof) + '\n')
        if status:
            model = set(solver.get_model())
            if not all(any(lit in model for lit in clause) for clause in full):
                raise ValueError('decoded CNF model')
            found = {pair for pair, color in fixed.items() if color} | {pair for pair, v in variables.items() if v in model}
            validate_candidate(found, red, fixed, not args.no_quotas, not args.no_mixed)
            if args.full:
                for vertices in combinations(range(43), 5):
                    if len({pair in found for pair in combinations(vertices, 2)}) == 1:
                        raise ValueError('global monochromatic five-set')
            print(json.dumps({'changed_edges': [list(e) for e in sorted(red ^ found)],
                              'red_adjacency': [''.join('1' if tuple(sorted((u, v))) in found else '0'
                                                       for v in range(43)) for u in range(43)]}, indent=2), flush=True)


if __name__ == '__main__':
    main()
