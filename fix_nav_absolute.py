import os
import re

files = [
    'index.html',
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

# Mapping of keywords to absolute URLs
nav_map = {
    'Home': 'https://www.fdlsorterai.com/',
    'Markets': 'https://www.fdlsorterai.com/#markets',
    'Solutions': 'https://www.fdlsorterai.com/#solutions',
    'Products': 'https://www.fdlsorterai.com/#products',
    'Technology': 'https://www.fdlsorterai.com/#technology',
    'Service': 'https://www.fdlsorterai.com/#services', # Handles 'Service' and 'Services'
    'Contact': 'https://www.fdlsorterai.com/#contact',
    'Inquiry': 'https://www.fdlsorterai.com/#contact'
}

def fix_links(content, is_index=False):
    # Fix Logo/Home links first
    content = re.sub(r'href="(/|\.\./|\.\./\.\./)?index\.html"', 'href="https://www.fdlsorterai.com/"', content)
    content = re.sub(r'href="/?"', 'href="https://www.fdlsorterai.com/"', content)
    content = re.sub(r'href="#top"', 'href="https://www.fdlsorterai.com/"', content)

    # Fix Anchors
    patterns = [
        (r'href="(/|\.\./|\.\./\.\./)?#markets"', 'href="https://www.fdlsorterai.com/#markets"'),
        (r'href="(/|\.\./|\.\./\.\./)?#solutions"', 'href="https://www.fdlsorterai.com/#solutions"'),
        (r'href="(/|\.\./|\.\./\.\./)?#products"', 'href="https://www.fdlsorterai.com/#products"'),
        (r'href="(/|\.\./|\.\./\.\./)?#technology"', 'href="https://www.fdlsorterai.com/#technology"'),
        (r'href="(/|\.\./|\.\./\.\./)?#services?"', 'href="https://www.fdlsorterai.com/#services"'),
        (r'href="(/|\.\./|\.\./\.\./)?#contact"', 'href="https://www.fdlsorterai.com/#contact"'),
        (r'href="(/|\.\./|\.\./\.\./)?#inquiry"', 'href="https://www.fdlsorterai.com/#contact"'),
    ]
    
    for old, new in patterns:
        content = re.sub(old, new, content)

    # Specific fix for "Back to Product Center"
    content = content.replace('href="../index.html"', 'https://www.fdlsorterai.com/products/index.html')
    # Cleanup any accidental relative paths that might have survived in detail pages
    content = content.replace('href="../../products/index.html"', 'href="https://www.fdlsorterai.com/products/index.html"')
    
    return content

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = fix_links(content, is_index=(file_path == 'index.html'))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {file_path}")
