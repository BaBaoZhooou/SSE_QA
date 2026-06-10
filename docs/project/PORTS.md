# 端口说明

本地开发默认端口来自 `resource/config/shared/infrastructure.shared.env` 与各服务启动脚本。

## 应用服务（必启）

| 端口 | 服务 | 说明 |
|------|------|------|
| **5173** | `frontend-vue` | Vite 开发服务器；`/api/*` 代理到网关 |
| **8101** | `gateway` | 统一 API 网关，浏览器与前端的主要后端入口 |
| **8102** | `public-service` | 认证、会话、上传、文档、配额、管理 |
| **8008** | `fastQA` | 快速问答（fast 模式） |
| **8009** | `highThinkingQA` | 深度思考问答（thinking 模式） |
| **8010** | `patent` | 专利问答（patent 模式） |

启动顺序见 `scripts/start_all.sh`：`public-service` → `fastQA` → `highThinkingQA` → `patent` → `gateway`（含 admission worker）。

## 前端生产态（可选）

| 端口 | 服务 | 说明 |
|------|------|------|
| **9093** | nginx | `scripts/start_nginx_frontend.sh` 默认端口（`FRONTEND_NGINX_PORT`） |
| **8080** | frontend nginx | Docker 部署时内部前端容器（`FRONTEND_PUBLISH_PORT`） |
| **80 / 443** | edge nginx | Docker 部署 HTTPS 入口（`HTTP_PUBLISH_PORT` / `HTTPS_PUBLISH_PORT`） |

## 基础设施依赖（本地或 Docker）

| 端口 | 服务 | 说明 |
|------|------|------|
| **3306** | MySQL | 用户、会话、配额等持久化（`MYSQL_PORT`） |
| **6379** | Redis | 缓存、队列、分布式锁（`REDIS_PORT`） |
| **9000** | MinIO API | 对象存储（原文 PDF 等） |
| **9001** | MinIO Console | MinIO 管理界面 |
| **7687 / 7688** | Neo4j 文献库 | Bolt 协议；本地 `graph.shared.env` 常用 **7688** |
| **8687** | Neo4j 专利库 | 专利图谱 Bolt 端口（`PATENT_NEO4J_URL`） |
| **7474** | Neo4j Browser | HTTP 管理界面（Docker 内部） |

## 内部 / 可选外部服务

| 端口 | 服务 | 说明 |
|------|------|------|
| **8012** | PDF QA Sidecar | fastQA 容器内 PDF 处理 sidecar（`PDFQA_SIDECAR_BASE_URL_INTERNAL`） |
| **8000** | LLM | 外部 LLM 兼容接口（部署时 `LLM_BASE_URL`） |
| **8001** | Embedding | 外部向量嵌入服务（`QA_EMBEDDING_BASE_URL`） |
| **8084** | Rerank | 外部重排序服务（`RERANK_BASE_URL`） |

## 快速检查

```bash
# 从 cowork 根目录
bash scripts/status_all.sh

# 或进入项目目录
cd "磷酸铁锂 QA 系统"
bash scripts/status_all.sh
```

检查端口占用：

```bash
ss -ltn | rg "5173|8101|8102|8008|8009|8010|3306|6379|9000"
```
