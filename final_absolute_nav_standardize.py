import os
import re

BASE_URL = "https://www.fdlsorterai.com"
PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]
ANCHORS = {
    'markets': f"{BASE_URL}/#markets",
    'solutions': f"{BASE_URL}/#solutions",
    'products': f"{BASE_URL}/#products",
    'technology': f"{BASE_URL}/#technology",
    'services': f"{BASE_URL}/#services",
    'service': f"{BASE_URL}/#services",
    'contact': f"{BASE_URL}/#contact",
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

def final_absolute_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean non-printable/control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    # 2. Fix Home/Logo to absolute main domain
    # Replace root or index.html variations
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{BASE_URL}/"', content)

    # 3. Standardize Navigation Anchors
    for key, val in ANCHORS.items():
        # Match href="#id", href="/#id", href="https://.../#id", href="../../index.html#id"
        pattern = r'href="(?:[^"]*?#|/)' + key + r'"'
        content = re.sub(pattern, f'href="{val}"', content)

    # 4. Standardize Product Detail Links (The core fix for cards)
    for slug in PRODUCT_SLUGS:
        # Match any link that references a product folder, ensure it leads to the index.html file
        # We use a pattern that catches common variations in cards and related products
        pattern = r'href="[^"]*?products/' + slug + r'(?:/|/index\.html)?"'
        content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # 5. Fix links that mistakenly point to the main domain root but should be detail pages
    # This happens in index.html and products/index.html after previous buggy runs
    if file_path == 'index.html' or file_path == 'products/index.html':
        for slug in PRODUCT_SLUGS:
            # Pattern: find the product card link followed by its specific image/title
            # We look for the href that's just the domain root but is part of a card for a specific machine
            pattern = r'href="' + re.escape(BASE_URL) + r'/"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
            content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"\\1', content)

    # 6. Standardize Product Center Index Link
    # Match "Equipment Center", "设备中心", or specific buttons
    content = re.sub(r'href="(?:/products/|(?:\.\./)+index\.html|index\.html)"(?=[^>]*?(?:Equipment Center|设备中心|返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"', content)
    # Also simple link to /products/
    content = re.sub(r'href="/products/"', f'href="{BASE_URL}/products/index.html"', content)

    # 7. Final Cleanup
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed & Standardized: {file_path}")

for f in FILES:
    final_absolute_fix(f)
