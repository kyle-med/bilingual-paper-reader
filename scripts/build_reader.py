#!/usr/bin/env python3
import argparse
import base64
import html
import json
import mimetypes
import re
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent


def esc(value):
    return html.escape(str(value or ""), quote=True)


def resolve(base, value):
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def validate(data, base):
    required = ["paper_id", "title", "authors", "journal", "source_pdf", "sections"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    if not resolve(base, data["source_pdf"]).is_file():
        raise FileNotFoundError(f"Source PDF not found: {data['source_pdf']}")
    ids, figures = set(), set()
    for section in data["sections"]:
        for key in ("id", "heading_en", "heading_zh", "note_zh"):
            if not section.get(key):
                raise ValueError(f"Section is missing {key}: {section.get('id', '<unknown>')}")
        if "blocks" not in section or not isinstance(section["blocks"], list):
            raise ValueError(f"Section is missing a blocks array: {section.get('id', '<unknown>')}")
        if section["id"] in ids:
            raise ValueError(f"Duplicate section id: {section['id']}")
        ids.add(section["id"])
        for block in section["blocks"]:
            if block.get("type") == "paragraph":
                if not block.get("en") or not block.get("zh"):
                    raise ValueError(f"Empty bilingual paragraph in {section['id']}")
            elif block.get("type") == "figure":
                for key in ("number", "image", "caption_en", "caption_zh"):
                    if not block.get(key):
                        raise ValueError(f"Figure in {section['id']} is missing {key}")
                if str(block["number"]) in figures:
                    raise ValueError(f"Duplicate figure number: {block['number']}")
                figures.add(str(block["number"]))
                if not resolve(base, block["image"]).is_file():
                    raise FileNotFoundError(f"Figure image not found: {block['image']}")
            else:
                raise ValueError(f"Unsupported block type: {block.get('type')}")


def build(data, json_path, output):
    base = json_path.parent
    validate(data, base)
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(resolve(base, data["source_pdf"]), output / "source-paper.pdf")
    css = (SKILL_DIR / "assets" / "reader.css").read_text(encoding="utf-8")
    js = (SKILL_DIR / "assets" / "reader.js").read_text(encoding="utf-8")
    main, toc, figures = [], [], []
    first_subsection = True
    for section in data["sections"]:
        level = section.get("level", "major")
        extra = " first-subsection" if level == "subsection" and first_subsection else ""
        if level == "subsection":
            first_subsection = False
        main.append(f'<section class="section-head {esc(level)}{extra}" id="{esc(section["id"])}"><p class="section-kicker">{esc(section["heading_zh"])}</p><h2>{esc(section["heading_en"])}</h2><aside class="reading-note"><b>阅读旁注</b><span>{esc(section["note_zh"])}</span></aside></section>')
        toc.append(f'<a href="#{esc(section["id"])}">{esc(section["heading_en"])}</a>')
        for block in section["blocks"]:
            if block["type"] == "paragraph":
                main.append(f'<article class="pair"><div class="english"><span class="language-label">English</span><p>{esc(block["en"])}</p></div><div class="chinese"><span class="language-label">中文</span><p>{esc(block["zh"])}</p></div></article>')
            else:
                number = str(block["number"])
                uri = data_uri(resolve(base, block["image"]))
                page = f'<span class="pdf-page">PDF p. {esc(block.get("source_page"))}</span>' if block.get("source_page") else ""
                main.append(f'<figure id="figure-{esc(number)}"><img src="{uri}" alt="Figure {esc(number)}"><figcaption><p class="caption-en">{esc(block["caption_en"])}</p><p class="caption-zh">{esc(block["caption_zh"])}</p>{page}</figcaption></figure>')
                figures.append(f'<a href="#figure-{esc(number)}">Figure {esc(number)}</a>')
    metadata = " · ".join(filter(None, [str(data.get("published", "")), f'DOI: {data["doi"]}' if data.get("doi") else ""]))
    initial = json.dumps({"version":1,"paperId":data["paper_id"],"updatedAt":"","notes":{}}, ensure_ascii=False).replace("<", "\\u003c")
    doc = f'''<!doctype html><html lang="zh-CN" data-paper-id="{esc(data['paper_id'])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(data['title'])} · 双语阅读器</title><style>{css}</style></head><body><div class="shell"><main><header><div class="journal">{esc(data['journal'])}</div><h1>{esc(data['title'])}</h1><p class="authors">{esc(data['authors'])}</p><p class="meta">{esc(metadata)}<br>英文依原文顺序排布；中文为忠实翻译。仅清理 PDF 断词与版面换行。</p><div class="toolbar"><button type="button" id="toggle-zh">显示 / 隐藏中文</button><button type="button" id="toggle-notes">显示 / 隐藏旁注</button><button type="button" id="save-html">保存批注版 HTML</button><a class="source-link" href="source-paper.pdf" target="_blank">打开原始 PDF</a></div></header>{''.join(main)}</main><nav class="sidebar"><h3>Contents</h3>{''.join(toc)}<div class="fig-links"><h3>Figures</h3>{''.join(figures)}</div><section class="sidebar-section"><div class="notebook-head"><h3>全文导出</h3></div><div class="note-tools"><button id="export-en" type="button">导出英文全文</button><button id="export-zh" type="button">导出中文全文</button></div></section><section class="sidebar-section"><div class="notebook-head"><h3>我的笔记</h3><span class="note-count" id="note-count">0 条</span></div><div class="note-tools"><button id="export-json" type="button">备份 JSON</button><button id="import-json" type="button">导入 JSON</button><button id="export-md" type="button">导出 Markdown</button></div><input id="import-json-file" type="file" accept=".json,application/json" hidden><div id="notebook-list"></div></section></nav></div><script id="paper-notes" type="application/json">{initial}</script><script>{js}</script></body></html>'''
    path = output / f"{re.sub(r'[^A-Za-z0-9._-]+', '_', data['paper_id'])}_reader.html"
    path.write_text(doc, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="Build a self-contained bilingual scientific paper reader.")
    parser.add_argument("paper_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    json_path = args.paper_json.resolve()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    result = build(data, json_path, args.output.resolve())
    print(result)


if __name__ == "__main__":
    main()
