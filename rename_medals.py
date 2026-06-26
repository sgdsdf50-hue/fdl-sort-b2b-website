import os
import shutil

medals_dir = "assets/img/about/medals"
source_dir = os.path.join(medals_dir, "处理过的奖牌图片")

if os.path.exists(source_dir):
    # 1. Get all files in the source directory
    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.png')]
    # Sort files to ensure stable naming sequence
    files.sort()
    
    # 2. Clear old files in medals_dir (JPGs and other older medals)
    for item in os.listdir(medals_dir):
        item_path = os.path.join(medals_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            
    # 3. Rename and move files
    for idx, f in enumerate(files, 1):
        src_path = os.path.join(source_dir, f)
        dest_path = os.path.join(medals_dir, f"medal-{idx}.png")
        shutil.copy2(src_path, dest_path)
        print(f"Standardized: {f} -> medal-{idx}.png")
        
    # 4. Clean up source directory
    shutil.rmtree(source_dir)
    print("Cleaned up temporary source directory successfully.")
else:
    print("Source directory for processed images not found. Checking if already done.")
