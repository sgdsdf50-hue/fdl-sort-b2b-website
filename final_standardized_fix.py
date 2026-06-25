import os
import re

# Standard paths
HOME = "/index.html"
PROD_INDEX = "/products/index.html"
BASE_URL = "https://www.fdlsorterai.com"

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

def standardized_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Fix all product detail links to point to physical index.html
    # Catches href="/products/xxx/", href="products/xxx/", or absolute domain versions
    for slug in SLUGS:
        pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
        content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # Step 2: Global Navigation Standardization (Header/Mobile/Footer)
    
    # 2a. Home & Logo (point to physical /index.html)
    # Target Home text or Logo class/href variations
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|' + re.escape(BASE_URL) + r'/?)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{HOME}"', content)
    
    # 2b. Navigation Anchors (point to /index.html#anchor)
    for anchor in ANCHORS:
        if anchor == 'products':
             # The "Products" menu item usually points to the catalog index
             content = re.sub(r'href="[^"]*?#products"', f'href="{PROD_INDEX}"', content)
        else:
             # Standard anchors for sections on the homepage
             pattern = r'href="[^"]*?#' + anchor + r'"'
             content = re.sub(pattern, f'href="{HOME}#{anchor}"', content)

    # Step 3: Specific Page Link Fixes
    
    # 3a. "Back to Product Center" buttons and Breadcrumbs
    content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|' + re.escape(BASE_URL) + r'/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center|Equipment Center|设备中心))', f'href="{PROD_INDEX}"', content)
    
    # 3b. Simple link to /products/ root should go to catalog index
    content = re.sub(r'href="/products/"', f'href="{PROD_INDEX}"', content)

    # Step 4: Final Sanitization & Clean-up
    
    # Fix double slashes in URLs if any
    content = content.replace('href="//', 'href="/')
    # Remove any leftover nested href artifacts from previous attempts
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Ensure any link to just "/" becomes /index.html in sub-pages for stability
    if file_path != 'index.html':
        content = re.sub(r'href="/"', f'href="{HOME}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        standardized_fix(f)
