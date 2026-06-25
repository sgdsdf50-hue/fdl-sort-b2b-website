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

# Redirect logic
fail_safe_script = """
  <script>
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (link) {
        const href = link.getAttribute('href');
        if (href && href.includes('index.html#')) {
          const anchor = href.split('#')[1];
          e.preventDefault();
          window.location.href = '/index.html#' + anchor;
        }
      }
    });
  </script>
"""

def repair_content(content, is_subpage):
    # 1. Clean up existing corrupted scripts
    content = re.sub(r'<script>.*?window\.location\.href\s*=\s*href.*?</script>', '', content, flags=re.DOTALL)
    
    # 2. Inject script if subpage
    if is_subpage and '</head>' in content:
        content = content.replace('</head>', fail_safe_script + '</head>')

    # 3. Aggressive cleanup of all corrupted href patterns and standardization
    # Matches: href="href="/index.html"" or href="/index.html#..." or href="../../index.html#..."
    
    # Standardize Home
    content = re.sub(r'href=["\s]*([^"]*index\.html|/|#top)["\s]*', 'href="/index.html"', content)
    
    # Standardize Anchors
    anchors = ['markets', 'solutions', 'products', 'technology', 'services', 'contact']
    for anchor in anchors:
        pattern = r'href=["\s]*[^"]*#' + anchor + r'["\s]*'
        content = re.sub(pattern, f'href="/index.html#{anchor}"', content)
        
    # Standardize Equipment Center return button
    content = re.sub(r'href=["\s]*[^"]*products/index\.html["\s]*', 'href="/products/index.html"', content)

    return content

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    is_subpage = (file_path != 'index.html')
    new_content = repair_content(content, is_subpage)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Repaired and standardizing navigation in: {file_path}")
