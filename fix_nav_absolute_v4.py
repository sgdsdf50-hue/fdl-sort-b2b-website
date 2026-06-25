import os
import re

BASE_URL = "https://www.fdlsorterai.com"
NAV_MAP = {
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

def fix_links(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Homepage logic
    if file_path == 'index.html':
        # Fix product entry points
        content = re.sub(r'href="/products/([^"/]+)/"', r'href="/products/\1/index.html"', content)
        # (Other homepage links are already anchors or handled by general logic if needed)

    # 2. Sub-page logic (all in products/ directory)
    else:
        # Standardize Navigation (Header, Footer, Mobile Panel)
        # Home and Logo
        content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html)"', f'href="{BASE_URL}/"', content)
        
        # Anchors (markets, solutions, etc.)
        for anchor, absolute_url in NAV_MAP.items():
            # Matches variations like /#markets, #markets, ../../index.html#markets
            pattern = r'href="[^"]*#' + anchor + r'"'
            content = re.sub(pattern, f'href="{absolute_url}"', content)
            
            # Matches path-style links without hash if they exist
            path_pattern = r'href="/' + anchor + r'"'
            content = re.sub(path_pattern, f'href="{absolute_url}"', content)

        # Fix "Back to Product Center" button logic
        # Targeted replacement for the button and the product index link
        content = re.sub(r'href="(?:(?:\.\./)*index\.html|/products/)"', f'href="{BASE_URL}/products/index.html"', content)
        
        # Related Products / Intra-directory links
        content = re.sub(r'href="/products/([^"/]+)/"', f'href="{BASE_URL}/products/\\1/index.html"', content)

    # Safety: ensure no nested hrefs like href="href=..."
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Repaired: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        fix_links(f)
