"""
Render a Jekyll markdown blog post into 9 separate JPG images
for sharing on WeChat Moments. Each section stays in one image.

Usage:
    python render_wechat_long_image.py

Dependencies:
    pip install markdown playwright Pillow
    playwright install chromium
"""

import markdown
import re
import os
from pathlib import Path

POST_PATH = "/Users/cqiao/projects/qiaochen.github.io/_posts/2026-03-19-nanyanglegend.md"
IMG_DIR = "/Users/cqiao/projects/qiaochen.github.io/img/nanyanglegend"
OUTPUT_DIR = "/Users/cqiao/projects/qiaochen.github.io/img/nanyanglegend/wechat"

SECTION_SPLITS = [
    ("序言", None, "## 第一章"),
    ("第一章", "## 第一章", "## 第二章"),
    ("第二章", "## 第二章", "## 第三章"),
    ("第三章", "## 第三章", "## 第四章"),
    ("第四章", "## 第四章", "## 第五章"),
    ("第五章", "## 第五章", "## 第六章"),
    ("第六章", "## 第六章", "## 第七章"),
    ("第七章·尾声", "## 第七章", "## 后记"),
    ("后记·附录", "## 后记", None),
]


def parse_front_matter(content):
    if content.startswith("---"):
        end = content.index("---", 3)
        front = content[3:end].strip()
        body = content[end + 3:].strip()
        meta = {}
        for line in front.split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
        return body, meta
    return content, {}


def split_sections(body):
    """Split markdown body into 9 sections based on headings."""
    sections = []
    for label, start_marker, end_marker in SECTION_SPLITS:
        if start_marker is None:
            start_idx = 0
        else:
            start_idx = body.find(start_marker)
            if start_idx == -1:
                sections.append((label, ""))
                continue

        if end_marker is None:
            section_md = body[start_idx:]
        else:
            end_idx = body.find(end_marker, start_idx + (len(start_marker) if start_marker else 0))
            if end_idx == -1:
                section_md = body[start_idx:]
            else:
                section_md = body[start_idx:end_idx]

        section_md = section_md.strip().rstrip("-").rstrip()
        sections.append((label, section_md))

    return sections


def resolve_images(html, img_dir):
    def replacer(match):
        src = match.group(1)
        if src.startswith("/img/nanyanglegend/"):
            filename = src.split("/")[-1]
            abs_path = os.path.join(img_dir, filename)
            if os.path.exists(abs_path):
                return f'src="file://{abs_path}"'
        return match.group(0)
    return re.sub(r'src="([^"]*)"', replacer, html)


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@300;400;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    width: 1080px;
    background: #1a1a2e;
    color: #e0dcd0;
    font-family: 'Noto Serif SC', 'Songti SC', 'STSong', serif;
    font-size: 32px;
    line-height: 2.0;
    letter-spacing: 0.05em;
}

.container { padding: 80px 90px 100px 90px; }

.header {
    text-align: center;
    padding-bottom: 60px;
    border-bottom: 1px solid rgba(200, 180, 150, 0.3);
    margin-bottom: 60px;
}
.header h1 {
    font-family: 'Noto Serif SC', serif;
    font-size: 56px; font-weight: 700; color: #f0e6d3;
    letter-spacing: 0.15em; line-height: 1.5; margin-bottom: 20px;
}
.header .subtitle {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 26px; color: #8a8070; letter-spacing: 0.1em;
}
.tag-list {
    margin-top: 30px; display: flex; justify-content: center;
    gap: 16px; flex-wrap: wrap;
}
.tag {
    display: inline-block; padding: 6px 20px;
    background: rgba(200, 180, 150, 0.12);
    border: 1px solid rgba(200, 180, 150, 0.25);
    border-radius: 20px;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 22px; color: #a09080;
}

.content h1 {
    font-size: 48px; font-weight: 700; color: #f0e6d3;
    text-align: center; margin: 30px 0 40px 0;
    letter-spacing: 0.12em; line-height: 1.6;
}
.content h2 {
    font-size: 42px; font-weight: 700; color: #d4c4a8;
    margin: 30px 0 35px 0; padding-bottom: 15px;
    border-bottom: 1px solid rgba(200, 180, 150, 0.2);
    letter-spacing: 0.1em; line-height: 1.5;
}
.content h3 {
    font-size: 36px; font-weight: 700; color: #c0b090;
    margin: 50px 0 25px 0;
}
.content p {
    margin-bottom: 35px; text-align: justify; text-indent: 2em;
}
.content p img { text-indent: 0; }
.content img {
    display: block; max-width: 100%; margin: 45px auto;
    border-radius: 6px; box-shadow: 0 4px 30px rgba(0,0,0,0.4);
}
.content hr {
    border: none; height: 1px;
    background: linear-gradient(to right, transparent, rgba(200,180,150,0.4), transparent);
    margin: 60px 0;
}
.content ul, .content ol { margin: 20px 0 35px 2em; }
.content li { margin-bottom: 12px; text-indent: 0; }
.content strong { color: #f0e6d3; }
.content em { color: #c8b898; font-style: italic; }
.content a {
    color: #8ab4d8; text-decoration: none;
    border-bottom: 1px dashed rgba(138,180,216,0.4);
}
.content blockquote {
    margin: 30px 0; padding: 20px 30px;
    border-left: 3px solid rgba(200,180,150,0.4);
    background: rgba(200,180,150,0.06);
    color: #b0a090; font-style: italic;
}

.page-number {
    text-align: center; margin-top: 60px; padding-top: 40px;
    border-top: 1px solid rgba(200,180,150,0.2);
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 24px; color: #605040; letter-spacing: 0.1em;
}

.footer {
    margin-top: 60px; padding-top: 50px;
    border-top: 1px solid rgba(200,180,150,0.3);
    text-align: center;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 24px; color: #706050;
    letter-spacing: 0.08em; line-height: 2.0;
}
.footer .blog-url {
    margin-top: 10px; font-size: 22px; color: #807060;
}
"""


def build_section_html(body_html, page_num, total_pages, section_label,
                       is_first=False, is_last=False):
    header = ""
    if is_first:
        header = """
    <div class="header">
        <h1>架空故事集<br>消失在雨林之下的人</h1>
        <div class="subtitle">Chen Qiao's Blog · 2026.03.19</div>
        <div class="tag-list">
            <span class="tag">昭南神社</span>
            <span class="tag">1942-1945</span>
            <span class="tag">宿命</span>
            <span class="tag">隐喻</span>
            <span class="tag">救赎</span>
        </div>
    </div>"""

    footer = ""
    if is_last:
        footer = """
    <div class="footer">
        <div>— 全文完 —</div>
        <div class="blog-url">qiaochen.github.io</div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>{CSS}</style>
</head>
<body>
<div class="container">
    {header}
    <div class="content">
        {body_html}
    </div>
    <div class="page-number">{page_num} / {total_pages}</div>
    {footer}
</div>
</body>
</html>"""


def main():
    print("Reading markdown post...")
    with open(POST_PATH, "r", encoding="utf-8") as f:
        raw = f.read()

    body, meta = parse_front_matter(raw)

    print("Splitting into sections...")
    sections = split_sections(body)
    total = len(sections)
    print(f"Found {total} sections:")
    for i, (label, md_text) in enumerate(sections):
        print(f"  [{i+1}] {label} ({len(md_text)} chars)")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\nRendering HTML for each section...")
    md_converter = markdown.Markdown(extensions=['extra', 'nl2br'])
    html_pages = []
    for i, (label, section_md) in enumerate(sections):
        md_converter.reset()
        section_html = md_converter.convert(section_md)
        section_html = resolve_images(section_html, IMG_DIR)

        full_html = build_section_html(
            section_html,
            page_num=i + 1,
            total_pages=total,
            section_label=label,
            is_first=(i == 0),
            is_last=(i == total - 1),
        )
        html_pages.append((label, full_html))

    print("Launching headless browser for screenshots...")
    from playwright.sync_api import sync_playwright
    from PIL import Image

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, (label, html_content) in enumerate(html_pages):
            page_num = i + 1
            print(f"\n  Rendering [{page_num}/{total}] {label}...")

            html_path = os.path.join(OUTPUT_DIR, f"_temp_{page_num}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            page = browser.new_page(viewport={"width": 1080, "height": 800})
            page.goto(f"file://{html_path}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)

            full_height = page.evaluate("document.documentElement.scrollHeight")
            page.set_viewport_size({"width": 1080, "height": full_height})
            page.wait_for_timeout(500)

            png_path = os.path.join(OUTPUT_DIR, f"part_{page_num:02d}.png")
            page.screenshot(path=png_path, full_page=True)

            page.close()
            os.remove(html_path)

            img = Image.open(png_path)
            if img.mode == "RGBA":
                bg = Image.new("RGB", img.size, (26, 26, 46))
                bg.paste(img, mask=img.split()[3])
                img = bg

            jpg_path = os.path.join(OUTPUT_DIR, f"part_{page_num:02d}_{label}.jpg")
            img.save(jpg_path, "JPEG", quality=90, optimize=True)
            os.remove(png_path)

            w, h = img.size
            size_kb = os.path.getsize(jpg_path) / 1024
            print(f"    -> {jpg_path}")
            print(f"       {w}x{h}px, {size_kb:.0f} KB")

        browser.close()

    print(f"\nAll {total} images saved to {OUTPUT_DIR}/")
    total_size = sum(
        os.path.getsize(os.path.join(OUTPUT_DIR, f))
        for f in os.listdir(OUTPUT_DIR) if f.endswith(".jpg")
    ) / (1024 * 1024)
    print(f"Total size: {total_size:.1f} MB")
    print("Done!")


if __name__ == "__main__":
    main()
