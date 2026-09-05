"""Shared discovery-only SAT base for the direct conditional encoding."""
from __future__ import annotations

import base64
from itertools import combinations

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def decode_graph6(encoded):
    data = base64.b64decode(encoded)
    order = data[0] - 63
    bits = [(value - 63) >> bit & 1 for value in data[1:] for bit in range(5, -1, -1)]
    edges = {
        edge
        for edge, flag in zip(((i, j) for j in range(1, order) for i in range(j)), bits)
        if flag
    }
    return order, edges


def build_base(data):
    _, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    red_core -= set(map(tuple, data["red_core_delete_edges"]))
    _, blue_core = decode_graph6(data["blue_core_graph6_base64"])
    partner = 3
    pool = IDPool()
    fixed = {}
    variables = {}
    for a, b in combinations(range(43), 2):
        edge = (a, b)
        if a == 0:
            fixed[edge] = b <= 22
        elif b <= 22:
            fixed[edge] = (a - 1, b - 1) in red_core
        elif a <= 22:
            variables[edge] = pool.id(edge)
        else:
            fixed[edge] = (a - 23, b - 23) not in blue_core

    clauses = []

    def prohibit(conditions):
        clause = set()
        for a, b, color in conditions:
            edge = tuple(sorted((a, b)))
            if edge in fixed:
                if fixed[edge] != color:
                    return
            else:
                literal = -variables[edge] if color else variables[edge]
                if -literal in clause:
                    return
                clause.add(literal)
        clauses.append(sorted(clause))

    for root in (0, partner):
        for color in (True, False):
            possible = [
                vertex
                for vertex in range(43)
                if vertex != root
                and fixed.get(tuple(sorted((root, vertex))), color) == color
            ]
            for size, target_color in ((4, color), (5, not color)):
                for subset in combinations(possible, size):
                    prohibit(
                        [(a, b, target_color) for a, b in combinations(subset, 2)]
                        + [(root, vertex, color) for vertex in subset]
                    )

    for vertex in range(43):
        fixed_red = sum(color for edge, color in fixed.items() if vertex in edge)
        literals = [variable for edge, variable in variables.items() if vertex in edge]
        low, high = (22, 22) if vertex == 0 else ((21, 22) if vertex <= 22 else (20, 21))
        for bound, negate in ((high - fixed_red, False), (len(literals) - (low - fixed_red), True)):
            if 0 <= bound < len(literals):
                clauses.extend(
                    CardEnc.atmost(
                        [-literal for literal in literals] if negate else literals,
                        bound=bound,
                        vpool=pool,
                        encoding=EncType.seqcounter,
                    ).clauses
                )
            elif bound < 0:
                clauses.append([])
    cross = [variable for (a, b), variable in variables.items() if a <= 22 < b]
    clauses.extend(CardEnc.equals(cross, bound=232, vpool=pool, encoding=EncType.totalizer).clauses)
    return partner, fixed, variables, clauses


def red_edges(model, fixed, variables):
    positive = set(model)
    return {edge for edge, color in fixed.items() if color} | {
        edge for edge, variable in variables.items() if variable in positive
    }
