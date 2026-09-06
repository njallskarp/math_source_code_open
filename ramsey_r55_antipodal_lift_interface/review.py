"""Independent review of height 3311's guarded interface and physical fixtures.

Downloads only pinned, inspected producer code; never imports upstream modules.
Generated interface files live in an automatically cleaned temporary directory.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import urlopen

from verify import BLOCKS, H_SHA, N, ROOTS, STARS, block_owner, fixed_colors, need, pair

BASE = "https://raw.githubusercontent.com/helgithorskarp/math_results/"
GLUING_COMMIT = "815b79be8f879d2bff7baa52b1132f9a0e115e64"
PARENT_COMMIT = "40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd"
PARENT_PINS = {
    "model.py": "f93bc5bdb33f920f4c1483652c6fa8478da76464f57d97ece7898f4bdafb7afd",
    "flow.py": "fa9aa09354729c704a5065b8dd7cbefe50a620c048533f23632c0173f2e8dab0",
    "H92.json": H_SHA,
}
GLUING_PINS = {
    "decompose.py": "94b628967a7cf2bed6f7535c2df425c96b5e4abeb2f9b90b5d23421ebd3d7ce2",
    "glue.py": "14bd6964a9b39e8a0062429b884d82682fead5415ca0f19602213c1f6735c9a1",
}
FIXTURE_PINS = {
    "negative.json": "bdc904daa4b43f4362afb3cdf55041e320e2a2854d46bf27d8c251cd10da51bc",
    "positive.json": "322370d346f7b01f0cba73c95941557cef07a0c3256e24c667b371a188fe4468",
}
SCHEMA_SHA = "ee1fa61df8ca667e348f3d3acf99136a26f0b96705e19f035dd18f86c05d15f2"
CLAUSES_SHA = "2192a68adb96d80cee3ded6c7503b5c96a81b771299500c9e3c58e594519f6b6"


def retrieve(root):
    for directory, commit, pins in (
        ("ramsey_r55_antipodal_degree_projection", PARENT_COMMIT, PARENT_PINS),
        ("ramsey_r55_antipodal_block_gluing", GLUING_COMMIT, GLUING_PINS),
    ):
        target = root / directory
        target.mkdir()
        for name, digest in pins.items():
            with urlopen(BASE + commit + "/" + directory + "/" + name, timeout=30) as f:
                data = f.read()
            need(sha256(data).hexdigest() == digest, "download source identity: " + name)
            (target / name).write_bytes(data)


def command(*args):
    return [sys.executable] + (["-O"] if sys.flags.optimize else []) + ["-B", *map(str, args)]


def run(*args):
    return subprocess.run(command(*args), check=True, capture_output=True,
                          text=True, timeout=120).stdout


def schema_check(schema, fixed, owner):
    visible = [e for e in combinations(range(N), 2) if e not in fixed and e not in owner]
    vi = {e: j for j, e in enumerate(visible, 1)}
    bp = [[pair(u, v) for u in L for v in R] for L, R in BLOCKS]
    residuals = [
        {"vertex": v, "constant": (20 if v in ROOTS else 21) -
         sum(c for e, c in fixed.items() if v in e),
         "subtract_variables": [vi[e] for e in visible if v in e]}
        for v in range(N)]
    densities = []
    for r in (0, 1):
        q = sorted(set(range(N)) - {r} - STARS[r])
        es = list(combinations(q, 2))
        densities.append({"root": r, "sum_variables": [vi[e] for e in es if e in vi],
                          "equals": 124 - sum(fixed.get(e, 0) for e in es)})
    expected = {
        "format": "r55-antipodal-guarded-k5-v1", "n": N,
        "visible_pairs": [list(e) for e in visible],
        "blocks": [{"left": list(L), "right": list(R), "pairs": [list(e) for e in ps]}
                   for (L, R), ps in zip(BLOCKS, bp)],
        "fixed_pairs": [[*e, c] for e, c in sorted(fixed.items())],
        "degree_targets": [20 if v in ROOTS else 21 for v in range(N)],
        "density_equalities": densities, "residuals": residuals,
        "parent_pins": PARENT_PINS,
        "warning": "All visible colors must be fixed before the conditional gluing oracle; this interface is not a SAT witness.",
    }
    need(schema == expected, "complete physical schema")
    physical = visible + sorted(owner)
    indices = {e: j for j, e in enumerate(physical, 1)}
    return visible, bp, indices


def expected_clauses(fixed, indices):
    rows = Counter()
    for vertices in combinations(range(N), 5):
        edges = tuple(combinations(vertices, 2))
        colors = {fixed[e] for e in edges if e in fixed}
        if len(colors) > 1:
            continue
        for c in sorted(colors) if colors else (0, 1):
            row = tuple(sorted((1 if c == 0 else -1) * indices[e]
                               for e in edges if e in indices))
            need(row, "no fixed monochromatic five-set")
            rows[row] += 1
    return rows


def unpack(record, visible, block_pairs, indices):
    need(type(record) is list and len(record) == 2, "record structure")
    guard, groups = record
    need(type(guard) is list and type(groups) is list, "guard/groups lists")
    row = []
    for literal in guard:
        need(type(literal) is int and 1 <= abs(literal) <= len(visible), "guard literal")
        row.append(literal)
    seen = []
    for item in groups:
        need(type(item) is list and len(item) == 2, "group structure")
        k, literals = item
        need(type(k) is int and 0 <= k < 3 and type(literals) is list and literals,
             "nonempty physical block")
        seen.append(k)
        for literal in literals:
            need(type(literal) is int and 1 <= abs(literal) <= len(block_pairs[k]),
                 "local literal")
            j = indices[block_pairs[k][abs(literal) - 1]]
            row.append(j if literal > 0 else -j)
    need(seen == sorted(set(seen)) and len(seen) <= 2, "canonical block support")
    need(len(row) == len(set(row)) and len({v > 0 for v in row}) == 1,
         "distinct monochromatic literals")
    return tuple(sorted(row))


def interface_check(root):
    fixed = fixed_colors()
    owner = block_owner(BLOCKS, fixed)
    producer = root / "ramsey_r55_antipodal_block_gluing" / "decompose.py"
    work = root / "generated"
    run(producer, "--work", work)
    schema_raw = (work / "schema.json").read_bytes()
    need(sha256(schema_raw).hexdigest() == SCHEMA_SHA, "actual schema bytes")
    visible, bp, indices = schema_check(json.loads(schema_raw), fixed, owner)
    wanted = expected_clauses(fixed, indices)
    physical_count, unique_count = sum(wanted.values()), len(wanted)
    multiplicities = Counter(wanted.values())
    counts = Counter()
    duplicate_by_arity = Counter()
    previous = None
    digest, byte_count = sha256(), 0
    first = None
    with (work / "clauses.jsonl").open("rb") as f:
        for line in f:
            digest.update(line)
            byte_count += len(line)
            record = json.loads(line)
            row = unpack(record, visible, bp, indices)
            if first is None:
                first = record, row
            key = len(row), row
            need(previous is None or previous < key, "complete unique canonical stream")
            previous = key
            multiplicity = wanted.pop(row, 0)
            need(multiplicity > 0, "unexpected or duplicate physical clause")
            arity = len(record[1])
            counts[arity] += 1
            duplicate_by_arity[arity] += multiplicity - 1
    need(not wanted, "missing full physical clauses")
    need(digest.hexdigest() == CLAUSES_SHA and byte_count == 30487019,
         "complete upstream interface bytes")
    # Changes to a real guard and a real physical block index cannot be ignored.
    need(first is not None, "nonempty stream")
    record, row = first
    broken = json.loads(json.dumps(record))
    need(broken[0], "first guard nonempty")
    broken[0][0] = 523 if broken[0][0] > 0 else -523
    rejected = False
    try:
        rejected = unpack(broken, visible, bp, indices) != row
    except ValueError:
        rejected = True
    need(rejected, "changed guard must change or invalidate physical predicate")
    return {
        "physical_records": physical_count, "unique_clauses": unique_count,
        "clause_counts_by_arity": [counts[i] for i in range(3)],
        "discarded_duplicate_occurrences_by_arity": [duplicate_by_arity[i] for i in range(3)],
        "multiplicity_histogram": dict(sorted(multiplicities.items())),
        "clauses_bytes": byte_count, "clauses_sha256": digest.hexdigest(),
        "schema_sha256": sha256(schema_raw).hexdigest(),
        "all_guards_and_hidden_literals_checked": True,
    }


def fixture_check(name, root):
    path = Path(__file__).with_name(name)
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == FIXTURE_PINS[name], "fixture identity")
    obj = json.loads(raw)
    need(obj["n"] == 12 and obj["blocks"] ==
         [[[0, 1], [2, 3]], [[4, 5], [6, 7]], [[8, 9], [10, 11]]],
         "fixture labels")
    need(obj["row_margins"] == obj["column_margins"] == [[1, 1]] * 3, "fixture margins")
    holes = [[pair(u, v) for u in L for v in R] for L, R in obj["blocks"]]
    owner = {e: (i, j) for i, es in enumerate(holes) for j, e in enumerate(es)}
    visible_red = {tuple(e) for e in obj["red_visible_edges"]}
    need(len(visible_red) == len(obj["red_visible_edges"]) and not visible_red & owner.keys(),
         "fixture visible colors")
    all_pairs = list(combinations(range(12), 2))
    index = {e: j for j, e in enumerate(all_pairs)}
    visible_mask = sum(1 << index[e] for e in visible_red)
    # A graph mask over all 66 physical edges is a separate truth oracle.
    five_masks = [(S, sum(1 << index[e] for e in combinations(S, 2)))
                  for S in combinations(range(12), 5)]
    records = []
    for S, _ in five_masks:
        es = tuple(combinations(S, 2))
        cs = {int(e in visible_red) for e in es if e not in owner}
        if len(cs) == 1:
            c = next(iter(cs))
            local = [sum(1 << j for j, e in enumerate(h) if e in es) for h in holes]
            need(any(local), "no visible monochromatic K5")
            records.append((c, local))
    good = []
    witnesses = []
    for states in product(range(16), repeat=3):
        mask = visible_mask | sum(1 << index[e] for i, es in enumerate(holes)
                                  for j, e in enumerate(es) if states[i] >> j & 1)
        bad = [(S, "blue" if mask & fm == 0 else "red") for S, fm in five_masks
               if mask & fm in (0, fm)]
        factored_bad = any(all((states[i] & m == m if c else states[i] & m == 0)
                              for i, m in enumerate(ms) if m) for c, ms in records)
        need(bool(bad) == factored_bad, "all physical fixture colorings")
        if all(s in (6, 9) for s in states):
            if bad:
                witnesses.append({"states": list(states), "vertices": list(bad[0][0]),
                                  "color": bad[0][1]})
            else:
                good.append(list(states))
    domains = []
    for i in range(3):
        domains.append([s for s in (6, 9) if not any(
            ms[i] and sum(bool(m) for m in ms) == 1 and
            (s & ms[i] == ms[i] if c else s & ms[i] == 0) for c, ms in records)])
    relations = {}
    for i, j in combinations(range(3), 2):
        relations[f"{i}-{j}"] = [[a, b] for a, b in product(domains[i], domains[j])
                                if not any(ms[i] and ms[j] and
                                    (a & ms[i] == ms[i] if c else a & ms[i] == 0) and
                                    (b & ms[j] == ms[j] if c else b & ms[j] == 0)
                                    for c, ms in records)]
    joined = [list(states) for states in product(*domains) if all(
        [states[i], states[j]] in relations[f"{i}-{j}"]
        for i, j in combinations(range(3), 2))]
    need(joined == good, "complete physical fixture lift set")
    output = root / (name + ".result")
    result = json.loads(run(root / "ramsey_r55_antipodal_block_gluing" / "glue.py",
                            "--input", path, "--output", output))
    need(result["domains"] == domains and result["relations"] == relations, "upstream oracle states")
    need(result["status"] == ("LIFT_FOUND" if good else "NO_LIFT_PAIRWISE_JOIN"),
         "upstream oracle status")
    if good:
        need(result["states"] in good, "actual positive lift")
        states = result["states"]
        expected_red = visible_red | {e for i, es in enumerate(holes)
                                     for j, e in enumerate(es) if states[i] >> j & 1}
        need(result["graph"] == {"n": 12, "red_edges": [list(e) for e in sorted(expected_red)]},
             "decoded actual positive graph")
    zero = json.loads(run(root / "ramsey_r55_antipodal_block_gluing" / "glue.py",
                         "--input", path, "--output", root / (name + ".zero"), "--work-limit", 0))
    need(zero["status"] == "INCOMPLETE", "budget is not a refutation")
    return {"domains": domains, "relations": relations, "valid_lifts": good,
            "margin_correct_bad_witnesses": witnesses, "all_hidden_colorings_checked": 4096,
            "oracle_status": result["status"], "zero_budget_status": zero["status"]}


def main():
    with tempfile.TemporaryDirectory(prefix="r55-lift-review-") as name:
        root = Path(name)
        retrieve(root)
        interface = interface_check(root)
        negative = fixture_check("negative.json", root)
        positive = fixture_check("positive.json", root)
        need(negative["domains"] == [[6, 9], [6, 9], [6]], "negative domains")
        need(negative["relations"] ==
             {"0-1": [[6, 9], [9, 6], [9, 9]], "0-2": [[6, 6]], "1-2": [[6, 6]]},
             "negative pair relations")
        need(not negative["valid_lifts"] and len(positive["valid_lifts"]) == 5,
             "physical obstruction and positive boundary")
        red0 = {tuple(e) for e in json.loads(Path(__file__).with_name("negative.json").read_text())["red_visible_edges"]}
        red1 = {tuple(e) for e in json.loads(Path(__file__).with_name("positive.json").read_text())["red_visible_edges"]}
        need(red1 - red0 == {(0, 4)} and red0 <= red1, "one visible edge change")
        print(json.dumps({"target_height": 3311, "upstream_commit": GLUING_COMMIT,
                          "interface": interface, "negative": negative, "positive": positive,
                          "scope": "structural theorem, full guarded interface, and two physical fixtures; no H92 decision",
                          "solver_called": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
