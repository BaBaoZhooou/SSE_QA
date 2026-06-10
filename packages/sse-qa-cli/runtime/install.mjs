import { spawnSync } from "node:child_process";

console.log("[sse-qa] checking prerequisites...");
const checks = [
  ["node", ["--version"]],
  ["python3", ["--version"]],
  ["docker", ["--version"]],
];
for (const [cmd, cmdArgs] of checks) {
  const result = spawnSync(cmd, cmdArgs, { encoding: "utf8" });
  if (result.status === 0) {
    console.log(`  ✓ ${cmd}: ${(result.stdout || result.stderr || "").trim()}`);
  } else {
    console.log(`  · ${cmd}: not found (optional for some modes)`);
  }
}
