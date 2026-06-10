#!/usr/bin/env node
import { runInstall, runStart, runStatus, runStop } from "./spawn-stack.mjs";
import { renderAllConfigs, validateUserConfig } from "./render-config.mjs";
import { loadUserConfig } from "./paths.mjs";

const args = process.argv.slice(2);
const command = args[0] || "--help";

function flagValue(name) {
  const idx = args.indexOf(name);
  return idx >= 0 ? args[idx + 1] : undefined;
}

function hasFlag(name) {
  return args.includes(name);
}

function modeArg() {
  return flagValue("--mode") || "auto";
}

async function main() {
  if (command === "--help" || command === "-h") {
    console.log(`sse-qa runtime — SSE QA backend (fastQA + highThinkingQA + Redis)

Usage:
  sse-qa server install
  sse-qa server start [--mode auto|docker|native] [--detach]
  sse-qa server stop [--mode auto|docker|native]
  sse-qa server status [--mode auto|docker|native]
  sse-qa server config render|validate
`);
    return;
  }
  if (command === "install") return runInstall();
  if (command === "start") {
    return runStart(modeArg(), { detach: hasFlag("--detach") });
  }
  if (command === "stop") return runStop(modeArg());
  if (command === "status") return runStatus(modeArg());
  if (command === "config") {
    const action = args[1] || "validate";
    if (action === "render") {
      const paths = renderAllConfigs(loadUserConfig());
      console.log(JSON.stringify({ success: true, ...paths }));
      return;
    }
    if (action === "validate") {
      const report = validateUserConfig(loadUserConfig());
      console.log(JSON.stringify(report));
      if (!report.success) process.exitCode = 1;
      return;
    }
    throw new Error(`unknown config action: ${action}`);
  }
  throw new Error(`unknown command: ${command}`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
