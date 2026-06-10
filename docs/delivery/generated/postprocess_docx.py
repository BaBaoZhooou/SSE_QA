#!/usr/bin/env python3
from __future__ import annotations

import shutil
import tempfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DOCX_DIR = Path(__file__).resolve().parent / "docx"

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("w", NS_W)
ET.register_namespace("r", NS_R)
ET.register_namespace("", NS_REL)

W = f"{{{NS_W}}}"
R = f"{{{NS_R}}}"
REL = f"{{{NS_REL}}}"
CT = f"{{{NS_CT}}}"


def _el(tag: str, attrs: dict[str, str] | None = None, text: str | None = None) -> ET.Element:
    node = ET.Element(tag, attrs or {})
    if text is not None:
        node.text = text
    return node


def _run_text(text: str) -> ET.Element:
    run = _el(W + "r")
    run.append(_el(W + "t", text=text))
    return run


def _field_run(instr: str, fallback: str) -> list[ET.Element]:
    return [
        _el(W + "r"),
        _el(W + "r"),
        _el(W + "r"),
        _el(W + "r"),
        _el(W + "r"),
    ]


def _field_sequence(instr: str, fallback: str) -> list[ET.Element]:
    begin = _el(W + "r")
    begin.append(_el(W + "fldChar", {W + "fldCharType": "begin"}))
    code = _el(W + "r")
    instr_text = _el(W + "instrText", {"{http://www.w3.org/XML/1998/namespace}space": "preserve"}, f" {instr} ")
    code.append(instr_text)
    sep = _el(W + "r")
    sep.append(_el(W + "fldChar", {W + "fldCharType": "separate"}))
    value = _run_text(fallback)
    end = _el(W + "r")
    end.append(_el(W + "fldChar", {W + "fldCharType": "end"}))
    return [begin, code, sep, value, end]


def _paragraph(alignment: str, runs: list[ET.Element]) -> ET.Element:
    p = _el(W + "p")
    ppr = _el(W + "pPr")
    ppr.append(_el(W + "jc", {W + "val": alignment}))
    p.append(ppr)
    for run in runs:
        p.append(run)
    return p


def _header_xml(title: str) -> bytes:
    root = _el(W + "hdr")
    root.append(_paragraph("center", [_run_text(f"LiFeO4Agent {title}")]))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _footer_xml() -> bytes:
    root = _el(W + "ftr")
    runs: list[ET.Element] = []
    runs.append(_run_text("第 "))
    runs.extend(_field_sequence("PAGE", "1"))
    runs.append(_run_text(" 页 / 共 "))
    runs.extend(_field_sequence("NUMPAGES", "1"))
    runs.append(_run_text(" 页"))
    root.append(_paragraph("center", runs))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _doc_title(path: Path) -> str:
    stem = path.stem
    prefix = "LiFeO4Agent-"
    if stem.startswith(prefix):
        stem = stem[len(prefix):]
    suffix = "-20260520-V1.0"
    if stem.endswith(suffix):
        stem = stem[: -len(suffix)]
    return stem


def _next_rel_id(root: ET.Element) -> str:
    used = set()
    for rel in root.findall(REL + "Relationship"):
        rid = rel.get("Id")
        if rid:
            used.add(rid)
    index = 1
    while f"rId{index}" in used:
        index += 1
    return f"rId{index}"


def _ensure_content_type(root: ET.Element, part_name: str, content_type: str) -> None:
    for override in root.findall(CT + "Override"):
        if override.get("PartName") == part_name:
            return
    root.append(_el(CT + "Override", {"PartName": part_name, "ContentType": content_type}))


def _ensure_default_content_type(root: ET.Element, extension: str, content_type: str) -> None:
    for default in root.findall(CT + "Default"):
        if default.get("Extension") == extension:
            return
    root.append(_el(CT + "Default", {"Extension": extension, "ContentType": content_type}))


def _path_from_external_target(target: str) -> Path | None:
    if target.startswith("file://"):
        parsed = urlparse(target)
        return Path(unquote(parsed.path))
    if target.startswith("/"):
        return Path(target)
    return None


def _embed_external_images(rels_root: ET.Element, content_types_root: ET.Element) -> list[tuple[str, bytes]]:
    embedded: list[tuple[str, bytes]] = []
    media_index = 1
    for rel in rels_root.findall(REL + "Relationship"):
        if rel.get("Type") != "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image":
            continue
        if rel.get("TargetMode") != "External":
            continue
        target = rel.get("Target") or ""
        image_path = _path_from_external_target(target)
        if image_path is None or not image_path.exists():
            continue
        ext = image_path.suffix.lower() or ".png"
        if ext not in {".png", ".jpg", ".jpeg"}:
            ext = ".png"
        media_name = f"media/image{media_index}{ext}"
        media_index += 1
        rel.set("Target", media_name)
        rel.attrib.pop("TargetMode", None)
        content_type = "image/png" if ext == ".png" else "image/jpeg"
        _ensure_default_content_type(content_types_root, ext.lstrip("."), content_type)
        embedded.append((f"word/{media_name}", image_path.read_bytes()))
    return embedded


def patch_docx(path: Path) -> None:
    title = _doc_title(path)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)

    with ZipFile(path, "r") as zin:
        document_xml = zin.read("word/document.xml")
        rels_xml = zin.read("word/_rels/document.xml.rels")
        content_types_xml = zin.read("[Content_Types].xml")

        document_root = ET.fromstring(document_xml)
        rels_root = ET.fromstring(rels_xml)
        content_types_root = ET.fromstring(content_types_xml)

        for rel in list(rels_root.findall(REL + "Relationship")):
            if rel.get("Type") in {
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer",
            }:
                rels_root.remove(rel)

        header_rid = _next_rel_id(rels_root)
        rels_root.append(
            _el(
                REL + "Relationship",
                {
                    "Id": header_rid,
                    "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header",
                    "Target": "header1.xml",
                },
            )
        )
        footer_rid = _next_rel_id(rels_root)
        rels_root.append(
            _el(
                REL + "Relationship",
                {
                    "Id": footer_rid,
                    "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer",
                    "Target": "footer1.xml",
                },
            )
        )

        sect_pr = document_root.find(f".//{W}sectPr")
        if sect_pr is not None:
            for child in list(sect_pr):
                if child.tag in {W + "headerReference", W + "footerReference"}:
                    sect_pr.remove(child)
            sect_pr.insert(0, _el(W + "footerReference", {W + "type": "default", R + "id": footer_rid}))
            sect_pr.insert(0, _el(W + "headerReference", {W + "type": "default", R + "id": header_rid}))
            pg_mar = sect_pr.find(W + "pgMar")
            if pg_mar is not None:
                pg_mar.set(W + "header", "851")
                pg_mar.set(W + "footer", "992")

        _ensure_content_type(
            content_types_root,
            "/word/header1.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml",
        )
        _ensure_content_type(
            content_types_root,
            "/word/footer1.xml",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml",
        )
        embedded_images = _embed_external_images(rels_root, content_types_root)

        with ZipFile(tmp_path, "w", ZIP_DEFLATED) as zout:
            embedded_names = {name for name, _ in embedded_images}
            for item in zin.infolist():
                if item.filename in {
                    "word/document.xml",
                    "word/_rels/document.xml.rels",
                    "[Content_Types].xml",
                    "word/header1.xml",
                    "word/footer1.xml",
                } or item.filename in embedded_names:
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr("word/document.xml", ET.tostring(document_root, encoding="utf-8", xml_declaration=True))
            zout.writestr("word/_rels/document.xml.rels", ET.tostring(rels_root, encoding="utf-8", xml_declaration=True))
            zout.writestr("[Content_Types].xml", ET.tostring(content_types_root, encoding="utf-8", xml_declaration=True))
            zout.writestr("word/header1.xml", _header_xml(title))
            zout.writestr("word/footer1.xml", _footer_xml())
            for name, payload in embedded_images:
                zout.writestr(name, payload)

    shutil.move(str(tmp_path), path)
    print(f"patched {path.name}")


def main() -> None:
    for path in sorted(DOCX_DIR.glob("*.docx")):
        patch_docx(path)


if __name__ == "__main__":
    main()
