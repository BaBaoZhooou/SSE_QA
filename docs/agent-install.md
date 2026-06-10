# Agent 安装指南 — `@sse-qa/cli` 单包

面向 Claude / Cursor / Codex 的 **单 npm 包**安装流程。主文档见 [README.md](../README.md)。

## 包内容

`@sse-qa/cli` v0.3.0+ 包含：

| 组件 | 说明 |
|------|------|
| `sse-qa` CLI | init、doctor、setup-check、server 启停 |
| MCP Server | `sse-qa mcp`，stdio 协议，工具：setup_check / health_check / ask_fast / ask_thinking |
| 配置模板 | `sse-qa init` → `~/.sse-qa/config.yaml` + `secrets.env` |
| 后端运行时 | `runtime/backend/` 内 fastQA + highThinkingQA + 启停脚本 |
| Docker | `runtime/docker/compose.yaml`（Redis + 两后端） |

**不在 npm 内**：Chroma 向量文件、Neo4j 数据、LLM/Embedding API Key（用户填入 secrets.env）。

---

## 1. 安装

```bash
npm install -g @sse-qa/cli
```

本地开发（仓库内）：

```bash
bash scripts/sync-server-bundle.sh
cd packages/sse-qa-cli && npm install && npm run build && npm link
```

---

## 2. 初始化配置

```bash
sse-qa init
```

编辑 `~/.sse-qa/config.yaml`：

```yaml
chroma:
  fastqa:
    vector_db_path: /your/abs/path/to/vector_database
  thinking:
    persist_dir: /your/abs/path/to/vectordb
    collection_name: sse_literature
```

编辑 `~/.sse-qa/secrets.env`：

```env
LLM_API_KEY=sk-...
NEO4J_PASSWORD=your-neo4j-password
```

校验：

```bash
sse-qa config validate --json
sse-qa doctor
```

---

## 3. 启动后端

```bash
sse-qa server install    # native：创建 ~/.sse-qa/runtime/venv
sse-qa server start      # auto：有 Docker 则 compose，否则 native
sse-qa server status
```

---

## 4. 注册 MCP

**Claude Code：**

```bash
claude mcp add sse-qa \
  --env SSE_QA_AUTO_START=1 \
  -- sse-qa mcp --auto-start
```

**发布后 npx：**

```bash
claude mcp add sse-qa -- npx -y @sse-qa/cli mcp --auto-start
```

**Cursor / Codex：** 复制 [`examples/cursor.mcp.json`](../packages/sse-qa-cli/examples/cursor.mcp.json) 或 [`examples/codex.config.toml`](../packages/sse-qa-cli/examples/codex.config.toml)。

---

## 5. 验证

```bash
claude mcp list
sse-qa health --json
sse-qa setup-check
```

在 Claude 中调用 MCP 工具 `setup_check`，确认 `ready_for_qa: true` 后再提问。

---

## 故障排查

| 问题 | 处理 |
|------|------|
| 后端未就绪 | `sse-qa server start`；检查 Docker 或 Python venv |
| Chroma 路径错误 | 使用绝对路径；`sse-qa config validate` |
| MCP 无响应 | 确认 `sse-qa mcp --auto-start` 可手动运行 |
| 重装后异常 | `npm uninstall -g @sse-qa/cli && npm install -g @sse-qa/cli` |
