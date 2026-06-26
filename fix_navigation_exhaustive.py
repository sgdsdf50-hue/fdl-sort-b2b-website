import os
import re

# Mapping for precision
PRODUCT_MAP = {
    'AI Optical Sorter': '/products/ai-optical-sorter/index.html',
    'AI Hyperspectral Material Sorter': '/products/hyperspectral-material-sorter/index.html',
    'AI Flexible Film Sorter': '/products/film-flexible-sorter/index.html',
    'AI Textile Sorter': '/products/textile-sorter/index.html',
    'AI Parallel Robot Sorter': '/products/parallel-robot-sorter/index.html',
    'Complete Sorting Line': '/products/solid-waste-line/index.html',
    'AI 智能视觉光选色选机': '/products/ai-optical-sorter/index.html',
    'AI 近红外多光谱材质选机': '/products/hyperspectral-material-sorter/index.html',
    'AI 柔性薄膜分选机': '/products/film-flexible-sorter/index.html',
    'AI 废旧纺织品物料分选机': '/products/textile-sorter/index.html',
    'AI 智能并联机械手分选机器人': '/products/parallel-robot-sorter/index.html',
    '智能固废分选整线解决方案': '/products/solid-waste-line/index.html'
}

FILES = [
    'index.html',
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

def fix_all_product_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Target links that point to root or index.html which are clearly product cards
    # We use a pattern that matches the <a> tag and its attributes, checking for keywords
    
    for name, target in PRODUCT_MAP.items():
        # Match href="/" or href="/index.html" or domain variations
        # AND check if the tag contains the product name in attributes (aria-label, data-zh, alt)
        pattern = r'href="(?:/|/index\.html|https?://www\.fdlsorterai\.com/?)"([^>]*?(?:data-zh|data-en|aria-label|alt)="' + re.escape(name) + r'")'
        content = re.sub(pattern, f'href="{target}"\\1', content)

    # 2. Specifically handle Related Products in sub-pages which might use proximity to img src
    # This matches <a class="product-card" href="/"> ... <img src="...slug.jpg">
    slug_map = {
        'ai-optical-sorter': '/products/ai-optical-sorter/index.html',
        'hyperspectral-material-sorter': '/products/hyperspectral-material-sorter/index.html',
        'film-flexible-sorter': '/products/film-flexible-sorter/index.html',
        'textile-sorter': '/products/textile-sorter/index.html',
        'parallel-robot-sorter': '/products/parallel-robot-sorter/index.html',
        'solid-waste-line': '/products/solid-waste-line/index.html'
    }
    
    for slug, target in slug_map.items():
        # Look for href="/" followed by content containing the specific image slug
        # Regex explanation:
        # href="..."
        # ([^>]*?) any non-bracket chars
        # src="...slug..."
        img_pattern = r'href="(?:/|/index\.html|https?://www\.fdlsorterai\.com/?)"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
        content = re.sub(img_pattern, f'href="{target}"\\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Surgically fixed: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_all_product_links(f)
