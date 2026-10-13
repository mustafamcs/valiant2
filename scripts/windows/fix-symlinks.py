"""Fix broken symlink-as-text-file references in assets/unpacked/data.

Git on Windows turns Linux symlinks into plain text files containing the
target path.  This script finds those tiny image files and replaces them
with the actual target content so FSArchiver packs real textures.
"""
import os, shutil, sys

root = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'assets', 'unpacked', 'data')
IMAGE_EXTS = {'.tga', '.dds', '.jpg', '.jpeg', '.png', '.bmp'}
fixed = 0
missing = 0

for dirpath, _dirs, filenames in os.walk(root):
    for fn in filenames:
        ext = os.path.splitext(fn)[1].lower()
        if ext not in IMAGE_EXTS:
            continue
        fpath = os.path.join(dirpath, fn)
        try:
            sz = os.path.getsize(fpath)
            if sz > 500:
                continue
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            if not (content.startswith('C:/') or content.startswith('../')
                    or content.startswith('./')):
                continue
            if content.startswith('C:/'):
                target_abs = content.replace('/', os.sep)
            else:
                target_abs = os.path.normpath(os.path.join(dirpath, content))
            if os.path.isfile(target_abs) and os.path.getsize(target_abs) > 100:
                shutil.copy2(target_abs, fpath)
                fixed += 1
            else:
                print(f"MISSING TARGET: {fpath} -> {content}")
                missing += 1
        except Exception:
            continue

print(f"Symlink fix: {fixed} fixed, {missing} missing targets")
