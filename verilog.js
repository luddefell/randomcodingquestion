// Verilog support: Yosys (WebAssembly, in a worker) turns the design into a
// netlist of single-bit gates and flip-flops, which Sim below simulates.
(function () {
  const YOSYS = "https://cdn.jsdelivr.net/npm/@yowasp/yosys@0.68.1207/gen/bundle.js";
  const SCRIPT = [
    "read_verilog -sv top_module.v", "hierarchy -check -top top_module", "proc", "flatten",
    "memory", "opt_clean", "async2sync", "dffunmap", "techmap", "opt_clean",
    "setundef -zero -undriven", "check -assert", "write_json out.json"
  ].join("; ");

  const WORKER_SRC = `
    import { runYosys } from "${YOSYS}";
    const dec = new TextDecoder();
    // Warm up: downloads and compiles the WebAssembly once.
    runYosys(["-V"], {}, { stdout: null, stderr: null })
      .then(() => postMessage({ ready: true }), e => postMessage({ fatal: String(e) }));
    onmessage = async e => {
      let log = "";
      const sink = b => { if (b) log += dec.decode(b); };
      try {
        const out = await runYosys(["-q", "-p", ${JSON.stringify(SCRIPT)}], { "top_module.v": e.data.code },
                                   { stdout: sink, stderr: sink });
        postMessage({ json: out["out.json"], log });
      } catch (err) {
        postMessage({ failed: true, log });
      }
    };`;

  let worker = null, ready = false, readyWaiters = [];

  function start() {
    if (worker) return;
    ready = false;
    worker = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: "text/javascript" })), { type: "module" });
    worker.addEventListener("message", e => {
      if (e.data.ready) { ready = true; readyWaiters.splice(0).forEach(f => f()); }
    });
  }

  function restart() {
    if (worker) worker.terminate();
    worker = null;
    start();
  }

  const whenReady = () => ready ? Promise.resolve() : new Promise(r => readyWaiters.push(r));

  // Clean up Yosys output for display.
  function tidyLog(log) {
    return log.split("\n")
      .filter(l => l.trim() && !/^\s*(End of script|Yosys \d|Exited)/.test(l))
      .map(l => l.replace(/\$auto\$[^ ]*\s*/g, "").replace(/\\(?=\w)/g, ""))
      .join("\n").trim();
  }

  // Compile Verilog to a netlist. Resolves to {netlist, warnings} or {error}.
  async function compile(code, timeoutMs = 20000) {
    start();
    await whenReady();
    const w = worker;
    return new Promise(resolve => {
      const timer = setTimeout(() => { restart(); resolve({ error: "Synthesis timed out." }); }, timeoutMs);
      w.onmessage = e => {
        if (e.data.ready || e.data.fatal) return;
        clearTimeout(timer);
        const log = tidyLog(e.data.log || "");
        if (e.data.failed) return resolve({ error: log || "Yosys failed." });
        if (/Latch inferred/i.test(log)) {
          return resolve({ error: "A latch was inferred. Make sure every output of a combinational block " +
                                  "is assigned on every path (add a default or an else).\n\n" + log });
        }
        resolve({ netlist: JSON.parse(e.data.json).modules.top_module, warnings: log });
      };
      w.postMessage({ code });
    });
  }

  // ---------- gate-level simulator ----------
  const GATES = {
    $_BUF_: (a) => a, $_NOT_: (a) => a ^ 1,
    $_AND_: (a, b) => a & b, $_NAND_: (a, b) => (a & b) ^ 1,
    $_OR_: (a, b) => a | b, $_NOR_: (a, b) => (a | b) ^ 1,
    $_XOR_: (a, b) => a ^ b, $_XNOR_: (a, b) => (a ^ b) ^ 1,
    $_ANDNOT_: (a, b) => a & (b ^ 1), $_ORNOT_: (a, b) => a | (b ^ 1),
    $_MUX_: (a, b, s) => s ? b : a, $_NMUX_: (a, b, s) => (s ? b : a) ^ 1,
  };

  class Sim {
    constructor(netlist, ports) {
      const bitId = b => (b === "1" ? 1 : typeof b === "number" ? b : 0); // "0", "x", "z" -> 0
      let max = 1;
      const seeBits = bits => bits.forEach(b => { if (typeof b === "number") max = Math.max(max, b); });
      Object.values(netlist.ports).forEach(p => seeBits(p.bits));
      Object.values(netlist.cells).forEach(c => Object.values(c.connections).forEach(seeBits));
      this.v = new Uint8Array(max + 1);
      this.v[1] = 1;

      // Ports: check names, directions and widths against the problem.
      this.ports = {};
      for (const p of ports) {
        const np = netlist.ports[p.name];
        if (!np) throw new Error(`Port '${p.name}' is missing from top_module.`);
        const dir = np.direction === "input" ? "in" : np.direction === "output" ? "out" : np.direction;
        if (dir !== p.dir) throw new Error(`Port '${p.name}' should be an ${p.dir === "in" ? "input" : "output"}.`);
        if (np.bits.length !== p.width) throw new Error(`Port '${p.name}' should be ${p.width} bit${p.width > 1 ? "s" : ""} wide, not ${np.bits.length}.`);
        this.ports[p.name] = np.bits.map(bitId);
      }
      for (const name of Object.keys(netlist.ports))
        if (!ports.some(p => p.name === name)) throw new Error(`Unexpected port '${name}' on top_module.`);
      const clk = this.ports.clk ? this.ports.clk[0] : -1;

      // Cells
      const comb = [], driver = new Map();
      this.ffs = [];
      for (const c of Object.values(netlist.cells)) {
        const k = c.connections, t = c.type;
        if (t === "$scopeinfo") continue;
        if (t === "$_DFF_P_" || t === "$_DFF_N_") {
          if (bitId(k.C[0]) !== clk) throw new Error("Only the clk input may be used as a clock.");
          this.ffs.push({ d: bitId(k.D[0]), q: bitId(k.Q[0]), neg: t === "$_DFF_N_" });
        } else if (t === "$_FF_" || t.startsWith("$_DLATCH") || t.startsWith("$_SR")) {
          throw new Error("A latch was inferred. Make sure every output of a combinational block is assigned on every path.");
        } else if (GATES[t]) {
          const cell = { f: GATES[t], a: bitId((k.A || [0])[0]), b: bitId((k.B || [0])[0]), s: bitId((k.S || [0])[0]), y: bitId(k.Y[0]) };
          driver.set(cell.y, cell);
          comb.push(cell);
        } else {
          throw new Error(`Unsupported construct (cell type ${t}).`);
        }
      }

      // Topological order of the combinational cells.
      this.order = [];
      const state = new Map(); // 1 = visiting, 2 = done
      const visit = cell => {
        const st = state.get(cell);
        if (st === 2) return;
        if (st === 1) throw new Error("Combinational loop detected.");
        state.set(cell, 1);
        for (const b of [cell.a, cell.b, cell.s]) { const d = driver.get(b); if (d) visit(d); }
        state.set(cell, 2);
        this.order.push(cell);
      };
      comb.forEach(visit);
    }

    set(name, value) {
      this.ports[name].forEach((b, i) => { if (b > 1) this.v[b] = (value >>> i) & 1; });
    }

    get(name) {
      return this.ports[name].reduce((acc, b, i) => acc + this.v[b] * 2 ** i, 0);
    }

    eval() {
      const v = this.v;
      for (const c of this.order) v[c.y] = c.f(v[c.a], v[c.b], v[c.s]);
    }

    edge(neg) {
      const next = this.ffs.map(f => (f.neg === neg ? this.v[f.d] : this.v[f.q]));
      this.ffs.forEach((f, i) => { this.v[f.q] = next[i]; });
      this.eval();
    }

    // One clock cycle: apply inputs, rising edge, sample, falling edge.
    cycle(inputs, outNames) {
      for (const [k, val] of Object.entries(inputs)) this.set(k, val);
      if (this.ports.clk) this.set("clk", 0);
      this.eval();
      this.edge(false);
      const out = outNames.map(n => this.get(n));
      this.edge(true);
      return out;
    }

    comb(inputs, outNames) {
      for (const [k, val] of Object.entries(inputs)) this.set(k, val);
      this.eval();
      return outNames.map(n => this.get(n));
    }
  }

  window.Verilog = { start, compile, Sim, isReady: () => ready };
})();
