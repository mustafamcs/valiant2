import os, re
root = r'C:\Users\Administrator\Desktop\VALIANT2\assets\unpacked\data'

visual_dirs = [
    'effect', 'patch_effect', 'patch_effect2', 'patch_effect3', 'patch_effect4',
    'patch_effect5', 'patch_effect6', 'pc', 'patch_pc', 'patch_pc_2', 'patch_pc_3',
    'patch_pc_4', 'patch_pc_5', 'patch_pc_6', 'pc2', 'patch_pc2', 'patch_pc2_2',
    'item', 'patch_item', 'patch_item2', 'monster', 'monster2', 'patch_monster2',
    'npc', 'npc2', 'patch_npc', 'zone', 'patch_zone', 'patch_zone2', 'patch_zone3',
    'patch_zone4', 'tree', 'terrain', 'environment', 'textureset', 'icon',
    'locale', 'patch', 'patch2', 'patch3', 'patch4', 'map', 'config', 'root',
]

# map visual_dir -> pack-root relative prefix
prefix = {
    'effect': 'effect', 'pc': 'pc', 'pc2': 'pc2', 'item': 'item',
    'monster': 'monster', 'monster2': 'monster2', 'npc': 'npc', 'npc2': 'npc2',
    'zone': 'zone', 'tree': 'tree', 'terrain': 'terrainmaps',
    'environment': 'environment', 'textureset': 'textureset', 'icon': 'icon',
    'locale': 'locale',
}

def exists_pack(virtual_path):
    # virtual_path like d:/ymir work/<vd>/sub/file.dds
    p = virtual_path.replace('d:/ymir work/', '')
    top = p.split('/')[0]
    for vd in visual_dirs:
        vd_prefix = prefix.get(vd, vd)
        if top == vd_prefix:
            # file under that pack root: strip prefix
            sub = p[len(vd_prefix):].lstrip('/')
            if os.path.exists(os.path.join(root, vd, sub)):
                return True
        # patch2/3/4 map to d:/ymir work/ directly
        if vd in ('patch2', 'patch3', 'patch4') and os.path.exists(os.path.join(root, vd, p)):
            return True
    return False

missing = {}
str_re = re.compile(rb'([ -~]{4,}?\.(?:dds|tga|jpg|png|bmp))', re.I)
for dp, _, fns in os.walk(root):
    for fn in fns:
        if not fn.lower().endswith(('.gr2', '.mde', '.msa')):
            continue
        fp = os.path.join(dp, fn)
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        for m in str_re.finditer(data):
            tex = m.group(1).decode('latin1').replace('\\', '/').strip().lstrip('/').lower()
            # keep only plausible texture paths
            if ' ' == tex[0] or len(tex) < 6:
                continue
            if tex.startswith('d:/ymir work/'):
                if exists_pack(tex):
                    continue
            else:
                # relative to model dir
                if os.path.exists(os.path.join(dp, tex)):
                    continue
                continue  # skip relative not-found to avoid noise
            missing.setdefault(tex, fp)
print('missing:', len(missing))
for tex, src in sorted(missing.items()):
    print('MISSING:', tex, '<-', src.replace(root, '')[:90])
