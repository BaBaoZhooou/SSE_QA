import { spawn, spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { join } from "node:path";

import { renderAllConfigs } from "./render-config.mjs";
import {
  backendRoot,
  dockerDir,
  dockerEnvPath,
  loadUserConfig,
  runtimeDir,
  systemYamlPath,
} from "./paths.mjs";

function commandExists(name) {
  const result = spawnSync("bash", ["-lc", `command -v ${name}`], { encoding: "utf8" });
  return result.status === 0;
}

function dockerAvailable() {
  if (!commandExists("docker")) return false;
  const result = spawnSync("docker", ["info"], { stdio: "ignore" });
  return result.status === 0;
}

export function detectMode(explicit) {
  const mode = (explicit || "auto").toLowerCase();
  if (mode === "docker" || mode === "native") return mode;
  return dockerAvailable() ? "docker" : "native";
}

function composeFile() {
  return join(dockerDir(), "compose.yaml");
}

export function runInstall() {
  const root = backendRoot();
  const requirements = join(root, "requirements.txt");
  if (!existsSync(requirements)) {
    throw new Error(`missing ${requirements}; run scripts/sync-server-bundle.sh from SSE_QA repo`);
  }
  const venv = join(runtimeDir(), "venv");
  if (!commandExists("python3")) {
    throw new Error("python3 is required for native mode");
  }
  spawnSync("python3", ["-m", "venv", venv], { stdio: "inherit" });
  const pip = join(venv, "bin", "pip");
  const steps = [
    [pip, "install", "--upgrade", "pip"],
    [pip, "install", "-r", requirements],
    [pip, "install", "pyyaml", "gunicorn"],
  ];
  for (const cmd of steps) {
    const result = spawnSync(cmd[0], cmd.slice(1), { stdio: "inherit" });
    if (result.status !== 0) throw new Error(`install failed: ${cmd.join(" ")}`);
  }
  console.log(`[sse-qa] venv ready: ${venv}`);
}

function runNativeStart({ detach = false } = {}) {
  const root = backendRoot();
  const script = join(root, "scripts", "start_agent_all.sh");
  if (!existsSync(script)) {
    throw new Error(`missing ${script}; run sync-server-bundle.sh`);
  }
  renderAllConfigs(loadUserConfig());
  const env = {
    ...process.env,
    SYSTEM_YAML: systemYamlPath(),
    SSE_QA_PROJECT_ROOT: root,
  };
  if (detach) {
    const child = spawn("bash", [script], { cwd: root, detached: true, stdio: "ignore", env });
    child.unref();
    console.log(`[sse-qa] native start dispatched (pid=${child.pid})`);
    return;
  }
  const child = spawn("bash", [script], { cwd: root, stdio: "inherit", env });
  child.on("exit", (code) => process.exit(code || 0));
}

function runNativeStop() {
  const root = backendRoot();
  const script = join(root, "scripts", "stop_agent_all.sh");
  if (!existsSync(script)) throw new Error(`missing ${script}`);
  renderAllConfigs(loadUserConfig());
  const result = spawnSync("bash", [script], {
    cwd: root,
    stdio: "inherit",
    env: {
      ...process.env,
      SYSTEM_YAML: systemYamlPath(),
      SSE_QA_PROJECT_ROOT: root,
    },
  });
  process.exit(result.status || 0);
}

function runDockerCompose(action) {
  renderAllConfigs(loadUserConfig());
  const file = composeFile();
  if (!existsSync(file)) throw new Error(`missing ${file}`);
  const args = ["compose", "-f", file, "--env-file", dockerEnvPath(), action];
  if (action === "up") args.push("-d");
  const child = spawn("docker", args, { stdio: "inherit", cwd: dockerDir() });
  child.on("exit", (code) => process.exit(code || 0));
}

export function runStart(modeArg, options = {}) {
  const mode = detectMode(modeArg);
  const detach = Boolean(options.detach);
  console.log(`[sse-qa] starting (${mode} mode, detach=${detach})`);
  if (mode === "docker") {
    if (detach) {
      renderAllConfigs(loadUserConfig());
      const file = composeFile();
      const child = spawn(
        "docker",
        ["compose", "-f", file, "--env-file", dockerEnvPath(), "up", "-d"],
        { detached: true, stdio: "ignore", cwd: dockerDir() },
      );
      child.unref();
      console.log("[sse-qa] docker compose dispatched");
      return;
    }
    return runDockerCompose("up");
  }
  return runNativeStart({ detach });
}

export function runStop(modeArg) {
  const mode = detectMode(modeArg);
  if (mode === "docker") return runDockerCompose("down");
  return runNativeStop();
}

export function runStatus(modeArg) {
  const mode = detectMode(modeArg);
  if (mode === "docker") {
    renderAllConfigs(loadUserConfig());
    const file = composeFile();
    spawnSync("docker", ["compose", "-f", file, "--env-file", dockerEnvPath(), "ps"], {
      stdio: "inherit",
      cwd: dockerDir(),
    });
    return;
  }
  console.log(`backend root: ${backendRoot()}`);
  console.log(`system yaml: ${systemYamlPath()}`);
}
