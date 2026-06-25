import os
import re

# Goal: Standardized root-relative physical links
# Home: /index.html
# Home Anchors: /index.html#anchor
# Sub-pages: /products/slug/index.html
# Product Center: /products/index.html

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

ANCHOR_MAP = {
    'markets': '/index.html#markets',
    'solutions': '/index.html#solutions',
    'technology': '/index.html#technology',
    'services': '/index.html#services',
    'service': '/index.html#services',
    'contact': '/index.html#contact',
    'inquiry': '/index.html#contact'
}

def standardize_links(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Home/Logo (Target specific strings or classes to be safe)
    # Match href="/", href="index.html", href="../../index.html", etc.
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https://www\.fdlsorterai\.com/)"(?=[^>]*?(?:logo|brand|Home|首页))', 'href="/index.html"', content)

    # 2. Standardize Anchor Navigation
    for anchor, target in ANCHOR_MAP.items():
        # Match href="#anchor", href="/#anchor", href="../../index.html#anchor", etc.
        pattern = r'href="[^"]*?#' + anchor + r'"'
        content = re.sub(pattern, f'href="{target}"', content)

    # 3. Standardize Product Detail Entrances
    for slug in PRODUCT_SLUGS:
        # Match products/slug/ or products/slug/index.html
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # 4. Standardize Product Center / Equipment Center
    # Target "Equipment Center", "Products", "设备中心"
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:Equipment Center|设备中心|返回设备中心|Product Center))', 'href="/products/index.html"', content)
    # Breadcrumbs and simple links to /products/
    content = re.sub(r'href="/products/"', 'href="/products/index.html"', content)

    # 5. Homepage Smooth Scroll (Restore simple anchors for homepage only)
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'products', 'technology', 'services', 'contact']:
             content = content.replace(f'href="/index.html#{anchor}"', f'href="#{anchor}"')
        # Equipment center menu item on homepage should probably still go to catalog index
        content = content.replace('href="#products"', 'href="/products/index.html"')

    # Final cleanup
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Correct double slashes
    content = content.replace('href="//', 'href="/')
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        standardize_links(f)
