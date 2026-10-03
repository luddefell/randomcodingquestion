// Verilog support: Yosys (in workers/yosys.worker.ts) turns the design into a
// netlist of single-bit gates and flip-flops, which Sim below simulates.
import type { Bit, Netlist, Port, YosysResponse } from "./types";

// ---------- Yosys worker ----------

let worker: Worker | null = null;
let ready = false;
let waiters: (() => void)[] = [];

/** Start downloading Yosys (about 12 MB) if it isn't already. */
export function start(): void {
  if (worker) return;
  ready = false;
  worker = new Worker(`yosys.worker.js?v=${__VERSION__}`, { type: "module" });
  worker.addEventListener("message", (e: MessageEvent<YosysResponse>) => {
    if ("ready" in e.data) {
      ready = true;
      waiters.splice(0).forEach(f => f());
    }
  });
}

function restart(): void {
  worker?.terminate();
  worker = null;
  start();
}

export const isReady = (): boolean => ready;

/** Clean up Yosys output for display. */
function tidyLog(log: string): string {
  return log.split("\n")
    .filter(l => l.trim() && !/^\s*(End of script|Yosys \d|Exited)/.test(l))
    .map(l => l.replace(/\$auto\$[^ ]*\s*/g, "").replace(/\\(?=\w)/g, ""))
    .join("\n").trim();
}

export type CompileResult = { netlist: Netlist; warnings: string } | { error: string };

/** Synthesize Verilog into a gate-level netlist. */
export async function compile(code: string, timeoutMs = 20000): Promise<CompileResult> {
  start();
  if (!ready) await new Promise<void>(r => waiters.push(r));
  const w = worker as Worker;
  return new Promise(resolve => {
    const timer = setTimeout(() => { restart(); resolve({ error: "Synthesis timed out." }); }, timeoutMs);
    w.onmessage = (e: MessageEvent<YosysResponse>) => {
      const msg = e.data;
      if ("ready" in msg || "fatal" in msg) return;
      clearTimeout(timer);
      const log = tidyLog(msg.log);
      if ("failed" in msg) return resolve({ error: log || "Yosys failed." });
      if (/Latch inferred/i.test(log)) {
        return resolve({ error: "A latch was inferred. Make sure every output of a combinational block " +
                                "is assigned on every path (add a default or an else).\n\n" + log });
      }
      const top = (JSON.parse(msg.json) as { modules: Record<string, Netlist> }).modules["top_module"];
      resolve(top ? { netlist: top, warnings: log } : { error: "Module top_module not found." });
    };
    w.postMessage({ code });
  });
}

// ---------- gate-level simulator ----------

type Gate = (a: number, b: number, s: number) => number;
const GATES: Record<string, Gate> = {
  $_BUF_: a => a, $_NOT_: a => a ^ 1,
  $_AND_: (a, b) => a & b, $_NAND_: (a, b) => (a & b) ^ 1,
  $_OR_: (a, b) => a | b, $_NOR_: (a, b) => (a | b) ^ 1,
  $_XOR_: (a, b) => a ^ b, $_XNOR_: (a, b) => (a ^ b) ^ 1,
  $_ANDNOT_: (a, b) => a & (b ^ 1), $_ORNOT_: (a, b) => a | (b ^ 1),
  $_MUX_: (a, b, s) => (s ? b : a), $_NMUX_: (a, b, s) => (s ? b : a) ^ 1,
};

interface Cell { f: Gate; a: number; b: number; s: number; y: number }
interface FlipFlop { d: number; q: number; neg: boolean }

/** Net ids: 0 and 1 are the constants; "x" and "z" are treated as 0. */
const bitId = (b: Bit | undefined): number => (b === "1" ? 1 : typeof b === "number" ? b : 0);

export class Sim {
  private v: Uint8Array;
  private ports: Record<string, number[]> = {};
  private ffs: FlipFlop[] = [];
  private order: Cell[] = [];

  constructor(netlist: Netlist, ports: Port[]) {
    let max = 1;
    const seeBits = (bs: Bit[]) => bs.forEach(b => { if (typeof b === "number") max = Math.max(max, b); });
    Object.values(netlist.ports).forEach(p => seeBits(p.bits));
    Object.values(netlist.cells).forEach(c => Object.values(c.connections).forEach(seeBits));
    this.v = new Uint8Array(max + 1);
    this.v[1] = 1;

    // Ports: check names, directions and widths against the problem.
    for (const p of ports) {
      const np = netlist.ports[p.name];
      if (!np) throw new Error(`Port '${p.name}' is missing from top_module.`);
      const dir = np.direction === "input" ? "in" : np.direction === "output" ? "out" : np.direction;
      if (dir !== p.dir) throw new Error(`Port '${p.name}' should be an ${p.dir === "in" ? "input" : "output"}.`);
      if (np.bits.length !== p.width) {
        throw new Error(`Port '${p.name}' should be ${p.width} bit${p.width > 1 ? "s" : ""} wide, not ${np.bits.length}.`);
      }
      this.ports[p.name] = np.bits.map(bitId);
    }
    for (const name of Object.keys(netlist.ports)) {
      if (!ports.some(p => p.name === name)) throw new Error(`Unexpected port '${name}' on top_module.`);
    }
    const clk = this.ports["clk"]?.[0] ?? -1;

    // Cells
    const comb: Cell[] = [];
    const driver = new Map<number, Cell>();
    for (const c of Object.values(netlist.cells)) {
      const k = c.connections, t = c.type;
      const pin = (name: string) => bitId(k[name]?.[0]);
      if (t === "$scopeinfo") continue;
      if (t === "$_DFF_P_" || t === "$_DFF_N_") {
        if (pin("C") !== clk) throw new Error("Only the clk input may be used as a clock.");
        this.ffs.push({ d: pin("D"), q: pin("Q"), neg: t === "$_DFF_N_" });
      } else if (t === "$_FF_" || t.startsWith("$_DLATCH") || t.startsWith("$_SR")) {
        throw new Error("A latch was inferred. Make sure every output of a combinational block is assigned on every path.");
      } else if (GATES[t]) {
        const cell: Cell = { f: GATES[t], a: pin("A"), b: pin("B"), s: pin("S"), y: pin("Y") };
        driver.set(cell.y, cell);
        comb.push(cell);
      } else {
        throw new Error(`Unsupported construct (cell type ${t}).`);
      }
    }

    // Topological order of the combinational cells.
    const state = new Map<Cell, 1 | 2>(); // 1 = visiting, 2 = done
    const visit = (cell: Cell): void => {
      const st = state.get(cell);
      if (st === 2) return;
      if (st === 1) throw new Error("Combinational loop detected.");
      state.set(cell, 1);
      for (const b of [cell.a, cell.b, cell.s]) {
        const d = driver.get(b);
        if (d) visit(d);
      }
      state.set(cell, 2);
      this.order.push(cell);
    };
    comb.forEach(visit);
  }

  private set(name: string, value: number): void {
    (this.ports[name] ?? []).forEach((b, i) => { if (b > 1) this.v[b] = (value >>> i) & 1; });
  }

  private get(name: string): number {
    return (this.ports[name] ?? []).reduce((acc, b, i) => acc + (this.v[b] ?? 0) * 2 ** i, 0);
  }

  private eval(): void {
    const v = this.v;
    for (const c of this.order) v[c.y] = c.f(v[c.a] ?? 0, v[c.b] ?? 0, v[c.s] ?? 0);
  }

  private edge(neg: boolean): void {
    const next = this.ffs.map(f => (f.neg === neg ? this.v[f.d] : this.v[f.q]) ?? 0);
    this.ffs.forEach((f, i) => { this.v[f.q] = next[i] ?? 0; });
    this.eval();
  }

  /** One clock cycle: apply inputs, rising edge, sample outputs, falling edge. */
  cycle(inputs: Record<string, number>, outNames: string[]): number[] {
    for (const [k, val] of Object.entries(inputs)) this.set(k, val);
    if (this.ports["clk"]) this.set("clk", 0);
    this.eval();
    this.edge(false);
    const out = outNames.map(n => this.get(n));
    this.edge(true);
    return out;
  }

  /** Combinational logic: apply inputs and read the outputs. */
  comb(inputs: Record<string, number>, outNames: string[]): number[] {
    for (const [k, val] of Object.entries(inputs)) this.set(k, val);
    this.eval();
    return outNames.map(n => this.get(n));
  }
}
