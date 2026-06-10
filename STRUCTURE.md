# SSE_QA 仓库结构

## Agent-only 主路径

```text
SSE_QA/
├── packages/sse-qa-cli/       # @sse-qa/cli — 单包（CLI + MCP + runtime/backend）
├── fastQA/                    # 快答源码（sync 到 runtime/backend）
├── highThinkingQA/            # 深度思考源码
├── scripts/                   # 源码开发启停、sync-server-bundle.sh
├── config/                    # 源码开发 system.agent.yaml
├── 知识图谱/                  # Neo4j 导入脚本与数据
└── docs/agent-install.md      # npm 安装指南
```

**不包含 / 已移除**：MySQL、public-service、frontend、MinIO、patent 支线、Gateway、双 npm 包拆分。

## `@sse-qa/cli` 包内

```text
packages/sse-qa-cli/
├── dist/              # sse-qa CLI + MCP
├── src/               # TypeScript 源码
├── runtime/
│   ├── backend/       # sync 后的 fastQA + highThinkingQA
│   ├── docker/        # compose.yaml
│   ├── src/           # 配置渲染与启停（server 子命令委托）
│   └── templates/     # config.schema.json
└── examples/          # MCP 配置示例
```

## 遗留

- `gateway/`、`patent/`、`public-service/` — 历史全栈组件，Agent-only npm 路径不使用
