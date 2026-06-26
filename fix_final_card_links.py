import os
import re

# Mapping of product names/images to their actual physical paths
PRODUCT_MAP = {
    'ai-optical-sorter': '/products/ai-optical-sorter/index.html',
    'hyperspectral-material-sorter': '/products/hyperspectral-material-sorter/index.html',
    'film-flexible-sorter': '/products/film-flexible-sorter/index.html',
    'textile-sorter': '/products/textile-sorter/index.html',
    'parallel-robot-sorter': '/products/parallel-robot-sorter/index.html',
    'solid-waste-line': '/products/solid-waste-line/index.html'
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

def fix_product_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix index.html specifically for the 6th card
    if file_path == 'index.html':
        # Target the 6th card: Complete Sorting Line
        # Matches: <a href="/index.html" ... aria-label="View Complete Sorting Line details">
        content = re.sub(
            r'href="/index\.html"([^>]*?aria-label="View Complete Sorting Line details")',
            r'href="/products/solid-waste-line/index.html"\1',
            content
        )

    # 2. General fix for Related Products cards pointing to root in all files
    # We look for <a class="product-card" href="..."> ... <img src="...slug..." ...>
    # or proximity-based replacement.
    
    # We'll use a regex that captures the anchor and its contents including the image
    # and replaces the href if it's currently root.
    for slug, target in PRODUCT_MAP.items():
        # Match product-card href pointing to root or index.html followed by an image with the slug
        pattern = r'href="(?:/|/index\.html|https://www\.fdlsorterai\.com/?)"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
        content = re.sub(pattern, f'href="{target}"\\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_product_links(f)
