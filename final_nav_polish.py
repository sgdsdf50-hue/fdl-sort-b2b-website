import os
import re

BASE_URL = "https://www.fdlsorterai.com"
ANCHORS = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']
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

def final_polish(content):
    # 1. Standardize Home/Logo
    # Match /index.html, index.html, ./index.html, ../index.html, etc.
    content = re.sub(r'href="[^"]*?index\.html"', f'href="{BASE_URL}/"', content)
    # Also handle href="/" or href=""
    content = re.sub(r'href="/?"', f'href="{BASE_URL}/"', content)
    
    # 2. Standardize Anchors to Absolute URLs
    for anchor in ANCHORS:
        # Match any href ending in #anchor
        content = re.sub(r'href="[^"]*?#' + anchor + r'"', f'href="{BASE_URL}/#{anchor}"', content)
    
    # 3. Standardize Product Links to Absolute index.html
    for slug in PRODUCT_SLUGS:
        # Match any href containing products/slug
        content = re.sub(r'href="[^"]*?products/' + slug + r'(/|/index\.html)?"', f'href="{BASE_URL}/products/{slug}/index.html"', content)

    # 4. Standardize Product Center Index
    content = re.sub(r'href="[^"]*?products/(index\.html)?"', f'href="{BASE_URL}/products/index.html"', content)

    # 5. Clean up logic
    # Remove nested hrefs
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)
    # Remove control characters like \x01 (SOH)
    content = "".join(ch for ch in content if ch.isprintable() or ch in '\n\r\t')
    # Fix double slashes in BASE_URL transitions
    content = content.replace(f'{BASE_URL}//', f'{BASE_URL}/')
    # Re-fix Home if it got messed up by anchor replacement
    content = content.replace(f'href="{BASE_URL}/#"', f'href="{BASE_URL}/"')

    return content

for file_path in FILES:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    new_text = final_polish(text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"Polished: {file_path}")
