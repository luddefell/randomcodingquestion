// Runs Python (Pyodide) off the main thread so a slow answer can't freeze the page.
import type { Json, PyResponse, PySpec } from "../types";

interface Pyodide {
  FS: { writeFile(path: string, data: string): void };
  runPython(code: string): unknown;
}
declare function loadPyodide(): Promise<Pyodide>;

importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

const post = (msg: PyResponse) => postMessage(msg);

const ready = (async () => {
  const [py, harness] = await Promise.all([
    loadPyodide(),
    fetch(`harness.py?v=${__VERSION__}`).then(r => r.text()),
  ]);
  py.FS.writeFile("harness.py", harness);
  py.runPython("import harness");
  post({ ready: true });
  return py;
})();

onmessage = async (e: MessageEvent<{ code: string; spec: PySpec; cases: Json[][] }>) => {
  const py = await ready;
  const { code, spec, cases } = e.data;
  try {
    const run = py.runPython("harness.run") as (code: string, spec: string, cases: string) => string;
    post(JSON.parse(run(code, JSON.stringify(spec), JSON.stringify(cases))) as PyResponse);
  } catch (err) {
    post({ error: String(err) });
  }
};
