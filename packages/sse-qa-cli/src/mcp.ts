import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { askStream, getEnabledModes, healthCheck, type QaMode } from "./client.js";
import { ensureBackend } from "./ensure-backend.js";
import { isAutoStartEnabled } from "./runtime-mode.js";
import { runSetupCheck, type SetupReport } from "./setup-check.js";

const modeToolMeta: Record<QaMode, { name: string; description: string }> = {
  fast: {
    name: "ask_fast",
    description:
      "Quick literature QA for solid-state electrolytes (definitions, facts, short answers). Prefer for simple factual questions.",
  },
  thinking: {
    name: "ask_thinking",
    description:
      "Deep thinking QA for SSE mechanisms, comparisons (sulfide vs oxide), tradeoffs, and synthesis. Prefer for complex analytical questions.",
  },
};

let cachedSetup: SetupReport | null = null;

async function getSetupReport(refresh = false): Promise<SetupReport> {
  if (!refresh && cachedSetup) return cachedSetup;
  cachedSetup = await runSetupCheck();
  return cachedSetup;
}

function gateAsk(report: SetupReport) {
  if (report.ready_for_qa) return null;
  return {
    success: false,
    blocked: true,
    reason: "setup_incomplete",
    user_guidance: report.user_guidance,
    issues: report.issues.filter((i) => i.severity === "blocking"),
    hint: "请先向用户说明 user_guidance 中的待办项，待配置完成后再调用 ask_fast/ask_thinking；或调用 setup_check 刷新状态。",
  };
}

export async function runMcp(argv: string[] = process.argv): Promise<void> {
  const enabledModes = getEnabledModes();
  const server = new McpServer({
    name: "sse-qa",
    version: "0.3.2",
  });

  server.tool(
    "setup_check",
    "Run full setup self-check (config, LLM/Embedding API, Chroma paths, Neo4j, backend). Returns user_guidance for Claude to tell the user what to configure. Call this before first ask or when health fails.",
    { refresh: z.boolean().optional() },
    async ({ refresh }) => json(await getSetupReport(refresh === true)),
  );

  server.tool(
    "health_check",
    "Backend health (fastQA + highThinkingQA) plus setup summary. If not ready, read user_guidance.",
    { refresh: z.boolean().optional() },
    async ({ refresh }) => {
      const setup = await getSetupReport(refresh === true);
      const health = await healthCheck();
      return json({
        ...health,
        setup_ready: setup.ready_for_qa,
        retrieval_ready: setup.ready_for_retrieval,
        issues: setup.issues,
        user_guidance: setup.user_guidance,
      });
    },
  );

  for (const mode of enabledModes) {
    const meta = modeToolMeta[mode];
    server.tool(
      meta.name,
      `${meta.description} If setup_check shows blocking issues, guide the user first instead of calling this.`,
      { question: z.string(), timeoutSeconds: z.number().optional() },
      async ({ question, timeoutSeconds }) => {
        const setup = await getSetupReport(false);
        const blocked = gateAsk(setup);
        if (blocked) return json(blocked);
        if (!setup.ready_for_retrieval) {
          return json({
            ...(await askStream(mode, question, {
              timeoutSeconds: timeoutSeconds ?? 360,
            })),
            setup_warning:
              "Chroma 向量库未就绪，检索可能无效；请将 setup_check.user_guidance 转述给用户以完善配置。",
            user_guidance: setup.user_guidance,
          });
        }
        return json(await askStream(mode, question, { timeoutSeconds: timeoutSeconds ?? 360 }));
      },
    );
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Do not block stdio handshake on backend warm-up or setup probes (Claude health ~30s).
  if (isAutoStartEnabled(argv)) {
    void ensureBackend({ argv }).catch((error) => {
      console.error(
        `[sse-qa] ensureBackend: ${error instanceof Error ? error.message : String(error)}`,
      );
    });
  }

  void runSetupCheck()
    .then((report) => {
      cachedSetup = report;
      if (!report.ready_for_qa) {
        console.error(
          "[sse-qa] setup incomplete — Claude should call setup_check and guide the user:\n",
        );
        console.error(report.user_guidance);
      }
    })
    .catch((error) => {
      console.error(
        `[sse-qa] setup probe: ${error instanceof Error ? error.message : String(error)}`,
      );
    });
}

function json(payload: unknown) {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(payload, null, 2),
      },
    ],
  };
}
