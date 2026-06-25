import os
import re

BASE_URL = "https://www.fdlsorterai.com"
ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']
PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

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

def apply_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Homepage Fix (index.html)
    if file_path == 'index.html':
        for slug in PRODUCT_SLUGS:
            # Fix product card links specifically
            # We match by slug inside the href
            content = re.sub(
                r'href="[^"]*?products/' + slug + r'[^"]*?"',
                f'href="{BASE_URL}/products/{slug}/index.html"',
                content
            )

    # 2. Sub-page Fixes (products/)
    else:
        # Standardize Header/Mobile/Footer nav
        # Logo and Home
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{BASE_URL}/"', content)
        
        # Anchors
        for anchor in ANCHORS:
            # Specifically target nav anchors
            content = re.sub(r'href="[^"]*?#' + anchor + r'"', f'href="{BASE_URL}/#{anchor}"', content)
        
        # Product cards and Related products
        for slug in PRODUCT_SLUGS:
            content = re.sub(
                r'href="[^"]*?products/' + slug + r'[^"]*?"',
                f'href="{BASE_URL}/products/{slug}/index.html"',
                content
            )
            
        # Product Center links
        content = re.sub(r'href="[^"]*?products/(index\.html)?"(?=[^>]*?(?:Equipment Center|设备中心|返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"', content)

    # Final logic cleanup
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

for f in FILES:
    apply_repair(f)
