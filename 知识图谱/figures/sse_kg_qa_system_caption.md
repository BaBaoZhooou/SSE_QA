# Figure caption draft

**Figure X. Neo4j-enabled knowledge graph retrieval-augmented question-answering system for solid-state electrolyte literature mining.**

(A) Knowledge graph representation of the extracted solid-state electrolyte literature corpus in Neo4j. The graph links papers, material instances, synthesis routes, electrochemical and battery properties, and normalized concept nodes such as formula, structure family, process tag and precursor. The current graph contains 90,730 nodes and 290,531 relationships.

(B) Retrieval architecture for graph-augmented QA. A natural-language question is parsed into retrieval intent, including material family, property category, synthesis-route request and material terms. The system queries the Neo4j graph through structured Cypher traversal and full-text search over indexed node properties. Ranked graph records are assembled as evidence context.

(C) Grounded QA output. Retrieved graph evidence is passed to an LLM only after graph retrieval, constraining answer generation to material-property-route evidence with DOI or source-json traceability. The output summarizes ranked materials, values and citations rather than relying on unsupported parametric knowledge.

Bottom trace: paper metadata, material instance, property or route record, evidence sentence or table row, and final cited answer form a traceable evidence chain.
