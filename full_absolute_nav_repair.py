import os
import re

BASE_URL = "https://www.fdlsorterai.com"
ANCHORS = {
    'markets': f"{BASE_URL}/#markets",
    'solutions': f"{BASE_URL}/#solutions",
    'products': f"{BASE_URL}/#products",
    'technology': f"{BASE_URL}/#technology",
    'services': f"{BASE_URL}/#services",
    'service': f"{BASE_URL}/#services",
    'contact': f"{BASE_URL}/#contact",
    'inquiry': f"{BASE_URL}/#contact"
}

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

def fix_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Home/Logo to root absolute
    # Matches href="/", href="index.html", href="../../index.html", etc.
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html)"', f'href="{BASE_URL}/"', content)

    # 2. Standardize Anchor Links
    for key, val in ANCHORS.items():
        # Match variations like href="/#markets", href="#markets", href="/markets", href="../../index.html#markets"
        pattern = r'href="(?:[^"]*?#|/)' + key + r'"'
        content = re.sub(pattern, f'href="{val}"', content)

    # 3. Standardize Product Detail Links
    for slug in PRODUCT_SLUGS:
        # Match any href pointing to a product folder
        pattern = r'href="(?:[^"]*?products/)?' + slug + r'(?:/|/index\.html)?"'
        content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # 4. Standardize Product Center Link
    # Match links specifically meant for the product catalog
    # Use negative lookahead to avoid matching detail pages already fixed
    content = re.sub(r'href="(?:/products/|(?:\.\./)+index\.html|index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|产品二级页面入口))', f'href="{BASE_URL}/products/index.html"', content)
    # Also handle the breadcrumb or simple links to /products/
    content = re.sub(r'href="/products/"', f'href="{BASE_URL}/products/index.html"', content)

    # 5. Correct card links in products/index.html that might have defaulted to root
    if file_path == 'products/index.html' or file_path == 'index.html':
        for slug in PRODUCT_SLUGS:
            # Look for cards where href is now root but should be the detail page based on image
            pattern = r'href="' + re.escape(BASE_URL) + r'/"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
            content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"\\1', content)

    # Final cleanup of any potential artifacts
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")

for f in FILES:
    fix_links(f)
