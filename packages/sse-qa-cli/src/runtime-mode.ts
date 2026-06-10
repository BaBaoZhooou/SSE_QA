function env(name: string, fallback = ""): string {
  return (
    process.env[`SSE_QA_${name}`] ||
    process.env[`LFP_QA_${name}`] ||
    process.env[`QA_${name}`] ||
    fallback
  );
}

function isTruthy(value: string | undefined, defaultValue = false): boolean {
  if (value === undefined || value === "") return defaultValue;
  return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

/** MCP 加载时是否自动预热/启动后端（默认开启，SSE_QA_AUTO_START=0 关闭）。 */
export function isAutoStartEnabled(argv: string[] = process.argv): boolean {
  if (argv.includes("--no-auto-start")) return false;
  if (argv.includes("--auto-start")) return true;
  return isTruthy(env("AUTO_START"), true);
}

export function backendUrl(mode: "fast" | "thinking"): string {
  const defaults = {
    fast: "http://127.0.0.1:18018",
    thinking: "http://127.0.0.1:18019",
  };
  const keys = {
    fast: "FASTQA_URL",
    thinking: "THINKING_URL",
  };
  return env(keys[mode], defaults[mode]).replace(/\/+$/, "");
}
