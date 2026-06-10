import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";

export interface SseQaUserConfig {
  llm: {
    base_url: string;
    model: string;
    api_key_file: string;
  };
  embedding: {
    type: string;
    base_url: string;
    model: string;
    api_key_file: string;
  };
  chroma: {
    fastqa: {
      vector_db_path: string;
      vector_db_md_path?: string;
    };
    thinking: {
      persist_dir: string;
      collection_name: string;
    };
  };
  neo4j: {
    enabled: boolean;
    url: string;
    username: string;
    password_file: string;
    database: string;
    schema: string;
  };
  ports: {
    fastqa: number;
    thinking: number;
    redis: number;
  };
  modes: {
    enabled: string;
  };
  rerank?: {
    provider: string;
  };
}

export function configHome(): string {
  return resolve(process.env.SSE_QA_CONFIG_HOME || join(homedir(), ".sse-qa"));
}

export function configYamlPath(): string {
  return resolve(process.env.SSE_QA_CONFIG_YAML || join(configHome(), "config.yaml"));
}

export function secretsEnvPath(): string {
  return resolve(process.env.SSE_QA_SECRETS_ENV || join(configHome(), "secrets.env"));
}

export function runtimeDir(): string {
  return resolve(process.env.SSE_QA_RUNTIME_DIR || join(configHome(), "runtime"));
}

export function expandPath(value: string): string {
  const trimmed = (value || "").trim();
  if (!trimmed) return trimmed;
  if (trimmed.startsWith("~/")) return join(homedir(), trimmed.slice(2));
  if (trimmed === "~") return homedir();
  return resolve(trimmed);
}

export function loadSecretsEnv(): Record<string, string> {
  const path = secretsEnvPath();
  if (!existsSync(path)) return {};
  const out: Record<string, string> = {};
  for (const line of readFileSync(path, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx <= 0) continue;
    const key = trimmed.slice(0, idx).trim();
    let value = trimmed.slice(idx + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    out[key] = value;
  }
  return out;
}

function parseScalar(raw: string): string | number | boolean {
  const value = raw.trim();
  if (value === "true") return true;
  if (value === "false") return false;
  if (/^-?\d+$/.test(value)) return Number(value);
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

/** Minimal YAML reader for flat/nested config.yaml (no external deps). */
export function parseSimpleYaml(text: string): Record<string, unknown> {
  const root: Record<string, unknown> = {};
  const stack: Array<{ indent: number; obj: Record<string, unknown> }> = [{ indent: -1, obj: root }];
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.replace(/\t/g, "  ");
    if (!line.trim() || line.trim().startsWith("#")) continue;
    const indent = line.match(/^ */)?.[0].length ?? 0;
    const content = line.trim();
    const colon = content.indexOf(":");
    if (colon <= 0) continue;
    const key = content.slice(0, colon).trim();
    const rest = content.slice(colon + 1).trim();
    while (stack.length > 1 && indent <= stack[stack.length - 1].indent) {
      stack.pop();
    }
    const parent = stack[stack.length - 1].obj;
    if (!rest) {
      const child: Record<string, unknown> = {};
      parent[key] = child;
      stack.push({ indent, obj: child });
      continue;
    }
    parent[key] = parseScalar(rest);
  }
  return root;
}

export function loadUserConfig(): SseQaUserConfig | null {
  const path = configYamlPath();
  if (!existsSync(path)) return null;
  const parsed = parseSimpleYaml(readFileSync(path, "utf8")) as Partial<SseQaUserConfig>;
  return parsed as SseQaUserConfig;
}

export function defaultConfigTemplate(): string {
  const home = configHome();
  return `# SSE QA user config — edit paths and run: sse-qa config validate
llm:
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
  model: qwen3.6-plus
  api_key_file: ${home}/secrets.env

embedding:
  type: remote
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
  model: text-embedding-v4
  api_key_file: ${home}/secrets.env

chroma:
  fastqa:
    vector_db_path: /absolute/path/to/vector_database
    vector_db_md_path: /absolute/path/to/vector_database_md
  thinking:
    persist_dir: /absolute/path/to/vectordb
    collection_name: sse_literature

neo4j:
  enabled: true
  url: bolt://127.0.0.1:7698
  username: neo4j
  password_file: ${home}/secrets.env
  database: neo4j
  schema: sse

ports:
  fastqa: 18018
  thinking: 18019
  redis: 16380

modes:
  enabled: fast,thinking

rerank:
  provider: none
`;
}

export function defaultSecretsTemplate(): string {
  return `# SSE QA secrets — do not commit
LLM_API_KEY=
INTENT_MODEL_API_KEY=
HIGHTHINKINGQA_EMBEDDING_API_KEY=
EMBEDDING_API_KEY=
NEO4J_PASSWORD=
FASTQA_NEO4J_PASSWORD=
`;
}
