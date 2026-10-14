import os, json, time, shutil, hashlib
from concurrent.futures import ThreadPoolExecutor

_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patchserver.json")
if os.path.isfile(_cfg):
    with open(_cfg, "r", encoding="utf-8-sig") as _fh:
        _d = json.load(_fh)
    GAME = _d["game_dir"]
    FILES = os.path.join(_d["patch_dir"], "files")
    LIST = os.path.join(_d["patch_dir"], "patchlist.json")
    CACHE = os.path.join(_d["patch_dir"], "hashcache_py.json")
    BASE = _d["base_url"] + "/update/files/"
else:
    raise SystemExit("patchserver.json bulunamadi - once setup.cmd calistir")

EXCLUDE_DIRS = {"userdata", "logs", "upload", "syserr", "screenshot"}
EXCLUDE_FILES = {"metin2.cfg", "mouse.cfg"}
INCLUDE_USERDATA = {"lang.cfg", "loca.cfg"}

def load_cache():
    if os.path.isfile(CACHE):
        try:
            with open(CACHE, "r", encoding="utf-8-sig") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {}

def save_cache(c):
    try:
        tmp = CACHE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(c, fh)
        os.replace(tmp, CACHE)
    except Exception:
        pass

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

def _hash_one(args):
    rel, cache = args
    p = os.path.join(FILES, rel.replace("/", os.sep))
    st = os.stat(p)
    key = "%s|%d|%d" % (rel, st.st_size, int(st.st_mtime * 1000))
    if key in cache:
        return rel, st.st_size, cache[key], key
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    digest = h.hexdigest()
    return rel, st.st_size, digest, key

def rebuild(files):
    cache = load_cache()
    new_cache = {}
    entries = []
    workers = max(4, os.cpu_count() or 8)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for rel, size, digest, key in ex.map(_hash_one, [(r, cache) for r in sorted(files)]):
            new_cache[key] = digest
            entries.append({"path": rel, "size": size, "sha256": digest})
    save_cache(new_cache)
    ver = 0
    if os.path.isfile(LIST):
        try:
            with open(LIST, "r", encoding="utf-8-sig") as fh:
                ver = int(json.load(fh).get("version", 0))
        except Exception:
            pass
    tmp = LIST + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"version": ver + 1, "base": BASE, "files": entries}, fh, indent=4)
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
    time.sleep(2)
    cur = snapshot()
    if cur != last:
        time.sleep(2)
        cur = snapshot()
        sync()
        last = cur
