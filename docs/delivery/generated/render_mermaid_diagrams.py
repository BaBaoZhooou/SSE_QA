#!/usr/bin/env python3
from __future__ import annotations

import html
import math
import re
from collections import defaultdict, deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "diagram_assets"

FONT_CANDIDATES = (
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = _font(24)
FONT_SMALL = _font(20)
FONT_TITLE = _font(28)


def _clean_label(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    return text.strip()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
    return box[2] - box[0], box[3] - box[1]


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, font: ImageFont.ImageFont) -> str:
    lines: list[str] = []
    for raw in text.splitlines() or [""]:
        current = ""
        for char in raw:
            trial = current + char
            if _text_size(draw, trial, font)[0] <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = char
        lines.append(current)
    return "\n".join(lines)


def _draw_center_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont = FONT,
    fill: str = "#1f2933",
) -> None:
    x1, y1, x2, y2 = box
    wrapped = _wrap_text(draw, text, max(40, x2 - x1 - 24), font)
    tw, th = _text_size(draw, wrapped, font)
    draw.multiline_text(
        (x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2),
        wrapped,
        font=font,
        fill=fill,
        align="center",
        spacing=4,
    )


def _arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], fill: str = "#475569") -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=fill, width=3)
    angle = math.atan2(ey - sy, ex - sx)
    size = 11
    p1 = (ex - size * math.cos(angle - math.pi / 6), ey - size * math.sin(angle - math.pi / 6))
    p2 = (ex - size * math.cos(angle + math.pi / 6), ey - size * math.sin(angle + math.pi / 6))
    draw.polygon([(ex, ey), p1, p2], fill=fill)


def _parse_node_spec(text: str) -> dict[str, tuple[str, str]]:
    nodes: dict[str, tuple[str, str]] = {}
    patterns = (
        (r"\b([A-Za-z][A-Za-z0-9_]*)\s*\[\((.*?)\)\]", "db"),
        (r"\b([A-Za-z][A-Za-z0-9_]*)\s*\{\s*(.*?)\s*\}", "diamond"),
        (r"\b([A-Za-z][A-Za-z0-9_]*)\s*\[\s*(.*?)\s*\]", "rect"),
        (r"\b([A-Za-z][A-Za-z0-9_]*)\s*\(\((.*?)\)\)", "round"),
    )
    for pattern, shape in patterns:
        for match in re.finditer(pattern, text):
            nodes.setdefault(match.group(1), (_clean_label(match.group(2)), shape))
    return nodes


def _extract_edge_chain(line: str) -> list[tuple[str, str]]:
    if "-->" not in line:
        return []
    normalized = re.sub(r"\s*--[^>]*-->\s*", "-->", line)
    normalized = re.sub(r"\s*-->\s*", "-->", normalized)
    parts = normalized.split("-->")
    ids: list[str] = []
    for part in parts:
        match = re.match(r"\s*([A-Za-z][A-Za-z0-9_]*)", part.strip())
        if match:
            ids.append(match.group(1))
    return [(ids[i], ids[i + 1]) for i in range(len(ids) - 1)]


def _edge_endpoints(
    boxes: dict[str, tuple[int, int, int, int]],
    src: str,
    dst: str,
    direction: str,
) -> tuple[tuple[float, float], tuple[float, float]]:
    sx1, sy1, sx2, sy2 = boxes[src]
    dx1, dy1, dx2, dy2 = boxes[dst]
    if direction == "LR":
        if sx1 <= dx1:
            return (sx2, (sy1 + sy2) / 2), (dx1, (dy1 + dy2) / 2)
        return (sx1, (sy1 + sy2) / 2), (dx2, (dy1 + dy2) / 2)
    if sy1 <= dy1:
        return ((sx1 + sx2) / 2, sy2), ((dx1 + dx2) / 2, dy1)
    return ((sx1 + sx2) / 2, sy1), ((dx1 + dx2) / 2, dy2)


def render_flowchart(source: str, out: Path) -> None:
    lines = [line.rstrip() for line in source.splitlines() if line.strip()]
    direction = "TB"
    if lines and " LR" in lines[0]:
        direction = "LR"
    nodes: dict[str, tuple[str, str]] = {}
    edges: list[tuple[str, str]] = []
    order: list[str] = []
    for line in lines[1:]:
        if line.strip().startswith(("subgraph", "end")):
            nodes.update(_parse_node_spec(line))
            continue
        for node_id, spec in _parse_node_spec(line).items():
            nodes[node_id] = spec
            if node_id not in order:
                order.append(node_id)
        for src, dst in _extract_edge_chain(line):
            edges.append((src, dst))
            for node_id in (src, dst):
                if node_id not in nodes:
                    nodes[node_id] = (node_id, "rect")
                if node_id not in order:
                    order.append(node_id)
    if not nodes:
        nodes = {"A": ("图示", "rect")}
        order = ["A"]

    indeg = defaultdict(int)
    adj = defaultdict(list)
    for src, dst in edges:
        adj[src].append(dst)
        indeg[dst] += 1
        indeg.setdefault(src, 0)
    layer = {node_id: 0 for node_id in nodes}
    queue = deque([node_id for node_id in order if indeg[node_id] == 0])
    seen = set(queue)
    while queue:
        src = queue.popleft()
        for dst in adj[src]:
            layer[dst] = max(layer[dst], layer[src] + 1)
            indeg[dst] -= 1
            if indeg[dst] == 0 and dst not in seen:
                queue.append(dst)
                seen.add(dst)
    groups: dict[int, list[str]] = defaultdict(list)
    for node_id in order:
        groups[layer.get(node_id, 0)].append(node_id)

    node_w, node_h = 210, 82
    gap_x, gap_y = 82, 54
    margin = 54
    max_layer = max(groups) if groups else 0
    max_group = max(len(v) for v in groups.values()) if groups else 1
    if direction == "LR":
        width = margin * 2 + (max_layer + 1) * node_w + max_layer * gap_x
        height = margin * 2 + max_group * node_h + max(0, max_group - 1) * gap_y
    else:
        width = margin * 2 + max_group * node_w + max(0, max_group - 1) * gap_x
        height = margin * 2 + (max_layer + 1) * node_h + max_layer * gap_y
    image = Image.new("RGB", (max(width, 780), max(height, 260)), "white")
    draw = ImageDraw.Draw(image)
    boxes: dict[str, tuple[int, int, int, int]] = {}
    for layer_index, node_ids in groups.items():
        for index, node_id in enumerate(node_ids):
            if direction == "LR":
                x = margin + layer_index * (node_w + gap_x)
                group_h = len(node_ids) * node_h + max(0, len(node_ids) - 1) * gap_y
                y = (image.height - group_h) // 2 + index * (node_h + gap_y)
            else:
                y = margin + layer_index * (node_h + gap_y)
                group_w = len(node_ids) * node_w + max(0, len(node_ids) - 1) * gap_x
                x = (image.width - group_w) // 2 + index * (node_w + gap_x)
            boxes[node_id] = (x, y, x + node_w, y + node_h)
    for src, dst in edges:
        if src in boxes and dst in boxes:
            _arrow(draw, *_edge_endpoints(boxes, src, dst, direction))
    for node_id, box in boxes.items():
        label, shape = nodes[node_id]
        if shape == "diamond":
            x1, y1, x2, y2 = box
            points = [((x1 + x2) / 2, y1), (x2, (y1 + y2) / 2), ((x1 + x2) / 2, y2), (x1, (y1 + y2) / 2)]
            draw.polygon(points, fill="#fff7ed", outline="#c2410c")
        else:
            fill = "#f8fafc" if shape != "db" else "#eef6ff"
            outline = "#2563eb" if shape == "db" else "#334155"
            draw.rounded_rectangle(box, radius=12, fill=fill, outline=outline, width=2)
        _draw_center_text(draw, box, label)
    image.save(out)


def render_sequence(source: str, out: Path) -> None:
    lines = [line.rstrip() for line in source.splitlines() if line.strip()]
    participants: list[tuple[str, str]] = []
    messages: list[tuple[str, str, str, str]] = []
    notes: list[str] = []
    for line in lines[1:]:
        stripped = line.strip()
        match = re.match(r"participant\s+(\w+)\s+as\s+(.+)", stripped)
        if match:
            participants.append((match.group(1), _clean_label(match.group(2))))
            continue
        match = re.match(r"(\w+)(-+>>)(\w+):\s*(.+)", stripped)
        if match:
            messages.append((match.group(1), match.group(3), _clean_label(match.group(4)), match.group(2)))
            continue
        if stripped.startswith(("alt ", "else", "loop ", "end")):
            notes.append(stripped)
            messages.append(("", "", stripped, "note"))
    if not participants:
        ids = []
        for src, dst, _, kind in messages:
            if kind != "note":
                ids.extend([src, dst])
        participants = [(node_id, node_id) for node_id in dict.fromkeys(ids)]
    count = max(1, len(participants))
    width = max(960, 150 + count * 190)
    row_h = 58
    height = 118 + max(1, len(messages)) * row_h + 50
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    x_by_id: dict[str, int] = {}
    left = 70
    usable = width - left * 2
    for index, (pid, label) in enumerate(participants):
        x = left + int(usable * (index + 0.5) / count)
        x_by_id[pid] = x
        box = (x - 80, 28, x + 80, 78)
        draw.rounded_rectangle(box, radius=8, fill="#eff6ff", outline="#2563eb", width=2)
        _draw_center_text(draw, box, label, FONT_SMALL)
        draw.line((x, 78, x, height - 24), fill="#cbd5e1", width=2)
    y = 118
    for src, dst, label, kind in messages:
        if kind == "note":
            draw.rounded_rectangle((55, y - 18, width - 55, y + 24), radius=6, fill="#f8fafc", outline="#cbd5e1")
            draw.text((70, y - 10), _clean_label(label), font=FONT_SMALL, fill="#475569")
            y += row_h
            continue
        sx, dx = x_by_id.get(src, left), x_by_id.get(dst, width - left)
        _arrow(draw, (sx, y), (dx, y))
        label_text = _wrap_text(draw, label, abs(dx - sx) + 120, FONT_SMALL)
        tw, _ = _text_size(draw, label_text, FONT_SMALL)
        draw.multiline_text(((sx + dx - tw) / 2, y - 28), label_text, font=FONT_SMALL, fill="#1f2933", align="center")
        y += row_h
    image.save(out)


def render_tree(source: str, out: Path) -> None:
    lines = [line.rstrip("\n") for line in source.splitlines() if line.strip() and not line.strip().startswith("mindmap")]
    nodes: list[tuple[int, str, int | None]] = []
    stack: list[tuple[int, int]] = []
    for raw in lines:
        indent = len(raw) - len(raw.lstrip(" "))
        label = raw.strip()
        label = re.sub(r"^root\(\((.*?)\)\)$", r"\1", label)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else None
        index = len(nodes)
        nodes.append((indent // 2, _clean_label(label), parent))
        stack.append((indent, index))
    if not nodes:
        nodes = [(0, "图示", None)]
    y_gap, x_gap = 74, 230
    width = max(920, 130 + (max(d for d, _, _ in nodes) + 1) * x_gap)
    height = max(300, 80 + len(nodes) * y_gap)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    boxes = []
    for idx, (depth, label, parent) in enumerate(nodes):
        x = 50 + depth * x_gap
        y = 38 + idx * y_gap
        box = (x, y, x + 190, y + 48)
        boxes.append(box)
    for idx, (_, _, parent) in enumerate(nodes):
        if parent is not None:
            px1, py1, px2, py2 = boxes[parent]
            x1, y1, x2, y2 = boxes[idx]
            _arrow(draw, (px2, (py1 + py2) / 2), (x1, (y1 + y2) / 2))
    for idx, (_, label, _) in enumerate(nodes):
        fill = "#ecfeff" if idx == 0 else "#f8fafc"
        outline = "#0891b2" if idx == 0 else "#334155"
        draw.rounded_rectangle(boxes[idx], radius=10, fill=fill, outline=outline, width=2)
        _draw_center_text(draw, boxes[idx], label, FONT_SMALL)
    image.save(out)


def render_er(source: str, out: Path) -> None:
    entities: list[str] = []
    edges: list[tuple[str, str, str]] = []
    for line in source.splitlines():
        match = re.match(r"\s*(\w+)\s+\S+\s+(\w+)\s*:\s*(.*)", line)
        if match:
            src, dst, label = match.group(1), match.group(2), _clean_label(match.group(3))
            edges.append((src, dst, label))
            for entity in (src, dst):
                if entity not in entities:
                    entities.append(entity)
    if not entities:
        entities = ["entity"]
    cols = 3
    node_w, node_h = 245, 62
    gap_x, gap_y = 70, 70
    rows = math.ceil(len(entities) / cols)
    width = max(940, 70 * 2 + cols * node_w + (cols - 1) * gap_x)
    height = max(360, 70 * 2 + rows * node_h + (rows - 1) * gap_y)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    boxes: dict[str, tuple[int, int, int, int]] = {}
    for index, entity in enumerate(entities):
        row, col = divmod(index, cols)
        x = 70 + col * (node_w + gap_x)
        y = 70 + row * (node_h + gap_y)
        boxes[entity] = (x, y, x + node_w, y + node_h)
    for src, dst, label in edges:
        if src in boxes and dst in boxes:
            sbox, dbox = boxes[src], boxes[dst]
            start = ((sbox[0] + sbox[2]) / 2, (sbox[1] + sbox[3]) / 2)
            end = ((dbox[0] + dbox[2]) / 2, (dbox[1] + dbox[3]) / 2)
            _arrow(draw, start, end, "#64748b")
            mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
            draw.text((mx - 35, my - 18), label, font=FONT_SMALL, fill="#475569")
    for entity, box in boxes.items():
        draw.rounded_rectangle(box, radius=10, fill="#f8fafc", outline="#334155", width=2)
        _draw_center_text(draw, box, entity, FONT_SMALL)
    image.save(out)


def render_source(source: str, out: Path) -> None:
    stripped = source.strip()
    if stripped.startswith("sequenceDiagram"):
        render_sequence(stripped, out)
    elif stripped.startswith("mindmap"):
        render_tree(stripped, out)
    elif stripped.startswith("erDiagram"):
        render_er(stripped, out)
    else:
        render_flowchart(stripped, out)


def render_all(root: Path = ROOT) -> None:
    asset_dir = root / "diagram_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(r"<pre class=\"mermaid\">(.*?)</pre>", re.S)
    for html_path in sorted(root.glob("LiFeO4Agent-*.html")):
        content = html_path.read_text(encoding="utf-8")
        replacements: list[tuple[str, str]] = []
        for index, match in enumerate(pattern.finditer(content), start=1):
            source = html.unescape(match.group(1))
            out_name = f"{html_path.stem}-diagram-{index:02d}.png"
            out_path = asset_dir / out_name
            render_source(source, out_path)
            replacement = (
                f'<p class="no-indent" style="text-align:center;">'
                f'<img src="diagram_assets/{out_name}" style="max-width:100%; width:16cm;" />'
                f"</p>"
            )
            replacements.append((match.group(0), replacement))
        if replacements:
            for old, new in replacements:
                content = content.replace(old, new, 1)
            html_path.write_text(content, encoding="utf-8")
            print(f"rendered {len(replacements)} diagrams in {html_path.name}")


def main() -> None:
    render_all(ROOT)


if __name__ == "__main__":
    main()
