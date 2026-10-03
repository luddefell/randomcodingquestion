// Runs Yosys (WebAssembly) off the main thread. It turns the Verilog into a
// netlist of single-bit gates and flip-flops, which src/verilog.ts simulates.
import type { YosysResponse } from "../types";

type Sink = ((bytes: Uint8Array | null) => void) | null;
type RunYosys = (args: string[], files: Record<string, string>,
                 options: { stdout: Sink; stderr: Sink }) => Promise<Record<string, unknown>>;

const YOSYS = "https://cdn.jsdelivr.net/npm/@yowasp/yosys@0.68.1207/gen/bundle.js";
const SCRIPT = [
  "read_verilog -sv top_module.v", "hierarchy -check -top top_module", "proc", "flatten",
  "memory", "opt_clean", "async2sync", "dffunmap", "techmap", "opt_clean",
  "setundef -zero -undriven", "check -assert", "write_json out.json",
].join("; ");

const post = (msg: YosysResponse) => postMessage(msg);
const yosys = import(YOSYS) as Promise<{ runYosys: RunYosys }>;

// Warm up: downloads and compiles the WebAssembly once.
yosys
  .then(({ runYosys }) => runYosys(["-V"], {}, { stdout: null, stderr: null }))
  .then(() => post({ ready: true }), (e: unknown) => post({ fatal: String(e) }));

onmessage = async (e: MessageEvent<{ code: string }>) => {
  const { runYosys } = await yosys;
  const dec = new TextDecoder();
  let log = "";
  const sink: Sink = b => { if (b) log += dec.decode(b); };
  try {
    const out = await runYosys(["-q", "-p", SCRIPT], { "top_module.v": e.data.code }, { stdout: sink, stderr: sink });
    post({ json: String(out["out.json"]), log });
  } catch {
    post({ failed: true, log });
  }
};
