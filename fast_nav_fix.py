import os
import re

FILES = [
    'products/index.html',
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

MAPPING = [
    (r'href="[^"]*?(?:logo|brand|Home|首页)[^"]*?"', 'href="/index.html"'), # Catch-all for home/logo links
    (r'href="[^"]*?#markets"', 'href="/index.html#markets"'),
    (r'href="[^"]*?#solutions"', 'href="/index.html#solutions"'),
    (r'href="[^"]*?#products"', 'href="/index.html#products"'),
    (r'href="[^"]*?#technology"', 'href="/index.html#technology"'),
    (r'href="[^"]*?#services?"', 'href="/index.html#services"'),
    (r'href="[^"]*?#contact"', 'href="/index.html#contact"'),
    (r'href="[^"]*?#inquiry"', 'href="/index.html#contact"'),
]

def fast_fix(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, fix the logo specifically
    content = re.sub(r'href="[^"]*?index\.html"(?=[^>]*?(?:logo|brand))', 'href="/index.html"', content)
    
    # 2. Fix known anchor patterns
    content = re.sub(r'href="[^"]*?#markets"', 'href="/index.html#markets"', content)
    content = re.sub(r'href="[^"]*?#solutions"', 'href="/index.html#solutions"', content)
    content = re.sub(r'href="[^"]*?#products"', 'href="/index.html#products"', content)
    content = re.sub(r'href="[^"]*?#technology"', 'href="/index.html#technology"', content)
    content = re.sub(r'href="[^"]*?#services?"', 'href="/index.html#services"', content)
    content = re.sub(r'href="[^"]*?#contact"', 'href="/index.html#contact"', content)
    content = re.sub(r'href="[^"]*?#inquiry"', 'href="/index.html#contact"', content)

    # 3. Handle simple root links that should be physical filenames for stability
    content = re.sub(r'href="/"(?=[^>]*?(?:Home|首页))', 'href="/index.html"', content)

    # 4. Final Cleanup of any potential corrupted hrefs like href="href=..."
    content = re.sub(r'href="href="([^"]+)"\s*"', r'href="\1"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for f in FILES:
        fast_fix(f)
