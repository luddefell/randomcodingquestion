// randomcodingquestion.com — page logic. Bundled by build.mjs into app.js.
import * as Finance from "./finance";
import { bits, esc, norm, py, table } from "./format";
import * as Python from "./python";
import * as Verilog from "./verilog";
import type { Monaco, MonacoEditor } from "./monaco";
import type { Json, Port, Problem, PyProblem, Track, VerilogProblem } from "./types";

const PROBLEMS = window.PROBLEMS;

function $<T extends HTMLElement = HTMLElement>(id: string): T {
  const el = document.getElementById(id);
  if (!el) throw new Error(`#${id} is missing from index.html`);
  return el as T;
}
const trackSelect = $<HTMLSelectElement>("track");
const diffSelect = $<HTMLSelectElement>("diff");
const checkButton = $<HTMLButtonElement>("check");
const complexityButton = $<HTMLButtonElement>("complexity");
const out = $("out");
const editorBox = $("editor");
const answerBox = $("answer"); // finance answers

const key = (p: Problem) => `${p.track}/${p.id}`;
const drafts = new Map<string, string>(); // code or answer per problem during this visit
let current: Problem;
let monaco: Monaco | null = null;
let editor: MonacoEditor | null = null;

const pyRet = (v: Json, p: PyProblem) => (p.spec.ret === "float" && typeof v === "number" && Number.isInteger(v) ? v.toFixed(1) : py(v));
const vIns = (p: VerilogProblem): Port[] => p.ports.filter(q => q.dir === "in" && q.name !== "clk");
const vOuts = (p: VerilogProblem): Port[] => p.ports.filter(q => q.dir === "out");
const widthOf = (ports: Port[], i: number) => ports[i]?.width ?? 1;

// ---------- problem display ----------

const DIFFICULTIES: [string, string][] = [["easy", "Easy"], ["medium", "Medium"], ["hard", "Hard"]];

/** The second dropdown filters by difficulty for code questions and by category for finance. */
function renderFilter(track: Track): void {
  if (diffSelect.dataset["track"] === track) return;
  const options: [string, string][] = [["all", "All"], ...(track === "fin" ? Finance.CATEGORIES : DIFFICULTIES)];
  diffSelect.replaceChildren(...options.map(([value, label]) => new Option(label, value)));
  diffSelect.setAttribute("aria-label", track === "fin" ? "Category" : "Difficulty");
  diffSelect.dataset["track"] = track;
}

function pool(): Problem[] {
  return PROBLEMS.filter(p => p.track === trackSelect.value && (diffSelect.value === "all" || p.diff === diffSelect.value));
}

function pythonInput(p: PyProblem, args: Json[]): string {
  return p.kind === "design" ? py(args[0]) : (p.spec.params ?? []).map(([n], i) => `${n} = ${py(args[i])}`).join(", ");
}

function examplesHTML(p: Problem): string {
  if (p.track === "fin") return "";
  if (p.track === "v") return verilogExamples(p);
  return p.tests.slice(0, p.examples).map(t => {
    if (p.kind === "design") {
      const [ops, args] = t.in;
      return `<pre>Input:  ${esc(py(ops))}\n        ${esc(py(args))}\nOutput: ${esc(py(t.out))}</pre>`;
    }
    return `<pre>Input:  ${esc(pythonInput(p, t.in))}\nOutput: ${esc(pyRet(t.out, p))}</pre>`;
  }).join("");
}

function verilogExamples(p: VerilogProblem): string {
  const ins = vIns(p), outs = vOuts(p);
  const head = [...ins.map(q => q.name), ...outs.map(q => q.name)];
  if (!p.seq) {
    const n = p.tests.length, k = Math.min(6, n);
    const picked = Array.from({ length: k }, (_, i) => p.tests[Math.floor(i * (n - 1) / Math.max(k - 1, 1))]);
    const rows = picked.flatMap(t => (t ? [[...t.in.map((v, i) => bits(v, widthOf(ins, i))),
                                            ...t.out.map((v, i) => bits(v, widthOf(outs, i)))]] : []));
    return `<p>Examples:</p><pre>${esc(table(head, rows, ins.length))}</pre>`;
  }
  const s = p.tests[0];
  if (!s) return "";
  // Show at least 12 edges, extended so that some output change is visible.
  const outAt = (c: number) => JSON.stringify(s.out[c]);
  let change = 3;
  while (change < s.out.length && outAt(change) === outAt(change - 1)) change++;
  const end = Math.min(Math.max(12, change + 4), 24, s.in.length);
  const rows = s.in.slice(0, end).map((inp, c) =>
    [c + 1, ...inp.map((v, i) => bits(v, widthOf(ins, i))), ...(s.out[c] ?? []).map((v, i) => bits(v, widthOf(outs, i)))]);
  return `<p>Example (inputs applied before each rising edge, outputs right after it):</p>` +
         `<pre>${esc(table(["edge", ...head], rows, ins.length + 1))}</pre>`;
}

function verilogStarter(p: VerilogProblem): string {
  const w = Math.max(...p.ports.map(q => (q.width > 1 ? `[${q.width - 1}:0] `.length : 0)));
  const lines = p.ports.map(q => {
    const range = q.width > 1 ? `[${q.width - 1}:0] ` : "";
    return `    ${q.dir === "in" ? "input " : "output"} logic ${range.padEnd(w)}${q.name}`;
  });
  return `module top_module (\n${lines.join(",\n")}\n);\n\n    \n\nendmodule\n`;
}

const starter = (p: Problem) => (p.track === "lc" ? p.starter : p.track === "v" ? verilogStarter(p) : "");

function languageFor(p: Problem): string {
  if (p.track === "lc" || !monaco) return "python";
  const ids = monaco.languages.getLanguages().map(l => l.id);
  return ids.includes("systemverilog") ? "systemverilog" : ids.includes("verilog") ? "verilog" : "plaintext";
}

function loadIntoEditor(p: Problem): void {
  if (!editor || !monaco || p.track === "fin") return;
  monaco.editor.setModelLanguage(editor.getModel(), languageFor(p));
  editor.setValue(drafts.get(key(p)) ?? starter(p));
  // Put the cursor on the first blank indented line, where the answer goes.
  const lines = editor.getValue().split("\n");
  let ln = lines.findIndex((l, i) => i > 0 && /^\s+$/.test(l));
  if (ln < 0) ln = lines.length - 1;
  editor.setPosition({ lineNumber: ln + 1, column: (lines[ln]?.length ?? 0) + 1 });
}

function setOutput(html: string, showing?: "complexity"): void {
  out.innerHTML = html;
  if (showing) out.dataset["showing"] = showing;
  else delete out.dataset["showing"];
}

/** Stretch the editor so its bottom edge sits 75% of the way down the window (never below 360px). */
function fitEditor(): void {
  const el = $("editor");
  const top = el.getBoundingClientRect().top + window.scrollY;
  el.style.height = Math.max(360, Math.round(window.innerHeight * 0.75 - top)) + "px";
}
window.addEventListener("resize", fitEditor);

function saveDraft(): void {
  if (!current) return;
  const draft = current.track === "fin" ? Finance.readDraft(answerBox) : editor?.getValue();
  if (draft !== undefined) drafts.set(key(current), draft);
}

function show(p: Problem): void {
  saveDraft();
  current = p;
  trackSelect.value = p.track;
  renderFilter(p.track);
  history.replaceState(null, "", "#" + key(p));
  const label = p.diff === "brainteaser" ? "brain teaser" : p.diff;
  $("title").textContent = `${p.title} (${label})`;
  $("desc").innerHTML = p.desc + examplesHTML(p);
  // Finance questions get an answer box instead of the code editor.
  editorBox.hidden = p.track === "fin";
  answerBox.hidden = p.track !== "fin";
  answerBox.innerHTML = p.track === "fin" ? Finance.answerHTML(p) : "";
  const draft = drafts.get(key(p));
  if (p.track === "fin" && draft !== undefined) Finance.restoreDraft(answerBox, draft);
  if (p.track !== "fin") fitEditor();
  setOutput("");
  complexityButton.hidden = p.track !== "lc"; // Big-O only applies to the Python questions
  if (p.track === "v") Verilog.start();
  loadIntoEditor(p);
}

function scramble(): void {
  const list = pool();
  let next: Problem | undefined;
  do { next = list[Math.floor(Math.random() * list.length)]; } while (list.length > 1 && next === current);
  if (next) show(next);
}

// ---------- checking ----------

async function checkPython(p: PyProblem, code: string, status: (s: string) => void): Promise<string> {
  status(Python.isReady() ? "Running..." : "Loading Python...");
  const res = await Python.run(code, p.spec, p.tests.map(t => t.in));
  if ("timeout" in res) return "Time limit exceeded (5s). Infinite loop?";
  if ("error" in res) return esc(res.error);
  let pass = 0;
  const lines = res.results.map((r, i) => {
    const t = p.tests[i];
    if (!t) return "";
    const got: Json = r.got === undefined ? null : (JSON.parse(r.got) as Json);
    const ok = r.error === undefined && JSON.stringify(norm(got, p.cmp)) === JSON.stringify(norm(t.out, p.cmp));
    if (ok) pass++;
    const input = pythonInput(p, t.in);
    const short = input.length > 140 ? input.slice(0, 140) + "…" : input;
    return ok
      ? `✓ ${esc(short)}`
      : `✗ ${esc(short)}\n    expected ${esc(pyRet(t.out, p))}\n    got      ${esc(r.error ?? pyRet(got, p))}`;
  });
  const total = p.tests.length;
  const head = pass === total ? `<b>Accepted.</b> ${pass}/${total} tests passed.` : `<b>${pass}/${total} tests passed.</b>`;
  const printed = res.stdout ? `\n\nstdout:\n${esc(res.stdout)}` : "";
  return head + "\n\n" + lines.join("\n") + printed;
}

async function checkVerilog(p: VerilogProblem, code: string, status: (s: string) => void): Promise<string> {
  status(Verilog.isReady() ? "Synthesizing..." : "Loading Yosys (first time only, ~12 MB)...");
  const res = await Verilog.compile(code);
  if ("error" in res) return esc(res.error);
  const ins = vIns(p), outs = vOuts(p), outNames = outs.map(q => q.name);
  const mkSim = () => new Verilog.Sim(res.netlist, p.ports);
  try { mkSim(); } catch (e) { return esc(e instanceof Error ? e.message : e); }
  const warn = res.warnings ? `\n\nyosys:\n${esc(res.warnings)}` : "";
  const same = (want: (number | null)[], got: number[]) => want.every((v, i) => v == null || v === got[i]);
  const inObj = (vals: number[]) => Object.fromEntries(ins.map((q, i) => [q.name, vals[i] ?? 0]));

  if (!p.seq) {
    const sim = mkSim(), fails: string[][] = [];
    let pass = 0;
    for (const t of p.tests) {
      const got = sim.comb(inObj(t.in), outNames);
      if (same(t.out, got)) pass++;
      else fails.push([...t.in.map((v, i) => bits(v, widthOf(ins, i))),
                       ...outs.map((q, i) => {
                         const want = t.out[i] ?? null, g = got[i] ?? 0;
                         return bits(want, q.width) + (want == null || want === g ? "" : " ≠ " + bits(g, q.width));
                       })]);
    }
    const total = p.tests.length;
    if (pass === total) return `<b>Accepted.</b> All ${total} input vectors match.${warn}`;
    const head = [...ins.map(q => q.name), ...outs.map(q => q.name)];
    return `<b>${pass}/${total} input vectors match.</b> First mismatches (expected ≠ got):\n` +
           `<pre>${esc(table(head, fails.slice(0, 8), ins.length))}</pre>${warn}`;
  }

  let pass = 0, report = "";
  p.tests.forEach((s, si) => {
    const sim = mkSim();
    const gots: number[][] = [];
    let bad = -1;
    for (let c = 0; c < s.in.length; c++) {
      const got = sim.cycle(inObj(s.in[c] ?? []), outNames);
      gots.push(got);
      if (!same(s.out[c] ?? [], got)) { bad = c; break; }
    }
    if (bad < 0) { pass++; return; }
    if (report) return; // show only the first failing sequence
    const from = Math.max(0, bad - 7);
    const rows: string[][] = [];
    for (let c = from; c <= bad; c++) {
      rows.push([(c === bad ? "✗ " : "  ") + (c + 1),
        ...(s.in[c] ?? []).map((v, i) => bits(v, widthOf(ins, i))),
        ...outs.map((q, i) => bits(s.out[c]?.[i] ?? null, q.width)),
        ...outs.map((q, i) => bits(gots[c]?.[i] ?? 0, q.width))]);
    }
    const head = ["edge", ...ins.map(q => q.name), ...outs.map(q => "exp " + q.name), ...outs.map(q => "got " + q.name)];
    report = `Test ${si + 1} fails after rising edge ${bad + 1}${from > 0 ? ` (showing edges ${from + 1}–${bad + 1})` : ""}:\n` +
             `<pre>${esc(table(head, rows, ins.length + 1))}</pre>`;
  });
  const total = p.tests.length, cycles = p.tests.reduce((a, s) => a + s.in.length, 0);
  if (pass === total) return `<b>Accepted.</b> ${total}/${total} test sequences (${cycles} clock cycles) match.${warn}`;
  return `<b>${pass}/${total} test sequences pass.</b> ${report}${warn}`;
}

async function check(): Promise<void> {
  if (checkButton.disabled) return;
  if (current.track === "fin") return setOutput(Finance.check(current, answerBox));
  if (!editor) return;
  checkButton.disabled = true;
  const p = current, code = editor.getValue();
  const status = (text: string) => { out.textContent = text; };
  setOutput("");
  let html: string;
  try {
    html = p.track === "lc" ? await checkPython(p, code, status) : p.track === "v" ? await checkVerilog(p, code, status) : "";
  } catch (e) {
    html = esc(e instanceof Error ? e.message : e);
  }
  checkButton.disabled = false;
  if (current === p) setOutput(html);
}

/** Complexity toggles: a second click hides it again. */
function toggleComplexity(): void {
  if (current.track !== "lc") return;
  if (out.dataset["showing"] === "complexity") return setOutput("");
  const c = current.complexity;
  setOutput(`<b>Target complexity:</b> Time ${esc(c.time)} · Space ${esc(c.space)}` + (c.note ? ` (${esc(c.note)})` : ""),
            "complexity");
}

// ---------- boot ----------

function fromHash(): Problem | undefined {
  const h = decodeURIComponent(location.hash.slice(1));
  const [t, id] = h.includes("/") ? h.split("/") : ["lc", h];
  return PROBLEMS.find(p => p.track === t && p.id === id);
}

$("scramble").onclick = scramble;
checkButton.onclick = () => void check();
complexityButton.onclick = toggleComplexity;
trackSelect.onchange = () => { renderFilter(trackSelect.value as Track); scramble(); };
// Enter in a one-line answer field (or Ctrl/Cmd+Enter anywhere) checks the answer.
answerBox.addEventListener("keydown", e => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey || e.target instanceof HTMLInputElement)) { e.preventDefault(); void check(); }
});
diffSelect.onchange = () => { if (!pool().includes(current)) scramble(); };
window.addEventListener("hashchange", () => { const p = fromHash(); if (p && p !== current) show(p); });

renderFilter(trackSelect.value as Track);
const initial = fromHash();
if (initial) show(initial);
else scramble();

/** Called from index.html once the Monaco editor has loaded. */
export function attachEditor(m: Monaco): void {
  monaco = m;
  editor = m.editor.create($("editor"), {
    value: starter(current), language: languageFor(current),
    minimap: { enabled: false }, scrollBeyondLastLine: false, automaticLayout: true,
    tabSize: 4, insertSpaces: true,
  });
  editor.addCommand(m.KeyMod.CtrlCmd | m.KeyCode.Enter, () => void check());
  loadIntoEditor(current);
}
