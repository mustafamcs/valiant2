import os, json, time, shutil, hashlib

# Ayarlar script'in yanindaki patchserver.json'dan okunur (setup.ps1 uretir).
_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patchserver.json")
if os.path.isfile(_cfg):
    _d = json.load(open(_cfg))
    GAME = _d["game_dir"]
    FILES = os.path.join(_d["patch_dir"], "files")
    LIST = os.path.join(_d["patch_dir"], "patchlist.json")
    BASE = _d["base_url"] + "/update/files/"
else:
    raise SystemExit("patchserver.json bulunamadi - once setup.cmd calistir")

EXCLUDE_DIRS = {"userdata", "logs", "upload", "syserr", "screenshot"}
EXCLUDE_FILES = {"metin2.cfg", "mouse.cfg"}
INCLUDE_USERDATA = {"lang.cfg", "loca.cfg"}

def snapshot():
    out = {}
    for dp, dn, fn in os.walk(GAME):
        rel_dir = os.path.relpath(dp, GAME).replace("\\", "/")
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, GAME).replace("\\", "/")
            low = rel.lower()
            parts = low.split("/")
            if parts[0] in EXCLUDE_DIRS and not (parts[0] == "userdata" and parts[-1] in INCLUDE_USERDATA):
                continue
            if rel_dir == "." and f.lower() in EXCLUDE_FILES:
                continue
            try:
                st = os.stat(p)
            except OSError:
                continue
            out[rel] = (st.st_size, st.st_mtime)
    return out

def rebuild(files):
    entries = []
    for rel in sorted(files):
        p = os.path.join(FILES, rel.replace("/", os.sep))
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        entries.append({"path": rel, "size": os.path.getsize(p), "sha256": h.hexdigest()})
    ver = 0
    if os.path.isfile(LIST):
        try:
            ver = int(json.load(open(LIST)).get("version", 0))
        except Exception:
            pass
    tmp = LIST + ".tmp"
    json.dump({"version": ver + 1, "base": BASE, "files": entries},
              open(tmp, "w"), indent=4)
    os.replace(tmp, LIST)
    return ver + 1

def sync():
    snap = snapshot()
    changed = False
    for rel in snap:
        src = os.path.join(GAME, rel.replace("/", os.sep))
        dst = os.path.join(FILES, rel.replace("/", os.sep))
        if not os.path.isfile(dst) or os.path.getsize(dst) != snap[rel][0] \
           or abs(os.path.getmtime(dst) - snap[rel][1]) > 1:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            changed = True
    # deleted files
    for dp, dn, fn in os.walk(FILES):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, FILES).replace("\\", "/")
            if rel not in snap:
                try:
                    os.remove(p); changed = True
                except OSError:
                    pass
    if changed:
        v = rebuild(list(snap.keys()))
        print("manifest v%d yayinlandi (%d dosya)" % (v, len(snap)), flush=True)
    return snap

# Ilk acilista: patch deposu eksik/bosssa hemen senkronla (taze kurulum destegi)
last = snapshot()
_need = False
for rel in last:
    dst = os.path.join(FILES, rel.replace("/", os.sep))
    if not os.path.isfile(dst):
        _need = True
        break
if _need:
    sync()
    print("ilk senkron tamamlandi", flush=True)

while True:
    time.sleep(5)
    cur = snapshot()
    if cur != last:
        time.sleep(10)  # debounce
        cur = snapshot()
        sync()
        last = cur
