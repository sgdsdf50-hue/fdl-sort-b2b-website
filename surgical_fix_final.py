import os
import re

FILES = [
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

PRODUCT_MAP = {
    'ai-optical-sorter': '/products/ai-optical-sorter/index.html',
    'film-flexible-sorter': '/products/film-flexible-sorter/index.html',
    'hyperspectral-material-sorter': '/products/hyperspectral-material-sorter/index.html',
    'parallel-robot-sorter': '/products/parallel-robot-sorter/index.html',
    'solid-waste-line': '/products/solid-waste-line/index.html',
    'textile-sorter': '/products/textile-sorter/index.html'
}

def final_surgical_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Related Product Cards
    for slug, target in PRODUCT_MAP.items():
        # Match product card links based on the image source filename
        # This is the most reliable way to find the correct link for the specific product card
        pattern = r'href="[^"]*?"(?=[^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="{target}"', content)

    # Ensure Navigation links are correct (Safety)
    content = content.replace('href="https://www.fdlsorterai.com/"', 'href="/index.html"')
    # Fix the specific "Back to Product Center" button
    content = re.sub(r'href="[^"]*?"(?=[^>]*?(?:返回设备中心|Back to Product Center))', 'href="/index.html#products"', content)

    # Homepage Nav Specific Fix (Confirming index.html line 244)
    if file_path == 'index.html':
        content = re.sub(r'href="/products/index\.html"([^>]*?data-i18n="nav_products")', r'href="#products"\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for f in FILES + ['index.html', 'products/index.html']:
        final_surgical_fix(f)
