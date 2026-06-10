# 固态电解质信息抽取知识图谱

本目录由 `scripts/知识图谱/build_sse_knowledge_graph.py` 自动生成，数据来源为 `信息提取结果/*/sse_extraction.json`。

## 规模

- 文献 JSON：3504
- 图谱节点：90730
- 图谱边：290531
- 电解质材料实例：9273
- 性能/界面/电池记录：40726
- 合成/加工路线：8178
- 表格摘要：13229

## 主要文件

- `sse_knowledge_graph_full.json`：全量节点和边。
- `nodes.csv` / `edges.csv`：通用图数据库导入表。
- `materials.csv`：论文内材料实体实例表。
- `property_records.csv`：性能、界面、电池性能记录表，含原始值、可解析数值和证据片段。
- `synthesis_routes.csv`：合成与加工路线表，含标准工艺标签、前驱体、溶剂、步骤 JSON。
- `tables.csv`：抽取出的表格标题和行列数摘要，不包含大段原始 Markdown。
- `summary.json`：计数和高频实体统计。
- `sse_knowledge_graph.html`：离线可打开的交互式知识图谱总览。
- `neo4j/README.md`：Neo4j 本地数据库启动、导入和 QA 检索增强问答说明。

## 图谱设计

材料节点采用“论文内实例”建模，例如同一个 `Li3PS4` 在不同论文中是不同 `MaterialInstance`；化学式、结构家族、SSE family、导电离子、工艺标签、前驱体、溶剂、性能类别等再作为全局归一概念节点连接。这样既保留单篇证据，也能按体系做跨文献统计。

核心关系包括：

- `Paper -> REPORTS_MATERIAL -> MaterialInstance`
- `MaterialInstance -> HAS_FORMULA / HAS_MATERIAL_TYPE / HAS_STRUCTURE_FAMILY`
- `MaterialInstance -> HAS_PROPERTY -> PropertyRecord -> HAS_PROPERTY_CATEGORY`
- `MaterialInstance -> MADE_BY -> SynthesisRoute -> HAS_PROCESS_TAG / USES_PRECURSOR / USES_SOLVENT`
- `Paper -> HAS_SSE_FAMILY / HAS_CONDUCTING_ION / PUBLISHED_YEAR / PUBLISHED_IN`

## 高频概览

- 高频 SSE family：polymer (1032), composite (920), oxide (586), sulfide (465), other (125), halide (113), borate/phosphate (43), hydride (37), phosphate (3)
- 高频性能类别：Battery performance (10376), Room-temperature ionic conductivity (7779), Interface property (5709), Electrochemical stability window (3247), Cation transference number (2927), Li-ion transference number (2817), Activation energy (2549), Thermal stability (2124), Conductivity-temperature relation (1327), Relative density (834)

## 重新生成

```bash
python3 scripts/知识图谱/build_sse_knowledge_graph.py
```

## Neo4j 与 QA

```bash
scripts/知识图谱/start_neo4j_kg.sh
NEO4J_PASSWORD=sse-kg-password python3 scripts/知识图谱/neo4j_qa.py "硫化物固态电解质中室温离子电导率较高的材料有哪些？" --no-llm
```
