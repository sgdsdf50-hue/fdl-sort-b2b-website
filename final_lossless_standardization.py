import os
import re

# Standard physical root-relative paths
HOME_URL = "/index.html"
PROD_CENTER_URL = "/products/index.html"
ANCHOR_BASE = "/index.html#"

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
    'products': '/products/index.html',
    'technology': '/index.html#technology',
    'services': '/index.html#services',
    'contact': '/index.html#contact',
    'inquiry': '/index.html#contact'
}

def apply_lossless_repair(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Fix Product Entrances (index.html cards and detail page cross-links)
    for slug in PRODUCT_SLUGS:
        # Match href pointing to machines, ensure they end with /index.html
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)
        
        # Proximity fix for cards that might have defaulted to root
        card_pattern = r'href="(?:/|index\.html|https?://www\.fdlsorterai\.com/?)"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(card_pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header, Footer, Mobile)
    if file_path != 'index.html':
        # Home & Logo
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https?://www\.fdlsorterai\.com/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{HOME_URL}"', content)
        
        # Navigation Anchors
        for anchor, target in ANCHOR_MAP.items():
            pattern = r'href="[^"]*?#' + anchor + r'"'
            content = re.sub(pattern, f'href="{target}"', content)

    # Step 3: Specific Navigation and Button Fixes
    if file_path.startswith('products/'):
        # "Back to Product Center" buttons
        content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https?://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{PROD_CENTER_URL}"', content)
        
        # Catalog breadcrumbs/links
        content = re.sub(r'href="/products/"', f'href="{PROD_CENTER_URL}"', content)

    # Step 4: Homepage Local Anchor Restoration
    if file_path == 'index.html':
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="/index.html#{anchor}"', f'href="#{anchor}"')

    # Final Sanitization
    content = content.replace('href="//', 'href="/')
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Lossless Repair Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        apply_lossless_repair(f)
