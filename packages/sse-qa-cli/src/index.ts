#!/usr/bin/env node
import { spawn } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

import { askStream, healthCheck, type QaMode } from "./client.js";
import { configYamlPath, loadUserConfig, parseSimpleYaml } from "./config.js";
import { runDoctor } from "./doctor.js";
import { runInit } from "./init.js";
import { runSetupCheck } from "./setup-check.js";
import { delegateServer, runServerSync, serverAvailable } from "./server-proxy.js";

const args = process.argv.slice(2);

async function main() {
  const command = args[0] || "--help";
  if (command === "--help" || command === "-h") return printHelp();
  if (command === "mcp") {
    const { runMcp } = await import("./mcp.js");
    return runMcp(process.argv);
  }
  if (command === "init") return initCli();
  if (command === "doctor") return doctorCli();
  if (command === "setup-check") return setupCheckCli();
  if (command === "config") return configCli(args.slice(1));
  if (command === "health") return print(await healthCheck(), jsonFlag());
  if (command === "ask-fast") return askCli("fast");
  if (command === "ask-thinking") return askCli("thinking");
  if (command === "server") return serverCli(args.slice(1));
  if (command === "stack") return stackCli(args.slice(1));
  throw new Error(`unknown command: ${command}`);
}

async function initCli() {
  const force = args.includes("--force");
  const result = runInit({ force });
  print(result, jsonFlag());
  if (!jsonFlag()) {
    console.log("\nNext steps:");
    console.log("  1. Edit ~/.sse-qa/config.yaml — set Chroma absolute paths");
    console.log("  2. Edit ~/.sse-qa/secrets.env — set LLM_API_KEY");
    console.log("  3. sse-qa server install && sse-qa server start");
    console.log("  4. sse-qa doctor");
    console.log("  5. claude mcp add sse-qa -- sse-qa mcp --auto-start");
  }
}

async function setupCheckCli() {
  const report = await runSetupCheck();
  if (!jsonFlag()) {
    console.log(report.user_guidance);
  } else {
    print(report, true);
  }
  if (!report.ready_for_qa) process.exitCode = 1;
}

async function doctorCli() {
  const report = await runDoctor();
  if (!jsonFlag()) {
    console.log(report.user_guidance);
    console.log("");
    for (const check of report.checks) {
      console.log(`${check.ok ? "✓" : "✗"} ${check.name}${check.detail ? `: ${check.detail}` : ""}`);
    }
    if (report.backend_included_in_npm) {
      console.log("");
      console.log(`ℹ ${report.backend_included_in_npm.note}`);
    }
  } else {
    print(report, true);
  }
  if (!report.ready_for_qa) process.exitCode = 1;
}

async function configCli(configArgs: string[]) {
  const action = configArgs[0] || "show";
  if (action === "show") {
    const path = configYamlPath();
    if (!existsSync(path)) throw new Error(`missing ${path}; run: sse-qa init`);
    print({ path, content: readFileSync(path, "utf8") }, jsonFlag());
    return;
  }
  if (action === "validate") {
    const cfg = loadUserConfig();
    if (!cfg) throw new Error(`missing ${configYamlPath()}; run: sse-qa init`);
    if (serverAvailable()) {
      const result = runServerSync(["config", "validate"]);
      if (!result.ok) throw new Error(result.stderr || result.stdout || "config validate failed");
      print(JSON.parse(result.stdout || "{}"), jsonFlag());
      return;
    }
    parseSimpleYaml(readFileSync(configYamlPath(), "utf8"));
    print({ success: true, message: "config.yaml syntax ok" }, jsonFlag());
    return;
  }
  throw new Error(`unknown config action: ${action}`);
}

async function serverCli(serverArgs: string[]) {
  if (!serverArgs.length) {
    throw new Error("usage: sse-qa server install|start|stop|status [--mode auto|docker|native]");
  }
  delegateServer(serverArgs);
}

async function askCli(mode: QaMode) {
  const question = positionalQuestion(args.slice(1));
  const result = await askStream(mode, question, { timeoutSeconds: numberOption("--timeout") });
  print(result, jsonFlag());
}

async function stackCli(stackArgs: string[]) {
  const action = stackArgs[0] || "status";
  if (action === "status" || action === "health") return print(await healthCheck(), jsonFlag());
  if (action === "start") {
    if (serverAvailable()) return delegateServer(["start", ...stackArgs.slice(1)]);
    return runProjectScript("scripts/start_agent_all.sh");
  }
  if (action === "stop") {
    if (serverAvailable()) return delegateServer(["stop", ...stackArgs.slice(1)]);
    return runProjectScript("scripts/stop_agent_all.sh");
  }
  throw new Error(`unknown stack action: ${action}`);
}

function runProjectScript(script: string) {
  const root = resolve(process.env.SSE_QA_PROJECT_ROOT || process.env.QA_PROJECT_ROOT || process.cwd());
  const full = resolve(root, script);
  if (!existsSync(full)) {
    throw new Error(`project script not found: ${full}; set SSE_QA_PROJECT_ROOT or reinstall @sse-qa/cli`);
  }
  const child = spawn("bash", [full], {
    cwd: root,
    stdio: "inherit",
    env: { ...process.env, SYSTEM_YAML: process.env.SYSTEM_YAML || resolve(root, "config/system.agent.yaml") },
  });
  child.on("exit", (code) => process.exit(code || 0));
}

function positionalQuestion(values: string[]) {
  const filtered = values.filter((item) => !item.startsWith("--"));
  const question = filtered.join(" ").trim();
  if (!question) throw new Error("question is required");
  return question;
}

function jsonFlag() {
  return args.includes("--json");
}

function numberOption(name: string) {
  const index = args.indexOf(name);
  if (index < 0) return undefined;
  const raw = args[index + 1];
  if (!raw) return undefined;
  const value = Number(raw);
  return Number.isFinite(value) ? value : undefined;
}

function print(payload: unknown, asJson: boolean) {
  if (asJson) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }
  const record = payload as Record<string, unknown>;
  if (typeof record.answer === "string") {
    console.log(record.answer);
    if (Array.isArray(record.references) && record.references.length) {
      console.log(`\nReferences: ${record.references.join(", ")}`);
    }
    if (record.trace_id) console.log(`\nTrace: ${record.trace_id}`);
    return;
  }
  if (Array.isArray(record.checks)) {
    for (const check of record.checks as Array<{ name: string; ok: boolean; detail?: string }>) {
      console.log(`${check.ok ? "✓" : "✗"} ${check.name}${check.detail ? `: ${check.detail}` : ""}`);
    }
    return;
  }
  console.log(JSON.stringify(payload, null, 2));
}

function printHelp() {
  console.log(`sse-qa — 固态电解质 QA（单包：CLI + MCP + 后端）

Usage:
  sse-qa init [--force] [--json]
  sse-qa config show|validate [--json]
  sse-qa doctor [--json]
  sse-qa setup-check [--json]
  sse-qa server install|start|stop|status [--mode auto|docker|native]
  sse-qa health [--json]
  sse-qa ask-fast|ask-thinking "问题" [--json] [--timeout 360]
  sse-qa mcp [--auto-start|--no-auto-start]
  sse-qa stack start|stop|status

Quick start:
  npm install -g @sse-qa/cli
  sse-qa init
  # edit ~/.sse-qa/config.yaml and secrets.env
  sse-qa server install && sse-qa server start
  sse-qa doctor
  claude mcp add sse-qa -- npx -y @sse-qa/cli mcp --auto-start

Env:
  SSE_QA_AUTO_START=1         # MCP 加载时自动启动后端（默认开）
  SSE_QA_START_TIMEOUT_MS=120000
  SSE_QA_FASTQA_URL=http://127.0.0.1:18018
  SSE_QA_THINKING_URL=http://127.0.0.1:18019
`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
