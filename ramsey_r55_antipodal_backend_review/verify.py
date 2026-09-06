"""Independent affine-conservation audit of the exact fixed-H92 CNF.

No generator/checker imports and no solver calls. The pinned generator is
executed only with --emit-only. Count-tree and ripple annotations are not
trusted: word meanings follow by exact integer elimination of local
full-adder identities.
"""
import argparse
from collections import Counter
import copy
import hashlib
import itertools as it
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request

PARENT = "40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd"
BACKEND = "7f25e7786bbb850b2979a9d877543f1dc44ec5df"
FILES = [
    (BACKEND, "ramsey_r55_antipodal_degree_backend/generate.py",
     "fd3008b7305bf2b9b179a7bea46872d0342c633db682b4c401d7c7af89a528c3"),
    (PARENT, "ramsey_r55_antipodal_degree_projection/model.py",
     "f93bc5bdb33f920f4c1483652c6fa8478da76464f57d97ece7898f4bdafb7afd"),
    (PARENT, "ramsey_r55_antipodal_degree_projection/flow.py",
     "fa9aa09354729c704a5065b8dd7cbefe50a620c048533f23632c0173f2e8dab0"),
    (PARENT, "ramsey_r55_antipodal_degree_projection/H92.json",
     "926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466"),
    (PARENT, "ramsey_r55_antipodal_degree_projection/PROOF.md",
     "f10926ef9d8c7a6f1b26825989c840ba9e8d72712dcdb776ca29bb1645f8a170"),
]
CNF = "9afab291586190b946e30b935970c0dc09f9fc36d906ec816d7c2f5bed5e306f"
LAYOUT = "8cac48de646842543af5cd207b8c176b11492e750806b179aabf0edfa1274e9e"
PHYSICAL = "ece2f0c1a0ebf7f43fee80bd848b0ff082602e91f36bdc9946cff230e8a4ac25"
PROJECTION = "0a5407af70b1711597b9bdd7a46753c78ee33a297f4812fc9b271172d6c2331a"


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(data):
    return (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()


def value(lit, assignment):
    return lit if type(lit) is bool else assignment[abs(lit)] == (lit > 0)


def inverse(lit):
    return not lit if type(lit) is bool else -lit


def simplify(rows):
    answer = []
    for row in rows:
        if any(x is True for x in row):
            continue
        literals = {x for x in row if type(x) is int}
        if any(-x in literals for x in literals):
            continue
        answer.append(tuple(sorted(literals)))
    return answer


def accumulate(form, lit, weight=1):
    """Affine form has constant coordinate 0; Boolean negation is 1-x."""
    if type(lit) is bool:
        form[0] += weight * int(lit)
    elif lit > 0:
        form[lit] += weight
    else:
        form[0] += weight
        form[-lit] -= weight


def cleaned(form):
    return {v: n for v, n in form.items() if n}


def input_sum(literals):
    result = Counter()
    for lit in literals:
        require(type(lit) is int and 1 <= abs(lit) <= 731, "primary literal domain")
        accumulate(result, lit)
    return cleaned(result)


def expected_system(projection):
    upper = {}
    for block in projection["blocks"]:
        for v in block["left"]:
            require(v not in upper, "disjoint left vertices")
            upper[v] = len(block["right"])
        for v in block["right"]:
            require(v not in upper, "disjoint right vertices")
            upper[v] = len(block["left"])
    margins = {}
    next_id = 524
    for v in sorted(upper):
        margins[str(v)] = list(range(next_id, next_id + upper[v]))
        next_id += upper[v]
    require(next_id == 732, "complete unary allocation")
    conditions = {}
    for row in projection["residuals"]:
        v = row["vertex"]
        conditions["degree-" + str(v)] = (
            "constant", row["subtract_variables"] + margins.get(str(v), []), row["constant"])
    for row in projection["density_equalities"]:
        conditions["density-" + str(row["root"])] = ("constant", row["sum_variables"], row["equals"])
    for b, block in enumerate(projection["blocks"]):
        l, r = block["left"], block["right"]
        flatten = lambda vertices: [x for v in vertices for x in margins[str(v)]]
        conditions["balance-" + str(b)] = ("balance", flatten(l), flatten(r))
        # Derive labels from the physical subset, not list position.
        for subset in block["subset_cuts"]:
            mask = sum(1 << l.index(v) for v in subset)
            conditions[f"cut-{b}-{mask}"] = (
                "cut", flatten(subset),
                [x for v in r for x in margins[str(v)][:len(subset)]])
    require(len(conditions) == 93, "complete physical high-level system")
    monotone = simplify([[-bits[i], bits[i - 1]]
                        for bits in margins.values() for i in range(1, len(bits))])
    return margins, conditions, monotone


def audit(meta, clauses, variables):
    require(meta["format"] == "r55-projected-binary-backend-v1", "format")
    require(meta["variables"] == variables and meta["clauses"] == len(clauses), "declared size")
    require(meta["physical_variables"] == 523 and meta["margin_variables"] == 208, "input partition")
    require(sha(canonical(meta["projection"])) == PROJECTION, "entire imported projection")
    base = meta["base_clauses"]
    require(base == 70848, "physical prefix length")
    raw = ("p cnf 523 70848\n" +
           "".join(" ".join(map(str, c)) + " 0\n" for c in clauses[:base])).encode()
    require(sha(raw) == PHYSICAL, "entire imported physical clause prefix")
    margins, definitions, monotone = expected_system(meta["projection"])
    end = base + len(monotone)
    require(meta["margins"] == margins and meta["monotone_end"] == end, "unary layout")
    require(clauses[base:end] == monotone, "all unary implications")
    owned = set(range(end))

    def own(start, stop):
        require(type(start) is int and type(stop) is int and end <= start <= stop <= len(clauses),
                "clause ownership interval")
        segment = set(range(start, stop))
        require(not owned.intersection(segment), "overlapping clause ownership")
        owned.update(segment)

    gates = meta["fulladders"]
    require(variables == 731 + 2 * len(gates), "complete auxiliary definition")
    truth_cases = 0
    for j, g in enumerate(gates):
        s, c = g["sum"], g["carry"]
        require((s, c) == (732 + 2 * j, 733 + 2 * j), "fresh ordered outputs")
        ins = g["inputs"]
        require(len(ins) == 3 and all(type(x) is bool or
                (type(x) is int and 1 <= abs(x) < s) for x in ins), "acyclic gate inputs")
        ids = sorted({abs(x) for x in ins if type(x) is int}) + [s, c]
        block = clauses[g["start"]:g["end"]]
        require(all(set(map(abs, row)) <= set(ids) for row in block), "gate clause support")
        own(g["start"], g["end"])
        for bits in it.product((False, True), repeat=len(ids)):
            a = dict(zip(ids, bits))
            predicate = all(any(value(x, a) for x in row) for row in block)
            identity = int(a[s]) + 2 * int(a[c]) == sum(value(x, a) for x in ins)
            require(predicate == identity, "exact local adder identity")
            truth_cases += 1

    rewrites = 0

    def reduce_word(word):
        """Eliminate gate identities backwards, without any tree annotation."""
        nonlocal rewrites
        form = Counter()
        for i, lit in enumerate(word):
            require(type(lit) is bool or
                    (type(lit) is int and 1 <= abs(lit) <= variables), "word literal")
            accumulate(form, lit, 1 << i)
        for g in reversed(gates):
            k = form.pop(g["sum"], 0)
            carry_weight = form.pop(g["carry"], 0)
            require(carry_weight == 2 * k, "unbalanced output weights / lost carry")
            if k:
                for lit in g["inputs"]:
                    accumulate(form, lit, k)
                rewrites += 1
        require(all(0 <= v <= 731 for v in form), "uneliminated auxiliary")
        return cleaned(form)

    counts = meta["counts"]
    forms = []
    for row in counts:
        form = reduce_word(row["output"])
        require(form == input_sum(row["inputs"]), "count affine identity")
        forms.append(form)
    rows = meta["constraints"]
    require(len(rows) == len(definitions) and {r["tag"] for r in rows} == set(definitions),
            "all 93 obligations exactly once")
    used_counts = set()
    evidence = []

    def count(index, physical_inputs):
        require(type(index) is int and 0 <= index < len(counts), "count index")
        require(forms[index] == input_sum(physical_inputs), "physical input expression")
        used_counts.add(index)
        return counts[index]["output"]

    for row in rows:
        kind, left, right = definitions[row["tag"]]
        require(row["kind"] == kind, "condition kind")
        a = count(row["left_count"], left)
        if kind == "constant":
            require(type(right) is int, "integer constant")
            terminal = [[]] if not 0 <= right < (1 << len(a)) else [
                [lit if right >> i & 1 else inverse(lit)] for i, lit in enumerate(a)]
            evidence.append([row["tag"], sorted(input_sum(left).items()), right])
        else:
            b = count(row["right_count"], right)
            width = max(len(a), len(b))
            if kind == "balance":
                aa = a + [False] * (width - len(a))
                bb = b + [False] * (width - len(b))
                terminal = [c for x, y in zip(aa, bb) for c in [[inverse(x), y], [x, inverse(y)]]]
            else:
                output = row["comparison"]["output"]
                require(len(output) == width + 1, "full comparison output including carry")
                actual = reduce_word(output)
                expected = Counter(input_sum(right))
                expected.subtract(input_sum(left))
                expected[0] += 1 << width
                require(actual == cleaned(expected), "global unsigned subtraction identity")
                terminal = [[output[-1]]]
            evidence.append([row["tag"], sorted(input_sum(left).items()), sorted(input_sum(right).items())])
        require(clauses[row["start"]:row["end"]] == simplify(terminal), "exact terminal clauses")
        own(row["start"], row["end"])
    require(used_counts == set(range(len(counts))), "all count outputs linked to obligations")
    require(owned == set(range(len(clauses))), "complete clause ownership")
    return {
        "clauses": len(clauses), "variables": variables, "physical_variables": 523,
        "margin_variables": 208, "deterministic_arithmetic_variables": variables - 731,
        "full_adders": len(gates), "local_truth_assignments": truth_cases,
        "population_count_identities": len(counts), "comparison_identities": 45,
        "affine_gate_eliminations": rewrites, "unary_implications": len(monotone),
        "conditions": dict(Counter(v[0] for v in definitions.values())),
        "physical_expression_sha256": sha(canonical(evidence)),
    }


def negative_controls(meta, clauses, variables):
    results = []
    for name in ["margin_direction", "missing_cut", "wrong_count", "lost_carry",
                 "reused_output", "adder_clause", "comparison_sign", "extra_clause"]:
        m = copy.deepcopy(meta)
        c = list(clauses)
        if name == "margin_direction":
            c[70848] = tuple(-x for x in c[70848])
        elif name == "missing_cut":
            m["constraints"].pop()
        elif name == "wrong_count":
            m["constraints"][2]["left_count"] = m["constraints"][3]["left_count"]
        elif name == "lost_carry":
            next(x for x in m["counts"] if len(x["output"]) > 2)["output"].pop()
        elif name == "reused_output":
            m["fulladders"][0]["sum"] += 2
        elif name == "adder_clause":
            at = m["fulladders"][0]["start"]
            c[at] = tuple(-x for x in c[at])
        elif name == "comparison_sign":
            at = m["constraints"][-1]["start"]
            c[at] = tuple(-x for x in c[at])
        elif name == "extra_clause":
            c.append((1,))
            m["clauses"] += 1
        try:
            audit(m, c, variables)
        except (ValueError, KeyError, IndexError):
            results.append(name)
        else:
            raise ValueError("invalid certificate accepted: " + name)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, help="offline root with the two pinned source directories")
    parser.add_argument("--work", type=Path, help="check an existing emitted case.cnf/encoding.json directory")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="r55-backend-review-") as tmp:
        root = Path(tmp)
        work = args.work
        if work is None:
            for commit, path, pin in FILES:
                raw = (args.upstream / path).read_bytes() if args.upstream else urllib.request.urlopen(
                    "https://raw.githubusercontent.com/helgithorskarp/math_results/" + commit + "/" + path,
                    timeout=60).read()
                require(sha(raw) == pin, "pinned source: " + path)
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
            work = root / "generated"
            command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
            subprocess.run(command + [str(root / FILES[0][1]), "--work", str(work), "--emit-only"],
                           check=True, capture_output=True, text=True, timeout=60)
        raw = (work / "case.cnf").read_bytes()
        layout = (work / "encoding.json").read_bytes()
        require(sha(raw) == CNF and sha(layout) == LAYOUT, "published instance identities")
        lines = raw.decode().splitlines()
        header = lines[0].split()
        require(header[:2] == ["p", "cnf"] and len(header) == 4, "DIMACS header")
        variables, declared = map(int, header[2:])
        clauses = []
        for line in lines[1:]:
            tokens = list(map(int, line.split()))
            require(tokens and tokens[-1] == 0 and
                    all(1 <= abs(x) <= variables for x in tokens[:-1]), "DIMACS clause")
            clauses.append(tuple(tokens[:-1]))
        require(len(clauses) == declared, "DIMACS count and EOF")
        meta = json.loads(layout)
        result = audit(meta, clauses, variables)
        # The alternative certificate does not depend on the author's
        # count-tree decomposition or ripple/comparator wiring annotations.
        stripped = copy.deepcopy(meta)
        for row in stripped["counts"]:
            row.pop("additions")
        for row in stripped["constraints"]:
            if row["kind"] == "cut":
                row["comparison"] = {"output": row["comparison"]["output"]}
        require(audit(stripped, clauses, variables) == result, "annotation-free independence")
        result["count_tree_and_ripple_annotations_required"] = False
        unary_words = 0
        for width in (4, 8, 9):
            for bits in it.product((False, True), repeat=width):
                total = sum(bits)
                monotone = all(not bits[i] or bits[i - 1] for i in range(1, width))
                prefix = bits == (True,) * total + (False,) * (width - total)
                require(monotone == prefix, "unary prefix characterization")
                if monotone:
                    require(all(sum(bits[:k]) == min(total, k) for k in range(1, 5)),
                            "all truncated margin meanings")
                unary_words += 1
        result["unary_words_checked"] = unary_words
        result["controls_rejected"] = negative_controls(meta, clauses, variables)
        result.update(status="INDEPENDENT_POINTWISE_BACKEND_EQUIVALENCE_PASS",
                      source_commit=BACKEND, cnf_sha256=sha(raw), layout_sha256=sha(layout),
                      scope="Exactly one auxiliary extension per satisfying retained-edge assignment of the fixed mixed system; no SAT verdict or global Ramsey coverage.")
        print(canonical(result).decode(), end="")


if __name__ == "__main__":
    main()
