# randomcodingquestion.com

A random coding question on a plain HTML page: pick Python or Verilog and a difficulty, write your answer,
and press **Check**. **Scramble** gives a new question. Everything runs in the browser:

- **LeetCode** track (144 problems, NeetCode 150-style): Python runs in [Pyodide](https://pyodide.org).
- **Verilog** track (42 problems): your design is synthesized with [Yosys](https://yosyshq.net/yosys/) (WebAssembly build from [YoWASP](https://yowasp.org)) and simulated gate by gate against a reference model.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Page and styles |
| `app.js` | UI, Python runner, Verilog checking |
| `verilog.js` | Yosys worker and gate-level simulator |
| `harness.py` | Python test harness (loaded by the site and by the build) |
| `problems.js` | **Generated** problem data. Don't edit by hand |
| `build/` | Problem sources and the build script (not needed on the server) |

## Deploy

It's a static site. Upload `index.html`, `about.html`, `app.js`, `verilog.js`, `harness.py`, and `problems.js` to any static host
(GitHub Pages, Netlify, Cloudflare Pages, Vercel). It must be served over http(s), not opened as a local file.
To preview locally:

```bash
python3 -m http.server 8123
```

`build/solutions.json` contains reference Verilog solutions, so leave `build/` off the server if you don't want answers public.

## Add or change problems

Problems live in `build/lc_*.py` (LeetCode) and `build/verilog.py`. Each one is a reference solution plus test inputs:

```python
@lc("two-sum", "Two Sum", "easy", "nums: List[int], target: int", "List[int]", cmp="any", desc="""...""",
    tests=[ex([2, 7, 11, 15], 9, out=[0, 1]), t([3, 3], 6)])
def twoSum(nums, target): ...
```

`ex(...)` tests have a known answer that the build checks the reference against; `t(...)` tests get their answer
from the reference. Verilog problems take a Python model (a function for combinational logic, a class with
`step()` for clocked logic) and a reference Verilog solution. Then regenerate:

```bash
python3 build/build.py
```
