#!/usr/bin/env python3
"""自动子集化 Nebulove 字体并内联进 introduce/index.html。

移植自 lingyicute/92li 的 scripts/subset_font.py：
扫描介绍页中出现的所有字符（外加完整 ASCII 与常用中文标点），
下载 Nebulove 全量字体后用 fontTools 子集化为 WOFF2，
转 base64 内联进 @font-face，并保留 jsDelivr 全量 TTF 作为回退。

用法:
    python3 scripts/subset_font.py
依赖:
    pip install fonttools brotli
"""
import re, base64, urllib.request, os, sys

FONT_URL = "https://raw.githubusercontent.com/lingyicute/Nebulove/main/Nebulove.ttf"
INDEX_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "introduce", "index.html"
)
TMP_FONT_PATH = "/tmp/Nebulove.ttf"

def main():
    if not os.path.exists(INDEX_PATH):
        print(f"Error: {INDEX_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    print("Reading index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Collect all characters needed
    chars = set(html)
    # Ensure full ASCII printable set (32 to 126)
    for c in range(32, 127):
        chars.add(chr(c))
    # Common punctuation
    chars.update(['：', '，', '。', '！', '？', '；', '“', '”', '‘', '’', '（', '）', '【', '】', '—', '…', '·', '《', '》', '×', '＝', '÷', '＋', '－'])

    print(f"Total unique characters needed: {len(chars)}")

    # 2. Download full Nebulove font
    print(f"Downloading font from {FONT_URL}...")
    try:
        urllib.request.urlretrieve(FONT_URL, TMP_FONT_PATH)
    except Exception as e:
        print(f"Failed to download font: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Subset font using fontTools
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options

    print("Subsetting font...")
    # recalcTimestamp=False：默认行为会在保存时把 head.modified 更新为当前时间，
    # 而 WOFF2 把所有表压缩进同一个 brotli 流，时间戳一变整个文件字节都会变，
    # 导致重复运行结果不稳定、"已最新"判断永远不命中。
    font = TTFont(TMP_FONT_PATH, recalcTimestamp=False)
    subsetter = Subsetter(options=Options())
    # 按码点排序：set 迭代顺序受 PYTHONHASHSEED 影响，不排序的话重复运行
    # 生成的 woff2 字节会有微小差异，导致"已最新、无需修改"判断永远不命中。
    subsetter.populate(text="".join(sorted(chars)))
    subsetter.subset(font)

    font.flavor = "woff2"
    tmp_woff2 = "/tmp/Nebulove-Subset.woff2"
    font.save(tmp_woff2)

    woff2_size = os.path.getsize(tmp_woff2)
    print(f"Subsetted WOFF2 size: {woff2_size} bytes ({woff2_size / 1024:.2f} KB)")

    # 4. Convert to base64
    with open(tmp_woff2, "rb") as f:
        b64_font = base64.b64encode(f.read()).decode("utf-8")

    # 5. Replace font-face in index.html
    font_css = f'''@font-face{{
  font-family:"Nebulove";
  src:url("data:font/woff2;charset=utf-8;base64,{b64_font}") format("woff2"),
      url("https://cdn.jsdelivr.net/gh/lingyicute/Nebulove@main/Nebulove.ttf") format("truetype");
  font-display:swap;
}}'''

    new_html = re.sub(r'@font-face\s*\{[^}]*\}', font_css, html, flags=re.DOTALL)

    if new_html == html:
        print("index.html is already up to date. No changes made.")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)

    print("index.html updated successfully!")

if __name__ == "__main__":
    main()
