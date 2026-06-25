import os
import re

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

PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

def final_surgical_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Homepage Specific Fix (Products nav button) ---
    if file_path == 'index.html':
        # Fix: <a href="/products/index.html" data-i18n="nav_products">Products</a> -> href="#products"
        content = re.sub(
            r'href="/products/index\.html"([^>]*?data-i18n="nav_products")',
            r'href="#products"\1',
            content
        )

    # --- 2. Sub-page Navigation Fix (Equipment Center link) ---
    else:
        # PC Nav & Mobile Menu
        # Target: data-zh="设备中心" or data-en="Products" links in header/mobile areas
        content = re.sub(
            r'href="(?:/products/index\.html|https://www\.fdlsorterai\.com/|/index\.html)"([^>]*?data-(?:zh|en)="(?:设备中心|Products)")',
            r'href="/index.html#products"\1',
            content
        )

    # --- 3. Related Products Link Fix (Detail pages互跳) ---
    if file_path.startswith('products/') and file_path != 'products/index.html':
        for slug in PRODUCT_SLUGS:
            # Look for product cards pointing to root domain but containing a specific machine image
            # Pattern: href="https://..." followed by an img tag with the slug filename
            pattern = r'href="(?:https?://www\.fdlsorterai\.com/?|/)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
            target_href = f'href="/products/{slug}/index.html"'
            content = re.sub(pattern, target_href, content)

    # --- 4. Final Safety Cleanup ---
    # Fix any potential href="href=..." syntax errors
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Correct double slashes
    content = content.replace('href="//', 'href="/')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Surgical fix applied to: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        final_surgical_repair(f)
