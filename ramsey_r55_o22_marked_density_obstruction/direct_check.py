#!/usr/bin/env python3
"""Separate recursive subset and clique audit; no primary import."""
import base64
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def vertices(bits):
    return tuple(i for i in range(bits.bit_length()) if bits >> i & 1)


def opposite(rows):
    return [((1 << len(rows)) - 1) ^ (1 << i) ^ row for i, row in enumerate(rows)]


def clique_list(rows, k, allowed=None):
    found = []
    def visit(chosen, available):
        left = k - len(chosen)
        if left == 0:
            found.append(chosen)
            return
        while available.bit_count() >= left:
            bit = available & -available
            available ^= bit
            v = bit.bit_length() - 1
            visit(chosen + (v,), available & rows[v])
    visit((), (1 << len(rows)) - 1 if allowed is None else allowed)
    return found


def free_sets(rows, order, forbidden_clique, allowed=None):
    """Increasing-vertex recursion, rejecting a clique at its newest vertex."""
    result = []
    def visit(chosen, size, available):
        if size == order:
            result.append(vertices(chosen))
            return
        while size + available.bit_count() >= order:
            bit = available & -available
            available ^= bit
            v = bit.bit_length() - 1
            if not clique_list(rows, forbidden_clique - 1, chosen & rows[v]):
                visit(chosen | bit, size + 1, available)
    visit(0, 0, (1 << len(rows)) - 1 if allowed is None else allowed)
    return sorted(result)


def input_rows():
    hdoc = json.loads((ROOT / 'H20.json').read_text())
    need(type(hdoc['n']) is int and hdoc['n'] == 20, 'H order')
    h = [0] * 20
    for u, v in hdoc['red_edges']:
        need(type(u) is int and type(v) is int and 0 <= u < v < 20
             and not (h[u] >> v & 1), 'H simple edge')
        h[u] |= 1 << v
        h[v] |= 1 << u
    need(sum(r.bit_count() for r in h) == 184, 'H edges')
    need(not clique_list(h, 4) and not clique_list(opposite(h), 5), 'H Ramsey')
    need(vertices(h[0]) == (1, 10, 11, 12, 13, 14, 15)
         and vertices(h[1]) == (0, 16, 17, 18, 19), 'marked H neighborhoods')
    need(clique_list(h, 2, h[1]) == [(16, 17), (16, 19), (17, 18), (18, 19)],
         'marked-neighborhood C4')
    source = json.loads((ROOT / 'SOURCE.json').read_text())
    data = base64.b64decode(source['red_parent_graph6_base64'], validate=True)
    need(len(data) == 40 and data[0] == 85 and all(63 <= b <= 126 for b in data)
         and (data[-1] - 63) & 7 == 0, 'graph6')
    original = [0] * 22
    offset = 0
    for v in range(1, 22):
        for u in range(v):
            if (data[1 + offset // 6] - 63) >> (5 - offset % 6) & 1:
                original[u] |= 1 << v
                original[v] |= 1 << u
            offset += 1
    need(sum(r.bit_count() for r in original) == 228, 'parent count')
    for u, v in source['red_deletions']:
        need(0 <= u < v < 22 and original[u] >> v & 1, 'source deletion')
        original[u] ^= 1 << v
        original[v] ^= 1 << u
    need(sum(r.bit_count() for r in original) == 216
         and not clique_list(original, 4)
         and not clique_list(opposite(original), 5), 'R2 local graph')
    return h, original, opposite(original)


def main():
    cert = json.loads((ROOT / 'CERTIFICATE.json').read_text())
    h, original, base = input_rows()
    domains = free_sets(base, 14, 4)
    need(len(domains) == 6, 'complete recursive fourteen-domains')
    records = []
    for q in domains:
        bits = sum(1 << v for v in q)
        need(not free_sets(base, 9, 3, bits), 'no triangle-free nine-set')
        eight = free_sets(base, 8, 3, bits)
        need(eight, 'capacity witness')
        bad = clique_list(base, 4, ((1 << 22) - 1) ^ bits)
        records.append({'vertices': list(q), 'red_edges': len(clique_list(base, 2, bits)),
                        'maximum_triangle_free_size': 8, 'capacity_witness': list(eight[0]),
                        'complement_red_K4': list(bad[0]) if bad else None})
    need(records == cert['base_fourteen_domains'], 'all domain/capacity/obstruction entries')
    need([i for i, r in enumerate(records) if r['complement_red_K4']] == [3],
         'sole rejected high-density domain')
    need(records[3]['complement_red_K4'] == [8, 11, 16, 18], 'literal red four-clique')
    family = []
    failed = []
    for u, v in clique_list(original, 2):
        rows = base[:]
        rows[u] |= 1 << v
        rows[v] |= 1 << u
        bad = clique_list(rows, 5)
        if bad:
            failed.append([[u, v], list(bad[0])])
            continue
        cases = []
        for i, vs in enumerate(domains):
            bits = sum(1 << w for w in vs)
            if clique_list(rows, 4, bits) or records[i]['complement_red_K4']:
                continue
            ec = len(clique_list(rows, 2, bits))
            need(ec <= 46, 'eligible fourteen-domain density')
            bound = 13 + ec + 32
            need(bound <= 91, 'strict density obstruction')
            cases.append([i, ec, bound])
        family.append({'added_red_edge': [u, v], 'cases': cases,
                       'marked_density_upper_bound': max(c[-1] for c in cases)})
    need(family == cert['candidate_family'], 'complete candidate/domain bounds')
    digest = lambda obj: sha256((json.dumps(obj, separators=(',', ':')) + '\n').encode()).hexdigest()
    need(digest(failed) == cert['invalid_deletion_witnesses_sha256'], 'all invalid-deletion witnesses')
    return {'status': 'RECURSIVE O22 MARKED DENSITY AUDIT VERIFIED',
            'recursive_fourteen_domains': len(domains),
            'eligible_base_domains': 5, 'candidate_family': family,
            'complete_domain_family_sha256': digest([records, family]),
            'certificate_sha256': sha256((ROOT / 'CERTIFICATE.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
