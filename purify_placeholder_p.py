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

keywords = [
    '参数由手册表格整理',
    '以下数据用于二级页面展示',
    '将手册中的 AI 算法',
    '将手册中的售前、售中、售后',
    '这里不再放整张手册截图',
    '手册中的核心技术、应用案例与服务支持已作为各产品页面内容来源'
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    initial_content = content
    for kw in keywords:
        # Regex to find <p> tags containing the keyword
        # Matches <p ...> ... keyword ... </p> (including multiline)
        pattern = r'<p[^>]*?>.*?' + re.escape(kw) + r'.*?</p>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if content != initial_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Purified: {file_path}")
    else:
        print(f"No changes needed: {file_path}")
