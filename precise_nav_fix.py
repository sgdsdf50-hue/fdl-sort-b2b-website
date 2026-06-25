import os
import re

# Absolute mappings
BASE_URL = "https://www.fdlsorterai.com"
NAV_MAPPING = {
    'markets': f"{BASE_URL}/#markets",
    'solutions': f"{BASE_URL}/#solutions",
    'products': f"{BASE_URL}/#products",
    'technology': f"{BASE_URL}/#technology",
    'services': f"{BASE_URL}/#services",
    'service': f"{BASE_URL}/#services",
    'contact': f"{BASE_URL}/#contact",
}

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

def repair_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Handle index.html specific logic: product entrance
    if file_path == 'index.html':
        # Convert /products/xxx/ to /products/xxx/index.html
        content = re.sub(r'href="/products/([^"/]+)/"', r'href="/products/\1/index.html"', content)
        # Ensure smooth scroll anchors in homepage don't have leading / if already absolute
        # But user wants "lossless", so we just fix the products links.
    
    # 2. Handle products/ files
    else:
        # Standardize Navigation (Header, Footer, Mobile Panel)
        # First, fix Home/Logo
        content = re.sub(r'href="([^"]*/)?index\.html"', f'href="{BASE_URL}/"', content)
        content = re.sub(r'href="/?"', f'href="{BASE_URL}/"', content)

        # Fix Anchors
        for key, absolute_url in NAV_MAPPING.items():
            # Matches href="/markets", href="#markets", href="../../index.html#markets", etc.
            # But avoids matching sub-page internal anchors like #specs
            pattern = r'href="([^"]*?)#' + key + r'(\s*)"'
            content = re.sub(pattern, f'href="{absolute_url}"', content)
            
            # Match path-based ones like href="/markets" (no anchor)
            path_pattern = r'href="/' + key + r'(\s*)"'
            content = re.sub(path_pattern, f'href="{absolute_url}"', content)

        # Fix "Back to Product Center" or directory links
        # href="../index.html" in sub-sub-pages usually means products/index.html
        if file_path.count('/') == 2: # products/xxx/index.html
             content = content.replace('href="../index.html"', f'href="{BASE_URL}/products/index.html"')
        
        # Related products in sub-pages
        content = re.sub(r'href="/products/([^"/]+)/"', f'href="{BASE_URL}/products/\\1/index.html"', content)

    # 3. Final cleanup for any href="href=..." (insurance)
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

for f in FILES:
    repair_file(f)
