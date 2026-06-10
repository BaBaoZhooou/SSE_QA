import { spawn, spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export function cliRootDir(): string {
  return dirname(dirname(fileURLToPath(import.meta.url)));
}

export function resolveServerBin(): string | null {
  const bundled = join(cliRootDir(), "runtime/src/index.mjs");
  if (existsSync(bundled)) return bundled;
  return null;
}

export function delegateServer(args: string[]): never | void {
  const bin = resolveServerBin();
  if (!bin) {
    throw new Error("bundled runtime missing; reinstall @sse-qa/cli");
  }
  const child = spawn(process.execPath, [bin, ...args], { stdio: "inherit" });
  child.on("exit", (code) => process.exit(code || 0));
}

export function serverAvailable(): boolean {
  return resolveServerBin() !== null;
}

export function runServerSync(args: string[]): { ok: boolean; stdout: string; stderr: string } {
  const bin = resolveServerBin();
  if (!bin) {
    return { ok: false, stdout: "", stderr: "bundled runtime missing" };
  }
  const result = spawnSync(process.execPath, [bin, ...args], { encoding: "utf8" });
  return {
    ok: result.status === 0,
    stdout: result.stdout || "",
    stderr: result.stderr || "",
  };
}

export function startServerDetached(options: { mode?: string } = {}): void {
  const bin = resolveServerBin();
  if (!bin) {
    throw new Error("bundled runtime missing; reinstall @sse-qa/cli");
  }
  const args = ["start", "--detach", "--mode", options.mode || "auto"];
  const child = spawn(process.execPath, [bin, ...args], {
    detached: true,
    stdio: "ignore",
  });
  child.unref();
}
