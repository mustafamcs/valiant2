import os, re
root = r'C:\Users\Administrator\Desktop\VALIANT2\assets\unpacked\data'

# Pack visual dirs
visual_dirs = [
    'effect', 'patch_effect', 'patch_effect2', 'patch_effect3', 'patch_effect4',
    'patch_effect5', 'patch_effect6', 'pc', 'patch_pc', 'patch_pc_2', 'patch_pc_3',
    'patch_pc_4', 'patch_pc_5', 'patch_pc_6', 'pc2', 'patch_pc2', 'patch_pc2_2',
    'item', 'patch_item', 'patch_item2', 'monster', 'monster2', 'patch_monster2',
    'npc', 'npc2', 'patch_npc', 'zone', 'patch_zone', 'patch_zone2', 'patch_zone3',
    'patch_zone4', 'tree', 'terrain', 'environment', 'textureset', 'icon',
    'locale', 'patch', 'patch2', 'patch3', 'patch4', 'map', 'config', 'root',
]

def exists_anywhere(rel):
    for vd in visual_dirs:
        if os.path.exists(os.path.join(root, vd, rel)):
            return True
    return False

missing = {}
for dp, _, fns in os.walk(root):
    for fn in fns:
        if not fn.lower().endswith(('.mse', '.msm')):
            continue
        fp = os.path.join(dp, fn)
        mse_dir = os.path.dirname(fp)
        try:
            txt = open(fp, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for m in re.finditer(r'(?:TextureFile|DiffuseTextureFile|SourceTextureFileName)\s+"([^"\r\n]+\.(?:dds|tga|jpg|png))"', txt, re.I):
            tex = m.group(1).replace('\\', '/').strip().lstrip('/').lower()
            if tex.startswith('d:/ymir work/'):
                rel = tex.replace('d:/ymir work/', '')
                # try as-is under each pack root
                if exists_anywhere(rel):
                    continue
            else:
                # relative to mse dir
                if os.path.exists(os.path.join(mse_dir, tex)):
                    continue
                # also try anywhere
                rel = tex
                if exists_anywhere(rel):
                    continue
            missing.setdefault(tex, fp)
print('missing:', len(missing))
for tex, src in sorted(missing.items())[:100]:
    print('MISSING:', tex, '<-', src.replace(root, '')[:90])
