# Test harness shared by the site (runs in Pyodide) and build/build.py.
import json, sys, io, copy, traceback
from typing import *


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


PRELUDE = """
from typing import *
import collections, heapq, math, itertools, functools, bisect, string, re
from collections import *
from heapq import *
from functools import *
from itertools import *
from math import inf
"""


# ---------- conversions between JSON test data and Python objects ----------

def build_list(arr):
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_arr(node):
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
        if len(out) > 10000:
            raise RuntimeError("linked list is too long (cycle?)")
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue, i = [root], 1
    for node in queue:
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
        if i >= len(arr):
            break
    return root


def tree_to_arr(root):
    out, queue = [], [root]
    for node in queue:
        if len(out) > 10000:
            raise RuntimeError("tree is too large (cycle?)")
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def to_py(val, typ):
    """JSON value -> argument object, guided by the type hint."""
    if typ.startswith("List[") and ("ListNode" in typ or "TreeNode" in typ):
        return [to_py(v, typ[5:-1]) for v in val]
    if "ListNode" in typ:
        return build_list(val)
    if "TreeNode" in typ:
        return build_tree(val)
    return copy.deepcopy(val)


def to_json(val):
    """Return value -> plain JSON-able data."""
    if isinstance(val, ListNode):
        return list_to_arr(val)
    if isinstance(val, TreeNode):
        return tree_to_arr(val)
    if isinstance(val, (list, tuple)):
        return [to_json(v) for v in val]
    if isinstance(val, (set, frozenset)):
        return sorted(to_json(v) for v in val)
    if isinstance(val, dict):
        return {str(k): to_json(v) for k, v in val.items()}
    return val


# ---------- running one case ----------

def call(spec, target, case):
    """spec: problem spec dict; target: function (fn) or class (design)."""
    if spec["kind"] == "design":
        ops, args = case
        obj = target(*args[0])
        out = [None]
        for op, a in zip(ops[1:], args[1:]):
            out.append(to_json(getattr(obj, op)(*copy.deepcopy(a))))
        return out
    types = [t for _, t in spec["params"]]
    args = [to_py(v, t) for v, t in zip(case, types)]
    res, typ = target(*args), spec.get("ret") or ""
    if spec.get("inplace") is not None:
        res, typ = args[spec["inplace"]], types[spec["inplace"]]
    if res is None and ("ListNode" in typ or "TreeNode" in typ):
        return []  # empty list / tree
    return to_json(res)


def fmt_err(e):
    msg = "".join(traceback.format_exception_only(type(e), e)).strip()
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "solution.py"]
    line = frames[-1].lineno if frames else getattr(e, "lineno", None)
    return f"{msg} (line {line})" if line else msg


def run(code, spec_json, cases_json):
    """Entry point used by the site. Returns a JSON string."""
    spec = json.loads(spec_json)
    ns = {"ListNode": ListNode, "TreeNode": TreeNode}
    exec(PRELUDE, ns)
    try:
        exec(compile(code, "solution.py", "exec"), ns)
    except Exception as e:
        return json.dumps({"error": fmt_err(e)})

    if spec["kind"] == "design":
        cls = ns.get(spec["cls"])
        if cls is None:
            return json.dumps({"error": f"Couldn't find class {spec['cls']}."})
        get_target = lambda: cls
    else:
        if "Solution" not in ns:
            return json.dumps({"error": "Couldn't find class Solution."})
        if not hasattr(ns["Solution"], spec["fn"]):
            return json.dumps({"error": f"Couldn't find method {spec['fn']} on class Solution."})
        get_target = lambda: getattr(ns["Solution"](), spec["fn"])

    results, out = [], io.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        for case in json.loads(cases_json):
            try:
                results.append({"got": json.dumps(call(spec, get_target(), case))})
            except Exception as e:
                results.append({"error": fmt_err(e)})
    finally:
        sys.stdout = old
    return json.dumps({"results": results, "stdout": out.getvalue()[:5000]})
