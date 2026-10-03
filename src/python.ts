// Main-thread side of the Python runner (see workers/python.worker.ts).
import type { Json, PyResponse, PySpec } from "./types";

export type PyRunResult = Exclude<PyResponse, { ready: true }> | { timeout: true };

let worker: Worker;
let ready = false;
let waiters: (() => void)[] = [];

function start(): void {
  ready = false;
  worker = new Worker(`python.worker.js?v=${__VERSION__}`);
  worker.addEventListener("message", (e: MessageEvent<PyResponse>) => {
    if ("ready" in e.data) {
      ready = true;
      waiters.splice(0).forEach(f => f());
    }
  });
}
start(); // begin loading Python right away

export const isReady = (): boolean => ready;

/** Run the user's code on every test case. A runaway answer is killed after `timeoutMs`. */
export async function run(code: string, spec: PySpec, cases: Json[][], timeoutMs = 5000): Promise<PyRunResult> {
  if (!ready) await new Promise<void>(r => waiters.push(r));
  const w = worker;
  return new Promise(resolve => {
    const timer = setTimeout(() => { w.terminate(); start(); resolve({ timeout: true }); }, timeoutMs);
    w.onmessage = (e: MessageEvent<PyResponse>) => {
      if ("ready" in e.data) return;
      clearTimeout(timer);
      resolve(e.data);
    };
    w.postMessage({ code, spec, cases });
  });
}
