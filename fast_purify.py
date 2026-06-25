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

# Precise keywords to identify tags for physical removal
KEYWORDS = [
    '将手册中的核心技术提炼为采购方可理解的',
    '将手册中的 AI 算法',
    '这里不再放整张手册截图',
    '参数由手册表格整理为网页原生表格',
    '将手册中的售前、售中、售后服务内容整理为网页模块'
]

def physical_purify(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Broad regex to find <p ...> ... </p> and check if keywords are inside
    # This correctly handles tags placed at the end of a line or multiline tags
    p_tag_pattern = r'<p[^>]*?>.*?</p>'
    
    def replacement_logic(match):
        tag_full = match.group(0)
        for kw in KEYWORDS:
            if kw in tag_full:
                print(f"Match found in {file_path}, keyword: {kw}. DELETING TAG.")
                return '' # Remove the tag
        return tag_full # Keep the tag

    new_content = re.sub(p_tag_pattern, replacement_logic, content, flags=re.DOTALL)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully purified: {file_path}")
    else:
        print(f"No match found in: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        physical_purify(f)
