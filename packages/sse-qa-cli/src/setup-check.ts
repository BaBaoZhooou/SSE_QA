import { existsSync, readdirSync } from "node:fs";

import { healthCheck } from "./client.js";
import {
  configHome,
  configYamlPath,
  expandPath,
  loadSecretsEnv,
  loadUserConfig,
  secretsEnvPath,
} from "./config.js";

export type SetupCategory =
  | "config"
  | "secrets"
  | "llm"
  | "embedding"
  | "chroma"
  | "neo4j"
  | "backend";

export type SetupSeverity = "blocking" | "warning";

export interface SetupIssue {
  id: string;
  severity: SetupSeverity;
  category: SetupCategory;
  message: string;
  user_action: string;
}

export interface SetupCheckItem {
  name: string;
  ok: boolean;
  category: SetupCategory;
  detail?: string;
}

export interface SetupReport {
  success: boolean;
  ready_for_qa: boolean;
  ready_for_retrieval: boolean;
  config_home: string;
  checks: SetupCheckItem[];
  issues: SetupIssue[];
  user_guidance: string;
  backend_included_in_npm: {
    fastQA: boolean;
    highThinkingQA: boolean;
    note: string;
  };
}

function hasChromaArtifacts(dir: string): boolean {
  if (!existsSync(dir)) return false;
  try {
    const entries = readdirSync(dir);
    return entries.some(
      (name) => name.includes("chroma") || name.endsWith(".sqlite3") || name.endsWith(".bin"),
    );
  } catch {
    return false;
  }
}

async function checkNeo4jBolt(url: string): Promise<{ ok: boolean; detail: string }> {
  const match = url.match(/^bolt(?:\+ssc)?:\/\/([^:/]+):(\d+)/i);
  if (!match) return { ok: false, detail: `invalid bolt url: ${url}` };
  const host = match[1];
  const port = Number(match[2]);
  try {
    const net = await import("node:net");
    await new Promise<void>((resolve, reject) => {
      const socket = net.createConnection({ host, port, timeout: 5000 }, () => {
        socket.end();
        resolve();
      });
      socket.on("error", reject);
      socket.on("timeout", () => {
        socket.destroy();
        reject(new Error("timeout"));
      });
    });
    return { ok: true, detail: `${host}:${port} reachable` };
  } catch (error) {
    return { ok: false, detail: error instanceof Error ? error.message : String(error) };
  }
}

async function checkApiKeyReachable(
  baseUrl: string,
  apiKey: string,
  label: string,
): Promise<{ ok: boolean; detail: string }> {
  if (!apiKey) return { ok: false, detail: `${label} missing in secrets.env` };
  const url = `${baseUrl.replace(/\/+$/, "")}/models`;
  try {
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: AbortSignal.timeout(15000),
    });
    if (response.ok || response.status === 404) {
      return { ok: true, detail: `${label} reachable (${response.status})` };
    }
    return { ok: false, detail: `${label} http ${response.status}` };
  } catch (error) {
    return { ok: false, detail: error instanceof Error ? error.message : String(error) };
  }
}

function pushIssue(issues: SetupIssue[], issue: SetupIssue) {
  issues.push(issue);
}

function buildUserGuidance(issues: SetupIssue[], configHomePath: string): string {
  if (!issues.length) {
    return "配置与依赖检查通过。可直接使用 ask_fast / ask_thinking 提问。";
  }
  const lines = [
    "SSE QA 自检发现以下待办，请按项完成后再提问（或接受降级能力）：",
    "",
  ];
  const blocking = issues.filter((i) => i.severity === "blocking");
  const warnings = issues.filter((i) => i.severity === "warning");
  let n = 1;
  for (const item of blocking) {
    lines.push(`${n}. [必须] ${item.message}`);
    lines.push(`   → ${item.user_action}`);
    n += 1;
  }
  for (const item of warnings) {
    lines.push(`${n}. [建议] ${item.message}`);
    lines.push(`   → ${item.user_action}`);
    n += 1;
  }
  lines.push("");
  lines.push(`配置目录：${configHomePath}`);
  lines.push("快速初始化：sse-qa init");
  lines.push("编辑配置：~/.sse-qa/config.yaml（Chroma 绝对路径）");
  lines.push("编辑密钥：~/.sse-qa/secrets.env（LLM_API_KEY 等）");
  return lines.join("\n");
}

export async function runSetupCheck(): Promise<SetupReport> {
  const issues: SetupIssue[] = [];
  const checks: SetupCheckItem[] = [];
  const home = configHome();

  const userConfig = loadUserConfig();
  if (!userConfig) {
    checks.push({ name: "config_yaml", ok: false, category: "config", detail: "missing" });
    pushIssue(issues, {
      id: "config_missing",
      severity: "blocking",
      category: "config",
      message: "尚未创建用户配置文件",
      user_action: `请运行 sse-qa init，然后编辑 ${configYamlPath()} 与 ${secretsEnvPath()}`,
    });
    return finalize(issues, checks, home, false, false);
  }
  checks.push({ name: "config_yaml", ok: true, category: "config", detail: configYamlPath() });

  if (!existsSync(secretsEnvPath())) {
    checks.push({ name: "secrets_env", ok: false, category: "secrets" });
    pushIssue(issues, {
      id: "secrets_missing",
      severity: "blocking",
      category: "secrets",
      message: "secrets.env 不存在",
      user_action: `运行 sse-qa init 或创建 ${secretsEnvPath()}，填入 LLM_API_KEY=sk-...`,
    });
  } else {
    checks.push({ name: "secrets_env", ok: true, category: "secrets", detail: secretsEnvPath() });
  }

  const secrets = loadSecretsEnv();
  const llmKey = secrets.LLM_API_KEY || secrets.DASHSCOPE_API_KEY || "";
  const embedKey =
    secrets.HIGHTHINKINGQA_EMBEDDING_API_KEY ||
    secrets.EMBEDDING_API_KEY ||
    llmKey;

  const llmBase = userConfig.llm?.base_url || "https://dashscope.aliyuncs.com/compatible-mode/v1";
  const llmResult = await checkApiKeyReachable(llmBase, llmKey, "LLM_API_KEY");
  checks.push({ name: "llm_api", ok: llmResult.ok, category: "llm", detail: llmResult.detail });
  if (!llmKey) {
    pushIssue(issues, {
      id: "llm_key_missing",
      severity: "blocking",
      category: "llm",
      message: "未配置 LLM API Key",
      user_action: `在 ${secretsEnvPath()} 添加 LLM_API_KEY=你的密钥（OpenAI 兼容，如 DashScope）`,
    });
  } else if (!llmResult.ok) {
    pushIssue(issues, {
      id: "llm_unreachable",
      severity: "blocking",
      category: "llm",
      message: `LLM API 不可达：${llmResult.detail}`,
      user_action: "检查 llm.base_url 与 API Key 是否正确，网络是否可访问",
    });
  }

  const embedBase =
    userConfig.embedding?.base_url || userConfig.llm?.base_url || llmBase;
  const embedType = userConfig.embedding?.type || "remote";
  if (embedType === "remote") {
    const embedResult = await checkApiKeyReachable(embedBase, embedKey, "EMBEDDING_API_KEY");
    checks.push({
      name: "embedding_api",
      ok: embedResult.ok,
      category: "embedding",
      detail: embedResult.detail,
    });
    if (!embedResult.ok) {
      pushIssue(issues, {
        id: "embedding_unreachable",
        severity: "blocking",
        category: "embedding",
        message: `Embedding API 不可用：${embedResult.detail}`,
        user_action: `在 secrets.env 设置 HIGHTHINKINGQA_EMBEDDING_API_KEY 或与 LLM 共用 LLM_API_KEY；确认 embedding.base_url`,
      });
    }
  }

  const fastPath = expandPath(userConfig.chroma?.fastqa?.vector_db_path || "");
  const thinkPath = expandPath(userConfig.chroma?.thinking?.persist_dir || "");
  let retrievalOk = true;

  if (!fastPath || !fastPath.startsWith("/")) {
    checks.push({ name: "chroma_fastqa_path", ok: false, category: "chroma" });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_fast_path",
      severity: "warning",
      category: "chroma",
      message: "fastQA Chroma 路径未配置或非绝对路径",
      user_action: `在 config.yaml 的 chroma.fastqa.vector_db_path 填写已 ingest 的 Chroma 目录绝对路径`,
    });
  } else if (!existsSync(fastPath)) {
    checks.push({ name: "chroma_fastqa", ok: false, category: "chroma", detail: fastPath });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_fast_missing",
      severity: "warning",
      category: "chroma",
      message: `fastQA 向量库目录不存在：${fastPath}`,
      user_action:
        "请提供已建好的 Chroma persist 目录（含 chroma.sqlite3），或先 ingest SSE 文献向量库后再填入路径",
    });
  } else if (!hasChromaArtifacts(fastPath)) {
    checks.push({ name: "chroma_fastqa", ok: false, category: "chroma", detail: "no artifacts" });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_fast_empty",
      severity: "warning",
      category: "chroma",
      message: `fastQA 目录存在但未见 Chroma 数据文件：${fastPath}`,
      user_action: "确认向量库已 ingest 完成；空库时 fastQA 仅能依赖 LLM 先验，检索质量很差",
    });
  } else {
    checks.push({ name: "chroma_fastqa", ok: true, category: "chroma", detail: fastPath });
  }

  if (!thinkPath || !thinkPath.startsWith("/")) {
    checks.push({ name: "chroma_thinking_path", ok: false, category: "chroma" });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_think_path",
      severity: "warning",
      category: "chroma",
      message: "thinking Chroma 路径未配置或非绝对路径",
      user_action: `在 config.yaml 的 chroma.thinking.persist_dir 填写绝对路径，collection_name 与建库一致（默认 sse_literature）`,
    });
  } else if (!existsSync(thinkPath)) {
    checks.push({ name: "chroma_thinking", ok: false, category: "chroma", detail: thinkPath });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_think_missing",
      severity: "warning",
      category: "chroma",
      message: `thinking 向量库目录不存在：${thinkPath}`,
      user_action: "请提供 highThinkingQA 使用的 Chroma persist 目录",
    });
  } else if (!hasChromaArtifacts(thinkPath)) {
    checks.push({ name: "chroma_thinking", ok: false, category: "chroma", detail: "no artifacts" });
    retrievalOk = false;
    pushIssue(issues, {
      id: "chroma_think_empty",
      severity: "warning",
      category: "chroma",
      message: `thinking 目录存在但未见 Chroma 数据：${thinkPath}`,
      user_action: "确认 collection 名与 ingest 一致；空库时 thinking 检索无效",
    });
  } else {
    checks.push({ name: "chroma_thinking", ok: true, category: "chroma", detail: thinkPath });
  }

  const neoEnabled = userConfig.neo4j?.enabled !== false && userConfig.neo4j?.schema !== "off";
  if (neoEnabled) {
    const neoUrl = userConfig.neo4j?.url || "bolt://127.0.0.1:7698";
    const bolt = await checkNeo4jBolt(neoUrl);
    checks.push({ name: "neo4j_bolt", ok: bolt.ok, category: "neo4j", detail: bolt.detail });
    if (!secrets.NEO4J_PASSWORD && !secrets.FASTQA_NEO4J_PASSWORD) {
      checks.push({ name: "neo4j_password", ok: false, category: "neo4j" });
      pushIssue(issues, {
        id: "neo4j_password",
        severity: "warning",
        category: "neo4j",
        message: "Neo4j 已启用但未配置密码",
        user_action: `在 secrets.env 添加 NEO4J_PASSWORD=...；若暂不用图谱，可在 config.yaml 设 neo4j.enabled: false`,
      });
    } else if (!bolt.ok) {
      pushIssue(issues, {
        id: "neo4j_unreachable",
        severity: "warning",
        category: "neo4j",
        message: `Neo4j 不可达（${bolt.detail}）`,
        user_action:
          "请启动自建 Neo4j 并修正 neo4j.url；或运行 bash scripts/知识图谱/start_neo4j_kg.sh 导入 SSE 图谱；不需要图谱可设 neo4j.enabled: false",
      });
    } else {
      checks.push({ name: "neo4j_password", ok: true, category: "neo4j" });
    }
  } else {
    checks.push({ name: "neo4j", ok: true, category: "neo4j", detail: "disabled" });
  }

  const health = await healthCheck();
  checks.push({
    name: "backend_health",
    ok: Boolean(health.success),
    category: "backend",
    detail: JSON.stringify(health.checks),
  });
  if (!health.success) {
    pushIssue(issues, {
      id: "backend_down",
      severity: "blocking",
      category: "backend",
      message: "问答后端未就绪（fastQA / highThinkingQA）",
      user_action:
        "运行 sse-qa server start；若已开 SSE_QA_AUTO_START=1，等待 1–2 分钟或查看 sse-qa doctor",
    });
  }

  const hasBlocking = issues.some((i) => i.severity === "blocking");
  const readyForQa = !hasBlocking;
  return finalize(issues, checks, home, readyForQa, retrievalOk);
}

function finalize(
  issues: SetupIssue[],
  checks: SetupCheckItem[],
  home: string,
  readyForQa: boolean,
  readyForRetrieval: boolean,
): SetupReport {
  const success = issues.length === 0;
  return {
    success,
    ready_for_qa: readyForQa,
    ready_for_retrieval: readyForRetrieval,
    config_home: home,
    checks,
    issues,
    user_guidance: buildUserGuidance(issues, home),
    backend_included_in_npm: {
      fastQA: true,
      highThinkingQA: true,
      note:
        "fastQA 与 highThinkingQA 服务代码已内嵌在 @sse-qa/cli 的 runtime/backend/ 中；Chroma 向量文件、Neo4j 图数据库、LLM/Embedding API Key 需用户自备并在 ~/.sse-qa 配置",
    },
  };
}

export function formatSetupReportForAgent(report: SetupReport): string {
  return JSON.stringify(report, null, 2);
}
