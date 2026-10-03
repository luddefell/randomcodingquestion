# randomcodingquestion.com

A random coding question on a plain HTML page: pick Python or Verilog and a difficulty, write your answer,
and press **Check**. **Scramble** gives a new question, **Complexity** shows the target Big-O.
Everything runs in the browser:

- **Python** track (144 questions, NeetCode 150-style): answers run in [Pyodide](https://pyodide.org).
- **Verilog** track (42 questions): your design is synthesized with [Yosys](https://yosyshq.net/yosys/)
  (WebAssembly build from [YoWASP](https://yowasp.org)) and simulated gate by gate against a reference model.
- **Finance** track (86 questions): technical, markets and brain-teaser questions, written in our own words.
  Number, multiple-choice and expression questions are checked exactly; open questions show the key points
  of a strong answer.

## Layout

| Path | What it is |
| --- | --- |
| `index.html`, `about.html` | The pages |
| `app.js`, `*.worker.js` | **Built** from `src/` by `npm run build`. Don't edit by hand, but do commit them (GitHub Pages serves them) |
| `problems.js` | **Built** from `build/` by `npm run problems`. Don't edit by hand |
| `harness.py` | Python test harness (used by the site and by the question build) |
| `src/main.ts` | Page logic: Scramble, Check, Complexity |
| `src/python.ts`, `src/workers/python.worker.ts` | Runs Python answers in a background thread |
| `src/verilog.ts`, `src/workers/yosys.worker.ts` | Yosys synthesis and the gate-level simulator |
| `src/finance.ts` | Finance answer boxes and checking |
| `build/` | Question sources (Python) and their build script |

## Develop

Needs Node 18+ and Python 3.

```bash
npm install
```

```bash
npm run build
```

`npm run build` type-checks everything (strict TypeScript), bundles `src/` into `app.js` and the worker files with esbuild,
and stamps a version on the script links in `index.html` so browsers never mix old and new files.

To preview locally:

```bash
npm run serve
```

Then open http://localhost:8123.

## Deploy

GitHub Pages publishes the root of the `main` branch (`.nojekyll` makes it serve files as-is).
Run `npm run build`, commit the rebuilt files, and push.

`build/solutions.json` contains reference Verilog solutions and is git-ignored, so it isn't published.

## Add or change questions

Questions live in `build/lc_*.py` (Python) and `build/verilog.py`. Each one is a reference solution plus test inputs:

```python
@lc("two-sum", "Two Sum", "easy", "nums: List[int], target: int", "List[int]", cmp="any", desc="""...""",
    tests=[ex([2, 7, 11, 15], 9, out=[0, 1]), t([3, 3], 6)])
def twoSum(nums, target): ...
```

`ex(...)` tests have a known answer that the build checks the reference against; `t(...)` tests get their answer
from the reference. Python questions also need a target complexity in `build/complexity.py`. Verilog questions
take a Python model (a function for combinational logic, a class with `step()` for clocked logic) and a
reference Verilog solution. Then regenerate the data and rebuild:

```bash
npm run problems
```

```bash
npm run build
```

### Finance questions

Finance questions live in `build/finance.py`. Each one is written in our own words and lists the report rows it came
from (`src="J18 J60"`); `build/finance_sources.json` lists only the row ids, so the build can check coverage
without the original reports. The build refuses to finish if:

- a question cites an unknown row, or a report row isn't used by any question (unless listed in `EXCLUDED` with a reason)
- two questions are near-duplicates
- a question contains a banned word such as a person's name, a school, a firm name or a link (`BANNED` in `build/build.py`)
- a numeric answer doesn't match what its `solve` function computes, a choice answer isn't one of the options,
  or an expression answer doesn't use each number once and hit the target
- an open question has fewer than 3 key points, or a numeric/choice question has no worked solution

