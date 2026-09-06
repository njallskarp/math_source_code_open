#!/usr/bin/env python3
"""Synthetic transport tests, NOT constructions of branch/Ramsey graphs."""

import itertools
from pathlib import Path
from independent_check import check_table, literal_root, projection_orbits, require
from pair_roots import normalize_adorned, root


def check_transport():
    expected, _ = projection_orbits()
    count = 0
    for key, (e, central) in expected.items():
        target = literal_root(key, e, central)
        require(root(*key) == target, "independent descriptor agreement")
        graph = [[0]*43 for _ in range(43)]
        for i, j in itertools.combinations(range(43), 2):
            bit = int((i*i+3*i*j+7*j*j+key[1]+key[2]) % 11 < 5)
            graph[i][j] = graph[j][i] = bit
        for i, j, bit in target["edge_units"]:
            graph[i][j] = graph[j][i] = bit
        if target["partition"]:
            p, q = target["anomalies"]
            graph[p][q] = graph[q][p] = 0
            for w in target["partition"]["one_red_to_pair"]:
                if w not in (0, 1):
                    bit = (w+key[1]) % 2
                    graph[w][p] = graph[p][w] = bit
                    graph[w][q] = graph[q][w] = 1-bit
        for offset in (0, 7, 19):
            scramble = {i: (17*i+offset) % 43 for i in range(43)}
            moved = [[0]*43 for _ in range(43)]
            for i, j in itertools.combinations(range(43), 2):
                moved[scramble[i]][scramble[j]] = graph[i][j]
                moved[scramble[j]][scramble[i]] = graph[i][j]
            descriptor, permutation, normalized = normalize_adorned(
                moved, [scramble[i] for i in target["E"]],
                [scramble[i] for i in target["anomalies"]],
                scramble[0], scramble[1], key[0])
            require(descriptor == target, "projection preserved")
            for i, j in itertools.combinations(range(43), 2):
                require(moved[i][j] == normalized[permutation[i]][permutation[j]],
                        "edge transport")
            require(all(normalized[i][j] == bit
                        for i, j, bit in target["edge_units"]), "root units")
            if target["partition"]:
                p, q = target["anomalies"]
                require(normalized[p][q] == 0, "partition blue edge")
                require(all(normalized[w][p]+normalized[w][q] == 1
                            for w in target["partition"]["one_red_to_pair"]),
                        "universal partition retained")
            buckets = target["ordering_buckets"]
            for bucket in buckets:
                signatures = [tuple(sum(normalized[w][z] for z in group)
                                    for group in buckets) for w in bucket]
                require(signatures == sorted(signatures), "safe residual ordering")
            count += 1
    return count


def check_corruptions():
    text = Path(__file__).with_name("roots.tsv").read_text()
    lines = text.splitlines()
    controls = ["\n".join(lines[:-1])+"\n",
                text + lines[1]+"\n"]
    fields = lines[1].split("\t")
    for index, value in [(0, "not_a_family"), (1, "8"), (2, "7"),
                         (4, "99,0,0,0"), (6, "0"), (7, "0"*64)]:
        bad_fields = fields[:]
        bad_fields[index] = value
        bad = lines[:]
        bad[1] = "\t".join(bad_fields)
        controls.append("\n".join(bad)+"\n")
    for bad in controls:
        try:
            check_table(bad)
        except ValueError:
            pass
        else:
            raise ValueError("damaged table accepted")
    return len(controls)


def main():
    print(f"PASS synthetic full-edge transports={check_transport()}")
    print(f"PASS damaged certificate controls={check_corruptions()}")
    print("Synthetic fixtures are not Ramsey graphs or branch witnesses.")


if __name__ == "__main__":
    main()
