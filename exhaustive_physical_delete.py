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

# Keywords that should trigger deletion of the entire <p> tag
KEYWORDS = [
    '将手册中的核心技术提炼为采购方可理解的',
    '将手册中的 AI 算法',
    '这里不再放整张手册截图',
    '参数由手册表格整理为网页原生表格',
    '将手册中的售前、售中、售后服务内容整理为网页模块'
]

def purify_page_exhaustive(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Broad regex to find <p ...> ... </p> and check if any keyword is inside
    p_tag_pattern = r'<p[^>]*?>.*?</p>'
    
    def check_and_delete(match):
        tag_content = match.group(0)
        for kw in KEYWORDS:
            if kw in tag_content:
                print(f"Deleting tag containing: {kw}")
                return '' # Remove the tag
        return tag_content # Keep the tag

    new_content = re.sub(p_tag_pattern, check_and_delete, content, flags=re.DOTALL)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"PHYSICALLY DELETED manual descriptions in: {file_path}")
    else:
        print(f"Confirmed clean: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        purify_page_exhaustive(f)
