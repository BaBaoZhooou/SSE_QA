export type QaMode = "fast" | "thinking";

export const ALL_QA_MODES: QaMode[] = ["fast", "thinking"];

export interface QaConfig {
  timeoutSeconds: number;
}

export interface QaResult {
  success?: boolean;
  mode?: string;
  answer?: string;
  error?: string;
  trace_id?: string;
  references?: unknown[];
  reference_objects?: unknown[];
  steps_summary?: unknown[];
  warnings?: string[];
  raw_metadata?: Record<string, unknown>;
  event_count?: number;
  backend_url?: string;
}

function env(name: string, fallback = ""): string {
  return (
    process.env[`SSE_QA_${name}`] ||
    process.env[`LFP_QA_${name}`] ||
    process.env[`QA_${name}`] ||
    fallback
  );
}

function resolveAskStreamUrl(mode: QaMode): string {
  const base = backendUrlForMode(mode);
  return `${base}/api/ask_stream`;
}

function backendUrlForMode(mode: QaMode): string {
  const defaults: Record<QaMode, string> = {
    fast: "http://127.0.0.1:18018",
    thinking: "http://127.0.0.1:18019",
  };
  const keys: Record<QaMode, string> = {
    fast: "FASTQA_URL",
    thinking: "THINKING_URL",
  };
  return env(keys[mode], defaults[mode]).replace(/\/+$/, "");
}

function isQaMode(value: string): value is QaMode {
  return value === "fast" || value === "thinking";
}

export function getEnabledModes(): QaMode[] {
  const raw = env("ENABLED_MODES") || process.env.QA_ENABLED_MODES || "";
  if (raw.trim()) {
    const parsed = raw
      .split(/[,;\s]+/)
      .map((item) => item.trim().toLowerCase())
      .filter(isQaMode);
    if (parsed.length) return parsed;
  }
  return [...ALL_QA_MODES];
}

export function assertModeEnabled(mode: QaMode, enabledModes: QaMode[] = getEnabledModes()): void {
  if (!enabledModes.includes(mode)) {
    throw new Error(`QA mode '${mode}' is disabled. Enabled modes: ${enabledModes.join(", ")}`);
  }
}

export function loadConfig(overrides: Partial<QaConfig> = {}): QaConfig {
  return {
    timeoutSeconds: Number(overrides.timeoutSeconds || env("TIMEOUT_SECONDS", "360")),
  };
}

export async function healthCheck(config: Partial<QaConfig> = {}) {
  const cfg = loadConfig(config);
  const enabledModes = getEnabledModes();
  const checks: Record<string, string> = {};

  if (enabledModes.includes("fast")) {
    checks.fastqa = `${backendUrlForMode("fast")}/healthz`;
  }
  if (enabledModes.includes("thinking")) {
    checks.thinking = `${backendUrlForMode("thinking")}/api/health`;
  }
  const results: Record<string, unknown> = {};
  for (const [name, url] of Object.entries(checks)) {
    const started = Date.now();
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(Math.min(cfg.timeoutSeconds, 15) * 1000) });
      results[name] = { ok: response.ok, status_code: response.status, elapsed_ms: Date.now() - started };
    } catch (error) {
      results[name] = { ok: false, error: error instanceof Error ? error.message : String(error) };
    }
  }
  return {
    success: Object.values(results).every((item: any) => Boolean(item?.ok)),
    enabled_modes: enabledModes,
    checks: results,
  };
}

export async function askStream(mode: QaMode, question: string, options: Record<string, unknown> = {}): Promise<QaResult> {
  assertModeEnabled(mode);
  const cfg = loadConfig(options as Partial<QaConfig>);
  const payload = {
    question,
    requested_mode: mode,
    conversation_id: options.conversationId || options.conversation_id || undefined,
    user_id: options.userId || options.user_id || undefined,
    chat_history: options.chatHistory || [],
    options: options.options || {},
  };
  const url = resolveAskStreamUrl(mode);
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(cfg.timeoutSeconds * 1000),
  });
  if (!response.ok || !response.body) {
    throw new Error(`ask_stream failed: http=${response.status} url=${url} body=${await response.text()}`);
  }
  const events = await parseSseStream(response.body);
  const result = collectAnswer(events);
  return {
    ...result,
    success: !result.error,
    mode,
    backend_url: backendUrlForMode(mode),
  };
}

async function parseSseStream(stream: ReadableStream<Uint8Array>): Promise<Record<string, unknown>[]> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  const events: Record<string, unknown>[] = [];
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let index: number;
    while ((index = buffer.indexOf("\n\n")) >= 0) {
      const frame = buffer.slice(0, index);
      buffer = buffer.slice(index + 2);
      appendFrame(events, frame);
    }
  }
  appendFrame(events, buffer);
  return events;
}

function appendFrame(events: Record<string, unknown>[], frame: string) {
  const data = frame
    .split(/\r?\n/)
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice(5).trim())
    .join("\n")
    .trim();
  if (!data) return;
  try {
    const parsed = JSON.parse(data);
    if (parsed && typeof parsed === "object") events.push(parsed);
  } catch {
    events.push({ type: "raw", raw: data });
  }
}

function collectAnswer(events: Record<string, any>[]): QaResult {
  const chunks: string[] = [];
  const steps: unknown[] = [];
  const references: unknown[] = [];
  const referenceObjects: unknown[] = [];
  const warnings: string[] = [];
  let metadata: Record<string, unknown> = {};
  let finalAnswer = "";
  let error = "";
  let traceId = "";
  for (const event of events) {
    const type = String(event.type || "");
    traceId = String(event.trace_id || traceId);
    if (type === "content") chunks.push(String(event.content || ""));
    else if (type === "step") {
      steps.push({ step: event.step, status: event.status, message: event.message || event.content });
      if (event.status === "error") warnings.push(String(event.error || event.message || "step error"));
    } else if (type === "metadata") {
      metadata = { ...metadata, ...event };
      references.push(...asArray(event.references));
      referenceObjects.push(...asArray(event.reference_objects));
    } else if (type === "done") {
      finalAnswer = String(event.final_answer || finalAnswer);
      metadata = { ...metadata, ...event };
      references.push(...asArray(event.references));
      referenceObjects.push(...asArray(event.reference_objects));
    } else if (type === "error") {
      error = String(event.error || event.message || "upstream error");
    }
  }
  return {
    answer: (finalAnswer || chunks.join("")).trim(),
    error,
    trace_id: traceId,
    references: dedupe(references),
    reference_objects: referenceObjects.slice(0, 50),
    steps_summary: steps.slice(-20),
    warnings: dedupe(warnings) as string[],
    raw_metadata: metadata,
    event_count: events.length,
  };
}

function asArray(value: unknown): unknown[] {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}

function dedupe(values: unknown[]) {
  const seen = new Set<string>();
  const out: unknown[] = [];
  for (const value of values) {
    const key = typeof value === "string" ? value : JSON.stringify(value);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(value);
  }
  return out;
}
