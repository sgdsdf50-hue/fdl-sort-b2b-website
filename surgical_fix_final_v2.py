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
        # Match href="..." followed by machine-specific img src
        # We allow matching across the '>' of the <a> tag
        pattern = r'href="[^"]*?"(?=[^<]*?><img [^>]*?src="[^"]*?' + slug + r'\.(?:jpg|png|webp)")'
        content = re.sub(pattern, f'href="{target}"', content)

    # Ensure "Back to Product Center" is also correct
    content = re.sub(
        r'href="[^"]*?"(?=[^>]*?data-zh="返回设备中心")',
        'href="/index.html#products"',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for f in FILES:
        final_surgical_fix(f)
