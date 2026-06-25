import os
import re

# Physical root-relative standardized paths
BASE_HOME = "/index.html"
BASE_PRODUCTS_INDEX = "/products/index.html"

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

def perform_lossless_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Step 1: index.html Entry Points (Product Cards) ---
    if file_path == 'index.html':
        # Fix card links to be explicit index.html files
        for slug in PRODUCT_SLUGS:
            pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # --- Step 2: Global Navigation in all Sub-pages ---
    else:
        # Standardize Home/Logo to physical /index.html
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top|https://www\.fdlsorterai\.com/)"(?=[^>]*?(?:logo|brand|Home|首页))', f'href="{BASE_HOME}"', content)
        
        # Standardize Navigation Anchors to /index.html#anchor
        for anchor in ANCHORS:
            # Special case for "Products/Equipment Center" in sub-pages: should go to /products/index.html
            if anchor == 'products':
                 content = re.sub(r'href="[^"]*?#products"', f'href="{BASE_PRODUCTS_INDEX}"', content)
            else:
                 pattern = r'href="[^"]*?#' + anchor + r'"'
                 content = re.sub(pattern, f'href="{BASE_HOME}#{anchor}"', content)
        
        # In sub-pages, any link to "/" should probably be /index.html
        content = re.sub(r'href="/"', f'href="{BASE_HOME}"', content)

    # --- Step 3: Product Detail Pages - Back/Related links ---
    if file_path.startswith('products/'):
        # Fix "Back to Product Center" buttons
        content = re.sub(r'href="(?:/products/|(?:\.\./)*index\.html|index\.html|https://www\.fdlsorterai\.com/products/index\.html)"(?=[^>]*?(?:返回设备中心|Product Center))', f'href="{BASE_PRODUCTS_INDEX}"', content)
        
        # Fix Related Product Cards in detail pages
        for slug in PRODUCT_SLUGS:
            pattern = r'href="[^"]*?products/' + slug + r'/(?:index\.html)?"'
            content = re.sub(pattern, f'href="/products/{slug}/index.html"', content)

    # --- Step 4: Final Sanitization ---
    # Fix any double leading slashes
    content = content.replace('href="//', 'href="/')
    # Cleanup any script logic that might conflict (if injected before)
    content = re.sub(r'\s*<script>.*?window\.location\.href\s*=\s*href.*?</script>', '', content, flags=re.DOTALL)
    # Ensure no nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Lossless Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        perform_lossless_fix(f)
