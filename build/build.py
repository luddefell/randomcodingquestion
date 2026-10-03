"""Generate ../problems.js from the problem definitions.

    python3 build/build.py

Runs every reference solution on its tests, checks it against the known
example outputs, and writes the expected outputs into problems.js.
Also writes build/solutions.json (reference Verilog, for verify.html)."""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import harness
from common import REGISTRY, md
import lc_arrays, lc_structures, lc_algorithms, verilog  # noqa: F401  (registers problems)
from complexity import C as COMPLEXITY

DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}


def norm(v, cmp):
    key = lambda x: json.dumps(x, sort_keys=True)
    if cmp == "any" and isinstance(v, list):
        return sorted(v, key=key)
    if cmp == "anyDeep" and isinstance(v, list):
        return sorted([sorted(x, key=key) if isinstance(x, list) else x for x in v], key=key)
    return v


def starter_lc(p):
    head = ""
    sig_text = json.dumps(p.get("params", "")) + p.get("ret", "") + " ".join(p.get("methods", []))
    if "ListNode" in sig_text:
        head += ("# Definition for singly-linked list.\n# class ListNode:\n"
                 "#     def __init__(self, val=0, next=None):\n"
                 "#         self.val = val\n#         self.next = next\n\n")
    if "TreeNode" in sig_text:
        head += ("# Definition for a binary tree node.\n# class TreeNode:\n"
                 "#     def __init__(self, val=0, left=None, right=None):\n"
                 "#         self.val = val\n#         self.left = left\n#         self.right = right\n\n")
    if p["kind"] == "design":
        body = "\n\n".join(f"    def {m}:\n        pass" for m in p["methods"])
        return f"{head}class {p['cls']}:\n\n{body}\n"
    args = ", ".join(f"{n}: {t}" for n, t in p["params"])
    return f"{head}class Solution:\n    def {p['fn']}(self, {args}) -> {p['ret']}:\n        "


def build_lc(p):
    spec = {k: p.get(k) for k in ("kind", "fn", "cls", "params", "ret", "inplace")}
    tests = []
    for i, case in enumerate(p["tests"]):
        args = case.args
        got = harness.call(spec, p["ref"], args)
        got = json.loads(json.dumps(got))
        if case.asserted:
            want = json.loads(json.dumps(harness.to_json(case.out)))
            if norm(got, p["cmp"]) != norm(want, p["cmp"]):
                raise AssertionError(f"{p['id']} test {i}: reference gave {got}, expected {want}")
        tests.append({"in": json.loads(json.dumps(args)), "out": got})
    out = {k: p[k] for k in ("track", "kind", "id", "title", "diff", "topic", "cmp", "examples")}
    assert p["id"] in COMPLEXITY, f"{p['id']}: add its complexity to build/complexity.py"
    time, space, note = COMPLEXITY[p["id"]]
    out.update(desc=md(p["desc"]), starter=starter_lc(p), tests=tests, spec=spec,
               complexity={"time": time, "space": space, "note": note})
    return out


# ---------- Verilog ----------

def rand_val(rng, port, bias):
    if port["name"] in bias:
        b = bias[port["name"]]
        if port["width"] == 1:
            return 1 if rng.random() < b else 0
    return rng.getrandbits(port["width"])


def build_v(p):
    ins = [q for q in p["ports"] if q["dir"] == "in" and q["name"] != "clk"]
    outs = [q for q in p["ports"] if q["dir"] == "out"]
    rng = random.Random(p["id"])
    data = {k: p[k] for k in ("track", "id", "title", "diff", "topic", "ports", "seq")}
    data["kind"] = "verilog"
    data["desc"] = md(p["desc"])

    def outs_list(o):
        assert set(o) == {q["name"] for q in outs}, f"{p['id']}: model outputs {set(o)}"
        return [None if o[q["name"]] is None else o[q["name"]] & ((1 << q["width"]) - 1) for q in outs]

    if not p["seq"]:
        bits = sum(q["width"] for q in ins)
        if p["vectors"]:
            vecs = p["vectors"](rng)
        elif bits <= 10:
            vecs = []
            for n in range(1 << bits):
                v, shift = {}, 0
                for q in reversed(ins):
                    v[q["name"]] = (n >> shift) & ((1 << q["width"]) - 1)
                    shift += q["width"]
                vecs.append(v)
        else:
            vecs = [{q["name"]: 0 for q in ins}, {q["name"]: (1 << q["width"]) - 1 for q in ins}]
            vecs += [{q["name"]: rand_val(rng, q, p["bias"]) for q in ins} for _ in range(150)]
        data["tests"] = [{"in": [v[q["name"]] for q in ins], "out": outs_list(p["model"](dict(v)))}
                         for v in vecs]
    else:
        seqs = []
        for s in range(p["seqs"]):
            if p["gen"]:
                cycles = p["gen"](rng, s)
            else:
                cycles = []
                for c in range(p["cycles"]):
                    v = {q["name"]: rand_val(rng, q, p["bias"]) for q in ins}
                    if "reset" in v:
                        v["reset"] = 1 if c < 2 else (1 if rng.random() < 0.04 else 0)
                    cycles.append(v)
            m = p["model"]()
            seqs.append({"in": [[v[q["name"]] for q in ins] for v in cycles],
                         "out": [outs_list(m.step(dict(v))) for v in cycles]})
        data["tests"] = seqs
    return data


def main():
    seen, problems, solutions = set(), [], {}
    for p in REGISTRY:
        assert (p["track"], p["id"]) not in seen, f"duplicate id {p['id']}"
        seen.add((p["track"], p["id"]))
        problems.append(build_lc(p) if p["track"] == "lc" else build_v(p))
        if p["track"] == "v":
            solutions[p["id"]] = p["solution"]
    problems.sort(key=lambda p: (p["track"], DIFF_ORDER[p["diff"]]))
    with open(os.path.join(ROOT, "problems.js"), "w") as f:
        f.write("// Generated by build/build.py. Do not edit by hand.\n")
        f.write("window.PROBLEMS = ")
        json.dump(problems, f, separators=(",", ":"))
        f.write(";\n")
    with open(os.path.join(HERE, "solutions.json"), "w") as f:
        json.dump(solutions, f, indent=1)
    counts = {}
    for p in problems:
        counts[(p["track"], p["diff"])] = counts.get((p["track"], p["diff"]), 0) + 1
    print(f"{len(problems)} problems:", ", ".join(f"{t}/{d}={n}" for (t, d), n in sorted(counts.items())))


if __name__ == "__main__":
    main()
