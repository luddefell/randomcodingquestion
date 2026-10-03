// Finance questions: the answer box for each kind of question, and checking.
// There's no code to run: numbers, choices and expressions are checked exactly;
// open questions show the key points a strong answer covers.
import { esc } from "./format";
import type { FinanceAnswer, FinanceProblem } from "./types";

export const CATEGORIES: [value: FinanceProblem["diff"], label: string][] = [
  ["technical", "Technical"],
  ["markets", "Markets"],
  ["brainteaser", "Brain teasers"],
];

const UNIT_HINTS: Record<string, string> = { $: "in dollars", $m: "in $ millions", "%": "in %", x: "as a multiple" };

export function answerHTML(p: FinanceProblem): string {
  const a = p.answer;
  switch (a.type) {
    case "open":
      return `<p><textarea id="fin-answer" rows="8" cols="80" aria-label="Your answer"></textarea></p>`;
    case "number":
      return `<p><label for="fin-answer">Your answer${a.unit ? ` (${UNIT_HINTS[a.unit] ?? ""})` : ""}:</label> ` +
             `<input id="fin-answer" size="16" inputmode="decimal" autocomplete="off"></p>`;
    case "choice":
      return `<fieldset><legend>Your answer</legend>` +
             a.options.map((o, i) => `<label><input type="radio" name="fin-choice" value="${i}"> ${esc(o)}</label><br>`).join("") +
             `</fieldset>`;
    case "expr":
      return `<p><label for="fin-answer">Your expression:</label> ` +
             `<input id="fin-answer" size="24" autocomplete="off" spellcheck="false"></p>`;
  }
}

/** What the user has entered, so it can be restored when they come back to the question. */
export function readDraft(root: HTMLElement): string | undefined {
  const radios = [...root.querySelectorAll<HTMLInputElement>("input[type=radio]")];
  if (radios.length) return radios.find(r => r.checked)?.value;
  return root.querySelector<HTMLInputElement | HTMLTextAreaElement>("#fin-answer")?.value;
}

export function restoreDraft(root: HTMLElement, draft: string): void {
  const radio = root.querySelector<HTMLInputElement>(`input[type=radio][value="${CSS.escape(draft)}"]`);
  if (radio) { radio.checked = true; return; }
  const field = root.querySelector<HTMLInputElement | HTMLTextAreaElement>("#fin-answer");
  if (field) field.value = draft;
}

// ---------- numbers ----------

/** Parse "24.6", "24.6%", "$2,500", "-10", "2/15", "5x", "$5,000m". Percentages come back as fractions. */
export function parseNumber(raw: string): number {
  let s = raw.trim().toLowerCase().replace(/[$,\s]/g, "").replace(/(usd|dollars|million|mm|m|x)$/, "").replace("−", "-");
  const percent = s.endsWith("%");
  if (percent) s = s.slice(0, -1);
  const frac = /^(-?\d*\.?\d+)\/(\d*\.?\d+)$/.exec(s);
  const v = frac ? Number(frac[1]) / Number(frac[2]) : /^-?\d*\.?\d+(e-?\d+)?$/.test(s) ? Number(s) : NaN;
  return percent ? v / 100 : v;
}

type NumberAnswer = Extract<FinanceAnswer, { type: "number" }>;

/** Accept the answer whether a percentage is typed as 24.6, 24.6% or 0.246. */
export function numberMatches(entered: number, a: NumberAnswer): boolean {
  const close = (v: number) => Math.abs(v - a.value) <= a.tol * Math.abs(a.value) + 1e-9;
  if (a.unit === "%") return close(entered) || close(entered * 100);
  if (a.unit === "") return close(entered) || close(entered / 100);
  return close(entered);
}

export function formatNumber(a: NumberAnswer): string {
  const n = a.value;
  const plain = (v: number, digits = 2) => v.toLocaleString("en-US", { maximumFractionDigits: digits });
  switch (a.unit) {
    case "$": return (n < 0 ? "−$" : "$") + plain(Math.abs(n));
    case "$m": return "$" + plain(n) + "m";
    case "%": return plain(n) + "%";
    case "x": return n.toFixed(1) + "x";
    default: return `${plain(n, 3)} (${plain(n * 100, 1)}%)`;
  }
}

// ---------- expressions ----------

/** Returns null if `raw` uses each number exactly once and equals the target, else what's wrong. */
export function exprProblem(raw: string, numbers: number[], target: number): string | null {
  const s = raw.replace(/×/g, "*").replace(/÷/g, "/").replace(/−/g, "-");
  if (!/^[0-9+\-*/(). ]+$/.test(s)) return "Use only the numbers, + − × ÷ and parentheses.";
  const used = (s.match(/\d+/g) ?? []).map(Number).sort((x, y) => x - y);
  if (JSON.stringify(used) !== JSON.stringify([...numbers].sort((x, y) => x - y))) {
    return `Use each of ${numbers.join(", ")} exactly once.`;
  }
  let value: unknown;
  try {
    // Safe to evaluate: the check above allows only digits, operators, parentheses and dots.
    value = Function(`"use strict"; return (${s});`)();
  } catch {
    return "That expression isn't valid.";
  }
  if (typeof value !== "number" || !Number.isFinite(value)) return "That expression doesn't give a number.";
  return Math.abs(value - target) < 1e-9 ? null : `That equals ${+value.toFixed(4)}, not ${target}.`;
}

// ---------- checking ----------

const list = (items: string[], tag: "ul" | "ol") => `<${tag}>${items.map(i => `<li>${esc(i)}</li>`).join("")}</${tag}>`;

/** Returns HTML for the output area. */
export function check(p: FinanceProblem, root: HTMLElement): string {
  const a = p.answer;
  const draft = readDraft(root)?.trim() ?? "";
  const solution = `<p>How to get there:</p>${list(p.explain, "ol")}`;
  switch (a.type) {
    case "open":
      return `<b>Key points a strong answer covers:</b>${list(p.key, "ul")}`;
    case "number": {
      if (!draft) return "Enter a number first.";
      const v = parseNumber(draft);
      if (Number.isNaN(v)) return `Couldn't read "${esc(draft)}" as a number. Try something like 24.6, 2,500 or 2/15.`;
      return (numberMatches(v, a) ? "<b>Correct.</b>" : `<b>Not quite.</b> The answer is ${esc(formatNumber(a))}.`) + solution;
    }
    case "choice": {
      if (draft === "") return "Pick an answer first.";
      const picked = a.options[Number(draft)];
      return (picked === a.correct ? "<b>Correct.</b>" : `<b>Not quite.</b> The answer is: ${esc(a.correct)}.`) + solution;
    }
    case "expr": {
      if (!draft) return "Enter an expression first.";
      const problem = exprProblem(draft, a.numbers, a.target);
      return (problem === null ? "<b>Correct.</b>" : `<b>Not quite.</b> ${esc(problem)}`) +
             `<p>One solution:</p>${list(p.explain, "ul")}`;
    }
  }
}
