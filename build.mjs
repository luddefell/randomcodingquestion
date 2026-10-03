// Bundles src/ into the site root and stamps a version on the file links so browsers
// never mix old and new files.  Run with: npm run build
import * as esbuild from "esbuild";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const walk = dir => readdirSync(dir, { withFileTypes: true })
  .flatMap(e => (e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]));

// The version is a hash of everything the site loads, so it changes exactly when they do.
const hash = createHash("sha256");
for (const f of [...walk("src").sort(), "problems.js", "harness.py"]) hash.update(readFileSync(f));
const version = hash.digest("hex").slice(0, 10);

const common = {
  bundle: true,
  minify: true,
  sourcemap: true,
  target: "es2020",
  define: { __VERSION__: JSON.stringify(version) },
  logLevel: "info",
};
await Promise.all([
  esbuild.build({ ...common, entryPoints: ["src/main.ts"], outfile: "app.js", format: "iife", globalName: "App" }),
  esbuild.build({ ...common, entryPoints: ["src/workers/python.worker.ts"], outfile: "python.worker.js", format: "iife" }),
  esbuild.build({ ...common, entryPoints: ["src/workers/yosys.worker.ts"], outfile: "yosys.worker.js", format: "esm" }),
]);

const html = readFileSync("index.html", "utf8")
  .replace(/src="(problems|app)\.js(\?v=[^"]*)?"/g, `src="$1.js?v=${version}"`);
writeFileSync("index.html", html);
console.log(`version ${version}`);
