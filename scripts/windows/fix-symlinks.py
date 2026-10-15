"""Fix broken symlink-as-text-file references in assets/unpacked/data.

Git on Windows turns Linux symlinks into plain text files containing the
target path.  This script finds ALL such files (images, text, proto, etc.)
and replaces them with the actual target content.
"""
import os, shutil, sys

root = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'assets', 'unpacked', 'data')
fixed = 0
missing = 0

for dirpath, _dirs, filenames in os.walk(root):
    for fn in filenames:
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
                marker = '/assets/unpacked/data/'
                norm_c = content.replace('\\', '/')
                if marker in norm_c:
                    rel_part = norm_c.split(marker, 1)[1]
                    target_abs = os.path.normpath(os.path.join(root, rel_part.replace('/', os.sep)))
                else:
                    target_abs = content.replace('/', os.sep)
            else:
                target_abs = os.path.normpath(os.path.join(dirpath, content))
            if os.path.isfile(target_abs) and os.path.getsize(target_abs) > 10:
                shutil.copy2(target_abs, fpath)
                fixed += 1
            else:
                print(f"MISSING TARGET: {fpath} -> {content}")
                missing += 1
        except Exception:
            continue

print(f"Symlink fix: {fixed} fixed, {missing} missing targets")
