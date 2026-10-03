// Small text-formatting helpers.
import type { Expected, Json } from "./types";

export const esc = (s: unknown): string =>
  String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c] as string);

/** A JSON value printed the way Python would print it. */
export const py = (v: Json | undefined): string =>
  v === true ? "True" : v === false ? "False" : v == null ? "None" :
  Array.isArray(v) ? "[" + v.map(py).join(", ") + "]" :
  typeof v === "string" ? JSON.stringify(v) : String(v);

/** Verilog values: binary up to 8 bits, hex above, "x" for don't care. */
export const bits = (v: Expected, width: number): string =>
  v == null ? "x" : width === 1 ? String(v) : width <= 8 ? v.toString(2).padStart(width, "0") :
  "0x" + v.toString(16).padStart(Math.ceil(width / 4), "0");

/** Plain-text table with padded columns and a divider before column `sep`. */
export function table(head: string[], rows: (string | number)[][], sep: number): string {
  const all = [head, ...rows];
  const widths = head.map((_, i) => Math.max(...all.map(r => String(r[i]).length)));
  const line = (r: (string | number)[]) =>
    r.map((c, i) => (i === sep ? "│ " : "") + String(c).padEnd(widths[i] ?? 0)).join("  ").trimEnd();
  return all.map(line).join("\n");
}

/** Normalise answers whose order doesn't matter, so they compare equal. */
export function norm(v: Json, cmp: "exact" | "any" | "anyDeep"): Json {
  const key = (x: Json) => JSON.stringify(x);
  const sort = (a: Json[]) => [...a].sort((x, y) => (key(x) < key(y) ? -1 : key(x) > key(y) ? 1 : 0));
  if (cmp === "any" && Array.isArray(v)) return sort(v);
  if (cmp === "anyDeep" && Array.isArray(v)) return sort(v.map(x => (Array.isArray(x) ? sort(x) : x)));
  return v;
}
