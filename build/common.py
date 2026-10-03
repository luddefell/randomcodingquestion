"""Problem registration helpers used by the problem files."""
import html, re

REGISTRY = []
_MISSING = object()


class Case:
    def __init__(self, args, out=_MISSING):
        self.args = list(args)
        self.out = out

    @property
    def asserted(self):
        return self.out is not _MISSING


def ex(*args, out):
    """A test whose expected output is known (checked against the reference)."""
    return Case(args, out)


def t(*args):
    """A test whose expected output is computed from the reference solution."""
    return Case(args)


def md(text):
    """Tiny markdown: `code`, **bold**, paragraphs, '- ' bullet lists."""
    text = html.escape(text.strip("\n"), quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    blocks = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.strip().split("\n")]
        if all(l.startswith("- ") for l in lines):
            blocks.append("<ul>" + "".join(f"<li>{l[2:]}</li>" for l in lines) + "</ul>")
        else:
            blocks.append("<p>" + " ".join(lines) + "</p>")
    return "".join(blocks)


def split_params(params):
    if not params.strip():
        return []
    parts = re.split(r",\s*(?=\w+\s*:)", params)
    return [[p.split(":", 1)[0].strip(), p.split(":", 1)[1].strip()] for p in parts]


def lc(slug, title, diff, params, ret, desc, tests, cmp="exact", inplace=None, examples=2, topic="", name=None):
    def deco(fn):
        REGISTRY.append(dict(track="lc", kind="fn", id=slug, title=title, diff=diff, topic=topic,
                             fn=name or fn.__name__, params=split_params(params), ret=ret, desc=desc,
                             tests=tests, cmp=cmp, inplace=inplace, examples=examples, ref=fn))
        return fn
    return deco


def design(slug, title, diff, methods, desc, tests, examples=1, topic=""):
    """methods: list of signature strings, first one is __init__."""
    def deco(cls):
        REGISTRY.append(dict(track="lc", kind="design", id=slug, title=title, diff=diff, topic=topic,
                             cls=cls.__name__, methods=methods, desc=desc, tests=tests,
                             cmp="exact", examples=examples, ref=cls))
        return cls
    return deco


# ---------- Verilog ----------

def parse_ports(s):
    ports = []
    for p in s.split(","):
        m = re.fullmatch(r"\s*(input|output)\s*(?:\[(\d+):0\])?\s*(\w+)\s*", p)
        assert m, f"bad port: {p}"
        ports.append(dict(name=m.group(3), dir="in" if m.group(1) == "input" else "out",
                          width=int(m.group(2)) + 1 if m.group(2) else 1))
    return ports


def vlog(slug, title, diff, ports, desc, solution, seq=False, gen=None, bias=None,
         cycles=40, seqs=3, vectors=None, topic=""):
    """Register a Verilog problem. The decorated object is the reference model:
    - combinational: a function inputs-dict -> outputs-dict
    - sequential: a class with step(inputs-dict) -> outputs-dict, called once per
      rising clock edge; outputs are what the circuit shows just after that edge.
    A None output value means "don't care"."""
    def deco(model):
        REGISTRY.append(dict(track="v", id=slug, title=title, diff=diff, topic=topic,
                             ports=parse_ports(ports), desc=desc, solution=solution, seq=seq,
                             gen=gen, bias=bias or {}, cycles=cycles, seqs=seqs,
                             vectors=vectors, model=model))
        return model
    return deco
