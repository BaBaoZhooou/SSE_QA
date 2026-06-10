# Neo4j + QA 检索增强问答

本目录提供本地 Neo4j 运行模板。数据导入和问答脚本在：

- `scripts/知识图谱/neo4j_import.py`
- `scripts/知识图谱/neo4j_qa.py`

## 1. 启动 Neo4j

从项目根目录运行：

```bash
docker compose -f 知识图谱/neo4j/compose.yaml up -d
```

也可以在 Docker Desktop 已启动后直接运行一键脚本，自动启动容器、等待 Bolt 端口并导入图谱：

```bash
scripts/知识图谱/start_neo4j_kg.sh
```

浏览器入口：

- Neo4j Browser: http://localhost:7476
- Bolt URI: `bolt://localhost:7698`
- 默认账号：`neo4j`
- 默认密码：`sse-kg-password`

如果本机没有 `neo4j:5-community` 镜像，第一次启动会拉取镜像，需要网络可用。

## 2. 导入知识图谱

```bash
NEO4J_PASSWORD=sse-kg-password \
python3 scripts/知识图谱/neo4j_import.py --clear --batch-size 1000
```

导入脚本会读取 `知识图谱/sse_knowledge_graph_full.json`，创建：

- 唯一约束：`KGNode.id`
- 普通索引：节点类型、文献 ID、材料 formula、材料类型、性能类别、路线 ID
- 全文索引：`kg_node_fulltext`
- 节点标签：`Paper`, `MaterialInstance`, `PropertyRecord`, `SynthesisRoute`, `Formula`, `ProcessTag` 等
- 关系类型：`REPORTS_MATERIAL`, `HAS_PROPERTY`, `MADE_BY`, `HAS_PROCESS_TAG`, `USES_PRECURSOR` 等

导入前可先 dry-run：

```bash
python3 scripts/知识图谱/neo4j_import.py --dry-run
```

## 3. QA 检索增强问答

只做检索，不调用模型：

```bash
NEO4J_PASSWORD=sse-kg-password \
python3 scripts/知识图谱/neo4j_qa.py "硫化物固态电解质中室温离子电导率较高的材料有哪些？" --no-llm
```

启用 OpenAI-compatible 模型生成中文回答：

```bash
export NEO4J_PASSWORD=sse-kg-password
export OPENAI_BASE_URL="https://your-compatible-endpoint/v1"
export OPENAI_MODEL="your-chat-model"
export OPENAI_API_KEY="..."

python3 scripts/知识图谱/neo4j_qa.py "LLZO 相关氧化物电解质常见合成工艺和前驱体是什么？"
```

脚本会先做结构化 Cypher 检索，再做 Neo4j fulltext 检索，最后把检索上下文交给模型。回答提示词要求只基于检索结果作答，并标注 DOI 或 `source_json`。

## 4. 常用 Cypher

统计节点和关系：

```cypher
MATCH (n:KGNode) RETURN labels(n), count(*) ORDER BY count(*) DESC;
MATCH ()-[r]->() RETURN type(r), count(*) ORDER BY count(*) DESC;
```

查询高电导材料：

```cypher
MATCH (m:MaterialInstance)-[:HAS_PROPERTY]->(p:PropertyRecord)
WHERE p.property_category = "ionic_conductivity_rt"
RETURN m.label, m.formula, m.material_type, p.value_raw, p.numeric_value, p.numeric_unit, p.source_json
ORDER BY p.numeric_value DESC
LIMIT 20;
```

查询材料合成路线：

```cypher
MATCH (m:MaterialInstance)-[:MADE_BY]->(r:SynthesisRoute)
OPTIONAL MATCH (r)-[:HAS_PROCESS_TAG]->(tag:ProcessTag)
OPTIONAL MATCH (r)-[:USES_PRECURSOR]->(precursor:Precursor)
RETURN m.label, r.process_summary, collect(DISTINCT tag.label) AS tags, collect(DISTINCT precursor.label) AS precursors
LIMIT 20;
```

全文检索：

```cypher
CALL db.index.fulltext.queryNodes("kg_node_fulltext", "LLZO OR garnet OR conductivity")
YIELD node, score
RETURN node.kind, node.label, node.source_json, score
ORDER BY score DESC
LIMIT 20;
```

## 5. 数据规模

当前全量图谱来自 3504 个 `sse_extraction.json`，包含 90730 个节点和 290531 条边。导入可能需要几分钟，取决于本机 Neo4j 内存配置和磁盘速度。
