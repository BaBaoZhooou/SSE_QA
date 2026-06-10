# @sse-qa/cli

固态电解质（SSE）文献问答 — **单 npm 包**：CLI + MCP + 后端运行时（fastQA + highThinkingQA）。

- **npm**：[`@sse-qa/cli`](https://www.npmjs.com/package/@sse-qa/cli)
- **源码**： [github.com/BaBaoZhooou/SSE_QA](https://github.com/BaBaoZhooou/SSE_QA)
- **完整文档**：见仓库根目录 [README.md](https://github.com/BaBaoZhooou/SSE_QA/blob/main/README.md)

## 安装

```bash
npm install -g @sse-qa/cli
export PATH="$(npm config get prefix)/bin:$PATH"
# 若 prefix 为 ~/.npm-global：export PATH="$HOME/.npm-global/bin:$PATH"
```

若出现 `allow-scripts` 提示：

```bash
npm approve-scripts @sse-qa/cli
```

## 快速开始

```bash
sse-qa init
# 编辑 ~/.sse-qa/config.yaml 与 ~/.sse-qa/secrets.env（LLM_API_KEY 等）

sse-qa config validate
sse-qa server install
sse-qa server start
sse-qa doctor --json
```

### 注册 MCP（Claude）

```bash
SSE_QA_BIN="$(command -v sse-qa)"   # 建议绝对路径
claude mcp add sse-qa \
  --env SSE_QA_AUTO_START=1 \
  -- "$SSE_QA_BIN" mcp --auto-start
```

Cursor / Codex 示例：包内 `examples/`。

## 命令

| 命令 | 说明 |
|------|------|
| `init` | 生成 `~/.sse-qa/config.yaml` + `secrets.env` |
| `config show\|validate` | 查看 / 校验配置 |
| `doctor` / `setup-check` | 全量自检 + `user_guidance` |
| `server install\|start\|stop\|status` | 内嵌后端（Docker / native） |
| `mcp` | MCP stdio（Claude / Cursor / Codex） |
| `ask-fast` / `ask-thinking` | CLI 直连问答 |
| `health` | 后端健康检查 |

## MCP 工具

| 工具 | 说明 |
|------|------|
| `setup_check` | 配置与依赖自检 |
| `health_check` | 健康 + 配置摘要 |
| `ask_fast` | fastQA 文献快答 |
| `ask_thinking` | highThinkingQA 深度分析 |

## 用户自备（不在 npm 包内）

| 项 | 说明 |
|----|------|
| **LLM API Key** | `~/.sse-qa/secrets.env` → `LLM_API_KEY` |
| **Chroma 向量库** | `config.yaml` 中绝对路径；collection：`lfp_papers` / `md_papers` / `sse_literature` |
| **Neo4j** | 可选，图谱 QA |

从结构化 MD 批量入库（需 clone GitHub 仓库中的脚本）：

```bash
git clone https://github.com/BaBaoZhooou/SSE_QA ~/sse-qa
python3 ~/sse-qa/scripts/ingest_sse_md_chroma.py \
  --source /path/to/your/md_papers \
  --out ~/.sse-qa/data/chroma
```

## 包内结构

- `dist/` — `sse-qa` CLI + MCP
- `runtime/backend/` — fastQA、highThinkingQA Python 服务
- `runtime/docker/` — Docker Compose
- `runtime/templates/` — 配置 Schema
- `examples/` — MCP 配置示例

## 故障排查

| 现象 | 处理 |
|------|------|
| `sse-qa: command not found` | 将 `$(npm config get prefix)/bin` 加入 PATH |
| `Collection [lfp_papers] does not exist` | 运行 ingest 脚本或配置已有 Chroma 路径 |
| MCP 连接失败 | 使用 `sse-qa` 绝对路径；先 `sse-qa server start` |

更多见 [仓库 README §10 故障排查](https://github.com/BaBaoZhooou/SSE_QA#10-故障排查)。
