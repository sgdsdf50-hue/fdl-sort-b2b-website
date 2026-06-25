import os
import re

# Physical root-relative path targets
HOME_PHYSICAL = "/index.html"
CATALOG_PHYSICAL = "/products/index.html"

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

ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

def apply_lossless_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: index.html Entry Points (Product Cards)
    if file_path == 'index.html':
        # Fix all card links to be explicit index.html files
        for slug in PRODUCT_SLUGS:
            # Match href="/products/xxx/" or variations, ensuring we point to index.html
            pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header, Footer, Mobile)
    if file_path != 'index.html':
        # 2a. Home & Logo (point to physical /index.html)
        # Identify Home/Logo links and ensure they point to /index.html
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https?://www\.fdlsorterai\.com/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{HOME_PHYSICAL}"', content)
        
        # 2b. Navigation Anchors (point to /index.html#anchor)
        for anchor in ANCHORS:
            if anchor == 'products':
                # "Products" or "Equipment Center" menu item in sub-pages should go to catalog index
                content = re.sub(r'href="[^"]*?#products"', f'href="{CATALOG_PHYSICAL}"', content)
            else:
                # Other anchors point back to homepage sections
                pattern = r'href="[^"]*?#' + anchor + r'"'
                content = re.sub(pattern, f'href="{HOME_PHYSICAL}#{anchor}"', content)

    # Step 3: Specific Page Link Fixes
    if file_path.startswith('products/'):
        # "Back to Product Center" buttons and catalog breadcrumbs
        content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https?://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{CATALOG_PHYSICAL}"', content)
        
        # Related product cards at the bottom of detail pages
        for slug in PRODUCT_SLUGS:
            pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 4: Homepage Smooth Scroll Preservation
    if file_path == 'index.html':
        # On homepage, links within the page should stay as local anchors
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{HOME_PHYSICAL}#{anchor}"', f'href="#{anchor}"')

    # Final Sanitization
    content = content.replace('href="//', 'href="/')
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Remove any stray nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Lossless Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        apply_lossless_fix(f)
