import os
import re

BASE_URL = "https://www.fdlsorterai.com"
PRODUCT_SLUGS = [
    'ai-optical-sorter',
    'film-flexible-sorter',
    'hyperspectral-material-sorter',
    'parallel-robot-sorter',
    'solid-waste-line',
    'textile-sorter'
]
ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']

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

def precise_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Global Navigation Standardize (Absolute URLs) ---
    # Logo & Home
    content = re.sub(r'href="(?:/|index\.html|(?:\.\./)+index\.html|#top)"', f'href="{BASE_URL}/"', content)
    
    # Global Anchors
    for anchor in ANCHORS:
        # Avoid double fixing by checking for BASE_URL
        pattern = r'href="(?!http)[^"]*#' + anchor + r'"'
        content = re.sub(pattern, f'href="{BASE_URL}/#{anchor}"', content)
        # Also path style
        path_pattern = r'href="/' + anchor + r'"'
        content = re.sub(path_pattern, f'href="{BASE_URL}/#{anchor}"', content)

    # --- 2. Product Entrance Fix (Crucial) ---
    # This applies to index.html cards and related-products in subpages
    for slug in PRODUCT_SLUGS:
        # Match any link that references the machine folder, ensuring it points to index.html
        # We look for the slug in the URL
        pattern = r'href="[^"]*?products/' + slug + r'(?:/|/index\.html)?"'
        content = re.sub(pattern, f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # --- 3. Specific logic for products/index.html card fix ---
    # Since many cards currently have href="BASE_URL/", we use proximity to img src to fix them
    if file_path == 'products/index.html' or file_path == 'index.html':
        for slug in PRODUCT_SLUGS:
            # Look for: href="BASE_URL/" ... src="...slug..."
            # Using a regex that captures the card structure
            card_pattern = r'href="' + re.escape(BASE_URL) + r'/"([^>]*?src="[^"]*?' + slug + r'[^"]*?")'
            content = re.sub(card_pattern, f'href="{BASE_URL}/products/{slug}/index.html"\\1', content)

    # --- 4. Back to Product Center ---
    content = re.sub(r'href="(?!http)[^"]*?products/(index\.html)?"', f'href="{BASE_URL}/products/index.html"', content)

    # --- 5. Final Safety Cleanup ---
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Precise Fix Applied: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        precise_fix(f)
