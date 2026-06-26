import os
import re

FILES_MAP = {
    'products/index.html': 'https://www.fdlsorterai.com/products/index.html',
    'products/ai-optical-sorter/index.html': 'https://www.fdlsorterai.com/products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html': 'https://www.fdlsorterai.com/products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html': 'https://www.fdlsorterai.com/products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html': 'https://www.fdlsorterai.com/products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html': 'https://www.fdlsorterai.com/products/solid-waste-line/index.html',
    'products/textile-sorter/index.html': 'https://www.fdlsorterai.com/products/textile-sorter/index.html'
}

def fix_canonical(file_path, target_url):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Precise replacement of the canonical link tag
    # Pattern looks for <link rel="canonical" href="...">
    pattern = r'<link rel="canonical" href="[^"]*">'
    new_tag = f'<link rel="canonical" href="{target_url}">'
    
    new_content = re.sub(pattern, new_tag, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated canonical in: {file_path}")
    else:
        print(f"Canonical tag not found or already correct in: {file_path}")

if __name__ == "__main__":
    for path, url in FILES_MAP.items():
        fix_canonical(path, url)
