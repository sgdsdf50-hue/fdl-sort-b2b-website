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

# Keywords that are definitely present but might be interrupted by <br> or spaces
TARGETS = [
    '将手册中的',
    '不再放整张手册截图',
    '手册表格整理为网页原生表格',
    '售后服务内容整理为网页模块'
]

def surgical_purify(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <p> tags
    p_tags = re.findall(r'<p[^>]*?>.*?</p>', content, flags=re.DOTALL)
    
    tags_to_delete = []
    for tag in p_tags:
        for target in TARGETS:
            if target in tag:
                tags_to_delete.append(tag)
                break

    if tags_to_delete:
        new_content = content
        for tag in tags_to_delete:
            new_content = new_content.replace(tag, '')
            print(f"DELETED tag containing keyword: {target}")
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"PHYSICALLY CLEANED: {file_path}")
    else:
        print(f"File is already clean or targets missing: {file_path}")

if __name__ == "__main__":
    for f in FILES:
        surgical_purify(f)
