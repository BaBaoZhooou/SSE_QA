# 环境配置

## 文件说明

| 文件 | 是否提交 Git | 用途 |
|------|-------------|------|
| `config.shared.env` | 是 | LLM/Embedding 端点、检索参数、Gunicorn、CORS 等公共默认值 |
| `config.secret.env` | **否** | DashScope API Key、JWT_SECRET 等密钥 |
| `config.secret.env.example` | 是 | 密钥填写模板 |
| `.dockerignore` | 是 | Docker 镜像构建时的排除规则 |

## 使用方式

1. 复制模板：`cp config.secret.env.example config.secret.env`
2. 填写 `config.secret.env` 中的 API Key 与 JWT 密钥
3. 各服务启动时会按优先级加载 `config.shared.env` → `config.secret.env`，并与 `resource/config/services/<service>/` 合并

## 已删除

- `config.env.example` — 已废弃的单文件配置模板，已由 `config.shared.env` + `config.secret.env` 替代
