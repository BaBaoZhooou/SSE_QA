from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import math

from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path(__file__).resolve().parent
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

BG = "#ffffff"
FILL = "#f0efff"
STROKE = "#a78bfa"
TEXT = "#3f3f46"
LINE = "#666666"
LABEL_BG = "#f3f4f6"


@dataclass
class Node:
    id: str
    text: str
    x: int
    y: int
    w: int
    h: int
    kind: str = "rect"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size, index=0)


BODY = font(28)
SMALL = font(24)
TITLE = font(36)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        current = ""
        for ch in raw:
            trial = current + ch
            if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines or [""]


def centered_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt: ImageFont.FreeTypeFont = BODY):
    x1, y1, x2, y2 = box
    lines = wrap_text(draw, text, fnt, max(20, x2 - x1 - 28))
    line_h = int(fnt.size * 1.28)
    total_h = line_h * len(lines)
    y = y1 + (y2 - y1 - total_h) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        tw = bbox[2] - bbox[0]
        draw.text((x1 + (x2 - x1 - tw) / 2, y), line, font=fnt, fill=TEXT)
        y += line_h


def draw_node(draw: ImageDraw.ImageDraw, node: Node):
    x, y, w, h = node.x, node.y, node.w, node.h
    if node.kind == "diamond":
        pts = [(x + w // 2, y), (x + w, y + h // 2), (x + w // 2, y + h), (x, y + h // 2)]
        draw.polygon(pts, fill=FILL, outline=STROKE)
        draw.line(pts + [pts[0]], fill=STROKE, width=3)
    elif node.kind == "round":
        draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=FILL, outline=STROKE, width=3)
    else:
        draw.rectangle((x, y, x + w, y + h), fill=FILL, outline=STROKE, width=3)
    centered_text(draw, (x, y, x + w, y + h), node.text)


def anchor(node: Node, side: str) -> tuple[int, int]:
    if side == "top":
        return node.x + node.w // 2, node.y
    if side == "bottom":
        return node.x + node.w // 2, node.y + node.h
    if side == "left":
        return node.x, node.y + node.h // 2
    if side == "right":
        return node.x + node.w, node.y + node.h // 2
    raise ValueError(side)


def arrowhead(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int]):
    x1, y1 = p1
    x2, y2 = p2
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 14
    a1 = ang + math.pi * 0.82
    a2 = ang - math.pi * 0.82
    pts = [
        (x2, y2),
        (x2 + size * math.cos(a1), y2 + size * math.sin(a1)),
        (x2 + size * math.cos(a2), y2 + size * math.sin(a2)),
    ]
    draw.polygon(pts, fill=LINE)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    points: Iterable[tuple[int, int]],
    label: str | None = None,
    label_at: float = 0.5,
):
    pts = list(points)
    for a, b in zip(pts, pts[1:]):
        draw.line((a, b), fill=LINE, width=3)
    arrowhead(draw, pts[-2], pts[-1])
    if label:
        seg_lengths = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
        total = sum(seg_lengths) or 1
        target = total * label_at
        run = 0.0
        lx, ly = pts[0]
        for (a, b), length in zip(zip(pts, pts[1:]), seg_lengths):
            if run + length >= target:
                ratio = (target - run) / max(length, 1)
                lx = a[0] + (b[0] - a[0]) * ratio
                ly = a[1] + (b[1] - a[1]) * ratio
                break
            run += length
        bbox = draw.textbbox((0, 0), label, font=SMALL)
        pad = 6
        draw.rectangle((lx - 6, ly - 17, lx + (bbox[2] - bbox[0]) + pad, ly + 16), fill=LABEL_BG)
        draw.text((lx, ly - 16), label, font=SMALL, fill=TEXT)


def make_canvas(width: int, height: int, title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    draw.text((40, 28), title, font=TITLE, fill=TEXT)
    return img, draw


def render(filename: str, width: int, height: int, title: str, nodes: list[Node], arrows: list[tuple[list[tuple[int, int]], str | None, float]]):
    img, draw = make_canvas(width, height, title)
    for node in nodes:
        draw_node(draw, node)
    for points, label, label_at in arrows:
        draw_arrow(draw, points, label, label_at)
    img.save(OUT_DIR / filename)


def diagram_register():
    nodes = [
        Node("start", "开始", 560, 90, 130, 70, "round"),
        Node("form", "用户填写注册信息\n用户名/密码/工号/姓名/校验码/安全问题", 405, 210, 440, 105),
        Node("u", "验证用户名唯一性", 455, 385, 340, 170, "diamond"),
        Node("uerr", "返回错误提示：用户名已存在", 895, 425, 360, 80),
        Node("p", "校验人员记录\n工号/姓名/校验码", 455, 625, 340, 170, "diamond"),
        Node("perr", "返回错误提示：人员校验失败", 895, 665, 360, 80),
        Node("pwd", "验证密码复杂度", 455, 865, 340, 170, "diamond"),
        Node("pwderr", "返回错误提示：密码不符合策略", 895, 905, 390, 80),
        Node("errend", "结束", 1030, 1110, 130, 70, "round"),
        Node("hash", "哈希密码与安全问题答案", 455, 1110, 340, 80),
        Node("create", "创建用户记录并绑定人员/部门", 455, 1245, 340, 80),
        Node("saveq", "保存安全问题", 455, 1380, 340, 80),
        Node("ok", "返回注册成功", 455, 1515, 340, 80),
        Node("end", "结束", 560, 1660, 130, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "bottom"), anchor(n["form"], "top")], None, 0.5),
        ([anchor(n["form"], "bottom"), anchor(n["u"], "top")], None, 0.5),
        ([anchor(n["u"], "bottom"), anchor(n["p"], "top")], "唯一", 0.25),
        ([anchor(n["u"], "right"), anchor(n["uerr"], "left")], "重复", 0.45),
        ([anchor(n["uerr"], "bottom"), (1075, 1110), anchor(n["errend"], "top")], None, 0.5),
        ([anchor(n["p"], "bottom"), anchor(n["pwd"], "top")], "通过", 0.25),
        ([anchor(n["p"], "right"), anchor(n["perr"], "left")], "失败", 0.45),
        ([anchor(n["perr"], "bottom"), (1075, 1110), anchor(n["errend"], "top")], None, 0.5),
        ([anchor(n["pwd"], "bottom"), anchor(n["hash"], "top")], "符合", 0.25),
        ([anchor(n["pwd"], "right"), anchor(n["pwderr"], "left")], "不符合", 0.45),
        ([anchor(n["pwderr"], "bottom"), anchor(n["errend"], "top")], None, 0.5),
        ([anchor(n["hash"], "bottom"), anchor(n["create"], "top")], None, 0.5),
        ([anchor(n["create"], "bottom"), anchor(n["saveq"], "top")], None, 0.5),
        ([anchor(n["saveq"], "bottom"), anchor(n["ok"], "top")], None, 0.5),
        ([anchor(n["ok"], "bottom"), anchor(n["end"], "top")], None, 0.5),
    ]
    render("01-用户注册流程.png", 1320, 1780, "用户注册流程", nodes, arrows)


def diagram_login():
    nodes = [
        Node("start", "开始", 590, 90, 130, 70, "round"),
        Node("input", "用户输入用户名和密码", 465, 220, 380, 80),
        Node("lock", "检查账户状态\n是否启用/是否锁定", 500, 385, 310, 170, "diamond"),
        Node("locked", "返回账户状态错误\n或锁定到期时间", 80, 1180, 380, 90),
        Node("verify", "验证用户名和密码", 775, 640, 310, 170, "diamond"),
        Node("inc", "增加失败计数", 1120, 690, 260, 80),
        Node("record_fail", "记录失败尝试", 1120, 820, 260, 80),
        Node("threshold", "是否达到锁定阈值", 1065, 975, 310, 170, "diamond"),
        Node("lock30", "锁定账户30分钟", 930, 1220, 280, 80),
        Node("failret", "返回失败信息和剩余次数", 1060, 1370, 360, 80),
        Node("reset", "重置失败计数", 520, 770, 280, 80),
        Node("token", "生成认证 Token", 520, 905, 280, 80),
        Node("profile", "返回用户信息\n首次登录/人员/部门补全状态", 470, 1040, 380, 100),
        Node("end", "结束", 595, 1510, 130, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "bottom"), anchor(n["input"], "top")], None, 0.5),
        ([anchor(n["input"], "bottom"), anchor(n["lock"], "top")], None, 0.5),
        ([anchor(n["lock"], "left"), (270, 470), (270, 1180), anchor(n["locked"], "top")], "禁用/已锁定", 0.45),
        ([anchor(n["locked"], "bottom"), (270, 1550), anchor(n["end"], "left")], None, 0.5),
        ([anchor(n["lock"], "right"), (930, 470), anchor(n["verify"], "top")], "正常", 0.35),
        ([anchor(n["verify"], "left"), (660, 725), anchor(n["reset"], "top")], "成功", 0.5),
        ([anchor(n["reset"], "bottom"), anchor(n["token"], "top")], None, 0.5),
        ([anchor(n["token"], "bottom"), anchor(n["profile"], "top")], None, 0.5),
        ([anchor(n["profile"], "bottom"), anchor(n["end"], "top")], None, 0.5),
        ([anchor(n["verify"], "right"), anchor(n["inc"], "left")], "失败", 0.45),
        ([anchor(n["inc"], "bottom"), anchor(n["record_fail"], "top")], None, 0.5),
        ([anchor(n["record_fail"], "bottom"), anchor(n["threshold"], "top")], None, 0.5),
        ([anchor(n["threshold"], "left"), anchor(n["lock30"], "top")], "是", 0.45),
        ([anchor(n["lock30"], "bottom"), anchor(n["failret"], "left")], None, 0.5),
        ([anchor(n["threshold"], "right"), anchor(n["failret"], "top")], "否", 0.45),
        ([anchor(n["failret"], "bottom"), (1240, 1550), anchor(n["end"], "right")], None, 0.5),
    ]
    render("02-用户登录流程.png", 1480, 1630, "用户登录流程", nodes, arrows)


def diagram_qa_stream():
    nodes = [
        Node("start", "开始", 600, 90, 130, 70, "round"),
        Node("ask", "用户输入问题\n选择 fast/thinking/patent 模式", 430, 220, 470, 95),
        Node("valid", "验证登录态\n参数与配额", 500, 395, 330, 170, "diamond"),
        Node("err", "返回错误提示\n未登录/参数错误/配额不足", 70, 515, 390, 100),
        Node("conv", "读取或创建会话", 500, 650, 330, 80),
        Node("file", "解析会话文件上下文\nPDF/Excel/CSV", 500, 785, 330, 90),
        Node("route", "gateway 根据模式路由", 500, 935, 330, 80),
        Node("target", "转发到 QA 服务\nfastQA / highThinkingQA / patent", 430, 1070, 470, 95),
        Node("retrieve", "检索向量库、Neo4j 图谱和 MinIO 原文", 430, 1225, 470, 95),
        Node("llm", "调用模型生成回答", 500, 1380, 330, 80),
        Node("stream", "SSE 流式返回内容", 500, 1515, 330, 80),
        Node("save", "保存消息与引用 metadata", 500, 1650, 330, 80),
        Node("done", "前端展示回答与引用", 500, 1785, 330, 80),
        Node("end", "结束", 600, 1940, 130, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "bottom"), anchor(n["ask"], "top")], None, 0.5),
        ([anchor(n["ask"], "bottom"), anchor(n["valid"], "top")], None, 0.5),
        ([anchor(n["valid"], "left"), anchor(n["err"], "right")], "失败", 0.45),
        ([anchor(n["err"], "bottom"), (265, 1975), anchor(n["end"], "left")], None, 0.5),
        ([anchor(n["valid"], "bottom"), anchor(n["conv"], "top")], "通过", 0.2),
        ([anchor(n["conv"], "bottom"), anchor(n["file"], "top")], None, 0.5),
        ([anchor(n["file"], "bottom"), anchor(n["route"], "top")], None, 0.5),
        ([anchor(n["route"], "bottom"), anchor(n["target"], "top")], None, 0.5),
        ([anchor(n["target"], "bottom"), anchor(n["retrieve"], "top")], None, 0.5),
        ([anchor(n["retrieve"], "bottom"), anchor(n["llm"], "top")], None, 0.5),
        ([anchor(n["llm"], "bottom"), anchor(n["stream"], "top")], None, 0.5),
        ([anchor(n["stream"], "bottom"), anchor(n["save"], "top")], None, 0.5),
        ([anchor(n["save"], "bottom"), anchor(n["done"], "top")], None, 0.5),
        ([anchor(n["done"], "bottom"), anchor(n["end"], "top")], None, 0.5),
    ]
    render("03-智能问答流式处理流程.png", 1180, 2060, "智能问答流式处理流程", nodes, arrows)


def diagram_file_upload():
    nodes = [
        Node("start", "用户选择文件\nPDF / Excel / CSV", 490, 90, 360, 90),
        Node("valid", "验证文件类型/大小", 520, 270, 300, 170, "diamond"),
        Node("user", "获取当前用户和会话信息", 490, 540, 360, 80),
        Node("minio", "上传文件到 MinIO", 490, 670, 360, 80),
        Node("meta", "记录文件元数据\nconversation_files", 160, 820, 360, 90),
        Node("ok", "返回上传成功\n文件可参与问答", 160, 970, 360, 90),
        Node("uperr", "返回错误：上传失败", 700, 920, 330, 80),
        Node("verr", "返回错误：验证失败", 930, 540, 330, 80),
        Node("end", "结束", 570, 1140, 130, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "bottom"), anchor(n["valid"], "top")], None, 0.5),
        ([anchor(n["valid"], "bottom"), anchor(n["user"], "top")], "通过", 0.2),
        ([anchor(n["valid"], "right"), (1095, 355), anchor(n["verr"], "top")], "失败", 0.45),
        ([anchor(n["user"], "bottom"), anchor(n["minio"], "top")], None, 0.5),
        ([anchor(n["minio"], "left"), anchor(n["meta"], "top")], "成功", 0.45),
        ([anchor(n["meta"], "bottom"), anchor(n["ok"], "top")], None, 0.5),
        ([anchor(n["ok"], "bottom"), (340, 1175), anchor(n["end"], "left")], None, 0.5),
        ([anchor(n["minio"], "right"), anchor(n["uperr"], "top")], "失败", 0.45),
        ([anchor(n["uperr"], "bottom"), (865, 1175), anchor(n["end"], "right")], None, 0.5),
        ([anchor(n["verr"], "bottom"), (1095, 1175), anchor(n["end"], "right")], None, 0.5),
    ]
    render("04-文件上传流程.png", 1300, 1270, "文件上传流程", nodes, arrows)


def diagram_kb_build():
    nodes = [
        Node("start", "开始", 520, 90, 130, 70, "round"),
        Node("src", "准备论文/专利原文数据", 390, 220, 390, 80),
        Node("valid", "校验原文路径\nDOI/专利号/文件完整性", 425, 380, 320, 170, "diamond"),
        Node("extract", "信息提取\n段落/表格/图片说明/metadata", 390, 640, 390, 95),
        Node("clean", "文本清洗与结构化", 390, 795, 390, 80),
        Node("vector", "制作向量数据库\n切分/Embedding/索引", 390, 930, 390, 95),
        Node("graph", "制作知识图谱\n实体/关系/Neo4j dump", 390, 1090, 390, 95),
        Node("pkg", "打包 deploy/data 数据包", 390, 1250, 390, 80),
        Node("seed", "部署时 seed job 自动导入", 390, 1385, 390, 80),
        Node("ok", "问答服务可检索使用", 390, 1520, 390, 80),
        Node("err", "返回/记录错误：数据无效", 835, 650, 360, 80),
        Node("end", "流程结束", 520, 1680, 130, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "bottom"), anchor(n["src"], "top")], None, 0.5),
        ([anchor(n["src"], "bottom"), anchor(n["valid"], "top")], None, 0.5),
        ([anchor(n["valid"], "bottom"), anchor(n["extract"], "top")], "有效", 0.25),
        ([anchor(n["valid"], "right"), anchor(n["err"], "top")], "无效", 0.45),
        ([anchor(n["err"], "bottom"), (1015, 1715), anchor(n["end"], "right")], None, 0.5),
        ([anchor(n["extract"], "bottom"), anchor(n["clean"], "top")], None, 0.5),
        ([anchor(n["clean"], "bottom"), anchor(n["vector"], "top")], None, 0.5),
        ([anchor(n["vector"], "bottom"), anchor(n["graph"], "top")], None, 0.5),
        ([anchor(n["graph"], "bottom"), anchor(n["pkg"], "top")], None, 0.5),
        ([anchor(n["pkg"], "bottom"), anchor(n["seed"], "top")], None, 0.5),
        ([anchor(n["seed"], "bottom"), anchor(n["ok"], "top")], None, 0.5),
        ([anchor(n["ok"], "bottom"), anchor(n["end"], "top")], None, 0.5),
    ]
    render("05-知识库数据加工流程.png", 1220, 1800, "知识库数据加工流程", nodes, arrows)


def diagram_admin_reset_password():
    nodes = [
        Node("select", "管理员选择用户", 50, 170, 240, 70),
        Node("click", "点击重置密码按钮", 350, 170, 280, 70),
        Node("confirm", "弹出确认框", 690, 120, 170, 170, "diamond"),
        Node("gen", "生成临时密码", 930, 170, 260, 70),
        Node("hash", "哈希后更新用户密码", 1250, 170, 320, 70),
        Node("flag", "设置首次登录强制改密", 1630, 170, 320, 70),
        Node("log", "记录管理员操作", 2010, 170, 300, 70),
        Node("show", "前端显示重置结果", 2370, 170, 300, 70),
        Node("end", "流程结束", 2730, 170, 170, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["select"], "right"), anchor(n["click"], "left")], None, 0.5),
        ([anchor(n["click"], "right"), anchor(n["confirm"], "left")], None, 0.5),
        ([anchor(n["confirm"], "right"), anchor(n["gen"], "left")], "确认", 0.45),
        ([anchor(n["confirm"], "top"), (780, 55), (2815, 55), anchor(n["end"], "top")], "取消", 0.45),
        ([anchor(n["gen"], "right"), anchor(n["hash"], "left")], None, 0.5),
        ([anchor(n["hash"], "right"), anchor(n["flag"], "left")], None, 0.5),
        ([anchor(n["flag"], "right"), anchor(n["log"], "left")], None, 0.5),
        ([anchor(n["log"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("06-管理员重置密码流程.png", 2960, 360, "管理员重置密码流程", nodes, arrows)


def diagram_admin_user_status():
    nodes = [
        Node("select", "管理员选择用户", 50, 150, 240, 70),
        Node("click", "点击启用/禁用\n或清除锁定状态", 350, 135, 300, 100),
        Node("perm", "校验管理员权限", 720, 150, 280, 70),
        Node("update", "更新 users 状态\nstatus/locked_until/失败次数", 1070, 135, 390, 100),
        Node("log", "记录操作日志", 1530, 150, 280, 70),
        Node("ret", "返回操作成功", 1870, 150, 280, 70),
        Node("show", "前端刷新用户列表", 2210, 150, 300, 70),
        Node("end", "流程结束", 2570, 150, 170, 70, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["select"], "right"), anchor(n["click"], "left")], None, 0.5),
        ([anchor(n["click"], "right"), anchor(n["perm"], "left")], None, 0.5),
        ([anchor(n["perm"], "right"), anchor(n["update"], "left")], None, 0.5),
        ([anchor(n["update"], "right"), anchor(n["log"], "left")], None, 0.5),
        ([anchor(n["log"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("07-管理员用户状态维护流程.png", 2800, 340, "管理员用户状态维护流程", nodes, arrows)


def diagram_public_reference_list():
    nodes = [
        Node("start", "用户进入公共知识库\n或引用面板", 40, 160, 300, 90),
        Node("frontend", "frontend-vue 发起\nreference_preview 查询", 420, 160, 360, 90),
        Node("gateway", "gateway 透明代理\n公共文档接口", 860, 160, 320, 90),
        Node("service", "public-service documents\n归一化 DOI / 限制条数", 1260, 145, 390, 120),
        Node("query", "查询 Neo4j / Chroma\n并检查 PDF 可用性", 1730, 145, 390, 120),
        Node("ret", "返回引用预览列表\n标题/作者/DOI/PDF状态", 2200, 145, 390, 120),
        Node("show", "前端展示公共文献列表", 2670, 160, 340, 90),
        Node("end", "流程结束", 3090, 160, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "right"), anchor(n["frontend"], "left")], None, 0.5),
        ([anchor(n["frontend"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["service"], "left")], None, 0.5),
        ([anchor(n["service"], "right"), anchor(n["query"], "left")], None, 0.5),
        ([anchor(n["query"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("08-公共知识库引用列表查询流程.png", 3320, 430, "公共知识库引用列表查询流程", nodes, arrows)


def diagram_public_document_detail():
    nodes = [
        Node("click", "用户点击文献\n或引用条目", 30, 170, 280, 90),
        Node("frontend", "frontend-vue 发送详情请求\nliterature_content / view_pdf", 390, 155, 430, 120),
        Node("gateway", "gateway 转发到\npublic-service", 900, 170, 310, 90),
        Node("service", "documents_service\n解析 DOI / 文档标识", 1290, 155, 360, 120),
        Node("meta", "查询图谱元数据\nNeo4j / Chroma fallback", 1730, 155, 400, 120),
        Node("asset", "检查 MinIO / 本地 papers\nPDF 是否可访问", 2210, 155, 410, 120),
        Node("ret", "返回文献详情\n摘要/引用/PDF链接", 2700, 155, 360, 120),
        Node("reader", "前端打开详情\n或 PdfReader 预览", 3140, 155, 360, 120),
        Node("end", "流程结束", 3580, 170, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["click"], "right"), anchor(n["frontend"], "left")], None, 0.5),
        ([anchor(n["frontend"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["service"], "left")], None, 0.5),
        ([anchor(n["service"], "right"), anchor(n["meta"], "left")], None, 0.5),
        ([anchor(n["meta"], "right"), anchor(n["asset"], "left")], None, 0.5),
        ([anchor(n["asset"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["reader"], "left")], None, 0.5),
        ([anchor(n["reader"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("09-公共文献详情与PDF预览流程.png", 3810, 450, "公共文献详情与 PDF 预览流程", nodes, arrows)


def diagram_document_assist_refresh():
    nodes = [
        Node("action", "用户点击摘要/翻译\n或刷新引用预览", 30, 240, 330, 100),
        Node("frontend", "前端整理请求参数\nDOI / 文本 / 文档ID", 440, 240, 370, 100),
        Node("quota", "校验登录态与配额", 890, 205, 280, 170, "diamond"),
        Node("deny", "返回未登录\n或配额不足", 780, 500, 300, 90),
        Node("valid", "校验参数格式", 1260, 205, 280, 170, "diamond"),
        Node("bad", "返回参数错误提示", 1260, 500, 300, 90),
        Node("gateway", "gateway 转发公共文档请求", 1620, 240, 360, 90),
        Node("service", "documents_service\n摘要/翻译/引用预览处理", 2060, 225, 390, 120),
        Node("cache", "读取或写入缓存\nMinIO / 本地缓存", 2530, 225, 360, 120),
        Node("llm", "必要时调用模型服务", 2970, 240, 330, 90),
        Node("ret", "返回处理结果", 3380, 240, 280, 90),
        Node("show", "前端刷新结果展示", 3740, 240, 320, 90),
        Node("end", "流程结束", 4140, 240, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["action"], "right"), anchor(n["frontend"], "left")], None, 0.5),
        ([anchor(n["frontend"], "right"), anchor(n["quota"], "left")], None, 0.5),
        ([anchor(n["quota"], "bottom"), anchor(n["deny"], "top")], "失败", 0.35),
        ([anchor(n["deny"], "right"), (4230, 545), anchor(n["end"], "bottom")], None, 0.55),
        ([anchor(n["quota"], "right"), anchor(n["valid"], "left")], "通过", 0.45),
        ([anchor(n["valid"], "bottom"), anchor(n["bad"], "top")], "无效", 0.35),
        ([anchor(n["bad"], "right"), (4230, 545), anchor(n["end"], "bottom")], None, 0.55),
        ([anchor(n["valid"], "right"), anchor(n["gateway"], "left")], "有效", 0.45),
        ([anchor(n["gateway"], "right"), anchor(n["service"], "left")], None, 0.5),
        ([anchor(n["service"], "right"), anchor(n["cache"], "left")], None, 0.5),
        ([anchor(n["cache"], "right"), anchor(n["llm"], "left")], "缓存未命中", 0.45),
        ([anchor(n["llm"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["cache"], "bottom"), (2710, 680), (3520, 680), anchor(n["ret"], "bottom")], "缓存命中", 0.35),
        ([anchor(n["ret"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("10-文档辅助结果刷新流程.png", 4360, 750, "文档辅助结果刷新流程", nodes, arrows)


def diagram_private_conversation_file_list():
    nodes = [
        Node("start", "用户进入会话\n文件列表区域", 40, 185, 300, 90),
        Node("auth", "从 Token 获取\n当前用户ID", 420, 145, 260, 170, "diamond"),
        Node("fail", "获取失败：前端提示\n登录失效并引导重新登录", 760, 365, 430, 100),
        Node("frontend", "frontend-vue 请求\n/api/conversations/{id}/files", 760, 145, 430, 120),
        Node("gateway", "gateway 转发到\npublic-service conversation", 1270, 160, 420, 90),
        Node("query", "后端按 user_id + conversation_id\n读取 conversation_files / JSON", 1770, 145, 520, 120),
        Node("ret", "返回当前用户会话文件列表", 2370, 160, 400, 90),
        Node("show", "前端展示文件状态\nuploaded/parsing/ready/failed", 2850, 145, 520, 120),
        Node("end", "流程结束", 3450, 160, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "right"), anchor(n["auth"], "left")], None, 0.5),
        ([anchor(n["auth"], "right"), anchor(n["frontend"], "left")], None, 0.5),
        ([anchor(n["auth"], "bottom"), anchor(n["fail"], "top")], "获取失败", 0.45),
        ([anchor(n["fail"], "right"), (3535, 415), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["frontend"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["query"], "left")], None, 0.5),
        ([anchor(n["query"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("11-会话文件列表查询流程.png", 3670, 560, "会话文件列表查询流程", nodes, arrows)


def diagram_private_conversation_file_auth():
    nodes = [
        Node("request", "用户请求文件详情\n或下载文件", 40, 270, 330, 100),
        Node("auth", "从 Token 获取\n当前用户ID", 450, 270, 330, 90),
        Node("query", "查询会话与文件记录\nconversation_id / file_id", 860, 270, 390, 90),
        Node("match", "校验记录 user_id\n是否等于当前用户ID", 1320, 185, 330, 260, "diamond"),
        Node("deny", "返回 403 Forbidden\n或 404 Not Found", 1820, 140, 360, 90),
        Node("load", "继续读取文件元数据\nJSON 主文档 / MinIO", 1820, 390, 360, 110),
        Node("ret", "返回文件详情\n或下载响应", 2260, 390, 320, 90),
        Node("end", "流程结束", 2660, 265, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["request"], "right"), anchor(n["auth"], "left")], None, 0.5),
        ([anchor(n["auth"], "right"), anchor(n["query"], "left")], None, 0.5),
        ([anchor(n["query"], "right"), anchor(n["match"], "left")], None, 0.5),
        ([anchor(n["match"], "right"), anchor(n["deny"], "left")], "不匹配", 0.38),
        ([anchor(n["deny"], "right"), (2745, 185), anchor(n["end"], "top")], None, 0.45),
        ([anchor(n["match"], "bottom"), anchor(n["load"], "left")], "匹配", 0.45),
        ([anchor(n["load"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("12-会话文件权限校验流程.png", 2890, 650, "会话文件权限校验流程", nodes, arrows)


def diagram_conversation_upload_submit():
    nodes = [
        Node("select", "用户选择文件\nPDF / Excel / CSV", 40, 190, 300, 90),
        Node("conv", "确认当前会话ID", 420, 190, 270, 90),
        Node("click", "点击上传按钮", 770, 190, 240, 90),
        Node("valid", "校验文件类型\n和上传上下文", 1090, 110, 320, 250, "diamond"),
        Node("save", "保存到本地 uploads", 1500, 190, 300, 90),
        Node("mirror", "镜像上传到 MinIO", 1880, 190, 300, 90),
        Node("meta", "写入 conversation_files\n并更新会话 JSON", 2260, 170, 390, 130),
        Node("task", "提交上传处理 Worker\n异步解析任务", 2730, 170, 420, 130),
        Node("ret", "返回 file_id\n和初始处理状态", 3230, 170, 330, 130),
        Node("bad", "返回错误\n类型不支持/缺少会话", 1500, 430, 360, 100),
        Node("storage_err", "返回错误\n对象存储不可用", 2260, 430, 360, 100),
        Node("end", "流程结束", 3640, 190, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["select"], "right"), anchor(n["conv"], "left")], None, 0.5),
        ([anchor(n["conv"], "right"), anchor(n["click"], "left")], None, 0.5),
        ([anchor(n["click"], "right"), anchor(n["valid"], "left")], None, 0.5),
        ([anchor(n["valid"], "right"), anchor(n["save"], "left")], "通过", 0.45),
        ([anchor(n["valid"], "bottom"), anchor(n["bad"], "top")], "失败", 0.35),
        ([anchor(n["bad"], "right"), (3725, 480), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["save"], "right"), anchor(n["mirror"], "left")], None, 0.5),
        ([anchor(n["mirror"], "right"), anchor(n["meta"], "left")], "成功", 0.45),
        ([anchor(n["mirror"], "bottom"), anchor(n["storage_err"], "top")], "失败", 0.35),
        ([anchor(n["storage_err"], "right"), (3725, 480), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["meta"], "right"), anchor(n["task"], "left")], None, 0.5),
        ([anchor(n["task"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("13-会话文件上传与处理任务提交流程.png", 3860, 620, "会话文件上传与处理任务提交流程", nodes, arrows)


def diagram_upload_processing_worker():
    nodes = [
        Node("start", "异步解析任务启动", 40, 190, 280, 90),
        Node("lock", "获取 Redis/MySQL\n文件处理锁", 400, 170, 320, 130),
        Node("file", "解析本地文件\n或从 MinIO 临时取回", 800, 170, 390, 130),
        Node("valid", "识别文件类型\nPDF / Excel / CSV", 1270, 105, 320, 250, "diamond"),
        Node("parse", "解析内容\nPDF文本/表格列和样例行", 1680, 170, 420, 130),
        Node("parsed", "更新 parse_status=parsed\n写入 file_meta", 2180, 170, 390, 130),
        Node("indexing", "更新索引状态\nindexing", 2650, 190, 370, 90),
        Node("ready", "标记 ready\nindex_mode=deferred", 3100, 170, 360, 130),
        Node("ret", "前端轮询/刷新\n显示 ready 状态", 3540, 170, 360, 130),
        Node("fail", "更新 failed\n记录 last_error", 2180, 430, 360, 100),
        Node("end", "流程结束", 3980, 190, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["start"], "right"), anchor(n["lock"], "left")], None, 0.5),
        ([anchor(n["lock"], "right"), anchor(n["file"], "left")], None, 0.5),
        ([anchor(n["file"], "right"), anchor(n["valid"], "left")], None, 0.5),
        ([anchor(n["valid"], "right"), anchor(n["parse"], "left")], "支持", 0.45),
        ([anchor(n["parse"], "right"), anchor(n["parsed"], "left")], None, 0.5),
        ([anchor(n["parsed"], "right"), anchor(n["indexing"], "left")], None, 0.5),
        ([anchor(n["indexing"], "right"), anchor(n["ready"], "left")], None, 0.5),
        ([anchor(n["ready"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["end"], "left")], None, 0.5),
        ([anchor(n["valid"], "bottom"), (1430, 480), anchor(n["fail"], "left")], "不支持/解析失败", 0.45),
        ([anchor(n["fail"], "right"), (4065, 480), anchor(n["end"], "bottom")], None, 0.5),
    ]
    render("14-上传文件解析与索引状态更新流程.png", 4200, 620, "上传文件解析与索引状态更新流程", nodes, arrows)


def diagram_admin_batch_import():
    nodes = [
        Node("type", "管理员选择导入类型\n用户/人员/部门", 40, 190, 340, 100),
        Node("template", "下载并填写模板\nxlsx / csv", 460, 190, 320, 100),
        Node("upload", "上传批量导入文件", 860, 205, 300, 70),
        Node("gateway", "gateway 转发\n/api/admin/*/batch-import", 1240, 190, 420, 100),
        Node("parse", "public-service 解析表格\nload_rows", 1740, 190, 370, 100),
        Node("valid", "校验必填列\n和重复记录", 2190, 120, 300, 240, "diamond"),
        Node("write", "批量写入 MySQL\nusers/personnel/departments", 2580, 180, 460, 120),
        Node("summary", "生成导入结果\n成功/失败/跳过", 3120, 180, 380, 120),
        Node("show", "前端展示结果弹窗\n可下载失败记录", 3580, 180, 410, 120),
        Node("bad", "返回错误明细\n行号/原因", 2580, 430, 330, 100),
        Node("end", "流程结束", 4070, 195, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["type"], "right"), anchor(n["template"], "left")], None, 0.5),
        ([anchor(n["template"], "right"), anchor(n["upload"], "left")], None, 0.5),
        ([anchor(n["upload"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["parse"], "left")], None, 0.5),
        ([anchor(n["parse"], "right"), anchor(n["valid"], "left")], None, 0.5),
        ([anchor(n["valid"], "right"), anchor(n["write"], "left")], "通过", 0.45),
        ([anchor(n["valid"], "bottom"), anchor(n["bad"], "top")], "失败", 0.35),
        ([anchor(n["bad"], "right"), (4155, 480), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["write"], "right"), anchor(n["summary"], "left")], None, 0.5),
        ([anchor(n["summary"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("15-管理数据批量导入流程.png", 4290, 620, "管理数据批量导入流程", nodes, arrows)


def diagram_conversation_file_download():
    nodes = [
        Node("click", "用户点击文件下载按钮", 40, 190, 330, 90),
        Node("frontend", "前端拼接会话文件\n下载接口地址", 450, 170, 560, 130),
        Node("gateway", "gateway 代理到\npublic-service conversation", 1090, 180, 430, 110),
        Node("auth", "校验用户归属\n和 file_view 配额", 1600, 115, 320, 240, "diamond"),
        Node("resolve", "resolve_download\n读取 storage_ref/local_path", 2010, 170, 430, 130),
        Node("minio", "MinIO 文件生成临时副本\n或返回本地文件", 2520, 170, 450, 130),
        Node("header", "设置 Content-Disposition\n并返回 FileResponse", 3050, 170, 430, 130),
        Node("client", "浏览器触发下载", 3560, 190, 300, 90),
        Node("deny", "返回 403/404/配额错误", 2010, 430, 360, 100),
        Node("end", "流程结束", 3940, 190, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["click"], "right"), anchor(n["frontend"], "left")], None, 0.5),
        ([anchor(n["frontend"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["auth"], "left")], None, 0.5),
        ([anchor(n["auth"], "right"), anchor(n["resolve"], "left")], "通过", 0.45),
        ([anchor(n["auth"], "bottom"), anchor(n["deny"], "top")], "失败", 0.35),
        ([anchor(n["deny"], "right"), (4025, 480), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["resolve"], "right"), anchor(n["minio"], "left")], None, 0.5),
        ([anchor(n["minio"], "right"), anchor(n["header"], "left")], None, 0.5),
        ([anchor(n["header"], "right"), anchor(n["client"], "left")], None, 0.5),
        ([anchor(n["client"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("16-会话文件下载流程.png", 4160, 620, "会话文件下载流程", nodes, arrows)


def diagram_recoverable_qa_task_start():
    nodes = [
        Node("config", "用户输入问题\n选择 fast/thinking/patent", 40, 190, 390, 100),
        Node("files", "选择会话文件\n或公共知识库范围", 510, 190, 360, 100),
        Node("click", "点击发送问题", 950, 205, 260, 70),
        Node("valid", "校验参数、登录态\n和配额预检查", 1290, 110, 320, 250, "diamond"),
        Node("route", "gateway 路由决策\nfile_qa / kb_qa / patent", 1700, 180, 420, 120),
        Node("task", "创建 task_id\n写入队列状态", 2200, 180, 360, 120),
        Node("turn", "public-service 创建会话轮次\nuser/assistant 占位消息", 2640, 170, 500, 140),
        Node("dispatch", "Admission worker\n调度后端执行", 3220, 180, 380, 120),
        Node("ret", "返回 task_id\n和 queued 状态", 3680, 180, 320, 120),
        Node("bad", "返回错误\n参数不合法/配额不足", 1700, 430, 360, 100),
        Node("end", "流程结束", 4080, 195, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["config"], "right"), anchor(n["files"], "left")], None, 0.5),
        ([anchor(n["files"], "right"), anchor(n["click"], "left")], None, 0.5),
        ([anchor(n["click"], "right"), anchor(n["valid"], "left")], None, 0.5),
        ([anchor(n["valid"], "right"), anchor(n["route"], "left")], "通过", 0.45),
        ([anchor(n["valid"], "bottom"), anchor(n["bad"], "top")], "失败", 0.35),
        ([anchor(n["bad"], "right"), (4165, 480), anchor(n["end"], "bottom")], None, 0.5),
        ([anchor(n["route"], "right"), anchor(n["task"], "left")], None, 0.5),
        ([anchor(n["task"], "right"), anchor(n["turn"], "left")], None, 0.5),
        ([anchor(n["turn"], "right"), anchor(n["dispatch"], "left")], None, 0.5),
        ([anchor(n["dispatch"], "right"), anchor(n["ret"], "left")], None, 0.5),
        ([anchor(n["ret"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("17-可恢复问答任务启动流程.png", 4300, 620, "可恢复问答任务启动流程", nodes, arrows)


def diagram_graph_enhanced_query():
    nodes = [
        Node("ask", "用户提出图谱相关问题\n文献/深度/专利模式", 40, 190, 410, 100),
        Node("gateway", "gateway 路由到\nfastQA / patentQA", 530, 190, 360, 100),
        Node("classify", "识别是否需要图谱增强", 970, 115, 300, 250, "diamond"),
        Node("planner", "构建图谱查询计划\n模板/参数化 Cypher", 1360, 180, 410, 120),
        Node("guard", "执行 Cypher 安全检查\n只允许受控只读查询", 1850, 180, 430, 120),
        Node("neo4j", "查询 Neo4j\n文献图谱或专利图谱", 2360, 180, 390, 120),
        Node("canon", "规范化图谱结果\nDOI/实体/事实/约束", 2830, 180, 420, 120),
        Node("rag", "转成 RAG 证据\n或直接回答素材", 3330, 180, 390, 120),
        Node("answer", "合并向量检索结果\n生成答案和引用", 3800, 180, 410, 120),
        Node("show", "前端展示阶段、回答\n和引用入口", 4290, 180, 390, 120),
        Node("skip", "跳过图谱\n走常规向量检索", 1360, 430, 360, 100),
        Node("fallback", "图谱不可用或无结果\n降级向量检索", 2360, 430, 390, 100),
        Node("end", "流程结束", 4760, 195, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["ask"], "right"), anchor(n["gateway"], "left")], None, 0.5),
        ([anchor(n["gateway"], "right"), anchor(n["classify"], "left")], None, 0.5),
        ([anchor(n["classify"], "right"), anchor(n["planner"], "left")], "需要", 0.45),
        ([anchor(n["classify"], "bottom"), anchor(n["skip"], "top")], "不需要", 0.35),
        ([anchor(n["skip"], "right"), (4005, 480), anchor(n["answer"], "bottom")], None, 0.5),
        ([anchor(n["planner"], "right"), anchor(n["guard"], "left")], None, 0.5),
        ([anchor(n["guard"], "right"), anchor(n["neo4j"], "left")], None, 0.5),
        ([anchor(n["neo4j"], "right"), anchor(n["canon"], "left")], "命中", 0.45),
        ([anchor(n["neo4j"], "bottom"), anchor(n["fallback"], "top")], "失败/空结果", 0.35),
        ([anchor(n["fallback"], "right"), (4005, 480), anchor(n["answer"], "bottom")], None, 0.5),
        ([anchor(n["canon"], "right"), anchor(n["rag"], "left")], None, 0.5),
        ([anchor(n["rag"], "right"), anchor(n["answer"], "left")], None, 0.5),
        ([anchor(n["answer"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("18-图谱增强查询流程.png", 4980, 620, "图谱增强查询流程", nodes, arrows)


def diagram_graph_relationship_evidence():
    nodes = [
        Node("focus", "问题命中 DOI、材料\n工艺或性能实体", 40, 190, 390, 100),
        Node("slots", "抽取图谱槽位\nDOI/材料/工艺/性能", 510, 180, 390, 120),
        Node("template", "选择关系展开模板\nlookup / expand / list", 980, 180, 410, 120),
        Node("cypher", "生成候选 Cypher\n和查询参数", 1470, 180, 360, 120),
        Node("neo4j", "执行 Neo4j 邻域查询", 1910, 195, 340, 90),
        Node("collect", "汇总关联节点和关系\n标题/原料/工艺/测试/性能", 2330, 170, 470, 140),
        Node("quality", "过滤异常 DOI\n去重并规范化证据", 2880, 180, 430, 120),
        Node("context", "形成图谱事实块\n和引用候选 DOI", 3390, 180, 390, 120),
        Node("merge", "并入检索上下文\n或直接渲染答案", 3860, 180, 390, 120),
        Node("show", "前端展示引用、原文入口\n和图谱增强结论", 4330, 170, 440, 140),
        Node("empty", "无关系结果\n回退 Chroma/常规检索", 2330, 430, 410, 100),
        Node("end", "流程结束", 4850, 195, 170, 90, "round"),
    ]
    n = {x.id: x for x in nodes}
    arrows = [
        ([anchor(n["focus"], "right"), anchor(n["slots"], "left")], None, 0.5),
        ([anchor(n["slots"], "right"), anchor(n["template"], "left")], None, 0.5),
        ([anchor(n["template"], "right"), anchor(n["cypher"], "left")], None, 0.5),
        ([anchor(n["cypher"], "right"), anchor(n["neo4j"], "left")], None, 0.5),
        ([anchor(n["neo4j"], "right"), anchor(n["collect"], "left")], "命中", 0.45),
        ([anchor(n["neo4j"], "bottom"), anchor(n["empty"], "top")], "无结果", 0.35),
        ([anchor(n["empty"], "right"), (4055, 480), anchor(n["merge"], "bottom")], None, 0.5),
        ([anchor(n["collect"], "right"), anchor(n["quality"], "left")], None, 0.5),
        ([anchor(n["quality"], "right"), anchor(n["context"], "left")], None, 0.5),
        ([anchor(n["context"], "right"), anchor(n["merge"], "left")], None, 0.5),
        ([anchor(n["merge"], "right"), anchor(n["show"], "left")], None, 0.5),
        ([anchor(n["show"], "right"), anchor(n["end"], "left")], None, 0.5),
    ]
    render("19-图谱关系证据展开流程.png", 5070, 620, "图谱关系证据展开流程", nodes, arrows)


def main():
    diagram_register()
    diagram_login()
    diagram_qa_stream()
    diagram_file_upload()
    diagram_kb_build()
    diagram_admin_reset_password()
    diagram_admin_user_status()
    diagram_public_reference_list()
    diagram_public_document_detail()
    diagram_document_assist_refresh()
    diagram_private_conversation_file_list()
    diagram_private_conversation_file_auth()
    diagram_conversation_upload_submit()
    diagram_upload_processing_worker()
    diagram_admin_batch_import()
    diagram_conversation_file_download()
    diagram_recoverable_qa_task_start()
    diagram_graph_enhanced_query()
    diagram_graph_relationship_evidence()
    print(f"Generated PNG files in {OUT_DIR}")


if __name__ == "__main__":
    main()
