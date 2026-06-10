# @sse-qa/cli

固态电解质（SSE）问答 — **单 npm 包**：CLI + MCP + 后端运行时。

## 安装

```bash
npm install -g @sse-qa/cli
```

## 快速开始

```bash
sse-qa init
# edit ~/.sse-qa/config.yaml and secrets.env
sse-qa server install && sse-qa server start
sse-qa doctor
claude mcp add sse-qa -- sse-qa mcp --auto-start
```

## 命令

| 命令 | 说明 |
|------|------|
| `init` | 生成 `~/.sse-qa/config.yaml` + `secrets.env` |
| `config validate` | 校验配置（含 Chroma 路径、API Key） |
| `doctor` / `setup-check` | 全量自检 + `user_guidance` |
| `server install\|start\|stop\|status` | 内嵌后端启停（Docker / native） |
| `mcp` | MCP stdio 服务（Claude/Cursor/Codex） |
| `ask-fast` / `ask-thinking` | CLI 直连问答 |
| `health` | 后端健康检查 |

## MCP 工具

- `setup_check` — 引导用户完成配置
- `health_check` — 健康 + setup 摘要
- `ask_fast` — fastQA
- `ask_thinking` — highThinkingQA

## 包内结构

- `dist/` — CLI + MCP
- `runtime/backend/` — fastQA + highThinkingQA Python 代码
- `runtime/docker/` — Docker Compose
- `runtime/templates/` — 配置 Schema
- `examples/` — MCP 配置示例

Chroma、Neo4j、API Key **不在包内**，由用户在 `~/.sse-qa/` 配置。

主文档：[../../README.md](../../README.md)
