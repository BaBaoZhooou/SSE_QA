# 用自己的 GitHub / npm 账号发布

与 `zhuyinghua6961/agentReconstruct` **无关联**。`SSE_QA/` 是独立仓库，cowork 根目录的 `origin` 已移除。

## 1. GitHub（源码）

在 [BaBaoZhooou](https://github.com/BaBaoZhooou) 账号下新建空仓库 **`SSE_QA`**（不要 fork agentReconstruct）。

```bash
cd /home/lwb/projects/cowork/SSE_QA

# 首次：设置提交身份（改成你自己的）
git config user.name "Wenbo Li"
git config user.email "BaBaoZhooou@users.noreply.github.com"

# 若尚未 init，见下方「初始化」；已有 .git 则直接：
git remote add origin git@github.com:BaBaoZhooou/SSE_QA.git
# HTTPS: git remote add origin https://github.com/BaBaoZhooou/SSE_QA.git

git push -u origin main
git tag v0.3.1
git push origin v0.3.1
```

推送前在 GitHub 仓库 **Settings → Secrets** 添加 `NPM_TOKEN`（供 release workflow 发 npm）。

### 初始化（仅第一次）

```bash
cd /home/lwb/projects/cowork/SSE_QA
git init -b main
git add .
git commit -m "feat: agent-only SSE QA CLI+MCP v0.3.1"
```

## 2. npm（`@sse-qa/cli`）

在 **你的 npm 账号** 登录（勿用他人 token）：

```bash
npm login
npm whoami
```

作用域包 `@sse-qa/cli` 需要你在 [npmjs.com](https://www.npmjs.com) 创建组织 **`sse-qa`**（或用你的用户名作 scope，则需改 `package.json` 的 `name` 字段）。

```bash
cd packages/sse-qa-cli
bash ../../scripts/sync-server-bundle.sh
npm ci && npm run build && npm run test:smoke
npm publish --access public
```

本地 `~/.npmrc` 应只有 `prefix=~/.npm-global`，**不要**保留他人账号的 `//registry.npmjs.org/:_authToken`。

## 3. 与 cowork 的关系

| 目录 | Git |
|------|-----|
| `cowork/SSE_QA/` | **独立** `.git`，推到你自己的 GitHub |
| `cowork/` 根 | 旧 agentReconstruct 历史仍在本地，**已无 remote**；`SSE_QA/` 已从跟踪中排除 |
| `cowork/磷酸铁锂 QA 系统/` | 未纳入任何 remote，可按需另建仓 |

## 4. 发布后改 package.json（可选）

```json
"repository": {
  "type": "git",
  "url": "https://github.com/BaBaoZhooou/SSE_QA.git",
  "directory": "packages/sse-qa-cli"
}
```
