import os
import re

# Mapping of product machines to their details pages
PRODUCT_MAP = {
    'ai-optical-sorter': '/products/ai-optical-sorter/index.html',
    'film-flexible-sorter': '/products/film-flexible-sorter/index.html',
    'hyperspectral-material-sorter': '/products/hyperspectral-material-sorter/index.html',
    'parallel-robot-sorter': '/products/parallel-robot-sorter/index.html',
    'solid-waste-line': '/products/solid-waste-line/index.html',
    'textile-sorter': '/products/textile-sorter/index.html'
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

def surgical_link_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Homepage index.html: Specifically target the 6th card
    if file_path == 'index.html':
        # Match the link with "Complete Sorting Line" label
        content = re.sub(
            r'href="/index\.html"([^>]*?aria-label="View Complete Sorting Line details")',
            r'href="/products/solid-waste-line/index.html"\1',
            content
        )

    # 2. General logic for all product cards in all files
    # We find links that are pointing to root or main domain but clearly belong to a specific machine
    # We use proximity to machine-specific keywords in data-zh, data-en, alt, or img src.
    
    for slug, target in PRODUCT_MAP.items():
        # This pattern finds an 'a' tag whose href is root/home, 
        # and which contains (in attributes or content) the product slug or name.
        # We look for href="/" or href="/index.html" or domain variations.
        
        # Regex explanation:
        # href="(...)" matches the current wrong link
        # ([^>]*?) matches any other attributes of the <a> tag
        # (?:src|alt|data-zh|data-en|aria-label)="[^"]*?slug_or_variation"
        
        # Match by slug in src/alt/attributes
        pattern = r'href="(?:/|/index\.html|https://www\.fdlsorterai\.com/?)"([^>]*?(?:src|alt|data-zh|data-en|aria-label)="[^"]*?' + slug + r'[^"]*?")'
        content = re.sub(pattern, f'href="{target}"\\1', content)

    # 3. Handle Chinese character name matches for products/index.html specifically
    cn_map = {
        'AI 智能视觉光选色选机': '/products/ai-optical-sorter/index.html',
        'AI 近红外多光谱材质选机': '/products/hyperspectral-material-sorter/index.html',
        'AI 柔性薄膜分选机': '/products/film-flexible-sorter/index.html',
        'AI 废旧纺织品物料分选机': '/products/textile-sorter/index.html',
        'AI 智能并联机械手分选机器人': '/products/parallel-robot-sorter/index.html',
        '智能固废分选整线解决方案': '/products/solid-waste-line/index.html'
    }
    
    for name, target in cn_map.items():
        pattern = r'href="(?:/|/index\.html|https://www\.fdlsorterai\.com/?)"([^>]*?(?:data-zh|data-en)="' + re.escape(name) + r'")'
        content = re.sub(pattern, f'href="{target}"\\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Surgically repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        surgical_link_repair(f)
