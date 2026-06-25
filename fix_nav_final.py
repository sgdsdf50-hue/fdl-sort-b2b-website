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

# Mapping of keywords/patterns to absolute URLs
replacements = [
    (r'href="(https://www\.fdlsorterai\.com/)?index\.html"', 'href="https://www.fdlsorterai.com/"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#markets"', 'href="https://www.fdlsorterai.com/#markets"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#solutions"', 'href="https://www.fdlsorterai.com/#solutions"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#products"', 'href="https://www.fdlsorterai.com/#products"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#technology"', 'href="https://www.fdlsorterai.com/#technology"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#services?"', 'href="https://www.fdlsorterai.com/#services"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#contact"', 'href="https://www.fdlsorterai.com/#contact"'),
    (r'href="(https://www\.fdlsorterai\.com/)?/?#inquiry"', 'href="https://www.fdlsorterai.com/#contact"'),
    
    # Specific catch-all for relative paths that often fail
    (r'href="\.\./\.\./index\.html(#\w+)?"', lambda m: 'href="https://www.fdlsorterai.com/' + (m.group(1) if m.group(1) else '') + '"'),
    (r'href="\.\./index\.html(#\w+)?"', lambda m: 'href="https://www.fdlsorterai.com/' + (m.group(1) if m.group(1) else '') + '"'),
    (r'href="/#markets"', 'href="https://www.fdlsorterai.com/#markets"'),
    (r'href="/#solutions"', 'href="https://www.fdlsorterai.com/#solutions"'),
    (r'href="/#products"', 'href="https://www.fdlsorterai.com/#products"'),
    (r'href="/#technology"', 'href="https://www.fdlsorterai.com/#technology"'),
    (r'href="/#services"', 'href="https://www.fdlsorterai.com/#services"'),
    (r'href="/#contact"', 'href="https://www.fdlsorterai.com/#contact"'),
    
    # "Back to Product Center" button
    (r'href="(https://www\.fdlsorterai\.com/)?(\.\./)?products/index\.html"', 'href="https://www.fdlsorterai.com/products/index.html"'),
    (r'href="/products/"', 'href="https://www.fdlsorterai.com/products/index.html"'),
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, sub in replacements:
        if callable(sub):
            content = re.sub(pattern, sub, content)
        else:
            content = re.sub(pattern, sub, content)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")
