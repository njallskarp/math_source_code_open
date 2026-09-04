#!/usr/bin/env python3
"""Exact small-case audit of the cycle-power packing transfer theorem."""

from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha256
from itertools import product


def linear_valid(word: tuple[int, ...], power: int) -> bool:
    last: dict[int, int] = {}
    for position, colour in enumerate(word):
        if colour in last and position - last[colour] <= power * colour:
            return False
        last[colour] = position
    return True


def cyclic_valid(word: tuple[int, ...], power: int) -> bool:
    length = len(word)
    for left in range(length):
        for right in range(left + 1, length):
            if word[left] == word[right]:
                separation = min(right - left, length - (right - left))
                if separation <= power * word[left]:
                    return False
    return True


def transfer_states(power: int, colours: int) -> list[tuple[int, ...]]:
    memory = power * colours
    return [
        word
        for word in product(range(1, colours + 1), repeat=memory)
        if linear_valid(word, power)
    ]


def transfer_successors(
    state: tuple[int, ...], power: int, colours: int
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        state[1:] + (colour,)
        for colour in range(1, colours + 1)
        if colour not in state[-power * colour :]
    )


def closed_walk_count(power: int, colours: int, length: int) -> int:
    states = transfer_states(power, colours)
    successors = {
        state: transfer_successors(state, power, colours) for state in states
    }
    total = 0
    for start in states:
        current = {start: 1}
        for _ in range(length):
            following: dict[tuple[int, ...], int] = defaultdict(int)
            for state, count in current.items():
                for target in successors[state]:
                    following[target] += count
            current = following
        total += current.get(start, 0)
    return total


def direct_cyclic_count(power: int, colours: int, length: int) -> int:
    return sum(
        cyclic_valid(word, power)
        for word in product(range(1, colours + 1), repeat=length)
    )


def cycle_power_edges(length: int, power: int) -> set[tuple[int, int]]:
    return {
        (left, right)
        for left in range(length)
        for right in range(left + 1, length)
        if min(right - left, length - (right - left)) <= power
    }


def graph_distances(length: int, power: int, start: int) -> list[int]:
    edges = cycle_power_edges(length, power)
    adjacency = [[] for _ in range(length)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    distances = [-1] * length
    distances[start] = 0
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for target in adjacency[vertex]:
            if distances[target] < 0:
                distances[target] = distances[vertex] + 1
                queue.append(target)
    return distances


def total_cycle_edges(n: int) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()

    def add(left: int, right: int) -> None:
        edges.add(tuple(sorted((left, right))))

    for i in range(n):
        next_i = (i + 1) % n
        add(2 * i, 2 * next_i)
        add(2 * i + 1, 2 * next_i + 1)
        add(2 * i, 2 * i + 1)
        add(2 * next_i, 2 * i + 1)
    return edges


def main() -> None:
    rows: list[str] = []

    distance_cases = 0
    for length in range(3, 16):
        for power in range(1, length + 1):
            for start in range(length):
                distances = graph_distances(length, power, start)
                for target in range(length):
                    if target != start:
                        cyclic_separation = min(
                            (target - start) % length, (start - target) % length
                        )
                        expected = (cyclic_separation + power - 1) // power
                        assert distances[target] == expected
            distance_cases += 1
    row = f"cycle_power_distance_cases={distance_cases}"
    print(row)
    rows.append(row)

    transfer_cases = 0
    parameter_pairs = ((1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (3, 2))
    for power, colours in parameter_pairs:
        memory = power * colours
        for length in range(memory + 1, memory + 4):
            direct = direct_cyclic_count(power, colours, length)
            transfer = closed_walk_count(power, colours, length)
            assert direct == transfer
            transfer_cases += 1
    row = f"trace_bijection_cases={transfer_cases} parameter_pairs={len(parameter_pairs)}"
    print(row)
    rows.append(row)

    total_cases = 0
    for n in range(3, 13):
        assert total_cycle_edges(n) == cycle_power_edges(2 * n, 2)
        total_cases += 1
    row = f"total_cycle_specialization_cases={total_cases}"
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
