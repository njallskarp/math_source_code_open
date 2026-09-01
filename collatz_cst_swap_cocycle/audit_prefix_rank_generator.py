"""Audit a suffix-DFS-free parameterization of wrapped CST swap edges.

For a coefficient-safe prefix ``p`` let ``rho`` and ``eta`` be its least
residue and endpoint, ``F=2^|p|``, and ``P=3^#1(p)``.  A target word of the
form ``p10s`` has a unique local lift

    x = chi + 4*t,

where ``chi`` is the unique residue in ``[0,4)`` making
``(3*P*chi + 3*eta + 1)/4`` integral.  Once ``p`` and ``t`` are fixed, the
entire suffix is the ordinary parity trajectory of that integer.  This file
checks that this forward generator is exactly equal to an independent
parity-word DFS on a complete finite frontier, then uses it for a targeted
small-rank search beyond that frontier.

All arithmetic is exact and dependency-free.  Words are stored
chronologically, with their first bit in the least significant position.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from dataclasses import dataclass

from audit_swap_cocycle import cylinder_from_bits, first_crossing_cylinders


@dataclass(frozen=True)
class PrefixState:
    """Independent parity-cylinder implementation for the generator."""

    length: int = 0
    odd_count: int = 0
    bits: int = 0
    residue: int = 0
    endpoint: int = 0
    pow2: int = 1
    pow3: int = 1

    def extend(self, bit: int) -> PrefixState:
        if bit not in (0, 1):
            raise ValueError("bit must be zero or one")
        lift = (self.endpoint & 1) if bit == 0 else ((1 - self.endpoint) & 1)
        lifted = self.endpoint + self.pow3 * lift
        if (lifted & 1) != bit:
            raise AssertionError("independent cylinder lift has wrong parity")
        endpoint = lifted // 2 if bit == 0 else (3 * lifted + 1) // 2
        return PrefixState(
            length=self.length + 1,
            odd_count=self.odd_count + bit,
            bits=self.bits | (bit << self.length),
            residue=self.residue + self.pow2 * lift,
            endpoint=endpoint,
            pow2=2 * self.pow2,
            pow3=self.pow3 if bit == 0 else 3 * self.pow3,
        )


@dataclass(frozen=True)
class GeneratedEdge:
    total_length: int
    bits: int
    position: int
    lift: int
    rank: int
    suffix_length: int
    margin: int
    barrier_rank: int

    @property
    def key(self) -> tuple[int, int, int, int, int]:
        return (
            self.total_length,
            self.bits,
            self.position,
            self.lift,
            self.suffix_length,
        )


def chronological_word(bits: int, length: int) -> str:
    return "".join(str((bits >> j) & 1) for j in range(length))


def safe_prefixes(max_length: int):
    """Yield every all-prefix coefficient-safe state through a depth."""
    stack = [PrefixState()]
    while stack:
        state = stack.pop()
        yield state
        if state.length == max_length:
            continue
        for bit in (1, 0):
            child = state.extend(bit)
            if child.pow3 >= child.pow2:
                stack.append(child)


def base_class(prefix: PrefixState) -> tuple[int, int]:
    """Return ``(chi,y0)`` for the unique integral ``p10`` lift class."""
    prefix_power = 3 * prefix.pow3
    constant = 3 * prefix.endpoint + 1
    chi = (-constant * pow(prefix_power, -1, 4)) % 4
    y0, remainder = divmod(prefix_power * chi + constant, 4)
    if remainder:
        raise AssertionError("base-class construction was not integral")
    return chi, y0


def generate_edge(
    prefix: PrefixState, rank: int, suffix_cap: int
) -> GeneratedEdge | None:
    """Generate the first relative coefficient crossing for ``(p,t)``.

    ``None`` means that the crossing was not reached within ``suffix_cap`` or
    that the resulting target is not a canonical wrapped edge.
    """
    if rank < 0:
        raise ValueError("rank must be nonnegative")
    if prefix.pow3 < 2 * prefix.pow2:
        return None  # The reverse source prefix p0 would already contract.

    chi, y0 = base_class(prefix)
    lift = chi + 4 * rank
    value = y0 + 3 * prefix.pow3 * rank
    relative_power3 = 3 * prefix.pow3
    relative_power2 = 4 * prefix.pow2
    suffix_bits = 0

    for suffix_length in range(1, suffix_cap + 1):
        bit = value & 1
        suffix_bits |= bit << (suffix_length - 1)
        if bit:
            value = (3 * value + 1) // 2
            relative_power3 *= 3
        else:
            value //= 2
        relative_power2 *= 2
        if relative_power3 >= relative_power2:
            continue

        local_modulus = 1 << (suffix_length + 2)
        if not (0 <= lift < local_modulus):
            return None
        inverse = pow(3 * prefix.pow3, -1, local_modulus)
        if lift >= inverse:
            return None

        total_length = prefix.length + suffix_length + 2
        bits = prefix.bits | (1 << prefix.length) | (suffix_bits << (prefix.length + 2))
        residue = prefix.residue + prefix.pow2 * lift
        margin = residue - value
        gap = (1 << total_length) - relative_power3
        split_surplus = local_modulus * margin - gap * lift
        base_barrier = gap * chi + split_surplus
        barrier_rank = 0 if base_barrier > 0 else (-base_barrier) // (4 * gap) + 1
        if (margin > 0) != (rank >= barrier_rank):
            raise AssertionError("ranked split-barrier equivalence failed")

        # Reconstruct the generated word independently and check all fields.
        target = PrefixState()
        for position in range(total_length):
            target = target.extend((bits >> position) & 1)
        if target.residue != residue or target.endpoint != value:
            raise AssertionError("generated word did not reconstruct")
        if target.pow3 != relative_power3 or target.pow2 != 1 << total_length:
            raise AssertionError("generated coefficient did not reconstruct")
        return GeneratedEdge(
            total_length=total_length,
            bits=bits,
            position=prefix.length,
            lift=lift,
            rank=rank,
            suffix_length=suffix_length,
            margin=margin,
            barrier_rank=barrier_rank,
        )
    return None


def dfs_wrapped_edges(max_length: int) -> set[tuple[int, int, int, int, int]]:
    """Independent reference set obtained by full parity-word DFS."""
    records: set[tuple[int, int, int, int, int]] = set()
    for length, states in first_crossing_cylinders(max_length).items():
        for bits, target in states.items():
            for position in range(length - 1):
                if ((bits >> position) & 3) != 1:  # target is p10s
                    continue
                prefix = cylinder_from_bits(bits, position)
                if prefix.pow3 < 2 * prefix.pow2:
                    continue
                lift, remainder = divmod(target.residue - prefix.residue, 1 << position)
                if remainder or lift < 0:
                    raise AssertionError("DFS target did not lift its prefix")
                local_modulus = 1 << (length - position)
                inverse = pow(3 * prefix.pow3, -1, local_modulus)
                if lift < inverse:
                    records.add((length, bits, position, lift, length - position - 2))
    return records


def generated_complete_edges(
    max_length: int,
) -> set[tuple[int, int, int, int, int]]:
    """Generate every possible wrapped edge through ``max_length``.

    A target with suffix length ``h`` has ``0<=t<2^h``.  Hence, for a prefix
    of length ``j`` and total length at most ``K``, it is enough to enumerate
    ``0<=t<2^(K-j-2)``; no suffix word is enumerated.
    """
    records: set[tuple[int, int, int, int, int]] = set()
    for prefix in safe_prefixes(max_length - 3):
        if prefix.pow3 < 2 * prefix.pow2:
            continue
        suffix_cap = max_length - prefix.length - 2
        for rank in range(1 << suffix_cap):
            edge = generate_edge(prefix, rank, suffix_cap)
            if edge is not None:
                records.add(edge.key)
    return records


def digest_records(records: set[tuple[int, int, int, int, int]]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records):
        digest.update((",".join(map(str, record)) + "\n").encode("ascii"))
    return digest.hexdigest()


def complete_audit(max_length: int) -> dict[str, int | str]:
    reference = dfs_wrapped_edges(max_length)
    generated = generated_complete_edges(max_length)
    missing = reference - generated
    extra = generated - reference
    if missing or extra:
        raise AssertionError(
            f"generator/DFS mismatch: missing={len(missing)}, extra={len(extra)}"
        )
    return {
        "complete_depth": max_length,
        "dfs_wrapped_edges": len(reference),
        "generated_wrapped_edges": len(generated),
        "missing_edges": len(missing),
        "extra_edges": len(extra),
        "edge_sha256": digest_records(reference),
    }


def targeted_rank_search(
    prefix_depth: int, rank_cap: int, suffix_cap: int
) -> dict[str, int | str | dict[int, int]]:
    """Search all safe prefixes and small ranks without enumerating suffixes."""
    prefixes = 0
    eligible_prefixes = 0
    trajectories = 0
    crossings = 0
    wrapped_edges = 0
    descent_failures = 0
    capped_trajectories = 0
    maximum_length = 0
    maximum_barrier_rank = 0
    minimum_margin: int | None = None
    minimum_example = "none"
    barrier_histogram: Counter[int] = Counter()
    digest = hashlib.sha256()

    for prefix in safe_prefixes(prefix_depth):
        prefixes += 1
        if prefix.pow3 < 2 * prefix.pow2:
            continue
        eligible_prefixes += 1
        for rank in range(rank_cap + 1):
            trajectories += 1
            edge = generate_edge(prefix, rank, suffix_cap)
            if edge is None:
                # Distinguish a true cap hit from a finite nonwrapped result by
                # replaying only the coefficient crossing, without accepting.
                _, y0 = base_class(prefix)
                value = y0 + 3 * prefix.pow3 * rank
                left = 3 * prefix.pow3
                right = 4 * prefix.pow2
                crossed = False
                for _ in range(suffix_cap):
                    if value & 1:
                        value = (3 * value + 1) // 2
                        left *= 3
                    else:
                        value //= 2
                    right *= 2
                    if left < right:
                        crossed = True
                        break
                if not crossed:
                    capped_trajectories += 1
                else:
                    crossings += 1
                continue
            crossings += 1
            wrapped_edges += 1
            maximum_length = max(maximum_length, edge.total_length)
            maximum_barrier_rank = max(maximum_barrier_rank, edge.barrier_rank)
            barrier_histogram[edge.barrier_rank] += 1
            if edge.margin <= 0:
                descent_failures += 1
            if minimum_margin is None or edge.margin < minimum_margin:
                minimum_margin = edge.margin
                minimum_example = (
                    f"K:{edge.total_length},j:{edge.position},"
                    f"t:{edge.rank},N:{edge.barrier_rank},"
                    f"word:{chronological_word(edge.bits, edge.total_length)}"
                )
            digest.update(
                (
                    f"{edge.total_length},{edge.bits:x},{edge.position},"
                    f"{edge.lift},{edge.rank},{edge.margin},"
                    f"{edge.barrier_rank}\n"
                ).encode("ascii")
            )

    return {
        "target_prefix_depth": prefix_depth,
        "target_rank_cap": rank_cap,
        "target_suffix_cap": suffix_cap,
        "safe_prefixes": prefixes,
        "eligible_prefixes": eligible_prefixes,
        "rank_trajectories": trajectories,
        "coefficient_crossings": crossings,
        "wrapped_edges": wrapped_edges,
        "capped_trajectories": capped_trajectories,
        "descent_failures": descent_failures,
        "maximum_generated_length": maximum_length,
        "maximum_barrier_rank": maximum_barrier_rank,
        "barrier_rank_histogram": dict(sorted(barrier_histogram.items())),
        "minimum_margin": minimum_margin if minimum_margin is not None else 0,
        "minimum_margin_example": minimum_example,
        "target_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete-depth", type=int, default=18)
    parser.add_argument("--target-prefix-depth", type=int, default=22)
    parser.add_argument("--target-rank-cap", type=int, default=5)
    parser.add_argument("--suffix-cap", type=int, default=10_000)
    args = parser.parse_args()
    if args.complete_depth < 3:
        raise SystemExit("--complete-depth must be at least 3")
    if args.target_prefix_depth < 0 or args.target_rank_cap < 0:
        raise SystemExit("depth and rank cap must be nonnegative")
    if args.suffix_cap < 1:
        raise SystemExit("--suffix-cap must be positive")

    for key, value in complete_audit(args.complete_depth).items():
        print(f"{key}={value}")
    for key, value in targeted_rank_search(
        args.target_prefix_depth, args.target_rank_cap, args.suffix_cap
    ).items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
