import os
import re

files = [
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

# Patterns for exact HREF replacement
replacements = [
    (r'href="(?:/|index\.html|(?:\.\./)+index\.html)"', 'href="https://www.fdlsorterai.com/"'),
    (r'href="(?:/#markets|#markets|(?:\.\./)+index\.html#markets)"', 'href="https://www.fdlsorterai.com/#markets"'),
    (r'href="(?:/#solutions|#solutions|(?:\.\./)+index\.html#solutions)"', 'href="https://www.fdlsorterai.com/#solutions"'),
    (r'href="(?:/products/|#products|(?:\.\./)+index\.html#products)"', 'href="https://www.fdlsorterai.com/#products"'),
    (r'href="(?:/#technology|#technology|(?:\.\./)+index\.html#technology)"', 'href="https://www.fdlsorterai.com/#technology"'),
    (r'href="(?:/#services|#services|(?:\.\./)+index\.html#services)"', 'href="https://www.fdlsorterai.com/#services"'),
    (r'href="(?:/#contact|#contact|#inquiry|(?:\.\./)+index\.html#contact)"', 'href="https://www.fdlsorterai.com/#contact"'),
    # Back to center button
    (r'href="(?:../index\.html|index\.html)" (data-zh="返回设备中心")', 'href="https://www.fdlsorterai.com/products/index.html" \\1'),
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, new_href in replacements:
        content = re.sub(pattern, new_href, content)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")
