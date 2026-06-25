import os
import re

files = [
    'products/ai-optical-sorter/index.html',
    'products/film-flexible-sorter/index.html',
    'products/hyperspectral-material-sorter/index.html',
    'products/parallel-robot-sorter/index.html',
    'products/solid-waste-line/index.html',
    'products/textile-sorter/index.html'
]

# Specific phrases to target within <p> tags
targets = [
    '参数由手册表格整理为网页原生表格',
    '以下数据用于二级页面展示',
    '将手册中的 AI 算法、视觉识别',
    '将手册中的售前、售中、售后服务内容整理为网页模块'
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find <p> tags containing any of the target phrases
    for target in targets:
        # Matches <p ...>...</p> where the inner content or attributes contain the target string
        # Non-greedy .*? and re.DOTALL to handle multiline tags
        pattern = r'<p[^>]*?>.*?' + re.escape(target) + r'.*?</p>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Purified {file_path}")
