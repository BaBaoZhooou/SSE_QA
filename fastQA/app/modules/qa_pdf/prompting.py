from __future__ import annotations

from typing import Optional

from app.core.prompt_loader import load_prompt_template


SUMMARY_KEYWORDS = ['总结', '概述', '概括', '研究内容', '主要内容', '核心内容', '研究重点', '重点']

GENERIC_PHRASES = [
    '橄榄石型晶体结构',
    '理论容量',
    '170mah/g',
    '工作电压',
    '3.2-3.3v',
    '高温固相法',
    '水热法',
    '溶胶-凝胶法',
    '共沉淀法',
]

PDF_QA_SYSTEM_MESSAGE = load_prompt_template("pdf_qa_system.txt")


def is_summary_question(question: str) -> bool:
    question_lower = str(question or '').lower()
    return any(keyword in question_lower for keyword in SUMMARY_KEYWORDS)


def build_kb_section(kb_verification: Optional[dict]) -> str:
    if not (kb_verification and kb_verification.get('kb_answer')):
        return ''

    return f"""

**📚 知识库验证信息**（用于验证PDF中提到的内容是否真实存在）：
{kb_verification.get('kb_answer', '')}

**重要说明**：
- 知识库信息仅用于**验证**PDF中提到的内容是否真实存在
- 如果PDF中提到某个材料、方法或数据，且知识库中也有相关信息，可以标注"（知识库验证：存在相关数据）"
- **不要**使用知识库信息来补充PDF中没有的内容
- **不要**使用知识库信息来替代PDF原文中的具体数据
- 如果PDF中提到但知识库中没有，仍然以PDF为准，但可以标注"（知识库中未找到相关验证数据）"
"""


def build_pdf_answer_prompt(
    *,
    question: str,
    pdf_content: str,
    kb_section: str,
    is_summary: bool,
) -> str:
    template_name = "pdf_qa_summary_user.txt" if is_summary else "pdf_qa_answer_user.txt"
    return load_prompt_template(template_name).format(
        question=question,
        pdf_content=pdf_content,
        kb_section=kb_section,
    )


__all__ = [
    'GENERIC_PHRASES',
    'PDF_QA_SYSTEM_MESSAGE',
    'build_kb_section',
    'build_pdf_answer_prompt',
    'is_summary_question',
]
