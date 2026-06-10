import { healthCheck } from "./client.js";
import { isAutoStartEnabled } from "./runtime-mode.js";
import { runServerSync, serverAvailable, startServerDetached } from "./server-proxy.js";

export interface EnsureBackendOptions {
  argv?: string[];
  timeoutMs?: number;
  pollMs?: number;
}

function logStatus(message: string) {
  console.error(`[sse-qa] ${message}`);
}

async function sleep(ms: number) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

export async function ensureBackend(options: EnsureBackendOptions = {}): Promise<void> {
  const argv = options.argv ?? process.argv;
  if (!isAutoStartEnabled(argv)) {
    logStatus("auto-start disabled (SSE_QA_AUTO_START=0 or --no-auto-start)");
    return;
  }

  const timeoutMs = options.timeoutMs ?? Number(process.env.SSE_QA_START_TIMEOUT_MS || "120000");
  const pollMs = options.pollMs ?? 2000;

  const probe = async () => {
    const report = await healthCheck();
    return report.success;
  };

  if (await probe()) {
    logStatus("backend ready");
    return;
  }

  if (!serverAvailable()) {
    throw new Error("bundled runtime missing; reinstall @sse-qa/cli");
  }

  logStatus("backend not ready; starting (detached)...");
  startServerDetached({ mode: "auto" });

  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    await sleep(pollMs);
    if (await probe()) {
      logStatus("backend became healthy");
      return;
    }
  }

  throw new Error(`backend did not become healthy within ${timeoutMs}ms; run: sse-qa doctor`);
}

export async function ensureBackendQuiet(): Promise<boolean> {
  const report = await healthCheck();
  return Boolean(report.success);
}
