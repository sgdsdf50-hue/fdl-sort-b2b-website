import os
import re

# Mapping of machine signatures to their actual detail pages
PRODUCT_MAP = {
    'AI Optical Sorter': '/products/ai-optical-sorter/index.html',
    'AI Hyperspectral Material Sorter': '/products/hyperspectral-material-sorter/index.html',
    'AI Flexible Film Sorter': '/products/film-flexible-sorter/index.html',
    'AI Textile Sorter': '/products/textile-sorter/index.html',
    'AI Parallel Robot Sorter': '/products/parallel-robot-sorter/index.html',
    'Solid Waste Sorting Line': '/products/solid-waste-line/index.html',
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

def fix_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the 6th card in index.html specifically
    if file_path == 'index.html':
        content = re.sub(
            r'href="/index\.html"([^>]*?aria-label="View Complete Sorting Line details")',
            r'href="/products/solid-waste-line/index.html"\1',
            content
        )

    # 2. General fix for Related Products cards in all files
    # We look for <a class="product-card" href="..."> ... contains data-zh or data-en for a product
    for name, target in PRODUCT_MAP.items():
        # Match product card href pointing to root or domain, followed by the specific product name in attributes
        pattern = r'href="(?:/|/index\.html|https?://www\.fdlsorterai\.com/?)"([^>]*?(?:data-zh|data-en)="' + re.escape(name) + r'")'
        content = re.sub(pattern, f'href="{target}"\\1', content)
        
        # Also catch the aria-label variation
        pattern_aria = r'href="(?:/|/index\.html|https?://www\.fdlsorterai\.com/?)"([^>]*?aria-label="View ' + re.escape(name) + r' details")'
        content = re.sub(pattern_aria, f'href="{target}"\\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_links(f)
