import os
import re

BASE_URL = "https://www.fdlsorterai.com"
PRODUCT_DATA = [
    ('AI Optical Sorter', 'ai-optical-sorter'),
    ('Hyperspectral Material Sorter', 'hyperspectral-material-sorter'),
    ('Plastic Film AI Sorter', 'film-flexible-sorter'),
    ('AI Textile Sorter', 'textile-sorter'),
    ('AI Parallel Robot Sorter', 'parallel-robot-sorter'),
    ('Solid Waste Sorting Line', 'solid-waste-line')
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

def ultimate_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Fix index.html Product Cards (The most damaged part) ---
    if file_path == 'index.html':
        for name, slug in PRODUCT_DATA:
            # Match the link preceding the specific machine's aria-label
            pattern = r'href="https://www\.fdlsorterai\.com/"([^>]*?aria-label="View ' + name + r' details")'
            content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"\\1', content)

    # --- 2. Fix products/index.html Product Cards ---
    if file_path == 'products/index.html':
        for name, slug in PRODUCT_DATA:
            # Match by image name proximity
            pattern = r'href="https://www\.fdlsorterai\.com/"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
            content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"\\1', content)

    # --- 3. Global Navigation Standardization ---
    # Logo & Home
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{BASE_URL}/"', content)
    
    # Anchors
    anchors = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']
    for anchor in anchors:
        pattern = r'href="[^"]*?#' + anchor + r'"'
        content = re.sub(pattern, f'href="{BASE_URL}/#{anchor}"', content)

    # --- 4. Sub-page specific buttons ---
    # Back to Center
    content = re.sub(r'href="[^"]*?products/(index\.html)?"(?=[^>]*?(?:Equipment Center|设备中心|返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"', content)
    # Related Products in detail pages
    for name, slug in PRODUCT_DATA:
        pattern = r'href="[^"]*?products/' + slug + r'(?:/|/index\.html)?"'
        content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # --- 5. Final Sanitization ---
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Ultimately Repaired: {file_path}")

for f in FILES:
    ultimate_repair(f)
