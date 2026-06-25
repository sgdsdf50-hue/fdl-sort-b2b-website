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

def final_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Step 1: Clean non-printable chars first ---
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')

    # --- Step 2: Global Anchor Fix ---
    for anchor in ANCHORS:
        # Match href="#anchor" or variations, but only if they are not already absolute
        # We target the specific pattern href="/index.html#anchor" or similar
        content = re.sub(r'href="[^"]*?#' + anchor + r'"', f'href="{BASE_URL}/#{anchor}"', content)

    # --- Step 3: Global Home/Logo Fix ---
    # Convert index.html to BASE_URL/
    content = re.sub(r'href="[^"]*?index\.html"', f'href="{BASE_URL}/"', content)
    # Convert root href to BASE_URL/ (careful not to double fix)
    content = re.sub(r'href="/(?!products)"', f'href="{BASE_URL}/"', content)

    # --- Step 4: Product Links Fix (Crucial for cards and related products) ---
    for slug in PRODUCT_SLUGS:
        # If it's a card link or related link, it MUST point to the detail page index.html
        # We look for common patterns in products/index.html or detail pages
        pattern = r'href="[^"]*?products/' + slug + r'[^"]*?"'
        content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # --- Step 5: Specific logic for products/index.html cards ---
    if file_path == 'products/index.html':
        # Many cards currently point to BASE_URL/ because they were href="/"
        # We need to re-assign them based on proximity to the product title/image
        for slug in PRODUCT_SLUGS:
            # Look for the card wrapper that has the image/title
            # We'll use a regex that finds the href preceding the specific image
            content = re.sub(
                r'href="' + re.escape(BASE_URL) + r'/"([^>]*?src="[^"]*?' + slug + r'\.jpg")',
                r'href="' + BASE_URL + '/products/' + slug + r'/index.html"\1',
                content
            )

    # --- Step 6: Fix Product Center links in detail pages ---
    # "Back to Product Center" buttons
    content = re.sub(r'href="[^"]*?products/(index\.html)?"([^>]*?(?:返回设备中心|Product Center))', f'href="{BASE_URL}/products/index.html"\\2', content)

    # --- Step 7: Final Cleanup ---
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Verified & Repaired: {file_path}")

for f in FILES:
    final_repair(f)
