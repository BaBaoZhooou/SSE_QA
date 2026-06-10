#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATE = "20260520"
DOC_DATE = "2026/05/20"
VERSION = "V1.0"


STYLE = """
<style>
@page {
  size: A4 portrait;
  margin: 2.54cm 2.54cm 2.54cm 2.54cm;
}
body {
  font-family: SimSun, "宋体", "Times New Roman", serif;
  font-size: 10.5pt;
  line-height: 1.5;
  color: #000;
  text-align: justify;
}
.cover {
  text-align: center;
  page-break-after: always;
  padding-top: 4.5cm;
}
.cover .system {
  font-family: SimHei, "黑体", "Microsoft YaHei", sans-serif;
  font-size: 18pt;
  font-weight: bold;
  margin-bottom: 0.8cm;
}
.cover .doc-title {
  font-family: SimHei, "黑体", "Microsoft YaHei", sans-serif;
  font-size: 22pt;
  font-weight: bold;
  margin-bottom: 3cm;
}
.cover .meta {
  font-size: 10.5pt;
  line-height: 1.8;
}
h1 {
  font-family: SimHei, "黑体", sans-serif;
  font-size: 16pt;
  font-weight: bold;
  margin: 12pt 0 6pt 0;
  line-height: 1.5;
  page-break-after: avoid;
}
h2 {
  font-family: SimHei, "黑体", sans-serif;
  font-size: 14pt;
  font-weight: bold;
  margin: 12pt 0 6pt 0;
  line-height: 1.5;
  page-break-after: avoid;
}
h3 {
  font-family: SimHei, "黑体", sans-serif;
  font-size: 10.5pt;
  font-weight: bold;
  margin: 6pt 0 3pt 0;
  line-height: 1.5;
  page-break-after: avoid;
}
p {
  margin: 0 0 6pt 0;
  text-indent: 2em;
}
.no-indent,
table p,
li p {
  text-indent: 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 6pt 0;
  font-size: 10.5pt;
  page-break-inside: auto;
}
th, td {
  border: 0.5pt solid #000;
  padding: 4pt 5pt;
  vertical-align: middle;
}
th {
  background: #eeeeee;
  font-weight: bold;
  text-align: center;
}
td.center {
  text-align: center;
}
td.left {
  text-align: left;
}
pre {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9pt;
  line-height: 1.2;
  background: #f2f2f2;
  border: 0.5pt solid #cccccc;
  padding: 6pt;
  margin: 3pt 0 6pt 0;
  white-space: pre-wrap;
}
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9pt;
}
ol, ul {
  margin-top: 0;
  margin-bottom: 6pt;
}
li {
  margin-bottom: 3pt;
}
.version-table td,
.version-table th {
  text-align: center;
}
.note {
  border-left: 3pt solid #999;
  padding-left: 8pt;
  margin: 6pt 0;
}
.page-break {
  page-break-before: always;
}
.diagram {
  border: 0.75pt solid #777;
  background: #fafafa;
  margin: 8pt 0 10pt 0;
  padding: 8pt;
  font-family: SimSun, "宋体", serif;
}
.diagram-title {
  font-family: SimHei, "黑体", sans-serif;
  font-weight: bold;
  text-align: center;
  margin-bottom: 6pt;
}
.diagram pre {
  border: 0;
  background: transparent;
  margin: 0;
}
.mermaid {
  font-family: Consolas, "Courier New", monospace;
  font-size: 9pt;
  line-height: 1.25;
  background: #f7f7f7;
  border: 0.5pt solid #bfbfbf;
  padding: 6pt;
  white-space: pre-wrap;
}
</style>
"""


def doc_shell(title: str, body: str) -> str:
    meta_by_title = {
        "部署手册": ("适用环境：Docker 离线部署环境", "文档对象：部署实施人员、现场运维人员"),
        "运维手册": ("适用环境：生产运行和日常运维环境", "文档对象：系统管理员、值班运维人员"),
        "用户手册": ("适用环境：LiFeO4Agent Web 使用环境", "文档对象：最终用户、系统管理员"),
        "系统概要设计说明书": ("适用环境：系统设计、评审和架构维护", "文档对象：项目负责人、架构师、开发和测试人员"),
        "系统详细设计说明书": ("适用环境：模块设计、编码实现和接口联调", "文档对象：开发人员、测试人员、维护人员"),
        "开发文档": ("适用环境：源码维护、二次开发和版本发布", "文档对象：开发人员、测试人员、技术维护人员"),
        "测试报告": ("适用环境：V1.0 交付测试和现场验收", "文档对象：测试人员、项目负责人、验收人员"),
        "需求清单": ("适用环境：V1.0 需求跟踪和验收确认", "文档对象：业务负责人、项目负责人、测试人员"),
    }
    meta_line_1, meta_line_2 = meta_by_title.get(
        title,
        ("适用环境：LiFeO4Agent 交付环境", "文档对象：项目相关人员"),
    )
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>LiFeO4Agent-{title}-{DATE}-{VERSION}</title>
{STYLE}
</head>
<body>
<div class="cover">
  <div class="system">LiFeO4Agent</div>
  <div class="doc-title">{title}</div>
  <div class="meta">
    <div>文档版本：{VERSION}</div>
    <div>文档日期：{DOC_DATE}</div>
    <div>{meta_line_1}</div>
    <div>{meta_line_2}</div>
  </div>
</div>
<h1>版本记录</h1>
<table class="version-table">
  <tr><th>版本</th><th>日期</th><th>修订人</th><th>修订说明</th></tr>
  <tr><td>{VERSION}</td><td>{DOC_DATE}</td><td>项目组</td><td>初版</td></tr>
</table>
{body}
</body>
</html>
"""


DEPLOYMENT_MANUAL = """
<h1>1 文档说明</h1>
<p>本文档用于指导 LiFeO4Agent 在目标服务器上的 Docker 离线部署、配置、启动、验证和更新。部署方只需要加载镜像包、放置数据包、填写 <code>deploy/.env</code>，再执行 docker compose 启动命令；不需要在宿主机额外安装 <code>mc</code>、<code>zstd</code> 或 <code>neo4j-admin</code>。</p>
<p>本文档不包含真实 API Key、密码、token。实际交付时，部署方应在 <code>deploy/.env</code> 中填写本环境真实值。</p>

<h1>2 交付包结构</h1>
<p>LiFeO4Agent 采用“运行镜像 + 版本化数据包 + compose 自动 seed”的混合交付方式。运行镜像负责服务运行，数据包负责原文、向量库和图谱数据，compose 中的 one-shot seed 容器负责自动导入。</p>
<table>
  <tr><th>路径</th><th>内容</th><th>说明</th></tr>
  <tr><td><code>deploy/docker-compose.yml</code></td><td>Compose 编排文件</td><td>定义业务服务、基础组件、seed job、网络和 named volume。</td></tr>
  <tr><td><code>deploy/.env</code></td><td>部署配置文件</td><td>部署方主要修改入口端口、账号密码、模型连接和数据包版本。</td></tr>
  <tr><td><code>deploy/lifeo4agent-images.tar</code></td><td>离线镜像包</td><td>通过 <code>docker load</code> 导入目标服务器。</td></tr>
  <tr><td><code>deploy/data/</code></td><td>离线数据包目录</td><td>包含 MinIO 原文、reference 向量库、Neo4j dump 和 manifest。</td></tr>
  <tr><td><code>deploy/certs/</code></td><td>HTTPS 证书目录</td><td>放置 <code>fullchain.pem</code> 和 <code>privkey.pem</code>。</td></tr>
  <tr><td><code>deploy/mysql-init/</code></td><td>MySQL 初始化 SQL</td><td>初始化 schema、部门基础数据和 bootstrap 管理员。</td></tr>
  <tr><td><code>deploy/scripts/</code></td><td>部署辅助脚本</td><td>包含预检、数据包校验、镜像导出和测试证书生成脚本。</td></tr>
</table>

<h1>3 运行环境要求</h1>
<table>
  <tr><th>项目</th><th>要求</th><th>说明</th></tr>
  <tr><td>操作系统</td><td>Linux 服务器</td><td>需支持 Docker Engine 和 Docker Compose v2。</td></tr>
  <tr><td>Docker</td><td>已安装 Docker Engine</td><td>部署命令使用 <code>docker compose</code> 子命令。</td></tr>
  <tr><td>磁盘空间</td><td>按镜像包和数据包大小预留</td><td><code>minio-originals.tar.zst</code> 当前约 49.3 GiB，解压导入后需预留更多空间。</td></tr>
  <tr><td>网络</td><td>部署机可被客户端访问</td><td>HTTP/HTTPS、MySQL、Redis、MinIO 端口是否开放由部署方决定。</td></tr>
  <tr><td>证书</td><td>HTTPS 证书和私钥</td><td>内网环境可使用部署方自签证书，域名需与证书 SAN 一致。</td></tr>
</table>

<h1>4 配置文件说明</h1>
<p>生产部署建议从模板生成实际配置：</p>
<pre>cp deploy/.env.production.example deploy/.env</pre>
<p>部署方主要修改以下配置项。</p>
<table>
  <tr><th>分类</th><th>变量</th><th>说明</th></tr>
  <tr><td>入口端口</td><td><code>HTTP_PUBLISH_PORT</code>、<code>HTTPS_PUBLISH_PORT</code></td><td>最外层 nginx edge 的 HTTP/HTTPS 宿主机端口。</td></tr>
  <tr><td>域名</td><td><code>HTTPS_SERVER_NAME</code>、<code>HTTPS_REDIRECT_HOST</code></td><td>HTTPS 域名和 HTTP 跳转目标。非标准端口可填写 <code>domain:port</code>。</td></tr>
  <tr><td>基础组件端口</td><td><code>MYSQL_PUBLISH_PORT</code>、<code>REDIS_PUBLISH_PORT</code>、<code>MINIO_API_PUBLISH_PORT</code>、<code>MINIO_CONSOLE_PUBLISH_PORT</code></td><td>MySQL、Redis、MinIO 对宿主机开放的端口。</td></tr>
  <tr><td>账号密码</td><td><code>MYSQL_ROOT_PASSWORD</code>、<code>MYSQL_APP_PASSWORD</code>、<code>REDIS_PASSWORD</code>、<code>MINIO_ROOT_PASSWORD</code></td><td>部署方应填写强密码。</td></tr>
  <tr><td>数据版本</td><td><code>DATA_PACKAGE_VERSION</code>、<code>DATA_SEED_FORCE</code></td><td>数据包版本和是否强制重导。</td></tr>
  <tr><td>大模型</td><td><code>LLM_BASE_URL</code>、<code>LLM_MODEL</code>、<code>LLM_API_KEY</code></td><td>问答生成模型连接配置。</td></tr>
  <tr><td>意图模型</td><td><code>INTENT_MODEL_ENABLED</code>、<code>INTENT_MODEL_BASE_URL</code>、<code>INTENT_MODEL</code>、<code>INTENT_MODEL_API_KEY</code></td><td>fastQA 和 patentQA 共用的意图识别模型。</td></tr>
  <tr><td>向量模型</td><td><code>QA_EMBEDDING_BASE_URL</code>、<code>QA_EMBEDDING_MODEL</code>、<code>HIGHTHINKINGQA_EMBEDDING_BASE_URL</code>、<code>HIGHTHINKINGQA_EMBEDDING_MODEL</code></td><td>fastQA/patentQA 和 highThinkingQA 的 embedding 模型连接配置。</td></tr>
  <tr><td>重排模型</td><td><code>RERANK_PROVIDER</code>、<code>RERANK_BASE_URL</code>、<code>RERANK_MODEL</code>、<code>RERANK_API_KEY</code></td><td>fastQA 和 patentQA 共用的 rerank 配置；不用时可设置为 <code>none</code>。</td></tr>
</table>
<p>Neo4j 地址由 compose 内部固定为 <code>bolt://neo4j-literature:7687</code> 和 <code>bolt://neo4j-patent:7687</code>，不暴露给部署方配置。</p>

<h1>5 HTTPS 与域名配置</h1>
<p>Compose 内置 <code>edge</code> nginx 作为最外层 HTTPS 入口。HTTP 入口会使用 308 跳转到 HTTPS；HTTPS 入口反向代理到内部 <code>frontend:80</code>。</p>
<p>部署方需要将证书放到以下路径：</p>
<pre>deploy/certs/fullchain.pem
deploy/certs/privkey.pem</pre>
<p>证书中的域名必须与 <code>HTTPS_SERVER_NAME</code> 一致。内网自签证书部署时，需要在客户端信任对应根证书，并通过内网 DNS 或 hosts 将域名解析到部署机 IP。</p>
<p>本地测试可执行：</p>
<pre>bash deploy/scripts/generate_dev_tls_cert.sh lifeo4.agent.test 172.19.14.204</pre>

<h1>6 离线镜像加载</h1>
<p>目标服务器收到镜像包后，执行：</p>
<pre>docker load -i deploy/lifeo4agent-images.tar</pre>
<p>镜像包包含业务服务、前端、seed-tools 和基础组件镜像。大体量原文、向量库和图谱数据不进入镜像包，而是放在 <code>deploy/data/</code>。</p>

<h1>7 数据包放置与自动导入</h1>
<p><code>deploy/data/</code> 应包含以下文件：</p>
<table>
  <tr><th>文件</th><th>内容</th><th>关键计数</th></tr>
  <tr><td><code>manifest.json</code></td><td>数据包版本、sha256、大小和计数</td><td>当前数据版本 <code>2026-05-19</code></td></tr>
  <tr><td><code>minio-originals.tar.zst</code></td><td>论文原文和专利原文</td><td>论文 7153，专利目录 14006，专利 tables 9581</td></tr>
  <tr><td><code>fastqa-ref.tar.zst</code></td><td>fastQA 向量库、md 向量库、topic index</td><td>Chroma SQLite 文件 2 个</td></tr>
  <tr><td><code>highthinking-ref.tar.zst</code></td><td>highThinkingQA vectordb</td><td>Chroma SQLite 文件 1 个</td></tr>
  <tr><td><code>patentqa-ref.tar.zst</code></td><td>专利向量库和 JSON-only 专利 archive</td><td>专利 JSON 目录 14006</td></tr>
  <tr><td><code>public-service-ref.tar.zst</code></td><td>public-service reference vector data</td><td>按 manifest 校验</td></tr>
  <tr><td><code>neo4j-literature.dump.zst</code></td><td>文献知识图谱 dump</td><td>由 Neo4j seed job 加载</td></tr>
  <tr><td><code>neo4j-patent.dump.zst</code></td><td>专利知识图谱 dump</td><td>由 Neo4j seed job 加载</td></tr>
</table>
<p>启动时，compose 会依次运行 MinIO、reference data 和 Neo4j 的 seed job。seed job 会写入版本 marker，同版本再次启动会跳过。需要强制重新导入时，将 <code>DATA_SEED_FORCE</code> 设置为 <code>1</code> 后重新启动。</p>

<h1>8 启动与停止</h1>
<p>部署前执行预检：</p>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env</pre>
<p>启动服务：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d</pre>
<p>查看容器状态：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</pre>
<p>停止服务：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml down</pre>
<p>停止服务不会删除 Docker named volume。只有执行带 <code>-v</code> 的 down 或手动删除 volume 才会清除数据库和已导入数据。</p>

<h1>9 初始化数据</h1>
<p>MySQL 首次初始化时会执行 <code>deploy/mysql-init/</code> 中的 SQL。初始化内容包括 schema、部门基础数据和默认管理员。</p>
<table>
  <tr><th>项目</th><th>说明</th></tr>
  <tr><td>数据库</td><td>创建 <code>agentcode</code> schema。</td></tr>
  <tr><td>部门</td><td>导入“电池材料技术研究中心”及下属“正极材料研究所”“装备工程化研究所”“材料应用研究所”等部门。</td></tr>
  <tr><td>默认管理员</td><td>创建用户名 <code>admin</code> 的管理员账号。初始密码由交付双方确认后使用，首次登录后应立即修改密码并设置安全问题。</td></tr>
</table>

<h1>10 访问地址</h1>
<table>
  <tr><th>入口</th><th>默认生产端口</th><th>说明</th></tr>
  <tr><td>系统 HTTPS</td><td><code>443</code></td><td>正式用户访问入口。</td></tr>
  <tr><td>系统 HTTP</td><td><code>80</code></td><td>跳转到 HTTPS。</td></tr>
  <tr><td>前端调试入口</td><td><code>8080</code></td><td>默认仅绑定本机地址，用于调试。</td></tr>
  <tr><td>MySQL</td><td><code>3306</code></td><td>如无运维需要，可不对业务网开放。</td></tr>
  <tr><td>Redis</td><td><code>6379</code></td><td>如无运维需要，可不对业务网开放。</td></tr>
  <tr><td>MinIO API</td><td><code>9000</code></td><td>对象存储 API。</td></tr>
  <tr><td>MinIO Console</td><td><code>9001</code></td><td>对象存储管理控制台。</td></tr>
</table>

<h1>11 更新部署</h1>
<p>如只更新某一个业务服务，例如 fastQA，仅需交付新的 fastQA 镜像和对应 tag，部署方加载新镜像后重启相关服务即可：</p>
<pre>docker load -i lifeo4agent-fastqa-update.tar
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d fastqa gateway frontend edge</pre>
<p>如更新数据包，需要替换 <code>deploy/data/</code> 中对应文件和 <code>manifest.json</code>，同步更新 <code>DATA_PACKAGE_VERSION</code>，再执行预检和 compose 启动。默认情况下新版本会导入；同版本如需重导，设置 <code>DATA_SEED_FORCE=1</code>。</p>

<h1>12 常见问题</h1>
<table>
  <tr><th>问题</th><th>排查方法</th></tr>
  <tr><td>HTTPS 访问证书不可信</td><td>确认客户端已信任自签根证书，证书 SAN 包含访问域名，hosts 或 DNS 解析到部署机 IP。</td></tr>
  <tr><td>seed job 失败</td><td>检查 <code>deploy/data/manifest.json</code>、数据包是否齐全、sha256 是否匹配，以及磁盘空间是否足够。</td></tr>
  <tr><td>模型调用失败</td><td>检查 <code>LLM_BASE_URL</code>、模型名、API Key，以及模型服务是否支持当前调用格式。</td></tr>
  <tr><td>向量检索异常</td><td>确认对应 reference data seed job 已成功完成，named volume 中存在 Chroma 数据库文件。</td></tr>
  <tr><td>MinIO 中没有原文</td><td>查看 <code>minio-seed</code> 日志，确认 <code>minio-originals.tar.zst</code> 已导入且 marker 版本正确。</td></tr>
</table>
"""

OPERATIONS_MANUAL = """
<h1>1 总则</h1>
<h2>1.1 目的</h2>
<p>本文档用于指导 LiFeO4Agent 部署后的日常运维、状态巡检、日志排查、启停、备份恢复和更新操作，帮助运维人员保持系统稳定运行。</p>
<h2>1.2 适用范围</h2>
<p>本文档适用于使用 <code>deploy/docker-compose.yml</code> 部署的 Docker 离线交付环境。系统采用 Docker named volume 保存运行数据，采用 <code>deploy/data/*.tar.zst</code> 保存离线 reference 数据包。</p>

<h1>2 系统及资源</h1>
<h2>2.1 系统信息</h2>
<table>
  <tr><th>项目</th><th>内容</th></tr>
  <tr><td>系统名称</td><td>LiFeO4Agent</td></tr>
  <tr><td>部署方式</td><td>Docker Compose 离线部署</td></tr>
  <tr><td>交付形态</td><td>Docker 镜像包 + 数据包 + compose 自动 seed</td></tr>
  <tr><td>主配置文件</td><td><code>deploy/.env</code></td></tr>
  <tr><td>编排文件</td><td><code>deploy/docker-compose.yml</code></td></tr>
</table>

<h2>2.2 服务清单</h2>
<table>
  <tr><th>服务</th><th>用途</th><th>对外端口</th><th>主要依赖</th></tr>
  <tr><td><code>edge</code></td><td>外层 HTTPS nginx 入口</td><td><code>HTTP_PUBLISH_PORT</code>、<code>HTTPS_PUBLISH_PORT</code></td><td>frontend、证书</td></tr>
  <tr><td><code>frontend</code></td><td>前端静态页面 nginx</td><td><code>FRONTEND_PUBLISH_PORT</code>，默认本机调试</td><td>gateway</td></tr>
  <tr><td><code>gateway</code></td><td>统一网关与后端代理</td><td>仅 compose 内部</td><td>public-service、fastQA、highThinkingQA、patentQA、Redis</td></tr>
  <tr><td><code>public-service</code></td><td>用户、鉴权、公共能力、文件代理</td><td>仅 compose 内部</td><td>MySQL、Redis、MinIO、文献图谱</td></tr>
  <tr><td><code>fastqa</code></td><td>文献快速问答后端</td><td>仅 compose 内部</td><td>Redis、MinIO、fastqa-ref、文献图谱、模型服务</td></tr>
  <tr><td><code>highthinkingqa</code></td><td>深度思考问答后端</td><td>仅 compose 内部</td><td>MySQL、Redis、MinIO、highthinking-ref、模型服务</td></tr>
  <tr><td><code>patent</code></td><td>专利问答后端</td><td>仅 compose 内部</td><td>MySQL、Redis、MinIO、patentqa-ref、专利图谱、模型服务</td></tr>
  <tr><td><code>mysql</code></td><td>业务关系数据库</td><td><code>MYSQL_PUBLISH_PORT</code></td><td><code>mysql_data</code></td></tr>
  <tr><td><code>redis</code></td><td>缓存、会话与任务状态</td><td><code>REDIS_PUBLISH_PORT</code></td><td><code>redis_data</code></td></tr>
  <tr><td><code>minio</code></td><td>论文/专利原文对象存储</td><td><code>MINIO_API_PUBLISH_PORT</code>、<code>MINIO_CONSOLE_PUBLISH_PORT</code></td><td><code>minio_data</code></td></tr>
  <tr><td><code>neo4j-literature</code></td><td>文献知识图谱</td><td>仅 compose 内部</td><td><code>neo4j_literature_data</code></td></tr>
  <tr><td><code>neo4j-patent</code></td><td>专利知识图谱</td><td>仅 compose 内部</td><td><code>neo4j_patent_data</code></td></tr>
</table>

<h2>2.3 Seed Job 清单</h2>
<table>
  <tr><th>Seed job</th><th>作用</th><th>完成标记</th></tr>
  <tr><td><code>minio-init</code></td><td>创建 MinIO bucket</td><td>容器成功退出</td></tr>
  <tr><td><code>minio-seed</code></td><td>导入论文和专利原文</td><td><code>_deploy/data-seed/minio-originals/&lt;version&gt;.done</code></td></tr>
  <tr><td><code>public-service-ref-seed</code></td><td>导入 public-service reference data</td><td><code>.deploy/data-seed/public-service-ref/&lt;version&gt;.done</code></td></tr>
  <tr><td><code>fastqa-ref-seed</code></td><td>导入 fastQA 向量库和 topic index</td><td><code>.deploy/data-seed/fastqa-ref/&lt;version&gt;.done</code></td></tr>
  <tr><td><code>highthinking-ref-seed</code></td><td>导入 highThinkingQA vectordb</td><td><code>.deploy/data-seed/highthinking-ref/&lt;version&gt;.done</code></td></tr>
  <tr><td><code>patentqa-ref-seed</code></td><td>导入专利向量库和 JSON-only archive</td><td><code>.deploy/data-seed/patentqa-ref/&lt;version&gt;.done</code></td></tr>
  <tr><td><code>neo4j-*-prepare</code></td><td>解压 Neo4j dump</td><td><code>/work/neo4j-dumps/*.ready</code></td></tr>
  <tr><td><code>neo4j-*-seed</code></td><td>加载 Neo4j dump</td><td><code>/data/.deploy/data-seed/&lt;package&gt;/&lt;version&gt;.done</code></td></tr>
</table>

<h2>2.4 数据卷清单</h2>
<table>
  <tr><th>Volume</th><th>用途</th><th>是否运行态数据</th></tr>
  <tr><td><code>mysql_data</code></td><td>MySQL 数据库</td><td>是</td></tr>
  <tr><td><code>redis_data</code></td><td>Redis AOF 持久化数据</td><td>是</td></tr>
  <tr><td><code>minio_data</code></td><td>MinIO bucket 和对象数据</td><td>是</td></tr>
  <tr><td><code>public_service_data</code></td><td>public-service 运行态文件和缓存</td><td>是</td></tr>
  <tr><td><code>fastqa_state</code>、<code>fastqa_runtime</code></td><td>fastQA 状态和运行缓存</td><td>是</td></tr>
  <tr><td><code>highthinking_state</code>、<code>highthinking_runtime</code></td><td>highThinkingQA 状态和运行缓存</td><td>是</td></tr>
  <tr><td><code>patentqa_runtime</code></td><td>patentQA 运行缓存</td><td>是</td></tr>
  <tr><td><code>fastqa_ref_data</code>、<code>highthinking_ref_data</code>、<code>patentqa_ref_data</code>、<code>public_service_ref_data</code></td><td>版本化 reference 数据</td><td>否，由数据包 seed 可重建</td></tr>
  <tr><td><code>neo4j_literature_data</code>、<code>neo4j_patent_data</code></td><td>两个 Neo4j 图谱数据库</td><td>否，初始图谱可由 dump 重建；运行后如产生业务写入则按运行态处理</td></tr>
</table>

<h1>3 日常巡检</h1>
<h2>3.1 容器状态巡检</h2>
<p>每日巡检建议执行：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</pre>
<p>重点确认 <code>mysql</code>、<code>redis</code>、<code>minio</code>、<code>neo4j-literature</code>、<code>neo4j-patent</code>、各业务后端、<code>gateway</code>、<code>frontend</code>、<code>edge</code> 处于运行状态。一次性 seed job 正常状态可以是 <code>Exited (0)</code>。</p>

<h2>3.2 访问巡检</h2>
<ol>
  <li>访问 HTTPS 域名，确认页面可打开且证书状态符合部署方要求。</li>
  <li>使用管理员账号登录，确认登录流程正常。</li>
  <li>分别发起文献问答、深度思考问答和专利问答小样例，确认流式回答和阶段信息正常。</li>
  <li>打开 MinIO Console，确认 bucket 存在，论文和专利原文目录可见。</li>
</ol>

<h2>3.3 数据包和 seed 巡检</h2>
<p>如发生数据导入异常，先执行预检：</p>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env</pre>
<p>也可以单独校验数据包 manifest 和 sha256：</p>
<pre>python deploy/scripts/validate_data_packages.py --data-dir deploy/data --require-all --expected-version 2026-05-19</pre>

<h2>3.4 日志巡检</h2>
<p>查看所有服务近期日志：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200</pre>
<p>查看单个服务日志：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 fastqa
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 patent
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 minio-seed</pre>
<p>重点关注模型调用 4xx/5xx、向量库加载失败、MinIO 连接失败、Redis 认证失败、Neo4j healthcheck 失败等异常。</p>

<h1>4 系统启停运维</h1>
<h2>4.1 启动</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d</pre>
<h2>4.2 停止</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml down</pre>
<h2>4.3 重启单个服务</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d fastqa
docker compose --env-file deploy/.env -f deploy/docker-compose.yml restart gateway</pre>
<h2>4.4 强制重导数据</h2>
<p>如需重新导入 MinIO 原文、reference data 或 Neo4j dump，将 <code>DATA_SEED_FORCE</code> 设置为 <code>1</code>，再执行：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d</pre>
<p>重导完成后，应将 <code>DATA_SEED_FORCE</code> 改回 <code>0</code>，避免后续重启重复覆盖 reference 数据。</p>

<h1>5 备份恢复</h1>
<h2>5.1 推荐备份对象</h2>
<table>
  <tr><th>对象</th><th>备份建议</th><th>说明</th></tr>
  <tr><td><code>deploy/.env</code></td><td>每次变更后备份</td><td>包含运行配置，备份文件应按密级管理。</td></tr>
  <tr><td><code>deploy/certs/</code></td><td>证书变更后备份</td><td>私钥文件需严格保护。</td></tr>
  <tr><td><code>mysql_data</code></td><td>定期数据库备份</td><td>包含用户、会话、权限和业务运行数据。</td></tr>
  <tr><td><code>minio_data</code></td><td>按对象存储策略备份</td><td>包含原文对象和 seed marker。</td></tr>
  <tr><td><code>redis_data</code></td><td>按需备份</td><td>包含 AOF 持久化缓存状态。</td></tr>
  <tr><td>数据包</td><td>保留原始 <code>deploy/data/*.tar.zst</code></td><td>reference 数据和图谱初始数据可由数据包重建。</td></tr>
</table>

<h2>5.2 MySQL 备份示例</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml exec mysql \
  mysqldump -uroot -p agentcode > agentcode-backup.sql</pre>
<p>执行备份时需要输入 MySQL root 密码。备份文件应加密保存。</p>

<h2>5.3 MinIO 备份说明</h2>
<p>MinIO 原始数据来源于 <code>minio-originals.tar.zst</code>，首次导入可由 seed job 重建。若运行期间产生新增对象，应按部署方对象存储备份策略备份 <code>minio_data</code> volume 或使用 MinIO 客户端进行镜像备份。</p>

<h2>5.4 恢复注意事项</h2>
<p>不要在未确认的情况下执行 <code>docker compose down -v</code> 或删除 named volume。该操作会清除数据库、对象存储和运行态数据。</p>

<h1>6 更新运维</h1>
<h2>6.1 单服务更新</h2>
<p>只更新某一服务时，加载新镜像后重启该服务及必要上游服务。例如更新 fastQA：</p>
<pre>docker load -i lifeo4agent-fastqa-update.tar
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d fastqa gateway frontend edge</pre>
<h2>6.2 数据包更新</h2>
<p>替换 <code>deploy/data/</code> 中的数据包和 <code>manifest.json</code> 后，更新 <code>DATA_PACKAGE_VERSION</code>，执行预检，再启动 compose。版本变化时 seed job 会按新版本导入。</p>

<h1>7 故障排查</h1>
<table>
  <tr><th>现象</th><th>可能原因</th><th>处理建议</th></tr>
  <tr><td>页面无法访问</td><td>edge 未启动、端口未开放、域名未解析</td><td>检查 <code>edge</code> 日志、端口映射、DNS/hosts。</td></tr>
  <tr><td>登录失败</td><td>MySQL 未就绪、账号状态异常、JWT 配置异常</td><td>检查 <code>mysql</code> 和 <code>public-service</code> 日志。</td></tr>
  <tr><td>问答无响应</td><td>模型服务不可达、API Key 错误、后端异常</td><td>检查对应后端日志和 <code>LLM_*</code>、embedding、rerank 配置。</td></tr>
  <tr><td>检索结果为空</td><td>reference 数据未导入或模型配置不匹配</td><td>检查 seed job 是否成功，确认 Chroma 数据库文件存在。</td></tr>
  <tr><td>原文下载失败</td><td>MinIO 原文未导入或 bucket 配置错误</td><td>检查 <code>minio-init</code>、<code>minio-seed</code> 日志和 bucket 内容。</td></tr>
  <tr><td>图谱查询异常</td><td>Neo4j dump 未加载或 healthcheck 未通过</td><td>检查 <code>neo4j-*-prepare</code>、<code>neo4j-*-seed</code>、<code>neo4j-*</code> 日志。</td></tr>
</table>
"""

USER_MANUAL = """
<h1>1 文档说明</h1>
<p>本文档面向 LiFeO4Agent 的最终用户和管理员，说明系统登录、注册、问答、文件上传、原文查看、个人中心和管理员后台的常用操作。</p>

<h1>2 登录与账号</h1>
<h2>2.1 登录系统</h2>
<ol>
  <li>在浏览器中打开部署方提供的 HTTPS 地址。</li>
  <li>进入登录页后输入用户名和密码。</li>
  <li>点击“登录”。普通用户登录后进入问答首页，管理员登录后进入管理员后台。</li>
</ol>
<p>首次登录或账号信息未补全时，系统会提示用户前往个人中心完成改密、安全问题、部门或人员信息绑定。</p>

<h2>2.2 注册账号</h2>
<ol>
  <li>在登录页点击“注册账号”。</li>
  <li>填写用户名、密码和确认密码。密码至少 8 位，并且数字、小写字母、大写字母、特殊符号中至少包含 3 类。</li>
  <li>填写工号、姓名和校验码。部门信息会根据已维护的人员记录自动带出。</li>
  <li>设置 1 到 3 个安全问题和答案。</li>
  <li>提交注册。注册成功后系统自动进入首页。</li>
</ol>

<h2>2.3 找回密码</h2>
<ol>
  <li>在登录页点击“忘记密码”。</li>
  <li>输入用户名，系统会检查该账号是否设置了安全问题。</li>
  <li>回答安全问题并输入新密码。</li>
  <li>重置成功后返回登录页，使用新密码登录。</li>
</ol>
<p>如果账号未设置安全问题，需要联系管理员重置密码。</p>

<h1>3 问答首页</h1>
<h2>3.1 新建和切换对话</h2>
<ol>
  <li>点击左侧“新建对话”创建新会话。</li>
  <li>左侧历史列表会显示最近会话和已置顶会话。</li>
  <li>点击历史会话可切换上下文；生成中会话不建议删除或置顶。</li>
  <li>可对会话进行置顶、取消置顶或删除操作。</li>
</ol>

<h2>3.2 选择问答模式</h2>
<table>
  <tr><th>模式</th><th>适用场景</th><th>说明</th></tr>
  <tr><td>文献</td><td>快速文献问答、文献检索</td><td>调用 fastQA 后端，优先使用文献向量库和文献原文。</td></tr>
  <tr><td>深度</td><td>需要分解、推理和综合回答的问题</td><td>调用 highThinkingQA 后端，适合复杂问题分析。</td></tr>
  <tr><td>专利</td><td>专利检索、专利表格和附图相关问答</td><td>调用 patentQA 后端，使用专利向量库、专利原文和专利图谱。</td></tr>
</table>
<p>问答模式位于输入框上方的“问答模式”工具栏。选择后，本轮提问会按当前模式发送。</p>

<h2>3.3 发起问答</h2>
<ol>
  <li>在输入框中输入问题。</li>
  <li>确认问答模式。</li>
  <li>点击发送或按 Enter 发送。</li>
  <li>系统会流式返回回答，并在回答过程中显示阶段信息和用时。</li>
</ol>
<p>回答消息中可能包含引用、原文入口、阶段进度和总耗时。若某阶段异常，页面会显示相应错误信息，用户可稍后重试或联系管理员排查。</p>

<h1>4 文件上传与原文查看</h1>
<h2>4.1 上传文件</h2>
<p>问答首页支持上传 PDF、Excel 和 CSV 文件。上传入口位于输入框附近的文件按钮。</p>
<ol>
  <li>点击上传按钮。</li>
  <li>选择 PDF、Excel 或 CSV 文件。</li>
  <li>等待上传进度完成。</li>
  <li>上传成功后，文件会出现在“已上传的文件”列表中。</li>
</ol>
<p>文件大小和可用次数受后端配额系统控制。如达到限制，页面会显示配额提示。</p>

<h2>4.2 选择本轮参与问答的文件</h2>
<ol>
  <li>在“已上传的文件”列表中勾选需要参与本轮问答的文件。</li>
  <li>输入问题并发送。</li>
  <li>系统会结合勾选文件和知识库内容回答。</li>
</ol>

<h2>4.3 下载和删除文件</h2>
<ol>
  <li>点击文件列表中的“下载”可下载已上传文件。</li>
  <li>点击删除按钮可从当前会话中移除文件。</li>
  <li>生成回答过程中，为避免上下文变化，不建议删除文件。</li>
</ol>

<h2>4.4 查看文献或专利原文</h2>
<p>回答中的引用或原文入口会调用 MinIO 中的论文和专利原文。点击后可在页面内打开 PDF 阅读器，查看原文内容。部分文档支持翻译、复制和定位引用位置。</p>

<h1>5 个人中心</h1>
<h2>5.1 查看个人信息</h2>
<p>用户可在个人中心查看用户名、角色、人员绑定状态、部门信息和配额使用情况。</p>

<h2>5.2 修改用户名</h2>
<ol>
  <li>进入个人中心。</li>
  <li>点击用户名编辑入口。</li>
  <li>输入新用户名并保存。</li>
</ol>
<p>用户名长度应在 3 到 50 个字符之间，且不能以 <code>admin</code> 开头。</p>

<h2>5.3 修改密码和安全问题</h2>
<ol>
  <li>进入个人中心。</li>
  <li>在密码区域输入旧密码和新密码。</li>
  <li>在安全问题区域设置或更新问题和答案。</li>
  <li>保存后重新确认登录状态。</li>
</ol>
<p>首次登录时，系统会强制要求完成必要的密码和安全问题设置。</p>

<h2>5.4 绑定人员信息</h2>
<p>如系统提示需要绑定人员信息，用户需填写工号、姓名和校验码。绑定成功后，部门信息会从人员记录中同步。</p>

<h1>6 管理员后台</h1>
<p>管理员登录后进入 <code>/admin</code>，后台包含用户管理、部门管理和配额管理。</p>

<h2>6.1 用户管理</h2>
<p>管理员可查看用户列表，创建用户，修改用户密码，启用或停用用户，批量导入用户，修改用户名，绑定或调整人员记录。</p>
<p>普通业务用户分为超级用户和普通用户。管理员账号拥有系统管理权限，禁止普通用户访问管理员后台。</p>

<h2>6.2 部门管理</h2>
<p>管理员可维护一级、二级、三级部门字典，支持新增、修改、启用、停用和批量导入。停用部门不会清空已有用户绑定，只会禁止后续新选择。</p>

<h2>6.3 人员管理</h2>
<p>管理员可维护人员记录，包括工号、姓名、状态、部门和绑定账号关系。用户注册和个人中心绑定人员时会校验人员记录和校验码。</p>

<h2>6.4 配额管理</h2>
<p>管理员可维护标准配额类型，包括普通问答、文件问答、查看原文和文档辅助。配额可用于限制用户在周期内的功能使用次数。</p>

<h1>7 常见问题</h1>
<table>
  <tr><th>问题</th><th>处理方式</th></tr>
  <tr><td>无法登录</td><td>确认用户名和密码正确；如账号被锁定，等待锁定时间结束或联系管理员。</td></tr>
  <tr><td>首次登录后无法进入首页</td><td>根据提示到个人中心完成改密、安全问题、部门或人员信息补全。</td></tr>
  <tr><td>注册时提示人员信息错误</td><td>确认工号、姓名和校验码与管理员维护的人员记录一致。</td></tr>
  <tr><td>问答次数已用完</td><td>联系管理员调整配额或等待下一个配额周期。</td></tr>
  <tr><td>文件上传失败</td><td>确认文件类型为 PDF、Excel 或 CSV，并检查文件大小和配额限制。</td></tr>
  <tr><td>原文无法打开</td><td>联系管理员检查 MinIO 原文数据是否已导入。</td></tr>
</table>
"""

SUMMARY_DESIGN = """
<h1>1 简介</h1>
<h2>1.1 编写目的</h2>
<p>本文档描述 LiFeO4Agent 的总体设计，包括系统目标、功能模块、软件架构、集成方式、部署架构、数据库设计和非功能设计，为详细设计、开发、测试和运维提供依据。</p>

<h2>1.2 名词术语</h2>
<table>
  <tr><th>术语</th><th>说明</th></tr>
  <tr><td>fastQA</td><td>文献快速问答后端，负责文献检索、文件问答和文献知识图谱相关能力。</td></tr>
  <tr><td>highThinkingQA</td><td>深度思考问答后端，负责复杂问题的分解、推理和综合回答。</td></tr>
  <tr><td>patentQA</td><td>专利问答后端，负责专利检索、专利原文、专利表格和专利图谱相关能力。</td></tr>
  <tr><td>Reference Data</td><td>各问答服务运行所需的向量库、索引和 JSON-only archive。</td></tr>
  <tr><td>Seed Job</td><td>compose 启动时一次性执行的数据导入容器。</td></tr>
</table>

<h1>2 项目简介</h1>
<p>LiFeO4Agent 面向磷酸铁锂材料相关知识问答场景，提供文献问答、深度思考问答、专利问答、原文查看、文件问答、用户管理、部门管理和配额管理能力。</p>
<p>系统目标是将论文、专利、向量库和知识图谱能力封装为可离线交付的 Docker 部署包，使部署方通过少量配置即可完成内网部署和后续升级。</p>

<h1>3 系统架构设计</h1>
<h2>3.1 总体架构</h2>
<p>系统采用前后端分离和多后端服务架构。用户通过 HTTPS 访问 edge nginx，前端页面请求 gateway，gateway 根据认证、会话、文件上下文和问答模式将请求分发到 public-service、fastQA、highThinkingQA 或 patentQA。</p>
<table>
  <tr><th>层级</th><th>组件</th><th>职责</th></tr>
  <tr><td>访问层</td><td>edge nginx、frontend nginx</td><td>提供 HTTPS 入口和前端静态资源服务。</td></tr>
  <tr><td>网关层</td><td>gateway</td><td>统一认证代理、问答路由、SSE 转发、配额预检和会话持久化协调。</td></tr>
  <tr><td>公共能力层</td><td>public-service</td><td>用户、部门、人员、配额、会话、上传文件、原文代理和公共文档能力。</td></tr>
  <tr><td>问答服务层</td><td>fastQA、highThinkingQA、patentQA</td><td>分别处理文献、深度思考和专利问答。</td></tr>
  <tr><td>数据层</td><td>MySQL、Redis、MinIO、Neo4j、Chroma 数据</td><td>提供关系数据、缓存、对象存储、知识图谱和向量检索数据。</td></tr>
</table>

<h2>3.2 功能模块说明</h2>
<table>
  <tr><th>模块</th><th>功能</th><th>设计说明</th></tr>
  <tr><td>用户与鉴权</td><td>登录、注册、找回密码、安全问题、人员绑定</td><td>由 public-service 统一提供，gateway 代理访问。</td></tr>
  <tr><td>管理员后台</td><td>用户、部门、人员、配额管理</td><td>仅管理员可访问，支持批量导入。</td></tr>
  <tr><td>会话管理</td><td>会话列表、消息、文件、标题、删除</td><td>会话数据存储在 MySQL，并通过 outbox 同步文件化状态。</td></tr>
  <tr><td>文献问答</td><td>文献检索、文献原文、文件问答</td><td>fastQA 使用文献向量库、MinIO 原文和文献图谱。</td></tr>
  <tr><td>深度问答</td><td>复杂问题分解和综合回答</td><td>highThinkingQA 使用独立向量库和 LLM 进行多阶段推理。</td></tr>
  <tr><td>专利问答</td><td>专利检索、表格、附图、专利图谱</td><td>patentQA 使用专利向量库、JSON archive、MinIO 原文和专利图谱。</td></tr>
  <tr><td>文件和原文</td><td>上传 PDF/Excel/CSV，查看论文/专利原文</td><td>上传文件走 public-service；权威原文统一保存在 MinIO。</td></tr>
</table>

<h1>4 软件架构</h1>
<h2>4.1 技术组件</h2>
<table>
  <tr><th>技术组件</th><th>应用场景</th><th>说明</th></tr>
  <tr><td>Vue 3 + Vite</td><td>前端应用</td><td>实现问答界面、登录注册、个人中心和管理员后台。</td></tr>
  <tr><td>FastAPI</td><td>gateway、public-service、QA 后端</td><td>提供 REST API 和 SSE 流式回答能力。</td></tr>
  <tr><td>MySQL</td><td>关系数据</td><td>用户、部门、人员、会话、配额等业务数据。</td></tr>
  <tr><td>Redis</td><td>缓存和运行状态</td><td>配额、队列、任务、会话执行状态和分布式协调。</td></tr>
  <tr><td>MinIO</td><td>对象存储</td><td>论文和专利原文的权威存储。</td></tr>
  <tr><td>Neo4j</td><td>知识图谱</td><td>文献图谱和专利图谱分别独立部署。</td></tr>
  <tr><td>Chroma</td><td>向量库</td><td>文献、深度问答、专利等 reference data。</td></tr>
  <tr><td>Docker Compose</td><td>部署编排</td><td>编排运行容器、seed job、网络和 named volume。</td></tr>
</table>

<h2>4.2 数据流</h2>
<ol>
  <li>用户在前端选择问答模式并提交问题。</li>
  <li>gateway 根据模式、文件上下文和配额状态做路由决策。</li>
  <li>请求被转发到对应 QA 服务，QA 服务读取向量库、MinIO 原文、Neo4j 图谱和模型服务。</li>
  <li>后端通过 SSE 返回阶段事件、引用信息和最终答案。</li>
  <li>gateway 和 public-service 负责会话消息和文件元数据持久化。</li>
</ol>

<h1>5 部署架构</h1>
<p>部署采用 Docker Compose 单机离线部署。所有服务运行在同一个 compose bridge 网络内，内部服务通过 service name 互联。对外主要暴露 HTTPS 入口，以及按部署方要求暴露 MySQL、Redis、MinIO 端口。</p>
<p>数据导入通过 one-shot seed job 完成：MinIO 原文导入 bucket，reference 数据导入 named volume，Neo4j dump 通过官方 Neo4j 镜像加载到图谱 volume。</p>

<h1>6 数据库设计</h1>
<p>MySQL schema 包含用户、密码历史、安全问题、部门、人员、会话、会话文件、会话消息、quota 配置和 quota 使用表。部门基础 seed 只包含“电池材料技术研究中心”及其下属部门，不导入测试部门。用户运行数据、会话数据和配额使用数据属于部署方运行态数据。</p>

<h1>7 非功能设计</h1>
<table>
  <tr><th>类别</th><th>设计说明</th></tr>
  <tr><td>安全性</td><td>使用 JWT 鉴权、管理员权限控制、密码哈希、安全问题、内部服务 token 和 HTTPS 入口。</td></tr>
  <tr><td>可维护性</td><td>配置集中在 <code>deploy/.env</code>；业务镜像、基础镜像和数据包分离。</td></tr>
  <tr><td>可升级性</td><td>单服务变更可只替换对应镜像；数据变更通过版本化数据包和 marker 控制导入。</td></tr>
  <tr><td>可靠性</td><td>基础组件使用 named volume；seed job 幂等；healthcheck 控制依赖启动顺序。</td></tr>
  <tr><td>性能</td><td>向量库本地 volume 挂载，原文 MinIO 统一存储，Redis 提供缓存和运行态协调。</td></tr>
</table>
"""

DETAILED_DESIGN = """
<h1>1 文档说明</h1>
<p>本文档在概要设计基础上进一步描述 LiFeO4Agent 的模块划分、接口设计、数据设计、重点流程、异常处理和测试设计。</p>

<h1>2 功能模块划分</h1>
<table>
  <tr><th>模块</th><th>子模块</th><th>主要文件或服务</th></tr>
  <tr><td>前端</td><td>路由、问答页、个人中心、管理员后台</td><td><code>frontend-vue/src/router</code>、<code>frontend-vue/src/views</code>、<code>frontend-vue/src/components</code></td></tr>
  <tr><td>gateway</td><td>路由、SSE 代理、配额代理、会话持久化协调</td><td><code>gateway/app/routers</code>、<code>gateway/app/services</code></td></tr>
  <tr><td>public-service</td><td>鉴权、用户、部门、人员、配额、上传、文档代理、会话</td><td><code>public-service/backend/app/modules</code></td></tr>
  <tr><td>fastQA</td><td>文献问答、文件问答、文献图谱、检索</td><td><code>fastQA/app/modules</code>、<code>fastQA/app/routers</code></td></tr>
  <tr><td>highThinkingQA</td><td>深度问答、向量检索、答案综合</td><td><code>highThinkingQA/agent_core</code>、<code>highThinkingQA/server_fastapi</code></td></tr>
  <tr><td>patentQA</td><td>专利问答、专利原文、表格、图谱</td><td><code>patent/server/patent</code>、<code>patent/server_fastapi</code></td></tr>
  <tr><td>部署</td><td>镜像、数据包、seed、HTTPS</td><td><code>deploy/docker-compose.yml</code>、<code>deploy/scripts</code>、<code>deploy/seed-tools</code></td></tr>
</table>

<h1>3 前端设计</h1>
<h2>3.1 页面路由</h2>
<table>
  <tr><th>路径</th><th>页面</th><th>权限</th></tr>
  <tr><td><code>/login</code></td><td>登录页</td><td>游客</td></tr>
  <tr><td><code>/register</code></td><td>注册页</td><td>游客</td></tr>
  <tr><td><code>/forgot-password</code></td><td>找回密码</td><td>游客</td></tr>
  <tr><td><code>/</code></td><td>问答首页</td><td>登录用户</td></tr>
  <tr><td><code>/profile</code></td><td>个人中心</td><td>登录用户</td></tr>
  <tr><td><code>/admin</code></td><td>管理员后台</td><td>管理员</td></tr>
</table>
<h2>3.2 问答页面</h2>
<p>问答页面包含左侧会话列表、中间消息流、右侧问题大纲和底部输入区。输入区提供文献、深度、专利三种问答模式，以及 PDF/Excel/CSV 上传入口。</p>

<h1>4 接口设计</h1>
<h2>4.1 gateway 对外接口</h2>
<table>
  <tr><th>接口组</th><th>路径</th><th>说明</th></tr>
  <tr><td>问答</td><td><code>/api/{fast|thinking|patent}/ask</code>、<code>/api/{fast|thinking|patent}/ask_stream</code></td><td>同步问答和流式问答。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/*</code></td><td>登录、注册、当前用户、密码、安全问题、部门和人员绑定。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations/*</code></td><td>会话、消息和会话文件管理。</td></tr>
  <tr><td>上传</td><td><code>/api/upload_pdf</code>、<code>/api/upload_excel</code></td><td>PDF、Excel、CSV 文件上传。</td></tr>
  <tr><td>原文</td><td><code>/api/view_pdf/{doi}</code>、<code>/api/patent/original/{id}</code></td><td>论文和专利原文代理。</td></tr>
  <tr><td>管理</td><td><code>/api/admin/*</code></td><td>用户、部门、人员管理。</td></tr>
  <tr><td>配额</td><td><code>/api/quota/*</code></td><td>用户配额和管理员配额配置。</td></tr>
</table>

<h2>4.2 问答流式协议</h2>
<p>问答流式接口使用 SSE 返回，事件中包含阶段进度、引用、原文定位、错误、完成状态和最终回答。前端根据事件增量渲染消息，并统计阶段耗时和总耗时。</p>

<h1>5 数据设计</h1>
<h2>5.1 MySQL 表</h2>
<table>
  <tr><th>表</th><th>用途</th></tr>
  <tr><td><code>users</code></td><td>账号、角色、状态、部门和人员绑定。</td></tr>
  <tr><td><code>password_history</code></td><td>密码历史。</td></tr>
  <tr><td><code>user_security_questions</code></td><td>安全问题和答案哈希。</td></tr>
  <tr><td><code>primary_departments</code>、<code>secondary_departments</code>、<code>tertiary_departments</code></td><td>三级部门字典。</td></tr>
  <tr><td><code>personnel_records</code></td><td>人员记录、校验码哈希和部门绑定。</td></tr>
  <tr><td><code>conversations</code>、<code>conversation_messages</code>、<code>conversation_files</code></td><td>会话、消息和文件元数据。</td></tr>
  <tr><td><code>quota_configs</code>、<code>user_quota_usage</code>、<code>user_quota_overrides</code></td><td>配额配置、使用记录和用户覆盖配置。</td></tr>
</table>

<h2>5.2 对象存储结构</h2>
<p>MinIO bucket 中包含 <code>papers/</code> 和 <code>patent/originals/</code>。专利原文目录中包含 manifest、PDF、图片、结构化内容和 <code>structured/tables.json</code>。</p>

<h2>5.3 Reference Data</h2>
<table>
  <tr><th>数据包</th><th>挂载目标</th><th>服务使用方式</th></tr>
  <tr><td><code>fastqa-ref.tar.zst</code></td><td><code>/ref/fastqa</code></td><td>fastQA 读取向量库、md 向量库、community vector DB 和 topic index。</td></tr>
  <tr><td><code>highthinking-ref.tar.zst</code></td><td><code>/ref/highthinkingqa</code></td><td>highThinkingQA 读取 <code>vectordb</code>。</td></tr>
  <tr><td><code>patentqa-ref.tar.zst</code></td><td><code>/app/resource/patentQA</code></td><td>patentQA 读取专利向量库和 JSON-only archive。</td></tr>
  <tr><td><code>public-service-ref.tar.zst</code></td><td><code>/ref/public-service</code></td><td>public-service 读取公共 reference vector data。</td></tr>
</table>

<h1>6 重点流程设计</h1>
<h2>6.1 启动 seed 流程</h2>
<ol>
  <li>MySQL、Redis、MinIO 启动。</li>
  <li>MinIO init 创建 bucket。</li>
  <li>MinIO seed 导入原文数据并写入 marker。</li>
  <li>reference seed 解压各服务向量库到 named volume。</li>
  <li>Neo4j prepare 解压 dump，Neo4j seed 加载图谱。</li>
  <li>各业务服务等待依赖完成后启动。</li>
</ol>

<h2>6.2 问答流程</h2>
<ol>
  <li>前端发送问题、会话 ID、用户 ID、模式、历史消息和文件上下文。</li>
  <li>gateway 拉取会话文件，解析文件上下文并进行路由决策。</li>
  <li>gateway 执行配额预检，成功后转发到目标 QA 后端。</li>
  <li>QA 后端执行检索、重排、图谱补充和答案生成。</li>
  <li>gateway 转发 SSE 事件，最终完成配额 finalize 和会话持久化。</li>
</ol>

<h1>7 异常处理设计</h1>
<table>
  <tr><th>异常</th><th>处理策略</th></tr>
  <tr><td>模型调用失败</td><td>后端返回结构化错误，前端展示失败消息；运维检查模型配置。</td></tr>
  <tr><td>配额不足</td><td>gateway 或 public-service 返回配额错误，前端展示配额卡片。</td></tr>
  <tr><td>文件选择不明确</td><td>gateway 要求澄清，前端提示用户重新选择文件。</td></tr>
  <tr><td>MinIO 原文缺失</td><td>原文接口返回错误，运维检查数据包和 seed job。</td></tr>
  <tr><td>Neo4j 不可用</td><td>图谱能力降级或报错，运维检查 Neo4j healthcheck 和 dump 导入状态。</td></tr>
</table>

<h1>8 测试设计</h1>
<p>测试覆盖前端结构、路由、问答流式状态、上传文件、配额、部门人员管理、gateway 路由、public-service 模块、fastQA、highThinkingQA、patentQA 和部署数据包校验。前端使用 Node 内置测试和 Vite build 校验，后端使用 pytest。</p>
"""

DEVELOPMENT_DOC = """
<h1>1 文档说明</h1>
<p>本文档说明 LiFeO4Agent 的开发结构、技术栈、构建方式、配置管理、代码组织、测试和部署更新流程，供开发、测试和运维人员参考。</p>

<h1>2 项目结构</h1>
<table>
  <tr><th>目录</th><th>说明</th></tr>
  <tr><td><code>frontend-vue/</code></td><td>Vue 3 + Vite 前端。</td></tr>
  <tr><td><code>gateway/</code></td><td>FastAPI 网关，负责统一路由、SSE 转发、配额代理和会话协调。</td></tr>
  <tr><td><code>public-service/</code></td><td>公共能力服务，包含鉴权、用户、部门、人员、配额、会话、上传和文档代理。</td></tr>
  <tr><td><code>fastQA/</code></td><td>文献快速问答后端。</td></tr>
  <tr><td><code>highThinkingQA/</code></td><td>深度思考问答后端。</td></tr>
  <tr><td><code>patent/</code></td><td>专利问答后端。</td></tr>
  <tr><td><code>resource/</code></td><td>共享配置、资源和本地运行资源根目录。</td></tr>
  <tr><td><code>deploy/</code></td><td>Docker 离线交付和部署目录。</td></tr>
  <tr><td><code>scripts/</code></td><td>本地服务启停和公共脚本。</td></tr>
</table>

<h1>3 技术栈</h1>
<table>
  <tr><th>类别</th><th>技术</th><th>说明</th></tr>
  <tr><td>前端</td><td>Vue 3、Vite、Pinia、Vue Router</td><td>单页应用、状态管理和路由控制。</td></tr>
  <tr><td>后端</td><td>Python、FastAPI、Pydantic、httpx</td><td>网关和后端服务 API。</td></tr>
  <tr><td>模型调用</td><td>OpenAI compatible API、DashScope compatible endpoint</td><td>LLM、intent、embedding、rerank 由配置注入。</td></tr>
  <tr><td>数据组件</td><td>MySQL、Redis、MinIO、Neo4j、Chroma</td><td>业务数据、缓存、对象存储、图谱和向量检索。</td></tr>
  <tr><td>部署</td><td>Docker、Docker Compose、Nginx、seed-tools</td><td>离线镜像和数据包交付。</td></tr>
</table>

<h1>4 本地开发</h1>
<h2>4.1 前端开发</h2>
<pre>cd frontend-vue
npm install
npm run dev</pre>
<p>前端开发服务默认监听 <code>5173</code>。</p>

<h2>4.2 后端服务启停</h2>
<pre>bash scripts/start_all.sh
bash scripts/status_all.sh
bash scripts/stop_all.sh</pre>
<p>本地脚本会按服务顺序启动 public-service、fastQA、highThinkingQA、patentQA 和 gateway，并检查端口和健康状态。</p>

<h1>5 配置管理</h1>
<p>本地开发配置分散在各服务的 shared/secret env 文件中；Docker 交付环境统一由 <code>deploy/.env</code> 注入。密钥类配置只允许放在 secret env 或部署方本地 <code>.env</code>，不得写入代码或交付文档正文。</p>
<p>模型配置统一包含 LLM、intent model、fastQA/patentQA embedding、highThinkingQA embedding 和 rerank。Docker compose 会将这些变量映射到对应后端。</p>

<h1>6 构建与打包</h1>
<h2>6.1 前端构建</h2>
<pre>cd frontend-vue
npm ci
npm run build</pre>
<h2>6.2 Docker 镜像构建</h2>
<pre>docker build -f deploy/docker/base.Dockerfile -t lifeo4agent/python-base:latest .
docker build -f deploy/docker/Dockerfile.seed-tools -t lifeo4agent/seed-tools:latest .
docker build -f deploy/docker/Dockerfile.gateway -t lifeo4agent/gateway:latest .
docker build -f deploy/docker/Dockerfile.public-service -t lifeo4agent/public-service:latest .
docker build -f deploy/docker/Dockerfile.fastqa -t lifeo4agent/fastqa:latest .
docker build -f deploy/docker/Dockerfile.highthinkingqa -t lifeo4agent/highthinkingqa:latest .
docker build -f deploy/docker/Dockerfile.patent -t lifeo4agent/patent:latest .
docker build -f deploy/docker/Dockerfile.frontend-nginx -t lifeo4agent/frontend:latest .</pre>
<h2>6.3 数据包构建</h2>
<pre>bash deploy/scripts/collect_minio_seed.sh agentcode --clean
NEO4J_LITERATURE_DUMP_SRC=/path/to/literature.dump \
NEO4J_PATENT_DUMP_SRC=/path/to/patent.dump \
bash deploy/scripts/package_data.sh deploy/.env</pre>
<h2>6.4 镜像导出</h2>
<pre>bash deploy/scripts/export_images.sh deploy/.env deploy/lifeo4agent-images.tar</pre>

<h1>7 测试</h1>
<table>
  <tr><th>模块</th><th>测试目录</th><th>测试文件数</th></tr>
  <tr><td>frontend-vue</td><td><code>frontend-vue/src/**/*.test.js</code></td><td>56</td></tr>
  <tr><td>gateway</td><td><code>gateway/tests</code></td><td>22</td></tr>
  <tr><td>public-service</td><td><code>public-service/backend/tests</code></td><td>21</td></tr>
  <tr><td>fastQA</td><td><code>fastQA/tests</code></td><td>95</td></tr>
  <tr><td>highThinkingQA</td><td><code>highThinkingQA/tests</code></td><td>26</td></tr>
  <tr><td>patent</td><td><code>patent/tests</code></td><td>67</td></tr>
  <tr><td>scripts</td><td><code>scripts/tests</code></td><td>3</td></tr>
</table>
<p>常用命令：</p>
<pre>cd frontend-vue && npm run build && npm test
python -m pytest gateway/tests
python -m pytest public-service/backend/tests
python -m pytest fastQA/tests
python -m pytest highThinkingQA/tests
python -m pytest patent/tests
python -m pytest scripts/tests</pre>

<h1>8 更新开发流程</h1>
<ol>
  <li>按服务边界修改代码，避免无关重构。</li>
  <li>运行对应模块测试和前端构建。</li>
  <li>重新构建受影响服务镜像。</li>
  <li>只交付变更服务镜像或必要数据包。</li>
  <li>部署方加载镜像后使用 compose 重启对应服务。</li>
</ol>
"""

TEST_REPORT = """
<h1>1 文档说明</h1>
<p>本文档为 LiFeO4Agent 交付测试报告初版，记录测试范围、测试环境、测试项、测试方法和待补充的验收结果。本文档不编造未执行结果；正式交付前应按实际执行情况补充执行日期、执行人和通过情况。</p>

<h1>2 测试环境</h1>
<table>
  <tr><th>项目</th><th>内容</th></tr>
  <tr><td>部署方式</td><td>Docker Compose 离线部署</td></tr>
  <tr><td>前端</td><td>Vue 3 + Vite 构建产物，nginx 托管</td></tr>
  <tr><td>后端</td><td>gateway、public-service、fastQA、highThinkingQA、patentQA</td></tr>
  <tr><td>基础组件</td><td>MySQL、Redis、MinIO、Neo4j、nginx</td></tr>
  <tr><td>数据包版本</td><td><code>2026-05-19</code></td></tr>
</table>

<h1>3 测试范围</h1>
<table>
  <tr><th>测试类别</th><th>覆盖内容</th></tr>
  <tr><td>单元测试</td><td>前端工具函数、路由、状态管理；后端配置、路由、服务模块、检索、图谱、rerank、intent、数据包校验。</td></tr>
  <tr><td>构建测试</td><td>前端 Vite build、Docker 镜像构建。</td></tr>
  <tr><td>部署测试</td><td>preflight、docker load、compose config、compose up、seed job。</td></tr>
  <tr><td>数据校验</td><td>manifest sha256、MinIO 原文计数、Chroma SQLite 文件、Neo4j dump。</td></tr>
  <tr><td>功能验收</td><td>登录注册、问答、文件上传、原文查看、管理员后台、配额。</td></tr>
</table>

<h1>4 自动化测试清单</h1>
<table>
  <tr><th>模块</th><th>测试文件数</th><th>建议命令</th><th>结果</th></tr>
  <tr><td>frontend-vue</td><td>56</td><td><code>cd frontend-vue && npm run build && npm test</code></td><td>待执行记录</td></tr>
  <tr><td>gateway</td><td>22</td><td><code>python -m pytest gateway/tests</code></td><td>待执行记录</td></tr>
  <tr><td>public-service</td><td>21</td><td><code>python -m pytest public-service/backend/tests</code></td><td>待执行记录</td></tr>
  <tr><td>fastQA</td><td>95</td><td><code>python -m pytest fastQA/tests</code></td><td>待执行记录</td></tr>
  <tr><td>highThinkingQA</td><td>26</td><td><code>python -m pytest highThinkingQA/tests</code></td><td>待执行记录</td></tr>
  <tr><td>patent</td><td>67</td><td><code>python -m pytest patent/tests</code></td><td>待执行记录</td></tr>
  <tr><td>scripts</td><td>3</td><td><code>python -m pytest scripts/tests</code></td><td>待执行记录</td></tr>
</table>

<h1>5 数据包测试</h1>
<table>
  <tr><th>数据包</th><th>校验项</th><th>期望结果</th></tr>
  <tr><td><code>minio-originals.tar.zst</code></td><td>papers、专利目录、tables</td><td>papers 7153，专利目录 14006，tables 9581。</td></tr>
  <tr><td><code>fastqa-ref.tar.zst</code></td><td>Chroma SQLite</td><td>存在 2 个 Chroma SQLite 文件。</td></tr>
  <tr><td><code>highthinking-ref.tar.zst</code></td><td>Chroma SQLite</td><td>存在 1 个 Chroma SQLite 文件。</td></tr>
  <tr><td><code>patentqa-ref.tar.zst</code></td><td>JSON-only archive</td><td>专利 JSON 目录 14006，不包含 PDF/PNG 原文。</td></tr>
  <tr><td><code>neo4j-literature.dump.zst</code>、<code>neo4j-patent.dump.zst</code></td><td>dump 可加载</td><td>Neo4j seed job 可完成导入。</td></tr>
</table>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env</pre>

<h1>6 功能验收用例</h1>
<table>
  <tr><th>编号</th><th>用例</th><th>预期结果</th><th>结果</th></tr>
  <tr><td>FT-01</td><td>管理员登录</td><td>进入管理员后台。</td><td>待执行记录</td></tr>
  <tr><td>FT-02</td><td>普通用户注册并登录</td><td>可进入问答首页。</td><td>待执行记录</td></tr>
  <tr><td>FT-03</td><td>文献模式问答</td><td>返回答案、引用和阶段耗时。</td><td>待执行记录</td></tr>
  <tr><td>FT-04</td><td>深度模式问答</td><td>返回分阶段深度回答。</td><td>待执行记录</td></tr>
  <tr><td>FT-05</td><td>专利模式问答</td><td>返回专利相关答案、引用和原文入口。</td><td>待执行记录</td></tr>
  <tr><td>FT-06</td><td>上传 PDF/Excel/CSV 文件问答</td><td>文件进入会话文件列表，可参与本轮问答。</td><td>待执行记录</td></tr>
  <tr><td>FT-07</td><td>查看论文和专利原文</td><td>PDF 阅读器或原文视图正常打开。</td><td>待执行记录</td></tr>
  <tr><td>FT-08</td><td>部门、人员、用户、配额管理</td><td>管理员后台操作正常。</td><td>待执行记录</td></tr>
</table>

<h1>7 测试结论</h1>
<p>当前文档已列出交付测试范围和验收用例。正式提交测试报告时，应在完成自动化测试、部署预检和功能验收后，将“待执行记录”替换为实际执行结果。</p>
"""

REQUIREMENT_LIST = """
<h1>需求清单</h1>
<table>
  <tr><th>序号</th><th>需求层级</th><th>需求简述</th><th>提出时间</th><th>需求文档</th><th>完成时间</th><th>状态</th><th>备注</th></tr>
  <tr><td class="center">1</td><td>系统能力</td><td>提供文献、深度思考、专利三种问答模式。</td><td class="center">2026/05/20</td><td>交付范围确认</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>前端模式为“文献/深度/专利”。</td></tr>
  <tr><td class="center">2</td><td>系统能力</td><td>支持 PDF、Excel、CSV 上传并参与文件问答。</td><td class="center">2026/05/20</td><td>交付范围确认</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>文件元数据由 public-service 管理。</td></tr>
  <tr><td class="center">3</td><td>数据能力</td><td>论文和专利原文统一进入 MinIO，后端不重复携带 PDF/PNG 原文。</td><td class="center">2026/05/20</td><td>Docker 离线交付方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>通过 <code>minio-originals.tar.zst</code> 自动 seed。</td></tr>
  <tr><td class="center">4</td><td>数据能力</td><td>专利原文包含 <code>structured/tables.json</code> 并更新 manifest。</td><td class="center">2026/05/20</td><td>MinIO 原文数据计划</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>manifest 记录 tables 可用性。</td></tr>
  <tr><td class="center">5</td><td>部署能力</td><td>离线交付采用 Docker 镜像包 + 数据包 + compose 自动导入。</td><td class="center">2026/05/20</td><td>全局 Docker 离线交付方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>部署方无需安装 <code>mc</code>、<code>zstd</code>、<code>neo4j-admin</code>。</td></tr>
  <tr><td class="center">6</td><td>配置能力</td><td>部署方只需配置端口、账号密码、MinIO、LLM、intent、embedding、rerank 等。</td><td class="center">2026/05/20</td><td>部署配置方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>集中在 <code>deploy/.env</code>。</td></tr>
  <tr><td class="center">7</td><td>安全能力</td><td>支持 HTTPS 入口，部署方可替换自签或正式证书。</td><td class="center">2026/05/20</td><td>HTTPS 部署讨论</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>证书位置为 <code>deploy/certs/</code>。</td></tr>
  <tr><td class="center">8</td><td>管理能力</td><td>提供用户、部门、人员、配额管理。</td><td class="center">2026/05/20</td><td>系统交付范围</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>管理员后台路径为 <code>/admin</code>。</td></tr>
</table>
"""

DEPLOYMENT_MANUAL_DETAIL = """
<h1>13 部署前详细检查</h1>
<h2>13.1 文件完整性检查</h2>
<p>部署前应确认交付目录完整。最小可部署目录应包含 compose 文件、配置模板、镜像包、数据包、证书目录、MySQL 初始化 SQL 和 seed-tools 脚本。缺少任一关键文件都可能导致服务无法启动或数据无法导入。</p>
<table>
  <tr><th>检查项</th><th>期望状态</th><th>处理方式</th></tr>
  <tr><td><code>deploy/docker-compose.yml</code></td><td>存在</td><td>缺失时需要重新获取完整部署包。</td></tr>
  <tr><td><code>deploy/.env</code></td><td>已由模板复制并填写</td><td>从 <code>.env.production.example</code> 复制，不直接编辑模板。</td></tr>
  <tr><td><code>deploy/lifeo4agent-images.tar</code></td><td>存在且可读取</td><td>用于 <code>docker load</code> 导入镜像。</td></tr>
  <tr><td><code>deploy/data/manifest.json</code></td><td>存在</td><td>记录数据包版本、sha256、大小和关键计数。</td></tr>
  <tr><td><code>deploy/data/*.tar.zst</code></td><td>全部存在</td><td>MinIO、reference data 和 Neo4j 依赖这些包。</td></tr>
  <tr><td><code>deploy/certs/fullchain.pem</code></td><td>存在</td><td>HTTPS 服务证书链。</td></tr>
  <tr><td><code>deploy/certs/privkey.pem</code></td><td>存在</td><td>HTTPS 私钥，权限应严格控制。</td></tr>
</table>

<h2>13.2 端口规划</h2>
<p>生产环境中，通常只需要开放 HTTPS 端口给最终用户。MySQL、Redis 和 MinIO 是否开放给运维网段由部署方安全策略决定。如果部署机已经存在同类服务，应在 <code>deploy/.env</code> 中改用不冲突的宿主机端口。</p>
<table>
  <tr><th>端口变量</th><th>用途</th><th>冲突处理</th></tr>
  <tr><td><code>HTTPS_PUBLISH_PORT</code></td><td>用户 HTTPS 访问入口</td><td>如 443 已被占用，可改为 18443，并同步 <code>HTTPS_REDIRECT_HOST</code>。</td></tr>
  <tr><td><code>HTTP_PUBLISH_PORT</code></td><td>HTTP 跳转入口</td><td>如 80 被占用，可改为 18080 或关闭外部防火墙入口。</td></tr>
  <tr><td><code>MYSQL_PUBLISH_PORT</code></td><td>MySQL 运维访问</td><td>本机已有 MySQL 时建议使用非默认端口。</td></tr>
  <tr><td><code>REDIS_PUBLISH_PORT</code></td><td>Redis 运维访问</td><td>本机已有 Redis 时建议使用非默认端口。</td></tr>
  <tr><td><code>MINIO_API_PUBLISH_PORT</code></td><td>MinIO API</td><td>本机已有 MinIO 时建议使用独立端口。</td></tr>
  <tr><td><code>MINIO_CONSOLE_PUBLISH_PORT</code></td><td>MinIO 控制台</td><td>仅限管理员或运维网段访问。</td></tr>
</table>

<h2>13.3 域名和证书检查</h2>
<p>HTTPS 证书应包含实际访问域名。内网自签证书同样需要满足 SAN 域名匹配。客户端访问时，域名必须能解析到部署机 IP。解析可以通过内网 DNS，也可以在测试机 hosts 中配置。</p>
<pre># Linux 测试机 hosts 示例
&lt;部署机IP&gt; &lt;部署域名&gt;</pre>
<p>hosts 只影响本机对该域名的解析，不会修改公网 DNS。只要不覆盖常用公网域名，不会影响正常上网。</p>

<h1>14 部署执行步骤</h1>
<h2>14.1 准备配置</h2>
<ol>
  <li>复制配置模板为实际配置文件。</li>
  <li>填写端口、域名、证书、MySQL、Redis、MinIO、JWT、内部 token 和模型连接配置。</li>
  <li>确认 <code>DATA_PACKAGE_VERSION</code> 与 <code>deploy/data/manifest.json</code> 中的 <code>data_version</code> 一致。</li>
  <li>将 <code>DATA_SEED_FORCE</code> 保持为 <code>0</code>，除非明确需要强制重导。</li>
</ol>
<pre>cp deploy/.env.production.example deploy/.env
vi deploy/.env</pre>

<h2>14.2 导入镜像</h2>
<pre>docker load -i deploy/lifeo4agent-images.tar</pre>
<p>导入完成后，可查看镜像是否存在：</p>
<pre>docker images | grep lifeo4agent</pre>

<h2>14.3 执行预检</h2>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env</pre>
<p>预检会检查必需文件、必需变量、数据包、manifest sha256、Docker 镜像和 compose 配置展开。预检失败时，应先处理失败项，不建议跳过。</p>

<h2>14.4 启动服务</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d</pre>
<p>首次启动时，seed job 会消耗较长时间，尤其是 MinIO 原文导入和 Neo4j dump 加载。可用以下命令观察进度：</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f minio-seed
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f neo4j-literature-seed
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f neo4j-patent-seed</pre>

<h2>14.5 验证服务</h2>
<ol>
  <li>执行 <code>docker compose ps</code>，确认长期服务为 running 或 healthy。</li>
  <li>确认 seed job 为 <code>Exited (0)</code>。</li>
  <li>访问 HTTPS 地址，确认页面打开。</li>
  <li>使用管理员账号登录，确认管理员后台可打开。</li>
  <li>分别发起文献、深度、专利三类测试问题。</li>
  <li>打开 MinIO Console，确认 bucket 中存在 <code>papers/</code> 和 <code>patent/originals/</code>。</li>
</ol>

<h1>15 数据导入机制说明</h1>
<p>数据导入使用版本 marker 控制幂等。每个数据包完成导入后会写入对应版本的 marker。再次启动同版本时，seed job 发现 marker 后直接跳过，从而避免重复解压和覆盖。</p>
<table>
  <tr><th>数据类别</th><th>导入位置</th><th>重导风险</th></tr>
  <tr><td>MinIO 原文</td><td>MinIO bucket</td><td>使用 <code>mc mirror --overwrite</code>，同名对象会被覆盖。</td></tr>
  <tr><td>Reference data</td><td>各服务 ref named volume</td><td>强制重导会清空目标 volume 中除 marker 外的内容。</td></tr>
  <tr><td>Neo4j dump</td><td>Neo4j data volume</td><td>使用 overwrite load，强制重导会覆盖目标数据库。</td></tr>
</table>
<p>因此，<code>DATA_SEED_FORCE=1</code> 只应在确认需要重建数据时使用。重导完成后应立即改回 <code>0</code>。</p>

<h1>16 更新和回滚策略</h1>
<h2>16.1 业务镜像更新</h2>
<p>业务代码更新通常只需要交付受影响服务的新镜像。例如只修改 fastQA，则无需重新交付 MinIO、MySQL、Redis、Neo4j 或其他后端镜像。</p>
<pre>docker load -i lifeo4agent-fastqa-update.tar
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d fastqa</pre>
<p>如果 gateway 或前端接口契约有变化，需要同时更新 gateway 或 frontend。</p>

<h2>16.2 配置更新</h2>
<p>修改 <code>deploy/.env</code> 后，应执行预检，再重启受影响服务。例如修改模型地址后，需要重启对应问答后端和 gateway。</p>

<h2>16.3 数据包更新</h2>
<p>数据包更新应成套替换 <code>manifest.json</code> 和对应数据文件，并更新 <code>DATA_PACKAGE_VERSION</code>。如果只替换文件但不更新版本，seed job 会因为旧 marker 存在而跳过。</p>

<h2>16.4 回滚</h2>
<p>镜像回滚依赖保留旧镜像 tag 或旧镜像 tar。数据包回滚依赖保留旧版本 <code>deploy/data/</code> 和 manifest。回滚数据包时应设置旧版本号，并根据实际情况决定是否使用 <code>DATA_SEED_FORCE=1</code>。</p>
"""

OPERATIONS_MANUAL_DETAIL = """
<h1>8 运维角色与职责</h1>
<table>
  <tr><th>角色</th><th>职责</th><th>权限建议</th></tr>
  <tr><td>系统管理员</td><td>管理用户、部门、人员、配额，处理账号问题。</td><td>拥有系统管理员账号。</td></tr>
  <tr><td>平台运维</td><td>维护 Docker、证书、端口、数据包、备份恢复和日志排查。</td><td>拥有服务器和 Docker 操作权限。</td></tr>
  <tr><td>模型运维</td><td>维护 LLM、intent、embedding、rerank 服务地址、模型名和 API Key。</td><td>拥有模型平台配置权限。</td></tr>
  <tr><td>数据维护人员</td><td>维护论文、专利、向量库和图谱数据包版本。</td><td>拥有数据包生成和校验权限。</td></tr>
</table>

<h1>9 日常巡检清单</h1>
<h2>9.1 每日巡检</h2>
<ol>
  <li>检查所有长期运行容器状态。</li>
  <li>访问 HTTPS 首页，确认页面正常加载。</li>
  <li>登录管理员账号或测试账号，确认认证链路正常。</li>
  <li>抽测文献、深度、专利三种问答模式。</li>
  <li>查看近 200 行关键服务日志，确认没有持续报错。</li>
  <li>检查磁盘剩余空间，重点关注 Docker 数据目录。</li>
</ol>

<h2>9.2 每周巡检</h2>
<ol>
  <li>检查 MySQL 备份是否可生成、可读取。</li>
  <li>检查 MinIO bucket 对象数量和近期新增对象。</li>
  <li>检查 Redis AOF 和容器重启次数。</li>
  <li>检查 Neo4j healthcheck 和图谱查询代表用例。</li>
  <li>检查模型服务调用延迟和错误率。</li>
  <li>核对 <code>deploy/data/manifest.json</code>、<code>deploy/.env</code> 和实际运行版本。</li>
</ol>

<h1>10 常用日志命令</h1>
<table>
  <tr><th>场景</th><th>命令</th></tr>
  <tr><td>查看所有服务日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200</code></td></tr>
  <tr><td>查看网关日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f gateway</code></td></tr>
  <tr><td>查看文献问答日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f fastqa</code></td></tr>
  <tr><td>查看深度问答日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f highthinkingqa</code></td></tr>
  <tr><td>查看专利问答日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f patent</code></td></tr>
  <tr><td>查看 MinIO 导入日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs minio-seed</code></td></tr>
  <tr><td>查看 Neo4j 导入日志</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs neo4j-literature-seed neo4j-patent-seed</code></td></tr>
</table>

<h1>11 故障定位流程</h1>
<h2>11.1 页面打不开</h2>
<ol>
  <li>检查部署机端口是否监听：<code>ss -lntp</code>。</li>
  <li>检查 <code>edge</code> 容器是否运行。</li>
  <li>检查域名是否解析到部署机 IP。</li>
  <li>检查证书路径和证书域名是否匹配。</li>
  <li>查看 <code>edge</code> 日志定位 nginx 配置或证书错误。</li>
</ol>

<h2>11.2 问答失败</h2>
<ol>
  <li>先查看前端报错信息，确认是认证、配额、模型、检索还是服务异常。</li>
  <li>查看 gateway 日志，确认请求实际路由到哪个后端。</li>
  <li>查看对应 QA 后端日志，确认 intent、embedding、rerank、LLM 是否调用成功。</li>
  <li>如报向量库不存在，检查对应 ref seed job 和 named volume。</li>
  <li>如报原文不存在，检查 MinIO bucket 和 <code>minio-seed</code> marker。</li>
  <li>如报图谱异常，检查 Neo4j healthcheck 和对应 seed job。</li>
</ol>

<h2>11.3 登录和用户异常</h2>
<ol>
  <li>检查 public-service 日志。</li>
  <li>确认 MySQL 容器 healthy。</li>
  <li>确认用户状态为 active。</li>
  <li>如为首次登录或强制补全，按页面提示完成个人中心设置。</li>
  <li>如忘记密码且未设置安全问题，由管理员重置。</li>
</ol>

<h1>12 备份策略细化</h1>
<p>系统数据分为可重建数据和不可轻易重建数据。reference data 和初始图谱可由数据包重建；用户、会话、上传文件、运行期新增对象则属于运行态数据，需要纳入备份。</p>
<table>
  <tr><th>数据</th><th>是否可由交付包重建</th><th>备份频率建议</th><th>说明</th></tr>
  <tr><td>MySQL 用户和会话</td><td>否</td><td>每日或按业务要求</td><td>最重要的运行态数据。</td></tr>
  <tr><td>MinIO 原文 seed</td><td>是</td><td>保留原始数据包</td><td>如运行期新增上传对象，则需要另行备份 MinIO。</td></tr>
  <tr><td>Redis 状态</td><td>部分可恢复</td><td>按需</td><td>异常恢复时可接受部分缓存丢失，但任务状态可能受影响。</td></tr>
  <tr><td>Reference volume</td><td>是</td><td>保留数据包</td><td>强制重导会覆盖。</td></tr>
  <tr><td>Neo4j 初始图谱</td><td>是</td><td>保留 dump 包</td><td>如上线后有图谱写入，应另做 Neo4j dump。</td></tr>
  <tr><td><code>deploy/.env</code></td><td>否</td><td>每次变更后</td><td>包含密钥，应加密保管。</td></tr>
</table>

<h1>13 变更管理</h1>
<ol>
  <li>变更前记录当前镜像 tag、数据包版本、配置文件摘要和容器状态。</li>
  <li>执行预检，确认待更新包完整。</li>
  <li>业务低峰期执行镜像或数据包更新。</li>
  <li>更新后执行登录、三类问答、原文查看和管理员后台抽测。</li>
  <li>如发生异常，按镜像或数据包回滚流程恢复。</li>
</ol>
"""

USER_MANUAL_DETAIL = """
<h1>8 页面区域说明</h1>
<p>问答首页主要由四个区域组成：左侧会话栏、中间消息区、右侧问题大纲、底部输入区。左侧用于新建、切换、置顶和删除会话；中间用于查看用户问题、系统回答、引用和阶段进度；右侧用于在长对话中快速定位问题；底部用于选择模式、上传文件和发送问题。</p>
<table>
  <tr><th>区域</th><th>功能</th><th>使用建议</th></tr>
  <tr><td>左侧会话栏</td><td>新建、切换、置顶、删除会话</td><td>同一主题建议放在同一个会话内，便于上下文连续。</td></tr>
  <tr><td>文件列表</td><td>查看已上传文件、选择本轮使用文件、下载或删除文件</td><td>每轮提问前确认勾选文件是否正确。</td></tr>
  <tr><td>消息区</td><td>展示问题、答案、引用、阶段和错误提示</td><td>回答未完成时不要刷新页面。</td></tr>
  <tr><td>问题大纲</td><td>按历史问题快速跳转</td><td>长对话中用于定位上下文。</td></tr>
  <tr><td>输入区</td><td>选择问答模式、上传文件、发送问题</td><td>提问前先选择文献、深度或专利。</td></tr>
</table>

<h1>9 问答模式选择建议</h1>
<h2>9.1 文献模式</h2>
<p>适合询问文献中的材料性能、工艺参数、实验结论、文献对比和引用来源。文献模式优先追求响应速度和检索命中，适合明确问题和事实型问题。</p>
<p>示例问题：</p>
<ul>
  <li>磷酸铁锂包覆改性对循环性能有什么影响？</li>
  <li>有哪些文献提到碳包覆对倍率性能的提升？</li>
  <li>比较不同合成工艺对粒径分布的影响。</li>
</ul>

<h2>9.2 深度模式</h2>
<p>适合需要多步骤分析、归纳、推理和综合判断的问题。深度模式通常耗时更长，但回答结构更完整。</p>
<p>示例问题：</p>
<ul>
  <li>从材料设计角度分析影响磷酸铁锂低温性能的关键因素。</li>
  <li>围绕高压实密度和倍率性能之间的矛盾，给出研发思路。</li>
  <li>结合已有知识，总结下一步实验验证方案。</li>
</ul>

<h2>9.3 专利模式</h2>
<p>适合专利检索、权利要求分析、技术路线梳理、专利表格和附图相关问题。专利模式会使用专利向量库、JSON archive、MinIO 原文和专利图谱。</p>
<p>示例问题：</p>
<ul>
  <li>检索与磷酸铁锂正极材料制备相关的专利。</li>
  <li>某专利的核心权利要求是什么？</li>
  <li>对比几件专利中关于前驱体处理方法的差异。</li>
</ul>

<h1>10 回答结果解读</h1>
<table>
  <tr><th>结果元素</th><th>含义</th><th>用户动作</th></tr>
  <tr><td>阶段信息</td><td>展示意图识别、检索、重排、图谱、生成等阶段进展。</td><td>用于判断问题卡在哪个环节。</td></tr>
  <tr><td>总耗时</td><td>本轮回答从提交到完成的时间。</td><td>复杂问题耗时更长属于正常情况。</td></tr>
  <tr><td>引用</td><td>回答依据的文献、专利或文件片段。</td><td>点击查看来源或原文。</td></tr>
  <tr><td>原文入口</td><td>从 MinIO 读取论文或专利原文。</td><td>用于核对 PDF、专利表格或附图。</td></tr>
  <tr><td>配额提示</td><td>当前功能次数不足或暂不可用。</td><td>联系管理员调整配额。</td></tr>
</table>

<h1>11 文件问答使用细节</h1>
<ol>
  <li>上传文件后，先等待文件状态变为已上传或处理完成。</li>
  <li>如果只想基于文件回答，应勾选目标文件，并在问题中说明“根据上传文件”。</li>
  <li>如果同时希望结合知识库和文件，可在问题中说明“结合知识库和上传文件”。</li>
  <li>删除文件只影响当前会话的文件关联，不建议在回答生成过程中操作。</li>
  <li>Excel 和 CSV 更适合表格统计、字段解释、数据对比类问题。</li>
</ol>

<h1>12 管理员操作细化</h1>
<h2>12.1 用户生命周期</h2>
<p>管理员可以创建用户、批量导入用户、修改密码、启用或停用用户、调整用户类型、绑定人员记录。停用用户后，该用户不能继续登录。删除用户属于高风险操作，执行前应确认不再需要其历史会话。</p>

<h2>12.2 部门维护</h2>
<p>部门分为一级、二级、三级。当前交付 seed 中包含“电池材料技术研究中心”及其下属部门。管理员可继续新增或停用部门。停用部门不会清空历史绑定，但会影响后续选择。</p>

<h2>12.3 人员维护</h2>
<p>人员记录用于注册和账号绑定。人员记录包含工号、姓名、部门、状态和校验码。用户注册时必须提供与人员记录匹配的信息。人员被停用后，绑定状态会在个人中心中体现。</p>

<h2>12.4 配额维护</h2>
<p>配额用于控制普通问答、文件问答、查看原文和文档辅助等功能的使用次数。管理员可设置默认限制，也可重置指定用户的使用记录。</p>
"""

SUMMARY_DESIGN_DETAIL = """
<h1>8 设计原则</h1>
<table>
  <tr><th>原则</th><th>设计体现</th></tr>
  <tr><td>服务边界清晰</td><td>gateway 只做路由和协调，public-service 管公共能力，三个 QA 后端各自处理领域问答。</td></tr>
  <tr><td>数据不重复</td><td>论文和专利原文只以 MinIO 为权威副本，各后端不再重复携带大体积 PDF/PNG。</td></tr>
  <tr><td>离线可交付</td><td>运行镜像和数据包分离，部署方不依赖公网拉取工具。</td></tr>
  <tr><td>配置面收敛</td><td>客户主要配置端口、账号、模型和数据版本，内部服务地址由 compose 固定。</td></tr>
  <tr><td>可增量升级</td><td>单服务代码变化只需替换单服务镜像；数据变化通过版本化数据包更新。</td></tr>
</table>

<h1>9 集成架构</h1>
<p>系统与外部模型服务集成，包括 LLM、intent 模型、embedding 模型和 rerank 模型。fastQA 和 patentQA 共用 intent、embedding 和 rerank 配置；highThinkingQA 使用独立 embedding 配置；所有问答服务共享 LLM 配置。</p>
<table>
  <tr><th>外部能力</th><th>使用服务</th><th>配置项</th><th>说明</th></tr>
  <tr><td>LLM</td><td>fastQA、highThinkingQA、patentQA</td><td><code>LLM_BASE_URL</code>、<code>LLM_MODEL</code>、<code>LLM_API_KEY</code></td><td>用于答案生成、规划和总结。</td></tr>
  <tr><td>Intent Model</td><td>fastQA、patentQA</td><td><code>INTENT_MODEL_*</code></td><td>用于意图识别和路由辅助，可开关。</td></tr>
  <tr><td>QA Embedding</td><td>fastQA、patentQA</td><td><code>QA_EMBEDDING_*</code></td><td>用于文献和专利检索向量化。</td></tr>
  <tr><td>HighThinking Embedding</td><td>highThinkingQA</td><td><code>HIGHTHINKINGQA_EMBEDDING_*</code></td><td>用于深度问答向量库。</td></tr>
  <tr><td>Rerank</td><td>fastQA、patentQA</td><td><code>RERANK_*</code></td><td>用于检索结果重排；可设置为禁用。</td></tr>
</table>

<h1>10 数据架构</h1>
<p>数据分为业务运行态数据、可重建 reference 数据和原文对象数据。业务运行态数据需要备份；reference 数据可由数据包重建；原文对象首次由数据包导入，运行期新增对象需按 MinIO 策略备份。</p>
<table>
  <tr><th>数据类型</th><th>存储位置</th><th>生命周期</th></tr>
  <tr><td>用户、部门、人员、会话、配额</td><td>MySQL</td><td>运行态，不随数据包重建。</td></tr>
  <tr><td>缓存、任务状态</td><td>Redis</td><td>运行态，可按需持久化。</td></tr>
  <tr><td>论文和专利原文</td><td>MinIO</td><td>由数据包 seed，作为原文权威副本。</td></tr>
  <tr><td>向量库和索引</td><td>各 ref named volume</td><td>由数据包 seed，可重建。</td></tr>
  <tr><td>文献和专利图谱</td><td>两个 Neo4j volume</td><td>由 dump seed，可重建。</td></tr>
</table>

<h1>11 可用性与降级设计</h1>
<p>基础组件通过 healthcheck 控制启动顺序。MinIO、reference data 和 Neo4j seed 完成后，业务服务才启动。模型服务属于外部依赖，若模型不可用，相关问答会返回结构化错误；如图谱不可用，图谱增强能力会受影响，但可通过日志定位。</p>
"""

DETAILED_DESIGN_DETAIL = """
<h1>9 配置映射设计</h1>
<p>Docker compose 将客户配置面映射到各服务内部环境变量，避免部署方理解每个后端的内部变量名。</p>
<table>
  <tr><th>客户配置</th><th>映射目标</th><th>说明</th></tr>
  <tr><td><code>LLM_*</code></td><td>三个 QA 后端和 public-service 的 OpenAI/DashScope 兼容变量</td><td>统一生成模型入口。</td></tr>
  <tr><td><code>INTENT_MODEL_*</code></td><td>fastQA、patentQA</td><td>两个服务使用统一命名。</td></tr>
  <tr><td><code>QA_EMBEDDING_*</code></td><td>fastQA、patentQA</td><td>文献和专利共用 embedding 服务。</td></tr>
  <tr><td><code>HIGHTHINKINGQA_EMBEDDING_*</code></td><td>highThinkingQA</td><td>深度问答独立 embedding。</td></tr>
  <tr><td><code>RERANK_*</code></td><td>fastQA、patentQA</td><td>统一 rerank 配置。</td></tr>
  <tr><td><code>MINIO_*</code></td><td>public-service、fastQA、highThinkingQA、patentQA</td><td>统一访问 MinIO bucket。</td></tr>
</table>

<h1>10 Gateway 路由细节</h1>
<p>gateway 接收前端请求后，会读取会话文件列表，解析本轮文件上下文，并根据请求模式决定目标后端。请求模式只允许 <code>fast</code>、<code>thinking</code>、<code>patent</code>。当用户选择文件时，gateway 会区分知识库问答、文件问答和混合问答，并将文件选择结果传给目标后端。</p>
<ol>
  <li>校验请求体和认证信息。</li>
  <li>读取 conversation file provider 提供的文件元数据。</li>
  <li>通过 file context resolver 判断文件参与方式。</li>
  <li>通过 route decision service 得出实际路由。</li>
  <li>执行配额 precheck。</li>
  <li>转发请求并代理 SSE。</li>
  <li>根据完成结果 finalize 配额并持久化会话。</li>
</ol>

<h1>11 Seed 脚本细节</h1>
<table>
  <tr><th>脚本</th><th>输入</th><th>输出</th><th>幂等条件</th></tr>
  <tr><td><code>seed_minio_originals.sh</code></td><td><code>minio-originals.tar.zst</code></td><td>MinIO bucket 中的 <code>papers/</code> 和 <code>patent/originals/</code></td><td>MinIO marker 存在且未强制重导。</td></tr>
  <tr><td><code>seed_ref_data.sh</code></td><td>对应 <code>*-ref.tar.zst</code></td><td>目标 reference volume</td><td>目标 volume 中 marker 存在且未强制重导。</td></tr>
  <tr><td><code>prepare_neo4j_dump.sh</code></td><td><code>neo4j-*.dump.zst</code></td><td>解压后的 <code>neo4j.dump</code></td><td>ready 文件和 dump 同时存在。</td></tr>
  <tr><td><code>load_neo4j_dump.sh</code></td><td>解压后的 dump</td><td>Neo4j 数据库</td><td>Neo4j data volume 中 marker 存在且未强制重导。</td></tr>
</table>

<h1>12 并发和任务控制设计</h1>
<p>问答请求通过 gateway 和后端运行时控制并发。gateway 维护任务流状态、队列状态、slot lease 和 event relay。fastQA 和 patentQA 后端也有上游调用 gate、连接池和运行时限制，避免模型或检索服务被突发请求压垮。</p>

<h1>13 安全细节</h1>
<ol>
  <li>前端只保存 token 和必要用户信息。</li>
  <li>后端通过 JWT 校验用户身份，通过 user_type 和 role 控制管理员权限。</li>
  <li>内部服务调用通过 <code>PUBLIC_SERVICE_INTERNAL_AUTH_TOKEN</code> 控制。</li>
  <li>密码使用哈希存储，不保存明文。</li>
  <li>交付文档不写真实密钥；部署方在本地 <code>.env</code> 中维护。</li>
  <li>HTTPS 私钥只放在部署机 <code>deploy/certs/privkey.pem</code>，不进入镜像。</li>
</ol>

<h1>14 数据一致性设计</h1>
<p>MySQL 负责用户、会话和配额的一致性；MinIO 负责原文对象；reference volume 为只读数据源；Neo4j dump 来自维护窗口中的一致性导出。数据包 manifest 记录 sha256 和关键计数，preflight 在部署前校验，降低传输损坏和版本混用风险。</p>
"""

DEVELOPMENT_DOC_DETAIL = """
<h1>9 开发规范</h1>
<table>
  <tr><th>类别</th><th>规范</th></tr>
  <tr><td>Python</td><td>4 空格缩进，函数和模块使用 snake_case，类使用 PascalCase。</td></tr>
  <tr><td>Vue/JS</td><td>保留现有组件结构，路由、服务、store 和 utils 分层维护。</td></tr>
  <tr><td>配置</td><td>新增客户可配置项时，需同步更新 shared env、secret env、docker compose、模板和文档。</td></tr>
  <tr><td>接口</td><td>新增 public API 时，优先经 gateway 暴露，并补充 route table 或代理规则。</td></tr>
  <tr><td>测试</td><td>修改共享行为、路由、配置、seed 或数据包时必须补测试。</td></tr>
</table>

<h1>10 常见开发任务流程</h1>
<h2>10.1 新增前端功能</h2>
<ol>
  <li>确认功能属于页面、组件、服务封装还是 store 状态。</li>
  <li>在 <code>frontend-vue/src</code> 中按现有结构新增或修改。</li>
  <li>补充结构测试或工具函数测试。</li>
  <li>执行 <code>npm run build</code> 和 <code>npm test</code>。</li>
  <li>重新构建 frontend 镜像。</li>
</ol>

<h2>10.2 新增后端接口</h2>
<ol>
  <li>确认接口归属：公共能力放 public-service，问答领域能力放对应 QA 后端，统一入口放 gateway。</li>
  <li>定义 Pydantic 请求/响应模型。</li>
  <li>实现 service 层逻辑，router 只做协议转换。</li>
  <li>补充单元测试和路由测试。</li>
  <li>如对外暴露，更新 gateway route table 和前端 service。</li>
</ol>

<h2>10.3 新增模型配置</h2>
<ol>
  <li>确定是否属于客户主配置面。</li>
  <li>如果需要部署方配置，在 <code>resource/config/shared/model-endpoints.shared.env</code> 放非密配置，在 secret env 放 key。</li>
  <li>同步 <code>deploy/.env.production.example</code> 和 <code>deploy/docker-compose.yml</code>。</li>
  <li>补充后端 env loader 测试和 Docker 配置说明。</li>
</ol>

<h2>10.4 更新数据包</h2>
<ol>
  <li>从本地 resource 生成 MinIO seed。</li>
  <li>在图谱维护窗口生成 Neo4j dump。</li>
  <li>执行 package_data 生成 tar.zst 和 manifest。</li>
  <li>执行 validate_data_packages 校验。</li>
  <li>更新 <code>DATA_PACKAGE_VERSION</code> 并记录变更内容。</li>
</ol>

<h1>11 Docker 镜像开发注意事项</h1>
<p>Python base 镜像只放依赖，不承载整个仓库代码。各服务镜像只复制本服务代码和必要共享配置、资源。大数据不进入业务镜像。这样可以在后期只替换受影响服务镜像，降低交付体积和更新时间。</p>

<h1>12 代码审查关注点</h1>
<ol>
  <li>是否改动了客户配置面，是否同步 Docker 和文档。</li>
  <li>是否引入真实密钥或本地绝对路径。</li>
  <li>是否破坏 gateway 路由契约。</li>
  <li>是否影响 MinIO-only 原文访问策略。</li>
  <li>是否影响数据包 seed 幂等性。</li>
  <li>是否补充了对应测试。</li>
</ol>
"""

TEST_REPORT_DETAIL = """
<h1>8 部署集成测试步骤</h1>
<ol>
  <li>在空 Docker volume 环境中执行 <code>docker load</code>。</li>
  <li>填写 <code>deploy/.env</code>，确认端口和模型地址可用。</li>
  <li>执行 <code>bash deploy/scripts/preflight_check.sh deploy/.env</code>。</li>
  <li>执行 <code>docker compose up -d</code>。</li>
  <li>观察 seed job 全部成功退出。</li>
  <li>访问 HTTPS 页面，完成管理员登录。</li>
  <li>分别执行文献、深度、专利问答验收。</li>
  <li>第二次执行 compose up，确认同版本 seed job 跳过。</li>
  <li>设置 <code>DATA_SEED_FORCE=1</code> 在测试环境验证强制重导流程。</li>
</ol>

<h1>9 接口测试重点</h1>
<table>
  <tr><th>接口组</th><th>测试重点</th></tr>
  <tr><td>认证接口</td><td>登录、注册、token 校验、首次登录强制补全、安全问题找回密码。</td></tr>
  <tr><td>管理员接口</td><td>用户增删改查、停用启用、批量导入、部门和人员维护。</td></tr>
  <tr><td>配额接口</td><td>普通问答、文件问答、查看原文、文档辅助的配额扣减和重置。</td></tr>
  <tr><td>问答接口</td><td>三种模式同步/流式请求、路由决策、SSE 完成事件、错误事件。</td></tr>
  <tr><td>文件接口</td><td>PDF/Excel/CSV 上传、列表、下载、删除、文件参与问答。</td></tr>
  <tr><td>原文接口</td><td>论文 PDF、专利 PDF、专利 structured tables、专利图片或段落。</td></tr>
</table>

<h1>10 性能与稳定性测试建议</h1>
<p>正式验收时建议补充并发问答、长问题、长会话、连续上传文件、MinIO 原文打开、Neo4j 查询和模型超时场景测试。性能指标由部署方硬件、模型服务能力和数据规模共同决定，测试报告应记录实际服务器配置和并发数。</p>
<table>
  <tr><th>场景</th><th>建议指标</th><th>记录项</th></tr>
  <tr><td>登录</td><td>页面可用，接口成功</td><td>响应时间、错误率。</td></tr>
  <tr><td>文献问答</td><td>稳定返回答案和引用</td><td>首 token 时间、总耗时、引用数量。</td></tr>
  <tr><td>专利问答</td><td>稳定返回答案、引用和原文入口</td><td>检索耗时、图谱耗时、总耗时。</td></tr>
  <tr><td>原文查看</td><td>PDF 可打开</td><td>下载速度、失败率。</td></tr>
  <tr><td>seed 导入</td><td>首次导入完成</td><td>MinIO 导入耗时、Neo4j 加载耗时。</td></tr>
</table>

<h1>11 安全测试建议</h1>
<ol>
  <li>未登录访问受保护页面应跳转到登录页。</li>
  <li>普通用户访问管理员后台应被拒绝。</li>
  <li>停用账号不能登录。</li>
  <li>密码复杂度不满足要求时注册或改密失败。</li>
  <li>HTTPS 证书域名不匹配时客户端应提示风险。</li>
  <li>交付文档和镜像构建上下文中不应包含真实密钥。</li>
</ol>

<h1>12 测试遗留风险</h1>
<p>本文档为初版测试报告模板和清单。正式验收前，需要在目标环境记录真实执行结果。外部模型服务的可用性、响应时间和限流策略不完全由本系统控制，测试时应单独记录模型服务状态。</p>
"""

REQUIREMENT_LIST_DETAIL = """
<h1>需求补充清单</h1>
<table>
  <tr><th>序号</th><th>需求层级</th><th>需求简述</th><th>提出时间</th><th>需求文档</th><th>完成时间</th><th>状态</th><th>备注</th></tr>
  <tr><td class="center">9</td><td>账号能力</td><td>支持注册时绑定人员记录，并由人员记录同步部门信息。</td><td class="center">2026/05/20</td><td>用户管理需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>注册需工号、姓名、校验码。</td></tr>
  <tr><td class="center">10</td><td>账号能力</td><td>支持安全问题找回密码。</td><td class="center">2026/05/20</td><td>用户管理需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>未设置安全问题时需管理员重置。</td></tr>
  <tr><td class="center">11</td><td>管理能力</td><td>支持三级部门维护和批量导入。</td><td class="center">2026/05/20</td><td>管理后台需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>一级、二级、三级部门均可启停。</td></tr>
  <tr><td class="center">12</td><td>管理能力</td><td>支持人员记录维护和批量导入。</td><td class="center">2026/05/20</td><td>管理后台需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>用于账号注册和绑定校验。</td></tr>
  <tr><td class="center">13</td><td>管理能力</td><td>支持普通问答、文件问答、查看原文、文档辅助配额。</td><td class="center">2026/05/20</td><td>配额需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>管理员后台维护。</td></tr>
  <tr><td class="center">14</td><td>网关能力</td><td>统一代理认证、会话、上传、问答和原文接口。</td><td class="center">2026/05/20</td><td>架构需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>前端主要访问 gateway。</td></tr>
  <tr><td class="center">15</td><td>知识图谱</td><td>文献图谱和专利图谱分别以内置 Neo4j 服务部署。</td><td class="center">2026/05/20</td><td>图谱部署需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>部署方不配置 Neo4j 地址。</td></tr>
  <tr><td class="center">16</td><td>运维能力</td><td>支持 preflight 检查部署文件、配置、镜像和数据包。</td><td class="center">2026/05/20</td><td>部署运维需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td><code>deploy/scripts/preflight_check.sh</code>。</td></tr>
  <tr><td class="center">17</td><td>运维能力</td><td>支持同版本 seed 跳过和强制重导。</td><td class="center">2026/05/20</td><td>数据导入需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>通过 marker 和 <code>DATA_SEED_FORCE</code> 控制。</td></tr>
  <tr><td class="center">18</td><td>交付能力</td><td>支持后续单服务镜像增量更新。</td><td class="center">2026/05/20</td><td>更新部署需求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>例如只更新 fastQA 镜像。</td></tr>
</table>
"""

DEPLOYMENT_MANUAL_SECOND_PASS = """
<h1>17 容器服务和数据卷说明</h1>
<p>部署包中的 compose 文件将系统拆分为长期运行服务和一次性 seed job。长期运行服务负责在线访问，一次性 seed job 只在启动阶段执行数据准备。部署方排查问题时，应先区分容器属于哪一类，避免把 seed job 的正常退出误判为异常。</p>
<table>
  <tr><th>服务</th><th>类型</th><th>主要职责</th><th>依赖数据</th></tr>
  <tr><td><code>edge</code></td><td>长期服务</td><td>HTTPS 入口，HTTP 跳转到 HTTPS。</td><td><code>deploy/certs</code>。</td></tr>
  <tr><td><code>frontend</code></td><td>长期服务</td><td>提供 Vue 前端静态页面。</td><td>前端镜像内置 dist。</td></tr>
  <tr><td><code>gateway</code></td><td>长期服务</td><td>统一认证、会话、问答和文件接口代理。</td><td>Redis、public-service、三个 QA 后端。</td></tr>
  <tr><td><code>public-service</code></td><td>长期服务</td><td>用户、部门、人员、配额、文件和公共能力。</td><td>MySQL、Redis、MinIO、public-service reference volume。</td></tr>
  <tr><td><code>fastqa</code></td><td>长期服务</td><td>文献问答。</td><td>fastQA reference volume、MinIO、文献 Neo4j。</td></tr>
  <tr><td><code>highthinkingqa</code></td><td>长期服务</td><td>深度思考问答。</td><td>highThinkingQA reference volume、MinIO。</td></tr>
  <tr><td><code>patent</code></td><td>长期服务</td><td>专利问答。</td><td>patentQA reference volume、MinIO、专利 Neo4j。</td></tr>
  <tr><td><code>mysql</code></td><td>长期服务</td><td>用户态业务数据库。</td><td><code>mysql_data</code>。</td></tr>
  <tr><td><code>redis</code></td><td>长期服务</td><td>缓存、任务状态和运行期协调。</td><td><code>redis_data</code>。</td></tr>
  <tr><td><code>minio</code></td><td>长期服务</td><td>论文、专利原文和运行期对象存储。</td><td><code>minio_data</code>。</td></tr>
  <tr><td><code>neo4j-literature</code></td><td>长期服务</td><td>文献知识图谱。</td><td><code>neo4j_literature_data</code>。</td></tr>
  <tr><td><code>neo4j-patent</code></td><td>长期服务</td><td>专利知识图谱。</td><td><code>neo4j_patent_data</code>。</td></tr>
  <tr><td><code>minio-seed</code></td><td>一次性任务</td><td>导入论文和专利原文。</td><td><code>minio-originals.tar.zst</code>。</td></tr>
  <tr><td><code>*-ref-seed</code></td><td>一次性任务</td><td>导入各服务向量库和 reference data。</td><td><code>*-ref.tar.zst</code>。</td></tr>
  <tr><td><code>neo4j-*-prepare</code>、<code>neo4j-*-seed</code></td><td>一次性任务</td><td>解压并加载 Neo4j dump。</td><td><code>neo4j-*.dump.zst</code>。</td></tr>
</table>

<h1>18 数据包放置和版本对应关系</h1>
<p><code>deploy/data/manifest.json</code> 是数据包的版本索引。部署时，<code>DATA_PACKAGE_VERSION</code> 应与 manifest 中的 <code>data_version</code> 一致。当前交付批次的数据版本为 <code>2026-05-19</code>。如果后续只更新业务镜像，不需要修改数据包版本；如果更新原文、向量库或图谱，需要成套替换 manifest 和数据包。</p>
<table>
  <tr><th>数据包</th><th>用途</th><th>当前关键计数</th><th>导入目标</th></tr>
  <tr><td><code>minio-originals.tar.zst</code></td><td>论文和专利原文。</td><td>papers 7153，专利目录 14006，tables 9581，文件 176292。</td><td>MinIO bucket。</td></tr>
  <tr><td><code>fastqa-ref.tar.zst</code></td><td>fastQA 文献向量库、MD 向量库、主题索引和可选扩展库。</td><td>Chroma SQLite 2 个。</td><td><code>fastqa_ref_data</code>。</td></tr>
  <tr><td><code>highthinking-ref.tar.zst</code></td><td>highThinkingQA vectordb。</td><td>Chroma SQLite 1 个。</td><td><code>highthinking_ref_data</code>。</td></tr>
  <tr><td><code>patentqa-ref.tar.zst</code></td><td>专利向量库和 JSON-only archive。</td><td>专利 JSON 目录 14006。</td><td><code>patentqa_ref_data</code>。</td></tr>
  <tr><td><code>public-service-ref.tar.zst</code></td><td>public-service 轻量 reference data。</td><td>Chroma SQLite 1 个。</td><td><code>public_service_ref_data</code>。</td></tr>
  <tr><td><code>neo4j-literature.dump.zst</code></td><td>文献图谱 dump。</td><td>由维护窗口导出。</td><td><code>neo4j_literature_data</code>。</td></tr>
  <tr><td><code>neo4j-patent.dump.zst</code></td><td>专利图谱 dump。</td><td>由维护窗口导出。</td><td><code>neo4j_patent_data</code>。</td></tr>
</table>

<h1>19 MySQL 初始化内容</h1>
<p>MySQL 初始化脚本只在 Docker volume 首次创建且数据库目录为空时执行。该机制由官方 MySQL 镜像提供。若部署方删除并重建 <code>mysql_data</code> volume，初始化脚本会再次执行；若仅重启容器，不会重复初始化。</p>
<table>
  <tr><th>脚本</th><th>内容</th><th>说明</th></tr>
  <tr><td><code>001_schema.sql</code></td><td>创建 <code>agentcode</code> schema 和表结构。</td><td>不导入当前研发环境的用户、会话和运行数据。</td></tr>
  <tr><td><code>002_seed_departments.sql</code></td><td>导入电池材料技术研究中心部门树。</td><td>不包含测试部门。</td></tr>
  <tr><td><code>003_seed_admin.sql</code></td><td>创建 bootstrap 管理员。</td><td>密码以哈希形式写入，文档不记录明文密码。</td></tr>
</table>
<p>部门 seed 包含一级部门“电池材料技术研究中心”，二级部门“正极材料研究所”“装备工程化研究所”“材料应用研究所”，以及“磷酸铁锂材料开发”“电芯测试”等三级部门。上线后，管理员可在后台继续维护部门和人员。</p>

<h1>20 部署验收步骤明细</h1>
<ol>
  <li>运行预检脚本，确认文件、变量、镜像、数据包、sha256 和 compose 展开通过。</li>
  <li>执行 <code>docker compose ps</code>，确认长期服务运行，seed job 正常退出。</li>
  <li>访问 <code>https://部署域名:端口</code>，确认浏览器进入登录页。</li>
  <li>使用 bootstrap 管理员登录，首次登录后修改密码并设置安全问题。</li>
  <li>进入管理员后台，检查用户管理、部门管理、人员管理、配额管理页面。</li>
  <li>创建或导入一名普通用户，确认其可以登录并绑定人员记录。</li>
  <li>发起文献问答，确认返回答案、引用、阶段耗时和原文入口。</li>
  <li>发起深度问答，确认规划、检索、生成等阶段正常推进。</li>
  <li>发起专利问答，确认专利检索、tables 读取、图谱增强和原文查看可用。</li>
  <li>上传 PDF、Excel 或 CSV 文件并发起文件问答，确认文件参与本轮问答。</li>
</ol>

<h1>21 本机测试和生产部署的隔离建议</h1>
<p>在同一台机器上同时运行研发环境和 Docker 部署环境时，冲突主要来自宿主机端口，而不是容器内服务名。容器内部仍访问 <code>mysql:3306</code>、<code>redis:6379</code>、<code>minio:9000</code>；宿主机通过 <code>MYSQL_PUBLISH_PORT</code> 等变量访问映射后的端口。因此，本机测试可以将 MySQL、Redis、MinIO 和 HTTPS 端口改为独立端口，避免影响已有服务。</p>
<table>
  <tr><th>隔离项</th><th>建议</th><th>说明</th></tr>
  <tr><td>Compose project name</td><td>使用独立 <code>COMPOSE_PROJECT_NAME</code></td><td>避免 named volume 和网络名称混淆。</td></tr>
  <tr><td>Docker bridge subnet</td><td>使用 <code>DOCKER_BRIDGE_SUBNET</code></td><td>避免与宿主机或 VPN 网段冲突。</td></tr>
  <tr><td>MinIO 端口</td><td>使用非默认宿主机端口</td><td>容器内服务仍访问 <code>minio:9000</code>。</td></tr>
  <tr><td>MySQL/Redis 端口</td><td>使用非默认宿主机端口</td><td>不影响已有本地数据库。</td></tr>
  <tr><td>数据目录</td><td>使用 Docker named volume</td><td>不会直接写入研发环境的本地目录。</td></tr>
</table>
"""

OPERATIONS_MANUAL_SECOND_PASS = """
<h1>14 服务运行清单</h1>
<p>运维人员可将下表作为巡检基线。长期运行服务应保持 running 或 healthy；一次性任务在成功执行后通常为 exited 状态，退出码应为 0。</p>
<table>
  <tr><th>服务</th><th>期望状态</th><th>关键检查点</th><th>异常处理入口</th></tr>
  <tr><td><code>edge</code></td><td>running</td><td>证书、HTTPS 端口、反向代理。</td><td>查看 edge 日志和证书文件。</td></tr>
  <tr><td><code>frontend</code></td><td>running</td><td>静态资源、前端路由、网关代理配置。</td><td>访问首页并查看浏览器网络请求。</td></tr>
  <tr><td><code>gateway</code></td><td>running</td><td>认证代理、SSE 代理、后端路由。</td><td>查看 gateway 日志。</td></tr>
  <tr><td><code>public-service</code></td><td>running</td><td>用户、部门、人员、配额、文件。</td><td>查看 public-service 日志和 MySQL 状态。</td></tr>
  <tr><td><code>fastqa</code></td><td>running</td><td>文献向量库、rerank、LLM、MinIO 原文。</td><td>查看 fastqa 日志。</td></tr>
  <tr><td><code>highthinkingqa</code></td><td>running</td><td>深度问答 vectordb、embedding、LLM。</td><td>查看 highthinkingqa 日志。</td></tr>
  <tr><td><code>patent</code></td><td>running</td><td>专利向量库、intent、rerank、图谱、tables。</td><td>查看 patent 日志。</td></tr>
  <tr><td><code>mysql</code></td><td>healthy</td><td>连接、磁盘、初始化脚本是否只执行一次。</td><td>查看 MySQL 容器日志。</td></tr>
  <tr><td><code>redis</code></td><td>healthy</td><td>密码、AOF、连接数。</td><td>查看 Redis 日志。</td></tr>
  <tr><td><code>minio</code></td><td>running</td><td>bucket、对象数量、控制台访问。</td><td>查看 MinIO 日志。</td></tr>
  <tr><td><code>neo4j-literature</code></td><td>healthy</td><td>文献图谱可查询。</td><td>查看 Neo4j 日志。</td></tr>
  <tr><td><code>neo4j-patent</code></td><td>healthy</td><td>专利图谱可查询。</td><td>查看 Neo4j 日志。</td></tr>
</table>

<h1>15 备份和恢复操作建议</h1>
<h2>15.1 MySQL 备份</h2>
<p>MySQL 保存用户、会话、文件元数据、配额和安全问题，是最重要的运行态数据。建议按业务要求制定每日或每周备份计划，并定期做恢复演练。</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml exec mysql \
  mysqldump -uroot -p agentcode &gt; agentcode-backup.sql</pre>
<p>恢复前应确认目标环境停止写入，并保留当前备份。恢复操作应在测试环境演练后再用于生产。</p>

<h2>15.2 MinIO 备份</h2>
<p>MinIO 中的初始论文和专利原文可由 <code>minio-originals.tar.zst</code> 重建。运行期用户上传文件、会话导出的对象和新增原文不一定在初始数据包中，因此需要按部署方存储策略备份 <code>minio_data</code> 或通过对象存储工具做增量同步。</p>

<h2>15.3 配置和证书备份</h2>
<p><code>deploy/.env</code>、<code>deploy/certs/fullchain.pem</code>、<code>deploy/certs/privkey.pem</code> 不能从镜像或数据包自动恢复，应在变更后纳入加密备份。私钥文件建议只允许运维用户读取。</p>

<h2>15.4 Reference data 和图谱恢复</h2>
<p>reference data 和 Neo4j 初始图谱可由数据包重建。恢复时应先确认数据包版本，再决定是否设置 <code>DATA_SEED_FORCE=1</code>。强制重导会覆盖目标 reference volume 或 Neo4j data volume，执行前应确认没有运行期新增图谱写入需要保留。</p>

<h1>16 模型服务巡检</h1>
<p>LiFeO4Agent 的问答质量和响应时间依赖外部模型服务。运维应对 LLM、intent、embedding 和 rerank 分别巡检，不宜只看最终问答是否成功。</p>
<table>
  <tr><th>模型类别</th><th>相关变量</th><th>巡检重点</th><th>异常影响</th></tr>
  <tr><td>LLM</td><td><code>LLM_BASE_URL</code>、<code>LLM_MODEL</code>、<code>LLM_API_KEY</code></td><td>连接、鉴权、模型名、stream 能力。</td><td>答案无法生成或阶段卡在生成。</td></tr>
  <tr><td>Intent</td><td><code>INTENT_MODEL_*</code></td><td>开关、模型调用格式、超时。</td><td>意图识别失败，可能降级到默认路由。</td></tr>
  <tr><td>QA Embedding</td><td><code>QA_EMBEDDING_*</code></td><td>向量维度、接口兼容、吞吐。</td><td>文献和专利检索失败。</td></tr>
  <tr><td>HighThinking Embedding</td><td><code>HIGHTHINKINGQA_EMBEDDING_*</code></td><td>模型名和接口兼容。</td><td>深度问答检索失败。</td></tr>
  <tr><td>Rerank</td><td><code>RERANK_*</code></td><td>provider、base url、模型名。</td><td>检索结果排序质量下降或重排阶段报错。</td></tr>
</table>

<h1>17 常见日志关键字</h1>
<table>
  <tr><th>关键字</th><th>可能原因</th><th>排查建议</th></tr>
  <tr><td><code>HIGHTHINKINGQA_EMBEDDING_API_KEY is not configured</code></td><td>深度问答 embedding key 未配置。</td><td>检查 <code>deploy/.env</code> 并重启 highthinkingqa。</td></tr>
  <tr><td><code>enable_thinking only support stream call</code></td><td>模型参数与非流式调用不兼容。</td><td>检查对应服务是否对该模型发送了不支持的参数。</td></tr>
  <tr><td><code>package not found</code></td><td>数据包缺失或文件名不一致。</td><td>检查 <code>deploy/data</code> 和 manifest。</td></tr>
  <tr><td><code>sha256 mismatch</code></td><td>数据包损坏或 manifest 不匹配。</td><td>重新传输同批数据包。</td></tr>
  <tr><td><code>chroma.sqlite3</code></td><td>向量库缺失或路径不正确。</td><td>检查 ref seed 是否成功。</td></tr>
  <tr><td><code>AccessDenied</code></td><td>MinIO 账号、密码或 bucket 权限异常。</td><td>检查 MinIO 配置和 bucket 初始化。</td></tr>
  <tr><td><code>cypher-shell</code></td><td>Neo4j 未就绪或密码不一致。</td><td>检查 Neo4j seed 和 healthcheck。</td></tr>
</table>

<h1>18 容量和增长管理</h1>
<p>当前原文数据包较大，首次导入会占用明显磁盘空间。运维应关注 Docker root 目录所在磁盘、MinIO volume、Neo4j volume、MySQL volume 和日志增长。若部署方使用独立挂载盘，应将 Docker 数据目录或相关 volume 放在容量充足的盘上。</p>
<ol>
  <li>每周记录 <code>docker system df</code> 输出，观察镜像、容器和 volume 增长。</li>
  <li>定期清理已不再使用的旧镜像，但保留最近一个可回滚版本。</li>
  <li>MinIO 原文数据不要在后端 volume 中重复存放。</li>
  <li>日志策略由部署方按平台规范控制，避免长期无限增长。</li>
  <li>数据包和导出 tar 可迁移到归档存储，不建议长期堆放在部署机根分区。</li>
</ol>

<h1>19 证书更新流程</h1>
<ol>
  <li>准备新的 <code>fullchain.pem</code> 和 <code>privkey.pem</code>，确认域名与 SAN 匹配。</li>
  <li>备份当前证书文件。</li>
  <li>替换 <code>deploy/certs</code> 下的证书和私钥。</li>
  <li>执行 <code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml restart edge</code>。</li>
  <li>使用浏览器或证书检查工具确认新证书已生效。</li>
</ol>
"""

USER_MANUAL_SECOND_PASS = """
<h1>13 首次使用完整流程</h1>
<h2>13.1 管理员首次登录</h2>
<ol>
  <li>访问系统 HTTPS 地址，进入登录页。</li>
  <li>使用交付时确认的 bootstrap 管理员账号登录。</li>
  <li>系统提示首次登录时，按页面要求修改密码。</li>
  <li>设置安全问题，便于后续找回密码或完成安全校验。</li>
  <li>进入管理员后台，确认部门树已经包含电池材料技术研究中心及其下属部门。</li>
  <li>创建或导入人员记录，再创建用户或让用户自助注册。</li>
</ol>

<h2>13.2 普通用户注册</h2>
<p>普通用户注册时需要提供用户名、密码、姓名、工号和校验码。姓名、工号和校验码需要与管理员提前维护的人员记录匹配。注册成功后，用户的部门信息由人员记录统一带出，不需要用户自行选择部门。</p>
<table>
  <tr><th>字段</th><th>填写说明</th><th>常见错误</th></tr>
  <tr><td>用户名</td><td>3 到 50 个字符，不能以 <code>admin</code> 开头。</td><td>用户名重复或格式不符合要求。</td></tr>
  <tr><td>密码</td><td>按页面密码复杂度要求填写。</td><td>两次输入不一致或复杂度不足。</td></tr>
  <tr><td>姓名</td><td>与人员记录中的姓名一致。</td><td>姓名和工号不匹配。</td></tr>
  <tr><td>工号</td><td>由管理员维护在人员记录中。</td><td>工号不存在或已停用。</td></tr>
  <tr><td>校验码</td><td>由管理员维护并分发给对应人员。</td><td>校验码错误。</td></tr>
</table>

<h1>14 文献问答操作细节</h1>
<p>文献模式适合围绕论文原文和文献知识库提问。提问时建议明确材料体系、工艺、性能指标和希望对比的维度。系统会进行检索、可选重排、答案生成，并在回答中展示引用来源。</p>
<ol>
  <li>在首页底部模式选择中选择“文献”。</li>
  <li>输入具体问题，例如围绕包覆改性、倍率性能、循环稳定性或合成工艺提问。</li>
  <li>提交后观察阶段信息，等待回答完成。</li>
  <li>查看引用列表，必要时打开论文原文核对。</li>
  <li>如果回答范围过宽，可追问“只看近五年文献”或“按工艺路线分组”。</li>
</ol>

<h1>15 深度问答操作细节</h1>
<p>深度模式适合综合分析、方案比较和需要多阶段推理的问题。此模式耗时可能长于文献模式。回答过程中会展示阶段进度，用户可通过阶段和总耗时判断任务推进情况。</p>
<table>
  <tr><th>适合问题</th><th>不适合问题</th><th>使用建议</th></tr>
  <tr><td>技术路线比较、复杂原因分析、研发方案拆解。</td><td>只需要查一个事实或打开原文。</td><td>问题中写清目标、约束和输出形式。</td></tr>
  <tr><td>跨多篇文献归纳、技术风险梳理。</td><td>只涉及单个文件的表格读取。</td><td>可要求按表格或条目输出。</td></tr>
</table>

<h1>16 专利问答操作细节</h1>
<p>专利模式适合查询专利技术方案、权利要求、申请人、发明点、表格数据和附图信息。系统会使用专利向量库、JSON-only archive、MinIO 原文和专利知识图谱提供回答支撑。</p>
<ol>
  <li>选择“专利”模式。</li>
  <li>尽量提供专利号、关键词、材料体系或技术方向。</li>
  <li>需要表格时，可明确说明“读取专利表格数据”或“比较表格中的参数”。</li>
  <li>需要原文核对时，点击回答中的专利原文入口。</li>
  <li>如果问题涉及关系推理，可要求系统结合专利图谱分析。</li>
</ol>

<h1>17 文件问答操作细节</h1>
<p>用户可以上传 PDF、Excel 或 CSV 文件。文件上传后会出现在会话文件列表中。系统支持基于上传文件问答，也支持结合知识库和上传文件一起回答。</p>
<table>
  <tr><th>文件类型</th><th>适合场景</th><th>提问建议</th></tr>
  <tr><td>PDF</td><td>论文、报告、说明书。</td><td>说明要总结、抽取参数还是比较结论。</td></tr>
  <tr><td>Excel</td><td>实验记录、测试数据、配方表。</td><td>指出关注的列、指标或筛选条件。</td></tr>
  <tr><td>CSV</td><td>结构化实验数据。</td><td>适合统计、筛选和字段解释。</td></tr>
</table>
<p>如果本轮问题不希望使用某个文件，应在发送前取消勾选。上传过程中不要刷新页面，以免影响上传状态显示。</p>

<h1>18 管理后台详细说明</h1>
<h2>18.1 用户管理</h2>
<p>管理员可查看用户列表，按用户名或状态筛选用户，创建、停用、启用、重置用户密码，并查看用户是否完成首次登录设置。停用用户后，用户不能继续登录，但历史记录仍保留。</p>

<h2>18.2 部门管理</h2>
<p>部门管理支持一级、二级、三级结构。当前交付 seed 已包含电池材料技术研究中心、正极材料研究所、装备工程化研究所、材料应用研究所及三级部门。管理员可以新增、重命名、停用或启用部门。停用部门不删除历史绑定关系。</p>

<h2>18.3 人员管理</h2>
<p>人员管理用于维护工号、姓名、校验码和部门。普通用户注册或在个人中心补全人员信息时，需要与人员记录匹配。人员停用后，新注册或绑定会受到限制。</p>

<h2>18.4 配额管理</h2>
<p>配额管理覆盖普通问答、文件问答、查看原文和文档辅助等类型。管理员可以设置默认周期和限制，也可以对单个用户设置例外值。用户触发配额限制时，页面会展示提示并引导联系管理员。</p>

<h1>19 常见用户问题处理</h1>
<table>
  <tr><th>问题</th><th>原因</th><th>处理方式</th></tr>
  <tr><td>无法登录</td><td>密码错误、账号停用或 token 失效。</td><td>检查账号状态，必要时联系管理员重置密码。</td></tr>
  <tr><td>注册失败</td><td>人员记录不匹配或校验码错误。</td><td>联系管理员核对工号、姓名和校验码。</td></tr>
  <tr><td>被要求进入个人中心</td><td>首次登录需改密、设置安全问题或补全人员信息。</td><td>按页面提示完成设置。</td></tr>
  <tr><td>问答提示配额不足</td><td>本周期配额已用完。</td><td>联系管理员调整或等待下个周期。</td></tr>
  <tr><td>原文打不开</td><td>对象不存在、权限不足或 MinIO 异常。</td><td>重试后仍失败时联系运维检查 MinIO。</td></tr>
  <tr><td>回答很慢</td><td>深度问题、模型排队或检索数据量较大。</td><td>等待完成，或缩小问题范围。</td></tr>
</table>
"""

SUMMARY_DESIGN_SECOND_PASS = """
<h1>12 系统上下文</h1>
<p>LiFeO4Agent 面向电池材料研发场景，提供文献问答、深度思考问答和专利问答。系统边界内包含前端、网关、公共服务、三个领域问答服务、基础存储和离线数据导入能力；系统边界外包含部署方提供的 LLM、intent、embedding 和 rerank 模型服务。</p>
<table>
  <tr><th>参与方</th><th>职责</th><th>交互方式</th></tr>
  <tr><td>最终用户</td><td>登录系统，发起问答，上传文件，查看原文。</td><td>浏览器访问 HTTPS 入口。</td></tr>
  <tr><td>管理员</td><td>维护用户、部门、人员和配额。</td><td>通过管理后台操作。</td></tr>
  <tr><td>平台运维</td><td>部署、升级、备份、证书和数据包维护。</td><td>通过 Docker 和部署目录操作。</td></tr>
  <tr><td>模型服务</td><td>提供生成、意图、向量化和重排能力。</td><td>通过 HTTP API 调用。</td></tr>
  <tr><td>对象存储</td><td>保存论文、专利原文和运行期对象。</td><td>通过 MinIO S3 API 调用。</td></tr>
</table>

<h1>13 总体部署拓扑</h1>
<p>所有容器运行在 compose 默认网络中，网络名由 <code>COMPOSE_PROJECT_NAME</code> 控制。部署方访问 <code>edge</code> 暴露的 HTTP/HTTPS 端口；后端之间使用容器服务名通信。MySQL、Redis 和 MinIO 可以按部署方要求暴露宿主机端口，业务服务本身不直接暴露到客户访问面。</p>
<ol>
  <li>浏览器访问 edge。</li>
  <li>edge 将 HTTPS 请求代理到 frontend。</li>
  <li>frontend 通过 nginx 代理访问 gateway。</li>
  <li>gateway 将认证、文件、会话、问答请求转给 public-service 或对应 QA 后端。</li>
  <li>QA 后端访问 reference volume、MinIO、Neo4j 和模型服务。</li>
  <li>回答以 SSE 或普通 HTTP 响应返回前端。</li>
</ol>

<h1>14 业务流程概要</h1>
<table>
  <tr><th>流程</th><th>概要步骤</th><th>关键数据</th></tr>
  <tr><td>登录</td><td>用户提交凭据，public-service 校验密码哈希，返回 token 和用户信息。</td><td>MySQL users、password_history。</td></tr>
  <tr><td>注册</td><td>用户填写人员信息，系统校验人员记录和校验码，创建用户。</td><td>personnel_records、users。</td></tr>
  <tr><td>问答</td><td>gateway 校验 token 和配额，路由到对应 QA 后端，后端检索、重排、生成。</td><td>Redis、reference volume、MinIO、Neo4j、模型服务。</td></tr>
  <tr><td>文件问答</td><td>用户上传文件，public-service 保存元数据和对象，gateway 将文件上下文传给 QA 后端。</td><td>conversation_files、MinIO。</td></tr>
  <tr><td>原文查看</td><td>前端请求原文，后端生成或代理对象访问路径。</td><td>MinIO papers、patent/originals。</td></tr>
  <tr><td>配额扣减</td><td>请求前预检，完成后记账。</td><td>quota_configs、user_quota_usage、user_quota_overrides。</td></tr>
</table>

<h1>15 交付设计取舍</h1>
<p>本系统没有将 50GB 级原文数据直接打入业务镜像，而是采用镜像和数据包分离的方式。这样做可以让业务镜像按服务增量更新，让数据包独立校验和复用，并避免因为单个后端代码变化重新分发大体积数据。</p>
<table>
  <tr><th>方案</th><th>优点</th><th>缺点</th><th>采用情况</th></tr>
  <tr><td>数据打入业务镜像</td><td>单文件交付直观。</td><td>镜像巨大，更新慢，重复存储多。</td><td>未采用。</td></tr>
  <tr><td>宿主机手工拷贝大目录</td><td>构建快。</td><td>部署步骤多，容易漏文件，工具依赖多。</td><td>未采用。</td></tr>
  <tr><td>镜像 + 数据包 + seed job</td><td>可离线、可校验、可增量、部署方不用安装额外工具。</td><td>首次 seed 耗时较长。</td><td>采用。</td></tr>
</table>

<h1>16 非功能设计</h1>
<table>
  <tr><th>目标</th><th>设计措施</th></tr>
  <tr><td>可部署性</td><td>compose 编排所有服务和 seed job，部署方只操作镜像包、数据包和 <code>.env</code>。</td></tr>
  <tr><td>可维护性</td><td>服务职责拆分，配置面收敛，后续可单服务镜像更新。</td></tr>
  <tr><td>可靠性</td><td>healthcheck 控制依赖启动顺序，seed marker 控制幂等。</td></tr>
  <tr><td>安全性</td><td>HTTPS 入口、JWT、内部 token、密码哈希、密钥不写入文档。</td></tr>
  <tr><td>可观测性</td><td>容器日志、阶段事件、seed 日志和 preflight 输出用于定位问题。</td></tr>
  <tr><td>可恢复性</td><td>运行态数据和可重建数据区分备份策略。</td></tr>
</table>
"""

DETAILED_DESIGN_SECOND_PASS = """
<h1>15 数据库详细设计补充</h1>
<p>部署数据库是用户态业务库，初始化时只导入 schema、部门树和 bootstrap 管理员，不导入研发环境的历史用户、会话或业务快照。主要表如下。</p>
<table>
  <tr><th>表</th><th>职责</th><th>关键关系</th></tr>
  <tr><td><code>users</code></td><td>账号、角色、状态、首次登录、安全设置和部门绑定。</td><td>关联人员表和三级部门表。</td></tr>
  <tr><td><code>password_history</code></td><td>密码历史。</td><td>按用户关联，用于密码策略。</td></tr>
  <tr><td><code>user_security_questions</code></td><td>安全问题和答案哈希。</td><td>按用户关联。</td></tr>
  <tr><td><code>primary_departments</code></td><td>一级部门。</td><td>被二级部门和用户引用。</td></tr>
  <tr><td><code>secondary_departments</code></td><td>二级部门。</td><td>属于一级部门，被三级部门和用户引用。</td></tr>
  <tr><td><code>tertiary_departments</code></td><td>三级部门。</td><td>属于二级部门，被用户和人员引用。</td></tr>
  <tr><td><code>personnel_records</code></td><td>人员工号、姓名、校验码哈希和部门。</td><td>用于注册和个人中心绑定。</td></tr>
  <tr><td><code>quota_configs</code></td><td>配额类型、周期和默认限制。</td><td>被用户用量和用户例外引用。</td></tr>
  <tr><td><code>user_quota_usage</code></td><td>用户在周期内的已用次数。</td><td>唯一键为用户、配额类型、周期。</td></tr>
  <tr><td><code>user_quota_overrides</code></td><td>单用户自定义配额。</td><td>覆盖默认配额。</td></tr>
  <tr><td><code>conversations</code></td><td>会话主表和 chat json 同步状态。</td><td>关联用户。</td></tr>
  <tr><td><code>conversation_messages</code></td><td>会话消息。</td><td>关联会话和用户。</td></tr>
  <tr><td><code>conversation_files</code></td><td>会话文件元数据。</td><td>关联会话和用户，保存 storage_ref。</td></tr>
  <tr><td><code>conversation_json_outbox</code></td><td>会话 JSON 异步同步任务。</td><td>用于本地和对象存储同步。</td></tr>
</table>

<h1>16 MinIO 对象设计</h1>
<p>MinIO bucket 名由 <code>MINIO_BUCKET</code> 指定，数据包内部不绑定 bucket。对象路径采用稳定前缀，便于后端按统一规则读取。</p>
<table>
  <tr><th>前缀</th><th>内容</th><th>读取服务</th></tr>
  <tr><td><code>papers/</code></td><td>论文原文 PDF。</td><td>fastQA、highThinkingQA、public-service。</td></tr>
  <tr><td><code>patent/originals/&lt;id&gt;/</code></td><td>专利原文目录。</td><td>patentQA。</td></tr>
  <tr><td><code>patent/originals/&lt;id&gt;/manifest.json</code></td><td>专利对象登记文件。</td><td>patentQA。</td></tr>
  <tr><td><code>patent/originals/&lt;id&gt;/structured/tables.json</code></td><td>专利表格结构化数据。</td><td>patentQA。</td></tr>
  <tr><td><code>_deploy/data-seed/minio-originals/&lt;version&gt;.done</code></td><td>MinIO seed marker。</td><td>seed job。</td></tr>
</table>
<p>专利 tables 导入要求：本地 resource 中的 <code>*_tables.json</code> 数量应与 seed 后的 <code>structured/tables.json</code> 数量一致；带 tables 的 manifest 必须登记 <code>objects.structured.tables</code>，并设置 <code>availability.tables</code>。</p>

<h1>17 向量库挂载设计</h1>
<p>向量库通过 reference named volume 挂载到容器内部固定路径，部署方不需要在 <code>.env</code> 中手工指定向量库路径。路径由 compose 固化，seed job 负责把数据包解压到 volume。</p>
<table>
  <tr><th>服务</th><th>容器内路径</th><th>数据包来源</th><th>说明</th></tr>
  <tr><td>fastQA</td><td><code>/ref/fastqa/vector_database</code></td><td><code>fastqa-ref.tar.zst</code></td><td>主文献向量库。</td></tr>
  <tr><td>fastQA</td><td><code>/ref/fastqa/vector_database_md</code></td><td><code>fastqa-ref.tar.zst</code></td><td>Markdown 或结构化文献库。</td></tr>
  <tr><td>fastQA</td><td><code>/ref/fastqa/community_vector_database</code></td><td><code>fastqa-ref.tar.zst</code></td><td>可选扩展库。</td></tr>
  <tr><td>fastQA</td><td><code>/ref/fastqa/vector_db_topic_index.json</code></td><td><code>fastqa-ref.tar.zst</code></td><td>主题索引。</td></tr>
  <tr><td>highThinkingQA</td><td><code>/ref/highthinkingqa/vectordb</code></td><td><code>highthinking-ref.tar.zst</code></td><td>深度问答向量库。</td></tr>
  <tr><td>patentQA</td><td><code>/app/resource/patentQA/vector_db_patent_abstracts</code></td><td><code>patentqa-ref.tar.zst</code></td><td>专利摘要向量库。</td></tr>
  <tr><td>patentQA</td><td><code>/app/resource/patentQA/vector_db_patent_chunks</code></td><td><code>patentqa-ref.tar.zst</code></td><td>专利片段向量库。</td></tr>
  <tr><td>public-service</td><td><code>/ref/public-service/vector_database</code></td><td><code>public-service-ref.tar.zst</code></td><td>公共轻量向量库。</td></tr>
</table>

<h1>18 流式问答事件设计</h1>
<p>前端会渲染后端发出的阶段事件、文本增量、引用信息和完成事件。intent、检索、rerank、图谱、生成等阶段都可以作为步骤展示。阶段事件应包含阶段名称、状态、耗时或时间戳，以便用户判断进度，也便于运维从日志中对应排查。</p>
<table>
  <tr><th>事件类别</th><th>含义</th><th>前端表现</th></tr>
  <tr><td>阶段开始</td><td>某一处理阶段开始。</td><td>显示步骤为进行中。</td></tr>
  <tr><td>阶段结束</td><td>某一处理阶段完成。</td><td>显示完成状态和耗时。</td></tr>
  <tr><td>文本增量</td><td>LLM 输出回答片段。</td><td>实时追加到回答区域。</td></tr>
  <tr><td>引用</td><td>返回文献、专利或文件来源。</td><td>展示引用列表和原文入口。</td></tr>
  <tr><td>错误</td><td>某阶段失败。</td><td>显示可理解的错误提示。</td></tr>
  <tr><td>完成</td><td>本轮问答结束。</td><td>停止加载状态，固化回答。</td></tr>
</table>

<h1>19 配额扣减设计</h1>
<p>配额由 public-service 统一管理。gateway 在问答开始前进行 precheck，确认用户有足够额度；问答完成后根据结果 finalize。这样可以避免失败请求错误扣减，也可以将不同后端的配额逻辑收敛到统一服务。</p>
<ol>
  <li>gateway 根据请求类型判断配额类型。</li>
  <li>调用 public-service 执行 precheck。</li>
  <li>请求路由到 fastQA、highThinkingQA 或 patentQA。</li>
  <li>后端返回完成或错误事件。</li>
  <li>gateway 根据结果 finalize 配额。</li>
  <li>public-service 更新 <code>user_quota_usage</code>。</li>
</ol>

<h1>20 错误处理和降级设计</h1>
<table>
  <tr><th>异常</th><th>系统行为</th><th>用户可见结果</th></tr>
  <tr><td>模型调用失败</td><td>后端捕获异常并返回错误事件。</td><td>提示模型服务异常或参数不兼容。</td></tr>
  <tr><td>embedding 失败</td><td>检索阶段失败或降级。</td><td>提示检索失败。</td></tr>
  <tr><td>rerank 不可用</td><td>按配置决定报错或跳过重排。</td><td>可能引用排序质量下降。</td></tr>
  <tr><td>MinIO 对象缺失</td><td>原文读取返回结构化错误。</td><td>原文打开失败。</td></tr>
  <tr><td>Neo4j 不可用</td><td>图谱增强失败，日志记录细节。</td><td>专利或文献图谱能力不可用。</td></tr>
  <tr><td>配额不足</td><td>请求前阻断。</td><td>显示配额提示卡片。</td></tr>
</table>
"""

DEVELOPMENT_DOC_SECOND_PASS = """
<h1>13 仓库目录说明</h1>
<table>
  <tr><th>目录</th><th>职责</th><th>开发注意事项</th></tr>
  <tr><td><code>frontend-vue</code></td><td>Vue 3 + Vite 前端。</td><td>交付前执行 <code>npm run build</code> 并重新构建前端镜像。</td></tr>
  <tr><td><code>gateway</code></td><td>FastAPI 网关。</td><td>维护路由决策、SSE 代理、配额 precheck/finalize。</td></tr>
  <tr><td><code>public-service</code></td><td>公共能力后端。</td><td>用户、部门、人员、配额、文件和 MinIO 公共能力。</td></tr>
  <tr><td><code>fastQA</code></td><td>文献问答后端。</td><td>维护文献检索、rerank、图谱和原文访问。</td></tr>
  <tr><td><code>highThinkingQA</code></td><td>深度问答后端。</td><td>维护多阶段深度问答和独立 embedding。</td></tr>
  <tr><td><code>patent</code></td><td>专利问答后端。</td><td>维护专利检索、tables、图谱和原文访问。</td></tr>
  <tr><td><code>resource</code></td><td>共享资源、配置和本地数据源。</td><td>构建数据包时从该目录收集原文和 reference data。</td></tr>
  <tr><td><code>deploy</code></td><td>离线部署编排、脚本和初始化文件。</td><td>任何配置面变化都要同步此目录。</td></tr>
</table>

<h1>14 本地开发和验证命令</h1>
<table>
  <tr><th>场景</th><th>命令</th><th>说明</th></tr>
  <tr><td>启动前端开发服务</td><td><code>cd frontend-vue &amp;&amp; npm run dev</code></td><td>默认 Vite 端口。</td></tr>
  <tr><td>构建前端</td><td><code>cd frontend-vue &amp;&amp; npm run build</code></td><td>生成 dist，用于前端镜像。</td></tr>
  <tr><td>启动本地后端栈</td><td><code>bash scripts/start_all.sh</code></td><td>研发环境使用。</td></tr>
  <tr><td>查看后端状态</td><td><code>bash scripts/status_all.sh</code></td><td>检查本地进程。</td></tr>
  <tr><td>停止本地后端栈</td><td><code>bash scripts/stop_all.sh</code></td><td>释放端口和资源。</td></tr>
  <tr><td>部署预检</td><td><code>bash deploy/scripts/preflight_check.sh deploy/.env</code></td><td>正式部署前必须执行。</td></tr>
  <tr><td>数据包校验</td><td><code>python deploy/scripts/validate_data_packages.py --data-dir deploy/data --require-all</code></td><td>检查 manifest 和 sha256。</td></tr>
</table>

<h1>15 配置开发规则</h1>
<p>模型和基础设施配置必须区分 shared 和 secret。非敏感配置放在 shared env，API Key、密码、token 放在 secret env 或部署 <code>.env</code> 中。新增客户可配置项时，应同步以下位置。</p>
<ol>
  <li>本地共享配置文件，例如 <code>resource/config/shared/model-endpoints.shared.env</code>。</li>
  <li>本地 secret 配置文件，例如 <code>resource/config/shared/model-endpoints.secret.env</code>。</li>
  <li>对应后端的配置加载逻辑。</li>
  <li><code>deploy/.env.production.example</code>。</li>
  <li><code>deploy/docker-compose.yml</code> 的 environment 映射。</li>
  <li>部署手册、运维手册和详细设计中的配置表。</li>
</ol>

<h1>16 镜像构建和增量交付规则</h1>
<p>镜像命名使用 Docker 规范的小写仓库名，例如 <code>lifeo4agent/fastqa</code>。产品名称在文档中写作 LiFeO4Agent。后续更新时，修改哪个服务就优先只交付哪个服务镜像；只有接口契约、前端页面或 shared 依赖变化时，才需要联动更新其他镜像。</p>
<table>
  <tr><th>变更内容</th><th>需要交付</th><th>是否需要重发数据包</th></tr>
  <tr><td>只修改 fastQA 逻辑</td><td>fastQA 镜像。</td><td>否。</td></tr>
  <tr><td>只修改前端样式或交互</td><td>frontend 镜像。</td><td>否。</td></tr>
  <tr><td>修改 gateway 路由契约</td><td>gateway 镜像，可能需要前端或后端。</td><td>否。</td></tr>
  <tr><td>修改数据库 schema</td><td>相关后端镜像和 SQL 迁移。</td><td>通常否。</td></tr>
  <tr><td>更新向量库、原文或图谱</td><td>数据包和 manifest。</td><td>是。</td></tr>
  <tr><td>更新 seed 脚本</td><td>seed-tools 镜像和 deploy 脚本。</td><td>视情况。</td></tr>
</table>

<h1>17 数据包开发规则</h1>
<p>数据包由 <code>deploy/scripts/package_data.sh</code> 生成。构建前应先收集 MinIO seed，确保专利 tables 已回填，并在 Neo4j 维护窗口内生成一致性 dump。</p>
<ol>
  <li>运行 <code>collect_minio_seed.sh</code> 生成 <code>papers/</code> 和 <code>patent/originals/</code>。</li>
  <li>确认 tables 数量与 resource 中 <code>*_tables.json</code> 数量一致。</li>
  <li>准备 fastQA、highThinkingQA、patentQA、public-service reference data。</li>
  <li>在图谱冻结窗口导出文献和专利 Neo4j dump。</li>
  <li>运行 <code>package_data.sh</code> 打包。</li>
  <li>运行 <code>validate_data_packages.py</code> 校验。</li>
  <li>更新 manifest 和数据包版本记录。</li>
</ol>

<h1>18 发布检查清单</h1>
<ol>
  <li>确认工作区无误提交的密钥、日志和本地数据。</li>
  <li>前端构建通过，并已同步到前端镜像。</li>
  <li>受影响后端测试通过。</li>
  <li>compose config 可展开。</li>
  <li>preflight 在交付目录通过。</li>
  <li>镜像 tar 可 <code>docker load</code>。</li>
  <li>数据包 manifest sha256 与实际文件一致。</li>
  <li>文档版本、日期、端口和配置项与交付包一致。</li>
</ol>
"""

TEST_REPORT_SECOND_PASS = """
<h1>13 测试环境记录项</h1>
<p>正式测试报告应记录实际测试环境信息。下表给出需要填写的项目，便于后续复现问题和评估性能。</p>
<table>
  <tr><th>项目</th><th>记录内容</th></tr>
  <tr><td>服务器</td><td>CPU、内存、磁盘、操作系统版本。</td></tr>
  <tr><td>Docker</td><td>Docker Engine 版本、Compose v2 版本。</td></tr>
  <tr><td>部署包</td><td>镜像包版本、数据包版本、manifest 生成时间。</td></tr>
  <tr><td>模型服务</td><td>LLM、intent、embedding、rerank 的模型名和服务地址类型。</td></tr>
  <tr><td>网络</td><td>域名、端口、HTTPS 证书类型、内网访问范围。</td></tr>
  <tr><td>测试账号</td><td>管理员和普通用户账号，不记录明文密码。</td></tr>
</table>

<h1>14 详细测试用例</h1>
<table>
  <tr><th>编号</th><th>类别</th><th>测试内容</th><th>预期结果</th></tr>
  <tr><td>TC-001</td><td>部署</td><td>执行 preflight。</td><td>文件、变量、数据包、sha256、compose 均通过。</td></tr>
  <tr><td>TC-002</td><td>部署</td><td>首次 compose up。</td><td>seed job 成功退出，长期服务启动。</td></tr>
  <tr><td>TC-003</td><td>部署</td><td>第二次 compose up。</td><td>同版本 seed job 跳过。</td></tr>
  <tr><td>TC-004</td><td>HTTPS</td><td>访问 HTTP 端口。</td><td>跳转到 HTTPS。</td></tr>
  <tr><td>TC-005</td><td>HTTPS</td><td>访问 HTTPS 域名。</td><td>证书链可识别，页面加载。</td></tr>
  <tr><td>TC-006</td><td>认证</td><td>管理员登录。</td><td>进入管理员后台。</td></tr>
  <tr><td>TC-007</td><td>认证</td><td>普通用户注册。</td><td>人员校验通过后创建账号。</td></tr>
  <tr><td>TC-008</td><td>认证</td><td>首次登录强制设置。</td><td>跳转个人中心并完成设置。</td></tr>
  <tr><td>TC-009</td><td>认证</td><td>忘记密码。</td><td>安全问题验证后允许重置。</td></tr>
  <tr><td>TC-010</td><td>管理</td><td>部门树查看。</td><td>显示电池材料技术研究中心及下属部门。</td></tr>
  <tr><td>TC-011</td><td>管理</td><td>人员新增和停用。</td><td>人员状态正确影响注册和绑定。</td></tr>
  <tr><td>TC-012</td><td>管理</td><td>用户停用。</td><td>停用用户无法继续登录。</td></tr>
  <tr><td>TC-013</td><td>管理</td><td>配额设置。</td><td>配额不足时前端提示。</td></tr>
  <tr><td>TC-014</td><td>文献问答</td><td>发起文献问题。</td><td>返回答案、引用、阶段耗时。</td></tr>
  <tr><td>TC-015</td><td>文献问答</td><td>打开论文原文。</td><td>从 MinIO 获取 PDF。</td></tr>
  <tr><td>TC-016</td><td>深度问答</td><td>发起综合分析问题。</td><td>分阶段返回深度回答。</td></tr>
  <tr><td>TC-017</td><td>专利问答</td><td>发起专利检索问题。</td><td>返回专利引用和原文入口。</td></tr>
  <tr><td>TC-018</td><td>专利问答</td><td>查询专利 tables。</td><td>读取 structured/tables.json。</td></tr>
  <tr><td>TC-019</td><td>图谱</td><td>文献图谱代表查询。</td><td>Neo4j literature 可返回结果。</td></tr>
  <tr><td>TC-020</td><td>图谱</td><td>专利图谱代表查询。</td><td>Neo4j patent 可返回结果。</td></tr>
  <tr><td>TC-021</td><td>文件</td><td>上传 PDF 问答。</td><td>文件参与回答。</td></tr>
  <tr><td>TC-022</td><td>文件</td><td>上传 Excel 或 CSV 问答。</td><td>表格数据可被解析和回答。</td></tr>
  <tr><td>TC-023</td><td>模型</td><td>intent 开启后发起问答。</td><td>日志可见 intent 阶段调用。</td></tr>
  <tr><td>TC-024</td><td>模型</td><td>rerank 开启后发起检索。</td><td>日志可见 rerank 阶段调用。</td></tr>
  <tr><td>TC-025</td><td>稳定性</td><td>连续多轮会话。</td><td>会话列表、消息和引用保持一致。</td></tr>
</table>

<h1>15 数据包验收标准</h1>
<table>
  <tr><th>数据包</th><th>验收标准</th><th>失败处理</th></tr>
  <tr><td><code>minio-originals</code></td><td>papers 7153，专利目录 14006，tables 9581，所有带 tables 的 manifest 已登记。</td><td>重新运行 MinIO seed 收集和 tables backfill。</td></tr>
  <tr><td><code>fastqa-ref</code></td><td>主向量库和 MD 向量库的 <code>chroma.sqlite3</code> 存在。</td><td>重新收集 fastQA reference data。</td></tr>
  <tr><td><code>highthinking-ref</code></td><td><code>vectordb/chroma.sqlite3</code> 存在。</td><td>重新收集 highThinkingQA vectordb。</td></tr>
  <tr><td><code>patentqa-ref</code></td><td>两个专利向量库存在，JSON archive 目录 14006，不含 PDF/PNG/JPG 原文。</td><td>重新打包 patentQA ref。</td></tr>
  <tr><td><code>public-service-ref</code></td><td>轻量 vector_database 存在。</td><td>重新收集 public-service ref。</td></tr>
  <tr><td><code>neo4j-*.dump.zst</code></td><td>seed job 可解压并由目标 Neo4j 版本加载。</td><td>在维护窗口重新导出 dump。</td></tr>
</table>

<h1>16 缺陷记录规则</h1>
<p>测试过程中发现的问题应记录为可复现缺陷。每条缺陷至少包含发生环境、操作步骤、实际结果、期望结果、日志片段、截图或接口响应、影响范围和当前处理状态。涉及密钥、账号、个人信息或内网地址的内容应脱敏。</p>
<table>
  <tr><th>字段</th><th>填写要求</th></tr>
  <tr><td>缺陷编号</td><td>按测试管理工具或项目约定生成。</td></tr>
  <tr><td>严重级别</td><td>阻塞、严重、一般、轻微。</td></tr>
  <tr><td>影响模块</td><td>前端、gateway、public-service、fastQA、highThinkingQA、patentQA、基础组件。</td></tr>
  <tr><td>复现步骤</td><td>写清输入、页面、接口和环境。</td></tr>
  <tr><td>日志证据</td><td>记录容器名、时间和关键错误。</td></tr>
  <tr><td>处理结论</td><td>已修复、暂缓、外部依赖、配置问题或无法复现。</td></tr>
</table>
"""

REQUIREMENT_LIST_SECOND_PASS = """
<h1>需求细化清单</h1>
<table>
  <tr><th>序号</th><th>需求层级</th><th>需求简述</th><th>提出时间</th><th>需求文档</th><th>完成时间</th><th>状态</th><th>备注</th></tr>
  <tr><td class="center">19</td><td>部署能力</td><td>支持 edge nginx 提供 HTTPS 统一入口，并将 HTTP 请求跳转到 HTTPS。</td><td class="center">2026/05/20</td><td>HTTPS 部署要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>证书由 <code>deploy/certs</code> 提供。</td></tr>
  <tr><td class="center">20</td><td>部署能力</td><td>支持内网自签证书和部署方替换证书。</td><td class="center">2026/05/20</td><td>HTTPS 部署要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>域名需与证书 SAN 一致。</td></tr>
  <tr><td class="center">21</td><td>部署能力</td><td>支持本机测试时改用非默认 MySQL、Redis、MinIO 和 HTTPS 端口。</td><td class="center">2026/05/20</td><td>本机部署验证</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>通过 <code>deploy/.env</code> 修改宿主机映射端口。</td></tr>
  <tr><td class="center">22</td><td>数据能力</td><td>MinIO 原文包不绑定 bucket 名，运行时导入到 <code>MINIO_BUCKET</code>。</td><td class="center">2026/05/20</td><td>MinIO seed 方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>bucket 由部署配置决定。</td></tr>
  <tr><td class="center">23</td><td>数据能力</td><td>MinIO seed 支持 marker，避免同版本重复导入。</td><td class="center">2026/05/20</td><td>MinIO seed 方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>marker 位于 <code>_deploy/data-seed</code>。</td></tr>
  <tr><td class="center">24</td><td>数据能力</td><td>Reference data 使用 named volume，与运行态 state volume 分离。</td><td class="center">2026/05/20</td><td>数据包交付方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>避免更新 seed 覆盖用户运行态数据。</td></tr>
  <tr><td class="center">25</td><td>数据能力</td><td>专利 reference data 排除 PDF、PNG、JPG 原文。</td><td class="center">2026/05/20</td><td>数据包交付方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>原文只保存在 MinIO。</td></tr>
  <tr><td class="center">26</td><td>图谱能力</td><td>文献和专利图谱分别由独立 Neo4j 容器承载。</td><td class="center">2026/05/20</td><td>图谱部署方案</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>内部地址固定。</td></tr>
  <tr><td class="center">27</td><td>模型能力</td><td>fastQA 和 patentQA 使用统一 intent 模型配置名称。</td><td class="center">2026/05/20</td><td>模型配置统一</td><td class="center">2026/05/20</td><td class="center">已实现</td><td><code>INTENT_MODEL_*</code>。</td></tr>
  <tr><td class="center">28</td><td>模型能力</td><td>fastQA 和 patentQA 共用 QA embedding 配置。</td><td class="center">2026/05/20</td><td>模型配置统一</td><td class="center">2026/05/20</td><td class="center">已实现</td><td><code>QA_EMBEDDING_*</code>。</td></tr>
  <tr><td class="center">29</td><td>模型能力</td><td>highThinkingQA 使用独立 embedding 配置。</td><td class="center">2026/05/20</td><td>模型配置统一</td><td class="center">2026/05/20</td><td class="center">已实现</td><td><code>HIGHTHINKINGQA_EMBEDDING_*</code>。</td></tr>
  <tr><td class="center">30</td><td>模型能力</td><td>fastQA 和 patentQA 支持统一 rerank 配置和禁用开关。</td><td class="center">2026/05/20</td><td>模型配置统一</td><td class="center">2026/05/20</td><td class="center">已实现</td><td><code>RERANK_PROVIDER</code> 可设置为 <code>none</code>。</td></tr>
  <tr><td class="center">31</td><td>前端能力</td><td>问答模式在前端显示为文献、深度、专利。</td><td class="center">2026/05/20</td><td>前端体验调整</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>统一用户可见名称。</td></tr>
  <tr><td class="center">32</td><td>前端能力</td><td>阶段事件和耗时可在问答过程中展示。</td><td class="center">2026/05/20</td><td>问答过程展示</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>包括 intent、检索、重排、生成等阶段。</td></tr>
  <tr><td class="center">33</td><td>账号能力</td><td>管理员账号初始化后要求首次登录修改密码并设置安全问题。</td><td class="center">2026/05/20</td><td>账号安全要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>文档不记录明文初始密码。</td></tr>
  <tr><td class="center">34</td><td>账号能力</td><td>注册用户必须绑定有效人员记录。</td><td class="center">2026/05/20</td><td>账号安全要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>通过姓名、工号和校验码校验。</td></tr>
  <tr><td class="center">35</td><td>运维能力</td><td>支持数据包 manifest sha256 校验。</td><td class="center">2026/05/20</td><td>运维校验要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>preflight 内置校验。</td></tr>
  <tr><td class="center">36</td><td>运维能力</td><td>支持按服务查看 Docker 日志。</td><td class="center">2026/05/20</td><td>运维排障要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>文档给出常用日志命令。</td></tr>
  <tr><td class="center">37</td><td>运维能力</td><td>支持备份 MySQL、MinIO、配置和证书。</td><td class="center">2026/05/20</td><td>运维备份要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>区分可重建数据和运行态数据。</td></tr>
  <tr><td class="center">38</td><td>开发能力</td><td>Python base 镜像只承载依赖，业务镜像复制各自服务代码。</td><td class="center">2026/05/20</td><td>镜像分层要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>减少后续单服务更新成本。</td></tr>
  <tr><td class="center">39</td><td>开发能力</td><td>新增部署配置项时必须同步 compose、env 模板和文档。</td><td class="center">2026/05/20</td><td>配置治理要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>开发文档已说明规则。</td></tr>
  <tr><td class="center">40</td><td>测试能力</td><td>测试报告覆盖部署、认证、管理、三类问答、文件、图谱、数据包和模型调用。</td><td class="center">2026/05/20</td><td>测试验收要求</td><td class="center">2026/05/20</td><td class="center">已实现</td><td>按用例编号执行。</td></tr>
</table>
"""

DEPLOYMENT_MANUAL_FINAL = """
<h1>1 文档说明</h1>
<p>本文档面向部署实施人员和现场运维人员，用于指导 LiFeO4Agent 在目标服务器上的安装、配置、启动、验证、更新和回滚。本文档只说明部署相关工作，不替代测试报告、开发文档和运维手册。</p>
<table>
  <tr><th>项目</th><th>说明</th></tr>
  <tr><td>系统名称</td><td>LiFeO4Agent</td></tr>
  <tr><td>部署形态</td><td>Docker 离线部署，Docker 镜像包 + <code>tar.zst</code> 数据包 + docker compose 编排。</td></tr>
  <tr><td>适用版本</td><td>文档版本 <code>V1.0</code>，数据包版本 <code>2026-05-19</code>。</td></tr>
  <tr><td>部署目标</td><td>完成系统服务启动、基础数据导入、HTTPS 访问、管理员登录和三类问答冒烟验证。</td></tr>
</table>

<h1>2 部署方案</h1>
<p>系统采用容器化微服务部署。前端、网关、公共服务、文献问答、深度问答、专利问答、MySQL、Redis、MinIO、Neo4j 和 seed job 均由 docker compose 编排。业务服务镜像和大体积数据包分离，避免后续单服务更新时重复分发原文、向量库和图谱数据。</p>
<div class="diagram">
  <div class="diagram-title">图 1 部署方案示意图</div>
  <pre class="mermaid">flowchart LR
  U[客户端浏览器] -- HTTPS -- E[edge nginx]
  E --> F[frontend nginx]
  F --> G[gateway]
  G --> P[public-service]
  G --> Q1[fastQA 文献问答]
  G --> Q2[highThinkingQA 深度问答]
  G --> Q3[patentQA 专利问答]
  P --> M[(MySQL)]
  P --> R[(Redis)]
  P --> O[(MinIO)]
  Q1 --> V1[(fastqa_ref_data)]
  Q1 --> N1[(Neo4j literature)]
  Q2 --> V2[(highthinking_ref_data)]
  Q3 --> V3[(patentqa_ref_data)]
  Q3 --> N2[(Neo4j patent)]
  Q1 --> LLM[模型服务]
  Q2 --> LLM
  Q3 --> LLM
  S[seed-tools one-shot jobs] --> O
  S --> V1
  S --> V2
  S --> V3
  S --> N1
  S --> N2</pre>
</div>
<p>当前交付为单机 compose 部署形态。若部署方需要高可用，可在后续方案中将 MySQL、Redis、MinIO 和 Neo4j 替换为部署方统一中间件集群，业务服务可通过外部负载均衡扩展为多实例；本次 V1.0 交付不默认启用高可用集群。</p>

<h1>3 运行环境要求</h1>
<h2>3.1 硬件要求</h2>
<table>
  <tr><th>资源</th><th>最低配置</th><th>推荐配置</th><th>说明</th></tr>
  <tr><td>CPU</td><td>16 核</td><td>32 核及以上</td><td>问答后端、Neo4j 和数据导入会消耗 CPU。</td></tr>
  <tr><td>内存</td><td>64 GB</td><td>128 GB 及以上</td><td>专利服务、向量库和图谱查询建议预留充足内存。</td></tr>
  <tr><td>磁盘</td><td>300 GB 可用空间</td><td>500 GB 及以上 SSD</td><td>需容纳镜像、数据包、MinIO 导入后对象、Neo4j 数据和日志。</td></tr>
  <tr><td>网络</td><td>内网可达</td><td>千兆内网</td><td>客户端、模型服务和部署机之间应保持稳定连接。</td></tr>
</table>

<h2>3.2 软件要求</h2>
<table>
  <tr><th>软件</th><th>版本要求</th><th>用途</th></tr>
  <tr><td>Linux</td><td>主流 64 位 Linux 发行版</td><td>部署宿主机操作系统。</td></tr>
  <tr><td>Docker Engine</td><td>建议 24.x 或以上</td><td>运行容器。</td></tr>
  <tr><td>Docker Compose</td><td>Compose v2</td><td>执行 <code>docker compose</code> 编排。</td></tr>
  <tr><td>浏览器</td><td>Chrome、Edge 或国产兼容浏览器</td><td>访问前端页面。</td></tr>
</table>
<p>宿主机不需要安装 <code>mc</code>、<code>zstd</code>、<code>neo4j-admin</code>；这些工具由 seed-tools 镜像或官方 Neo4j 镜像提供。</p>

<h1>4 交付物清单</h1>
<table>
  <tr><th>交付物</th><th>说明</th><th>部署位置</th></tr>
  <tr><td><code>deploy/docker-compose.yml</code></td><td>容器编排文件。</td><td>部署目录。</td></tr>
  <tr><td><code>deploy/.env.production.example</code></td><td>生产配置模板。</td><td>复制为 <code>deploy/.env</code>。</td></tr>
  <tr><td><code>deploy/lifeo4agent-images.tar</code></td><td>离线镜像包。</td><td>通过 <code>docker load</code> 导入。</td></tr>
  <tr><td><code>deploy/data/manifest.json</code></td><td>数据包清单、版本和 sha256。</td><td>部署目录。</td></tr>
  <tr><td><code>deploy/data/*.tar.zst</code></td><td>MinIO 原文和 reference data。</td><td>部署目录。</td></tr>
  <tr><td><code>deploy/data/neo4j-*.dump.zst</code></td><td>文献和专利图谱 dump。</td><td>部署目录。</td></tr>
  <tr><td><code>deploy/certs/fullchain.pem</code></td><td>HTTPS 证书链。</td><td>部署目录。</td></tr>
  <tr><td><code>deploy/certs/privkey.pem</code></td><td>HTTPS 私钥。</td><td>部署目录，需限制权限。</td></tr>
</table>

<h1>5 镜像拉取和镜像重载</h1>
<h2>5.1 离线镜像加载</h2>
<p>离线部署时，部署方将镜像 tar 包放到部署机后执行加载命令。</p>
<pre>docker load -i deploy/lifeo4agent-images.tar</pre>
<p>成功输出参考：</p>
<pre>Loaded image: lifeo4agent/gateway:latest
Loaded image: lifeo4agent/public-service:latest
Loaded image: lifeo4agent/fastqa:latest
Loaded image: lifeo4agent/highthinkingqa:latest
Loaded image: lifeo4agent/patent:latest
Loaded image: lifeo4agent/frontend:latest
Loaded image: lifeo4agent/seed-tools:latest</pre>
<p>失败输出参考：</p>
<pre>open deploy/lifeo4agent-images.tar: no such file or directory</pre>
<p>处理方式：确认镜像包路径是否正确，确认文件传输完整。</p>

<h2>5.2 在线镜像拉取</h2>
<p>如部署方使用私有镜像仓库，可按镜像仓库规范登录并拉取。当前离线交付不要求使用在线拉取。</p>
<pre>docker login &lt;镜像仓库地址&gt;
docker pull lifeo4agent/gateway:latest</pre>
<p>成功输出参考：</p>
<pre>Login Succeeded
latest: Pulling from lifeo4agent/gateway
Status: Downloaded newer image for lifeo4agent/gateway:latest</pre>
<p>失败输出参考：</p>
<pre>Error response from daemon: unauthorized: authentication required</pre>
<p>处理方式：检查仓库地址、用户名、密码、网络连通性和镜像 tag。</p>

<h1>6 配置文件准备</h1>
<h2>6.1 生成实际配置</h2>
<pre>cp deploy/.env.production.example deploy/.env</pre>
<p>成功输出参考：命令无输出，且 <code>deploy/.env</code> 文件存在。</p>
<p>失败输出参考：</p>
<pre>cp: cannot stat 'deploy/.env.production.example': No such file or directory</pre>
<p>处理方式：确认部署目录完整。</p>

<h2>6.2 必填配置项</h2>
<table>
  <tr><th>配置类别</th><th>变量</th><th>说明</th></tr>
  <tr><td>访问入口</td><td><code>HTTP_PUBLISH_PORT</code>、<code>HTTPS_PUBLISH_PORT</code>、<code>HTTPS_SERVER_NAME</code>、<code>HTTPS_REDIRECT_HOST</code></td><td>HTTP/HTTPS 端口和域名。</td></tr>
  <tr><td>基础组件</td><td><code>MYSQL_ROOT_PASSWORD</code>、<code>MYSQL_APP_PASSWORD</code>、<code>REDIS_PASSWORD</code>、<code>MINIO_ROOT_PASSWORD</code></td><td>数据库、缓存、对象存储密码。</td></tr>
  <tr><td>业务鉴权</td><td><code>JWT_SECRET</code>、<code>PUBLIC_SERVICE_INTERNAL_AUTH_TOKEN</code></td><td>用户 token 和内部服务鉴权。</td></tr>
  <tr><td>数据包</td><td><code>DATA_PACKAGE_VERSION</code>、<code>DATA_SEED_FORCE</code></td><td>版本应与 manifest 一致；强制重导默认为 0。</td></tr>
  <tr><td>大模型</td><td><code>LLM_BASE_URL</code>、<code>LLM_MODEL</code>、<code>LLM_API_KEY</code></td><td>OpenAI 兼容接口或部署方模型网关。</td></tr>
  <tr><td>意图模型</td><td><code>INTENT_MODEL_ENABLED</code>、<code>INTENT_MODEL_BASE_URL</code>、<code>INTENT_MODEL</code>、<code>INTENT_MODEL_API_KEY</code></td><td>fastQA 和 patentQA 共享。</td></tr>
  <tr><td>Embedding</td><td><code>QA_EMBEDDING_*</code>、<code>HIGHTHINKINGQA_EMBEDDING_*</code></td><td>文献/专利与深度问答分开配置。</td></tr>
  <tr><td>Rerank</td><td><code>RERANK_PROVIDER</code>、<code>RERANK_BASE_URL</code>、<code>RERANK_MODEL</code>、<code>RERANK_API_KEY</code></td><td>不用时 provider 设置为 <code>none</code>。</td></tr>
</table>

<h2>6.3 大模型参数说明</h2>
<table>
  <tr><th>参数</th><th>当前配置方式</th><th>说明</th></tr>
  <tr><td>API Key</td><td><code>LLM_API_KEY</code></td><td>真实密钥只填写在 <code>deploy/.env</code>，不得写入文档。</td></tr>
  <tr><td>Base URL</td><td><code>LLM_BASE_URL</code></td><td>应为 OpenAI 兼容 chat completions 入口所在的 base url。</td></tr>
  <tr><td>模型名称</td><td><code>LLM_MODEL</code></td><td>由部署方模型服务提供。</td></tr>
  <tr><td>超时</td><td><code>LLM_CONNECT_TIMEOUT_SECONDS</code>、<code>LLM_READ_TIMEOUT_SECONDS</code>、<code>LLM_STREAM_READ_TIMEOUT_SECONDS</code></td><td>共享配置中默认连接 15 秒、读取 180 秒、流式读取 600 秒。</td></tr>
  <tr><td>并发连接</td><td><code>LLM_MAX_CONNECTIONS</code>、<code>LLM_MAX_KEEPALIVE_CONNECTIONS</code></td><td>共享配置默认最大连接 160、保活连接 64。</td></tr>
  <tr><td>温度和最大 token</td><td>按服务内部默认值控制</td><td>文件问答等局部能力使用内部默认值，例如 top_p 0.95、max_tokens 2500 左右。</td></tr>
</table>

<h1>7 数据包放置和预检</h1>
<p>数据包必须放在 <code>deploy/data</code> 下。当前 manifest 记录的数据版本为 <code>2026-05-19</code>。</p>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env</pre>
<p>成功输出参考：</p>
<pre>ok: data package manifest and sha256 validated with python
ok: docker image present: lifeo4agent/gateway:latest
preflight check passed</pre>
<p>失败输出参考：</p>
<pre>missing required data package: deploy/data/minio-originals.tar.zst</pre>
<p>处理方式：补齐数据包，或检查 <code>DEPLOY_DATA_DIR</code> 是否指向正确目录。</p>

<h1>8 上线启动与访问</h1>
<h2>8.1 启动命令</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d</pre>
<p>成功输出参考：</p>
<pre>Container lifeo4agent-mysql        Healthy
Container lifeo4agent-redis        Healthy
Container lifeo4agent-minio        Started
Container lifeo4agent-minio-seed   Exited
Container lifeo4agent-gateway      Started
Container lifeo4agent-edge         Started</pre>
<p>失败输出参考：</p>
<pre>Error response from daemon: driver failed programming external connectivity on endpoint lifeo4agent-edge: Bind for 0.0.0.0:443 failed: port is already allocated</pre>
<p>处理方式：修改 <code>HTTPS_PUBLISH_PORT</code> 或释放宿主机 443 端口。</p>

<h2>8.2 健康检查</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</pre>
<p>成功输出参考：</p>
<pre>NAME                              STATUS
lifeo4agent-mysql                 Up (healthy)
lifeo4agent-redis                 Up (healthy)
lifeo4agent-gateway               Up
lifeo4agent-edge                  Up
lifeo4agent-minio-seed            Exited (0)</pre>
<p>失败输出参考：</p>
<pre>lifeo4agent-neo4j-patent          Restarting</pre>
<p>处理方式：查看对应服务日志，优先检查数据卷、密码和 seed job。</p>

<h2>8.3 访问验证</h2>
<pre>curl -k -I https://&lt;部署域名&gt;:&lt;HTTPS端口&gt;/</pre>
<p>成功输出参考：</p>
<pre>HTTP/2 200
server: nginx</pre>
<p>失败输出参考：</p>
<pre>curl: (7) Failed to connect to &lt;部署域名&gt; port &lt;HTTPS端口&gt;</pre>
<p>处理方式：检查域名解析、服务器防火墙、端口映射和 edge 容器状态。</p>

<h1>9 初始账号</h1>
<p>部署脚本会在空数据库初始化时创建 bootstrap 管理员账号。管理员用户名为 <code>admin</code>，初始密码由交付渠道单独确认，不在本文档记录。首次登录后应立即修改密码并设置安全问题。</p>

<h1>10 更新部署方案</h1>
<h2>10.1 单服务镜像更新</h2>
<p>如果只修改 fastQA，则只需要导入 fastQA 新镜像并重启该服务。</p>
<pre>docker load -i lifeo4agent-fastqa-update.tar
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d fastqa</pre>
<p>成功输出参考：</p>
<pre>Loaded image: lifeo4agent/fastqa:20260520
Container lifeo4agent-fastqa Started</pre>
<p>失败输出参考：</p>
<pre>No such service: fastqa</pre>
<p>处理方式：确认 compose 文件版本和服务名是否一致。</p>

<h2>10.2 数据包更新</h2>
<p>更新原文、向量库或图谱时，需要替换 <code>deploy/data</code> 中的数据包和 manifest，并同步修改 <code>DATA_PACKAGE_VERSION</code>。同版本 marker 存在时会跳过导入；需要重导时设置 <code>DATA_SEED_FORCE=1</code>，完成后改回 <code>0</code>。</p>

<h2>10.3 回滚策略</h2>
<ol>
  <li>镜像回滚：保留上一版本镜像 tar 或 tag，重新 <code>docker load</code> 后启动对应服务。</li>
  <li>配置回滚：恢复备份的 <code>deploy/.env</code>，执行预检后重启受影响服务。</li>
  <li>数据回滚：恢复旧版本数据包和 manifest，设置旧版本号，并按需强制重导。</li>
  <li>数据库回滚：使用上线前 MySQL 备份恢复，恢复前应停止写入。</li>
</ol>

<h1>11 部署常见问题</h1>
<table>
  <tr><th>问题</th><th>典型日志或现象</th><th>解决方法</th></tr>
  <tr><td>端口冲突</td><td><code>port is already allocated</code></td><td>修改 <code>deploy/.env</code> 中对应发布端口。</td></tr>
  <tr><td>数据库连接失败</td><td><code>Access denied for user</code> 或服务健康检查失败。</td><td>检查 MySQL 密码、数据库初始化和 compose 环境变量。</td></tr>
  <tr><td>MinIO 导入失败</td><td><code>package not found</code>、<code>AccessDenied</code></td><td>检查数据包路径、MinIO 账号密码和 bucket 初始化。</td></tr>
  <tr><td>向量库不存在</td><td>后端日志出现 <code>chroma.sqlite3</code> 路径错误。</td><td>检查对应 <code>*-ref-seed</code> 是否 Exited (0)。</td></tr>
  <tr><td>模型 400 错误</td><td>模型接口返回参数不兼容。</td><td>检查模型是否支持 OpenAI 兼容格式、stream、thinking 参数。</td></tr>
  <tr><td>HTTPS 证书错误</td><td>浏览器提示证书不受信或域名不匹配。</td><td>确认证书 SAN、域名解析和客户端信任链。</td></tr>
</table>
"""

TEST_REPORT_FINAL = """
<h1>1 项目介绍</h1>
<p>LiFeO4Agent 是面向电池材料研发场景的智能问答系统，提供文献问答、深度思考问答、专利问答、文件问答、原文查看、用户管理、部门人员管理和配额管理。本报告用于记录 V1.0 交付版本的测试范围、测试环境、功能测试、性能测试、安全测试和发布结论。</p>
<table>
  <tr><th>测试对象</th><th>测试范围</th><th>测试目标</th></tr>
  <tr><td>前端与网关</td><td>登录、路由、问答入口、SSE 展示、文件上传。</td><td>验证用户可完成核心操作。</td></tr>
  <tr><td>公共服务</td><td>用户、部门、人员、配额、会话、文件元数据。</td><td>验证基础业务数据一致。</td></tr>
  <tr><td>QA 后端</td><td>文献、深度、专利三类问答。</td><td>验证检索、重排、生成、引用和原文入口。</td></tr>
  <tr><td>基础组件</td><td>MySQL、Redis、MinIO、Neo4j、seed job。</td><td>验证数据可导入、服务可启动、健康检查可通过。</td></tr>
  <tr><td>非功能</td><td>部署、性能、安全、稳定性。</td><td>验证达到发布准入要求。</td></tr>
</table>

<h1>2 测试环境</h1>
<h2>2.1 硬件环境</h2>
<table>
  <tr><th>项目</th><th>测试记录</th><th>说明</th></tr>
  <tr><td>服务器型号</td><td>目标部署服务器或等效测试服务器</td><td>正式验收时填写实际型号。</td></tr>
  <tr><td>CPU</td><td>建议 16 核以上</td><td>记录实际核数和型号。</td></tr>
  <tr><td>内存</td><td>建议 64 GB 以上</td><td>记录实际内存容量。</td></tr>
  <tr><td>磁盘</td><td>建议 300 GB 以上可用空间</td><td>记录磁盘类型、容量和 Docker 数据目录。</td></tr>
</table>

<h2>2.2 网络环境</h2>
<table>
  <tr><th>项目</th><th>要求</th><th>验证方式</th></tr>
  <tr><td>访问网络</td><td>客户端可访问部署机 HTTPS 端口。</td><td>浏览器访问和 <code>curl -k -I</code>。</td></tr>
  <tr><td>模型网络</td><td>容器可访问 LLM、intent、embedding、rerank 服务。</td><td>问答请求和后端日志。</td></tr>
  <tr><td>内网解析</td><td>部署域名解析到部署机 IP。</td><td><code>ping</code>、<code>nslookup</code> 或 hosts 检查。</td></tr>
</table>

<h2>2.3 软件环境</h2>
<table>
  <tr><th>软件</th><th>版本或配置</th><th>用途</th></tr>
  <tr><td>Docker</td><td>Docker Engine + Compose v2</td><td>容器运行和编排。</td></tr>
  <tr><td>MySQL</td><td>镜像 <code>mysql:8.0</code></td><td>用户态业务库。</td></tr>
  <tr><td>Redis</td><td>镜像 <code>redis:7</code></td><td>缓存和运行状态。</td></tr>
  <tr><td>MinIO</td><td>官方镜像</td><td>论文、专利原文和文件对象。</td></tr>
  <tr><td>Neo4j</td><td>镜像 <code>neo4j:5.26.12</code></td><td>文献和专利知识图谱。</td></tr>
  <tr><td>前端</td><td><code>lifeo4agent/frontend</code></td><td>Vue 3 + nginx。</td></tr>
  <tr><td>后端</td><td>gateway、public-service、fastQA、highThinkingQA、patentQA</td><td>FastAPI 服务。</td></tr>
</table>

<h2>2.4 被测服务信息</h2>
<table>
  <tr><th>服务</th><th>容器内地址</th><th>对外入口</th><th>版本标识</th></tr>
  <tr><td>edge</td><td><code>edge:443</code></td><td><code>https://部署域名</code></td><td>V1.0</td></tr>
  <tr><td>gateway</td><td><code>gateway:8101</code></td><td>经前端 nginx 代理</td><td>V1.0</td></tr>
  <tr><td>public-service</td><td><code>public-service:8102</code></td><td>经 gateway 代理</td><td>V1.0</td></tr>
  <tr><td>fastQA</td><td><code>fastqa:8008</code></td><td>经 gateway 代理</td><td>V1.0</td></tr>
  <tr><td>highThinkingQA</td><td><code>highthinkingqa:8009</code></td><td>经 gateway 代理</td><td>V1.0</td></tr>
  <tr><td>patentQA</td><td><code>patent:8010</code></td><td>经 gateway 代理</td><td>V1.0</td></tr>
</table>

<h1>3 功能测试</h1>
<table>
  <tr><th>编号</th><th>模块</th><th>测试项</th><th>预期结果</th><th>状态</th></tr>
  <tr><td>FT-001</td><td>认证</td><td>管理员登录</td><td>进入管理后台，提示首次安全设置。</td><td>通过标准：目标环境执行无阻塞。</td></tr>
  <tr><td>FT-002</td><td>认证</td><td>普通用户注册</td><td>人员记录校验通过后创建账号。</td><td>通过标准：返回成功并可登录。</td></tr>
  <tr><td>FT-003</td><td>用户中心</td><td>修改密码和设置安全问题</td><td>密码更新后旧密码不可登录。</td><td>通过标准：安全信息持久化。</td></tr>
  <tr><td>FT-004</td><td>管理后台</td><td>部门树查看</td><td>显示电池材料技术研究中心及下属部门。</td><td>通过标准：三级部门完整。</td></tr>
  <tr><td>FT-005</td><td>管理后台</td><td>人员记录维护</td><td>新增、编辑、停用、批量导入可用。</td><td>通过标准：状态影响注册。</td></tr>
  <tr><td>FT-006</td><td>配额</td><td>普通问答、文件问答、查看原文配额</td><td>配额不足时拦截并给出提示。</td><td>通过标准：扣减和重置正确。</td></tr>
  <tr><td>FT-007</td><td>文献问答</td><td>提交文献问题</td><td>返回答案、引用、阶段和耗时。</td><td>通过标准：引用可打开原文。</td></tr>
  <tr><td>FT-008</td><td>深度问答</td><td>提交综合分析问题</td><td>分阶段返回深度回答。</td><td>通过标准：SSE 不断流。</td></tr>
  <tr><td>FT-009</td><td>专利问答</td><td>提交专利问题</td><td>返回专利引用、tables 或原文入口。</td><td>通过标准：专利对象可读取。</td></tr>
  <tr><td>FT-010</td><td>文件问答</td><td>上传 PDF、Excel、CSV 并提问</td><td>文件参与本轮问答。</td><td>通过标准：上传、列表、下载、删除均可用。</td></tr>
</table>

<h1>4 数据包和部署测试</h1>
<table>
  <tr><th>编号</th><th>测试项</th><th>期望结果</th><th>关键指标</th></tr>
  <tr><td>DT-001</td><td>数据包 manifest 校验</td><td>sha256 校验通过。</td><td>所有必需包存在。</td></tr>
  <tr><td>DT-002</td><td>MinIO 原文导入</td><td>papers、patent/originals 导入成功。</td><td>papers 7153，专利目录 14006，tables 9581。</td></tr>
  <tr><td>DT-003</td><td>fastQA reference 导入</td><td>向量库进入 <code>fastqa_ref_data</code>。</td><td>Chroma SQLite 2 个。</td></tr>
  <tr><td>DT-004</td><td>highThinking reference 导入</td><td>vectordb 进入 <code>highthinking_ref_data</code>。</td><td>Chroma SQLite 1 个。</td></tr>
  <tr><td>DT-005</td><td>patentQA reference 导入</td><td>JSON-only archive 和专利向量库导入。</td><td>专利 JSON 目录 14006。</td></tr>
  <tr><td>DT-006</td><td>Neo4j dump 导入</td><td>文献和专利 Neo4j 均 healthy。</td><td>seed job 退出码 0。</td></tr>
  <tr><td>DT-007</td><td>同版本重启</td><td>seed job 识别 marker 并跳过。</td><td>无重复长时间导入。</td></tr>
</table>

<h1>5 性能测试</h1>
<p>性能测试用于验证系统在目标硬件和目标模型服务能力下的响应表现。由于 LLM、embedding 和 rerank 延迟受外部模型平台影响，报告应同时记录模型服务状态。</p>
<table>
  <tr><th>场景</th><th>目的</th><th>建议指标</th><th>完成情况记录</th></tr>
  <tr><td>登录接口</td><td>验证认证链路基础性能。</td><td>平均响应时间小于 1 秒，错误率 0。</td><td>目标环境执行后填写。</td></tr>
  <tr><td>文献问答</td><td>验证检索和生成链路。</td><td>首包时间和总耗时满足业务可接受范围。</td><td>记录首 token、总耗时、引用数量。</td></tr>
  <tr><td>深度问答</td><td>验证长流程稳定性。</td><td>SSE 持续输出，无 5xx。</td><td>记录阶段耗时。</td></tr>
  <tr><td>专利问答</td><td>验证专利检索、图谱和原文。</td><td>错误率 0，原文入口可用。</td><td>记录检索、rerank、图谱耗时。</td></tr>
  <tr><td>原文查看</td><td>验证 MinIO 下载能力。</td><td>PDF 可打开，无 404。</td><td>记录下载耗时。</td></tr>
</table>
<p>若部署方有明确并发要求，例如 500 并发用户、平均响应时间小于 2 秒，应在目标模型服务和目标硬件上补充压测，并将 TPS、P95、P99、错误率、CPU、内存、磁盘 I/O 写入本节。</p>

<h1>6 安全测试</h1>
<table>
  <tr><th>编号</th><th>测试项</th><th>预期结果</th></tr>
  <tr><td>ST-001</td><td>未登录访问首页</td><td>跳转登录页。</td></tr>
  <tr><td>ST-002</td><td>普通用户访问管理后台</td><td>拒绝访问或跳转首页。</td></tr>
  <tr><td>ST-003</td><td>停用用户登录</td><td>登录失败并提示账号状态异常。</td></tr>
  <tr><td>ST-004</td><td>错误密码多次登录</td><td>触发失败计数或锁定策略。</td></tr>
  <tr><td>ST-005</td><td>HTTPS 访问</td><td>传输使用 TLS。</td></tr>
  <tr><td>ST-006</td><td>交付文档和镜像上下文检查</td><td>不包含真实 API Key、密码和 token。</td></tr>
</table>

<h1>7 缺陷统计</h1>
<table>
  <tr><th>严重级别</th><th>数量</th><th>状态说明</th></tr>
  <tr><td>Blocker</td><td>0</td><td>发布前不得存在阻塞缺陷。</td></tr>
  <tr><td>Critical</td><td>0</td><td>发布前应全部关闭。</td></tr>
  <tr><td>Major</td><td>目标环境执行后填写</td><td>可按验收标准决定是否遗留。</td></tr>
  <tr><td>Minor</td><td>目标环境执行后填写</td><td>记录不影响发布的体验问题。</td></tr>
</table>

<h1>8 测试结论</h1>
<p>V1.0 交付版本的测试结论应以目标环境最终执行结果为准。发布准入建议如下：部署预检、数据包校验、容器健康检查、管理员登录、普通用户注册、文献问答、深度问答、专利问答、原文查看、文件问答均通过时，结论为“通过”；如存在 seed 失败、基础组件无法启动、核心问答不可用或安全阻断缺陷，结论为“不通过”。</p>
<p>当前文档已将功能、部署、性能和安全测试项展开为可执行清单。正式提交测试报告时，应补充目标环境截图、性能曲线和实际测试结果。</p>
"""

DEVELOPMENT_DOC_FINAL = """
<h1>1 设计维护记录</h1>
<table>
  <tr><th>版本</th><th>日期</th><th>作者</th><th>修订摘要</th></tr>
  <tr><td>V1.0</td><td>2026/05/20</td><td>项目组</td><td>形成 LiFeO4Agent 开发文档初版，覆盖架构、模块、接口、数据库、开发环境和发布规则。</td></tr>
</table>

<h1>2 文档引言</h1>
<h2>2.1 目的</h2>
<p>本文档面向开发人员、测试人员和维护人员，说明 LiFeO4Agent 的工程结构、核心模块、数据库设计、接口设计、开发环境、编码规范、数据包构建和常见问题。部署人员应主要阅读部署手册和运维手册。</p>
<h2>2.2 背景</h2>
<p>系统用于支撑电池材料研发过程中的文献检索、深度分析、专利检索和原文核对。项目从单体和本地资源依赖逐步演进为前端、网关、公共服务和多个 QA 后端组成的容器化系统，以便离线交付、增量升级和运维管理。</p>
<h2>2.3 术语</h2>
<table>
  <tr><th>术语</th><th>说明</th></tr>
  <tr><td>fastQA</td><td>文献快速问答后端。</td></tr>
  <tr><td>highThinkingQA</td><td>深度思考问答后端，负责多阶段分析。</td></tr>
  <tr><td>patentQA</td><td>专利问答后端，负责专利检索、tables 和图谱增强。</td></tr>
  <tr><td>public-service</td><td>公共能力服务，负责用户、部门、人员、配额、会话和文件。</td></tr>
  <tr><td>reference data</td><td>向量库、索引、JSON archive 等可由数据包重建的数据。</td></tr>
  <tr><td>seed job</td><td>compose 启动时执行的一次性数据导入容器。</td></tr>
</table>

<h1>3 需求说明</h1>
<table>
  <tr><th>需求编号</th><th>业务需求</th><th>实现模块</th></tr>
  <tr><td>REQ-001</td><td>用户可使用文献、深度、专利三种问答模式。</td><td>frontend、gateway、fastQA、highThinkingQA、patentQA。</td></tr>
  <tr><td>REQ-002</td><td>用户可上传 PDF、Excel、CSV 并参与问答。</td><td>frontend、gateway、public-service、QA 后端。</td></tr>
  <tr><td>REQ-003</td><td>管理员可维护用户、部门、人员和配额。</td><td>frontend admin、public-service。</td></tr>
  <tr><td>REQ-004</td><td>论文和专利原文统一存储在 MinIO。</td><td>seed-tools、public-service、fastQA、highThinkingQA、patentQA。</td></tr>
  <tr><td>REQ-005</td><td>系统可离线部署和增量更新。</td><td>deploy、Dockerfile、compose、package scripts。</td></tr>
</table>

<h1>4 系统设计</h1>
<h2>4.1 总体架构</h2>
<div class="diagram">
  <div class="diagram-title">图 1 开发视角总体架构</div>
  <pre class="mermaid">flowchart TB
  FE[frontend-vue<br/>Vue 3 + Vite] --> GW[gateway/app<br/>路由、SSE、配额、文件上下文]
  GW --> PS[public-service/backend/app]
  GW --> FQ[fastQA/app]
  GW --> HT[highThinkingQA]
  GW --> PT[patent/server/patent]
  PS --> PS1[auth / admin_users / departments / personnel]
  PS --> PS2[quota / conversation / documents / uploads / system]
  FQ --> FQ1[generation_pipeline / graph_kb]
  FQ --> FQ2[qa_pdf / qa_tabular / documents / storage]
  HT --> HT1[server_fastapi / agent_core / ingest]
  PT --> PT1[intent / retrieval / graph_kb / tabular / answering]</pre>
</div>

<h2>4.2 仓库目录</h2>
<table>
  <tr><th>目录</th><th>职责</th><th>维护规则</th></tr>
  <tr><td><code>frontend-vue</code></td><td>Vue 3 + Vite 前端。</td><td>前端体验和 API 调用封装在此维护。</td></tr>
  <tr><td><code>gateway</code></td><td>FastAPI 网关。</td><td>统一路由、SSE 代理、文件上下文、配额 precheck/finalize。</td></tr>
  <tr><td><code>public-service</code></td><td>公共能力后端。</td><td>用户、部门、人员、配额、会话、文件、原文代理。</td></tr>
  <tr><td><code>fastQA</code></td><td>文献问答后端。</td><td>文献检索、rerank、图谱和生成。</td></tr>
  <tr><td><code>highThinkingQA</code></td><td>深度问答后端。</td><td>规划、分解、检索、综合生成。</td></tr>
  <tr><td><code>patent</code></td><td>专利问答后端。</td><td>专利检索、tables、图谱和回答生成。</td></tr>
  <tr><td><code>resource</code></td><td>共享资源、配置和本地数据源。</td><td>数据包构建从这里取原始资源。</td></tr>
  <tr><td><code>deploy</code></td><td>部署编排、seed 脚本、MySQL 初始化。</td><td>客户配置面变化必须同步。</td></tr>
</table>

<h2>4.3 模块设计</h2>
<table>
  <tr><th>模块</th><th>输入</th><th>输出</th><th>核心函数或类</th></tr>
  <tr><td>gateway QA router</td><td>用户问题、模式、文件选择、token。</td><td>同步回答或 SSE 事件。</td><td><code>gateway/app/routers/qa.py</code>。</td></tr>
  <tr><td>file context resolver</td><td>会话文件列表和用户选择。</td><td>路由决策和文件上下文。</td><td><code>gateway/app/services/file_context_resolver.py</code>。</td></tr>
  <tr><td>quota service</td><td>用户 ID、配额类型。</td><td>是否允许、剩余额度、grant id。</td><td><code>public-service/backend/app/modules/quota/service.py</code>。</td></tr>
  <tr><td>auth service</td><td>用户名、密码、人员信息。</td><td>token、用户资料、注册结果。</td><td><code>public-service/backend/app/modules/auth</code>。</td></tr>
  <tr><td>fastQA generation pipeline</td><td>问题、检索配置、模型配置。</td><td>阶段事件、引用、答案。</td><td><code>fastQA/app/modules/generation_pipeline</code>。</td></tr>
  <tr><td>highThinking agent core</td><td>问题、模式 profile、向量库。</td><td>直接回答、分解、子答案、综合答案。</td><td><code>highThinkingQA/agent_core</code>。</td></tr>
  <tr><td>patent retrieval service</td><td>专利问题、intent、向量库。</td><td>专利候选、段落、tables、图谱补充。</td><td><code>patent/server/patent/retrieval_service.py</code>。</td></tr>
</table>

<h1>5 数据库设计</h1>
<p>数据库为 MySQL <code>agentcode</code>，当前部署初始化只导入 schema、真实部门树和 bootstrap 管理员，不导入研发环境用户数据。</p>
<table>
  <tr><th>表</th><th>关键字段</th><th>说明</th></tr>
  <tr><td><code>users</code></td><td><code>id</code>、<code>username</code>、<code>password_hash</code>、<code>role</code>、<code>user_type</code>、<code>status</code>、<code>created_at</code>、<code>updated_at</code></td><td>用户账号和权限。</td></tr>
  <tr><td><code>personnel_records</code></td><td><code>employee_no</code>、<code>full_name</code>、<code>verification_code_hash</code>、部门 ID、<code>status</code></td><td>注册和绑定人员。</td></tr>
  <tr><td><code>primary_departments</code>、<code>secondary_departments</code>、<code>tertiary_departments</code></td><td><code>id</code>、<code>name</code>、<code>status</code></td><td>三级部门树。</td></tr>
  <tr><td><code>quota_configs</code></td><td><code>quota_type</code>、<code>period</code>、<code>default_limit</code>、<code>is_active</code></td><td>配额配置。</td></tr>
  <tr><td><code>user_quota_usage</code></td><td><code>user_id</code>、<code>quota_type</code>、<code>period_key</code>、<code>used_count</code></td><td>用户配额用量。</td></tr>
  <tr><td><code>conversations</code>、<code>conversation_messages</code>、<code>conversation_files</code></td><td>会话、消息、文件元数据字段。</td><td>会话历史和文件关联。</td></tr>
</table>
<p>表结构中普遍包含 <code>created_at</code> 和 <code>updated_at</code>，用于增量同步和审计。当前表没有统一 <code>is_deleted</code> 字段，用户、部门和人员通过 <code>status</code> 做业务停用；后续若新增强删除类业务表，应优先采用逻辑删除。</p>

<h1>6 接口设计</h1>
<table>
  <tr><th>接口</th><th>方法</th><th>职责</th><th>提供方</th></tr>
  <tr><td><code>/api/auth/login</code></td><td>POST</td><td>用户登录。</td><td>public-service。</td></tr>
  <tr><td><code>/api/auth/register</code></td><td>POST</td><td>用户注册。</td><td>public-service。</td></tr>
  <tr><td><code>/api/auth/me</code></td><td>GET</td><td>获取当前用户。</td><td>public-service。</td></tr>
  <tr><td><code>/api/admin/users</code></td><td>GET/POST</td><td>用户管理。</td><td>public-service。</td></tr>
  <tr><td><code>/api/admin/departments/tree</code></td><td>GET</td><td>部门树。</td><td>public-service。</td></tr>
  <tr><td><code>/api/admin/personnel</code></td><td>GET/POST/PUT</td><td>人员管理。</td><td>public-service。</td></tr>
  <tr><td><code>/api/quota/configs</code></td><td>GET/POST/PUT</td><td>配额管理。</td><td>public-service。</td></tr>
  <tr><td><code>/api/fast/ask_stream</code></td><td>POST</td><td>文献流式问答。</td><td>gateway -> fastQA。</td></tr>
  <tr><td><code>/api/thinking/ask_stream</code></td><td>POST</td><td>深度流式问答。</td><td>gateway -> highThinkingQA。</td></tr>
  <tr><td><code>/api/patent/ask_stream</code></td><td>POST</td><td>专利流式问答。</td><td>gateway -> patentQA。</td></tr>
  <tr><td><code>/api/view_pdf/{doi}</code></td><td>GET/HEAD</td><td>查看论文 PDF。</td><td>public-service 或 QA 后端。</td></tr>
  <tr><td><code>/api/patent/original/{id}</code></td><td>GET/HEAD</td><td>查看专利原文。</td><td>public-service。</td></tr>
</table>

<h1>7 开发实现</h1>
<h2>7.1 开发环境</h2>
<table>
  <tr><th>类别</th><th>建议</th></tr>
  <tr><td>Python</td><td>使用项目现有虚拟环境或 conda 环境，保持依赖与各服务 requirements 一致。</td></tr>
  <tr><td>Node</td><td>使用前端项目兼容的 Node 版本，执行 <code>npm install</code> 后开发。</td></tr>
  <tr><td>IDE</td><td>建议开启 Python、Vue、ESLint 或等效检查。</td></tr>
  <tr><td>数据库</td><td>本地开发可连接用户态 MySQL，部署测试使用 Docker MySQL。</td></tr>
</table>

<h2>7.2 核心问答伪代码</h2>
<pre>def ask(question, mode, selected_files, user):
    check_auth(user)
    route = resolve_route(mode, selected_files)
    grant = quota_precheck(user.id, route.quota_type)
    try:
        context = build_file_context(selected_files)
        for event in route.backend.ask_stream(question, context):
            yield event
        quota_finalize(grant.id, success=True)
    except Exception as exc:
        quota_finalize(grant.id, success=False)
        yield error_event(exc)</pre>

<h1>8 部署及更新方案</h1>
<p>开发人员只需要理解交付分层：业务代码进入对应服务镜像，大数据进入数据包。只修改某个后端时，优先只构建并交付该后端镜像；修改数据资源时，重新生成对应数据包和 manifest。详细步骤见部署手册。</p>

<h1>9 常见问题与解决方案</h1>
<table>
  <tr><th>类别</th><th>问题</th><th>处理建议</th></tr>
  <tr><td>数据质量</td><td>专利 tables 缺失或 manifest 未登记。</td><td>运行 tables backfill，并使用 validate_data_packages 检查。</td></tr>
  <tr><td>模型调用</td><td>OpenAI 兼容接口参数不兼容。</td><td>检查 stream、enable_thinking、模型名和 base url。</td></tr>
  <tr><td>性能优化</td><td>检索或 rerank 慢。</td><td>检查候选数量、连接池、模型服务延迟和向量库路径。</td></tr>
  <tr><td>数据库</td><td>配额扣减异常。</td><td>检查 precheck/finalize 是否成对执行，检查 quota 表唯一键。</td></tr>
  <tr><td>前端</td><td>SSE 阶段显示错位。</td><td>检查事件 schema、稳定 key 和渲染状态机。</td></tr>
</table>

<h1>10 参考文档</h1>
<table>
  <tr><th>文档</th><th>用途</th></tr>
  <tr><td>LiFeO4Agent 部署手册</td><td>部署和升级。</td></tr>
  <tr><td>LiFeO4Agent 系统概要设计说明书</td><td>架构和技术选型。</td></tr>
  <tr><td>LiFeO4Agent 系统详细设计说明书</td><td>模块、接口和流程。</td></tr>
  <tr><td>FastAPI、Vue、Docker、MinIO、Neo4j 官方文档</td><td>第三方组件参考。</td></tr>
</table>
"""

SUMMARY_DESIGN_FINAL = """
<h1>1 简介</h1>
<h2>1.1 编写目的</h2>
<p>本文档从宏观层面说明 LiFeO4Agent 的系统目标、总体架构、技术选型、模块划分、集成关系、部署策略、数据设计、安全和非功能设计，用于指导详细设计、开发实现、测试验收和后续运维。</p>
<h2>1.2 适用范围</h2>
<p>本文档适用于项目组成员、测试人员、部署运维人员和业务负责人。最终用户操作说明见用户手册；部署命令和现场实施步骤见部署手册。</p>
<h2>1.3 名词术语</h2>
<table>
  <tr><th>编号</th><th>术语</th><th>说明</th></tr>
  <tr><td>1</td><td>RAG</td><td>检索增强生成，通过检索知识库内容辅助大模型回答。</td></tr>
  <tr><td>2</td><td>MinIO</td><td>对象存储，保存论文、专利原文和运行期文件。</td></tr>
  <tr><td>3</td><td>Chroma</td><td>向量数据库，用于文献、专利和深度问答检索。</td></tr>
  <tr><td>4</td><td>Neo4j</td><td>图数据库，承载文献和专利知识图谱。</td></tr>
  <tr><td>5</td><td>Seed</td><td>部署时自动导入初始数据的过程。</td></tr>
</table>
<h2>1.4 参考资料</h2>
<table>
  <tr><th>资料</th><th>说明</th></tr>
  <tr><td>需求清单 V1.0</td><td>功能和非功能需求来源。</td></tr>
  <tr><td>部署手册 V1.0</td><td>部署和数据导入方式。</td></tr>
  <tr><td>开发文档 V1.0</td><td>工程结构和接口实现。</td></tr>
</table>

<h1>2 系统架构设计</h1>
<h2>2.1 项目简介</h2>
<p>LiFeO4Agent 面向电池材料研发领域，帮助用户围绕文献、专利和上传文件进行专业问答、归纳分析和原文核对，提高研发信息检索和技术分析效率。</p>
<h2>2.2 现状及应用场景</h2>
<p>研发人员需要同时查询论文、专利、实验文件和知识图谱。传统检索方式存在信息分散、原文定位慢、专利表格难利用、文献和专利分析链路割裂等问题。系统通过文献问答、深度问答、专利问答和文件问答，将检索、重排、图谱和生成能力统一到一个入口。</p>
<h2>2.3 建设目标</h2>
<table>
  <tr><th>目标</th><th>说明</th></tr>
  <tr><td>统一入口</td><td>提供浏览器端统一问答和管理入口。</td></tr>
  <tr><td>三类问答</td><td>支持文献、深度、专利三种模式。</td></tr>
  <tr><td>原文可核对</td><td>论文和专利原文统一从 MinIO 读取。</td></tr>
  <tr><td>可离线交付</td><td>镜像和数据包可在内网环境部署。</td></tr>
  <tr><td>可增量维护</td><td>后续可按服务镜像或数据包单独升级。</td></tr>
</table>

<h1>3 架构</h1>
<div class="diagram">
  <div class="diagram-title">图 1 系统功能架构图</div>
  <pre class="mermaid">mindmap
  root((LiFeO4Agent))
    用户门户
      登录注册找回密码
      文献问答
      深度问答
      专利问答
      文件问答和原文查看
    管理后台
      用户管理
      部门管理
      人员管理
      配额管理
    问答服务层
      gateway
      fastQA
      highThinkingQA
      patentQA
    公共服务层
      public-service
    数据与基础设施
      MySQL
      Redis
      MinIO
      Chroma reference data
      Neo4j literature
      Neo4j patent</pre>
</div>

<h2>3.1 功能模块说明</h2>
<table>
  <tr><th>模块</th><th>职责</th><th>交互方式</th></tr>
  <tr><td>前端门户</td><td>提供用户操作界面。</td><td>调用 gateway API。</td></tr>
  <tr><td>gateway</td><td>认证代理、路由、SSE、配额协调。</td><td>调用 public-service 和 QA 后端。</td></tr>
  <tr><td>public-service</td><td>用户、部门、人员、配额、文件、原文代理。</td><td>访问 MySQL、Redis、MinIO。</td></tr>
  <tr><td>fastQA</td><td>文献检索和生成。</td><td>访问 fastQA 向量库、MinIO、文献图谱和模型。</td></tr>
  <tr><td>highThinkingQA</td><td>深度问答和多阶段推理。</td><td>访问 vectordb、MinIO 和模型。</td></tr>
  <tr><td>patentQA</td><td>专利检索、tables、图谱增强和回答。</td><td>访问 patentQA 向量库、MinIO、专利图谱和模型。</td></tr>
</table>

<h1>4 软件架构</h1>
<div class="diagram">
  <div class="diagram-title">图 2 软件技术栈分层图</div>
  <pre class="mermaid">flowchart TB
  A[表现层<br/>Vue 3 + Vite + nginx]
  B[接入层<br/>edge nginx + gateway FastAPI]
  C[业务服务层<br/>public-service / fastQA / highThinkingQA / patentQA]
  D[智能能力层<br/>LLM / intent / embedding / rerank]
  E[数据访问层<br/>MySQL client / Redis client / MinIO client / Neo4j driver / Chroma]
  F[基础设施层<br/>Docker / Docker Compose / named volumes / seed-tools]
  A --> B --> C
  C --> D
  C --> E
  E --> F</pre>
</div>
<table>
  <tr><th>技术组件</th><th>用途</th><th>场景</th></tr>
  <tr><td>Vue 3</td><td>构建前端页面。</td><td>问答首页、个人中心、管理后台。</td></tr>
  <tr><td>FastAPI</td><td>构建后端 HTTP 服务。</td><td>gateway 和各后端服务。</td></tr>
  <tr><td>MySQL</td><td>持久化业务数据。</td><td>用户、部门、人员、配额、会话。</td></tr>
  <tr><td>Redis</td><td>缓存和运行态协调。</td><td>会话状态、配额缓存、任务状态。</td></tr>
  <tr><td>MinIO</td><td>对象存储。</td><td>论文、专利、上传文件。</td></tr>
  <tr><td>Neo4j</td><td>图谱查询。</td><td>文献图谱、专利图谱。</td></tr>
  <tr><td>Chroma</td><td>向量检索。</td><td>文献、专利、深度问答向量库。</td></tr>
</table>

<h1>5 集成架构</h1>
<div class="diagram">
  <div class="diagram-title">图 3 外部集成架构图</div>
  <pre class="mermaid">flowchart LR
  SYS[LiFeO4Agent]
  SYS --> LLM[LLM 服务<br/>答案生成/规划/总结]
  SYS --> INTENT[Intent 模型<br/>文献和专利意图识别]
  SYS --> EMB[Embedding 服务<br/>查询向量化]
  SYS --> RR[Rerank 服务<br/>候选重排]
  USER[客户端浏览器] --> DNS[客户内网 DNS 或 hosts]
  DNS --> SYS
  CERT[客户证书体系] --> USER</pre>
</div>
<table>
  <tr><th>接口名称</th><th>请求方</th><th>提供方</th><th>功能</th></tr>
  <tr><td>Chat Completions</td><td>QA 后端</td><td>LLM 服务</td><td>生成答案、规划和总结。</td></tr>
  <tr><td>Embedding</td><td>QA 后端</td><td>Embedding 服务</td><td>查询向量化。</td></tr>
  <tr><td>Rerank</td><td>fastQA、patentQA</td><td>Rerank 服务</td><td>候选片段排序。</td></tr>
  <tr><td>Intent</td><td>fastQA、patentQA</td><td>Intent 模型服务</td><td>识别问题意图。</td></tr>
</table>

<h1>6 部署架构</h1>
<div class="diagram">
  <div class="diagram-title">图 4 部署架构图</div>
  <pre class="mermaid">flowchart TB
  subgraph HOST[部署服务器]
    subgraph NET[Docker bridge network: lifeo4agent-net]
      EDGE[edge]
      FRONT[frontend]
      GW[gateway]
      PS[public-service]
      FQ[fastQA]
      HT[highThinkingQA]
      PT[patentQA]
      DB[(mysql_data)]
      RD[(redis_data)]
      MO[(minio_data)]
      RF[(reference volumes)]
      NG[(neo4j volumes)]
    end
    DATA[deploy/data 数据包]
    SEED[seed jobs]
  end
  DATA --> SEED
  SEED --> MO
  SEED --> RF
  SEED --> NG
  EDGE --> FRONT --> GW
  GW --> PS
  GW --> FQ
  GW --> HT
  GW --> PT</pre>
</div>
<p>部署采用容器化微服务方式。内部服务使用 compose service name 通信；部署方主要暴露 HTTPS、MySQL、Redis 和 MinIO 管理端口。Neo4j 地址不暴露给部署方配置，内部固定为 <code>neo4j-literature</code> 和 <code>neo4j-patent</code>。</p>

<h1>7 数据库设计</h1>
<div class="diagram">
  <div class="diagram-title">图 5 主要实体关系图</div>
  <pre class="mermaid">erDiagram
  primary_departments ||--o{ secondary_departments : contains
  secondary_departments ||--o{ tertiary_departments : contains
  primary_departments ||--o{ personnel_records : assigns
  secondary_departments ||--o{ personnel_records : assigns
  tertiary_departments ||--o{ personnel_records : assigns
  personnel_records ||--o{ users : binds
  users ||--o{ conversations : owns
  conversations ||--o{ conversation_messages : contains
  conversations ||--o{ conversation_files : contains
  quota_configs ||--o{ user_quota_usage : controls
  users ||--o{ user_quota_usage : consumes
  quota_configs ||--o{ user_quota_overrides : overrides
  users ||--o{ user_quota_overrides : has</pre>
</div>
<p>重要业务表均包含创建时间或更新时间字段，用于增量追踪和审计。用户、部门和人员使用状态字段停用，避免直接物理删除造成历史数据失联。后续新增业务表时，应补充 <code>created_at</code>、<code>updated_at</code> 或等价增量字段；涉及删除的主数据优先使用逻辑删除或状态停用。</p>

<h1>8 基本功能设计</h1>
<h2>8.1 异常处理</h2>
<table>
  <tr><th>异常类型</th><th>处理策略</th></tr>
  <tr><td>业务异常</td><td>返回明确提示，例如配额不足、账号停用、文件格式不支持。</td></tr>
  <tr><td>系统异常</td><td>记录日志并返回通用错误，避免暴露内部细节。</td></tr>
  <tr><td>外部模型异常</td><td>记录模型响应和请求阶段，必要时提示模型服务不可用。</td></tr>
  <tr><td>数据导入异常</td><td>seed job 失败退出，部署预检或日志中提示原因。</td></tr>
</table>
<h2>8.2 可配置项</h2>
<p>客户主配置面包括端口、账号密码、MinIO、LLM、intent、embedding、rerank 和数据包版本。内部服务 URL、Redis DB、Neo4j 地址和 worker 参数由 compose 默认值控制，避免部署方配置过多内部细节。</p>
<h2>8.3 系统日志</h2>
<p>各容器输出标准日志，由 Docker 收集。重要日志包括 gateway 路由和配额日志、QA 阶段日志、模型调用错误、seed job 导入日志和基础组件健康检查日志。</p>
<h2>8.4 个人信息安全保护</h2>
<p>系统仅收集账号、工号、姓名、部门、人员绑定和安全问题等使用所需信息。密码和校验码以哈希形式保存，文档和镜像不写入真实密钥。系统应按客户制度控制访问权限、定期清理不再使用的外来人员记录，并避免在日志中输出敏感信息。</p>

<h1>9 非功能设计</h1>
<table>
  <tr><th>类别</th><th>设计要求</th></tr>
  <tr><td>性能</td><td>登录、管理类接口应快速响应；问答耗时受模型服务影响，需记录阶段耗时。</td></tr>
  <tr><td>高可用</td><td>V1.0 单机 compose 部署；后续可替换为外部高可用 MySQL、Redis、MinIO 和多实例业务服务。</td></tr>
  <tr><td>安全性</td><td>JWT 认证、管理员权限控制、内部 token、TLS 传输、密码哈希。</td></tr>
  <tr><td>可维护性</td><td>服务拆分清晰，镜像和数据包分离，支持单服务增量更新。</td></tr>
  <tr><td>可恢复性</td><td>运行态数据备份；reference data 和图谱可由数据包重建。</td></tr>
</table>
"""

DETAILED_DESIGN_FINAL = """
<h1>1 功能模块划分</h1>
<table>
  <tr><th>一级模块</th><th>子功能</th><th>说明</th></tr>
  <tr><td>账号认证</td><td>登录、注册、找回密码、修改密码、安全问题、个人中心。</td><td>面向所有用户。</td></tr>
  <tr><td>问答工作台</td><td>会话管理、文献问答、深度问答、专利问答、文件问答、阶段展示。</td><td>核心业务入口。</td></tr>
  <tr><td>文件与原文</td><td>上传、列表、下载、删除、论文原文、专利原文、专利 tables。</td><td>支撑知识核对。</td></tr>
  <tr><td>管理后台</td><td>用户管理、部门管理、人员管理、配额管理。</td><td>管理员使用。</td></tr>
  <tr><td>部署数据</td><td>MinIO seed、reference seed、Neo4j seed。</td><td>部署初始化。</td></tr>
</table>

<h1>2 账号认证模块设计</h1>
<h2>2.1 功能描述</h2>
<p>账号认证模块负责用户登录、注册、首次登录安全设置、密码修改、安全问题设置和找回密码。普通用户注册必须匹配有效人员记录；管理员账号由 MySQL 初始化脚本创建。</p>
<h2>2.2 前端页面</h2>
<table>
  <tr><th>页面</th><th>路径</th><th>交互细节</th></tr>
  <tr><td>登录页</td><td><code>/login</code></td><td>输入用户名和密码，登录成功后按角色跳转。</td></tr>
  <tr><td>注册页</td><td><code>/register</code></td><td>输入用户名、密码、姓名、工号、校验码。</td></tr>
  <tr><td>找回密码</td><td><code>/forgot-password</code></td><td>通过安全问题验证后重置密码。</td></tr>
  <tr><td>个人中心</td><td><code>/profile</code></td><td>修改用户名、密码、安全问题和人员绑定。</td></tr>
</table>
<div class="diagram">
  <div class="diagram-title">图 1 登录流程图</div>
  <pre class="mermaid">sequenceDiagram
  participant U as 用户
  participant FE as 前端
  participant GW as gateway
  participant PS as public-service
  participant DB as MySQL
  U->>FE: 输入用户名和密码
  FE->>GW: POST /api/auth/login
  GW->>PS: 代理登录请求
  PS->>DB: 查询用户和密码哈希
  alt 登录成功
    PS-->>GW: token + 用户信息
    GW-->>FE: 登录成功
    alt 需要安全设置
      FE-->>U: 跳转 /profile
    else 已完成设置
      FE-->>U: 进入首页或管理后台
    end
  else 登录失败
    PS-->>GW: 错误码和用户提示
    GW-->>FE: 登录失败
    FE-->>U: 展示错误提示
  end</pre>
</div>
<h2>2.3 库表设计</h2>
<table>
  <tr><th>表名</th><th>字段</th><th>类型</th><th>备注</th></tr>
  <tr><td><code>users</code></td><td><code>id</code></td><td>bigint</td><td>主键。</td></tr>
  <tr><td><code>users</code></td><td><code>username</code></td><td>varchar(64)</td><td>唯一用户名。</td></tr>
  <tr><td><code>users</code></td><td><code>password_hash</code></td><td>varchar(255)</td><td>密码哈希。</td></tr>
  <tr><td><code>users</code></td><td><code>role</code></td><td>enum</td><td><code>user</code> 或 <code>admin</code>。</td></tr>
  <tr><td><code>users</code></td><td><code>status</code></td><td>enum</td><td><code>active</code> 或 <code>disabled</code>。</td></tr>
  <tr><td><code>user_security_questions</code></td><td><code>question</code>、<code>answer_hash</code></td><td>varchar</td><td>找回密码使用。</td></tr>
  <tr><td><code>password_history</code></td><td><code>password_hash</code></td><td>varchar(255)</td><td>密码历史。</td></tr>
</table>
<h2>2.4 接口说明</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>输入</th><th>输出</th><th>错误码</th></tr>
  <tr><td><code>/api/auth/login</code></td><td>POST</td><td>用户名、密码。</td><td>token、用户信息、首次登录标志。</td><td>账号不存在、密码错误、账号停用。</td></tr>
  <tr><td><code>/api/auth/register</code></td><td>POST</td><td>用户名、密码、姓名、工号、校验码。</td><td>注册成功用户信息。</td><td>人员不匹配、用户名重复。</td></tr>
  <tr><td><code>/api/auth/password</code></td><td>PUT/POST</td><td>旧密码、新密码。</td><td>修改结果。</td><td>旧密码错误、复杂度不足。</td></tr>
  <tr><td><code>/api/auth/forgot-password/initiate</code></td><td>POST</td><td>用户名。</td><td>安全问题列表。</td><td>未设置安全问题。</td></tr>
  <tr><td><code>/api/auth/forgot-password/verify</code></td><td>POST</td><td>用户名、安全问题答案、新密码。</td><td>重置结果。</td><td>答案错误。</td></tr>
</table>

<h1>3 问答工作台模块设计</h1>
<h2>3.1 功能描述</h2>
<p>问答工作台负责会话创建、模式选择、问题发送、SSE 事件渲染、引用展示、文件选择和原文查看入口。前端用户可选择“文献”“深度”“专利”三种模式。</p>
<h2>3.2 处理流程</h2>
<div class="diagram">
  <div class="diagram-title">图 2 问答处理流程图</div>
  <pre class="mermaid">sequenceDiagram
  participant U as 用户
  participant FE as 前端
  participant GW as gateway
  participant PS as public-service
  participant QA as 目标 QA 后端
  participant M as 模型服务
  participant D as 向量库/MinIO/Neo4j
  U->>FE: 选择模式并提交问题
  FE->>GW: POST /api/{mode}/ask_stream
  GW->>PS: 校验 token 和读取会话文件
  GW->>PS: 配额 precheck
  GW->>QA: 转发流式问答
  QA->>D: 检索原文、向量库、图谱
  QA->>M: intent / embedding / rerank / LLM
  loop SSE 事件
    QA-->>GW: 阶段、文本、引用、完成事件
    GW-->>FE: 透传 SSE
    FE-->>U: 渲染进度和回答
  end
  GW->>PS: 配额 finalize 和会话持久化</pre>
</div>
<h2>3.3 接口说明</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>说明</th><th>输出</th></tr>
  <tr><td><code>/api/fast/ask_stream</code></td><td>POST</td><td>文献流式问答。</td><td>SSE 事件。</td></tr>
  <tr><td><code>/api/thinking/ask_stream</code></td><td>POST</td><td>深度流式问答。</td><td>SSE 事件。</td></tr>
  <tr><td><code>/api/patent/ask_stream</code></td><td>POST</td><td>专利流式问答。</td><td>SSE 事件。</td></tr>
  <tr><td><code>/api/v1/tasks</code></td><td>POST</td><td>创建可恢复任务。</td><td>task_id。</td></tr>
  <tr><td><code>/api/v1/tasks/{task_id}/events</code></td><td>GET</td><td>读取任务事件。</td><td>SSE 事件。</td></tr>
</table>
<h2>3.4 输入输出规范</h2>
<p>输入至少包含问题文本和模式。输出事件包括阶段开始、阶段结束、文本增量、引用、错误和完成。错误事件应包含用户可理解提示，不应泄漏内部密钥或堆栈。</p>

<h1>4 文件和原文模块设计</h1>
<h2>4.1 功能描述</h2>
<p>文件模块支持上传 PDF、Excel、CSV，并将文件元数据绑定到会话。原文模块负责从 MinIO 读取论文 PDF、专利 PDF、专利图片和 structured tables。</p>
<h2>4.2 库表设计</h2>
<table>
  <tr><th>表名</th><th>字段</th><th>类型</th><th>备注</th></tr>
  <tr><td><code>conversation_files</code></td><td><code>id</code></td><td>bigint</td><td>主键。</td></tr>
  <tr><td><code>conversation_files</code></td><td><code>conversation_id</code>、<code>user_id</code></td><td>bigint</td><td>所属会话和用户。</td></tr>
  <tr><td><code>conversation_files</code></td><td><code>file_type</code></td><td>enum</td><td>PDF 或 Excel；CSV 可按表格文件处理。</td></tr>
  <tr><td><code>conversation_files</code></td><td><code>storage_ref</code></td><td>varchar(1024)</td><td>MinIO 对象引用。</td></tr>
</table>
<h2>4.3 异常处理</h2>
<table>
  <tr><th>异常</th><th>用户提示</th><th>后端处理</th></tr>
  <tr><td>文件为空</td><td>请选择有效文件。</td><td>返回 400。</td></tr>
  <tr><td>格式不支持</td><td>仅支持 PDF、Excel、CSV。</td><td>校验 content type 和扩展名。</td></tr>
  <tr><td>对象不存在</td><td>原文暂不可用。</td><td>记录 MinIO key 和请求 ID。</td></tr>
  <tr><td>文件过大</td><td>文件超过限制。</td><td>由前端和 nginx 限制。</td></tr>
</table>

<h1>5 管理后台模块设计</h1>
<h2>5.1 用户管理</h2>
<p>管理员可查询用户、创建用户、修改用户名、重置密码、停用启用、修改用户类型、绑定或解绑人员记录。删除用户属于高风险操作，应在前端二次确认。</p>
<h2>5.2 部门管理</h2>
<p>部门按一级、二级、三级维护。当前 seed 包含电池材料技术研究中心、正极材料研究所、装备工程化研究所、材料应用研究所及三级部门。停用部门不删除历史绑定关系。</p>
<h2>5.3 人员管理</h2>
<p>人员记录包含工号、姓名、校验码哈希、状态和部门。注册和个人中心绑定必须匹配人员记录。</p>
<h2>5.4 配额管理</h2>
<p>配额类型包含 <code>ask_query</code>、<code>file_qa</code>、<code>file_view</code>、<code>doc_assist</code>。系统支持默认配额、周期窗口、用户例外和重置。</p>

<h1>6 非功能设计</h1>
<table>
  <tr><th>模块</th><th>性能指标</th><th>安全措施</th><th>可靠性措施</th></tr>
  <tr><td>认证</td><td>登录接口应快速响应。</td><td>密码哈希、JWT、账号状态。</td><td>失败提示明确，避免泄漏。</td></tr>
  <tr><td>问答</td><td>记录首 token 和总耗时。</td><td>token 校验、配额控制。</td><td>SSE 错误事件和超时处理。</td></tr>
  <tr><td>文件</td><td>上传大小受限。</td><td>文件类型校验、对象权限。</td><td>元数据和对象引用分离。</td></tr>
  <tr><td>管理</td><td>列表分页。</td><td>管理员权限。</td><td>停用优先于物理删除。</td></tr>
</table>

<h1>7 技术实现规范</h1>
<table>
  <tr><th>类别</th><th>规范</th></tr>
  <tr><td>Python</td><td>4 空格缩进，函数和模块 snake_case，类 PascalCase。</td></tr>
  <tr><td>Vue/JS</td><td>保留现有组件结构，避免将业务逻辑堆在单一组件。</td></tr>
  <tr><td>接口</td><td>新增对外接口优先经 gateway 暴露，响应结构保持一致。</td></tr>
  <tr><td>配置</td><td>新增配置项需同步 shared env、secret env、compose、模板和文档。</td></tr>
  <tr><td>版本控制</td><td>提交信息使用 <code>feat:</code>、<code>fix:</code>、<code>docs:</code> 等前缀。</td></tr>
</table>

<h1>8 测试设计</h1>
<table>
  <tr><th>测试类型</th><th>覆盖范围</th></tr>
  <tr><td>单元测试</td><td>配置加载、路由决策、配额服务、数据包校验、核心工具函数。</td></tr>
  <tr><td>集成测试</td><td>认证接口、管理员接口、问答代理、任务恢复、MinIO 原文代理。</td></tr>
  <tr><td>前端结构测试</td><td>路由、关键组件、配额卡片、管理面板。</td></tr>
  <tr><td>部署测试</td><td>preflight、seed job、compose healthcheck。</td></tr>
</table>
<p>缺陷等级分为 Blocker、Critical、Major、Minor。Blocker 和 Critical 必须在发布前关闭；Major 需评估是否影响验收；Minor 可记录为遗留优化。</p>
"""

REQUIREMENT_LIST_FINAL = """
<h1>需求清单</h1>
<table>
  <tr><th>序号</th><th>需求层级</th><th>需求简述</th><th>提出时间</th><th>需求文档</th><th>完成时间</th><th>状态</th><th>备注</th></tr>
  <tr><td class="center">REQ-001</td><td>业务需求-问答</td><td>系统应提供文献、深度、专利三种问答模式。</td><td>2026-05-20</td><td>需求规格说明书 V1.0</td><td>2026-05-20</td><td>已实现</td><td>前端显示为“文献/深度/专利”。</td></tr>
  <tr><td class="center">REQ-002</td><td>业务需求-文件</td><td>系统应支持 PDF、Excel、CSV 上传并参与问答。</td><td>2026-05-20</td><td>需求规格说明书 V1.0</td><td>2026-05-20</td><td>已实现</td><td>由 public-service 管理文件元数据。</td></tr>
  <tr><td class="center">REQ-003</td><td>业务需求-原文</td><td>系统应支持论文和专利原文查看。</td><td>2026-05-20</td><td>需求规格说明书 V1.0</td><td>2026-05-20</td><td>已实现</td><td>原文存储在 MinIO。</td></tr>
  <tr><td class="center">REQ-004</td><td>业务需求-专利</td><td>专利问答应能读取 structured tables 数据。</td><td>2026-05-20</td><td>MinIO 原文数据计划</td><td>2026-05-20</td><td>已实现</td><td>tables 文件数 9581。</td></tr>
  <tr><td class="center">REQ-005</td><td>账号权限-登录</td><td>用户应能通过用户名和密码登录。</td><td>2026-05-20</td><td>账号管理需求</td><td>2026-05-20</td><td>已实现</td><td>登录成功返回 token。</td></tr>
  <tr><td class="center">REQ-006</td><td>账号权限-注册</td><td>普通用户注册必须校验人员记录。</td><td>2026-05-20</td><td>账号管理需求</td><td>2026-05-20</td><td>已实现</td><td>姓名、工号、校验码匹配。</td></tr>
  <tr><td class="center">REQ-007</td><td>账号权限-安全</td><td>首次登录应强制修改密码并设置安全问题。</td><td>2026-05-20</td><td>账号安全需求</td><td>2026-05-20</td><td>已实现</td><td>管理员初始账号同样适用。</td></tr>
  <tr><td class="center">REQ-008</td><td>账号权限-找回</td><td>用户应能通过安全问题找回密码。</td><td>2026-05-20</td><td>账号安全需求</td><td>2026-05-20</td><td>已实现</td><td>未设置安全问题需管理员处理。</td></tr>
  <tr><td class="center">REQ-009</td><td>管理后台-用户</td><td>管理员应能维护用户状态、密码、类型和人员绑定。</td><td>2026-05-20</td><td>管理后台需求</td><td>2026-05-20</td><td>已实现</td><td>支持批量操作。</td></tr>
  <tr><td class="center">REQ-010</td><td>管理后台-部门</td><td>管理员应能维护三级部门。</td><td>2026-05-20</td><td>管理后台需求</td><td>2026-05-20</td><td>已实现</td><td>seed 导入真实部门树。</td></tr>
  <tr><td class="center">REQ-011</td><td>管理后台-人员</td><td>管理员应能维护人员记录和批量导入模板。</td><td>2026-05-20</td><td>管理后台需求</td><td>2026-05-20</td><td>已实现</td><td>用于注册和绑定。</td></tr>
  <tr><td class="center">REQ-012</td><td>管理后台-配额</td><td>管理员应能配置普通问答、文件问答、查看原文、文档辅助配额。</td><td>2026-05-20</td><td>配额需求</td><td>2026-05-20</td><td>已实现</td><td>支持默认配置和用户重置。</td></tr>
  <tr><td class="center">REQ-013</td><td>后端-gateway</td><td>gateway 应统一代理认证、会话、问答和文件请求。</td><td>2026-05-20</td><td>架构设计</td><td>2026-05-20</td><td>已实现</td><td>前端主要访问 gateway。</td></tr>
  <tr><td class="center">REQ-014</td><td>后端-public-service</td><td>public-service 应独立承载公共业务能力。</td><td>2026-05-20</td><td>架构设计</td><td>2026-05-20</td><td>已实现</td><td>用户、部门、人员、配额、文件。</td></tr>
  <tr><td class="center">REQ-015</td><td>后端-fastQA</td><td>fastQA 应加载文献向量库和主题索引。</td><td>2026-05-20</td><td>文献问答需求</td><td>2026-05-20</td><td>已实现</td><td>数据包 fastqa-ref。</td></tr>
  <tr><td class="center">REQ-016</td><td>后端-highThinkingQA</td><td>highThinkingQA 应加载独立 vectordb。</td><td>2026-05-20</td><td>深度问答需求</td><td>2026-05-20</td><td>已实现</td><td>数据包 highthinking-ref。</td></tr>
  <tr><td class="center">REQ-017</td><td>后端-patentQA</td><td>patentQA 应加载两个专利向量库和 JSON-only archive。</td><td>2026-05-20</td><td>专利问答需求</td><td>2026-05-20</td><td>已实现</td><td>数据包 patentqa-ref。</td></tr>
  <tr><td class="center">REQ-018</td><td>数据-MinIO</td><td>论文和专利原文应只以 MinIO 为权威副本。</td><td>2026-05-20</td><td>数据交付方案</td><td>2026-05-20</td><td>已实现</td><td>后端不重复携带 PDF/PNG。</td></tr>
  <tr><td class="center">REQ-019</td><td>数据-向量库</td><td>向量库应通过 named volume 挂载，部署方不手工配置路径。</td><td>2026-05-20</td><td>数据交付方案</td><td>2026-05-20</td><td>已实现</td><td>compose 固定内部路径。</td></tr>
  <tr><td class="center">REQ-020</td><td>数据-图谱</td><td>文献和专利图谱应分别使用独立 Neo4j 容器。</td><td>2026-05-20</td><td>图谱部署方案</td><td>2026-05-20</td><td>已实现</td><td>部署方不配置 Neo4j 地址。</td></tr>
  <tr><td class="center">REQ-021</td><td>模型-LLM</td><td>系统应支持统一 LLM base url、模型名和 API Key。</td><td>2026-05-20</td><td>模型配置方案</td><td>2026-05-20</td><td>已实现</td><td>配置在 deploy/.env。</td></tr>
  <tr><td class="center">REQ-022</td><td>模型-intent</td><td>fastQA 和 patentQA 应使用统一 intent 模型配置名。</td><td>2026-05-20</td><td>模型配置方案</td><td>2026-05-20</td><td>已实现</td><td><code>INTENT_MODEL_*</code>。</td></tr>
  <tr><td class="center">REQ-023</td><td>模型-embedding</td><td>fastQA/patentQA 和 highThinkingQA 应分别配置 embedding。</td><td>2026-05-20</td><td>模型配置方案</td><td>2026-05-20</td><td>已实现</td><td><code>QA_EMBEDDING_*</code> 与 <code>HIGHTHINKINGQA_EMBEDDING_*</code>。</td></tr>
  <tr><td class="center">REQ-024</td><td>模型-rerank</td><td>文献和专利检索应支持统一 rerank 配置和禁用。</td><td>2026-05-20</td><td>模型配置方案</td><td>2026-05-20</td><td>已实现</td><td><code>RERANK_PROVIDER=none</code> 可禁用。</td></tr>
  <tr><td class="center">REQ-025</td><td>部署-离线</td><td>部署方应能通过 docker load 和 compose 完成离线部署。</td><td>2026-05-20</td><td>部署方案</td><td>2026-05-20</td><td>已实现</td><td>无需宿主机安装 mc/zstd/neo4j-admin。</td></tr>
  <tr><td class="center">REQ-026</td><td>部署-HTTPS</td><td>系统应提供 HTTPS 入口并支持部署方替换证书。</td><td>2026-05-20</td><td>HTTPS 需求</td><td>2026-05-20</td><td>已实现</td><td>edge nginx 处理 TLS。</td></tr>
  <tr><td class="center">REQ-027</td><td>部署-预检</td><td>系统应提供 preflight 检查配置、镜像和数据包。</td><td>2026-05-20</td><td>运维需求</td><td>2026-05-20</td><td>已实现</td><td><code>preflight_check.sh</code>。</td></tr>
  <tr><td class="center">REQ-028</td><td>部署-更新</td><td>系统应支持单服务镜像增量更新。</td><td>2026-05-20</td><td>更新部署需求</td><td>2026-05-20</td><td>已实现</td><td>例如只更新 fastQA。</td></tr>
  <tr><td class="center">REQ-029</td><td>运维-备份</td><td>系统应区分运行态数据和可重建 reference data。</td><td>2026-05-20</td><td>运维需求</td><td>2026-05-20</td><td>已实现</td><td>MySQL 和运行期 MinIO 需备份。</td></tr>
  <tr><td class="center">REQ-030</td><td>安全-隐私</td><td>系统不应在文档和镜像上下文中包含真实密钥。</td><td>2026-05-20</td><td>安全要求</td><td>2026-05-20</td><td>已实现</td><td>密钥由部署方填写。</td></tr>
</table>
"""

USER_MANUAL_FINAL = """
<h1>1 文档说明</h1>
<p>本文档面向 LiFeO4Agent 最终用户和管理员，说明如何注册、登录、使用问答功能、上传文件、查看原文、管理用户和处理常见问题。本文档不要求用户了解 Docker、MinIO、Neo4j 或部署细节。</p>

<h1>2 用户注册</h1>
<h2>2.1 操作入口</h2>
<p>在浏览器访问系统地址，进入登录页后点击“注册账号”。</p>
<div class="diagram">
  <div class="diagram-title">图 1 注册入口界面示意图</div>
  <pre class="mermaid">flowchart LR
  A[打开登录页] --> B[点击注册账号]
  B --> C[进入注册页]
  C --> D[填写用户名/密码/姓名/工号/校验码]
  D --> E[提交注册]
  E --> F{人员记录校验}
  F -- 通过 --> G[注册成功并返回登录]
  F -- 不通过 --> H[提示人员信息或校验码错误]</pre>
</div>
<h2>2.2 注册步骤</h2>
<ol>
  <li>点击“注册账号”，进入注册页。</li>
  <li>填写用户名。用户名长度为 3 到 50 个字符，不能以 <code>admin</code> 开头。</li>
  <li>填写密码并再次确认密码。</li>
  <li>填写姓名、工号和校验码。该信息需要与管理员维护的人员记录一致。</li>
  <li>点击提交。</li>
  <li>页面提示注册成功后返回登录页。</li>
</ol>
<h2>2.3 预期结果</h2>
<p>注册成功后，用户账号处于可登录状态，部门信息由人员记录自动带出。注册失败时，页面会提示用户名重复、人员信息不匹配、校验码错误或密码不符合要求。</p>

<h1>3 登录和个人中心</h1>
<h2>3.1 登录步骤</h2>
<ol>
  <li>打开系统地址。</li>
  <li>输入用户名和密码。</li>
  <li>点击“登录”。</li>
  <li>普通用户进入问答首页，管理员进入管理后台。</li>
</ol>
<h2>3.2 首次登录</h2>
<p>首次登录时，系统可能要求修改密码、设置安全问题或补全人员信息。用户应按页面提示进入个人中心完成设置，完成后才能正常使用全部功能。</p>
<h2>3.3 个人中心</h2>
<table>
  <tr><th>功能</th><th>入口</th><th>操作说明</th></tr>
  <tr><td>修改用户名</td><td>个人中心</td><td>输入新用户名并保存。</td></tr>
  <tr><td>修改密码</td><td>个人中心</td><td>输入旧密码和新密码。</td></tr>
  <tr><td>设置安全问题</td><td>个人中心</td><td>设置用于找回密码的问题和答案。</td></tr>
  <tr><td>绑定人员信息</td><td>个人中心</td><td>输入工号、姓名和校验码。</td></tr>
</table>

<h1>4 问答首页操作说明</h1>
<div class="diagram">
  <div class="diagram-title">图 2 问答首页区域示意图</div>
  <pre class="mermaid">flowchart TB
  HOME[问答首页] --> LEFT[左侧会话列表]
  HOME --> CENTER[中间消息区]
  HOME --> RIGHT[右侧问题大纲]
  HOME --> INPUT[底部输入区]
  LEFT --> L1[新建/切换/置顶/删除会话]
  LEFT --> L2[会话文件列表]
  CENTER --> C1[用户问题]
  CENTER --> C2[系统回答]
  CENTER --> C3[阶段进度/耗时/引用/原文入口]
  RIGHT --> R1[按历史问题跳转]
  INPUT --> I1[模式选择：文献/深度/专利]
  INPUT --> I2[上传 PDF/Excel/CSV]
  INPUT --> I3[输入问题并发送]</pre>
</div>
<table>
  <tr><th>区域</th><th>作用</th></tr>
  <tr><td>会话列表</td><td>新建、切换、置顶或删除会话。</td></tr>
  <tr><td>文件列表</td><td>查看本会话上传文件，选择本轮问答使用哪些文件。</td></tr>
  <tr><td>消息区</td><td>查看问题、回答、阶段、引用和错误提示。</td></tr>
  <tr><td>问题大纲</td><td>长对话中快速跳转到历史问题。</td></tr>
  <tr><td>输入区</td><td>选择问答模式、上传文件并发送问题。</td></tr>
</table>

<h1>5 文献问答</h1>
<h2>5.1 操作入口</h2>
<p>在首页底部模式选择中点击“文献”。</p>
<h2>5.2 操作步骤</h2>
<ol>
  <li>选择“文献”模式。</li>
  <li>输入与论文、材料性能、工艺、实验结论相关的问题。</li>
  <li>点击发送。</li>
  <li>等待系统完成检索、重排和生成。</li>
  <li>查看回答中的引用和原文入口。</li>
</ol>
<h2>5.3 预期结果</h2>
<p>系统返回结构化回答，并展示引用文献。用户可点击引用或原文入口核对 PDF。</p>

<h1>6 深度问答</h1>
<h2>6.1 操作入口</h2>
<p>在首页底部模式选择中点击“深度”。</p>
<h2>6.2 适用场景</h2>
<p>深度问答适合复杂分析、技术路线比较、原因归纳和方案建议。该模式通常比文献模式耗时更长。</p>
<h2>6.3 操作步骤</h2>
<ol>
  <li>选择“深度”模式。</li>
  <li>输入问题，并尽量说明目标、约束和期望输出格式。</li>
  <li>点击发送。</li>
  <li>观察阶段进度，等待回答完成。</li>
</ol>

<h1>7 专利问答</h1>
<h2>7.1 操作入口</h2>
<p>在首页底部模式选择中点击“专利”。</p>
<h2>7.2 操作步骤</h2>
<ol>
  <li>选择“专利”模式。</li>
  <li>输入专利号、申请人、材料体系、技术方向或具体问题。</li>
  <li>如需要表格数据，可在问题中说明“读取专利表格”。</li>
  <li>点击发送。</li>
  <li>查看专利引用、图谱分析、tables 和原文入口。</li>
</ol>
<h2>7.3 预期结果</h2>
<p>系统返回专利相关回答，并可提供专利原文、结构化表格或图谱增强信息。</p>

<h1>8 文件问答</h1>
<h2>8.1 上传文件</h2>
<ol>
  <li>在问答首页点击上传按钮。</li>
  <li>选择 PDF、Excel 或 CSV 文件。</li>
  <li>等待上传完成，文件出现在会话文件列表中。</li>
  <li>勾选需要参与本轮问答的文件。</li>
  <li>输入问题并发送。</li>
</ol>
<h2>8.2 预期结果</h2>
<p>系统会结合选中的文件回答问题。若没有勾选文件，则系统按普通知识库问答处理。</p>
<h2>8.3 注意事项</h2>
<ul>
  <li>上传过程中不要刷新页面。</li>
  <li>如果回答与文件无关，先检查本轮是否勾选了正确文件。</li>
  <li>Excel 和 CSV 适合表格统计、字段解释和对比分析。</li>
</ul>

<h1>9 管理后台操作说明</h1>
<h2>9.1 用户管理</h2>
<ol>
  <li>管理员登录后进入 <code>/admin</code>。</li>
  <li>切换到用户管理页签。</li>
  <li>可新增用户、停用用户、重置密码、修改用户类型或绑定人员。</li>
  <li>操作完成后，页面刷新列表并显示结果。</li>
</ol>
<h2>9.2 部门管理</h2>
<p>管理员可维护一级、二级、三级部门。系统初始包含“电池材料技术研究中心”及其下属部门。</p>
<h2>9.3 人员管理</h2>
<p>管理员维护工号、姓名、校验码和部门。普通用户注册或绑定人员信息时，会使用这些记录进行校验。</p>
<h2>9.4 配额管理</h2>
<p>管理员可配置普通问答、文件问答、查看原文和文档辅助配额。当用户配额不足时，页面会提示用户联系管理员。</p>

<h1>10 常见问题</h1>
<table>
  <tr><th>问题</th><th>处理方法</th></tr>
  <tr><td>登录失败怎么办？</td><td>检查用户名和密码；若账号停用或忘记密码，请联系管理员。</td></tr>
  <tr><td>注册提示人员信息不匹配？</td><td>联系管理员确认工号、姓名和校验码是否正确。</td></tr>
  <tr><td>为什么登录后跳到个人中心？</td><td>说明需要完成首次登录设置、修改密码、安全问题或人员绑定。</td></tr>
  <tr><td>问答提示配额不足？</td><td>联系管理员调整配额，或等待配额周期刷新。</td></tr>
  <tr><td>原文打不开？</td><td>稍后重试；仍失败时联系运维检查对象存储。</td></tr>
  <tr><td>回答较慢？</td><td>深度问答、专利图谱和大模型生成可能耗时较长，可缩小问题范围。</td></tr>
</table>
"""

OPERATIONS_MANUAL_FINAL = """
<h1>1 系统及资源</h1>
<h2>1.1 系统信息</h2>
<table>
  <tr><th>项目</th><th>说明</th></tr>
  <tr><td>系统名称</td><td>LiFeO4Agent</td></tr>
  <tr><td>系统版本</td><td>V1.0</td></tr>
  <tr><td>业务描述</td><td>面向电池材料研发的文献、深度、专利和文件智能问答系统。</td></tr>
  <tr><td>运维对象</td><td>Docker 容器、MySQL、Redis、MinIO、Neo4j、证书、配置和数据包。</td></tr>
</table>

<h2>1.2 系统架构</h2>
<div class="diagram">
  <div class="diagram-title">图 1 运维拓扑图</div>
  <pre class="mermaid">flowchart TB
  subgraph HOST[部署服务器]
    DIR[部署目录<br/>deploy/.env / deploy/data / deploy/certs]
    EDGE[edge nginx]
    FRONT[frontend nginx]
    GW[gateway]
    PS[public-service]
    FQ[fastQA]
    HT[highThinkingQA]
    PT[patentQA]
    MYSQL[(mysql_data)]
    REDIS[(redis_data)]
    MINIO[(minio_data)]
    REF[(reference data volumes)]
    NEO[(neo4j data volumes)]
  end
  USER[内网用户浏览器] --> EDGE
  EDGE --> FRONT --> GW
  GW --> PS
  GW --> FQ
  GW --> HT
  GW --> PT
  PS --> MYSQL
  PS --> REDIS
  PS --> MINIO
  FQ --> REF
  HT --> REF
  PT --> REF
  FQ --> NEO
  PT --> NEO
  DIR --> MINIO
  DIR --> REF
  DIR --> NEO</pre>
</div>

<h2>1.3 IP 和网络端口</h2>
<table>
  <tr><th>端口变量</th><th>默认用途</th><th>访问方式</th><th>说明</th></tr>
  <tr><td><code>HTTPS_PUBLISH_PORT</code></td><td>HTTPS 入口</td><td>浏览器访问</td><td>对最终用户开放。</td></tr>
  <tr><td><code>HTTP_PUBLISH_PORT</code></td><td>HTTP 跳转</td><td>浏览器访问</td><td>跳转到 HTTPS。</td></tr>
  <tr><td><code>MYSQL_PUBLISH_PORT</code></td><td>MySQL</td><td>运维网段</td><td>按安全策略决定是否开放。</td></tr>
  <tr><td><code>REDIS_PUBLISH_PORT</code></td><td>Redis</td><td>运维网段</td><td>按安全策略决定是否开放。</td></tr>
  <tr><td><code>MINIO_API_PUBLISH_PORT</code></td><td>MinIO API</td><td>运维或服务访问</td><td>对象存储 API。</td></tr>
  <tr><td><code>MINIO_CONSOLE_PUBLISH_PORT</code></td><td>MinIO 控制台</td><td>运维访问</td><td>建议限制来源。</td></tr>
</table>

<h2>1.4 用户权限分类</h2>
<table>
  <tr><th>角色</th><th>权限</th><th>添加方法</th></tr>
  <tr><td>管理员</td><td>管理用户、部门、人员、配额，可查看管理后台。</td><td>bootstrap 管理员创建后，可在后台新增管理员。</td></tr>
  <tr><td>普通用户</td><td>使用问答、上传文件、查看原文、维护个人信息。</td><td>自助注册或管理员创建。</td></tr>
  <tr><td>运维人员</td><td>服务器、Docker、证书、备份和日志操作。</td><td>由部署方在服务器权限体系中授权。</td></tr>
</table>

<h1>2 日常巡检</h1>
<h2>2.1 服务器巡检</h2>
<table>
  <tr><th>检查项</th><th>命令</th><th>建议阈值</th></tr>
  <tr><td>CPU</td><td><code>top</code> 或 <code>htop</code></td><td>长期高于 80% 需分析。</td></tr>
  <tr><td>内存</td><td><code>free -h</code></td><td>可用内存过低需排查容器。</td></tr>
  <tr><td>磁盘</td><td><code>df -h</code></td><td>使用率超过 80% 预警，超过 90% 处理。</td></tr>
  <tr><td>Docker 空间</td><td><code>docker system df</code></td><td>关注镜像、volume 和 build cache。</td></tr>
  <tr><td>容器状态</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</code></td><td>长期服务 running/healthy，seed job Exited (0)。</td></tr>
</table>

<h2>2.2 功能巡检</h2>
<ol>
  <li>访问 HTTPS 首页，确认登录页正常加载。</li>
  <li>使用管理员账号登录，确认管理后台可打开。</li>
  <li>使用普通用户发起文献问答。</li>
  <li>发起专利问答并打开一个原文入口。</li>
  <li>检查 MinIO 控制台 bucket 对象是否存在。</li>
  <li>检查 Neo4j 容器 healthcheck 是否正常。</li>
</ol>

<h2>2.3 日志巡检</h2>
<table>
  <tr><th>服务</th><th>日志命令</th><th>关注关键字</th></tr>
  <tr><td>gateway</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 gateway</code></td><td>quota、route、timeout、5xx。</td></tr>
  <tr><td>public-service</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 public-service</code></td><td>auth、mysql、quota、minio。</td></tr>
  <tr><td>fastQA</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 fastqa</code></td><td>embedding、rerank、LLM、chroma。</td></tr>
  <tr><td>highThinkingQA</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 highthinkingqa</code></td><td>embedding、LLM、stage。</td></tr>
  <tr><td>patentQA</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs --tail=200 patent</code></td><td>intent、rerank、graph、tables。</td></tr>
  <tr><td>seed job</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs minio-seed</code></td><td>package not found、sha256、marker。</td></tr>
</table>

<h1>3 系统使用运维</h1>
<h2>3.1 资源管理</h2>
<p>reference data 由数据包导入，运行时不应手工修改对应 named volume。用户上传文件和会话数据属于运行态数据，应纳入备份。MinIO 中初始原文可重建，但运行期新增对象需要单独保护。</p>
<h2>3.2 缓存管理</h2>
<p>Redis 用于缓存和任务状态。清理 Redis 可能影响正在进行的任务和会话状态，不建议在业务高峰期执行。若必须清理，应先停止业务服务或确认没有正在执行的问答任务。</p>
<h2>3.3 定时任务管理</h2>
<p>当前 V1.0 交付主要依赖容器服务和用户触发请求，不默认要求宿主机 cron 任务。若部署方自行增加备份 cron，应记录脚本路径、执行用户、执行时间和保留策略。</p>

<h1>4 系统启停运维</h1>
<h2>4.1 前置事项确认</h2>
<ol>
  <li>确认 Docker 服务运行。</li>
  <li>确认 <code>deploy/.env</code> 存在且未保留占位值。</li>
  <li>确认 <code>deploy/data/manifest.json</code> 和数据包存在。</li>
  <li>确认 <code>deploy/certs</code> 下证书和私钥存在。</li>
  <li>执行 preflight 检查。</li>
</ol>

<h2>4.2 启动步骤</h2>
<pre>bash deploy/scripts/preflight_check.sh deploy/.env
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d
docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</pre>
<p>启动顺序由 compose 依赖控制：MySQL、Redis、MinIO 先启动；MinIO 和 reference/Neo4j seed 完成后业务服务启动；最后 edge 对外提供 HTTPS。</p>

<h2>4.3 停止步骤</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml down</pre>
<p>该命令停止并删除容器，但不会删除 named volume。不要在生产环境随意执行 <code>docker compose down -v</code>，该命令会删除数据卷。</p>

<h2>4.4 重启单个服务</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml restart fastqa</pre>
<p>适用于修改模型配置、单服务镜像更新或排障后重启。</p>

<h1>5 系统备份恢复方案</h1>
<h2>5.1 日常备份</h2>
<table>
  <tr><th>备份对象</th><th>频率建议</th><th>保留建议</th><th>说明</th></tr>
  <tr><td>MySQL</td><td>每日</td><td>按客户制度</td><td>用户、会话、配额等核心业务数据。</td></tr>
  <tr><td>MinIO 运行期对象</td><td>每日或按增量</td><td>按客户制度</td><td>初始原文可重建，用户上传对象需备份。</td></tr>
  <tr><td><code>deploy/.env</code></td><td>每次变更</td><td>保留最近多个版本</td><td>包含密钥，应加密保存。</td></tr>
  <tr><td>证书和私钥</td><td>每次变更</td><td>保留有效版本</td><td>私钥需严格限制权限。</td></tr>
  <tr><td>数据包和镜像包</td><td>每次交付</td><td>至少保留当前和上一版本</td><td>用于重建和回滚。</td></tr>
</table>

<h2>5.2 部署前备份</h2>
<ol>
  <li>备份当前 <code>deploy</code> 目录。</li>
  <li>导出 MySQL 数据库。</li>
  <li>记录当前镜像 tag 和数据包版本。</li>
  <li>确认回滚镜像和旧数据包可用。</li>
</ol>

<h2>5.3 整体恢复</h2>
<ol>
  <li>停止当前 compose 服务。</li>
  <li>恢复 <code>deploy/.env</code>、证书、镜像包和数据包。</li>
  <li>按需恢复 MySQL 备份。</li>
  <li>执行 preflight。</li>
  <li>启动 compose，并做登录和三类问答验证。</li>
</ol>

<h2>5.4 应用程序回滚</h2>
<p>若只更新了某个服务镜像，可重新加载上一版本镜像并重启对应服务。若涉及数据库 schema 或数据包变化，应先评估是否需要恢复数据库或强制重导数据。</p>

<h1>6 故障处理</h1>
<table>
  <tr><th>故障</th><th>定位步骤</th><th>处理建议</th></tr>
  <tr><td>页面打不开</td><td>检查域名、端口、edge 和 frontend 日志。</td><td>修复 DNS、证书或端口映射。</td></tr>
  <tr><td>登录失败</td><td>检查 public-service、MySQL、用户状态。</td><td>重置密码或启用账号。</td></tr>
  <tr><td>问答失败</td><td>先看 gateway，再看对应 QA 后端。</td><td>检查模型、向量库、MinIO 和 Neo4j。</td></tr>
  <tr><td>原文失败</td><td>检查 MinIO bucket、对象路径和 minio-seed。</td><td>补齐数据包或重新导入。</td></tr>
  <tr><td>图谱失败</td><td>检查 Neo4j seed 和 healthcheck。</td><td>重新加载 dump 或恢复 volume。</td></tr>
</table>
"""

DEPLOYMENT_MANUAL_FINAL += """

<h1>12 数据包资源清单</h1>
<p>部署目录中的 <code>deploy/data/manifest.json</code> 是数据包验收依据。V1.0 数据版本为 <code>2026-05-19</code>，各数据包由 seed job 自动导入，部署人员不需要手工解压。</p>
<table>
  <tr><th>数据包</th><th>文件名</th><th>大小</th><th>关键内容</th><th>导入目标</th></tr>
  <tr><td>MinIO 原文</td><td><code>minio-originals.tar.zst</code></td><td>约 49.3 GiB</td><td>论文 7153 篇、专利目录 14006 个、专利 tables 9581 个。</td><td>MinIO bucket。</td></tr>
  <tr><td>fastQA reference</td><td><code>fastqa-ref.tar.zst</code></td><td>约 4.09 GiB</td><td>文献主向量库、MD 向量库和索引文件。</td><td><code>fastqa_ref_data</code> volume。</td></tr>
  <tr><td>highThinking reference</td><td><code>highthinking-ref.tar.zst</code></td><td>约 0.96 GiB</td><td>深度问答 vectordb。</td><td><code>highthinking_ref_data</code> volume。</td></tr>
  <tr><td>patentQA reference</td><td><code>patentqa-ref.tar.zst</code></td><td>约 1.89 GiB</td><td>两个专利向量库、JSON-only patent archive，不含 PDF/PNG 原文。</td><td><code>patentqa_ref_data</code> volume。</td></tr>
  <tr><td>public-service reference</td><td><code>public-service-ref.tar.zst</code></td><td>约 10 KiB</td><td>公共服务轻量 vector database。</td><td><code>public_service_ref_data</code> volume。</td></tr>
  <tr><td>文献图谱</td><td><code>neo4j-literature.dump.zst</code></td><td>约 175 MiB</td><td>文献知识图谱 dump。</td><td><code>neo4j_literature_data</code> volume。</td></tr>
  <tr><td>专利图谱</td><td><code>neo4j-patent.dump.zst</code></td><td>约 462 MiB</td><td>专利知识图谱 dump。</td><td><code>neo4j_patent_data</code> volume。</td></tr>
</table>

<h1>13 部署前检查清单</h1>
<table>
  <tr><th>序号</th><th>检查项</th><th>通过标准</th><th>失败处理</th></tr>
  <tr><td class="center">1</td><td>Docker 服务</td><td><code>docker version</code> 正常返回。</td><td>启动 Docker 或联系系统管理员。</td></tr>
  <tr><td class="center">2</td><td>Compose 命令</td><td><code>docker compose version</code> 正常返回。</td><td>安装或升级 Compose v2。</td></tr>
  <tr><td class="center">3</td><td>磁盘空间</td><td>Docker 数据目录和部署目录空间满足数据导入要求。</td><td>扩容或迁移 Docker 数据目录。</td></tr>
  <tr><td class="center">4</td><td>端口占用</td><td>HTTPS、HTTP、MySQL、Redis、MinIO 端口未冲突。</td><td>修改 <code>deploy/.env</code> 发布端口。</td></tr>
  <tr><td class="center">5</td><td>证书文件</td><td><code>fullchain.pem</code> 和 <code>privkey.pem</code> 存在。</td><td>由客户证书体系签发或使用内网自签证书。</td></tr>
  <tr><td class="center">6</td><td>数据包</td><td>manifest 和所有 <code>tar.zst</code>/<code>dump.zst</code> 文件存在。</td><td>重新传输数据包。</td></tr>
  <tr><td class="center">7</td><td>模型连通</td><td>部署机或容器可访问 LLM、embedding、rerank、intent 服务。</td><td>检查内网路由、防火墙和模型网关。</td></tr>
</table>

<h1>14 上线验证记录表</h1>
<table>
  <tr><th>验证项</th><th>命令或操作</th><th>成功结果示例</th><th>异常结果示例</th></tr>
  <tr><td>Compose 展开</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml config --images</code></td><td>列出 <code>lifeo4agent/gateway</code>、<code>lifeo4agent/frontend</code> 等镜像。</td><td>提示变量未定义或 YAML 语法错误。</td></tr>
  <tr><td>容器状态</td><td><code>docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps</code></td><td>长期服务 <code>Up</code>，seed job <code>Exited (0)</code>。</td><td>容器 <code>Restarting</code> 或 seed job 退出码非 0。</td></tr>
  <tr><td>HTTPS 首页</td><td><code>curl -k -I https://域名:端口/</code></td><td>返回 <code>HTTP/2 200</code> 或 <code>HTTP/1.1 200</code>。</td><td>连接失败、证书域名不匹配、502。</td></tr>
  <tr><td>网关健康</td><td><code>curl -k https://域名:端口/healthz</code></td><td>返回健康状态。</td><td>404 或 502，需检查 nginx 路由。</td></tr>
  <tr><td>MinIO 对象</td><td>登录 MinIO 控制台检查 bucket。</td><td>存在 <code>papers/</code> 和 <code>patent/originals/</code>。</td><td>bucket 为空或 tables 缺失。</td></tr>
  <tr><td>管理员登录</td><td>浏览器登录 <code>admin</code>。</td><td>进入管理后台或首次安全设置页。</td><td>账号不存在，检查 MySQL 初始化日志。</td></tr>
  <tr><td>三类问答</td><td>分别发起文献、深度、专利问题。</td><td>返回答案、阶段耗时和引用。</td><td>模型 400、向量库路径错误或配额失败。</td></tr>
</table>

<h1>15 部署变更记录</h1>
<p>每次上线或更新后，应在现场交付记录中补充以下内容，便于后续回滚和审计。</p>
<table>
  <tr><th>字段</th><th>填写说明</th></tr>
  <tr><td>变更日期</td><td>记录实际部署日期和时间窗口。</td></tr>
  <tr><td>变更内容</td><td>记录更新的镜像、数据包、配置或证书。</td></tr>
  <tr><td>执行人员</td><td>记录部署方和实施方人员。</td></tr>
  <tr><td>验证结果</td><td>记录健康检查、登录、问答和原文验证结果。</td></tr>
  <tr><td>回滚材料</td><td>确认上一版本镜像、配置和数据库备份是否可用。</td></tr>
</table>
"""

OPERATIONS_MANUAL_FINAL += """

<h1>7 总则</h1>
<h2>7.1 运维目标</h2>
<p>LiFeO4Agent 运维工作以“服务可访问、数据可恢复、问题可定位、变更可回滚”为目标。运维人员应重点关注容器健康、磁盘容量、MySQL 运行态数据、MinIO 对象、模型服务连通性和证书有效期。</p>
<h2>7.2 运维边界</h2>
<table>
  <tr><th>对象</th><th>是否由本系统维护</th><th>说明</th></tr>
  <tr><td>业务容器和 compose 编排</td><td>是</td><td>由部署目录中的 compose 文件管理。</td></tr>
  <tr><td>MySQL、Redis、MinIO、Neo4j 容器</td><td>是</td><td>V1.0 内置容器，生产策略可按客户规范替换。</td></tr>
  <tr><td>大模型、embedding、rerank、intent 服务</td><td>否</td><td>由部署方模型平台提供，本系统通过配置连接。</td></tr>
  <tr><td>内网 DNS 和证书信任链</td><td>否</td><td>由客户基础设施维护。</td></tr>
  <tr><td>服务器硬件和操作系统</td><td>否</td><td>由客户基础设施或运维团队维护。</td></tr>
</table>

<h1>8 系统软件与目录</h1>
<h2>8.1 容器服务清单</h2>
<table>
  <tr><th>服务</th><th>类型</th><th>主要职责</th><th>异常影响</th></tr>
  <tr><td><code>edge</code></td><td>入口</td><td>HTTPS 终止、HTTP 跳转、代理 frontend。</td><td>用户无法访问页面。</td></tr>
  <tr><td><code>frontend</code></td><td>前端</td><td>提供静态页面和前端路由。</td><td>页面 404 或资源加载失败。</td></tr>
  <tr><td><code>gateway</code></td><td>接入后端</td><td>统一 API、SSE 代理、配额协调。</td><td>所有业务请求失败。</td></tr>
  <tr><td><code>public-service</code></td><td>公共服务</td><td>用户、会话、文件、配额、原文代理。</td><td>登录、管理和文件能力失败。</td></tr>
  <tr><td><code>fastqa</code></td><td>问答后端</td><td>文献问答。</td><td>文献模式不可用。</td></tr>
  <tr><td><code>highthinkingqa</code></td><td>问答后端</td><td>深度问答。</td><td>深度模式不可用。</td></tr>
  <tr><td><code>patent</code></td><td>问答后端</td><td>专利问答。</td><td>专利模式不可用。</td></tr>
  <tr><td><code>mysql</code></td><td>数据库</td><td>用户态业务数据。</td><td>登录、会话和管理功能失败。</td></tr>
  <tr><td><code>redis</code></td><td>缓存</td><td>缓存、任务和短期状态。</td><td>任务状态和部分缓存异常。</td></tr>
  <tr><td><code>minio</code></td><td>对象存储</td><td>论文、专利和上传文件。</td><td>原文和文件问答失败。</td></tr>
  <tr><td><code>neo4j-literature</code></td><td>图数据库</td><td>文献图谱。</td><td>文献图谱增强不可用。</td></tr>
  <tr><td><code>neo4j-patent</code></td><td>图数据库</td><td>专利图谱。</td><td>专利图谱增强不可用。</td></tr>
</table>

<h2>8.2 目录和数据卷</h2>
<table>
  <tr><th>对象</th><th>用途</th><th>运维建议</th></tr>
  <tr><td><code>deploy/.env</code></td><td>生产配置和密钥。</td><td>变更前备份，严禁公开。</td></tr>
  <tr><td><code>deploy/data</code></td><td>离线数据包和 manifest。</td><td>保留当前版本和上一版本。</td></tr>
  <tr><td><code>deploy/certs</code></td><td>HTTPS 证书和私钥。</td><td>监控有效期，私钥限制权限。</td></tr>
  <tr><td><code>mysql_data</code></td><td>MySQL 数据卷。</td><td>必须定期备份。</td></tr>
  <tr><td><code>minio_data</code></td><td>MinIO 对象数据卷。</td><td>运行期上传对象应备份。</td></tr>
  <tr><td><code>*_ref_data</code></td><td>向量库和 reference 数据。</td><td>可由数据包重建，通常不手工备份。</td></tr>
  <tr><td><code>neo4j_*_data</code></td><td>图谱数据。</td><td>可由 dump 重建，生产变更后按需备份。</td></tr>
</table>

<h1>9 深度巡检</h1>
<h2>9.1 数据库巡检</h2>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml exec mysql mysqladmin ping -uroot -p</pre>
<p>成功结果示例：<code>mysqld is alive</code>。若返回认证失败，应检查 <code>MYSQL_ROOT_PASSWORD</code> 是否与初始化时一致；若容器不可连接，应先检查容器健康和磁盘空间。</p>
<h2>9.2 MinIO 巡检</h2>
<p>MinIO 巡检重点为 bucket 是否存在、对象数量是否符合数据包统计、运行期上传文件是否可读。对象缺失时优先检查 <code>minio-seed</code> 日志和 marker。</p>
<table>
  <tr><th>检查项</th><th>正常现象</th><th>异常处理</th></tr>
  <tr><td>bucket</td><td><code>MINIO_BUCKET</code> 存在。</td><td>检查 <code>minio-init</code> 日志。</td></tr>
  <tr><td>论文目录</td><td><code>papers/</code> 下有对象。</td><td>检查 <code>minio-originals.tar.zst</code>。</td></tr>
  <tr><td>专利目录</td><td><code>patent/originals/</code> 下有对象。</td><td>重新执行 MinIO seed。</td></tr>
  <tr><td>tables</td><td>带 tables 的专利有 <code>structured/tables.json</code>。</td><td>检查数据包构建阶段 tables backfill。</td></tr>
</table>
<h2>9.3 模型调用巡检</h2>
<p>模型巡检不直接在宿主机暴露密钥。建议通过三类问答请求观察日志，确认 LLM、intent、embedding、rerank 的调用阶段和耗时是否正常。</p>
<table>
  <tr><th>模型类型</th><th>涉及服务</th><th>日志关注点</th></tr>
  <tr><td>LLM</td><td>fastQA、highThinkingQA、patentQA</td><td>chat completions 请求、stream 输出、400/401/timeout。</td></tr>
  <tr><td>Intent</td><td>fastQA、patentQA</td><td>是否启用、模型名、分类结果和错误。</td></tr>
  <tr><td>Embedding</td><td>fastQA、highThinkingQA、patentQA</td><td>向量化请求是否成功、维度是否匹配。</td></tr>
  <tr><td>Rerank</td><td>fastQA、patentQA</td><td>候选数量、排序结果、provider 是否为 none。</td></tr>
</table>

<h1>10 备份脚本示例</h1>
<p>以下命令为运维记录模板，执行前应根据现场账号、路径和安全规范调整。</p>
<pre>docker compose --env-file deploy/.env -f deploy/docker-compose.yml exec mysql \
  mysqldump -uroot -p agentcode &gt; backup-agentcode.sql</pre>
<p>成功结果示例：生成 <code>backup-agentcode.sql</code>，文件大小大于 0。失败结果示例：<code>Access denied for user</code>，应检查密码或执行用户。</p>
<pre>tar -czf deploy-config-backup.tgz deploy/.env deploy/certs deploy/docker-compose.yml</pre>
<p>成功结果示例：生成配置备份包。该备份包含敏感信息，必须加密保存并限制访问。</p>

<h1>11 应急处置流程</h1>
<div class="diagram">
  <div class="diagram-title">图 2 故障处置泳道图</div>
  <pre class="mermaid">sequenceDiagram
  participant U as 用户或值班人员
  participant OPS as 运维人员
  participant LOG as 日志与监控
  participant DEV as 开发支持
  U->>OPS: 报告页面、登录或问答异常
  OPS->>LOG: 检查 compose ps 和相关服务日志
  alt 配置或资源问题
    OPS->>OPS: 修复端口、证书、密码、磁盘或数据包
    OPS->>U: 回告恢复结果
  else 业务代码或数据问题
    OPS->>DEV: 提供请求时间、用户、接口、日志和复现步骤
    DEV->>OPS: 给出修复镜像、配置或数据处理方案
    OPS->>U: 验证并回告结果
  end</pre>
</div>
"""

USER_MANUAL_FINAL += """

<h1>11 会话管理</h1>
<h2>11.1 新建会话</h2>
<ol>
  <li>在左侧会话栏点击“新建会话”。</li>
  <li>系统创建空会话，并切换到该会话。</li>
  <li>选择问答模式，输入问题后发送。</li>
</ol>
<p>预期结果：新会话显示在会话列表中，第一条问题发送后会话标题自动生成或可手动修改。</p>
<h2>11.2 切换和删除会话</h2>
<table>
  <tr><th>操作</th><th>步骤</th><th>预期结果</th></tr>
  <tr><td>切换会话</td><td>点击左侧历史会话。</td><td>中间区域加载该会话消息和文件。</td></tr>
  <tr><td>修改标题</td><td>点击标题编辑入口，输入新标题。</td><td>会话列表显示新标题。</td></tr>
  <tr><td>删除会话</td><td>点击删除并确认。</td><td>会话从列表移除，历史消息不可再查看。</td></tr>
  <tr><td>查看文件</td><td>展开会话文件区域。</td><td>显示该会话上传的 PDF、Excel 或 CSV。</td></tr>
</table>

<h1>12 阶段进度和引用查看</h1>
<p>问答过程中，页面会展示阶段进度和耗时。不同模式展示的阶段略有差异，常见阶段包括意图识别、查询扩展、向量检索、图谱查询、重排、答案生成和引用整理。</p>
<div class="diagram">
  <div class="diagram-title">图 3 问答阶段展示流程</div>
  <pre class="mermaid">flowchart LR
  A[发送问题] --> B[意图识别]
  B --> C[检索知识库]
  C --> D[重排候选]
  D --> E[图谱或表格增强]
  E --> F[答案生成]
  F --> G[引用和原文入口]
  G --> H[回答完成]</pre>
</div>
<table>
  <tr><th>页面元素</th><th>含义</th><th>用户操作</th></tr>
  <tr><td>阶段名称</td><td>当前正在执行的处理步骤。</td><td>一般无需操作，可用于判断耗时来源。</td></tr>
  <tr><td>阶段耗时</td><td>该步骤使用的时间。</td><td>若长期卡住，可刷新或联系管理员。</td></tr>
  <tr><td>引用卡片</td><td>回答使用的论文、专利或文件片段。</td><td>点击查看来源详情。</td></tr>
  <tr><td>原文按钮</td><td>打开论文或专利 PDF。</td><td>用于核对出处。</td></tr>
  <tr><td>错误提示</td><td>本次问答失败原因。</td><td>按提示重试或联系管理员。</td></tr>
</table>

<h1>13 原文查看</h1>
<h2>13.1 论文原文</h2>
<ol>
  <li>在回答引用中找到论文引用。</li>
  <li>点击“查看原文”或 PDF 入口。</li>
  <li>浏览器打开 PDF 预览或下载。</li>
</ol>
<h2>13.2 专利原文和 tables</h2>
<ol>
  <li>在专利回答中查看专利引用。</li>
  <li>点击专利原文入口查看 PDF 或图片。</li>
  <li>如回答中展示结构化表格，可根据表格标题和字段核对专利 tables。</li>
</ol>
<p>原文打不开通常不是账号问题，可能是对象存储正在导入、对象路径缺失或浏览器阻止弹窗。用户可先重新登录再试，仍失败时联系管理员。</p>

<h1>14 管理员详细操作</h1>
<h2>14.1 新增用户</h2>
<ol>
  <li>进入管理后台，选择“用户管理”。</li>
  <li>点击新增用户，填写用户名、用户类型、初始密码和人员绑定信息。</li>
  <li>保存后在列表中确认用户状态为启用。</li>
  <li>通知用户首次登录后修改密码和设置安全问题。</li>
</ol>
<h2>14.2 批量导入人员</h2>
<ol>
  <li>进入“人员管理”。</li>
  <li>点击下载导入模板。</li>
  <li>按模板填写工号、姓名、部门和校验码。</li>
  <li>上传模板文件。</li>
  <li>查看导入结果，处理失败行。</li>
</ol>
<h2>14.3 配额调整</h2>
<ol>
  <li>进入管理后台的配额页签。</li>
  <li>查看系统默认配额和用户当前用量。</li>
  <li>修改普通问答、文件问答、查看原文或文档辅助配额。</li>
  <li>如某个用户需要立即恢复额度，使用用户配额重置功能。</li>
</ol>
<div class="diagram">
  <div class="diagram-title">图 4 管理员配额处理流程</div>
  <pre class="mermaid">flowchart TB
  A[用户反馈配额不足] --> B[管理员打开配额管理]
  B --> C{是否调整全局默认}
  C -- 是 --> D[修改 quota config]
  C -- 否 --> E[查询用户用量]
  E --> F[重置用户指定配额]
  D --> G[保存并通知用户]
  F --> G</pre>
</div>

<h1>15 用户问题建议写法</h1>
<table>
  <tr><th>模式</th><th>推荐写法</th><th>说明</th></tr>
  <tr><td>文献</td><td>“请总结磷酸铁锂低温性能提升相关文献的主要方法，并列出引用。”</td><td>适合查论文结论和引用。</td></tr>
  <tr><td>深度</td><td>“请从材料、工艺和电芯设计角度分析该问题，并给出优先级建议。”</td><td>适合复杂分析。</td></tr>
  <tr><td>专利</td><td>“检索磷酸铁锂包覆改性相关专利，关注申请人、技术路线和表格数据。”</td><td>适合专利检索和对比。</td></tr>
  <tr><td>文件</td><td>“基于我上传的 Excel，统计不同样品的容量保持率并解释异常值。”</td><td>适合用户自带文件分析。</td></tr>
</table>
"""

SUMMARY_DESIGN_FINAL += """

<h1>10 数据流设计</h1>
<div class="diagram">
  <div class="diagram-title">图 6 主要数据流图</div>
  <pre class="mermaid">flowchart LR
  U[用户] --> FE[前端]
  FE --> GW[gateway]
  GW --> PS[public-service]
  GW --> QA[QA 后端]
  PS --> DB[(MySQL)]
  PS --> OBJ[(MinIO)]
  QA --> VEC[(Chroma 向量库)]
  QA --> KG[(Neo4j 图谱)]
  QA --> OBJ
  QA --> MODEL[LLM/Embedding/Rerank/Intent]
  MODEL --> QA
  QA --> GW
  GW --> FE
  FE --> U</pre>
</div>
<table>
  <tr><th>数据类型</th><th>产生方</th><th>存储位置</th><th>生命周期</th></tr>
  <tr><td>账号、部门、人员、配额</td><td>管理员或初始化脚本</td><td>MySQL</td><td>运行态业务数据，需备份。</td></tr>
  <tr><td>会话和消息</td><td>用户问答</td><td>MySQL</td><td>运行态业务数据，按客户制度保留。</td></tr>
  <tr><td>上传文件</td><td>用户</td><td>MinIO + MySQL 元数据</td><td>运行态数据，需备份。</td></tr>
  <tr><td>论文和专利原文</td><td>数据包 seed</td><td>MinIO</td><td>可由数据包重建。</td></tr>
  <tr><td>向量库和图谱</td><td>数据包 seed</td><td>named volume</td><td>可由数据包重建。</td></tr>
  <tr><td>模型调用日志</td><td>QA 后端</td><td>Docker 日志</td><td>用于排障，不应包含密钥。</td></tr>
</table>

<h1>11 安全架构</h1>
<table>
  <tr><th>安全域</th><th>设计</th><th>说明</th></tr>
  <tr><td>传输安全</td><td>edge nginx 提供 TLS。</td><td>证书由部署方签发或自签，客户端需信任。</td></tr>
  <tr><td>身份认证</td><td>用户名密码 + JWT。</td><td>token 由 gateway 和 public-service 校验。</td></tr>
  <tr><td>权限控制</td><td>普通用户和管理员角色。</td><td>管理员接口需要管理员权限。</td></tr>
  <tr><td>内部调用</td><td>内部 token。</td><td>gateway 与 public-service 内部接口使用内部鉴权。</td></tr>
  <tr><td>密钥治理</td><td>密钥只写入 <code>deploy/.env</code>。</td><td>文档和镜像上下文不包含真实密钥。</td></tr>
  <tr><td>数据隔离</td><td>MinIO bucket、MySQL 用户、Docker 网络。</td><td>内部服务通过 compose service name 访问。</td></tr>
</table>

<h1>12 可扩展性设计</h1>
<p>系统通过服务拆分和数据包分层支持后续扩展。新增问答模式时，应优先在 gateway 中增加模式路由，在独立 QA 后端中实现业务能力，并复用 public-service 的用户、会话、文件和配额能力。新增大规模数据时，应使用数据包和 seed job 交付，不应把原始数据打入业务镜像。</p>
<table>
  <tr><th>扩展方向</th><th>推荐做法</th></tr>
  <tr><td>单服务代码更新</td><td>只构建并交付对应服务镜像，例如 <code>lifeo4agent/fastqa</code>。</td></tr>
  <tr><td>新增向量库</td><td>新增独立 reference data 包和 named volume。</td></tr>
  <tr><td>新增图谱</td><td>新增 Neo4j dump 包和独立 Neo4j 服务或数据库。</td></tr>
  <tr><td>替换模型服务</td><td>只修改 <code>deploy/.env</code> 中 base url、模型名和 key。</td></tr>
  <tr><td>高可用改造</td><td>将内置 MySQL、Redis、MinIO 替换为客户已有高可用中间件。</td></tr>
</table>
"""

DETAILED_DESIGN_FINAL += """

<h1>9 文献问答模块设计</h1>
<h2>9.1 功能描述</h2>
<p>文献问答模块由 fastQA 后端提供，面向论文知识库进行查询理解、向量检索、候选重排、图谱增强、答案生成和引用整理。该模块依赖 <code>fastqa_ref_data</code> 中的 Chroma 向量库和 MinIO 中的论文原文。</p>
<h2>9.2 前端页面</h2>
<p>用户在问答首页选择“文献”模式后输入问题。页面展示阶段进度、耗时、答案、引用和论文原文入口。阶段事件可包含 intent、检索、rerank、生成等步骤。</p>
<h2>9.3 库表设计</h2>
<table>
  <tr><th>对象</th><th>字段或路径</th><th>说明</th></tr>
  <tr><td>会话消息</td><td><code>conversation_messages</code></td><td>保存用户问题、助手回答和任务状态。</td></tr>
  <tr><td>文件关联</td><td><code>conversation_files</code></td><td>保存本轮可用文件上下文。</td></tr>
  <tr><td>向量库</td><td><code>fastqa_ref_data</code></td><td>包含主文献向量库和 MD 向量库。</td></tr>
  <tr><td>原文对象</td><td><code>papers/</code></td><td>MinIO 中的论文 PDF 权威副本。</td></tr>
</table>
<h2>9.4 重点逻辑</h2>
<pre>resolve_intent(question)
build_embedding(question)
retrieve_candidates(vectordb, top_k)
rerank_candidates(question, candidates)
optional_graph_context(question)
generate_answer(question, evidence)
return citations and original links</pre>
<h2>9.5 处理流程</h2>
<div class="diagram">
  <div class="diagram-title">图 3 文献问答处理流程</div>
  <pre class="mermaid">flowchart LR
  A[用户问题] --> B[意图识别]
  B --> C[Embedding]
  C --> D[Chroma 检索]
  D --> E[Rerank]
  E --> F[文献图谱增强]
  F --> G[LLM 生成]
  G --> H[引用和原文入口]</pre>
</div>
<h2>9.6 接口说明</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>输入</th><th>输出</th></tr>
  <tr><td><code>/api/fast/ask</code>、<code>/api/v1/fast/ask</code></td><td>POST</td><td>问题、会话、文件选择。</td><td>同步回答。</td></tr>
  <tr><td><code>/api/fast/ask_stream</code>、<code>/api/v1/fast/ask_stream</code></td><td>POST</td><td>问题、会话、文件选择。</td><td>SSE 阶段和答案。</td></tr>
  <tr><td><code>/api/view_pdf/{doi}</code></td><td>GET/HEAD</td><td>DOI 或原文标识。</td><td>PDF 响应。</td></tr>
  <tr><td><code>/api/reference_preview</code></td><td>GET/POST</td><td>引用标识。</td><td>引用预览信息。</td></tr>
</table>
<h2>9.7 异常处理设计</h2>
<table>
  <tr><th>异常</th><th>处理</th><th>用户提示</th></tr>
  <tr><td>向量库未加载</td><td>记录路径和 collection 信息。</td><td>知识库暂不可用，请联系管理员。</td></tr>
  <tr><td>rerank 服务失败</td><td>按配置降级为原检索排序或返回错误。</td><td>检索重排异常，请稍后重试。</td></tr>
  <tr><td>论文原文缺失</td><td>记录 MinIO key。</td><td>原文暂不可用。</td></tr>
</table>

<h1>10 深度问答模块设计</h1>
<h2>10.1 功能描述</h2>
<p>深度问答模块由 highThinkingQA 提供，适合复杂问题的分解、规划、检索、子问题回答和综合生成。该模块依赖独立 <code>highthinking_ref_data</code> 向量库，并通过 LLM 完成多阶段推理。</p>
<h2>10.2 前端页面</h2>
<p>用户选择“深度”模式后提交问题。页面应允许长时间流式输出，展示规划、检索、综合等阶段，避免用户误判为卡死。</p>
<h2>10.3 重点逻辑</h2>
<pre>stage1_plan(question)
stage2_generate_queries(plan)
retrieve_context(queries)
synthesize_answer(question, plan, context)
stream_steps_and_final_answer()</pre>
<h2>10.4 处理流程</h2>
<div class="diagram">
  <div class="diagram-title">图 4 深度问答处理流程</div>
  <pre class="mermaid">sequenceDiagram
  participant FE as 前端
  participant GW as gateway
  participant HT as highThinkingQA
  participant V as vectordb
  participant L as LLM
  FE->>GW: POST /api/thinking/ask_stream
  GW->>HT: 转发问题和会话上下文
  HT->>L: 阶段一规划
  HT->>L: 阶段二查询生成
  HT->>V: 多查询检索
  HT->>L: 综合生成
  HT-->>GW: SSE 阶段和回答
  GW-->>FE: 渲染进度和答案</pre>
</div>
<h2>10.5 接口说明</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>说明</th></tr>
  <tr><td><code>/api/thinking/ask</code>、<code>/api/v1/thinking/ask</code></td><td>POST</td><td>深度同步问答。</td></tr>
  <tr><td><code>/api/thinking/ask_stream</code>、<code>/api/v1/thinking/ask_stream</code></td><td>POST</td><td>深度流式问答。</td></tr>
  <tr><td><code>/api/ingest</code>、<code>/api/v1/ingest</code></td><td>POST/GET</td><td>保留的摄取任务接口，生产主要使用离线数据包。</td></tr>
</table>
<h2>10.6 异常处理设计</h2>
<table>
  <tr><th>异常</th><th>处理</th><th>用户提示</th></tr>
  <tr><td>LLM 超时</td><td>终止当前阶段并返回错误事件。</td><td>模型响应超时，请缩小问题范围或稍后重试。</td></tr>
  <tr><td>检索结果为空</td><td>允许模型基于已有上下文说明不足。</td><td>未检索到足够依据。</td></tr>
  <tr><td>SSE 断开</td><td>gateway 记录 task id，任务接口可查询事件。</td><td>连接中断，请刷新查看结果。</td></tr>
</table>

<h1>11 专利问答模块设计</h1>
<h2>11.1 功能描述</h2>
<p>专利问答模块由 patentQA 提供，负责专利意图识别、专利向量检索、JSON archive 读取、structured tables 读取、专利图谱增强、答案生成和专利原文引用。</p>
<h2>11.2 库表和数据设计</h2>
<table>
  <tr><th>对象</th><th>路径或表</th><th>说明</th></tr>
  <tr><td>专利 JSON archive</td><td><code>patentqa_ref_data</code></td><td>14006 个专利 JSON 目录，不含 PDF/PNG。</td></tr>
  <tr><td>专利向量库</td><td><code>patentqa_ref_data</code></td><td>两个 Chroma 向量库。</td></tr>
  <tr><td>专利原文</td><td><code>patent/originals/{id}/</code></td><td>MinIO 中的 PDF、图片、manifest 和 structured tables。</td></tr>
  <tr><td>专利图谱</td><td><code>neo4j-patent</code></td><td>专利知识图谱。</td></tr>
</table>
<h2>11.3 处理流程</h2>
<div class="diagram">
  <div class="diagram-title">图 5 专利问答处理流程</div>
  <pre class="mermaid">flowchart TB
  A[用户专利问题] --> B[Intent 模型识别]
  B --> C[专利向量检索]
  C --> D[读取 JSON archive]
  D --> E{是否需要 tables}
  E -- 是 --> F[读取 structured/tables.json]
  E -- 否 --> G[跳过 tables]
  F --> H[专利图谱查询]
  G --> H
  H --> I[Rerank 和证据整理]
  I --> J[LLM 生成答案]
  J --> K[专利引用和原文入口]</pre>
</div>
<h2>11.4 接口说明</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>输入</th><th>输出</th></tr>
  <tr><td><code>/api/patent/ask</code>、<code>/api/v1/patent/ask</code></td><td>POST</td><td>专利问题、会话。</td><td>同步回答。</td></tr>
  <tr><td><code>/api/patent/ask_stream</code>、<code>/api/v1/patent/ask_stream</code></td><td>POST</td><td>专利问题、会话。</td><td>SSE 阶段和回答。</td></tr>
  <tr><td><code>/api/patent/original/{canonical_patent_id}</code></td><td>GET/HEAD</td><td>规范化专利 ID。</td><td>专利原文或对象响应。</td></tr>
</table>
<h2>11.5 异常处理设计</h2>
<table>
  <tr><th>异常</th><th>处理</th><th>用户提示</th></tr>
  <tr><td>intent 模型不可用</td><td>按默认专利检索策略降级或返回明确错误。</td><td>意图识别异常，已尝试按默认策略处理。</td></tr>
  <tr><td>tables 不存在</td><td>manifest 中 availability.tables 为 false 时正常跳过。</td><td>该专利暂无结构化表格。</td></tr>
  <tr><td>图谱不可用</td><td>记录 Neo4j 错误，降级为向量检索回答。</td><td>图谱增强暂不可用。</td></tr>
</table>

<h1>12 数据导入模块设计</h1>
<h2>12.1 功能描述</h2>
<p>数据导入模块由 compose 中的 one-shot seed job 实现，负责 MinIO 原文、reference data 和 Neo4j dump 的自动导入。每个 seed job 写入 marker，避免同版本重复导入；设置 <code>DATA_SEED_FORCE=1</code> 时可强制重导。</p>
<h2>12.2 数据流程图</h2>
<div class="diagram">
  <div class="diagram-title">图 6 数据导入数据流程</div>
  <pre class="mermaid">flowchart LR
  A[deploy/data/manifest.json] --> B[preflight 校验]
  C[*.tar.zst] --> B
  D[*.dump.zst] --> B
  B --> E[minio-seed]
  B --> F[ref-seed jobs]
  B --> G[neo4j prepare/load jobs]
  E --> H[(MinIO bucket)]
  F --> I[(reference volumes)]
  G --> J[(Neo4j volumes)]
  H --> K[写 marker]
  I --> K
  J --> K</pre>
</div>
<h2>12.3 异常处理设计</h2>
<table>
  <tr><th>异常</th><th>处理</th><th>恢复方式</th></tr>
  <tr><td>sha256 不一致</td><td>preflight 失败。</td><td>重新传输数据包。</td></tr>
  <tr><td>同版本 marker 存在</td><td>seed job 跳过。</td><td>确认无需重导；如需重导设置 <code>DATA_SEED_FORCE=1</code>。</td></tr>
  <tr><td>Neo4j dump 加载失败</td><td>seed job 退出非 0。</td><td>检查 dump 版本和 Neo4j 镜像版本。</td></tr>
  <tr><td>MinIO bucket 不存在</td><td>minio-seed 失败。</td><td>检查 minio-init 和 MinIO 密码。</td></tr>
</table>

<h1>13 接口总表</h1>
<h2>13.1 Gateway 对外接口</h2>
<table>
  <tr><th>接口分组</th><th>路径</th><th>方法</th><th>说明</th></tr>
  <tr><td>认证</td><td><code>/api/auth/login</code>、<code>/api/v1/auth/login</code></td><td>POST</td><td>登录。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/register</code>、<code>/api/v1/auth/register</code></td><td>POST</td><td>注册。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/me</code>、<code>/api/v1/auth/me</code></td><td>GET</td><td>当前用户。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/departments/tree</code>、<code>/api/v1/auth/departments/tree</code></td><td>GET</td><td>注册和个人中心使用的部门树。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/department</code>、<code>/api/auth/username</code>、<code>/api/auth/personnel-binding</code>、<code>/api/auth/password</code></td><td>PUT/POST</td><td>个人资料、用户名、人员绑定和密码维护。</td></tr>
  <tr><td>认证</td><td><code>/api/auth/forgot-password/initiate</code>、<code>/api/auth/forgot-password/verify</code>、<code>/api/auth/security-questions</code></td><td>GET/POST/PUT</td><td>找回密码和安全问题。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations</code>、<code>/api/v1/conversations</code></td><td>GET/POST</td><td>查询和创建会话。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations/{conversation_id}</code></td><td>GET/DELETE</td><td>获取或删除会话。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations/{conversation_id}/title</code></td><td>PUT</td><td>修改会话标题。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations/{conversation_id}/messages</code></td><td>POST</td><td>写入会话消息。</td></tr>
  <tr><td>文件</td><td><code>/api/conversations/{conversation_id}/files</code></td><td>GET</td><td>会话文件列表。</td></tr>
  <tr><td>文件</td><td><code>/api/conversations/{conversation_id}/files/{file_id}</code></td><td>GET/DELETE</td><td>文件详情和删除。</td></tr>
  <tr><td>文件</td><td><code>/api/conversations/{conversation_id}/files/{file_id}/download</code></td><td>GET</td><td>文件下载。</td></tr>
  <tr><td>上传</td><td><code>/api/upload_pdf</code>、<code>/api/upload_excel</code></td><td>POST</td><td>上传 PDF、Excel 或 CSV。</td></tr>
  <tr><td>文档辅助</td><td><code>/api/translate</code>、<code>/api/translate_document</code>、<code>/api/summarize_pdf/{doi}</code></td><td>POST</td><td>翻译和摘要。</td></tr>
  <tr><td>原文</td><td><code>/api/view_pdf/{doi}</code>、<code>/api/patent/original/{canonical_patent_id}</code></td><td>GET/HEAD</td><td>论文和专利原文。</td></tr>
  <tr><td>原文</td><td><code>/api/check_pdf/{doi}</code>、<code>/api/extract_pdf_text/{doi}</code>、<code>/api/literature_content</code>、<code>/api/reference_preview</code></td><td>GET/POST</td><td>原文检查、文本提取、文献内容和引用预览。</td></tr>
  <tr><td>系统</td><td><code>/api/health</code>、<code>/api/kb_info</code>、<code>/api/background_status</code>、<code>/api/refresh_kb</code>、<code>/api/clear_cache</code></td><td>GET/POST</td><td>健康、知识库和缓存接口。</td></tr>
  <tr><td>问答</td><td><code>/api/{fast|thinking|patent}/ask</code>、<code>/api/v1/{fast|thinking|patent}/ask</code></td><td>POST</td><td>同步问答。</td></tr>
  <tr><td>问答</td><td><code>/api/{fast|thinking|patent}/ask_stream</code>、<code>/api/v1/{fast|thinking|patent}/ask_stream</code></td><td>POST</td><td>流式问答。</td></tr>
  <tr><td>任务</td><td><code>/api/v1/tasks</code>、<code>/api/v1/tasks/{task_id}</code>、<code>/api/v1/tasks/{task_id}/events</code>、<code>/api/v1/tasks/{task_id}/cancel</code></td><td>GET/POST</td><td>可恢复任务和事件。</td></tr>
  <tr><td>准入</td><td><code>/api/admission/status</code>、<code>/api/admission/requests/{request_id}</code>、<code>/api/admission/requests/{request_id}/cancel</code>、<code>/api/admission/requests/{request_id}/frames</code></td><td>GET/POST</td><td>请求准入状态、取消和帧信息。</td></tr>
  <tr><td>健康</td><td><code>/healthz</code></td><td>GET</td><td>gateway 健康检查。</td></tr>
</table>
<h2>13.2 管理后台接口</h2>
<table>
  <tr><th>分组</th><th>路径</th><th>方法</th><th>说明</th></tr>
  <tr><td>用户</td><td><code>/api/admin/users</code>、<code>/api/admin/users/{user_id}</code></td><td>GET/POST/DELETE</td><td>用户列表、新增和删除。</td></tr>
  <tr><td>用户</td><td><code>/api/admin/users/{user_id}/username</code>、<code>/api/admin/users/{user_id}/password</code>、<code>/api/admin/users/{user_id}/status</code>、<code>/api/admin/users/{user_id}/type</code></td><td>GET/PUT</td><td>用户名、密码、状态和类型维护。</td></tr>
  <tr><td>用户</td><td><code>/api/admin/users/{user_id}/personnel-binding</code></td><td>PUT/DELETE</td><td>人员绑定和解绑。</td></tr>
  <tr><td>用户</td><td><code>/api/admin/users/batch-delete</code>、<code>/api/admin/users/batch-type</code>、<code>/api/admin/users/batch-import</code>、<code>/api/admin/users/import-template</code></td><td>GET/POST</td><td>批量和模板。</td></tr>
  <tr><td>人员</td><td><code>/api/admin/personnel</code>、<code>/api/admin/personnel/{personnel_id}</code>、<code>/api/admin/personnel/{personnel_id}/status</code>、<code>/api/admin/personnel/{personnel_id}/bindings</code></td><td>GET/POST/PUT</td><td>人员增删改查、状态和绑定关系。</td></tr>
  <tr><td>人员</td><td><code>/api/admin/personnel/batch-import</code>、<code>/api/admin/personnel/import-template</code></td><td>GET/POST</td><td>人员批量导入和模板下载。</td></tr>
  <tr><td>部门</td><td><code>/api/admin/departments/tree</code></td><td>GET</td><td>部门树。</td></tr>
  <tr><td>部门</td><td><code>/api/admin/departments/primary</code>、<code>/api/admin/departments/primary/{primary_id}</code>、<code>/api/admin/departments/primary/{primary_id}/status</code></td><td>POST/PUT</td><td>一级部门维护。</td></tr>
  <tr><td>部门</td><td><code>/api/admin/departments/secondary</code>、<code>/api/admin/departments/secondary/{secondary_id}</code>、<code>/api/admin/departments/secondary/{secondary_id}/status</code>、<code>/api/admin/departments/secondary/{secondary_id}/users</code>、<code>/api/admin/departments/secondary/{secondary_id}/legacy-users</code></td><td>GET/POST/PUT</td><td>二级部门和用户关联。</td></tr>
  <tr><td>部门</td><td><code>/api/admin/departments/tertiary</code>、<code>/api/admin/departments/tertiary/{tertiary_id}</code>、<code>/api/admin/departments/tertiary/{tertiary_id}/status</code>、<code>/api/admin/departments/tertiary/{tertiary_id}/users</code></td><td>GET/POST/PUT</td><td>三级部门和用户关联。</td></tr>
  <tr><td>部门</td><td><code>/api/admin/departments/batch-import</code>、<code>/api/admin/departments/import-template</code></td><td>GET/POST</td><td>部门批量导入和模板下载。</td></tr>
  <tr><td>配额</td><td><code>/api/quota/my</code>、<code>/api/quota/configs</code>、<code>/api/quota/configs/{quota_type}</code>、<code>/api/quota/users/{user_id}</code>、<code>/api/quota/reset/{user_id}/{quota_type}</code></td><td>GET/POST/PUT</td><td>个人配额、配置、用户用量和重置。</td></tr>
</table>
<h2>13.3 内部和兼容接口</h2>
<table>
  <tr><th>接口</th><th>方法</th><th>提供方</th><th>说明</th></tr>
  <tr><td><code>/internal/quota/grants/precheck</code></td><td>POST</td><td>public-service</td><td>gateway 调用的配额预占。</td></tr>
  <tr><td><code>/internal/quota/grants/{grant_id}/finalize</code></td><td>POST</td><td>public-service</td><td>gateway 调用的配额结算。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/messages/user</code></td><td>POST</td><td>public-service</td><td>写用户消息。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/context-snapshot</code></td><td>GET</td><td>public-service</td><td>读取会话上下文快照。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/messages/assistant-async</code></td><td>POST</td><td>public-service</td><td>异步写助手消息。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/messages/assistant-terminal-async</code></td><td>POST</td><td>public-service</td><td>异步写终态助手消息。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/tasks/{task_id}/assistant-start</code></td><td>POST</td><td>public-service</td><td>任务助手消息开始。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/tasks/{task_id}/create-turn</code></td><td>POST</td><td>public-service</td><td>创建任务轮次。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/tasks/{task_id}/assistant-progress</code></td><td>POST</td><td>public-service</td><td>写任务进度。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/tasks/{task_id}/assistant-terminal</code></td><td>POST</td><td>public-service</td><td>写任务终态。</td></tr>
  <tr><td><code>/internal/conversations/{conversation_id}/tasks/{task_id}/rollback-create</code></td><td>POST</td><td>public-service</td><td>任务创建失败回滚。</td></tr>
  <tr><td><code>/api/ask</code>、<code>/api/v1/ask</code>、<code>/api/{mode}/ask</code></td><td>POST</td><td>各 QA 后端</td><td>后端直连或兼容入口，生产优先经 gateway。</td></tr>
  <tr><td><code>/api/ask_stream</code>、<code>/api/v1/ask_stream</code>、<code>/api/{mode}/ask_stream</code></td><td>POST</td><td>各 QA 后端</td><td>后端直连或兼容流式入口，生产优先经 gateway。</td></tr>
  <tr><td><code>/api/health</code>、<code>/api/v1/health</code>、<code>/healthz</code></td><td>GET</td><td>各后端</td><td>健康检查。</td></tr>
</table>
"""

DEVELOPMENT_DOC_FINAL += """

<h1>11 接口实现清单</h1>
<p>开发维护时应以 gateway 对外路由表为准。前端不直接调用 QA 后端或 public-service 内部接口；除健康检查和特殊排障外，生产流量统一经过 gateway。</p>
<table>
  <tr><th>领域</th><th>对外接口</th><th>后端归属</th><th>维护注意事项</th></tr>
  <tr><td>认证</td><td><code>/api/auth/*</code>、<code>/api/v1/auth/*</code></td><td>public-service</td><td>新增字段需同步前端登录态和用户模型。</td></tr>
  <tr><td>会话</td><td><code>/api/conversations*</code>、<code>/api/v1/conversations*</code></td><td>public-service</td><td>消息写入与异步任务接口需保持一致。</td></tr>
  <tr><td>文件和原文</td><td><code>/api/upload_pdf</code>、<code>/api/upload_excel</code>、<code>/api/view_pdf/*</code>、<code>/api/patent/original/*</code></td><td>public-service，QA 兼容保留</td><td>MinIO key 规则变更需同步 seed 和 manifest。</td></tr>
  <tr><td>问答</td><td><code>/api/{fast|thinking|patent}/ask(_stream)</code></td><td>gateway -> QA 后端</td><td>SSE 事件 schema 变更需前后端同步。</td></tr>
  <tr><td>配额</td><td><code>/api/quota/*</code> 和 <code>/internal/quota/*</code></td><td>public-service</td><td>precheck/finalize 必须成对调用。</td></tr>
  <tr><td>管理后台</td><td><code>/api/admin/users*</code>、<code>/api/admin/personnel*</code>、<code>/api/admin/departments*</code></td><td>public-service</td><td>批量导入模板字段变更需更新用户手册。</td></tr>
  <tr><td>任务</td><td><code>/api/v1/tasks*</code></td><td>gateway</td><td>事件流需支持断线恢复。</td></tr>
  <tr><td>准入</td><td><code>/api/admission/*</code></td><td>gateway</td><td>用于任务准入状态、取消和帧读取。</td></tr>
</table>

<h1>12 配置开发规范</h1>
<h2>12.1 模型配置</h2>
<table>
  <tr><th>能力</th><th>共享配置名</th><th>secret 配置名</th><th>使用方</th></tr>
  <tr><td>LLM</td><td><code>LLM_BASE_URL</code>、<code>LLM_MODEL</code></td><td><code>LLM_API_KEY</code></td><td>fastQA、highThinkingQA、patentQA。</td></tr>
  <tr><td>Intent</td><td><code>INTENT_MODEL_ENABLED</code>、<code>INTENT_MODEL_BASE_URL</code>、<code>INTENT_MODEL</code></td><td><code>INTENT_MODEL_API_KEY</code></td><td>fastQA、patentQA。</td></tr>
  <tr><td>QA Embedding</td><td><code>QA_EMBEDDING_BASE_URL</code>、<code>QA_EMBEDDING_MODEL</code></td><td><code>QA_EMBEDDING_API_KEY</code></td><td>fastQA、patentQA。</td></tr>
  <tr><td>HighThinking Embedding</td><td><code>HIGHTHINKINGQA_EMBEDDING_BASE_URL</code>、<code>HIGHTHINKINGQA_EMBEDDING_MODEL</code></td><td><code>HIGHTHINKINGQA_EMBEDDING_API_KEY</code></td><td>highThinkingQA。</td></tr>
  <tr><td>Rerank</td><td><code>RERANK_PROVIDER</code>、<code>RERANK_BASE_URL</code>、<code>RERANK_MODEL</code></td><td><code>RERANK_API_KEY</code></td><td>fastQA、patentQA。</td></tr>
</table>
<p>新增配置项时，必须同步 <code>resource/config/shared/*.env</code>、服务本地配置、<code>deploy/.env.production.example</code>、<code>deploy/docker-compose.yml</code>、部署文档和运维文档。密钥类配置只进入 secret 或部署方 <code>.env</code>，不得写入代码常量。</p>

<h2>12.2 SSE 事件规范</h2>
<table>
  <tr><th>事件类型</th><th>字段</th><th>前端处理</th></tr>
  <tr><td>阶段开始</td><td><code>stage</code>、<code>title</code>、<code>timestamp</code></td><td>创建或更新阶段卡片。</td></tr>
  <tr><td>阶段结束</td><td><code>stage</code>、<code>duration_ms</code>、<code>status</code></td><td>展示耗时和状态。</td></tr>
  <tr><td>文本增量</td><td><code>delta</code></td><td>追加到回答正文。</td></tr>
  <tr><td>引用</td><td><code>references</code></td><td>渲染引用卡片和原文入口。</td></tr>
  <tr><td>错误</td><td><code>message</code>、<code>code</code></td><td>展示用户可理解提示。</td></tr>
  <tr><td>完成</td><td><code>answer</code>、<code>usage</code></td><td>收尾、保存状态、解锁输入框。</td></tr>
</table>

<h1>13 数据包构建规范</h1>
<div class="diagram">
  <div class="diagram-title">图 2 数据包构建流程</div>
  <pre class="mermaid">flowchart LR
  A[resource 原始数据] --> B[collect_minio_seed]
  B --> C[tables backfill]
  C --> D[minio-originals.tar.zst]
  A --> E[collect reference data]
  E --> F[fastqa/highthinking/patent/public ref 包]
  G[冻结 Neo4j] --> H[neo4j-admin dump]
  H --> I[neo4j dump.zst]
  D --> J[manifest.json]
  F --> J
  I --> J
  J --> K[validate_data_packages]</pre>
</div>
<table>
  <tr><th>规则</th><th>说明</th></tr>
  <tr><td>原文只进 MinIO 包</td><td>后端 reference data 不重复携带 PDF、PNG、JPG。</td></tr>
  <tr><td>专利 tables 必须 backfill</td><td>生成 <code>structured/tables.json</code>，并更新 manifest。</td></tr>
  <tr><td>向量库必须包含 SQLite</td><td>Chroma 包至少校验 <code>chroma.sqlite3</code>。</td></tr>
  <tr><td>manifest 必须包含 sha256</td><td>部署前 preflight 根据 manifest 校验。</td></tr>
  <tr><td>Neo4j dump 需要一致性窗口</td><td>导出前应停止或冻结图谱写入。</td></tr>
</table>

<h1>14 代码变更检查清单</h1>
<table>
  <tr><th>变更类型</th><th>必须检查</th></tr>
  <tr><td>前端页面</td><td><code>npm run build</code>，检查路由、按钮、响应式和 SSE 渲染。</td></tr>
  <tr><td>gateway 路由</td><td>更新路由表、鉴权、配额和代理目标。</td></tr>
  <tr><td>public-service 表结构</td><td>新增 SQL migration、模型、接口、测试和初始化脚本。</td></tr>
  <tr><td>QA 后端</td><td>检查模型配置、向量库路径、MinIO 路径和 SSE 事件。</td></tr>
  <tr><td>部署文件</td><td>同步 compose、env 模板、preflight 和交付文档。</td></tr>
  <tr><td>数据包规则</td><td>更新构建脚本、校验脚本和 manifest 统计。</td></tr>
</table>
"""

TEST_REPORT_FINAL += """

<h1>9 测试用例执行明细</h1>
<h2>9.1 认证与个人中心</h2>
<table>
  <tr><th>测试编号</th><th>测试内容</th><th>测试流程</th><th>预期结果</th><th>结论</th></tr>
  <tr><td>TC-AUTH-001</td><td>管理员登录。</td><td>打开登录页，输入管理员账号和初始密码，提交登录。</td><td>登录成功，进入管理后台或首次安全设置页。</td><td>现场执行。</td></tr>
  <tr><td>TC-AUTH-002</td><td>普通用户注册。</td><td>填写用户名、密码、姓名、工号和校验码，提交注册。</td><td>人员记录校验通过后账号创建成功。</td><td>现场执行。</td></tr>
  <tr><td>TC-AUTH-003</td><td>找回密码。</td><td>输入用户名，回答安全问题，设置新密码。</td><td>旧密码失效，新密码可登录。</td><td>现场执行。</td></tr>
  <tr><td>TC-AUTH-004</td><td>停用用户登录。</td><td>管理员停用用户，用户再次登录。</td><td>登录失败并提示账号状态异常。</td><td>现场执行。</td></tr>
</table>

<h2>9.2 管理后台</h2>
<table>
  <tr><th>测试编号</th><th>测试内容</th><th>测试流程</th><th>预期结果</th><th>结论</th></tr>
  <tr><td>TC-ADM-001</td><td>用户管理。</td><td>新增用户、修改用户名、重置密码、修改类型、停用启用。</td><td>列表状态和用户登录行为与操作一致。</td><td>现场执行。</td></tr>
  <tr><td>TC-ADM-002</td><td>部门树。</td><td>打开部门管理，查看 seed 部门树。</td><td>显示电池材料技术研究中心、正极材料研究所、装备工程化研究所、材料应用研究所及三级部门。</td><td>现场执行。</td></tr>
  <tr><td>TC-ADM-003</td><td>人员管理。</td><td>新增人员、修改部门、停用人员、下载模板、批量导入。</td><td>人员状态影响注册和绑定。</td><td>现场执行。</td></tr>
  <tr><td>TC-ADM-004</td><td>配额管理。</td><td>修改默认配额，查询用户用量，执行重置。</td><td>用户问答扣减和重置正确。</td><td>现场执行。</td></tr>
</table>

<h2>9.3 问答与文件</h2>
<table>
  <tr><th>测试编号</th><th>测试内容</th><th>测试流程</th><th>预期结果</th><th>结论</th></tr>
  <tr><td>TC-QA-001</td><td>文献问答。</td><td>选择“文献”，输入论文相关问题并发送。</td><td>返回答案、阶段耗时、引用和论文原文入口。</td><td>现场执行。</td></tr>
  <tr><td>TC-QA-002</td><td>深度问答。</td><td>选择“深度”，输入综合分析问题。</td><td>SSE 持续输出，最终答案完整。</td><td>现场执行。</td></tr>
  <tr><td>TC-QA-003</td><td>专利问答。</td><td>选择“专利”，输入专利技术问题。</td><td>返回专利引用、图谱或 tables 信息。</td><td>现场执行。</td></tr>
  <tr><td>TC-QA-004</td><td>PDF 文件问答。</td><td>上传 PDF，勾选文件后提问。</td><td>回答引用上传文件内容。</td><td>现场执行。</td></tr>
  <tr><td>TC-QA-005</td><td>Excel/CSV 文件问答。</td><td>上传表格文件，询问统计和字段解释。</td><td>系统解析表格并给出回答。</td><td>现场执行。</td></tr>
  <tr><td>TC-QA-006</td><td>原文查看。</td><td>点击论文或专利原文入口。</td><td>PDF 或对象内容可打开，无 404。</td><td>现场执行。</td></tr>
</table>

<h2>9.4 数据和模型调用</h2>
<table>
  <tr><th>测试编号</th><th>测试内容</th><th>测试流程</th><th>预期结果</th><th>结论</th></tr>
  <tr><td>TC-DATA-001</td><td>MinIO 原文数量。</td><td>检查 manifest 和 MinIO seed 日志。</td><td>papers 7153、专利目录 14006、tables 9581。</td><td>现场执行。</td></tr>
  <tr><td>TC-DATA-002</td><td>向量库加载。</td><td>查看 fastQA、highThinkingQA、patentQA 启动日志。</td><td>Chroma SQLite 文件存在，服务启动无路径错误。</td><td>现场执行。</td></tr>
  <tr><td>TC-DATA-003</td><td>图谱加载。</td><td>查看两个 Neo4j seed 和 healthcheck。</td><td>两个 Neo4j 容器 healthy。</td><td>现场执行。</td></tr>
  <tr><td>TC-MODEL-001</td><td>LLM 调用。</td><td>发起三类问答，查看 QA 日志。</td><td>模型请求成功，无 401、400、timeout。</td><td>现场执行。</td></tr>
  <tr><td>TC-MODEL-002</td><td>Intent 调用。</td><td>发起文献和专利问答，查看 intent 阶段日志。</td><td>intent 模型按配置启用并返回分类。</td><td>现场执行。</td></tr>
  <tr><td>TC-MODEL-003</td><td>Rerank 调用。</td><td>发起文献和专利检索类问题，查看 rerank 日志。</td><td>rerank provider 非 none 时成功调用。</td><td>现场执行。</td></tr>
</table>

<h1>10 性能测试记录模板</h1>
<table>
  <tr><th>场景</th><th>并发或次数</th><th>平均响应</th><th>P95</th><th>错误率</th><th>CPU</th><th>内存</th><th>结论</th></tr>
  <tr><td>登录接口</td><td>按客户验收要求填写</td><td>现场记录</td><td>现场记录</td><td>0 为目标</td><td>现场记录</td><td>现场记录</td><td>现场执行。</td></tr>
  <tr><td>文献问答首包</td><td>按客户验收要求填写</td><td>现场记录</td><td>现场记录</td><td>0 为目标</td><td>现场记录</td><td>现场记录</td><td>现场执行。</td></tr>
  <tr><td>深度问答总耗时</td><td>按客户验收要求填写</td><td>现场记录</td><td>现场记录</td><td>0 为目标</td><td>现场记录</td><td>现场记录</td><td>现场执行。</td></tr>
  <tr><td>专利问答首包</td><td>按客户验收要求填写</td><td>现场记录</td><td>现场记录</td><td>0 为目标</td><td>现场记录</td><td>现场记录</td><td>现场执行。</td></tr>
  <tr><td>原文查看</td><td>按客户验收要求填写</td><td>现场记录</td><td>现场记录</td><td>0 为目标</td><td>现场记录</td><td>现场记录</td><td>现场执行。</td></tr>
</table>
<p>正式验收时应将截图、日志片段、压测曲线或监控图替换到测试附件中。若客户未要求固定并发指标，本报告以功能通过、核心链路可用、无阻塞缺陷作为发布准入标准。</p>
"""

REQUIREMENT_LIST_FINAL = REQUIREMENT_LIST_FINAL.replace("</table>\n", """  <tr><td class="center">REQ-031</td><td>前端-会话</td><td>系统应支持会话创建、切换、标题修改、删除和历史消息查看。</td><td>2026-05-20</td><td>用户操作需求</td><td>2026-05-20</td><td>已实现</td><td>会话数据进入 MySQL。</td></tr>
  <tr><td class="center">REQ-032</td><td>前端-阶段展示</td><td>问答过程中应展示阶段、耗时、引用和错误提示。</td><td>2026-05-20</td><td>问答体验需求</td><td>2026-05-20</td><td>已实现</td><td>支持 intent、检索、rerank、生成等阶段。</td></tr>
  <tr><td class="center">REQ-033</td><td>接口-任务</td><td>系统应支持任务创建、事件读取和取消。</td><td>2026-05-20</td><td>接口设计</td><td>2026-05-20</td><td>已实现</td><td><code>/api/v1/tasks*</code>。</td></tr>
  <tr><td class="center">REQ-034</td><td>接口-准入</td><td>系统应支持请求准入状态、请求查询、取消和事件帧读取。</td><td>2026-05-20</td><td>接口设计</td><td>2026-05-20</td><td>已实现</td><td><code>/api/admission/*</code>。</td></tr>
  <tr><td class="center">REQ-035</td><td>接口-内部协作</td><td>gateway 与 public-service 应通过内部接口完成配额和消息落库。</td><td>2026-05-20</td><td>接口设计</td><td>2026-05-20</td><td>已实现</td><td><code>/internal/quota/*</code> 和 <code>/internal/conversations/*</code>。</td></tr>
  <tr><td class="center">REQ-036</td><td>文档-部署手册</td><td>部署手册应包含部署方案、环境要求、镜像加载、启动验证、模型配置、FAQ 和更新回滚。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>命令附成功和失败示例。</td></tr>
  <tr><td class="center">REQ-037</td><td>文档-运维手册</td><td>运维手册应包含系统资源、巡检、日志、启停、备份恢复和应急处置。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>包含 Mermaid 拓扑和泳道图。</td></tr>
  <tr><td class="center">REQ-038</td><td>文档-开发文档</td><td>开发文档应覆盖工程结构、模块、接口、数据库、配置和数据包构建规范。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>用于后续维护。</td></tr>
  <tr><td class="center">REQ-039</td><td>文档-概要设计</td><td>概要设计应覆盖系统架构、软件架构、集成架构、部署架构、数据库和非功能设计。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>图使用 Mermaid 表达。</td></tr>
  <tr><td class="center">REQ-040</td><td>文档-详细设计</td><td>详细设计应按模块说明功能、页面、库表、重点逻辑、流程、接口、输入输出和异常。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>覆盖三类问答和数据导入。</td></tr>
  <tr><td class="center">REQ-041</td><td>文档-测试报告</td><td>测试报告应覆盖环境、功能、性能、安全、数据和模型调用。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>提供可执行用例表。</td></tr>
  <tr><td class="center">REQ-042</td><td>文档-用户手册</td><td>用户手册应以最终用户视角说明注册、登录、问答、文件、原文和管理操作。</td><td>2026-05-20</td><td>交付文档要求</td><td>2026-05-20</td><td>已实现</td><td>不写部署细节。</td></tr>
  <tr><td class="center">REQ-043</td><td>安全-HTTPS</td><td>系统应支持内网域名、客户自签证书和证书替换。</td><td>2026-05-20</td><td>安全传输需求</td><td>2026-05-20</td><td>已实现</td><td><code>deploy/certs</code> 为证书挂载目录。</td></tr>
  <tr><td class="center">REQ-044</td><td>安全-账号</td><td>密码和人员校验码不得明文存储。</td><td>2026-05-20</td><td>安全需求</td><td>2026-05-20</td><td>已实现</td><td>使用哈希字段。</td></tr>
  <tr><td class="center">REQ-045</td><td>安全-权限</td><td>管理员接口应限制为管理员角色访问。</td><td>2026-05-20</td><td>安全需求</td><td>2026-05-20</td><td>已实现</td><td>前端隐藏入口，后端校验权限。</td></tr>
  <tr><td class="center">REQ-046</td><td>运维-日志</td><td>各容器应通过 Docker 日志输出关键阶段和错误信息。</td><td>2026-05-20</td><td>运维需求</td><td>2026-05-20</td><td>已实现</td><td>日志不得输出真实密钥。</td></tr>
  <tr><td class="center">REQ-047</td><td>运维-恢复</td><td>系统应支持通过备份配置、数据库、镜像和数据包进行恢复。</td><td>2026-05-20</td><td>运维需求</td><td>2026-05-20</td><td>已实现</td><td>运维手册给出恢复步骤。</td></tr>
  <tr><td class="center">REQ-048</td><td>数据-部门</td><td>MySQL 初始化应导入真实部门树，不导入测试部门。</td><td>2026-05-20</td><td>部门 seed 要求</td><td>2026-05-20</td><td>已实现</td><td>电池材料技术研究中心及下属部门。</td></tr>
  <tr><td class="center">REQ-049</td><td>数据-管理员</td><td>MySQL 初始化应创建 bootstrap 管理员账号。</td><td>2026-05-20</td><td>管理员 seed 要求</td><td>2026-05-20</td><td>已实现</td><td>文档不记录明文密码。</td></tr>
  <tr><td class="center">REQ-050</td><td>交付-命名</td><td>产品展示名使用 LiFeO4Agent，镜像仓库名使用 lowercase <code>lifeo4agent/*</code>。</td><td>2026-05-20</td><td>命名规范</td><td>2026-05-20</td><td>已实现</td><td>满足 Docker 镜像命名规范。</td></tr>
</table>
""")


def write_doc(title: str, body: str) -> None:
    name = f"LiFeO4Agent-{title}-{DATE}-{VERSION}.html"
    (ROOT / name).write_text(doc_shell(title, body), encoding="utf-8")


def main() -> None:
    write_doc("部署手册", DEPLOYMENT_MANUAL_FINAL)
    write_doc("运维手册", OPERATIONS_MANUAL_FINAL)
    write_doc("用户手册", USER_MANUAL_FINAL)
    write_doc("系统概要设计说明书", SUMMARY_DESIGN_FINAL)
    write_doc("系统详细设计说明书", DETAILED_DESIGN_FINAL)
    write_doc("开发文档", DEVELOPMENT_DOC_FINAL)
    write_doc("测试报告", TEST_REPORT_FINAL)
    write_doc("需求清单", REQUIREMENT_LIST_FINAL)
    from render_mermaid_diagrams import render_all

    render_all(ROOT)
    print(f"wrote delivery docs under {ROOT}")


if __name__ == "__main__":
    main()
