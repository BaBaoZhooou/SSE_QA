# 发布指南 — Git 与 npm

> **账号**：推送到 **你自己的 GitHub / npm**，与 `agentReconstruct` 无关。详见 [`OWN_ACCOUNT_SETUP.md`](OWN_ACCOUNT_SETUP.md)。

## Git（源码仓库）

```bash
cd /path/to/cowork   # 或独立 SSE_QA 仓库根
git add SSE_QA/
git status            # 确认无 *.secret.env、无 neo4j/data、无 runtime/backend
git commit -m "feat(sse-qa): agent-only CLI+MCP single package v0.3.x"
git push origin main
```

**勿提交**：`~/.sse-qa/`、`.cursor/`、`.claude/`、`.codex`、`.superpowers/`、`**/*.secret.env`（仅保留 `*.example`）、Neo4j `data/`、Chroma 向量、`runtime/backend/`。

发布前运行：`bash scripts/audit-release-safety.sh`

## npm（`@sse-qa/cli`）

```bash
cd SSE_QA
bash scripts/sync-server-bundle.sh
cd packages/sse-qa-cli
npm ci
npm run build
npm run test:smoke
bash ../../scripts/audit-release-safety.sh
npm pack --dry-run
```

发布到 registry（需 `NPM_TOKEN`）：

```bash
npm publish --access public
```

或打 tag 触发 [`.github/workflows/release.yml`](.github/workflows/release.yml)：

```bash
git tag v0.3.2
git push origin v0.3.2
```

## 用户安装

```bash
npm install -g @sse-qa/cli
sse-qa init
# 编辑 ~/.sse-qa/config.yaml 与 secrets.env
sse-qa server start
claude mcp add sse-qa -- $(command -v sse-qa) mcp --auto-start
```

本地未发布时：`npm link` 见 [README.md §0](README.md#0-一键安装给-coding-agent)。
