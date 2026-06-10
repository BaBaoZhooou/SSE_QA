import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PACKAGE_ROOT = resolve(__dirname, "..");

export function configHome() {
  return resolve(process.env.SSE_QA_CONFIG_HOME || join(homedir(), ".sse-qa"));
}

export function configYamlPath() {
  return resolve(process.env.SSE_QA_CONFIG_YAML || join(configHome(), "config.yaml"));
}

export function secretsEnvPath() {
  return resolve(process.env.SSE_QA_SECRETS_ENV || join(configHome(), "secrets.env"));
}

export function runtimeDir() {
  return resolve(process.env.SSE_QA_RUNTIME_DIR || join(configHome(), "runtime"));
}

export function systemYamlPath() {
  return join(runtimeDir(), "system.agent.yaml");
}

export function systemEnvPath() {
  return join(runtimeDir(), "system.env");
}

export function dockerEnvPath() {
  return join(runtimeDir(), "docker.env");
}

export function expandPath(value) {
  const trimmed = String(value || "").trim();
  if (!trimmed) return trimmed;
  if (trimmed.startsWith("~/")) return join(homedir(), trimmed.slice(2));
  if (trimmed === "~") return homedir();
  return resolve(trimmed);
}

export function backendRoot() {
  if (process.env.SSE_QA_BACKEND_ROOT) {
    return resolve(process.env.SSE_QA_BACKEND_ROOT);
  }
  const bundled = join(PACKAGE_ROOT, "backend");
  if (existsSync(join(bundled, "scripts", "start_agent_all.sh"))) {
    return bundled;
  }
  if (process.env.SSE_QA_PROJECT_ROOT) {
    return resolve(process.env.SSE_QA_PROJECT_ROOT);
  }
  let dir = process.cwd();
  for (let i = 0; i < 8; i += 1) {
    if (existsSync(join(dir, "scripts", "start_agent_all.sh"))) return dir;
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return bundled;
}

export function dockerDir() {
  return join(PACKAGE_ROOT, "docker");
}

export function packageRoot() {
  return PACKAGE_ROOT;
}

export function loadSecretsEnv() {
  const path = secretsEnvPath();
  if (!existsSync(path)) return {};
  const out = {};
  for (const line of readFileSync(path, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx <= 0) continue;
    out[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
  }
  return out;
}

export function parseSimpleYaml(text) {
  const root = {};
  const stack = [{ indent: -1, obj: root }];
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.replace(/\t/g, "  ");
    if (!line.trim() || line.trim().startsWith("#")) continue;
    const indent = line.match(/^ */)?.[0].length ?? 0;
    const content = line.trim();
    const colon = content.indexOf(":");
    if (colon <= 0) continue;
    const key = content.slice(0, colon).trim();
    const rest = content.slice(colon + 1).trim();
    while (stack.length > 1 && indent <= stack[stack.length - 1].indent) stack.pop();
    const parent = stack[stack.length - 1].obj;
    if (!rest) {
      const child = {};
      parent[key] = child;
      stack.push({ indent, obj: child });
      continue;
    }
    let value = rest;
    if (value === "true") value = true;
    else if (value === "false") value = false;
    else if (/^-?\d+$/.test(value)) value = Number(value);
    else if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    parent[key] = value;
  }
  return root;
}

export function loadUserConfig() {
  const path = configYamlPath();
  if (!existsSync(path)) {
    throw new Error(`missing ${path}; run: sse-qa init`);
  }
  return parseSimpleYaml(readFileSync(path, "utf8"));
}

export function ensureRuntimeDir() {
  mkdirSync(runtimeDir(), { recursive: true });
}

export function writeText(path, content) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content, "utf8");
}
