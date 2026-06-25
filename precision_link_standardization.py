import os
import re

# Standard paths
HOME_FILE = "/index.html"
CATALOG_FILE = "/products/index.html"

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

SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]

ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

def perform_precision_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Fix all product detail links across the site
    # They MUST point to the physical index.html file
    for slug in SLUGS:
        # Match href="/products/xxx/", href="products/xxx/", or any existing variants
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header, Footer, Mobile)
    if file_path != 'index.html':
        # 2a. Standardize Home/Logo to physical /index.html
        # Target elements representing home/brand links
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https?://www\.fdlsorterai\.com/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{HOME_FILE}"', content)
        
        # 2b. Standardize Anchors to /index.html#anchor
        for anchor in ANCHORS:
            if anchor == 'products':
                 # In sub-pages, the "Products" menu item points to the catalog index
                 content = re.sub(r'href="[^"]*?#products"', f'href="{CATALOG_FILE}"', content)
            else:
                 # Other anchors point back to homepage sections
                 pattern = r'href="[^"]*?#' + anchor + r'"'
                 content = re.sub(pattern, f'href="{HOME_FILE}#{anchor}"', content)

    # Step 3: Specific Navigation and Button Fixes in sub-pages
    if file_path.startswith('products/'):
        # "Back to Product Center" buttons
        content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https?://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{CATALOG_FILE}"', content)
        
        # Breadcrumbs or simple relative links to catalog
        content = re.sub(r'href="/products/"', f'href="{CATALOG_FILE}"', content)

    # Step 4: Homepage Smooth Scroll Integrity
    if file_path == 'index.html':
        # Ensure that internal section links remain simple anchors for smooth scroll
        for anchor in ['markets', 'solutions', 'technology', 'services', 'contact']:
             content = content.replace(f'href="{HOME_FILE}#{anchor}"', f'href="#{anchor}"')
        # Re-fix the "Products" link on home to point to physical index
        content = content.replace('href="#products"', f'href="{CATALOG_FILE}"')

    # Final Sanitization
    # Fix any double leading slashes
    content = content.replace('href="//', 'href="/')
    # Remove control characters
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Prevent nested href artifacts (href="href=...")
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Precise Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        perform_precision_fix(f)
